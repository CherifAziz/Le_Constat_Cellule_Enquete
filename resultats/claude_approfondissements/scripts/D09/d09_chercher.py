# -*- coding: utf-8 -*-
"""D09 - recherche d'un motif dans le texte d'un PDF, page par page (pymupdf), avec contexte.

Usage : python d09_chercher.py <pdf> <motif regex> [largeur]
Affiche le numéro de page du PDF (1 = première page du fichier) et le contexte.
Sert seulement à localiser les pages ; les chiffres porteurs sont relus sur image (d09_images.py).
"""
import re
import sys

import fitz

pdf, motif = sys.argv[1], sys.argv[2]
larg = int(sys.argv[3]) if len(sys.argv) > 3 else 250
doc = fitz.open(pdf)
rx = re.compile(motif, re.I)
for i, page in enumerate(doc, 1):
    t = " ".join(page.get_text().split())
    for m in rx.finditer(t):
        a, b = max(0, m.start() - larg), min(len(t), m.end() + larg)
        print(f"--- p.{i} : ...{t[a:b]}...")
