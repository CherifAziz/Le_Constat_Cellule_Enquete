"""S07 - extraction Eurostat (API JSON-stat) : croissance du PIB en volume, dette brute,
dépenses et recettes totales des APU, pour EL, PT, IE, ES, FR, 2008-2019.
Usage : python -I eurostat_programmes.py <dossier_sources> <sortie_csv>
Écrit les JSON bruts dans <dossier_sources> et une table longue (geo;serie;annee;valeur) en CSV."""
import sys, json, csv, os, requests

src, out = sys.argv[1], sys.argv[2]
GEOS = ["EL", "PT", "IE", "ES", "FR"]
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
REQS = {
    "pib_vol_pct": ("nama_10_gdp", {"unit": "CLV_PCH_PRE", "na_item": "B1GQ"}),
    "dette_pct_pib": ("gov_10dd_edpt1", {"unit": "PC_GDP", "sector": "S13", "na_item": "GD"}),
    "depenses_pct_pib": ("gov_10a_main", {"unit": "PC_GDP", "sector": "S13", "na_item": "TE"}),
    "recettes_pct_pib": ("gov_10a_main", {"unit": "PC_GDP", "sector": "S13", "na_item": "TR"}),
    "solde_pct_pib": ("gov_10a_main", {"unit": "PC_GDP", "sector": "S13", "na_item": "B9"}),
}
rows = []
for serie, (ds, flt) in REQS.items():
    params = [("format", "JSON"), ("lang", "en"), ("sinceTimePeriod", "2008"), ("untilTimePeriod", "2019")]
    params += [(k, v) for k, v in flt.items()] + [("geo", g) for g in GEOS]
    r = requests.get(BASE + ds, params=params, timeout=120)
    r.raise_for_status()
    fn = os.path.join(src, f"eurostat_{serie}.json")
    open(fn, "wb").write(r.content)
    j = r.json()
    dims = j["id"]; sizes = j["size"]
    idx = {d: j["dimension"][d]["category"]["index"] for d in dims}
    # strides
    strides = []
    s = 1
    for sz in reversed(sizes):
        strides.insert(0, s); s *= sz
    inv = {d: {v: k for k, v in idx[d].items()} for d in dims}
    for key, val in j["value"].items():
        k = int(key); coords = {}
        for d, st, sz in zip(dims, strides, sizes):
            coords[d] = inv[d][(k // st) % sz]
        rows.append((coords["geo"], serie, coords["time"], val))
rows.sort()
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["geo", "serie", "annee", "valeur"])
    w.writerows(rows)
print(len(rows), "lignes ->", out)
