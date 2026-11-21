# -*- coding: utf-8 -*-
"""A18 partie 2 - verification independante de chiffres centraux de la cellule.
Sources : base commune (lecture seule) + pieces retelechargees par A18 (donnees\\A18\\sources\\p2).
Aucun script d'agent n'est reutilise. Fichiers d'agents lus seulement quand c'est dit (copie).
Sortie : donnees\\A18\\a18_p2_verif_sortie.txt"""
import csv, json, os, zipfile, unicodedata
import openpyxl

R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
C = os.path.join(R, "commun"); P2 = os.path.join(R, "A18", "sources", "p2")
OUT = os.path.join(R, "A18", "a18_p2_verif_sortie.txt")
L = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().strip().lower()

# ---------------------------------------------------------------- Insee base 2020 (base commune)
def insee_csv(f):
    d = {}
    with open(os.path.join(C, f), encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            d.setdefault((norm(r["feuille"]), norm(r["unite"]), norm(r["serie"])), {})[int(r["annee"])] = float(r["valeur"])
    return d
DR = insee_csv("base_insee_dep_rec_pctPIB.csv")
def drs(prefix):
    for k, v in DR.items():
        if k[2].startswith(prefix):
            return v
dep, rec, sol = drs("depenses"), drs("recettes"), drs("deficit au sens")
dette_pct = drs("dette des administrations publiques (brute)")
SS = insee_csv("base_insee_solde_sous_secteurs.csv")
sol_md = SS[("figure 1", "en milliards d'euros", "ensemble")]
DT = insee_csv("base_insee_dette_sous_secteurs.csv")
dette_md = DT[("figure 1", "en milliards d'euros", "ensemble")]

# t_3201 : Md EUR, S13
wb = openpyxl.load_workbook(os.path.join(C, "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
rows = list(wb.worksheets[0].iter_rows(values_only=True))
def _yr(x):
    try:
        v = int(float(str(x).strip()))
        return v if 1900 < v < 2100 else None
    except ValueError:
        return None
ycol = {j: _yr(x) for j, x in enumerate(rows[2]) if _yr(x) is not None}
log("t_3201 colonnes d'annees :", min(ycol.values()), "-", max(ycol.values()), "; premiere colonne", min(ycol))
def t(rowidx):
    return {y: float(rows[rowidx][j]) for j, y in ycol.items() if rows[rowidx][j] not in (None, " ")}
def lab(i):
    return norm(next((x for x in rows[i][:2] if x not in (None, " ")), ""))
for i, pref in ((11, "interets (d41)"), (26, "total des depenses"), (15, "prestations sociales autres"), (16, "transferts sociaux en nature"), (65, "capacite")):
    assert lab(i).startswith(pref), (i, lab(i))
D41, TE_md, D62, D632, B9_md = t(11), t(26), t(15), t(16), t(65)
# PIB nominal (Md EUR) = depenses Md / depenses % PIB
Y = {y: TE_md[y] / dep[y] * 100 for y in TE_md if y in dep}
log("Controle PIB 2025 (Md EUR) :", round(Y[2025], 1), "; B9 t_3201 2025 :", round(B9_md[2025], 1), "; solde Figure 1 :", sol_md.get(2025))

# ---------------------------------------------------------------- V01-V04
neg = [y for y in sorted(sol) if y >= 1960]
last_pos = max(y for y in sol if sol[y] > 0)
run = [y for y in range(last_pos + 1, 2026) if sol[y] < 0]
log("\nV01 dernier excedent :", last_pos, round(sol[last_pos], 2), "% ; annees de deficit consecutives", run[0], "-", run[-1], ":", len(run))
log("V01 controle Md EUR (Figure 1) : 1974", sol_md.get(1974), "; nb deficits 1975-2025 :", sum(1 for y in range(1975, 2026) if sol_md[y] < 0))
log("V02 annees excedentaires 1960-1974 :", [(y, round(sol[y], 2)) for y in range(1960, 1975) if sol[y] > 0])
log("V03 solde 2025 :", sol_md[2025], "Md EUR ;", round(sol[2025], 3), "% PIB")
log("V04 dep/rec 1974 :", round(dep[1974], 2), round(rec[1974], 2), "; 2025 :", round(dep[2025], 2), round(rec[2025], 2),
    "; hausses :", round(dep[2025] - dep[1974], 2), round(rec[2025] - rec[1974], 2),
    "; dep 1985 :", round(dep[1985], 2), "acquis en 1985 :", round(dep[1985] - dep[1974], 2),
    "soit", round(100 * (dep[1985] - dep[1974]) / (dep[2025] - dep[1974]), 1), "%")

# ---------------------------------------------------------------- Eurostat helpers
def eu_csv(f):
    d = {}
    with open(os.path.join(C, f), encoding="utf-8") as h:
        for r in csv.DictReader(h):
            if r["value"] not in ("", None):
                key = tuple(r[k] for k in r if k not in ("value", "status", "freq"))
                d[key] = float(r["value"])
    return d
def js(p):
    j = json.load(open(p, encoding="utf-8"))
    dims, size = j["id"], j["size"]
    idx = {d: {v: k for k, v in j["dimension"][d]["category"]["index"].items()} for d in dims}
    out = {}
    for flat, val in j["value"].items():
        flat = int(flat); key = []
        for d, s in zip(reversed(dims), reversed(size)):
            key.append(idx[d][flat % s]); flat //= s
        out[tuple(reversed(key))] = val
    return dims, out
MAIN = eu_csv("eurostat_gov_10a_main.csv")   # (unit, sector, na_item, geo, time)
def m(unit, item, geo, year, sector="S13"):
    return MAIN.get((unit, sector, item, geo, str(year)))

# V05 : ecarts 2025 avec la zone euro, avec et sans la France (montants)
for yr in (2024, 2025):
    res = {}
    for it in ("TE", "TR"):
        fr, ea = m("MIO_EUR", it, "FR", yr), m("MIO_EUR", it, "EA20", yr)
        yfr = fr / m("PC_GDP", it, "FR", yr) * 100; yea = ea / m("PC_GDP", it, "EA20", yr) * 100
        hf = (ea - fr) / (yea - yfr) * 100
        res[it] = (round(fr / yfr * 100, 2), round(ea / yea * 100, 2), round(hf, 2), round(fr / yfr * 100 - ea / yea * 100, 2), round(fr / yfr * 100 - hf, 2))
    log(f"\nV05 {yr} (FR, EA20, EA20 hors FR, ecart avec EA20, ecart hors FR) : depenses {res['TE']} ; recettes {res['TR']}")

# V06 : COFOG 2024 en montants (piece retelechargee) ; PIB nama
dims, CO = js(os.path.join(P2, "eurostat_gov_10a_exp_MIOEUR_FR_EA20_2022_2024.json"))
dn, NA = js(os.path.join(P2, "eurostat_nama_10_gdp_FR_EA20_B1GQ.json"))
def gdp(geo, yr, unit="CP_MEUR"):
    return NA.get(("A", unit, "B1GQ", geo, str(yr)))
def co(geo, code, yr):
    return CO.get(("A", "MIO_EUR", "S13", code, "TE", geo, str(yr)))
for yr in (2022, 2023, 2024):
    yfr, yea = gdp("FR", yr), gdp("EA20", yr)
    def ratios(code):
        fr, ea = co("FR", code, yr), co("EA20", code, yr)
        if fr is None or ea is None:
            return None
        return fr / yfr * 100, ea / yea * 100, (ea - fr) / (yea - yfr) * 100
    tot = ratios("TOTAL")
    gap_hf = tot[0] - tot[2]; gap_ea = tot[0] - tot[1]
    soc = ratios("GF10"); hea = ratios("GF07"); old = ratios("GF1002"); intr = ratios("GF0107")
    gs = (soc[0] - soc[2]) + (hea[0] - hea[2])
    log(f"V06 {yr} COFOG montants : total FR {tot[0]:.2f} EA {tot[1]:.2f} EAhorsFR {tot[2]:.2f} | ecart hors FR {gap_hf:.2f} (avec FR {gap_ea:.2f}) | "
        f"prot. sociale+sante hors FR {gs:.2f} = {100*gs/gap_hf:.1f} % | reste {gap_hf-gs:.2f} | vieillesse hors FR {old[0]-old[2]:.2f} (avec FR {old[0]-old[1]:.2f})"
        + (f" | interets GF0107 hors FR {intr[0]-intr[2]:.2f}" if intr else ""))
    if yr == 2024:
        det = []
        for code in ("GF01", "GF02", "GF03", "GF04", "GF05", "GF06", "GF08", "GF09"):
            r_ = ratios(code)
            det.append(f"{code} {r_[0]-r_[2]:+.2f}")
        log("     detail hors protection sociale et sante (hors FR) :", " ; ".join(det))

# V07 : excedents primaires 2002-2025 (B9 + D41PAY, % PIB) - base commune
geos = sorted(set(k[3] for k in MAIN))
cnt = {}
for g in geos:
    n = 0; ok = True
    for yr in range(2002, 2026):
        b, i = m("PC_GDP", "B9", g, yr), m("PC_GDP", "D41PAY", g, yr)
        if b is None or i is None:
            ok = False; continue
        n += (b + i) > 0
    cnt[g] = (n, ok)
log("\nV07 excedents primaires 2002-2025 :", {g: cnt[g][0] for g in geos}, "; series incompletes :", [g for g in geos if not cnt[g][1]])

# ---------------------------------------------------------------- V09-V13 dette (Insee : t_3201 + dette Md)
d = {y: dette_md[y] / Y[y] * 100 for y in dette_md if y in Y}
log("\nControle ratio dette calcule/publie 1978, 1996, 2025 :", [(y, round(d[y], 1), round(dette_pct[y], 1)) for y in (1978, 1996, 2025)])
def decomp(a, b):
    S = {"var": 0, "prim": 0, "bdn": 0, "res": 0}
    for y in range(a, b + 1):
        g = Y[y] / Y[y - 1] - 1
        pd = -(B9_md[y] + D41[y]) / Y[y] * 100
        bdn = D41[y] / Y[y] * 100 - d[y - 1] * g / (1 + g)
        dv = d[y] - d[y - 1]
        S["var"] += dv; S["prim"] += pd; S["bdn"] += bdn; S["res"] += dv - pd - bdn
    return {k: round(v, 1) for k, v in S.items()}
log("V09 1979-2025 :", decomp(1979, 2025))
log("V09b dont 1979-1998 :", decomp(1979, 1998), "; 1999-2025 :", decomp(1999, 2025))
log("V10 2001-2025 :", decomp(2001, 2025))
log("V11 1984-1997 :", decomp(1984, 1997), "; 1987-1998 :", decomp(1987, 1998))
log("V11b 1979-1990 :", decomp(1979, 1990))
ip = {y: D41[y] / Y[y] * 100 for y in range(1974, 2026)}
ymax = max(ip, key=ip.get)
log("V12 charge d'interets max :", ymax, round(ip[ymax], 2), "% ; 1995-1997 :", [(y, round(ip[y], 2)) for y in (1995, 1996, 1997)], "; 2025 :", round(ip[2025], 2))
baisses = [y for y in range(1979, 2026) if dette_pct[y] < dette_pct[y - 1]]
log("V13 annees de baisse du ratio de dette (serie publiee) depuis 1978 :", len(baisses), baisses)
pre = {1993: None}
log("V13b ratio 2007 / 2019 / 2025 :", round(dette_pct[2007], 1), round(dette_pct[2019], 1), round(dette_pct[2025], 1), "; maximum ulterieur toujours superieur au niveau d'avant-crise ?",
    [ (c, round(dette_pct[c], 1), round(min(dette_pct[y] for y in range(c + 1, 2026)), 1)) for c in (1980, 1992, 2007, 2019)])

# V20/V21 soldes primaires
pb = {y: (B9_md[y] + D41[y]) / Y[y] * 100 for y in range(1974, 2026)}
log("\nV20 solde primaire 2010 / 2014 :", round(pb[2010], 2), round(pb[2014], 2), "; 2014 -> 2019 :", round(pb[2014], 2), "->", round(pb[2019], 2),
    "(", round(pb[2019] - pb[2014], 2), ") ; interets 2014 -> 2019 :", round(ip[2014], 2), "->", round(ip[2019], 2), "(", round(ip[2019] - ip[2014], 2), ")")
log("V20b solde primaire 2015 -> 2019 :", round(pb[2015], 2), "->", round(pb[2019], 2), "(", round(pb[2019] - pb[2015], 2), ") ; interets 2015->2019 :", round(ip[2019] - ip[2015], 2))
log("V21 2025 : solde primaire", round(pb[2025], 2), "% (", round(B9_md[2025] + D41[2025], 1), "Md) ; interets", round(ip[2025], 2))
exc = [y for y in range(1975, 2026) if pb[y] > 0]
log("V14b excedents primaires 1975-2025 (Insee) :", exc)

# V14 : 37 exercices de majorite absolue (classement : copie A09) contre deficits (Insee, A18)
with open(os.path.join(R, "A09", "a09_table_exercices_1975_2025.csv"), encoding="utf-8") as h:
    rr = list(csv.DictReader(h, delimiter=";"))
types = sorted(set(r["type_majorite"] for r in rr))
log("V14 types de majorite (copie A09) :", types)
for ty in types:
    ys = [int(r["exercice"]) for r in rr if r["type_majorite"] == ty]
    log(f"   {ty} : n={len(ys)} ; deficits (Insee) {sum(1 for y in ys if sol[y] < 0)} ; excedents primaires {[y for y in ys if pb[y] > 0]}")
ABS = ("parti_seul", "coalition", "coalition_etroite", "coalition_non_etablie")
abso = [int(r["exercice"]) for r in rr if r["type_majorite"] in ABS]
log("V14 (convention A18 : majorite absolue = parti seul + coalitions, y compris etroite et non etablie)")
log("V14 exercices 'absolue' :", len(abso), "; dont en deficit (Insee) :", sum(1 for y in abso if sol[y] < 0), "; excedents primaires parmi eux :", [y for y in abso if pb[y] > 0])

# V22 : volume de la depense primaire (deflateur du PIB, Eurostat nama)
defl = {}
for yr in range(1975, 2026):
    cp, cl = gdp("FR", yr), gdp("FR", yr, "CLV20_MEUR") or gdp("FR", yr, "CLV10_MEUR")
    if cp and cl:
        defl[yr] = cp / cl
vol = {}
for yr in range(1996, 2026):
    if yr in defl and yr - 1 in defl:
        vol[yr] = ((TE_md[yr] - D41[yr]) / defl[yr]) / ((TE_md[yr - 1] - D41[yr - 1]) / defl[yr - 1]) * 100 - 100
log("\nV22 croissance en volume de la depense primaire (deflateur PIB) :", {y: round(v, 2) for y, v in vol.items()})
log("V22 annees <= 0 depuis 1996 :", [y for y in vol if vol[y] <= 0])
def moy(a, b):
    p = 1
    for y in range(a, b + 1):
        p *= 1 + vol[y] / 100
    return round((p ** (1 / (b - a + 1)) - 1) * 100, 2)
log("V22 moyennes 1996-2007", moy(1996, 2007), "; 2010-2019", moy(2010, 2019), "; 2015-2019", moy(2015, 2019))
trois = [(y, y + 2) for y in range(1996, 2024) if all(vol.get(z, 9) <= 0 for z in (y, y + 1, y + 2))]
log("V22 periodes de 3 ans consecutifs a volume <= 0 (brut, sans neutralisation) :", trois)

# V23 : protection sociale 1974-1985 (t_3201)
ps = {y: (D62[y] + D632[y]) / Y[y] * 100 for y in (1974, 1985)}
log("\nV23 prestations D62+D632 % PIB 1974 / 1985 :", round(ps[1974], 2), round(ps[1985], 2), "hausse", round(ps[1985] - ps[1974], 2),
    "; dont D62 :", round(D62[1985] / Y[1985] * 100 - D62[1974] / Y[1974] * 100, 2))

# V16 : taux de prelevements (Eurostat taxag) et rang 2025
TX = eu_csv("eurostat_gov_10a_taxag.csv")   # (unit, sector, na_item, geo, time)
items = sorted(set(k[2] for k in TX))
cand = [i for i in items if i.startswith("D2_D5_D91_D61")]
log("\nV16 agregats disponibles :", cand)
agg = "D2_D5_D91_D61_M_D995" if "D2_D5_D91_D61_M_D995" in items else cand[0]
for yr in (2017, 2022, 2023, 2025):
    log(f"V16 {agg} FR {yr} :", TX.get(("PC_GDP", "S13_S212", agg, "FR", str(yr))))
rk = sorted(((TX.get(("PC_GDP", "S13_S212", agg, g, "2025")) or -1, g) for g in set(k[3] for k in TX) if g not in ("EA20", "EU27_2020")), reverse=True)
log("V16b rang 2025 (pays de la base) :", rk[:5])
rk24 = sorted(((TX.get(("PC_GDP", "S13_S212", agg, g, "2024")) or -1, g) for g in set(k[3] for k in TX) if g not in ("EA20", "EU27_2020")), reverse=True)
log("V16b rang 2024 :", rk24[:4])

# V24 : 2015-2019, pays dont le ratio de dette monte (edpt1)
ED = eu_csv("eurostat_gov_10dd_edpt1.csv")
up = [(g, ED.get(("PC_GDP", "S13", "GD", g, "2015")), ED.get(("PC_GDP", "S13", "GD", g, "2019"))) for g in sorted(set(k[3] for k in ED))]
log("\nV24 dette 2015 -> 2019 :", [(g, a, b) for g, a, b in up if a and b], "; en hausse :", [g for g, a, b in up if a and b and b > a])

# V25 : part structurelle (AMECO retelecharge)
z = zipfile.ZipFile(os.path.join(P2, "ameco", "ameco17.zip"))
txt = z.read([n for n in z.namelist() if n.upper().endswith(".TXT")][0]).decode("latin-1").splitlines()
hd = [x.strip() for x in txt[0].split(";")]
for ln in txt[1:]:
    p = ln.split(";")
    if p[0].startswith("FRA.") and (p[0].endswith(".UBLGAPS") or p[0].endswith(".UBLG") or p[0].endswith(".UBLGAP")):
        vals = {hd[i]: p[i].strip() for i in range(len(p)) if hd[i] in ("2024", "2025", "2026")}
        log("V25 AMECO", p[0], p[2].strip()[:60], p[4].strip()[:50], vals)

# V18 : ecart programme - execute (programme : copie A08 ; execute : Insee, A18)
with open(os.path.join(R, "A08", "A08_programme_vs_execute.csv"), encoding="utf-8") as h:
    pv = list(csv.DictReader(h, delimiter=";"))
def f_(x):
    try:
        return float(str(x).replace(",", "."))
    except ValueError:
        return None
for hz in ("0", "1", "2", "3"):
    sel = [r for r in pv if r["horizon"] == hz and f_(r["solde_programme"]) is not None and int(r["annee_cible"]) <= 2025]
    nocr = [r for r in sel if norm(r["fenetre_touche_crise"]) in ("non", "false", "0", "")]
    gaps = [sol[int(r["annee_cible"])] - f_(r["solde_programme"]) for r in sel]
    gaps2 = [sol[int(r["annee_cible"])] - f_(r["solde_programme"]) for r in nocr]
    diff = [abs(sol[int(r["annee_cible"])] - f_(r["solde_execute_base2020"])) for r in sel if f_(r["solde_execute_base2020"]) is not None]
    log(f"V18 h={hz} : n={len(sel)} ecart moyen {sum(gaps)/len(gaps):.2f} ; hors fenetres de crise n={len(nocr)} {sum(gaps2)/max(1,len(nocr)):.2f} ; "
        f"ecart max entre mon execute et celui d'A08 : {max(diff) if diff else None}")
log("V18 valeurs de fenetre_touche_crise :", sorted(set(r["fenetre_touche_crise"] for r in pv)))

# V26 : enveloppes (copies A13 et A14)
for f, a in (("A13", "A13_enveloppes.csv"), ("A14", "A14_enveloppes.csv")):
    with open(os.path.join(R, f, a), encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            vals = list(r.values())
            if "2030" in vals:
                log("V26", f, {k: v for k, v in r.items() if v not in ("",)})

with open(OUT, "w", encoding="utf-8") as h:
    h.write("\n".join(L))
