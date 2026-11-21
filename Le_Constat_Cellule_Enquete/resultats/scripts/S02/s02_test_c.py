"""S02 - Test C : composition du redressement OBSERVE (non des mesures) pour les episodes de la liste d'A12.
Entrees (copies des pieces d'A12, jamais ses fichiers) : donnees\\S02\\copies_A12\\oecd_eo119_finpub.csv (YRGTQ recettes,
YPGTQ depenses, NLGQ solde, NLGXQ primaire hors interets nets, NLGXQA primaire corrige du cycle), oecd_eo119_interets.csv
(GGINTP interets verses), oecd_eo119_macro.csv (GDP nominal).
Sortie : donnees\\S02\\S02_test_c_composition_observee.csv
Definitions :
  depenses primaires = YPGTQ - GGINTP/GDP (interets bruts verses) ; solde primaire (brut) = YRGTQ - depenses primaires.
  d_primaire_brut = d_recettes - d_dep_primaires.
  effet de denominateur d'un ratio X/Y entre t0 et t1 : X0/Y1 - X0/Y0 ; effet du numerateur : (X1-X0)/Y1.
  part_cycle (niveau D) = d(NLGXQ) - d(NLGXQA) : variation du primaire OCDE attribuee au cycle par l'OCDE (estimation 2026).
  part_depenses = -d_dep_primaires / d_primaire_brut ; part_recettes = d_recettes / d_primaire_brut (si d_primaire_brut > 0.5).
Identite comptable : ne dit rien des causes.
"""
import csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S02"
C = os.path.join(R, "copies_A12")
EP = [("E1", "SWE", 1993), ("E2", "CAN", 1994), ("E3", "DNK", 1982), ("E4", "BEL", 1992), ("E5", "ITA", 1991),
      ("E6", "DEU", 2002), ("E7", "GBR", 2009), ("E8", "PRT", 2009), ("E9", "GRC", 2009), ("E10", "JPN", 1996),
      ("E11a", "ESP", 2009), ("E11c", "IRL", 2009), ("E11d", "FIN", 1993), ("E11e", "NLD", 1982),
      ("REF1", "FRA", 1993), ("REF2", "FRA", 2010)]
want = {"YRGTQ", "YPGTQ", "NLGQ", "NLGXQ", "NLGXQA", "GGINTP", "GDP"}
d = {}
for fn in ["oecd_eo119_finpub.csv", "oecd_eo119_interets.csv", "oecd_eo119_macro.csv"]:
    with open(os.path.join(C, fn), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["MEASURE"] in want and r["OBS_VALUE"]:
                d[(r["REF_AREA"], r["MEASURE"], int(r["TIME_PERIOD"]))] = float(r["OBS_VALUE"])


def g(c, m, y):
    return d.get((c, m, y))


rows = []
for ep, c, t0 in EP:
    for h in (3, 5, 10):
        t1 = t0 + h
        try:
            Y0, Y1 = g(c, "GDP", t0), g(c, "GDP", t1)
            r0, r1 = g(c, "YRGTQ", t0), g(c, "YRGTQ", t1)
            e0, e1 = g(c, "YPGTQ", t0), g(c, "YPGTQ", t1)
            i0, i1 = g(c, "GGINTP", t0) / Y0 * 100, g(c, "GGINTP", t1) / Y1 * 100
        except TypeError:
            rows.append([ep, c, t0, t1] + ["n.d."] * 14); continue
        p0, p1 = e0 - i0, e1 - i1
        dr, dp, di = r1 - r0, p1 - p0, i1 - i0
        dprim = dr - dp
        den_r = r0 * (Y0 / Y1) - r0
        den_p = p0 * (Y0 / Y1) - p0
        nom_p = dp - den_p
        nominal_growth = (Y1 / Y0 - 1) * 100
        x0, x1 = g(c, "NLGXQ", t0), g(c, "NLGXQ", t1)
        a0, a1 = g(c, "NLGXQA", t0), g(c, "NLGXQA", t1)
        cyc = round((x1 - x0) - (a1 - a0), 2) if None not in (x0, x1, a0, a1) else "n.d."
        sh_d = round(-dp / dprim * 100) if dprim > 0.5 else "n.s."
        sh_r = round(dr / dprim * 100) if dprim > 0.5 else "n.s."
        # variation nominale des depenses primaires en valeur
        pval = (p1 * Y1) / (p0 * Y0) * 100 - 100
        rows.append([ep, c, t0, t1, round(r0, 2), round(p0, 2), round(i0, 2), round(dr, 2), round(dp, 2), round(di, 2),
                     round(dprim, 2), sh_d, sh_r, round(den_p, 2), round(nom_p, 2), round(pval, 1), round(nominal_growth, 1), cyc])
hdr = ["episode", "pays", "t0", "t1", "recettes_t0", "dep_primaires_t0", "interets_t0", "d_recettes", "d_dep_primaires",
       "d_interets", "d_primaire_brut", "part_depenses_pct", "part_recettes_pct", "d_dep_prim_effet_denominateur",
       "d_dep_prim_effet_numerateur", "dep_primaires_var_valeur_pct", "PIB_nominal_var_pct", "part_cycle_OCDE_pts"]
out = os.path.join(R, "S02_test_c_composition_observee.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(hdr); w.writerows(rows)
print(";".join(hdr))
for r in rows:
    print(";".join(str(x) for x in r))
