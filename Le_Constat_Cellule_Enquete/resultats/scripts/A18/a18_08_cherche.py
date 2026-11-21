# A18 - recherche d'une expression dans un texte extrait (renvoie page PDF et contexte)
# Usage : python -I a18_08_cherche.py <fichier_txt> <largeur> <max_par_motif> <motif1> [motif2 ...]
# Les motifs sont des expressions régulières insensibles à la casse ; les espaces et retours à la ligne sont normalisés.
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
f, w, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
t = open(f, encoding="utf-8").read()
parts = re.split(r"\[\[p\.(\d+)\]\]", t)
if len(parts) > 1:
    pg = [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]
else:
    pg = [(0, t)]
for pat in sys.argv[4:]:
    n = 0
    for num, s in pg:
        s2 = " ".join(s.split())
        for m in re.finditer(pat, s2, flags=re.I):
            print(f"## [{pat}] p.{num} : ...{s2[max(0, m.start() - w):m.end() + w]}...")
            n += 1
            if n >= k: break
        if n >= k: break
    if n == 0: print(f"## [{pat}] AUCUNE OCCURRENCE")
