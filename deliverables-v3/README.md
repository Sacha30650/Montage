# Round 3 v4 — 3 pilotes long-form parentalité (ElevenLabs v3)

Vidéos finales **avec VO ElevenLabs v3** (modèle 2025, intonation naturelle).
Format : 1080×1920 vertical, 70-80s, H.264, MP4.

---

## ⚡ Changements vs version précédente

**Avant** (v2 du multilingual v2) :
- Modèle `eleven_multilingual_v2` (2023, prosodie plate)
- `stability=0.55`, `style=0.15` → monotone
- `atempo=1.08` post-traitement → voix compressée, intonation déformée
- Scripts plats sans marqueurs de prosodie

**Maintenant** (v4 avec v3) :
- Modèle `eleven_v3` (le plus expressif, 74 langues)
- `stability=0.35` (variation naturelle), `use_speaker_boost=True`
- **Aucun atempo** — rythme naturel respecté
- Scripts ré-écrits avec **ellipses, virgules, CAPS** pour l'emphase
  - Ex: `« 97 pour cent des parents... font CETTE erreur le soir. »`
  - Pauses sur ellipses (...) → suspense
  - CAPS → emphase audio
  - Virgules placées pour micro-respirations

---

## 📹 Les 3 pilotes

### 1. **`01__sommeil__hook-97percent.mp4`** (75s)
- Hook : **« 97 % font CETTE erreur le soir »** (V2-style, viral 62)
- Body : 3 erreurs concrètes (écrans après 19h, mot « DORMIR », céder à la 3ème demande)
- Outro : Sauvegarde 💾 — Pour un parent épuisé
- VO v3 raw : 66s + 1.5s silence pad

### 2. **`02__crises__hook-personne-verite.mp4`** (70s)
- Hook : **« Personne ne te dit la VÉRITÉ sur les crises »** (V10-style, viral 63)
- Body : reframe émotionnel + erreurs courantes + méthode 90s
- Outro : Sauvegarde 💾 — Pour la prochaine crise
- VO v3 raw : 61s + 1.5s silence pad

### 3. **`03__discipline__hook-STOP-red.mp4`** (80s)
- Hook : **« STOP. Tu disciplines pour RIEN »** (V4-style, brain 63, RED ALERT)
- Body : 3 comportements normaux mal compris (refus partage à 2 ans, supermarché, « non »)
- Outro : Pas besoin de punir 💛 — Sauvegarde 💾 — Pour un parent qui doute
- VO v3 raw : 71s + 1.5s silence pad

---

## 🎬 Structure (validée R2)

```
0-1.5s     SILENCE — caption MOT/CHIFFRE 200px + hook-boom SFX
1.5-7s     VO commence + hook captions sur image floutée
7-(N-12)s  BODY cosy slow — captions au bas, images cosy en succession
(N-12)s-N  OUTRO CTA — caption gros + image cosy finale
```

## 🎙 Réglages ElevenLabs v3 utilisés

```python
{
    "model_id": "eleven_v3",
    "voice_id": "sCino0QUmZiNEifQ1lT4",  # Clara FR
    "voice_settings": {
        "stability": 0.35,           # variation expressive
        "similarity_boost": 0.75,
        "use_speaker_boost": True,
    }
}
```

> Note : v3 ne supporte plus le paramètre `style` (remplacé par le contrôle via le texte avec ellipses, CAPS, ponctuation). La prosodie vient de l'écriture du script lui-même.

## 📦 Comment publier

1. Télécharger un .mp4 via GitHub Raw ou le clone du repo
2. Importer dans TikTok / Reels / Shorts (formats vertical 9:16)
3. Description suggérée : recopier le hook texte + le contenu informatif
4. Hashtags niche : `#parentalité #educationpositive #sommeilbebe #crisesenfant #disciplinepositive #parentexhausted`

## 📁 Sources dans le repo

- `pilots/pilot-05-sommeil-97/` — projet HyperFrames
- `pilots/pilot-06-crises-personne/` — projet HyperFrames
- `pilots/pilot-07-discipline-stop/` — projet HyperFrames
- `scripts/gen_pilots_v4.py` — générateur Python (modifiable)
- `pilots/*/assets/audio/voiceover-v3-raw.mp3` — VO v3 brut (avant pad)
- `pilots/*/assets/audio/voiceover.mp3` — VO finale (avec pad 1.5s)

## 💰 Coût total cumulé

- R1 (test hooks) : 7.5 cr
- R2 (test hooks v2) : 0 cr
- R3 (3 pilotes images) : 10.5 cr
- R4 (re-gen v3 VOs) : 0 cr (free)
- **Total** : 18 cr sur ~600 cr initiaux
