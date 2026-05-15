#!/usr/bin/env python3
"""Generate DYNAMIC long-form pilots — v5.

Tighter VOs (eleven_multilingual_v2 + style 0.50 + atempo 1.10 + 0.5s pad).
~15-18 body captions per pilot (every 2-3s) — TikTok pacing.
6-8 image cuts via reuse with different Ken Burns directions.
"""
from pathlib import Path

STYLES = {
    "punch": {
        "bg": "#0a0a0a",
        "hl_color": "rgba(242, 200, 75, 0.62)",
        "hl_text": "#1a1410",
        "cap_color": "#fbf5ef",
        "hook_blur": "blur(14px) brightness(0.45)",
        "scrim_hook": 0.88,
    },
    "red": {
        "bg": "#1a0606",
        "hl_color": "rgba(255, 60, 60, 0.78)",
        "hl_text": "#1a0606",
        "cap_color": "#fbeae8",
        "hook_blur": "blur(14px) brightness(0.38) sepia(0.3) hue-rotate(-25deg)",
        "scrim_hook": 0.85,
    },
}

PILOTS = {
    "pilot-05-sommeil-97": {
        "hook_style": "punch",
        "total_dur": 62,  # VO 58.6s + small CTA tail — minimal silence
        # Timings synced to silencedetect of the v3 VO
        "images": [
            ("00-hook-stat.png",     0,    4, "hook", "in"),
            ("01-screens.png",       4,    6, "body", "in"),
            ("00-hook-stat.png",    10,    3, "body", "out"),
            ("01-screens.png",      13,    9, "body", "left"),
            ("02-notes.png",        22,    8, "body", "in"),
            ("03-phrase.png",       30,    6, "body", "in"),
            ("03-phrase.png",       36,    4, "body", "out"),
            ("04-outro.png",        40,    7, "body", "in"),
            ("02-notes.png",        47,    6, "body", "out"),
            ("04-outro.png",        53,    9, "body", "in"),
        ],
        # Hook 0-3.94s (synced to first major pause)
        "hook_caps": [
            ("97 %",                            0.0, 1.0, "xxl"),
            ("font CETTE erreur",               1.0, 1.5, "white"),
            ("le soir",                         2.6, 1.3, "hl"),
        ],
        # Body caps synced to silence_end times from ffmpeg silencedetect
        "body_caps": [
            ("45 min à s'endormir 😴",          3.95, 3.05, "hl"),
            ("Voici les 3 ERREURS",             7.05, 2.50, "hl"),
            ("ERREUR 1",                        9.65, 1.75, "hl"),
            ("Écrans après 19h",               11.45, 1.95, "white"),
            ("Même la TV en arrière-plan",     13.50, 2.60, "white"),
            ("Cerveau confond jour & nuit",    16.20, 2.30, "hl"),
            ("Passe en LUMIÈRE CHAUDE 💡",      18.55, 2.65, "hl"),
            ("ERREUR 2",                       21.70, 1.20, "hl"),
            ('"va dormir" → anxiété',          22.95, 3.05, "white"),
            ('Dis "on va se CALMER"',          26.05, 3.20, "hl"),
            ("Utilise le mot CALME ✨",         29.35, 3.05, "hl"),
            ("ERREUR 3",                       32.95, 1.10, "hl"),
            ("Tu cèdes à la 3ème demande",     34.15, 2.10, "white"),
            ("Eau · Câlin · Pipi",             36.30, 1.95, "white"),
            ("Tu rentres dans le jeu",         38.30, 2.00, "white"),
            ("Pose les règles AVANT 📋",        40.35, 3.45, "hl"),
            ("1 seule demande max",            43.90, 2.40, "white"),
            ("Lumière chaude · Phrase calme · Règles avant", 46.35, 2.20, "hl"),
            ("Tu gagnes 2h de sommeil 🌙",      48.60, 4.95, "hl"),
            ("Il fait ses NUITS ✨",            53.65, 2.15, "xxl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                  55.85, 2.60, "xxl"),
            ("Partage à un parent épuisé 🤝",  58.50, 3.50, "hl"),
        ],
    },
    "pilot-06-crises-personne": {
        "hook_style": "punch",
        "total_dur": 56,
        "images": [
            ("00-hook-door.png",     0,    4, "hook", "in"),
            ("01-crisis-fist.png",   4,    6, "body", "in"),
            ("01-crisis-fist.png",  10,    4, "body", "out"),
            ("02-silhouette.png",   14,    7, "body", "in"),
            ("02-silhouette.png",   21,    3, "body", "left"),
            ("03-kneeling.png",     24,    8, "body", "in"),
            ("04-calm.png",         32,    7, "body", "in"),
            ("05-outro.png",        39,   17, "body", "in"),
        ],
        "hook_caps": [
            ("Personne",                0.0, 1.0, "xxl"),
            ("ne te dit la VÉRITÉ",     1.0, 1.5, "hl"),
            ("sur les crises",          2.6, 1.4, "white"),
        ],
        "body_caps": [
            ("La moitié des parents",              4.0, 2.5, "white"),
            ("les gèrent MAL",                     6.6, 2.0, "hl"),
            ("La crise ≠ caprice",                 8.8, 2.5, "hl"),
            ("C'est une SATURATION émotionnelle", 11.4, 3.0, "hl"),
            ("Le cerveau n'a pas les outils",     14.5, 3.0, "white"),
            ("Ce qu'on fait MAL",                 17.6, 2.0, "hl"),
            ("Crier · Menacer · Punir",           19.7, 2.5, "white"),
            ("La crise dure 3× plus longtemps",   22.3, 3.5, "hl"),
            ("Émotions = DANGEREUSES",            25.9, 3.0, "white"),
            ("LA SOLUTION",                       29.0, 2.0, "hl"),
            ("Se baisser à sa hauteur",           31.1, 2.5, "white"),
            ("Une main calme. Pas de mots.",      33.7, 3.0, "white"),
            ("Nommer l'émotion",                  36.8, 2.5, "hl"),
            ('"Tu es très en colère, c\'est dur"', 39.4, 3.5, "white"),
            ("En 90s, l'orage passe 🌤️",          43.0, 3.5, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     46.6, 4.5, "xxl"),
            ("Pour la prochaine crise",           51.2, 4.8, "hl"),
        ],
    },
    "pilot-07-discipline-stop": {
        "hook_style": "red",
        "total_dur": 56,
        "images": [
            ("00-hook-fist.png",     0,    4, "hook", "in"),
            ("01-hands-toy.png",     4,    8, "body", "in"),
            ("01-hands-toy.png",    12,    3, "body", "left"),
            ("02-cart.png",         15,    8, "body", "in"),
            ("02-cart.png",         23,    3, "body", "out"),
            ("03-non-blocks.png",   26,    9, "body", "in"),
            ("03-non-blocks.png",   35,    4, "body", "left"),
            ("04-outro.png",        39,   17, "body", "in"),
        ],
        "hook_caps": [
            ("STOP.",                    0.0, 1.0, "xxl"),
            ("Tu disciplines",           1.0, 1.5, "white"),
            ("pour RIEN",                2.6, 1.4, "hl"),
        ],
        "body_caps": [
            ("3 comportements NORMAUX",           4.0, 2.5, "hl"),
            ("punis à tort",                      6.6, 2.0, "white"),
            ("N°1 — Refuser de partager",         8.7, 2.5, "hl"),
            ("à 2 ans",                          11.3, 1.5, "white"),
            ("Ce n'est PAS de l'égoïsme",         12.9, 2.5, "white"),
            ("C'est neurologique",                15.5, 2.5, "hl"),
            ("N°2 — Crise au supermarché",       18.1, 2.5, "hl"),
            ("Ce n'est PAS du caprice",           20.7, 2.5, "white"),
            ("SURCHARGE sensorielle",             23.3, 2.5, "hl"),
            ("Lumières · Bruits · Foule",         25.9, 2.5, "white"),
            ('N°3 — Dire "NON" à tout',           28.5, 2.5, "hl"),
            ("Ce n'est PAS de la défiance",       31.1, 2.5, "white"),
            ("Il découvre qu'il EXISTE",          33.7, 3.0, "hl"),
            ("Pas besoin de PUNIR 💛",            36.8, 3.0, "hl"),
            ("Présence · Patience · Temps",       39.9, 4.0, "white"),
            ("Il devient grand, c'est tout",      44.0, 3.5, "white"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     47.6, 4.5, "xxl"),
            ("Pour un parent qui doute",          52.2, 3.8, "hl"),
        ],
    },
}

def ken_burns_anim(sid, start, dur, kind, direction):
    """Build a GSAP Ken Burns line based on direction."""
    if kind == "hook":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.25 }}, {{ scale: 1.40, duration: {dur}, ease: "none" }}, {start});'
    # Body: 4 directions
    if direction == "in":   # zoom in
        return f'      tl.fromTo("#{sid}", {{ scale: 1.02 }}, {{ scale: 1.12, duration: {dur}, ease: "none" }}, {start});'
    if direction == "out":  # zoom out
        return f'      tl.fromTo("#{sid}", {{ scale: 1.12 }}, {{ scale: 1.02, duration: {dur}, ease: "none" }}, {start});'
    if direction == "left": # pan left
        return f'      tl.fromTo("#{sid}", {{ scale: 1.08, x: 30 }}, {{ scale: 1.08, x: -30, duration: {dur}, ease: "none" }}, {start});'
    if direction == "right":
        return f'      tl.fromTo("#{sid}", {{ scale: 1.08, x: -30 }}, {{ scale: 1.08, x: 30, duration: {dur}, ease: "none" }}, {start});'
    return f'      tl.fromTo("#{sid}", {{ scale: 1.02 }}, {{ scale: 1.10, duration: {dur}, ease: "none" }}, {start});'

def render(pilot_slug, cfg):
    s = STYLES[cfg["hook_style"]]
    total = cfg["total_dur"]
    asset_prefix = f"pilots/{pilot_slug}/assets"

    img_html_parts = []
    ken_burns_lines = []
    for idx, item in enumerate(cfg["images"]):
        filename, start, dur, kind, direction = item
        sid = f"broll-{idx}"
        cls = "broll-hook" if kind == "hook" else "broll-body"
        img_html_parts.append(
            f'      <img class="clip {cls}" id="{sid}" '
            f'data-start="{start}" data-duration="{dur}" data-track-index="0" '
            f'src="{asset_prefix}/broll/{filename}">'
        )
        ken_burns_lines.append(ken_burns_anim(sid, start, dur, kind, direction))

    def caps_block(caps, track, kind):
        sorted_caps = sorted(enumerate(caps), key=lambda kv: kv[1][1])
        html_parts = []
        anim_parts = []
        for j, (i, (text, t0, dur, kind_cap)) in enumerate(sorted_caps):
            if j + 1 < len(sorted_caps):
                next_t0 = sorted_caps[j+1][1][1]
                eff_dur = min(dur, next_t0 - t0 - 0.02)
            else:
                eff_dur = dur
            inner = f'<span class="hl-mark">{text}</span>' if kind_cap in ("hl", "xxl") else text
            if kind == "body":
                base_size = 86 if kind_cap == "hl" else 80
            else:
                base_size = 210 if kind_cap == "xxl" else (170 if kind_cap == "hl" else 150)
            cls = f"caption-{kind}"
            cid = f"cap-{kind}-{i}"
            # Faster caption fade for dynamism
            fade = 0.08 if kind == "body" else 0.10
            html_parts.append(
                f'      <div class="clip {cls}" id="{cid}" '
                f'data-start="{t0}" data-duration="{eff_dur:.2f}" '
                f'data-track-index="{track}" style="font-size:{base_size}px;">{inner}</div>'
            )
            anim_parts.append(
                f'      tl.from("#{cid}", {{ y: 30, opacity: 0, '
                f'duration: {fade}, ease: "power3.out" }}, {t0});'
            )
        return "\n".join(html_parts), "\n".join(anim_parts)

    hook_html, hook_anim = caps_block(cfg["hook_caps"], 2, "hook")
    body_html, body_anim = caps_block(cfg["body_caps"], 3, "body")
    outro_html, outro_anim = caps_block(cfg["outro_caps"], 4, "outro")

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
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:{s['bg']}; font-family:"Plus Jakarta Sans",sans-serif; }}
      .broll-hook {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter: {s['hook_blur']}; }}
      .broll-body {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
      .scrim-hook {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,{s['scrim_hook']}) 0%, rgba(0,0,0,{s['scrim_hook']-0.5 if s['scrim_hook']-0.5 > 0 else 0.1}) 60%, rgba(0,0,0,0.85) 100%); pointer-events:none; }}
      .scrim-body {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.50) 0%, rgba(0,0,0,0) 35%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.72) 100%); pointer-events:none; }}
      .caption-hook {{
        position:absolute; left:48px; right:48px; top:720px;
        text-align:center; font-weight:900; line-height:0.96;
        color:{s['cap_color']};
        text-shadow:0 6px 28px rgba(0,0,0,0.95), 0 0 18px rgba(0,0,0,0.6);
        letter-spacing:-0.02em;
      }}
      .caption-body {{
        position:absolute; left:60px; right:60px; top:1140px;
        text-align:center; font-weight:800; line-height:1.05;
        color:#fbf5ef;
        text-shadow:0 4px 24px rgba(0,0,0,0.85), 0 0 14px rgba(0,0,0,0.4);
        letter-spacing:-0.01em;
      }}
      .caption-outro {{
        position:absolute; left:48px; right:48px; top:760px;
        text-align:center; font-weight:900; line-height:0.96;
        color:#fbf5ef;
        text-shadow:0 6px 28px rgba(0,0,0,0.95);
        letter-spacing:-0.02em;
      }}
      .hl-mark {{ background:{s['hl_color']}; padding:0 16px; border-radius:8px; color:{s['hl_text']}; }}
      .caption-body .hl-mark {{ background:rgba(242,200,75,0.55); color:#2a2520; padding:0 12px; border-radius:6px; }}
      .caption-outro .hl-mark {{ background:rgba(242,200,75,0.55); color:#2a2520; padding:0 16px; border-radius:8px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{chr(10).join(img_html_parts)}

      <div class="clip scrim-hook" id="scrim-hook" data-start="0" data-duration="3.5" data-track-index="1"></div>
      <div class="clip scrim-body" id="scrim-body" data-start="3.5" data-duration="{total - 3.5}" data-track-index="1"></div>

{hook_html}
{body_html}
{outro_html}

      <audio id="voiceover" class="clip" data-start="0" data-duration="{total}" data-track-index="10" data-volume="1.0" src="{asset_prefix}/audio/voiceover.mp3"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="{total}" data-track-index="11" data-volume="0.035" src="{asset_prefix}/audio/music-pad.mp3"></audio>
      <audio id="hook-boom" class="clip" data-start="0" data-duration="0.55" data-track-index="12" data-volume="0.60" src="{asset_prefix}/audio/sfx/hook-boom.mp3"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(ken_burns_lines)}
{hook_anim}
{body_anim}
{outro_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

for slug, cfg in PILOTS.items():
    html = render(slug, cfg)
    Path(f"pilots/{slug}/index.html").write_text(html)
    n_caps = len(cfg["hook_caps"]) + len(cfg["body_caps"]) + len(cfg["outro_caps"])
    print(f"  {slug}: dur={cfg['total_dur']}s, {len(cfg['images'])} img cuts, {n_caps} captions")
