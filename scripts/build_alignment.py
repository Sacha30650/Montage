#!/usr/bin/env python3
"""Build a character-level alignment JSON (ElevenLabs shape) for a voiceover.

The dynamic carousel template (hf_dynamic_carousel.read_words) consumes the
ElevenLabs `characters` / `character_*_times_seconds` shape. ElevenLabs returns
it for free with its TTS; for locally generated voiceovers (Kokoro) we
reconstruct it: transcribe with faster-whisper for word timings, then snap the
*ground-truth* script text onto those timings so captions never carry ASR
typos. Unmatched words get timings interpolated between matched neighbours.

Usage:
    python3 scripts/build_alignment.py <voiceover.(mp3|wav)> <script.txt> <out.json> [--model small]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import unicodedata
from pathlib import Path


def normalize(token: str) -> str:
    token = unicodedata.normalize("NFD", token.lower())
    token = "".join(ch for ch in token if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", token)


def transcribe_words(audio: Path, model_name: str) -> list[tuple[str, float, float]]:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio), language="fr", word_timestamps=True)
    words: list[tuple[str, float, float]] = []
    for segment in segments:
        for word in segment.words or []:
            text = word.word.strip()
            if text:
                words.append((text, float(word.start), float(word.end)))
    print(f"whisper({model_name}): {len(words)} words, audio={info.duration:.2f}s")
    return words


def align_truth_to_asr(
    truth: list[str], asr: list[tuple[str, float, float]]
) -> list[tuple[float, float] | None]:
    """Return per-truth-word (start, end) using SequenceMatcher on normalized words."""
    truth_norm = [normalize(word) for word in truth]
    asr_norm = [normalize(text) for text, _, _ in asr]
    timings: list[tuple[float, float] | None] = [None] * len(truth)
    matcher = difflib.SequenceMatcher(a=truth_norm, b=asr_norm, autojunk=False)
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            _, start, end = asr[block.b + offset]
            timings[block.a + offset] = (start, end)
    return timings


def fill_gaps(timings: list[tuple[float, float] | None], words: list[str], total: float) -> list[tuple[float, float]]:
    """Linearly interpolate timings for unmatched words, weighted by word length."""
    filled = list(timings)
    n = len(filled)
    index = 0
    while index < n:
        if filled[index] is not None:
            index += 1
            continue
        gap_start = index
        while index < n and filled[index] is None:
            index += 1
        gap_end = index  # exclusive
        left_time = filled[gap_start - 1][1] if gap_start > 0 else 0.0
        right_time = filled[gap_end][0] if gap_end < n else total
        span = max(0.05, right_time - left_time)
        weights = [max(1, len(words[i])) for i in range(gap_start, gap_end)]
        weight_total = sum(weights)
        cursor = left_time
        for slot, weight in zip(range(gap_start, gap_end), weights):
            duration = span * weight / weight_total
            filled[slot] = (cursor, cursor + duration)
            cursor += duration
    # enforce monotonicity
    last_end = 0.0
    result: list[tuple[float, float]] = []
    for start, end in filled:  # type: ignore[misc]
        start = max(start, last_end)
        end = max(end, start + 0.02)
        result.append((round(start, 3), round(end, 3)))
        last_end = end
    return result


def build_char_alignment(text: str, words: list[str], timings: list[tuple[float, float]]) -> dict[str, list]:
    characters: list[str] = []
    starts: list[float] = []
    ends: list[float] = []

    def push(chars: str, start: float, end: float) -> None:
        if not chars:
            return
        step = (end - start) / len(chars)
        for offset, char in enumerate(chars):
            characters.append(char)
            starts.append(round(start + offset * step, 3))
            ends.append(round(start + (offset + 1) * step, 3))

    cursor = 0
    previous_end = 0.0
    for word, (start, end) in zip(words, timings):
        position = text.index(word, cursor)
        push(text[cursor:position], previous_end, start)  # whitespace/punctuation between words
        push(word, start, end)
        cursor = position + len(word)
        previous_end = end
    push(text[cursor:], previous_end, previous_end + 0.05)
    return {
        "characters": characters,
        "character_start_times_seconds": starts,
        "character_end_times_seconds": ends,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audio")
    parser.add_argument("script_txt")
    parser.add_argument("out_json")
    parser.add_argument("--model", default="small")
    args = parser.parse_args()

    text = Path(args.script_txt).read_text(encoding="utf-8").strip()
    truth_words = text.split()
    asr_words = transcribe_words(Path(args.audio), args.model)
    total = max(end for _, _, end in asr_words) if asr_words else 0.0

    timings = align_truth_to_asr(truth_words, asr_words)
    matched = sum(1 for timing in timings if timing is not None)
    print(f"matched {matched}/{len(truth_words)} script words to ASR timings")
    filled = fill_gaps(timings, truth_words, total)
    alignment = build_char_alignment(text, truth_words, filled)

    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(alignment, ensure_ascii=False))
    print(f"wrote {out} ({len(alignment['characters'])} chars, last end={alignment['character_end_times_seconds'][-1]:.2f}s)")


if __name__ == "__main__":
    main()
