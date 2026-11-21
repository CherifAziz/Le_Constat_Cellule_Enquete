# -*- coding: utf-8 -*-
"""S11 - Controles NON pre-enregistres (ecarts declares dans S11.md par. 5).
But : verifier si la correlation de T3b (dF -> d solde primaire) tient au denominateur (PIB) et au cycle.
Lancer apres s11_tests.py : python -I s11_posthoc.py
"""
import csv, json, math, os
import numpy as np

R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
OUT = os.path.join(R, "donnees", "S11")
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


def rd(p):
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def r_ci(r, n, k=0):
    z = math.atanh(r); se = 1 / math.sqrt(n - 3 - k)
    return math.tanh(z - 1.959964 * se), math.tanh(z + 1.959964 * se)


def partial(x, y, z):
    """Correlation partielle de x et y en controlant z (matrice n x k)."""
    Z = np.column_stack([np.ones(len(x))] + [np.asarray(c, float) for c in z])
    rx = x - Z @ np.linalg.lstsq(Z, x, rcond=None)[0]
    ry = y - Z @ np.linalg.lstsq(Z, y, rcond=None)[0]
    return np.corrcoef(rx, ry)[0, 1]


t3 = {int(r["annee"]): {k: float(v) if v not in ("", "None") else None for k, v in r.items()} for r in rd(os.path.join(OUT, "S11_T3_financement.csv"))}
a09 = {int(r["exercice"]): r for r in rd(os.path.join(R, "donnees", "A09", "a09_table_exercices_1975_2025.csv"))}
g = json.load(open(os.path.join(OUT, "sources", "eurostat_nama_10_gdp_FR_CLV_PCH_PRE.json"), encoding="utf-8"))
gdp = {int(y): float(g["value"][str(i)]) for y, i in g["dimension"]["time"]["category"]["index"].items() if str(i) in g["value"]}

yy = [y for y in sorted(t3) if (y - 1) in t3 and y in a09 and y in gdp]
dsp = np.array([float(a09[y]["d_solde_primaire"]) for y in yy])
dF = np.array([t3[y]["F_pct"] - t3[y - 1]["F_pct"] for y in yy])
dshare = np.array([t3[y]["part_F_dans_dep"] - t3[y - 1]["part_F_dans_dep"] for y in yy])
growth = np.array([gdp[y] for y in yy])
pib_nom = np.array([100 * (t3[y]["PIB"] / t3[y - 1]["PIB"] - 1) for y in yy])
n = len(yy)

r1 = np.corrcoef(dshare, dsp)[0, 1]; lo, hi = r_ci(r1, n)
log(f"PH1 part de F dans la depense APUL+ASSO (sans effet de denominateur PIB) -> d solde primaire : n={n} r={r1:+.3f} IC95=[{lo:+.3f};{hi:+.3f}]")
r2 = partial(dF, dsp, [growth]); lo, hi = r_ci(r2, n, 1)
log(f"PH2 dF -> d solde primaire, controle croissance reelle : r partiel={r2:+.3f} IC95=[{lo:+.3f};{hi:+.3f}]")
r3 = partial(dF, dsp, [pib_nom]); lo, hi = r_ci(r3, n, 1)
log(f"PH3 dF -> d solde primaire, controle croissance nominale : r partiel={r3:+.3f} IC95=[{lo:+.3f};{hi:+.3f}]")
r4 = np.corrcoef(dF, pib_nom)[0, 1]
log(f"PH4 correlation dF / croissance nominale du PIB : r={r4:+.3f} (signe attendu negatif si F suit le denominateur)")
r5 = partial(dshare, dsp, [pib_nom]); lo, hi = r_ci(r5, n, 1)
log(f"PH5 part de F dans la depense -> d solde primaire, controle croissance nominale : r partiel={r5:+.3f} IC95=[{lo:+.3f};{hi:+.3f}]")
# T2 : complement en nombre d'annees (non pre-enregistre)
log("PH6 T2 en nombre d'annees : voir S11_T2_degradations_hors_crise.csv (colonne dominante)")
with open(os.path.join(OUT, "S11_posthoc_sortie.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
