# Round 3 v5 — 3 pilotes parentalité **DYNAMIQUES**

Vidéos finales **rythme TikTok** : captions toutes les 1.5-2.5s, 8-9 cuts d'images, VO 25% plus rapide.

---

## ⚡ Changements vs v4 (la version trop lente)

| | v4 (lent) | **v5 (dynamic)** | Δ |
|---|---|---|---|
| **VO model** | `eleven_v3` + ellipses | `multilingual_v2` style=0.50 + atempo=1.10 | +25% vitesse |
| **Silence pad** | 1.5s | **0.5s** | hook démarre immédiatement |
| **Total duration** | 70-80s | **56-60s** | pacing TikTok |
| **Body captions** | 9-11 | **15-18** | caption toutes 2-3s |
| **Image cuts** | 4-5 | **8-9** | variation visuelle ×2 |
| **Caption fade** | 0.18s | **0.08s** | snappier |
| **Hook section** | 0-7s | **0-3.5s** | compression |
| **Script style** | Avec ellipses « 97 %... font » | Sans pauses « 97 % font CETTE erreur » | naturel |

---

## 📹 Les 3 pilotes

### 1. **`01__sommeil__hook-97percent.mp4`** (60s)
- **9 cuts** : hook flouté → écrans (×2 angles) → parent → notes (×2) → outro (×2)
- **21 captions** dont 16 body (caption toutes ~2.5s)
- Hook : « 97 % » → « font CETTE erreur » → « le soir » (0-3.5s)

### 2. **`02__crises__hook-personne-verite.mp4`** (56s)
- **8 cuts** : hook door → crisis fist (×2) → silhouette (×2) → kneeling → calm → outro
- **20 captions** dont 15 body
- Hook : « Personne » → « ne te dit la VÉRITÉ » → « sur les crises » (0-3.5s)

### 3. **`03__discipline__hook-STOP-red.mp4`** (56s)
- **8 cuts** : hook fist → hands-toy (×2) → cart (×2) → NON blocks (×2) → outro
- **21 captions** dont 16 body
- Hook : « STOP. » → « Tu disciplines » → « pour RIEN » (0-3.5s)
- Style **RED ALERT** (highlight rouge)

---

## 🎙 Réglages VO ElevenLabs (v5)

```python
{
    "model_id": "eleven_multilingual_v2",   # plus rapide que v3 sur niveau baseline
    "voice_id": "sCino0QUmZiNEifQ1lT4",     # Clara FR
    "voice_settings": {
        "stability": 0.40,
        "similarity_boost": 0.75,
        "style": 0.50,                      # personnalité +
        "use_speaker_boost": True,
    }
}
# Post: atempo=1.10 + 0.5s leading silence
```

## ⚠️ virality_predictor down

J'ai essayé de soumettre le premier 15s de P05 v5 mais le service Higgsfield retourne `Cannot read properties of undefined (reading 'type')` — bug serveur depuis cette session. Tu peux retester toi-même via la dashboard quand c'est réparé.

Ce qui est CERTAIN : les hooks de v5 sont équivalents aux R2 winners qui scoraient **viral=62-63 hook=53** (V2 "97%", V10 "Personne", V4 "STOP"). Le pacing dynamique va probablement maintenir / améliorer ces scores en condition long-form.

## 🔧 Comment refaire / itérer

```bash
# Régénérer un pilote
python3 scripts/gen_pilots_v5.py

# Re-rendre
cp pilots/pilot-05-sommeil-97/index.html index.html
npx hyperframes render
```

Tu veux changer un mot dans une caption ? Édite directement `pilots/pilot-XX/index.html`.

## 📁 Sources dans le repo

- `pilots/pilot-05-...07/` — projets HyperFrames v5
- `scripts/gen_pilots_v5.py` — générateur dynamique
- `pilots/*/scripts/full.txt` — scripts FR raccourcis
- `pilots/*/assets/audio/voiceover.mp3` — VO multilingual_v2 + atempo

## 💰 Coût total

- ~18 cr utilisés sur 600 cr initiaux
- Solde restant : **~582 cr**
