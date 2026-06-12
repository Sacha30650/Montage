#!/usr/bin/env python3
"""Audit HyperFrames timelines and long-form pacing density."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

from recent_pilots import RECENT_ORDER


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATHS = [ROOT / "index.html", *[ROOT / "pilots" / slug / "index.html" for slug in RECENT_ORDER]]
EXCLUDED_DIRS = {".git", ".agents", "node_modules", "out", "renders", "dist", "deliverables-v3", "tests"}
EPSILON = 0.00001


@dataclass
class Clip:
    tag: str
    attrs: dict[str, str]
    line: int

    @property
    def id(self) -> str:
        return self.attrs.get("id", f"{self.tag}@{self.line}")

    @property
    def class_names(self) -> set[str]:
        return set(self.attrs.get("class", "").split())

    @property
    def src(self) -> str:
        return self.attrs.get("src", "")

    @property
    def track(self) -> int | None:
        value = self.attrs.get("data-track-index")
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    @property
    def start(self) -> float | None:
        return parse_float(self.attrs.get("data-start"))

    @property
    def duration(self) -> float | None:
        return parse_float(self.attrs.get("data-duration"))

    @property
    def end(self) -> float | None:
        if self.start is None or self.duration is None:
            return None
        return self.start + self.duration


class TimelineParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.clips: list[Clip] = []
        self.composition_duration: float | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        if attr_map.get("data-composition-id") and "data-duration" in attr_map and self.composition_duration is None:
            self.composition_duration = parse_float(attr_map.get("data-duration"))
        if "data-start" in attr_map or "data-duration" in attr_map or "data-track-index" in attr_map:
            self.clips.append(Clip(tag=tag, attrs=attr_map, line=self.getpos()[0]))


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def discover_all_html() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*.html"):
        if any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        paths.append(path)
    return sorted(paths)


def ffprobe_duration(src: str) -> float | None:
    path = ROOT / src
    if not path.exists():
        return None
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return parse_float(result.stdout.strip())


def audit_file(path: Path) -> tuple[list[str], list[str], str]:
    html_text = path.read_text()
    parser = TimelineParser()
    parser.feed(html_text)
    no_music_allowed = "no-music-bed" in html_text
    errors: list[str] = []
    warnings: list[str] = []

    clips = [clip for clip in parser.clips if clip.track is not None]
    for clip in clips:
        if "clip" not in clip.class_names:
            errors.append(f"{path}:{clip.line} timed element `{clip.id}` is missing class=\"clip\"")
        if clip.start is None:
            errors.append(f"{path}:{clip.line} `{clip.id}` has non-numeric data-start")
        if clip.duration is None:
            errors.append(f"{path}:{clip.line} `{clip.id}` has non-numeric data-duration")

    by_track: dict[int, list[Clip]] = {}
    for clip in clips:
        if clip.start is None or clip.end is None or clip.track is None:
            continue
        by_track.setdefault(clip.track, []).append(clip)

    for track, track_clips in sorted(by_track.items()):
        ordered = sorted(track_clips, key=lambda clip: (clip.start or 0, clip.end or 0))
        for previous, current in zip(ordered, ordered[1:]):
            if previous.end is not None and current.start is not None and previous.end > current.start + EPSILON:
                errors.append(
                    f"{path}:{current.line} track {track} overlap: `{previous.id}` ends at "
                    f"{previous.end:.6f}s, `{current.id}` starts at {current.start:.6f}s"
                )

    duration = parser.composition_duration or max((clip.end or 0 for clip in clips), default=0)
    image_clips = [clip for clip in clips if clip.tag == "img"]
    caption_clips = [clip for clip in clips if "caption" in clip.class_names]
    audio_clips = [clip for clip in clips if clip.tag == "audio"]
    music_clips = [
        clip
        for clip in audio_clips
        if clip.id == "music" or ("music" in clip.src and "voiceover" not in clip.src)
    ]
    sfx_clips = [clip for clip in audio_clips if "/sfx/" in clip.src]
    max_image_duration = max((clip.duration or 0 for clip in image_clips), default=0)
    cuts_per_min = len(image_clips) / duration * 60 if duration else 0
    captions_per_min = len(caption_clips) / duration * 60 if duration else 0

    voiceover = next((clip for clip in audio_clips if clip.id == "voiceover" or "voiceover" in clip.src), None)
    vo_note = "vo=?"
    if voiceover:
        actual_vo = ffprobe_duration(voiceover.src)
        if actual_vo is not None:
            vo_note = f"vo={actual_vo:.1f}s"
            if duration and abs(actual_vo - duration) > 3.0:
                warnings.append(
                    f"{path}: voiceover duration {actual_vo:.2f}s differs from composition {duration:.2f}s by >3s"
                )

    if duration >= 60:
        if len(image_clips) < 14 or cuts_per_min < 12:
            errors.append(f"{path}: long video needs >=12 image cuts/min, found {cuts_per_min:.1f}/min")
        if len(caption_clips) < 18 or captions_per_min < 16:
            errors.append(f"{path}: long video needs frequent captions, found {captions_per_min:.1f}/min")
        if max_image_duration > 4.2:
            errors.append(f"{path}: image hold too long ({max_image_duration:.2f}s > 4.2s)")
        if not music_clips and not no_music_allowed:
            errors.append(f"{path}: long video has no music bed")
        if len(sfx_clips) < 6:
            warnings.append(f"{path}: fewer than 6 SFX clips on a long video")

    summary = (
        f"{path.relative_to(ROOT)}: duration={duration:.1f}s cuts={len(image_clips)} "
        f"({cuts_per_min:.1f}/min) captions={len(caption_clips)} ({captions_per_min:.1f}/min) "
        f"sfx={len(sfx_clips)} music={len(music_clips)} max_hold={max_image_duration:.2f}s {vo_note}"
    )
    return errors, warnings, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="HTML files to audit")
    parser.add_argument("--all", action="store_true", help="Audit every composition HTML outside generated output dirs")
    args = parser.parse_args()

    if args.all:
        paths = discover_all_html()
    elif args.paths:
        paths = [ROOT / path for path in args.paths]
    else:
        paths = DEFAULT_PATHS

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for path in paths:
        if not path.exists():
            all_errors.append(f"{path}: file does not exist")
            continue
        errors, warnings, summary = audit_file(path)
        print(summary)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    for warning in all_warnings:
        print(f"WARN {warning}", file=sys.stderr)
    for error in all_errors:
        print(f"ERROR {error}", file=sys.stderr)

    if all_errors:
        print(f"timeline audit failed: {len(all_errors)} error(s), {len(all_warnings)} warning(s)", file=sys.stderr)
        return 1
    print(f"timeline audit passed: {len(paths)} file(s), {len(all_warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
