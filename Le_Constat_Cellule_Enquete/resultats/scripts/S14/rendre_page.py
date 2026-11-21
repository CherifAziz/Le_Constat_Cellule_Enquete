"""Rend des pages d'un PDF en PNG (lecture de graphiques).
Usage : python -I rendre_page.py <chemin_pdf> <page1> [<page2> ...]  (pages numérotées à partir de 1)"""
import sys, os, pymupdf

OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\images"
os.makedirs(OUT, exist_ok=True)
chemin = sys.argv[1]
d = pymupdf.open(chemin)
base = os.path.splitext(os.path.basename(chemin))[0]
for n in sys.argv[2:]:
    p = d[int(n) - 1]
    pix = p.get_pixmap(dpi=150)
    sortie = os.path.join(OUT, f"{base}_p{n}.png")
    pix.save(sortie)
    print(sortie)
