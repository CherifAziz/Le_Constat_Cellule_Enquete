"""A01 - Extraction en format long des tableaux Insee t_3201 à t_3214 (comptes des APU, base 2020).
Lecture seule de resultats/donnees/commun. Relançable : python -I 02_extraire_t32xx.py
Sortie : resultats/donnees/A01/A01_t32xx_long.csv
  colonnes : tableau;secteur;section;ligne_excel;poste;annee;valeur_mdeur
  section = DEPENSES / RECETTES / SOLDES (suivi des titres de bloc du tableau)
"""
import os, csv, openpyxl

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
SORTIE = os.path.join(RACINE, "resultats", "donnees", "A01", "A01_t32xx_long.csv")

TABLES = {
    "3201": "S13", "3202": "S1311", "3203": "S13111", "3204": "S13112", "3205": "S1313",
    "3206": "S13131", "3207": "S131311", "3208": "S131312", "3209": "S131313", "3210": "S131314",
    "3211": "S13132", "3212": "S1314", "3213": "S13141", "3214": "S13142",
}

def lire(num):
    ws = openpyxl.load_workbook(os.path.join(COMMUN, f"insee_cn_t_{num}.xlsx"), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    # ligne des années : première ligne contenant au moins 5 entiers >= 1900
    hdr_i = next(i for i, r in enumerate(rows) if sum(isinstance(c, (int, float)) and 1900 <= c <= 2100 for c in r) >= 5)
    hdr = rows[hdr_i]
    cols = {j: int(c) for j, c in enumerate(hdr) if isinstance(c, (int, float)) and 1900 <= c <= 2100}
    out, section = [], None
    for i in range(hdr_i + 1, len(rows)):
        r = rows[i]
        lab = next((c for c in r[:2] if isinstance(c, str) and c.strip()), None)
        if lab is None:
            continue
        l = lab.strip()
        if l == "DEPENSES":
            section = "DEPENSES"; continue
        if l == "RECETTES":
            section = "RECETTES"; continue
        if l == "SOLDES":
            section = "SOLDES"; continue
        if section is None:
            continue
        if l.startswith("Milliards") or l.startswith("Source"):
            break
        for j, an in cols.items():
            v = r[j] if j < len(r) else None
            if isinstance(v, (int, float)):
                out.append((section, i + 1, l, an, float(v)))
            elif isinstance(v, str) and v.strip():
                out.append((section, i + 1, l, an, v.strip()))  # N.D. etc. conservé
    return out

with open(SORTIE, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["tableau", "secteur", "section", "ligne_excel", "poste", "annee", "valeur_mdeur"])
    n = 0
    for num, sec in TABLES.items():
        for section, li, lab, an, v in lire(num):
            w.writerow([f"t_{num}", sec, section, li, lab, an, v]); n += 1
print("lignes écrites :", n, "->", SORTIE)
