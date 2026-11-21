# -*- coding: utf-8 -*-
"""Extrait le texte d'un PDF (pages reelles) vers un .txt UTF-8, avec marqueurs de page.
Usage : python -I pdf2txt.py fichier.pdf [p_debut p_fin]   (pages numerotees a partir de 1)
"""
import sys, pymupdf
src = sys.argv[1]
d = pymupdf.open(src)
a = int(sys.argv[2]) if len(sys.argv) > 2 else 1
b = int(sys.argv[3]) if len(sys.argv) > 3 else d.page_count
out = src.rsplit('.', 1)[0] + (f'_p{a}-{b}' if len(sys.argv) > 2 else '') + '.txt'
with open(out, 'w', encoding='utf-8') as f:
    for i in range(a - 1, min(b, d.page_count)):
        f.write(f'\n=== PAGE PDF {i+1} ===\n')
        f.write(d[i].get_text())
print(out, d.page_count)
