"""D02 - Calculs : conversion en points de PIB, décomposition 1980 -> 1981 par sous-secteur,
rendement et perte de la cotisation de 1 % (1979-1981), cadres comptables côte à côte.

Entrées (conservées) : ../../donnees/D02/sources/a04_po_recettes_1959_2025.csv (PIB base 2020),
  ../../donnees/D02/sources/insee_solde_par_sous_secteur.xlsx, ../../donnees/D02/D02_valeurs_pieces.csv
Sorties : ../../donnees/D02/D02_*.csv (séparateur ;, UTF-8).
Conventions : 1 EUR = 6,55957 F ; PIB de l'année d'effet ; on n'additionne jamais deux cadres comptables.
Lancer : python -X utf8 -I d02_calculs.py
"""
import os, csv
import openpyxl

ICI = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D02'))
S = os.path.join(D, 'sources')
F_PAR_EUR = 6.55957


def ecrire(nom, entete, lignes):
    with open(os.path.join(D, nom), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(entete)
        for l in lignes:
            w.writerow([('%.3f' % x).replace('.', ',') if isinstance(x, float) else x for x in l])


# PIB en milliards de francs
pib = {}
for r in csv.DictReader(open(os.path.join(S, 'a04_po_recettes_1959_2025.csv'), encoding='utf-8'), delimiter=';'):
    a = int(r['annee'])
    if 1974 <= a <= 1986:
        pib[a] = float(r['PIB_implicite_Md_EUR']) * F_PAR_EUR
solde_a04 = {int(r['annee']): r['solde_pctPIB'] for r in
             csv.DictReader(open(os.path.join(S, 'a04_po_recettes_1959_2025.csv'), encoding='utf-8'), delimiter=';')}


def pct(md_f, annee):
    return 100.0 * md_f / pib[annee]


# Valeurs relevées sur pièces (millions de francs sauf indication)
V = {}
for r in csv.DictReader(open(os.path.join(D, 'D02_valeurs_pieces.csv'), encoding='utf-8'), delimiter=';'):
    V[r['cle']] = float(r['valeur'])

# 0. Contrôles : nombre de champs des tables écrites à la main ; sommes des autres régimes (tableau du n° 102 t. III p.10)
for nom, n in (('D02_valeurs_pieces.csv', 11), ('D02_plans_1976_1983.csv', 17)):
    for i, r in enumerate(csv.reader(open(os.path.join(D, nom), encoding='utf-8'), delimiter=';'), 1):
        assert len(r) == n, (nom, i, len(r))
AUTRES = {  # fonctionnaires, salariés agricoles, mines, marins, SNCF, RATP, clercs de notaires, militaires (image)
    1979: (463, 43, 14, 7, 15, 4, 0, 48), 1980: (1592, 292, 58, 31, 65, 26, 8, 163), 1981: (299, 108, 15, 8, 18, 7, 5, 31)}
for a, t in AUTRES.items():
    assert sum(t) == V['cotis1pct_autres_%d' % a], (a, sum(t))

# 1. Sous-secteurs (Insee, base 2020), milliards d'euros
wb = openpyxl.load_workbook(os.path.join(S, 'insee_solde_par_sous_secteur.xlsx'), data_only=True)
ws = wb['Figure 1']
hdr = [c.value for c in ws[4]]
cols = {v: i for i, v in enumerate(hdr) if isinstance(v, int) and 1975 <= v <= 1985}
ss = {}
for row in ws.iter_rows(min_row=5, values_only=True):
    if row[0] in ('État', "Organismes divers d'administration centrale", 'Administrations publiques locales',
                  'Administrations de sécurité sociale', 'Ensemble'):
        ss[row[0]] = {a: row[i] for a, i in cols.items()}
lignes = []
for a in range(1975, 1986):
    pib_e = pib[a] / F_PAR_EUR
    lignes.append([a, round(pib[a], 1)] + [100 * ss[k][a] / pib_e for k in
                                            ('État', "Organismes divers d'administration centrale",
                                             'Administrations publiques locales',
                                             'Administrations de sécurité sociale', 'Ensemble')] + [solde_a04[a]])
ecrire('D02_soldes_sous_secteurs_1975_1985.csv',
       ['annee', 'PIB_Md_F', 'Etat_pctPIB', 'ODAC_pctPIB', 'APUL_pctPIB', 'ASSO_pctPIB', 'S13_pctPIB_calcule',
        'S13_pctPIB_serie_A04'], lignes)

# Décomposition 1980 -> 1981 (comptes nationaux, une seule convention)
dec = []
tot = ss['Ensemble'][1981] - ss['Ensemble'][1980]
for k in ('État', "Organismes divers d'administration centrale", 'Administrations publiques locales',
          'Administrations de sécurité sociale', 'Ensemble'):
    d_e = ss[k][1981] - ss[k][1980]
    d_pts = 100 * ss[k][1981] / (pib[1981] / F_PAR_EUR) - 100 * ss[k][1980] / (pib[1980] / F_PAR_EUR)
    dec.append([k, ss[k][1980], ss[k][1981], d_e, d_e * F_PAR_EUR, d_pts, 100 * d_e / tot])
ecrire('D02_ecart_1980_1981_sous_secteurs.csv',
       ['sous_secteur', 'solde_1980_Md_EUR', 'solde_1981_Md_EUR', 'variation_Md_EUR', 'variation_Md_F',
        'variation_points_PIB', 'part_de_la_variation_totale_pct'], dec)

# Décomposition par périodes, en points de PIB (variation des ratios)
per = []
for a0, a1 in ((1975, 1980), (1978, 1980), (1979, 1980), (1980, 1981), (1981, 1983), (1980, 1985)):
    tot_pts = 100 * ss['Ensemble'][a1] / (pib[a1] / F_PAR_EUR) - 100 * ss['Ensemble'][a0] / (pib[a0] / F_PAR_EUR)
    for k in ('État', "Organismes divers d'administration centrale", 'Administrations publiques locales',
              'Administrations de sécurité sociale', 'Ensemble'):
        d_pts = 100 * ss[k][a1] / (pib[a1] / F_PAR_EUR) - 100 * ss[k][a0] / (pib[a0] / F_PAR_EUR)
        per.append(['%d-%d' % (a0, a1), k, d_pts, 100 * d_pts / tot_pts])
ecrire('D02_variations_soldes_par_periode.csv',
       ['periode', 'sous_secteur', 'variation_points_PIB', 'part_de_la_variation_S13_pct'], per)

# 2. Cotisation de 1 % : rendements et perte en 1981
c = []
for a in (1979, 1980, 1981):
    rg = V['cotis1pct_rg_%d' % a] / 1000
    au = V['cotis1pct_autres_%d' % a] / 1000
    c.append([a, 'ex ante (Sénat n° 102 t. III, nov. 1980)', rg, au, rg + au, pct(rg + au, a)])
rg80 = V['cotis1pct_rg_1980_expost'] / 1000
c.append([1980, 'ex post, régime général seul (CCSS juillet 1981)', rg80, '', '', pct(rg80, 1980)])
c.append([1980, 'montant global annoncé, tous régimes (Sénat n° 98)', '', '', V['cotis1pct_global_annonce'] / 1000,
          pct(V['cotis1pct_global_annonce'] / 1000, 1980)])
ecrire('D02_cotisation_1pct_1979_1981.csv',
       ['annee', 'statut', 'regime_general_Md_F', 'autres_regimes_Md_F', 'total_Md_F', 'total_pct_PIB'], c)

# Perte en 1981 (neuf mois sans la cotisation, février à octobre) : arithmétique, deux conventions, pas une estimation
perte = []
base_bas = (V['cotis1pct_rg_1980'] + V['cotis1pct_autres_1980']) / 1000  # ex ante 1980, tous régimes
base_rg_post = rg80                                                       # ex post 1980, RG
base_haut = V['point_deplafonne_annee_pleine'] / 1000                     # un point déplafonné, RG, 1981-1982
for lib, b in (('rendement 1980 ex ante, tous régimes, x 9/12 (sans croissance de l\'assiette)', base_bas),
               ('rendement 1980 ex post, régime général seul, x 9/12', base_rg_post),
               ('un point déplafonné « près de 13 Md F en année pleine » (CCSS déc. 1982), RG, x 9/12', base_haut)):
    perte.append([lib, b, b * 9 / 12, pct(b * 9 / 12, 1981)])
# Convention retenue : parts en points de PIB (perte en % du PIB 1981 rapportée à la variation des ratios 1980 -> 1981)
def ratio(k, a):
    return 100 * ss[k][a] * F_PAR_EUR / pib[a]
dS13 = ratio('Ensemble', 1981) - ratio('Ensemble', 1980)
dASSO = ratio('Administrations de sécurité sociale', 1981) - ratio('Administrations de sécurité sociale', 1980)
for l in perte:
    l += [100 * l[3] / -dS13, 100 * l[3] / -dASSO]
ecrire('D02_perte_1pct_1981_arithmetique.csv',
       ['convention', 'base_annee_pleine_Md_F', 'perte_9_mois_Md_F', 'perte_pct_PIB_1981',
        'part_de_la_degradation_S13_1980_1981_pct', 'part_de_la_degradation_ASSO_1980_1981_pct'], perte)

# 3. Trois cadres comptables côte à côte (jamais sommés)
cad = []
def ajout(cadre, poste, v80, v81, src):
    cad.append([cadre, poste, v80, v81, v81 - v80, pct(v80, 1980), pct(v81, 1981), pct(v81, 1981) - pct(v80, 1980), src])
ajout('Budget de l\'État (lois de finances, hors FMI et Fonds de stabilisation des changes)', 'solde',
      V['etat_solde_1980'] / 1000, V['etat_solde_1981'] / 1000, 'Sénat n° 405 (1982-1983) p.29')
ajout('Budget de l\'État', 'charge de la dette publique stricto sensu (dépense)',
      V['etat_dette_stricto_1980'] / 1000, V['etat_dette_stricto_1981'] / 1000, 'Sénat n° 405 p.13')
ajout('Régime général (comptes des caisses)', 'solde', V['rg_solde_1980'] / 1000, V['rg_solde_1981'] / 1000,
      'CCSS juillet 1981 p.18 ; CCSS juin 1983 p.30')
ajout('Régime général', 'solde hors cotisation de 1 % (1980 seulement)', V['rg_solde_1980_hors_1pct'] / 1000,
      V['rg_solde_1981'] / 1000, 'CCSS juillet 1981 p.18 (1981 : la cotisation est absente 9 mois sur 12)')
ajout('Assurance chômage (Unédic)', 'charges (dépense brute)', V['unedic_charges_1980'] / 1000,
      V['unedic_charges_1981'] / 1000, 'Sénat n° 32 (1982-1983) p.13')
ajout('Comptes nationaux base 2020 (S13)', 'solde ensemble', ss['Ensemble'][1980] * F_PAR_EUR,
      ss['Ensemble'][1981] * F_PAR_EUR, 'Insee, solde par sous-secteur')
ajout('Comptes nationaux base 2020 (S13)', 'solde des administrations de sécurité sociale',
      ss['Administrations de sécurité sociale'][1980] * F_PAR_EUR,
      ss['Administrations de sécurité sociale'][1981] * F_PAR_EUR, 'Insee, solde par sous-secteur')
ajout('Comptes nationaux base 2020 (S13)', 'solde de l\'État', ss['État'][1980] * F_PAR_EUR,
      ss['État'][1981] * F_PAR_EUR, 'Insee, solde par sous-secteur')
ecrire('D02_cadres_1980_1981.csv',
       ['cadre_comptable', 'poste', 'valeur_1980_Md_F', 'valeur_1981_Md_F', 'variation_Md_F', '1980_pct_PIB',
        '1981_pct_PIB', 'variation_points_PIB', 'source'], cad)

# 4. Remise à niveau de juillet 1981 (ex ante, année pleine), en points de PIB 1981
rn = [[k, V[k] / 1000, pct(V[k] / 1000, 1981)] for k in
      ('lfr1981_remise_niveau', 'lfr1981_rn_dette', 'lfr1981_rn_chomage', 'lfr1981_rn_prets',
       'lfr1981_actions_nouvelles', 'lfr1981_non_gage')]
ecrire('D02_collectif_juillet_1981.csv', ['poste', 'Md_F', 'pct_PIB_1981'], rn)

# 5. Soldes de l'État en % du PIB base 2020
et = [[a, V['etat_solde_%d' % a] / 1000, pct(V['etat_solde_%d' % a] / 1000, a)] for a in range(1976, 1982)]
ecrire('D02_solde_budget_etat_1976_1981.csv', ['annee', 'solde_Md_F', 'pct_PIB_base2020'], et)

print('PIB 1980 / 1981 (Md F) :', round(pib[1980], 1), round(pib[1981], 1))
for l in dec: print('décomposition', l[0], round(l[4], 1), 'Md F', round(l[5], 2), 'pt', round(l[6], 1), '%')
for l in perte: print('perte', [round(x, 2) if isinstance(x, float) else x for x in l])
for l in cad: print('cadre', l[0][:30], l[1][:30], [round(x, 2) for x in l[2:8]])
for l in c: print('1 %', l)
