# -*- coding: utf-8 -*-
"""S01 - recherche dans un texte extrait (format [[p.N]]) : affiche, page par page,
les passages autour d'un motif (expression reguliere, insensible a la casse).
Usage : python -I s01_chercher.py FICHIER.txt MOTIF [largeur=400] [maxi=30]
        python -I s01_chercher.py FICHIER.txt --pages 12-15   (pages PDF completes)
"""
import sys, re

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
f = sys.argv[1]
t = open(f, encoding="utf-8").read()
parts = re.split(r"\[\[p\.(\d+)\]\]", t)
pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
if sys.argv[2] == "--pages":
    a, b = sys.argv[3].split("-") if "-" in sys.argv[3] else (sys.argv[3], sys.argv[3])
    for k in range(int(a), int(b) + 1):
        print(f"[[p.{k}]]", pages.get(k, "").strip())
    sys.exit()
motif = re.compile(sys.argv[2], re.I)
larg = int(sys.argv[3]) if len(sys.argv) > 3 else 400
maxi = int(sys.argv[4]) if len(sys.argv) > 4 else 30
n = 0
for k in sorted(pages):
    v = pages[k]
    for m in motif.finditer(v):
        a, b = max(0, m.start() - larg), min(len(v), m.end() + larg)
        print(f"--- p.{k} : ...{v[a:b]}...")
        n += 1
        if n >= maxi:
            sys.exit()
