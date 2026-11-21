# -*- coding: utf-8 -*-
"""A03 - tests quantitatifs (cliquet, consolidations, France-Allemagne, ecarts de prevision).
Entrees : donnees/A03/table_annuelle_A03.csv ; base commune eurostat_gov_10a_main.csv et eurostat_gov_10dd_edpt1.csv (lecture seule) ;
donnees/A03/ecarts_prevision_execution_AN1274.csv.
Sorties : donnees/A03/test_dette_decomposition.csv, test_cliquet.csv, test_france_allemagne.csv ; resume imprime.
Formules :
  d_t = D_t / Y_t ; pb_t = solde primaire (% PIB, + = excedent) ; i_t = interets_t / D_{t-1} ; g_t = Y_t / Y_{t-1} - 1
  Delta d_t = -pb_t + (i_t - g_t)/(1+g_t) * d_{t-1} + sfa_t     (sfa = residu = ajustement stock-flux)
  L'effet "boule de neige" (i-g)/(1+g)*d_{t-1} se separe en effet taux i/(1+g)*d_{t-1} et effet croissance -g/(1+g)*d_{t-1}.
Lancer : python -I tests_A03.py
"""
import os, csv
ICI = os.path.dirname(os.path.abspath(__file__))
A03 = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03"))
COM = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "commun"))


def f(x):
    try:
        return float(x)
    except Exception:
        return None


T = {int(r["annee"]): {k: f(v) for k, v in r.items()} for r in csv.DictReader(open(os.path.join(A03, "table_annuelle_A03.csv"), encoding="utf-8-sig"), delimiter=";")}

# 1. Decomposition de la variation du ratio de dette
out = []
for a in range(2001, 2026):
    p, c = T[a - 1], T[a]
    d0, d1 = p["dette_Md"] / p["pib_Md"], c["dette_Md"] / c["pib_Md"]
    g = c["pib_Md"] / p["pib_Md"] - 1
    i = c["interets_D41_Md"] / p["dette_Md"]
    pb = (c["solde_Md"] + c["interets_D41_Md"]) / c["pib_Md"]
    eff_i = i / (1 + g) * d0
    eff_g = -g / (1 + g) * d0
    sfa = (d1 - d0) - (-pb + eff_i + eff_g)
    out.append([a, 100 * (d1 - d0), -100 * pb, 100 * eff_i, 100 * eff_g, 100 * sfa, 100 * i, 100 * g])
with open(os.path.join(A03, "test_dette_decomposition.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["annee", "var_ratio_pt", "contrib_deficit_primaire_pt", "effet_taux_pt", "effet_croissance_nominale_pt", "ajust_stock_flux_pt", "taux_apparent_pct", "croiss_nominale_pct"])
    for r in out:
        w.writerow([r[0]] + ["%.2f" % x for x in r[1:]])


def cumul(a0, a1):
    s = [0] * 5
    for r in out:
        if a0 <= r[0] <= a1:
            for k in range(5):
                s[k] += r[k + 1]
    return s


# 2. Comparaisons avant/apres crise (moyennes de periode)
def moy(c, a0, a1):
    v = [T[a][c] for a in range(a0, a1 + 1) if T[a].get(c) is not None]
    return sum(v) / len(v) if v else None


per = [("2005-2007 (avant 2008)", 2005, 2007), ("2007", 2007, 2007), ("2009-2010 (crise)", 2009, 2010),
       ("2011-2014", 2011, 2014), ("2015-2019", 2015, 2019), ("2019", 2019, 2019), ("2020-2021 (Covid)", 2020, 2021),
       ("2022", 2022, 2022), ("2023-2025", 2023, 2025)]
cols = ["dep_pct", "rec_pct", "solde_calc_pct", "interets_pct", "solde_primaire_pct", "ameco_solde_CAB_pct", "ameco_primaire_CA_pct", "dette_pct"]
with open(os.path.join(A03, "test_cliquet.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["periode"] + cols)
    for lib, a0, a1 in per:
        w.writerow([lib] + ["%.2f" % moy(c, a0, a1) for c in cols])

# 3. France - Allemagne (Eurostat gov_10a_main, base commune)
E = {}
for r in csv.DictReader(open(os.path.join(COM, "eurostat_gov_10a_main.csv"), encoding="utf-8")):
    if r["unit"] == "PC_GDP" and r["sector"] == "S13" and r["geo"] in ("FR", "DE"):
        E[(r["geo"], r["na_item"], int(r["time"]))] = f(r["value"])
D = {}
for r in csv.DictReader(open(os.path.join(COM, "eurostat_gov_10dd_edpt1.csv"), encoding="utf-8")):
    if r["unit"] == "PC_GDP" and r["na_item"] == "GD" and r["geo"] in ("FR", "DE"):
        D[(r["geo"], int(r["time"]))] = f(r["value"])
with open(os.path.join(A03, "test_france_allemagne.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["annee", "FR_solde", "DE_solde", "FR_interets", "DE_interets", "FR_primaire", "DE_primaire", "FR_depenses", "DE_depenses", "FR_recettes", "DE_recettes", "FR_dette", "DE_dette"])
    for a in range(2010, 2026):
        row = [a]
        for it in ("B9", "D41PAY"):
            for g in ("FR", "DE"):
                row.append(E.get((g, it, a)))
        row += [E[("FR", "B9", a)] + E[("FR", "D41PAY", a)], E[("DE", "B9", a)] + E[("DE", "D41PAY", a)]]
        for it in ("TE", "TR"):
            for g in ("FR", "DE"):
                row.append(E.get((g, it, a)))
        row += [D.get(("FR", a)), D.get(("DE", a))]
        w.writerow([row[0]] + ["%.1f" % x if x is not None else "indisponible" for x in row[1:]])

# 4. Ecarts de prevision (AN 1274) : asymetrie et annees electorales
ec = []
for l in open(os.path.join(A03, "ecarts_prevision_execution_AN1274.csv"), encoding="utf-8"):
    if l[:1].isdigit():
        a, e1, e2, _ = l.strip().split(";")
        ec.append((int(a), float(e1.replace(",", ".")), float(e2.replace(",", "."))))

if __name__ == "__main__":
    print("== Decomposition du ratio de dette (cumuls, points de PIB) : var, primaire, effet taux, effet croissance, stock-flux")
    for a0, a1 in [(2001, 2007), (2002, 2007), (2008, 2010), (2011, 2014), (2015, 2019), (2020, 2021), (2022, 2025), (2001, 2025)]:
        print(a0, a1, ["%.1f" % x for x in cumul(a0, a1)])
    print("== Annuel"); [print(r[0], ["%.2f" % x for x in r[1:]]) for r in out]
    print("== Periodes"); [print(l) for l in open(os.path.join(A03, "test_cliquet.csv"), encoding="utf-8-sig")]
    print("== FR-DE"); [print(l.strip()) for l in open(os.path.join(A03, "test_france_allemagne.csv"), encoding="utf-8-sig")]
    hors = [e for e in ec if e[0] not in (2008, 2009, 2020, 2021)]
    print("== Ecarts prevision initiale 2008-2024 : n=%d, moyenne %.2f, mediane %.2f, nb negatifs %d" % (len(ec), sum(e[1] for e in ec) / len(ec), sorted(e[1] for e in ec)[len(ec) // 2], sum(e[1] < 0 for e in ec)))
    print("   hors 2008-09/2020-21 : n=%d, moyenne %.2f, nb negatifs %d" % (len(hors), sum(e[1] for e in hors) / len(hors), sum(e[1] < 0 for e in hors)))
    elec = {2012, 2017, 2022}
    pe = [e[1] for e in ec if e[0] in elec]; npe = [e[1] for e in hors if e[0] not in elec]
    print("   annees de presidentielle", pe, "moyenne %.2f ; autres hors crises moyenne %.2f" % (sum(pe) / len(pe), sum(npe) / len(npe)))
