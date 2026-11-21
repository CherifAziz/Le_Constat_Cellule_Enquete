# -*- coding: utf-8 -*-
"""S11 - Controles NON pre-enregistres de T1 (sensibilite de la pente fragmentation -> solde).
Retrait d'une legislature a la fois, ponderation par le nombre d'exercices, exclusion des annees de crise.
Lancer apres s11_tests.py : python -I s11_posthoc_t1.py
"""
import csv, json, math, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
OUT = os.path.join(R, "donnees", "S11")
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


def tq975(df):
    # quantiles de Student a 97,5 % (table) pour df = 8..12
    return {7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179}[df]


def wls(x, y, w):
    x = np.asarray(x, float); y = np.asarray(y, float); w = np.asarray(w, float)
    X = np.column_stack([np.ones(len(x)), x]); W = np.diag(w)
    b = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
    res = y - X @ b
    s2 = (res * w) @ res / (len(x) - 2)
    cov = s2 * np.linalg.inv(X.T @ W @ X)
    se = math.sqrt(cov[1, 1]); t = tq975(len(x) - 2)
    return b[1], b[1] - t * se, b[1] + t * se


with open(os.path.join(R, "donnees", "A09", "a09_table_exercices_1975_2025.csv"), encoding="utf-8-sig") as f:
    a09 = list(csv.DictReader(f, delimiter=";"))
g = json.load(open(os.path.join(OUT, "sources", "eurostat_nama_10_gdp_FR_CLV_PCH_PRE.json"), encoding="utf-8"))
gdp = {int(y): float(g["value"][str(i)]) for y, i in g["dimension"]["time"]["category"]["index"].items() if str(i) in g["value"]}
neg = [y for y, v in gdp.items() if v < 0]
crise = set(neg) | {y + 1 for y in neg}

camp = {"V": [184, 55], "VI": [155, 124], "VII": [287], "VIII": [156, 131], "IX": [275], "X": [257, 214],
        "XI": [250, 36, 33], "XII": [365], "XIII": [320], "XIV": [294], "XVI": [172, 48, 30], "XVII": [95, 36, 33, 47]}


def frag(r):
    L = r["legislature_vote_LFI"]; y = int(r["exercice"])
    if L == "XV":
        if y <= 2020:
            return 1.0, 1
        s = np.array([271, 56.]) / 327; return 1 / np.sum(s ** 2), 2
    s = np.array(camp[L], float); s = s / s.sum(); return 1 / np.sum(s ** 2), len(camp[L])


def build(excl_crise):
    rows = []
    for L in ["V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII"]:
        ex = [r for r in a09 if r["legislature_vote_LFI"] == L and not (excl_crise and int(r["exercice"]) in crise)]
        if not ex:
            continue
        fr = [frag(r) for r in ex]
        sp = [float(r["d_solde_primaire"]) for r in ex]
        sc = [float(r["d_spcc_ameco"]) for r in ex if r["d_spcc_ameco"] not in ("", None)]
        rows.append(dict(L=L, n=len(ex), enp=np.mean([f[0] for f in fr]), grp=np.mean([f[1] for f in fr]),
                         dsp=np.mean(sp), dspcc=(np.mean(sc) if sc else None)))
    return rows


specs = [("enp", "dsp"), ("enp", "dspcc"), ("grp", "dsp"), ("grp", "dspcc")]
for excl in (False, True):
    rows = build(excl)
    log(f"\n=== {'Annees de crise exclues' if excl else 'Toutes annees'} : {len(rows)} legislatures ===")
    for xv, yv in specs:
        sub = [r for r in rows if r[yv] is not None]
        b, lo, hi = wls([r[xv] for r in sub], [r[yv] for r in sub], [1] * len(sub))
        bw, low, hiw = wls([r[xv] for r in sub], [r[yv] for r in sub], [r["n"] for r in sub])
        loo = []
        for k in range(len(sub)):
            s2 = sub[:k] + sub[k + 1:]
            bb, ll, hh = wls([r[xv] for r in s2], [r[yv] for r in s2], [1] * len(s2))
            loo.append((sub[k]["L"], bb, ll, hh))
        worst = max(loo, key=lambda t: -t[2])  # borne basse la plus faible
        n_excl = sum(1 for t in loo if t[2] > -0.3)
        n_pos0 = sum(1 for t in loo if t[2] > 0); n_neg = sum(1 for t in loo if t[3] < 0)
        log(f"{xv}->{yv}: n={len(sub)} pente={b:+.3f} IC=[{lo:+.3f};{hi:+.3f}] | ponderee par exercices {bw:+.3f} [{low:+.3f};{hiw:+.3f}] | "
            f"retrait d'une legislature : IC exclut -0,3 dans {n_excl}/{len(loo)} cas, IC entierement negatif {n_neg}/{len(loo)}, exclut 0 dans {n_pos0}/{len(loo)} ; "
            f"pire cas sans {worst[0]} : {worst[1]:+.3f} [{worst[2]:+.3f};{worst[3]:+.3f}]")
with open(os.path.join(OUT, "S11_posthoc_T1_sortie.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
