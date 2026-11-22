# -*- coding: utf-8 -*-
"""D08, test 3.6 : que changerait réellement, dans les comptes de 2025, davantage d'heures
travaillées ou davantage de productivité ?

GRILLE D'HYPOTHÈSES EXPLICITES, PAS UNE ESTIMATION. Aucune de ces cases n'est une prévision
ni le rendement d'une politique. Le but est de montrer de quels paramètres le résultat dépend.

Comptes 2025 (Insee, base 2020) : PIB Y, recettes R, dépenses D.
Scénario « heures » : +h % d'heures travaillées.
    PIB : Y' = Y (1 + rho*h), rho = production d'une heure ajoutée / production moyenne
          (rho = 0,46 : rapport implicite de la note du Trésor de 2024 citée par A06,
           +7 % d'heures pour +3,2 % de PIB ; 0,7 ; 1,0).
    Recettes : R' = R + tau * (Y' - Y), tau = prélèvement sur le revenu ajouté
          (0,35 : emplois peu qualifiés avec allègements ; 0,459 : taux moyen 2025).
    Dépenses : D' = D - eco, eco = prestations économisées, en part du PIB ajouté (0 ; 0,10 ; 0,20).
Scénario « productivité » : PIB par heure plus haut de p %.
    Y' = Y (1+p) ; R' = R (1+p) (élasticité unitaire) ; D' = D (1 + phi*p),
    phi = part de la dépense qui suit les salaires et les prix relatifs à long terme
          (1,0 : tout suit, le ratio ne bouge pas ; 0,8 ; 0,5 : borne basse de court terme,
           pensions indexées sur les prix et salaires publics gelés).
Sorties : ../../donnees/D08/D08_grille_heures.csv, D08_grille_productivite.csv, D08_heures_france_mediane.csv
"""
import csv
import os
import statistics
import sys
import warnings

import openpyxl

warnings.filterwarnings("ignore")
def _racine_depot(depart):
    """Remonte depuis `depart` jusqu'au dossier qui contient la première enquête (indépendant de l'emplacement)."""
    p = os.path.abspath(depart)
    while True:
        if os.path.isdir(os.path.join(p, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "commun")):
            return p
        q = os.path.dirname(p)
        if q == p:
            raise SystemExit("racine du dépôt introuvable depuis " + depart)
        p = q


ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(ICI, "..", "..", "donnees", "D08"))
D06 = os.path.normpath(os.path.join(ICI, "..", "..", "donnees", "D06"))
RACINE = _racine_depot(ICI)
BASE = os.path.join(RACINE, "Le_Constat_Cellule_Enquete", "resultats", "donnees")

wb = openpyxl.load_workbook(os.path.join(BASE, "commun", "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
L = list(wb.worksheets[0].iter_rows(values_only=True))


def val(debut, annee=2025):
    for r in L:
        if r and len(r) > 1 and r[1] is not None and str(r[1]).strip().startswith(debut):
            return dict(zip([str(a).strip() if a is not None else "" for a in L[2]], r))[str(annee)]
    raise SystemExit(debut)


R, D = val("Total des recettes"), val("Total des dépenses")
Y = None
for r in csv.DictReader(open(os.path.join(BASE, "A04", "a04_po_recettes_1959_2025.csv"), encoding="utf-8-sig"), delimiter=";"):
    if r["annee"] == "2025":
        Y = float(r["PIB_implicite_Md_EUR"])
solde0 = 100 * (R - D) / Y

# --- 1. Heures par habitant de 15 à 64 ans : France et médiane des sept autres pays (séries de D06)
h = {}
for r in csv.DictReader(open(os.path.join(D06, "D06_series_comparees.csv"), encoding="utf-8-sig"), delimiter=";"):
    if r["heures_par_15_64"].strip():
        h.setdefault(int(r["annee"]), {})[r["pays"]] = float(r["heures_par_15_64"].replace(",", "."))
pays_fr = [p for p in next(iter(h.values())) if p.upper().startswith("FR")][0]
tab_h = []
for a in sorted(h):
    autres = [v for p, v in h[a].items() if p != pays_fr]
    if pays_fr in h[a] and len(autres) >= 6:
        med = statistics.median(autres)
        tab_h.append({"annee": a, "heures_France": round(h[a][pays_fr], 1), "mediane_autres": round(med, 1),
                      "nb_autres": len(autres), "ecart_France_pct": round(100 * (h[a][pays_fr] / med - 1), 1)})
with open(os.path.join(OUT, "D08_heures_france_mediane.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(tab_h[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(tab_h)
ecart_dernier = -tab_h[-1]["ecart_France_pct"]

# --- 2. Grille « heures »
g1 = []
for hh in (1.0, 5.0, round(ecart_dernier, 1)):
    for rho in (0.46, 0.7, 1.0):
        for tau in (0.35, R / Y * 0 + 0.459):
            for eco in (0.0, 0.10, 0.20):
                dY = Y * rho * hh / 100
                s1 = 100 * ((R + tau * dY) - (D - eco * dY)) / (Y + dY)
                g1.append({"heures_en_plus_pct": hh, "rho": rho, "tau": tau, "eco_prestations": eco,
                           "PIB_en_plus_pct": round(rho * hh, 2), "solde_2025_observe": round(solde0, 2),
                           "solde_sous_hypotheses": round(s1, 2), "amelioration_pts_PIB": round(s1 - solde0, 2)})
with open(os.path.join(OUT, "D08_grille_heures.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(g1[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(g1)

# --- 3. Grille « productivité »
g2 = []
for p in (1.0, 5.0, 10.0):
    for phi in (1.0, 0.8, 0.5):
        s1 = 100 * (R * (1 + p / 100) - D * (1 + phi * p / 100)) / (Y * (1 + p / 100))
        g2.append({"productivite_en_plus_pct": p, "phi_part_de_la_depense_qui_suit": phi,
                   "solde_2025_observe": round(solde0, 2), "solde_sous_hypotheses": round(s1, 2),
                   "amelioration_pts_PIB": round(s1 - solde0, 2)})
with open(os.path.join(OUT, "D08_grille_productivite.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(g2[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(g2)

sys.stdout.reconfigure(encoding="utf-8")
print("Y, R, D, solde 2025 :", round(Y, 1), round(R, 1), round(D, 1), round(solde0, 2))
for t in tab_h:
    if t["annee"] in (1974, 1990, 1999, 2007, 2019, tab_h[-1]["annee"]):
        print(t)
print("--- heures : amelioration du solde (min, max) par ampleur")
for hh in sorted(set(x["heures_en_plus_pct"] for x in g1)):
    v = [x["amelioration_pts_PIB"] for x in g1 if x["heures_en_plus_pct"] == hh]
    print(hh, min(v), max(v))
print("--- productivité")
for x in g2:
    print(x["productivite_en_plus_pct"], x["phi_part_de_la_depense_qui_suit"], x["amelioration_pts_PIB"])
