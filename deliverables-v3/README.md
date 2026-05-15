# Round 3 — 3 pilotes long-form parentalité (62s chacun)

Vidéos produites à partir des hooks gagnants validés en round 1+2.
Format : 1080×1920 vertical, 62s exactement, H.264, MP4.

---

## 📹 Les 3 pilotes

### 1. **`01__sommeil__hook-97percent.mp4`** — Sommeil bébé
- **Hook V2-style** (round 2 best hook score, 53/100)
- Texte d'accroche : **« 97 % font CETTE erreur le soir »**
- Style : PUNCH (text-first big captions, jaune)
- Structure (62s) :
  - 0-5s — Hook PUNCH plein écran sur image floutée
  - 5-50s — Body cosy slow : 3 erreurs concrètes (écrans après 19h, mot « dormir », céder à la 3ème demande) + solution
  - 50-62s — Outro CTA : « Sauvegarde » → « Pour un parent épuisé »
- 5 images B-roll (1 hook, 4 body)

### 2. **`02__crises__hook-personne-verite.mp4`** — Crises de colère
- **Hook V10-style** (round 2 best viral score, 63/100)
- Texte d'accroche : **« Personne ne te dit la VÉRITÉ sur les crises »**
- Style : PUNCH (text-first big captions, jaune)
- Structure (62s) :
  - 0-5s — Hook PUNCH curiosity-driven sur image floutée
  - 5-50s — Body cosy : reframe neuro (saturation émotionnelle), ce qu'on fait mal vs la méthode 90 sec
  - 50-62s — Outro CTA : « Sauvegarde » → « Pour la prochaine crise »
- 6 images B-roll (1 hook, 5 body)

### 3. **`03__discipline__hook-STOP-red.mp4`** — Discipline / 3 comportements normaux
- **Hook V4-style** (round 2 brain engagement 63/100)
- Texte d'accroche : **« STOP. Tu disciplines pour RIEN »**
- Style : **RED ALERT** (text-first + highlight rouge, urgence)
- Structure (62s) :
  - 0-5s — Hook RED ALERT pattern interrupt
  - 5-50s — Body cosy : 3 comportements parfaitement normaux (refus partage 2 ans, supermarché, « non » à tout)
  - 50-62s — Outro : « Pas besoin de punir 💛 » → « Sauvegarde » → « Pour un parent qui doute »
- 5 images B-roll (1 hook, 4 body)

---

## 🎯 Prédictions virality_predictor (hooks 15s extraits)

Le predictor cap à 16s, donc on a testé les **15 premières secondes** de chaque pilote pour valider que le hook tient en format long.

(Résultats en cours — voir `tests/hooks/pilots-v3-hooks/` quand jobs finissent)

---

## 🔧 Comment regénérer

```bash
# Régénérer un pilote à partir de son config Python
python3 scripts/gen_pilots_v3.py

# Rendre un pilote spécifique
cp pilots/pilot-05-sommeil-97/index.html index.html
npx hyperframes render
# Output dans renders/
```

## 📁 Sources dans le repo

- `pilots/pilot-05-sommeil-97/` — projet HyperFrames sommeil
- `pilots/pilot-06-crises-personne/` — projet HyperFrames crises
- `pilots/pilot-07-discipline-stop/` — projet HyperFrames discipline
- `scripts/gen_pilots_v3.py` — générateur de templates
- `tests/hooks/pilots-v3-hooks/` — extraits 15s soumis au predictor

## 💰 Coût round 3

- 7 nouvelles images nano_banana_flash : **10.5 cr**
- 3 VOs ElevenLabs : free
- 3 renders locaux : free
- 3 hooks-15s virality_predictor : free
- Solde avant : 579 cr → après : **~568 cr**

## 🚀 Insights de fabrication

Les 3 pilotes appliquent **exactement** la recette gagnante du round 2 :
1. **PUNCH style** pour les 5 premières secondes (texte massif text-first, image floutée)
2. **COSY slow** pour le body (5-50s) — image claire, caption au bas, Ken Burns lent
3. **PUNCH style** pour l'outro CTA (50-62s) — texte centré, image cosy en arrière-plan
4. **Hooks chiffrés / curiosity / commandement** placés sur les 1-3 premières secondes
5. **Premier caption = MOT SEUL** affiché 1-1.3s en gros (200px) pour maximiser le hook score

Tu peux tester ces 3 vidéos sur tes plateformes (TikTok/Reels/Shorts) et comparer les vraies métriques (view-through, save rate, share rate) avec ce que le predictor a annoncé.
