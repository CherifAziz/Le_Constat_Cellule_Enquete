# Recette du dossier A18, parties 2 et 3 — Vérification indépendante et arbitrage des contre-expertises

**Contrôle fait par l'orchestrateur le 20 novembre 2026, 19 h 36 – 19 h 38.** Mission lancée à 19 h 11 dans une nouvelle session du même rôle, terminée à 19 h 35 (25 minutes, 116 appels d'outils).

## Verdict : recette passée pour l'arbitrage des 15 attaques et pour 28 vérifications, dont 24 entièrement refaites ; **l'arbitre est du même modèle que les agents qu'il arbitre ; les versions de l'équipe Codex ne sont pas dans son périmètre ; neuf points sont déclarés non faits**. Statut : arbitrage de la cellule, à confronter aux travaux de Codex.

## 1. Contrôles de l'orchestrateur

| Élément | Contrôle | Résultat |
|---|---|---|
| Fichier de la première passe d'audit intact | Empreinte recalculée | **Inchangée** (d8832d18…) |
| Décompte de l'arbitrage | Recompté par script dans `A18_arbitrage.csv` | **19 lignes** : 15 attaques (2 fondées, 12 fondées en partie, 1 non fondée), la correction d'A17 sur le taux de 2,8 % (fondée), et 3 tensions (2 « dépend d'une convention », 1 « indécidable ») |
| Décompte des vérifications | Recompté dans `A18_verification_25.csv` | **28 lignes**, aucune infirmée ; 2 relues dans la copie seulement ; 2 recalculées en partie ; 6 dépendent d'une convention |
| « De 2015 à 2019, la France est le seul pays étudié dont la dette monte » | Recalcul par l'orchestrateur sur la base commune | **Constat d'A18 confirmé** : la Grèce aussi (179,6 → 183,2 % ; France 97,0 → 98,2 %). « Seul pays » ne vaut que hors Grèce |

Non revérifiés : les 27 autres vérifications ; le rejeu du script d'A16 par A18 ; la relecture de la base AMECO pour T-07.

## 2. Ce que l'arbitrage établit (résultat d'agent)

**Aucune attaque n'infirme un chiffre de la cellule.** Douze sont « fondées en partie » : le calcul tient, la portée était énoncée trop largement.

Modifications demandées aux dossiers (texte exact dans `donnees\A18\A18_arbitrage.csv` ; liste lisible dans `corrections_demandees.md`) :

| Dossier | Modification |
|---|---|
| A15 | écrire « aucune combinaison **des mesures chiffrées** » ; afficher la dette de 2035 en fourchette (137 à 140 %) ; donner en regard le rythme de dépense qui suffirait ; supprimer la phrase sur le taux de 2,8 % ; donner une fourchette pour le test de crédibilité (6,5 à 7,2 % en 2030) |
| A01 | « structurel à plus de 92 % dans les estimations **officielles** lues » ; mentionner l'estimation alternative (environ 84 %) ; « structurel » ne veut pas dire « décidé » |
| A11 | retirer la conclusion « la capture ne peut pas être présentée comme une explication du déficit », qui dépasse la mesure ; classer « non établie, non écartée » |
| A09 | limiter le résultat au veto parlementaire ; inscrire le « bien commun budgétaire » comme hypothèse non testée |
| A13 | l'ordre des multiplicateurs (transferts au-dessus des impôts) est une hypothèse ; vieillesse et santé font environ deux tiers de l'écart de dépense |
| A14 | la seconde moitié de son résultat sur la nécessité de passer par la dépense est un jugement |
| A03 | 2004–2006 n'est pas une consolidation en solde corrigé du cycle ; la série citée n'a pas été retrouvée |

Tensions : T-07 (un assouplissement suit-il chaque consolidation ?) dépend de la série retenue ; sur les deux consolidations corrigées du cycle de plus de 2 points (1993–1999, 2010–2016), le solde se dégrade ensuite dans un à trois ans — deux cas seulement. T-06 (emploi et solde) est indécidable sur les pièces accessibles.

Convergences des deux contradicteurs, relevées par l'arbitre : la persistance de l'effet sur l'activité est le paramètre décisif ; l'effort nécessaire est d'environ 5 points de PIB ; les programmes de 2010 doivent être instruits sur pièces. Désaccords non tranchés : les multiplicateurs au-delà d'un an ; la lecture d'un résultat d'A12 sur la composition.

## 3. Ce que la vérification établit

28 chiffres centraux refaits par des scripts propres à A18, dont 13 que personne n'avait recalculés : 51 déficits, excédent de 1974, déficit de 2025, écarts avec la zone euro, absence d'excédent primaire depuis 2002, décomposition de la dette, charge d'intérêts de 1996, 37 budgets de majorité absolue, écart programmé-exécuté, aides de crise, prestations de 1974–1985. **Aucun n'est infirmé.**

Deux nuances nouvelles : la Grèce (ci-dessus) ; « le solde primaire s'améliore de 1,5 point de 2015 à 2019 » suppose 2014 pour année de base (+1,0 de 2015 à 2019).

## 4. Portée à ne pas perdre

- **L'arbitre et les arbitrés sont le même modèle.** « Aucun chiffre infirmé » vaut contre les erreurs de calcul et de transcription, moins contre une erreur de raisonnement partagée. La comparaison avec Codex reste nécessaire.
- **Vérifications réellement indépendantes : 24, pas 28** (corrigé à 19 h 41). Deux lignes sont des relectures de copies (retraites, enveloppes des portefeuilles). Deux autres ne sont refaites qu'en partie, et la partie non refaite porte le résultat : le classement des majorités pour « 37 budgets de majorité absolue en déficit », et la colonne « programmé » pour l'écart de −2,1 point à trois ans. Le critère de fin demande 25 vérifications, **dont toutes les affirmations retenues pour la vidéo** : cette seconde condition ne peut pas être constatée avant l'étape éditoriale. Critère : **partiel**.
- Non fait par A18 : Canada ; recalcul des baisses de prélèvements d'A04 ; référence d'A15 vérifiée à la source ; écart entre « 3 % en 2029 » (engagement européen) et « 2035 » (modèle) ; sondage des étiquettes de provenance ; lecture intégrale des pré-enregistrements.

## 5. Suites décidées

1. Les dossiers des agents **ne sont pas réécrits** : les modifications demandées sont consignées dans `corrections_demandees.md`, qui fera foi pour le rapport intégral.
2. Lacunes rouvertes, désignées par les contradicteurs et retenues par l'arbitre : programmes de 2010 sur pièces et multiplicateur de 2011–2014 ; incidence par niveau de vie des baisses de prélèvements de 2018–2023 ; exécution des normes de dépense.
3. Comparaison avec les travaux de Codex : première mission de la prochaine fenêtre.
4. Manifeste d'A06 à régulariser (adresse d'un rapport du COR introuvable selon A18).
