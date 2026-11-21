# -*- coding: utf-8 -*-
"""A05 travail 3 (volet retraites, refait par A05) - décomposition de l'évolution de la dépense COFOG vieillesse (GF1002)
en % du PIB : effet démographique (part des 65 ans et plus, Eurostat demo_pjanind) et effet « dépense par personne âgée
rapportée au PIB par habitant ». Décomposition logarithmique exacte : ln(V/Y) = ln(p65) + ln[(V/Y)/p65].
Ce n'est PAS une décomposition par bénéficiaire (les retraités de moins de 65 ans sont comptés dans le second terme).
Sortie : A05_vieillesse_decomposition.csv"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *
dem = lire_jsonstat(os.path.join(SRC, "eurostat_demo_pjanind.json"))
P65 = {(x["geo"], int(x["time"])): x["value"] for x in dem if x["indic_de"] == "PC_Y65_MAX"}
mx = lire_jsonstat(os.path.join(SRC, "eurostat_gov_10a_exp_mioeur.json"))
C = {(x["geo"], x["cofog99"], int(x["time"])): x["value"] for x in mx}
gdp = lire_jsonstat(os.path.join(SRC, "eurostat_nama_10_gdp.json"))
PIB = {(x["geo"], int(x["time"])): x["value"] for x in gdp if x["unit"] == "CP_MEUR"}
out = []
for g in ["FR", "EA20", "DE", "IT", "ES", "SE", "AT", "FI", "BE", "NL"]:
    for a, b in [(1995, 2007), (2007, 2019), (2019, 2024), (1995, 2024), (2007, 2024)]:
        try:
            va = 100 * C[(g, "GF1002", a)] / PIB[(g, a)]; vb = 100 * C[(g, "GF1002", b)] / PIB[(g, b)]
            pa, pb = P65[(g, a)], P65[(g, b)]
        except KeyError:
            continue
        dl = math.log(vb / va); dd = math.log(pb / pa); dp = dl - dd
        out.append([g, "%d-%d" % (a, b), va, vb, vb - va, pa, pb, (vb - va) * dd / dl if dl else "", (vb - va) * dp / dl if dl else ""])
ecrire_csv("A05_vieillesse_decomposition.csv", ["geo", "periode", "vieillesse_pctPIB_debut", "vieillesse_pctPIB_fin", "variation_points",
                                                 "part65_debut", "part65_fin", "contribution_demographie_points", "contribution_depense_par_65plus_rel_PIBhab_points"], out)
for l in out:
    print(["%.2f" % x if isinstance(x, float) else x for x in l])
