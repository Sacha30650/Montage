#!/usr/bin/env python3
"""Generate pilot-09-mensonges — Carousel-to-video.

Source: 7 carousel slides 1088×1344 (4:5) about "Ton enfant ment et c'est plutôt bon signe".
Output: 1080×1920 9:16 vertical video with Marie-Alice VO + slides centered + blurred backdrop.

No music (user adds trending sound on TikTok). Just VO + minimal SFX (whoosh on transitions + 1 bass-drop on hook).
Subtle Ken Burns + scale punch on transitions to keep visual life.
"""
from pathlib import Path

PILOT = {
    "slug": "pilot-09-mensonges",
    "total_dur": 82,
    "asset_prefix": "pilots/pilot-09-mensonges/assets",
    # (filename, start, duration) — timing from silencedetect on actual Marie-Alice VO
    "slides": [
        ("01_hook.png",       0.0,  6.89),
        ("02_empathy.png",    6.89, 12.76),
        ("03_science.png",   19.65, 11.08),
        ("04_argument2.png", 30.73, 13.67),
        ("05_metaphor.png",  44.40, 11.67),
        ("06_advice.png",    56.07, 14.25),
        ("07_cta.png",       70.32, 11.68),
    ],
    "transitions": [6.89, 19.65, 30.73, 44.40, 56.07, 70.32],
    "bass_drops": [0.0, 70.32],  # hook + final CTA reveal
}


def render(p):
    total = p["total_dur"]
    asset = p["asset_prefix"]

    # Each slide gets 2 images: blurred backdrop (track 0) + clean centered (track 1)
    img_html = []
    ken_burns_lines = []
    for idx, (fn, st, dur) in enumerate(p["slides"]):
        bg_id = f"bg-{idx}"
        fg_id = f"fg-{idx}"
        img_html.append(
            f'      <img class="clip bg-blur" id="{bg_id}" data-start="{st}" data-duration="{dur}" data-track-index="0" src="{asset}/broll/{fn}">'
        )
        img_html.append(
            f'      <img class="clip slide-fg" id="{fg_id}" data-start="{st}" data-duration="{dur}" data-track-index="1" src="{asset}/broll/{fn}">'
        )
        # Foreground: scale punch in (1.04 → 1.0) + slow Ken Burns to 1.03
        ken_burns_lines.append(
            f'      tl.fromTo("#{fg_id}", {{ scale: 1.045 }}, {{ scale: 1.00, duration: 0.30, ease: "power2.out" }}, {st});'
        )
        ken_burns_lines.append(
            f'      tl.to("#{fg_id}", {{ scale: 1.03, duration: {dur - 0.30:.2f}, ease: "power1.inOut" }}, {st + 0.30});'
        )
        # Background: very subtle scale drift
        ken_burns_lines.append(
            f'      tl.fromTo("#{bg_id}", {{ scale: 1.08 }}, {{ scale: 1.14, duration: {dur}, ease: "none" }}, {st});'
        )

    # Whoosh SFX on transitions
    whoosh_html = [
        f'      <audio id="wh-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="11" data-volume="0.40" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        for i, t0 in enumerate(p["transitions"])
    ]
    # Wait — these all on track 11 will overlap. Need different tracks per whoosh.
    whoosh_html = [
        f'      <audio id="wh-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{11+i}" data-volume="0.40" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        for i, t0 in enumerate(p["transitions"])
    ]
    bass_html = [
        f'      <audio id="bd-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{20+i}" data-volume="0.45" src="{asset}/audio/sfx/bass-drop.mp3"></audio>'
        for i, t0 in enumerate(p["bass_drops"])
    ]

    # Camera shake on hook only
    shake_anim = f"""
      tl.to("#shake-wrap", {{ x: 6,  y: -3, duration: 0.04, ease: "none" }}, 0);
      tl.to("#shake-wrap", {{ x: -5, y: 3,  duration: 0.04, ease: "none" }}, 0.04);
      tl.to("#shake-wrap", {{ x: 4,  y: -2, duration: 0.04, ease: "none" }}, 0.08);
      tl.to("#shake-wrap", {{ x: 0,  y: 0,  duration: 0.05, ease: "power2.out" }}, 0.12);"""

    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#f0e6dc; }}
      #shake-wrap {{ position:absolute; inset:0; }}
      .bg-blur {{
        position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
        filter: blur(45px) brightness(0.85) saturate(1.15);
        transform-origin: center;
      }}
      .slide-fg {{
        position:absolute;
        left:0; right:0;
        width:1080px;
        height:1335px;
        top:292px;     /* (1920 - 1335) / 2 ≈ 292 — center vertically */
        object-fit:contain;
        transform-origin: center;
        box-shadow: 0 0 80px rgba(0,0,0,0.25);
      }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      <div id="shake-wrap">
{chr(10).join(img_html)}
      </div>

      <audio id="voiceover" class="clip" data-start="0" data-duration="{total}" data-track-index="8" data-volume="1.0" src="{asset}/audio/voiceover.mp3"></audio>
{chr(10).join(whoosh_html)}
{chr(10).join(bass_html)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(ken_burns_lines)}
{shake_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

html = render(PILOT)
Path(f"pilots/{PILOT['slug']}/index.html").write_text(html)
print(f"  generated pilots/{PILOT['slug']}/index.html")
print(f"  total={PILOT['total_dur']}s, slides={len(PILOT['slides'])}, transitions={len(PILOT['transitions'])}")
