"""Convertit un HTML téléchargé en texte (donnees/S14/textes/<nom>.txt) et affiche le contexte des mots-clés.
Usage : python -I html_texte_grep.py <fichier.html> <mot-clé> [<mot-clé> ...]  (filtre : contexte contenant CVAE, production ou sociétés)"""
import sys, re, os
from bs4 import BeautifulSoup
sys.stdout.reconfigure(encoding="utf-8")
OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14\textes"
f = sys.argv[1]
t = re.sub(r"\s+", " ", BeautifulSoup(open(f, "rb").read(), "html.parser").get_text(" "))
open(os.path.join(OUT, os.path.splitext(os.path.basename(f))[0] + ".txt"), "w", encoding="utf-8").write(t)
print("#####", f, len(t))
for k in sys.argv[2:]:
    for m in list(re.finditer(re.escape(k), t))[:6]:
        s = t[max(0, m.start() - 350): m.end() + 350]
        if any(w in s for w in ("CVAE", "production", "sociétés")):
            print(">>", k, ":", s, "\n")
