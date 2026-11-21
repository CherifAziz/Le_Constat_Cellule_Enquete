"""C-S14-001 — Parts du gain de la suppression de la taxe d'habitation (2018-2023) par dixième de niveau de vie.
Source : Insee, France portrait social 2024, dossier 1, fichier FPORSOC24-D1.xlsx, feuille « Figure Encadré »
(effet moyen sur le niveau de vie, euros constants 2023, par dixième de personnes).
Les dixièmes comptent le même nombre de personnes : la part d'un dixième dans la masse des gains de niveau de vie
= effet moyen du dixième / somme des dix effets moyens. Les valeurs Insee sont arrondies à 10 euros : on calcule
des bornes en décalant chaque valeur de -5/+5 (borne défavorable / favorable au groupe considéré).
Lecture du fichier par openpyxl (aucune saisie manuelle).
Usage : python -I th_parts_par_dixieme.py"""
import openpyxl, csv, os

SRC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\sources\FPORSOC24-D1.xlsx"
OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\th_parts_par_dixieme.csv"

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = [w for w in wb if w.title.startswith("Figure Encadr")][0]
lignes = []
for r in ws.iter_rows(values_only=True):
    if r[0] and isinstance(r[1], (int, float)) and str(r[0]).strip() != "Ensemble":
        lignes.append((str(r[0]).replace("\n", " ").strip(), list(r[1:8])))
assert len(lignes) == 10, lignes
annees = ["2018", "2019", "2020", "2021", "2022", "2023", "ensemble"]
tot = [l[1][6] for l in lignes]          # effet cumulé 2018-2023 par dixième
S = sum(tot)

def part(groupe, vals):
    return sum(vals[i] for i in groupe) / sum(vals)

def bornes(groupe, vals):
    bas = [v - 5 if i in groupe else v + 5 for i, v in enumerate(vals)]
    haut = [v + 5 if i in groupe else v - 5 for i, v in enumerate(vals)]
    return part(groupe, bas), part(groupe, haut)

groupes = {"10 % les plus aisés (D10)": [9], "20 % les plus aisés (D9-D10)": [8, 9],
           "50 % les plus modestes (D1-D5)": [0, 1, 2, 3, 4], "30 % les plus aisés (D8-D10)": [7, 8, 9]}
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["dixieme"] + [f"effet_{a}_eur2023" for a in annees] + ["part_du_cumul_pct"])
    for nom, v in lignes:
        w.writerow([nom] + v + [round(100 * v[6] / S, 1)])
    w.writerow([])
    w.writerow(["groupe", "part_centrale_pct", "borne_basse_pct", "borne_haute_pct"])
    for g, idx in groupes.items():
        b, h = bornes(idx, tot)
        w.writerow([g, round(100 * part(idx, tot), 1), round(100 * b, 1), round(100 * h, 1)])
        print(f"{g}: {100*part(idx, tot):.1f} % (arrondis : {100*b:.1f}-{100*h:.1f} %)")
    # Phase 2021-2023 seule (20 % des foyers les plus aisés)
    p2 = [sum(l[1][3:6]) for l in lignes]
    w.writerow(["phase 2021-2023 : part D9-D10", round(100 * part([8, 9], p2), 1), "", ""])
    p1 = [sum(l[1][0:3]) for l in lignes]
    w.writerow(["phase 2018-2020 : part D1-D5", round(100 * part([0, 1, 2, 3, 4], p1), 1), "", ""])
    w.writerow(["rapport D10/D1 (cumul)", round(tot[9] / tot[0], 1), "", ""])
print("somme des effets moyens", S, "moyenne", S / 10)
print("phase 2021-2023 part D9-D10 :", round(100 * part([8, 9], p2), 1), "% ; phase 2018-2020 part D1-D5 :", round(100 * part([0,1,2,3,4], p1), 1), "%")
print("phase 2018-2020 part D9-D10 :", round(100 * part([8, 9], p1), 1), "% ; D10/D1 :", round(tot[9] / tot[0], 1))
