"""Extrait le texte page par page d'un PDF vers un .txt (UTF-8) dans donnees/S14/textes.
Usage : python -I extraire_texte.py <chemin_pdf> [<chemin_pdf> ...]"""
import sys, os, pymupdf

OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\textes"
os.makedirs(OUT, exist_ok=True)
for chemin in sys.argv[1:]:
    d = pymupdf.open(chemin)
    nom = os.path.splitext(os.path.basename(chemin))[0] + ".txt"
    with open(os.path.join(OUT, nom), "w", encoding="utf-8") as f:
        for i, p in enumerate(d):
            f.write(f"\n=== page {i+1} ===\n")
            f.write(p.get_text())
    print(nom, d.page_count, "pages")
