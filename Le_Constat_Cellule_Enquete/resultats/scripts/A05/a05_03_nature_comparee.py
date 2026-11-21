# -*- coding: utf-8 -*-
"""A05 travaux 6, 7, 8, 9 (volet comptable) - nature de dépense comparée et par sous-secteur.
Sources : eurostat_gov_10a_main.csv (base commune ; MIO_EUR) / PIB nama_10_gdp (A05/sources, updated 2026-11-11) ;
          Insee tableaux 3202 (APUC), 3203 (État), 3204 (ODAC), 3205 (APUL), 3212 (ASSO), 3201 (S13 consolidé).
Avertissement : les dépenses par sous-secteur Insee ne sont PAS consolidées entre sous-secteurs ; leur somme
dépasse le total S13 (transferts entre administrations). On ne les additionne pas.
Sorties :
  A05_nature_comparee_EA.csv      D1, P2, D62, D632, D41, D3, P51G, TE en % PIB : FR, EA20, EA20 hors FR, DE, etc. 1995-2025
  A05_soussecteurs_nature.csv     rémunérations, FBCF, intérêts, prestations par sous-secteur Insee, Md€ et % PIB, 1978-2025
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *
import openpyxl

gdp = lire_jsonstat(os.path.join(SRC, "eurostat_nama_10_gdp.json"))
PIB = {(x["geo"], int(x["time"])): x["value"] for x in gdp if x["unit"] == "CP_MEUR"}
main = lire_csv_commun("eurostat_gov_10a_main.csv")
M = {}
for r in main:
    if r["unit"] == "MIO_EUR" and r["value"] and r["sector"] == "S13":
        M[(r["geo"], r["na_item"], int(r["time"]))] = float(r["value"])
ITEMS = ["TE", "D1PAY", "P2", "D62PAY", "D632PAY", "D41PAY", "D3PAY", "P51G", "TR", "B9"]
GEOS = ["FR", "EA20", "EA20xFR", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT", "EU27_2020"]
out = []
for y in range(1995, 2026):
    for it in ITEMS:
        for g in GEOS:
            if g == "EA20xFR":
                if ("EA20", it, y) in M and ("FR", it, y) in M and ("EA20", y) in PIB and ("FR", y) in PIB:
                    v = 100 * (M[("EA20", it, y)] - M[("FR", it, y)]) / (PIB[("EA20", y)] - PIB[("FR", y)])
                else:
                    continue
            else:
                if (g, it, y) not in M or (g, y) not in PIB:
                    continue
                v = 100 * M[(g, it, y)] / PIB[(g, y)]
            out.append([y, it, g, v])
ecrire_csv("A05_nature_comparee_EA.csv", ["annee", "na_item", "geo", "pct_PIB_recalcule"], out)
D = {(a, b, c): d for a, b, c, d in out}

# Insee par sous-secteur
TAB = {"S13_consolide": "3201", "APUC_S1311": "3202", "Etat_S13111": "3203", "ODAC_S13112": "3204", "APUL_S1313": "3205", "ASSO_S1314": "3212"}
LAB = {"Remunerations_D1": "Rémunération des salariés (D1)", "FBCF_P51g": "Formation brute de capital fixe (P51g)",
       "Interets_D41": "Intérêts (D41)", "Prestations_D62": "Prestations sociales autres que transferts sociaux en nature (D62)",
       "Total": "Total des dépenses", "CI_P2": "Consommation intermédiaire (P2)", "Subventions_D3": "Subventions (D3)"}
_, t01 = lire_insee_32xx("3201")
wb = openpyxl.load_workbook(os.path.join(SRC, "insee_T_1101_1103_fr.xlsx"), read_only=True, data_only=True)
rows = list(wb["T_1101 en niveau"].iter_rows(values_only=True))
pib = {int(h): float(v) for h, v in zip(rows[3], [r for r in rows if r[0] == "B1GQ"][0]) if h and isinstance(v, (int, float))}
ss = []
for nom, num in TAB.items():
    _, t = lire_insee_32xx(num)
    for k, lab in LAB.items():
        if lab not in t:
            continue
        for y, v in sorted(t[lab].items()):
            if y >= 1978 and y in pib:
                ss.append([nom, k, y, v, 100 * v / pib[y]])
ecrire_csv("A05_soussecteurs_nature.csv", ["sous_secteur", "nature", "annee", "Mdeur", "pct_PIB"], ss)
S = {(a, b, c): (d, e) for a, b, c, d, e in ss}

if __name__ == "__main__":
    for it in ITEMS:
        print(it.ljust(8), " ".join("%d:FR=%5.2f EA=%5.2f xFR=%5.2f DE=%5.2f" % (y, D.get((y, it, "FR"), float('nan')), D.get((y, it, "EA20"), float('nan')),
              D.get((y, it, "EA20xFR"), float('nan')), D.get((y, it, "DE"), float('nan'))) for y in (1995, 2007, 2019, 2024, 2025)))
    for nom in TAB:
        print(nom.ljust(14), " ".join("%d: D1=%5.2f FBCF=%4.2f" % (y, S.get((nom, "Remunerations_D1", y), (0, float('nan')))[1], S.get((nom, "FBCF_P51g", y), (0, float('nan')))[1]) for y in (1980, 1993, 2007, 2019, 2025)))
