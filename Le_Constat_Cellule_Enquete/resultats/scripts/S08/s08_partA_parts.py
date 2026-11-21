# -*- coding: utf-8 -*-
"""S08 - Partie A : parts des gains par groupe de niveau de vie à partir de montants PUBLIÉS.

C-S08-010 : OFCE, Policy brief n° 104 (17 mars 2022), graphique 3 : gain moyen en euros par UC
  et par vingtième de niveau de vie (étiquettes texte du graphique, lues dans le PDF).
  Hypothèse de calcul (agent) : vingtièmes de même effectif et nombre d'UC voisin entre
  vingtièmes ; part du groupe g = somme des gains moyens des vingtièmes de g / somme des 20.
  Contrôle : la part du dernier vingtième doit retrouver les 17 % publiés en texte par l'OFCE.
C-S08-011 : décomposition indicative ménages / entreprises des baisses (montants publiés,
  périmètres hétérogènes), voir S08.md §5.
Usage : python -I s08_partA_parts.py
"""
import os, sys, csv
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S08"

# Étiquettes du graphique 3 (v1..v20), dans l'ordre d'extraction du texte du PDF, en € par UC et par an
ofce = [65, 230, 295, 255, 255, 300, 410, 495, 485, 515, 590, 625, 665, 705, 680, 615, 480, 390, 360, 1720]
assert len(ofce) == 20
tot = sum(ofce)
p_top5 = ofce[19] / tot
p_top10 = sum(ofce[18:]) / tot
p_bot50 = sum(ofce[:10]) / tot
p_mid = sum(ofce[10:18]) / tot
lines = [
    f"C-S08-010 OFCE PB104 graphique 3 : somme des gains moyens par vingtième = {tot} €/UC",
    f"  dernier vingtième (5 % les plus aisés) : {p_top5:.1%}  [contrôle : OFCE publie 17 %]",
    f"  10 % les plus aisés (v19+v20) : {p_top10:.1%}",
    f"  50 % les plus modestes (v1..v10) : {p_bot50:.1%}",
    f"  v11..v18 (P50-P90) : {p_mid:.1%}",
]
# Application indicative au total simulé publié (22 Md€) - calcul de l'agent
for lab, p in (("top 5 %", p_top5), ("top 10 %", p_top10), ("50 % modestes", p_bot50)):
    lines.append(f"  {lab} : {p*22:.1f} Md€ sur 22 Md€ (calcul de l'agent)")

# C-S08-011 : ménages / entreprises (Md€, montants publiés, périmètres et années hétérogènes)
men = {
 "TH résidences principales (Cour janv. 2025, gain 2023 à législation 2017)": 19.0,
 "Contribution à l'audiovisuel public (Cour janv. 2025, perte État)": 3.8,
 "ISF->IFI (Insee ES 530-31, 2018, statique)": 3.44,
 "PFU volet IR (Insee ES 530-31, statique)": 1.76,
 # La hausse de CSG sur le patrimoine (-1,83, Insee) est déjà comprise dans les +21,6 de l'IPP : non comptée à part.
 "Baisse d'IR 2020 (OFCE PB104, texte)": 5.0,
 "Bascule cotisations-CSG nette, toutes CSG (IPP n°81 : -26,2 + 21,6, calcul de l'agent)": 4.6,
}
ent = {
 "CVAE (Cour janv. 2025, au moins)": 15.0,
 "Locaux industriels (Cour janv. 2025)": 4.3,
 "Taux normal d'IS 33,3 -> 25 % ([S] RESF PLF 2022 cité par Fipeco, consulté ; RESF non consulté)": 11.0,
}
th_top20 = 5.7 / 19.0
lines.append(f"C-S08-012 TH : tranche des 20 % de foyers au RFR le plus élevé 5,7 Md€ / 19 Md€ = {th_top20:.0%} (indicatif : RFR et non niveau de vie)")
m, e = sum(men.values()), sum(ent.values())
lines.append(f"C-S08-011 ménages {m:.1f} Md€ ; entreprises {e:.1f} Md€ ; part ménages {m/(m+e):.0%} (ordre de grandeur, périmètres hétérogènes)")
lines.append(f"  variante sans IS ([S]) : part ménages {m/(m+e-11):.0%}")
lines.append(f"  fiscalité locale seule (Cour) : ménages 19 / entreprises >= 19,3 -> part ménages <= {19/(19+19.3):.0%}")
txt = "\n".join(lines)
print(txt)
open(os.path.join(OUT, "S08_A_calculs.txt"), "w", encoding="utf-8").write(txt + "\n")
with open(os.path.join(OUT, "S08_A_ofce_vingtiemes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["vingtieme", "gain_eur_par_UC", "part_calc_agent"])
    for i, v in enumerate(ofce): w.writerow([f"v{i+1}", v, f"{v/tot:.4f}"])
