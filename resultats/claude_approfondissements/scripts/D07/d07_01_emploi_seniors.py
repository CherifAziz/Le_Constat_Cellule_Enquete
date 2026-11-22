# -*- coding: utf-8 -*-
"""D07 - Taux d'emploi par age : France 1975-2025 (Insee T207, edition 2025)
et comparaison France / Allemagne / Pays-Bas / Suede (ILOSTAT, enquetes forces de travail).

Entrees (conservees) :
  ../../donnees/D07/sources/insee_EEC_T207_2025.xlsx
  ../../donnees/D07/sources/ilostat_emp_dwap_age_FR_DE_NL_SE.csv
Sorties :
  ../../donnees/D07/D07_taux_emploi_age_france_1975_2025.csv
  ../../donnees/D07/D07_taux_emploi_seniors_4pays.csv
  ../../donnees/D07/D07_retournements_seniors.csv
  ../../donnees/D07/D07_controle_insee_ilostat_france.csv
"""
import csv
import os
import openpyxl

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07', 'sources'))
OUT = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07'))

# ---------- 1. Insee T207 ----------
ws = openpyxl.load_workbook(os.path.join(SRC, 'insee_EEC_T207_2025.xlsx'), data_only=True).active
rows = list(ws.iter_rows(values_only=True))
annees = [int(a) for a in rows[3][2:] if a is not None]
WANT = {
    ('Total', 'De 15 à 64 ans'): 'tot_15_64',
    ('Total', 'De 25 à 49 ans'): 'tot_25_49',
    ('Total', 'De 50 à 54 ans'): 'tot_50_54',
    ('Total', 'De 55 à 64 ans'): 'tot_55_64',
    ('Total', 'De 55 à 59 ans'): 'tot_55_59',
    ('Total', 'De 60 à 64 ans'): 'tot_60_64',
    ('Homme', 'De 55 à 59 ans'): 'hom_55_59',
    ('Homme', 'De 60 à 64 ans'): 'hom_60_64',
    ('Femme', 'De 55 à 59 ans'): 'fem_55_59',
    ('Femme', 'De 60 à 64 ans'): 'fem_60_64',
}
series = {}
for r in rows[6:]:
    if r[0] is None or r[1] is None:
        continue
    key = (r[0].strip(), r[1].strip())
    if key in WANT:
        series[WANT[key]] = dict(zip(annees, r[2:2 + len(annees)]))
cols = list(WANT.values())
with open(os.path.join(OUT, 'D07_taux_emploi_age_france_1975_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee'] + cols + ['source'])
    for a in annees:
        w.writerow([a] + [series[c][a] for c in cols] + ['Insee T207 ed. 2025, corrige des ruptures'])

# ---------- 2. ILOSTAT 4 pays ----------
ilo = {}
with open(os.path.join(SRC, 'ilostat_emp_dwap_age_FR_DE_NL_SE.csv'), encoding='utf-8-sig') as f:
    for x in csv.DictReader(f):
        age = x['classif1.label'][-5:]
        ilo.setdefault((x['ref_area.label'], age), {})[int(x['time'])] = float(x['obs_value'])
pays = ['France', 'Germany', 'Netherlands', 'Sweden']
toutes = sorted({a for v in ilo.values() for a in v})
with open(os.path.join(OUT, 'D07_taux_emploi_seniors_4pays.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee'] + [f'{p}_{a}' for p in pays for a in ('55-59', '60-64')] +
               ['note'])
    for an in toutes:
        w.writerow([an] + [ilo.get((p, a), {}).get(an, '') for p in pays for a in ('55-59', '60-64')] +
                   ['ILOSTAT EMP_DWAP_SEX_AGE_RT_A ; Allemagne avant 1991 = ex-RFA probable (rupture non documentee dans le fichier)'])

# ---------- 3. Retournements : annee du minimum et niveau ----------
def minimum(d, debut=None, fin=None):
    items = [(a, v) for a, v in d.items() if v is not None and (debut is None or a >= debut) and (fin is None or a <= fin)]
    a, v = min(items, key=lambda t: (t[1], t[0]))
    return a, v

def retournement(d, seuil=2.0):
    """Regle D07 : le retournement est la derniere annee ou la serie est encore a moins de
    `seuil` points de son minimum ; ensuite elle reste durablement au-dessus.
    Le creux plat est la periode entre la premiere et la derniere annee a moins de `seuil` points."""
    a_min, v_min = minimum(d)
    proches = sorted(a for a, v in d.items() if v is not None and v <= v_min + seuil)
    return proches[0], proches[-1]


out = []
for nom, d in [('France (Insee) 55-59', series['tot_55_59']), ('France (Insee) 60-64', series['tot_60_64']),
               ('France (Insee) 55-64', series['tot_55_64'])]:
    a, v = minimum(d)
    c0, c1 = retournement(d)
    out.append([nom, min(d), d[min(d)], a, v, c0, c1, max(d), d[max(d)], 'Insee T207'])
for p in pays:
    if p == 'France':
        continue  # serie ILOSTAT France non retenue (ecart a Eurostat/Insee apres 2003)
    for age in ('55-59', '60-64'):
        d = ilo.get((p, age), {})
        if not d:
            continue
        a, v = minimum(d)
        c0, c1 = retournement(d)
        note = 'ILOSTAT ; Allemagne : rupture probable 1991 (reunification) non documentee' if p == 'Germany' else 'ILOSTAT'
        out.append([f'{p} (ILOSTAT) {age}', min(d), d[min(d)], a, v, c0, c1, max(d), d[max(d)], note])
with open(os.path.join(OUT, 'D07_retournements_seniors.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['serie', 'premiere_annee', 'valeur_premiere_annee', 'annee_minimum', 'valeur_minimum',
                'creux_debut_(min+2pts)', 'retournement_fin_du_creux_(min+2pts)',
                'derniere_annee', 'valeur_derniere_annee', 'source'])
    w.writerows(out)

# ---------- 4. Controle : France Insee contre ILOSTAT ----------
with open(os.path.join(OUT, 'D07_controle_insee_ilostat_france.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'insee_55_59', 'ilostat_55_59', 'ecart_55_59', 'insee_60_64', 'ilostat_60_64', 'ecart_60_64'])
    for an in (1985, 1990, 1995, 2000, 2005, 2010, 2015, 2019, 2024, 2025):
        i1, i2 = series['tot_55_59'].get(an), series['tot_60_64'].get(an)
        o1, o2 = ilo.get(('France', '55-59'), {}).get(an), ilo.get(('France', '60-64'), {}).get(an)
        e1 = round(o1 - i1, 1) if (i1 is not None and o1 is not None) else ''
        e2 = round(o2 - i2, 1) if (i2 is not None and o2 is not None) else ''
        w.writerow([an, i1, o1, e1, i2, o2, e2])

# ---------- 5. Controle : Eurostat (lfsa_ergan) contre ILOSTAT, 4 pays ----------
import json
d = json.load(open(os.path.join(SRC, 'eurostat_lfsa_ergan.json'), encoding='utf-8'))
dims, size = d['id'], d['size']
idx = {k: d['dimension'][k]['category']['index'] for k in dims}


def eurostat(geo, age, an):
    kw = dict(freq='A', unit='PC', sex='T', citizen='TOTAL', age=age, geo=geo, time=str(an))
    pos = 0
    for k, s in zip(dims, size):
        pos = pos * s + idx[k][kw[k]]
    return d['value'].get(str(pos))


GEO = {'France': 'FR', 'Germany': 'DE', 'Netherlands': 'NL', 'Sweden': 'SE'}
with open(os.path.join(OUT, 'D07_controle_eurostat_ilostat_4pays.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['pays', 'age', 'annee', 'eurostat', 'ilostat', 'insee_si_france'])
    for p, g in GEO.items():
        for age, ae in (('55-59', 'Y55-59'), ('60-64', 'Y60-64')):
            for an in (1995, 2000, 2010, 2019, 2025):
                ins = series['tot_' + age.replace('-', '_')].get(an) if p == 'France' else ''
                w.writerow([p, age, an, eurostat(g, ae, an), round(ilo.get((p, age), {}).get(an, float('nan')), 1), ins])

for r in out:
    print(r)
print('ok')
