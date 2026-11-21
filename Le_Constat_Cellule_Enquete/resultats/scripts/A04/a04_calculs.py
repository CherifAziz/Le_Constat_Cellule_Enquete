# -*- coding: utf-8 -*-
"""A04 - calculs reproductibles.
C-A04-001 : reconstitution du cumul des mesures nouvelles de PO 2018-2023 (Insee Premiere, chiffrage DG Tresor)
C-A04-002 : classement UE des impots+cotisations 2024-2025 (Eurostat gov_10a_taxag, extraction A04 du 20/11/2026)
C-A04-003 : decomposition de l'ecart FR - EA20 par grande categorie (base commune)
Execution : python -I a04_calculs.py  (depuis n'importe quel dossier)
"""
import csv, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = os.path.join(ROOT, 'donnees', 'A04')

# PIB implicite (Md EUR courants, base 2020) = PO / taux PO, Insee t_3216
pib = {}
with open(os.path.join(D, 'a04_po_recettes_1959_2025.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        if r['PIB_implicite_Md_EUR']:
            pib[int(r['annee'])] = float(r['PIB_implicite_Md_EUR'])

# Mesures nouvelles de PO (Md EUR), Insee Premiere de chaque annee (chiffrage DG Tresor), millesimes successifs
mn = {2018: -9.7, 2019: -23.6, 2020: 5.1, 2021: -14.8, 2022: -7.7, 2023: -7.1, 2024: 3.6, 2025: 23.0}
src = {2018: 'IP 1753', 2019: 'IP 1801', 2020: 'IP 1859', 2021: 'IP 1903', 2022: 'IP 1949', 2023: 'IP 1998',
       2024: 'IP 2054', 2025: 'IP 2106'}
out = []
cum_md = cum_pt = 0.0
print('C-A04-001 mesures nouvelles PO')
for y in sorted(mn):
    pt = mn[y] / pib[y] * 100
    cum_md += mn[y]; cum_pt += pt
    out.append([y, mn[y], round(pib[y], 1), round(pt, 3), round(cum_md, 1), round(cum_pt, 3), src[y]])
    print(y, mn[y], round(pt, 2), 'cumul', round(cum_md, 1), round(cum_pt, 2))
s1823_md = sum(mn[y] for y in range(2018, 2024))
s1823_pt = sum(mn[y] / pib[y] * 100 for y in range(2018, 2024))
print('Somme 2018-2023 :', round(s1823_md, 1), 'Md EUR ;', round(s1823_pt, 2), 'pt de PIB (somme des ratios annuels)')
print('Exprime au PIB 2023 :', round(s1823_pt * pib[2023] / 100, 1), 'Md EUR')
s1925 = sum(mn[y] for y in range(2018, 2026))
print('Somme 2018-2025 :', round(s1925, 1), 'Md EUR ; hors exceptionnelles 2025 (8,0) :', round(s1925 - 8.0, 1))
with open(os.path.join(D, 'C-A04-001_mesures_nouvelles_2018_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'mesures_nouvelles_Md', 'PIB_Md_base2020', 'mesures_pt_PIB', 'cumul_Md', 'cumul_pt', 'source'])
    w.writerows(out)

# C-A04-002 classement UE
j = json.load(open(os.path.join(D, 'eurostat_taxag_EU27_toutpays_2024_2025.json'), encoding='utf-8'))
dims = j['id']; sizes = j['size']
idx = {d: j['dimension'][d]['category']['index'] for d in dims}
def get(**k):
    pos = 0
    for d, s in zip(dims, sizes):
        pos = pos * s + idx[d][k[d]]
    return j['value'].get(str(pos))
eu27 = ['BE','BG','CZ','DK','DE','EE','IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE']
print('\nC-A04-002 classement UE27, impots + cotisations nettes (D2_D5_D91_D61_M_D995), % PIB')
rows = []
for t in ('2024', '2025'):
    vals = []
    for g in eu27:
        if g in idx['geo']:
            v = get(freq='A', unit='PC_GDP', sector='S13_S212', na_item='D2_D5_D91_D61_M_D995', geo=g, time=t)
            v2 = get(freq='A', unit='PC_GDP', sector='S13_S212', na_item='D2_D5_D91_D61_M_D611V_D612_M_M_D613V_D614_M_D995', geo=g, time=t)
            if v is not None:
                vals.append((v, g, v2))
    vals.sort(reverse=True)
    print(t, [(g, v) for v, g, _ in vals[:6]])
    v2s = sorted([(v2, g) for v, g, v2 in vals if v2 is not None], reverse=True)
    print(t, 'hors cotisations imputees/volontaires :', v2s[:6])
    for rank, (v, g, v2) in enumerate(vals, 1):
        rows.append([t, rank, g, v, v2])
with open(os.path.join(D, 'C-A04-002_classement_UE27_taxag.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'rang', 'pays', 'impots_cotis_nettes_pctPIB', 'idem_hors_imputees_volontaires'])
    w.writerows(rows)

# C-A04-003 decomposition ecart FR - EA20 2025 (base commune)
print('\nC-A04-003 ecart FR - EA20, 2025, points de PIB')
items = ['D211', 'D214', 'D29A', 'D29', 'D51A_C1', 'D51B_C2', 'D59', 'D91', 'D611', 'D612', 'D613', 'D61', 'D2', 'D5',
         'D2_D5_D91_D61_M_D995']
val = {}
with open(os.path.join(ROOT, 'donnees', 'commun', 'eurostat_gov_10a_taxag.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['na_item'] in items and r['geo'] in ('FR', 'EA20', 'DE', 'IT', 'BE', 'AT') and r['time'] in ('2025', '2019', '2000'):
            try: val[(r['na_item'], r['geo'], r['time'])] = float(r['value'])
            except ValueError: pass
res = []
for it in items:
    for t in ('2000', '2019', '2025'):
        fr = val.get((it, 'FR', t)); ea = val.get((it, 'EA20', t))
        res.append([it, t, fr, ea, round(fr - ea, 2) if fr is not None and ea is not None else None,
                    val.get((it, 'DE', t)), val.get((it, 'IT', t)), val.get((it, 'BE', t)), val.get((it, 'AT', t))])
        if t == '2025':
            print(it, fr, ea, res[-1][4])
with open(os.path.join(D, 'C-A04-003_ecart_FR_EA20.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['na_item', 'annee', 'FR', 'EA20', 'FR_moins_EA20', 'DE', 'IT', 'BE', 'AT'])
    w.writerows(res)

# C-A04-004 : variation du taux de PO et des recettes par sous-periode ; residu "spontane" quand les mesures nouvelles sont connues
po = {}; rec = {}
with open(os.path.join(D, 'a04_po_recettes_1959_2025.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        y = int(r['annee'])
        if r['PO_pctPIB']: po[y] = float(r['PO_pctPIB'])
        if r['recettes_pctPIB']: rec[y] = float(r['recettes_pctPIB'])
# periodes de la mission : variation entre l'annee precedant la periode et la derniere annee
mission = [(1975, 1985), (1986, 1993), (1994, 1999), (2000, 2007), (2008, 2010), (2011, 2014), (2015, 2017), (2018, 2023), (2024, 2025)]
# mesures nouvelles cumulees (pts de PIB) : Fipeco [S] (1989-2019) ; Insee/DG Tresor [C] (2018-2025, somme des ratios annuels)
mn_pts = {(1989, 1998): 2.9, (1999, 2002): -2.7, (2003, 2006): 0.7, (2007, 2009): -2.1, (2010, 2014): 3.9, (2015, 2017): -0.2,
          (2018, 2023): round(sum(mn[y] / pib[y] * 100 for y in range(2018, 2024)), 2),
          (2024, 2025): round(sum(mn[y] / pib[y] * 100 for y in range(2024, 2026)), 2)}
rows = []
print('\nC-A04-004 variation du taux de PO (Insee base 2020) par sous-periode')
for a, b in mission + [p for p in mn_pts if p not in mission]:
    dpo = po[b] - po[a - 1]; drec = rec[b] - rec[a - 1]
    m = mn_pts.get((a, b))
    resid = round(dpo - m, 2) if m is not None else None
    rows.append([f'{a}-{b}', round(po[a - 1], 2), round(po[b], 2), round(dpo, 2), round(drec, 2), m, resid,
                 'mission' if (a, b) in mission else 'decoupage Fipeco/Insee'])
    print(f'{a}-{b}', 'PO', round(po[a-1], 1), '->', round(po[b], 1), 'dPO', round(dpo, 2), 'dRec', round(drec, 2), 'MN', m, 'residu', resid)
with open(os.path.join(D, 'C-A04-004_PO_sous_periodes.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['periode', 'PO_annee_precedente', 'PO_fin', 'delta_PO_pts', 'delta_recettes_pts', 'mesures_nouvelles_pts',
                'residu_spontane_approx_pts', 'decoupage'])
    w.writerows(rows)

# C-A04-005 : elasticite annuelle des PO au PIB 2018-2025 = croissance spontanee / croissance du PIB en valeur
# croissance spontanee = (PO_t - PO_{t-1} - MN_t) / PO_{t-1} ; PO en Md EUR base 2020 (t_3216) ; MN Insee (millesimes successifs)
po_md = {}
with open(os.path.join(D, 'a04_po_recettes_1959_2025.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        if r['PO_Md_EUR']: po_md[int(r['annee'])] = float(r['PO_Md_EUR'])
rows = []
print('\nC-A04-005 elasticite des PO au PIB (reconstitution A04)')
for y in range(2018, 2026):
    g_po = (po_md[y] - po_md[y - 1] - mn[y]) / po_md[y - 1]
    g_pib = pib[y] / pib[y - 1] - 1
    e = g_po / g_pib
    rows.append([y, round(po_md[y], 1), mn[y], round(g_po * 100, 2), round(g_pib * 100, 2), round(e, 2)])
    print(y, 'spontane %', round(g_po * 100, 2), 'PIB %', round(g_pib * 100, 2), 'elasticite', round(e, 2))
with open(os.path.join(D, 'C-A04-005_elasticite_2018_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'PO_Md_base2020', 'mesures_nouvelles_Md', 'croissance_spontanee_pct', 'croissance_PIB_valeur_pct', 'elasticite'])
    w.writerows(rows)
