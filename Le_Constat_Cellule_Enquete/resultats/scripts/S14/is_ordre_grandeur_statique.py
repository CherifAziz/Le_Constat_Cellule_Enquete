"""C-S14-003 — IS : ordre de grandeur STATIQUE du gain mécanique de la baisse du taux normal, à base 2022.
Source : Insee Analyses n° 112 (sept. 2025), fichier IA112.xlsx, feuille « Figure 1 » (bénéfice imposable par taux, Md€).
Gain = somme sur les tranches (33,33 % - taux appliqué en 2022) x bénéfice imposé à ce taux en 2022.
Ignore : contribution sociale de 3,3 %, plus-values et brevets, crédits d'impôt, réaction de la base. Ce n'est PAS
le coût budgétaire officiel ; c'est un ordre de grandeur pour comparer aux autres baisses.
Contrôle : les recettes d'IS (Insee, Les entreprises en France 2023, fiche 3.7, fig. 1) passent de 54,4 Md€ (2018) à 75,0 Md€ (2022).
Usage : python -I is_ordre_grandeur_statique.py"""
import openpyxl, sys
sys.stdout.reconfigure(encoding="utf-8")
SRC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\sources\IA112.xlsx"
ws = openpyxl.load_workbook(SRC, data_only=True)["Figure 1"]
taux = {"25 %": 25.0, "26,5 %": 26.5, "27,5 %": 27.5, "28 %": 28.0, "31 %": 31.0}
gain = 0.0
for r in ws.iter_rows(values_only=True):
    if r[0] and str(r[0]).startswith("Bénéfice imposable à"):
        for k, t in taux.items():
            if str(r[0]).strip().endswith(k):
                b22 = r[7]
                g = b22 * (100 / 3 - t) / 100
                gain += g
                print(f"tranche {k}: bénéfice 2022 = {b22} Md€ ; gain statique = {g:.2f} Md€")
print(f"Gain statique total à base 2022 ≈ {gain:.1f} Md€")
