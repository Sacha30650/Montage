#!/usr/bin/env python3
"""Generate long-form pilots (60+s) using R2 winning hook styles.

Structure per pilot:
- 0-5s    HOOK (PUNCH or RED) — text-first big captions, blurred image
- 5-50s   BODY (COSY slow) — 3-4 image segments, bottom captions
- 50-62s  OUTRO (PUNCH) — text-first CTA captions
"""
from pathlib import Path

# Style palettes
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

# Per-pilot configs
PILOTS = {
    "pilot-05-sommeil-97": {
        "hook_style": "punch",
        "total_dur": 62,
        "images": [
            # (filename, start, duration, kind="hook"|"body")
            ("00-hook-stat.png",     0,  5, "hook"),
            ("01-screens.png",       5, 13, "body"),
            ("03-phrase.png",       18, 12, "body"),
            ("02-notes.png",        30, 12, "body"),
            ("04-outro.png",        42, 20, "body"),
        ],
        "hook_caps": [
            ("97 %",                    0.0, 1.2, "xxl"),
            ("font CETTE erreur",       1.4, 1.8, "white"),
            ("le soir",                 3.4, 1.6, "hl"),
        ],
        "body_caps": [
            ("Voici les 3 ERREURS du soir",        5.2, 3.6, "hl"),
            ("ERREUR 1 — Les écrans après 19h",    9.0, 4.3, "hl"),
            ("Le cerveau confond jour et nuit",   13.5, 4.3, "white"),
            ("ERREUR 2 — Le mot « DORMIR »",      18.0, 4.8, "hl"),
            ("Dis « on va se calmer » à la place",23.0, 6.8, "white"),
            ("ERREUR 3 — Tu cèdes à la 3ème demande", 30.0, 3.3, "hl"),
            ("Eau. Câlin. Pipi.",                 33.5, 4.3, "white"),
            ("Pose les RÈGLES avant le coucher",  38.0, 4.8, "hl"),
            ("Tu gagnes 2h de sommeil 🌙",         43.0, 6.8, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     50.0, 5.8, "xxl"),
            ("Pour un parent épuisé",             56.0, 6.0, "hl"),
        ],
    },
    "pilot-06-crises-personne": {
        "hook_style": "punch",
        "total_dur": 62,
        "images": [
            ("00-hook-door.png",     0,  5, "hook"),
            ("01-crisis-fist.png",   5, 12, "body"),
            ("02-silhouette.png",   17, 13, "body"),
            ("03-kneeling.png",     30, 11, "body"),
            ("04-calm.png",         41,  9, "body"),
            ("05-outro.png",        50, 12, "body"),
        ],
        "hook_caps": [
            ("Personne",                0.0, 1.3, "xxl"),
            ("ne te dit la VÉRITÉ",     1.5, 2.0, "hl"),
            ("sur les crises",          3.6, 1.4, "white"),
        ],
        "body_caps": [
            ("La crise N'EST PAS un caprice",       5.2, 3.6, "hl"),
            ("C'est une SATURATION émotionnelle",   9.0, 3.8, "hl"),
            ("Le cerveau n'a pas les outils",      13.0, 3.8, "white"),
            ("Ce qu'on fait MAL — crier, punir",   17.2, 4.6, "hl"),
            ("La crise dure 3× plus longtemps",    22.0, 3.8, "white"),
            ("L'enfant apprend : émotions = danger", 26.0, 3.8, "white"),
            ("La SOLUTION en 4 gestes",            30.0, 3.8, "hl"),
            ("Se baisser à sa hauteur",            34.0, 3.0, "white"),
            ("Nommer l'émotion. Pas de mots.",     37.2, 3.6, "white"),
            ("En 90 secondes, l'orage passe 🌤️",    41.0, 5.0, "hl"),
            ("Compétence pour la vie",             46.2, 3.6, "white"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     50.0, 5.8, "xxl"),
            ("Pour la prochaine crise",           56.0, 6.0, "hl"),
        ],
    },
    "pilot-07-discipline-stop": {
        "hook_style": "red",
        "total_dur": 62,
        "images": [
            ("00-hook-fist.png",     0,  5, "hook"),
            ("01-hands-toy.png",     5, 13, "body"),
            ("02-cart.png",         18, 10, "body"),
            ("03-non-blocks.png",   28, 14, "body"),
            ("04-outro.png",        42, 20, "body"),
        ],
        "hook_caps": [
            ("STOP.",                    0.0, 1.0, "xxl"),
            ("Tu disciplines",           1.2, 1.3, "white"),
            ("pour RIEN",                2.6, 2.4, "hl"),
        ],
        "body_caps": [
            ("3 comportements NORMAUX punis à tort", 5.2, 4.6, "hl"),
            ("1 — Refuser de partager à 2 ans",   10.0, 4.0, "hl"),
            ("C'est neurologique. Pas l'égoïsme.",14.2, 3.6, "white"),
            ("2 — Crise au supermarché",          18.0, 4.6, "hl"),
            ("C'est de la SURCHARGE sensorielle", 23.0, 4.8, "white"),
            ("3 — Dire « NON » à tout",           28.0, 4.0, "hl"),
            ("C'est l'apprentissage de SOI",      32.2, 4.0, "white"),
            ("Il découvre qu'il existe.",         36.4, 5.4, "white"),
            ("Pas besoin de punir 💛",            42.0, 8.0, "hl"),
        ],
        "outro_caps": [
            ("Sauvegarde 💾",                     50.0, 5.8, "xxl"),
            ("Pour un parent qui doute",          56.0, 6.0, "hl"),
        ],
    },
}

# ------------------------------------------------------------------
# HTML template
# ------------------------------------------------------------------
def render(pilot_slug, cfg):
    s = STYLES[cfg["hook_style"]]
    # Shift body/outro by 1.5s — VO has 1.5s leading silence so the hook visual
    # breathes before VO kicks in (replicates short-test V2 pattern).
    VO_PAD = 1.5
    total = cfg["total_dur"] + VO_PAD
    asset_prefix = f"pilots/{pilot_slug}/assets"

    # Build images. Hook image is extended by VO_PAD (it stays visible during the silence).
    # Body images are shifted by VO_PAD.
    img_html_parts = []
    ken_burns_lines = []
    for idx, (filename, start, dur, kind) in enumerate(cfg["images"]):
        sid = f"broll-{idx}"
        cls = "broll-hook" if kind == "hook" else "broll-body"
        if kind == "hook":
            img_start = start  # stays at 0
            img_dur = dur + VO_PAD  # extends to cover the silence
        else:
            img_start = start + VO_PAD
            img_dur = dur
        img_html_parts.append(
            f'      <img class="clip {cls}" id="{sid}" '
            f'data-start="{img_start}" data-duration="{img_dur}" data-track-index="0" '
            f'src="{asset_prefix}/broll/{filename}">'
        )
        # Ken Burns per image: slight scale animation over its window
        if kind == "hook":
            ken_burns_lines.append(
                f'      tl.fromTo("#{sid}", {{ scale: 1.25 }}, '
                f'{{ scale: 1.40, duration: {img_dur}, ease: "none" }}, {img_start});'
            )
        else:
            ken_burns_lines.append(
                f'      tl.fromTo("#{sid}", {{ scale: 1.04 }}, '
                f'{{ scale: 1.12, duration: {img_dur}, ease: "none" }}, {img_start});'
            )
    img_html = "\n".join(img_html_parts)
    ken_burns_anim = "\n".join(ken_burns_lines)

    # Build captions for each phase (hook = track 2, body = track 3, outro = track 4)
    # Hook captions stay at original timings (start at 0). Body/outro shifted by VO_PAD.
    def caps_block(caps, track, kind, shift=0.0):
        sorted_caps = sorted(enumerate(caps), key=lambda kv: kv[1][1])
        html_parts = []
        anim_parts = []
        for j, (i, (text, t0, dur, kind_cap)) in enumerate(sorted_caps):
            t0s = t0 + shift
            if j + 1 < len(sorted_caps):
                next_t0 = sorted_caps[j+1][1][1] + shift
                eff_dur = min(dur, next_t0 - t0s - 0.02)
            else:
                eff_dur = dur
            inner = (
                f'<span class="hl-mark">{text}</span>'
                if kind_cap in ("hl", "xxl") else text
            )
            if kind == "body":
                base_size = 84 if kind_cap == "hl" else 80
            else:
                base_size = 200 if kind_cap == "xxl" else (160 if kind_cap == "hl" else 150)
            cls = f"caption-{kind}"
            cid = f"cap-{kind}-{i}"
            html_parts.append(
                f'      <div class="clip {cls}" id="{cid}" '
                f'data-start="{t0s:.2f}" data-duration="{eff_dur:.2f}" '
                f'data-track-index="{track}" style="font-size:{base_size}px;">{inner}</div>'
            )
            anim_parts.append(
                f'      tl.from("#{cid}", {{ y: 40, opacity: 0, '
                f'duration: 0.18, ease: "power3.out" }}, {t0s});'
            )
        return "\n".join(html_parts), "\n".join(anim_parts)

    hook_html, hook_anim = caps_block(cfg["hook_caps"], 2, "hook", shift=0.0)
    body_html, body_anim = caps_block(cfg["body_caps"], 3, "body", shift=VO_PAD)
    outro_html, outro_anim = caps_block(cfg["outro_caps"], 4, "outro", shift=VO_PAD)

    return f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@1,800&family=Plus+Jakarta+Sans:wght@800;900&display=swap" rel="stylesheet" />
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
{img_html}

      <div class="clip scrim-hook" id="scrim-hook" data-start="0" data-duration="{5 + VO_PAD}" data-track-index="1"></div>
      <div class="clip scrim-body" id="scrim-body" data-start="{5 + VO_PAD}" data-duration="{total - 5 - VO_PAD}" data-track-index="1"></div>

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
{ken_burns_anim}
{hook_anim}
{body_anim}
{outro_anim}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""

# ------------------------------------------------------------------
# Write each pilot
# ------------------------------------------------------------------
for slug, cfg in PILOTS.items():
    html = render(slug, cfg)
    path = Path(f"pilots/{slug}/index.html")
    path.write_text(html)
    print(f"  generated {path}  (style={cfg['hook_style']}, dur={cfg['total_dur']}s, "
          f"{len(cfg['images'])} images, {len(cfg['hook_caps']) + len(cfg['body_caps']) + len(cfg['outro_caps'])} captions)")
