# -*- coding: utf-8 -*-
"""A07 - Comparaisons internationales (Eurostat, base commune extraite le 20/11/2026, lecture seule).
Usage : python -I 05_comparaisons_eurostat.py <dossier donnees>
- gov_10a_main : TE, TR, B9, D41PAY (S13, MIO_EUR et PC_GDP)
- gov_10dd_edpt1 : GD (dette brute Maastricht, MIO_EUR et PC_GDP)
Calculs :
 (1) solde primaire = B9 + D41PAY ; depense primaire = TE - D41PAY (en % du PIB)
 (2) taux apparent i_t = D41PAY_t / GD_{t-1}
 (3) Fenetre de taux bas : economie d'interets 2015-2021 par rapport a deux contrefactuels
     A : taux apparent fige a son niveau de 2014 : sum_t (i_2014 - i_t) * GD_{t-1}
     B : charge d'interets figee a son ratio au PIB de 2014 : sum_t (int/PIB_2014 - int/PIB_t) * PIB_t
     (contrefactuels comptables statiques : ni la dette ni le PIB ne reagissent ; borne haute de l'economie)
 (4) Variation du solde primaire et de la depense primaire 2014->2019 et 2014->2021.
Sorties : comparaisons_pays_1995_2025.csv ; fenetre_taux_bas_2015_2021.csv
"""
import sys, os, csv
D = sys.argv[1]
COM = os.path.join(D, "commun"); A07 = os.path.join(D, "A07")
GEOS = ["FR", "DE", "IT", "ES", "PT", "BE", "NL", "AT", "SE", "EA20"]
M = {}
for r in csv.DictReader(open(os.path.join(COM, "eurostat_gov_10a_main.csv"), encoding="utf-8")):
    if r["sector"] == "S13" and r["geo"] in GEOS and r["na_item"] in ("TE", "TR", "B9", "D41PAY") and r["value"] not in ("", None):
        M[(r["geo"], r["unit"], r["na_item"], int(r["time"]))] = float(r["value"])
for r in csv.DictReader(open(os.path.join(COM, "eurostat_gov_10dd_edpt1.csv"), encoding="utf-8")):
    if r["sector"] == "S13" and r["geo"] in GEOS and r["na_item"] in ("GD", "B9", "D41PAY") and r["value"] not in ("", None):
        M[(r["geo"], r["unit"], "EDP_" + r["na_item"], int(r["time"]))] = float(r["value"])

def g(geo, unit, item, y):
    return M.get((geo, unit, item, y))

rows = []
for geo in GEOS:
    for y in range(1995, 2026):
        te, b9, it = g(geo, "PC_GDP", "TE", y), g(geo, "PC_GDP", "B9", y), g(geo, "PC_GDP", "D41PAY", y)
        gd, gdm, gdm0 = g(geo, "PC_GDP", "EDP_GD", y), g(geo, "MIO_EUR", "EDP_GD", y), g(geo, "MIO_EUR", "EDP_GD", y - 1)
        itm = g(geo, "MIO_EUR", "D41PAY", y)
        gdp = gdm / gd * 100 if gdm and gd else None
        rows.append(dict(geo=geo, annee=y, depenses_pct=te, solde_pct=b9, interets_pct=it,
                         solde_primaire_pct=round(b9 + it, 2) if b9 is not None and it is not None else "",
                         depense_primaire_pct=round(te - it, 2) if te is not None and it is not None else "",
                         dette_pct=gd, dette_mio=gdm, pib_mio=round(gdp, 1) if gdp else "",
                         interets_mio=itm,
                         taux_apparent_pct=round(100 * itm / gdm0, 3) if itm and gdm0 else ""))
with open(os.path.join(A07, "comparaisons_pays_1995_2025.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter=";"); w.writeheader(); w.writerows(rows)
R = {(r["geo"], r["annee"]): r for r in rows}

out = []
for geo in GEOS:
    try:
        i14 = R[(geo, 2014)]["taux_apparent_pct"] / 100
        s14 = R[(geo, 2014)]["interets_pct"] / 100
        ecoA = sum((i14 - R[(geo, y)]["taux_apparent_pct"] / 100) * R[(geo, y - 1)]["dette_mio"] for y in range(2015, 2022)) / 1000
        ecoB = sum((s14 - R[(geo, y)]["interets_pct"] / 100) * R[(geo, y)]["pib_mio"] for y in range(2015, 2022)) / 1000
        ecoA_pct = sum((i14 - R[(geo, y)]["taux_apparent_pct"] / 100) * R[(geo, y - 1)]["dette_mio"] / R[(geo, y)]["pib_mio"] * 100 for y in range(2015, 2022))
        f = lambda y, k: R[(geo, y)][k]
        out.append(dict(geo=geo, taux_apparent_2014=round(100 * i14, 2), taux_apparent_2019=f(2019, "taux_apparent_pct"),
                        taux_apparent_2021=f(2021, "taux_apparent_pct"),
                        interets_pct_2014=f(2014, "interets_pct"), interets_pct_2019=f(2019, "interets_pct"), interets_pct_2021=f(2021, "interets_pct"),
                        economie_A_md_2015_2021=round(ecoA, 1), economie_A_somme_pts_PIB=round(ecoA_pct, 2),
                        economie_B_md_2015_2021=round(ecoB, 1),
                        solde_prim_2014=f(2014, "solde_primaire_pct"), solde_prim_2019=f(2019, "solde_primaire_pct"),
                        var_solde_prim_14_19=round(f(2019, "solde_primaire_pct") - f(2014, "solde_primaire_pct"), 2),
                        dep_prim_2014=f(2014, "depense_primaire_pct"), dep_prim_2019=f(2019, "depense_primaire_pct"),
                        var_dep_prim_14_19=round(f(2019, "depense_primaire_pct") - f(2014, "depense_primaire_pct"), 2),
                        var_recettes_14_19=round(M[(geo, "PC_GDP", "TR", 2019)] - M[(geo, "PC_GDP", "TR", 2014)], 2),
                        var_interets_14_19=round(f(2019, "interets_pct") - f(2014, "interets_pct"), 2),
                        solde_2014=f(2014, "solde_pct"), solde_2019=f(2019, "solde_pct"),
                        dette_2014=f(2014, "dette_pct"), dette_2019=f(2019, "dette_pct"), dette_2021=f(2021, "dette_pct")))
    except (KeyError, TypeError) as e:
        print("manque", geo, e)
with open(os.path.join(A07, "fenetre_taux_bas_2015_2021.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter=";"); w.writeheader(); w.writerows(out)
for o in out:
    print(o)
print()
for geo in ["FR", "IT", "DE", "ES", "BE", "PT", "EA20"]:
    print(geo, [(y, R[(geo, y)]["solde_primaire_pct"], R[(geo, y)]["interets_pct"]) for y in (2019, 2022, 2023, 2024, 2025)])
