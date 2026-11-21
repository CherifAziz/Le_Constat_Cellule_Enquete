"""S02 - reconstitue les lignes d'un tableau PDF (mots regroupes par ordonnee).
Usage : python -I s02_pdf_rows.py <pdf> <page1-based> [page2 ...] [--grep motif]
"""
import sys, re
import pymupdf

args = sys.argv[1:]
pat = None
if "--grep" in args:
    i = args.index("--grep"); pat = re.compile(args[i + 1], re.I); args = args[:i] + args[i + 2:]
pdf = args[0]
doc = pymupdf.open(pdf)
for pg in args[1:]:
    page = doc[int(pg) - 1]
    words = page.get_text("words")  # x0,y0,x1,y1,word,block,line,wordno
    rows = {}
    for w in words:
        key = round((w[1] + w[3]) / 2 / 3)  # bucket of 3 pt
        rows.setdefault(key, []).append(w)
    print(f"==== page {pg} ====")
    for k in sorted(rows):
        line = " | ".join(x[4] for x in sorted(rows[k], key=lambda x: x[0]))
        if pat is None or pat.search(line):
            print(line)
