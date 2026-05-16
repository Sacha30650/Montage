#!/usr/bin/env python3
"""Generate P05 sommeil v6 — MAXIMUM DYNAMISM.

New hook: "47 stratégies pour endormir ton bébé. 46 sont FAUSSES."
- Stutter zoom on hook (5 scale punches in 0.5s)
- Camera shake on bass-drops (±8px translate, 4 oscillations)
- 4 yellow flash overlays at key beats
- 5 whoosh SFX between major section transitions
- workout-beat.mp3 music loop (high BPM vs the ambient pad)
- 22 image cuts in 65s (vs 10 previously) — reuse with KB variations
- Caption back.out(3.5) overshoot — bigger pops
- "FAUSSES" reveal with massive yellow flash + max overshoot
"""
from pathlib import Path

PILOT = {
    "slug": "pilot-05-sommeil-97",
    "total_dur": 65,
    "asset_prefix": "pilots/pilot-05-sommeil-97/assets",
    # 22 image cuts — heavy reuse with varied KB directions for visual variety
    "images": [
        # filename, start, duration, kind (hook/body), kb_direction
        ("00-hook-stat.png",      0.0, 3.3, "hook", "stutter"),  # STUTTER ZOOM 0-3.3s
        ("01-screens.png",        3.3, 2.6, "body", "in"),
        ("00-hook-stat.png",      5.9, 1.89, "body", "out"),
        ("03-phrase.png",         7.8, 1.4, "body", "in"),
        ("01-screens.png",        9.2, 2.6, "body", "left"),
        ("00-hook-stat.png",     11.8, 1.39, "body", "out"),
        ("01-screens.png",       13.2, 3.0, "body", "in"),
        ("01-screens.png",       16.2, 3.2, "body", "right"),
        ("00-hook-stat.png",     19.4, 2.0, "body", "in"),
        ("02-notes.png",         21.4, 3.5, "body", "in"),
        ("03-phrase.png",        24.9, 1.4, "body", "in"),
        ("03-phrase.png",        26.3, 3.9, "body", "left"),
        ("01-screens.png",       30.2, 3.3, "body", "out"),
        ("02-notes.png",         33.5, 3.5, "body", "in"),
        ("00-hook-stat.png",     37.0, 1.5, "body", "out"),
        ("02-notes.png",         38.5, 3.9, "body", "left"),
        ("02-notes.png",         42.9, 3.6, "body", "in"),
        ("00-hook-stat.png",     46.5, 1.3, "body", "out"),
        ("04-outro.png",         47.9, 2.5, "body", "in"),
        ("04-outro.png",         50.4, 2.4, "body", "out"),
        ("04-outro.png",         52.8, 3.7, "body", "left"),
        ("04-outro.png",         56.5, 8.5, "body", "in"),
    ],

    # Captions — synced to silencedetect on Marie-Alice v3 VO
    # kind:
    #   "xxl"   → yellow plein hl, font 200px — WOW reveal moments only
    #   "hl"    → yellow plein hl, font 140px — strong emphasis
    #   "white" → white outlined no yellow, font 115px — body default (clean)
    "hook_caps": [
        ("47",                                0.55, 1.0,  "xxl", "stutter"),
        ("stratégies pour endormir",          1.6,  1.6,  "white", "pop"),
        ("ton bébé.",                         3.0,  0.27, "white", "pop"),
        ("46",                                3.30, 1.3,  "xxl", "shake"),
        ("sont FAUSSES.",                     4.65, 1.25, "hl",  "shake"),
    ],
    "bridge_caps": [
        ("Tu les essaies toutes ce soir.",    5.92, 1.83, "white", "pop"),
        ("La VRAIE raison ?",                 7.78, 1.40, "white", "pop"),
        ("3 erreurs invisibles 👇",           9.20, 2.50, "hl",   "pop"),
    ],
    "body_caps": [
        ("ERREUR 1",                         11.85, 1.20, "xxl", "pop"),
        ("Les écrans après 19h",             13.20, 2.95, "white", "pop"),
        ("Même la TV en arrière-plan",       16.25, 3.10, "white", "pop"),
        ("Le cerveau confond jour & nuit",   19.45, 1.85, "white", "pop"),
        ("Lumière CHAUDE 💡 1h avant",       21.40, 3.45, "white", "pop"),

        ("ERREUR 2",                         24.92, 1.30, "xxl", "shake"),
        ('"va dormir" → ANXIÉTÉ',            26.32, 3.85, "white", "pop"),
        ('Dis "on va se CALMER"',            30.25, 3.25, "white", "pop"),
        ("Utilise le mot CALME",             33.55, 3.40, "white", "pop"),

        ("ERREUR 3",                         37.05, 1.40, "xxl", "shake"),
        ("Tu cèdes à la 3ème demande",       38.55, 1.85, "white", "pop"),
        ("Eau · Câlin · Pipi 🤦",            40.45, 2.40, "white", "pop"),
        ("Tu rentres dans le JEU",           42.90, 1.60, "white", "pop"),
        ("Règles AVANT le coucher",          44.55, 1.90, "white", "pop"),
        ("1 seule demande max",              46.55, 1.35, "white", "pop"),

        ("Lumière · Phrase · Règles",        47.90, 2.45, "white", "pop"),
        ("Tu gagnes 2h de sommeil 🌙",        50.40, 4.45, "white", "pop"),
        ("Il fait ses NUITS ✨",              54.90, 1.55, "xxl", "shake"),
    ],
    "outro_caps": [
        ("Sauvegarde 💾",                    56.45, 2.40, "xxl", "pop"),
        ("Partage à un parent épuisé 🤝",    58.85, 6.15, "white", "pop"),
    ],

    # Yellow flash overlays at key impact moments
    "flashes": [
        ("yellow", 0.0,  0.10, 0.90),   # hook punch
        ("yellow", 3.30, 0.10, 0.95),   # "46 FAUSSES" reveal
        ("yellow", 24.92, 0.08, 0.85),  # ERREUR 2 transition
        ("yellow", 37.05, 0.08, 0.85),  # ERREUR 3 transition
        ("yellow", 54.90, 0.10, 0.95),  # "Il fait ses NUITS" climax
        ("black",  11.80, 0.06, 1.0),   # bridge → body cut
    ],

    # Whoosh SFX between major image sections
    "whooshes": [
        3.30, 11.85, 24.92, 37.05, 47.90, 54.90
    ],

    # Bass-drop SFX at major hits
    "bass_drops": [
        0.0,     # hook punch
        3.30,    # "46 FAUSSES" reveal
        24.92,   # ERREUR 2
        37.05,   # ERREUR 3
        54.90,   # "Il fait ses NUITS" reveal
    ],

    # Camera shake on these times (composition-wide, 0.4s burst)
    "shakes": [
        0.0,     # hook
        3.30,    # FAUSSES reveal
        24.92,   # ERREUR 2
        37.05,   # ERREUR 3
        54.90,   # NUITS
    ],
}

def ken_burns(sid, start, dur, kind, direction):
    if kind == "hook" and direction == "stutter":
        # STUTTER ZOOM: 5 rapid scale punches in 0.5s, then settle
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
        # Stutter pop: scale bumps + rotation kick
        return f"""
      tl.from("#{cid}", {{ scale: 0.3, opacity: 0, rotation: -8, duration: 0.18, ease: "back.out(4.0)" }}, {t0});
      tl.to("#{cid}",   {{ scale: 1.12, duration: 0.06, ease: "power2.out" }}, {t0 + 0.18});
      tl.to("#{cid}",   {{ scale: 1.00, duration: 0.10, ease: "power2.in" }}, {t0 + 0.24});"""
    if anim == "shake":
        # Pop in + shake the caption
        return f"""
      tl.from("#{cid}", {{ scale: 0.5, opacity: 0, duration: 0.22, ease: "back.out(3.5)" }}, {t0});
      tl.to("#{cid}",   {{ x: 8,  duration: 0.04 }}, {t0 + 0.22});
      tl.to("#{cid}",   {{ x: -7, duration: 0.04 }}, {t0 + 0.26});
      tl.to("#{cid}",   {{ x: 5,  duration: 0.04 }}, {t0 + 0.30});
      tl.to("#{cid}",   {{ x: 0,  duration: 0.06 }}, {t0 + 0.34});"""
    # default: pop with overshoot
    return f'      tl.from("#{cid}", {{ y: 40, scale: 0.7, opacity: 0, duration: 0.22, ease: "back.out(3.0)" }}, {t0});'


def render(p):
    total = p["total_dur"]
    asset = p["asset_prefix"]

    # Image elements + Ken Burns
    img_html = []
    ken_burns_lines = []
    for idx, (fn, st, dur, kind, dir_) in enumerate(p["images"]):
        sid = f"img-{idx}"
        cls = "broll-hook" if kind == "hook" else "broll-body"
        img_html.append(
            f'      <img class="clip {cls}" id="{sid}" data-start="{st}" data-duration="{dur}" data-track-index="0" src="{asset}/broll/{fn}">'
        )
        ken_burns_lines.append(ken_burns(sid, st, dur, kind, dir_))

    # Captions on 4 tracks (hook=2, bridge=3, body=4, outro=5)
    def caps_block(caps, track, kind):
        sorted_caps = sorted(enumerate(caps), key=lambda kv: kv[1][1])
        html = []
        anim = []
        for j, (i, item) in enumerate(sorted_caps):
            text, t0, dur, ck, ca = item
            if j + 1 < len(sorted_caps):
                next_t0 = sorted_caps[j+1][1][1]
                eff_dur = min(dur, next_t0 - t0 - 0.02)
            else:
                eff_dur = dur
            inner = f'<span class="hl-mark">{text}</span>' if ck in ("hl", "xxl") else text
            base_size = 210 if ck == "xxl" else (140 if ck == "hl" else 115)
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

    # Flash overlays
    flash_html = []
    flash_anim = []
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

    # SFX whooshes — each on its own track (7+ to avoid overlap)
    whoosh_html = []
    for i, t0 in enumerate(p["whooshes"]):
        track = 11 + i  # tracks 11, 12, 13, 14, 15, 16
        whoosh_html.append(
            f'      <audio id="wh-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{track}" data-volume="0.45" src="{asset}/audio/sfx/whoosh.mp3"></audio>'
        )

    # Bass-drops on tracks 17+
    bass_html = []
    for i, t0 in enumerate(p["bass_drops"]):
        track = 17 + i
        bass_html.append(
            f'      <audio id="bd-{i}" class="clip" data-start="{t0:.2f}" data-duration="0.55" data-track-index="{track}" data-volume="0.60" src="{asset}/audio/sfx/bass-drop.mp3"></audio>'
        )

    # Camera shake — apply to the root container at each shake time
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

      // === KEN BURNS / STUTTER ZOOM per image ===
{chr(10).join(ken_burns_lines)}

      // === CAPTION ANIMATIONS ===
{hook_anim}
{bridge_anim}
{body_anim}
{outro_anim}

      // === FLASH OVERLAYS ===
{chr(10).join(flash_anim)}

      // === CAMERA SHAKE bursts ===
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
print(f"  total_dur={PILOT['total_dur']}s, images={len(PILOT['images'])}, captions={n_caps}, "
      f"flashes={len(PILOT['flashes'])}, whooshes={len(PILOT['whooshes'])}, bass_drops={len(PILOT['bass_drops'])}, shakes={len(PILOT['shakes'])}")
