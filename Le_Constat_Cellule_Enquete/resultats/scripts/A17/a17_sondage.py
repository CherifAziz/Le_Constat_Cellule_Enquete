# -*- coding: utf-8 -*-
"""A17 - sondage : refaire a la source des chiffres pris dans les dossiers critiques.
Lancer : python -I a17_sondage.py ; sortie : donnees\\A17\\a17_sondage.txt
Sources lues en lecture seule : donnees\\commun\\base_insee_dep_rec_pctPIB.csv (Insee, base 2020),
donnees\\commun\\eurostat_gov_10a_main.csv, donnees\\A05\\sources\\oecd_DF_SOCX_AGG.csv (OCDE SOCX brut),
donnees\\A07\\table_france_1974_2025.csv (pour les contributions a la dette, construites par A07)."""
import csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
OUT = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

# 1. Base commune Insee : recettes et depenses 2017, 2019, 2025 ; 1974
base = {}
with open(os.path.join(R, "commun", "base_insee_dep_rec_pctPIB.csv"), encoding="utf-8") as h:
    for r in csv.DictReader(h, delimiter=";"):
        try:
            base[(r["serie"], int(float(r["annee"])))] = float(r["valeur"])
        except ValueError:
            pass
series = sorted({k[0] for k in base})
log("Series de la base commune :", series)
for a in (1974, 2017, 2019, 2025):
    log(a, {s: round(base.get((s, a), float('nan')), 2) for s in series})

# 2. OCDE SOCX brut : France 2019, net total (ES50) et public brut (ES10)
socx = []
with open(os.path.join(R, "A05", "sources", "oecd_DF_SOCX_AGG.csv"), encoding="utf-8-sig") as h:
    rd = csv.reader(h)
    head = next(rd)
    idx = {n: i for i, n in enumerate(head)}
    for row in rd:
        if row[idx["REF_AREA"]] in ("FRA", "DEU", "NLD", "SWE") and row[idx["TIME_PERIOD"]] == "2019":
            socx.append(row)
for row in socx:
    es, sp, pt, um = row[idx["EXPEND_SOURCE"]], row[idx["SPENDING_TYPE"]], row[idx["PROGRAMME_TYPE"]], row[idx["UNIT_MEASURE"]]
    if pt in ("TP", "_T") and es in ("ES10", "ES50") and "GDP" in um:
        log("SOCX 2019", row[idx["REF_AREA"]], es, sp, pt, um, row[idx["MEASURE"]], row[idx["OBS_VALUE"]])

# 3. Table A07 : boule de neige 1984-1997 ; 2015-2019 : solde primaire moyen, croissance nominale moyenne ;
#    economies d'interets et amelioration du primaire 2015-2019 (A15 : 52 et 121 Md€)
T = {}
with open(os.path.join(R, "A07", "table_france_1974_2025.csv"), encoding="utf-8") as h:
    for r in csv.DictReader(h, delimiter=";"):
        T[int(r["annee"])] = r
f = lambda a, k: float(T[a][k]) if T[a][k] not in ("", "nan") else 0.0
log("Boule de neige cumulee 1984-1997 :", round(sum(f(a, "contrib_boule_de_neige_pts") for a in range(1984, 1998)), 1),
    "; deficits primaires cumules 1984-1997 :", round(sum(f(a, "contrib_solde_primaire_pts") for a in range(1984, 1998)), 1))
log("1979-2025 : primaire", round(sum(f(a, "contrib_solde_primaire_pts") for a in range(1979, 2026)), 1),
    "boule de neige", round(sum(f(a, "contrib_boule_de_neige_pts") for a in range(1979, 2026)), 1),
    "SFA", round(sum(f(a, "contrib_sfa_pts") for a in range(1979, 2026)), 1),
    "variation du ratio", round(f(2025, "dette_pct") - f(1978, "dette_pct"), 1) if T[1978]["dette_pct"] else "n.d.")
log("2015-2019 : solde primaire moyen", round(sum(f(a, "solde_primaire_pct") for a in range(2015, 2020)) / 5, 2),
    "% ; croissance nominale moyenne", round(sum(f(a, "croiss_nominale_pct") for a in range(2015, 2020)) / 5, 2), "%")
eco = sum(f(2014, "interets_pct") / 100 * f(a, "pib_mdeur") - f(a, "interets_verses_mdeur") for a in range(2015, 2020))
amel = sum((f(a, "solde_primaire_pct") - f(2014, "solde_primaire_pct")) / 100 * f(a, "pib_mdeur") for a in range(2015, 2020))
log(f"2015-2019, economies d'interets cumulees (ratio de 2014 maintenu) : {eco:.0f} Md€ ; amelioration cumulee du primaire contre 2014 : {amel:.0f} Md€")
log("Solde primaire 2025 :", T[2025]["solde_primaire_pct"], "% ; interets", T[2025]["interets_pct"], "% ; dette", T[2025]["dette_pct"])

# 4. Eurostat gov_10a_main : ecart France - zone euro 2025 (depenses, recettes), pour l'ordre de grandeur V5
try:
    E = {}
    with open(os.path.join(R, "commun", "eurostat_gov_10a_main.csv"), encoding="utf-8") as h:
        rd = csv.DictReader(h, delimiter=";") if ";" in h.readline() else None
    with open(os.path.join(R, "commun", "eurostat_gov_10a_main.csv"), encoding="utf-8") as h:
        first = h.readline(); h.seek(0)
        rd = csv.DictReader(h, delimiter=";" if ";" in first else ",")
        cols = rd.fieldnames
        log("Colonnes eurostat_gov_10a_main :", cols[:12])
except Exception as e:
    log("eurostat_gov_10a_main non lu :", e)

with open(os.path.join(R, "A17", "a17_sondage.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(OUT))
