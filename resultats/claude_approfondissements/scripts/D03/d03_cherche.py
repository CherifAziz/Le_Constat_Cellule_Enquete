"""Recherche par mot-clé dans les textes extraits (une page par ligne, marqueur [[p.N]]).
Usage : python d03_cherche.py "<regex>" fichier1.txt [fichier2.txt ...] [--ctx 300] [--max 20]
Affiche, pour chaque occurrence, le fichier, la page et le contexte.
Outil de lecture ; ne produit pas de table."""
import re
import sys
from pathlib import Path

def main():
    args = sys.argv[1:]
    ctx, mx = 300, 20
    if "--ctx" in args:
        i = args.index("--ctx"); ctx = int(args[i + 1]); del args[i:i + 2]
    if "--max" in args:
        i = args.index("--max"); mx = int(args[i + 1]); del args[i:i + 2]
    pat = re.compile(args[0], re.I)
    for f in args[1:]:
        p = Path(f)
        n = 0
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            # recolle les mots coupés (trait d'union conditionnel, coupure de fin de ligne)
            line = re.sub(r"(\w)­\s*(\w)", r"\1\2", line)
            line = re.sub(r"([a-zà-ÿ])- ([a-zà-ÿ])", r"\1\2", line)
            m0 = re.match(r"\[\[p\.(\d+)\]\]", line)
            page = m0.group(1) if m0 else "?"
            for m in pat.finditer(line):
                a, b = max(0, m.start() - ctx), min(len(line), m.end() + ctx)
                print(f"--- {p.name} p.{page}: ...{line[a:b]}...")
                n += 1
                if n >= mx:
                    break
            if n >= mx:
                break
        if n == 0:
            print(f"--- {p.name}: aucune occurrence")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
