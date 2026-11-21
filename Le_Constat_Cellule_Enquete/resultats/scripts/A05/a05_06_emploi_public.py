# -*- coding: utf-8 -*-
"""A05 travail 6 - emploi des APU (comptes nationaux, OCDE table 0200 / DF_TABLE12_EMPDC, personnes, milliers)
rapporté à la population (Eurostat nama_10_pe POP_NC, milliers), 1980-2025 ; + masse salariale et achats (Insee 3.201).
Sorties : A05_emploi_APU_par_habitant.csv ; A05_train_de_vie_ordres_grandeur.csv
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *

r = list(csv.DictReader(open(os.path.join(SRC, "oecd_T12_emploi_APU.csv"), encoding="utf-8")))
E = {(x["REF_AREA"], x["SECTOR"], int(x["TIME_PERIOD"])): float(x["OBS_VALUE"]) for x in r if x["OBS_VALUE"]}
pe = lire_jsonstat(os.path.join(SRC, "eurostat_nama_10_pe.json"))
ISO = {"FR": "FRA", "DE": "DEU", "IT": "ITA", "ES": "ESP", "NL": "NLD", "BE": "BEL", "SE": "SWE", "DK": "DNK", "FI": "FIN", "AT": "AUT"}
POP = {(ISO[x["geo"]], int(x["time"])): x["value"] for x in pe if x["geo"] in ISO}
# population France avant 1995 : Insee (population_menages_fr.xlsx, onglet Population_France)
import openpyxl
wb = openpyxl.load_workbook(os.path.join(SRC, "insee_population_menages_fr.xlsx"), read_only=True, data_only=True)
rows = list(wb["Population_France"].iter_rows(values_only=True))
hdr = rows[3]
popfr = {int(h): float(v) for h, v in zip(hdr, rows[6]) if h and str(h).isdigit() and isinstance(v, (int, float))}
out = []
for (c, s, y), v in sorted(E.items()):
    if s != "S13":
        continue
    p = popfr.get(y) if c == "FRA" else POP.get((c, y))
    if p:
        out.append([c, y, v, p, 1000 * v / p])
ecrire_csv("A05_emploi_APU_par_habitant.csv", ["pays", "annee", "emploi_APU_milliers", "population_milliers", "emplois_APU_pour_1000_hab"], out)

_, t = lire_insee_32xx("3201")
tot = t["Total des dépenses"][2025]
od = []
for lab, cle in [("Rémunérations (D1), S13", "Rémunération des salariés (D1)"), ("Consommations intermédiaires (P2), S13", "Consommation intermédiaire (P2)"),
                 ("FBCF (P51g), S13", "Formation brute de capital fixe (P51g)"),
                 ("Transferts sociaux en nature marchands (D632)", "Transferts sociaux en nature de produits marchands (D632)")]:
    v = t[cle][2025]
    od.append([lab, 2025, v, 100 * v / tot, "Insee 3.201, base 2020"])
od.append(["Mission Pouvoirs publics (PLF 2026, Sénat)", 2026, 1.1402, 100 * 1.1402 / tot, "Sénat, rapport l25-139-322 synthèse ; rapporté à la dépense 2025 (ordre de grandeur)"])
od.append(["Cabinets ministériels : dotation ISP 2025 (2 741 personnes)", 2025, 0.02736, 100 * 0.02736 / tot, "Jaune PLF 2026 cabinets ministériels"])
ecrire_csv("A05_train_de_vie_ordres_grandeur.csv", ["poste", "annee", "Mdeur", "pct_depense_totale_S13_2025", "source"], od)

if __name__ == "__main__":
    D = {(a, b): e for a, b, c, d, e in out}
    for y in (1980, 1990, 2000, 2007, 2019, 2024, 2025):
        print(y, " ".join("%s=%.1f" % (c, D[(c, y)]) for c in ["FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "SWE", "DNK", "FIN", "AUT"] if (c, y) in D))
    for l in od: print(l)
