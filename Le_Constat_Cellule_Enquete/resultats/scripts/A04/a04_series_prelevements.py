# -*- coding: utf-8 -*-
"""A04 - extraction des series de prelevements depuis la base commune (lecture seule).
Sorties dans resultats/donnees/A04/ :
 - a04_po_recettes_1959_2025.csv : taux de PO (Insee t_3216), recettes et depenses (serie longue), PIB implicite
 - a04_impots_par_categorie_pctPIB.csv : principaux impots (t_3217) en Md EUR et % du PIB, annees choisies
 - a04_eurostat_structure_2024_2025.csv : structure des impots et cotisations (gov_10a_taxag, % PIB) FR vs comparateurs
Execution : python -I a04_series_prelevements.py
"""
import csv, os, openpyxl

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
COM = os.path.join(ROOT, 'donnees', 'commun')
OUT = os.path.join(ROOT, 'donnees', 'A04')
os.makedirs(OUT, exist_ok=True)

# --- 1. t_3216 : PO en Md EUR et % PIB, 1959-2025
ws = openpyxl.load_workbook(os.path.join(COM, 'insee_cn_t_3216.xlsx'), data_only=True).active
rows = [list(r) for r in ws.iter_rows(values_only=True)]
years = rows[2]
def rowby(label_start, after=0):
    for i, r in enumerate(rows):
        if i >= after and r[1] and str(r[1]).strip().startswith(label_start):
            return i, r
    raise KeyError(label_start)
i_md, po_md = rowby('S13 et S212')
i_pct, po_pct = rowby('S13 et S212', after=i_md + 1)
_, asso_pct = rowby('S1314', after=i_pct)
_, apul_pct = rowby('S1313', after=i_pct)
_, apuc_pct = rowby('S1311', after=i_pct)
po = {}
for j, y in enumerate(years):
    if isinstance(y, int):
        md, pc = po_md[j], po_pct[j]
        po[y] = dict(po_md=md, po_pct=pc, pib_md=(md / pc * 100 if isinstance(md, (int, float)) and pc else None),
                     apuc_pct=apuc_pct[j], apul_pct=apul_pct[j], asso_pct=asso_pct[j])

# --- 2. serie longue recettes / depenses / solde (% PIB)
rd = {}
with open(os.path.join(COM, 'base_insee_dep_rec_pctPIB.csv'), encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        s = r['serie']
        key = {'Dépenses': 'dep', 'Recettes': 'rec', 'Déficit au sens de Maastricht': 'solde',
               'dont recettes hors éléments imputés1': 'rec_hors_imput'}.get(s)
        if key:
            try:
                rd.setdefault(int(r['annee']), {})[key] = float(r['valeur'])
            except ValueError:
                pass

with open(os.path.join(OUT, 'a04_po_recettes_1959_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['annee', 'PO_Md_EUR', 'PO_pctPIB', 'PIB_implicite_Md_EUR', 'PO_APUC_pctPIB', 'PO_APUL_pctPIB',
                'PO_ASSO_pctPIB', 'recettes_pctPIB', 'depenses_pctPIB', 'solde_pctPIB', 'recettes_non_PO_pctPIB'])
    for y in sorted(set(po) | set(rd)):
        p = po.get(y, {}); d = rd.get(y, {})
        nonpo = (d['rec'] - p['po_pct']) if ('rec' in d and isinstance(p.get('po_pct'), float)) else None
        w.writerow([y] + [p.get(k) for k in ('po_md', 'po_pct', 'pib_md', 'apuc_pct', 'apul_pct', 'asso_pct')]
                   + [d.get('rec'), d.get('dep'), d.get('solde'), nonpo])

# --- 3. t_3217 : principaux impots par categorie
ws = openpyxl.load_workbook(os.path.join(COM, 'insee_cn_t_3217.xlsx'), data_only=True).active
rows = [list(r) for r in ws.iter_rows(values_only=True)]
yrs = rows[2]
sel = [1995, 2000, 2007, 2010, 2013, 2017, 2019, 2022, 2023, 2024, 2025]
with open(os.path.join(OUT, 'a04_impots_par_categorie_pctPIB.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['ligne_t3217', 'libelle'] + [f'{y}_Md' for y in sel] + [f'{y}_pctPIB' for y in sel])
    for i, r in enumerate(rows):
        lab = r[1]
        if not lab or not any(isinstance(v, (int, float)) for v in r[2:]):
            continue
        md = []; pc = []
        for y in sel:
            v = r[yrs.index(y)] if y in yrs else None
            md.append(round(v, 3) if isinstance(v, (int, float)) else v)
            pib = po.get(y, {}).get('pib_md')
            pc.append(round(v / pib * 100, 3) if isinstance(v, (int, float)) and pib else None)
        w.writerow([i + 1, str(lab).strip()] + md + pc)

# --- 4. Eurostat gov_10a_taxag : structure FR vs comparateurs
items = {
    'D2_D5_D91_D61_M_D995': 'Total impots + cotisations sociales nettes (moins non recouvrables)',
    'D2_D5_D91_D61_M_D611V_D612_M_M_D613V_D614_M_D995': 'Idem hors cotisations imputees et volontaires',
    'D2': 'Impots sur la production et les importations', 'D211': 'TVA',
    'D29': 'Autres impots sur la production', 'D214': 'Impots sur les produits hors TVA et importations',
    'D5': 'Impots courants sur le revenu et le patrimoine', 'D51A_C1': 'Impots sur le revenu des menages',
    'D51B_C2': 'Impots sur le revenu/benefices des societes', 'D59': 'Autres impots courants',
    'D91': 'Impots en capital', 'D61': 'Cotisations sociales nettes', 'D611': 'Cotisations employeurs effectives',
    'D613': 'Cotisations effectives des menages', 'D612': 'Cotisations imputees employeurs',
    'D29A': 'Impots sur la masse salariale', 'D29B': 'Impots fonciers/sur utilisation d actifs (production)',
    'D59A': 'Impots courants sur le capital', 'D214A': 'Accises', 'D995': 'Montants non recouvrables',
}
geos = ['FR', 'DE', 'IT', 'ES', 'NL', 'BE', 'SE', 'DK', 'FI', 'AT', 'EA20', 'EU27_2020']
val = {}
with open(os.path.join(COM, 'eurostat_gov_10a_taxag.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['na_item'] in items and r['geo'] in geos and r['time'] in ('2000', '2007', '2019', '2024', '2025'):
            try:
                val[(r['na_item'], r['geo'], r['time'])] = float(r['value'])
            except ValueError:
                pass
with open(os.path.join(OUT, 'a04_eurostat_structure_2000_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['na_item', 'libelle', 'annee'] + geos + ['FR_moins_EA20', 'FR_moins_DE'])
    for it, lab in items.items():
        for t in ('2000', '2007', '2019', '2024', '2025'):
            vs = [val.get((it, g, t)) for g in geos]
            fr, ea, de = val.get((it, 'FR', t)), val.get((it, 'EA20', t)), val.get((it, 'DE', t))
            w.writerow([it, lab, t] + vs + [round(fr - ea, 2) if fr is not None and ea is not None else None,
                                            round(fr - de, 2) if fr is not None and de is not None else None])
print('ok')
