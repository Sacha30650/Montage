#!/usr/bin/env python3
"""Generate a French voice-over with ElevenLabs.

Reads ELEVENLABS_API_KEY from environment (.env auto-loaded). Voice IDs:
  - Charlotte (XB0fDUnXU5powFXDhCwa) — warm, recommended for parenting
  - Alice    (Xb7hH8MSUJpSbSDYk0k2)
  - Sarah    (EXAVITQu4vr4xnSDxMaL)

Usage:
  python3 scripts/tts_elevenlabs.py <input.txt> <output.mp3> [voice_id] [model_id]
"""
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

def tts(text: str, out: Path, voice_id: str, model_id: str) -> None:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY missing (put it in .env)")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.15,
            "use_speaker_boost": True,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs HTTP {e.code}: {e.read().decode()[:500]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(f"wrote {out} ({len(data):,} bytes)")

def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    inp, outp = Path(sys.argv[1]), Path(sys.argv[2])
    voice = sys.argv[3] if len(sys.argv) > 3 else "XB0fDUnXU5powFXDhCwa"  # Charlotte
    model = sys.argv[4] if len(sys.argv) > 4 else "eleven_multilingual_v2"
    load_env(Path(__file__).resolve().parent.parent / ".env")
    text = inp.read_text(encoding="utf-8").strip()
    print(f"voice={voice} model={model} chars={len(text)}")
    tts(text, outp, voice, model)

if __name__ == "__main__":
    main()
