# -*- coding: utf-8 -*-
"""S11 - Tests pre-enregistres de H0040 (bien commun budgetaire).
Pre-enregistrement : resultats/agents/S11_annexe_preenregistrement.md (SHA-256 DDAE1D64...).
Lecture seule des donnees d'autres dossiers ; ecritures dans resultats/donnees/S11/ uniquement.
Lancer : python -I s11_tests.py
"""
import csv, json, math, os
import numpy as np
import openpyxl

R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
D = os.path.join(R, "donnees")
OUT = os.path.join(D, "S11")
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def read_csv(path, delim=";"):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(path, encoding=enc) as f:
                return list(csv.DictReader(f, delimiter=delim))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(path)


def fnum(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


# ---------- outils statistiques (sans scipy) ----------
def t_ppf(p, df):
    """Quantile de Student par dichotomie sur la CDF (integration numerique)."""
    def cdf(t):
        # CDF de Student via la fonction beta incomplete regularisee
        x = df / (df + t * t)
        ib = betainc(df / 2.0, 0.5, x)
        return 1 - 0.5 * ib if t > 0 else 0.5 * ib
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def betainc(a, b, x):
    """Beta incomplete regularisee (fraction continue, Numerical Recipes)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return front * cf(a, b, x) / a
    return 1 - front * cf(b, a, 1 - x) / b


def cf(a, b, x):
    tiny = 1e-30
    c, d = 1.0, 1 - (a + b) * x / (a + 1)
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((a + m2 - 1) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny)
        c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        de = d * c
        h *= de
        if abs(de - 1) < 1e-12:
            break
    return h


def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    n = len(x)
    X = np.column_stack([np.ones(n), x])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b
    s2 = res @ res / (n - 2)
    cov = s2 * np.linalg.inv(X.T @ X)
    se = math.sqrt(cov[1, 1])
    tq = t_ppf(0.975, n - 2)
    t80 = t_ppf(0.80, n - 2)
    return dict(n=n, pente=b[1], se=se, ic_bas=b[1] - tq * se, ic_haut=b[1] + tq * se,
                mde80=(tq + t80) * se, r=np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return np.corrcoef(rx, ry)[0, 1]


def r_ci(r, n):
    z = math.atanh(r); se = 1 / math.sqrt(n - 3)
    return math.tanh(z - 1.959964 * se), math.tanh(z + 1.959964 * se)


def power_r(rho, n, alpha_z=1.959964):
    """Puissance bilaterale approx. (Fisher z) pour detecter une correlation rho."""
    z = abs(math.atanh(rho)) * math.sqrt(n - 3)
    phi = lambda u: 0.5 * (1 + math.erf(u / math.sqrt(2)))
    return phi(z - alpha_z) + phi(-z - alpha_z)


def perm_p(x, y, n_perm=20000, seed=11):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float); y = np.asarray(y, float)
    r0 = abs(np.corrcoef(x, y)[0, 1]); c = 0
    for _ in range(n_perm):
        if abs(np.corrcoef(x, rng.permutation(y))[0, 1]) >= r0:
            c += 1
    return (c + 1) / (n_perm + 1)


# ---------- donnees communes ----------
a09 = read_csv(os.path.join(D, "A09", "a09_table_exercices_1975_2025.csv"))
for r in a09:
    r["annee"] = int(r["exercice"])
    for k in ("solde_primaire_pct", "d_solde_primaire", "d_depenses_primaires", "d_recettes", "spcc_ameco", "d_spcc_ameco"):
        r[k] = fnum(r[k])
A = {r["annee"]: r for r in a09}

# controle d'identite comptable : d_sp = d_rec - d_dep
ecarts = [abs(r["d_solde_primaire"] - (r["d_recettes"] - r["d_depenses_primaires"])) for r in a09 if r["d_solde_primaire"] is not None]
log("Controle identite d_sp = d_rec - d_dep : ecart max =", round(max(ecarts), 3), "pt de PIB sur", len(ecarts), "exercices")

# ================= T1 =================
log("\n================ T1 - Fragmentation de la majorite (niveau legislature) ================")
# Sieges du camp gouvernemental : a09_composition_majorites.csv, colonne camp_gouvernemental_effectif (recopies ici).
camp = {
    "V": [184, 55],           # UDR + RI (RDS/UC non etabli : exclus)
    "VI": [155, 124],         # RPR + UDF
    "VII": [287],             # S (participation communiste au gouvernement [M] : non comptee, comme A09)
    "VIII": [156, 131],       # RPR + UDF
    "IX": [275],              # S, majorite relative
    "X": [257, 214],          # RPR + UDF
    "XI": [250, 36, 33],      # SOC + COM + RCV
    "XII": [365],
    "XIII": [320],
    "XIV": [294],
    "XV": None,               # traite par exercice ci-dessous
    "XVI": [172, 48, 30],     # RE + DEM + HOR
    "XVII": [95, 36, 33, 47], # EPR + DEM + HOR + DR
}


def enp(seats):
    s = np.array(seats, float); s = s / s.sum()
    return 1 / np.sum(s ** 2)


def frag_exercice(r):
    L = r["legislature_vote_LFI"]
    if L == "XV":
        # A09 : parti seul pour les budgets votes en 2017-2019 (exercices 2018-2020), coalition pour ceux votes en 2020-2021
        # LREM 271 + MoDem 56 = 327 (A09, octobre 2020)
        if r["annee"] <= 2020:
            return 1.0, 1
        return enp([271, 56]), 2
    return enp(camp[L]), len(camp[L])


leg_order = ["V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII"]
rows_t1 = []
for L in leg_order:
    ex = [r for r in a09 if r["legislature_vote_LFI"] == L]
    if not ex:
        continue
    fr = [frag_exercice(r) for r in ex]
    dsp = [r["d_solde_primaire"] for r in ex]
    ddep = [r["d_depenses_primaires"] for r in ex]
    dsc = [r["d_spcc_ameco"] for r in ex if r["d_spcc_ameco"] is not None]
    rows_t1.append(dict(legislature=L, exercices=f"{ex[0]['annee']}-{ex[-1]['annee']}", n_ex=len(ex),
                        enp_majorite=float(np.mean([f[0] for f in fr])), nb_groupes_camp=float(np.mean([f[1] for f in fr])),
                        d_sp_moy=float(np.mean(dsp)), d_dep_moy=float(np.mean(ddep)),
                        d_spcc_moy=(float(np.mean(dsc)) if len(dsc) == len(ex) else (float(np.mean(dsc)) if dsc else None)),
                        n_spcc=len(dsc)))
for r in rows_t1:
    log(f"{r['legislature']:5s} {r['exercices']:10s} n={r['n_ex']}  ENPmaj={r['enp_majorite']:.2f}  groupes={r['nb_groupes_camp']:.2f}  dSP={r['d_sp_moy']:+.2f}  dDEP={r['d_dep_moy']:+.2f}  dSPCC={'' if r['d_spcc_moy'] is None else round(r['d_spcc_moy'],2)} (n={r['n_spcc']})")

res_t1 = {}
for xv in ("enp_majorite", "nb_groupes_camp"):
    for yv in ("d_sp_moy", "d_dep_moy", "d_spcc_moy"):
        sub = [r for r in rows_t1 if r[yv] is not None]
        x = [r[xv] for r in sub]; y = [r[yv] for r in sub]
        o = ols(x, y); rho = spearman(x, y); p = perm_p(x, y)
        res_t1[(xv, yv)] = o
        log(f"T1 {xv:16s} -> {yv:10s}: n={o['n']} pente={o['pente']:+.3f} IC95=[{o['ic_bas']:+.3f};{o['ic_haut']:+.3f}] "
            f"pente detectable a 80%={o['mde80']:.3f} r={o['r']:+.2f} rho={rho:+.2f} p_perm={p:.3f}")
    # sensibilite sans XVI et XVII (seules legislatures tres fragmentees, cf. A09)
    sub = [r for r in rows_t1 if r["legislature"] not in ("XVI", "XVII")]
    o = ols([r[xv] for r in sub], [r["d_sp_moy"] for r in sub])
    log(f"T1 sensibilite sans XVI-XVII {xv} -> d_sp_moy: n={o['n']} pente={o['pente']:+.3f} IC95=[{o['ic_bas']:+.3f};{o['ic_haut']:+.3f}]")
log("Puissance (n=13) pour detecter r=0,3 :", round(power_r(0.3, 13), 2), "; r=0,5 :", round(power_r(0.5, 13), 2), "; r=0,7 :", round(power_r(0.7, 13), 2))

with open(os.path.join(OUT, "S11_T1_legislatures.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_t1[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(rows_t1)

# ================= T2 =================
log("\n================ T2 - Composition des degradations hors crise ================")
g = json.load(open(os.path.join(OUT, "sources", "eurostat_nama_10_gdp_FR_CLV_PCH_PRE.json"), encoding="utf-8"))
tix = g["dimension"]["time"]["category"]["index"]
gdp = {int(y): float(g["value"][str(i)]) for y, i in tix.items() if str(i) in g["value"]}
neg = sorted(y for y, v in gdp.items() if v < 0)
crise = set(neg) | {y + 1 for y in neg}
log("Annees de croissance negative (Eurostat nama_10_gdp, CLV_PCH_PRE) :", neg, "-> exclues avec l'annee suivante :", sorted(crise))

rows_t2 = []
for incl in (False, True):
    deg = [r for r in a09 if r["d_solde_primaire"] is not None and r["d_solde_primaire"] <= -0.5 and (incl or r["annee"] not in crise)]
    sdep = sum(r["d_depenses_primaires"] for r in deg)
    srec = sum(r["d_recettes"] for r in deg)
    S = sdep / (sdep - srec)
    log(("Toutes annees" if incl else "Hors crise") + f" : {len(deg)} annees de degradation <= -0,5 pt ; somme Ddep={sdep:+.2f}, somme Drec={srec:+.2f}, S (part depense)={S:.2f}")
    for r in deg:
        typ = "depense" if r["d_depenses_primaires"] > -r["d_recettes"] else "recettes"
        log(f"   {r['annee']} dSP={r['d_solde_primaire']:+.2f} dDEP={r['d_depenses_primaires']:+.2f} dREC={r['d_recettes']:+.2f} croissance={gdp.get(r['annee'])} dominante={typ} leg={r['legislature_vote_LFI']}")
        if not incl:
            rows_t2.append(dict(annee=r["annee"], d_solde_primaire=r["d_solde_primaire"], d_dep=r["d_depenses_primaires"],
                                d_rec=r["d_recettes"], croissance_vol=gdp.get(r["annee"]), dominante=typ, legislature=r["legislature_vote_LFI"]))
    # bootstrap sur les annees (incertitude d'echantillonnage de S)
    rng = np.random.default_rng(11); bs = []
    arr = np.array([[r["d_depenses_primaires"], r["d_recettes"]] for r in deg])
    for _ in range(20000):
        s = arr[rng.integers(0, len(arr), len(arr))]
        den = s[:, 0].sum() - s[:, 1].sum()
        if den != 0:
            bs.append(s[:, 0].sum() / den)
    log(f"   S bootstrap IC95 = [{np.percentile(bs,2.5):.2f} ; {np.percentile(bs,97.5):.2f}] (n={len(arr)})")
# Variante corrigee du cycle (AMECO, disponible sur une partie de la periode)
deg_c = [r for r in a09 if r["d_spcc_ameco"] is not None and r["d_spcc_ameco"] <= -0.5]
log("Variante : annees ou le solde primaire corrige du cycle (AMECO) recule d'au moins 0,5 pt :",
    [(r["annee"], round(r["d_spcc_ameco"], 2), round(r["d_depenses_primaires"], 2), round(r["d_recettes"], 2)) for r in deg_c])
with open(os.path.join(OUT, "S11_T2_degradations_hors_crise.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_t2[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(rows_t2)

# ================= T3 =================
log("\n================ T3 - Fragmentation du financement (APUL + ASSO) ================")
# PIB nominal : base commune Insee (Ensemble, Md EUR / % du PIB)
sol = read_csv(os.path.join(D, "commun", "base_insee_solde_sous_secteurs.csv"))
md, pc = {}, {}
for r in sol:
    if r["serie"] == "Ensemble":
        y = int(r["annee"]); v = fnum(r["valeur"])
        if "milliards" in r["unite"]:
            md[y] = v
        elif "PIB" in r["unite"]:
            pc[y] = v
PIB = {y: md[y] / (pc[y] / 100) for y in md if y in pc and pc[y] not in (0, None) and abs(pc[y]) > 0.05}


def insee_table(fname):
    ws = openpyxl.load_workbook(os.path.join(D, "commun", fname), read_only=True, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    years = rows[2]
    lab = {}
    for i, r in enumerate(rows):
        l = (r[1] or "") if len(r) > 1 else ""
        if l:
            lab[i] = str(l).strip()
    def get(i, expect):
        assert expect in lab[i], (fname, i, lab[i], expect)
        return {int(years[j]): float(rows[i][j]) for j in range(len(years)) if isinstance(years[j], (int, float)) and rows[i][j] is not None}
    return dict(dep=get(26, "Total des d"), D2=get(45, "(D2)"), D5=get(46, "(D5)"), D91=get(47, "(D91r)"),
                D733=get(48, "(D733)"), D61=get(49, "(D61)"), D995=get(50, "(D995r)"), D73r=get(53, "(D73 hors D733)"),
                rec=get(57, "Total des recettes"), B9=get(65, "(B9NF)"), D41=get(11, "(D41)"))


L_ = insee_table("insee_cn_t_3205.xlsx")
S_ = insee_table("insee_cn_t_3212.xlsx")
E_ = insee_table("insee_cn_t_3203.xlsx")
flux = read_csv(os.path.join(D, "A01", "A01_flux_d73_par_sous_secteur.csv"))
FX = {}
for r in flux:
    FX[(int(r["annee"]), r["secteur"])] = {k: fnum(v) for k, v in r.items() if k not in ("annee", "secteur")}

years = sorted(y for y in L_["dep"] if y in PIB and y in S_["dep"])
rows_t3 = []
for y in years:
    pib = PIB[y]
    F = 0.0; F9 = 0.0
    for s in ("S1313", "S1314"):
        fx = FX[(y, s)]
        F += fx["D73_net_recu"] + fx["D733_recu"]
        F9 += fx["D9_recus"]
    own = sum(T[k][y] for T in (L_, S_) for k in ("D2", "D5", "D91", "D61", "D995"))
    dep = L_["dep"][y] + S_["dep"][y]
    rows_t3.append(dict(annee=y, PIB=pib, F_pct=100 * F / pib, F_avec_D9_pct=100 * (F + F9) / pib,
                        part_F_dans_dep=100 * F / dep, dep_APUL_ASSO_pct=100 * dep / pib, propres_APUL_ASSO_pct=100 * own / pib,
                        dep_APUL_pct=100 * L_["dep"][y] / pib, propres_APUL_pct=100 * sum(L_[k][y] for k in ("D2", "D5", "D91", "D61", "D995")) / pib,
                        dep_ASSO_pct=100 * S_["dep"][y] / pib, propres_ASSO_pct=100 * sum(S_[k][y] for k in ("D2", "D5", "D91", "D61", "D995")) / pib,
                        B9_Etat_pct=100 * E_["B9"][y] / pib, B9_APUL_pct=100 * L_["B9"][y] / pib, B9_ASSO_pct=100 * S_["B9"][y] / pib,
                        sp_S13=A[y]["solde_primaire_pct"] if y in A else None))
for r in rows_t3[::5] + [rows_t3[-1]]:
    log(f"{r['annee']} F={r['F_pct']:.2f} (avec D9 {r['F_avec_D9_pct']:.2f}) partF/dep={r['part_F_dans_dep']:.1f}% depAPUL+ASSO={r['dep_APUL_ASSO_pct']:.2f} propres={r['propres_APUL_ASSO_pct']:.2f} | APUL dep={r['dep_APUL_pct']:.2f} propres={r['propres_APUL_pct']:.2f} | ASSO dep={r['dep_ASSO_pct']:.2f} propres={r['propres_ASSO_pct']:.2f}")

# T3a : decomposition par periode
def period(a, b):
    ra = next(r for r in rows_t3 if r["annee"] == a); rb = next(r for r in rows_t3 if r["annee"] == b)
    dF = rb["F_pct"] - ra["F_pct"]; dDep = rb["dep_APUL_ASSO_pct"] - ra["dep_APUL_ASSO_pct"]; dOwn = rb["propres_APUL_ASSO_pct"] - ra["propres_APUL_ASSO_pct"]
    dDepL = rb["dep_APUL_pct"] - ra["dep_APUL_pct"]; dOwnL = rb["propres_APUL_pct"] - ra["propres_APUL_pct"]
    if dF > 0:
        if dOwn <= -0.5 * dF:
            cls = "substitution (R)"
        elif dDep >= dF and dOwn >= -0.5 * dF:
            cls = "tiree par la depense (H)"
        else:
            cls = "mixte"
    else:
        cls = "F en baisse : sans objet"
    log(f"T3a {a}-{b}: dF={dF:+.2f} dDep(APUL+ASSO)={dDep:+.2f} dPropres={dOwn:+.2f} | APUL seules dDep={dDepL:+.2f} dPropres={dOwnL:+.2f} -> {cls}")
    return dict(periode=f"{a}-{b}", dF=dF, dDep=dDep, dPropres=dOwn, dDep_APUL=dDepL, dPropres_APUL=dOwnL, classement=cls)

per = [(1978, 2025), (1978, 1989), (1989, 1999), (1999, 2009), (2009, 2019), (2019, 2025)]
rows_t3a = [period(a, b) for a, b in per]
# periodes de hausse de F sur au moins 3 ans consecutifs (identifiees mecaniquement)
Fs = {r["annee"]: r["F_pct"] for r in rows_t3}
up = [y for y in years[1:] if Fs[y] > Fs[y - 1]]
log("Annees ou F augmente :", up)

# T3b : differences premieres
yy = [y for y in years[1:] if y in A and (y - 1) in Fs]
dF = [Fs[y] - Fs[y - 1] for y in yy]
dsp = [A[y]["d_solde_primaire"] for y in yy]
o = ols(dF, dsp); lo, hi = r_ci(o["r"], o["n"])
log(f"T3b dF -> d_solde_primaire S13 : n={o['n']} r={o['r']:+.3f} IC95(r)=[{lo:+.3f};{hi:+.3f}] pente={o['pente']:+.3f} IC95=[{o['ic_bas']:+.3f};{o['ic_haut']:+.3f}] p_perm={perm_p(dF, dsp):.3f}")
log("   Puissance n=%d pour |r|=0,3 : %.2f ; |r|=0,4 : %.2f" % (o["n"], power_r(0.3, o["n"]), power_r(0.4, o["n"])))
yy2 = [y for y in yy if y not in crise]
o2 = ols([Fs[y] - Fs[y - 1] for y in yy2], [A[y]["d_solde_primaire"] for y in yy2]); lo2, hi2 = r_ci(o2["r"], o2["n"])
log(f"T3b hors crise : n={o2['n']} r={o2['r']:+.3f} IC95(r)=[{lo2:+.3f};{hi2:+.3f}]")
# variante post-2010 (D73 et D733 separement interpretables) et variante avec D9
yy3 = [y for y in yy if y >= 2011]
o3 = ols([Fs[y] - Fs[y - 1] for y in yy3], [A[y]["d_solde_primaire"] for y in yy3]); lo3, hi3 = r_ci(o3["r"], o3["n"])
log(f"T3b 2011-2025 : n={o3['n']} r={o3['r']:+.3f} IC95(r)=[{lo3:+.3f};{hi3:+.3f}]")
F9s = {r["annee"]: r["F_avec_D9_pct"] for r in rows_t3}
o4 = ols([F9s[y] - F9s[y - 1] for y in yy], dsp); lo4, hi4 = r_ci(o4["r"], o4["n"])
log(f"T3b variante avec D9 recus : n={o4['n']} r={o4['r']:+.3f} IC95(r)=[{lo4:+.3f};{hi4:+.3f}]")

# T3c : soldes cumules par sous-secteur (convention C1 publiee), en points de PIB
for a, b in ((1978, 2025), (2002, 2025)):
    sub = [r for r in rows_t3 if a <= r["annee"] <= b]
    log(f"T3c {a}-{b} soldes moyens (% PIB, C1) : Etat={np.mean([r['B9_Etat_pct'] for r in sub]):+.2f} APUL={np.mean([r['B9_APUL_pct'] for r in sub]):+.2f} ASSO={np.mean([r['B9_ASSO_pct'] for r in sub]):+.2f}")

with open(os.path.join(OUT, "S11_T3_financement.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_t3[0].keys()), delimiter=";")
    w.writeheader()
    for r in rows_t3:
        w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
with open(os.path.join(OUT, "S11_T3a_periodes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows_t3a[0].keys()), delimiter=";")
    w.writeheader()
    for r in rows_t3a:
        w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})

# ================= T4 =================
log("\n================ T4 - Tenue des normes par sous-secteur (descriptif, non confirmatoire) ================")
nor = read_csv(os.path.join(D, "S08", "S08_B_table_normes.csv"))
fam = lambda n: "ASSO" if n == "ONDAM" else ("APUL" if n in ("CAHORS_321", "LPFP23_APUL") else ("ETAT" if n.startswith("ETAT") else "AUTRE"))
agg = {}
for r in nor:
    k = fam(r["norme"])
    for t in ("t_init", "t_cour"):
        v = (r[t] or "").strip().lower()
        a = agg.setdefault((k, t), {"tenue": 0, "non": 0, "autre": 0, "valeurs": set()})
        a["valeurs"].add(v)
        if v in ("oui", "1", "tenue", "o", "true"):
            a["tenue"] += 1
        elif v in ("non", "0", "non tenue", "n", "false"):
            a["non"] += 1
        else:
            a["autre"] += 1
for (k, t), a in sorted(agg.items()):
    tot = a["tenue"] + a["non"]
    log(f"T4 {k:5s} {t}: tenues={a['tenue']} non tenues={a['non']} non etabli/autre={a['autre']} part tenue={'' if tot == 0 else round(a['tenue']/tot, 2)} (valeurs vues : {sorted(a['valeurs'])})")

with open(os.path.join(OUT, "S11_tests_sortie.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
