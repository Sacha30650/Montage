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
        "total_dur": 63,  # VO 63s — 0 silent hold
        "images": [
            ("00-hook-door.png",      0,    4, "hook", "in"),
            ("01-crisis-fist.png",    4,    7, "body", "in"),
            ("01-crisis-fist.png",   11,    6, "body", "out"),
            ("02-silhouette.png",    17,    6, "body", "in"),
            ("02-silhouette.png",    23,    7, "body", "left"),
            ("03-kneeling.png",      30,    8, "body", "in"),
            ("03-kneeling.png",      38,    6, "body", "out"),
            ("04-calm.png",          44,    9, "body", "in"),
            ("04-calm.png",          53,    6, "body", "out"),
            ("05-outro.png",         59,    4, "body", "in"),
        ],
        "hook_caps": [
            ("Personne",                       0.0, 1.0, "xxl"),
            ("ne te dit la VÉRITÉ",            1.0, 1.5, "hl"),
            ("sur les crises",                 2.6, 1.4, "white"),
        ],
        # Synced to silencedetect of v3 VO (63s)
        "body_caps": [
            ("Moitié des parents = MAL",       3.98, 2.90, "hl"),
            ("La crise ≠ caprice",             6.88, 4.33, "hl"),
            ("SATURATION émotionnelle",       11.21, 3.92, "hl"),
            ("Pas encore les outils mentaux", 15.13, 2.00, "white"),
            ("Ce qu'on fait MAL",             17.08, 2.02, "hl"),
            ("Crier · Menacer · Punir",       19.10, 3.56, "white"),
            ("Crise ×3 plus longue",          22.66, 4.33, "hl"),
            ("Émotions = DANGEREUSES",        26.99, 2.18, "white"),
            ("LA MÉTHODE en 3 étapes",        29.17, 1.33, "hl"),
            ("Étape 1",                       30.50, 2.93, "hl"),
            ("Te baisser à ses YEUX",         33.43, 4.58, "white"),
            ("Étape 2",                       38.01, 1.31, "hl"),
            ("Main calme · Sans serrer",      39.32, 2.28, "white"),
            ("Étape 3",                       41.60, 2.40, "hl"),
            ("Nomme l'ÉMOTION",               43.99, 2.93, "hl"),
            ('"Tu es très en colère"',        46.92, 3.46, "white"),
            ('"Je suis là"',                  50.38, 2.76, "white"),
            ("Pas de leçon · PRÉSENCE",       53.14, 3.69, "hl"),
            ("90s, l'orage passe 🌤️",         56.83, 1.91, "hl"),
            ("Compétence pour la VIE",        58.74, 2.29, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                 61.03, 1.97, "xxl"),
        ],
    },
    "pilot-07-discipline-stop": {
        "hook_style": "red",
        "total_dur": 64,  # VO 64s — 0 silent hold
        "images": [
            ("00-hook-fist.png",      0,    4, "hook", "in"),
            ("01-hands-toy.png",      4,    8, "body", "in"),
            ("00-hook-fist.png",     12,    5, "body", "out"),
            ("01-hands-toy.png",     17,   11, "body", "left"),
            ("02-cart.png",          28,    7, "body", "in"),
            ("02-cart.png",          35,    9, "body", "out"),
            ("03-non-blocks.png",    44,    8, "body", "in"),
            ("03-non-blocks.png",    52,    8, "body", "left"),
            ("04-outro.png",         60,    4, "body", "in"),
        ],
        "hook_caps": [
            ("STOP.",                          0.0, 1.0, "xxl"),
            ("Tu disciplines",                 1.0, 1.4, "white"),
            ("pour RIEN",                      2.4, 1.1, "hl"),
        ],
        "body_caps": [
            ("3 comportements NORMAUX",        5.59, 2.50, "hl"),
            ("punis à tort",                   8.09, 2.94, "white"),
            ("N°1 — Refuser de partager",     11.03, 3.00, "hl"),
            ("à 2 ans",                       14.03, 1.13, "white"),
            ("Pas de l'égoïsme",              15.16, 2.61, "white"),
            ("C'est NEUROLOGIQUE",            17.77, 2.73, "hl"),
            ("Le partage s'apprend après 3 ans", 20.50, 3.81, "white"),
            ("Joue à côté · Pas avec",        24.31, 3.79, "hl"),
            ("N°2 — Crise au supermarché",    28.10, 3.89, "hl"),
            ("Pas du caprice",                31.99, 3.01, "white"),
            ("SURCHARGE sensorielle",         35.00, 3.13, "hl"),
            ("Lumières · Bruits · Foule",     38.13, 2.29, "white"),
            ("Sors 5 min dehors",             40.42, 4.47, "hl"),
            ("N°3 — Dire NON à tout",         44.89, 3.85, "hl"),
            ("Pas de la défiance",            48.74, 2.59, "white"),
            ("Apprentissage de SOI",          51.33, 2.26, "hl"),
            ("Il découvre qu'il EXISTE",      53.59, 4.93, "hl"),
            ("Donne 2 options à choisir",     58.52, 3.05, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                 61.57, 2.43, "xxl"),
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
