"""C-S14-002 — Baisse des impôts de production 2021 (CET) : part approchée du gain par décile de taille.
LECTURE DE GRAPHIQUE (pas de données publiées en tableau) : IPP, rapport n° 60, oct. 2025, figure 1.12 (a), p. 44
(image : donnees/S14/images/FS_ImpotsProductions-9_p44.png). Points rouges = gain moyen de CET en % de la VA,
par décile de valeur ajoutée formé selon le nombre de postes (chaque décile = 10 % de la VA de l'échantillon).
Valeurs lues à l'œil par l'agent S14 ; précision estimée ±0,03 point par lecture.
Hypothèse explicite : la moyenne (non pondérée) des ratios gain/VA approxime le ratio agrégé du décile.
Comme chaque décile pèse 10 % de la VA, part du décile ≈ moyenne_d / Σ moyennes.
Usage : python -I ip_lecture_graphique_taille.py"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

lu = [0.16, 0.29, 0.55, 0.72, 0.82, 0.85, 0.90, 0.93, 0.92, 0.83]   # % de VA, lecture de graphique
unites = [211000, 102000, 43000, 21000, 9000, 4200, 2000, 700, 230, 35]  # note de la figure
postes_median = [6, 18, 40, 83, 183, 376, 740, 1879, 5089, 29009]       # étiquettes de la figure
E = 0.03

def part(idx, v):
    return sum(v[i] for i in idx) / sum(v)

groupes = {"décile 1-2 (≈313 000 unités, médiane ≤18 postes)": [0, 1],
           "déciles 1-4 (≈377 000 unités, médiane ≤83 postes)": [0, 1, 2, 3],
           "déciles 7-10 (≈2 965 unités, médiane ≥740 postes)": [6, 7, 8, 9],
           "décile 10 (≈35 unités, médiane ≈29 000 postes)": [9]}
for g, idx in groupes.items():
    bas = [v - E if i in idx else v + E for i, v in enumerate(lu)]
    haut = [v + E if i in idx else v - E for i, v in enumerate(lu)]
    print(f"{g}: {100*part(idx, lu):.1f} % (fourchette de lecture {100*part(idx, bas):.1f}-{100*part(idx, haut):.1f} %)")
print("somme des moyennes lues :", round(sum(lu), 2), "; gain moyen pondéré par la VA ≈", round(sum(lu) / 10, 2), "% de la VA")
# Variante : le texte du rapport donne 0,12 % (et non ≈0,16) pour le décile 1
lu2 = [0.12] + lu[1:]
print("variante décile 1 = 0,12 (texte) : déciles 1-4 =", round(100 * part([0, 1, 2, 3], lu2), 1), "% ; déciles 7-10 =", round(100 * part([6, 7, 8, 9], lu2), 1), "%")
