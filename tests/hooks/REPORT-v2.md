# Hook A/B test — Round 2 — Push the ceiling

**Date** : 2026-05-15
**Goal** : Combiner les patterns gagnants du round 1 pour dépasser viral=60.
**Stratégie** : text-first refined (PUNCH) + chiffres dans le hook + mots forts.
**Résultat** : viral 60 → **63**, hook 46 → **53**.

---

## 🏆 Leaderboard v2 (par viral_potential)

| Rang | ID | Style | Hook text | Viral | Hook (0-3s) | Brain | Δ vs R1 best |
|------|----|-------|-----------|-------|-------------|-------|--------------|
| 🥇 | **V10** | Punch | « **Personne** ne te dit la **VÉRITÉ** sur le sommeil » | **63** | 49 | 62 | **+3 viral** |
| 🥈 | **V2** | Punch | « **97 %** font CETTE erreur le soir » | 62 | **53** ⭐ | 63 | +2 / **+10 hook** |
| 🥈 | V4 | Red alert | « **STOP**. Tu fais pleurer ton bébé pour RIEN » | 62 | 52 | **63** | +2 / +9 |
| 🥈 | V6 | Punch | « À 2h du matin, **73 %** des bébés font CECI » | 62 | 51 | 63 | +2 / +8 |
| 🥈 | V3 | Punch | « **1 bébé sur 3** dort MAL » | 62 | 51 | 61 | +2 / +8 |
| 🥈 | V8 | Punch | « Pour qu'il dorme MIEUX, fais l'**INVERSE** » | 62 | 48 | 59 | +2 / +5 |
| 7 | V5 | Punch | « Ce que les pédiatres ne disent **JAMAIS** » | 60 | 49 | 60 | 0 / +6 |
| 8 | V9 | Mixed | « **11h** de sommeil. UN changement » | 57 | 46 | 58 | -3 / +3 |
| 9 | V1 | Mixed | « **92 %** des parents ratent CETTE phrase » | 55 | 40 | 50 | -5 / -3 |
| ❌ | V7 | Red alert | « **ARRÊTE** de bercer ton bébé » | _bug API confirm_ | | | |

> **Reference round 1 best** : N3 cosy "92%" → viral=60 / hook=43.
> **Round 2 best**     : V10 → viral=**63** / hook=49. V2 → hook=**53**.

---

## 🎯 Conclusions confirmées

### 1. **Le plateau viral=62 est atteint par 5 tests, un test crève le plafond à 63**
5 des 6 tests en style PUNCH ont touché **exactement** viral=62. V10 a passé à viral=63 — **point unique** qui montre qu'on peut grappiller +1 avec le bon hook curiosity. **Le vrai plafond du modèle pour ce sujet/format est probablement entre 63 et 65.**

### 2. **+10 points de hook_score** (V2 hook=53 vs N2 hook=46)
La progression vient de :
- **Fonts plus grosses** (200px pour le chiffre vs 150px en R1)
- **Fades plus rapides** (0.12s vs 0.25s) → pulse rythm
- **Premier caption = MOT/CHIFFRE seul** (« 97 % », « STOP », « ARRÊTE », « Personne » isolés sur 1-1.5s avant la suite)

### 3. **Le hook « curiosity ouvert » bat le hook « chiffre précis » sur le viral**
V10 « **Personne** ne te dit la VÉRITÉ » → viral=63 (best)
V2 « **97 %** font CETTE erreur » → viral=62 (best hook score)

Le chiffre **gagne le stop-scroll** (hook_score). La curiosité ouverte **gagne la rétention** (sustain=100 et brain reste haut sur toute la durée). À utiliser selon l'objectif : reach vs view-through.

### 4. **Le style « mixed » (text-first → cosy) ne marche pas**
- V1 (mixed avec hook winner du R1) : **55/40** — perd 5 viral vs même hook en cosy R1
- V9 (mixed "11h"+story) : **57/46**

L'animation de transition de l'image (blur → clear) à t=3s casse l'attention. **À abandonner**.

### 5. **Le style « red alert » égale punch jaune**
V4 (STOP rouge) viral=62 brain=63 — identique à V2/V3/V6 punch jaune.
Pas de gain mesurable. À choisir selon le hook : rouge pour les commandements (STOP, ARRÊTE), jaune pour les chiffres/curiosité.

---

## 📈 Évolution sur 2 rounds (sujet sommeil bébé)

| Test | Round | Style | Hook | Viral | Hook |
|------|-------|-------|------|-------|------|
| H1 (pilot-01) | R1 | Cosy slow | « Si ton enfant se réveille 2h » | 46 | 28 |
| N1 | R1 | Dynamic | « Si ton enfant se réveille 2h » | 56 | 44 |
| N2 | R1 | Text-first | « Si ton enfant se réveille 2h » | 59 | 46 |
| N3 | R1 | Cosy | « **92 %** des parents font CETTE erreur » | 60 | 43 |
| **V2** | **R2** | **Punch** | « **97 %** font CETTE erreur » | 62 | **53** |
| **V10** | **R2** | **Punch** | « **Personne** ne te dit la VÉRITÉ » | **63** | 49 |

**Gain total** : viral 46 → 63 (**+37 %**), hook 28 → 53 (**+89 %**).

---

## 🚀 Template gagnant final

```
Style  : PUNCH (text-first refined)
Hook   : Premier mot/chiffre SEUL pendant 1-1.5s (200px, xxl)
         - Chiffre %    → maximise hook score (V2, V6)
         - Commandement → maximise hook score + attention (V4 STOP)
         - Curiosity    → maximise viral/sustain (V10 Personne)
Visual : Image blurred bg, filter blur(14px) brightness(0.45)
         Ken Burns lent 1.25 → 1.40 sur 15s
Audio  : Hook-boom à t=0s (volume 0.55)
         VO Clara v2 atempo=1.10 (légèrement plus rapide)
Captions : Plus Jakarta Sans 900, 200px → 160-170px → 110-120px
Hl     : Yellow rgba(242,200,75,0.62) | Red rgba(255,60,60,0.78)
```

### Combinaisons gagnantes confirmées (viral ≥ 62)
- « **Personne** ne te dit la VÉRITÉ sur le X » → 63 viral
- « **97 %** font CETTE erreur le soir » → 62 viral, 53 hook
- « **STOP**. Tu fais [X] pour RIEN » → 62 viral, brain 63
- « À **2h du matin**, **73 %** des bébés font CECI » → 62 viral
- « **1 bébé sur 3** dort MAL » → 62 viral
- « Pour qu'il dorme MIEUX, fais l'**INVERSE** » → 62 viral

### À éviter
- Style mixed (text-first → cosy reveal) : **−5 à −7 viral**
- Hooks longs sans chiffre/verbe avant 2s
- Hook story personnelle (« Quand mon enfant… »)

---

## 💰 Coût

- 0 image générée (réutilisation R1)
- 10 VOs ElevenLabs (free)
- 10 renders locaux (free)
- 9 virality_predictor (free Ultimate)
- **Coût round 2 : 0 cr** ✅
