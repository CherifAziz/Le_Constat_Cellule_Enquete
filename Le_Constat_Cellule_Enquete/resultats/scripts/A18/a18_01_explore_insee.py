# A18 - exploration brute des classeurs Insee de la base commune (lecture seule)
# Usage : python -I a18_01_explore_insee.py <dossier_commun>
import sys, hashlib, os, openpyxl
d = sys.argv[1]
for f in ["insee_dep_rec_serie_longue.xlsx", "insee_solde_par_sous_secteur.xlsx",
          "insee_dette_par_sous_secteur.xlsx", "insee_ip2106_compte_apu_2025.xlsx"]:
    p = os.path.join(d, f)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print("=====", f, h)
    wb = openpyxl.load_workbook(p, data_only=True)
    for ws in wb.worksheets:
        print("--- feuille", ws.title, ws.max_row, ws.max_column)
        for row in ws.iter_rows(max_row=min(ws.max_row, 12), values_only=True):
            print(row[:12])
