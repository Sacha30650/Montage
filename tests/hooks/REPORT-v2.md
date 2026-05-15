# Hook A/B test — Round 2 — Push the ceiling

**Date** : 2026-05-15
**Goal** : Combiner les patterns gagnants du round 1 pour dépasser viral=60.
**Stratégie** : text-first refined (PUNCH) + chiffres dans le hook + mots forts.

---

## 🏆 Leaderboard v2 (par viral_potential)

| Rang | ID | Style | Hook text | Viral | Hook (0-3s) | Brain | Δ vs R1 best |
|------|----|-------|-----------|-------|-------------|-------|--------------|
| 🥇 | **V2** | Punch | « **97 %** font CETTE erreur le soir » | **62** | **53** | 63 | **+2 viral / +7 hook** |
| 🥇 | **V4** | Red alert | « **STOP**. Tu fais pleurer ton bébé pour RIEN » | **62** | 52 | **63** | +2 / +6 |
| 🥇 | **V6** | Punch | « À 2h du matin, **73 %** des bébés font CECI » | **62** | 51 | 63 | +2 / +5 |
| 🥇 | **V3** | Punch | « **1 bébé sur 3** dort MAL » | **62** | 51 | 61 | +2 / +5 |
| 5 | V5 | Punch | « Ce que les pédiatres ne disent **JAMAIS** » | 60 | 49 | 60 | 0 / +3 |
| 6 | V9 | Mixed | « **11h** de sommeil. UN changement » | 57 | 46 | 58 | -3 / 0 |
| 7 | V1 | Mixed | « **92 %** des parents ratent CETTE phrase » | 55 | 40 | 50 | -5 / -6 |
| ⏳ | V8 | Punch | « Pour qu'il dorme MIEUX, fais l'**INVERSE** » | _en cours_ | | | |
| ⏳ | V10 | Punch | « Personne ne te dit la **VÉRITÉ** » | _en cours_ | | | |
| ❌ | V7 | Red alert | « **ARRÊTE** de bercer ton bébé » | _bug API confirm_ | | | |

> **Reference round 1 best** : N3 cosy "92%" → viral=60 / hook=43.

---

## 🎯 Conclusions confirmées

### 1. **Le plateau viral=62 est atteignable de façon répétable**
4 tests sur 6 du style PUNCH ont touché **exactement** viral=62. Ce n'est pas du hasard — c'est le score que le modèle attribue de façon stable à la combinaison « text-first refined + premier mot fort + chiffre/commandement ».

### 2. **+7 points de hook_score sur le meilleur** (V2 hook=53 vs N2 hook=46)
La progression vient de :
- **Fonts plus grosses** (200px pour le chiffre vs 150px en R1)
- **Fades plus rapides** (0.12s vs 0.25s) → pulse rythm
- **Premier caption = MOT/CHIFFRE seul** (« 92 % » / « STOP » / « ARRÊTE » isolés sur 1-1.5s avant la suite)

### 3. **Le style « mixed » (text-first → cosy) ne marche pas**
- V1 (mixed avec hook winner du R1) : **55/40**, soit -5 viral vs même hook en R1 cosy pur
- V9 (mixed "11h"+story) : **57/46**

L'animation de transition de l'image (blur → clear) à t=3s casse l'attention. Le modèle pénalise ce changement de format. **À abandonner**.

### 4. **Le style « red alert » performe au même niveau que punch jaune**
V4 (STOP rouge) : viral=62, brain=63 — **identique** à V2/V3/V6 punch jaune.
Pas de gain mesurable du rouge. À choisir selon le hook : rouge pour les commandements (STOP, ARRÊTE), jaune pour les chiffres/curiosité.

### 5. **Le « pédiatres jamais » (V5) coince à 60**
Le hook « Ce que les pédiatres ne disent JAMAIS » est plus long et la première frame n'a pas de chiffre/mot-choc. Le hook_score 49 confirme que **les chiffres + commandements ouvrent mieux** que les promesses de révélation.

---

## 📈 Évolution sur 2 rounds (sur le même sujet sommeil)

| Test | Round | Style | Hook | Viral | Hook |
|------|-------|-------|------|-------|------|
| H1 (pilot-01) | R1 | Cosy slow | « Si ton enfant se réveille 2h » | 46 | 28 |
| N1 | R1 | Dynamic | « Si ton enfant se réveille 2h » | 56 | 44 |
| N2 | R1 | Text-first | « Si ton enfant se réveille 2h » | 59 | 46 |
| N3 | R1 | Cosy | « **92 %** des parents font CETTE erreur » | 60 | 43 |
| **V2** | **R2** | **Punch** | « **97 %** font CETTE erreur » | **62** | **53** |

**Gain total** : viral 46 → 62 (+35 %), hook 28 → 53 (+89 %).

---

## 🚀 Template gagnant pour la suite

```
Style  : "PUNCH" (text-first refined)
Hook   : Chiffre seul OU commandement bref (1-1.5s)
         → Captions secondaires bold + highlight
         → Premier vrai mot = CHIFFRE / VERBE D'ACTION
Visual : Image blurred bg (filter blur(14px) brightness(0.45))
         Ken Burns lent 1.25 → 1.40
Audio  : Hook-boom à t=0s, VO Clara v2 atempo=1.10
SFX    : Pas de whoosh (testé non corrélé au score)
Font   : Plus Jakarta Sans 900 — 200px first hit, 160-170px ensuite
Hl     : Yellow rgba(242,200,75,0.62) | Red rgba(255,60,60,0.78)
```

### Hooks confirmés top tier (viral ≥ 62)
- « **97 %** font CETTE erreur le soir »
- « **1 bébé sur 3** dort MAL »
- « **STOP**. Tu fais pleurer ton bébé pour RIEN »
- « À **2h du matin**, **73 %** des bébés font CECI »

### À éviter
- Style mixed (text-first → cosy reveal)
- Hooks longs sans chiffre/verbe avant 2s (« Ce que les pédiatres… »)
- Hook story personnelle (« Quand mon enfant… » comme N6/V9)

---

## 💰 Coût

- 0 image générée (réutilisation R1)
- 10 VOs ElevenLabs (free)
- 10 renders locaux (free)
- 9 virality_predictor (free Ultimate)
- **Coût round 2 : 0 cr** ✅
