"""A01 - Décomposition comptable annuelle de la variation du ratio dette/PIB (S13), 1979-2025.
Identité exacte (convention : B9 < 0 = besoin de financement) :
  D_t = D_{t-1} - B9_t + AFS_t        (AFS = ajustement stocks-flux, résidu)
  d_t - d_{t-1} = -sp_t + [(i_t - g_t)/(1+g_t)] * d_{t-1} + afs_t
  avec sp_t = (B9_t + I_t)/Y_t (solde primaire, I = intérêts versés D41 y.c. correction Sifim),
       i_t = I_t / D_{t-1} (taux apparent), g_t = Y_t/Y_{t-1} - 1 (croissance nominale), afs_t = AFS_t / Y_t.
Variante « intérêts nets » : I remplacé par D41 versés - D41 reçus (le résidu AFS est inchangé car il est
  défini sur la dette brute et B9 ; seule la répartition sp / effet boule de neige change).
Entrée : resultats/donnees/A01/A01_table_passage_1974_2025.csv (script 03).
Sortie : resultats/donnees/A01/A01_dynamique_dette_1979_2025.csv et A01_dynamique_dette_periodes.csv
Limite : pas de séparation croissance réelle / inflation (déflateur du PIB non présent dans la base commune).
Relançable : python -I 05_dynamique_dette.py
"""
import os, csv

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
A01 = os.path.join(RACINE, "resultats", "donnees", "A01")
T = {}
with open(os.path.join(A01, "A01_table_passage_1974_2025.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter=";"):
        if r["secteur"] == "S13":
            T[int(r["annee"])] = r

def fl(x):
    return float(x) if x not in ("", None) else None

out = []
for a in range(1979, 2026):
    p, c = T[a - 1], T[a]
    D0, D1 = fl(p["dette_maastricht_mdeur"]), fl(c["dette_maastricht_mdeur"])
    Y0, Y1 = fl(p["pib_mdeur"]), fl(c["pib_mdeur"])
    B9, I, Ir = fl(c["solde_b9_mdeur"]), fl(c["interets_verses_d41_mdeur"]), fl(c["interets_recus_d41_mdeur"])
    d0, d1 = D0 / Y0, D1 / Y1
    g = Y1 / Y0 - 1
    i = I / D0
    sp = (B9 + I) / Y1
    snow = (i - g) / (1 + g) * d0
    afs_md = (D1 - D0) + B9
    afs = afs_md / Y1
    chk = d1 - d0 - (-sp + snow + afs)
    # variante intérêts nets
    i_net = (I - Ir) / D0
    sp_net = (B9 + I - Ir) / Y1
    snow_net = (i_net - g) / (1 + g) * d0
    # séparation de l'effet boule de neige : intérêt et croissance
    eff_int = i / (1 + g) * d0
    eff_g = -g / (1 + g) * d0
    out.append([a, round(d0 * 100, 3), round(d1 * 100, 3), round((d1 - d0) * 100, 3),
                round(-sp * 100, 3), round(snow * 100, 3), round(eff_int * 100, 3), round(eff_g * 100, 3), round(afs * 100, 3),
                round(i * 100, 3), round(g * 100, 3), round(afs_md, 3), round(-sp_net * 100, 3), round(snow_net * 100, 3), f"{chk:.1e}"])

with open(os.path.join(A01, "A01_dynamique_dette_1979_2025.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "dette_pib_debut_pct", "dette_pib_fin_pct", "variation_ratio_pts",
                "contrib_deficit_primaire_pts", "contrib_boule_de_neige_pts", "dont_interets_pts", "dont_croissance_nominale_pts",
                "contrib_ajust_stocks_flux_pts", "taux_apparent_pct", "croissance_nominale_pct", "ajust_stocks_flux_mdeur",
                "variante_net_deficit_primaire_pts", "variante_net_boule_de_neige_pts", "residu_identite"])
    w.writerows(out)

# périodes : cumul des contributions entre années charnières
PER = [(1979, 1990), (1991, 1997), (1998, 2001), (2002, 2007), (2008, 2012), (2013, 2019), (2020, 2020), (2021, 2023), (2024, 2025), (1979, 2025)]
idx = {r[0]: r for r in out}
with open(os.path.join(A01, "A01_dynamique_dette_periodes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["periode", "ratio_debut", "ratio_fin", "variation", "deficit_primaire", "boule_de_neige", "dont_interets", "dont_croissance", "ajust_stocks_flux"])
    for a, b in PER:
        rs = [idx[x] for x in range(a, b + 1)]
        w.writerow([f"{a}-{b}", rs[0][1], rs[-1][2], round(sum(r[3] for r in rs), 2), round(sum(r[4] for r in rs), 2),
                    round(sum(r[5] for r in rs), 2), round(sum(r[6] for r in rs), 2), round(sum(r[7] for r in rs), 2), round(sum(r[8] for r in rs), 2)])
# années de baisse du ratio
print("années de baisse du ratio :", [r[0] for r in out if r[3] < 0])
print("max |résidu identité| :", max(abs(float(r[-1])) for r in out))
