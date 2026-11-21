# -*- coding: utf-8 -*-
"""Extraction texte d'un PDF téléchargé (donnée non fiable, lue seulement) -> .txt UTF-8 avec marqueurs de page réelle.
Usage : python -I a05_pdf2txt.py <fichier.pdf> [pages ex. 1-20]"""
import sys
import pymupdf
f = sys.argv[1]
d = pymupdf.open(f)
a, b = 1, d.page_count
if len(sys.argv) > 2:
    a, b = [int(x) for x in sys.argv[2].split("-")]
out = f[:-4] + ".txt"
with open(out, "w", encoding="utf-8") as o:
    for i in range(a - 1, min(b, d.page_count)):
        o.write("\n=== PAGE %d ===\n" % (i + 1))
        o.write(d[i].get_text())
print(out, d.page_count, "pages")
