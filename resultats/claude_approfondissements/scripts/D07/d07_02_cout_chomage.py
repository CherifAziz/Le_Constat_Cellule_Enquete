# -*- coding: utf-8 -*-
"""D07 - Cout public du chomage et chomage structurel estime.

Entrees (conservees) :
  ../../donnees/D07/sources/drees_cps_1959_2024.xlsx      (comptes de la protection sociale, M EUR)
  ../../donnees/D07/sources/eurostat_gov_10a_exp_GF1005.json (COFOG 10.5 chomage, S13, % PIB)
  ../../donnees/D07/sources/eurostat_une_ltu_a.json       (part du chomage de longue duree)
  ../../donnees/D07/sources/ameco_1.0.0.0.ZNAWRU.html     (NAWRU, Commission europeenne)
  ../../donnees/D07/sources/ameco_1.0.0.0.ZUTN.html       (taux de chomage)
  PIB : Le_Constat_Cellule_Enquete/resultats/donnees/A04/a04_po_recettes_1959_2025.csv (PIB_implicite_Md_EUR)
Sorties :
  ../../donnees/D07/D07_cout_chomage_series.csv
  ../../donnees/D07/D07_cout_chomage_moyennes_periodes.csv
  ../../donnees/D07/D07_chomage_structurel_ameco.csv
Conventions : CPS = prestations de protection sociale du risque "emploi" (chomage + insertion),
tous regimes (y compris regimes d'employeurs), en euros courants (francs convertis a 6,55957),
rapportees au PIB Insee base 2020. COFOG = depense des administrations publiques (S13).
Les deux conventions ne s'additionnent pas.
"""
import csv
import json
import os
import re
import openpyxl

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
SRC = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07', 'sources'))
OUT = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07'))
PIB_F = os.path.normpath(os.path.join(_racine_depot(ICI), 'Le_Constat_Cellule_Enquete',
                                      'resultats', 'donnees', 'A04', 'a04_po_recettes_1959_2025.csv'))

pib = {}
with open(PIB_F, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        pib[int(r['annee'])] = float(r['PIB_implicite_Md_EUR'])

# --- CPS Drees ---
ws = openpyxl.load_workbook(os.path.join(SRC, 'drees_cps_1959_2024.xlsx'), read_only=True, data_only=True)['prestations_1959_2024']
rows = list(ws.iter_rows(values_only=True))
hdr = rows[0]
an_col = {}
for i, h in enumerate(hdr):
    if h:
        m = re.match(r'(\d{4})', str(h))
        if m:
            an_col[int(m.group(1))] = i
LIGNES = {'Emploi': 'cps_emploi', 'Chômage': 'cps_chomage', 'Insertion et réinsertion professionnelles': 'cps_insertion',
          'Préretraites': 'cps_preretraites', 'Allocation chômage': 'cps_allocation_chomage'}
cps = {}
for r in rows:
    if r[0] in LIGNES and LIGNES[r[0]] not in cps:
        cps[LIGNES[r[0]]] = {a: r[i] for a, i in an_col.items()}

# --- Eurostat ---
def lire_eurostat(fn, fixes):
    d = json.load(open(os.path.join(SRC, fn), encoding='utf-8'))
    dims, size = d['id'], d['size']
    idx = {k: d['dimension'][k]['category']['index'] for k in dims}
    res = {}
    for geo in idx['geo']:
        for t in idx['time']:
            kw = dict(fixes, geo=geo, time=t)
            pos = 0
            for k, s in zip(dims, size):
                pos = pos * s + (idx[k][kw[k]] if k in kw else 0)
            v = d['value'].get(str(pos))
            if v is not None:
                res[(geo, int(t))] = v
    return res

cofog = lire_eurostat('eurostat_gov_10a_exp_GF1005.json', {})
ltu = lire_eurostat('eurostat_une_ltu_a.json', {})

# --- AMECO ---
def lire_ameco(fn):
    t = open(os.path.join(SRC, fn), encoding='utf-8', errors='replace').read()
    cells = [re.sub(r'<[^>]+>', '', c).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', t, flags=re.S)]
    years = [int(c) for c in cells if re.fullmatch(r'(19|20)\d\d', c)]
    years = years[:len(set(years))]
    res = {}
    for pays in ('Germany', 'France'):
        i = cells.index(pays)
        vals = cells[i + 3:i + 3 + len(years)]
        res[pays] = {y: (float(v) if v not in ('', 'NA') else None) for y, v in zip(years, vals)}
    return res

nawru = lire_ameco('ameco_1.0.0.0.ZNAWRU.html')
utn = lire_ameco('ameco_1.0.0.0.ZUTN.html')

# --- Sortie annuelle ---
annees = list(range(1959, 2026))
with open(os.path.join(OUT, 'D07_cout_chomage_series.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'pib_Md_EUR',
                'cps_emploi_Md_EUR', 'cps_emploi_pctPIB', 'cps_chomage_pctPIB', 'cps_insertion_pctPIB',
                'cps_preretraites_pctPIB', 'cps_allocation_chomage_pctPIB',
                'cofog_GF1005_FR_pctPIB', 'cofog_GF1005_DE_pctPIB',
                'part_chomage_longue_duree_FR_pct', 'part_chomage_longue_duree_DE_pct',
                'taux_chomage_FR_ameco', 'nawru_FR_ameco'])
    for a in annees:
        p = pib.get(a)
        def pct(k):
            v = cps.get(k, {}).get(a)
            return round(v / 1000 / p * 100, 3) if (v not in (None, 0) and p) else ''
        em = cps['cps_emploi'].get(a)
        w.writerow([a, p, round(em / 1000, 3) if em else '', pct('cps_emploi'), pct('cps_chomage'), pct('cps_insertion'),
                    pct('cps_preretraites'), pct('cps_allocation_chomage'),
                    cofog.get(('FR', a), ''), cofog.get(('DE', a), ''),
                    ltu.get(('FR', a), ''), ltu.get(('DE', a), ''),
                    utn['France'].get(a, ''), nawru['France'].get(a, '')])

# --- Moyennes par periode ---
PER = [(1970, 1974), (1975, 1984), (1985, 1993), (1994, 2002), (2003, 2008), (2009, 2015), (2016, 2019), (2020, 2024)]
with open(os.path.join(OUT, 'D07_cout_chomage_moyennes_periodes.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['periode', 'cps_emploi_pctPIB_moy', 'cps_chomage_pctPIB_moy', 'cofog_GF1005_FR_pctPIB_moy',
                'taux_chomage_FR_moy', 'nawru_FR_moy'])
    for a0, a1 in PER:
        def moy(vals):
            vals = [v for v in vals if v not in (None, '')]
            return round(sum(vals) / len(vals), 2) if vals else ''
        ce = moy([cps['cps_emploi'][a] / 1000 / pib[a] * 100 for a in range(a0, a1 + 1) if cps['cps_emploi'].get(a)])
        cc = moy([cps['cps_chomage'][a] / 1000 / pib[a] * 100 for a in range(a0, a1 + 1) if cps['cps_chomage'].get(a)])
        cf = moy([cofog.get(('FR', a)) for a in range(a0, a1 + 1)])
        u = moy([utn['France'].get(a) for a in range(a0, a1 + 1)])
        n = moy([nawru['France'].get(a) for a in range(a0, a1 + 1)])
        w.writerow([f'{a0}-{a1}', ce, cc, cf, u, n])

with open(os.path.join(OUT, 'D07_chomage_structurel_ameco.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'taux_chomage_FR', 'nawru_FR', 'taux_chomage_DE', 'nawru_DE', 'note'])
    for a in range(1965, 2028):
        w.writerow([a, utn['France'].get(a, ''), nawru['France'].get(a, ''), utn['Germany'].get(a, ''),
                    nawru['Germany'].get(a, ''), 'AMECO, estimation de la Commission (modele), pas une mesure ; 2026-2027 = prevision'])
# Recoupement avec S10 (preretraites, rubrique B, 56,2 Md F constates en 1985 ; SES 1986 via S10)
ch85 = cps['cps_chomage'][1985] / 1000  # Md EUR
with open(os.path.join(OUT, 'D07_recoupement_S10_1985.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['indicateur', 'valeur', 'unite', 'convention'])
    w.writerow(['CPS risque chomage 1985', round(ch85, 3), 'Md EUR', 'Drees, tous regimes'])
    w.writerow(['CPS risque chomage 1985', round(ch85 * 6.55957, 1), 'Md F', 'conversion 6,55957'])
    w.writerow(['Preretraites rubrique B 1985 (S10)', 56.2, 'Md F', 'statistique ministerielle SES 1986'])
    w.writerow(['Part S10 / CPS chomage', round(56.2 / (ch85 * 6.55957) * 100, 1), '%', 'deux conventions differentes : ordre de grandeur'])
print('ok')
