# -*- coding: utf-8 -*-
"""A07 - Ecarts de taux a 10 ans (taux de convergence BCE, serie IRS M.xx.L.L40.CI.0000.EUR.N.Z, moyennes mensuelles).
Usage : python -I 04_ecarts_de_taux.py <dossier A07>
Sorties : ecarts_taux_mensuels.csv (1986-2026), ecarts_taux_annuels.csv, et impression des dates clefs.
"""
import sys, os, csv, collections
A07 = sys.argv[1]
SRC = os.path.join(A07, "sources")
GEOS = ["FR", "DE", "IT", "ES", "PT", "BE", "NL", "AT", "IE", "GR", "FI"]
S = {}
for g in GEOS:
    for r in csv.DictReader(open(os.path.join(SRC, f"ecb_IRS_M_{g}.csv"), encoding="utf-8")):
        if r["OBS_VALUE"]:
            S.setdefault(r["TIME_PERIOD"], {})[g] = float(r["OBS_VALUE"])
months = sorted(S)
with open(os.path.join(A07, "ecarts_taux_mensuels.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["mois"] + GEOS + ["FR_DE_pb", "IT_DE_pb", "FR_IT_pb", "ES_DE_pb", "PT_DE_pb", "BE_DE_pb"])
    for m in months:
        v = S[m]
        sp = lambda a, b: round(100 * (v[a] - v[b]), 1) if a in v and b in v else ""
        w.writerow([m] + [v.get(g, "") for g in GEOS] + [sp("FR", "DE"), sp("IT", "DE"), sp("FR", "IT"), sp("ES", "DE"), sp("PT", "DE"), sp("BE", "DE")])
ann = collections.defaultdict(lambda: collections.defaultdict(list))
for m in months:
    for g, x in S[m].items():
        ann[m[:4]][g].append(x)
with open(os.path.join(A07, "ecarts_taux_annuels.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["annee", "n_mois_FR"] + GEOS + ["FR_DE_pb", "IT_DE_pb", "FR_IT_pb"])
    for y in sorted(ann):
        a = {g: sum(v) / len(v) for g, v in ann[y].items()}
        sp = lambda p, q: round(100 * (a[p] - a[q]), 1) if p in a and q in a else ""
        w.writerow([y, len(ann[y].get("FR", []))] + [round(a[g], 3) if g in a else "" for g in GEOS] + [sp("FR", "DE"), sp("IT", "DE"), sp("FR", "IT")])
KEY = ["1992-09", "1993-07", "1995-03", "1999-01", "2008-12", "2011-11", "2012-07", "2014-12", "2016-08", "2019-08", "2020-03",
       "2021-12", "2022-06", "2022-10", "2023-10", "2024-01", "2024-05", "2024-06", "2024-07", "2024-11", "2024-12",
       "2025-06", "2025-09", "2025-10", "2026-01", "2026-06", "2026-08", "2026-09", "2026-10"]
for m in KEY:
    if m in S:
        v = S[m]
        print(m, {g: v.get(g) for g in ["FR", "DE", "IT", "ES", "BE", "PT"]},
              "FR-DE", round(100 * (v["FR"] - v["DE"])), "FR-IT", round(100 * (v["FR"] - v["IT"])) if "IT" in v else "")
# premier mois ou FR >= IT depuis 1993
cross = [m for m in months if "IT" in S[m] and S[m]["FR"] >= S[m]["IT"]]
print("Mois ou FR >= IT :", cross)
