# A06 - Téléchargement Eurostat (API dissemination 1.0, JSON-stat 2.0) et mise à plat CSV.
# Usage: python -I 02_fetch_eurostat.py <dossier_sortie>
# Chaque requête est conservée en JSON brut + CSV long ; l'URL est écrite dans le CSV de journal.
import sys, os, json, csv, itertools, datetime, hashlib
import requests

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
BASE = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
GEOS = ['FR', 'DE', 'NL', 'SE', 'IT', 'ES', 'DK', 'BE', 'EU27_2020', 'EA20']
Q = {
    # taux d'emploi par sexe et âge (enquête Forces de travail)
    'lfsa_ergan': dict(unit='PC', citizen='TOTAL', sex=['T', 'M', 'F'],
                       age=['Y15-24', 'Y25-54', 'Y55-64', 'Y20-64', 'Y15-64', 'Y60-64', 'Y55-59']),
    # taux de chômage par âge
    'une_rt_a': dict(unit='PC_ACT', sex='T', age=['Y15-74', 'Y15-24', 'Y25-74']),
    # taux d'emploi par âge (y compris UK historique)
    'lfsa_ergaed': dict(unit='PC', sex='T', isced11='TOTAL', age=['Y20-64', 'Y55-64']),
    # population au 1er janvier par grands groupes d'âge (indicateurs de structure)
    'demo_pjanind': dict(indic_de=['OLDDEP1', 'PC_Y65_MAX', 'PC_Y15_64', 'PC_Y80_MAX', 'MEDAGEPOP']),
    # fécondité
    'demo_find': dict(indic_de=['TOTFERRT']),
    # espérance de vie à 65 ans et à la naissance
    'demo_mlexpec': dict(unit='YR', sex=['T', 'M', 'F'], age=['Y_LT1', 'Y65']),
    # PIB et heures - productivité (nama_10_lp_ulc)
    'nama_10_lp_ulc': dict(unit=['EUR_HW_CP', 'PC_EU27_2020_HW_PPS', 'I20'], na_item=['NLPR_HW', 'RLPR_HW']),
    # emploi en milliers par âge (pour reconstituer les populations par âge = emploi / taux)
    'lfsa_egan': dict(unit='THS_PER', citizen='TOTAL', sex='T',
                      age=['Y15-24', 'Y25-54', 'Y55-64', 'Y15-64', 'Y60-64', 'Y55-59']),
    # dépenses de protection sociale : vieillesse et maladie en % du PIB (SESPROS)
    'spr_exp_func': dict(unit='PC_GDP', spdepb='TOTAL', spdepm='TOTAL', spfunc=['OLD', 'SICK', 'UNEMPLOY', 'DIS']),
}
if len(sys.argv) > 2:
    Q = {k: v for k, v in Q.items() if k in sys.argv[2].split(',')}

log = []
for ds, params in Q.items():
    p = [('format', 'JSON'), ('lang', 'EN')]
    for k, v in params.items():
        for x in (v if isinstance(v, list) else [v]):
            p.append((k, x))
    for g in GEOS + (['UK'] if ds in ('lfsa_ergan', 'une_rt_a', 'lfsa_ergaed', 'demo_pjanind', 'demo_find', 'demo_mlexpec', 'nama_10_lp_ulc') else []):
        p.append(('geo', g))
    r = requests.get(BASE + ds, params=p, timeout=120)
    url = r.url
    status = r.status_code
    raw = r.content
    with open(os.path.join(OUT, ds + '.json'), 'wb') as fh:
        fh.write(raw)
    n = 0
    if status == 200:
        js = r.json()
        dims = js['id']
        size = js['size']
        cats = []
        for d in dims:
            idx = js['dimension'][d]['category']['index']
            inv = sorted(idx.items(), key=lambda kv: kv[1])
            cats.append([k for k, _ in inv])
        vals = js['value']
        with open(os.path.join(OUT, ds + '.csv'), 'w', newline='', encoding='utf-8') as fo:
            w = csv.writer(fo, delimiter=';')
            w.writerow(dims + ['value', 'status'])
            for i, combo in enumerate(itertools.product(*cats)):
                v = vals.get(str(i)) if isinstance(vals, dict) else (vals[i] if i < len(vals) else None)
                if v is None:
                    continue
                st = js.get('status', {}).get(str(i), '') if isinstance(js.get('status'), dict) else ''
                w.writerow(list(combo) + [v, st])
                n += 1
        upd = js.get('updated', '')
    else:
        upd = ''
    log.append([ds, url, status, len(raw), hashlib.sha256(raw).hexdigest(), upd, n,
                datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')])
    print(ds, status, n, upd)

jp = os.path.join(OUT, 'journal_eurostat.csv')
new = not os.path.exists(jp)
with open(jp, 'a', newline='', encoding='utf-8') as fo:
    w = csv.writer(fo, delimiter=';')
    if new: w.writerow(['dataset', 'url', 'http', 'octets', 'sha256', 'maj_eurostat', 'n_valeurs', 'extraction_utc'])
    w.writerows(log)
