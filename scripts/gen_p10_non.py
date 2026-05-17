#!/usr/bin/env python3
"""Generate pilot-10-non — Carousel "Son non n'est pas contre toi" v2.

Improvements over pilot-09:
- Slide 02 (empathy) visible only 6.2s (vs 12.8s previously) — user dropped off there
- VO reads only 1 of the 3 quotes instead of all 3 (faster)
- Total 72s (vs 82s) — better retention
- Same cosy aesthetic: centered slide + blurred backdrop + Marie-Alice VO
"""
from pathlib import Path

PILOT = {
    "slug": "pilot-10-non",
    "total_dur": 72,
    "asset_prefix": "pilots/pilot-10-non/assets",
    # Timings synced to alignment.json
    "slides": [
        ("01_hook.png",       0.0,  7.68),
        ("02_empathy.png",    7.68, 6.24),   # SHORT — was the drop-off zone
        ("03_science.png",   13.92, 12.46),
        ("04_argument2.png", 26.38, 12.49),
        ("05_metaphor.png",  38.87, 12.32),
        ("06_advice.png",    51.19, 13.73),
        ("07_cta.png",       64.92,  7.08),  # 5s VO + 2s read-time for CTA question
    ],
    "transitions": [7.68, 13.92, 26.38, 38.87, 51.19, 64.92],
    "bass_drops": [0.0, 64.92],
}


def render(p):
    total = p["total_dur"]
    asset = p["asset_prefix"]
    img_html = []
    ken_burns_lines = []
    for idx, (fn, st, dur) in enumerate(p["slides"]):
        bg_id, fg_id = f"bg-{idx}", f"fg-{idx}"
        img_html.append(
            f'      <img class="clip bg-blur" id="{bg_id}" data-start="{st}" data-duration="{dur}" data-track-index="0" src="{asset}/broll/{fn}">'
        )
        img_html.append(
            f'      <img class="clip slide-fg" id="{fg_id}" data-start="{st}" data-duration="{dur}" data-track-index="1" src="{asset}/broll/{fn}">'
        )
        ken_burns_lines.append(
            f'      tl.fromTo("#{fg_id}", {{ scale: 1.045 }}, {{ scale: 1.00, duration: 0.30, ease: "power2.out" }}, {st});'
        )
        ken_burns_lines.append(
            f'      tl.to("#{fg_id}", {{ scale: 1.03, duration: {dur - 0.30:.2f}, ease: "power1.inOut" }}, {st + 0.30});'
        )
        ken_burns_lines.append(
            f'      tl.fromTo("#{bg_id}", {{ scale: 1.08 }}, {{ scale: 1.14, duration: {dur}, ease: "none" }}, {st});'
        )

    whoosh_html = [
        f'      <audio id="wh-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{11+i}" data-volume="0.40" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        for i, t0 in enumerate(p["transitions"])
    ]
    bass_html = [
        f'      <audio id="bd-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{20+i}" data-volume="0.45" src="{asset}/audio/sfx/bass-drop.mp3"></audio>'
        for i, t0 in enumerate(p["bass_drops"])
    ]
    shake_anim = """
      tl.to("#shake-wrap", { x: 6,  y: -3, duration: 0.04, ease: "none" }, 0);
      tl.to("#shake-wrap", { x: -5, y: 3,  duration: 0.04, ease: "none" }, 0.04);
      tl.to("#shake-wrap", { x: 4,  y: -2, duration: 0.04, ease: "none" }, 0.08);
      tl.to("#shake-wrap", { x: 0,  y: 0,  duration: 0.05, ease: "power2.out" }, 0.12);"""

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
        top:292px;
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
print(f"  generated pilots/{PILOT['slug']}/index.html, total={PILOT['total_dur']}s, slides={len(PILOT['slides'])}")
