"""Extrait le texte d'un PDF de donnees/S05/sources vers donnees/S05/extraits/<nom>.txt, page par page.
Usage : python -I extraire.py <nom_pdf>  -> affiche le nombre de pages et la 1re page.
"""
import sys, os, fitz

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S05"
nom = sys.argv[1]
doc = fitz.open(os.path.join(RACINE, "sources", nom))
sortie = os.path.join(RACINE, "extraits", os.path.splitext(nom)[0] + ".txt")
with open(sortie, "w", encoding="utf-8") as f:
    for i, p in enumerate(doc, 1):
        f.write(f"\n===== PAGE {i} =====\n")
        f.write(p.get_text())
print(nom, "pages:", len(doc), "->", sortie, os.path.getsize(sortie), "octets")
