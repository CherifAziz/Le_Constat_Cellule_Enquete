# -*- coding: utf-8 -*-
"""A03 - tests complementaires : (1) ventilations recettes/depenses avec les series Insee 'hors elements imputes'
(cotisations imputees, production pour emploi propre, credits d'impot ; neutralise le traitement CICE) ;
(2) ecart du PIB en volume a la tendance 2001-2007 (Eurostat nama_10_gdp, CLV_PCH_PRE). Sortie : donnees/A03/tests_complementaires.txt
"""
import os, csv, json
ICI = os.path.dirname(os.path.abspath(__file__))
A03 = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03"))
COM = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "commun"))
S = {}
for r in csv.DictReader(open(os.path.join(COM, "base_insee_dep_rec_pctPIB.csv"), encoding="utf-8-sig"), delimiter=";"):
    S[(r["serie"][:40], int(r["annee"]))] = float(r["valeur"])
k = sorted({s for s, _ in S})
dep_hei = [s for s in k if s.startswith("dont dépenses hors")][0]
rec_hei = [s for s in k if s.startswith("dont recettes hors")][0]
T = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(A03, "table_annuelle_A03.csv"), encoding="utf-8-sig"), delimiter=";")}
out = []
out.append("== Ventilations (pts de PIB) : series totales vs hors elements imputes (HEI)")
for a0, a1 in [(2000, 2007), (2005, 2015), (2007, 2019), (2010, 2015), (2017, 2024), (2019, 2024), (2019, 2025), (2017, 2019), (2018, 2019)]:
    dr = float(T[a1]["rec_pct"]) - float(T[a0]["rec_pct"]); dd = float(T[a1]["dep_pct"]) - float(T[a0]["dep_pct"])
    di = float(T[a1]["interets_pct"]) - float(T[a0]["interets_pct"])
    drh = S[(rec_hei, a1)] - S[(rec_hei, a0)]; ddh = S[(dep_hei, a1)] - S[(dep_hei, a0)]
    out.append("%d->%d | total: rec %+.2f dep %+.2f (primaires %+.2f) | HEI: rec %+.2f dep %+.2f (primaires %+.2f) | interets %+.2f" % (a0, a1, dr, dd, dd - di, drh, ddh, ddh - di, di))
out.append("Niveaux HEI : " + " ".join("%d dep %.1f rec %.1f;" % (a, S[(dep_hei, a)], S[(rec_hei, a)]) for a in (2005, 2006, 2007, 2015, 2017, 2018, 2019, 2024, 2025)))
# (2) tendance du PIB en volume
js = json.load(open(os.path.join(A03, "sources", "eurostat_nama_10_gdp.json"), encoding="utf-8"))
dims, sizes = js["id"], js["size"]
idx = {d: {v: kk for kk, v in js["dimension"][d]["category"]["index"].items()} for d in dims}
g = {}
for flat, val in js["value"].items():
    flat = int(flat); co = []
    for s in reversed(sizes):
        co.append(flat % s); flat //= s
    kd = dict(zip(dims, [idx[d][c] for d, c in zip(dims, reversed(co))]))
    if kd["unit"] == "CLV_PCH_PRE" and kd["geo"] == "FR":
        g[int(kd["time"])] = val
niv = {2000: 100.0}
for a in range(2001, 2026):
    niv[a] = niv[a - 1] * (1 + g[a] / 100)
tend = (niv[2007] / niv[2000]) ** (1 / 7) - 1
out.append("== PIB en volume (indice 2000=100) ; tendance 2001-2007 = %.2f %%/an" % (100 * tend))
for a in (2007, 2009, 2010, 2012, 2015, 2019, 2020, 2022, 2025):
    t = niv[2007] * (1 + tend) ** (a - 2007)
    out.append("%d niveau %.1f tendance %.1f ecart %+.1f %%" % (a, niv[a], t, 100 * (niv[a] / t - 1)))
tend2 = (niv[2019] / niv[2015]) ** (1 / 4) - 1
out.append("tendance 2016-2019 = %.2f %%/an" % (100 * tend2))
for a in (2022, 2025):
    t = niv[2019] * (1 + tend2) ** (a - 2019)
    out.append("%d ecart a la tendance 2016-2019 prolongee %+.1f %%" % (a, 100 * (niv[a] / t - 1)))
open(os.path.join(A03, "tests_complementaires.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
