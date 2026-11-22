# -*- coding: utf-8 -*-
"""D07 - Table de bilan des politiques d'emploi et conversion des montants en % du PIB.

Toutes les valeurs saisies ci-dessous ont ete lues dans les pieces conservees sous
../../donnees/D07/sources/ (page et marque indiquees). Le script :
  - convertit chaque montant annuel en % du PIB de l'annee (PIB Insee base 2020, A04) ;
  - calcule un cout BRUT par emploi seulement quand la piece donne le cout et le nombre d'emplois
    pour le meme champ et la meme annee (sinon : vide, motif dans 'desaccords') ;
  - ecrit D07_politiques_emploi.csv et D07_montants_pct_pib.csv.
Convention de page : page imprimee du document ; 'PDF n' quand le document n'a pas de numero imprime.
"""
import csv
import os

def _racine_depot(depart):
    """Remonte depuis `depart` jusqu'au dossier qui contient la première enquête (indépendant de l'emplacement)."""
    p = os.path.abspath(depart)
    while True:
        if os.path.isdir(os.path.join(p, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "commun")):
            return p
        q = os.path.dirname(p)
        if q == p:
            raise SystemExit("racine du dépôt introuvable depuis " + depart)
        p = q


ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07'))
PIB_F = os.path.normpath(os.path.join(_racine_depot(ICI), 'Le_Constat_Cellule_Enquete',
                                      'resultats', 'donnees', 'A04', 'a04_po_recettes_1959_2025.csv'))
pib = {}
with open(PIB_F, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        pib[int(r['annee'])] = float(r['PIB_implicite_Md_EUR'])

# (politique, periode, cout Md EUR, unite, annee, bas, haut, methode, identification, cout_net_par_emploi_lu,
#  source, page, marque, desaccords, calculer_ratio)
L = [
    ("Allegements generaux bas salaires, vague 1 (Balladur-Juppe)", "1993-1997", round(38 / 6.55957, 3), "Md EUR (38 Md F courants en 1996, brut)", 1996,
     "70000 (peu qualifies seulement, Jamet)", 460000, "Donnees d'entreprises (BRN, DADS), comparaison selon l'intensite de la baisse de cout ex ante ; Crepon-Desplatz 2001 = 460 000 crees ou sauvegardes 1994-1997 (lu) ; Jamet 2005 = 70 000-180 000 ; Gafsi-L'Horty-Mihoubi 2005 = 118 000-140 000 peu qualifies (et -41 000 a -76 000 qualifies) (via revue)",
     "quasi-experience", "", "Crepon-Desplatz, Economie et statistique n° 348, 2001 ; Bozio-Wasmer, rapport France Strategie, oct. 2024 (revue)", "ES p. 3-4 ; BW p. 89", "[C] Crepon-Desplatz et revue ; Jamet, Gafsi et al. [S] via revue",
     "Ecart 70 000 a 460 000 : champ (peu qualifies seuls ou tous), prise en compte ou non du financement (critique principale de Crepon-Desplatz), specification ; Cahuc-Carcillo 2012 : 400 000 a 1 million sauvegardes 1993-1998. Ratio = cout annuel 1996 (tout le dispositif) / 460 000 emplois identifies sur les extensions 1995-1996, hors effet du financement : ordre de grandeur seulement.", True),
    ("Allegements Juppe (cout cite)", "1996-2002", 6.5, "Md EUR courants (brut, ensemble des APU via compensation)", "",
     None, None, "Montant cite en audition (E. Heyer, OFCE)", "declaration", "", "Rapport AN n° 2436 (Romagnan), 2014", "p. 87", "[C] (citation d'audition)",
     "Annee non precisee dans la piece : pas de conversion en % du PIB.", False),
    ("Allegements Fillon (unification 2003-2005)", "2003-2005", 15.9, "Md EUR courants, allegements generaux totaux 2003 (brut)", 2003,
     None, None, "Aucune estimation d'emplois chiffree lue ; Bunel-L'Horty 2012 citee sans chiffre", "sans evaluation chiffree lue", "",
     "Rapport AN n° 2436 (chiffre de H. Novelli) ; Bozio-Wasmer 2024 p. 90", "p. 106", "[C]",
     "Effet emploi de la vague 2003-2005 non etabli sur les pieces lues.", False),
    ("Bandeaux maladie et famille (CICE bascule 2019, Pacte 2015)", "2015-2023", 34.68, "Md EUR courants 2023 (25,36 maladie + 9,32 famille, brut, statique)", 2023,
     None, None, "Aucune evaluation ex post de l'emploi lue ; Malgouyres 2019 : aucun effet sur les exportations du bandeau famille", "sans evaluation chiffree lue (emploi)", "",
     "Bozio-Wasmer 2024, tableau 1.1 et p. 120", "p. 68 ; p. 120", "[C]",
     "Pour le CICE, prolonge par le bandeau maladie, voir ligne CICE.", False),
    ("Ensemble des exonerations generales", "2023", 74.90, "Md EUR courants 2023, cout statique (brut)", 2023,
     -1000000, -980000, "SIMULATION de suppression totale : -980 000 ETP (elasticites du rapport) ; -1,0 M ETP (Mesange, Tresor). Solde primaire APU +1,7 pt de PIB a 1 an, -0,1 pt a long terme",
     "modele", "", "Bozio-Wasmer 2024, encadre 1.1", "p. 66-69", "[C]",
     "Ce n'est pas un effet mesure : simulation. Recette nette statique de la suppression estimee a 48 Md EUR avant effets macro (67 - 19).", False),
    ("35 heures (lois Aubry I et II)", "1998-2002", 10.5, "Md EUR courants 2002, allegements Aubry (brut)", 2002,
     "non significatif (Chemin-Wasmer, Alsace-Moselle)", 350000, "Etudes Dares sur entreprises passees aux 35 h (Robien, Aubry I) comparees aux restees a 39 h ; Crepon-Leclair-Roux 2004 : effet net ~5 % dans les entreprises Aubry II ; OFCE : 320 000-350 000",
     "quasi-experience (selection contestee)", 8000, "Rapport AN n° 2436 (Romagnan), 2014", "p. 82-85 ; p. 111-113", "[C] (auditions)",
     "Chemin-Wasmer 2009 (Alsace-Moselle, doubles differences) : aucun ecart d'emploi significatif [S, resume]. Biais de selection des entreprises volontaires (p. 83-84). Cout net 2,5 Md EUR et 8 000 EUR/emploi = SIMULATION OFCE. Cout brut 1re phase ~20 000 EUR/emploi selon le rapport Bur 2008 cite p. 113 (6 Md EUR / 300 000). OFCE : baisse de charges inconditionnelle de meme cout = 124 000 emplois (SIMULATION, p. 112).", True),
    ("35 heures dans les fonctions publiques d'Etat et hospitaliere", "2002-2005", 2.548, "Md EUR courants, cumul 2002-2005 (brut ; postes et mesures categorielles)", "",
     53143, 53143, "Chiffrage direction du Budget : emplois crees (dont 45 000 FPH non medicaux)", "declaration (chiffrage administratif)", "",
     "Rapport AN n° 2436, tableau", "p. 115", "[C]",
     "Ordres de grandeur selon la piece ; comptes epargne-temps (1,364 Md EUR) en sus, probablement surestimes. Ne pas confondre avec le cout net 2,5 Md EUR de la p. 111.", False),
    ("CICE", "2013-2018", 18.510, "Md EUR courants, creances 2016 (brut)", 2016,
     "non significatif (LIEPP)", 100000, "Micro-econometrie TEPP (doubles/triples differences selon l'intensite) : ~100 000 emplois, effet seulement dans le quart le plus beneficiaire ; LIEPP : effet non significatif",
     "quasi-experience", "", "France Strategie, Evaluation du CICE, sept. 2020", "p. 6 ; p. 20 ; tableau 1 p. 10", "[C]",
     "LIEPP (non significatif) contre TEPP (~100 000) : meme source fiscale, specifications differentes. OFCE macro-sectoriel : 150 000-200 000 direct, 400 000 non finance, 160 000 finance (MODELE).", True),
    ("Contrats aides secteur marchand (CIE, CI-RMA)", "2005-2007 (entrees)", None, "", "",
     None, None, "Appariement, Panel 2008 Dares : +23 points d'emploi non aide a 2,5 ans (CIE), +17 (CI-RMA)",
     "quasi-experience (appariement)", "", "Benoteau, Economie et statistique n° 477, 2015", "p. 103-104", "[C]",
     "Effet individuel : ne mesure ni l'aubaine ni la substitution (p. 104). Ne donne pas d'emplois nets.", False),
    ("Contrats aides secteur non marchand (CAE, CAV)", "2005-2007 (entrees)", None, "", "",
     None, None, "Appariement, Panel 2008 : -5 points (CAE), -12 points (CAV) d'emploi non aide a 2,5 ans",
     "quasi-experience (appariement)", "", "Benoteau, Economie et statistique n° 477, 2015", "p. 108", "[C]",
     "Toutes politiques de contrats aides : plus de 25 Md EUR sur 2005-2010 (~0,22 pt de PIB par an selon la piece, p. 86).", False),
    ("Apprentissage depuis 2018 (aide exceptionnelle 2020-2022)", "2018-2025", 14.9, "Md EUR courants 2023 (Tresor : CFA + aides + exonerations salariales)", 2023,
     120000, 252000, "Inference comptable et par elasticite (Coquet, OFCE) : 252 000 emplois d'apprentis 'n'auraient pas existe' sans l'aide ; 120 000 avec une elasticite de 0,7",
     "modele / decomposition comptable", "", "Tresor-Eco n° 376, nov. 2025 ; OFCE Policy brief n° 135, sept. 2024", "Tresor p. 5 ; OFCE p. 1, 6-7", "[C]",
     "Cout 2023 : 14,9 Md EUR (Tresor) contre 24,9 Md EUR (OFCE, qui ajoute exonerations sociales et fiscales y compris allegements generaux et depenses d'assurance chomage). Aucune evaluation quasi experimentale lue ; IGAS-IGF 2024 (p. 6, 22) : les primes 'ont pu induire des effets d'aubaine' (qualitatif). Insertion : comparaisons descriptives selon le Tresor (p. 9).", False),
    ("Apprentissage (cout OFCE)", "2023-2025", 24.9, "Md EUR courants 2023 (perimetre OFCE elargi)", 2023,
     None, None, "Chiffrage de perimetre", "", "", "OFCE Policy brief n° 135 ; n° 157 (24,1 en 2024 ; 22,2 en 2025)", "p. 11 ; n° 157 p. 1", "[C]",
     "Perimetre different du Tresor : ne pas additionner.", False),
    ("Assurance chomage 2019-2021 : salaire journalier de reference", "2021-", 1.0, "Md EUR/an, economie EX ANTE mecanique (Unedic)", 2021,
     None, None, "Evaluations sur donnees administratives : une baisse de 10 % du SJR reduit de 1,4 a 5 % la duree sans emploi ; effet porte par des contrats de moins de 6 mois",
     "quasi-experience", "", "Rapport du comite d'evaluation (Dares), avr. 2025", "p. 1-2 ; p. 16-17", "[C]",
     "Effet sur l'emploi total non mesure. Economies constatees non publiees : seulement chiffrage ex ante hors comportements.", False),
    ("Assurance chomage 2019-2021 : condition d'affiliation 4 a 6 mois", "2021-", 0.8, "Md EUR/an, economie EX ANTE mecanique", 2021,
     None, None, "Reprise d'emploi stimulee, pour moitie emploi durable", "quasi-experience", "", "Rapport du comite d'evaluation (Dares), avr. 2025", "p. 1 ; p. 16-17", "[C]",
     "Moindre inscription a France Travail. Effet emploi total non mesure.", False),
    ("Assurance chomage 2019-2021 : degressivite hauts revenus", "2021-", 0.46, "Md EUR/an, economie EX ANTE mecanique", 2021,
     None, None, "Duree indemnisee -2 mois environ, non-emploi salarie -1,5 mois (taux de 30 %)", "quasi-experience", "", "Rapport du comite d'evaluation (Dares), avr. 2025 ; synthese Unedic mars 2025", "p. 1-2 ; Unedic p. 6", "[C]",
     "3 % des allocataires. Unedic : -24 jours de non-emploi en moyenne.", False),
    ("Assurance chomage 2019-2021 : bonus-malus", "2022-", 0.0, "neutre par construction", 2022,
     0, 0, "Taux de separation -2,5 points ; aucun effet mesurable sur l'emploi des entreprises", "quasi-experience", "", "Rapport du comite d'evaluation (Dares), avr. 2025", "p. 2 ; p. 67", "[C]", "", False),
    ("Assurance chomage 2023 : contracyclicite (-25 % de duree)", "2023-", 4.5, "Md EUR/an a l'horizon 2027, economie EX ANTE (Unedic)", 2027,
     None, None, "Suivi descriptif : duree potentielle -20 %, duree indemnisee -14 % (moins de 53 ans), fins de droit de 41 000 a 70 000 entre mars 2023 et mars 2025 (periodicite non precisee dans la synthese) ; effet sur la reprise d'emploi non encore evalue",
     "sans evaluation causale accessible", "", "Unedic, Reforme 2023 : premiers effets, dec. 2025", "p. 1-2", "[C]",
     "CAE n° 90 (2026) SUPPOSE, d'apres la litterature, -2,7 % de duree de chomage pour -10 % de duree d'indemnisation : hypothese, pas mesure francaise.", False),
    ("Contribution Delalande (licenciement des salaries ages)", "1987-2008", None, "", "",
     None, None, "Exoneration en 1992 des embauches apres 50 ans : amelioration relative du retour a l'emploi des chomeurs de plus de 50 ans ; effet sur les licenciements faible ou difficile a mettre en evidence",
     "quasi-experience (changement de bareme)", "", "Behaghel, Crepon, Sedillot, Economie et statistique n° 372, 2004", "p. 61 (resume)", "[C] resume ; texte complet non lu",
     "Ampleur chiffree non lue (PDF Persee non accessible). Date de suppression (2008) non verifiee sur piece.", False),
    ("Preretraites (garantie de ressources, FNE...)", "1972-2011", 56.2, "Md F courants 1985 (rubrique B, constate)", 1985,
     None, None, "Aucune evaluation causale de l'effet sur l'emploi des jeunes lue", "sans evaluation chiffree lue", "",
     "S10 (premiere enquete) d'apres SES 1986", "S10 §11", "[S] (S10)",
     "Montant en francs : converti en euros dans D07_montants_pct_pib.csv.", False),
]

with open(os.path.join(OUT, 'D07_politiques_emploi.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['politique', 'periode', 'cout_public_annuel', 'unite', 'annee', 'emplois_estimes_bas', 'emplois_estimes_haut',
                'methode', 'identification', 'cout_brut_par_emploi', 'cout_net_par_emploi', 'source', 'page', 'marque', 'desaccords'])
    for (pol, per, cout, unite, an, bas, haut, meth, ident, net, src, page, marque, des, ratio) in L:
        brut = ''
        if ratio and cout and haut:
            # calcul D07 : cout brut annuel / estimation HAUTE d'emplois -> EUR par emploi et par an.
            # L'estimation basse etant nulle ou non significative (ou d'un autre champ), aucun ratio bas.
            b1 = round(cout * 1e9 / haut)
            brut = f"{b1} EUR pour l'estimation haute seulement (calcul D07, brut statique)"
        w.writerow([pol, per, cout if cout is not None else '', unite, an, bas if bas is not None else '',
                    haut if haut is not None else '', meth, ident, brut, net, src, page, marque, des])

# Montants en % du PIB
M = [
    ("Allegements bas salaires (Crepon-Desplatz)", 1993, 4.0, 'FRF'),
    ("Allegements bas salaires (Crepon-Desplatz)", 1996, 38.0, 'FRF'),
    ("Exonerations generales (total)", 2023, 74.90, 'EUR'),
    ("Exonerations generales (total)", 2019, 57.74, 'EUR'),
    ("Reduction generale bas salaires", 2023, 40.21, 'EUR'),
    ("CICE creances", 2013, 11.820, 'EUR'),
    ("CICE creances", 2016, 18.510, 'EUR'),
    ("CICE creances", 2017, 22.152, 'EUR'),
    ("Allegements Aubry", 2002, 10.5, 'EUR'),
    ("Allegements generaux totaux", 2003, 15.9, 'EUR'),
    ("Surcout 35 h des allegements (direction du Budget)", 2013, 12.8, 'EUR'),
    ("Apprentissage (Tresor)", 2023, 14.9, 'EUR'),
    ("Apprentissage (Tresor)", 2018, 6.1, 'EUR'),
    ("Apprentissage (OFCE)", 2023, 24.9, 'EUR'),
    ("Apprentissage (OFCE)", 2024, 24.1, 'EUR'),
    ("Apprentissage (OFCE)", 2025, 22.2, 'EUR'),
    ("Allocation d'aide au retour a l'emploi (ARE)", 2023, 31.0, 'EUR'),
    ("Economie ex ante AC 2019-2021 (3 mesures)", 2023, 2.26, 'EUR'),
    ("Economie ex ante AC 2023", 2025, 4.5, 'EUR'),
    ("Preretraites rubrique B (S10)", 1985, 56.2, 'FRF'),
]
with open(os.path.join(OUT, 'D07_montants_pct_pib.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['poste', 'annee', 'montant_Md', 'devise', 'montant_Md_EUR', 'pib_Md_EUR', 'pct_PIB', 'note'])
    for poste, an, m, dev in M:
        eur = m / 6.55957 if dev == 'FRF' else m
        note = 'ex ante, annee de PIB 2025 conventionnelle (horizon 2027)' if 'AC 2023' in poste else (
            'ex ante, rapporte au PIB 2023 par convention' if 'ex ante' in poste else '')
        w.writerow([poste, an, m, dev, round(eur, 3), pib[an], round(eur / pib[an] * 100, 2), note])
print('ok')
