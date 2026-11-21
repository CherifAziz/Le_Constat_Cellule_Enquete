# -*- coding: utf-8 -*-
"""A18 partie 2/3 : recherche de motifs dans un PDF telecharge (lu avec pymupdf, sans execution).
Usage : python -I a18_p2_cherche_pdf.py <fichier.pdf> <sortie.txt> motif1 motif2 ...
Ecrit, pour chaque occurrence, la page reelle (1-based) et 300 caracteres de contexte."""
import sys, re
import pymupdf

pdf, sortie, motifs = sys.argv[1], sys.argv[2], sys.argv[3:]
doc = pymupdf.open(pdf)
out = []
for i, page in enumerate(doc):
    t = page.get_text()
    t1 = re.sub(r"\s+", " ", t)
    for m in motifs:
        for mm in re.finditer(m, t1):
            a, b = max(0, mm.start() - 300), min(len(t1), mm.end() + 300)
            out.append(f"[p.{i+1}] motif={m!r} :: {t1[a:b]}")
with open(sortie, "w", encoding="utf-8") as h:
    h.write(f"{pdf}\n{len(doc)} pages\n\n" + "\n\n".join(out))
print(len(out), "occurrences ->", sortie)
