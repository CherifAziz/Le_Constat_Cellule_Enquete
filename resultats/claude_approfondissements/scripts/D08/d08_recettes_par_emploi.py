# -*- coding: utf-8 -*-
"""D08, test 3.5 : les cotisations sociales rapportées aux salaires et à l'emploi, 2000-2025.

Question (hypothèse H-A06-015 de la première enquête) : l'emploi ajouté depuis 2019
a-t-il rapporté moins de cotisations par euro de salaire et par emploi ?

Entrées (comptes nationaux annuels de l'Insee, base 2020) :
  - T_1107 : partage de la valeur ajoutée (D1, D11, D12), économie totale
  - T_1105 : PIB à prix courants
  - T_1109 : emploi intérieur total en équivalent temps plein
  - t_3201 : dépenses et recettes des administrations publiques (D61, D612)
  - T_1101_1103 : PIB en volume (pour le prix du PIB)
Sorties : ../../donnees/D08/D08_cotisations_par_salaire.csv et D08_cotisations_decomposition.csv
Lancement : python d08_recettes_par_emploi.py
"""
import csv
import os
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
SRC = os.path.join(OUT, "sources")
RACINE = _racine_depot(ICI)  # dépôt principal
COMMUN = os.path.join(RACINE, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "commun")
CODEX = os.path.join(RACINE, "resultats", "codex", "donnees")


def feuille(chemin, motif=None):
    wb = openpyxl.load_workbook(chemin, read_only=True, data_only=True)
    for ws in wb.worksheets:
        if ws.title.lower().startswith("m"):  # Métadonnées
            continue
        if motif is None or motif in ws.title:
            return list(ws.iter_rows(values_only=True))
    raise SystemExit("feuille introuvable : " + chemin)


def serie_par_code(lignes, code, occurrence=0):
    """Tables T_xxxx : colonne 0 = code, colonne 1 = libellé, années en ligne 3."""
    annees = None
    for r in lignes[:6]:
        vals = [x for x in r if x is not None]
        if vals and all(str(v).strip().isdigit() for v in vals[:3]):
            annees = r
            break
    vu = 0
    for r in lignes:
        if r and r[0] is not None and str(r[0]).strip() == code:
            if vu == occurrence:
                return {int(str(a).strip()): v for a, v in zip(annees, r)
                        if a is not None and str(a).strip().isdigit() and isinstance(v, (int, float))}
            vu += 1
    raise SystemExit("code introuvable : " + code)


def serie_par_libelle(lignes, debut, occurrence=0):
    """Table t_3201 de la base commune : colonne 1 = libellé, années en ligne 2."""
    annees = lignes[2]
    vu = 0
    for r in lignes:
        if r and len(r) > 1 and r[1] is not None and str(r[1]).strip().startswith(debut):
            if vu == occurrence:
                return {int(str(a).strip()): v for a, v in zip(annees, r)
                        if a is not None and str(a).strip().isdigit() and isinstance(v, (int, float))}
            vu += 1
    raise SystemExit("libellé introuvable : " + debut)


t1107 = feuille(os.path.join(SRC, "T_1107_fr.xlsx"), "niveau")
t1105 = feuille(os.path.join(SRC, "T_1105_fr.xlsx"), "niveau")
t1109 = feuille(os.path.join(CODEX, "T_1109_fr.xlsx"), "niveau")
t3201 = feuille(os.path.join(COMMUN, "insee_cn_t_3201.xlsx"))

D1 = serie_par_code(t1107, "D1")
D11 = serie_par_code(t1107, "D11")
D12 = serie_par_code(t1107, "D12")
PIB = serie_par_code(t1105, "B1GQ")
ETP = serie_par_code(t1109, "S1")
D61 = serie_par_libelle(t3201, "Cotisations sociales nettes (D61)")
D612 = serie_par_libelle(t3201, "dont (a) - Cotisations sociales imputées (D612)")
PO = serie_par_libelle(t3201, "Impôts et cotisations sociales")

annees = [a for a in range(1990, 2026) if all(a in s for s in (D1, D11, PIB, ETP, D61, D612, PO))]
lignes = []
for a in annees:
    eff = D61[a] - D612[a]  # cotisations effectives reçues par les administrations
    lignes.append({
        "annee": a,
        "PIB_MdEUR": round(PIB[a], 3),
        "salaires_bruts_D11_MdEUR": round(D11[a], 3),
        "cotisations_effectives_MdEUR": round(eff, 3),
        "cotisations_effectives_pct_PIB": round(100 * eff / PIB[a], 3),
        "salaires_bruts_pct_PIB": round(100 * D11[a] / PIB[a], 3),
        "taux_apparent_cotisations_sur_salaires_pct": round(100 * eff / D11[a], 3),
        "emploi_ETP_milliers": round(ETP[a], 1),
        "cotisations_par_ETP_EUR": round(1e6 * eff / ETP[a], 1),
        "salaire_brut_par_ETP_EUR": round(1e6 * D11[a] / ETP[a], 1),
        "PIB_par_ETP_EUR": round(1e6 * PIB[a] / ETP[a], 1),
        "impots_et_cotisations_pct_PIB": round(100 * PO[a] / PIB[a], 3),
    })

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "D08_cotisations_par_salaire.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(lignes)

par_annee = {l["annee"]: l for l in lignes}


def decomposition(a0, a1):
    """Variation de cotisations/PIB = effet taux apparent + effet part des salaires (moyenne des deux pondérations)."""
    x0, x1 = par_annee[a0], par_annee[a1]
    t0, t1 = x0["taux_apparent_cotisations_sur_salaires_pct"] / 100, x1["taux_apparent_cotisations_sur_salaires_pct"] / 100
    s0, s1 = x0["salaires_bruts_pct_PIB"], x1["salaires_bruts_pct_PIB"]
    effet_taux = (t1 - t0) * (s0 + s1) / 2
    effet_part = (s1 - s0) * (t0 + t1) / 2
    total = x1["cotisations_effectives_pct_PIB"] - x0["cotisations_effectives_pct_PIB"]
    manque = (t0 - t1) * D11[a1]  # cotisations en moins en a1 si le taux apparent de a0 s'était maintenu
    return {
        "debut": a0, "fin": a1,
        "variation_cotisations_pts_PIB": round(total, 3),
        "dont_effet_taux_apparent_pts": round(effet_taux, 3),
        "dont_effet_part_des_salaires_pts": round(effet_part, 3),
        "taux_apparent_debut_pct": round(100 * t0, 2), "taux_apparent_fin_pct": round(100 * t1, 2),
        "cotisations_en_moins_a_taux_apparent_constant_MdEUR": round(manque, 1),
        "idem_pts_PIB": round(100 * manque / PIB[a1], 2),
        "emploi_ETP_variation_pct": round(100 * (ETP[a1] / ETP[a0] - 1), 2),
        "salaire_brut_par_ETP_variation_nominale_pct": round(100 * (x1["salaire_brut_par_ETP_EUR"] / x0["salaire_brut_par_ETP_EUR"] - 1), 2),
        "PIB_nominal_par_ETP_variation_pct": round(100 * (x1["PIB_par_ETP_EUR"] / x0["PIB_par_ETP_EUR"] - 1), 2),
    }


fenetres = [(1993, 2000), (2000, 2007), (2007, 2012), (2012, 2017), (2017, 2019), (2019, 2025), (2019, 2023), (1993, 2025)]
dec = [decomposition(a, b) for a, b in fenetres if a in par_annee and b in par_annee]
with open(os.path.join(OUT, "D08_cotisations_decomposition.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(dec[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(dec)

sys.stdout.reconfigure(encoding="utf-8")
for l in lignes:
    if l["annee"] in (1993, 2000, 2007, 2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025):
        print(l["annee"], "cotis/PIB", l["cotisations_effectives_pct_PIB"], "| salaires/PIB", l["salaires_bruts_pct_PIB"],
              "| taux apparent", l["taux_apparent_cotisations_sur_salaires_pct"], "| PO/PIB", l["impots_et_cotisations_pct_PIB"])
for d in dec:
    print(d)
