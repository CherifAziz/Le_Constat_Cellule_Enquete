# -*- coding: utf-8 -*-
"""D09 - rendu en image (PNG, 150 dpi par défaut) des pages citées, pour lecture visuelle.

Usage : python d09_images.py <pdf> <page[,page...]> [dpi] [prefixe]
Pages = numéros de page du fichier PDF (1 = première page). Sortie : donnees/D09/images/<prefixe>_p<N>.png
"""
import sys
from pathlib import Path

import fitz

ICI = Path(__file__).resolve().parent
IMG = ICI.parent.parent / "donnees" / "D09" / "images"
IMG.mkdir(parents=True, exist_ok=True)

pdf = Path(sys.argv[1])
pages = [int(x) for x in sys.argv[2].split(",")]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 150
pref = sys.argv[4] if len(sys.argv) > 4 else pdf.stem
doc = fitz.open(pdf)
for p in pages:
    pix = doc[p - 1].get_pixmap(dpi=dpi)
    out = IMG / f"{pref}_p{p}.png"
    pix.save(out)
    print(out)
