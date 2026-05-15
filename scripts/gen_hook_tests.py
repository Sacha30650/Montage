#!/usr/bin/env python3
"""Generate 6 hook test HTMLs from a shared template.

3 styles tested (cosy / dynamic / text-first) x 5 scripts.
Each clip is 15s exactly (virality_predictor max).
"""
import json
from pathlib import Path

# ------------------------------------------------------------------
# Define the 6 tests
# ------------------------------------------------------------------
TESTS = [
    {
        "id": "N1",
        "style": "dynamic",
        "script": "A",
        "vo_dur": 8.12,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "captions": [
            ("Ton enfant se réveille", 0.0, 2.5, "white"),
            ("toutes les 2 h ?", 2.5, 4.5, "highlight"),
            ("CE N'EST PAS UN CAPRICE.", 4.5, 8.5, "white"),
            ("L'erreur invisible 👇", 9.5, 5.5, "highlight"),
        ],
    },
    {
        "id": "N2",
        "style": "text-first",
        "script": "A",
        "vo_dur": 8.12,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "captions": [
            ("Si ton enfant", 0.0, 2.0, "white"),
            ("se réveille TOUTES LES 2H", 2.0, 3.0, "highlight"),
            ("ce n'est pas un caprice.", 5.0, 3.5, "white"),
            ("L'erreur INVISIBLE.", 8.5, 6.5, "highlight"),
        ],
    },
    {
        "id": "N3",
        "style": "cosy",
        "script": "B",
        "vo_dur": 6.11,
        "image": "tests/hooks/images/N3-92percent-notebook.png",
        "captions": [
            ("92 % des parents", 0.0, 2.5, "highlight"),
            ("font CETTE erreur", 2.5, 2.5, "white"),
            ("chaque soir.", 5.0, 2.0, "highlight"),
            ("Voici laquelle 👇", 7.0, 8.0, "white"),
        ],
    },
    {
        "id": "N4",
        "style": "dynamic",
        "script": "C",
        "vo_dur": 6.84,
        "image": "tests/hooks/images/N4-toddler-fist.png",
        "captions": [
            ("Tu dis « calme-toi »", 0.0, 2.3, "white"),
            ("ARRÊTE.", 2.3, 1.5, "highlight"),
            ("Tu aggraves la crise.", 3.8, 3.5, "white"),
            ("Voici quoi dire 👇", 7.5, 7.5, "highlight"),
        ],
    },
    {
        "id": "N5",
        "style": "cosy",
        "script": "D",
        "vo_dur": 7.31,
        "image": "tests/hooks/images/N5-mysterious-door.png",
        "captions": [
            ("L'erreur n°1", 0.0, 2.0, "highlight"),
            ("qui empêche ton bébé", 2.0, 2.5, "white"),
            ("de dormir…", 4.5, 2.0, "white"),
            ("…tu la fais ce soir.", 7.0, 8.0, "highlight"),
        ],
    },
    {
        "id": "N6",
        "style": "cosy",
        "script": "E",
        "vo_dur": 6.79,
        "image": "tests/hooks/images/N6-intimate-tear.png",
        "captions": [
            ("Quand mon enfant", 0.0, 2.0, "white"),
            ("a fait sa 1ère NUIT", 2.0, 2.5, "highlight"),
            ("j'ai pleuré.", 4.5, 2.5, "white"),
            ("3 changements 👇", 7.5, 7.5, "highlight"),
        ],
    },
]

# ------------------------------------------------------------------
# Template
# ------------------------------------------------------------------
def render_template(test):
    sid = test["id"]
    image = test["image"]
    script = test["script"]
    audio = f"tests/hooks/audio/{script}.mp3"
    style = test["style"]
    caps = test["captions"]

    # Style-specific CSS + animations
    if style == "cosy":
        bg = "#1a1410"
        cap_size = 92
        cap_top = 1100
        ken_burns = "scale=1.0 → 1.10 over 15s"
        scrim_op = 0.55
        cap_fade = 0.30
        cap_y = 30
    elif style == "dynamic":
        bg = "#0a0a0a"
        cap_size = 108
        cap_top = 1050
        ken_burns = "scale=1.05 → 1.18 over 15s"
        scrim_op = 0.70
        cap_fade = 0.18
        cap_y = 50
    else:  # text-first
        bg = "#1a1410"
        cap_size = 150
        cap_top = 700
        ken_burns = "scale=1.20 → 1.35 over 15s, blurred"
        scrim_op = 0.85
        cap_fade = 0.25
        cap_y = 40

    blur = "filter: blur(12px) brightness(0.5);" if style == "text-first" else ""

    # Caption blocks HTML — fix overlap: cap each caption duration at (next_start - this_start - 0.02)
    caption_html = ""
    sorted_caps = sorted(enumerate(caps), key=lambda kv: kv[1][1])
    for j, (i, (text, t0, dur, color)) in enumerate(sorted_caps):
        # Recompute effective duration so no overlap with next
        if j + 1 < len(sorted_caps):
            next_start = sorted_caps[j+1][1][1]
            eff_dur = min(dur, next_start - t0 - 0.02)
        else:
            eff_dur = min(dur, 15.0 - t0)
        if color == "highlight":
            text_html = f'<span class="hl-mark">{text}</span>'
        else:
            text_html = text
        size_attr = f"font-size:{cap_size}px; line-height:0.98;"
        caption_html += f'      <div class="clip caption" id="cap-{sid}-{i}" data-start="{t0}" data-duration="{eff_dur:.2f}" data-track-index="3" style="{size_attr}">{text_html}</div>\n'

    # GSAP from animation per caption (use original t0)
    cap_anim = "\n".join([
        f'      tl.from("#cap-{sid}-{i}", {{ y: {cap_y}, opacity: 0, duration: {cap_fade}, ease: "power3.out" }}, {c[1]});'
        for i, c in enumerate(caps)
    ])

    # Ken Burns
    if style == "dynamic":
        # stutter zoom: 3 punches in 15s
        ken_burns_anim = f"""
      tl.fromTo("#broll", {{ scale: 1.05 }}, {{ scale: 1.10, duration: 5, ease: "none" }}, 0);
      tl.to("#broll", {{ scale: 1.18, duration: 5, ease: "power2.in" }}, 5);
      tl.to("#broll", {{ scale: 1.04, duration: 0.20, ease: "power2.out" }}, 10);
      tl.to("#broll", {{ scale: 1.18, duration: 5, ease: "power2.in" }}, 10.2);"""
    elif style == "text-first":
        ken_burns_anim = '      tl.fromTo("#broll", { scale: 1.20 }, { scale: 1.35, duration: 15, ease: "none" }, 0);'
    else:  # cosy
        ken_burns_anim = '      tl.fromTo("#broll", { scale: 1.0 }, { scale: 1.10, duration: 15, ease: "none" }, 0);'

    # whoosh SFX only in dynamic style — track 13 to avoid overlap with hook-boom on 12
    sfx_html = ""
    if style == "dynamic":
        for i, c in enumerate(caps):
            t0_whoosh = max(0.6, c[1] - 0.05)  # always after the hook-boom
            sfx_html += f'      <audio id="sfx-{sid}-w{i}" class="clip" data-start="{t0_whoosh}" data-duration="0.62" data-track-index="13" data-volume="0.30" src="assets/audio/sfx/whoosh.mp3"></audio>\n'

    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,800;1,800&family=Plus+Jakarta+Sans:wght@800&display=swap" rel="stylesheet" />
    <style>
      :root {{
        --bg-cream: #fbf5ef;
        --brown-deep: #2a2520;
        --terracotta: #c56f4a;
        --sage: #87a878;
        --highlight: #f2c84b;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:{bg}; font-family:"Plus Jakarta Sans",sans-serif; }}
      .broll {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; {blur} }}
      .scrim {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,{scrim_op}) 0%, rgba(0,0,0,0) 35%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.7) 100%); pointer-events:none; }}
      .caption {{
        position:absolute; left:60px; right:60px; top:{cap_top}px;
        text-align:center; font-weight:800; line-height:1.05;
        color:var(--bg-cream);
        text-shadow:0 4px 24px rgba(0,0,0,0.85), 0 0 14px rgba(0,0,0,0.4);
        letter-spacing:-0.01em;
      }}
      .hl-mark {{ background: rgba(242,200,75,0.55); padding:0 12px; border-radius:6px; color:var(--brown-deep); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
      <img class="clip broll" id="broll" data-start="0" data-duration="15" data-track-index="0" src="{image}">
      <div class="clip scrim" id="scrim" data-start="0" data-duration="15" data-track-index="1"></div>

{caption_html}
      <audio id="voiceover" class="clip" data-start="0" data-duration="15" data-track-index="10" data-volume="1.0" src="{audio}"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="15" data-track-index="11" data-volume="0.025" src="assets/audio/music-pad.mp3"></audio>
      <audio id="sfx-boom" class="clip" data-start="0" data-duration="0.55" data-track-index="12" data-volume="0.45" src="assets/audio/sfx/hook-boom.mp3"></audio>
{sfx_html}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{ken_burns_anim}
{cap_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

# ------------------------------------------------------------------
# Write each test HTML
# ------------------------------------------------------------------
Path("tests/hooks/builds").mkdir(parents=True, exist_ok=True)
for t in TESTS:
    html = render_template(t)
    Path(f"tests/hooks/builds/{t['id']}.html").write_text(html)
    print(f"  generated tests/hooks/builds/{t['id']}.html  (style={t['style']}, script={t['script']})")
