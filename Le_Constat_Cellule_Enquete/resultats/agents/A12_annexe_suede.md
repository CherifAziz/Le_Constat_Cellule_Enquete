# A12 — Annexe Suède : vérification indépendante des pièces de la contre-enquête Astra (20/11/2026)

Annexe du dossier `A12.md` (épisode E1). Toutes les pièces sont dans `resultats\donnees\A12\sources\` (empreintes dans `MANIFESTE_PIECES.csv`). Étiquettes [C]/[S]/[M]/[X] et niveaux A–F comme dans le dossier.

## 1. Pièces consultées et canal

| Pièce | Canal | Statut |
|---|---|---|
| FMI, *Sweden: Selected Issues*, Staff Country Report 98/124, B. Arnason et A. Thomas, daté du 1er septembre 1998 (métadonnées PDF : 20/11/1998) — `imf_cr98124_sweden_selected_issues.pdf` | WebFetch sur `https://www.imf.org/external/pubs/ft/scr/1998/cr98124.pdf` (curl : 403) ; PDF **scanné sans couche texte** : pages rendues en image (`imf_pages\p007.png` à `p013.png`) et lues visuellement par A12 | [C], niveau A (document officiel daté) |
| OCDE, J. Blöndal, *Budgeting in Sweden*, PUMA/SBO(98)5/REV1, 24–29 juin 1998, appendice I — `oecd_PUMA_SBO_98_5_REV1.pdf` | `one.oecd.org` refuse curl et WebFetch (403) ; lu via la capture Wayback du 24/02/2024 (`https://web.archive.org/web/20240224130141id_/https://one.oecd.org/document/PUMA/SBO(98)5/REV1/en/pdf`) | [C] via archive, niveau A |
| G. Persson, « Overview », *Budget Deficits and Debt: Issues and Options*, symposium de la Fed de Kansas City (Jackson Hole), 1995, pp. 413–417 — `persson_1995_kcfed_JH95.pdf` | WebFetch (`https://www.kansascityfed.org/documents/6818/Persson_JH95.PDF`) ; texte extrait localement (pymupdf) | [C], niveau E (déclaration d'acteur, datée) |
| Gouvernement suédois, *Sweden's Convergence Programme 1998–2001* (décembre 1998) — `swe_convergence_programme_1998_2001.pdf` | WebFetch (`https://regeringen.se/contentassets/bb70ca16dc184a3eaa49bccdb9d2389c/swedens-convergence-programme-1998-2001`) | [C], niveau A |
| Gouvernement suédois, *The Fiscal Policy Framework*, Skr. 2025/26:76 (PDF créé le 05/03/2026) — `swe_skr_2025_26_76.pdf` | curl direct (`https://www.government.se/contentassets/afd79a1ff8954c78b7681f6a8fa6c8e1/the-fiscal-policy-framework-skr.-20252676.pdf`) | [C], niveau A |
| M. Flodén, « A Role Model for the Conduct of Fiscal Policy? Experiences from Sweden », CEPR DP 9095, août 2012 | copie d'A07 (`donnees\A07\sources\floden_2012_cepr_dp9095.txt`), relue directement par A12 | [C], niveau C |
| Devries, Guajardo, Leigh, Pescatori, IMF WP/11/128, juin 2011 — `imf_wp11128_devries_et_al_2011.pdf` | WebFetch sur `https://www.imf.org/external/pubs/ft/wp/2011/wp11128.pdf` ; texte extrait localement | [C], niveau B (jeu de données construit sur pièces d'époque) |
| Pièce citée par Astra pour 1997 : *Updated Swedish Convergence Programme 2007* (`https://www.government.se/contentassets/05df9908195944759e7fde672633c6b9/updated-swedish-convergence-programme-2007/`) | WebFetch : 403 ; aucune capture Wayback | **[X]** — remplacée par le programme de 1998 |

**Erreur de citation chez Astra** : la note 2, le tableau 1 et les §8–9 du rapport du FMI sont au **chapitre I** (« Fiscal Developments 1994–98 », rédigé par B. Arnason), non au chapitre II, qui traite des salaires. Les chiffres cités sont les bons ; le renvoi est faux.

## 2. Pièce 1 — Part du soutien bancaire dans le déficit de 1993

- **FMI 98/124, p. 6, note 2** [C] : le déficit enregistré de 1993 est de 12¼ % du PIB ; « one-off bank support measures added about 3 percentage points of GDP to the deficit that year ». **Confirmé mot pour mot.**
- **Flodén 2012, p. 15** [C] : dépenses de restauration du système bancaire de **2,3 % du PIB en 1993 et 1,5 % en 1994** ; injections de capital d'environ **61 Md SEK en 1992–1993, soit environ 4 % du PIB** (p. 14). Ces chiffres portent sur l'administration centrale (le paragraphe parle d'emprunt net de l'État : 11 % du PIB en 1992, 13 % en 1993).
- **Comptes actuels (SEC 2010)** : solde des APU de 1993 = **−10,7 % du PIB** (AMECO UBLG et OCDE NLGQ, concordants, `A12_contexte_episodes.csv`), non −12¼. La part du soutien bancaire dans ce −10,7 n'est donnée par aucune pièce lue.
- **Verdict** : « environ 3 points sur 12¼ » **tient** pour le compte de l'époque (FMI) ; une seconde pièce donne 2,3 points pour 1993 (Flodén) ; l'ordre de grandeur 2–3 points est établi (niveau A/C). En revanche la soustraction d'Astra (12¼ − 3 = 9¼) mélange deux millésimes si on la compare à un déficit français en SEC 2010 : en comptes actuels, le point de départ suédois est 10,7 % (soit 2,1 fois le déficit français de 2025, 5,07 %), et on ne sait pas combien de soutien bancaire il contient. La V5 (« environ 12 %, plus du double ») reste exacte dans les deux millésimes ; la phrase d'Astra « la comparaison … disparaît » n'est établie que dans le millésime de 1998 et après retrait d'une dépense que les comptes actuels ne ventilent pas.

## 3. Pièce 2 — Composition du programme

Quatre décomptes différents, de quatre objets différents :

| Décompte | Dépenses | Recettes | Objet mesuré | Pièce |
|---|---|---|---|---|
| Persson, août 1995 | « almost two-thirds » | ≈ un tiers | mesures déjà votées (7,5 % du PIB) | Persson 1995, p. 415 [C] |
| FMI 1998, §1 | « in about equal measure » | | programme de l'hiver 1994–95 (7½ % du PIB) + ½ point en 1996 | FMI 98/124, p. 6 [C] |
| FMI 1998, tableau 2, colonne « Consolidation Program » | −7,6 pts de PIB de dépenses (dont transferts aux ménages −4,8 ; consommation et investissement −3,1) | +1,9 (impôts +1,8) | **variation projetée des ratios** 1994–98 au lancement du programme | FMI 98/124, p. 11 [C] |
| FMI 1998, tableau 2, colonne « 1998 Spring Budget Bill » | −8,2 (dont intérêts −1,1, donc hors intérêts −7,1) | +2,8 (impôts +4,1 ; autres −1,3) | **variation observée des ratios** 1994–98 (hors élément ponctuel de 1998) | FMI 98/124, p. 11 [C] |
| OCDE, *Budgeting in Sweden*, appendice I | 66,2 Md SEK (52,7 %) | 59,3 Md SEK (47,3 %) | rendement des mesures du programme élargi (125,5 Md SEK), source citée : *OECD Economic Surveys* | OCDE PUMA/SBO(98)5/REV1, p. 37 [C via archive] |
| Devries et al. 2011 (FMI), 1995–1998 | 4,8 pts de PIB (60 %) | 3,2 (40 %) | profil annuel (3,5 ; 2,0 ; 1,5 ; 1,0) de l'OCDE 1997, auquel est appliqué uniformément le ratio 60/40 de l'*OECD Economic Survey* 1995, p. 31 (« 60 percent on the spending side ») ; **64 %** de dépenses si l'on ajoute 1993–1994 | WP/11/128, pp. 73–74 [C] ; `A12_composition_mesures_devries2011.csv` |

Calculs A12 : 66,2 / 125,5 = 52,7 % (l'arithmétique d'Astra est exacte). L'appendice I compte « Financing the EU contribution » (20,0 Md SEK) dans le programme ; son classement entre recettes et dépenses n'est pas détaillé dans la pièce.

**Verdict** :
- Les chiffres d'Astra (66,2 / 59,3 / 125,5) **sont exacts** et la pièce existe. Astra qualifie correctement la pièce (« programme élargi »). Une autre estimation de l'OCDE existe : 60/40 pour le programme initial (*Economic Survey* 1995, p. 31, citée par Devries et al. 2011, p. 73, qui l'applique à chaque année 1995–1998). La différence 60/40 → 53/47 tient au périmètre (programme initial ou élargi, dont 20 Md SEK de « financement de la contribution à l'UE ») ; aucune pièce lue ne la réconcilie ligne à ligne. La phrase de la V5 (« presque deux tiers des mesures sont des baisses de dépenses, d'après le ministre lui-même ») est **exacte comme citation** (Persson 1995, p. 415) et **cohérente** avec Devries (60–64 %) ; elle est plus haute que l'OCDE (53 %) et que le « about equal » du FMI de 1998.
- Astra a raison sur un point central : **en variation des ratios**, les impôts et cotisations montent de 4,1 points de PIB (tableau 2), plus du double de ce que prévoyait le programme (1,8) ; la croissance d'assiettes « difficiles à prévoir » (bénéfices, plus-values) l'explique selon le FMI (§11, p. 12). Inversement, mesuré par les ratios, le redressement observé porte aux trois quarts sur les dépenses (8,2 sur 11,0), dont une partie est un effet de dénominateur (croissance de 2½ % par an).
- Conclusion : « deux tiers de coupes » est défendable pour les **mesures du programme initial** (Persson ; OCDE 1995 à 60 % — deux estimations de 1995, non indépendantes entre elles), moins pour le programme élargi (53 %), et non pour le **redressement final** (où la contribution des recettes est du même ordre que celle des coupes hors effet de dénominateur). Les deux objets doivent être nommés séparément. Niveau : A pour les tableaux, B pour Devries.

## 4. Pièce 3 — Rôle du change et de la demande extérieure

- **Flodén 2012** [C] : flottement en novembre 1992, dépréciation nominale de 20 % de mi-1992 à fin 1993 ; coûts salariaux unitaires relatifs de l'industrie −30 % en un an ; l'industrie (< 15 % du PIB) fait plus de la moitié de la croissance en 1994 et un tiers en 1995 ; « the initial recovery was generated by the currency depreciation » et absence de contraction budgétaire expansionniste (p. 16) ; « the Swedish consolidation had standard contractionary short-run effects » (pause de 1996–1997, chômage au maximum en 1997) ; résumé : expériences « of limited applicability » pour la crise de la zone euro parce que la dépréciation et la croissance des marchés d'exportation étaient « a key ingredient ».
- **FMI 1998, p. 6, §1** [C] : couronne « more than 30 percent below » son ancien ancrage à l'écu à l'automne 1994 ; écart de taux longs avec le mark « almost 5 percentage points » ; ramené à environ ¼ point à l'été 1998.
- **Données (grille A12)** : marchés d'exportation suédois +7,6 % (1994), +7,8 % (1995), +6,8 % (1996), +10,5 % (1997) (OCDE XMKT) ; croissance du PIB 3,8 % et 4,4 % en 1994–1995 ; taux long réel 7,0 % (1994), 6,3 % (1995) (AMECO ILRV). Taux de change effectif nominal AMECO disponible seulement à partir de 1994 (98,8 en 1994, 110,6 en 1996, base 2020 = 100) : la dépréciation de 1992–1993 n'est pas visible dans cette série ; elle repose sur Flodén et le FMI.
- **Verdict** : le rôle du change et de la demande extérieure **tient** (deux pièces indépendantes, niveau A et C). Ce qui ne tient pas : l'idée d'une monnaie qui aurait supprimé la prime de risque — l'écart avec l'Allemagne a atteint 4 à 5 points en 1994 (FMI ; Flodén ; A07 F-A07-041 : 339 pb en moyenne en 1995).

## 5. Pièce 4 — Calendrier du plafond de dépenses

- **Persson, août 1995, p. 417** [C] : « The government **has proposed** the imposition of a multi-year ceiling on public expenditure » ; le Parlement a déjà voté le principe d'un vote du total puis des enveloppes (« Parliament cannot pass a budget that is weaker than the one presented by the government »).
- **Programme de convergence 1998–2001, pp. 3 et 6** [C] : « the stricter budget process that has been in effect since 1997, which includes a provision for a ceiling on public expenditure » ; « Since the 1997 budget … ceilings » ; « Expenditure was held under the expenditure ceiling by a wide margin in 1997 ».
- **Flodén 2012, p. 18** [C] : plafonds « introduced in 1996 », fixés trois ans à l'avance (« ceilings for 1997–1999 were set in 1996 ») ; « The elimination of the budget deficit was therefore achieved with little help from the fiscal framework » ; objectif d'excédent introduit en 1997, pleinement applicable en 2001.
- **FMI 1998, §7, p. 7 et p. 10** [C] : plus de 8 des 11¾ points d'amélioration du solde ont lieu en 1995–1996, avant la première année de plafond.
- **Périmètre actuel** (Skr. 2025/26:76, lu par A12) : la pièce décrit le cadre actuel ; elle ne date pas l'introduction du plafond (aucune occurrence pertinente d'une année des années 1990 hors références réglementaires).
- **Verdict** : « entré en application en 1997, après le début du redressement » (Astra) **tient**, avec une précision : décidé en 1996 (Flodén), proposé dès 1995 (Persson). La pièce qu'Astra cite pour cette date (programme de 2007) est **[X]** ; deux autres pièces établissent la date. Conséquence : le plafond ne peut pas expliquer la phase 1995–1996 du redressement ; il peut avoir contribué à la conservation des excédents ensuite (Flodén : excédents et croissance n'expliquent qu'un tiers de la baisse de la dette après 1997 — le reste tient à d'autres opérations, non décomposées ici).

## 6. Pièce 5 — Investissement public

- **FMI 1998, tableau 1** [C] : investissement public 3,0 % du PIB (1994) → 2,0 (1996) → 2,4 (1997) → **1,4 (1998)** ; §5 : « more than a halving of the 1994 level » au point bas ; note 1 du tableau : 1998 inclut un élément ponctuel de 0,8 % du PIB lié à l'intégration du patrimoine immobilier du fonds national de pension.
- **Comptes actuels (SEC 2010)** : FBCF des APU 5,27 % (1993), 5,57 (1994), 4,88 (1996), **4,29 (1998)**, 3,92 (2000), point bas (AMECO UIGG0 et OCDE IGAA/PIB, concordants).
- **Lecture A12** : la baisse de 1997 à 1998 dans le tableau du FMI (−1,0 point) est du même ordre que l'élément ponctuel de 0,8 point ; il est **compatible, non établi**, que cet élément soit enregistré en investissement négatif (cession d'actifs non financiers à une société de portefeuille) ; la pièce ne le dit pas. En comptes actuels, la baisse 1994–1998 est de **1,3 point de PIB (−23 %)**, pas une division par deux. Le niveau plus élevé en SEC 2010 peut tenir en partie à la capitalisation de la recherche-développement [M, non vérifié].
- **Verdict** : « l'investissement public passe de 3,0 à 1,4 % du PIB » est **exact dans le tableau de 1998** mais **ne doit pas être montré** sans dire que les comptes actuels donnent 5,6 → 4,3 % ; « le succès a eu ce coût » tient en direction (baisse réelle et documentée), pas en ampleur.

## 7. Autres affirmations de la V5 sur la Suède

| V5 | Pièce | Verdict |
|---|---|---|
| « En 1993, son déficit public atteint environ 12 % de sa richesse. Plus du double du nôtre aujourd'hui » | FMI 12¼ (compte de 1998) ; SEC 2010 : 10,7 | exact dans les deux millésimes ; préciser la part bancaire (2–3 pts) |
| « Cinq ans plus tard, en 1998, ses comptes sont en excédent » | FMI : +1,6 (1998, avec 0,8 pt ponctuel ; en règles SEC de l'époque : +0,8, note 6) ; SEC 2010 : +0,8 | exact |
| « presque deux tiers des mesures sont des baisses de dépenses, d'après le ministre » | Persson 1995 p. 415 ; OCDE 1995 : 60 % (via Devries) | exact comme citation ; programme élargi : OCDE 1998 53 % ; FMI 1998 « about equal » |
| « Ne dites jamais que ça ne fera pas mal » | Persson 1995 p. 414 : « Never say that it won't hurt » | confirmé |
| « 94 % du Parlement » | Persson 1995 p. 416 : « This goal is supported by 94 percent in Parliament » | confirmé (porte sur l'objectif) |
| Trois conditions (équité, paquet unique, transparence) | Persson 1995 p. 414 | confirmé |
| « il n'a jamais eu à corriger une prévision de déficit dans le mauvais sens » | Persson 1995 p. 416 | confirmé (déclaration d'acteur, niveau E) |
| « le Parlement vote d'abord le total des dépenses … ne peut plus sortir un budget plus déséquilibré » | Persson 1995 pp. 416–417 | confirmé ; le plafond pluriannuel n'est alors que **proposé** |
| « le pouvoir passe des élus à ceux qui lui prêtent » | Persson 1995 p. 417 : « power was shifted from the elected representatives to the owners of capital » | confirmé |
| Hôtel « infesté de cafards » ; coopération avec le Parti du centre « écrite » par le gouvernement | absents du texte de 1995 lu ; aucune autre pièce consultée | **non vérifié** [X] |
| « En 1996, le chômage est encore à 8 %, et à plus de 12 % en comptant les programmes » | OCDE UNR : 11,7 % en 1996 (définition harmonisée actuelle) ; aucune pièce lue pour 8 % / 12 % | **non vérifié** ; la définition compte (chômage ouvert d'époque contre série harmonisée) |

## 8. Ce que le cas suédois permet d'inférer pour un pays de la zone euro à dette élevée et croissance faible

- **Permet** : (i) un ajustement primaire corrigé du cycle de 8 points en cinq ans est possible dans une démocratie parlementaire, avec un gouvernement minoritaire, une consolidation présentée d'un bloc et un objectif soutenu par 94 % du Parlement (pièces A et E) ; (ii) une part importante de l'amélioration observée peut venir de recettes non prévues (impôts +4,1 pts contre +1,8 prévus) ; (iii) un ajustement concentré sur les transferts aux ménages s'accompagne d'un chômage qui reste au-dessus de 10 % pendant quatre ans (11,0 % en 1993, 11,9 % en 1997, OCDE).
- **Ne permet pas** : (i) d'attribuer la reprise à la consolidation (Flodén : reprise tirée par la dépréciation de 20 % et les marchés d'exportation à +7–10 % par an) ; (ii) d'attribuer le redressement au plafond de dépenses (en vigueur en 1997, après l'essentiel) ; (iii) de transposer le canal de change à un pays de la zone euro ; (iv) de conclure qu'une monnaie propre protège de la prime de risque (écart de 4–5 points avec l'Allemagne en 1994).
- **Point de départ non comparable** : la Suède partait d'un déficit de 10,7 % (SEC 2010) dont 2–3 points de soutien bancaire ponctuel et une large part cyclique (écart de production −3,8 % en 1994, FMI tableau 1), avec une dette de 66 % ; la France de 2025 part d'un déficit de 5,1 % dont au moins 92 % structurel (A01) et d'une dette de 115,7 %. Un déficit majoritairement cyclique se résorbe en partie avec la reprise ; un déficit structurel, non.
