# A03 — Annexe : fiches annuelles 2001–2025 et fiche 2026 (exercice en cours)

Généré par `resultats\scripts\A03\generer_fiches_A03.py` à partir de `resultats\donnees\A03\table_annuelle_A03.csv` (chiffres, produits par script) et de `resultats\donnees\A03\fiches_narratif.md` (texte, pièces et étiquettes). **Ne pas éditer cette annexe à la main** : modifier le narratif et relancer.

**Sources des colonnes chiffrées** (toutes [C], extraction 20/11/2026) :
- PIB nominal, croissance en volume, déflateur : Eurostat `nama_10_gdp` (B1GQ, CP_MEUR, CLV_PCH_PRE, PD_PCH_PRE_EUR), mise à jour Eurostat consultée le 20/11/2026 — données transmises par l'Insee (base 2020).
- Inflation : IPCH, taux annuel moyen, Eurostat `prc_hicp_aind` (CP00, RCH_A_AVG). L'IPC Insee n'a pas été extrait.
- Chômage : Insee, taux de chômage BIT France hors Mayotte, idbank 001688527 (CVS, trimestriel), moyenne des quatre trimestres calculée par A03.
- Taux à 10 ans : Eurostat `irt_lt_mcby_a` (critère de convergence), France et Allemagne.
- Dépenses, recettes, solde (% PIB), dette brute et nette (% PIB) : Insee série longue `econ-fin-pub-rec-dep.xlsx` (base commune, `base_insee_dep_rec_pctPIB.csv`). Le solde en % y est **arrondi au dixième** ; la colonne « solde recalculé » = solde Md€ / PIB nominal.
- Solde en Md€ et par sous-secteur : Insee `econ-fin-pub-deficit-secteur.xlsx` (base commune). Dette en Md€ : Insee `econ-fin-pub-dette-adm-pub.xlsx`.
- Charge d'intérêts : **D41 payés, consolidés, y compris correction SIFIM** (Insee tableau 3.201 ; identique à Eurostat `D41PAY` de la base commune). Solde primaire = (solde + D41) / PIB, calculé par A03. Une variante D41G (hors SIFIM) existe dans le même tableau ; elle donne 64,65 Md€ en 2025 contre 65,72 Md€.
- Solde corrigé du cycle (CAB), solde structurel (hors mesures ponctuelles, disponible seulement depuis 2010), écart de production : **Commission européenne, AMECO**, variables UBLGAP, UBLGAPS, UBLGBP, UBLGBPS, AVGDGP, extraction du 20/11/2026 ; millésime AMECO non affiché par l'interface — voir A03.md §5. Ces grandeurs sont des **estimations** révisables (catégorie « cause plausible non isolée »).

**Statut des fiches** : aucune fiche n'est complète au sens strict du gabarit. Il manque partout les références complètes des LFI, LFSS et lois de programmation, le niveau de la prévision initiale avant 2008 et l'explication officielle de l'écart. Le tableau ci-dessous distingue les fiches dont chaque champ porte au moins une pièce [C] et celles où un champ en est dépourvu. Les montants annuels d'IR 2001–2007 viennent d'un tableau du rapport Carrez mis à plat par extraction texte (alignement des colonnes non vérifié).


## Tableau d'état des fiches

| Année | État |
|---|---|
| 2001 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2002 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2003 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2004 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2005 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2006 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2007 | partielle — non documenté sur pièce : prevision; majorité [M] |
| 2008 | partielle — non documenté sur pièce : lois; majorité [M] |
| 2009 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2010 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2011 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2012 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2013 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2014 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2015 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2016 | partielle — non documenté sur pièce : lois; majorité [M] |
| 2017 | partielle — non documenté sur pièce : lois; majorité [M] |
| 2018 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2019 | partielle — non documenté sur pièce : lois; majorité [M] |
| 2020 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2021 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2022 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2023 | chaque champ étayé par au moins une pièce (sauf majorité [M]) ; partielle au sens du gabarit |
| 2024 | chaque champ étayé par au moins une pièce ; partielle au sens du gabarit |
| 2025 | chaque champ étayé par au moins une pièce ; partielle au sens du gabarit |
| 2026 | rédigée (voir fiche) |

## 2001

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1530,07 Md€ ; 1,90 % (déflateur 1,90 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,80 % (Eurostat) ; chômage BIT 7,75 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 52,82 % ; recettes 51,41 % ; solde -1,40 % du PIB (recalculé -1,42 %) ; **-21,69 Md€** ; variation du solde -0,11 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 46,71 Md€ = 3,05 % du PIB ; solde primaire 1,64 % du PIB (variation -0,01 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 59,30 % du PIB ; 907,67 Md€ ; dette nette 50,40 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -32,33 (-2,10 %) ; ODAC -0,44 (0,00 %) ; APUL 0,80 (0,10 %) ; ASSO 10,28 (0,70 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -2,50 % du PIB potentiel (variation -0,05 pt) ; solde structurel indisponible ; primaire corrigé du cycle 0,55 % (variation = effort hors intérêts +0,04 pt) ; écart de production 1,72 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,11 pt = intérêts -0,09 + composante cyclique -0,06 + primaire corrigé du cycle +0,04 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président Jacques Chirac (cohabitation) ; Premier ministre Lionel Jospin (4/6/1997–6/5/2002) ; ministre de l'économie, des finances et de l'industrie Laurent Fabius (27/3/2000–6/5/2002), secrétaire d'État au budget Florence Parly [C : data.gouv.fr, « Historique des Gouvernements de la Ve République », fichier mis à jour le 13/03/2025, extrait `donnees\A03\executif_2001_2025.csv`]. Majorité à l'Assemblée : gauche plurielle issue des législatives de 1997 [M, non vérifié sur pièce]. |
| Lois de finances, LFSS, programmation, mesures | Baisses d'impôt sur le revenu : réforme du barème votée en LFI 2001 (coût 3,2 Md€ en 2001 et 2 Md€ supplémentaires en 2002) et création de la prime pour l'emploi (2,4 Md€) ; les mesures nouvelles cumulées depuis 2000 coûtent au budget de l'État 19,8 à 20,4 Md€ en 2001 (fourchettes basse/haute) [C : rapport AN n° 2689 (Carrez, 30/06/2010), p. 7 et 10, chiffres DB/DG Trésor ; périmètre : recettes fiscales de l'État seulement]. LFSS, programmation : indisponible. |
| Prévision initiale du solde et exécution | Prévision initiale du solde APU en LFI 2001 : indisponible (la série AN n° 1274 commence en 2008 ; le graphique du Sénat r23-685 depuis 2000 n'est pas lisible en texte). |
| Contexte externe | Ralentissement mondial (croissance en volume 1,9 % après 4,1 % en 2000) ; taux à 10 ans 4,94 % ; écart avec le Bund 0,14 pt [C : Eurostat]. Pacte de stabilité en vigueur ; la Commission recommandera une alerte précoce le 19/11/2002 [C : page PDE France, Commission]. |
| Changement de convention / rupture | Série en base 2020, rétropolée par l'Insee « essentiellement selon des méthodes statistiques » pour les années antérieures à 2019 [C : Insee, fiche méthodologique base 2020 n° 7, juillet 2024]. |
| Lecture causale de la variation du solde | Le solde se dégrade de 0,11 pt seulement : la hausse des intérêts et la conjoncture compensent un primaire corrigé du cycle quasi stable (décomposition ci-dessus). Les baisses d'impôts de 2001 sont absorbées cette année-là par des recettes encore dynamiques ; le passage à un déficit primaire n'apparaît qu'en 2002. Preuve : A pour les montants, C pour la décomposition. Incertitude : élasticités et écart de production estimés. |

## 2002

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1578,33 Md€ ; 1,10 % (déflateur 2,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,90 % (Eurostat) ; chômage BIT 7,88 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 53,92 % ; recettes 50,75 % ; solde -3,20 % du PIB (recalculé -3,18 %) ; **-50,12 Md€** ; variation du solde -1,76 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 47,79 Md€ = 3,03 % du PIB ; solde primaire -0,15 % du PIB (variation -1,79 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 61,30 % du PIB ; 966,82 Md€ ; dette nette 52,00 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -56,67 (-3,60 %) ; ODAC 2,21 (0,10 %) ; APUL 1,32 (0,10 %) ; ASSO 3,02 (0,20 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,78 % du PIB potentiel (variation -1,28 pt) ; solde structurel indisponible ; primaire corrigé du cycle -0,75 % (variation = effort hors intérêts -1,30 pt) ; écart de production 0,96 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -1,76 pt = intérêts +0,02 + composante cyclique -0,48 + primaire corrigé du cycle -1,30 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président Jacques Chirac (nouveau mandat à partir du 17/5/2002 selon data.gouv.fr) ; Premiers ministres L. Jospin puis Jean-Pierre Raffarin (7/5/2002) ; ministre de l'économie Francis Mer, ministre délégué au budget Alain Lambert [C : data.gouv.fr]. Majorité UMP issue des législatives de juin 2002 [M]. |
| Lois de finances, LFSS, programmation, mesures | Deuxième étape de la baisse du barème de l'IR (LFI 2001 : 2 Md€ en 2002) ; mesures nouvelles cumulées depuis 2000 : 25,2 à 25,9 Md€ en 2002 sur le budget de l'État [C : AN n° 2689, p. 7, 10]. Rapport Carrez : les trois premières années de la décennie (2000–2002) concentrent 1,8 pt de PIB de baisses d'impôts d'État, autant que 2003–2007 (1,7 pt) [C]. Baisse de 5 % de l'IR votée à l'été 2002 : [M] (non isolée dans la pièce lue). |
| Prévision initiale du solde et exécution | Indisponible (prévision initiale) ; la Commission recommande une alerte précoce le 19/11/2002 [C]. |
| Contexte externe | Croissance 1,1 % ; IPCH 1,9 % ; chômage 7,9 % ; taux 10 ans 4,86 % [C]. |
| Changement de convention / rupture | Voir 2001 (rétropolation base 2020). |
| Lecture causale de la variation du solde | Dégradation de 1,76 pt : −0,48 pt de composante cyclique, −1,30 pt de primaire corrigé du cycle, intérêts neutres (décomposition AMECO). La part discrétionnaire de recettes est documentée (baisses d'IR 2001–2002), la part dépenses ne l'est pas ici. C'est l'année où la France repasse en déficit primaire (−0,15 % du PIB). Preuve : A (montants), C (décomposition) ; part exacte des décisions : non isolée. |

## 2003

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1622,31 Md€ ; 1,00 % (déflateur 1,80 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,20 % (Eurostat) ; chômage BIT 8,53 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 54,35 % ; recettes 50,27 % ; solde -4,10 % du PIB (recalculé -4,09 %) ; **-66,32 Md€** ; variation du solde -0,91 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 46,66 Md€ = 2,88 % du PIB ; solde primaire -1,21 % du PIB (variation -1,06 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 65,40 % du PIB ; 1060,41 Md€ ; dette nette 55,80 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -61,50 (-3,80 %) ; ODAC -0,40 (0,00 %) ; APUL 0,21 (0,00 %) ; ASSO -4,63 (-0,30 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,14 % du PIB potentiel (variation -0,36 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,27 % (variation = effort hors intérêts -0,52 pt) ; écart de production 0,09 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,91 pt = intérêts +0,15 + composante cyclique -0,55 + primaire corrigé du cycle -0,52 (+ résidu +0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président J. Chirac ; PM J.-P. Raffarin ; économie F. Mer, budget A. Lambert [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | LFI 2003 : baisse du barème de l'IR (3,6 Md€ selon le tableau Carrez) ; mesures nouvelles cumulées depuis 2000 : 30,2 à 31,8 Md€ en 2003 [C : AN n° 2689]. Réforme des retraites de 2003 : [M] (non instruite ici, voir A06). |
| Prévision initiale du solde et exécution | Indisponible. Procédure de déficit excessif : rapport de la Commission 2/4/2003, décision du Conseil sur l'existence d'un déficit excessif et recommandation le 3/6/2003, mise en demeure proposée le 21/10/2003, conclusions du Conseil du 25/11/2003, annulées par la Cour de justice le 13/7/2004 [C : Commission, page « closed EDP France »]. |
| Contexte externe | Croissance 1,0 % ; chômage 8,5 % ; taux 10 ans 4,13 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Dégradation de 0,91 pt : composante cyclique −0,55, primaire corrigé du cycle −0,52, intérêts +0,15. Le déficit dépasse 3 % (4,1 %) et déclenche la procédure européenne. Le ratio de dette gagne 4,1 pts, dont 1,7 pt d'ajustement stock-flux (test_dette_decomposition.csv). Preuve : A/C. |

## 2004

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1696,11 Md€ ; 2,90 % (déflateur 1,60 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,30 % (Eurostat) ; chômage BIT 8,88 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 54,00 % ; recettes 50,45 % ; solde -3,60 % du PIB (recalculé -3,56 %) ; **-60,30 Md€** ; variation du solde +0,53 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 47,51 Md€ = 2,80 % du PIB ; solde primaire -0,75 % du PIB (variation +0,46 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 66,90 % du PIB ; 1134,35 Md€ ; dette nette 57,50 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -53,23 (-3,10 %) ; ODAC 7,36 (0,40 %) ; APUL -2,97 (-0,20 %) ; ASSO -11,46 (-0,70 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,19 % du PIB potentiel (variation -0,05 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,39 % (variation = effort hors intérêts -0,12 pt) ; écart de production 1,01 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,53 pt = intérêts +0,08 + composante cyclique +0,58 + primaire corrigé du cycle -0,12 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président J. Chirac ; PM J.-P. Raffarin (gouvernement du 31/3/2004) ; économie Nicolas Sarkozy (31/3/2004), puis Hervé Gaymard (29/11/2004) ; budget Dominique Bussereau puis Jean-François Copé [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | LFI 2004 : baisse du barème de l'IR (1,8 Md€, tableau Carrez) ; mesures nouvelles cumulées depuis 2000 : 32,5 à 36,2 Md€ [C : AN n° 2689]. Le rapport Carrez note la montée des dépenses fiscales IR « à partir de 2004 » [C]. Hausse des recettes fiscales nettes de l'État de 10,8 % en 2004 (269,9 Md€ contre 243,6), dont une partie liée à des transferts de périmètre : indisponible en détail. |
| Prévision initiale du solde et exécution | Indisponible. |
| Contexte externe | Croissance 2,9 % ; taux 10 ans 4,10 % ; arrêt de la CJUE du 13/7/2004 annulant les conclusions du Conseil de novembre 2003 [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,53 pt, presque entièrement cyclique (+0,58) ; primaire corrigé du cycle −0,12. L'embellie vient de la conjoncture, pas d'un effort mesuré. Preuve : C. |

## 2005

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1762,05 Md€ ; 1,90 % (déflateur 2,00 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,90 % (Eurostat) ; chômage BIT 8,88 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 54,26 % ; recettes 50,76 % ; solde -3,50 % du PIB (recalculé -3,51 %) ; **-61,80 Md€** ; variation du solde +0,05 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 47,85 Md€ = 2,72 % du PIB ; solde primaire -0,79 % du PIB (variation -0,04 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 68,20 % du PIB ; 1201,47 Md€ ; dette nette 59,70 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -53,68 (-3,00 %) ; ODAC 4,75 (0,30 %) ; APUL -3,58 (-0,20 %) ; ASSO -9,29 (-0,50 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,12 % du PIB potentiel (variation +0,07 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,40 % (variation = effort hors intérêts -0,01 pt) ; écart de production 0,97 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,05 pt = intérêts +0,08 + composante cyclique -0,02 + primaire corrigé du cycle -0,01 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président J. Chirac ; PM J.-P. Raffarin puis Dominique de Villepin (2/6/2005) ; économie Hervé Gaymard puis Thierry Breton (25/2/2005) ; budget J.-F. Copé [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | Mesures nouvelles cumulées depuis 2000 sur le budget de l'État : 33,9 à 40,0 Md€ [C : AN n° 2689]. Rapport Pébereau « Rompre avec la facilité de la dette publique » (décembre 2005) : cité par le rapport Carrez 2010 comme ayant proposé de stabiliser les ressources pendant le retour à l'équilibre [S : AN n° 2689 cite Pébereau ; rapport lui-même non consulté]. |
| Prévision initiale du solde et exécution | Indisponible. |
| Contexte externe | Croissance 1,9 % ; taux 10 ans 3,41 % (plus bas de la décennie) [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Quasi-stabilité (+0,05 pt) ; tous les termes proches de zéro. Le déficit reste au-dessus de 3 % malgré une croissance proche du potentiel. Preuve : C. |

## 2006

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1846,02 Md€ ; 2,70 % (déflateur 2,00 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,90 % (Eurostat) ; chômage BIT 8,88 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 53,75 % ; recettes 51,09 % ; solde -2,70 % du PIB (recalculé -2,66 %) ; **-49,06 Md€** ; variation du solde +0,85 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 48,06 Md€ = 2,60 % du PIB ; solde primaire -0,05 % du PIB (variation +0,74 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 65,40 % du PIB ; 1207,31 Md€ ; dette nette 58,80 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -53,68 (-2,90 %) ; ODAC 7,60 (0,40 %) ; APUL -4,08 (-0,20 %) ; ASSO 1,10 (0,10 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,79 % du PIB potentiel (variation +0,33 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,19 % (variation = effort hors intérêts +0,21 pt) ; écart de production 1,80 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,85 pt = intérêts +0,12 + composante cyclique +0,52 + primaire corrigé du cycle +0,21 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président J. Chirac ; PM Dominique de Villepin ; économie Thierry Breton ; budget Jean-François Copé [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | Mesures nouvelles cumulées depuis 2000 sur le budget de l'État : 41,6 à 50,5 Md€ en 2006 [C : AN n° 2689]. LFI 2006 : réforme du barème de l'IR (coût 4,4 Md€, imputé à l'année d'effet dans le tableau Carrez) ; réforme de la taxe professionnelle de 2006 (plafonnement à la valeur ajoutée, dégrèvement pour investissements nouveaux) ; selon Carrez les réformes successives de la TP réduisent son produit d'environ 1 pt de PIB entre 2000 et 2009 [C : AN n° 2689, p. 10–11]. |
| Prévision initiale du solde et exécution | Indisponible. |
| Contexte externe | Croissance 2,7 % ; chômage 8,9 % ; taux 10 ans 3,80 % [C]. La Commission recommande le 29/11/2006 l'abrogation de la procédure de déficit excessif [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,85 pt : composante cyclique +0,52, primaire corrigé du cycle +0,21, intérêts +0,12. Le ratio de dette baisse de 2,8 pts, dont 2,3 pts d'ajustement stock-flux (réduction de trésorerie et cessions selon la littérature [M], non vérifié). Preuve : C. |

## 2007

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1937,88 Md€ ; 2,50 % (déflateur 2,40 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,60 % (Eurostat) ; chômage BIT 8,03 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 53,63 % ; recettes 50,64 % ; solde -3,00 % du PIB (recalculé -2,99 %) ; **-57,94 Md€** ; variation du solde -0,33 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 52,10 Md€ = 2,69 % du PIB ; solde primaire -0,30 % du PIB (variation -0,25 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 65,50 % du PIB ; 1268,86 Md€ ; dette nette 58,90 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -45,76 (-2,40 %) ; ODAC -6,14 (-0,30 %) ; APUL -8,28 (-0,40 %) ; ASSO 2,25 (0,10 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,58 % du PIB potentiel (variation -0,79 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,89 % (variation = effort hors intérêts -0,70 pt) ; écart de production 2,52 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,33 pt = intérêts -0,09 + composante cyclique +0,46 + primaire corrigé du cycle -0,70 (+ résidu -0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président J. Chirac puis Nicolas Sarkozy (16/5/2007) ; PM D. de Villepin puis François Fillon (18/5/2007) ; économie Jean-Louis Borloo puis Christine Lagarde (19/6/2007) ; budget et comptes publics Éric Woerth [C : data.gouv.fr]. Majorité UMP reconduite aux législatives de juin 2007 [M]. |
| Lois de finances, LFSS, programmation, mesures | Loi « en faveur du travail, de l'emploi et du pouvoir d'achat » (été 2007) : exonération des heures supplémentaires (coût IR 0,2 Md€ puis 1 Md€ selon le tableau Carrez), crédit d'impôt sur les intérêts d'emprunt (0,3 puis 0,8 Md€) [C : AN n° 2689, p. 10 ; coût complet de la loi, cotisations et droits de succession compris : indisponible]. Mesures nouvelles cumulées depuis 2000 : 53,5 à 65,6 Md€ [C]. |
| Prévision initiale du solde et exécution | Indisponible. Le Conseil abroge le 30/1/2007 la décision de déficit excessif ouverte en 2003 [C : Commission]. |
| Contexte externe | Croissance 2,5 % ; écart de production estimé +2,5 % (AMECO) : l'économie est au-dessus de son potentiel ; taux 10 ans 4,30 % [C : Eurostat, AMECO] ; début des tensions financières à l'été 2007 [M]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Dégradation de 0,33 pt **malgré une conjoncture favorable** : composante cyclique +0,46, mais primaire corrigé du cycle −0,70. Solde 2007 : −3,0 % ; corrigé du cycle (AMECO) −4,6 % du PIB potentiel. **La France n'était pas à l'équilibre structurel avant la crise.** Preuve : A (solde), C (correction du cycle, révisable : en temps réel les estimations étaient différentes, non retrouvées). |

## 2008

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1990,00 Md€ ; 0,40 % (déflateur 2,30 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 3,20 % (Eurostat) ; chômage BIT 7,42 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 54,28 % ; recettes 50,78 % ; solde -3,50 % du PIB (recalculé -3,50 %) ; **-69,69 Md€** ; variation du solde -0,51 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 57,17 Md€ = 2,87 % du PIB ; solde primaire -0,63 % du PIB (variation -0,33 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 69,80 % du PIB ; 1389,40 Md€ ; dette nette 61,40 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -69,42 (-3,50 %) ; ODAC -2,11 (-0,10 %) ; APUL -10,13 (-0,50 %) ; ASSO 11,97 (0,60 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,30 % du PIB potentiel (variation +0,28 pt) ; solde structurel indisponible ; primaire corrigé du cycle -1,42 % (variation = effort hors intérêts +0,47 pt) ; écart de production 1,26 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,51 pt = intérêts -0,18 + composante cyclique -0,79 + primaire corrigé du cycle +0,47 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président N. Sarkozy ; PM F. Fillon ; économie Christine Lagarde (ministre de l'économie, de l'industrie et de l'emploi à partir du 18/3/2008) ; budget É. Woerth [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | Loi de programmation des finances publiques 2009–2012 : [M] (non consultée). Réponse à la crise financière (SFEF, SPPE, garanties) : montants mobilisés de l'ordre de 120 Md€ selon une commission parlementaire, coût net indisponible [S : extrait de recherche citant un rapport de la commission des finances ; pièce non lue en entier]. |
| Prévision initiale du solde et exécution | Écart entre prévision initiale (LFI) et exécution : **−1,1 pt** ; écart avec la dernière prévision révisée : −0,7 pt [C : AN n° 1274, p. 108 ; convention : exécution moins prévision]. La Commission émet le 28/5/2008 une recommandation de politique budgétaire [C]. |
| Contexte externe | Faillite de Lehman Brothers et crise financière [M] ; croissance 0,4 % ; IPCH 3,2 % ; taux 10 ans 4,23 % ; écart avec le Bund 0,25 pt [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Dégradation de 0,51 pt : composante cyclique −0,79, intérêts −0,18, primaire corrigé du cycle +0,47. Le choc est d'abord conjoncturel. Le ratio de dette gagne 4,3 pts dont 2,6 pts d'ajustement stock-flux (opérations financières de soutien et trésorerie : hypothèse non vérifiée). Preuve : C. |

## 2009

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1935,84 Md€ ; -2,80 % (déflateur 0,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,10 % (Eurostat) ; chômage BIT 9,15 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,99 % ; recettes 50,61 % ; solde -7,40 % du PIB (recalculé -7,38 %) ; **-142,83 Md€** ; variation du solde -3,88 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 49,28 Md€ = 2,55 % du PIB ; solde primaire -4,83 % du PIB (variation -4,20 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 84,10 % du PIB ; 1627,18 Md€ ; dette nette 71,50 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -119,01 (-6,10 %) ; ODAC -0,22 (0,00 %) ; APUL -6,46 (-0,30 %) ; ASSO -17,14 (-0,90 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -5,63 % du PIB potentiel (variation -1,33 pt) ; solde structurel indisponible ; primaire corrigé du cycle -3,09 % (variation = effort hors intérêts -1,67 pt) ; écart de production -2,77 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -3,88 pt = intérêts +0,32 + composante cyclique -2,55 + primaire corrigé du cycle -1,67 (+ résidu +0,02 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président N. Sarkozy ; PM F. Fillon ; économie C. Lagarde ; budget É. Woerth [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | **Plan de relance** : coût budgétaire et fiscal total d'environ 34 Md€ sur 2009–2010, dont 17,5 Md€ de mesures fiscales et 3,8 Md€ de remboursement anticipé du FCTVA ; impact sur le solde APU « environ 27 milliards d'euros sur les deux années », soit 1,4 % du PIB ; la Cour relève « quelques cas de pérennisation », dont 1,6 Md€ de crédit d'impôt recherche et environ 460 M€ de crédits de l'Écologie [C : rapport AN n° 2813 (J. Cahuzac, 13e législature) citant la Cour des comptes]. Baisse de la TVA dans la restauration (2009) : coût non établi sur pièce primaire pour 2009 ; la Cour (2026) évalue le taux réduit à 4,3 Md€ en 2026 [S : contre-enquête Astra citant Cour, contribution du 9/11/2026, non consultée]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−4,8 pts** ; écart avec la dernière prévision révisée : +0,7 pt [C : AN n° 1274]. Procédure de déficit excessif : rapport de la Commission 18/2/2009, décision du Conseil et recommandation le 27/4/2009 [C]. |
| Contexte externe | Récession : −2,8 % en volume ; IPCH 0,1 % ; chômage 9,2 % ; écart de production −2,8 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Dégradation de 3,88 pts : **composante cyclique −2,55** (stabilisateurs automatiques), primaire corrigé du cycle −1,67 (plan de relance et autres mesures, mais aussi effets non discrétionnaires des recettes), intérêts +0,32. Les recettes ne baissent que de 0,2 pt de PIB (50,6 %) tandis que les dépenses gagnent 3,7 pts, en grande partie par l'effet dénominateur (PIB nominal −2,7 %). Ratio de dette +14,2 pts : 4,8 pts de déficit primaire, 2,0 pts d'effet de la baisse du PIB nominal, 4,9 pts d'ajustement stock-flux. Preuve : A/C. Part exacte du plan de relance dans 2009 : ~1 pt de PIB selon une estimation de la Cour [S, via extrait de recherche ; non lu]. |

## 2010

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 1996,08 Md€ ; 2,00 % (déflateur 1,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,70 % (Eurostat) ; chômage BIT 9,25 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,71 % ; recettes 50,56 % ; solde -7,20 % du PIB (recalculé -7,15 %) ; **-142,76 Md€** ; variation du solde +0,23 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 50,71 Md€ = 2,54 % du PIB ; solde primaire -4,61 % du PIB (variation +0,22 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 86,30 % du PIB ; 1722,17 Md€ ; dette nette 75,40 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -127,00 (-6,40 %) ; ODAC 12,17 (0,60 %) ; APUL -2,14 (-0,10 %) ; ASSO -25,79 (-1,30 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -5,90 % du PIB potentiel (variation -0,27 pt) ; solde structurel -5,74 % ; primaire corrigé du cycle -3,36 % (variation = effort hors intérêts -0,27 pt) ; écart de production -1,99 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,23 pt = intérêts +0,01 + composante cyclique +0,50 + primaire corrigé du cycle -0,27 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président N. Sarkozy ; PM F. Fillon (gouvernement remanié le 14/11/2010) ; économie C. Lagarde ; budget É. Woerth puis François Baroin (22/3/2010) [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | Fin du plan de relance ; suppression de la taxe professionnelle (au moins 0,2 pt de PIB de perte de ressources à partir de 2010 selon Carrez) [C : AN n° 2689, p. 11]. Réforme des retraites de 2010 (âge de 60 à 62 ans) : [M], voir A06 ; effet causal sur l'emploi des seniors documenté par l'Insee selon Astra [S]. Conférence sur les déficits publics (20/5/2010) [C : rapport Carrez-Thénault, 20/5/2010, lu via web.archive.org]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+1,4 pt** (exécution meilleure) [C : AN n° 1274]. Recommandation du Conseil du 2/12/2009 fixant le délai de correction : non lue en détail. |
| Contexte externe | Croissance 2,0 % ; début de la crise des dettes souveraines de la zone euro [M] ; taux 10 ans 3,12 %, écart avec le Bund 0,38 pt [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,23 pt : composante cyclique +0,50, primaire corrigé du cycle −0,27. Le déficit reste à 7,2 %. Rapport Carrez (30/6/2010) : la France « a accumulé, depuis 2000, les baisses d'impôts sans les gager par des réductions de dépense » ; déficit structurel de 5 % du PIB en 2009 selon la Cour [C, jugement d'un rapporteur et estimation de la Cour citée]. Preuve : C/E. |

## 2011

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2062,14 Md€ ; 2,40 % (déflateur 0,90 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,30 % (Eurostat) ; chômage BIT 9,20 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,01 % ; recettes 51,71 % ; solde -5,30 % du PIB (recalculé -5,30 %) ; **-109,39 Md€** ; variation du solde +1,85 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 56,00 Md€ = 2,72 % du PIB ; solde primaire -2,59 % du PIB (variation +2,02 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 88,70 % du PIB ; 1830,14 Md€ ; dette nette 78,30 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -92,58 (-4,50 %) ; ODAC -0,66 (0,00 %) ; APUL -1,48 (-0,10 %) ; ASSO -14,66 (-0,70 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,83 % du PIB potentiel (variation +1,07 pt) ; solde structurel -4,96 % ; primaire corrigé du cycle -2,12 % (variation = effort hors intérêts +1,24 pt) ; écart de production -0,75 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +1,85 pt = intérêts -0,18 + composante cyclique +0,78 + primaire corrigé du cycle +1,24 (+ résidu +0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président N. Sarkozy ; PM F. Fillon ; économie C. Lagarde puis François Baroin (29/6/2011) ; budget F. Baroin puis Valérie Pécresse (29/6/2011) [C : data.gouv.fr]. Majorité UMP [M]. |
| Lois de finances, LFSS, programmation, mesures | Début de la consolidation ; plans d'ajustement de l'automne 2011 : [M] (non consultés). Taux de prélèvements obligatoires 42,6 % en 2011 selon le Sénat [C : rapport Sénat n° 113 (2016-2017), « Cinq années sans modération fiscale », A. de Montgolfier, 9/11/2016]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,8 pt** [C : AN n° 1274]. |
| Contexte externe | Crise des dettes souveraines ; écart de taux avec le Bund 0,71 pt en moyenne annuelle (3,32 % contre 2,61 %) [C : Eurostat]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 1,85 pt : primaire corrigé du cycle +1,24 (effort), composante cyclique +0,78, intérêts −0,18. Les recettes gagnent 1,2 pt de PIB, les dépenses baissent de 0,7 pt. Preuve : C ; répartition discrétionnaire recettes/dépenses : non établie sur pièce pour 2011. |

## 2012

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2088,29 Md€ ; 0,20 % (déflateur 1,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,20 % (Eurostat) ; chômage BIT 9,78 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,89 % ; recettes 52,72 % ; solde -5,20 % du PIB (recalculé -5,17 %) ; **-107,99 Md€** ; variation du solde +0,13 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 54,94 Md€ = 2,63 % du PIB ; solde primaire -2,54 % du PIB (variation +0,05 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 91,70 % du PIB ; 1915,84 Md€ ; dette nette 82,00 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -85,71 (-4,10 %) ; ODAC -3,03 (-0,10 %) ; APUL -4,70 (-0,20 %) ; ASSO -14,54 (-0,70 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,17 % du PIB potentiel (variation +0,66 pt) ; solde structurel -4,20 % ; primaire corrigé du cycle -1,54 % (variation = effort hors intérêts +0,58 pt) ; écart de production -1,58 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,13 pt = intérêts +0,09 + composante cyclique -0,53 + primaire corrigé du cycle +0,58 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président N. Sarkozy puis François Hollande (15/5/2012) ; PM F. Fillon puis Jean-Marc Ayrault (16/5/2012) ; économie Pierre Moscovici ; budget Jérôme Cahuzac [C : data.gouv.fr]. Majorité PS et alliés issue des législatives de juin 2012 [M]. |
| Lois de finances, LFSS, programmation, mesures | LFR d'août 2012 : hausses d'impôts de « plus de sept milliards d'euros » en 2012 et « environ six milliards » en 2013 ; textes de l'automne 2012 : près de 18 Md€ de mesures nouvelles pour 2013 ; hausses cumulées 2012–2013 : 15,5 Md€ pour les entreprises, près de 30 Md€ pour les ménages (périmètres non additifs) [C : Sénat n° 113 (2016-2017)]. Création du CICE (fin 2012) : [M]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−0,3 pt** [C : AN n° 1274]. |
| Contexte externe | Croissance 0,2 % ; chômage 9,8 % ; taux 10 ans 2,54 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,13 pt malgré une composante cyclique −0,53 : primaire corrigé du cycle +0,58, porté par les hausses de prélèvements (recettes +1,0 pt de PIB, dépenses +0,9 pt). Preuve : A (mesures votées) / C (décomposition). |

## 2013

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2120,35 Md€ ; 0,80 % (déflateur 0,70 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,00 % (Eurostat) ; chômage BIT 10,28 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 58,59 % ; recettes 53,65 % ; solde -4,90 % du PIB (recalculé -4,94 %) ; **-104,71 Md€** ; variation du solde +0,23 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 49,43 Md€ = 2,33 % du PIB ; solde primaire -2,61 % du PIB (variation -0,07 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 94,60 % du PIB ; 2004,96 Md€ ; dette nette 85,01 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -84,41 (-4,00 %) ; ODAC -1,21 (-0,10 %) ; APUL -8,28 (-0,40 %) ; ASSO -10,82 (-0,50 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,79 % du PIB potentiel (variation +0,38 pt) ; solde structurel -3,97 % ; primaire corrigé du cycle -1,46 % (variation = effort hors intérêts +0,08 pt) ; écart de production -1,82 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,23 pt = intérêts +0,30 + composante cyclique -0,15 + primaire corrigé du cycle +0,08 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président F. Hollande ; PM J.-M. Ayrault ; économie P. Moscovici ; budget J. Cahuzac puis Bernard Cazeneuve (19/3/2013) [C : data.gouv.fr]. Majorité PS [M]. |
| Lois de finances, LFSS, programmation, mesures | Mesures nouvelles de prélèvements de près de 18 Md€ pour 2013 (cf. 2012) [C : Sénat n° 113]. Recommandation du Conseil du 21/6/2013 pour mettre fin au déficit excessif [C : Commission]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−1,3 pt** [C : AN n° 1274]. Élasticité des prélèvements de 0,2 en 2013 citée comme précédent par le Sénat [C : Sénat r23-685, synthèse]. |
| Contexte externe | Croissance 0,8 % ; chômage 10,3 % ; taux 10 ans 2,20 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,23 pt : intérêts +0,30 (baisse des taux), composante cyclique −0,15, primaire corrigé du cycle +0,08 seulement **malgré** ~18 Md€ de hausses d'impôts votées : la faible élasticité des recettes (0,2) et la croissance des dépenses (+0,7 pt de PIB) absorbent l'effort. Preuve : C ; c'est l'année qui illustre le mieux l'écart entre effort voté et amélioration observée. |

## 2014

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2153,73 Md€ ; 1,00 % (déflateur 0,60 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,60 % (Eurostat) ; chômage BIT 10,28 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 58,39 % ; recettes 53,82 % ; solde -4,60 % du PIB (recalculé -4,57 %) ; **-98,50 Md€** ; variation du solde +0,37 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 47,32 Md€ = 2,20 % du PIB ; solde primaire -2,38 % du PIB (variation +0,23 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 96,20 % du PIB ; 2071,12 Md€ ; dette nette 87,67 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -83,78 (-3,90 %) ; ODAC 0,09 (0,00 %) ; APUL -5,68 (-0,30 %) ; ASSO -9,13 (-0,40 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,49 % du PIB potentiel (variation +0,30 pt) ; solde structurel -3,50 % ; primaire corrigé du cycle -1,29 % (variation = effort hors intérêts +0,17 pt) ; écart de production -1,72 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,37 pt = intérêts +0,13 + composante cyclique +0,07 + primaire corrigé du cycle +0,17 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président F. Hollande ; PM J.-M. Ayrault puis Manuel Valls (2/4/2014) ; finances et comptes publics Michel Sapin ; économie Arnaud Montebourg puis Emmanuel Macron (26/8/2014) ; budget Christian Eckert [C : data.gouv.fr]. Majorité PS [M]. |
| Lois de finances, LFSS, programmation, mesures | Pacte de responsabilité et de solidarité, montée en charge du CICE : [M] (non instruits sur pièce ici ; transmis à A04). Taux de PO 44,8 % en 2014 [C : Sénat n° 113]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−0,4 pt** [C : AN n° 1274]. Recommandation de la Commission du 5/3/2014 [C]. |
| Contexte externe | Croissance 1,0 % ; IPCH 0,6 % ; taux 10 ans 1,67 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,37 pt : intérêts +0,13, composante cyclique +0,07, primaire corrigé du cycle +0,17. Preuve : C. |

## 2015

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2201,40 Md€ ; 1,10 % (déflateur 1,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,10 % (Eurostat) ; chômage BIT 10,35 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,60 % ; recettes 53,71 % ; solde -3,90 % du PIB (recalculé -3,89 %) ; **-85,68 Md€** ; variation du solde +0,68 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 44,71 Md€ = 2,03 % du PIB ; solde primaire -1,86 % du PIB (variation +0,52 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 97,00 % du PIB ; 2134,87 Md€ ; dette nette 88,62 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -74,77 (-3,40 %) ; ODAC -4,81 (-0,20 %) ; APUL -0,44 (0,00 %) ; ASSO -5,66 (-0,30 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,01 % du PIB potentiel (variation +0,48 pt) ; solde structurel -2,99 % ; primaire corrigé du cycle -0,98 % (variation = effort hors intérêts +0,31 pt) ; écart de production -1,40 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,68 pt = intérêts +0,17 + composante cyclique +0,20 + primaire corrigé du cycle +0,31 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président F. Hollande ; PM M. Valls ; finances et comptes publics M. Sapin ; économie E. Macron ; budget C. Eckert [C : data.gouv.fr]. Majorité PS [M]. |
| Lois de finances, LFSS, programmation, mesures | Effort structurel 2015 : 0,4 pt de PIB (0,5 pt en dépense, −0,1 pt de mesures nouvelles de PO) contre 0,6 pt prévu en programmation [S : rapport Sénat sur le projet de loi de règlement 2015 (l15-759), via extrait de recherche ; page non lue en entier]. Recommandation du Conseil du 10/3/2015 (nouveau délai de correction) [C : Commission]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,5 pt** [C : AN n° 1274]. |
| Contexte externe | Assouplissement quantitatif de la BCE (2015) [M] ; taux 10 ans 0,84 % ; IPCH 0,1 % [C]. |
| Changement de convention / rupture | Voir 2001. |
| Lecture causale de la variation du solde | Amélioration de 0,68 pt : intérêts +0,17, composante cyclique +0,20, primaire corrigé du cycle +0,31. Dans la période 2011–2015, le primaire corrigé du cycle passe de −3,36 (2010) à −0,98 (2015) : **+2,4 pts d'amélioration corrigée du cycle**, pendant que le solde effectif gagne 3,3 pts. Preuve : C. |

## 2016

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2231,82 Md€ ; 0,90 % (déflateur 0,50 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,30 % (Eurostat) ; chômage BIT 10,03 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,38 % ; recettes 53,62 % ; solde -3,80 % du PIB (recalculé -3,76 %) ; **-84,03 Md€** ; variation du solde +0,13 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 42,43 Md€ = 1,90 % du PIB ; solde primaire -1,86 % du PIB (variation +0,00 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 98,20 % du PIB ; 2190,52 Md€ ; dette nette 89,87 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -77,16 (-3,50 %) ; ODAC -4,74 (-0,20 %) ; APUL 2,26 (0,10 %) ; ASSO -4,38 (-0,20 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -2,97 % du PIB potentiel (variation +0,04 pt) ; solde structurel -2,90 % ; primaire corrigé du cycle -1,06 % (variation = effort hors intérêts -0,08 pt) ; écart de production -1,27 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,13 pt = intérêts +0,13 + composante cyclique +0,09 + primaire corrigé du cycle -0,08 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président F. Hollande ; PM M. Valls puis Bernard Cazeneuve (6/12/2016) ; économie E. Macron puis M. Sapin (ministre de l'économie et des finances, 30/8/2016) ; budget C. Eckert [C : data.gouv.fr]. Majorité PS [M]. |
| Lois de finances, LFSS, programmation, mesures | Indisponible sur pièce (transmis à A04 pour les mesures fiscales). |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−0,1 pt** [C : AN n° 1274]. |
| Contexte externe | Taux 10 ans 0,47 % (France), 0,09 % (Allemagne) [C]. |
| Changement de convention / rupture | **SNCF Réseau reclassé en APU à compter de 2016** (décision Insee/Eurostat, notification d'octobre 2018) : +35,8 Md€ de dette en 2016 et +3,2 Md€ de déficit [S : extrait de recherche sur la page Insee 3607979, non lue] ; intégration complète des comptes de SNCF Réseau seulement en base 2020 [C : Insee, fiche base 2020 n° 7]. |
| Lecture causale de la variation du solde | Amélioration de 0,13 pt : intérêts +0,13, composante cyclique +0,09. Preuve : C. |

## 2017

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2291,68 Md€ ; 2,10 % (déflateur 0,60 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,20 % (Eurostat) ; chômage BIT 9,40 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,66 % ; recettes 54,30 % ; solde -3,40 % du PIB (recalculé -3,36 %) ; **-77,06 Md€** ; variation du solde +0,40 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 41,02 Md€ = 1,79 % du PIB ; solde primaire -1,57 % du PIB (variation +0,29 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 98,80 % du PIB ; 2263,29 Md€ ; dette nette 89,46 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -78,24 (-3,40 %) ; ODAC -3,63 (-0,20 %) ; APUL 1,41 (0,10 %) ; ASSO 3,41 (0,10 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,36 % du PIB potentiel (variation -0,39 pt) ; solde structurel -3,16 % ; primaire corrigé du cycle -1,57 % (variation = effort hors intérêts -0,51 pt) ; écart de production -0,01 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,40 pt = intérêts +0,11 + composante cyclique +0,79 + primaire corrigé du cycle -0,51 (+ résidu +0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président F. Hollande puis Emmanuel Macron (14/5/2017) ; PM B. Cazeneuve puis Édouard Philippe (17/5/2017) ; économie Bruno Le Maire ; action et comptes publics Gérald Darmanin [C : data.gouv.fr]. Majorité LREM-MoDem issue des législatives de juin 2017 [M]. |
| Lois de finances, LFSS, programmation, mesures | Début des baisses de prélèvements comptées par la Cour à partir de 2018 (voir 2018). Indisponible pour 2017 même. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,1 pt** [C : AN n° 1274]. |
| Contexte externe | Croissance 2,1 % ; taux 10 ans 0,81 % [C]. |
| Changement de convention / rupture | Voir 2016. |
| Lecture causale de la variation du solde | Amélioration de 0,40 pt alors que le primaire corrigé du cycle se dégrade (−0,51) : la conjoncture (+0,79) et les intérêts (+0,11) font l'amélioration. Preuve : C. |

## 2018

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2355,36 Md€ ; 1,60 % (déflateur 1,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,10 % (Eurostat) ; chômage BIT 9,03 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 56,37 % ; recettes 54,05 % ; solde -2,30 % du PIB (recalculé -2,32 %) ; **-54,62 Md€** ; variation du solde +1,04 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 41,66 Md€ = 1,77 % du PIB ; solde primaire -0,55 % du PIB (variation +1,02 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 98,50 % du PIB ; 2320,74 Md€ ; dette nette 89,42 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -62,81 (-2,70 %) ; ODAC -2,80 (-0,10 %) ; APUL 1,78 (0,10 %) ; ASSO 9,21 (0,40 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -2,78 % du PIB potentiel (variation +0,58 pt) ; solde structurel -2,75 % ; primaire corrigé du cycle -1,01 % (variation = effort hors intérêts +0,56 pt) ; écart de production 0,74 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +1,04 pt = intérêts +0,02 + composante cyclique +0,46 + primaire corrigé du cycle +0,56 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM É. Philippe ; économie B. Le Maire ; action et comptes publics G. Darmanin [C : data.gouv.fr]. Majorité LREM-MoDem [M]. |
| Lois de finances, LFSS, programmation, mesures | Baisses d'impôts et de cotisations 2018–2023 (suppression de la taxe d'habitation sur les résidences principales, baisse de l'IS, CVAE, allègements de cotisations…) : impact estimé à **62 Md€ en 2023, soit 2,2 pts de PIB**, « non compensées par des économies en dépenses » [C : Cour des comptes, *La situation et les perspectives des finances publiques*, juillet 2024, p. 35–36, lu via archive web.archive.org de vie-publique.fr]. Calendrier par année : indisponible dans la pièce lue. Abrogation de la procédure de déficit excessif le 22/6/2018 [C : Commission]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,3 pt** [C : AN n° 1274]. |
| Contexte externe | Croissance 1,6 % ; taux 10 ans 0,78 % [C]. |
| Changement de convention / rupture | **Base 2020 : les dépenses de CICE sont enregistrées au fait générateur ; le CICE « prend fin en 2018 en base 2020 au lieu de 2019 en base 2014 »**, ce qui supprime la double charge de 2019 visible dans les séries anciennes [C : Insee, fiche base 2020 n° 7, p. 1–2]. |
| Lecture causale de la variation du solde | Amélioration de 1,04 pt : primaire corrigé du cycle +0,56, composante cyclique +0,46. Solde −2,3 % (base 2020). Preuve : C. |

## 2019

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2432,21 Md€ ; 2,00 % (déflateur 1,20 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 1,30 % (Eurostat) ; chômage BIT 8,40 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 55,35 % ; recettes 52,95 % ; solde -2,40 % du PIB (recalculé -2,39 %) ; **-58,23 Md€** ; variation du solde -0,07 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 36,87 Md€ = 1,52 % du PIB ; solde primaire -0,88 % du PIB (variation -0,33 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 98,20 % du PIB ; 2387,40 Md€ ; dette nette 88,99 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -65,86 (-2,70 %) ; ODAC -1,91 (-0,10 %) ; APUL -2,54 (-0,10 %) ; ASSO 12,09 (0,50 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -3,52 % du PIB potentiel (variation -0,74 pt) ; solde structurel -2,63 % ; primaire corrigé du cycle -2,00 % (variation = effort hors intérêts -0,99 pt) ; écart de production 1,78 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,07 pt = intérêts +0,25 + composante cyclique +0,67 + primaire corrigé du cycle -0,99 (+ résidu -0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM É. Philippe ; économie B. Le Maire ; action et comptes publics G. Darmanin [C : data.gouv.fr]. Majorité LREM-MoDem [M]. |
| Lois de finances, LFSS, programmation, mesures | Mesures d'urgence économiques et sociales de décembre 2018 et baisses d'IR 2019–2020 : [M], non chiffrées sur pièce ici (incluses dans les 62 Md€ de la Cour). Transformation du CICE en allègement de cotisations au 1/1/2019 [M]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,2 pt** [C : AN n° 1274]. |
| Contexte externe | Taux 10 ans 0,13 % (France), −0,25 % (Allemagne) [C]. |
| Changement de convention / rupture | Base 2020 : solde 2019 révisé de −3,1 % (base 2014) à −2,4 % (+16,5 Md€), dont +20,4 Md€ dus au décalage des crédits d'impôt ; dette 98,1 % au lieu de 97,4 % [C : Insee, fiche base 2020 n° 7, tableaux 1-1 et 1-2]. Les commentaires d'époque (« déficit 2019 à 3 % ») portent sur la base 2014. |
| Lecture causale de la variation du solde | Quasi-stabilité (−0,07 pt) : intérêts +0,25 et conjoncture +0,67 compensés par un primaire corrigé du cycle −0,99, cohérent avec des baisses de prélèvements non compensées (mais la correction AMECO de 2018–2019 peut porter un résidu du traitement du CICE : non vérifié). Avant le Covid, le déficit corrigé du cycle (AMECO) est de −3,5 % du PIB potentiel. Preuve : C. |

## 2020

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2318,28 Md€ ; -7,40 % (déflateur 3,00 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,50 % (Eurostat) ; chômage BIT 8,03 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 61,70 % ; recettes 52,77 % ; solde -8,90 % du PIB (recalculé -8,93 %) ; **-207,08 Md€** ; variation du solde -6,54 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 29,72 Md€ = 1,28 % du PIB ; solde primaire -7,65 % du PIB (variation -6,77 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 114,90 % du PIB ; 2663,85 Md€ ; dette nette 101,61 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -177,00 (-7,60 %) ; ODAC 22,08 (1,00 %) ; APUL -3,86 (-0,20 %) ; ASSO -48,30 (-2,10 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,75 % du PIB potentiel (variation -1,23 pt) ; solde structurel -4,62 % ; primaire corrigé du cycle -3,47 % (variation = effort hors intérêts -1,47 pt) ; écart de production -6,64 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -6,54 pt = intérêts +0,24 + composante cyclique -5,31 + primaire corrigé du cycle -1,47 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM É. Philippe puis Jean Castex (6/7/2020) ; économie, finances et relance B. Le Maire ; comptes publics O. Dussopt (ministre délégué, 6/7/2020) [C : data.gouv.fr]. Majorité LREM-MoDem [M]. |
| Lois de finances, LFSS, programmation, mesures | **Dépenses d'urgence et de relance : 72,5 Md€ en 2020**, dont activité partielle 25,3, fonds de solidarité 16,0, santé 14,0, exonérations de cotisations 5,8, relance 2,5 [C : Cour des comptes, juillet 2024, tableau 4 p. 43, données du ministère]. PGE : sinistralité nette des primes −0,4 Md€ en 2020 [C, même tableau]. Clause dérogatoire générale du pacte de stabilité : [M] (l'IGF citée par l'AN mentionne son maintien jusqu'au 31/12/2023) [S : AN n° 1274, p. 109]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **−7,0 pts** ; écart avec la dernière prévision révisée : +2,1 pts [C : AN n° 1274]. |
| Contexte externe | Pandémie ; PIB −7,4 % en volume ; écart de production −6,6 % (AMECO) ; taux 10 ans −0,15 % [C]. |
| Changement de convention / rupture | Base 2020 : solde 2020 révisé de −9,0 % à −8,9 % [C : Insee fiche n° 7]. |
| Lecture causale de la variation du solde | Dégradation de 6,54 pts : **composante cyclique −5,31**, primaire corrigé du cycle −1,47 (mesures d'urgence), intérêts +0,24. Ratio de dette +16,8 pts : 7,7 pts de déficit primaire, 4,8 pts d'effet de la chute du PIB nominal, 3,0 pts d'ajustement stock-flux (trésorerie). Preuve : A (mesures), C (décomposition). |

## 2021

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2508,10 Md€ ; 6,90 % (déflateur 1,20 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,10 % (Eurostat) ; chômage BIT 7,85 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 59,46 % ; recettes 52,88 % ; solde -6,60 % du PIB (recalculé -6,58 %) ; **-165,15 Md€** ; variation du solde +2,35 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 34,80 Md€ = 1,39 % du PIB ; solde primaire -5,20 % du PIB (variation +2,45 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 112,80 % du PIB ; 2828,78 Md€ ; dette nette 100,53 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -144,06 (-5,70 %) ; ODAC -0,49 (0,00 %) ; APUL -0,89 (0,00 %) ; ASSO -19,71 (-0,80 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -5,61 % du PIB potentiel (variation -0,86 pt) ; solde structurel -5,52 % ; primaire corrigé du cycle -4,22 % (variation = effort hors intérêts -0,75 pt) ; écart de production -1,54 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +2,35 pt = intérêts -0,11 + composante cyclique +3,21 + primaire corrigé du cycle -0,75 (+ résidu -0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM J. Castex ; économie, finances et relance B. Le Maire ; comptes publics O. Dussopt [C : data.gouv.fr]. Majorité LREM-MoDem [M]. |
| Lois de finances, LFSS, programmation, mesures | Dépenses d'urgence et de relance : **83,7 Md€** (fonds de solidarité 23,9 ; santé 18,3 ; activité partielle 8,1 ; relance 22,5) [C : Cour des comptes, juillet 2024, tableau 4]. Mesures énergie : premiers coûts à l'automne 2021 ; besoin de financement net de l'État −1,0 Md€ en 2021 (les moindres charges de service public de l'énergie dépassent le coût) [C : Cour des comptes, *Les mesures exceptionnelles de lutte contre la hausse des prix de l'énergie*, mars 2024, tableau 3 p. 86]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+2,0 pts** (−6,5 % exécuté contre −8,5 % prévu) [C : AN n° 1274, p. 107]. Élasticité des PO au PIB : 1,2 [C : Sénat r23-685]. |
| Contexte externe | Rebond : +6,9 % en volume ; taux 10 ans 0,01 % [C]. |
| Changement de convention / rupture | Voir 2019. |
| Lecture causale de la variation du solde | Amélioration de 2,35 pts, **plus que cyclique** : composante cyclique +3,21, primaire corrigé du cycle −0,75 (relance et urgence encore élevées), intérêts −0,11. Ratio de dette −2,1 pts grâce à la croissance nominale (−8,7 pts d'effet croissance). Preuve : C. |

## 2022

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2654,00 Md€ ; 2,70 % (déflateur 3,00 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 5,90 % (Eurostat) ; chômage BIT 7,30 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 58,41 % ; recettes 53,67 % ; solde -4,70 % du PIB (recalculé -4,74 %) ; **-125,90 Md€** ; variation du solde +1,84 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 50,93 Md€ = 1,92 % du PIB ; solde primaire -2,82 % du PIB (variation +2,38 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 111,40 % du PIB ; 2955,64 Md€ ; dette nette 101,08 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -148,12 (-5,60 %) ; ODAC 14,88 (0,60 %) ; APUL -1,15 (0,00 %) ; ASSO 8,50 (0,30 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,62 % du PIB potentiel (variation +0,99 pt) ; solde structurel -4,60 % ; primaire corrigé du cycle -2,70 % (variation = effort hors intérêts +1,52 pt) ; écart de production -0,20 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +1,84 pt = intérêts -0,53 + composante cyclique +0,85 + primaire corrigé du cycle +1,52 (+ résidu +0,00 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron (réélu, 14/5/2022) ; PM J. Castex puis Élisabeth Borne (16/5/2022) ; économie, finances et souveraineté industrielle et numérique B. Le Maire ; comptes publics Gabriel Attal (ministre délégué, 20/5/2022) [C : data.gouv.fr]. Après les législatives de juin 2022, majorité relative [M]. |
| Lois de finances, LFSS, programmation, mesures | Dépenses d'urgence et de relance : 34,9 Md€ [C : Cour, juillet 2024]. Mesures énergie : coût brut des dispositifs 23,8 Md€, besoin de financement net de l'État 14,9 Md€ ; mesures énergie et inflation en dépense, coût net 20,8 Md€ [C : Cour, mars 2024 tableau 3 ; Cour, juillet 2024 p. 41–43]. Contribution sur la rente inframarginale (Crim) : 0,4 Md€ en 2022 contre 12,3 Md€ attendus sur 2022–2023 [C : Cour, juillet 2024, p. 35]. |
| Prévision initiale du solde et exécution | Écart prévision initiale – exécution : **+0,3 pt** [C : AN n° 1274]. Élasticité des PO : 1,5 [C : Sénat r23-685]. |
| Contexte externe | Invasion de l'Ukraine, choc énergétique ; IPCH 5,9 % ; taux 10 ans 1,70 % [C]. |
| Changement de convention / rupture | Voir 2019. |
| Lecture causale de la variation du solde | Amélioration de 1,84 pt : primaire corrigé du cycle +1,52 (retrait des mesures Covid plus fort que la montée des mesures énergie, recettes très dynamiques), composante cyclique +0,85, **intérêts −0,53** (indexation sur l'inflation). Ratio de dette −1,4 pt grâce à l'inflation (effet croissance nominale −6,2 pts). Preuve : C. |

## 2023

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2833,83 Md€ ; 1,60 % (déflateur 5,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 5,70 % (Eurostat) ; chômage BIT 7,33 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 56,75 % ; recettes 51,39 % ; solde -5,40 % du PIB (recalculé -5,36 %) ; **-151,92 Md€** ; variation du solde -0,62 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 53,41 Md€ = 1,88 % du PIB ; solde primaire -3,48 % du PIB (variation -0,66 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 109,50 % du PIB ; 3103,25 Md€ ; dette nette 101,40 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -152,92 (-5,40 %) ; ODAC -0,90 (0,00 %) ; APUL -9,95 (-0,40 %) ; ASSO 11,85 (0,40 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -5,27 % du PIB potentiel (variation -0,65 pt) ; solde structurel -5,20 % ; primaire corrigé du cycle -3,38 % (variation = effort hors intérêts -0,68 pt) ; écart de production -0,15 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,62 pt = intérêts +0,04 + composante cyclique +0,03 + primaire corrigé du cycle -0,68 (+ résidu -0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM É. Borne ; économie B. Le Maire ; comptes publics G. Attal puis Thomas Cazenave (20/7/2023) [C : data.gouv.fr]. Majorité relative [M]. |
| Lois de finances, LFSS, programmation, mesures | Réforme des retraites : loi du 14 avril 2023 de financement rectificative de la sécurité sociale ; la Cour note qu'elle pèse légèrement sur le solde 2023 du fait des mesures d'accompagnement [C : Cour, juillet 2024, p. 42, note 20] ; adoption par 49.3 : [S] (V5), non vérifiée ici. Dépenses d'urgence et de relance : 12,4 Md€ ; mesures énergie : coût brut 37,3 Md€, besoin net 23,1 Md€ (Cour, mars 2024) ; mesures énergie/inflation en dépense 17,0 Md€ (Cour, juillet 2024) [C]. **LPFP 2023–2027 promulguée le 18/12/2023** ; elle prévoyait 4,4 % de déficit en 2024 et 3,7 % en 2025 [C : Sénat r24-153] ; 2,7 % en 2027 [S : V5, non vérifié sur le texte de la loi]. |
| Prévision initiale du solde et exécution | PLF 2023 : −5,0 % ; LPFP, LFG et PLF 2024 : −4,9 % ; exécuté −5,5 % (première publication) puis −5,4 % (série actuelle) ; écarts −0,5 pt (initial) et −0,6 pt (révisé) [C : Sénat r23-685 ; AN n° 1274]. Moins-values de PO : 20,7 Md€ ; effet du passage en base 2020 : 4 Md€ (0,14 pt) [C : AN n° 1274 p. 56 ; Sénat r23-685]. **Note DG Trésor/DB du 7/12/2023** estimant le déficit à 5,2 % (voir épisode 6 dans A03.md). |
| Contexte externe | IPCH 5,7 % ; élasticité des PO 0,4 ; taux 10 ans 2,99 % ; France moins chère que l'Italie de 1,1 à 1,6 pt selon les mois [C : Eurostat]. |
| Changement de convention / rupture | Passage à la base 2020 publié en 2024 [C : Insee fiche n° 7]. |
| Lecture causale de la variation du solde | Dégradation de 0,62 pt : primaire corrigé du cycle −0,68, autres termes proches de zéro. Selon le Sénat et l'AN, l'écart à la prévision vient surtout de **recettes plus faibles qu'attendu** (élasticité 0,4 après 1,2 et 1,5) ; la Cour attribue la baisse de 1,8 pt du taux de PO surtout à l'évolution spontanée (−1,6 pt), moins aux baisses nouvelles (−0,2 pt). Lectures concurrentes au sein de la commission d'enquête de l'AN : erreur de politique liée aux baisses d'impôts depuis 2017 (président É. Coquerel) ; « défaillance technique » de prévision (rapporteur M. Lefèvre) ; « renoncements politiques » (rapporteur É. Ciotti). Preuve : A/C pour les chiffres, E pour les imputations. |

## 2024

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2935,24 Md€ ; 1,50 % (déflateur 2,00 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 2,30 % (Eurostat) ; chômage BIT 7,38 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 56,98 % ; recettes 51,22 % ; solde -5,80 % du PIB (recalculé -5,76 %) ; **-169,12 Md€** ; variation du solde -0,40 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 60,13 Md€ = 2,05 % du PIB ; solde primaire -3,71 % du PIB (variation -0,23 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 112,60 % du PIB ; 3306,10 Md€ ; dette nette 104,50 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -151,07 (-5,10 %) ; ODAC -1,39 (0,00 %) ; APUL -17,79 (-0,60 %) ; ASSO 1,14 (0,00 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -5,59 % du PIB potentiel (variation -0,32 pt) ; solde structurel -5,54 % ; primaire corrigé du cycle -3,54 % (variation = effort hors intérêts -0,16 pt) ; écart de production -0,28 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde -0,40 pt = intérêts -0,17 + composante cyclique -0,08 + primaire corrigé du cycle -0,16 (+ résidu +0,01 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM É. Borne puis Gabriel Attal (9/1/2024), Michel Barnier (5/9/2024–5/12/2024), François Bayrou (13/12/2024) ; économie B. Le Maire, Antoine Armand (21/9/2024), Éric Lombard (13/12/2024) ; comptes publics T. Cazenave, Laurent Saint-Martin (ministre chargé du budget, 21/9/2024), Amélie de Montchalin (13/12/2024) [C : data.gouv.fr]. Dissolution de l'Assemblée en 2024, mentionnée par le rapporteur Ciotti [C : AN n° 1274, p. 43 ; mois non lu sur pièce] ; pas de majorité absolue [S]. **Censure du gouvernement Barnier le 4/12/2024 : motion adoptée par 331 voix**, scrutin n° 519 [C : assemblee-nationale.fr, WebFetch]. |
| Lois de finances, LFSS, programmation, mesures | Décret d'annulation de 10 Md€ de crédits du 21/2/2024 ; pas de loi de finances rectificative au premier semestre [C : Sénat r23-685 ; r24-153]. Coût brut des mesures énergie 9,1 Md€, besoin net −0,6 Md€ (prévision de mars 2024) [C : Cour, mars 2024]. Décision du Conseil ouvrant une procédure de déficit excessif le 26/7/2024 [C : Commission]. |
| Prévision initiale du solde et exécution | LFI 2024 : −4,4 % ; PSTAB d'avril 2024 : −5,1 % ; LFG 2024 : −6,1 % ; exécuté −5,8 % (première publication et série Insee actuelle) ; écarts −1,4 pt (initial) et +0,3 pt (révisé) [C : AN n° 1274, p. 56 et 108]. Moins-values de PO : 40,1 Md€ ; écart de recettes au PLFG de 41,5 Md€ dont 22,6 Md€ hérités de 2023 ; dépenses des collectivités supérieures de 13,4 Md€ à la LFI [C : AN n° 1274 ; Sénat r24-153]. OFCE : 0,6 pt dû au point de départ 2023, 0,3 pt à la croissance nominale, 0,5 pt aux collectivités, 0,3 pt aux élasticités [S : Sénat r24-153 citant l'OFCE, policy brief n° 137]. |
| Contexte externe | Dégradation de la note par S&P le 31/5/2024 [C : Sénat r23-685] ; écart de taux avec le Bund passant de 0,51 pt (mai) à 0,83 pt (décembre) [C : Eurostat mensuel]. |
| Changement de convention / rupture | Aucune. |
| Lecture causale de la variation du solde | Dégradation de 0,40 pt : intérêts −0,17, primaire corrigé du cycle −0,16, composante cyclique −0,08. Les pièces parlementaires attribuent l'écart à la prévision d'abord aux recettes, puis aux dépenses locales ; la variation du solde d'une année sur l'autre reste modeste comparée à l'écart à la prévision (1,4 pt). Preuve : A/C. |

## 2025

| Champ | Contenu |
|---|---|
| PIB nominal (Md€) ; croissance en volume (%) | 2991,06 Md€ ; 0,80 % (déflateur 1,10 %) — Eurostat nama_10_gdp [C] |
| Inflation (%) ; chômage (%) | IPCH 0,90 % (Eurostat) ; chômage BIT 7,62 % (Insee 001688527, moyenne annuelle) [C] |
| Dépenses, recettes, solde APU | Dépenses 57,31 % ; recettes 52,24 % ; solde -5,10 % du PIB (recalculé -5,07 %) ; **-151,59 Md€** ; variation du solde +0,69 pt — Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026) [C] |
| Charge d'intérêts ; solde primaire | Intérêts D41 65,72 Md€ = 2,20 % du PIB ; solde primaire -2,87 % du PIB (variation +0,84 pt) — Insee 3.201 + calcul A03 [C] |
| Dette de Maastricht | 115,70 % du PIB ; 3460,10 Md€ ; dette nette 108,41 % — Insee (base commune) [C] |
| Solde par sous-secteur (Md€ ; % PIB) | État -128,10 (-4,30 %) ; ODAC -2,15 (-0,10 %) ; APUL -15,55 (-0,50 %) ; ASSO -5,78 (-0,20 %) — Insee [C] |
| Solde structurel et effort structurel | Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle -4,72 % du PIB potentiel (variation +0,87 pt) ; solde structurel -4,72 % ; primaire corrigé du cycle -2,50 % (variation = effort hors intérêts +1,04 pt) ; écart de production -0,59 % [C] |
| Décomposition mécanique de la variation du solde | Variation du solde +0,69 pt = intérêts -0,15 + composante cyclique -0,18 + primaire corrigé du cycle +1,04 (+ résidu -0,02 dû au mélange PIB effectif / potentiel). Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C] |
| Exécutif et majorité | Président E. Macron ; PM F. Bayrou jusqu'au 9/9/2025 (déclaration de politique générale désapprouvée le 8/9/2025 : 573 votants, 194 pour, 364 contre) [C : assemblee-nationale.fr, WebFetch] ; puis Sébastien Lecornu [S : Public Sénat, Légifiscal ; nomination non vérifiée sur pièce primaire]. Économie É. Lombard, comptes publics A. de Montchalin (gouvernement Bayrou) [C : data.gouv.fr, à jour au 13/03/2025] ; composition des gouvernements Lecornu : indisponible. Pas de majorité absolue [S]. |
| Lois de finances, LFSS, programmation, mesures | **LFI 2025 : loi n° 2025-127 du 14 février 2025** (décision n° 2025-874 DC du 13/2/2025, dix articles censurés) [S : extrait de recherche sur conseil-constitutionnel.fr ; décision non lue]. Recommandation du Conseil du 21/1/2025 pour mettre fin au déficit excessif [C : Commission] ; plafond de dépense nette +0,8 % en 2025 [S : Astra]. **LFSS 2026 adoptée le 16/12/2025** avec l'article 105 de décalage de la réforme des retraites [S/C : voir fiche 2026]. |
| Prévision initiale du solde et exécution | Cible LFI 2025 : indisponible sur pièce lue (5,4 % : [M]) ; exécution −5,1 % (151,6 Md€) [C : Insee/Eurostat]. Décomposition gouvernementale (saisine HCFP) : solde structurel −5,2 % du PIB potentiel, effort structurel +0,4 pt, dont +0,8 pt en PO et −0,4 pt en dépense [C : HCFP avis 2026-5, tableau 12]. |
| Contexte externe | Taux 10 ans 3,35 % ; écart avec le Bund 0,82 pt en septembre–octobre ; la France rejoint le taux italien à l'automne 2025 (écart FR−IT 0,00 en octobre, +0,01 en décembre) [C : Eurostat mensuel]. |
| Changement de convention / rupture | Aucune connue. |
| Lecture causale de la variation du solde | Amélioration de 0,69 pt : **primaire corrigé du cycle +1,04**, composante cyclique −0,18, intérêts −0,15. L'effort passe surtout par les recettes (HCFP, d'après la saisine : +0,8 pt de PO) ; titre de l'Insee Première n° 2106 : « Baisse du déficit avec des recettes croissantes et des dépenses en ralentissement » [C : base commune]. Preuve : A/C. |

## 2026 — exercice en cours (aucun chiffre « réalisé »)

### a_Statut

Exercice en cours au 20/11/2026. **Aucun chiffre ci-dessous n'est un résultat « réalisé » de 2026 sauf mention « observé » avec sa date.** Chaque chiffre porte son statut : loi votée, prévision du gouvernement, prévision de la Commission, avis du HCFP, observation infra-annuelle.

### b_Loi_de_finances_initiale_2026

- **LFI 2026** : loi n° 2026-103 du 19 février 2026 de finances pour 2026, publiée au JO du 20 février 2026. Décision du Conseil constitutionnel n° 2026-901 DC du 19 février 2026 (non-conformité partielle, une réserve) [C, conseil-constitutionnel.fr, WebFetch 20/11/2026]. La décision mentionne que le gouvernement a engagé sa responsabilité (art. 49 al. 3) en nouvelle lecture puis en lecture définitive à l'Assemblée, que les requérants invoquaient des annonces de non-recours au 49.3, et que le Conseil juge que « de simples annonces » ne lient pas le Premier ministre (cons. 12) ; le projet avait été déposé le 14 octobre 2025, après le délai organique du 7 octobre (cons. 10) [C]. Le nombre total de 49.3 (trois, dont un sur la première partie le 20 janvier) n'est établi que par la presse spécialisée [S : Légifiscal, Public Sénat, consultés via recherche ; pièce primaire non lue] ; l'adoption définitive le 2 février 2026 après rejet des motions de censure est rapportée par Maire-info [S].
- **Cible de solde public 2026 en LFI : −5,0 % du PIB ; croissance 1,0 %** — chiffres rapportés par le HCFP (avis 2026-5, synthèse) [C, via web.archive.org, capture du 21/10/2026, hcfp.fr étant injoignable].
- **LFSS 2026** : loi n° 2025-1403 du 30 décembre 2025 ; décision n° 2025-899 DC du 30 décembre 2025, saisine de soixante députés (LFI-NFP) du 18 décembre 2025 [C, conseil-constitutionnel.fr]. La décision ne traite pas l'article de suspension des retraites et ne mentionne pas de 49.3 [C]. Absence de 49.3 sur la LFSS : non vérifiée sur pièce primaire (indisponible).
- **Article 105 de la LFSS 2026 (décalage de la réforme des retraites de 2023)** : coût évalué par la commission des affaires sociales du Sénat (rapport n° 144, 2026-2027, tome I, 4 novembre 2026) à environ 0,3 Md€ en 2026 tous régimes et **1,9 Md€ en 2027 tous régimes, dont 1,2 Md€ pour la sécurité sociale**, 0,1 Md€ État, 0,7 Md€ complémentaires ; 3 Md€ en 2027 pour l'ensemble des APU en incluant la moindre activité ; dégradation du solde chaque année jusqu'en 2032 ; la commission propose d'annuler la suspension (gain 0,6 Md€ en 2027) [C, senat.fr, WebFetch 20/11/2026].
- Changement de ministre en cours d'année : l'avis HCFP 2026-5 précise que la présidente du HCFP a été « ministre de l'action et des comptes publics jusqu'au 22 février 2026 » et s'est déportée sur l'année 2026 [C]. Le ministre de l'action et des comptes publics en novembre 2026 est David Amiel (compte rendu AN du 4/11/2026) [C].

### c_Execution_connue_a_date

- **Dette de Maastricht fin T2 2026 (observé, provisoire)** : 3 595,5 Md€, **119,0 % du PIB**, après 117,5 % fin T1 ; +59,6 Md€ au T2 après +75,8 Md€ au T1 ; dette nette 111,4 % [C, Insee Informations rapides n° 239, parue le 29/09/2026, curl]. Prochaine publication (T3) le 18/12/2026.
- **Chômage BIT** : 8,2 % en moyenne des trois premiers trimestres 2026 (Insee idbank 001688527, calcul A03) [C] ; la Commission indique 8,3 % au T2 2026 [C].
- **Taux à 10 ans** (moyennes mensuelles Eurostat `irt_lt_mcby_m`, mise à jour 12/11/2026) : France 4,89 % en octobre 2026 contre 3,53 % en janvier ; écart avec l'Allemagne 1,47 point en octobre 2026 contre 0,72 en janvier 2026 et 0,51 en mai 2024 ; écart avec l'Italie positif (France plus chère) en décembre 2025, janvier, février, août, septembre (0,08) et octobre 2026 (0,21) [C, calcul A03]. Le dépassement de 5 % le 22 octobre (V5) n'est pas vérifiable sur moyenne mensuelle : donnée quotidienne indisponible.
- Exécution du budget de l'État à fin septembre 2026 (situation mensuelle) : **indisponible** (non recherchée faute de temps).
- Déficit trimestriel APU 2026 (comptes trimestriels) : **indisponible** (page Insee T2 2026 consultée, chiffre non extrait).

### d_Previsions_du_gouvernement

- **PLF 2027 / RESF 2027** (publié le 6 octobre 2026, PLF déposé fin septembre 2026) [C, PDF Trésor, curl] : solde public **2026 : −5,4 %** ; **2027 : −5,0 %** ; 2028 : −3,9 % ; 2029 : −2,8 % ; 2030 : −2,4 % ; dette 119,3 % fin 2026, 122,4 % en 2028, 121,9 % en 2029 (RESF p. 98 et p. 134). Croissance 2026 0,5 %, 2027 1,0 % ; IPC 2,1 % et 1,8 % (tableau 1, p. 71). Intérêts APU 79,2 Md€ en 2026 → 91,2 Md€ en 2027 (note 219, p. 95). Charge de la dette de l'État (comptabilité nationale, tableau 18, p. 128) : 51,8 Md€ en 2025, 64,9 en 2026, **74,9 en 2027**, 107,4 en 2030.
- RESF p. 134 : « Cette trajectoire pluriannuelle revêt un caractère conventionnel du fait des échéances électorales de 2027 ; il appartiendra au prochain Gouvernement de définir une nouvelle trajectoire… » [C].
- Décomposition (tableau 12 de l'avis HCFP, d'après la saisine) : solde structurel −5,2 % (2025), −5,1 % (2026), −4,6 % (2027) du PIB potentiel ; effort structurel 0,4 / 0,4 / 0,9 point ; 2027 : effort de 0,9 pt ≈ 28 Md€, dont 17 Md€ en recettes et 11 Md€ en dépenses ; le gouvernement chiffre 43 Md€ de mesures par rapport à une trajectoire « à politique inchangée » (déficit spontané ≈ 6,5 % en 2027) [C].
- **Après l'examen de la première partie à l'Assemblée** (4 novembre 2026) : le ministre David Amiel indique que le déficit budgétaire de l'État passerait à 177,1 Md€ (+20,7 Md€ par rapport au projet) et que le solde APU passerait de 5 % à **5,9 % du PIB** (−16 Md€ de prélèvements, +8 Md€ de transferts aux collectivités et rejet d'économies locales, +2 Md€ de crédits d'impôt). Statut : **estimation ministérielle d'un texte amendé, présentée dans l'amendement n° 1 de seconde délibération de l'article liminaire, amendement rejeté (80 pour, 168 contre)** [C, compte rendu de la 2e séance du 4/11/2026, curl].

### e_Previsions_Commission_et_HCFP

- **Commission européenne, prévisions d'automne 2026** (Institutional Paper 348, novembre 2026 ; PDF créé le 16/11/2026) [C, curl] : solde **2026 −5,5 %**, **2027 −5,4 %**, 2028 −5,7 % (à politique inchangée) ; solde structurel −4,6 / −4,3 / −4,7 % du PIB potentiel ; dette 119,2 / 122,1 / 123,2 % ; croissance 0,4 / 0,6 / 1,4 % ; IPCH 2,6 / 2,9 % ; chômage 8,4 / 9,2 / 9,8 % ; intérêts 2,6 % du PIB en 2026, 3,0 % en 2027, 3,3 % en 2028. Les mesures de dépense du projet de budget retenues valent « environ 0,8 % du PIB » en 2027 ; les mesures de recettes nouvelles et passées ≈ 0,7 % du PIB. La Commission suppose le **rétablissement de la réforme des retraites de 2023** (« assumed reinstatement ») pour 2028. Statut : prévision.
- **HCFP, avis n° 2026-5 du 25 septembre 2026** (publié le 1er octobre) [C via web.archive.org] : prévision de croissance 2027 (1,0 %) « optimiste » ; prévision de solde 2026 à 5,4 % « plausible » ; prévision de dépense « atteignable » si toutes les mesures sont adoptées ; la LPFP 2023-2027 « n'a eu aucun caractère opératoire » ; retour sous 3 % en 2029 : les retards « rendent très peu vraisemblable sa concrétisation, sauf évolutions conjoncturelles très favorables ».
- AMECO (extraction 20/11/2026) affiche −5,1 % (2026) et −5,7 % (2027) : ce millésime **ne correspond pas** à la prévision d'automne publiée ; il n'est pas utilisé pour 2026–2027.

### f_Projet_de_budget_2027_et_votes

- PLF 2027 initial : solde APU −5,0 % (2027) [C, RESF]. Version amendée par l'Assemblée en première partie : −5,9 % selon le ministre [C]. **Vote sur l'ensemble de la première partie, 4 novembre 2026 : 460 votants, 458 exprimés, 0 pour, 458 contre** ; « l'ensemble du projet de loi de finances pour 2027 est considéré comme rejeté » [C, compte rendu officiel]. Suite de la navette (Sénat, ordonnances, loi spéciale) au 20/11/2026 : **indisponible** (non établie sur pièce).
- PLFSS 2027 : rapport Sénat n° 144 (4/11/2026) consulté pour l'article 105 seulement ; votes PLFSS 2027 : indisponible.

### g_Lecture

L'année 2026 est marquée, selon les pièces, par (i) une révision de la croissance (1,0 % en LFI → 0,5 % gouvernement → 0,4 % Commission), (ii) un choc de prix de l'énergie lié au conflit au Moyen-Orient (HCFP, Commission), (iii) une hausse des taux et de l'écart avec le Bund (Eurostat), (iv) une hausse de la charge d'intérêts de 0,4 point de PIB (Commission). Le gouvernement et la Commission attribuent la dégradation 2025 → 2026 (−5,1 → −5,4/−5,5) au ralentissement des recettes et à la charge d'intérêts, plus qu'à des décisions nouvelles ; le HCFP relève en plus un dépassement de dépenses (intérêts, chômage). Niveau de preuve : D (prévisions). Incertitude : forte (budget 2027 non adopté).

