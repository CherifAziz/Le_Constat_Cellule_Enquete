"""Extraction du texte des PDF (pymupdf), avec marqueur de page '=== PAGE PDF N ==='.
Usage : python -I d04_extraire.py dossier_ou_fichier [...]
Ecrit un .txt a cote de chaque PDF (ne reecrit pas un .txt existant)."""
import sys, os, glob
import fitz  # pymupdf

def extraire(pdf):
    txt = pdf[:-4] + '.txt'
    if os.path.exists(txt):
        return txt, 'deja'
    doc = fitz.open(pdf)
    with open(txt, 'w', encoding='utf-8') as f:
        for i, page in enumerate(doc, start=1):
            f.write(f'\n=== PAGE PDF {i} ===\n')
            f.write(page.get_text())
    return txt, f'{len(doc)} pages'

for a in sys.argv[1:]:
    fichiers = sorted(glob.glob(os.path.join(a, '*.pdf'))) if os.path.isdir(a) else [a]
    for p in fichiers:
        t, info = extraire(p)
        print(os.path.basename(p), info, os.path.getsize(t))
