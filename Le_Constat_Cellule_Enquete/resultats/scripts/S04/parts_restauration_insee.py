"""S04 - Part de chaque quintile de niveau de vie dans la depense de « Restauration et hotels » (Insee, enquete Budget de
famille 2017, chiffre cle publie le 15/09/2020, fichier reve-conso-struct-dep-niv-vie.xlsx). CALCUL DE L'AGENT (niveau D).

La piece ne donne que la structure du budget de chaque quintile (s_qk, en %) et de l'ensemble (S_k). Identite :
S_k = somme_q w_q s_qk, ou w_q est la part du quintile q dans la depense totale. On estime w_q (somme = 1) par moindres
carres sur les 12 postes ; puis part du quintile q dans le poste k = w_q s_qk / S_k.
Usage : python -I parts_restauration_insee.py"""
import openpyxl, numpy as np, os, csv
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S04"
wb = openpyxl.load_workbook(os.path.join(R, "sources", "insee_reve-conso-struct-dep-niv-vie.xlsx"), data_only=True)
ws = wb.worksheets[0]
lignes = []
for r in ws.iter_rows(values_only=True):
    v = [c for c in r if c is not None]
    if len(v) == 25 and isinstance(v[0], str) and isinstance(v[1], (int, float)):
        lignes.append(v)
postes = [l[0] for l in lignes if not l[0].startswith("D")]  # exclut « Depense totale » (=100)
M = np.array([l[19:24] for l in lignes if not l[0].startswith("D")], dtype=float)  # 2017 : colonnes 19-23 = Q1..Q5
S = np.array([l[24] for l in lignes if not l[0].startswith("D")], dtype=float)    # 2017 : ensemble
# contrainte somme w = 1 : w5 = 1 - w1..w4
A = M[:, :4] - M[:, [4]]
b = S - M[:, 4]
w4, *_ = np.linalg.lstsq(A, b, rcond=None)
w = np.append(w4, 1 - w4.sum())
print("Parts estimees de la depense totale par quintile (2017) :", np.round(w, 3))
print("Residus max (points) :", np.round(np.max(np.abs(M @ w - S)), 3))
out = [["poste", "Q1", "Q2", "Q3", "Q4", "Q5"]]
for p, row, s in zip(postes, M, S):
    parts = w * row / s
    out.append([p] + [round(float(x), 3) for x in parts])
    if p.startswith("Restauration"):
        print("Restauration et hotels : part de la depense par quintile", np.round(parts, 3))
with open(os.path.join(R, "C-S04-002_parts_restauration_insee2017.csv"), "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter=";").writerows([["# parts depense totale estimees"] + [round(float(x), 4) for x in w]] + out)
