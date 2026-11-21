# Politiques de redressement : mesures, combinaisons, payeurs

**Table assemblée le 21/11/2026 à 10 h 56 par `scripts\commun\assembler_politiques.py`.** Elle n'ajoute aucun chiffre : elle rapproche les tables d'A13 (dépense), d'A14 (recettes), d'A15 (combinaisons et objectifs) et de S04 (qui paie). **Ce n'est ni une recommandation ni un programme** : la charte interdit à la cellule de prescrire. Statut : dossiers passés en recette avec réserves ; arbitrage dans `corrections_demandees.md`, qui fait foi. Rendements en milliards d'euros de 2025, nets des effets en retour estimés par chaque agent ; les deux portefeuilles n'emploient pas la même méthode de passage du brut au net.

## 1. Ce que les objectifs demandent (A15)

Effort à voter contre la trajectoire sans aucune mesure (déficit de 6,5 % en 2027 avant le budget, 7,3 % en 2030). **Trois grandeurs à ne pas confondre** : cet effort ; l'écart à un instant (62 Md€ entre le déficit de 2025 et 3 %) ; le rendement d'un portefeuille.

**Selon le point de départ et le modèle (réconciliation C03)** : pour stabiliser la dette, 4,3 à 5,5 points de PIB en partant d'une trajectoire sans aucune mesure ; 3,0 à 3,8 points au-delà du budget 2027 s'il est adopté tel quel (il ne l'est pas au 21 novembre 2026). Le tableau ci-dessous est celui du modèle de la cellule, sans le budget 2027.

| Objectif | Horizon | Mesures nécessaires à l'horizon (points de PIB) | En Md€ de 2025 | Dette à l'horizon (% du PIB) |
|---|---|---|---|---|
| équilibre | 2027 | 9,9 | 297 | 123 |
| équilibre | 2030 | 9,2 | 275 | 120 |
| équilibre | 2035 | 9,0 | 268 | 120 |
| déficit à 3 % | 2027 | 5,3 | 160 | 122 |
| déficit à 3 % | 2030 | 5,4 | 162 | 125 |
| déficit à 3 % | 2035 | 5,9 | 175 | 132 |
| stabilisation de la dette | 2027 | 4,4 | 133 | 122 |
| stabilisation de la dette | 2030 | 5,2 | 155 | 125 |
| stabilisation de la dette | 2035 | 5,2 | 157 | 134 |
| baisse du ratio de dette | 2027 | 6,0 | 179 | 122 |
| baisse du ratio de dette | 2030 | 6,5 | 193 | 124 |
| baisse du ratio de dette | 2035 | 6,4 | 190 | 130 |

## 2. Combinaisons sans double compte (A15)

Lecture corrigée par l'arbitrage : aucune combinaison **des mesures déjà chiffrées** n'atteint 3 % ni ne stabilise la dette avant 2035, même avec un taux à l'émission de 2,8 % ; une dépense primaire stable en volume y parviendrait vers 2035 dans le même modèle, sans qu'aucune période française de trois ans l'ait tenue.

| Combinaison | Mesures | Rendement 2030 (Md€) | Déficit 2030 | Déficit 2035 | Dette 2035 |
|---|---|---|---|---|---|
| K1 centrale, branche gel — si adopte | 38 | 62 | 5,4 | 5,5 | 137 |
| K1 centrale, branche gel — decote d'execution A13 | 38 | 41 | 6,0 | 6,6 | 143 |
| K2 centrale, branche abattement — si adopte | 37 | 60 | 5,5 | 5,6 | 137 |
| K2 centrale, branche abattement — decote d'execution A13 | 37 | 40 | 6,1 | 6,7 | 143 |
| K3 centrale gel, sans mesures rejetees — si adopte | 31 | 41 | 6,0 | 6,3 | 142 |
| K3 centrale gel, sans mesures rejetees — decote d'execution A13 | 31 | 30 | 6,4 | 7,0 | 145 |
| K4 prudente — si adopte | 24 | 45 | 5,9 | 6,8 | 142 |
| K4 prudente — decote d'execution A13 | 24 | 28 | 6,4 | 7,5 | 146 |
| K5 ambitieuse large — si adopte | 42 | 71 | 5,1 | 5,1 | 135 |
| K5 ambitieuse large — decote d'execution A13 | 42 | 47 | 5,9 | 6,3 | 141 |

K1 : enveloppes centrales, retraites par le gel. K2 : par la fin de l'abattement. K3 : K1 sans les mesures rejetées au Parlement. K4 : prudente. K5 : ambitieuse.

## 3. Mesures du portefeuille « dépense » (A13)

| Id | Mesure | Net 2030 si adoptée | Net 2030 après décote | Combinaisons | Qui paie (S04) | Preuve |
|---|---|---|---|---|---|---|
| P-A13-001 | Non-revalorisation en 2027 des pensions de base et des prestations hors minima et prime d'activite | 4,5 | 2,3 | K1 K4 K5 | retraités 80 %, autres ménages 20 % ; dixième aisé 12–15 %, moitié modeste 37–45 % | C (rendement mecanique, depend de […] |
| P-A13-001b | VARIANTE non sommee : suppression de l'abattement de 10 % sur les pensions a l'IR | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C |
| P-A13-002 | Regle 2028-2032 : pensions de base au-dessus de 1 260 EUR revalorisees a l'inflation moins 0,4 point (coefficient de soutenabilite) | 1,9 | 0,9 | K1 K3 K4 K5 | retraités 100 % | D (1 pt = 2,9 Md EUR en 2025 / part […] |
| P-A13-003 | Annulation de la suspension de la reforme de 2023 (art. 105 LFSS 2026) | 1,4 | 0,7 | K1 K2 K4 K5 | autres ménages 100 % | D |
| P-A13-004 | Age d'ouverture des droits porte a 65 ans a partir de la generation 1968 | 0,0 | 0,0 | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D (simulation) / report B […] |
| P-A13-004b | VARIANTE non sommee : duree d'assurance portee a 44 ans des la generation 1972 | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A13-005 | Indemnites journalieres : remplacement 50 a 45 % (ou carence de 7 jours), duree maximale 2 ans des 2029, plafond AT-MP a 1,4 Smic | 2,6 | 2,0 | K1 K2 K3 K4 K5 | non ventilé 100 % | C/D |
| P-A13-006 | Maitrise du cout des produits de sante (baisses de prix, biosimilaires) | 1,5 | 1,1 | K1 K2 K3 K4 K5 | entreprises 100 % | C |
| P-A13-007 | Hausse de certains tickets moderateurs et extension des franchises | 2,0 | 1,0 | K1 K2 K3 K4 K5 | ménages non ventilés 100 % | C |
| P-A13-008 | Gel des revalorisations conventionnelles prevues en 2027 | 0,0 | 0,0 | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A13-009 | Aides au logement : bareme abaisse de 3 % etale 2028-2030 | 0,3 | 0,3 | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | B (incidence) / D (chiffrage) |
| P-A13-010 | Suspension pour un an des avancements et promotions (GVT) en 2027 | 3,2 | 2,4 | K1 K2 K3 K4 K5 | agents publics 100 % | D |
| P-A13-011 | Effectifs enseignants ajustes a la demographie scolaire : 5 000 ETP a la rentree 2027 (Cour) | 0,1 | 0,1 | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (demographie projetee) |
| P-A13-011b | Extension 2028-2035 : moitie du potentiel demographique (1,7 million d'eleves de moins) rendue, l'autre moitie redeployee vers le primaire | 0,4 | 0,3 | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D (calcul A13 au ratio de la Cour) |
| P-A13-012 | Recentrage emploi-formation : primes d'apprentissage du superieur, ticket moderateur CPF, CEJ, prime d'activite des apprentis | 2,0 | 1,8 | K1 K2 K3 K4 K5 | non ventilé 100 % | C |
| P-A13-013 | Allegements generaux : gel du bareme et assiette elargie (PLFSS 2027), forfait social sur les aides directes (Cour) | 6,7 | 5,0 | aucune | entreprises 100 % | B/C (microsimulation) |
| P-A13-014 | Aides budgetaires a faible additionnalite (missions des CCI et CMA, accompagnement Bpifrance, buralistes, presse, FASEP) | 0,8 | 0,6 | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (revue sans evaluation causale) |
| P-A13-015 | Credit d'impot recherche resserre (jeunes docteurs, perimetre Frascati, forfait de fonctionnement 43 a 40 %) | 0,4 | 0,3 | K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C |
| P-A13-016 | FCTVA : taux abaisse de 5 points | 1,1 | 0,5 | K1 K2 K4 K5 | collectivités 100 % | A (2014-2017 : chute de […] |
| P-A13-017 | Baisse des recettes de fonctionnement transferees au bloc communal et aux regions (part forfaitaire de la DGF, fraction de TVA), […] | 3,4 | 1,7 | K1 K2 K4 K5 | collectivités 100 % | D (la Cour suppose 80 % d'effet sur le […] |
| P-A13-018 | Operateurs : fonctions support reduites de 20 % a missions constantes | 0,4 | 0,3 | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (borne volontariste) |
| P-A13-019 | Efficience des interventions culture et jeunesse | 0,4 | 0,3 | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A13-020 | Mutualisation des achats de l'Etat (gains achats) | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | E (gain mesure a la notification contre […] |
| P-A13-021 | Norme de depense nette pluriannuelle par sous-secteur, plafond nominal vote a trois ans avec marge de 1 a 3 % et cordes de rappel | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |
| P-A13-022 | Extinction automatique et plafonds des depenses fiscales et exonerations, instance de suivi des evaluations | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |
| P-A13-023 | Revues de depenses arrimees au calendrier budgetaire avec instance d'arbitrage (59,5 Md EUR de pistes non exploitees) | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |
| P-A13-024 | Contractualisation des depenses de fonctionnement des grandes collectivites (type Cahors) en contrepartie de la baisse des transferts | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |
| P-A13-025 | Ondam pluriannuel contraignant et mise en reserve consolidee des soins de ville | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |
| P-A13-026 | Transmission automatique au Parlement des notes de prevision et regle de surplus etendue aux collectifs | 0,0 | 0,0 | — | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C (effet causal des regles discute) |

## 4. Mesures du portefeuille « recettes » (A14)

| Id | Mesure | Net 2030 | Statut | Combinaisons | Qui paie (S04) | Preuve |
|---|---|---|---|---|---|---|
| P-A14-001 | Niches IR du PLF 2027 : plafond 3 000 EUR de l'abattement de 10 % sur les pensions, fiscalisation IJ AT-MP/ALD, fin de la purge 150-0 B […] | 3,0 | PLF/PLFSS 2027 (rejete le 4/11/2026) | K1 K2 K4 K5 | retraités 44 %, ménages non ventilés 56 % | A (texte du PLF) / D (chiffrage ex ante) |
| P-A14-002 | Allegements et complements de salaire du PLFSS 2027 : complements de salaire dans l'assiette de la RGD, gel AG, exclusion PPV, indemnites […] | 3,7 | PLF/PLFSS 2027 (rejete) | K1 K2 K3 K4 K5 | entreprises 100 % | D (Mesange) ; B pour le signe […] |
| P-A14-003 | Surtaxe exceptionnelle sur les organismes complementaires (prolongation) | 0,0 | PLFSS 2027 (rejete) | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | A (texte) / D |
| P-A14-004 | Lutte contre la fraude du PLF 2027 (delegation interministerielle, mise en conformite, facturation electronique 2027) | 0,8 | PLF 2027 (rejete) | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D (cible) ; E |
| P-A14-005 | Autres prelevements recurrents du PLF 2027 (TEITLD, fin TVA 10 % television, TSCA, produits sucres, tarification AT-MP) | 1,7 | PLF/PLFSS 2027 (rejete) | K1 K2 K3 K4 K5 | non ventilé 100 % | A (texte) / D |
| P-A14-006 | Prelevement sur les actifs en desherence (PLF 2027) | 0,0 | PLF 2027 (rejete) | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A14-007 | Contribution exceptionnelle sur les benefices des grandes entreprises transformee en tranche permanente d'IS (niveau 2026, 7,3 Md) | 5,7 | perennisation (2025 la contient deja) | K1 K2 K4 K5 | entreprises 100 % | A (rendement 2025 constate Insee 8 Md […] |
| P-A14-008 | Contribution differentielle sur les hauts revenus (CDHR) rendue permanente | 0,3 | perennisation | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | A/D |
| P-A14-009 | Abattement de 10 % sur les pensions : suppression (au-dela du plafond du PLF 2027) | 4,4 | Cour nov. 2026 (non retenu tel quel par le PLF) | K2 | retraités 100 % ; dixième aisé 24–28 %, moitié modeste 17–18 % | A (fiche VM II) / D |
| P-A14-010 | Forfait social de 8 % sur les aides directes aux salaries (titres-restaurant, cheques vacances, CSE) | 0,7 | Cour nov. 2026 | K1 K2 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A14-011 | TVA a 20 % dans la restauration et les services a la personne (hors garde d'enfants et autonomie) | 3,9 | Cour nov. 2026 | K1 K2 K3 K5 | ménages non ventilés 44 %, entreprises 56 % | B (incidence) / D (rendement) |
| P-A14-012 | Credit d'impot services a la personne ramene a 40 % pour les activites de la vie quotidienne | 0,9 | Cour nov. 2026 | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C/D |
| P-A14-013 | Pacte Dutreil : abattement ramene de 75 % a 50 % | 1,2 | Cour nov. 2026 | K1 K2 K3 K4 K5 | ménages non ventilés 100 % | A/C (Cour, IPP n°62) |
| P-A14-014 | Logement : fin de l'exoneration d'IS des organismes HLM, recentrage de l'abattement de taxe fonciere en QPV | 0,6 | Cour nov. 2026 | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C/D |
| P-A14-015 | Successions : assurance-vie integree au bareme au-dela de 152 500 EUR par beneficiaire ; fin de la reduction de 50 % des donations avant 70 […] | 3,4 | nouveau | K1 K2 K3 K5 | ménages non ventilés 100 % | C (CAE, donnees fiscales) / D |
| P-A14-016 | Successions : taxation de l'usufruit a sa reunion avec la nue-propriete (fin de l'avantage du demembrement) | 0,8 | nouveau | K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D |
| P-A14-017 | Allegements generaux : desindexation nominale du bareme 2028-2035 (gel en euros des seuils relatifs au SMIC) | 5,6 | nouveau | K1 K2 K3 K5 | entreprises 100 % | B (signe) / D (ampleur) |
| P-A14-018 | Reductions majorees de cotisations ciblees sur les jeunes et les publics eloignes de l'emploi (recyclage partiel) | -1,0 | nouveau | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | B (meta-analyses citees par le CAE) |
| P-A14-019 | Credit d'impot recherche calcule au niveau du groupe | 0,6 | nouveau (piste IGF/CPO) | K1 K2 K3 K4 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | B (CNEPI : pas d'effet pour les GE) / D |
| P-A14-020 | Revenus durablement loges dans des holdings patrimoniales controlees par peu de personnes : imposition (version CPO) | 0,5 | nouveau (renforcement) | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D [S] |
| P-A14-021 | Impot plancher de 2 % sur les patrimoines > 100 M EUR ('taxe Zucman') | 6,0 | nouveau | aucune | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D (simulation WIL) ; C (elasticites […] |
| P-A14-022 | TVA : reduire l'ecart de recouvrement d'un point de la TVA theorique d'ici 2030 (facturation electronique) | 1,6 | nouveau | K1 K2 K3 K5 | entreprises 100 % | C (ecart Commission) / D |
| P-A14-023 | Fraude aux cotisations : precompte des plateformes, recouvrement des redressements | 0,4 | nouveau | K1 K2 K3 K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | C/D |
| P-A14-024 | Quotient conjugal plafonne au niveau du plafond du quotient familial | 2,9 | nouveau | K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D [S] |
| P-A14-027 | CSG : fin de la deductibilite avec recyclage partiel sur les bas taux | 4,5 | nouveau | K5 | non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale) | D [S] |

## 5. Limites à garder avec cette table

- Un profil par niveau de vie n'est publié que pour un cinquième des montants de chaque portefeuille ; les parts par dixième et par moitié sont des calculs de S04 à partir d'effets publiés.
- Les décotes d'exécution d'A13 sont un jugement chiffré calé sur cinq précédents ; A14 applique à la place un test parlementaire.
- L'ordre des multiplicateurs (transferts au-dessus des impôts) est une hypothèse ; le multiplicateur d'ensemble de 0,6 n'est pas validé sur le passé.
- Aucune mesure d'emploi, d'efficience ou d'impôt large non chiffrée par A13 ou A14 ne figure ici.
