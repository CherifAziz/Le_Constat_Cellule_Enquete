# A06 - extraction texte PDF (pymupdf) et recherche de motifs avec numéro de page réel.
# Usage : python -I pdfgrep.py <fichier.pdf> <regex> [contexte_caracteres] [max]
#         python -I pdfgrep.py <fichier.pdf> --page N   (affiche la page N, numérotation PDF à partir de 1)
import sys, re
import fitz
doc = fitz.open(sys.argv[1])
if sys.argv[2] == '--page':
    for n in sys.argv[3].split(','):
        print(f'----- page PDF {n} -----')
        print(doc[int(n) - 1].get_text())
    sys.exit()
pat = re.compile(sys.argv[2], re.I)
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 200
mx = int(sys.argv[4]) if len(sys.argv) > 4 else 30
k = 0
for i, p in enumerate(doc):
    t = p.get_text().replace('\n', ' ')
    for m in pat.finditer(t):
        a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
        print(f'[p.{i+1}] ...{t[a:b]}...')
        k += 1
        if k >= mx: sys.exit()
