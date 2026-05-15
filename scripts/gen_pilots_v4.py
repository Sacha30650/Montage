#!/usr/bin/env python3
"""Generate long-form pilots — VERSION 4.

Uses ElevenLabs v3 voiceovers (more expressive) with timings adjusted to
natural phrase boundaries detected via ffmpeg silencedetect.

VO format: 1.5s leading silence pad + raw v3 audio (no atempo, no speed-up).

Total durations:
- pilot-05: 75s (VO 67s + outro hold)
- pilot-06: 70s (VO 62s + outro hold)
- pilot-07: 80s (VO 72s + outro hold)
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
        "total_dur": 75,
        "images": [
            ("00-hook-stat.png",     0,  9, "hook"),
            ("01-screens.png",       9, 16, "body"),
            ("03-phrase.png",       25, 13, "body"),
            ("02-notes.png",        38, 16, "body"),
            ("04-outro.png",        54, 21, "body"),
        ],
        # Hook caps: 0-7s (silence pad 1.5s + "97 pour cent...le soir" ends ~7s)
        "hook_caps": [
            ("97 %",                    0.0, 2.0, "xxl"),
            ("font CETTE erreur",       2.2, 3.0, "white"),
            ("le soir",                 5.3, 2.5, "hl"),
        ],
        # Body caps: align with natural pauses (8-62s)
        "body_caps": [
            ("Voici les 3 ERREURS du soir",        8.0, 5.0, "hl"),
            ("ERREUR 1 — Les écrans après 19h",   13.5, 6.0, "hl"),
            ("Le cerveau confond jour et nuit",   19.8, 5.5, "white"),
            ("ERREUR 2 — Le mot « DORMIR »",      25.5, 6.0, "hl"),
            ("Dis « on va se calmer »",           31.8, 6.0, "white"),
            ("ERREUR 3 — Tu cèdes à la 3ème demande", 38.0, 5.5, "hl"),
            ("Eau. Câlin. Pipi.",                 43.8, 5.0, "white"),
            ("Pose les RÈGLES AVANT le coucher",  49.0, 6.0, "hl"),
            ("Tu gagnes 2h de sommeil 🌙",         55.2, 7.5, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     63.0, 6.0, "xxl"),
            ("Pour un parent épuisé",             69.2, 5.8, "hl"),
        ],
    },
    "pilot-06-crises-personne": {
        "hook_style": "punch",
        "total_dur": 70,
        "images": [
            ("00-hook-door.png",     0,  8, "hook"),
            ("01-crisis-fist.png",   8, 14, "body"),
            ("02-silhouette.png",   22, 14, "body"),
            ("03-kneeling.png",     36, 12, "body"),
            ("04-calm.png",         48, 10, "body"),
            ("05-outro.png",        58, 12, "body"),
        ],
        # Hook 0-7s during "Personne...sur les crises de colère"
        "hook_caps": [
            ("Personne",                0.0, 2.0, "xxl"),
            ("ne te dit la VÉRITÉ",     2.2, 3.0, "hl"),
            ("sur les crises",          5.3, 2.5, "white"),
        ],
        "body_caps": [
            ("La crise n'est PAS un caprice",        7.0, 5.0, "hl"),
            ("C'est une SATURATION émotionnelle",   12.5, 5.5, "hl"),
            ("Le cerveau n'a pas les outils",       18.5, 4.5, "white"),
            ("Ce qu'on fait MAL — crier, punir",    23.5, 5.5, "hl"),
            ("La crise dure 3× plus longtemps",     29.5, 4.5, "white"),
            ("Émotions = DANGEREUSES",              34.2, 4.0, "white"),
            ("La SOLUTION en 4 gestes",             38.5, 4.0, "hl"),
            ("Se baisser à sa hauteur",             42.8, 3.5, "white"),
            ("Nommer l'émotion. Pas de mots.",      46.5, 4.0, "white"),
            ("En 90 secondes, l'orage passe 🌤️",     50.8, 5.5, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     58.0, 5.8, "xxl"),
            ("Pour la prochaine crise",           64.0, 6.0, "hl"),
        ],
    },
    "pilot-07-discipline-stop": {
        "hook_style": "red",
        "total_dur": 80,
        "images": [
            ("00-hook-fist.png",     0,  9, "hook"),
            ("01-hands-toy.png",     9, 16, "body"),
            ("02-cart.png",         25, 14, "body"),
            ("03-non-blocks.png",   39, 17, "body"),
            ("04-outro.png",        56, 24, "body"),
        ],
        # Hook 0-8s during "STOP...pour RIEN"
        "hook_caps": [
            ("STOP.",                    0.0, 2.5, "xxl"),
            ("Tu disciplines",           2.7, 2.5, "white"),
            ("pour RIEN",                5.3, 2.5, "hl"),
        ],
        "body_caps": [
            ("3 comportements NORMAUX punis à tort", 8.5, 6.5, "hl"),
            ("1 — Refuser de partager à 2 ans",     15.5, 6.0, "hl"),
            ("C'est neurologique. Pas l'égoïsme.",  21.8, 5.0, "white"),
            ("2 — Crise au supermarché",            27.0, 6.0, "hl"),
            ("C'est une SURCHARGE sensorielle",     33.2, 5.5, "white"),
            ("3 — Dire « NON » à tout",             39.0, 6.0, "hl"),
            ("C'est l'apprentissage de SOI",        45.2, 5.0, "white"),
            ("Il découvre qu'il existe.",           50.5, 5.5, "white"),
            ("Pas besoin de punir 💛",              56.2, 8.0, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     65.0, 7.0, "xxl"),
            ("Pour un parent qui doute",          72.2, 7.5, "hl"),
        ],
    },
}

def render(pilot_slug, cfg):
    s = STYLES[cfg["hook_style"]]
    total = cfg["total_dur"]
    asset_prefix = f"pilots/{pilot_slug}/assets"

    img_html_parts = []
    ken_burns_lines = []
    for idx, (filename, start, dur, kind) in enumerate(cfg["images"]):
        sid = f"broll-{idx}"
        cls = "broll-hook" if kind == "hook" else "broll-body"
        img_html_parts.append(
            f'      <img class="clip {cls}" id="{sid}" '
            f'data-start="{start}" data-duration="{dur}" data-track-index="0" '
            f'src="{asset_prefix}/broll/{filename}">'
        )
        if kind == "hook":
            ken_burns_lines.append(
                f'      tl.fromTo("#{sid}", {{ scale: 1.25 }}, '
                f'{{ scale: 1.40, duration: {dur}, ease: "none" }}, {start});'
            )
        else:
            ken_burns_lines.append(
                f'      tl.fromTo("#{sid}", {{ scale: 1.04 }}, '
                f'{{ scale: 1.12, duration: {dur}, ease: "none" }}, {start});'
            )

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
                base_size = 84 if kind_cap == "hl" else 80
            else:
                base_size = 200 if kind_cap == "xxl" else (160 if kind_cap == "hl" else 150)
            cls = f"caption-{kind}"
            cid = f"cap-{kind}-{i}"
            html_parts.append(
                f'      <div class="clip {cls}" id="{cid}" '
                f'data-start="{t0}" data-duration="{eff_dur:.2f}" '
                f'data-track-index="{track}" style="font-size:{base_size}px;">{inner}</div>'
            )
            anim_parts.append(
                f'      tl.from("#{cid}", {{ y: 40, opacity: 0, '
                f'duration: 0.18, ease: "power3.out" }}, {t0});'
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

      <div class="clip scrim-hook" id="scrim-hook" data-start="0" data-duration="7" data-track-index="1"></div>
      <div class="clip scrim-body" id="scrim-body" data-start="7" data-duration="{total - 7}" data-track-index="1"></div>

{hook_html}
{body_html}
{outro_html}

      <audio id="voiceover" class="clip" data-start="0" data-duration="{total}" data-track-index="10" data-volume="1.0" src="{asset_prefix}/audio/voiceover.mp3"></audio>
      <audio id="music" class="clip" data-start="0" data-duration="{total}" data-track-index="11" data-volume="0.025" src="{asset_prefix}/audio/music-pad.mp3"></audio>
      <audio id="hook-boom" class="clip" data-start="0" data-duration="0.55" data-track-index="12" data-volume="0.55" src="{asset_prefix}/audio/sfx/hook-boom.mp3"></audio>
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
    print(f"  generated pilots/{slug}/index.html  (dur={cfg['total_dur']}s, "
          f"{len(cfg['images'])} images, "
          f"{len(cfg['hook_caps']) + len(cfg['body_caps']) + len(cfg['outro_caps'])} captions)")
