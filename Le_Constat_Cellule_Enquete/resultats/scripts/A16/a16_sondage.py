# -*- coding: utf-8 -*-
"""A16 - sondage : chiffres et citations de la cellule refaits sur des pieces retelechargees a l'origine
le 20/11/2026 (donnees\\A16\\sources\\, voir MANIFESTE_PIECES.csv). Lancer : python -I a16_sondage.py
Les fichiers telecharges sont lus comme donnees (openpyxl, json, pymupdf), jamais executes."""
import os, json, re
import openpyxl
import fitz  # pymupdf

S = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A16\sources"
OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A16\a16_sortie_sondage.txt"
L = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)

# 1. Insee, serie longue depenses / recettes (fichier retelecharge sur insee.fr)
wb = openpyxl.load_workbook(os.path.join(S, "insee_econ-fin-pub-rec-dep.xlsx"), read_only=True, data_only=True)
ws = wb[wb.sheetnames[0]]
rows = [r for r in ws.iter_rows(values_only=True)]
hdr_i = next(i for i, r in enumerate(rows) if r and any(isinstance(c, (int, float)) and c == 1974 for c in r) or
             (r and any(str(c).strip() == "1974" for c in r if c is not None)))
log("Insee : feuille", ws.title, "; ligne d'en-tete des annees :", hdr_i)
hdr = rows[hdr_i]
def val(label_start, year):
    # en-tetes du type 2021, '2024 (sd)', '2025 (p)'
    col = next(j for j, c in enumerate(hdr) if c is not None and str(c).strip().startswith(str(year)))
    for r in rows[hdr_i + 1:]:
        if r and r[0] and str(r[0]).strip().lower().startswith(label_start.lower()):
            return r[col]
    return None
for lab in ("Dépenses", "Recettes", "Déficit"):
    for y in (1974, 2025):
        try:
            log(f"  {lab} {y} : {val(lab, y)}")
        except StopIteration:
            log(f"  {lab} {y} : colonne introuvable (format en lignes ?)")

# 2. Eurostat gov_10a_main (API, retelecharge)
def lire_jsonstat(f):
    d = json.load(open(os.path.join(S, f), encoding="utf-8"))
    dims = d["id"]; size = d["size"]
    idx = {k: {v: i for v, i in d["dimension"][k]["category"]["index"].items()} for k in dims}
    out = {}
    for flat, v in d["value"].items():
        flat = int(flat); coords = []
        for k, n in zip(reversed(dims), reversed(size)):
            coords.append(flat % n); flat //= n
        coords = list(reversed(coords))
        key = tuple(next(c for c, i in idx[k].items() if i == coords[j]) for j, k in enumerate(dims))
        out[key] = v
    return dims, out
dims, v = lire_jsonstat("eurostat_gov_10a_main_FR_EA20.json")
log("Eurostat gov_10a_main, dimensions", dims, "; mise a jour :", json.load(open(os.path.join(S, "eurostat_gov_10a_main_FR_EA20.json"), encoding="utf-8")).get("updated"))
for k in sorted(v):
    log("  ", k, v[k])
for f in ("eurostat_lfsi_emp_a.json", "eurostat_lfsa_ergan_60_64.json"):
    dims, v = lire_jsonstat(f)
    log("Eurostat", f, "dimensions", dims)
    for k in sorted(v):
        log("  ", k, v[k])

# 2 bis. Excedents primaires 2002-2025 (B9 + D41PAY), FR IT DE BE
dims, v = lire_jsonstat("eurostat_gov_10a_main_B9_D41_2002_2025.json")
for g in ("FR", "IT", "DE", "BE"):
    n = sum(1 for y in range(2002, 2026)
            if ("A", "PC_GDP", "S13", "B9", g, str(y)) in v
            and v[("A", "PC_GDP", "S13", "B9", g, str(y))] + v[("A", "PC_GDP", "S13", "D41PAY", g, str(y))] > 0)
    log(f"  excedents primaires 2002-2025 {g} : {n}")

# 3. Cour des comptes, RSPFP juillet 2024 (vie-publique.fr) : phrase des 62 Md EUR
doc = fitz.open(os.path.join(S, "vp294882_cour_RSPFP_juillet2024.pdf"))
for i, p in enumerate(doc):
    t = p.get_text()
    for m in re.finditer(r"62\s?Md", t):
        a = max(0, m.start() - 350); b = min(len(t), m.end() + 250)
        log(f"  Cour RSPFP 2024, page PDF {i+1} :", " ".join(t[a:b].split()))
open(OUT, "w", encoding="utf-8").write("\n".join(L))
