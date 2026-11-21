# -*- coding: utf-8 -*-
"""A05 travail 4 - Comparabilité internationale de l'écart de dépense.
(1) Écart total 2025 (gov_10a_main, recalculé sur PIB nama_10_gdp) : FR vs EA20, EA20 hors FR, voisins.
(2) OCDE SOCX 2019 (année de référence pré-Covid ; 2021 en sensibilité) :
    public brut (ES10) -> + privé obligatoire (ES20) -> + privé volontaire (ES30, via ES20_30) -> net total (ES50) ;
    net public (ES40). Les corrections sont SYMÉTRIQUES (appliquées à chaque pays par l'OCDE).
(3) Standardisation démographique de la vieillesse (COFOG GF1002 / part des 65 ans et plus, Eurostat demo_pjanind).
(4) Éléments propres à la France (non symétrisables avec les données en main) : montants seulement.
Sorties : A05_socx_corrections.csv ; A05_vieillesse_par_65plus.csv ; A05_ecart_total_2025.csv
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *

# (1) écart total 2025
gdp = lire_jsonstat(os.path.join(SRC, "eurostat_nama_10_gdp.json"))
PIB = {(x["geo"], int(x["time"])): x["value"] for x in gdp if x["unit"] == "CP_MEUR"}
M = {}
for r in lire_csv_commun("eurostat_gov_10a_main.csv"):
    if r["unit"] == "MIO_EUR" and r["value"] and r["sector"] == "S13":
        M[(r["geo"], r["na_item"], int(r["time"]))] = float(r["value"])
def ratio(g, it, y):
    if g == "EA20xFR":
        return 100 * (M[("EA20", it, y)] - M[("FR", it, y)]) / (PIB[("EA20", y)] - PIB[("FR", y)])
    return 100 * M[(g, it, y)] / PIB[(g, y)]
et = []
for y in (2019, 2024, 2025):
    for g in ["EA20", "EA20xFR", "EU27_2020", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT"]:
        try:
            et.append([y, g, ratio("FR", "TE", y), ratio(g, "TE", y), ratio("FR", "TE", y) - ratio(g, "TE", y),
                       ratio("FR", "TR", y), ratio(g, "TR", y), ratio("FR", "TR", y) - ratio(g, "TR", y),
                       ratio("FR", "B9", y) - ratio(g, "B9", y)])
        except KeyError:
            pass
ecrire_csv("A05_ecart_total_2025.csv", ["annee", "comparateur", "TE_FR", "TE_comp", "ecart_TE", "TR_FR", "TR_comp", "ecart_TR", "ecart_solde_B9"], et)

# (2) SOCX
r = list(csv.DictReader(open(os.path.join(SRC, "oecd_DF_SOCX_AGG.csv"), encoding="utf-8")))
S = {}
for x in r:
    if x["SPENDING_TYPE"] == "_T" and x["OBS_VALUE"]:
        S[(x["REF_AREA"], x["EXPEND_SOURCE"], x["PROGRAMME_TYPE"], x["TIME_PERIOD"])] = float(x["OBS_VALUE"])
net = list(csv.DictReader(open(os.path.join(SRC, "oecd_DF_NET_GDP.csv"), encoding="utf-8")))
for x in net:
    if x["OBS_VALUE"]:
        S.setdefault((x["REF_AREA"], "ES50", "_T", x["TIME_PERIOD"]), float(x["OBS_VALUE"]))
PAYS = ["FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "SWE", "DNK", "FIN", "AUT"]
lignes = []
for an in ("2019", "2021"):
    vals = {}
    for p in PAYS + ["OECD"]:
        pub = S.get((p, "ES10", "_T", an)); mand = S.get((p, "ES20", "_T", an)); privt = S.get((p, "ES20_30", "_T", an))
        netpub = S.get((p, "ES40", "_T", an)); nettot = S.get((p, "ES50", "_T", an))
        vol = privt - mand if privt is not None and mand is not None else None
        vals[p] = (pub, mand, vol, (pub + privt) if pub is not None and privt is not None else None, netpub, nettot)
        lignes.append([an, p, pub, mand, vol, vals[p][3], netpub, nettot])
    # moyenne simple des 9 comparateurs UE
    comp = [p for p in PAYS if p != "FRA"]
    for i, lab in enumerate(["public_brut", "prive_obligatoire", "prive_volontaire", "brut_total", "net_public", "net_total"]):
        xs = [vals[p][i] for p in comp if vals[p][i] is not None]
        moy = sum(xs) / len(xs) if xs else None
        f = vals["FRA"][i]
        lignes.append([an, "ECART_FR_moins_moyenne9_" + lab, f, moy, (f - moy) if f is not None and moy is not None else "", len(xs), "", ""])
    for p in comp:
        e = [(vals["FRA"][i] - vals[p][i]) if vals["FRA"][i] is not None and vals[p][i] is not None else "" for i in range(6)]
        lignes.append([an, "ECART_FR_moins_" + p] + e)
ecrire_csv("A05_socx_corrections.csv", ["annee", "pays_ou_ecart", "public_brut_ES10", "prive_obligatoire_ES20", "prive_volontaire_ES30",
                                         "brut_total_public_plus_prive", "net_public_ES40", "net_total_ES50"], lignes)

# (3) vieillesse par personne de 65 ans et plus
dem = lire_jsonstat(os.path.join(SRC, "eurostat_demo_pjanind.json"))
P65 = {(x["geo"], int(x["time"])): x["value"] for x in dem if x["indic_de"] == "PC_Y65_MAX"}
mx = lire_jsonstat(os.path.join(SRC, "eurostat_gov_10a_exp_mioeur.json"))
C = {(x["geo"], x["cofog99"], int(x["time"])): x["value"] for x in mx}
vl = []
for y in (2007, 2019, 2024):
    for g in ["FR", "EA20", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT"]:
        if (g, y) in P65 and (g, "GF1002", y) in C and (g, y) in PIB:
            old = 100 * C[(g, "GF1002", y)] / PIB[(g, y)]
            oldsurv = 100 * (C[(g, "GF1002", y)] + C.get((g, "GF1003", y), 0)) / PIB[(g, y)]
            vl.append([y, g, P65[(g, y)], old, oldsurv, 100 * old / P65[(g, y)], 100 * oldsurv / P65[(g, y)]])
ecrire_csv("A05_vieillesse_par_65plus.csv", ["annee", "geo", "part_65plus_pct", "vieillesse_pctPIB", "vieillesse_survivants_pctPIB",
                                              "vieillesse_par_65plus_en_pct_PIB_par_hab", "vieill_surv_par_65plus_en_pct_PIB_par_hab"], vl)

if __name__ == "__main__":
    for l in et:
        if l[0] == 2025: print("2025", l[1], "TE %.2f/%.2f ecart %.2f | TR ecart %.2f | solde ecart %.2f" % (l[2], l[3], l[4], l[7], l[8]))
    for l in lignes:
        if l[0] == "2019": print(l)
    for l in vl:
        if l[0] in (2019, 2024): print(["%.2f" % v if isinstance(v, float) else v for v in l])
