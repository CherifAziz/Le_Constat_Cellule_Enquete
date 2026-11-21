"""S04 - Conversion des effets publies par l'IPP (Perspectives budgetaires, juin 2025, chapitre 2, tableau 2.2, p.48 ;
TAXIPP 2.4.1) en PARTS DE L'EFFORT par groupe de niveau de vie. CALCUL DE L'AGENT, pas une microsimulation.

Principe (identite comptable) : si e_g est la variation du niveau de vie du groupe g en % de son niveau de vie (ratio des
moyennes, cf. note des figures IPP) et s_g la part du groupe dans la masse des niveaux de vie, alors
    e_moyen = somme_g s_g * e_g     et    part de l'effort du groupe g = s_g * e_g / e_moyen.
Les parts s_g (50 % les plus modestes, P50-P90, 10 % les plus aises) ne sont pas publiees dans la piece : on les ESTIME
par moindres carres sous contrainte somme = 1, a partir des dix lignes du tableau elles-memes (meme modele, meme annee).
Les residus mesurent l'incoherence due aux arrondis (deux decimales). Resultat a lire comme ordre de grandeur (niveau D).
Usage : python -I parts_ipp_tableau22.py"""
import numpy as np, csv, os

# (mesure, Md EUR, effet moyen, 50 % plus modestes, P50-P90, 10 % plus aises, 1 % plus aises) - recopie du tableau 2.2
T = [
    ("Hausse de 1 point CSG", 14.6, -1.06, -0.75, -1.15, -1.26, -1.31),
    ("Baisse de 10% seuils IR", 11.9, -0.85, -0.20, -1.02, -1.31, -1.02),
    ("Hausse de 1 point taux IR", 6.4, -0.45, -0.09, -0.50, -0.80, -0.89),
    ("Baisse de 10% credits et reductions d'impot", 1.1, -0.08, -0.03, -0.07, -0.16, -0.14),
    ("Suppression abattement retraite", 5.0, -0.32, -0.18, -0.40, -0.32, -0.15),
    ("Baisse du plafond abattement retraite", 2.0, -0.13, -0.02, -0.18, -0.17, -0.07),
    ("Suppression PFU", 9.0, -0.64, -0.08, -0.13, -2.26, -5.44),
    ("Annee blanche 2026", 5.7, -0.38, -0.48, -0.37, -0.29, -0.19),
    ("Gel bareme IR 2026", 1.8, -0.13, -0.03, -0.15, -0.19, -0.15),
    ("Gel retraites 2026", 2.6, -0.16, -0.21, -0.17, -0.10, -0.04),
    ("Gel prestations 2026", 1.3, -0.09, -0.24, -0.04, -0.01, 0.0),
]
E = np.array([[r[3], r[4], r[5]] for r in T])
m = np.array([r[2] for r in T])
# contrainte s1+s2+s3=1 : s3 = 1 - s1 - s2  -> m - e3 = s1 (e1-e3) + s2 (e2-e3)
A = np.column_stack([E[:, 0] - E[:, 2], E[:, 1] - E[:, 2]])
b = m - E[:, 2]
(s1, s2), *_ = np.linalg.lstsq(A, b, rcond=None)
s = np.array([s1, s2, 1 - s1 - s2])
print("Parts estimees de la masse des niveaux de vie (TAXIPP) : 50 %% modestes %.3f ; P50-P90 %.3f ; 10 %% aises %.3f" % tuple(s))
rows = [["mesure", "Md_EUR", "effet_moyen_publie", "effet_moyen_reconstitue", "part_effort_50pc_modestes",
         "part_effort_P50_P90", "part_effort_10pc_aises"]]
for r, e in zip(T, E):
    rec = float(s @ e)
    parts = s * e / rec if rec != 0 else [float("nan")] * 3
    rows.append([r[0], r[1], r[2], round(rec, 3)] + [round(float(p), 3) for p in parts])
    print("%-45s publie %.2f reconst. %.2f | parts : %.2f %.2f %.2f" % (r[0], r[2], rec, *parts))
# Recoupement : poids publies par l'Insee (part de la masse des niveaux de vie, 2023, publie le 09/07/2026,
# https://www.insee.fr/fr/statistiques/2409785) : D1..D5 = 3,4+5,2+6,3+7,3+8,2 = 30,4 ; D6..D9 = 9,2+10,3+11,7+14,0 = 45,2 ; D10 = 24,5
s_insee = np.array([0.304, 0.452, 0.245])
s_insee = s_insee / s_insee.sum()
print("Poids Insee 2023 :", np.round(s_insee, 3))
# Bande d'arrondi : chaque effet publie a +/- 0,005 point ; on recalcule les parts aux extremes (pire cas sur e_g)
rows.append([])
rows.append(["# variante poids Insee 2023 et bande d'arrondi +/-0,005", "", "", "", "parts (poids Insee)", "", "",
             "top10 min", "top10 max", "bas50 min", "bas50 max"])
for r, e in zip(T, E):
    for poids, lab in ((s_insee, "Insee"),):
        rec = float(poids @ e)
        parts = poids * e / rec
        # bande d'arrondi sur la part du top10 et du bas50
        ext = []
        for g in (2, 0):
            vals = []
            for d in (-0.005, 0.005):
                for d2 in (-0.005, 0.005):
                    e2 = e.copy()
                    e2[g] += d
                    autres = [i for i in range(3) if i != g]
                    e2[autres] += d2
                    vals.append(poids[g] * e2[g] / float(poids @ e2))
            ext += [min(vals), max(vals)]
        rows.append([r[0], r[1], r[2], round(rec, 3)] + [round(float(p), 3) for p in parts] + [round(x, 3) for x in ext])
        print("%-45s Insee : %.2f %.2f %.2f | top10 %.2f-%.2f | bas50 %.2f-%.2f" % (r[0], *parts, *ext))
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S04"
with open(os.path.join(R, "C-S04-001_parts_effort_ipp2025.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["# parts de masse estimees", *[round(float(x), 4) for x in s]])
    w.writerows(rows)
