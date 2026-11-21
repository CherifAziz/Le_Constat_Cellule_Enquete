# S06 - recherche de mots-clés dans un PDF téléchargé (lecture seule, pymupdf).
# Usage : python -I s06_pdf_grep.py <fichier.pdf> <motif regex> [contexte_caracteres] [pages max]
import sys, re, warnings
warnings.filterwarnings("ignore")
import fitz
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path, pat = sys.argv[1], sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 250
maxhits = int(sys.argv[4]) if len(sys.argv) > 4 else 40
doc = fitz.open(path)
n = 0
for i, p in enumerate(doc):
    t = re.sub(r"\s+", " ", p.get_text())
    for m in re.finditer(pat, t, flags=re.I):
        n += 1
        if n > maxhits:
            sys.exit(0)
        a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
        print(f"--- p.{i+1} (pdf) : ...{t[a:b]}...")
print(f"[{n} occurrences, {len(doc)} pages]")
