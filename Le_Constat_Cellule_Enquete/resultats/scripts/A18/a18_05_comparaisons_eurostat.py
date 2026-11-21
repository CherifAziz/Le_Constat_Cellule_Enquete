# A18 - comparaisons européennes (Eurostat, notification d'octobre 2026 ; extraction 20/11/2026)
# Usage : python -I a18_05_comparaisons_eurostat.py <dossier_commun> <dossier_sources_A18>
import sys, os, json, csv, itertools
dc, ds = sys.argv[1], sys.argv[2]

def jstat(path):
    j = json.load(open(path, encoding="utf-8"))
    ids, size = j["id"], j["size"]
    cats = []
    for d in ids:
        idx = j["dimension"][d]["category"]["index"]
        inv = sorted(idx.items(), key=lambda kv: kv[1])
        cats.append([k for k, _ in inv])
    out = {}
    for flat, v in j["value"].items():
        flat = int(flat); key = []
        for s in reversed(size):
            key.append(flat % s); flat //= s
        key = tuple(c[i] for c, i in zip(cats, reversed(key)))
        out[key] = v
    return ids, out

def comm(csvname):
    d = {}
    for r in csv.DictReader(open(os.path.join(dc, csvname), encoding="utf-8")):
        if r["value"] not in ("", None):
            d[tuple(r[k] for k in r if k not in ("value", "status", "freq"))] = float(r["value"])
    return d

print("=== 1. Prélèvements obligatoires (impôts + cotisations sociales nettes), % PIB, EU27, gov_10a_taxag")
ids, T = jstat(os.path.join(ds, "eurostat_taxag_EU27_PO_2019_2025.json"))
for item in ["D2_D5_D91_D61_M_D995", "D2_D5_D91_D61_M_D612_M_D614_M_D995"]:
    for y in ["2023", "2024", "2025"]:
        vals = {k[ids.index("geo")]: v for k, v in T.items() if k[ids.index("na_item")] == item and k[ids.index("time")] == y}
        rk = sorted(((g, v) for g, v in vals.items() if g not in ("EU27_2020", "EA20")), key=lambda t: -t[1])
        print(item, y, "n=%d" % len(rk), rk[:5], "EA20", vals.get("EA20"), "EU27", vals.get("EU27_2020"))

print("=== 2. France vs zone euro 2025 (gov_10a_main, PC_GDP, base commune)")
M = comm("eurostat_gov_10a_main.csv")
def g(unit, sector, item, geo, y): return M.get((unit, sector, item, geo, str(y)))
for y in [2024, 2025]:
    fr = {i: g("PC_GDP", "S13", i, "FR", y) for i in ["TE", "TR", "B9", "D41PAY"]}
    ea = {i: g("PC_GDP", "S13", i, "EA20", y) for i in ["TE", "TR", "B9", "D41PAY"]}
    print(y, "FR", fr, "EA20", ea, "écarts FR-EA20 TE %.2f TR %.2f B9 %.2f" % (fr["TE"] - ea["TE"], fr["TR"] - ea["TR"], fr["B9"] - ea["B9"]))
ids2, A = jstat(os.path.join(ds, "eurostat_main_EA20_MIOEUR_2024_2025.json"))
ids3, G = jstat(os.path.join(ds, "eurostat_nama_gdp_EA20_MIOEUR_2023_2025.json"))
gdp = {(k[ids3.index("geo")], k[ids3.index("time")]): v for k, v in G.items()}
def a(item, geo, y): return A.get(tuple({"freq": "A", "unit": "MIO_EUR", "sector": "S13", "na_item": item, "geo": geo, "time": y}[d] for d in ids2))
for y in ["2024", "2025"]:
    res = {}
    for i in ["TE", "TR", "B9"]:
        ea, fr = a(i, "EA20", y), a(i, "FR", y)
        if ea is None or fr is None: continue
        res[i] = (100 * fr / gdp[("FR", y)], 100 * (ea - fr) / (gdp[("EA20", y)] - gdp[("FR", y)]))
    print(y, "FR vs EA20 hors France (MIO_EUR / PIB nama):", {k: (round(v[0], 2), round(v[1], 2), round(v[0] - v[1], 2)) for k, v in res.items()})

print("=== 3. COFOG : écart FR - EA20 par division, % PIB (gov_10a_exp, base commune, PC_GDP)")
E = comm("eurostat_gov_10a_exp.csv")
def e(cof, geo, y): return E.get(("PC_GDP", "S13", cof, "TE", geo, str(y)))
years = sorted({int(k[-1]) for k in E if k[2] == "TOTAL" and k[4] == "FR"})
print("années COFOG disponibles FR :", years[-3:])
yc = years[-1]
divs = ["GF01", "GF02", "GF03", "GF04", "GF05", "GF06", "GF07", "GF08", "GF09", "GF10"]
tot_gap = e("TOTAL", "FR", yc) - e("TOTAL", "EA20", yc)
print(yc, "TOTAL FR %.1f EA20 %.1f écart %.2f" % (e("TOTAL", "FR", yc), e("TOTAL", "EA20", yc), tot_gap))
for dv in divs:
    gp = e(dv, "FR", yc) - e(dv, "EA20", yc)
    print(dv, "FR %.1f EA20 %.1f écart %+.2f part %.0f%%" % (e(dv, "FR", yc), e(dv, "EA20", yc), gp, 100 * gp / tot_gap))
sp_h = (e("GF10", "FR", yc) - e("GF10", "EA20", yc)) + (e("GF07", "FR", yc) - e("GF07", "EA20", yc))
print("GF10+GF07 écart %.2f = %.0f%% de l'écart total" % (sp_h, 100 * sp_h / tot_gap))
for sub in ["GF1001", "GF1002", "GF1003", "GF1004", "GF1005", "GF1006", "GF1007", "GF1008"]:
    print(sub, e(sub, "FR", yc), e(sub, "EA20", yc))
print("=== 4. Part des fonctions dans la dépense FR", yc)
te = e("TOTAL", "FR", yc)
for dv in ["GF1002", "GF1003", "GF07", "GF10", "GF09", "GF02", "GF03", "GF01", "GF04", "GF0107"]:
    v = e(dv, "FR", yc)
    print(dv, v, "sur 100 € : %.1f" % (100 * v / te) if v is not None else "")
v3 = e("GF10", "FR", yc) + e("GF07", "FR", yc)
print("GF10 + GF07 sur 100 € : %.1f" % (100 * v3 / te))
print("=== 4b. COFOG hors France (MIO_EUR)", )
ids4, C = jstat(os.path.join(ds, "eurostat_cofog_EA20_MIOEUR_2023_2024.json"))
def c(cof, geo, y): return C.get(tuple({"freq": "A", "unit": "MIO_EUR", "sector": "S13", "cofog99": cof, "na_item": "TE", "geo": geo, "time": y}[d] for d in ids4))
y = str(yc)
gx = gdp[("EA20", y)] - gdp[("FR", y)]
totx = 100 * (c("TOTAL", "EA20", y) - c("TOTAL", "FR", y)) / gx
totf = 100 * c("TOTAL", "FR", y) / gdp[("FR", y)]
print("TOTAL FR %.2f EA20horsFR %.2f écart %.2f" % (totf, totx, totf - totx))
s = 0
for dv in divs:
    fx = 100 * c(dv, "FR", y) / gdp[("FR", y)]; xx = 100 * (c(dv, "EA20", y) - c(dv, "FR", y)) / gx
    print(dv, "écart vs EA hors FR %+.2f part %.0f%%" % (fx - xx, 100 * (fx - xx) / (totf - totx)))
print("=== 5. Allemagne et Italie (edpt1 / main, base commune)")
D = comm("eurostat_gov_10dd_edpt1.csv")
keys = sorted({k[2] for k in D}); print("items edpt1:", keys)
for geo in ["DE", "IT", "FR"]:
    for yy in range(2012, 2026):
        b9 = D.get(("PC_GDP", "S13", "B9", geo, str(yy))); gd = D.get(("PC_GDP", "S13", "GD", geo, str(yy)))
        print(geo, yy, "B9", b9, "dette", gd, "mois %.2f" % (gd * 12 / 100) if gd else "")
for geo in ["IT", "FR", "EA20"]:
    b9 = g("PC_GDP", "S13", "B9", geo, 2025); i = g("PC_GDP", "S13", "D41PAY", geo, 2025)
    print(geo, 2025, "B9", b9, "D41", i, "solde primaire %.2f" % (b9 + i))
print("=== 6. Combler par l'impôt ou la dépense (2025)")
fr_te, ea_te = g("PC_GDP", "S13", "TE", "FR", 2025), g("PC_GDP", "S13", "TE", "EA20", 2025)
b9 = g("PC_GDP", "S13", "B9", "FR", 2025)
po = {k[ids.index("geo")]: v for k, v in T.items() if k[ids.index("na_item")] == "D2_D5_D91_D61_M_D995" and k[ids.index("time")] == "2025"}
print("PO FR 2025 %.1f + déficit %.1f = %.1f ; max autre pays %s" % (po["FR"], -b9, po["FR"] - b9, max(((gg, v) for gg, v in po.items() if gg not in ("FR", "EU27_2020", "EA20")), key=lambda t: t[1])))
print("Dépense FR %.1f - déficit %.1f = %.1f vs EA20 %.1f" % (fr_te, -b9, fr_te + b9, ea_te))
print("=== 7. Suède")
ids5, S = jstat(os.path.join(ds, "eurostat_main_SE_1995_2000.json"))
for k, v in sorted(S.items(), key=lambda kv: (kv[0][ids5.index("na_item")], kv[0][ids5.index("time")])):
    print(k[ids5.index("na_item")], k[ids5.index("time")], v)
