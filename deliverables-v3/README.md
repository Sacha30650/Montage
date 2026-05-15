# Round 3 — 3 pilotes long-form parentalité (63.5s chacun)

Vidéos finales prêtes pour publication TikTok / Reels / Shorts.
Format : 1080×1920 vertical, 63.5s, H.264, MP4.

---

## 📹 Les 3 pilotes

### 1. **`01__sommeil__hook-97percent.mp4`** — Sommeil bébé (PUNCH)
- **Hook V2-style** (round 2 best hook score : 53/100, viral 62)
- Texte d'accroche : **« 97 % font CETTE erreur le soir »**
- Style : PUNCH (text-first big captions, jaune)
- 0-1.5s : silence visual — caption « 97 % » flashe en gros + hook-boom SFX
- 1.5-6.5s : VO démarre, captions hook continuent
- 6.5-55s : Body cosy slow — 3 erreurs (écrans après 19h, mot « DORMIR », céder à la 3ème demande)
- 55-63.5s : Outro CTA « Sauvegarde 💾 » → « Pour un parent épuisé »
- 5 images B-roll (1 hook, 4 body)

### 2. **`02__crises__hook-personne-verite.mp4`** — Crises de colère (PUNCH)
- **Hook V10-style** (round 2 best viral : 63/100, hook 49)
- Texte d'accroche : **« Personne ne te dit la VÉRITÉ sur les crises »**
- Style : PUNCH (text-first, jaune, curiosity-driven)
- 0-1.5s : silence visual — caption « Personne » flashe
- 1.5-6.5s : VO + captions hook
- 6.5-55s : Body cosy — reframe neuro (saturation émotionnelle), erreurs courantes, méthode 90 secondes
- 55-63.5s : Outro CTA « Sauvegarde 💾 » → « Pour la prochaine crise »
- 6 images B-roll (1 hook, 5 body)

### 3. **`03__discipline__hook-STOP-red.mp4`** — Discipline / 3 comportements normaux (RED ALERT)
- **Hook V4-style** (round 2 best brain engagement : 63/100, viral 62)
- Texte d'accroche : **« STOP. Tu disciplines pour RIEN »**
- Style : RED ALERT (text-first + highlight rouge, urgence/pattern interrupt)
- 0-1.5s : silence visual — caption « STOP. » rouge flashe + hook-boom SFX
- 1.5-6.5s : VO + captions hook
- 6.5-55s : Body cosy — 3 comportements normaux mal compris (refus partage à 2 ans, supermarché, « non » à tout)
- 55-63.5s : Outro CTA « Pas besoin de punir 💛 » → « Sauvegarde 💾 » → « Pour un parent qui doute »
- 5 images B-roll (1 hook, 4 body)

---

## 🎯 Recettes appliquées (validées en round 1+2)

Chaque pilote utilise **la recette gagnante**, plafond viral=62-63 sur tests 15s :

```
HOOK (0-6.5s)
├─ 0-1.5s    Visual punch SILENCIEUX : caption "MOT/CHIFFRE" géant (200px)
│            + hook-boom SFX, image floutée
├─ 1.5s      VO démarre (a 1.5s pour laisser le hook respirer)
└─ 1.5-6.5s  Captions hook complets sur image floutée

BODY (6.5-55s)
├─ Image cosy claire en plein écran avec Ken Burns slow
├─ Captions au bas, taille moyenne (84px), highlight jaune sur mots-clés
└─ Image change toutes les 10-13s avec le sujet

OUTRO (55-63.5s)
└─ Captions CTA centrées en gros (200px), image cosy finale en fond
```

## 🔍 À propos des scores du predictor

J'ai testé les **15 premières secondes** de chaque pilote sur virality_predictor. Les scores sortent **plus bas** que les tests 15s isolés du round 2 :
- Pilot 05 (v1 sans padding) : viral=44, hook=27 (vs V2 isolé viral=62, hook=53)
- Pilot 06 (v1 sans padding) : viral=47, hook=34 (vs V10 isolé viral=63, hook=49)

**Pourquoi ce décalage ?**
Le predictor analyse les 15 premières secondes seulement. Dans le pilote long-form, ces 15s contiennent déjà du body content (image qui change à 5s, VO continue). Dans les tests 15s isolés, toute la vidéo EST le hook → format optimisé pour le predictor.

**La v2 (rendue ici) ajoute 1.5s de silence visuel au début** pour reproduire le pattern du test isolé : punch visual silencieux puis VO. Re-tests predictor au moment du push (à valider à la prochaine session si le service répond — il a planté ce soir avec « Cannot read properties of undefined (reading 'type') »).

**Important** : le score predictor n'est pas une vérité absolue pour le long-form. Le predictor est calibré pour du 15s where every second counts. Pour du 60s d'éducation, ce qui compte vraiment en vrai = save rate + share rate + complétion → métriques que seul TikTok/Reels mesure.

---

## 📦 Comment publier

1. Télécharger un des `.mp4` du dossier (clic droit → enregistrer sous, ou via GitHub Raw)
2. Importer dans TikTok / Reels / Shorts
3. Description suggérée : repartir du hook texte + le contenu informatif
4. Hashtags niche : `#parentalité #parentexhausted #educationpositive #sommeilbebe #crisesenfant #disciplinepositive`

## 📁 Sources dans le repo

- `pilots/pilot-05-sommeil-97/` — projet HyperFrames sommeil
- `pilots/pilot-06-crises-personne/` — projet HyperFrames crises
- `pilots/pilot-07-discipline-stop/` — projet HyperFrames discipline
- `scripts/gen_pilots_v3.py` — générateur de templates (modifiable)
- `tests/hooks/pilots-v3-hooks/` — extraits 15s pour le predictor

## 💰 Coût round 3

- 7 nouvelles images nano_banana_flash : **10.5 cr**
- 3 VOs ElevenLabs : free
- 6 renders locaux (1ère + 2ème version padded) : free
- predictor : free (mais buggé sur cette session)
- Solde après : ~**568 cr** (sur 579 cr)
