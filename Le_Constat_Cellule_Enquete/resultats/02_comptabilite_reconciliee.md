# Comptabilité réconciliée des administrations publiques, 1974–2025

**Fichier de synthèse assemblé le 21 novembre 2026 à 09 h 26 par l'orchestrateur.** Le texte ci-dessous est l'annexe du dossier A01 (`agents\A01_annexe_comptabilite_reconciliee.md`), reprise sans réécriture. Statut : dossier passé en recette avec réserves (`journal\recette_A01.md`). Contrôles ultérieurs : chiffres centraux refaits par A18 (déficit de 2025, écarts avec la zone euro, décomposition de la dette : confirmés) ; comparaison avec l'équipe Codex (C01) : aucun écart de fait, décomposition de la dette identique à fenêtres d'années égales. Réserve de l'arbitrage (`corrections_demandees.md`) : la part structurelle du déficit de 2025, « plus de 92 % », vaut pour les estimations officielles lues ; une estimation alternative donne environ 84 %. Anomalie connue de la source : de 1959 à 1977, les soldes de l'État et des organismes divers d'administration centrale ne redonnent pas celui de l'administration centrale.

Annexe du dossier `A01.md`. Toutes les tables citées sont dans `resultats\donnees\A01\` et sont produites par les scripts `resultats\scripts\A01\01` à `07` (relançables, `python -I`). Convention : solde = B9 (capacité + / besoin − de financement), Md€ courants, % du PIB nominal Insee base 2020 (PIB 2025 = 2 991,056 Md€).

## A. Table des définitions (travail 1)

| Notion | Définition opérationnelle | Source normative / producteur | Valeur 2025 | Notion voisine et écart 2025 | Pièce [C] |
|---|---|---|---|---|---|
| Solde public au sens de Maastricht | B9 « capacité/besoin de financement » de S13 (État S13111, ODAC S13112, APUL S1313, ASSO S1314), en droits constatés, consolidé ; notifié à la Commission (PDE) deux fois par an. Depuis octobre 2014, identique à B9 (avant : flux d'intérêts de swaps inclus). | SEC 2010 ; règlement (CE) 479/2009 [M, texte non consulté] ; Insee t_3106 note (*) [C] ; Eurostat | −151,6 Md€ ; −5,07 % | solde budgétaire de l'État : −124,7 Md€ (−4,2 %) | Insee t_3106, t_3107 (28/08/2026) ; Eurostat edpt1 (21/10/2026) |
| Solde budgétaire de l'État (résultat d'exécution des lois de finances) | Encaissements − décaissements du budget général et des comptes spéciaux (comptabilité budgétaire, caisse), hors opérations avec le FMI. | LOLF 2001 ; loi relative aux résultats de la gestion (ex-loi de règlement) | −124,7 Md€ (budget général −122,5 ; comptes spéciaux −2,3) | déficit de l'État en CN −128,1 : écart −3,4 = opérations financières −0,5 + droits constatés −1,9 + opérations non budgétaires −0,9 | t_3107 |
| Comptabilité nationale / budgétaire / générale | CN : droits constatés, périmètre S13 défini par le SEC (critère : une entité dont les ventes couvrent moins de 50 % des coûts est classée en APU — appliqué à SNCF Réseau, note Insee mars 2024 p. 5 [C]) ; budgétaire : caisse, périmètre juridique de l'État ; générale (État) : droits constatés, bilan patrimonial. | SEC 2010 ; LOLF ; Recueil des normes comptables de l'État | — | voir lignes ci-dessus | t_3107 |
| SEC 2010 et base 2020 | Base = année de référence des prix et ensemble des conventions et sources ; la base 2020 (publiée le 31/05/2024) a changé le périmètre S13 (SNCF Réseau sur toute la chronique, ERAFP sortie, Action Logement Services), avancé d'un an l'enregistrement des crédits d'impôt (MGDD 2023), « rebasé » les années 2019–2020 et **rétropolé** les années antérieures « essentiellement selon des méthodes statistiques ». | Insee, note « Révision des ratios de finances publiques en base 2020 », mars 2024, p. 1–7 | — | solde 2019 : −3,1 % (base 2014) → −2,4 % (base 2020) | A01\sources\insee_revision_ratios_B2020_20240325.pdf |
| Recettes publiques totales | Total des recettes S13 (production, revenus de la propriété, impôts et cotisations, autres transferts) | Insee t_3201 l.58 | 1 562,5 Md€ ; 52,24 % | recettes hors éléments imputés 1 457,8 (48,74 %) | t_3201 |
| Impôts et cotisations sociales (Insee, CN) | D2 + D5 + D91 + D733 (0 en consolidé) + D61 − D995 | t_3201 l.45 | 1 374,1 Md€ ; 45,94 % | Eurostat S13+S212 (avec impôts UE 2,9 Md€) : 46,0 % | t_3201 ; gov_10a_taxag |
| Impôts et cotisations (Eurostat) | D2+D5+D91+D61−D995, S13+S212 (institutions de l'UE) ; variantes : hors D612 et D614 (cotisations imputées et cotisations supplémentaires des ménages) : 44,3 % ; hors D611V, D612, D613V, D614 (en outre hors cotisations volontaires) : 44,2 % ; impôts seuls (D2+D5+D91) : 29,6 % | Eurostat gov_10a_taxag (05/11/2026) | 46,0 % | rang FR : 1er parmi 13 pays du fichier ; marge sur DK 0,1 pt hors cotisations imputées | gov_10a_taxag |
| Prélèvements obligatoires (Insee) | Impôts et cotisations effectivement prélevés, y compris impôts de l'UE, **nets des crédits d'impôt**, hors cotisations imputées et nets des montants non recouvrables. | Insee t_3216, t_3217 l.104–111 | 1 305,1 Md€ ; 43,63 % | passage : (I) 1 383,6 − non recouvrables 6,7 − cotisations imputées 52,4 − crédits d'impôt 19,4 | t_3217 |
| Dépenses publiques (consolidées) | Total des emplois S13, consolidé des transferts entre administrations (D73, D9, D41 entre APU) | t_3201 l.27 | 1 714,1 Md€ ; 57,31 % | somme non consolidée APUC+APUL+ASSO : 1 819,7 Md€ (écart 105,6) ; dépense « hors crédits d'impôt » de l'article liminaire du PLF 2027 : 1 694 Md€, 56,6 % | t_3201 ; PLF 2027 n° 3210, article liminaire |
| Crédits d'impôt restituables | Enregistrés en dépenses (subventions, prestations, transferts) pour leur montant total, avec en contrepartie une recette d'impôt D51 ; depuis la base 2020, au fait générateur. | t_3201 note (**) ; Insee note base 2020 | dépenses 20,2 ; recettes 19,4 Md€ | — | t_3201 l.30, l.61 |
| Cotisations sociales imputées | Contrepartie des droits à pension des agents publics non financés par des cotisations effectives (régime de l'État employeur) : comptées en dépense (D122) et en recette (D612) — double compte. | t_3201 note (***) | 52,4 Md€ | dont État 49,4 | t_3201 l.28, l.59 ; t_3203 |
| Dépenses/recettes « hors éléments imputés » | Retranche cotisations imputées, production pour compte propre et crédits d'impôt. **Avant 1978, asymétrique** (P12 retranchée des recettes, rien en dépenses) : solde « hors éléments imputés » biaisé de −P12 (−0,76 pt en 1974). | Insee série longue | dépenses 53,78 % ; recettes 48,74 % | — | t_3201 l.29, l.60 |
| Solde primaire | B9 + intérêts versés (D41) ; variantes : intérêts hors Sifim, intérêts nets des intérêts reçus | 04_PREUVES §III.3 | −85,9 Md€ ; −2,87 % | hors Sifim −86,9 ; net −89,4 | t_3201 l.12, l.13, l.41 |
| Intérêts bruts / nets | D41 versés (y.c. correction Sifim) 65,7 ; hors Sifim 64,7 ; intérêts reçus 3,5 (hors Sifim 3,0) | t_3201 | 2,20 % | « charge de la dette de l'État » budgétaire : autre concept (non chiffré ici) | t_3201 |
| Solde structurel, conjoncturel, mesures ponctuelles | Solde corrigé de la position cyclique (écart de production × semi-élasticité) et des mesures ponctuelles et temporaires, en % du PIB **potentiel** ; dépend de l'estimation du PIB potentiel propre à chaque institution. | LOLF art. 1er/62 ; règlement UE ; méthode commune UE | voir §G | — | §G |
| Écart de production | (PIB − PIB potentiel)/PIB potentiel | chaque institution | 2025 : Commission −0,6 % ; Gouvernement (PLF 2027) positif (solde conjoncturel +0,1 ; valeur de l'écart non lue) | — | §G |
| Dette brute (Maastricht) | Passifs F2 + F3 + F4 de S13, valeur nominale, consolidée (titres d'une APU détenus par une autre exclus) | Insee, page 8988843 « Pour comprendre » [C] ; Eurostat edpt1 (GD_F2, F3, F4) [C] ; règlement 479/2009 [M] | 3 460,1 Md€ ; 115,7 % | — | Eurostat edpt1 ; t_3101 |
| Dette nette | Dette brute − dépôts, crédits et titres de créance détenus par les APU sur les autres secteurs | Insee t_3103 | 3 242,7 Md€ ; 108,4 % | « autres actifs liquides » (actions cotées, fonds) 316,9 Md€ non déduits ; IP 2106 (mai) donnait 3 245,5 | t_3103 |
| Ajustement stocks-flux | ΔDette − déficit = acquisitions nettes d'actifs + intérêts courus non échus + effets de valorisation (change) + autres | Insee t_3105 | +2,4 Md€ | dont trésorerie −18,8 ; ICNE +15,0 ; change +6,0 ; actions +6,5 ; comptes à payer +4,5 ; écart statistique −1,6 | t_3105 |
| Point de PIB | 1 % du PIB nominal de l'année | — | 29,91 Md€ | — | t_3106 « série de PIB utilisée » |

## B. Table de passage 1974–2025 (travail 2)

Fichier `A01_table_passage_1974_2025.csv` (312 lignes = 52 ans × 6 secteurs). Colonnes : annee ; secteur ; libelle ; depenses_mdeur ; recettes_mdeur ; solde_b9_mdeur ; source_solde ; interets_verses_d41_mdeur ; interets_recus_d41_mdeur ; solde_primaire_mdeur ; solde_primaire_net_interets_recus_mdeur ; dette_maastricht_mdeur ; pib_mdeur ; depenses_pct_pib ; recettes_pct_pib ; solde_pct_pib ; interets_pct_pib ; solde_primaire_pct_pib ; dette_pct_pib_insee ; indisponible.

Avertissements de périmètre pour les utilisateurs (A02, A03, A05, A07) :
1. Les dépenses/recettes des sous-secteurs ne s'additionnent pas à S13 (non consolidées entre sous-secteurs) ; seuls les **soldes** s'additionnent.
2. 1974–1977 : sous-secteurs = solde seulement (APUC, APUL, ASSO) ; les soldes État et ODAC sont **laissés vides** dans le CSV (non additifs en base 2020, « N.D. » dans les bases antérieures ; F-A01-005, K-013).
3. Les intérêts des sous-secteurs incluent les intérêts versés à d'autres APU (0,2 Md€ en 2025, négligeable).
4. La dette par sous-secteur est la contribution de chaque sous-secteur à la dette consolidée (Insee) ; la somme redonne S13.
5. Millésime : août 2026 (= notification d'octobre 2026). Le compte de mai 2026 diffère de 0,9 Md€ sur 2025 (ASSO).
6. Les niveaux de dépenses et de recettes en % du PIB **dépendent de la base** : +1,1 à +1,9 pt entre base 2014 et base 2020 avant 1995 (§F).

## C. Réconciliation sous-secteurs ↔ S13 (travail 3)

`A01_reconciliation_sous_secteurs.csv` : par année 1978–2025, B9 de S13, somme des B9 (niveaux 1 et 2), écart de consolidation et décomposition. Résidu nul toutes années.

| Année | Écart dépenses non consolidées − S13 (Md€) | dont D73 | dont D9 inter-APU | dont D41 inter-APU | Écart État+ODAC − APUC |
|---|---|---|---|---|---|
| 1978 | 15,7 | 14,2 | 1,4 | 0,1 | 9,1 |
| 1985 | 34,2 | 30,0 | 3,9 | 0,2 | 21,8 |
| 1990 | 43,9 | 38,0 | 5,7 | 0,2 | 20,8 |
| 1995 | 52,9 | 45,4 | 7,3 | 0,2 | 23,7 |
| 2000 | 62,4 | 54,1 | 8,2 | 0,1 | 28,9 |
| 2005 | 95,1 | 86,4 | 8,6 | 0,1 | 41,7 |
| 2010 | 126,7 | 113,5 | 12,9 | 0,3 | 57,4 |
| 2015 | 88,6 | 77,9 | 10,6 | 0,1 | 52,6 |
| 2020 | 101,0 | 88,1 | 13,0 | 0,0 | 79,0 |
| 2024 | 106,4 | 90,5 | 15,8 | 0,2 | 72,1 |
| 2025 | 105,6 | 89,4 | 16,0 | 0,2 | 68,9 |

Budget de l'État ↔ État CN ↔ S13 (2025, Md€) : résultat d'exécution des lois de finances −124,7 → (opérations budgétaires traitées en opérations financières −0,5 ; corrections de droits constatés −1,9 ; opérations non budgétaires −0,9) → État CN −128,1 → + ODAC −2,2 → APUC −130,3 → + APUL −15,6 + ASSO −5,8 → S13 −151,6 (Insee t_3107, t_3106).

Passage ASSO : le tableau Insee t_3108 (« Passage du résultat comptable du régime général au déficit des ASSO ») a été téléchargé (A01\sources\insee_t_3108.xlsx, 205 Ko) mais **non exploité** faute de temps (§13 du dossier).

## D. Flux entre administrations : qui finance qui (travail 3)

`A01_flux_d73_par_sous_secteur.csv` (1978–2025, Md€) : D73 versés, reçus, nets ; D733 ; D9 versés, reçus ; D41 versés, reçus — pour État, ODAC, APUC, APUL, ASSO.

Ce que les tableaux identifient : (i) l'APUC verse aux APUL et ASSO plus qu'elle n'en reçoit (D73 nets −47,4 Md€ en 2025 au niveau APUC, −86,6 au niveau de l'État, dont une partie va aux ODAC : +39,2) ; (ii) les APUL reçoivent 44,5 Md€ de D73 nets et 9,5 de D733 ; (iii) les ASSO ne reçoivent que 3,0 Md€ de D73 nets ; (iv) leur financement « public » passe par **299,1 Md€ d'impôts** qui leur sont directement attribués en comptabilité nationale (t_3216 l.13), dont CSG 156,6 et CRDS 9,3 (t_3217 ; montants toutes APU).

Ce qu'ils n'identifient pas : la matrice bilatérale ; la part des impôts affectés aux ASSO qui « compense » des exonérations de cotisations ; les subventions d'équilibre des régimes spéciaux (en partie D73, en partie dans le compte de l'État, qui inclut le CAS Pensions) ; les reprises de dette (CADES : opérations financières, pas de flux B9). À chercher dans : rapport CCSS, annexe PLFSS « relations financières État–sécurité sociale », Cour des comptes (RALFSS) — transmis à A04/A06.

**Anomalie de rétropolation** : D733 constant 1978–2009 (État −16,886 ; APUL +17,070 ; ASSO −0,184 Md€) et D73 reçus par les APUL négatifs 1978–1985 (−9,1 Md€ en 1978). Seule la somme D73 + D733 est interprétable avant 2010.

## E. Conventions d'attribution du déficit (travail 4)

`A01_attribution_conventions.csv` : 5 conventions × 48 années × 3 sous-secteurs ; contrôle : somme = B9 S13 (écart 0,000).

| Convention | Règle | Auteur / usage | Critique principale |
|---|---|---|---|
| C1 publiée | SEC 2010 tel quel | Insee, Eurostat | Dépend des affectations décidées par le législateur (COR 2026, p. 82 : « le gouvernement et le Parlement peuvent ainsi en faire un usage stratégique ») |
| C2 sans D73 | soustraire les transferts courants nets reçus d'autres APU | A01 (exercice) | Non interprétable avant 2010 (anomalie D733) |
| C3 sans D73 ni D733 | idem + transferts de recettes fiscales | A01 | N'agit pas sur les impôts affectés directement (ASSO) |
| C4 C3 + D9 inter-APU → APUL | borne haute pour les APUL | A01 | Hypothèse non vérifiable dans les tableaux |
| C5 C3 + impôts des ASSO → APUC | régimes sociaux financés par leurs seules cotisations | A01 (illustratif) | Traite la CSG comme un impôt « d'État » alors qu'elle est affectée par la loi et partiellement contributive |

Résultats (Md€) : voir dossier §5.4. Années choisies :

| Année | C1 APUC/APUL/ASSO | C3 APUC/APUL/ASSO | C5 APUC/APUL/ASSO |
|---|---|---|---|
| 2000 | −31,8 / +1,1 / +11,4 | +23,8 / −42,0 / −1,1 | +109,2 / −42,0 / −86,5 |
| 2007 | −51,9 / −8,3 / +2,2 | +10,4 / −67,3 / −1,1 | +137,9 / −67,3 / −128,6 |
| 2019 | −67,8 / −2,5 / +12,1 | −1,0 / −63,1 / +5,8 | +231,1 / −63,1 / −226,2 |
| 2024 | −152,5 / −17,8 / +1,1 | −92,7 / −72,4 / −4,0 | +199,7 / −72,4 / −296,4 |
| 2025 | −130,3 / −15,6 / −5,8 | −73,2 / −69,5 / −8,9 | +225,9 / −69,5 / −308,0 |

**Conventions débattues pour les retraites** (pièce : COR, rapport annuel juin 2026, partie 2 chap. 2, p. 82–84, et annexe 2, p. 226–227 [C], PDF téléchargé `cor_RA_2026.pdf`) :
1. **« Convention conforme à la législation »** (COR, CCSS, LFSS) : régime de la fonction publique d'État et régimes spéciaux équilibrés chaque année par la contribution de l'État (CAS Pensions, LOLF art. 20–21 ; LFI 2006 art. 51). Solde 2025 du système : −5,1 Md€ hors produits et charges financiers (−0,2 % du PIB), −1,3 Md€ en les incluant ; projection −2,4 pts de PIB en 2070. Ressources 2025 : 416,6 Md€ hors produits financiers (13,9 % du PIB). Dépenses 2025 : 422 Md€, 14,1 % du PIB, 24,3 % des dépenses publiques.
2. **Convention EEC** (« effort de l'État constant », COR annexe 2) : contribution de l'État aux régimes de fonctionnaires et spéciaux figée en % du PIB (moyenne 2021–2025) → soldes « significativement améliorés » en projection ; critique du COR : considère comme acquise pour le futur la part de financement de l'État et dépend de la période de référence.
3. **Convention « taux employeur du privé »** : « d'autres travaux » (non nommés dans le passage lu) proposent de ramener le taux implicite de cotisation employeur de l'État (82,4 % du traitement indiciaire) au taux du privé (16,67 % en 2026), ce qui ferait apparaître un déficit beaucoup plus élevé. Critique du COR : le taux élevé « ne résulte pas d'une générosité plus importante » mais de la démographie du régime (1,29 cotisant par retraité en 2020 contre 2,05 tous régimes, calcul IPP), d'une compensation démographique faible (0,5 Md€ perçus en 2021 contre ~11 Md€ selon un calcul de la Cour des comptes, RALFSS mai 2024), de soultes (France Télécom 5,7 Md€, La Poste 2 Md€) comptées en recettes publiques l'année de leur versement, et d'un champ plus large (invalidité, majorations, catégories actives). [M] piste non vérifiée : la thèse d'un « déficit caché » des retraites de l'ordre de 40 Md€ a été défendue publiquement en 2024–2025 (J.-P. Beaufret, reprise par F. Bayrou en janvier 2025) ; non consultée.
4. **Chiffrage IPP** (Aubert, Pedrono, Tô, Tochev, « Retraites des fonctionnaires d'État : faut-il changer la convention comptable ? », 30/06/2025, cité par le COR [S]) : dépenses liées au déséquilibre démographique et aux dispositifs de solidarité 1,1 % du PIB (25,8 Md€) ; taux employeur d'équilibre hors invalidité et départs anticipés 34,7 % en 2020. Le COR situe sa propre convention « intermédiaire » entre EEC et IPP.
Phrase-clé du COR (p. 227) : « Quelle que soit la convention adoptée, le solde global des finances publiques n'en est pas affecté ».

## F. Ruptures, bases et révisions (travail 5)

`A01_revisions_millesimes.csv`, `A01_revisions_sup_0_2pt.csv`, `A01_revisions_dette.csv` (script 07). Pièces : copies Wayback Machine des fichiers Insee (captures du 06/11/2020, 11/12/2022, 09/06/2020, 27/04/2022, 24/07/2025), lues comme données ; note Insee mars 2024.

1. **Solde 1959–1982 identique en base 2014 et en base 2020** (Md€ arrondis au dixième en base 2014 ; base 2020 = mêmes valeurs à 0,05 près) : ce n'est pas un test indépendant (reprise de la rétropolation). 1974 : +0,2 (base 2014) et +0,199 (base 2020). 1970 : 0,0 en base 2014 et −0,042 en base 2020.
2. **Base 2005** (t_3106.xls capturé le 16/04/2012, `A01_revisions_base2005_vs_base2020.csv`) : 1974 = +0,447 Md€ (+0,2 %) ; 1970 +0,122 ; 1972 +0,550 ; **1973 +0,096** ; 1975–2010 tous négatifs. Révisions du solde > 0,2 pt (base 2020 − base 2005) : 1995 +0,4 ; 1997 −0,4 ; 1999 +0,3 ; 2005 −0,6 ; 2006 −0,4 ; 2007 −0,3. État/ODAC « N.D. » avant 1978 (de même en base 2014). Bases 2010, 2000, 1995, 1980 : non testées (la capture base 2010 de t_3106 est une redirection 301 non suivie). Un tiers (iFRAP, 30/01/2024, page consultée) écrit à la fois « +8,5 milliards de francs » et « 200 millions € » pour 1974, montants incompatibles entre eux et avec chacune des trois bases ; probablement un autre concept (budget de l'État) — non vérifié [S].
3. **Niveaux de dépenses et de recettes relevés en base 2020 de 1,0 à 1,9 pt de PIB** pour 1960–2005 (1974 : dépenses 39,76 % → 41,34 % ; recettes 39,85 % → 41,44 %), de 0,3 à 1,4 pt ensuite, **sans effet sur le solde** avant 2006. Cause documentée pour 2019–2020 : périmètre (SNCF Réseau, audiovisuel public, Action Logement), production pour compte propre de R&D (+4,4 Md€) ; pour les années antérieures, rétropolation.
4. **Révisions du solde > 0,2 pt (base 2020 − base 2014)** : 2006 −0,3 ; 2007 −0,4 (crédit d'impôt recherche) ; 2010 −0,3 ; 2013 −0,8 (CICE) ; 2014 −0,7 (CICE) ; 2015 −0,3 ; 2017 −0,4 (CICE) ; 2019 **+0,7** (fin du CICE avancée à 2018, sortie de l'ERAFP −2,4 Md€, SNCF Réseau). Explication : Insee, note mars 2024, p. 2–5 [C].
5. **Révisions de la dette > 0,2 pt** : base 2014 (capture 2022) → base 2020 (août 2026) : 2010 +4,6 ; 2011 +3,5 ; 2012 +2,2 ; 2013 +1,2 ; 2014 +1,3 ; 2015 +1,4 ; 2017–2019 +0,7 à +0,8 ; 2020 +0,3. Dans la base 2020 : 2023 −0,3 et 2024 −0,6 entre la capture de juillet 2025 (109,8 ; 113,2) et août 2026 (109,5 ; 112,6) — effet dénominateur (croissance 2023–2024 révisée en hausse, note Insee du 03/06/2026). SNCF Réseau explique ~32 Md€ (≈1,5 pt) en 2015 (note Insee) ; **l'écart de 4,6 pts en 2010 n'est pas entièrement expliqué** par les pièces lues.
6. Erreur dans un fichier archivé : base 2014 (capture 27/04/2022), dépenses 1982 = dépenses 1981 (48,957 % répété) → révision apparente de +3,1 pts en 1982 à ne pas interpréter.
7. Ruptures internes à la base 2020 : État/ODAC non additifs avant 1978 ; D733 figé 1978–2009 ; série « hors éléments imputés » asymétrique avant 1978 ; dette disponible à partir de 1978 seulement ; dette nette à partir de 1995.

## G. Année 2025 : estimations concurrentes (travail 7)

| Source (date) | Solde total | Solde primaire | Solde structurel (% PIB pot.) | Solde conjoncturel | Mesures ponctuelles | Écart de production | Pièce |
|---|---|---|---|---|---|---|---|
| Insee, compte provisoire (27/03/2026) | −5,1 % ; dette 115,6 % | — | — | — | — | — | cité par PLRG 2025 (AN n° 2694, 22/04/2026) [C] |
| Insee IP 2106 (29/05/2026) | −152,5 Md€ (−5,1 %) | −87,8 (intérêts hors Sifim) | — | — | — | — | [C] |
| Insee compte semi-définitif avancé (28/08/2026) = Eurostat (21/10/2026) | −151,6 Md€ (−5,07 %) | −85,9 (D41) ; −2,87 % | — | — | — | — | t_3106 ; edpt1 [C] |
| Gouvernement, PLRG 2025, article liminaire (22/04/2026), cadre potentiel LPFP | −5,1 % | — | **−4,7** | −0,4 | −0,1 | (négatif) | AN n° 2694 [C] ; avis HCFP 2026-2 annexe 1 [C via AN] |
| HCFP, avis 2026-2 (16/04/2026), tableau 3 (potentiel retenu au moment de l'avis) | −5,1 % | — | **−4,9** (ajustement +0,8 ; effort +0,7) | — | — | — | AN, PDF de l'avis [C, lu via assemblee-nationale.fr car hcfp.fr injoignable] |
| Gouvernement, PLF 2027, article liminaire (01/10/2026) | −5,1 % | — | **−5,2** | **+0,1** | 0,0 | positif (≈ +0,2, déduit) | AN n° 3210 [C] |
| HCFP, avis 2026-5 sur PLF 2027 (09–10/2026) | — | — | −5,2 selon Astra (= chiffre de l'article liminaire du PLF 2027, vérifié ci-dessus) | — | — | — | **[X]** hcfp.fr injoignable ; Légifrance JORFTEXT000054939509 : 403 ; pas de capture Wayback |
| Commission européenne, prévisions d'automne (17/11/2026, IP 348) | −5,1 % | CAPB −2,5 | **−4,7** | — | — | **−0,6** (printemps 2026 : −0,6) | IP 348, tableau III.8.1 p. 123 et annexe statistique p. 232, 244, 245 [C] |
| FMI (WEO / Fiscal Monitor oct. 2026) | — | — | — | — | — | — | **[X]** API datamapper : 403/503 (curl), 404 (WebFetch) |
| OCDE | — | — | — | — | — | — | non tenté (§13) |
| Trésor-Éco n° 397 (24/08/2026) | −5,1 % ; prévision LFI −5,4 % ; PLF −5,0 % | — | — | — | — | — | page Trésor [C] (étude complète non lue) |

Plage d'incertitude sur le solde structurel 2025 : **de −4,7 à −5,2 % du PIB potentiel** (0,5 pt ≈ 15 Md€), selon l'estimation du PIB potentiel ; le signe même de la composante conjoncturelle diffère (−0,4 PLRG ; +0,1 PLF 2027 ; Commission −0,4 implicite = total − structurel). L'écart de production « ≈ +0,2 » attribué au PLF 2027 est une déduction A01 (solde conjoncturel +0,1 divisé par une semi-élasticité supposée ≈ 0,57), non une valeur lue. Le solde total (−5,07 %) et le primaire (−2,87 %) sont, eux, des observations.

## H. Contresens statistiques possibles dans la V5 et le dossier Astra (travail 8)

Voir dossier §12.1 (table complète, 25 entrées) ; vérifications chiffrées dans `A01_verifications_astra_v5.csv`.

## I. Chiffres à double millésime (pour A18)

| Grandeur | Valeur 1 (date) | Valeur 2 (date) | Cause |
|---|---|---|---|
| Déficit S13 2025 | 152,5 Md€ (IP 2106, 29/05/2026) | 151,6 Md€ (Insee 28/08/2026 = Eurostat 21/10/2026) | compte semi-définitif avancé, ASSO −6,7 → −5,8 |
| Solde ASSO 2025 | −6,7 Md€ (29/05/2026) | −5,8 Md€ (28/08/2026) | idem |
| Dette 2025 % PIB | 115,6 % (27/03/2026, PLRG) | 115,7 % (29/05 et 21/10/2026) | arrondi / révision mineure |
| Dette 2025 Md€ | 3 460,5 (IP 2106) | 3 460,1 (Eurostat) | idem |
| Dette nette 2025 | 3 245,5 (IP 2106) | 3 242,7 (t_3103, 28/08/2026) | idem |
| Intérêts 2025 | 64,7 « charges d'intérêts », hors Sifim (IP 2106) | 65,7 D41 y.c. Sifim (t_3201, Eurostat) | **concept**, pas millésime |
| Déficit primaire 2025 | 87,8 (Astra : 152,5 − 64,7) | 85,9 (151,6 − 65,7) | millésime + concept |
| Dette 2019 % PIB | 97,9 (IP 2106 fig. 1 ; note Insee mars 2024 avec PIB base 2014) | 98,2 (fichiers d'août 2026) | PIB de référence |
| Dette 2023, 2024 % PIB | 109,8 ; 113,2 (fichier Insee capturé 24/07/2025) | 109,5 ; 112,6 (2026) | révision du PIB 2023–2024 |
| Solde 2019 % PIB | −3,1 (base 2014) | −2,4 (base 2020) | CICE, ERAFP, SNCF Réseau |
| Solde 2013 % PIB | −4,1 (base 2014) | −4,9 (base 2020) | CICE avancé |
| Dépenses 1974 % PIB | 39,8 (base 2014) | 41,3 (base 2020) | rétropolation des niveaux |
| Dépenses FR 2024 % PIB | 57,3 (COFOG, gov_10a_exp) | 57,0 (gov_10a_main, Insee) | jeux Eurostat de calendriers différents |
| Solde structurel 2025 | −4,7 (PLRG avril 2026 ; Commission nov. 2026) ; −4,9 (HCFP avril) | −5,2 (PLF 2027, oct. 2026) | PIB potentiel |
| Solde S13 1974 | +0,447 Md€, +0,2 % (base 2005, 2012) | +0,2 / +0,199 Md€, +0,1 % (bases 2014, 2020) | changement de base |
| Solde S13 1973 | +0,096 Md€ (base 2005) | −0,1 / −0,123 Md€ (bases 2014, 2020) | changement de base (signe) |
| Rang FR, impôts + cotisations (Eurostat) | 2e en 2024 (BE 45,2 ; FR 45,1) | 1re en 2025 (46,0 ; BE 44,7 p) | année |
