# -*- coding: utf-8 -*-
"""A17 - calculs historiques sur la table d'A07 (lecture seule).
Lancer : python -I a17_historique_taux_croissance.py
Entree : donnees\\A07\\table_france_1974_2025.csv (construite par A07 sur donnees\\commun, Insee base 2020,
         Eurostat ; taux OCDE/BCE).
Sorties : donnees\\A17\\a17_r_moins_g_par_periode.csv, a17_tendance_pib.csv, a17_recettes_2017_2025.txt,
          a17_sortie_historique.txt
Objet :
 1. ecart taux - croissance nominale par periode, sous deux definitions :
    (a) taux apparent (interets / dette de l'annee precedente, colonne d'A07) ;
    (b) taux "a l'emission" construit comme dans A15 : 0,6 x taux 10 ans + 0,4 x taux 3 mois + 0,5 pt
        (parametres retenus par A15, C-A15-001), pour comparer a l'hypothese de long terme d'A15
        (r_m = 4,0 % contre croissance nominale 2,77 %, soit +1,2 pt).
 2. ecart du PIB reel a sa tendance 1997-2007 prolongee (ce n'est PAS un ecart de production) et
    effet de denominateur sur le ratio de dette (borne haute, purement arithmetique).
 3. recettes et depenses en % du PIB, 2017 contre 2025.
 4. effet boule de neige cumule par sous-periode (colonne d'A07), pour confronter la prediction P4.
"""
import csv, os, math

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
ENTREE = os.path.join(RACINE, "donnees", "A07", "table_france_1974_2025.csv")
SORTIE = os.path.join(RACINE, "donnees", "A17")
LOG = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

def lire():
    out = {}
    with open(ENTREE, encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            d = {}
            for k, v in r.items():
                try:
                    d[k] = float(v)
                except (TypeError, ValueError):
                    d[k] = None
            out[int(r["annee"])] = d
    return out

T = lire()

def moy(vals):
    v = [x for x in vals if x is not None and not math.isnan(x)]
    return (sum(v) / len(v), len(v)) if v else (None, 0)

# ------------------------------------------------------------------ 1. r - g par periode
PERIODES = [(1979, 1986), (1987, 1998), (1991, 1998), (1999, 2007), (2008, 2014), (2015, 2021),
            (2022, 2025), (1999, 2025), (2010, 2025), (1979, 2025)]
lignes = []
for a0, a1 in PERIODES:
    ans = range(a0, a1 + 1)
    g = moy([T[a]["croiss_nominale_pct"] for a in ans])[0]
    ia = moy([T[a]["taux_apparent_pct"] for a in ans])
    # taux "a l'emission" facon A15
    rms = []
    for a in ans:
        t10, t3 = T[a]["taux10_FR"], T[a]["taux3m_FR"]
        if t10 is None or t3 is None or math.isnan(t10) or math.isnan(t3):
            rms.append(None)
        else:
            rms.append(max(0.0, 0.6 * t10 + 0.4 * t3) + 0.5)
    rm = moy(rms)
    t10m = moy([T[a]["taux10_FR"] for a in ans])[0]
    gap_app = moy([(T[a]["taux_apparent_pct"] - T[a]["croiss_nominale_pct"]) if T[a]["taux_apparent_pct"] is not None else None for a in ans])
    gap_rm = moy([(r - T[a]["croiss_nominale_pct"]) if r is not None else None for a, r in zip(ans, rms)])
    sb = sum((T[a]["contrib_boule_de_neige_pts"] or 0.0) for a in ans if T[a]["contrib_boule_de_neige_pts"] is not None)
    sp = sum((T[a]["contrib_solde_primaire_pts"] or 0.0) for a in ans if T[a]["contrib_solde_primaire_pts"] is not None)
    l = dict(periode=f"{a0}-{a1}", croissance_nominale_moy=g, taux_apparent_moy=ia[0], n_taux_apparent=ia[1],
             taux_10ans_moy=t10m, taux_emission_facon_A15_moy=rm[0], n_emission=rm[1],
             ecart_apparent_moins_g=gap_app[0], ecart_emission_moins_g=gap_rm[0],
             boule_de_neige_cumulee_pts=sb, deficits_primaires_cumules_pts=sp)
    lignes.append(l)
    log(f"{a0}-{a1}: g={g:.2f}  i_app={ia[0] if ia[0] is None else round(ia[0],2)}  r_m(A15)={rm[0] if rm[0] is None else round(rm[0],2)}  "
        f"i_app-g={gap_app[0] if gap_app[0] is None else round(gap_app[0],2)}  r_m-g={gap_rm[0] if gap_rm[0] is None else round(gap_rm[0],2)}  "
        f"boule de neige cumulee={sb:.1f} pts ; deficits primaires cumules={sp:.1f} pts")

# annees avec r_m - g >= +1,2 pt (hypothese A15 de long terme), depuis 1999
n_sup = [a for a in range(1999, 2026) if T[a]["taux10_FR"] is not None and T[a]["taux3m_FR"] is not None
         and (max(0.0, 0.6 * T[a]["taux10_FR"] + 0.4 * T[a]["taux3m_FR"]) + 0.5 - T[a]["croiss_nominale_pct"]) >= 1.2]
log("Annees 1999-2025 ou le taux a l'emission facon A15 depasse la croissance nominale d'au moins 1,2 pt :", n_sup)
n_sup_app = [a for a in range(1999, 2026) if T[a]["taux_apparent_pct"] is not None
             and (T[a]["taux_apparent_pct"] - T[a]["croiss_nominale_pct"]) >= 1.2]
log("Annees 1999-2025 ou le taux apparent depasse la croissance nominale d'au moins 1,2 pt :", n_sup_app)

with open(os.path.join(SORTIE, "a17_r_moins_g_par_periode.csv"), "w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=list(lignes[0].keys()), delimiter=";")
    w.writeheader()
    for l in lignes:
        w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})

# ------------------------------------------------------------------ 2. PIB reel et tendance 1997-2007
idx = {1974: 100.0}
for a in range(1975, 2026):
    g = T[a]["croiss_reelle_pct"]
    idx[a] = idx[a - 1] * (1 + g / 100.0)
# tendance log-lineaire 1997-2007 (moindres carres)
xs = list(range(1997, 2008))
ys = [math.log(idx[a]) for a in xs]
xb = sum(xs) / len(xs); yb = sum(ys) / len(ys)
b = sum((x - xb) * (y - yb) for x, y in zip(xs, ys)) / sum((x - xb) ** 2 for x in xs)
c = yb - b * xb
log(f"Tendance du PIB reel 1997-2007 : {100*(math.exp(b)-1):.2f} % par an")
# variante : tendance 1990-2007
xs2 = list(range(1990, 2008)); ys2 = [math.log(idx[a]) for a in xs2]
xb2 = sum(xs2) / len(xs2); yb2 = sum(ys2) / len(ys2)
b2 = sum((x - xb2) * (y - yb2) for x, y in zip(xs2, ys2)) / sum((x - xb2) ** 2 for x in xs2)
c2 = yb2 - b2 * xb2
log(f"Tendance du PIB reel 1990-2007 : {100*(math.exp(b2)-1):.2f} % par an")
tl = []
for a in (2007, 2009, 2012, 2014, 2019, 2021, 2025):
    tr = math.exp(c + b * a); tr2 = math.exp(c2 + b2 * a)
    ec = 100 * (idx[a] / tr - 1); ec2 = 100 * (idx[a] / tr2 - 1)
    d = T[a]["dette_pct"]
    # effet de denominateur seul : meme dette en euros, PIB nominal porte a la tendance (PIB x 1/(1+ec)),
    # donc ratio x (1+ec). Borne arithmetique, pas un contrefactuel : la tendance 1997-2007 n'est pas un potentiel.
    d_cf = d * (1 + ec / 100.0) if d else None
    tl.append(dict(annee=a, pib_reel_indice_1974_100=idx[a], ecart_tendance_1997_2007_pct=ec, ecart_tendance_1990_2007_pct=ec2,
                   dette_pct=d, dette_si_PIB_sur_tendance_1997_2007_denominateur_seul=d_cf))
    log(f"{a}: PIB reel a {ec:.1f} % de la tendance 1997-2007 ({ec2:.1f} % de la tendance 1990-2007) ; dette {d} % ; "
        f"denominateur seul -> {d_cf if d_cf is None else round(d_cf,1)} %")
with open(os.path.join(SORTIE, "a17_tendance_pib.csv"), "w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=list(tl[0].keys()), delimiter=";")
    w.writeheader()
    for l in tl:
        w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})

# 2 bis. manque de PIB reel 2025 par rapport a la tendance 2013-2019 prolongee (perte de niveau post-2019),
# et traduction en solde a la semi-elasticite de 0,57 (RESF 2027) : ORDRE DE GRANDEUR de ce qui, dans le
# deficit "structurel", correspond a une perte de niveau dont la permanence n'est pas identifiee.
xs3 = list(range(2013, 2020)); ys3 = [math.log(idx[a]) for a in xs3]
xb3 = sum(xs3) / len(xs3); yb3 = sum(ys3) / len(ys3)
b3 = sum((x - xb3) * (y - yb3) for x, y in zip(xs3, ys3)) / sum((x - xb3) ** 2 for x in xs3)
c3 = yb3 - b3 * xb3
log(f"Tendance du PIB reel 2013-2019 : {100*(math.exp(b3)-1):.2f} % par an")
for a in (2019, 2022, 2025):
    ec3 = 100 * (idx[a] / math.exp(c3 + b3 * a) - 1)
    log(f"{a}: PIB reel a {ec3:.2f} % de la tendance 2013-2019 ; x 0,57 = {0.57*ec3:.2f} pt de PIB de solde")
cum = 100 * (idx[2025] / idx[2019] - 1)
log(f"Croissance reelle cumulee 2019-2025 : {cum:.2f} % ({100*((idx[2025]/idx[2019])**(1/6)-1):.2f} % par an)")

# ------------------------------------------------------------------ 3. recettes et depenses 2017 / 2019 / 2025
rec = []
for a in (2006, 2012, 2017, 2019, 2025):
    rec.append(f"{a}: recettes {T[a]['recettes_pct']:.2f} % ; depenses {T[a]['depenses_pct']:.2f} % ; solde {T[a]['solde_pct']:.2f} % ; "
               f"solde primaire {T[a]['solde_primaire_pct']:.2f} % ; interets {T[a]['interets_pct']:.2f} %")
for r in rec:
    log(r)
with open(os.path.join(SORTIE, "a17_recettes_2017_2025.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(rec))

with open(os.path.join(SORTIE, "a17_sortie_historique.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
