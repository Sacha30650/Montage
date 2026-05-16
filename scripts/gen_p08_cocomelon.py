#!/usr/bin/env python3
"""Generate pilot-08-cocomelon — DYNAMIC.

Hook: "Cocomelon est INTERDIT chez les pédiatres américains. Voici pourquoi."
Marie-Alice v3 voice. Yellow plein WOW words only, white outlined body.
Stutter zoom + camera shake + yellow flashes + whooshes + workout-beat music.
"""
from pathlib import Path

PILOT = {
    "slug": "pilot-08-cocomelon",
    "total_dur": 62,
    "asset_prefix": "pilots/pilot-08-cocomelon/assets",
    "images": [
        ("00-hook-eye.png",       0.0,  3.5,  "hook", "stutter"),
        ("00-hook-eye.png",       3.5,  2.0,  "body", "in"),
        ("01-tv-flicker.png",     5.5,  3.1,  "body", "in"),
        ("02-tablet-hands.png",   8.6,  2.4,  "body", "in"),
        ("01-tv-flicker.png",    11.0,  2.4,  "body", "out"),
        ("02-tablet-hands.png",  13.4,  3.6,  "body", "right"),
        ("02-tablet-hands.png",  17.0,  4.0,  "body", "out"),
        ("01-tv-flicker.png",    21.0,  3.4,  "body", "left"),
        ("02-tablet-hands.png",  24.4,  3.9,  "body", "in"),
        ("01-tv-flicker.png",    28.3,  4.2,  "body", "in"),
        ("04-book.png",          32.5,  4.2,  "body", "in"),
        ("03-three-blocks.png",  36.7,  3.9,  "body", "in"),
        ("03-three-blocks.png",  40.6,  2.69, "body", "left"),
        ("03-three-blocks.png",  43.3,  3.0,  "body", "out"),
        ("04-book.png",          46.3,  2.9,  "body", "in"),
        ("04-book.png",          49.2,  4.59, "body", "left"),
        ("04-book.png",          53.8,  4.3,  "body", "out"),
        ("04-book.png",          58.1,  3.9,  "body", "in"),
    ],

    # Captions synced via alignment.json sentence boundaries (+0.5s pad)
    "hook_caps": [
        ("Cocomelon",                       0.50, 1.30, "hl", "stutter"),
        ("INTERDIT",                        1.80, 1.40, "xxl", "shake"),
        ("chez les pédiatres",              3.20, 1.05, "white", "pop"),
        ("Voici pourquoi 👇",               4.25, 1.25, "hl", "pop"),
    ],
    "bridge_caps": [
        ("1 minute =",                      5.55, 1.50, "white", "pop"),
        ("600 CUTS",                        7.10, 1.45, "xxl", "shake"),
        ("Le cerveau n'a AUCUNE chance",    8.60, 2.20, "white", "pop"),
        ("3 effets mesurés 👇",             10.85, 2.50, "hl", "pop"),
    ],
    "body_caps": [
        ("EFFET 1",                         13.40, 1.05, "xxl", "shake"),
        ("Déficit d'ATTENTION",             14.50, 1.10, "hl", "pop"),
        ("Après 12 min",                    15.65, 2.20, "white", "pop"),
        ("→ 30 min sans concentration",     17.90, 2.95, "white", "pop"),

        ("EFFET 2",                         20.90, 1.95, "xxl", "shake"),
        ("Régression du LANGAGE",           22.90, 1.40, "hl", "pop"),
        ("Parlent moins, plus tard",        24.35, 2.95, "white", "pop"),
        ("Moins de MOTS",                   27.35, 0.85, "white", "pop"),

        ("EFFET 3",                         28.30, 1.60, "xxl", "shake"),
        ("Dépendance à la stimulation",     29.95, 2.50, "white", "pop"),
        ("Le livre devient ENNUYEUX 📕",     32.55, 2.00, "white", "pop"),
        ("La vraie vie devient ennuyeuse",  34.60, 2.10, "white", "pop"),

        ("LE TEST 👇",                       36.75, 2.60, "xxl", "shake"),
        ("Pose 3 cubes au sol",             39.40, 1.15, "white", "pop"),
        ("5 min seul = OK ✅",              40.60, 2.65, "white", "pop"),
        ("Sinon → baisse la DOSE",          43.30, 2.95, "hl", "shake"),

        ("Les ALTERNATIVES saines",         46.35, 2.80, "xxl", "shake"),
        ("📖 Livre · 🎵 Comptine · 🌳 Dehors", 49.25, 4.55, "white", "pop"),

        ("Curiosité naturelle RETROUVÉE",   53.90, 4.20, "hl", "pop"),
    ],
    "outro_caps": [
        ("Sauvegarde 💾",                   58.20, 2.00, "xxl", "shake"),
        ("Partage à un parent 🤝",          60.25, 1.75, "white", "pop"),
    ],

    "flashes": [
        ("yellow", 0.0,  0.10, 0.90),
        ("yellow", 5.55, 0.10, 0.95),   # 600 CUTS reveal
        ("black",  10.80, 0.06, 1.0),    # bridge → body
        ("yellow", 13.40, 0.08, 0.85),  # EFFET 1
        ("yellow", 20.90, 0.08, 0.85),  # EFFET 2
        ("yellow", 28.30, 0.08, 0.85),  # EFFET 3
        ("yellow", 36.75, 0.10, 0.95),  # LE TEST
        ("yellow", 46.35, 0.08, 0.85),  # ALTERNATIVES
    ],

    "whooshes": [
        3.50, 5.55, 8.60, 13.40, 20.90, 28.30, 36.75, 46.35,
    ],

    "bass_drops": [
        0.0,    # hook punch
        5.55,   # 600 CUTS
        13.40,  # EFFET 1
        20.90,  # EFFET 2
        28.30,  # EFFET 3
        36.75,  # LE TEST
        58.20,  # Sauvegarde climax
    ],

    "shakes": [
        0.0, 5.55, 13.40, 20.90, 28.30, 36.75, 58.20,
    ],
}

def ken_burns(sid, start, dur, kind, direction):
    if kind == "hook" and direction == "stutter":
        return f"""
      tl.fromTo("#{sid}", {{ scale: 1.00 }}, {{ scale: 1.22, duration: 0.07, ease: "power3.out" }}, {start});
      tl.to("#{sid}", {{ scale: 1.04, duration: 0.07, ease: "power3.in" }}, {start + 0.07});
      tl.to("#{sid}", {{ scale: 1.20, duration: 0.07, ease: "power3.out" }}, {start + 0.14});
      tl.to("#{sid}", {{ scale: 1.03, duration: 0.07, ease: "power3.in" }}, {start + 0.21});
      tl.to("#{sid}", {{ scale: 1.18, duration: 0.06, ease: "power3.out" }}, {start + 0.28});
      tl.to("#{sid}", {{ scale: 1.00, duration: 0.40, ease: "power2.out" }}, {start + 0.34});
      tl.to("#{sid}", {{ scale: 1.10, duration: {dur - 0.74:.2f}, ease: "power1.in" }}, {start + 0.74});"""
    if direction == "in":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.02 }}, {{ scale: 1.14, duration: {dur}, ease: "none" }}, {start});'
    if direction == "out":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.14 }}, {{ scale: 1.02, duration: {dur}, ease: "none" }}, {start});'
    if direction == "left":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.10, x: 50 }}, {{ scale: 1.10, x: -50, duration: {dur}, ease: "none" }}, {start});'
    if direction == "right":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.10, x: -50 }}, {{ scale: 1.10, x: 50, duration: {dur}, ease: "none" }}, {start});'
    return f'      tl.fromTo("#{sid}", {{ scale: 1.02 }}, {{ scale: 1.12, duration: {dur}, ease: "none" }}, {start});'


def caption_anim(cid, t0, anim):
    if anim == "stutter":
        return f"""
      tl.from("#{cid}", {{ scale: 0.3, opacity: 0, rotation: -8, duration: 0.18, ease: "back.out(4.0)" }}, {t0});
      tl.to("#{cid}",   {{ scale: 1.12, duration: 0.06, ease: "power2.out" }}, {t0 + 0.18});
      tl.to("#{cid}",   {{ scale: 1.00, duration: 0.10, ease: "power2.in" }}, {t0 + 0.24});"""
    if anim == "shake":
        return f"""
      tl.from("#{cid}", {{ scale: 0.5, opacity: 0, duration: 0.22, ease: "back.out(3.5)" }}, {t0});
      tl.to("#{cid}",   {{ x: 8,  duration: 0.04 }}, {t0 + 0.22});
      tl.to("#{cid}",   {{ x: -7, duration: 0.04 }}, {t0 + 0.26});
      tl.to("#{cid}",   {{ x: 5,  duration: 0.04 }}, {t0 + 0.30});
      tl.to("#{cid}",   {{ x: 0,  duration: 0.06 }}, {t0 + 0.34});"""
    return f'      tl.from("#{cid}", {{ y: 40, scale: 0.7, opacity: 0, duration: 0.22, ease: "back.out(3.0)" }}, {t0});'


def render(p):
    total = p["total_dur"]
    asset = p["asset_prefix"]
    img_html = []
    ken_burns_lines = []
    for idx, (fn, st, dur, kind, dir_) in enumerate(p["images"]):
        sid = f"img-{idx}"
        cls = "broll-hook" if kind == "hook" else "broll-body"
        img_html.append(
            f'      <img class="clip {cls}" id="{sid}" data-start="{st}" data-duration="{dur}" data-track-index="0" src="{asset}/broll/{fn}">'
        )
        ken_burns_lines.append(ken_burns(sid, st, dur, kind, dir_))

    def caps_block(caps, track, kind):
        sc = sorted(enumerate(caps), key=lambda kv: kv[1][1])
        html, anim = [], []
        for j, (i, item) in enumerate(sc):
            text, t0, dur, ck, ca = item
            if j + 1 < len(sc):
                next_t0 = sc[j+1][1][1]
                eff_dur = min(dur, next_t0 - t0 - 0.02)
            else:
                eff_dur = dur
            inner = f'<span class="hl-mark">{text}</span>' if ck in ("hl", "xxl") else text
            base_size = 175 if ck == "xxl" else (135 if ck == "hl" else 110)
            cid = f"cap-{kind}-{i}"
            html.append(
                f'      <div class="clip caption" id="{cid}" data-start="{t0}" data-duration="{eff_dur:.2f}" '
                f'data-track-index="{track}" style="font-size:{base_size}px;">{inner}</div>'
            )
            anim.append(caption_anim(cid, t0, ca))
        return "\n".join(html), "\n".join(anim)

    hook_html, hook_anim = caps_block(p["hook_caps"], 2, "hook")
    bridge_html, bridge_anim = caps_block(p["bridge_caps"], 3, "bridge")
    body_html, body_anim = caps_block(p["body_caps"], 4, "body")
    outro_html, outro_anim = caps_block(p["outro_caps"], 5, "outro")

    flash_html, flash_anim = [], []
    for i, (color, t0, dur, op) in enumerate(p["flashes"]):
        fid = f"flash-{i}"
        bg = "#FFE600" if color == "yellow" else "#000000"
        blend = "screen" if color == "yellow" else "normal"
        flash_html.append(
            f'      <div class="clip flash" id="{fid}" data-start="{t0}" data-duration="{dur}" data-track-index="6" style="background:{bg}; mix-blend-mode:{blend};"></div>'
        )
        flash_anim.append(
            f'      tl.fromTo("#{fid}", {{ opacity: 0 }}, {{ opacity: {op}, duration: 0.03, ease: "none" }}, {t0});\n'
            f'      tl.to("#{fid}", {{ opacity: 0, duration: {dur - 0.03}, ease: "power1.out" }}, {t0 + 0.03});'
        )

    whoosh_html = [
        f'      <audio id="wh-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{11+i}" data-volume="0.45" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        for i, t0 in enumerate(p["whooshes"])
    ]
    bass_html = [
        f'      <audio id="bd-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{19+i}" data-volume="0.60" src="{asset}/audio/sfx/bass-drop.mp3"></audio>'
        for i, t0 in enumerate(p["bass_drops"])
    ]

    shake_anim = []
    for t0 in p["shakes"]:
        shake_anim.append(f"""
      tl.to("#shake-wrap", {{ x: 8,  y: -5, duration: 0.04, ease: "none" }}, {t0});
      tl.to("#shake-wrap", {{ x: -7, y: 4,  duration: 0.04, ease: "none" }}, {t0 + 0.04});
      tl.to("#shake-wrap", {{ x: 5,  y: -3, duration: 0.04, ease: "none" }}, {t0 + 0.08});
      tl.to("#shake-wrap", {{ x: -3, y: 2,  duration: 0.04, ease: "none" }}, {t0 + 0.12});
      tl.to("#shake-wrap", {{ x: 0,  y: 0,  duration: 0.05, ease: "power2.out" }}, {t0 + 0.16});""")

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
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0a0a0a; font-family:"Plus Jakarta Sans",sans-serif; }}
      #shake-wrap {{ position:absolute; inset:0; }}
      .broll-hook {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter: blur(14px) brightness(0.45); }}
      .broll-body {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
      .scrim-hook {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.30) 60%, rgba(0,0,0,0.85) 100%); pointer-events:none; }}
      .scrim-body {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 35%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.72) 100%); pointer-events:none; }}
      .caption {{
        position:absolute; left:60px; right:60px; top:780px;
        text-align:center; font-weight:900; line-height:0.98;
        color:#ffffff;
        text-shadow:
          4px 4px 0 #000, -4px -4px 0 #000,
          4px -4px 0 #000, -4px 4px 0 #000,
          0 4px 0 #000, 0 -4px 0 #000,
          4px 0 0 #000, -4px 0 0 #000,
          0 10px 28px rgba(0,0,0,0.85);
        letter-spacing:-0.02em;
      }}
      .hl-mark {{
        background:#FFE600;
        padding:6px 22px;
        color:#0a0a0a;
        text-shadow:none;
        font-weight:900;
        -webkit-box-decoration-break:clone;
        box-decoration-break:clone;
        line-height:1.05;
        display:inline;
      }}
      .flash {{ position:absolute; inset:0; pointer-events:none; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
      <div id="shake-wrap">
{chr(10).join(img_html)}

      <div class="clip scrim-hook" data-start="0" data-duration="6" data-track-index="1"></div>
      <div class="clip scrim-body" data-start="6" data-duration="{total - 6}" data-track-index="1"></div>

{hook_html}
{bridge_html}
{body_html}
{outro_html}

{chr(10).join(flash_html)}
      </div>

      <audio id="voiceover" class="clip" data-start="0" data-duration="{total}" data-track-index="8" data-volume="1.0" src="{asset}/audio/voiceover.mp3"></audio>
      <audio id="music"     class="clip" data-start="0" data-duration="{total}" data-track-index="9" data-volume="0.10" src="{asset}/audio/music-loop.mp3"></audio>
      <audio id="hook-boom" class="clip" data-start="0" data-duration="0.55" data-track-index="10" data-volume="0.55" src="{asset}/audio/sfx/hook-boom.mp3"></audio>
{chr(10).join(whoosh_html)}
{chr(10).join(bass_html)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(ken_burns_lines)}

{hook_anim}
{bridge_anim}
{body_anim}
{outro_anim}

{chr(10).join(flash_anim)}

{"".join(shake_anim)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

html = render(PILOT)
Path(f"pilots/{PILOT['slug']}/index.html").write_text(html)
n_caps = len(PILOT["hook_caps"]) + len(PILOT["bridge_caps"]) + len(PILOT["body_caps"]) + len(PILOT["outro_caps"])
print(f"  generated pilots/{PILOT['slug']}/index.html")
print(f"  total={PILOT['total_dur']}s, images={len(PILOT['images'])}, captions={n_caps}, "
      f"flashes={len(PILOT['flashes'])}, whooshes={len(PILOT['whooshes'])}, bass={len(PILOT['bass_drops'])}, shakes={len(PILOT['shakes'])}")
