# -*- coding: utf-8 -*-
"""A02 - decompositions et tests sur 1960-2000 a partir de A02_series_1960_2000.csv.

1. Decomposition comptable de la variation annuelle du solde S13 (points de PIB) :
     d_solde = d_composante_cyclique(AMECO) - d_interets(Insee, % PIB) + residu
   Le residu (approx. variation du solde primaire corrige du cycle) melange mesures discretionnaires,
   elasticites des recettes differentes de l'unite, operations ponctuelles et erreurs d'estimation du PIB potentiel.
   Unites heterogenes (AMECO en % du PIB potentiel, Insee en % du PIB effectif) : approximation au premier ordre.
2. Variation du ratio depenses/PIB : part numerateur (croissance en volume de la depense deflatee par le prix du PIB)
   et part denominateur (croissance du PIB en volume). d(D/Y) ~ (D/Y)_{t-1} * (gD - gY)/(1+gY).
   Variante : part due au fait que le PIB croit moins que sa tendance 1960-1973 (5,4 % ; calculee ici).
3. Dynamique de la dette 1979-2000 : d(dette/PIB) = -solde primaire + effet boule de neige + ajustement stock-flux (residu).
Sortie : resultats/donnees/A02/A02_decompositions.csv et impression console.
"""
import csv, os, sys

R = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
src = os.path.join(R, "donnees", "A02", "A02_series_1960_2000.csv")
rows = {int(r["annee"]): {k: (float(v) if v not in ("",) else None) for k, v in r.items() if k != "annee"}
        for r in csv.DictReader(open(src, encoding="utf-8"), delimiter=";")}

def v(y, k):
    return rows.get(y, {}).get(k)

# tendance de croissance en volume 1960-1973 (moyenne geometrique)
g = [v(y, "pib_vol_pct") for y in range(1960, 1974)]
trend = 1.0
for x in g:
    trend *= 1 + x / 100
trend_6073 = (trend ** (1 / len(g)) - 1) * 100
g2 = [v(y, "pib_vol_pct") for y in range(1975, 2001)]
t2 = 1.0
for x in g2:
    t2 *= 1 + x / 100
trend_7500 = (t2 ** (1 / len(g2)) - 1) * 100
print("croissance moyenne en volume 1960-1973 : %.2f %% ; 1975-2000 : %.2f %%" % (trend_6073, trend_7500))

out = []
for y in range(1961, 2001):
    d = {"annee": y}
    s1, s0 = v(y, "solde_pct"), v(y - 1, "solde_pct")
    # solde recalcule avec plus de decimales (B9 / PIB) pour eviter l'arrondi a 0,1 de la serie publiee
    b1 = 100 * v(y, "b9_md_3201") / v(y, "pib_md"); b0 = 100 * v(y - 1, "b9_md_3201") / v(y - 1, "pib_md")
    d["solde_pct"] = b1
    d["d_solde"] = b1 - b0
    c1, c0 = v(y, "composante_cyclique_ameco"), v(y - 1, "composante_cyclique_ameco")
    d["d_cyclique"] = (c1 - c0) if (c1 is not None and c0 is not None) else None
    i1, i0 = v(y, "interets_payes_pct"), v(y - 1, "interets_payes_pct")
    d["d_interets_effet_solde"] = -(i1 - i0)
    d["residu_primaire_cvs"] = (d["d_solde"] - d["d_cyclique"] - d["d_interets_effet_solde"]) if d["d_cyclique"] is not None else None
    # ratio de depenses
    D1, D0 = v(y, "dep_md_3201"), v(y - 1, "dep_md_3201")
    Y1, Y0 = v(y, "pib_md"), v(y - 1, "pib_md")
    p = v(y, "deflateur_pib_pct") / 100
    gY = v(y, "pib_vol_pct") / 100
    gD = (D1 / D0) / (1 + p) - 1          # depense en volume (deflateur du PIB)
    r0, r1 = 100 * D0 / Y0, 100 * D1 / Y1
    d["dep_ratio"] = r1
    d["d_dep_ratio"] = r1 - r0
    d["croiss_depense_volume"] = 100 * gD
    d["croiss_pib_volume"] = 100 * gY
    d["part_numerateur"] = r0 * gD / (1 + gY)
    d["part_denominateur"] = -r0 * gY / (1 + gY)
    # contrefactuel : PIB a la tendance 1960-73 l'annee consideree (une seule annee, pas cumule)
    gT = trend_6073 / 100
    d["d_dep_ratio_si_pib_tendance6073"] = r0 * (1 + gD) / (1 + gT) - r0
    d["d_dep_ratio_si_pib_moyenne7500"] = r0 * (1 + gD) / (1 + trend_7500 / 100) - r0
    # recettes
    R1, R0 = v(y, "rec_md_3201"), v(y - 1, "rec_md_3201")
    d["rec_ratio"] = 100 * R1 / Y1
    d["d_rec_ratio"] = 100 * R1 / Y1 - 100 * R0 / Y0
    # dette
    db1, db0 = v(y, "dette_pct"), v(y - 1, "dette_pct")
    if db1 is not None and db0 is not None:
        gn = Y1 / Y0 - 1
        ip = v(y, "interets_payes_md")
        Dm0 = v(y - 1, "dette_md")
        i_eff = ip / Dm0
        d["taux_interet_apparent_pct"] = 100 * i_eff
        d["croiss_pib_nominal_pct"] = 100 * gn
        d["taux_reel_apparent_pct"] = 100 * ((1 + i_eff) / (1 + p) - 1)
        d["d_dette_pct"] = db1 - db0
        d["contrib_solde_primaire"] = -(v(y, "solde_primaire_pct"))
        d["contrib_boule_de_neige"] = db0 * (i_eff - gn) / (1 + gn)
        d["contrib_stock_flux_residu"] = d["d_dette_pct"] - d["contrib_solde_primaire"] - d["contrib_boule_de_neige"]
        d["dette_md_var"] = v(y, "dette_md") - Dm0
        d["deficit_md"] = -v(y, "b9_md_3201")
        d["ajust_stock_flux_md"] = d["dette_md_var"] - d["deficit_md"]
    out.append(d)

cols = []
for d in out:
    for k in d:
        if k not in cols:
            cols.append(k)
dest = os.path.join(R, "donnees", "A02", "A02_decompositions.csv")
with open(dest, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
    w.writeheader()
    for d in out:
        w.writerow({k: ("" if d.get(k) is None else (round(d[k], 3) if isinstance(d[k], float) else d[k])) for k in cols})
print("ecrit", dest)

def f(x, n=2):
    return "   n.d." if x is None else ("%7.*f" % (n, x))
print("\nan    solde  d_solde d_cycl  d_int  resid | dep%  d_dep  num   denom  gD    gY   d_dep(si g=tend) | d_rec")
for d in out:
    if d["annee"] >= 1970:
        print(d["annee"], f(d["solde_pct"]), f(d["d_solde"]), f(d["d_cyclique"]), f(d["d_interets_effet_solde"]), f(d["residu_primaire_cvs"]), "|",
              f(d["dep_ratio"], 1), f(d["d_dep_ratio"]), f(d["part_numerateur"]), f(d["part_denominateur"]), f(d["croiss_depense_volume"], 1), f(d["croiss_pib_volume"], 1),
              f(d["d_dep_ratio_si_pib_tendance6073"]), "|", f(d["d_rec_ratio"]))
print("\nan   d_dette  prim   bdn   sfa | i_app  g_nom  r_reel | var_dette_md deficit_md sfa_md")
for d in out:
    if "d_dette_pct" in d:
        print(d["annee"], f(d["d_dette_pct"]), f(d["contrib_solde_primaire"]), f(d["contrib_boule_de_neige"]), f(d["contrib_stock_flux_residu"]), "|",
              f(d["taux_interet_apparent_pct"]), f(d["croiss_pib_nominal_pct"]), f(d["taux_reel_apparent_pct"]), "|",
              f(d["dette_md_var"], 1), f(d["deficit_md"], 1), f(d["ajust_stock_flux_md"], 1))

# Sommes par sous-periode
def somme(a, b, k):
    return sum(d[k] for d in out if a <= d["annee"] <= b and d.get(k) is not None)
print("\nPlus fortes hausses du ratio de depenses : part due a une croissance du PIB inferieure a la tendance")
for d in sorted(out, key=lambda d: -d["d_dep_ratio"])[:6]:
    a, b6, b7 = d["d_dep_ratio"], d["d_dep_ratio_si_pib_tendance6073"], d["d_dep_ratio_si_pib_moyenne7500"]
    print("%d hausse %.2f | si PIB a 5,79 %%: %.2f -> part denominateur %.2f | si PIB a 2,43 %%: %.2f -> part denominateur %.2f" % (d["annee"], a, b6, a - b6, b7, a - b7))
print("\nSous-periodes (somme des variations, points de PIB) :")
for a, b in [(1975, 1975), (1976, 1980), (1981, 1983), (1984, 1990), (1991, 1993), (1994, 1997), (1998, 2000), (1975, 2000), (1974, 1993)]:
    print("%d-%d d_solde %6.2f | cycl %6.2f | interets %6.2f | residu %6.2f || d_dep %6.2f (num %6.2f denom %6.2f) d_rec %6.2f" % (
        a, b, somme(a, b, "d_solde"), somme(a, b, "d_cyclique"), somme(a, b, "d_interets_effet_solde"), somme(a, b, "residu_primaire_cvs"),
        somme(a, b, "d_dep_ratio"), somme(a, b, "part_numerateur"), somme(a, b, "part_denominateur"), somme(a, b, "d_rec_ratio")))
