# -*- coding: utf-8 -*-
"""
Infrastructure commune (orchestrateur) : met a plat les trois fichiers Insee "series longues"
(telecharges par telecharger_series_communes.py) en CSV longs, sans aucun retraitement :
  - base_insee_dep_rec_pctPIB.csv      : toutes les lignes du fichier 2381414 (en % du PIB)
  - base_insee_solde_sous_secteurs.csv : fichier 2381402, toutes feuilles
  - base_insee_dette_sous_secteurs.csv : fichier 2830192, toutes feuilles
Chaque ligne : fichier, feuille, unite (libelle de la feuille), serie (libelle Insee), annee, valeur.
Les libelles sont ceux de l'Insee ; 'nd' et cellules vides sont ignores (indisponible).
"""
import csv, os, re, warnings
import openpyxl
warnings.filterwarnings("ignore")
D = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "donnees", "commun"))

def annee(x):
    if isinstance(x, (int, float)) and 1900 < x < 2100:
        return int(x)
    if isinstance(x, str):
        m = re.match(r"^\s*((?:19|20)\d\d)", x)
        if m:
            return int(m.group(1))
    return None

def aplatir(fichier, sortie):
    wb = openpyxl.load_workbook(os.path.join(D, fichier), data_only=True)
    lignes = []
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        unite, annees = "", None
        for r in rows:
            cells = list(r)
            if not any(c is not None for c in cells):
                continue
            premier = cells[0]
            ans = [annee(c) for c in cells[1:]]
            if sum(a is not None for a in ans) >= 5:
                annees = ans
                continue
            if isinstance(premier, str) and annees is None and premier.strip().lower().startswith("en "):
                unite = premier.strip()
                continue
            if annees is not None and isinstance(premier, str):
                vals = cells[1:]
                if sum(isinstance(v, (int, float)) for v in vals) >= 3:
                    for a, v in zip(annees, vals):
                        if a is not None and isinstance(v, (int, float)):
                            lignes.append([fichier, ws.title, unite, premier.strip(), a, v])
    with open(os.path.join(D, sortie), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["fichier", "feuille", "unite", "serie", "annee", "valeur"])
        w.writerows(lignes)
    return lignes

for fichier, sortie in [("insee_dep_rec_serie_longue.xlsx", "base_insee_dep_rec_pctPIB.csv"),
                        ("insee_solde_par_sous_secteur.xlsx", "base_insee_solde_sous_secteurs.csv"),
                        ("insee_dette_par_sous_secteur.xlsx", "base_insee_dette_sous_secteurs.csv")]:
    L = aplatir(fichier, sortie)
    series = sorted({(l[1], l[2], l[3]) for l in L})
    print(f"== {sortie}: {len(L)} observations, {len(series)} series")
    for s in series:
        ans = [l[4] for l in L if (l[1], l[2], l[3]) == s]
        print("   ", s, min(ans), "-", max(ans))
