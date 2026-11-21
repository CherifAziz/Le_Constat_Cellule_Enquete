"""A01 - Inventaire des classeurs Insee de la base commune (lecture seule).
Usage : python -I 01_inventaire_xlsx.py
Sortie : resultats/donnees/A01/inventaire_xlsx.txt (feuilles, dimensions, 12 premières lignes, libellés de lignes)
"""
import os, openpyxl

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
SORTIE = os.path.join(RACINE, "resultats", "donnees", "A01", "inventaire_xlsx.txt")

def court(v):
    if v is None:
        return ""
    s = str(v).replace("\n", " ")
    return s[:60]

with open(SORTIE, "w", encoding="utf-8") as out:
    for f in sorted(os.listdir(COMMUN)):
        if not f.endswith(".xlsx"):
            continue
        wb = openpyxl.load_workbook(os.path.join(COMMUN, f), read_only=True, data_only=True)
        out.write(f"\n######## {f}\n")
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            out.write(f"=== feuille '{ws.title}' : {len(rows)} lignes x {max((len(r) for r in rows), default=0)} col\n")
            for i, r in enumerate(rows[:8]):
                out.write(f"  L{i+1}: " + " | ".join(court(c) for c in r[:12]) + "\n")
            # libellés de toutes les lignes (2 premières colonnes non vides)
            out.write("  -- libellés --\n")
            for i, r in enumerate(rows):
                lab = [court(c) for c in r[:3] if c is not None and not isinstance(c, (int, float))]
                if lab:
                    out.write(f"  L{i+1}: " + " / ".join(lab) + "\n")
print("ok", SORTIE)
