"""A14 - Portefeuille recettes / croissance : table des mesures, enveloppes, tests adverses.
Usage : python -I a14_portefeuille.py <dossier_sortie>
Toutes les valeurs d'entree viennent des pieces citees dans la colonne 'source' (voir A14.md, sections 3 et 17).
Les coefficients 'net_*' sont soit documentes (colonne 'base_net'), soit des hypotheses H-A14 explicites.
Montants en Md EUR, annee pleine, a l'echelle du PIB 2025 (1 pt de PIB = 29,91 Md EUR ; Eurostat, oct. 2026).
"""
import csv
import sys
import os

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
PT = 29.91  # Md EUR par point de PIB 2025 (151,592 / 5,068 % ; A01, Eurostat 21/10/2026)

# Coefficients documentes
EMPLOI_ALLEG = 1 - (20000 * (19.0 / 980000)) / 2.5   # Cour nov. 2026 (Mesange : 20 000 emplois pour 2,5 Md) x Bozio-Wasmer (19 Md / 980 000 ETP)
IS_PARTIEL = 4.4 / 8.0                                # IAG ch. 6 citant Bach (IPP) : 4,4 (reactivite partielle) / 8 (aucune)
JAKOBSEN = 0.26                                       # CAE Focus 118 citant Jakobsen et al. 2024 : -74 % vs effet mecanique
H_STD = (0.70, 0.85, 1.00)                            # H-A14-001 : bande generique sans piece (bas, central, haut)

# id ; nom ; famille ; assiette ; groupe d'exclusion ; recoupement ; statut ; recurrence ;
# brut (annee pleine) ; (net_bas, net_central, net_haut) en coefficients ; base_net ;
# rampe {2027,2030,2035,2050} (part du net plein) ; gain_vs_2025 (1 si nouveau par rapport a 2025, 0 sinon) ;
# drapeaux : mobile (assiette mobile), conteste (retire/rejete en seance 2025-2026), temporaire ;
# enveloppes (P/C/A) ; perdants_revenu ; perdants_acteurs ; preuve ; source ; plan_si_decoit
M = []
def m(**k):
    M.append(k)

R_FULL = {2027: 1.0, 2030: 1.0, 2035: 1.0, 2050: 1.0}

m(id="P-A14-001", nom="Niches IR du PLF 2027 : plafond 3 000 EUR de l'abattement de 10 % sur les pensions, fiscalisation IJ AT-MP/ALD, fin de la purge 150-0 B ter, amortissement LMNP",
  famille="niches fiscales", assiette="IR (pensions, IJ, plus-values d'apport, location meublee)", groupe="G-RETRAITES-IR ; G-LOGEMENT",
  recoupement="RESF 2027 T18 'Niches fiscales' 2,9 + 150-0 B ter ASSO 0,3 ; Cour 2026 n°1 (alternative) et n°17 (LMNP)", statut="PLF/PLFSS 2027 (rejete le 4/11/2026)",
  recurrence="recurrent", brut=3.2, net=(0.90, 0.95, 1.0), base_net="H-A14-002 : assiettes peu mobiles (pensions, IJ) ; LMNP : effet sur l'offre locative non chiffre",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=1, temporaire=0, env="PCA",
  perdants_rev="retraites imposables (1/3 des foyers comportant un retraite selon le Gouvernement) ; deciles 6-10", perdants_act="retraites imposables ; victimes d'AT en arret ; investisseurs LMNP",
  preuve="A (texte du PLF) / D (chiffrage ex ante)", source="RESF 2027 tableau 18 p.195 [C copie A03] ; DP budget 2027 p.18 [C copie A07] ; Cour nov. 2026 p.80 [C archive]",
  plan="si rejet : remplacer par P-A14-009 (suppression) sous condition de ressources (CPO), ou basculer l'effort sur P-A14-015")
m(id="P-A14-002", nom="Allegements et complements de salaire du PLFSS 2027 : complements de salaire dans l'assiette de la RGD, gel AG, exclusion PPV, indemnites de rupture, net de l'effet retour IS",
  famille="cotisations et allegements", assiette="cotisations employeurs (bas salaires)", groupe="G-ALLEGEMENTS",
  recoupement="RESF T18 ASSO 3,3+0,8+0,4+0,4 ; Etat 0,4 - 0,9 ; Cour 2026 n°13 (gel AG 2,5)", statut="PLF/PLFSS 2027 (rejete)",
  recurrence="recurrent", brut=4.4, net=(EMPLOI_ALLEG - 0.10, EMPLOI_ALLEG, 1.0), base_net="C-A14-002 : Mesange via Cour (20 000 emplois / 2,5 Md) x cotisations perdues par ETP (Bozio-Wasmer)",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="PCA",
  perdants_rev="salaries pres du SMIC (moindres embauches, environ 35 000 emplois selon le meme ratio)", perdants_act="employeurs de main-d'oeuvre peu qualifiee (commerce, hotellerie, proprete)",
  preuve="D (Mesange) ; B pour le signe (litterature allegements)", source="RESF 2027 T18 [C copie A03] ; Cour nov. 2026 p.41-42 et p.107 [C archive] ; Bozio-Wasmer 2024 p.68-69 [C copie A04]",
  plan="si pertes d'emploi superieures : recycler 0,5-1 Md vers les reductions majorees jeunes (CAE n°91, rec. 4)")
m(id="P-A14-003", nom="Surtaxe exceptionnelle sur les organismes complementaires (prolongation)", famille="taxes sectorielles", assiette="primes d'assurance sante complementaire",
  groupe="G-SANTE-OC", recoupement="RESF T18 ASSO 1,1 ; Cour 2026 n°7 (meme payeur final)", statut="PLFSS 2027 (rejete)",
  recurrence="temporaire", brut=1.1, net=(0.8, 0.9, 1.0), base_net="H-A14-002 ; incidence : hausse des primes possible (non mesuree)",
  rampe={2027: 1.0, 2030: 0.0, 2035: 0.0, 2050: 0.0}, vs2025=1, mobile=0, conteste=0, temporaire=1, env="PCA",
  perdants_rev="assures complementaires, proportionnel aux primes (regressif)", perdants_act="mutuelles, assureurs",
  preuve="A (texte) / D", source="RESF 2027 T18 [C copie A03]", plan="ne pas reconduire : temporaire par construction")
m(id="P-A14-004", nom="Lutte contre la fraude du PLF 2027 (delegation interministerielle, mise en conformite, facturation electronique 2027)", famille="fraude",
  assiette="TVA, IS, cotisations", groupe="G-FRAUDE", recoupement="RESF T18 0,8 + 0,2 (ASSO) + 0,2 (facturation electronique)", statut="PLF 2027 (rejete)",
  recurrence="recurrent", brut=1.2, net=(0.33, 0.67, 0.83), base_net="DP 2027 : cible de 1 Md 'effectivement recouvre' ; HCFiPS : 680 M recouvres pour > 2 Md detectes",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="PCA",
  perdants_rev="fraudeurs (non ventilable)", perdants_act="entreprises et travailleurs non declares", preuve="D (cible) ; E",
  source="DP budget 2027 p.12 [C copie A07] ; RESF T18 ; HCFiPS 2026 [C copie A04]", plan="ne compter que l'encaisse constate N-1 ; pas de rendement inscrit d'avance au-dela de 0,4")
m(id="P-A14-005", nom="Autres prelevements recurrents du PLF 2027 (TEITLD, fin TVA 10 % television, TSCA, produits sucres, tarification AT-MP)", famille="taxes sectorielles",
  assiette="autoroutes, television, assurance, consommation", groupe="G-DIVERS-PLF", recoupement="RESF T18 0,8+0,4+0,2+0,3+0,3", statut="PLF/PLFSS 2027 (rejete)",
  recurrence="recurrent", brut=2.0, net=H_STD, base_net="H-A14-001", rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="PCA",
  perdants_rev="consommateurs (sucres : regressif)", perdants_act="concessionnaires d'autoroutes, chaines de television, assureurs",
  preuve="A (texte) / D", source="RESF 2027 T18 [C copie A03]", plan="mesures independantes : abandon de l'une sans effet sur les autres")
m(id="P-A14-006", nom="Prelevement sur les actifs en desherence (PLF 2027)", famille="exceptionnel", assiette="avoirs non reclames", groupe="G-EXCEPTIONNEL",
  recoupement="RESF T18 1,4", statut="PLF 2027 (rejete)", recurrence="exceptionnel", brut=1.4, net=(1.0, 1.0, 1.0), base_net="montant ex ante",
  rampe={2027: 1.0, 2030: 0.0, 2035: 0.0, 2050: 0.0}, vs2025=1, mobile=0, conteste=0, temporaire=1, env="CA",
  perdants_rev="sans objet", perdants_act="detenteurs (CDC, assureurs)", preuve="D", source="RESF 2027 T18 [C copie A03]", plan="ne jamais l'inscrire en recurrent")
m(id="P-A14-007", nom="Contribution exceptionnelle sur les benefices des grandes entreprises transformee en tranche permanente d'IS (niveau 2026, 7,3 Md)", famille="IS",
  assiette="benefices des entreprises > 1 Md de CA", groupe="G-IS", recoupement="RESF T18 : 8,0 (2025), 7,3 (2026), PLF 2027 5,0 ; exclusif de P-A14-025",
  statut="perennisation (2025 la contient deja)", recurrence="recurrent si perennise", brut=7.3, net=(IS_PARTIEL, (IS_PARTIEL + 1) / 2, 1.0),
  base_net="IAG ch.6 citant Bach (IPP) : 4,4/8 en reactivite partielle", rampe=R_FULL, vs2025=0, mobile=1, conteste=1, temporaire=0, env="PCA",
  perdants_rev="actionnaires (deciles 9-10, surtout top 1 %) ; salaries via partage de la valeur (non mesure)", perdants_act="environ 440 grandes entreprises [S]",
  preuve="A (rendement 2025 constate Insee 8 Md avec le fret) ; D (reaction)", source="Insee IP 2106 [C copie A04] ; RESF T18 ; CC 2025-874 DC [C]",
  plan="si base IS chute : clause de revoyure annuelle sur le taux ; pas d'inscription au-dessus de 4 Md")
m(id="P-A14-008", nom="Contribution differentielle sur les hauts revenus (CDHR) rendue permanente", famille="revenus eleves", assiette="revenu fiscal > 250 000 EUR",
  groupe="G-CAPITAL", recoupement="RESF T18 : LFI 2025 0,4 ; PLF 2026 prolongation 0,5", statut="perennisation", recurrence="recurrent si perennise",
  brut=0.4, net=(0.5, 0.75, 1.0), base_net="H-A14-003 : assiette mobile (revenus du capital)", rampe=R_FULL, vs2025=0, mobile=1, conteste=0, temporaire=0, env="PCA",
  perdants_rev="top 0,1 %", perdants_act="foyers a tres hauts revenus faiblement imposes", preuve="A/D", source="RESF 2027 T18 [C copie A03]", plan="petit montant : sans incidence sur l'enveloppe")
m(id="P-A14-009", nom="Abattement de 10 % sur les pensions : suppression (au-dela du plafond du PLF 2027)", famille="niches fiscales", assiette="IR sur pensions",
  groupe="G-RETRAITES-IR (exclusif du gel des pensions, Cour n°1)", recoupement="Cour 2026 n°1 alternative : 5,8 plein (7,3 premiere annee) ; moins 1,4 deja dans P-A14-001",
  statut="Cour nov. 2026 (non retenu tel quel par le PLF)", recurrence="recurrent", brut=4.4, net=(0.95, 1.0, 1.0), base_net="assiette non mobile ; chiffrage DG Tresor cite par la Cour",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=1, temporaire=0, env="CA",
  perdants_rev="retraites imposables, au-dessus de la mediane ; 28 % du cout pour les menages du dernier decile (2023)", perdants_act="15,1 millions de menages beneficiaires",
  preuve="A (fiche VM II) / D", source="Cour nov. 2026 p.18 et p.80-81 [C archive] ; PLF 2026 VM II fiche 120401 [C copie A04]",
  plan="si refus : condition de ressources (CPO) = environ 28 % du cout (1,6 Md)")
m(id="P-A14-010", nom="Forfait social de 8 % sur les aides directes aux salaries (titres-restaurant, cheques vacances, CSE)", famille="cotisations et allegements",
  assiette="complements de salaire exemptes", groupe="G-ALLEGEMENTS", recoupement="Cour 2026 n°13 ; rejete au PLFSS 2026", statut="Cour nov. 2026",
  recurrence="recurrent", brut=0.8, net=(0.8, 0.9, 1.0), base_net="Cour : reduction des attributions 'probablement limitee'",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=1, temporaire=0, env="CA", perdants_rev="salaries des entreprises dotees d'un CSE (deciles 3-8)",
  perdants_act="employeurs, emetteurs de titres", preuve="D", source="Cour nov. 2026 p.42 [C archive]", plan="abandon sans effet sur le reste")
m(id="P-A14-011", nom="TVA a 20 % dans la restauration et les services a la personne (hors garde d'enfants et autonomie)", famille="consommation",
  assiette="TVA taux intermediaire", groupe="G-TVA (exclusif de 10->13 %, Cour n°14 option 2)", recoupement="Cour 2026 n°14 option 1",
  statut="Cour nov. 2026", recurrence="recurrent", brut=4.6, net=H_STD, base_net="H-A14-001 ; incidence : hausses 2012 et 2014 repercutees 4 a 5 fois plus que la baisse (IPP n°32)",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="CA",
  perdants_rev="clients des restaurants (tous deciles, plus en valeur dans le haut) ; menages employeurs de services de confort", perdants_act="restaurateurs (marges), salaries du secteur (19 % du gain de 2009)",
  preuve="B (incidence) / D (rendement)", source="Cour nov. 2026 p.43-44 [C archive] ; IPP note 32 [C copie A04] ; IGF 2024 annexe III [C via A11]",
  plan="si emploi du secteur recule : mesurer 24 mois ; pas de retour au taux reduit sans evaluation")
m(id="P-A14-012", nom="Credit d'impot services a la personne ramene a 40 % pour les activites de la vie quotidienne", famille="niches fiscales",
  assiette="IR (CISAP)", groupe="G-CISAP", recoupement="Cour 2026 n°15", statut="Cour nov. 2026", recurrence="recurrent", brut=1.1, net=H_STD,
  base_net="H-A14-001 ; risque de travail non declare non evalue (Cour)", rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="PCA",
  perdants_rev="dernier decile = 44 % de l'avantage", perdants_act="entreprises de menage, jardinage, soutien scolaire", preuve="C/D",
  source="Cour nov. 2026 p.44-45 [C archive]", plan="si declaratif recule : suivi URSSAF du nombre d'heures declarees")
m(id="P-A14-013", nom="Pacte Dutreil : abattement ramene de 75 % a 50 %", famille="successions", assiette="DMTG (biens professionnels)", groupe="G-TRANSMISSION",
  recoupement="Cour 2026 n°16 ; CPO dec. 2025 ; LFI 2026 deja sur l'assiette", statut="Cour nov. 2026", recurrence="recurrent", brut=1.34, net=(0.75, 0.9, 1.0),
  base_net="Cour : effets comportementaux des DMTG 'moindres et plus etales' ; regime reste attractif", rampe=R_FULL, vs2025=1, mobile=1, conteste=0, temporaire=0, env="PCA",
  perdants_rev="heritiers d'entreprises de grande valeur : 65 % de l'avantage pour 110 personnes (2024)", perdants_act="ETI et grandes entreprises familiales",
  preuve="A/C (Cour, IPP n°62)", source="Cour nov. 2026 p.46 et annexe [C archive] ; synthese Cour Dutreil nov. 2025 [C via A11] ; IPP n°62 [C copie A04]",
  plan="si anticipations (donations avancees) : rendement 2027 gonfle puis creux ; lisser sur 3 ans")
m(id="P-A14-014", nom="Logement : fin de l'exoneration d'IS des organismes HLM, recentrage de l'abattement de taxe fonciere en QPV", famille="niches fiscales",
  assiette="IS, taxe fonciere", groupe="G-LOGEMENT", recoupement="Cour 2026 n°17 (hors LMNP deja au PLF)", statut="Cour nov. 2026", recurrence="recurrent",
  brut=0.7, net=H_STD, base_net="H-A14-001", rampe={2027: 0.43, 2030: 1.0, 2035: 1.0, 2050: 1.0}, vs2025=1, mobile=0, conteste=0, temporaire=0, env="PCA",
  perdants_rev="locataires HLM si moindre entretien (non mesure)", perdants_act="organismes HLM les plus rentables", preuve="C/D",
  source="Cour nov. 2026 p.47-48 [C archive]", plan="moduler selon l'autofinancement net du secteur (taux du livret A)")
m(id="P-A14-015", nom="Successions : assurance-vie integree au bareme au-dela de 152 500 EUR par beneficiaire ; fin de la reduction de 50 % des donations avant 70 ans",
  famille="successions", assiette="DMTG (assurance-vie, donations)", groupe="G-TRANSMISSION", recoupement="aucun dans le PLF 2027 ni la Cour 2026 (Cour : refonte 'a plus long terme')",
  statut="nouveau", recurrence="recurrent", brut=4.5, net=(0.5, 0.75, 1.0), base_net="H-A14-004 : CAE n°69 donne 4-5 Md (FICOVIE 2017-2018) ; anticipations et donnees anciennes",
  rampe={2027: 0.25, 2030: 1.0, 2035: 1.0, 2050: 1.0}, vs2025=1, mobile=1, conteste=0, temporaire=0, env="CA",
  perdants_rev="45 000 beneficiaires par an recevant > 152 500 EUR (17,5 Md transmis) ; 1 900 > 852 500 EUR", perdants_act="assureurs-vie (collecte)",
  preuve="C (CAE, donnees fiscales) / D", source="CAE note n°69, dec. 2021, p.7-8 et graphiques 3-4 [C]",
  plan="si collecte et transmissions se deplacent (democrement, holdings) : etendre a P-A14-016 ; sinon relever les abattements en ligne directe pour la majorite (CAE bareme 3)")
m(id="P-A14-016", nom="Successions : taxation de l'usufruit a sa reunion avec la nue-propriete (fin de l'avantage du demembrement)", famille="successions",
  assiette="DMTG (demembrement)", groupe="G-TRANSMISSION", recoupement="aucun", statut="nouveau", recurrence="recurrent", brut=2.5, net=(0.4, 0.6, 0.8),
  base_net="H-A14-004 ; CAE : 2-3 Md avec donnees 2006 ; securite juridique des donations passees", rampe={2027: 0.0, 2030: 0.5, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=1, conteste=0, temporaire=0, env="A", perdants_rev="donateurs patrimoniaux (deciles 9-10)", perdants_act="notariat, gestion de patrimoine",
  preuve="D", source="CAE note n°69 p.7 [C]", plan="appliquer aux seules donations nouvelles")
m(id="P-A14-017", nom="Allegements generaux : desindexation nominale du bareme 2028-2035 (gel en euros des seuils relatifs au SMIC)", famille="cotisations et allegements",
  assiette="cotisations employeurs", groupe="G-ALLEGEMENTS", recoupement="prolonge le gel 2026-2027 (RESF, Cour n°13)", statut="nouveau",
  recurrence="recurrent cumulatif", brut=17.6, net=(EMPLOI_ALLEG - 0.15, EMPLOI_ALLEG, 0.95), base_net="C-A14-002 (Mesange) ; Cour : +2,41 % de SMIC = +2,2 Md ; IAG : 16 Md a 10 ans",
  rampe={2027: 0.0, 2030: 6.6 / 17.6, 2035: 1.0, 2050: 1.0}, vs2025=1, mobile=0, conteste=0, temporaire=0, env="CA",
  perdants_rev="salaries entre 1 et 1,6 SMIC (embauches) ; la pente des taux marginaux baisse (gain salarial attendu, CAE)", perdants_act="secteurs a bas salaires",
  preuve="B (signe) / D (ampleur)", source="CAE n°91 juin 2026 rec. 2 [C] ; Cour nov. 2026 p.41 [C archive] ; IAG ch.6 p.13 [C]",
  plan="si chomage des peu qualifies monte de plus de 0,3 pt : reindexer partiellement et cibler jeunes (P-A14-018)")
m(id="P-A14-018", nom="Reductions majorees de cotisations ciblees sur les jeunes et les publics eloignes de l'emploi (recyclage partiel)", famille="emploi",
  assiette="cotisations employeurs", groupe="G-ALLEGEMENTS", recoupement="contrepartie de P-A14-017", statut="nouveau", recurrence="recurrent (cout)",
  brut=-1.0, net=(1.0, 1.0, 1.0), base_net="cout fixe par choix ; effet emploi plus fort sur les jeunes (CAE n°91)", rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=0, conteste=0, temporaire=0, env="CA", perdants_rev="aucun (cout public)", perdants_act="aucun", preuve="B (meta-analyses citees par le CAE)",
  source="CAE n°91 rec. 4 [C]", plan="evaluer l'effet par cohorte (InserJeunes) avant toute extension")
m(id="P-A14-019", nom="Credit d'impot recherche calcule au niveau du groupe", famille="niches fiscales", assiette="IS (CIR)", groupe="G-CIR",
  recoupement="LFI 2025 deja +0,37 ; IGF 2024 ; non repris par la Cour 2026", statut="nouveau (piste IGF/CPO)", recurrence="recurrent", brut=0.7, net=H_STD,
  base_net="H-A14-001 ; A11 : 0,47 (critere 95 %) a 0,96 (50 %)", rampe={2027: 0.3, 2030: 1.0, 2035: 1.0, 2050: 1.0}, vs2025=1, mobile=1, conteste=0, temporaire=0, env="PCA",
  perdants_rev="sans objet", perdants_act="grands groupes (50 entreprises = environ la moitie de la creance)", preuve="B (CNEPI : pas d'effet pour les GE) / D",
  source="A11 F-A11-010 et §10 [C via A11] ; CNEPI 2021 [C copie A04]", plan="si R&D des groupes recule (enquete R&D) : revoir le seuil")
m(id="P-A14-020", nom="Revenus durablement loges dans des holdings patrimoniales controlees par peu de personnes : imposition (version CPO)", famille="capital",
  assiette="revenus du capital (holdings)", groupe="G-CAPITAL", recoupement="PLF 2026 'taxe sur les holdings' : 0,1 Md (RESF) ; CPO dec. 2025 rec. 16.1", statut="nouveau (renforcement)",
  recurrence="recurrent", brut=1.0, net=(0.1, 0.5, 1.0), base_net="H-A14-003 ; ecart RESF (0,1) / CPO (1,0) non reconcilie", rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=1, conteste=0, temporaire=0, env="CA", perdants_rev="top 0,1 % (detenteurs de holdings)", perdants_act="family offices",
  preuve="D [S]", source="IAG ch.6 citant CPO dec. 2025 rec. 16.1 [S] ; RESF T18 [C copie A03]", plan="si rendement < 0,3 : revoir l'assiette (anti-abus) plutot que le taux")
m(id="P-A14-021", nom="Impot plancher de 2 % sur les patrimoines > 100 M EUR ('taxe Zucman')", famille="patrimoine", assiette="patrimoine net (dont biens professionnels)",
  groupe="G-CAPITAL (exclusif d'un ISF retabli)", recoupement="aucun ; rejete au Senat en juin 2025 [S]", statut="nouveau", recurrence="recurrent",
  brut=23.0, net=(0.0, JAKOBSEN, 0.5), base_net="brut = scenario WIL sans evasion ni depreciation (IAG, 5-23) ; x 0,26 (Jakobsen via CAE Focus 118) ; bas = censure (inference A14 a partir de CC 2012-662 DC §95-96)",
  rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0}, vs2025=1, mobile=1, conteste=1, temporaire=0, env="", perdants_rev="environ 1 800 foyers [S]",
  perdants_act="actionnaires de controle d'entreprises familiales", preuve="D (simulation WIL) ; C (elasticites scandinaves)",
  source="IAG ch.5 p.21 citant WIL [S] ; CAE Focus 118 p.15-16 [C] ; CC 2012-662 DC [C]", plan="CONDITIONNEL, hors enveloppes : ne l'inscrire qu'apres decision du Conseil constitutionnel et une annee d'encaissement")
m(id="P-A14-022", nom="TVA : reduire l'ecart de recouvrement d'un point de la TVA theorique d'ici 2030 (facturation electronique)", famille="fraude",
  assiette="TVA", groupe="G-FRAUDE", recoupement="au-dela des 0,2 de facturation electronique du PLF 2027", statut="nouveau", recurrence="recurrent", brut=2.2, net=(0.5, 0.75, 1.0),
  base_net="C-A14-003 : 12 121 M / 5,6 pts = 2,2 Md par point ; H-A14-005 sur l'atteinte", rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=0, conteste=0, temporaire=0, env="CA", perdants_rev="non ventilable", perdants_act="entreprises fraudeuses", preuve="C (ecart Commission) / D",
  source="Commission, VAT gap 2025 [C WebFetch]", plan="n'inscrire que l'ecart constate deux ans plus tard")
m(id="P-A14-023", nom="Fraude aux cotisations : precompte des plateformes, recouvrement des redressements", famille="fraude", assiette="cotisations",
  groupe="G-FRAUDE", recoupement="au-dela des 0,2 ASSO du PLFSS 2027", statut="nouveau", recurrence="recurrent", brut=0.5, net=(0.5, 0.75, 1.0),
  base_net="H-A14-005 ; HCFiPS : 1,4-1,8 Md eludes par les micro-entrepreneurs, 680 M recouvres", rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=0, conteste=0, temporaire=0, env="CA", perdants_rev="micro-entrepreneurs sous-declarant", perdants_act="plateformes", preuve="C/D",
  source="HCFiPS 2026 [C copie A04]", plan="idem P-A14-022")
m(id="P-A14-024", nom="Quotient conjugal plafonne au niveau du plafond du quotient familial", famille="revenu", assiette="IR", groupe="G-IR-BAREME",
  recoupement="aucun", statut="nouveau", recurrence="recurrent", brut=3.2, net=(0.8, 0.9, 1.0), base_net="H-A14-002 (IR, assiette peu mobile)",
  rampe=R_FULL, vs2025=1, mobile=0, conteste=0, temporaire=0, env="A", perdants_rev="couples mono-actifs ou a revenus tres inegaux, deciles 8-10",
  perdants_act="sans objet", preuve="D [S]", source="IAG ch.5 p.19 citant OFCE (Perivier, Pucci, fev. 2025) [S]", plan="abandon sans effet sur le reste")
m(id="P-A14-027", nom="CSG : fin de la deductibilite avec recyclage partiel sur les bas taux", famille="revenu", assiette="IR / CSG", groupe="G-IR-BAREME",
  recoupement="aucun", statut="nouveau", recurrence="recurrent", brut=5.0, net=(0.8, 0.9, 1.0), base_net="H-A14-002", rampe={2027: 0.0, 2030: 1.0, 2035: 1.0, 2050: 1.0},
  vs2025=1, mobile=0, conteste=0, temporaire=0, env="A", perdants_rev="contribuables imposes aux tranches superieures (deciles 8-10)", perdants_act="sans objet",
  preuve="D [S]", source="IAG ch.5 p.18 citant CPO, fev. 2025 [S]", plan="abandon sans effet sur le reste")

# Mesures listees mais hors totaux (alternatives, non retenues, voie emploi, gouvernance)
HORS = [
    ("P-A14-025", "IS : taux normal 25 % -> 33,5 % (alternative a P-A14-007)", "G-IS", "4,4 a 8 Md (IAG citant Bach, IPP) [S]", "exclusif de P-A14-007 ; non retenu : la France est revenue a la moyenne OCDE ; effet negatif de l'IS sur l'investissement converge dans la litterature citee par le comite (via Fipeco) [S]"),
    ("P-A14-026", "Suppression du PFU (retour au bareme)", "G-CAPITAL", "9 Md affiches (IAG citant IPP 2025) [S]", "NE RESISTE PAS : dividendes tres elastiques (14 -> 23 Md en 2018, comite fiscalite du capital) ; rendement net possiblement proche de zero"),
    ("P-A14-028", "Reprise du calendrier de la reforme de 2023 apres la suspension", "G-RETRAITES-AGE", "regimes +1,4 a +2,0 Md/an 2028-2032 ; APU environ 3 Md (A06)", "hors enveloppe recettes : depense de pension (recoupement probable avec A13), chiffre pour A15"),
    ("P-A14-029", "Investissement public : sanctuarisation de l'entretien et des projets prets", "G-INVEST", "cout 0 (contrainte) ; FMI 2014 : +1 pt d'investissement = +0,4 % de PIB an 1, +1,5 % an 4 [S via Astra]", "aucun autofinancement inscrit"),
    ("P-A14-030", "Fiscalite carbone : degel de la composante carbone", "G-ENERGIE", "non estime (aucune piece chiffree lue)", "non retenu : recul de 2018 sous la pression de la rue (A09) ; a instruire avec compensation"),
    ("P-A14-031", "TVA : taux intermediaire 10 % -> 13 % (alternative a P-A14-011)", "G-TVA", "4,3 Md (Cour n°14 option 2)", "exclusif de P-A14-011"),
    ("P-A14-032", "Retablissement de l'ISF (alternative a P-A14-021)", "G-CAPITAL", "4,5 Md (comite fiscalite du capital 2023 via IAG) [S]", "exclusif de P-A14-021"),
    ("P-A14-036", "Retour au taux de CVAE de 2023", "G-PRODUCTION", "environ 4 Md (IAG ch.6 p.18) [S]", "non retenu : IPP n°60 ne trouve pas d'effet robuste de la baisse de 2021, mais l'absence d'effet mesure n'est pas une preuve d'innocuite ; assiette ou l'ecart francais est le plus fort"),
    ("P-A14-037", "Successions : elargissement d'assiette et baisse de taux (CAE assiette 1, bareme 3)", "G-TRANSMISSION", "0 par construction ; 99 % d'heritiers gagnants (CAE n°69)", "variante redistributive de 013/015 : non cumulable avec leur rendement"),
    ("P-A14-038", "Productivite : aucun gain inscrit", "-", "1 pt de PIB permanent = 13,8 Md de prelevements bruts (Astra [S])", "non inscriptible ; couplage avec l'indexation des pensions (A06)"),
    ("P-A14-033", "Gouvernance : recettes superieures a la prevision traitees comme temporaires et affectees au solde", "-", "0 ex ante", "regle LOLF jamais appliquee (A08)"),
    ("P-A14-034", "Gouvernance : chiffrage actualise et clause d'extinction de chaque depense fiscale > 500 M", "-", "0 ex ante", "lecon Dutreil (A04, A11)"),
    ("P-A14-035", "Gouvernance : cadrage pluriannuel fiscalo-social et ajustement infra-annuel des credits d'impot (Cour leviers 2 et 7)", "-", "0 ex ante", "Cour nov. 2026 tableau 2"),
]

HORIZONS = [2027, 2030, 2035, 2050]
k_of = {"bas": 0, "central": 1, "haut": 2}

def net_val(x, h, scen="central", factor=1.0, override=None):
    c = x["net"][k_of[scen]] if override is None else override
    return x["brut"] * c * x["rampe"][h] * factor

rows = []
for x in M:
    r = {k: x[k] for k in ("id", "nom", "famille", "assiette", "groupe", "recoupement", "statut", "recurrence")}
    r["brut_annee_pleine"] = x["brut"]
    for s in ("bas", "central", "haut"):
        r[f"net_plein_{s}"] = round(x["brut"] * x["net"][k_of[s]], 2)
    for h in HORIZONS:
        r[f"net_central_{h}"] = round(net_val(x, h), 2)
    r["nouveau_vs_2025"] = "oui" if x["vs2025"] else "non (deja dans le solde 2025)"
    r["enveloppes"] = x["env"]
    r["base_du_net"] = x["base_net"]
    r["perdants_revenu"] = x["perdants_rev"]
    r["perdants_acteurs"] = x["perdants_act"]
    r["niveau_preuve"] = x["preuve"]
    r["source"] = x["source"]
    r["si_rendement_decoit"] = x["plan"]
    rows.append(r)

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "A14_table_mesures.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, "A14_mesures_hors_totaux.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["id", "mesure", "groupe", "rendement_affiche", "raison"])
    w.writerows(HORS)

# Controle d'exclusion : dans une enveloppe, un groupe exclusif ne peut contenir deux variantes du meme objet
# (les exclusions ont ete construites a la main : P-A14-007/025, 011/031, 021/032, 009 vs gel des pensions -> A13)

MULT = {"bas": 0.3, "central": 0.5, "haut": 1.0}   # multiplicateurs de prelevements (voir A14.md §5)
SEMI = 0.57                                         # semi-elasticite du solde (RESF 2027, note de tableau, copie A03)

def enveloppe(env, h, scen="central", factor=1.0, filt=lambda x: True, base="2027"):
    tot = 0.0
    for x in M:
        if env not in x["env"] or not filt(x):
            continue
        if base == "2025" and not x["vs2025"]:
            continue
        tot += net_val(x, h, scen, factor)
    return tot

out = []
for env, lab in (("P", "prudente"), ("C", "centrale"), ("A", "ambitieuse")):
    for h in HORIZONS:
        lo, ce, hi = (enveloppe(env, h, s) for s in ("bas", "central", "haut"))
        ce25 = enveloppe(env, h, "central", base="2025")
        lo25, hi25 = enveloppe(env, h, "bas", base="2025"), enveloppe(env, h, "haut", base="2025")
        macro = -SEMI * MULT["central"] * ce if h == 2027 else 0.0
        macro_hi = -SEMI * MULT["haut"] * ce if h == 2027 else 0.0
        out.append({"enveloppe": lab, "horizon": h, "net_bas": round(lo, 1), "net_central": round(ce, 1), "net_haut": round(hi, 1),
                    "net_central_vs_2025": round(ce25, 1), "net_bas_vs_2025": round(lo25, 1), "net_haut_vs_2025": round(hi25, 1), "retour_macro_central": round(macro, 1), "retour_macro_fort": round(macro_hi, 1),
                    "net_apres_macro_central": round(ce + macro, 1), "pts_PIB_central": round(ce / PT, 2)})

with open(os.path.join(OUT, "A14_enveloppes.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(out)

# Couverture des objectifs
CIBLES_2025 = {"3 %": (62, 62), "stabilisation": (67, 87), "equilibre": (152, 152)}
DEF27_PI = 6.5  # % PIB, RESF 2027 p.94 (politique inchangee)
CIBLES_2027 = {"3 %": ((DEF27_PI - 3.0) * PT,) * 2, "stabilisation": ((DEF27_PI - 2.8) * PT, (DEF27_PI - 2.2) * PT), "equilibre": ((DEF27_PI) * PT,) * 2}
cov = []
for o in out:
    if o["horizon"] not in (2027, 2030, 2035):
        continue
    for cname, (a, b) in CIBLES_2025.items():
        cov.append({"enveloppe": o["enveloppe"], "horizon": o["horizon"], "reference": "deficit 2025 (151,6 Md)", "cible": cname,
                    "besoin_Md": f"{a:.0f}-{b:.0f}" if a != b else f"{a:.0f}",
                    "part_couverte_central": f"{100*o['net_central_vs_2025']/b:.0f}-{100*o['net_central_vs_2025']/a:.0f} %" if a != b else f"{100*o['net_central_vs_2025']/a:.0f} %",
                    "part_couverte_bas_haut": f"{100*o['net_bas_vs_2025']/b:.0f} a {100*o['net_haut_vs_2025']/a:.0f} %"})
    for cname, (a, b) in CIBLES_2027.items():
        cov.append({"enveloppe": o["enveloppe"], "horizon": o["horizon"], "reference": "2027 a politique inchangee (6,5 %)", "cible": cname,
                    "besoin_Md": f"{a:.0f}-{b:.0f}" if round(a) != round(b) else f"{a:.0f}",
                    "part_couverte_central": f"{100*o['net_central']/b:.0f}-{100*o['net_central']/a:.0f} %" if round(a) != round(b) else f"{100*o['net_central']/a:.0f} %",
                    "part_couverte_bas_haut": f"{100*o['net_bas']/b:.0f} a {100*o['net_haut']/a:.0f} %"})
with open(os.path.join(OUT, "A14_couverture_objectifs.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(cov[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(cov)

# Tests adverses (trois enveloppes, horizons 2027 et 2030)
tests = []
def mob(env, h):
    t = 0.0
    for x in M:
        if env not in x["env"]:
            continue
        if x["mobile"]:
            t += x["brut"] * min(x["net"][1], JAKOBSEN if x["famille"] in ("patrimoine", "capital", "revenus eleves", "successions") else IS_PARTIEL) * x["rampe"][h]
        else:
            t += net_val(x, h)
    return t
def exil(env, h):
    return enveloppe(env, h) - 0.2 * sum(net_val(x, h) for x in M if env in x["env"] and x["famille"] in ("capital", "patrimoine", "revenus eleves"))
SURT = 7.3 * (IS_PARTIEL + 1) / 2
for env, lab in (("P", "prudente"), ("C", "centrale"), ("A", "ambitieuse")):
    defs = [
        ("reference (central)", lambda h: enveloppe(env, h), ""),
        ("1. elasticites fortes des assiettes mobiles", lambda h: mob(env, h), "capital/patrimoine/successions a 26 % (Jakobsen via CAE) ; IS a 55 % (IAG/IPP)"),
        ("2. rendement inferieur de moitie", lambda h: 0.5 * enveloppe(env, h), "toutes mesures x 0,5"),
        ("3. exil (marge extensive seule)", lambda h: exil(env, h), "20 centimes par euro sur les mesures de capital"),
        ("4. effet recessif fort (m = 1,0)", lambda h: enveloppe(env, h) * ((1 - SEMI) if h == 2027 else 1), "semi-elasticite 0,57 ; dissipe en 2030"),
        ("5. plafond d'acceptation", lambda h: enveloppe(env, h, filt=lambda x: not x["conteste"]), "exclut 001, 007, 009, 010 (retires le 4/11/2026 ou rejetes au PLFSS 2026)"),
        ("6. temporaires non reconduites", lambda h: enveloppe(env, h, filt=lambda x: not x["temporaire"]) - SURT, "surtaxe IS non perennisee ; OC et desherence eteintes"),
        ("7. cumul 2 + 4 + 5", lambda h: enveloppe(env, h, factor=0.5, filt=lambda x: not x["conteste"]) * ((1 - SEMI) if h == 2027 else 1), "scenario defavorable combine"),
    ]
    for nom, fn, note in defs:
        tests.append({"enveloppe": lab, "test": nom, "net_2027": round(fn(2027), 1), "net_2030": round(fn(2030), 1), "note": note})
# Sensibilite : impot plancher (021) ajoute a l'ambitieuse, et desindexation (017) selon la croissance du SMIC
x21 = [x for x in M if x["id"] == "P-A14-021"][0]
for h in (2030, 2035):
    tests.append({"enveloppe": "ambitieuse + 021 (conditionnel)", "test": "sensibilite", "net_2027": "", "net_2030": round(enveloppe("A", h) + net_val(x21, h), 1), "note": f"horizon {h}"})
x17 = [x for x in M if x["id"] == "P-A14-017"][0]
for g in (1.5, 2.41, 3.5):
    tests.append({"enveloppe": "P-A14-017 seule", "test": f"SMIC +{g} %/an", "net_2027": "", "net_2030": round(net_val(x17, 2030) * g / 2.41, 1), "note": "rendement proportionnel a la hausse du SMIC (Cour : +2,41 % = +2,2 Md)"})
with open(os.path.join(OUT, "A14_tests_adverses.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(tests[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(tests)

print("EMPLOI_ALLEG=", round(EMPLOI_ALLEG, 3), "IS_PARTIEL=", round(IS_PARTIEL, 3))
for o in out: print(o)
for t in tests: print(t)
for c in cov: print(c)
