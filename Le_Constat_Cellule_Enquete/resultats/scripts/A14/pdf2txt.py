"""Extraction du texte d'un PDF avec numéros de page PDF (A14).
Usage : python -I pdf2txt.py <entree.pdf> <sortie.txt>
"""
import sys
import fitz  # pymupdf

src, dst = sys.argv[1], sys.argv[2]
doc = fitz.open(src)
with open(dst, "w", encoding="utf-8") as out:
    for i, page in enumerate(doc, start=1):
        out.write(f"\n=== PAGE PDF {i} ===\n")
        out.write(page.get_text())
print(f"{len(doc)} pages -> {dst}")
