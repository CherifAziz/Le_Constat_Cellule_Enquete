# -*- coding: utf-8 -*-
"""D01 - décomposition comptable du basculement de 1974 à 1985.

Lit les pièces (d01_lecture), écrit toutes les tables dans donnees/D01/
et un résumé texte D01_sortie.txt. Relançable d'un seul appel (via lancer_d01.py).
"""
import csv
import math
import itertools
import sys

import d01_lecture as L

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

OUTD = L.SORTIES
OUTD.mkdir(parents=True, exist_ok=True)
LOG = []
CTRL = []


def p(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s)


def ecrire(nom, entete, lignes):
    with open(OUTD / nom, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(entete)
        for r in lignes:
            w.writerow([(f"{v:.4f}" if isinstance(v, float) else ("" if v is None else v)) for v in r])


def controle(nom, valeur, seuil, detail=""):
    ok = abs(valeur) <= seuil
    CTRL.append([nom, valeur, seuil, "ok" if ok else "ECART", detail])
    if not ok:
        p(f"  !! contrôle en écart : {nom} = {valeur:.4f} (seuil {seuil})")


def cagr(a, b, n):
    return (b / a) ** (1.0 / n) - 1.0


def logmean(a, b):
    if a == b:
        return a
    return (a - b) / math.log(a / b)


# ==========================================================================
# 0. Lecture
T = L.lire_3201()
Y, A04_DEP, A04_REC = L.lire_pib_a04()
SL = L.lire_serie_longue()
N = L.lire_t1101_1103()
S13 = L.lire_t7301()
ETP = L.lire_t1109()
T1105 = L.lire_t1105()
BR = L.lire_t6211()
DET = L.lire_t3101()
OCDE = L.lire_ocde()
UWSH = L.lire_ameco("FRA.1.0.0.0.UWSH")          # salaires bruts reçus par les ménages (D11)
UWCH = L.lire_ameco("FRA.1.0.0.0.UWCH")          # rémunération reçue par les ménages (D1)
CDX_PONTS = L.lire_codex_ponts()
CDX_AN = L.lire_codex_annuel()

ANS = list(range(1959, 2026))
V = N["B1GQ_vol"]                                  # PIB en volume, Md EUR 2020 chaînés
P = {a: Y[a] / V[a] for a in ANS}                  # prix du PIB (A04 nominal / volume Insee)
PC = {a: N["P3_S14B_nom"][a] / N["P3_S14B_vol"][a] for a in N["P3_S14B_vol"]}  # prix conso ménages

for a in ANS:
    controle(f"PIB A04 - PIB T_1101 {a}", Y[a] - N["B1GQ_nom"][a], 0.01, "Md EUR")

# ==========================================================================
# 1. Lignes par nature
DEP = [
    ("D1", "Rémunération des salariés (D1)", lambda a: T["D1"][a]),
    ("P2", "Consommation intermédiaire (P2)", lambda a: T["P2"][a]),
    ("AF", "Autres dépenses de fonctionnement (D29 + D4 hors D41 + D5)",
     lambda a: T["D29"][a] + T["D4hD41_dep"][a] + T["D5_dep"][a]),
    ("D41", "Intérêts (D41)", lambda a: T["D41"][a]),
    ("D62", "Prestations sociales en espèces (D62)", lambda a: T["D62"][a]),
    ("D632", "Transferts sociaux en nature marchands (D632)", lambda a: T["D632"][a]),
    ("D3", "Subventions (D3)", lambda a: T["D3"][a]),
    ("D7", "Autres transferts courants (D7, D73 nul)", lambda a: T["D7_dep"][a] + T["D73_dep"][a]),
    ("D9p", "Transferts en capital (D9p)", lambda a: T["D9p"][a]),
    ("P51g", "Investissement (FBCF, P51g)", lambda a: T["P51g"][a]),
    ("P5a", "Autres acquisitions d'actifs non financiers (P52, P53, NP)", lambda a: T["P5autres"][a]),
]
REC = [
    ("D2", "Impôts sur la production et les importations (D2)", lambda a: T["D2"][a]),
    ("D5r", "Impôts courants sur le revenu et le patrimoine (D5)", lambda a: T["D5"][a]),
    ("D91r", "Impôts en capital (D91)", lambda a: T["D91r"][a]),
    ("COTEFF", "Cotisations sociales effectives (D61 - D612)", lambda a: T["D61"][a] - T["D612"][a]),
    ("D612", "Cotisations sociales imputées (D612)", lambda a: T["D612"][a]),
    ("D995r", "Impôts et cotisations non recouvrables (D995, négatif)", lambda a: T["D995r"][a]),
    ("PROD", "Recettes de production (P11, P12, P13 partiel, D39)", lambda a: T["REC_prod"][a]),
    ("PROPR", "Revenus de la propriété (D4, dont intérêts reçus)", lambda a: T["REC_propr"][a]),
    ("AUTR", "Autres transferts reçus (D7, D9 hors impôts, D73, D733)",
     lambda a: T["REC_autres"][a] + T["D733"][a]),
]
BLOCS_CODEX = {
    "fonctionnement": ["D1", "P2", "AF"],
    "transferts_prestations": ["D62", "D632", "D3", "D7", "D9p"],
    "actifs_non_financiers": ["P51g", "P5a"],
    "interets": ["D41"],
}

X = {}      # X[code][annee] en Md EUR
LIB = {}
COTE = {}
for cote, lst in (("depense", DEP), ("recette", REC)):
    for code, lib, f in lst:
        X[code] = {a: f(a) for a in ANS}
        LIB[code] = lib
        COTE[code] = cote
X["DEP"] = {a: T["DEP_tot"][a] for a in ANS}
X["REC"] = {a: T["REC_tot"][a] for a in ANS}
X["DEPPRIM"] = {a: T["DEP_tot"][a] - T["D41"][a] for a in ANS}
X["SOLDE"] = {a: T["REC_tot"][a] - T["DEP_tot"][a] for a in ANS}
LIB.update({"DEP": "Total des dépenses", "REC": "Total des recettes",
            "DEPPRIM": "Dépenses primaires (hors D41)", "SOLDE": "Solde (recettes - dépenses)"})
COTE.update({"DEP": "depense", "REC": "recette", "DEPPRIM": "depense", "SOLDE": "solde"})

for a in ANS:
    controle(f"Somme des lignes de dépense - total 3.201 {a}", sum(X[c][a] for c, _, _ in DEP) - X["DEP"][a], 0.002, "Md EUR")
    controle(f"Somme des lignes de recette - total 3.201 {a}", sum(X[c][a] for c, _, _ in REC) - X["REC"][a], 0.002, "Md EUR")
    controle(f"Recettes - dépenses - B9NF {a}", X["SOLDE"][a] - T["B9NF"][a], 0.002, "Md EUR")


def r(code, a):
    return 100.0 * X[code][a] / Y[a]


lignes = []
for a in ANS:
    for code in [c for c, _, _ in DEP] + ["DEP", "DEPPRIM"] + [c for c, _, _ in REC] + ["REC", "SOLDE"]:
        lignes.append([a, COTE[code], code, LIB[code], X[code][a], r(code, a)])
ecrire("D01_nature_annuel.csv", ["annee", "cote", "code", "libelle", "Md_EUR_courants", "pct_PIB"], lignes)

# contrôles de raccord aux séries publiées
for a in range(1960, 2026):
    if a in SL["dep"]:
        controle(f"Dépenses/PIB - série longue Insee {a}", r("DEP", a) - SL["dep"][a], 0.05, "points")
        controle(f"Recettes/PIB - série longue Insee {a}", r("REC", a) - SL["rec"][a], 0.05, "points")
    if a in A04_DEP:
        controle(f"Dépenses/PIB - A04 {a}", r("DEP", a) - A04_DEP[a], 0.05, "points")
        controle(f"Recettes/PIB - A04 {a}", r("REC", a) - A04_REC[a], 0.05, "points")

controle("déjà établi : dépenses +15,97 points 1974-2025", r("DEP", 2025) - r("DEP", 1974) - 15.97, 0.006, "points")
controle("déjà établi : recettes +10,80 points 1974-2025", r("REC", 2025) - r("REC", 1974) - 10.80, 0.006, "points")
controle("déjà établi : dépenses +12,84 points 1974-1985", r("DEP", 1985) - r("DEP", 1974) - 12.84, 0.006, "points")

PER = [(1974, 1975), (1975, 1980), (1980, 1985), (1974, 1985)]
CODES_D = [c for c, _, _ in DEP] + ["DEP", "DEPPRIM"]
CODES_R = [c for c, _, _ in REC] + ["REC"]
lignes = []
for code in CODES_D + CODES_R + ["SOLDE"]:
    lv = [r(code, a) for a in (1960, 1973, 1974, 1975, 1980, 1985)]
    dv = [r(code, b) - r(code, a) for a, b in PER]
    lignes.append([COTE[code], code, LIB[code]] + lv + dv)
ecrire("D01_nature_periodes.csv",
       ["cote", "code", "libelle", "pct_1960", "pct_1973", "pct_1974", "pct_1975", "pct_1980", "pct_1985",
        "var_1974_1975", "var_1975_1980", "var_1980_1985", "var_1974_1985"], lignes)

p("=== 1. Niveaux et variations (points de PIB), 1974 -> 1985 ===")
for code in CODES_D + CODES_R + ["SOLDE"]:
    p(f"{code:8s} {r(code,1974):7.2f} -> {r(code,1985):7.2f}  ({r(code,1985)-r(code,1974):+.2f})  "
      f"74-75 {r(code,1975)-r(code,1974):+.2f} | 75-80 {r(code,1980)-r(code,1975):+.2f} | 80-85 {r(code,1985)-r(code,1980):+.2f}  {LIB[code]}")

# Sous-détail (compte S13, T_7301), contrôlé contre 3.201
for k3201, k7301 in (("D1", "D1"), ("D62", "D62"), ("D2", "D2"), ("D5", "D5"), ("D61", "D61"), ("D612", "D612"), ("P2", "P2")):
    for a in range(1959, 2026):
        if a in S13[k7301]:
            controle(f"T_7301 {k7301} - 3.201 {a}", S13[k7301][a] - T[k3201][a], 0.01, "Md EUR")
for a in range(1959, 2026):
    if a in S13["D611"]:
        controle(f"T_7301 D611+D613 - (D61-D612) 3.201 {a}", S13["D611"][a] + S13["D613"][a] - (T["D61"][a] - T["D612"][a]), 0.01, "Md EUR")
lignes = []
for a in range(1959, 2026):
    if a in S13["D3_vers"]:
        controle(f"T_7301 D3 versées - 3.201 D3 {a}", S13["D3_vers"][a] - T["D3"][a], 0.01, "Md EUR")
    # D7 versés : T_7301 n'est consolidé de D73 que jusqu'en 1977 ; on compare la somme D71+D72+D74+D75+D76
    if all(a in S13[k] for k in ("D71_vers", "D72_vers", "D74_vers", "D75_vers", "D76_vers")):
        controle(f"T_7301 D71+D72+D74+D75+D76 versés - 3.201 D7 {a}",
                 sum(S13[k][a] for k in ("D71_vers", "D72_vers", "D74_vers", "D75_vers", "D76_vers")) - T["D7_dep"][a], 0.02, "Md EUR")
for k in ("D11", "D121", "D122", "D621", "D622", "D623", "D631", "D31_vers", "D39_vers", "D391_vers", "D392_vers",
          "D399_vers", "D71_vers", "D72_vers", "D74_vers", "D75_vers", "D76_vers",
          "D211", "D212", "D214", "D29", "D291", "D51", "D59", "D611", "D613CE", "D613NSI", "D612"):
    s = S13[k]
    vals = [100 * s[a] / Y[a] if a in s else None for a in (1974, 1975, 1980, 1985)]
    d = [(vals[j + 1] - vals[j]) if vals[j] is not None and vals[j + 1] is not None else None for j in range(3)]
    tot = (vals[3] - vals[0]) if vals[0] is not None and vals[3] is not None else None
    lignes.append([k] + vals + d + [tot])
ecrire("D01_sous_detail_T7301.csv",
       ["code_T7301", "pct_1974", "pct_1975", "pct_1980", "pct_1985", "var_74_75", "var_75_80", "var_80_85", "var_74_85"], lignes)
p("\n=== Sous-détail T_7301 (points de PIB 1974 -> 1985) ===")
for row in lignes:
    p("  " + row[0] + " : " + " ".join("n.d." if v is None else f"{v:.2f}" for v in row[1:5])
      + ("" if row[-1] is None else f"  ({row[-1]:+.2f})"))

# Sensibilité à l'année de départ (1973, 1974, 1975 -> 1985)
p("\n=== Sensibilité à l'année de départ (variation jusqu'en 1985, points de PIB) ===")
lignes = []
for code in CODES_D + CODES_R + ["SOLDE"]:
    v = [r(code, 1985) - r(code, a0) for a0 in (1973, 1974, 1975)]
    lignes.append(["3.201", code, LIB[code]] + [r(code, a0) for a0 in (1972, 1973, 1974, 1975)] + v)
for k in ("D29", "D59", "D51", "D211", "D214", "D611", "D613CE"):
    s = S13[k]
    v = [100 * s[1985] / Y[1985] - 100 * s[a0] / Y[a0] for a0 in (1973, 1974, 1975)]
    lignes.append(["T_7301", k, k] + [100 * s[a0] / Y[a0] for a0 in (1972, 1973, 1974, 1975)] + v)
ecrire("D01_sensibilite_annee_depart.csv",
       ["source", "code", "libelle", "pct_1972", "pct_1973", "pct_1974", "pct_1975",
        "var_1973_1985", "var_1974_1985", "var_1975_1985"], lignes)
for row in lignes:
    if row[1] in ("DEP", "REC", "SOLDE", "COTEFF", "D2", "D5r", "D29", "D59", "D51"):
        p(f"  {row[1]:7s} niveaux 72-75 {row[3]:.2f} {row[4]:.2f} {row[5]:.2f} {row[6]:.2f} | Δ→1985 depuis 1973 {row[7]:+.2f}, 1974 {row[8]:+.2f}, 1975 {row[9]:+.2f}")

# ==========================================================================
# 2(a). Identité : contribution du poste et contribution du PIB (formes exactes, additives)
p("\n=== 2(a) Identité : variation = contribution du poste + contribution du PIB ===")
lignes = []
for code in CODES_D + CODES_R + ["SOLDE"]:
    for a0, a1 in PER:
        X0, X1, Y0, Y1 = X[code][a0], X[code][a1], Y[a0], Y[a1]
        r0, r1 = 100 * X0 / Y0, 100 * X1 / Y1
        d = r1 - r0
        num_n = 100 * (X1 - X0) / Y1
        den_n = -r0 * (Y1 - Y0) / Y1
        x0, x1 = X0 / P[a0], X1 / P[a1]
        num_r = 100 * (x1 - x0) / V[a1]
        den_r = -r0 * (V[a1] - V[a0]) / V[a1]
        if r0 != 0 and r1 != 0 and (r0 > 0) == (r1 > 0):
            Lm = logmean(r1, r0)
            num_l = Lm * math.log(x1 / x0)
            den_l = -Lm * math.log(V[a1] / V[a0])
        else:
            num_l = den_l = None
        controle(f"identité nominale {code} {a0}-{a1}", num_n + den_n - d, 1e-9)
        controle(f"identité réelle {code} {a0}-{a1}", num_r + den_r - d, 1e-9)
        if num_l is not None:
            controle(f"identité log-moyenne {code} {a0}-{a1}", num_l + den_l - d, 1e-9)
        lignes.append([COTE[code], code, f"{a0}-{a1}", r0, r1, d, num_n, den_n, num_r, den_r, num_l, den_l])
ecrire("D01_convention_a_identite.csv",
       ["cote", "code", "periode", "ratio_debut", "ratio_fin", "variation_pts",
        "a_nominal_contrib_poste", "a_nominal_contrib_PIB",
        "a_reel_contrib_volume_poste", "a_reel_contrib_volume_PIB",
        "a_logmoy_contrib_volume_poste", "a_logmoy_contrib_volume_PIB"], lignes)
for row in lignes:
    if row[1] in ("DEP", "REC", "DEPPRIM") or (row[2] == "1974-1985" and row[0] != "solde"):
        p(f"  {row[1]:8s} {row[2]} : Δ {row[5]:+.2f} = nominal {row[6]:+.2f} {row[7]:+.2f} | réel {row[8]:+.2f} {row[9]:+.2f}"
          + (f" | log-moy {row[10]:+.2f} {row[11]:+.2f}" if row[10] is not None else ""))

# ==========================================================================
# 2(b)(c). Tendance antérieure du PIB ; rythme réel antérieur de chaque poste
p("\n=== 2(b)(c) Contrefactuels, ancrage 1974, horizon 1985 (et 1980) ===")
FEN = [(1960, 1973), (1968, 1973)]
A0 = 1974
lignes, carre = [], []
for f0, f1 in FEN:
    gV = cagr(V[f0], V[f1], f1 - f0)
    for H in (1980, 1985):
        n = H - A0
        Vcf = V[A0] * (1 + gV) ** n
        for code in CODES_D + CODES_R:
            x = {a: X[code][a] / P[a] for a in ANS}
            gx = cagr(x[f0], x[f1], f1 - f0) if x[f0] > 0 and x[f1] > 0 else None
            r74, rH = r(code, A0), r(code, H)
            rb = rH * V[H] / Vcf
            rc = (100 * x[A0] * (1 + gx) ** n * P[H] / Y[H]) if gx is not None else None
            lignes.append([COTE[code], code, f"{f0}-{f1}", H, 100 * gV, None if gx is None else 100 * gx,
                           r74, rH, rH - r74, rb, rH - rb, rc, None if rc is None else rH - rc])
        # somme des contrefactuels (c) par ligne
        for agg, comps in (("DEP", [c for c, _, _ in DEP]), ("DEPPRIM", [c for c, _, _ in DEP if c != "D41"]),
                           ("REC", [c for c, _, _ in REC if c not in ("D995r",)])):
            rc_sum = 0.0
            for c in comps:
                x = {a: X[c][a] / P[a] for a in ANS}
                gx = cagr(x[f0], x[f1], f1 - f0)
                rc_sum += 100 * x[A0] * (1 + gx) ** n * P[H] / Y[H]
            if agg == "REC":
                rc_sum += r("D995r", H)   # ligne négative, rythme non défini : laissée observée
            xa = {a: X[agg][a] / P[a] for a in ANS}
            gX = cagr(xa[f0], xa[f1], f1 - f0)
            r74, rH = r(agg, A0), r(agg, H)
            rb = rH * V[H] / Vcf
            rc_tot = 100 * xa[A0] * (1 + gX) ** n * P[H] / Y[H]
            rpre = r74 * ((1 + gX) / (1 + gV)) ** n
            B = rH - rb
            C = rH - rc_tot
            Tpre = rpre - r74
            I = rH - rb - rc_tot + rpre
            controle(f"carré 2x2 {agg} {f0}-{f1} {H}", (B + C - I + Tpre) - (rH - r74), 1e-9)
            carre.append([agg, f"{f0}-{f1}", H, 100 * gV, 100 * gX, r74, rH, rH - r74, rb, rc_tot, rc_sum, rpre,
                          B, C, rH - rc_sum, rc_tot - rc_sum, Tpre, I, B + C])
ecrire("D01_conventions_b_c_par_poste.csv",
       ["cote", "code", "fenetre_reference", "horizon", "g_PIB_volume_ref_pct_an", "g_reel_poste_ref_pct_an",
        "ratio_1974", "ratio_horizon", "variation_observee",
        "b_ratio_si_PIB_tendance", "b_part_attribuee_au_ralentissement_PIB",
        "c_ratio_si_poste_au_rythme_anterieur", "c_part_attribuee_a_l_ecart_du_poste"], lignes)
ecrire("D01_conventions_carre_2x2.csv",
       ["agregat", "fenetre_reference", "horizon", "g_PIB_ref_pct_an", "g_reel_agregat_ref_pct_an",
        "r_1974", "r_obs", "variation_obs", "r_b_PIB_tendance_depense_obs", "r_c_PIB_obs_depense_tendance_agregat",
        "r_c_somme_des_postes", "r_tendance_PIB_et_depense",
        "B_part_PIB_(b)", "C_part_depense_(c)_agregat", "C_part_depense_(c)_somme_postes",
        "effet_de_composition_(c)", "T_derive_anterieure_du_ratio", "I_interaction", "B_plus_C"], carre)
for row in carre:
    p(f"  {row[0]:7s} réf {row[1]} → {row[2]} : obs {row[6]:.2f} (Δ {row[7]:+.2f}) | (b) {row[8]:.2f} part PIB {row[12]:+.2f}"
      f" | (c) agrégat {row[9]:.2f} part dépense {row[13]:+.2f} ; somme postes {row[10]:.2f} part {row[14]:+.2f}"
      f" | tendance double {row[11]:.2f} T {row[16]:+.2f} I {row[17]:+.2f} | B+C {row[18]:+.2f}")

# ==========================================================================
# 3. Volumes et prix par poste
p("\n=== 3. Croissance réelle annuelle moyenne (déflateur du PIB ; entre parenthèses prix conso ménages) ===")
PERV = [(1960, 1973), (1968, 1973), (1974, 1980), (1980, 1985), (1974, 1985)]
lignes = []
for code in CODES_D + CODES_R:
    row = [COTE[code], code, LIB[code]]
    txt = []
    for a0, a1 in PERV:
        n = a1 - a0
        gn = cagr(X[code][a0], X[code][a1], n) if X[code][a0] > 0 and X[code][a1] > 0 else None
        gp = cagr(P[a0], P[a1], n)
        gc = cagr(PC[a0], PC[a1], n)
        gr = None if gn is None else (1 + gn) / (1 + gp) - 1
        grc = None if gn is None else (1 + gn) / (1 + gc) - 1
        row += [None if gn is None else 100 * gn, None if gr is None else 100 * gr, None if grc is None else 100 * grc]
        txt.append("n.d." if gr is None else f"{100*gr:5.2f} ({100*grc:5.2f})")
    lignes.append(row)
    p(f"  {code:8s} " + " | ".join(txt))
gv = [100 * cagr(V[a0], V[a1], a1 - a0) for a0, a1 in PERV]
gpv = [100 * cagr(P[a0], P[a1], a1 - a0) for a0, a1 in PERV]
p("  PIB vol  " + " | ".join(f"{g:5.2f}" for g in gv) + "   ;  prix du PIB " + " | ".join(f"{g:5.2f}" for g in gpv))
lignes.append(["reference", "PIB", "PIB en volume / prix du PIB"] + sum([[None, g, gp] for g, gp in zip(gv, gpv)], []))
ent = ["cote", "code", "libelle"]
for a0, a1 in PERV:
    ent += [f"nominal_{a0}_{a1}", f"reel_defl_PIB_{a0}_{a1}", f"reel_prix_conso_{a0}_{a1}"]
ecrire("D01_volumes_prix_par_poste.csv", ent, lignes)
gd = cagr(X["DEP"][1974] / P[1974], X["DEP"][1985] / P[1985], 11)
controle("A06 : dépense en volume 1974-85 = 4,75 %/an", 100 * gd - 4.75, 0.01, "%/an")
controle("A06 : PIB en volume 1974-85 = 2,20 %/an", 100 * cagr(V[1974], V[1985], 11) - 2.20, 0.01, "%/an")

# Rémunérations : effectifs et rémunération par tête
p("\n=== 3bis. Rémunérations des APU : effectifs x rémunération réelle par tête ===")
OZPZ = {a: BR["OZ"][a] + BR["PZ"][a] for a in BR["OZ"] if a in BR["PZ"]}
lignes = []
for a in range(1959, 1991):
    lignes.append([a, T["D1"][a], S13["D11"].get(a), S13["D121"].get(a), S13["D122"].get(a),
                   ETP["S13"].get(a), OZPZ.get(a), BR["OQ"].get(a), T1105["D1"][a], BR["TOT"].get(a), P[a]])
ecrire("D01_remunerations_annuel.csv",
       ["annee", "D1_APU_MdEUR", "D11_APU", "D121_APU", "D122_APU", "ETP_S13_milliers_T1109",
        "ETP_salaries_branches_OZ_PZ_T6211", "ETP_salaries_branche_OQ_T6211", "D1_economie_T1105",
        "ETP_salaries_economie_T6211", "prix_PIB"], lignes)
lignes = []


def greel(s, a0, a1, prix):
    n = a1 - a0
    return (1 + cagr(s[a0], s[a1], n)) / (1 + cagr(prix[a0], prix[a1], n)) - 1


for a0, a1 in [(1960, 1973), (1968, 1973), (1970, 1973), (1974, 1980), (1974, 1978), (1978, 1985), (1980, 1985), (1974, 1985)]:
    n = a1 - a0
    g = {(k, dn): greel(s, a0, a1, pr) for k, s in (("D1", T["D1"]), ("D11", S13["D11"]))
         for dn, pr in (("PIB", P), ("conso", PC))}
    for nom, eff in (("S13 (T_1109)", ETP["S13"]), ("branches OZ+PZ (T_6211)", OZPZ), ("branche OQ (T_6211)", BR["OQ"])):
        if a0 in eff and a1 in eff:
            ge = cagr(eff[a0], eff[a1], n)
            pt = {kd: 100 * ((1 + v) / (1 + ge) - 1) for kd, v in g.items()}
            lignes.append([f"{a0}-{a1}", nom, 100 * ge, 100 * g[("D1", "PIB")], 100 * g[("D11", "PIB")],
                           100 * g[("D11", "conso")], pt[("D1", "PIB")], pt[("D1", "conso")],
                           pt[("D11", "PIB")], pt[("D11", "conso")]])
    # référence : économie entière (D1 seulement : pas de D11 intérieur Insee conservé)
    ge = cagr(BR["TOT"][a0], BR["TOT"][a1], n)
    gw = greel(T1105["D1"], a0, a1, P)
    gwc = greel(T1105["D1"], a0, a1, PC)
    lignes.append([f"{a0}-{a1}", "économie entière (D1 T_1105 / salariés T_6211)", 100 * ge, 100 * gw, None, None,
                   100 * ((1 + gw) / (1 + ge) - 1), 100 * ((1 + gwc) / (1 + ge) - 1), None, None])
ecrire("D01_remunerations_effectifs_par_tete.csv",
       ["periode", "effectifs", "effectifs_pct_an", "D1_reel_prix_PIB_pct_an", "D11_reel_prix_PIB_pct_an",
        "D11_reel_prix_conso_pct_an", "D1_par_tete_prix_PIB", "D1_par_tete_prix_conso",
        "D11_par_tete_prix_PIB", "D11_par_tete_prix_conso"], lignes)
f2 = lambda v: "  n.d." if v is None else f"{v:6.2f}"
for row in lignes:
    p(f"  {row[0]} {row[1]:48s} effectifs {row[2]:5.2f} | par tête D1 {f2(row[6])} (conso {f2(row[7])}) | D11 {f2(row[8])} (conso {f2(row[9])})")
# validation du substitut sur 1978-1985
ge_s13 = cagr(ETP["S13"][1978], ETP["S13"][1985], 7)
ge_ozpz = cagr(OZPZ[1978], OZPZ[1985], 7)
ge_oq = cagr(BR["OQ"][1978], BR["OQ"][1985], 7)
p(f"  validation 1978-85 : ETP S13 {100*ge_s13:.2f} %/an ; OZ+PZ {100*ge_ozpz:.2f} ; OQ {100*ge_oq:.2f}")

# ==========================================================================
# 4. Trois sous-périodes : qui porte la variation du solde
p("\n=== 4. Sous-périodes : contributions à la variation du solde (points de PIB) ===")
lignes = []
for a0, a1 in PER:
    contrib = []
    for code, _, _ in DEP:
        d = r(code, a1) - r(code, a0)
        contrib.append(("depense", code, d, -d))
    for code, _, _ in REC:
        d = r(code, a1) - r(code, a0)
        contrib.append(("recette", code, d, d))
    ds = r("SOLDE", a1) - r("SOLDE", a0)
    controle(f"somme des contributions = Δsolde {a0}-{a1}", sum(c[3] for c in contrib) - ds, 1e-9)
    db9 = 100 * T["B9NF"][a1] / Y[a1] - 100 * T["B9NF"][a0] / Y[a0]
    controle(f"Δsolde = ΔB9NF {a0}-{a1}", ds - db9, 0.001)
    tri = sorted(contrib, key=lambda c: c[3])
    for rang, c in enumerate(tri, 1):
        lignes.append([f"{a0}-{a1}", c[0], c[1], LIB[c[1]], c[2], c[3], 100 * c[3] / ds if ds else None, rang])
    p(f"  {a0}-{a1} : Δsolde {ds:+.2f} ; Δrecettes {r('REC',a1)-r('REC',a0):+.2f} ; Δdépenses {r('DEP',a1)-r('DEP',a0):+.2f}")
    p("     plus défavorables : " + ", ".join(f"{c[1]} {c[3]:+.2f}" for c in tri[:4]))
    p("     plus favorables   : " + ", ".join(f"{c[1]} {c[3]:+.2f}" for c in tri[-4:][::-1]))
ecrire("D01_sous_periodes_solde.csv",
       ["periode", "cote", "code", "libelle", "variation_ratio_pts", "contribution_au_solde_pts",
        "part_de_la_variation_du_solde_pct", "rang_du_plus_defavorable"], lignes)

# ==========================================================================
# 5. Recettes : cotisations = taux légal x écart taux apparent/légal x assiette
p("\n=== 5. Cotisations effectives sur salaires : taux légal x écart x assiette ===")


def taux_moyen(table, an):
    tot = 0.0
    for c, sched in table.items():
        vals = []
        for m in range(12):
            t = an + m / 12
            v = None
            for d, x in sched:
                if d <= t + 1e-9:
                    v = x
            vals.append(v)
        tot += sum(vals) / 12
    return tot


TL_E = {a: taux_moyen(L.TAUX_EMPLOYEUR, a) for a in range(1974, 1987)}
TL_S = {a: taux_moyen(L.TAUX_SALARIE, a) for a in range(1974, 1987)}
TL = {a: TL_E[a] + TL_S[a] for a in TL_E}
controle("reproduction du taux légal S01 1974 (36,37)", TL[1974] - 36.37, 0.006)
controle("reproduction du taux légal S01 1985 (45,83)", TL[1985] - 45.83, 0.006)

AN5 = list(range(1974, 1987))
W1 = {a: UWSH[a] for a in AN5}                                  # D11 reçu par les ménages (AMECO)
W2 = {a: UWSH[a] * T1105["D1"][a] / UWCH[a] for a in AN5}       # même rapport D11/D1, rapporté à D1 intérieur Insee
CS = {a: S13["D611"][a] + S13["D613CE"][a] for a in AN5}        # cotisations effectives sur salaires
CE_ = {a: S13["D611"][a] for a in AN5}
CSal = {a: S13["D613CE"][a] for a in AN5}
NSI = {a: S13["D613NSI"][a] for a in AN5}
lignes = []
for a in AN5:
    lignes.append([a, TL_E[a], TL_S[a], TL[a], CE_[a], CSal[a], NSI[a], S13["D612"][a], W1[a], W2[a],
                   T1105["D1"][a], T1105["B1G"][a], Y[a],
                   100 * CS[a] / Y[a], 100 * CS[a] / W1[a], 100 * W1[a] / Y[a], 100 * CS[a] / W1[a] / TL[a],
                   100 * NSI[a] / Y[a], 100 * T1105["D1"][a] / T1105["B1G"][a]])
ecrire("D01_cotisations_annuel.csv",
       ["annee", "taux_legal_employeur_pct", "taux_legal_salarie_pct", "taux_legal_total_pct",
        "D611_MdEUR", "D613CE_MdEUR", "D613NSI_MdEUR", "D612_MdEUR",
        "W1_D11_menages_AMECO", "W2_D11_rapporte_D1_interieur", "D1_economie_Insee", "VA_brute_Insee", "PIB",
        "cotis_salaires_pct_PIB", "taux_apparent_pct_W1", "W1_pct_PIB", "ecart_k_taux_apparent_sur_legal",
        "cotis_non_salaries_pct_PIB", "part_D1_dans_VA_pct"], lignes)


def decomp3(c0, c1, f0, f1):
    """c = prod f ; renvoie (LMDI, min, max par facteur sur les 6 ordres)."""
    Lm = logmean(c1, c0)
    lm = [Lm * math.log(f1[i] / f0[i]) for i in range(3)]
    res = {i: [] for i in range(3)}
    for ordre in itertools.permutations(range(3)):
        cur = list(f0)
        prev = c0
        for i in ordre:
            cur[i] = f1[i]
            val = c0 * (cur[0] / f0[0]) * (cur[1] / f0[1]) * (cur[2] / f0[2])
            res[i].append(val - prev)
            prev = val
    return lm, [min(res[i]) for i in range(3)], [max(res[i]) for i in range(3)]


lignes = []
for a0, a1 in [(1974, 1985), (1974, 1980), (1980, 1985)]:
    for nomW, W in (("W1", W1), ("W2", W2)):
        for cote_, Cn, TLx in (("employeur+salarié", CS, TL), ("employeur (D611)", CE_, TL_E), ("salarié (D613CE)", CSal, TL_S)):
            c0, c1 = 100 * Cn[a0] / Y[a0], 100 * Cn[a1] / Y[a1]
            f0 = [TLx[a0], (Cn[a0] / W[a0]) / TLx[a0], W[a0] / Y[a0]]
            f1 = [TLx[a1], (Cn[a1] / W[a1]) / TLx[a1], W[a1] / Y[a1]]
            lm, mn, mx = decomp3(c0, c1, f0, f1)
            controle(f"décomposition cotisations {cote_} {nomW} {a0}-{a1}", sum(lm) - (c1 - c0), 1e-9)
            lignes.append([f"{a0}-{a1}", nomW, cote_, c0, c1, c1 - c0, lm[0], mn[0], mx[0], lm[1], mn[1], mx[1], lm[2], mn[2], mx[2]])
ecrire("D01_cotisations_decomposition.csv",
       ["periode", "assiette", "cotisations", "pct_PIB_debut", "pct_PIB_fin", "variation",
        "taux_legal_LMDI", "taux_legal_min", "taux_legal_max",
        "ecart_apparent_legal_LMDI", "ecart_min", "ecart_max",
        "assiette_salaires_PIB_LMDI", "assiette_min", "assiette_max"], lignes)
for row in lignes:
    if row[1] == "W1" or row[0] == "1974-1985":
        p(f"  {row[0]} {row[1]} {row[2]:18s} : {row[3]:.2f} -> {row[4]:.2f} ({row[5]:+.2f}) = taux légal {row[6]:+.2f} [{row[7]:+.2f};{row[8]:+.2f}]"
          f" + écart {row[9]:+.2f} [{row[10]:+.2f};{row[11]:+.2f}] + assiette {row[12]:+.2f} [{row[13]:+.2f};{row[14]:+.2f}]")
# sous-décomposition de l'assiette W/PIB = (W/D1) x (D1/VA) x (VA/PIB)
lignes = []
for a0, a1 in [(1974, 1985), (1974, 1980), (1980, 1985)]:
    w0, w1 = 100 * W2[a0] / Y[a0], 100 * W2[a1] / Y[a1]
    f0 = [W2[a0] / T1105["D1"][a0], T1105["D1"][a0] / T1105["B1G"][a0], T1105["B1G"][a0] / Y[a0]]
    f1 = [W2[a1] / T1105["D1"][a1], T1105["D1"][a1] / T1105["B1G"][a1], T1105["B1G"][a1] / Y[a1]]
    lm, mn, mx = decomp3(w0, w1, f0, f1)
    lignes.append([f"{a0}-{a1}", w0, w1, w1 - w0, lm[0], lm[1], lm[2], 100 * f0[1], 100 * f1[1]])
    p(f"  assiette W2/PIB {a0}-{a1} : {w0:.2f} -> {w1:.2f} ({w1-w0:+.2f}) = D11/D1 {lm[0]:+.2f} + D1/VA {lm[1]:+.2f} + VA/PIB {lm[2]:+.2f} ;"
      f" part des rémunérations dans la VA {100*f0[1]:.1f} -> {100*f1[1]:.1f} %")
ecrire("D01_assiette_salaires_decomposition.csv",
       ["periode", "W2_pct_PIB_debut", "W2_pct_PIB_fin", "variation", "contrib_D11_sur_D1", "contrib_part_D1_dans_VA",
        "contrib_VA_sur_PIB", "part_D1_VA_debut_pct", "part_D1_VA_fin_pct"], lignes)
dce = r("COTEFF", 1985) - r("COTEFF", 1974)
dcs = 100 * CS[1985] / Y[1985] - 100 * CS[1974] / Y[1974]
dnsi = 100 * NSI[1985] / Y[1985] - 100 * NSI[1974] / Y[1974]
p(f"  cotisations effectives (D61-D612) {r('COTEFF',1974):.2f} -> {r('COTEFF',1985):.2f} ({dce:+.2f}) = sur salaires {dcs:+.2f} + non-salariés {dnsi:+.2f}")
controle("S01 : cotisations effectives 1974 = 13,44", r("COTEFF", 1974) - 13.44, 0.006)
controle("S01 : cotisations effectives 1985 = 18,46", r("COTEFF", 1985) - 18.46, 0.006)

# Impôt sur le revenu et inflation
p("\n=== 5bis. Impôt sur le revenu, inflation et barème ===")
lignes = []
for a in range(1973, 1987):
    irpp = OCDE[("T_1110", "XDC")].get(a)
    is_ = OCDE[("T_1200", "XDC")].get(a)
    inf_prec = 100 * (PC[a - 1] / PC[a - 2] - 1)
    b = L.BAREME_IR.get(a)
    maj = L.MAJORATIONS_IR.get(a)
    lignes.append([a, None if irpp is None else 100 * irpp / Y[a], OCDE[("T_1110", "PT_B1GQ")].get(a),
                   None if maj is None else 100 * maj / 6.55957 / Y[a],
                   None if is_ is None else 100 * is_ / Y[a], r("D5r", a),
                   100 * S13["D51"][a] / Y[a], 100 * S13["D59"][a] / Y[a], 100 * (PC[a] / PC[a - 1] - 1), inf_prec,
                   None if b is None else b[0], None if b is None else b[1],
                   None if b is None else inf_prec - b[0], None if b is None else inf_prec - b[1]])
ecrire("D01_impot_revenu_inflation.csv",
       ["annee", "IRPP_OCDE_1110_pct_PIB_Insee", "IRPP_OCDE_1110_pct_PIB_OCDE", "majorations_exceptionnelles_IR_S01_pct_PIB",
        "IS_OCDE_1200_pct_PIB_Insee",
        "D5_3201_pct_PIB", "D51_T7301_pct_PIB", "D59_T7301_pct_PIB", "inflation_conso_menages_annee_pct",
        "inflation_annee_precedente_pct", "relevement_bareme_plus_fort_pct", "relevement_bareme_plus_faible_pct",
        "non_indexation_tranches_basses_pts", "non_indexation_tranches_hautes_pts"], lignes)
for row in lignes:
    p(f"  {row[0]} IRPP {row[1]:.2f} | majorations {'-' if row[3] is None else format(row[3], '.2f')} | IS {row[4]:.2f}"
      f" | D5 {row[5]:.2f} | D51 {row[6]:.2f} | inflation N-1 {row[9]:.1f}"
      + ("" if row[10] is None else f" | barème +{row[10]:.1f}/+{row[11]:.1f}"))

# ==========================================================================
# 6. Intérêts
p("\n=== 6. Intérêts : taux apparent x dette ===")
D = DET["dette"]
lignes = []
for a in range(1974, 1987):
    I_ = T["D41"][a]
    d_prev = D.get(a - 1)
    ta = (100 * I_ / d_prev) if d_prev else None
    ta_moy = (100 * I_ / ((d_prev + D[a]) / 2)) if d_prev and a in D else None
    lignes.append([a, I_, T["D41G_dep"][a], T["D41_rec"][a], 100 * I_ / Y[a], 100 * T["D41_rec"][a] / Y[a],
                   100 * (I_ - T["D41_rec"][a]) / Y[a], D.get(a), None if a not in D else 100 * D[a] / Y[a], ta, ta_moy])
ecrire("D01_interets_annuel.csv",
       ["annee", "D41_verses_MdEUR", "D41G_verses", "D41_recus", "D41_verses_pct_PIB", "D41_recus_pct_PIB",
        "interets_nets_pct_PIB", "dette_Maastricht_MdEUR", "dette_pct_PIB", "taux_apparent_sur_dette_N-1_pct",
        "taux_apparent_sur_dette_moyenne_pct"], lignes)
lignes2 = []
for a0, a1 in [(1979, 1985), (1979, 1981), (1981, 1985)]:
    i0, i1 = r("D41", a0), r("D41", a1)
    f0 = [T["D41"][a0] / D[a0 - 1], D[a0 - 1] / Y[a0]]
    f1 = [T["D41"][a1] / D[a1 - 1], D[a1 - 1] / Y[a1]]
    Lm = logmean(i1, i0)
    ct = Lm * math.log(f1[0] / f0[0])
    cd = Lm * math.log(f1[1] / f0[1])
    controle(f"décomposition intérêts {a0}-{a1}", ct + cd - (i1 - i0), 1e-9)
    # ordres : taux d'abord / dette d'abord
    ct_a = i0 * (f1[0] / f0[0] - 1)
    ct_b = i0 * (f1[1] / f0[1]) * (f1[0] / f0[0] - 1)
    lignes2.append([f"{a0}-{a1}", i0, i1, i1 - i0, 100 * f0[0], 100 * f1[0], 100 * f0[1], 100 * f1[1], ct, cd,
                    min(ct_a, ct_b), max(ct_a, ct_b)])
    p(f"  {a0}-{a1} : intérêts {i0:.2f} -> {i1:.2f} ({i1-i0:+.2f}) ; taux apparent {100*f0[0]:.2f} -> {100*f1[0]:.2f} % ;"
      f" dette(N-1)/PIB {100*f0[1]:.1f} -> {100*f1[1]:.1f} % ; contribution taux {ct:+.2f} [{min(ct_a,ct_b):+.2f};{max(ct_a,ct_b):+.2f}], dette {cd:+.2f}")
ecrire("D01_interets_decomposition.csv",
       ["periode", "interets_pct_PIB_debut", "fin", "variation", "taux_apparent_debut_pct", "taux_apparent_fin_pct",
        "dette_N-1_pct_PIB_debut", "dette_N-1_pct_PIB_fin", "contrib_taux_LMDI", "contrib_dette_LMDI",
        "contrib_taux_min_ordre", "contrib_taux_max_ordre"], lignes2)
p(f"  1974-1979 : intérêts {r('D41',1974):.2f} -> {r('D41',1979):.2f} ({r('D41',1979)-r('D41',1974):+.2f}) — dette non disponible avant 1978 : non décomposé")
p(f"  1974-1985 : intérêts versés {r('D41',1974):.2f} -> {r('D41',1985):.2f} ({r('D41',1985)-r('D41',1974):+.2f}) ; reçus "
  f"{100*T['D41_rec'][1974]/Y[1974]:.2f} -> {100*T['D41_rec'][1985]/Y[1985]:.2f} ; nets "
  f"{100*(T['D41'][1974]-T['D41_rec'][1974])/Y[1974]:+.2f} -> {100*(T['D41'][1985]-T['D41_rec'][1985])/Y[1985]:+.2f}")
for a in (1978, 1979, 1980, 1985):
    controle(f"dette T_3101 = Codex annuel {a}", D[a] - float(CDX_AN[a]["dette"]), 0.05, "Md EUR")

# ==========================================================================
# 7. Rapprochements
p("\n=== 7. Rapprochement avec Codex, A05, S03 ===")
lignes = []
def mine(codes, a0, a1):
    return sum(r(c, a1) - r(c, a0) for c in codes)
pmap = {(int(x["debut"]), int(x["fin"])): x for x in CDX_PONTS}
for a0, a1 in [(1974, 1975), (1975, 1980), (1980, 1985), (1974, 1985)]:
    if (a0, a1) in pmap:
        cx = {k: float(v) for k, v in pmap[(a0, a1)].items() if k not in ("debut", "fin")}
    else:
        cx = {}
        for k in ("b9", "rec", "dep_primaires", "interets", "fonctionnement", "transferts_prestations", "actifs_non_financiers"):
            cx[k] = sum(float(pmap[pp][k]) for pp in [(1974, 1975), (1975, 1980), (1980, 1985)])
    for k, codes, lab in (("rec", ["REC"], "recettes"), ("dep_primaires", ["DEPPRIM"], "dépenses primaires"),
                          ("interets", ["D41"], "intérêts"), ("fonctionnement", BLOCS_CODEX["fonctionnement"], "fonctionnement"),
                          ("transferts_prestations", BLOCS_CODEX["transferts_prestations"], "transferts et prestations"),
                          ("actifs_non_financiers", BLOCS_CODEX["actifs_non_financiers"], "actifs non financiers"),
                          ("b9", ["SOLDE"], "solde")):
        m = mine(codes, a0, a1)
        e = m - cx[k]
        controle(f"Codex {k} {a0}-{a1}", e, 0.05, "points")
        lignes.append(["Codex ponts_points_pib.csv", f"{a0}-{a1}", lab, "+".join(codes), m, cx[k], e,
                       "même source (3.201) et même PIB ; écart = arrondi du PIB Codex"])
# A05
a05 = {row["nature"]: row for row in L.lire_csv(L.DON / "A05" / "A05_nature_contrib_periodes.csv") if row["periode"] == "1974-1985"}
cmp_a05 = [("Remunerations_D1", ["D1"]), ("Conso_intermediaires_P2", ["P2"]), ("Prestations_especes_D62", ["D62"]),
           ("Prestations_nature_marchandes_D632", ["D632"]), ("Interets_D41", ["D41"]), ("Subventions_D3", ["D3"]),
           ("Autres_transferts_courants_D7", ["D7"]), ("Transferts_capital_D9", ["D9p"]), ("FBCF_P51g", ["P51g"]),
           ("Autres_D29_D4_D5_P52_NP", ["AF", "P5a"]), ("Total", ["DEP"])]
for nat, codes in cmp_a05:
    m = mine(codes, 1974, 1985)
    v = float(a05[nat]["variation_points"])
    controle(f"A05 {nat} 1974-1985", m - v, 0.05, "points")
    note = "A05 regroupe D29, D4, D5 (bloc fonctionnement de Codex) et P52, P53, NP (bloc actifs de Codex)" if nat.startswith("Autres_D29") else "même source 3.201"
    lignes.append(["A05 A05_nature_contrib_periodes.csv", "1974-1985", nat, "+".join(codes), m, v, m - v, note])
# AF et P5a séparés (pour la table de passage A05 -> Codex)
lignes.append(["D01 (détail du regroupement A05)", "1974-1985", "AF : D29 + D4 hors D41 + D5 (bloc fonctionnement)", "AF",
               mine(["AF"], 1974, 1985), None, None, "à ranger dans « fonctionnement » chez Codex"])
lignes.append(["D01 (détail du regroupement A05)", "1974-1985", "P5a : P52 + P53 + NP (bloc actifs)", "P5a",
               mine(["P5a"], 1974, 1985), None, None, "à ranger dans « actifs non financiers » chez Codex"])
# Première enquête : prestations +5,5 ; S03 (Drees) +7,78
s03 = [row for row in L.lire_csv(L.DON / "S03" / "S03_decomposition.csv")
       if row["risque"].startswith("Total des prestations") and row["periode"] == "1974-1985"][0]
pr = mine(["D62", "D632"], 1974, 1985)
d631 = 100 * S13["D631"][1985] / Y[1985] - 100 * S13["D631"][1974] / Y[1974]
lignes.append(["Première enquête (prestations décomposées)", "1974-1985", "D62 + D632 (APU, comptes nationaux)", "D62+D632",
               pr, 5.5, pr - 5.5, "« +5,5 points » arrondi"])
lignes.append(["S03 S03_decomposition.csv (Drees, protection sociale)", "1974-1985", "Total des prestations de protection sociale",
               "D62+D632", pr, float(s03["hausse_pts"]), pr - float(s03["hausse_pts"]),
               "périmètres différents : Drees inclut les prestations hors APU et les soins des hôpitaux publics (D631)"])
lignes.append(["T_7301 (D631, information)", "1974-1985", "Transferts sociaux en nature non marchands (D631 : santé et éducation publiques, compris dans D1 et P2)",
               "D631", d631, None, None, "élément de passage vers la Drees, non séparable santé / éducation ici"])
lignes.append(["S03 - (D62+D632+D631)", "1974-1985", "écart de périmètre restant, non décomposé", "", float(s03["hausse_pts"]) - pr - d631, None, None,
               "régimes hors APU, prestations d'employeurs, différences de champ ; non attribué"])
ecrire("D01_rapprochement.csv",
       ["reference", "periode", "agregat", "codes_D01", "D01_points", "reference_points", "ecart", "explication"], lignes)
for row in lignes:
    p("  " + " | ".join("" if v is None else (f"{v:+.3f}" if isinstance(v, float) else str(v)) for v in row[:7]))

# ==========================================================================
ecrire("D01_controles.csv", ["controle", "ecart", "seuil", "statut", "unite_ou_detail"], CTRL)
n_ko = sum(1 for c in CTRL if c[3] != "ok")
p(f"\n=== Contrôles : {len(CTRL)} ; en écart : {n_ko} ===")
for c in CTRL:
    if c[3] != "ok":
        p("  ECART : " + c[0] + f" = {c[1]:.4f}")
with open(OUTD / "D01_sortie.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
