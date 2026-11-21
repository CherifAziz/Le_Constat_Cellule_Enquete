# Index des preuves

**Version 1, 20 novembre 2026, orchestrateur.** Chaque agent tient son propre registre dans son dossier (`F-Axx-…`, `H-Axx-…`, `C-Axx-…`, `P-Axx-…`). Ce fichier en est l'index. Une entrée d'agent n'y entre qu'après la recette de son dossier, avec le statut **non contre-expertisé** ; elle ne devient *confirmée* qu'après vérification par A18 ou par la contre-expertise Codex. Rien n'est fusionné avant.

Champs : affirmation atomique ; métrique (unité, période, périmètre) ; source primaire exacte ; méthode ; reproduction ; critique ; statut ; effet éditorial.

## A. Faits de contrôle établis par l'orchestrateur

Lus directement dans la base commune (`resultats\donnees\commun\`, Insee, comptes nationaux base 2020, extraits de insee.fr le 20/11/2026 à 09 h 37 UTC ; reproduction : `scripts\commun\construire_base_annuelle.py`). Ils servent d'étalon à la recette. Statut commun : **lu à la source, non contre-expertisé**.

| Id | Affirmation | Valeur | Fichier |
|---|---|---|---|
| F-ORC-001 | Nombre d'exercices à solde négatif des APU de 1975 à 2025, en % du PIB | 51 sur 51 | `base_insee_dep_rec_pctPIB.csv` |
| F-ORC-002 | Années à solde positif depuis 1960 | 1960 à 1966, 1972, 1974 | idem |
| F-ORC-003 | Solde des APU de 1967 à 1974, % du PIB | −0,5 ; −1,4 ; −0,2 ; 0,0 ; −0,3 ; +0,2 ; −0,1 ; +0,1 | idem |
| F-ORC-004 | Dépenses et recettes des APU en 1974, % du PIB | 41,3 et 41,4 | idem |
| F-ORC-005 | Dépenses, recettes, solde en 1975, % du PIB | 46,2 ; 43,2 ; −2,9 | idem |
| F-ORC-006 | Dépenses, recettes, solde en 1985 | 54,2 ; 51,2 ; −3,0 | idem |
| F-ORC-007 | Dépenses, recettes, solde, dette en 1993 | 56,5 ; 50,1 ; −6,4 ; 48,2 | idem |
| F-ORC-008 | Dépenses, recettes, solde, dette en 2000 | 52,6 ; 51,3 ; −1,3 ; 59,7 | idem |
| F-ORC-009 | Dépenses, recettes, solde, dette en 2007 | 53,6 ; 50,6 ; −3,0 ; 65,5 | idem |
| F-ORC-010 | Dépenses, recettes, solde, dette en 2019 | 55,3 ; 53,0 ; −2,4 ; 98,2 | idem |
| F-ORC-011 | Dépenses, recettes, solde, dette en 2025 | 57,3 ; 52,2 ; −5,1 ; 115,7 | idem |
| F-ORC-012 | Meilleur et pire solde depuis 1975 | −0,4 (1980) ; −8,9 (2020) | idem |
| F-ORC-013 | Années de baisse du ratio de dette brute depuis 1979 | 1980, 1988, 1999, 2000, 2001, 2006, 2018, 2019, 2021, 2022, 2023 | idem |
| F-ORC-014 | Variation des dépenses et des recettes, points de PIB : 1974–1985 ; 1985–1993 ; 1993–2000 ; 2000–2007 ; 2007–2019 ; 2019–2025 | +12,8 / +9,7 ; +2,4 / −1,0 ; −3,9 / +1,2 ; +1,0 / −0,7 ; +1,7 / +2,3 ; +2,0 / −0,7 | idem |
| F-ORC-015 | Variation 1974–2025 et 1985–2025 | +16,0 / +10,8 ; +3,1 / +1,1 | idem |
| F-ORC-016 | Solde 2025 par sous-secteur, Md€ | État −128,1 ; ODAC −2,2 ; APUL −15,6 ; ASSO −5,8 ; ensemble −151,6 | `base_insee_solde_sous_secteurs.csv` |
| F-ORC-017 | Série « hors éléments imputés » en 2025, % du PIB | dépenses 53,8 ; recettes 48,7 | `base_insee_dep_rec_pctPIB.csv` |
| F-ORC-018 | Dette nette des APU, % du PIB | 50,5 (2000) ; 58,9 (2007) ; 89,0 (2019) ; 108,4 (2025) | idem |

**Critique commune** : ce sont des lectures d'un seul millésime ; les arrondis au dixième peuvent décaler d'un dixième une différence calculée ; les années antérieures à 1978 n'ont pas de dette dans ce fichier. Ces identités ne disent rien des causes.

## B. Faits des agents

État au 20 novembre 2026, 11 h 36. Les registres détaillés sont dans la section 3 de chaque dossier. Colonne « sondage » : nombre d'affirmations que l'orchestrateur a relues lui-même, dans la copie de la pièce conservée par l'agent ou par recalcul sur la base commune, et résultat.

| Dossier | Faits / calculs / pistes | Pièces [C] / [S] / [M] / [X] | Recette | Sondage de l'orchestrateur | Contre-expertise |
|---|---|---|---|---|---|
| A01 | 19 / 9 / 5 | 56 / 4 / 6 / 9 | passée avec réserves | 7 : 5 confirmées, 1 nuancée, 1 non revérifiée | aucune |
| A02 | 29 / 4 / 4 | 268 / 54 / 82 / 19 | passée avec réserves | 6 : 6 confirmées | aucune |
| A03 | 25 / 6 / 0 | 314 / 16 / 63 / 8 | passée avec réserves | 6 : 6 confirmées | aucune |
| A04 | 41 / 5 / 7 | 162 / 31 / 7 / 3 | passée avec réserves | 6 : 6 confirmées | aucune |
| A05 | 31 / 18 / 6 | 50 / 8 / 5 / 6 | passée avec réserves (légère) | 3 : 3 confirmées | aucune |
| A06 | 52 / 8 / 7 | 49 / 14 / 3 / 2 | passée avec réserves (légère) | 3 : 3 confirmées, dont 1 partiellement | aucune |
| A07 | 45 / 10 / 0 | 61 / 11 / 18 / 2 | passée avec réserves (légère) | 4 : 3 confirmées, 1 en source secondaire | aucune |
| A10 | 30 / 4 / 6 | 65 / 33 / 20 / 23 | passée avec réserves | 3 : 2 confirmées, 1 partiellement | aucune |
| A08, A09, A11, A12 | — | — | en cours | — | — |
| A13 à A18 | — | — | non lancés | — | — |

**Total relu par l'orchestrateur : 38 affirmations sur 272 faits enregistrés.** Aucune n'a été trouvée fausse ; une est nuancée (baisse du ratio de dette en 1979, invisible au dixième publié) ; trois ne sont que partiellement revérifiées. Ce sondage porte sur les affirmations les plus lourdes de conséquences, pas sur un échantillon aléatoire : il ne permet pas d'estimer un taux d'erreur.

## C. Résultats relus par l'orchestrateur (statut : relu, non contre-expertisé)

**Portée de cette relecture.** Les pièces ont été relues dans la copie conservée par l'agent. Pour sept d'entre elles, l'orchestrateur a ensuite retéléchargé le document à l'origine et vérifié qu'il est identique à la copie (avis du HCFP 2026-5 via une archive web, rapport annexé au budget 2027, rapport de la Cour de juillet 2024 via vie-publique.fr, rapport 2026 du COR, prévisions d'automne de la Commission, synthèse du Sénat r24-153, rapport du Sénat n° 133 de 1975) ; le scrutin du 4 novembre 2026 a été retrouvé sur la page d'origine. Les autres lignes restent « relues dans la copie de l'agent ». Détail : `journal\controle_provenance.md`.

| Id d'origine | Affirmation | Pièce relue |
|---|---|---|
| F-A01-018 | Base 2005 de l'Insee : solde de 1974 de +0,45 Md€ ; 1973 de +0,10 | classeur archivé de 2012 |
| C-A01-009 | Zone euro hors France en 2025 : écart de dépenses de 9,2 points, de recettes de 6,7 | recalcul sur la base commune Eurostat |
| F-A01-019 | Impôts et cotisations : France 46,0 en 2025 (Belgique 44,7) ; 2024 : Belgique 45,2, France 45,1 | fichier Eurostat commun (13 pays) |
| A01 §5.8 | Projet de budget 2027 : solde structurel de −5,2 en 2025 ; soldes effectifs de −5,1, −5,4, −5,0 ; loi de programmation : −2,7 en 2027 | texte n° 3210 de l'Assemblée |
| F-A02-005 | Déficit prévu de l'État pour 1975 : 45 698 millions de francs ; plans de soutien « proches de 36 milliards » | Sénat, rapport n° 133 (1975-1976) |
| A02, épisode 8 | Collectif de 2000 : 15,4 milliards de francs de recettes non fiscales exceptionnelles ; TVA : 18,45 puis 31,05 milliards en année pleine | projet de loi n° 2335 ; Sénat, rapport n° 371 |
| A02, épisode 7 | Soulte France Télécom de 37,5 milliards de francs dans le solde de 1997 | Sénat, rapport n° 168 ; audit de 1997 |
| A03 §12 | Avis du HCFP sur le budget 2027 : « très peu vraisemblable » | avis n° 2026-5 lu via une archive |
| A03 §12 | Charge de la dette de l'État : 74,9 Md€ en 2027 en comptabilité nationale | rapport annexé au budget 2027, tableau 18 |
| A03, épisode 6 | Vote du 4 novembre 2026 : 458 contre, 0 pour ; 5,9 % annoncés par le ministre | compte rendu de séance |
| A03, épisode 5 | Mesures d'urgence et de relance : 83,7 ; 34,9 ; 12,4 Md€ de 2021 à 2023 | Cour des comptes, juillet 2024, via vie-publique.fr |
| A03 | Commission : déficit de 5,5 % en 2026, 5,4 % en 2027 | prévisions d'automne 2026 |
| F-A04-001 | Cour : baisses d'impôts de 2018–2023 « estimé à 62 Md€ en 2023, soit 2,2 pts de PIB » | rapport de juillet 2024, via vie-publique.fr |
| F-A04-005 | Mesures nouvelles : −9,7 Md€ (2018), −23,6 (2019), +23,0 dont +8,0 exceptionnels (2025) | Insee Première n° 1753, 1801, 2106 |
| F-A04-021 | Pacte Dutreil réévalué de +4,2 Md€ | évaluation des voies et moyens du budget 2026 |
| F-A04-028 | Suppression des exonérations générales : 980 000 emplois détruits dans une simulation | rapport Bozio-Wasmer, 2024 |
| F-A04-031 | TVA dans la restauration : environ 56 % du gain aux propriétaires | note IPP n° 32 |
| A05 §15 | Ratios par fonction 2024 d'Eurostat : France 57,3 contre 57,0 au compte principal | base commune |
| F-A06-014 | 3,7 points de dépenses de retraite évitées en 2018, contre un scénario indexé sur les salaires | COR, document n° 7 du 16 octobre 2025 |
| A06 §12 | Cotisants par retraité : 2,1 en 2002, 1,8 en 2025 | rapport annuel 2026 du COR |
| A07 R5 | Taux à 10 ans d'octobre 2026 : France 4,89 ; Italie 4,68 ; écart avec l'Allemagne 147 points de base (51 en mai 2024) | fichier Eurostat téléchargé par A03 (second téléchargement ; mêmes données de la BCE que la série d'A07, pas un second fournisseur) |
| A07 R6 | Crédits du programme 117 pour 2027 : 72,373 Md€ | projet annuel de performances |
| A07 §12 | Commission : écart français au-delà de 160 points de base fin octobre 2026 | prévisions d'automne 2026 |

## D. Index des contrôles de l'orchestrateur, par dossier (généré)

**Généré le 21/11/2026 à 14 h 22 par `scripts\commun\indexer_controles.py`** à partir des comptes rendus de recette. 147 contrôles. Les sections A à C ci-dessus datent de la première vague (20 novembre, 12 h 56) et ne sont pas tenues à jour : **cet index et `corrections_demandees.md` font foi.** Un contrôle « relu dans la copie » porte sur la pièce conservée par l'agent, non sur l'original.

| Dossier | Élément contrôlé | Contrôle | Résultat |
|---|---|---|---|
| A01 | Écart de dépenses France – zone euro hors France : 9,2 points en 2025 ; recettes 6,7 | Recalcul sur `donnees\commun\eurostat_gov_10a_main.csv` : (EA20 − FR) / (PIB EA20 − PIB FR) | **Confirmé** : 9,24 et 6,66 ; poids de la France 18,8 % |
| A01 | Impôts et cotisations : France 46,0 en 2025 devant la Belgique 44,7 ; en 2024, Belgique 45,2 devant France 45,1 | Lecture de `eurostat_gov_10a_taxag.csv` (13 pays) | **Confirmé** sur les 13 pays du fichier commun ; le classement sur 30 pays repose sur l'extraction propre d'A01, non revérifiée |
| A01 | Hors cotisations imputées : France 44,3 contre Danemark 44,2 en 2025 ; Danemark devant en 2024 | idem | **Confirmé** |
| A01 | Projet de loi de finances 2027, article liminaire : solde structurel 2025 de −5,2 ; solde effectif −5,1 / −5,4 / −5,0 pour 2025, 2026, 2027 ; trajectoire de la loi de programmation : −2,7 en 2027 | Lecture de la copie locale du texte n° 3210 de l'Assemblée | **Confirmé** mot pour mot ; dette prévue 119,3 % en 2026 et 121,7 % en 2027 |
| A01 | Base 2005 de l'Insee (capture d'archive de 2012) : solde 1974 de +0,45 Md€, 1973 de +0,10, ventilation État/ODAC « N.D. » | Lecture directe du classeur archivé | **Confirmé** : 1974 +0,4467 ; 1973 +0,0962 ; 1972 +0,5497 ; 1970 +0,1222 ; 1975 −6,5963 |
| A01 | Le ratio de dette a baissé 12 années, dont 1979 | Lecture de la série publiée | **Nuance** : en 1979 le ratio publié est inchangé à 21,6 % ; la baisse n'existe qu'au-delà de la première décimale. Onze années au dixième publié (F-ORC-013) |
| A01 | Solde structurel 2025 de −4,7 selon la Commission (prévisions d'automne 2026, annexe) | Tentative de lecture du tableau 38 du PDF local | **Non revérifié** par l'orchestrateur (tableau en colonnes, extraction non concluante) ; à reprendre par A18 ou CX-05 |
| A02 | Déficit du budget de l'État prévu pour 1975 : de +27 millions à −45,7 milliards de francs, 3,57 % de la production intérieure brute prévue | Sénat, rapport n° 133 (1975-1976) | **Confirmé** : « 45 698 millions de francs », « 3,57 % » |
| A02 | Plans de soutien de 1975 : conséquences budgétaires « proches de 36 milliards de francs » ; perte de recettes de 16,8 milliards dont environ 14 dus aux mesures fiscales | même rapport | **Confirmé** mot pour mot (« 16 805 millions », « environ 14 000 millions ») |
| A02 | Collectif du printemps 2000 : 15,4 milliards de francs de « recettes non fiscales exceptionnelles » (fonds d'épargne 7, CADES 5, COFACE 3) | Projet de loi de finances rectificative n° 2335 | **Confirmé** mot pour mot |
| A02 | Baisse d'un point de TVA : 18,45 milliards de francs en 2000, 31,05 en année pleine | Sénat, rapport n° 371 (1999-2000) | **Confirmé** |
| A02 | Soulte France Télécom de 37,5 milliards de francs comptée dans le solde de 1997 | Sénat, rapport n° 168 (1997-1998) ; audit des finances publiques de 1997 | **Confirmé** ; l'audit écrit « 3,5 – 3,7 % en 1997 en intégrant la soulte » |
| A02 | Solde de 1997 à −3,7 % dans les comptes actuels | Base commune | **Confirmé** (−3,7) |
| A03 | L'avis du HCFP sur le budget 2027 écrit « très peu vraisemblable » ; la formule « semble peu plausible » citée par la V5 n'y figure pas | Avis n° 2026-5, lu via une archive web | **Confirmé** : « rendent très peu vraisemblable sa concrétisation, sauf évolutions conjoncturelles très favorables » ; « peu plausible » : aucune occurrence dans cet avis |
| A03 | Charge de la dette de l'État prévue à 74,9 Md€ pour 2027 dans le rapport économique, social et financier (la V5 dit 72) | Rapport annexé au projet de budget 2027, tableau 18 | **Confirmé** : 39,0 ; 44,5 ; 51,8 ; 64,9 ; **74,9** ; 86,8 ; 97,1 ; 107,4 de 2023 à 2030, en comptabilité nationale. Les 72 Md€ de la V5 correspondent aux crédits budgétaires du programme 117 (72,4 Md€), retrouvés ensuite par A07 : écart de périmètre, pas d'erreur |
| A03 | Première partie du budget 2027 rejetée par 458 voix contre et aucune pour, le 4 novembre 2026 | Compte rendu de la séance | **Confirmé** : 460 votants, 458 exprimés, 0 pour, 458 contre |
| A03 | Le 5,9 % est une estimation du ministre sur le texte amendé | même compte rendu | **Confirmé** : « À l'issue de l'examen de la première partie, il s'élèverait à 5,9 % » |
| A03 | Mesures d'urgence et de relance : 83,7 Md€ en 2021, 34,9 en 2022, 12,4 en 2023 | Cour des comptes, juillet 2024, lu via vie-publique.fr | **Confirmé** |
| A03 | Commission, automne 2026 : déficit de 5,5 % en 2026 et 5,4 % en 2027 | Fiche France des prévisions | **Confirmé** ; dette prévue à 123,2 % en 2028 |
| A04 | Cour des comptes, juillet 2024 : baisses d'impôts de 2018–2023 « dont l'impact est estimé à 62 Md€ en 2023, soit 2,2 pts de PIB » | Rapport lu via vie-publique.fr (copie locale) | **Confirmé** mot pour mot |
| A04 | Insee : mesures nouvelles de −9,7 Md€ en 2018, −23,6 en 2019, +23,0 en 2025 dont +8,0 de contributions exceptionnelles | Insee Première n° 1753, 1801, 2106 (copies locales) | **Confirmé** pour ces trois années ; 2020 à 2024 non relues |
| A04 | Rapport Bozio-Wasmer : suppression complète des exonérations générales = 980 000 emplois détruits, environ 19 Md€ de cotisations perdues | Copie locale du rapport, p. 68–69 | **Confirmé** ; c'est une illustration par simulation, présentée comme telle |
| A04 | Projet de budget 2026, évaluation des voies et moyens : Pacte Dutreil réévalué de +4,2 Md€ « résultant d'une nouvelle actualisation de son chiffrage » | Copie locale du tome II | **Confirmé** mot pour mot |
| A04 | Note IPP n° 32 : environ 56 % du gain de la baisse de TVA aux propriétaires de restaurants, 18,6 % aux salariés, 12,1 % aux fournisseurs | Copie locale de la note | **Confirmé** |
| A04 | Reconstitution des 62 Md€ : −2,29 points de PIB cumulés de 2018 à 2023, −1,40 point à fin 2025 | Relecture du fichier de calcul | Arithmétique **cohérente** avec les valeurs sources ; le rapprochement avec le chiffre de la Cour est une reconstitution d'A04, pas la méthode de la Cour |
| A05 | Dans le fichier Eurostat des dépenses par fonction, les ratios 2023–2024 reposent sur un PIB d'un millésime antérieur : France 2024 à 57,3 au lieu de 57,0 ; Allemagne 49,4 au lieu de 49,0 | Comparaison directe de `eurostat_gov_10a_exp.csv` et `eurostat_gov_10a_main.csv` | **Confirmé** : France 57,3 (provisoire) contre 57,0 ; Allemagne 49,4 contre 49,0 ; zone euro 49,2 contre 49,3 ; Suède et Italie cohérentes |
| A05 | Conséquence : l'écart France – zone euro de 2024 vaut environ 7,7 à 7,8 points, non 8,1 | 57,0 − 49,3 | **Confirmé** : 7,7 au dixième publié ; le tableau d'Astra reprend les ratios du fichier par fonction |
| A05 | Variation du ratio de dépense : +12,8 points de 1974 à 1985 sur +16,0 depuis 1974 | Faits de contrôle F-ORC-014 et F-ORC-015 | **Confirmé** (80 %) |
| A06 | Les « 3,7 points » de dépenses de retraite évitées en 2018 viennent du document n° 7 de la séance du COR du 16 octobre 2025 ; le contrefactuel inclut une indexation sur les salaires | Document n° 7, p. 6 | **Confirmé** : « 3,7 points de pourcentage de plus » en 2018 ; 19,5 % contre 13,2 % du PIB à terme ; la phrase suivante porte sur « le passage à une indexation prix » |
| A06 | Cour des comptes, février 2025 : plusieurs chiffrages de la réforme de 2023, dont des modèles macroéconomiques exprimés en points de PIB de 2033 | Rapport lu via vie-publique.fr, p. 66 | **Confirmé** pour l'existence du tableau n° 4 et des deux modèles ; les valeurs (+0,1 à +0,9 point) n'ont pas été relues cellule par cellule |
| A06 | Rapport cotisants/retraités : 2,1 en 2002, 1,8 en 2025 | Rapport annuel 2026 du COR | **Confirmé** : « passant de 2,1 à 1,8 en 2025 » (page 74 du PDF) ; la valeur de 2070 n'a pas été relue |
| A07 | Taux à 10 ans en octobre 2026 (moyenne mensuelle) : France 4,89 %, Italie 4,68 % ; écart avec l'Allemagne de 147 points de base, contre 51 en mai 2024 | Second téléchargement : fichier Eurostat récupéré par A03 (série dérivée des mêmes données de la BCE que celle d'A07 ; ce n'est pas un second fournisseur) | **Confirmé** : France 4,89 ; Allemagne 3,416 ; Italie 4,68 ; écart 147 ; mai 2024 : 51 |
| A07 | Charge de la dette de l'État pour 2027 : 72,4 Md€ de crédits | Projet annuel de performances du programme 117, copie locale | **Confirmé** : 72 373 000 000 € (dette 71,884 ; trésorerie 0,489) ; 58,6 Md€ en loi de finances 2026 |
| A07 | La Commission écrit que l'écart français a dépassé 160 points de base fin octobre | Prévisions d'automne 2026, copie locale | **Confirmé** : le taux français à 10 ans « increased to around 5% at the end of October », écart « exceeded 160 bps », contre 65 début mai ; la Commission l'associe à l'incertitude perçue par les marchés |
| A07 | Convention de 1973 plafonnant les avances de la Banque de France à 20,5 milliards de francs | Copie locale | **Confirmé dans une source secondaire** (article de revue de 2014) ; les textes du Sénat de 1972–1973 conservés par A07 n'ont pas été relus par l'orchestrateur |
| A08 | Colonne « exécuté » de la table | Comparaison ligne à ligne avec la base commune de l'Insee | **145 lignes comparées, aucun écart** supérieur à 0,06 point |
| A08 | Écart moyen entre solde programmé et solde exécuté, hors 2009 et 2020 : −0,23 point pour l'année en cours, −1,07 à un an, −2,05 à deux ans, −2,93 à trois ans | Recalcul direct à partir de la table d'A08 | **Reproduit à l'identique** ; part des cas défavorables : 57 %, 81 %, 97 %, 100 % |
| A08 | Rapport d'information de l'Assemblée n° 1891 : un amendement de suppression d'un article est « toujours recevable » | Pièce **retéléchargée à l'origine** par l'orchestrateur (identique à la copie d'A08), p. 40 | **Confirmé** : « Un amendement de suppression d'un article est toujours recevable puisque l'Assemblée peut décider de maintenir la législation en vigueur en votant contre l'adoption de l'article » |
| A08 | Loi de programmation de décembre 2023 : −2,7 % en 2027 | Déjà relu dans le projet de budget 2027 (recette d'A01) | **Confirmé** |
| A09 | Partie recettes du budget 2025 rejetée, 192 pour, 362 contre | n° 438, 12 novembre 2024 | **Confirmé** |
| A09 | Partie recettes du budget 2026 rejetée, 1 pour, 404 contre | n° 4241, 21 novembre 2025 | **Confirmé** |
| A09 | Partie recettes du budget 2027 rejetée, 0 pour, 458 contre | n° 9759, 4 novembre 2026 | **Confirmé** |
| A09 | Censure du 4 décembre 2024 adoptée par 331 voix | n° 519 | **Confirmé** |
| A09 | Confiance refusée le 8 septembre 2025, 194 pour, 364 contre | n° 3054 | **Confirmé** |
| A10 | Les séries d'opinion de la Drees sont recalculées à partir des microdonnées publiques | Script `drees_test_principe_mesure.py` relancé par l'orchestrateur | **Le script tourne** et régénère le tableau par année et par groupe (cette relance a réécrit le fichier de sortie d'A10 ; le contenu avant et après n'a pas été comparé) ; les valeurs 2025 n'ont pas été comparées une à une au texte |
| A10 | Sondage de juillet 2025 pour RTL : 1 006 personnes ; 73 % approuvent l'objectif de déficit | Copie locale du rapport de l'institut | **Confirmé** pour l'échantillon et les 73 % ; les 39 % (année blanche) et 30 % (jours fériés) sont dans des graphiques dont l'extraction de texte ne restitue pas les valeurs : non revérifiés |
| A10 | Les quatre étages de preuve sont tenus séparés ; les résultats non lus en texte intégral sont signalés | Relecture des sections 12 et 13 | **Conforme** : chaque affirmation de la V5 est rattachée à un étage ; une erreur de mémoire sur une référence est documentée et corrigée par l'agent |
| A11 | Coût du pacte Dutreil « supposé de 500 M€ par an de 2011 à 2024 », 800 M€ au budget 2025, plus de 5,5 Md€ en 2024 selon la Cour ; 65 % pour 1 % des bénéficiaires, soit 110 personnes ; « jamais évalué » | Synthèse de la Cour, novembre 2025 (copie vérifiée identique à l'archive) | **Confirmé** mot pour mot ; la Cour donne aussi 1,2 Md€ en 2020, 2,0 en 2022, 3,3 en 2023 |
| A11 | Proposition de loi n° 1341 « retirée par son auteur le 5 juin 2025, au cours de la discussion en séance publique » | Texte de l'Assemblée (copie vérifiée identique à l'origine) | **Confirmé** |
| A11 | Le Gouvernement avait actualisé l'article d'équilibre du même budget au Sénat le 30 novembre 2023 (amendement I-2300) ; la note du 7 décembre « recommande de ne pas communiquer » | Sénat, rapport n° 685, p. 82–83 (copie d'A11) | **Confirmé** ; le rapport ajoute que le Gouvernement « aurait pu décider d'actualiser » |
| A11 | Revue de l'IGF de 2024 : environ 400 M€ d'économies proposées sur le crédit d'impôt recherche ; « oppositions recueillies : France industrie » | Rapport lu via vie-publique.fr (copie d'A11) | **Confirmé** |
| A12 | Aucun excédent en France de 1995 à 2025 ; l'Italie non plus | Recalcul de l'orchestrateur sur la base commune Eurostat (13 pays) | **Confirmé** sur 1995–2025 : France 0, Italie 0 ; Autriche 2, Belgique 3, Espagne 3. La période 1975–1994 repose sur les séries de l'OCDE et de la Commission utilisées par A12, non recalculées |
| A12 | La France est le seul pays de l'Union sans excédent primaire depuis 2002 | Recalcul de l'orchestrateur : solde plus intérêts versés, 13 pays, 2002–2025 | **Confirmé sur les 13 pays du fichier commun** : France 0 année ; Italie 19, Belgique 13, Allemagne 12, Portugal 9, Grèce 8, Espagne 6. Les 14 autres pays de l'Union reposent sur le contrôle d'A12 |
| A12 | Persson, 1995 : « presque deux tiers des mesures sont des baisses de dépenses » ; objectif soutenu par « 94 % » du Parlement ; « ne dites jamais que ça ne fera pas mal » ; plafond pluriannuel de dépenses proposé | Lecture directe du PDF conservé par A12 | **Confirmé** dans la copie de l'agent ; le retéléchargement à l'origine a échoué (délai dépassé) : copie non vérifiée contre l'origine |
| A13 | Enveloppe centrale, si adoptée : 20,6 / 33,2 / 57,7 Md€ en 2027, 2030, 2035 ; après décote d'exécution : 13,5 / 21,7 / 35,6 | Somme refaite à partir de la table des mesures, variantes exclues | **Reproduit à l'identique** pour les six totaux |
| A13 | Un cinquième à un quart du net du portefeuille « dépense » est un prélèvement au sens de la comptabilité nationale | Somme des mesures classées en prélèvements, enveloppe centrale 2030 | **Reproduit** : 7,1 Md€ sur 33,2, soit 21 % (gel des allègements de cotisations, crédit d'impôt recherche) |
| A13 | Cour, novembre 2026 : gel des prestations hors minima, 4,8 Md€ en 2027 et 5,2 en année pleine ; masse salariale, 3,9 Md€ en 2027 ; recoupement avec les projets du Gouvernement, 11 à 14 Md€ | Texte de la contribution, pièce vérifiée identique à l'archive web lors de la recette d'A14 | **Confirmé** pour les trois chiffres |
| A13 | Le PDF de la Cour utilisé par A13 est le même que celui partagé par l'orchestrateur | Comparaison d'empreintes | **Identique** pour le rapport ; la synthèse est un second fichier, non comparé |
| A14 | Totaux nets centraux : 18,8 / 18,6 / 18,6 (prudente), 30,1 / 38,1 / 47,4 (centrale), 32,9 / 46,2 / 56,2 Md€ (ambitieuse) en 2027, 2030, 2035 | Somme refaite à partir de la table des mesures | **Reproduit** (33,0 au lieu de 32,9 pour une cellule : arrondi) |
| A14 | Sur les 38,1 Md€ de l'enveloppe centrale en 2030 : 9,3 du budget 2027 rejeté, 6,0 de pérennisations, 11,8 de mesures de la Cour, 11,1 nouveaux | Somme refaite par origine | **Reproduit** |
| A14 | Cour des comptes, contribution du 9 novembre 2026 : ensemble de mesures de 32 à 38 Md€ ; TVA à 20 % dans la restauration et certains services : 4,6 Md€ en 2027 ; fin de l'abattement de 10 % sur les pensions : 5,8 Md€ en régime de croisière, 7,3 la première année | Pièce **retéléchargée par l'orchestrateur** depuis une archive web du 14 novembre 2026, identique à la copie d'A14 ; texte relu | **Confirmé** mot pour mot |
| A14 | IPP, rapport n° 60 (octobre 2025) sur la baisse des impôts de production : pas d'effet significatif sur les entreprises | Pièce **retéléchargée à l'origine**, identique ; texte relu | **Confirmé** : la seconde étape « ne trouve aucun effet significatif » |
| A15 | Les scripts tournent de bout en bout | Copie des quatre scripts hors du dossier, sortie redirigée, relance de la validation, de l'exécution et de l'historique | **24 fichiers de sortie identiques octet pour octet** à ceux de l'agent ; fichiers de l'agent non touchés |
| A15 | Déficit de 2027 « à politique inchangée » : 6,5 % (rapport économique, social et financier pour 2027) | Texte relu dans la copie d'A03 | **Confirmé** : « avoisinerait 6,5 % », avant les mesures du budget 2027 |
| A15 | Commission, prévision d'automne du 17 novembre 2026 : déficit 5,5 % en 2026 et 5,4 % en 2027 ; intérêts 2,6 %, 3,0 % puis 3,3 % du PIB en 2026, 2027 et 2028 | Document **retéléchargé à l'origine** (264 pages), page 139 relue | **Confirmé** pour les cinq chiffres ; la Commission attribue la hausse aux taux à l'émission et aux obligations indexées |
| A15 | Passage de 5,1 % (2025) à 6,5 % (2027) : intérêts +0,8, cycle +0,5, reste +0,1 | Table relue ; la hausse des intérêts (2,2 → 3,0 % du PIB) est celle de la Commission | **Cohérent** avec la pièce ; la part du cycle vient du modèle, non recoupée |
| A15 | Référence : déficit de 7,3 % en 2030 et dette de 154 % en 2035 | Identité de dette refaite de tête sur trois années ; hypothèses relues | **Cohérent avec ses hypothèses** : aucune mesure votée pendant neuf ans, y compris celles du budget 2027, et taux à l'émission de 4 % à long terme. Ce n'est pas une prévision |
| A16 | Pré-enregistrement figé avant la phase 2 | Empreinte recalculée ; horodatages | **Conforme** (e49820aa…) ; fichier daté de 18 h 44, dossier de 19 h 07 |
| A16 | Fichiers d'A15 non modifiés par le rejeu du contradicteur | Comparaison des 24 sorties d'A15 avec le rejeu fait par l'orchestrateur à 18 h 41 | **Identiques** : rien n'a été touché |
| A16 | Indépendance vis-à-vis d'A17, d'A18 et de Codex | Déclaration de l'agent | Non vérifiable par l'orchestrateur |
| A16 | Taux d'emploi des 60–64 ans en 2025 : France 44,4 %, Allemagne 67,6 % | Eurostat interrogé directement par l'orchestrateur | **Confirmé** (2024 : 42,4 et 66,6) |
| A16 | Scénarios de norme de dépense | Sortie du script lue en entier pour le taux de 4 % | **Cohérent avec le message** : voir §3 |
| A17 | Pré-enregistrement figé avant la phase 2 | Empreinte recalculée ; horodatages | **Conforme** (c728f1ed…) ; fichier daté de 18 h 45, dossier de 19 h 08 |
| A17 | Fichiers d'A15 non modifiés | Comparaison des 24 sorties d'A15 avec le rejeu de l'orchestrateur | **Identiques** |
| A17 | Indépendance vis-à-vis d'A16 | Recherche du mot « A16 » dans le dossier : il n'apparaît que dans la liste des fichiers non lus | Cohérent avec la déclaration ; non vérifiable autrement |
| A17 | Correction d'A15 : au taux de 2,8 %, la combinaison la plus large ne stabilise pas la dette | Sortie d'A15 (« dette 2030 126, 2035 132, 2040 135 ») et sortie d'A17 (« 132, 135, puis 144 en 2050 ») relues | **Confirmé** : A15 arrêtait sa lecture en 2040 et écrivait « presque stable » ; la dette continue de monter. La réserve inscrite dans la recette d'A15 (« le résultat central dépend du taux ») est donc **trop favorable** : même à 2,8 %, aucune combinaison ne stabilise |
| A18 partie1 | Passe 1 figée avant la confrontation | Empreinte du fichier `A18_audit_V5_passe1.csv` recalculée ; horodatages | **Empreinte conforme** à celle annoncée (d8832d18…) ; fichier daté de 18 h 47, passe 2 de 19 h 01. Que l'agent n'ait rien lu de la cellule avant 18 h 47 est sa déclaration : non vérifiable par l'orchestrateur |
| A18 partie1 | Décompte des verdicts | Recompté par script dans `passe2.csv` | **208 lignes** : 167 exact, 16 non démontré, 12 trop général, 7 inexact, 4 non vérifié, 2 sans verdict. Le message de fin annonçait 200 lignes et 162 / 15 / 12 / 7 / 4 : il ne compte pas les lignes ajoutées en passe 2. **Les fichiers font foi** |
| A18 partie1 | « La charge de la dette pèsera autant que tout le budget de la Défense : 72 milliards » | Projet de loi de finances pour 2027 **retéléchargé à l'origine**, identique ; état B relu p. 246–247 | **Confirmé** : Défense, 73,15 Md€ de crédits de paiement, pensions comprises ; charge de la dette, 72,37 Md€ (58,6 en 2026). La phrase de la V5 tient ; la cellule ne l'avait pas vérifiée pensions comprises |
| A18 partie1 | Un député peut déplacer des crédits entre programmes d'une même mission | Rapport de l'Assemblée n° 1891 **retéléchargé à l'origine**, identique ; p. 99 relue | **Confirmé**. Corrige la formule d'A08 reprise dans la transmission de la vague 2 : un parlementaire ne peut pas augmenter le total d'une mission, mais il peut y redéployer |
| A18 parties2et3 | Fichier de la première passe d'audit intact | Empreinte recalculée | **Inchangée** (d8832d18…) |
| A18 parties2et3 | Décompte de l'arbitrage | Recompté par script dans `A18_arbitrage.csv` | **19 lignes** : 15 attaques (2 fondées, 12 fondées en partie, 1 non fondée), la correction d'A17 sur le taux de 2,8 % (fondée), et 3 tensions (2 « dépend d'une convention », 1 « indécidable ») |
| A18 parties2et3 | Décompte des vérifications | Recompté dans `A18_verification_25.csv` | **28 lignes**, aucune infirmée ; 2 relues dans la copie seulement ; 2 recalculées en partie ; 6 dépendent d'une convention |
| A18 parties2et3 | « De 2015 à 2019, la France est le seul pays étudié dont la dette monte » | Recalcul par l'orchestrateur sur la base commune | **Constat d'A18 confirmé** : la Grèce aussi (179,6 → 183,2 % ; France 97,0 → 98,2 %). « Seul pays » ne vaut que hors Grèce |
| C01 | Dossier de l'équipe Codex intact | Décompte des fichiers et recherche de toute modification postérieure à 11 h 10 | **113 fichiers, aucun modifié** ; l'agent a travaillé sur des copies placées dans le dossier de la cellule |
| C01 | Décompte de la concordance | Recompté dans `C01_concordance_audit.csv` | **211 lignes** : 174 accords, 17 désaccords, 15 lignes auditées par la cellule seule, 4 par Codex seul, 1 sans objet |
| C01 | Taux à dix ans au-dessus de 5 % « le 22 octobre » | Page de la Banque de France **relue à l'origine** par l'orchestrateur | **Confirmé** : les valeurs 4,985 et 5,126 y figurent. La V5 a raison ; l'objection de la cellule (« le 21 », d'après la presse) n'est pas établie |
| C01 | HCFP : « semble peu plausible » | Compte rendu de l'audition à l'Assemblée du 1er octobre 2026, relu dans la copie de l'agent | **Confirmé** : « il nous semble peu plausible qu'elle soit atteinte en 2029 ». La phrase existe, dans une audition, non dans l'avis écrit. L'identité de l'orateur n'a pas été recontrôlée par l'orchestrateur |
| C02 | Dossier de l'équipe Codex intact | Décompte, recherche de modification après le 20 novembre à 11 h 10, comparaison des deux relevés d'empreintes de l'agent | **113 fichiers, aucun modifié ; empreintes identiques au début et à la fin** |
| C02 | « Aucun excédent primaire depuis 2002 » dépend de la convention | **Recalcul de l'orchestrateur** sur la base commune (Eurostat, solde plus intérêts versés) | **Confirmé** : en 2006, le solde primaire est de **−1,0 Md€** (−49,06 + 48,06), soit 0,05 % du PIB. Le résultat tient dans cette convention, à un milliard près |
| C02 | Variante de l'Insee où 2006 devient un excédent de 0,4 Md€ | Sortie du script de l'agent relue | **Cohérent** : 9 années d'excédent primaire de 1975 à 2025 avec les intérêts versés, 11 hors correction des services bancaires (dont 2006), 7 en intérêts nets. Non recalculé par l'orchestrateur |
| C03 | Dossier de l'équipe Codex intact | Décompte et recherche de modification depuis le 20 novembre, 11 h 10 | **113 fichiers, aucun modifié** |
| C03 | Fichiers d'A15 intacts | Comparaison des 24 sorties avec le rejeu de l'orchestrateur du 20 novembre | **Identiques** |
| C03 | La table de passage somme à l'écart | Somme refaite à la main : 5,168 − 1,494 − 0,957 + 0,677 − 0,526 + 0,227 + 0,209 − 0,206 − 0,020 | **3,078** : égal au chiffre de Codex ; reste inexpliqué nul |
| C03 | Sénat, 18 novembre 2026 : budget de la Sécurité sociale pour 2027 adopté modifié par 201 voix contre 124 | Compte rendu **retéléchargé à l'origine**, identique ; scrutin n° 118 relu | **Confirmé** : 340 votants, 325 exprimés, 201 pour, 124 contre |
| R01 | Lecture | Rapport lu **en entier** (469 lignes, sections 0 à 10) | Structure imposée respectée ; aucune recommandation ; aucun verdict sur la thèse ; aucune formulation pour le film |
| R01 | Table des 50 affirmations | Tous les nombres de la colonne « valeur » cherchés par script dans les comptes rendus de recette, le fichier des corrections, les transmissions et les tables d'A18, C01 et C02 | **Aucune ligne avec un nombre introuvable** (contrôle de transcription) |
| R01 | Corrections de l'arbitrage et de la comparaison | Recherche des formules corrigées : excédent primaire et 2006 ; deux références d'effort ; « mesures chiffrées » ; taux de 2,8 % ; multiplicateurs en fourchette ; 13 à 32 % ; norme sans précédent ; Grèce | **Toutes présentes** |
| R01 | Masse salariale | « 88 Md€, recalculé par l'orchestrateur » : le recalcul donnait 87 | **Corrigé** dans le rapport (« 87 à 88 Md€ ») |
| S01 | Déficit d'exécution du budget de l'État en 1975 : 37,8 milliards de francs | Sénat, rapport n° 378 (1976-1977) sur le règlement de 1975, p. 53 | **Confirmé** : « un déficit de 37,8 milliards » |
| S01 | Une partie des mesures de 1975 est un décalage de trésorerie | même rapport, p. 15 | **Confirmé** pour un élément : recettes de 1975 minorées « de 5 milliards de versements reportés à 1976 » ; le total de 7,4 milliards retenu par S01 n'a pas été relu |
| S01 | Retraite à 60 ans : coût annoncé de 3 à 5 milliards de francs pour 1985 | Sénat, rapport n° 131 (1981-1982) | **Confirmé** : « 3 à 5 milliards de francs pour l'échéance 1985 », financement prévu « en partie » par la disparition de la garantie de ressources |
| S02 | Budget fédéral canadien de 1995 et étude de l'IRPP de 2006 conservés dans `donnees\S02\sources\` | Pièces **retéléchargées à l'origine** (budget.canada.ca, irpp.org), empreintes comparées | **Identiques** (425 200 et 331 821 octets) |
| S02 | Canada, 1994 à 1999 : 82 % de l'amélioration primaire vient des dépenses | Recalcul à partir du tableau de l'agent (`S02_canada_decomposition.csv`, en lecture seule) : recettes +1,31 point, dépenses primaires courantes −5,39 | **80 %** par ce calcul ; **82 %** avec la définition de l'agent (solde primaire moins recettes, investissement compris). Écart de définition, pas d'erreur |
| S02 | Même grandeur sur d'autres fenêtres | Même tableau | **76 %** (1994–1997), **88 %** (1993–1997), **90 %** (1993–1999) : la part dépend de l'année de départ |
| S03 | Les trois scripts tournent dans l'ordre indiqué | Copie hors du dossier, sortie redirigée, relance | **4 fichiers de sortie identiques octet pour octet** ; fichiers de l'agent non touchés |
| S03 | Inertie identifiée : 46 à 89 % selon douze conventions ; décisions chiffrées : 3 à 7 % ; plafond de la part décidée : 11 à 54 % | Récapitulatif produit par le rejeu | **Reproduit** ; la part d'inertie dépasse 50 % dans 11 conventions sur 12 |
| S03 | Revalorisations des pensions du régime général, 1974–1985 : 11,45 % par an ; PIB nominal par emploi : 11,49 % ; prix : 9,63 % | Sortie du rejeu | **Reproduit** |
| S03 | Conseil des ministres du 9 février 1983 : +26,6 % en vingt mois pour les pensions, +56 % pour le minimum vieillesse | Texte relu dans la copie de l'agent (page de vie-publique.fr obtenue par une archive web) ; la page d'origine n'a rendu que 44 caractères à l'orchestrateur | **Confirmé dans la copie** ; non relu à l'origine |
| S03 | Note du Conseil d'orientation des retraites et publication de l'Insee de 1986 conservées par l'agent | **Retéléchargées à l'origine**, empreintes comparées | **Identiques** (230 029 et 3 702 256 octets) |
| S04 | Note de l'Institut des politiques publiques n° 129 (septembre 2026) et chapitre fiscal de juin 2025 | **Retéléchargés à l'origine** (ipp.eu), empreintes comparées | **Identiques** (1 856 684 et 3 263 590 octets) |
| S04 | Fichier de la Drees sur les déremboursements | Retéléchargement tenté | **Refusé par le site** (page de rejet de 6 291 octets) ; l'agent l'avait signalé et obtenu la pièce par un autre canal ; empreinte de sa copie conforme à son manifeste |
| S04 | Gel des pensions : 37 à 40 % de l'effort sur la moitié la plus modeste, 14 à 16 % sur les 10 % les plus aisés ; suppression de l'abattement : 17 à 18 % et 24 à 28 % | Table de calcul relue (`C-S04-001`) | **Cohérent avec la table** : 0,374 à 0,386 et 0,148 à 0,150 pour le gel ; 0,167 à 0,174 et 0,249 à 0,250 pour la suppression ; la borne de 28 % vient d'une seconde source non relue |
| S05 | Note de France Stratégie de 2019, note du Conseil d'analyse économique, note de l'OFCE sur l'apprentissage | **Retéléchargées à l'origine**, empreintes comparées | **Identiques** |
| S05 | France Stratégie : l'excès des dépenses de fonctionnement des administrations « représente tout au plus 0,5 point de PIB », « sans doute surestimé » | Phrase relue dans la pièce | **Confirmé**, « sur un total de 6 points de PIB » |
| S05 | Aides au logement : 78 % de l'aide absorbée par la hausse des loyers | Phrase relue (Insee, *Économie et statistique*, 2005) | **Confirmé** |
| S05 | Cour des comptes, mai 2026 : hospitalisations inadéquates, 3,2 Md€ pour les séjours trop longs | Phrase relue dans la copie (vie-publique.fr) | **Confirmé** : 4,2 Md€ en 2024, dont 3,2 pour les séjours anormalement longs et 1 pour les admissions évitables |
| S06 | Masse salariale publique en 2025 : France 12,4 % du PIB ; zone euro hors France 9,5 % ; écart de 2,9 points, 88 Md€ | **Recalcul indépendant** à partir de la base commune (Eurostat, extraction du 20 novembre), sans le script de l'agent | **Reproduit** : 12,37 ; 9,47 ; 2,90 points ; 87 Md€. En 1995 : 13,53 contre 10,11, écart de 3,42 points. Allemagne : 8,47 % en 2025 |
| S06 | Note du Sénat sur les affaires européennes (budget 2027) et lettre du Cepii n° 394 | **Retéléchargées à l'origine**, empreintes comparées | **Identiques** |
| S06 | Cepii : contribution de l'immigration aux finances publiques « plutôt négative mais faible, jamais en deçà de −0,5 % du PIB » | Phrase relue dans la pièce | **Confirmé** (scénario de référence, période 1979–2011) |
| S06 | Contribution brute à l'Union : 23,0 Md€ | Recherche du chiffre dans la note du Sénat | **Non retrouvé par l'orchestrateur** sous cette forme ; non contrôlé |
| S07 | Trois documents de la Commission (modèle de 2013, évaluations des programmes irlandais et espagnol) | **Retéléchargés à l'origine**, empreintes comparées | **Identiques** |
| S07 | FMI, évaluation du programme grec : multiplicateur supposé de 0,5, puis « twice the size » | Phrase relue dans la pièce | **Confirmé** : « Recent iterations of the Greek program have assumed a multiplier of twice the size » |
| S07 | Commission, programme irlandais : pas d'évaluation a posteriori de l'effet des mesures | Phrase relue | **Confirmé** : « no ex post assessment of the actual impact of the measures was undertaken » |
| S07 | Étude du FMI de 2011 : une consolidation d'un point de PIB réduit le PIB de 0,62 % à deux ans | Phrase relue dans les deux copies (archive web et copie de Codex) | **Confirmé** |
| S08 | Deux rapports du Sénat et l'étude de l'Insee sur les réformes du capital de 2018 | **Retéléchargés à l'origine**, empreintes comparées | **Identiques** |
| S08 | Réformes du capital de 2018 : 80 % du gain aux 10 % les plus aisés | Phrase relue dans l'étude de l'Insee | **Confirmé** : « Au total, les 10 % les plus aisés obtiennent 80 % du gain total de niveau de vie » (trois réformes cumulées) |
| S08 | Ensemble des mesures pour les ménages, 2017–2022 : 17 % du gain aux 5 % les plus aisés | Phrase relue dans la note de l'OFCE | **Confirmé** : sur 22 Md€ de hausse simulée du revenu disponible, 17 % au dernier vingtième |
| S08 | Aucune période de trois ans où la dépense primaire recule en volume, de 1976 à 2025 | **Recalcul de l'orchestrateur** sur la série d'A16 | **Reproduit** : minimum +0,18 % cumulé en 2022–2024 ; quatre années isolées en baisse (2015, 2018, 2022, 2023) |
| S10 | Deux rapports du Sénat de 1982–1983 | **Retéléchargés à l'origine**, empreintes comparées | **Identiques** |
| S10 | Pièce maîtresse : tableau du coût de la politique de l'emploi (ministère, septembre 1986), document scanné transcrit à la main par l'agent | **Page relue en image par l'orchestrateur** | **Transcription exacte** : « incitation au retrait d'activité », 1 576,9 millions de francs en 1973, 10 966,3 en 1980, 50 736,3 en 1983, 56 202,6 en 1985 (provisoire) ; le texte dit que la garantie de ressources « pèse encore près de 29 » milliards et les contrats de solidarité « plus de 10 » en 1985 |
| S10 | Conversion en points de PIB | Refaite à la main : 56,2 / 4 916,9 et 29 / 4 916,9 | **1,14 et 0,59 point** : conforme |
| S10 | Total de 1985 | Somme refaite à partir de la table de l'agent | **Reproduit** : 0,81 / 1,27 / 1,99 point (bas, central, haut) |
| S11 | Pré-enregistrement figé avant tout calcul | Empreinte recalculée ; horodatages des fichiers | **Conforme** (ddae1d64…) : fichier de 10 h 37 min 04 s ; premier script à 10 h 41 min 16 s ; premières sorties à 10 h 41 min 22 s |
| S11 | Les tests se rejouent | Copie du script hors du dossier, sortie redirigée, relance | **5 fichiers de sortie identiques octet pour octet**, et l'affichage identique au fichier de sortie conservé |
| S11 | Contrôle mécanique | 17 titres ; 22 pièces consultées, 2 souvenirs, 3 recherches infructueuses ; manifeste de 7 pièces avec adresse d'origine | conforme |
| S12 | Pré-enregistrement de la partie B figé avant calcul | Empreinte recalculée ; horodatages | **Conforme** (322e0998…) : fichier de 11 h 15 ; script de 11 h 21 ; sorties de 11 h 26 |
| S12 | Décompte des majorités | Recompté par script dans la table de l'agent | **42 exercices** votés par une majorité absolue (22 par un seul groupe, 20 par une coalition), 9 sans ; 6 désaccords avec A09, tous dans le même sens ou sans effet |
| S12 | Déficits et excédents primaires par type de majorité | Recompté dans la même table | **42 déficits sur 42** sous majorité absolue, **9 sur 9** sans ; excédents primaires : **6 sur 42** sous majorité absolue (tous sous coalition : 1979, 1980, 1998 à 2001), **3 sur 9** sans (1987, 1989, 1990) ; aucun sous la majorité absolue d'un seul groupe |
| S12 | Contrôle mécanique | 17 titres ; 38 pièces consultées, 4 souvenirs ; manifeste de 33 pièces avec adresse d'origine | conforme |
| S13 | Trois documents de travail (deux de l'équipe favorable à la dépense, un qui corrige le biais de sélection) | **Retéléchargés à l'origine**, empreintes comparées | **Identiques** |
| S13 | FMI, avril 2023 : les consolidations ne réduisent pas le ratio de dette en moyenne | Phrase relue dans l'extrait | **Confirmé** : « fiscal consolidations do not reduce debt ratios, on average » |
| S13 | Plans par l'impôt : plus de deux points de PIB de perte, pendant trois à quatre ans | Phrase relue dans la synthèse de 2019 | **Confirmé** |
| S13 | Seuil de multiplicateur au-dessus duquel une consolidation fait monter le ratio de dette la première année : 0,595 | Recalcul : 1 / (1,157 + 0,522) | **0,596** : conforme |
| S14 | Tableau de l'Insee (*France, portrait social*, édition 2024) sur l'effet de la taxe d'habitation par dixième de niveau de vie | Fichier **retéléchargé à l'origine**, empreinte comparée ; figure 5 relue dans le fichier | **Identique** ; les valeurs de 2023 de l'agent (0 jusqu'au sixième dixième, puis 20, 70, 170 et 300 euros) sont celles du fichier |
| S14 | Parts du gain cumulé de 2018 à 2023 : 21,2 % au dixième le plus aisé, 36,6 % aux deux derniers dixièmes, 27,3 % à la moitié la plus modeste | Refaites à la main à partir des effets par dixième (870, 1 500 et 1 120 sur un total de 4 100 euros) | **Reproduit** |
| S14 | Contrôle mécanique | 17 titres ; 51 pièces marquées consultées, 5 secondaires, 1 souvenir, 4 recherches infructueuses ; manifeste de 17 pièces avec adresse d'origine | conforme |
