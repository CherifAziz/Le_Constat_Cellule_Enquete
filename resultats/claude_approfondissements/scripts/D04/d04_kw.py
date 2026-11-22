"""Recherche par mot-cle dans un texte extrait.
Usage : python d04_kw.py fichier.txt motif [largeur] [max]
Page : marqueur '=== PAGE PDF N ===' s'il existe, sinon saut de page (\\f)."""
import sys, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
path, pat = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 300
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 30
t = open(path, encoding='utf-8', errors='replace').read()
marks = [(m.start(), m.group(1)) for m in re.finditer(r'=== PAGE PDF (\d+) ===', t)]
n = 0
for m in re.finditer(pat, t, flags=re.I):
    if marks:
        prev = [p for (pos, p) in marks if pos < m.start()]
        page = prev[-1] if prev else '1'
    else:
        page = t.count('\f', 0, m.start()) + 1
    s = t[max(0, m.start() - w): m.end() + w]
    print(f"--- p.{page} @{m.start()}: {re.sub(r'\s+', ' ', s)}")
    n += 1
    if n >= mx:
        break
print(f"[{n} occurrences affichees]")
