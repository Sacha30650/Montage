#!/usr/bin/env python3
"""Round 2 hook tests — combine winning patterns from round 1.

Styles tested:
  A "text-first-punch"  — refined N2 (bigger fonts, faster fades, yellow hl)
  B "text-first-red"    — pattern-interrupt (red highlight, urgency colors)
  C "mixed"             — text-first 0-3s → cosy 3-15s (predicted winner)
"""
from pathlib import Path

# ------------------------------------------------------------------
# 10 V-tests
# ------------------------------------------------------------------
TESTS = [
    {  # combo gagnant: N3 hook + N2 style + cosy body reveal
        "id": "V1", "style": "mixed", "script": "V1", "vo_dur": 7.81,
        "image": "tests/hooks/images/N3-92percent-notebook.png",
        "caps": [
            ("92 %", 0.0, 1.5, "xxl"),
            ("des parents ratent", 1.5, 1.5, "white"),
            ("CETTE phrase", 3.0, 1.8, "hl"),
            ("au coucher.", 4.8, 1.6, "white"),
            ("La phrase exacte 👇", 7.5, 7.5, "hl"),
        ],
    },
    {  # chiffre encore plus haut
        "id": "V2", "style": "punch", "script": "V2", "vo_dur": 5.51,
        "image": "tests/hooks/images/N3-92percent-notebook.png",
        "caps": [
            ("97 %", 0.0, 1.5, "xxl"),
            ("font CETTE erreur", 1.5, 2.0, "white"),
            ("le soir.", 3.5, 1.5, "hl"),
            ("On l'a tous appris.", 5.5, 9.5, "hl"),
        ],
    },
    {  # fraction concrète
        "id": "V3", "style": "punch", "script": "V3", "vo_dur": 4.49,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "caps": [
            ("1 bébé sur 3", 0.0, 2.0, "xxl"),
            ("dort MAL.", 2.0, 2.0, "white"),
            ("Pas pour la raison qu'on croit.", 4.5, 10.5, "hl"),
        ],
    },
    {  # pattern interrupt rouge
        "id": "V4", "style": "red", "script": "V4", "vo_dur": 4.23,
        "image": "tests/hooks/images/N4-toddler-fist.png",
        "caps": [
            ("STOP.", 0.0, 1.0, "xxl"),
            ("Tu fais pleurer ton bébé", 1.0, 2.0, "white"),
            ("pour RIEN.", 3.0, 1.5, "hl"),
            ("Voici comment savoir 👇", 5.0, 10.0, "hl"),
        ],
    },
    {  # authority break
        "id": "V5", "style": "punch", "script": "V5", "vo_dur": 5.30,
        "image": "tests/hooks/images/N5-mysterious-door.png",
        "caps": [
            ("Ce que les pédiatres", 0.0, 2.0, "white"),
            ("ne disent JAMAIS", 2.0, 2.0, "hl"),
            ("sur le sommeil.", 4.0, 1.5, "white"),
            ("La vérité 👇", 5.8, 9.2, "hl"),
        ],
    },
    {  # time + stat
        "id": "V6", "style": "punch", "script": "V6", "vo_dur": 6.40,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "caps": [
            ("À 2h du matin,", 0.0, 2.0, "white"),
            ("73 %", 2.0, 1.5, "xxl"),
            ("des bébés font CECI.", 3.5, 2.5, "white"),
            ("La plupart des parents répondent mal.", 6.2, 8.8, "hl"),
        ],
    },
    {  # arrête + rouge
        "id": "V7", "style": "red", "script": "V7", "vo_dur": 5.20,
        "image": "tests/hooks/images/N6-intimate-tear.png",
        "caps": [
            ("ARRÊTE", 0.0, 1.2, "xxl"),
            ("de bercer ton bébé", 1.2, 2.0, "white"),
            ("pour l'endormir.", 3.2, 1.8, "hl"),
            ("L'erreur invisible 👇", 5.2, 9.8, "hl"),
        ],
    },
    {  # paradoxe
        "id": "V8", "style": "punch", "script": "V8", "vo_dur": 4.60,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "caps": [
            ("Pour qu'il dorme MIEUX", 0.0, 2.5, "white"),
            ("fais l'INVERSE.", 2.5, 2.0, "xxl"),
            ("3 changements 👇", 4.8, 10.2, "hl"),
        ],
    },
    {  # story + stat — mixed
        "id": "V9", "style": "mixed", "script": "V9", "vo_dur": 4.65,
        "image": "tests/hooks/images/N1-dynamic-nursery.png",
        "caps": [
            ("11h", 0.0, 1.2, "xxl"),
            ("de sommeil d'affilée.", 1.2, 1.8, "white"),
            ("UN changement.", 3.0, 1.8, "hl"),
            ("Voici lequel 👇", 4.9, 10.1, "hl"),
        ],
    },
    {  # curiosity + authority
        "id": "V10", "style": "punch", "script": "V10", "vo_dur": 4.57,
        "image": "tests/hooks/images/N5-mysterious-door.png",
        "caps": [
            ("Personne", 0.0, 1.2, "xxl"),
            ("ne te dit la", 1.2, 1.0, "white"),
            ("VÉRITÉ", 2.2, 1.5, "hl"),
            ("sur le sommeil.", 3.7, 1.5, "white"),
            ("3 min 👇", 5.3, 9.7, "hl"),
        ],
    },
]

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
def render_template(test):
    sid = test["id"]
    image = test["image"]
    audio = f"tests/hooks/audio/{test['script']}.mp3"
    style = test["style"]
    caps = test["caps"]

    # Style-specific palette
    if style == "punch":
        bg = "#0a0a0a"
        scrim_op = 0.88
        hl_color = "rgba(242, 200, 75, 0.62)"      # yellow
        hl_text = "#1a1410"
        cap_color = "#fbf5ef"
        img_filter_initial = "blur(14px) brightness(0.45)"
        img_filter_final = "blur(14px) brightness(0.45)"
        cap_top_initial = 720
        cap_top_final = 720
        cap_fade = 0.12
        ken_burns = ('tl.fromTo("#broll", { scale: 1.25 }, '
                     '{ scale: 1.40, duration: 15, ease: "none" }, 0);')
    elif style == "red":
        bg = "#1a0606"
        scrim_op = 0.85
        hl_color = "rgba(255, 60, 60, 0.78)"
        hl_text = "#1a0606"
        cap_color = "#fbeae8"
        img_filter_initial = "blur(14px) brightness(0.38) sepia(0.3) hue-rotate(-25deg)"
        img_filter_final = img_filter_initial
        cap_top_initial = 720
        cap_top_final = 720
        cap_fade = 0.10
        ken_burns = ('tl.fromTo("#broll", { scale: 1.25 }, '
                     '{ scale: 1.45, duration: 15, ease: "power1.in" }, 0);')
    else:  # mixed: text-first 0-3s, cosy 3-15s
        bg = "#1a1410"
        scrim_op = 0.85
        hl_color = "rgba(242, 200, 75, 0.55)"
        hl_text = "#2a2520"
        cap_color = "#fbf5ef"
        img_filter_initial = "blur(14px) brightness(0.45)"
        img_filter_final = "blur(0px) brightness(1.0)"
        cap_top_initial = 720
        cap_top_final = 1100
        cap_fade = 0.18
        # Mixed needs explicit blur->clear animation at t=3s
        ken_burns = (
            'tl.fromTo("#broll", { scale: 1.20 }, '
            '{ scale: 1.32, duration: 3, ease: "none" }, 0);\n'
            '      tl.to("#broll", { filter: "blur(0px) brightness(1.0)", '
            'scale: 1.0, duration: 0.8, ease: "power2.out" }, 3);\n'
            '      tl.to("#broll", { scale: 1.12, duration: 12, ease: "none" }, 3.8);'
        )

    # Sort captions chronologically + cap duration to next-start
    sorted_caps = sorted(enumerate(caps), key=lambda kv: kv[1][1])
    caption_html_parts = []
    cap_anim_lines = []
    for j, (i, (text, t0, dur, kind)) in enumerate(sorted_caps):
        if j + 1 < len(sorted_caps):
            next_t0 = sorted_caps[j+1][1][1]
            eff_dur = min(dur, next_t0 - t0 - 0.02)
        else:
            eff_dur = min(dur, 15.0 - t0)

        # Per-caption size based on `kind` + position transition for mixed
        in_intro = (t0 < 3.0)
        if kind == "xxl":
            base_size = 200 if in_intro else 110
        elif kind == "hl":
            base_size = 160 if in_intro else 96
        else:
            base_size = 150 if in_intro else 92

        # For mixed style: pick position based on intro vs body
        if style == "mixed":
            top_px = cap_top_initial if in_intro else cap_top_final
        else:
            top_px = cap_top_initial

        if kind in ("hl", "xxl"):
            inner = f'<span class="hl-mark">{text}</span>'
        else:
            inner = text

        cid = f"cap-{sid}-{i}"
        caption_html_parts.append(
            f'      <div class="clip caption" id="{cid}" '
            f'data-start="{t0}" data-duration="{eff_dur:.2f}" data-track-index="3" '
            f'style="font-size:{base_size}px; top:{top_px}px;">{inner}</div>'
        )
        cap_anim_lines.append(
            f'      tl.from("#{cid}", {{ y: 60, opacity: 0, '
            f'duration: {cap_fade}, ease: "power3.out" }}, {t0});'
        )

    caption_html = "\n".join(caption_html_parts)
    cap_anim = "\n".join(cap_anim_lines)

    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@800;900&display=swap" rel="stylesheet" />
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:{bg}; font-family:"Plus Jakarta Sans",sans-serif; }}
      .broll {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter: {img_filter_initial}; }}
      .scrim {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,{scrim_op}) 0%, rgba(0,0,0,{scrim_op-0.4 if scrim_op-0.4 > 0 else 0.1}) 60%, rgba(0,0,0,0.85) 100%); pointer-events:none; }}
      .caption {{
        position:absolute; left:48px; right:48px;
        text-align:center; font-weight:900; line-height:0.95;
        color:{cap_color};
        text-shadow:0 6px 28px rgba(0,0,0,0.95), 0 0 18px rgba(0,0,0,0.6);
        letter-spacing:-0.02em;
      }}
      .hl-mark {{ background: {hl_color}; padding:0 16px; border-radius:8px; color:{hl_text}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
      <img class="clip broll" id="broll" data-start="0" data-duration="15" data-track-index="0" src="{image}">
      <div class="clip scrim" id="scrim" data-start="0" data-duration="15" data-track-index="1"></div>

{caption_html}
      <audio id="voiceover" class="clip" data-start="0" data-duration="15" data-track-index="10" data-volume="1.0" src="{audio}"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="15" data-track-index="11" data-volume="0.025" src="assets/audio/music-pad.mp3"></audio>
      <audio id="sfx-boom" class="clip" data-start="0" data-duration="0.55" data-track-index="12" data-volume="0.55" src="assets/audio/sfx/hook-boom.mp3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {ken_burns}
{cap_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

# ------------------------------------------------------------------
# Write all 10
# ------------------------------------------------------------------
Path("tests/hooks/builds").mkdir(parents=True, exist_ok=True)
for t in TESTS:
    html = render_template(t)
    Path(f"tests/hooks/builds/{t['id']}.html").write_text(html)
    print(f"  generated tests/hooks/builds/{t['id']}.html  (style={t['style']}, script={t['script']})")
