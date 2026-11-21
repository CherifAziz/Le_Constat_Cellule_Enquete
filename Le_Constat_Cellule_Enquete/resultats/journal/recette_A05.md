# Recette du dossier A05 — Dépenses et qualité des services

**Contrôle fait par l'orchestrateur le 20 novembre 2026, vers 11 h 30.** Durée de la mission A05 : 41 minutes, 176 appels d'outils.

## Verdict : recette passée pour les décompositions et la comparabilité ; **partielle sur l'efficience et sur la part des décisions**. Statut : non contre-expertisé.

## 1. Contrôle mécanique

`journal\recette_2026-11-20_11h27.md` : 17 titres obligatoires présents ; 50 pièces marquées consultées, 8 secondaires, 5 souvenirs non vérifiés, 6 recherches infructueuses ; 31 faits, 7 hypothèses, 18 calculs, 6 pistes ; 73 fichiers de données ; 11 scripts. Seulement 3 URL écrites en clair dans le dossier : les références renvoient au manifeste `donnees\A05\A05_sources_manifeste.csv`, à contrôler par la contre-expertise.

## 2. Relecture

Sections 11 à 15 lues intégralement par l'orchestrateur ; les sections 3 à 10 ne l'ont pas été. Cette recette est donc plus légère que celles d'A01, A02 et A04.

## 3. Sondage à la source (refait par l'orchestrateur sur la base commune)

| Affirmation d'A05 | Contrôle | Résultat |
|---|---|---|
| Dans le fichier Eurostat des dépenses par fonction, les ratios 2023–2024 reposent sur un PIB d'un millésime antérieur : France 2024 à 57,3 au lieu de 57,0 ; Allemagne 49,4 au lieu de 49,0 | Comparaison directe de `eurostat_gov_10a_exp.csv` et `eurostat_gov_10a_main.csv` | **Confirmé** : France 57,3 (provisoire) contre 57,0 ; Allemagne 49,4 contre 49,0 ; zone euro 49,2 contre 49,3 ; Suède et Italie cohérentes |
| Conséquence : l'écart France – zone euro de 2024 vaut environ 7,7 à 7,8 points, non 8,1 | 57,0 − 49,3 | **Confirmé** : 7,7 au dixième publié ; le tableau d'Astra reprend les ratios du fichier par fonction |
| Variation du ratio de dépense : +12,8 points de 1974 à 1985 sur +16,0 depuis 1974 | Faits de contrôle F-ORC-014 et F-ORC-015 | **Confirmé** (80 %) |

Non revérifiés par l'orchestrateur : dépense sociale nette de l'OCDE (2019), comparaison de la santé selon les comptes de la santé, pauvreté des plus de 66 ans, part du « train de vie » (moins de 0,1 % de la dépense), part des plus de 65 ans (France 21,5 %, zone euro 21,9 %).

## 4. Ce que le dossier ne contient pas (reconnu par A05)

- Aucune étude d'efficience ni de coûts unitaires : la question « moindre dépense à résultat égal » reste sans preuve dans un sens ou dans l'autre.
- Part des décisions dans la hausse de 1974–1985 non identifiée : selon la référence choisie, 31 % ou 91 %.
- Dépenses par fonction avant 1995 ; volume et prix de la santé ; masse salariale ; emploi public par versant depuis 1980 ; opérateurs ; achats ; part indexée de la dépense ; additionnalité des aides aux entreprises ; entretien des infrastructures.
- Corrections symétriques des cotisations imputées et des crédits d'impôt entre pays.

## 5. Suites décidées

1. **Avertissement à toute la cellule** : ne plus citer les ratios par fonction de 2023–2024 du fichier Eurostat tels quels ; recalculer à partir des montants.
2. Seconde passe ciblée : études d'efficience et de coûts unitaires (FMI, Commission, travaux académiques) ; volume et prix de la santé.
3. Contradiction à inscrire : écart de 8,1 points chez Astra contre 7,7 à 7,8.
