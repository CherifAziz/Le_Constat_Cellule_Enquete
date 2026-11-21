# -*- coding: utf-8 -*-
"""A18 partie 2 - inventaire des series disponibles dans la base commune (lecture seule)."""
import csv, collections, os
C = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\commun"
for f in ("base_insee_dep_rec_pctPIB.csv", "base_insee_solde_sous_secteurs.csv", "base_insee_dette_sous_secteurs.csv"):
    s = collections.Counter()
    with open(os.path.join(C, f), encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            s[(r["feuille"], r["unite"], r["serie"])] += 1
    print("===", f)
    for k, v in s.items():
        print("  ", k, v)
for f in ("eurostat_gov_10a_main.csv", "eurostat_gov_10a_exp.csv", "eurostat_gov_10a_taxag.csv", "eurostat_gov_10dd_edpt1.csv"):
    s = collections.defaultdict(set)
    with open(os.path.join(C, f), encoding="utf-8") as h:
        for r in csv.DictReader(h):
            s["unit"].add(r["unit"]); s["sector"].add(r["sector"]); s["na_item"].add(r["na_item"]); s["geo"].add(r["geo"])
            s["time"].add(r["time"])
            if "cofog99" in r:
                s["cofog99"].add(r["cofog99"])
    print("===", f)
    for k, v in s.items():
        v = sorted(v)
        print("  ", k, v if len(v) < 40 else (v[:5], "...", v[-5:], len(v)))
