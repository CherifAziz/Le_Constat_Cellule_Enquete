# Recette du dossier A01 — Architecte comptable

**Contrôle fait par l'orchestrateur le 20 novembre 2026, 11 h 20 – 11 h 25.** Durée de la mission A01 : 36 minutes, 180 appels d'outils.

## Verdict : recette passée, avec réserves. Statut : non contre-expertisé.

## 1. Contrôle mécanique

`journal\recette_2026-11-20_11h21.md` : 17 titres obligatoires présents ; 56 pièces marquées consultées, 4 secondaires, 6 souvenirs non vérifiés, 9 recherches infructueuses ; 19 faits, 4 hypothèses, 9 calculs, 5 propositions ; 52 fichiers de données ; 7 scripts.

## 2. Relecture

Dossier principal et registre lus intégralement par l'orchestrateur (412 lignes). L'annexe n'a été lue que par ses renvois. Les passages marqués [M] sont bien présentés comme non vérifiés (pic de transferts de 2010, règles propres aux collectivités).

## 3. Sondage à la source (refait par l'orchestrateur, indépendamment des scripts d'A01)

| Affirmation d'A01 | Contrôle | Résultat |
|---|---|---|
| Écart de dépenses France – zone euro hors France : 9,2 points en 2025 ; recettes 6,7 | Recalcul sur `donnees\commun\eurostat_gov_10a_main.csv` : (EA20 − FR) / (PIB EA20 − PIB FR) | **Confirmé** : 9,24 et 6,66 ; poids de la France 18,8 % |
| Impôts et cotisations : France 46,0 en 2025 devant la Belgique 44,7 ; en 2024, Belgique 45,2 devant France 45,1 | Lecture de `eurostat_gov_10a_taxag.csv` (13 pays) | **Confirmé** sur les 13 pays du fichier commun ; le classement sur 30 pays repose sur l'extraction propre d'A01, non revérifiée |
| Hors cotisations imputées : France 44,3 contre Danemark 44,2 en 2025 ; Danemark devant en 2024 | idem | **Confirmé** |
| Projet de loi de finances 2027, article liminaire : solde structurel 2025 de −5,2 ; solde effectif −5,1 / −5,4 / −5,0 pour 2025, 2026, 2027 ; trajectoire de la loi de programmation : −2,7 en 2027 | Lecture de la copie locale du texte n° 3210 de l'Assemblée | **Confirmé** mot pour mot ; dette prévue 119,3 % en 2026 et 121,7 % en 2027 |
| Base 2005 de l'Insee (capture d'archive de 2012) : solde 1974 de +0,45 Md€, 1973 de +0,10, ventilation État/ODAC « N.D. » | Lecture directe du classeur archivé | **Confirmé** : 1974 +0,4467 ; 1973 +0,0962 ; 1972 +0,5497 ; 1970 +0,1222 ; 1975 −6,5963 |
| Le ratio de dette a baissé 12 années, dont 1979 | Lecture de la série publiée | **Nuance** : en 1979 le ratio publié est inchangé à 21,6 % ; la baisse n'existe qu'au-delà de la première décimale. Onze années au dixième publié (F-ORC-013) |
| Solde structurel 2025 de −4,7 selon la Commission (prévisions d'automne 2026, annexe) | Tentative de lecture du tableau 38 du PDF local | **Non revérifié** par l'orchestrateur (tableau en colonnes, extraction non concluante) ; à reprendre par A18 ou CX-05 |

## 4. Ce que le dossier ne contient pas (reconnu par A01)

- Matrice bilatérale des transferts État → sécurité sociale (compensations d'exonérations, subventions d'équilibre, reprises de dette par la CADES) ; tableau t_3108 téléchargé mais non exploité. **Travail n° 3 partiel.**
- Avis du HCFP sur le budget 2027, estimations du FMI et de l'OCDE pour 2025. **Travail n° 7 partiel.**
- Bases Insee antérieures à 2005 pour le signe des soldes de 1970 à 1975. **Travail n° 5 partiel.**
- Explication du résidu d'ajustements stocks-flux d'avant 1998 (environ 20 points de ratio de dette) et de la révision de la dette de 2010 entre bases.
- Sections 6, 9 et 10 limitées à la comptabilité, ce qui est conforme au rôle.

## 5. Suites décidées

1. La table de passage d'A01 devient la table de référence de la cellule pour les vagues suivantes, avec ses avertissements (pas d'État/ODAC avant 1978 ; pas de série « hors éléments imputés » avant 1978 ; pas de ventilation D73/D733 avant 2010).
2. Complément ciblé à lancer en seconde passe : transferts État → sécurité sociale et t_3108 ; résidu stocks-flux d'avant 1998.
3. K-011 et K-013 passent à « instruite » dans l'index des contradictions.
4. Anomalie de la source Insee (État + ODAC ≠ administration centrale de 1959 à 1977) : à signaler au commanditaire ; un signalement à l'Insee relève de sa décision.
