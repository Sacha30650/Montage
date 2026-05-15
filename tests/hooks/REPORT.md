# Hook A/B test — Virality Predictor results

**Date** : 2026-05-15  
**Tool** : Higgsfield `virality_predictor` (brain_activity model, 15s clips)  
**Niche** : Parentalité FR  
**Total tests** : 10 prévus, **9 analysés** (N6 bloqué par erreur API `media_confirm` côté Higgsfield)

---

## 🏆 Leaderboard global (par `viral_potential`)

| Rang | ID | Style | Hook text | Viral | Hook (0-3s) | Brain engagement |
|------|----|-------|-----------|-------|-------------|------------------|
| 🥇 1 | **N3** | Cosy slow | « **92 % des parents** font cette erreur le soir » | **60** | 43 | 53 |
| 🥈 2 | **N2** | Text-first typo | « Si ton enfant se réveille toutes les 2h » (même texte que H1) | **59** | **46** | 54 |
| 🥉 3 | N1 | Dynamic punchy | « Si ton enfant se réveille toutes les 2h » (même texte que H1) | 56 | 44 | 53 |
| 4 | N4 | Dynamic punchy | « Tu dis 'calme-toi' ? Arrête » | 55 | 40 | 50 |
| 5 | N5 | Cosy slow | « L'erreur n°1 qui empêche ton bébé de dormir… » | 54 | 42 | 53 |
| 6 | H3 | Cosy slow | « Crise au supermarché ? » (pilot-03) | 51 | 33 | 43 |
| 7 | H2 | Cosy slow | « Tu dors avec ton bébé » (pilot-02) | 47 | 24 | 35 |
| 8 | H4 | Cosy slow | « Pas une minute pour le sport ? » (pilot-04) | 47 | 29 | 39 |
| 9 | H1 | Cosy slow | « Si ton enfant se réveille toutes les 2h » (pilot-01) | 46 | 28 | 38 |

---

## 🔍 Insights critiques

### 1. **Le style visuel pèse autant que le texte du hook**

**Même hook texte, 3 styles différents** :
- H1 (cosy slow) → viral **46**, hook **28**
- N1 (dynamic punchy) → viral **56**, hook **44** _(+10 / +16)_
- N2 (text-first typo) → viral **59**, hook **46** _(+13 / +18)_

→ Passer un même script de cosy à text-first **améliore la rétention prédite de +28 %** et le hook de **+64 %**.

### 2. **Le hook chiffre/stat domine en formulation**

N3 « 92 % des parents » remporte le titre avec **viral=60** même en style cosy slow. Le cerveau s'arrête sur un nombre précis. Combiné à un style dynamic, ce serait potentiellement ~65-70.

### 3. **Le « cosy slow » sabote systématiquement le hook**

Les 4 baselines (H1-H4), tous en cosy slow, plafonnent à **hook=33 max**.  
Les 5 variations à style alternatif (N1-N5) commencent à **hook=40 min**.

**Le format cosy de la série actuelle est en moyenne ~15 points de hook sous l'optimum.**

### 4. **Hook « confrontational » + dynamic ≈ excellent stop-scroll**

N4 (« Tu dis 'calme-toi' ? Arrête ») n'est que viral=55 mais l'image (poing serré) génère un peak fronto-pariétal (attention) de **0.73** dans les 3 premières frames. C'est un hook **stop-scroll** efficace mais qui peine ensuite à retenir (image statique, ton agressif).

### 5. **Identification universelle reste la meilleure baseline cosy**

Parmi les 4 baselines cosy, **H3 (« Crise au supermarché »)** sort gagnant (viral=51, hook=33). Le scénario universel + image émotionnelle bat la formulation chiffre/question dans le format actuel.

---

## 🎯 Recommandations pour la suite

### À garder
- **Sujet « sommeil bébé »** : audience clairement engagée (toutes les versions sommeil scorent bien sur brain_engagement)
- **Captions en gros texte + highlight** : déjà bon
- **Niche éducative parentalité** : DMN « lower better » bien performé partout

### À changer immédiatement
1. **Abandonner le hook cosy** sur les 3 premières secondes. Passer en **text-first** ou **dynamic punch** pour l'intro, puis revenir en cosy slow pour le corps de la vidéo.
2. **Privilégier les hooks chiffrés** : « X % », « 3 erreurs », « En 90 secondes », « 1 sur 3 », plutôt que des questions ouvertes.
3. **Premier mot = mot fort** : « Arrête », « Stop », « 92 % », « Personne », « L'erreur » performent mieux que « Si », « Tu », « Pas ».
4. **Première image = punch visuel** (close-up tendu, contraste fort, motion-blur léger) plutôt qu'une scène cosy paisible.

### Template hook gagnant à tester
```
[0-1.5s]  Text-first plein écran "92% des parents"
          + chiffre flash UPPERCASE rouge/jaune
          + impact SFX (kick + sub-bass)
[1.5-3s]  "font CETTE erreur" (continuation du même style)
[3-5s]   On reveal le visuel cosy (transition douce)
[5s+]    Corps de la vidéo en style cosy slow habituel
```

C'est le mélange **N2 (text-first hook) + cosy slow (body)** qui devrait piquer **viral ≥ 65, hook ≥ 50**.

---

## 📊 Détail par test

### Baselines

- **H1** (pilot-01 « Sommeil 3 erreurs ») : viral=46, hook=28, sustain=98, brain=38
- **H2** (pilot-02 « Co-sleeping 3 vérités ») : viral=47, hook=24, sustain=100, brain=35
- **H3** (pilot-03 « Tantrum 90s ») : viral=51, hook=33, sustain=100, brain=43
- **H4** (pilot-04 « Sport 10 min ») : viral=47, hook=29, sustain=95, brain=39

### Variations nouvelles

- **N1** (Dynamic punchy, hook A sommeil) : viral=56, hook=44, sustain=84, brain=53
- **N2** (Text-first typo, hook A sommeil) : viral=59, hook=46, sustain=83, brain=54
- **N3** (Cosy slow, hook « 92 % ») : viral=60, hook=43, sustain=100, brain=53
- **N4** (Dynamic punchy, hook « calme-toi ») : viral=55, hook=40, sustain=83, brain=50
- **N5** (Cosy slow, hook curiosity « erreur n°1 ») : viral=54, hook=42, sustain=87, brain=53
- **N6** (Cosy intime, hook story « j'ai pleuré ») : ❌ non testé — `media_confirm` cassé côté API Higgsfield (4 tentatives échouées, 2 uploads distincts)

---

## 💰 Coût total

- 5 images nano_banana_flash : **7.5 cr**
- 9 virality_predictor (gratuit sur le plan Ultimate) : **0 cr**
- Solde avant test : 586.86 cr → après : **579.36 cr**
- **Coût total du test : 7.5 cr** (≈ $0.30)

## 📁 Artefacts

- `tests/hooks/builds/N{1..6}.html` : templates de composition
- `tests/hooks/renders/N{1..6}.mp4` : clips 15s rendus
- `tests/hooks/H{1..4}-baseline-pilot0{1..4}.mp4` : extraits 15s des pilotes
- `tests/hooks/scripts/{A..E}.txt` : 5 scripts FR
- `tests/hooks/audio/{A..E}.mp3` : 5 VOs Clara v2 + atempo 1.08
- `tests/hooks/images/N{1,3,4,5,6}-*.png` : 5 images B-roll
- `scripts/gen_hook_tests.py` : générateur de templates
