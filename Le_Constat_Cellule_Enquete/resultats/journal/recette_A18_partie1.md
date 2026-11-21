# Recette du dossier A18, partie 1 — Audit factuel de la V5, ligne à ligne

**Contrôle fait par l'orchestrateur le 20 novembre 2026, 19 h 02 – 19 h 04.** Mission lancée à 14 h 19, interrompue à 14 h 25, reprise à 18 h 13, terminée à 19 h 01 (181 appels d'outils au total). Les parties 2 (vérification de 25 conclusions de la cellule) et 3 (arbitrage des contradicteurs) ne sont pas commencées.

## Verdict : recette passée pour l'audit en deux passes ; **le caractère aveugle de la première passe repose sur la déclaration de l'agent et sur les horodatages ; le décompte du message de fin diffère légèrement de celui des fichiers ; une quinzaine de lignes « exactes » reposent sur une source secondaire**. Statut : audit de la cellule, non comparé à l'audit de l'équipe Codex.

## 1. Contrôle mécanique

17 titres présents dans le dossier principal, dont 5 presque vides et déclarés « sans objet pour la partie 1 » (chronologie, échelles, gagnants et perdants, mesures) : accepté pour un dossier d'audit, à compléter aux parties 2 et 3. Annexe d'audit de 97 Ko. 194 pièces marquées consultées, 18 secondaires, 2 souvenirs, 4 recherches infructueuses. Manifeste : 68 pièces, toutes avec adresse d'origine ; 13 scripts.

## 2. Contrôles de l'orchestrateur

| Élément | Contrôle | Résultat |
|---|---|---|
| Passe 1 figée avant la confrontation | Empreinte du fichier `A18_audit_V5_passe1.csv` recalculée ; horodatages | **Empreinte conforme** à celle annoncée (d8832d18…) ; fichier daté de 18 h 47, passe 2 de 19 h 01. Que l'agent n'ait rien lu de la cellule avant 18 h 47 est sa déclaration : non vérifiable par l'orchestrateur |
| Décompte des verdicts | Recompté par script dans `passe2.csv` | **208 lignes** : 167 exact, 16 non démontré, 12 trop général, 7 inexact, 4 non vérifié, 2 sans verdict. Le message de fin annonçait 200 lignes et 162 / 15 / 12 / 7 / 4 : il ne compte pas les lignes ajoutées en passe 2. **Les fichiers font foi** |
| « La charge de la dette pèsera autant que tout le budget de la Défense : 72 milliards » | Projet de loi de finances pour 2027 **retéléchargé à l'origine**, identique ; état B relu p. 246–247 | **Confirmé** : Défense, 73,15 Md€ de crédits de paiement, pensions comprises ; charge de la dette, 72,37 Md€ (58,6 en 2026). La phrase de la V5 tient ; la cellule ne l'avait pas vérifiée pensions comprises |
| Un député peut déplacer des crédits entre programmes d'une même mission | Rapport de l'Assemblée n° 1891 **retéléchargé à l'origine**, identique ; p. 99 relue | **Confirmé**. Corrige la formule d'A08 reprise dans la transmission de la vague 2 : un parlementaire ne peut pas augmenter le total d'une mission, mais il peut y redéployer |

Non revérifiés : les 200 autres lignes. En particulier les cinq points que la cellule laissait ouverts et pour lesquels A18 dit avoir trouvé les pièces (chômage suédois de 1996, Parti du centre, « depuis 1962 », rapport Pébereau, hôtel).

## 3. Ce que dit l'audit (résultat d'agent, à comparer à l'audit de Codex en fin d'enquête)

Sept affirmations classées **inexactes** :

| Ligne | Affirmation de la V5 | Motif |
|---|---|---|
| B3-23 | « Elle a prélevé plus aussi : un peu plus de 5 points » | moins de 5 points en impôts et cotisations (4,7) ; plus de 5 seulement en recettes totales |
| B4-19 | « l'aide dure » | les aides de crise sont passées de 83,7 Md€ en 2021 à 12,4 en 2023 |
| B4-22 | Allemagne : dette « de près de 10 mois de production à 7 » | 8,9 à 9,3 mois |
| B4-34 | loi de programmation « votée en novembre » | adoptée par l'article 49.3 |
| B4-39 | HCFP : « semble peu plausible » | les avis lus disent « très peu vraisemblable » ; guillemets non conformes |
| B6-06 | Suède, 1993 : déficit d'« environ 12 % » | 10,7 % en comptes harmonisés ; 12 % dans les comptes de l'époque |
| B6-31 | « 10 / 44 / 150 » | trois grandeurs d'années et de périmètres différents |

Douze affirmations « trop générales », seize « non démontrées » (dont la citation attribuée au Gouvernement sur « la situation politique en France », introuvable ; la Commission, elle, fait ce lien), quatre « non vérifiées » (dont le franchissement de 5 % « le 22 octobre » : la presse lue dit le 21).

Les chiffres d'ouverture sont classés exacts : 51 ans, 1974, 152 Md€, 458 voix contre 0, taux français au-dessus de l'italien en octobre.

## 4. Portée à ne pas perdre

- **Huit verdicts ont changé entre la passe aveugle et la confrontation**, dans les deux sens : la cellule avait raison sur quatre points (aides de crise, points de prélèvements, 1975, écart par fonction) ; A18 corrige la cellule sur trois (Défense, redéploiement des crédits, nombre de recours au 49.3 chez A03) et se corrige lui-même sur deux (Défense, coût du dixième de point).
- « Exact sous condition » (49 lignes) n'est pas « exact » : la condition est écrite ligne par ligne dans le fichier.
- **Cet audit ne dit pas quoi écrire** : aucune formulation de remplacement, conformément à la charte.
- Non vérifiable par A18 : série quotidienne des taux, autres avis du HCFP, document du FMI de 1998, rapport Pébereau original, texte article par article de trois lois.

## 5. Suites décidées

1. Correction à porter dans `transmissions\vague2.md` (§3.1) : règle de redéploiement des crédits.
2. Contradictions à inscrire : Défense avec ou sans pensions ; nombre de recours au 49.3 dans A03.
3. Parties 2 et 3 d'A18 : après la remise d'A16 et d'A17, vraisemblablement à la prochaine fenêtre d'usage.
4. Le fichier final `audit_factuel_V5.md` de la cellule ne sera produit qu'après la partie 3 et la comparaison avec l'audit de l'équipe Codex, que la cellule n'a pas lu.
