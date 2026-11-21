# A18 - extraction texte des pièces (PDF : pymupdf, marqueurs [[p.N]] = page du PDF ; HTML : bs4)
# Usage : python -I a18_07_extrait_texte.py <dossier_sources> <dossier_textes>
import sys, os, fitz
from bs4 import BeautifulSoup
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
for fn in sorted(os.listdir(src)):
    p = os.path.join(src, fn); t = os.path.join(out, os.path.splitext(fn)[0] + ".txt")
    if os.path.exists(t) or os.path.isdir(p): continue
    head = open(p, "rb").read(5)
    if head.startswith(b"%PDF"):
        doc = fitz.open(p)
        txt = "".join(f"\n[[p.{i+1}]]\n" + pg.get_text() for i, pg in enumerate(doc))
    elif fn.endswith((".html", ".htm")):
        txt = BeautifulSoup(open(p, "rb").read(), "html.parser").get_text("\n")
    else:
        continue
    open(t, "w", encoding="utf-8").write(txt)
    print(fn, len(txt))
