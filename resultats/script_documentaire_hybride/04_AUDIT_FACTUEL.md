# 04 · Audit factuel du script hybride

**22 novembre 2026.** Audit de la version finale de [02_SCRIPT_ANNOTE.md](02_SCRIPT_ANNOTE.md). Il s'est fait en trois passes.

1. **Relecture indépendante.** Un relecteur a lu le premier jet (commit `e4580f2`) sans connaître les conclusions de la rédaction. Il disposait des six rapports d'Astra, de l'audit de la V6 et des données de la cellule. Son rapport complet est dans [annexes/relecture_factuelle_agent.md](annexes/relecture_factuelle_agent.md). Il compte 5 points bloquants, 16 à corriger et 20 mineurs.
2. **Consolidation.** La rédaction a appliqué ces corrections, revérifié la version finale par recherche de chaînes et reconstruit la voix seule et les durées. La concordance entre le script annoté et la voix a été contrôlée par `outils/verifier_concordance.py`.
3. **Contre-relecture.** Le même relecteur a relu le différentiel `e4580f2..2da0d47` et le tableau du §5. Son résultat est au §9 de l'annexe ; les suites données sont au §8 ci-dessous.

Aucune nouvelle enquête économique n'a été faite. Le référentiel est la contre-expertise d'Astra au commit [`938fc95`](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/938fc95fa4c2265319438fa47124d917e8b1ab4a/resultats/audit_independant_hybride). Pour les actes I et II, repris de la V6, c'est l'audit de la V6 au commit [`d398aaf`](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/d398aaf7990619709c51ecef15b14263baca26bd/resultats/audit_independant_v6).

## 1. Verdict

**Conforme, sous les réserves du §7.** Les cinq points bloquants sont corrigés, et la contre-relecture indépendante confirme qu'ils sont levés. Les trois défauts qu'elle a encore trouvés (un insuffisant, deux erreurs introduites par les réécritures) sont corrigés, ainsi que ses mineurs (§8). Les toutes dernières retouches (§8) n'ont pas été relues une troisième fois par le relecteur : elles reprennent mot pour mot ses propres formulations. Il ne reste dans la voix aucune des formulations réfutées par Astra : la jauge 130–165 / 60–70 / 40–50, « au mieux la moitié », « comme les précédentes », les 63 Md€ de dérive, le 0,6 point attribué à une règle, les 0,8–2,7 points d'emploi, les 3,9 Md€ pour la restauration seule, les « deux tiers de coupes », le « pire déficit » de 1993, l'hôtel de New York, et les « dix milliards en dix jours ». La recherche de chaînes sur la voix finale ne trouve aucune de ces formulations.

## 2. Les cinq points bloquants

| # | Problème relevé | Correction appliquée |
|---|---|---|
| B1 | « où en sera son déficit trois ans plus tard » : depuis la publication, le compte donne 31 cibles manquées sur 32, et non 31 sur 31 | « trois budgets plus loin », conforme à la convention d'A08. Le carton précise « trois exercices au-delà de l'année budgétaire de départ » |
| B2 | Les parts « quatre sur dix » étaient rattachées au gel général des pensions et des prestations, alors qu'elles portent sur un gel des seules pensions, étudié dans une autre étude | « Prends un gel des seules pensions, simulé par l'Institut des politiques publiques. D'après nos calculs sur ses résultats… » Le carton nomme le calcul de la cellule (S04) sur le tableau 2.2 de l'IPP |
| B3 | La règle « inflation − 0,4 point » était présentée comme une variante du gel, et comparée à lui comme « prix de la protection » | Elle devient « une autre règle », avec son propre rendement : « Elle rapporterait autour de deux milliards en 2030. » Le carton dit « autre mesure, distincte du gel ». Plus aucune comparaison n'est faite entre les deux |
| B4 | « Les déficits font la dette », une formule qu'Astra avait corrigée dans la V6 | « Les déficits contribuent à augmenter la dette » |
| B5 | « quarante-deux ont été votés alors que… » assimile un classement des sièges à un décompte des votes | « pour quarante-deux de nos cinquante et un budgets, le camp du gouvernement est classé majoritaire, seul ou avec ses alliés » |

## 3. Corrections de base, de période et de causalité (16)

| Passage | Correction |
|---|---|
| Ouverture : la page qui « annonce que ça ne va pas durer » | « que les comptes de la Sécurité sociale vont replonger » |
| Séq. 1 : « Elle garde son élan » | « Par rapport aux dernières années d'avant-crise, elle garde simplement son rythme » |
| Séq. 1 : « les quatre cinquièmes de cette montée », sans bornes | « Depuis 1974… les quatre cinquièmes de cette montée, jusqu'à aujourd'hui, sont faits dès 1985 » (80,4 %) |
| Séq. 2 : parts État et Sécurité sociale étendues à 1975–1980 | « Sur la dernière ligne droite, de 1978 à 1980… » |
| Séq. 4, carton : + 8,3 affiché alors que la voix dit « un peu moins de 11 » | Légende ajoutée : 1980 et 1981 sont des prévisions de novembre 1980 ; l'excédent constaté de 1980 est d'un peu moins de 11 Md F |
| Séq. 8 : la part exceptionnelle de la recette de 2000 manquait | « Et une partie de cette recette y est classée exceptionnelle : elle ne reviendra pas » |
| Séq. 12 : contribution 2025 « présentée comme exceptionnelle », avec le tableau de 1979 en surimpression | Mention et surimpression retirées : la contribution a été prolongée en 2026 (A14) |
| Séq. 14 : « Le bénéfice plein, sept ans plus tard » | « Le gain chiffré, sept ans plus tard » (les 9,7 à 11,8 Md€ sont un point en 2030, pas un plein effet) |
| Séq. 14 : « La réforme passe sans vote » | « sans vote à l'Assemblée » (le Sénat a voté) |
| Séq. 14, carton art. 105 | Le calendrier est décalé par génération, à partir des pensions prenant effet en septembre 2026 ; âge maintenu à 62 ans et 9 mois jusqu'en janvier 2028 |
| Séq. 15 : « Il ne l'a pas créé » | « Il n'a pas créé celui d'hier » (formule validée en V6) |
| Séq. 16 : « hypothèse prudente » | « dans une hypothèse où une partie seulement est appliquée » (la grille 90/75/50 est la décote centrale) |
| Séq. 18 : « Et ça a coûté », qui attribuait chômage et défaite de 1998 au plan | « Ces années sont dures » ; pour l'emploi des jeunes, « crise et plan sont mêlés » ; pour 1998, « sans qu'on sache quelle part revient aux coupes ». Seules les coupes locales sont attribuées au plan, et au conseiller qui les rapporte |
| Séq. 19 : « Ils n'ont pas fait le redressement » | « Ils s'appliquent quand l'essentiel de l'amélioration est déjà fait. Ce n'est donc pas leur application qui a redressé les comptes. » La première phrase borne la seconde à ce qu'établit la chronologie |
| Séq. 20 : « l'économie la plus rapide qui existe » | « une économie rapide » |
| Séq. 22 : « a bondi de 16 à 17 points » | « a gagné entre 16 et 17 points » |

## 4. Mineurs (20)

Bilan des vingt mineurs :

- « Neuf mois trop tard » → « Neuf mois après » (aucune pièce ne permet de juger).
- « n'a jamais suffi » → « ne suffit pas ».
- « effort budgétaire mesuré ».
- « Cinquante et un ans ».
- « 23 milliards d'euros de mesures de recettes ».
- « Juste arrêter la hausse de son poids », parce que la dette nominale continue de croître.
- « dirigé par un gouvernement minoritaire ».
- « soutiennent l'objectif de redressement », formulation de la consigne. La page 416 du discours n'a pas été relue.
- Collectivités locales et coupes attribuées au conseiller de Persson.
- « ont déjà été retirés, ou rattrapés ».
- « Une pension exonérée **peut** rester protégée ; les revenus du capital concentrent davantage l'effort chez les plus aisés ».
- « environ deux milliards dans notre exemple » pour la compensation. Pour les niches (M17, première partie), « en général quelques milliards à chaque fois ».
- « une grande partie de l'effet ».
- « dans les documents qu'elle examine ».
- « dans nos simulations ».
- Carton du besoin : « sans nouvelles mesures, ni celles du projet de budget 2027 ».

- M1 : les deux fichiers de renvoi manquants existent désormais.
- M2 et M5 : conformes, aucun changement nécessaire.
- M4 : sans objet, la phrase ayant été réécrite (« La question du printemps 2000, la France se l'est donc reposée. Par écrit. »).

**Reste ouvert :** M14, qui demandait d'aligner la paraphrase des trois conditions de Persson sur la page 414, reste à faire au montage. La traduction affichée à l'écran fera foi, et la voix devra la suivre mot pour mot une fois la traduction arrêtée.

## 5. Chiffres dits dans les actes III, IV et la conclusion (version finale)

Les chiffres dits dans l'ouverture et les actes I–II sont contrôlés ligne par ligne dans l'annexe, §1. Ils reprennent la V6 auditée, avec les retouches du §3.

| Séq. | Dit | Base, année, périmètre | Source | Statut |
|---|---|---|---|---|
| 12 | 23 milliards de mesures de recettes | Mesures annoncées pour 2025, sans lien un pour un avec la baisse du déficit | A/05 ; A09 | conforme |
| 12 | 46 % ; premier des 27 | Impôts et cotisations sociales nettes, 2025, Eurostat UE-27 | A/05 | conforme |
| 12 | autour de 51 % | Exercice : tout le déficit 2025 refermé par les prélèvements, PIB constant | A/05 (51,1 %) | conforme |
| 13 | au mieux un demi-milliard ; un cinquième | −20 % sur les fonctions support des opérateurs, plafond d'exercice du Sénat | A/03 (0,54 Md€) | conforme |
| 13 | 57 sur 100, en 2024 | Santé et protection sociale dans la dépense publique 2024 | A/05 | conforme |
| 14 | 62 à 64 ans ; une dizaine de milliards en 2030 | Gain de solde des régimes de retraite, calendrier d'origine, 9,7 à 11,8 Md€ | A/03 (Cour, février 2025) | conforme |
| 14 | à neuf voix | Motion de censure du 20 mars 2023, 278 voix sur 287 requises | A/05 | conforme |
| 14 | jusqu'en 2028 | LFSS 2026, art. 105 : âge maintenu à 62 ans et 9 mois jusqu'en janvier 2028 | A06 (OFCE, Sénat) | conforme |
| 15 | 26 ; 16 | Déclaration du ministre en séance, 4 novembre 2026 | A/05 | conforme, attribué |
| 15 | plus de 6 milliards | Coût net prévu pour 2019 (6,4 ; 10,3 bruts à l'écran), chiffrage fait à l'avance | A/05 (Sénat n° 232) | conforme |
| 15 | 42 sur 51 | Classement des groupes, pas des voix | A/05 ; V6 | conforme |
| 16 | 135 à 165 milliards par an | Niveau atteint en 2030, maintenu, taille du PIB 2025, depuis 6,5 % en 2027 sans mesures du projet, stabilité effective du ratio, deux modèles | A/02 §2 (134,6 à 164,9) | conforme |
| 16 | près de 4 ; 2 ; environ 2,5 points | Hausse du ratio de dette 2029→2030, A15, même référence ; K1 entier ; K1 décoté 90/75/50 | A/02 §5 (+3,754 ; +2,007 ; +2,613) | conforme |
| 17 | plus de 10 % ; plus du double | Déficit suédois 1993, comptes harmonisés révisés (10,7 %) ; France 2025 (5,1 %) | A/04 §3 | conforme |
| 17 | 94 % | Déclaration de Persson, août 1995, sur l'objectif | A/04 §2 | conforme, attribué |
| 17 | 8 % ; moitié-moitié | Programme porté à 8 % du PIB en avril 1996 ; 50,8 % (ministère) ou 52,75 % (OCDE) de dépenses | A/04 §1 | conforme |
| 18 | un cinquième ; 7 à 10 % | Dépréciation nominale mi-1992 à fin 1993 (Flodén) ; débouchés extérieurs 1994–97 (6,8 à 10,5 %) | A/04 §3 | conforme. « environ 7 à 10 % » arrondit 6,8 |
| 18 | plus de 10 % jusqu'en 1997 | Chômage harmonisé de l'OCDE, 1993–1997 | A/04 §3 | conforme |
| 18 | près de neuf points | Sociaux-démocrates, 45,3 % → 36,4 % (1994–1998) | A/04 §3 | conforme, sans attribution |
| 20 | 1 300 € ; 2 % ; 26 € | Cas illustratif, inflation supposée | calcul : 1 300 × 2 % | conforme (déclaré illustratif) |
| 20 | quatre milliards et demi en 2030 | Gel général 2027 : 4,52 nets courants (A13) ; 4,7 directs à l'échelle 2025 (A15) | A/03 | conforme. L'arrondi couvre les deux bases, chacune au carton |
| 20 | quatre sur dix ; un sur deux | Gel des seules pensions, ménages classés par niveau de vie, 37–40 % et 47–48 % | A/03 (S04) | conforme |
| 20 | 1 260 € ; deux milliards, « à la taille de l'économie de 2025 » | Règle distincte, inflation − 0,4 point, 2028–2032, 1,945 Md€ direct en 2030 (A15) | A/03 | conforme |
| 21 | quelques milliards par niche | « en général quelques milliards à chaque fois » | A/03 (lignes de 1,2 à 4,6 Md€) | conforme |
| 21 | 10 % ; 30 → près de 33 € | TVA restauration ; repas illustratif, répercussion complète supposée | calcul : 30 / 1,10 × 1,20 = 32,73 | conforme (hypothèse dite) |
| 21 | 56 % ; 2009 | Baisse de 2009, restaurants avec service à table, part allée aux propriétaires | A/03 (IPP n° 32) | conforme, non transposé |
| 21 | 7,5 milliards, année pleine | + 1 point du seul taux normal, base 2025, après achats publics, avant effets | A/03 §1 (Trésor) | conforme |
| 21 | 2 000 € ; 10 € par mois ; « du même ordre, en théorie » | + 0,5 point de CSG sur une assiette de 2 000 € ; 8,95 Md€ théoriques à l'écran | A/03 §1 (DSS) | conforme. Écart toléré entre un chiffrage statique net (7,5) et un point théorique (8,95) |
| 21 | environ deux milliards | Exemple de compensation : 200 € × 10 millions | A/03 §1 | conforme |
| 22 | quatre sur dix ; sept sur dix | 60–64 ans en emploi, 2025, 44,4 % et 67,6 % (Eurostat) | A/03 | conforme |
| 22 | 60 → 62 ans ; 16 à 17 points | Probabilité d'emploi à 60 ans, premières générations touchées par la réforme de 2010 | A/03 (Insee Analyses n° 30) | conforme |
| 23 | quatorze ans | De 2005 à l'enquête de la Cour de 2019 | A/05 | conforme |
| Concl. | trente-huit mesures | Portefeuille central K1 | A/02 §3 | conforme |
| Concl. | 3 % en 2029 | Cible du projet de budget 2027, RESF p. 134 | V6 | conforme |

**Comparaisons orales.** La voix ne rapporte jamais le besoin (135–165) aux rendements des mesures (4,5 ; 7,5 ; 2). Le carton du besoin et le graphique de pente ne sont jamais divisés l'un par l'autre. La conclusion ne fait pas d'addition de rendements. Elle reprend le résultat du graphique : « même les trente-huit mesures… ralentissent dans nos simulations la hausse ». Trois rapprochements restent, signalés :
- Séq. 20 : « quatre milliards et demi » (gel, A13 net courant ou A15 direct à 4,7) puis « deux milliards, à la taille de l'économie de 2025 » (règle distincte, A15). La voix ne les compare pas, mais l'oreille les rapproche. La base du second est dite ; les deux bases du premier sont au carton.
- Séq. 16–17 : « un effort de cette ampleur ». Le programme suédois atteint 8 % du PIB, contre 4,5 à 5,5 points pour le besoin français : la comparaison est d'ordre de grandeur, sans calcul, et la Suède est plutôt au-dessus.
- Séq. 21 : CSG « du même ordre, en théorie », que la TVA. L'écart de nature entre les deux chiffrages est signalé au carton.

Les dates dites (1974, 1980, 2005, 2019…) ne figurent pas dans ce tableau. Elles sont contrôlées dans l'annexe, §1, et dans l'audit de la V6.

## 6. Causalités

Les affirmations causales sont limitées à celles qu'Astra valide :

- Le choc a contribué à la chute de 1975.
- La fin de la cotisation pèse 11 à 15 % de la dégradation de 1981.
- Après 2010, la hausse de l'emploi à 60 ans s'explique par le report de l'âge.
- Dépréciation et débouchés ont soutenu la Suède, sans part chiffrée.

Sont présentés comme des coïncidences de dates, sans flèche causale :

- les baisses d'impôts votées en décembre 2017 et la fin de la procédure en juin 2018 ;
- la suspension de 2025 et la présidentielle.

Sur ce que le film ne sait pas, la voix le dit :

- « Quelle part pour chacun ? Les comptes de l'époque ne permettent pas de le dire » ;
- « impossible de faire la part de chacun » ;
- « sans qu'on sache quelle part revient aux coupes » ;
- « Personne ne sait d'avance combien il en restera ».

La position finale est présentée comme un choix : « C'est une position, pas un calcul » ; « Dans quelles proportions ? Les preuves ne le disent pas ».

## 7. Ce qui n'a pas été vérifié sur pièce dans cet audit

| Point | Risque | Action avant enregistrement |
|---|---|---|
| Page 416 du discours de Persson : l'objectif exact visé par le 94 % | Faible : la voix dit « l'objectif de redressement », formulation validée par la consigne et par A/04 | Relire la page et aligner la traduction affichée |
| Traduction des trois conditions de Persson (p. 414) | Faible | Arrêter la traduction ; la voix la suit |
| Décembre 2018 : « au plus fort de la crise des gilets jaunes » | Très faible : contexte historique notoire, absent du corpus | Ajouter la référence de presse au dossier d'archives |
| Prolongation en 2026 de la contribution de 2025 | Sans effet sur la voix, qui ne la mentionne plus | — |
| Vote du Sénat sur la réforme de 2023 | Sans effet : la voix dit « sans vote à l'Assemblée » | — |
| Pièces d'archive : décret de 1979 (non retrouvé, dit dans la voix) ; une de presse avec « cagnotte » | Déjà signalé dans la V6 | Sourcer la une |
| Chiffres des actes I–II | Recalculés pour la V6 et validés par Astra, non recalculés ici | — |
| Tous les chiffres de 2025–2027 | Dépendent du sort du PLF et du PLFSS 2027 | Voir [03](03_NOTE_CORRECTIONS_ASTRA.md), §4 |

## 8. Contre-relecture de la version corrigée

Le relecteur indépendant a relu le différentiel `e4580f2..2da0d47`. Son bilan :

- 5 bloquants sur 5 levés ;
- 15 des 16 « à corriger » conformes ;
- 17 des 20 mineurs conformes, M14 restant ouvert comme prévu ;
- le tableau du §5 conforme sur les valeurs.

Suites données, toutes appliquées dans la version finale :

| Point | Avant | Après |
|---|---|---|
| Séq. 19, insuffisant | « Ce n'est donc pas leur application qui a redressé les comptes. » | « Ce n'est donc pas leur application qui a fait l'essentiel du redressement. » |
| Séq. 20, erreur nouvelle | « baisser la dotation d'une commune, c'est souvent déplacer la dépense vers […] les communes » | « Et baisser la dotation d'une commune n'économise rien si la commune ne dépense pas moins. » |
| Conclusion, erreur nouvelle | « aucun levier ne suffit seul. Pas sans faire payer toujours les mêmes. » (la première phrase, isolée, contredit Astra et la séq. 12) | « aucun levier ne suffit seul sans faire payer toujours les mêmes. » |
| Séq. 10, mineur | « trois budgets plus loin » | « trois exercices après l'année du budget qu'elle présente » |
| Séq. 9, mineur | — | « Sa dette, pourtant, a continué de monter. » (un excédent primaire ne suffit pas) |
| Séq. 21, mineurs | « en relevant les prix sur les cartes » ; « Sur 2 000 euros » | « sur les prix des cartes, mais aussi sur les marges et les salaires » ; « Sur 2 000 euros soumis à la CSG » |
| Séq. 23, mineur | Le suivi annuel était présenté comme inexistant | « Depuis 2012, un mécanisme oblige déjà à expliquer un écart important. Pas à le combler. » (A08) |
| Conclusion, mineur | « c'est ce que la Suède a de transposable » | « Et la méthode, c'est ce que la Suède a de transposable » |
| Séq. 18, mineur | « Ce qui relève bien du plan » | « Ce que le conseiller de Persson attribue au plan » |
| Séq. 20, mineur | « autour de deux milliards en 2030 » | « …, à la taille de l'économie de 2025 » |
| Séq. 12, mineur | « une seule moitié du budget » | « un seul côté du budget » |
| Séq. 2, mineur | « la Sécurité sociale… Le budget de l'État » | « les administrations de sécurité sociale… L'État » |
| Séq. 22, mineur | « ce levier a une preuve » | « il y a une preuve » ; « pour les premières générations concernées » |
| Cartons | État « un huitième » ; semestres non légendés ; « courbe des recettes » ; pas de « relevé non exhaustif » en conclusion ; « au plus quatre dixièmes » ; légende double en séq. 4 | « environ un huitième » ; légende des trois semestres ; « poids des recettes publiques dans le PIB » ; mention ajoutée ; « environ quatre dixièmes » ; légendes fondues |

Ces retouches allongent la voix de 48 mots : la durée calculée passe de 28:42 à 28:58.

