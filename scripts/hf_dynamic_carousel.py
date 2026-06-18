#!/usr/bin/env python3
"""Shared dynamic renderer for long carousel-to-video pilots."""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLIP_GAP = 0.006


@dataclass(frozen=True)
class Word:
    text: str
    start: float
    end: float


def sec(value: float) -> str:
    """Format seconds without float-tail values that can trip overlap linting."""
    value = 0 if abs(value) < 0.0005 else value
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return text or "0"


def safe_duration(duration: float) -> float:
    if duration <= CLIP_GAP * 2:
        return max(0.001, duration)
    return max(0.001, duration - CLIP_GAP)


def asset_exists(src: str) -> bool:
    return (ROOT / src).exists()


def read_words(alignment_path: Path) -> list[Word]:
    data = json.loads(alignment_path.read_text())
    chars = data["characters"]
    starts = data["character_start_times_seconds"]
    ends = data["character_end_times_seconds"]

    words: list[Word] = []
    i = 0
    while i < len(chars):
        while i < len(chars) and chars[i].isspace():
            i += 1
        if i >= len(chars):
            break
        first = i
        while i < len(chars) and not chars[i].isspace():
            i += 1
        text = "".join(chars[first:i]).strip()
        if text:
            words.append(Word(text=text, start=float(starts[first]), end=float(ends[i - 1])))
    return words


def caption_chunks(words: list[Word], total: float) -> list[dict[str, object]]:
    chunks: list[dict[str, object]] = []
    current: list[Word] = []

    def close() -> None:
        if not current:
            return
        text = " ".join(word.text for word in current)
        start = current[0].start
        end = min(total, current[-1].end + 0.16)
        chunks.append(
            {
                "text": text,
                "start": start,
                "duration": max(0.35, end - start),
                "hit": is_hit_caption(text, start, len(chunks)),
                "xxl": start < 4.8 or strong_caption(text),
            }
        )
        current.clear()

    for word in words:
        current.append(word)
        text = " ".join(item.text for item in current)
        span = current[-1].end - current[0].start
        hard_punct = bool(re.search(r'[.!?":]$', word.text))
        soft_punct = bool(re.search(r"[,;]$", word.text))
        too_long = len(text) >= 34
        too_many = len(current) >= 5
        too_slow = span >= 2.45
        if too_long or too_many or too_slow or (hard_punct and span >= 0.55) or (soft_punct and span >= 1.25):
            close()

    close()

    for idx, chunk in enumerate(chunks[:-1]):
        next_start = float(chunks[idx + 1]["start"])
        max_duration = next_start - float(chunk["start"]) - 0.025
        chunk["duration"] = max(0.25, min(float(chunk["duration"]), max_duration))
    return chunks


def strong_caption(text: str) -> bool:
    lowered = text.lower()
    strong_words = (
        "vraie",
        "science",
        "erreur",
        "non",
        "interdit",
        "fausses",
        "retard",
        "retard.",
        "peur",
        "pression",
        "sauvegarde",
    )
    return any(word in lowered for word in strong_words) or bool(re.search(r"\d", text))


def is_hit_caption(text: str, start: float, index: int) -> bool:
    return start < 5.0 or strong_caption(text) or index % 5 == 0


def build_image_cuts(slides: list[tuple[str, float, float]], total: float) -> list[dict[str, object]]:
    cuts: list[dict[str, object]] = []
    directions = ["in", "right", "out", "left", "in-fast", "out"]
    pattern = [2.35, 2.75, 3.15, 2.25, 3.4]

    for slide_idx, (filename, start, duration) in enumerate(slides):
        slide_end = min(total, start + duration)
        cursor = start
        part = 0
        while cursor < slide_end - 0.08:
            remaining = slide_end - cursor
            target = pattern[(len(cuts) + part) % len(pattern)]
            if remaining <= target + 1.05:
                end = slide_end
            else:
                end = cursor + target
            cuts.append(
                {
                    "filename": filename,
                    "start": cursor,
                    "duration": end - cursor,
                    "direction": "stutter" if not cuts else directions[len(cuts) % len(directions)],
                    "slide": slide_idx,
                }
            )
            cursor = end
            part += 1
    return cuts


def main_times(slides: list[tuple[str, float, float]], total: float) -> dict[str, list[float]]:
    transitions = [round(start, 3) for _, start, _ in slides[1:]]
    beats = [0.0]
    beats.extend(transitions[1::2])
    if transitions:
        beats.append(transitions[-1])
    beats = sorted({time for time in beats if time < total - 0.2})

    whooshes = sorted(
        {
            *transitions,
            *[round(time + 0.18, 3) for time in beats if time > 0.1],
        }
    )
    whooshes = [time for time in whooshes if time < total - 0.2]
    return {"beats": beats, "whooshes": whooshes}


def image_tween(element_id: str, start: float, duration: float, direction: str, is_bg: bool = False) -> str:
    duration_text = sec(safe_duration(duration))
    start_text = sec(start)
    if direction == "stutter" and not is_bg:
        return f"""
      tl.fromTo("#{element_id}", {{ scale: 1.00 }}, {{ scale: 1.18, duration: 0.07, ease: "power3.out" }}, {start_text});
      tl.to("#{element_id}", {{ scale: 1.02, duration: 0.07, ease: "power3.in" }}, {sec(start + 0.07)});
      tl.to("#{element_id}", {{ scale: 1.15, duration: 0.07, ease: "power3.out" }}, {sec(start + 0.14)});
      tl.to("#{element_id}", {{ scale: 1.00, duration: 0.28, ease: "power2.out" }}, {sec(start + 0.22)});
      tl.to("#{element_id}", {{ scale: 1.08, duration: {sec(max(0.25, duration - 0.51))}, ease: "none" }}, {sec(start + 0.51)});"""
    if direction == "right":
        return f'      tl.fromTo("#{element_id}", {{ scale: 1.08, x: -34 }}, {{ scale: 1.13, x: 34, duration: {duration_text}, ease: "none" }}, {start_text});'
    if direction == "left":
        return f'      tl.fromTo("#{element_id}", {{ scale: 1.08, x: 34 }}, {{ scale: 1.13, x: -34, duration: {duration_text}, ease: "none" }}, {start_text});'
    if direction == "out":
        return f'      tl.fromTo("#{element_id}", {{ scale: 1.14 }}, {{ scale: 1.03, duration: {duration_text}, ease: "none" }}, {start_text});'
    if direction == "in-fast":
        return f'      tl.fromTo("#{element_id}", {{ scale: 1.00 }}, {{ scale: 1.16, duration: {duration_text}, ease: "none" }}, {start_text});'
    return f'      tl.fromTo("#{element_id}", {{ scale: 1.03 }}, {{ scale: 1.14, duration: {duration_text}, ease: "none" }}, {start_text});'


def caption_tween(element_id: str, start: float, hit: bool) -> str:
    ease = "back.out(3.4)" if hit else "back.out(2.6)"
    scale = "0.52" if hit else "0.72"
    return f'      tl.from("#{element_id}", {{ y: 46, scale: {scale}, opacity: 0, duration: 0.22, ease: "{ease}" }}, {sec(start)});'


def shake_tween(start: float) -> str:
    return f"""
      tl.to("#shake-wrap", {{ x: 8, y: -5, duration: 0.04, ease: "none" }}, {sec(start)});
      tl.to("#shake-wrap", {{ x: -7, y: 4, duration: 0.04, ease: "none" }}, {sec(start + 0.04)});
      tl.to("#shake-wrap", {{ x: 5, y: -3, duration: 0.04, ease: "none" }}, {sec(start + 0.08)});
      tl.to("#shake-wrap", {{ x: 0, y: 0, duration: 0.06, ease: "power2.out" }}, {sec(start + 0.12)});"""


def resolve_slides(config: dict[str, object]) -> tuple[list[tuple[str, float, float]], str, bool]:
    """Prefer full-bleed Higgsfield b-roll when every file exists; else legacy carousel slides.

    Returns (slides, broll_dir, full_bleed).
    """
    asset = str(config["asset_prefix"])
    hf_slides = config.get("hf_slides")
    hf_dir = str(config.get("hf_broll_dir", "broll-hf"))
    if hf_slides:
        missing = [name for name, _, _ in hf_slides if not asset_exists(f"{asset}/{hf_dir}/{name}")]
        if not missing:
            return list(hf_slides), hf_dir, True
        print(f"[hf_dynamic_carousel] {config['slug']}: missing {len(missing)} Higgsfield asset(s) "
              f"in {hf_dir} ({', '.join(missing[:3])}…) — falling back to legacy slides")
    return list(config["slides"]), "broll", False  # type: ignore[arg-type]


def render_html(config: dict[str, object]) -> str:
    slug = str(config["slug"])
    total = float(config["total_dur"])
    asset = str(config["asset_prefix"])
    slides, broll_dir, full_bleed = resolve_slides(config)
    slide_height = int(config.get("slide_height", 1335))
    slide_top = int(config.get("slide_top", 292))
    pilot_dir = ROOT / "pilots" / slug

    words = read_words(pilot_dir / "assets/audio/alignment-marie.json")
    captions = caption_chunks(words, total)
    cuts = build_image_cuts(slides, total)
    times = main_times(slides, total)

    img_html: list[str] = []
    anim_lines: list[str] = []
    for idx, cut in enumerate(cuts):
        start = float(cut["start"])
        duration = float(cut["duration"])
        duration_attr = sec(safe_duration(duration))
        filename = str(cut["filename"])
        src = f"{asset}/{broll_dir}/{filename}"
        bg_id = f"bg-{idx}"
        fg_id = f"fg-{idx}"
        if not full_bleed:
            img_html.append(
                f'      <div id="{bg_id}" class="clip bg-blur" data-start="{sec(start)}" '
                f'data-duration="{duration_attr}" data-track-index="0" style="background-image:url(&quot;{src}&quot;)"></div>'
            )
            anim_lines.append(image_tween(bg_id, start, duration, str(cut["direction"]), is_bg=True))
        img_html.append(
            f'      <img id="{fg_id}" class="clip slide-fg" data-start="{sec(start)}" '
            f'data-duration="{duration_attr}" data-track-index="1" src="{src}" />'
        )
        anim_lines.append(image_tween(fg_id, start, duration, str(cut["direction"])))

    caption_html: list[str] = []
    caption_anim: list[str] = []
    for idx, item in enumerate(captions):
        text = html.escape(str(item["text"]))
        start = float(item["start"])
        duration = float(item["duration"])
        hit = bool(item["hit"])
        xxl = bool(item["xxl"])
        cid = f"cap-{idx}"
        classes = ["clip", "caption"]
        if hit:
            classes.append("is-hit")
        if xxl:
            classes.append("is-xxl")
        caption_html.append(
            f'      <div id="{cid}" class="{" ".join(classes)}" data-start="{sec(start)}" '
            f'data-duration="{sec(safe_duration(duration))}" data-track-index="3"><span>{text}</span></div>'
        )
        caption_anim.append(caption_tween(cid, start, hit))

    flash_html: list[str] = []
    flash_anim: list[str] = []
    for idx, start in enumerate(times["beats"]):
        fid = f"flash-{idx}"
        flash_html.append(
            f'      <div id="{fid}" class="clip flash" data-start="{sec(start)}" data-duration="0.11" data-track-index="6"></div>'
        )
        flash_anim.append(
            f'      tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: 0.85, duration: 0.03, ease: "none" }}, {sec(start)});\n'
            f'      tl.to("#{fid}", {{ opacity: 0, duration: 0.08, ease: "power1.out" }}, {sec(start + 0.03)});'
        )

    whoosh_html = []
    for idx, start in enumerate(times["whooshes"][:14]):
        whoosh_html.append(
            f'      <audio id="wh-{idx}" class="clip" data-start="{sec(start)}" data-duration="0.55" '
            f'data-track-index="{11 + idx}" data-volume="0.42" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        )

    bass_html = []
    for idx, start in enumerate(times["beats"][:8]):
        bass_html.append(
            f'      <audio id="bd-{idx}" class="clip" data-start="{sec(start)}" data-duration="0.55" '
            f'data-track-index="{30 + idx}" data-volume="0.52" src="{asset}/audio/sfx/bass-drop.mp3"></audio>'
        )

    music_src = str(config.get("music_src", "assets/audio/rasenfieber.mp3"))
    music_tag = "      <!-- no-music-bed: intentional voiceover-only render -->" if not music_src else ""
    if music_src and asset_exists(music_src):
        music_tag = (
            f'      <audio id="music" class="clip" data-start="0" data-duration="{sec(total)}" '
            f'data-track-index="9" data-volume="{config.get("music_volume", "0.08")}" src="{music_src}"></audio>'
        )

    shake_anim = "".join(shake_tween(time) for time in times["beats"][:8])

    if full_bleed:
        slide_css = """.slide-fg {
        position:absolute; left:0; top:0; width:1080px; height:1920px;
        object-fit:cover; transform-origin:center; z-index:1;
      }"""
        scrim_css = """.scrim {
        position:absolute; inset:0; z-index:2; pointer-events:none;
        background:
          radial-gradient(ellipse 140% 90% at 50% 38%, rgba(0,0,0,0) 52%, rgba(0,0,0,0.42) 100%),
          linear-gradient(180deg, rgba(0,0,0,0.34) 0%, rgba(0,0,0,0.04) 30%, rgba(0,0,0,0.10) 54%, rgba(0,0,0,0.50) 72%, rgba(0,0,0,0.80) 100%);
      }"""
    else:
        slide_css = f""".slide-fg {{
        position:absolute; left:0; right:0; width:1080px; height:{slide_height}px; top:{slide_top}px;
        object-fit:contain; transform-origin:center; z-index:1;
        filter: drop-shadow(0 26px 48px rgba(0,0,0,0.45));
      }}"""
        scrim_css = """.scrim {
        position:absolute; inset:0; z-index:2; pointer-events:none;
        background:linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.14) 34%, rgba(0,0,0,0.58) 56%, rgba(0,0,0,0.92) 100%);
      }"""

    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{
        width:1080px; height:1920px; overflow:hidden; background:#0b0b0b;
        font-family: Arial, system-ui, sans-serif;
      }}
      #shake-wrap {{ position:absolute; inset:0; }}
      .bg-blur {{
        position:absolute; inset:-70px; background-size:cover; background-position:center;
        filter: blur(44px) brightness(0.62) saturate(1.18); transform-origin:center; z-index:0;
      }}
      {slide_css}
      {scrim_css}
      .caption {{
        position:absolute; left:64px; right:64px; top:1248px; z-index:4;
        min-height:132px; display:flex; align-items:center; justify-content:center;
        text-align:center; color:#fff; font-weight:900; font-size:78px; line-height:1;
        letter-spacing:0; overflow-wrap:anywhere;
        text-shadow:
          4px 4px 0 #000, -4px -4px 0 #000, 4px -4px 0 #000, -4px 4px 0 #000,
          0 8px 26px rgba(0,0,0,0.88);
      }}
      .caption.is-xxl {{ font-size:104px; top:1192px; }}
      .caption span {{
        background:#000; padding:10px 20px 14px;
        box-decoration-break:clone; -webkit-box-decoration-break:clone;
      }}
      .caption.is-hit span {{
        color:#101010; background:#ffe600; padding:10px 22px 14px;
        box-decoration-break:clone; -webkit-box-decoration-break:clone;
        text-shadow:none;
      }}
      .flash {{
        position:absolute; inset:0; z-index:5; pointer-events:none;
        background:#ffe600; mix-blend-mode:screen;
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{sec(total)}" data-width="1080" data-height="1920">
      <div id="shake-wrap" data-layout-allow-overflow>
{chr(10).join(img_html)}
      <div id="scrim" class="clip scrim" data-start="0" data-duration="{sec(total)}" data-track-index="2"></div>
{chr(10).join(caption_html)}
{chr(10).join(flash_html)}
      </div>
      <audio id="voiceover" class="clip" data-start="0" data-duration="{sec(total)}" data-track-index="8" data-volume="1.0" src="{asset}/audio/voiceover.mp3"></audio>
{music_tag}
{chr(10).join(whoosh_html)}
{chr(10).join(bass_html)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(anim_lines)}
{chr(10).join(caption_anim)}
{chr(10).join(flash_anim)}
{shake_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def render_pilot(config: dict[str, object], write_root: bool = False) -> Path:
    slug = str(config["slug"])
    html_text = render_html(config)
    target = ROOT / "pilots" / slug / "index.html"
    target.write_text(html_text)
    if write_root:
        (ROOT / "index.html").write_text(html_text)
    return target


def copy_shared_music_to_pilot(config: dict[str, object]) -> None:
    music_src = str(config.get("music_src", "assets/audio/rasenfieber.mp3"))
    if not music_src or not asset_exists(music_src):
        return
    slug = str(config["slug"])
    destination = ROOT / "pilots" / slug / "assets/audio/music-bed.mp3"
    if not destination.exists():
        shutil.copyfile(ROOT / music_src, destination)
