"""Compacte un extrait texte (fusion des lignes, suppression des blancs) pour lecture intégrale.
Usage : python -I compacter.py <extrait.txt> [page_debut page_fin]
Écrit <extrait>_compact.txt à côté et affiche la taille.
"""
import sys, re
src = sys.argv[1]
t = open(src, encoding="utf-8").read()
parts = re.split(r"\n===== PAGE (\d+) =====\n", t)
d1 = int(sys.argv[2]) if len(sys.argv) > 2 else 1
d2 = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6
out = []
for i in range(1, len(parts), 2):
    p = int(parts[i])
    if d1 <= p <= d2:
        txt = re.sub(r"-\n(?=[a-zà-ÿ])", "", parts[i + 1])
        txt = re.sub(r"\s*\n\s*", " ", txt)
        txt = re.sub(r" {2,}", " ", txt)
        out.append(f"[p{p}] {txt.strip()}")
dst = src.replace(".txt", "_compact.txt")
open(dst, "w", encoding="utf-8").write("\n".join(out))
print(dst, len("\n".join(out)))
