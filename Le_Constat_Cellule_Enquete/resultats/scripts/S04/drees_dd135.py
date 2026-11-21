"""S04 - Lecture des donnees publiees Drees, Les Dossiers de la Drees n°135 (fevrier 2026), feuilles Graphique 4a, 4b et 5a.
Sortie : donnees/S04/drees_dd135_quintiles.csv + parts de l'effort par cinquieme (calcul de l'agent : cout moyen par menage
d'un cinquieme / somme des cinq couts moyens ; les cinquiemes de menages ont des effectifs egaux par construction).
Usage : python -I drees_dd135.py"""
import openpyxl, csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S04"
wb = openpyxl.load_workbook(os.path.join(R, "sources", "DD135_Mesures_deremboursements.xlsx"), data_only=True)
out = []
for nom in ["Graphique 4a", "Graphique 4b", "Graphique 5a"]:
    ws = wb[nom]
    rows = [r for r in ws.iter_rows(values_only=True)]
    entete = None
    for r in rows:
        v = [c for c in r if c is not None]
        if not v:
            continue
        if entete is None and len(v) >= 3 and isinstance(v[1], str):
            entete = v
            continue
        if entete is not None and len(v) == len(entete):
            out.append([nom] + v)
            print(nom, v)
    print(nom, "entete:", entete)
    out.append([nom, "ENTETE"] + list(entete or []))
with open(os.path.join(R, "drees_dd135_quintiles.csv"), "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter=";").writerows(out)

# C-S04-003 : part de l'effort par cinquieme = cout moyen du cinquieme / somme des cinq (effectifs egaux de menages)
g4a = [r for r in out if r[0] == "Graphique 4a" and r[1] != "ENTETE"]
entete = [r for r in out if r[0] == "Graphique 4a" and r[1] == "ENTETE"][0][3:]
res = [["mesure", "Q1", "Q2", "Q3", "Q4", "Q5", "Q1+Q2"]]
for j, nom in enumerate(entete):
    couts = [float(r[2 + j]) for r in g4a]
    tot = sum(couts)
    parts = [c / tot for c in couts]
    res.append([nom] + [round(p, 3) for p in parts] + [round(parts[0] + parts[1], 3)])
    print("C-S04-003", nom[:45], [round(p, 3) for p in parts])
with open(os.path.join(R, "C-S04-003_parts_effort_drees_dd135.csv"), "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter=";").writerows(res)
