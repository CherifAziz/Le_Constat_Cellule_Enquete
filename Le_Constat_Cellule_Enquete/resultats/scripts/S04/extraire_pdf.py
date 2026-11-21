"""S04 - extraction texte des PDF de donnees/S04/sources vers donnees/S04/textes (une page = un bloc '=== p.N ===').
Usage : python -I extraire_pdf.py <fichier.pdf> [<fichier.pdf> ...]"""
import sys, os
import fitz  # pymupdf

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S04"
SORTIE = os.path.join(RACINE, "textes")
os.makedirs(SORTIE, exist_ok=True)
for chemin in sys.argv[1:]:
    doc = fitz.open(chemin)
    nom = os.path.splitext(os.path.basename(chemin))[0] + ".txt"
    with open(os.path.join(SORTIE, nom), "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, 1):
            f.write(f"\n=== p.{i} ===\n")
            f.write(page.get_text())
    print(nom, len(doc), "pages")
