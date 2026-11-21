"""S07 - extraction texte page par page d'un PDF (pymupdf) et recherche de motifs.
Usage : python -I extraire.py <pdf> <sortie.txt> [motif1 motif2 ...]
Écrit le texte avec des marqueurs '=== page N ===' (N = page réelle du PDF, base 1)
puis affiche les pages contenant chaque motif (insensible à la casse)."""
import sys, re
import fitz  # pymupdf
sys.stdout.reconfigure(encoding="utf-8")

pdf, out = sys.argv[1], sys.argv[2]
motifs = sys.argv[3:]
doc = fitz.open(pdf)
hits = {m: [] for m in motifs}
with open(out, "w", encoding="utf-8") as f:
    for i, p in enumerate(doc, 1):
        t = p.get_text()
        f.write(f"\n=== page {i} ===\n{t}")
        for m in motifs:
            if re.search(m, t, re.I):
                hits[m].append(i)
print(pdf, "pages:", len(doc))
for m, v in hits.items():
    print(m, "->", v[:40])
