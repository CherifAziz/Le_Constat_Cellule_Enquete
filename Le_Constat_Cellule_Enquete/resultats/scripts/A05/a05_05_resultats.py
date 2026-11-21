# -*- coding: utf-8 -*-
"""A05 travail 5 - indicateurs de résultat comparables (OCDE SDMX, téléchargés le 20/11/2026).
DF_AM (mortalité évitable, taux standardisés pour 100 000), DF_IPOP (pauvreté et revenu relatif des 66+),
DF_PRR (taux de remplacement théoriques, Pensions at a Glance 2025, cas-type entrant en 2024).
Ces indicateurs sont des RÉSULTATS ; leur lien avec la dépense est une corrélation (catégorie charte :
cause plausible non isolée), jamais un effet causal.
Sortie : A05_resultats_indicateurs.csv
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *

PAYS = ["FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "SWE", "DNK", "FIN", "AUT", "EU27", "OECD"]
out = []
def charge(nom):
    return [x for x in csv.DictReader(open(os.path.join(SRC, "oecd_%s.csv" % nom), encoding="utf-8")) if x["REF_AREA"] in PAYS]

for x in charge("DF_AM"):
    if x["UNIT_MEASURE"] == "DT_10P5HB" and x["SEX"] == "_T" and x["CALC_METHODOLOGY"] == "STANDARD":
        out.append(["mortalite_evitable", x["MEASURE"], x["Measure"], "_T", x["REF_AREA"], x["TIME_PERIOD"], x["OBS_VALUE"], "deces pour 100 000, standardise"])
for x in charge("DF_IPOP"):
    if x["MEASURE"] in ("OAIP", "EDIOP") and x["AGE"] in ("Y_GE66",) and x["SEX"] in ("_T", "_Z"):
        out.append(["revenu_ages", x["MEASURE"], x["Measure"], x["AGE"], x["REF_AREA"], x["TIME_PERIOD"], x["OBS_VALUE"], x["Unit of measure"]])
    if x["MEASURE"] == "PTOP":
        out.append(["revenu_ages", x["MEASURE"], x["Measure"], x["AGE"], x["REF_AREA"], x["TIME_PERIOD"], x["OBS_VALUE"], x["Unit of measure"]])
for x in charge("DF_PRR"):
    if x["SEX"] == "M":
        out.append(["taux_remplacement", x["MEASURE"], x["Measure"], x["SEX"], x["REF_AREA"], x["TIME_PERIOD"], x["OBS_VALUE"], x["Unit of measure"]])
ecrire_csv("A05_resultats_indicateurs.csv", ["domaine", "code", "indicateur", "age_ou_sexe", "pays", "annee", "valeur", "unite"], out)

if __name__ == "__main__":
    import collections
    D = collections.defaultdict(dict)
    for d, c, lab, a, p, y, v, u in out:
        D[(d, c)][(p, y)] = v
    for k in sorted(D):
        ys = sorted(set(y for (p, y) in D[k]))
        y = ys[-1]
        # année la plus récente commune avec FR
        yfr = max(yy for (p, yy) in D[k] if p == "FRA")
        print(k, yfr, " ".join("%s=%s" % (p, D[k].get((p, yfr), "")[:5]) for p in PAYS))
