# A18 - téléchargement API Eurostat (JSON-stat brut) + manifeste
# Usage : python -I a18_04_telecharge_eurostat.py <dossier_sources> <manifeste.csv>
import sys, os, hashlib, datetime, requests
src, man = sys.argv[1], sys.argv[2]
EU27 = "BE BG CZ DK DE EE IE EL ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE".split()
EA20 = "BE DE EE IE EL ES FR HR IT CY LV LT LU MT NL AT PT SI SK FI".split()
base = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
def q(ds, params):
    parts = []
    for k, v in params.items():
        for x in (v if isinstance(v, list) else [v]):
            parts.append(f"{k}={x}")
    return base + ds + "?format=JSON&lang=EN&" + "&".join(parts)
jobs = {
 "eurostat_taxag_EU27_PO_2019_2025.json": q("gov_10a_taxag", {"freq": "A", "unit": "PC_GDP", "sector": "S13_S212",
     "na_item": ["D2_D5_D91_D61_M_D995", "D2_D5_D91_D61_M_D612_M_D614_M_D995"], "geo": EU27 + ["EU27_2020", "EA20"],
     "time": [str(y) for y in range(2019, 2026)]}),
 "eurostat_cofog_EA20_MIOEUR_2023_2024.json": q("gov_10a_exp", {"freq": "A", "unit": "MIO_EUR", "sector": "S13", "na_item": "TE",
     "geo": EA20 + ["EA20"], "time": ["2023", "2024"]}),
 "eurostat_main_EA20_MIOEUR_2024_2025.json": q("gov_10a_main", {"freq": "A", "unit": "MIO_EUR", "sector": "S13",
     "na_item": ["TE", "TR", "B9", "D41PAY", "B1GQ"], "geo": EA20 + ["EA20"], "time": ["2023", "2024", "2025"]}),
 "eurostat_nama_gdp_EA20_MIOEUR_2023_2025.json": q("nama_10_gdp", {"freq": "A", "unit": "CP_MEUR", "na_item": "B1GQ",
     "geo": EA20 + ["EA20"], "time": ["2023", "2024", "2025"]}),
 "eurostat_main_SE_1995_2000.json": q("gov_10a_main", {"freq": "A", "unit": "PC_GDP", "sector": "S13", "na_item": ["B9", "TE", "TR"],
     "geo": "SE", "time": [str(y) for y in range(1995, 2001)]}),
}
with open(man, "a", encoding="utf-8") as m:
    for fn, url in jobs.items():
        r = requests.get(url, timeout=120)
        b = r.content
        p = os.path.join(src, fn); open(p, "wb").write(b)
        h = hashlib.sha256(b).hexdigest()
        m.write(f"{fn};{url};requests API Eurostat (HTTP {r.status_code});{datetime.datetime.utcnow():%Y-%m-%dT%H:%MZ};{len(b)};{h}\n")
        print(fn, r.status_code, len(b))
