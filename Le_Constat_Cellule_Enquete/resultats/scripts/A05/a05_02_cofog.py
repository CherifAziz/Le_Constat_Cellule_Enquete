# -*- coding: utf-8 -*-
"""A05 travaux 2 et 4 - Dépense par fonction (COFOG), France et comparateurs, % du PIB.

PROBLÈME DE MILLÉSIME CONSTATÉ (20/11/2026) : dans eurostat_gov_10a_exp (PC_GDP, base commune),
FR 2024 TOTAL = 57,3 % alors que gov_10a_main TE = 57,0 % et Insee = 56,98 %. Les montants en euros
concordent (COFOG 1 671 794 M€ ; main 1 672 708 M€) : c'est le DÉNOMINATEUR (PIB) du ratio COFOG
qui est d'un millésime antérieur. Même phénomène pour DE (49,4 vs 49,0) et FR 2023 (56,9 vs 56,8).
=> Ce script RECALCULE tous les ratios : COFOG en M€ (gov_10a_exp, MIO_EUR, téléchargé par A05
le 20/11/2026, Eurostat updated 2026-10-21) / PIB nama_10_gdp CP_MEUR (updated 2026-11-11).
Avant 1999, Eurostat exprime les montants en écus : les ratios restent valides (même unité au
numérateur et au dénominateur), pas les niveaux.
Zone euro hors France : (dépense EA20 - dépense FR) / (PIB EA20 - PIB FR), en euros.
Sorties :
  A05_cofog_niveaux.csv     ratios recalculés + ratio publié en PC_GDP (base commune) pour contrôle
  A05_cofog_ecarts.csv      écarts FR - comparateur par fonction (points), années 1995, 2007, 2019, 2023, 2024
  A05_cofog_evolution_FR.csv
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *

mx = lire_jsonstat(os.path.join(SRC, "eurostat_gov_10a_exp_mioeur.json"))
gdp = lire_jsonstat(os.path.join(SRC, "eurostat_nama_10_gdp.json"))
PIB = {(x["geo"], int(x["time"])): x["value"] for x in gdp if x["unit"] == "CP_MEUR"}
M = {(x["geo"], x["cofog99"], int(x["time"])): x["value"] for x in mx}
STAT = {(x["geo"], x["cofog99"], int(x["time"])): x["status"] for x in mx}
pub = {(r["geo"], r["cofog99"], int(r["time"])): float(r["value"]) for r in lire_csv_commun("eurostat_gov_10a_exp.csv") if r["value"]}

codes = sorted(set(k[1] for k in M))
geos = sorted(set(k[0] for k in M))
years = sorted(set(k[2] for k in M))
R = {}
for (g, c, y), v in M.items():
    if (g, y) in PIB:
        R[(g, c, y)] = 100 * v / PIB[(g, y)]
for c in codes:
    for y in years:
        if ("EA20", c, y) in M and ("FR", c, y) in M and ("EA20", y) in PIB and ("FR", y) in PIB:
            R[("EA20xFR", c, y)] = 100 * (M[("EA20", c, y)] - M[("FR", c, y)]) / (PIB[("EA20", y)] - PIB[("FR", y)])

LIB = {"TOTAL": "Total", "GF01": "Services generaux", "GF0101": "Organes executifs et legislatifs, affaires financieres et fiscales, affaires etrangeres",
       "GF0102": "Aide economique exterieure", "GF0103": "Services generaux (personnel, planification, statistique)", "GF0104": "Recherche fondamentale",
       "GF0105": "R&D services generaux", "GF0106": "Services generaux n.c.a. (autres)", "GF0107": "Operations concernant la dette publique (interets)",
       "GF0108": "Transferts de caractere general entre niveaux d'administration", "GF02": "Defense", "GF03": "Ordre et securite publics",
       "GF0301": "Police", "GF0302": "Protection civile", "GF0303": "Tribunaux", "GF0304": "Administration penitentiaire",
       "GF04": "Affaires economiques", "GF0401": "Tutelle economique generale, commerciale et emploi", "GF0402": "Agriculture, sylviculture, peche",
       "GF0403": "Combustibles et energie", "GF0404": "Industries extractives, manufacturieres, construction", "GF0405": "Transports",
       "GF0406": "Communications", "GF0407": "Autres branches", "GF0408": "R&D affaires economiques", "GF0409": "Affaires economiques n.c.a.",
       "GF05": "Protection de l'environnement", "GF06": "Logement et equipements collectifs", "GF07": "Sante",
       "GF0701": "Produits, appareils et materiels medicaux", "GF0702": "Services ambulatoires", "GF0703": "Services hospitaliers",
       "GF0704": "Services de sante publique", "GF0705": "R&D sante", "GF0706": "Sante n.c.a.", "GF08": "Loisirs, culture et culte", "GF09": "Enseignement",
       "GF0901": "Pre-elementaire et primaire", "GF0902": "Secondaire", "GF0903": "Post-secondaire non superieur", "GF0904": "Superieur",
       "GF0905": "Non defini par niveau", "GF0906": "Services annexes", "GF0907": "R&D enseignement", "GF0908": "Enseignement n.c.a.",
       "GF10": "Protection sociale", "GF1001": "Maladie et invalidite", "GF1002": "Vieillesse", "GF1003": "Survivants", "GF1004": "Famille et enfants",
       "GF1005": "Chomage", "GF1006": "Logement (allocations)", "GF1007": "Exclusion sociale n.c.a.", "GF1008": "R&D protection sociale", "GF1009": "Protection sociale n.c.a."}

lignes = []
for (g, c, y) in sorted(R):
    lignes.append([g, c, LIB.get(c, ""), y, R[(g, c, y)], M.get((g, c, y), ""), pub.get((g, c, y), ""),
                   STAT.get((g, c, y), "calc")])
ecrire_csv("A05_cofog_niveaux.csv", ["geo", "cofog", "libelle", "annee", "pct_PIB_recalcule", "MIO_EUR", "pct_PIB_publie_base_commune", "statut_eurostat"], lignes)

COMP = ["EA20", "EA20xFR", "EU27_2020", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT"]
el = []
for y in (1995, 2007, 2019, 2023, 2024):
    for comp in COMP:
        if ("FR", "TOTAL", y) not in R or (comp, "TOTAL", y) not in R:
            continue
        tot = R[("FR", "TOTAL", y)] - R[(comp, "TOTAL", y)]
        for c in codes:
            if ("FR", c, y) in R and (comp, c, y) in R:
                d = R[("FR", c, y)] - R[(comp, c, y)]
                el.append([y, comp, c, LIB.get(c, ""), R[("FR", c, y)], R[(comp, c, y)], d, 100 * d / tot])
ecrire_csv("A05_cofog_ecarts.csv", ["annee", "comparateur", "cofog", "libelle", "FR_pctPIB", "comp_pctPIB", "ecart_points", "part_ecart_total_pct"], el)

ev = []
YS = (1995, 2000, 2007, 2009, 2013, 2019, 2020, 2022, 2023, 2024)
for c in codes:
    row = [c, LIB.get(c, "")] + [R.get(("FR", c, y), "") for y in YS]
    a, b, m = R.get(("FR", c, 1995)), R.get(("FR", c, 2024)), R.get(("FR", c, 2019))
    row += [b - a if a is not None and b is not None else "", m - a if a is not None and m is not None else ""]
    ev.append(row)
ecrire_csv("A05_cofog_evolution_FR.csv", ["cofog", "libelle"] + [str(y) for y in YS] + ["var_1995_2024", "var_1995_2019"], ev)

if __name__ == "__main__":
    for y in (2024, 2019):
        print("== Annee", y, "(ratios recalcules)")
        for c in ["TOTAL", "GF01", "GF0101", "GF0107", "GF02", "GF03", "GF04", "GF05", "GF06", "GF07", "GF08", "GF09", "GF10", "GF1001", "GF1002", "GF1003", "GF1004", "GF1005", "GF1006", "GF1007"]:
            print(c.ljust(7), " ".join("%s=%5.2f" % (g, R.get((g, c, y), float('nan'))) for g in ["FR", "EA20", "EA20xFR", "DE", "IT", "BE", "SE", "DK", "NL", "AT", "FI", "ES"]))
