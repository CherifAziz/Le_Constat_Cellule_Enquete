# Extraction de texte PDF -> .txt avec marqueurs de page [[p.N]] (lecture seule des pieces)
import sys, fitz
for p in sys.argv[1:]:
    d = fitz.open(p)
    out = p[:-4] + ".txt"
    with open(out, "w", encoding="utf-8") as f:
        for i, pg in enumerate(d, 1):
            f.write(f"\n[[p.{i}]]\n")
            f.write(pg.get_text())
    print(out, d.page_count)
