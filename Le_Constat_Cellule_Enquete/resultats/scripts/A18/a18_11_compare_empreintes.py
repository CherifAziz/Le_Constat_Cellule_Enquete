# A18 - compare l'empreinte de chaque pièce retéléchargée par A18 avec la copie conservée par la cellule (quand elle existe)
# Usage : python -I a18_11_compare_empreintes.py <racine_resultats> <sortie.csv>
import sys, os, glob, hashlib, csv
racine, out = sys.argv[1], sys.argv[2]
def h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
rows = []
for lst in sorted(glob.glob(os.path.join(racine, "donnees", "A18", "liste_pieces_*.tsv"))):
    for line in open(lst, encoding="utf-8"):
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3 or not parts[2].strip(): continue
        a18 = os.path.join(racine, "donnees", "A18", "sources", parts[0])
        cel = os.path.join(racine, parts[2].replace("donnees/", "donnees" + os.sep, 1))
        if not os.path.exists(a18) or not os.path.exists(cel):
            rows.append((parts[0], parts[2], "absent", "", "")); continue
        ha, hc = h(a18), h(cel)
        rows.append((parts[0], parts[2], "IDENTIQUE" if ha == hc else "DIFFERENTE", ha, hc))
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["piece_A18", "copie_cellule", "comparaison", "sha256_A18", "sha256_copie"]); w.writerows(rows)
for r in rows: print(r[0], r[2])
