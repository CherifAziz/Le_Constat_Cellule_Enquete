"""A10 - retrouve la page PDF (marqueur '=== page N ===') ou figure une expression dans un .txt extrait.
Usage : python -I page_de.py <fichier.txt> "<expression>" ["<expression>" ...]"""
import sys
f = sys.argv[1]
page = 0
lignes = open(f, encoding="utf-8", errors="replace").read().split("\n")
for expr in sys.argv[2:]:
    page = 0
    trouve = []
    for l in lignes:
        if l.startswith("=== page "):
            page = int(l.split()[2])
        elif expr.lower() in l.lower():
            trouve.append(page)
    print(repr(expr), "-> pages PDF", sorted(set(trouve))[:10])
