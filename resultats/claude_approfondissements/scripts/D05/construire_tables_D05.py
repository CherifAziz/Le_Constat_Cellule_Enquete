# -*- coding: utf-8 -*-
"""D05 - construit les tables de la mission D05 à partir des transcriptions de pièces conservées.

Entrées :
  - les relevés transcrits ci-dessous (chaque ligne renvoie à une pièce de ../../donnees/D05/sources/
    ou à une pièce déjà conservée par la première enquête, avec page et citation) ;
  - le PIB base 2020 de l'Insee : Le_Constat_Cellule_Enquete/resultats/donnees/A04/a04_po_recettes_1959_2025.csv
Sorties (../../donnees/D05/) :
  - D05_mesures_nouvelles_annuelles.csv  (une ligne par année x source x millésime)
  - D05_cumuls_par_segment.csv           (sommes à l'intérieur d'un segment homogène seulement)
  - D05_chiffrages_cumules.csv
  - D05_grandes_decisions.csv
Règles : aucun cumul à travers une rupture de segment ; aucune addition entre conventions.
Lancer : python -I construire_tables_D05.py
"""
import csv, os

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
SORTIE = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D05'))
PIB_CSV = os.path.normpath(os.path.join(_racine_depot(ICI),
                           'Le_Constat_Cellule_Enquete', 'resultats', 'donnees', 'A04',
                           'a04_po_recettes_1959_2025.csv'))
F_PAR_EUR = 6.55957

PIB = {}
with open(PIB_CSV, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        PIB[int(r['annee'])] = float(r['PIB_implicite_Md_EUR'])

# ---------------------------------------------------------------------------
# 1. Série annuelle des mesures nouvelles (relevés)
# Conventions :
#  A = contribution des mesures nouvelles à l'évolution des prélèvements obligatoires, toutes
#      administrations (DG Trésor, fiche PO du RESF ; Insee Première d'après la DG Trésor) ;
#      inclut les mesures temporaires et les contrecoups (plan de relance, surtaxes).
#  B = mesures nouvelles en PO dans la décomposition de l'effort structurel (DG Trésor) ;
#      en point de PIB ou de PIB potentiel ; à partir de 2017 « nettes des crédits d'impôt et hors one-offs ».
#  C = chiffrage de la Cour des comptes (composantes données séparément).
# statut : constatation (année écoulée), estimation (année en cours, automne), prevision.
# ---------------------------------------------------------------------------
COLS = ['annee', 'convention', 'statut', 'millesime', 'source', 'page', 'mesures_Md_EUR',
        'mesures_pts_PIB_source', 'unite_pts', 'mesures_pts_PIB_base2020', 'evol_spontanee_PO',
        'elasticite_PO_PIB', 'perimetre', 'traitement_temporaires_CI', 'citation', 'marque',
        'segment', 'retenu', 'note']

GS = 'DG Trésor, Cahiers de la DGTPE n°2009-13 (Guyon, Sorbe), tableau 3 ; sources/dgtresor_DT2009-13_Guyon_Sorbe.pdf'
SEN07 = 'Sénat, rapport d\'information n°60 (2007-2008) Marini, tome II, tableau 4 (source : ministère) ; sources/senat_r07-060-21.pdf'
def resf(n, fich):
    return 'RESF annexé au PLF %d ; sources/%s' % (n, fich)

L = []
def obs(**k):
    row = {c: '' for c in COLS}
    row.update({a: ('' if b is None else b) for a, b in k.items()})
    L.append(row)

# --- Segment S1 : 2000-2008, convention B, DG Trésor 2009 (constatations, 2008 provisoire)
gs = {2000: -1.2, 2001: -1.0, 2002: -0.4, 2003: 0.1, 2004: 0.1, 2005: 0.4, 2006: 0.1, 2007: -0.6, 2008: -0.5}
for a, v in gs.items():
    obs(annee=a, convention='B', statut='constatation' if a < 2008 else 'constatation provisoire',
        millesime='2009-12', source=GS, page='p. 15 du document (p. 18 du PDF)', mesures_pts_PIB_source=v,
        unite_pts='point de PIB', perimetre='ensemble des administrations publiques',
        traitement_temporaires_CI='hors soultes ; mesures temporaires non isolées',
        citation='« dont mesures nouvelles en PO » (ligne du tableau 3)', marque='[C] lecture du tableau sur image de page',
        segment='S1_2000_2008_DGTresor_2009', retenu='oui')
# Recouvrement : Sénat 2007 (DG Trésor, octobre 2007)
sen = {2002: (-0.4, 'constatation'), 2003: (0.1, 'constatation'), 2004: (0.0, 'constatation'),
       2005: (0.4, 'constatation'), 2006: (0.1, 'constatation'), 2007: (-0.7, 'prevision'), 2008: (-0.4, 'prevision')}
for a, (v, s) in sen.items():
    obs(annee=a, convention='A', statut=s, millesime='2007-10', source=SEN07, page='p. 10', mesures_pts_PIB_source=v,
        unite_pts='point de PIB', perimetre='ensemble des administrations publiques (ligne Total)',
        citation='« Montant des mesures nouvelles en point de PIB sur les prélèvements obligatoires »',
        marque='[C] lecture du tableau sur image de page', segment='recouvrement', retenu='non')
# Estimations d'automne du RESF
obs(annee=2007, convention='A', statut='estimation', millesime='2007-09', source=resf(2008, 'RESF_PLF2008_vp194000311.pdf'),
    page='p. 67', mesures_pts_PIB_source=-0.7, unite_pts='point de PIB', perimetre='APU',
    citation='« Contribution des mesures nouvelles » -0,7 (colonne APU)', marque='[C]', segment='recouvrement', retenu='non',
    note='État -0,6 point soit 11,4 Md€ (p. 66)')
obs(annee=2008, convention='A', statut='estimation', millesime='2008-09', source=resf(2009, 'RESF_PLF2009_vp194000312.pdf'),
    page='p. 54', mesures_pts_PIB_source=-0.5, unite_pts='point de PIB', perimetre='APU',
    citation='« Contribution des mesures nouvelles » -0,5 (colonne APU)', marque='[C]', segment='recouvrement', retenu='non')

# --- Segment S2 : 2009-2011, sources hétérogènes (rupture)
obs(annee=2009, convention='A', statut='estimation', millesime='2009-09', source=resf(2010, 'RESF_PLF2010_tI_vp194000313.pdf'),
    page='p. 65', mesures_pts_PIB_source=-0.8, unite_pts='point de PIB', perimetre='APU',
    citation='« Contribution des mesures nouvelles » -0,8 (colonne APU)', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2009, convention='C', statut='constatation', millesime='2010-06',
    source='Cour des comptes, RSPFP juin 2010 ; sources/cour_RSPFP_juin2010_vp104000325.pdf',
    page='p. 10-11 du rapport (p. 14-15 du PDF)', mesures_Md_EUR=-15.4,
    perimetre='APU : relance fiscale -13 Md€ (temporaire) + mesures pérennes nettes -2,4 Md€',
    traitement_temporaires_CI='inclut le plan de relance (temporaire)',
    citation='« Le volet fiscal du plan de relance y a contribué pour 13 Md€ »',
    marque='[C] somme D05 de deux composantes du même document', segment='S2_2009_2011_heterogene', retenu='oui',
    note='Pérennes : « augmenter le déficit public de 2,4 Md€ » (APU) ; État+ASSO : -4,6 Md€')
obs(annee=2009, convention='A', statut='constatation provisoire', millesime='2010-09', source=resf(2011, 'RESF_PLF2011_tI_vp194000314.pdf'),
    page='p. 78', evol_spontanee_PO='-3,3 %', elasticite_PO_PIB=1.6, perimetre='APU',
    citation='« Évolution effective des PO - 5,1 % » ; « Évolution spontanée des PO - 3,3 % »',
    marque='[C]', segment='recouvrement', retenu='non',
    note='mesures implicites ≈ -1,8 % du produit 2008 des PO (écart effectif - spontané), calcul D05 non retenu')
obs(annee=2010, convention='A', statut='estimation', millesime='2010-09', source=resf(2011, 'RESF_PLF2011_tI_vp194000314.pdf'),
    page='p. 78', mesures_pts_PIB_source=0.1, unite_pts='point de PIB', evol_spontanee_PO='+2,9 %', elasticite_PO_PIB=1.3,
    perimetre='APU', traitement_temporaires_CI='y compris réforme de la taxe professionnelle (surcoût 2010 temporaire) et contrecoup du plan de relance',
    citation='« Contribution des mesures nouvelles (y.c. réforme TP) » 0,1 (APU)', marque='[C]',
    segment='S2_2009_2011_heterogene', retenu='oui', note='aucune constatation en convention A retrouvée pour 2010')
obs(annee=2010, convention='B', statut='constatation', millesime='2011-06',
    source='Cour des comptes, RSPFP juin 2011 ; sources/cour_RSPFP_juin2011_vp114000338.pdf', page='p. 28 du PDF (p. 31 du rapport)',
    mesures_pts_PIB_source=-0.4, unite_pts='point de PIB', perimetre='APU',
    traitement_temporaires_CI='hors plan de relance ; coût 2010 de la réforme TP compté en totalité',
    citation='« réduits par des mesures nouvelles (hors plan de relance) »', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2011, convention='A', statut='estimation', millesime='2011-09', source=resf(2012, 'RESF_PLF2012_vp194000315.pdf'),
    page='p. 67-68', mesures_Md_EUR=19.2, mesures_pts_PIB_source=1.0, unite_pts='point de PIB', evol_spontanee_PO='+3,8 %', elasticite_PO_PIB=1.2,
    perimetre='APU', citation='« les mesures nouvelles contribueraient à hauteur de 19,2 Md€ »', marque='[C]',
    segment='S2_2009_2011_heterogene', retenu='oui')
obs(annee=2011, convention='B', statut='constatation provisoire', millesime='2012-09', source=resf(2013, 'RESF_PLF2013_vp194000316.pdf'),
    page='p. 64', mesures_pts_PIB_source=1.0, unite_pts='point de PIB potentiel', perimetre='APU',
    citation='« mesures nouvelles en prélèvements obligatoires 1,0 »', marque='[C]', segment='recouvrement', retenu='non')

# --- Segment S3 : 2012-2016, convention A, RESF « retour sur l'année N-2 » (constatations)
obs(annee=2012, convention='A', statut='estimation', millesime='2012-09', source=resf(2013, 'RESF_PLF2013_vp194000316.pdf'),
    page='p. 71-72', mesures_Md_EUR=20.1, mesures_pts_PIB_source=1.0, unite_pts='point de PIB', perimetre='APU',
    citation='« les mesures nouvelles contribueraient à hauteur de 20,1 Md€ »', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2012, convention='A', statut='constatation', millesime='2013-09', source=resf(2014, 'RESF_PLF2014_vp194000317.pdf'),
    page='p. 66', mesures_pts_PIB_source=1.1, unite_pts='point de PIB', evol_spontanee_PO='+0,1 point de PIB', perimetre='APU',
    citation='« l\'ensemble des mesures nouvelles fiscales et sociales, à hauteur de 1,1 point »', marque='[C]',
    segment='S3_2012_2016_RESF', retenu='oui', note='État 0,7 point ; ASSO 0,4 point')
obs(annee=2012, convention='B', statut='constatation', millesime='2013-09', source=resf(2014, 'RESF_PLF2014_vp194000317.pdf'),
    page='p. 69', mesures_pts_PIB_source=1.2, unite_pts='point de PIB potentiel', perimetre='APU',
    citation='« dont mesures nouvelles en recettes » 1,2', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2013, convention='A', statut='constatation', millesime='2014-10', source=resf(2015, 'RESF_PLF2015_vp194000031.pdf'),
    page='p. 58', mesures_Md_EUR=30.0, mesures_pts_PIB_source=1.4, unite_pts='point de PIB', evol_spontanee_PO='+0,2 %', elasticite_PO_PIB=0.2,
    perimetre='APU', citation='« Les mesures nouvelles se sont élevées à près de 30 Md€ »', marque='[C]',
    segment='S3_2012_2016_RESF', retenu='oui', note='montant en Md€ arrondi par la source (« près de »)')
obs(annee=2013, convention='A', statut='constatation', millesime='2014-05', source='Insee Première n°1500 ; sources/insee_ip1500_APU2013.pdf',
    page='p. 2', mesures_pts_PIB_source=1.4, unite_pts='point de PIB', perimetre='APU',
    citation='« nouvelles mesures fiscales et sociales (+ 1,4 point de PIB) »', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2013, convention='B', statut='constatation provisoire', millesime='2013-09', source=resf(2014, 'RESF_PLF2014_vp194000317.pdf'),
    page='p. 69', mesures_pts_PIB_source=1.5, unite_pts='point de PIB potentiel', perimetre='APU',
    citation='« essentiellement porté par des mesures nouvelles en prélèvements obligatoires (+ 1,5 point »', marque='[C]',
    segment='recouvrement', retenu='non')
obs(annee=2014, convention='A', statut='constatation', millesime='2015-10', source=resf(2016, 'RESF_PLF2016_vp194000026.pdf'),
    page='p. 62', mesures_Md_EUR=3.3, mesures_pts_PIB_source=0.2, unite_pts='point de PIB', evol_spontanee_PO='+0,8 %', elasticite_PO_PIB=1.1,
    perimetre='APU', citation='« Les mesures nouvelles ont joué à la hausse à hauteur de 3,3 Md€ »', marque='[C]',
    segment='S3_2012_2016_RESF', retenu='oui')
obs(annee=2014, convention='A', statut='constatation', millesime='2015-05', source='Insee Première n°1548 ; sources/insee_ip1548_APU2014.pdf',
    page='p. 2', mesures_pts_PIB_source=0.1, unite_pts='point de PIB', perimetre='APU',
    citation='« contribuent modérément à cette hausse (+ 0,1 point de PIB) »', marque='[C]', segment='recouvrement', retenu='non')
obs(annee=2015, convention='A', statut='constatation', millesime='2016-10', source=resf(2017, 'RESF_PLF2017_vp194000022.pdf'),
    page='p. 61', mesures_Md_EUR=-1.6, mesures_pts_PIB_source=-0.1, unite_pts='point de PIB', perimetre='APU',
    citation='« Ces mesures nouvelles ont représenté une baisse de - 1,6 Md€ »', marque='[C]',
    segment='S3_2012_2016_RESF', retenu='oui', note='renvoi de note 4 attaché au montant non lu')
obs(annee=2016, convention='A', statut='constatation', millesime='2017-10', source=resf(2018, 'RESF_PLF2018.pdf'),
    page='p. 77-78', mesures_Md_EUR=-3.4, mesures_pts_PIB_source=-0.2, unite_pts='point de PIB', evol_spontanee_PO='+1,9 %', elasticite_PO_PIB=1.2,
    perimetre='APU', citation='« ont contribué à faire baisser les prélèvements obligatoires de 3,4 Md€ »', marque='[C]',
    segment='S3_2012_2016_RESF', retenu='oui')
obs(annee=2016, convention='A', statut='constatation', millesime='2017-05', source='Insee Première n°1651 ; sources/insee_ip1651_APU2016.pdf',
    page='p. 1', mesures_Md_EUR=-3.9, perimetre='APU', citation='« impacté par des mesures nouvelles en 2016, à hauteur de – 3,9 milliards »',
    marque='[C]', segment='recouvrement', retenu='non', note='écart de 0,5 Md€ avec le RESF : millésimes différents')
for a, v, pg in [(2016, -0.1, 'p. 84'), (2017, -0.1, 'p. 84'), (2018, -0.3, 'p. 84')]:
    obs(annee=a, convention='B', statut='constatation' if a == 2016 else ('estimation' if a == 2017 else 'prevision'), millesime='2017-10',
        source=resf(2018, 'RESF_PLF2018.pdf'), page=pg, mesures_pts_PIB_source=v, unite_pts='point de PIB potentiel', perimetre='APU',
        traitement_temporaires_CI='nettes des crédits d\'impôt, hors one-offs',
        citation='« dont mesures nouvelles en recettes (nettes des CI) et hors one-offs »', marque='[C]', segment='recouvrement', retenu='non')

# --- Segment S4 : 2017-2025, convention A, Insee Première (chiffrage DG Trésor), constatations
obs(annee=2017, convention='A', statut='constatation', millesime='2018-05', source='Insee Première n°1698 ; sources/insee_ip1698_APU2017.pdf',
    page='p. 2', mesures_Md_EUR=3.6, perimetre='APU', traitement_temporaires_CI='inclut la surtaxe exceptionnelle d\'IS de fin 2017',
    citation='« les mesures nouvelles contribuent à hauteur de + 3,6 milliards »', marque='[C]', segment='S4_2017_2025_Insee', retenu='oui')
obs(annee=2017, convention='A', statut='constatation', millesime='2018-10', source=resf(2019, 'RESF_PLF2019.pdf'),
    page='p. 77', perimetre='APU', traitement_temporaires_CI='surtaxe IS +0,2 point ; hors surtaxe, effet négatif non chiffré',
    citation='« Hors cette mesure exceptionnelle, les mesures nouvelles ont diminué »', marque='[C]', segment='recouvrement', retenu='non')
for a, v in [(2017, -0.1), (2018, -0.2), (2019, 0.0)]:
    obs(annee=a, convention='B', statut={2017: 'constatation', 2018: 'estimation', 2019: 'prevision'}[a], millesime='2018-10',
        source=resf(2019, 'RESF_PLF2019.pdf'), page='p. 85', mesures_pts_PIB_source=v, unite_pts='point de PIB potentiel', perimetre='APU',
        traitement_temporaires_CI='nettes des crédits d\'impôt, hors one-offs',
        citation='« dont mesures nouvelles en recettes (nettes des CI) et hors one-offs »', marque='[C]', segment='recouvrement', retenu='non')
A04S = 'pièce conservée par A04 : donnees/A04/sources/insee_ip/'
insee = [(2018, -9.7, 'Insee Première n°1753', 'ip1753.pdf', 'p. 2', '« contribuent à hauteur de − 9,7 milliards d\'euros »'),
         (2019, -23.6, 'Insee Première n°1801', 'ip1801.pdf', 'p. 1', '« à hauteur de – 23,6 milliards d\'euros »'),
         (2020, 5.1, 'Insee Première n°1859', 'ip1859.pdf', 'p. 1', '« augmenter les prélèvements obligatoires de 5,1 milliards »'),
         (2021, -14.8, 'Insee Première n°1903', 'ip1903.pdf', 'p. 1', '« abaisser les prélèvements obligatoires à hauteur de 14,8 Md€ »'),
         (2022, -7.7, 'Insee Première n°1949', 'IP1949_Comptes_APU2022_V2.pdf', 'p. 1', '« contribuent, à hauteur de -7,7 Md€ »'),
         (2023, -7.1, 'Insee Première n°1998', 'IP1998_CompteAPU2023.pdf', 'p. 1-2', '« hauteur de -7,1 Md€ »'),
         (2024, 3.6, 'Insee Première n°2054', 'IP2054.pdf', 'p. 2', '« effet positif sur les prélèvements obligatoires de 2024 à hauteur de 3,6 Md€ »'),
         (2025, 23.0, 'Insee Première n°2106', 'ip2106.pdf', 'p. 1', '« de 2025 à hauteur de 23,0 Md€ »')]
for a, v, t, fich, pg, cit in insee:
    note = {2019: 'inclut le surcoût ponctuel de la bascule CICE-allègements (double avantage 2019)',
            2025: 'dont 8,0 Md€ de contributions exceptionnelles (temporaires)'}.get(a, '')
    obs(annee=a, convention='A', statut='constatation', millesime='%d-05' % (a + 1), source='%s ; %s%s' % (t, A04S, fich), page=pg,
        mesures_Md_EUR=v, perimetre='APU', citation=cit, marque='[C] (relu par D05)', segment='S4_2017_2025_Insee', retenu='oui', note=note)

# pts de PIB base 2020 recalculés
for r in L:
    if r['mesures_Md_EUR'] != '':
        r['mesures_pts_PIB_base2020'] = round(100 * float(r['mesures_Md_EUR']) / PIB[int(r['annee'])], 2)

with open(os.path.join(SORTIE, 'D05_mesures_nouvelles_annuelles.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=COLS, delimiter=';'); w.writeheader(); w.writerows(sorted(L, key=lambda r: (r['annee'], r['retenu'] != 'oui')))

# ---------------------------------------------------------------------------
# 2. Cumuls par segment (jamais à travers une rupture)
# ---------------------------------------------------------------------------
seg = {}
for r in L:
    if r['retenu'] == 'oui':
        seg.setdefault(r['segment'], []).append(r)
rows = []
for s, rr in sorted(seg.items()):
    an = sorted(int(r['annee']) for r in rr)
    conv = sorted(set(r['convention'] for r in rr))
    pts_src = [r['mesures_pts_PIB_source'] for r in rr]
    md = [r['mesures_Md_EUR'] for r in rr]
    pts_b20 = [r['mesures_pts_PIB_base2020'] for r in rr]
    rows.append({'segment': s, 'annees': '%d-%d' % (an[0], an[-1]), 'nb_annees': len(an), 'conventions': '+'.join(conv),
                 'somme_pts_PIB_source': round(sum(float(x) for x in pts_src), 2) if all(x != '' for x in pts_src) else 'non calculable (points manquants)',
                 'somme_Md_EUR_courants': round(sum(float(x) for x in md), 1) if all(x != '' for x in md) else 'non calculable (Md€ manquants)',
                 'somme_pts_PIB_base2020': round(sum(float(x) for x in pts_b20), 2) if all(x != '' for x in pts_b20) else 'non calculable',
                 'avertissement': 'somme d\'effets annuels ex ante, sans effet retour ; points de PIB de bases comptables différentes' if s.startswith('S1') else
                                  ('conventions mélangées : ne pas cumuler' if len(conv) > 1 else 'somme d\'effets annuels ex ante, sans effet retour')})
with open(os.path.join(SORTIE, 'D05_cumuls_par_segment.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';'); w.writeheader(); w.writerows(rows)

# Contrôle contre les sommes par période de Fipeco (secondaire, A04) : écarts imprimés
ret = {int(r['annee']): r for r in L if r['retenu'] == 'oui'}
def pts(a):
    r = ret[a]
    return float(r['mesures_pts_PIB_source']) if r['mesures_pts_PIB_source'] != '' else float(r['mesures_pts_PIB_base2020'])
print('Contrôles (série retenue, pts de PIB source sinon base 2020) contre Fipeco [S] :')
for (a, b, fip) in [(2003, 2006, 0.7), (2007, 2009, -2.1), (2010, 2014, 3.9), (2015, 2017, -0.2), (2000, 2002, None)]:
    s = round(sum(pts(x) for x in range(a, b + 1)), 2)
    print('  %d-%d : série D05 %+.2f ; Fipeco %s' % (a, b, s, fip))

# ---------------------------------------------------------------------------
# 3. Chiffrages publiés du coût cumulé
# ---------------------------------------------------------------------------
CC = ['id', 'document', 'date', 'page', 'montant', 'unite', 'annee_mesuree', 'periode_des_decisions', 'perimetre',
      'convention', 'brut_ou_net', 'effet_sur_activite', 'contrefactuel_solde_dette', 'citation', 'marque', 'niveau']
C = [
 dict(id='CC01', document='AN, rapport d\'information n°2689, Carrez (juin 2010) ; pièce A04 AN_rapinfo_i2689_Carrez_2010.pdf', date='2010-06-30',
      page='p. 7', montant='101,2 à 119,3 (5,3 à 6,2 % du PIB)', unite='Md€ courants', annee_mesuree='2009', periode_des_decisions='2000-2009',
      perimetre='recettes fiscales nettes du budget général de l\'État', convention='mesures nouvelles (environ 2/3) + transferts de recettes aux autres administrations (environ 1/3) ; fourchettes avec ou sans vieillissement des mesures ; IS de retour compté',
      brut_ou_net='net des hausses', effet_sur_activite='aucun (comptable)', contrefactuel_solde_dette='voir CC03',
      citation='« entre 101,2 – 5,3 % de PIB – et 119,3 milliards d\'euros »', marque='[C]', niveau='A (chiffrage administratif)'),
 dict(id='CC02', document='idem Carrez 2010', date='2010-06-30', page='p. 7 (tableau)', montant='68,3 à 77,7 (2009) ; 53,5 à 65,6 (2007)', unite='Md€ courants',
      annee_mesuree='2009 et 2007', periode_des_decisions='mesures publiées après le 1er janvier 2000', perimetre='budget général de l\'État, hors mesures sur PO non affectés à l\'État',
      convention='coût cumulé des mesures nouvelles ; fourchette basse = coût initial figé, haute = vieillissement comme l\'impôt ; hors relance 2009',
      brut_ou_net='net des hausses', effet_sur_activite='aucun', contrefactuel_solde_dette='',
      citation='« Coût cumulé des mesures nouvelles depuis 2000 »', marque='[C] tableau relu sur image de la p. 7 ; contrôle : 68,3 + 32,9 = 101,2 et 77,7 + 41,6 = 119,3', niveau='A'),
 dict(id='CC03', document='idem Carrez 2010', date='2010-06-30', page='p. 16', montant='déficit 3,7 % et dette 54,6 % du PIB en 2009 au lieu de 7,5 % et 77,4 %', unite='% du PIB',
      annee_mesuree='2009', periode_des_decisions='2000-2009', perimetre='baisses d\'impôts d\'État seules (hors transferts et dégrèvements)',
      convention='gage systématique des baisses ; neutralité sur le PIB', brut_ou_net='net', effet_sur_activite='supposé nul',
      contrefactuel_solde_dette='excédent 2006-2008 ; dette < 50 % du PIB en 2007-2008',
      citation='« se seraient établis à 3,7 % et 54,6 % du PIB en 2009 »', marque='[C]', niveau='D (simulation comptable)'),
 dict(id='CC04', document='idem Carrez 2010', date='2010-06-30', page='p. 6', montant='au moins 2,4 % du PIB', unite='% du PIB', annee_mesuree='2001-2002',
      periode_des_decisions='2000-2002', perimetre='ensemble des prélèvements obligatoires (État, sécurité sociale, collectivités)', convention='non précisée',
      brut_ou_net='non précisé', effet_sur_activite='non précisé', contrefactuel_solde_dette='« quasiment à l\'équilibre en 2001 »',
      citation='« une perte de ressources d\'au moins 2,4 % de PIB »', marque='[C]', niveau='D'),
 dict(id='CC05', document='Champsaur et Cotis, Rapport sur la situation des finances publiques (avril 2010) ; sources/champsaur_cotis_avril2010_vp104000234.pdf',
      date='2010-04', page='p. 18 du PDF', montant='près de 3', unite='points de PIB', annee_mesuree='2008', periode_des_decisions='1999-2008',
      perimetre='ensemble des prélèvements obligatoires (APU)', convention='somme des mesures nouvelles ; taux de PO à législation 1999 = 45,3 % en 2008',
      brut_ou_net='net (ensemble des mesures)', effet_sur_activite='non (comptable)',
      contrefactuel_solde_dette='dépense hors intérêts plus faible de 0,4 % par an nécessaire pour compenser',
      citation='« ont ainsi réduit les recettes publiques de près de 3 points de PIB »', marque='[C]', niveau='A/D'),
 dict(id='CC06', document='idem Champsaur et Cotis, graphique 20 intitulé (1997-2008), source DG Trésor DT 2009/13', date='2010-04', page='p. 30 du PDF', montant='-2,8', unite='points de PIB',
      annee_mesuree='2008', periode_des_decisions='1999-2008 (solde structurel 1999 à 2008)', perimetre='APU',
      convention='décomposition de la variation du solde structurel (effort structurel)', brut_ou_net='net', effet_sur_activite='non',
      contrefactuel_solde_dette='solde structurel -2,1 % (1999) → -3,1 % (2008) ; effort en dépense +0,9 point',
      citation='« Mesures nouvelles en prélèvements obigatoires : - 2,8 points »', marque='[C]', niveau='A'),
 dict(id='CC07', document='Cour des comptes, RSPFP juin 2011 ; sources/cour_RSPFP_juin2011_vp114000338.pdf', date='2011-06', page='p. 27 du PDF',
      montant='2,8', unite='points de PIB', annee_mesuree='2007', periode_des_decisions='1997-2007', perimetre='prélèvements obligatoires (APU)',
      convention='non précisée dans le passage', brut_ou_net='non précisé', effet_sur_activite='non précisé', contrefactuel_solde_dette='',
      citation='« baisses des prélèvements obligatoires qui ont représenté 2,8 points de PIB »', marque='[C]', niveau='A'),
 dict(id='CC08', document='Cour des comptes, RSPFP juin 2010 ; sources/cour_RSPFP_juin2010_vp104000325.pdf', date='2010-06', page='p. 10-11 du rapport',
      montant='4,6 (État et ASSO) ; 2,4 (APU, net des hausses locales) ; relance 13 (temporaire)', unite='Md€ courants', annee_mesuree='2009',
      periode_des_decisions='2009', perimetre='voir montant', convention='coût net des mesures pérennes de baisse', brut_ou_net='net',
      effet_sur_activite='non', contrefactuel_solde_dette='', citation='« Le coût net des mesures pérennes de baisse des prélèvements obligatoires »',
      marque='[C]', niveau='A'),
 dict(id='CC09', document='Cour des comptes, RSPFP juillet 2024 ; pièce A04 cour_RSPFP_juillet2024_vp294882.pdf', date='2024-07', page='p. 35 du PDF',
      montant='62 (2,2 points de PIB)', unite='Md€ courants', annee_mesuree='2023', periode_des_decisions='2018-2023', perimetre='non précisé (baisses d\'impôts et de cotisations)',
      convention='méthode non publiée', brut_ou_net='non précisé', effet_sur_activite='non précisé', contrefactuel_solde_dette='',
      citation='« dont l\'impact est estimé à 62 Md€ en 2023, soit 2,2 pts de PIB »', marque='[C]', niveau='A'),
 dict(id='CC10', document='Cour des comptes, fiscalité locale, janvier 2025 ; pièce A04 cour_fiscalite_locale_jan2025_vp296927.pdf', date='2025-01', page='p. 67 du PDF',
      montant='moitié de la hausse du déficit 2017-2023 ; un tiers 2018-2023', unite='part de la hausse du déficit', annee_mesuree='2023',
      periode_des_decisions='2017-2023 (fiscalité locale et audiovisuel public)', perimetre='APU', convention='toutes choses égales par ailleurs',
      brut_ou_net='net des compensations', effet_sur_activite='non', contrefactuel_solde_dette='',
      citation='« à l\'origine de la moitié de la hausse du déficit »', marque='[C]', niveau='A/D'),
 dict(id='CC11', document='idem Cour janvier 2025', date='2025-01', page='p. 8 du PDF', montant='près de 19 (ménages, TH) ; au moins 19 (entreprises, impôts locaux de production)',
      unite='Md€ courants', annee_mesuree='2023', periode_des_decisions='2018-2023', perimetre='impôts locaux', convention='législation inchangée',
      brut_ou_net='brut (gain des contribuables)', effet_sur_activite='non', contrefactuel_solde_dette='',
      citation='« les ménages ont bénéficié en 2023 de près de 19 Md€ »', marque='[C]', niveau='A'),
 dict(id='CC12', document='Fipeco, Les principales réformes fiscales du quinquennat (27/01/2022) ; pièce S08 fipeco_mesures_fiscales.pdf', date='2022-01-27', page='p. 1',
      montant='environ 44', unite='Md€ courants', annee_mesuree='2022', periode_des_decisions='2017-2022', perimetre='ensemble des mesures fiscales du quinquennat',
      convention='non précisée', brut_ou_net='non précisé', effet_sur_activite='non', contrefactuel_solde_dette='« pas été compensé par des économies »',
      citation='« est d\'environ 44 Md€ en 2022 »', marque='[S]', niveau='F'),
]
with open(os.path.join(SORTIE, 'D05_chiffrages_cumules.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=CC, delimiter=';'); w.writeheader(); w.writerows(C)

# ---------------------------------------------------------------------------
# 4. Inventaire des grandes décisions
# ---------------------------------------------------------------------------
GD = ['annee', 'texte', 'date', 'mesure', 'type', 'impot', 'montant', 'unite', 'annee_du_montant', 'ex_ante_ou_ex_post',
      'brut_ou_net', 'perimetre', 'temporaire_ou_permanent', 'pct_PIB', 'encore_en_vigueur_2025', 'beneficiaires_ou_payeurs',
      'source_incidence', 'source', 'page', 'marque']
def pct(m, an, francs=False):
    v = m / F_PAR_EUR if francs else m
    return round(100 * v / PIB[an], 2)
G = [
 dict(annee=1995, texte='loi n° 95-858 (LFR 1995)', date='1995-07-28', mesure='taux normal de TVA de 18,6 % à 20,6 %', type='hausse', impot='TVA',
      montant=57, unite='MdF (gain attendu en année pleine)', annee_du_montant=1996, ex_ante_ou_ex_post='ex ante', brut_ou_net='brut', perimetre='État',
      temporaire_ou_permanent='permanent puis baisse d\'un point en 2000', pct_PIB=pct(57, 1996, True), encore_en_vigueur_2025='non (taux 20 % depuis 2014 après 19,6 % en 2000)',
      beneficiaires_ou_payeurs='consommateurs', source_incidence='non publié', source='AN, réponse à la question écrite n°2062 (11e législature), JO 8/2/1999 ; sources/AN_QE2062_L11_TVA1995.pdf', page='p. 1', marque='[C]'),
 dict(annee=1997, texte='loi portant mesures urgentes à caractère fiscal et financier', date='1997-11-10', mesure='contribution temporaire sur l\'IS (loi du 10/11/1997)', type='hausse',
      impot='IS', montant=24, unite='MdF', annee_du_montant=1997, ex_ante_ou_ex_post='ex ante', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='temporaire [M] ; la suppression 2000-2002 chiffrée par Carrez p. 11 vise la contribution de 10 pour cent de 1995',
      pct_PIB=pct(24, 1997, True), encore_en_vigueur_2025='non', beneficiaires_ou_payeurs='sociétés bénéficiaires', source_incidence='non publié',
      source='Sénat, rapport n°168 (1997-1998) sur la LFR 1997 ; sources/senat_l97-1686_LFR1997.html', page='section II.3', marque='[C]'),
 dict(annee=1993, texte='exonérations générales de cotisations sur les bas salaires (1993, renforcées 1995-1996, 35 heures 1998-2002, Fillon 2003)', date='1993',
      mesure='allègements généraux de cotisations patronales', type='exonération ou niche', impot='cotisations sociales employeurs', montant=75, unite='Md€ (coût estimé)',
      annee_du_montant=2023, ex_ante_ou_ex_post='ex post (coût estimé)', brut_ou_net='brut (avant effets emploi)', perimetre='ASSO (compensé par l\'État) ; stock 2023 incluant les extensions du Pacte (2015) et de la bascule du CICE (2019) : recoupe ces lignes, ne pas additionner', temporaire_ou_permanent='permanent',
      pct_PIB=pct(75, 2023), encore_en_vigueur_2025='oui (reprofilé 2025)', beneficiaires_ou_payeurs='employeurs de salariés proches du Smic',
      source_incidence='Bozio-Wasmer 2024 (pièce A04)', source='Bozio et Wasmer, rapport 2024 ; pièce A04 bozio_wasmer_2024_vp295596.pdf', page='p. 66', marque='[C]'),
 dict(annee=2000, texte='LFR 2000', date='2000', mesure='baisse d\'un point du taux normal de TVA (20,6 % → 19,6 %)', type='baisse', impot='TVA', montant='-2,9 (2000) ; -1,9 supplémentaire (2001)',
      unite='Md€', annee_du_montant='2000-2001', ex_ante_ou_ex_post='chiffrage administratif rétrospectif', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='permanent',
      pct_PIB=pct(-4.8, 2001), encore_en_vigueur_2025='partiellement (taux porté à 20 % en 2014)', beneficiaires_ou_payeurs='consommateurs', source_incidence='non publié',
      source='Carrez 2010, pièce A04', page='p. 12', marque='[C]'),
 dict(annee=2000, texte='LFR 2000, LFI 2001, LFI 2003, LFI 2004, LFI 2006', date='2000-2006', mesure='réformes successives du barème de l\'impôt sur le revenu', type='baisse',
      impot='IR', montant='-1,7 ; -3,2 et -2 ; -3,6 ; -1,8 ; -4,4', unite='Md€ (coût de chaque texte l\'année de sa montée en charge)', annee_du_montant='2000-2007',
      ex_ante_ou_ex_post='chiffrage administratif rétrospectif', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='permanent',
      pct_PIB='', encore_en_vigueur_2025='oui (barème refondu, pas rétabli)', beneficiaires_ou_payeurs='foyers imposables', source_incidence='non publié',
      source='Carrez 2010, pièce A04', page='p. 10', marque='[C]'),
 dict(annee=2001, texte='loi du 30 mai 2001 et revalorisations', date='2001', mesure='création de la prime pour l\'emploi', type='baisse', impot='IR (crédit)', montant=4,
      unite='Md€ (ordre de grandeur)', annee_du_montant=2009, ex_ante_ou_ex_post='ex post', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='permanent jusqu\'en 2015',
      pct_PIB=pct(4, 2009), encore_en_vigueur_2025='non (remplacée par la prime d\'activité en 2016)', beneficiaires_ou_payeurs='actifs modestes', source_incidence='non publié',
      source='Carrez 2010, pièce A04', page='p. 11', marque='[C]'),
 dict(annee=1999, texte='LFI 1999 (part salaires) puis LFI 2006 (plafonnement à la valeur ajoutée)', date='1999-2006', mesure='suppression de la part salaires et réformes de la taxe professionnelle',
      type='baisse', impot='taxe professionnelle', montant='environ 1 point de PIB 2000-2009', unite='% du PIB', annee_du_montant=2009, ex_ante_ou_ex_post='chiffrage rétrospectif',
      brut_ou_net='net', perimetre='APUL, compensé par l\'État', temporaire_ou_permanent='permanent', pct_PIB=1.0, encore_en_vigueur_2025='oui (TP supprimée en 2010)',
      beneficiaires_ou_payeurs='entreprises', source_incidence='non publié', source='Carrez 2010, pièce A04', page='p. 15', marque='[C]'),
 dict(annee=2007, texte='loi n° 2007-1223 (TEPA)', date='2007-08-21', mesure='heures supplémentaires, bouclier fiscal, intérêts d\'emprunt, droits de succession', type='baisse',
      impot='IR, cotisations, ISF, DMTG', montant='-1,6 (2007) ; -7,5 (2008)', unite='Md€', annee_du_montant='2007-2008', ex_ante_ou_ex_post='ex ante (estimation d\'automne)',
      brut_ou_net='brut', perimetre='État (dont 5,1 Md€ compensés à la sécurité sociale)', temporaire_ou_permanent='permanent, en grande partie supprimé 2011-2012',
      pct_PIB=pct(-9.1, 2008), encore_en_vigueur_2025='partiellement (exonération des heures supplémentaires rétablie 2019)', beneficiaires_ou_payeurs='salariés faisant des heures supplémentaires ; patrimoines élevés',
      source_incidence='non publié', source='RESF PLF 2009 ; sources/RESF_PLF2009_vp194000312.pdf', page='p. 67', marque='[C]'),
 dict(annee=2009, texte='LFR 2009 (plan de relance)', date='2009', mesure='volet fiscal du plan de relance (remboursements anticipés IS, TVA)', type='baisse', impot='IS, TVA, IR',
      montant=-13, unite='Md€', annee_du_montant=2009, ex_ante_ou_ex_post='ex post', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='temporaire',
      pct_PIB=pct(-13, 2009), encore_en_vigueur_2025='non', beneficiaires_ou_payeurs='entreprises (trésorerie), ménages modestes', source_incidence='non publié',
      source='Cour des comptes, RSPFP juin 2010 ; sources/cour_RSPFP_juin2010_vp104000325.pdf', page='p. 10', marque='[C]'),
 dict(annee=2009, texte='loi de développement et de modernisation des services touristiques', date='2009-07', mesure='TVA à 5,5 % dans la restauration', type='exonération ou niche',
      impot='TVA', montant=-3.0, unite='Md€ en année pleine', annee_du_montant=2010, ex_ante_ou_ex_post='ex post (Cour)', brut_ou_net='brut', perimetre='État',
      temporaire_ou_permanent='permanent (taux porté à 7 % en 2012 puis 10 % en 2014)', pct_PIB=pct(-3.0, 2010), encore_en_vigueur_2025='oui (taux réduit 10 %)',
      beneficiaires_ou_payeurs='propriétaires de restaurants (56 % du gain selon l\'IPP)', source_incidence='IPP note 32 (pièce A04)',
      source='Cour des comptes, RSPFP juin 2010', page='p. 10', marque='[C]'),
 dict(annee=2010, texte='LFI 2010', date='2009-12-30', mesure='suppression de la taxe professionnelle (CET)', type='baisse', impot='taxe professionnelle', montant='-12,7 (2010, dont surcoût temporaire) ; environ -6 en régime permanent hors IS',
      unite='Md€', annee_du_montant=2010, ex_ante_ou_ex_post='ex ante', brut_ou_net='net', perimetre='APU (compensé par l\'État)', temporaire_ou_permanent='permanent',
      pct_PIB=pct(-6, 2010), encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='entreprises (industrie)', source_incidence='non publié',
      source='Cour des comptes, RSPFP juin 2010', page='p. 54 et 56 du PDF', marque='[C]'),
 dict(annee=2011, texte='LFI et LFSS 2011, LFR 2011', date='2010-2011', mesure='réduction de niches et hausses (rabot, prélèvements sociaux)', type='hausse', impot='multiples',
      montant=19.2, unite='Md€', annee_du_montant=2011, ex_ante_ou_ex_post='ex ante (estimation)', brut_ou_net='net', perimetre='APU', temporaire_ou_permanent='permanent pour l\'essentiel',
      pct_PIB=pct(19.2, 2011), encore_en_vigueur_2025='en partie', beneficiaires_ou_payeurs='ménages et entreprises', source_incidence='non publié',
      source='RESF PLF 2012 ; sources/RESF_PLF2012_vp194000315.pdf', page='p. 67', marque='[C]'),
 dict(annee=2012, texte='LFR août 2012, LFI et LFSS 2013', date='2012-2013', mesure='hausses d\'IR (tranche 45 %, barème des revenus du capital), d\'IS, de prélèvements sociaux', type='hausse',
      impot='multiples', montant='près de 30 (2013)', unite='Md€', annee_du_montant=2013, ex_ante_ou_ex_post='ex post', brut_ou_net='net', perimetre='APU',
      temporaire_ou_permanent='mixte (contributions exceptionnelles temporaires)', pct_PIB=1.4, encore_en_vigueur_2025='en partie', beneficiaires_ou_payeurs='ménages aisés, grandes entreprises',
      source_incidence='non publié', source='RESF PLF 2015 ; sources/RESF_PLF2015_vp194000031.pdf', page='p. 58', marque='[C]'),
 dict(annee=2013, texte='LFR 2012 (CICE)', date='2012-12-29', mesure='crédit d\'impôt pour la compétitivité et l\'emploi', type='baisse', impot='IS et IR (crédit d\'impôt)',
      montant=-9.4, unite='Md€ (impact sur l\'IS)', annee_du_montant=2014, ex_ante_ou_ex_post='ex ante', brut_ou_net='brut', perimetre='État',
      temporaire_ou_permanent='remplacé en 2019 par des allègements de cotisations', pct_PIB=pct(-9.4, 2014), encore_en_vigueur_2025='oui sous forme d\'allègements',
      beneficiaires_ou_payeurs='employeurs (salaires ≤ 2,5 Smic)', source_incidence='France Stratégie 2020 (pièce A04)', source='RESF PLF 2014 ; sources/RESF_PLF2014_vp194000317.pdf', page='p. 89', marque='[C]'),
 dict(annee=2015, texte='Pacte de responsabilité et de solidarité (LFRSS 2014, LFI 2015-2017)', date='2014-2017', mesure='allègements de cotisations, baisse de la C3S, suppression de la contribution exceptionnelle d\'IS, baisse d\'IR',
      type='baisse', impot='cotisations, C3S, IS, IR', montant='-1,6 (2015) ; -3,4 (2016), nets de toutes les autres mesures', unite='Md€', annee_du_montant='2015-2016',
      ex_ante_ou_ex_post='ex post', brut_ou_net='net (montant propre du Pacte non isolé)', perimetre='APU', temporaire_ou_permanent='permanent',
      pct_PIB='', encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='entreprises ; ménages modestes (IR)', source_incidence='non publié',
      source='RESF PLF 2017 et 2018', page='p. 61 ; p. 77-78', marque='[C]'),
 dict(annee=2018, texte='LFI 2018', date='2017-12-30', mesure='baisse du taux d\'IS de 33,3 % à 25 % (2018-2022)', type='baisse', impot='IS', montant='-0,3 (2017) ; -1,2 (2018) ; -2,4 (2019)',
      unite='Md€ (mesure nouvelle de l\'année)', annee_du_montant='2017-2019', ex_ante_ou_ex_post='ex ante', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='permanent',
      pct_PIB='', encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='sociétés, gain relatif croissant avec la taille (S14)', source_incidence='IPP (S14) ; incidence finale non mesurée',
      source='RESF PLF 2019, tableau 21 ; sources/RESF_PLF2019.pdf', page='p. 210', marque='[C]'),
 dict(annee=2018, texte='LFI 2018', date='2017-12-30', mesure='ISF remplacé par l\'IFI ; prélèvement forfaitaire unique', type='baisse', impot='ISF, IR capital', montant='-3,2 (IFI) ; -1,6 puis -0,3 (PFU)',
      unite='Md€', annee_du_montant='2018-2019', ex_ante_ou_ex_post='ex ante', brut_ou_net='brut', perimetre='État', temporaire_ou_permanent='permanent', pct_PIB=pct(-4.8, 2018),
      encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='80 % du gain aux 10 % les plus aisés (S08)', source_incidence='Insee (S08)', source='RESF PLF 2019, tableau 21', page='p. 210', marque='[C]'),
 dict(annee=2018, texte='LFI 2018 à LFI 2020', date='2017-2023', mesure='suppression de la taxe d\'habitation sur les résidences principales', type='baisse', impot='TH',
      montant=18.9, unite='Md€ (gain des ménages, législation 2017)', annee_du_montant=2023, ex_ante_ou_ex_post='ex post', brut_ou_net='brut', perimetre='APUL, compensé par l\'État',
      temporaire_ou_permanent='permanent', pct_PIB=pct(18.9, 2023) * -1, encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='ménages ; 84 % du gain 2021-2023 aux 20 % les plus aisés (S14)',
      source_incidence='IPP/CPO (S14) ; Cour 2025', source='Cour des comptes, fiscalité locale, janvier 2025 ; pièce A04', page='p. 42 du PDF', marque='[C]'),
 dict(annee=2019, texte='LFI et LFSS 2018', date='2017-12', mesure='bascule du CICE en allègements de cotisations (double avantage en 2019)', type='transfert entre administrations',
      impot='IS / cotisations', montant=-23.6, unite='Md€ (ensemble des mesures 2019, dont surcoût ponctuel)', annee_du_montant=2019, ex_ante_ou_ex_post='ex post',
      brut_ou_net='net', perimetre='APU', temporaire_ou_permanent='surcoût temporaire (environ 20 Md€ selon Fipeco [S])', pct_PIB=pct(-23.6, 2019),
      encore_en_vigueur_2025='allègements oui', beneficiaires_ou_payeurs='employeurs', source_incidence='non publié', source='Insee Première n°1801 (pièce A04)', page='p. 1', marque='[C]'),
 dict(annee=2021, texte='LFI 2021 (plan de relance)', date='2020-12-29', mesure='baisse des impôts de production (CVAE régionale, valeurs locatives industrielles)', type='baisse',
      impot='CVAE, CFE, TFPB', montant='au moins 19 (avec suppression de la CVAE 2023-2024)', unite='Md€', annee_du_montant=2023, ex_ante_ou_ex_post='ex post',
      brut_ou_net='brut', perimetre='APUL, compensé par l\'État', temporaire_ou_permanent='permanent', pct_PIB='', encore_en_vigueur_2025='oui (suppression CVAE reportée)',
      beneficiaires_ou_payeurs='entreprises ; industrie 28 à 37 % selon le périmètre (S14)', source_incidence='IPP n°60 (S14)', source='Cour des comptes, fiscalité locale, janvier 2025', page='p. 8 du PDF', marque='[C]'),
 dict(annee=2025, texte='LFI et LFSS 2025', date='2025-02', mesure='contributions exceptionnelles (grandes entreprises, fret maritime), reprofilage des allègements, cotisations CNRACL', type='hausse',
      impot='IS, cotisations', montant=23.0, unite='Md€ (dont 8,0 temporaires)', annee_du_montant=2025, ex_ante_ou_ex_post='ex post (première estimation)', brut_ou_net='net',
      perimetre='APU', temporaire_ou_permanent='mixte', pct_PIB=pct(23.0, 2025), encore_en_vigueur_2025='oui', beneficiaires_ou_payeurs='grandes entreprises ; employeurs publics locaux',
      source_incidence='non publié', source='Insee Première n°2106 (pièce A04)', page='p. 1', marque='[C]'),
]
for g in G:
    if g['source_incidence'] == 'non publié':
        g['source_incidence'] = 'non recherché par D05'
    g['marque'] = '[C] montant, unité, année du montant et page ; autres champs (texte, date, vigueur 2025, bénéficiaires) [M] sauf renvoi à S08 ou S14'
    g['contrepartie_votee'] = 'la pièce source ne le dit pas'
    if g['annee'] == 2009:
        g['contrepartie_votee'] = 'non : règle de gage de la loi de programmation non respectée (Cour, RSPFP 2010, p. 14 du PDF)'
    if g['annee'] == 2011:
        g['contrepartie_votee'] = 'hausse imposée par la règle de la loi de programmation 2011-2014 (Cour, RSPFP 2011, p. 133 du PDF)'
GD.append('contrepartie_votee')
for g in G:
    if isinstance(g['pct_PIB'], float):
        g['pct_PIB'] = round(g['pct_PIB'], 2)
with open(os.path.join(SORTIE, 'D05_grandes_decisions.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=GD, delimiter=';'); w.writeheader(); w.writerows(sorted(G, key=lambda r: r['annee']))
print('Écrit :', len(L), 'relevés ;', len(rows), 'segments ;', len(C), 'chiffrages ;', len(G), 'décisions')
