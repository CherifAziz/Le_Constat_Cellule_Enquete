# A18 - chiffres-clés tirés des classeurs Insee bruts (base 2020, téléchargés le 20/11/2026, base commune)
# Usage : python -I a18_02_series_insee.py <dossier_commun> <fichier_sortie_csv>
import sys, os, openpyxl, csv
d, out = sys.argv[1], sys.argv[2]

import re
def yr(y):
    m = re.match(r'\s*(\d{4})', str(y)) if y is not None else None
    return int(m.group(1)) if m else None

def table(path, sheet, header_row_idx):
    wb = openpyxl.load_workbook(os.path.join(d, path), data_only=True)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[header_row_idx]
    res = {}
    for r in rows[header_row_idx + 1:]:
        if r[0] is None:
            continue
        name = str(r[0]).strip()
        res[name] = {yr(y): v for y, v in zip(hdr[1:], r[1:]) if yr(y) and isinstance(v, (int, float))}
    return res

dr = table("insee_dep_rec_serie_longue.xlsx", None, 3)
DEP, REC, SOL = dr["Dépenses"], dr["Recettes"], dr["Déficit au sens de Maastricht"]
DET = [v for k, v in dr.items() if k.startswith("Dette des administrations publiques (brute)")][0]
sb = table("insee_solde_par_sous_secteur.xlsx", "Figure 1", 3)["Ensemble"]
sp = table("insee_solde_par_sous_secteur.xlsx", "Figure 2", 3)["Ensemble"]
de = table("insee_dette_par_sous_secteur.xlsx", "Figure 1", 3)
debt_eur = [v for k, v in de.items() if k.startswith("Ensemble")][0]
rows = []
def add(cle, val, note=""):
    rows.append((cle, val, note)); print(cle, ";", val, ";", note)

# Solde : années d'excédent
exc = [y for y, v in sp.items() if v > 0]
add("annees_solde_positif_pctPIB_fig2", exc, "Figure 2 solde % PIB, signe + = capacité")
add("solde_1974_Md€", sb.get(1974)); add("solde_1974_pctPIB", sp.get(1974))
add("solde_1975_pctPIB", sp.get(1975)); add("solde_1975_Md€", sb.get(1975))
neg = [y for y in range(1975, 2026) if sp.get(y, 0) < 0]
add("nb_annees_deficit_1975_2025", len(neg), "sur 51 exercices 1975-2025")
add("annees_non_negatives_1975_2025", [y for y in range(1975, 2026) if sp.get(y, -1) >= 0])
add("deficit_maastricht_serie_longue_1974", SOL.get(1974), "convention déficit positif")
for y in [2009, 2020, 2021, 2025]:
    add(f"solde_{y}_Md€", sb.get(y)); add(f"solde_{y}_pctPIB", sp.get(y))
add("record_deficit_Md€", min(sb.items(), key=lambda kv: kv[1]))
for y in [1960, 1973, 1974, 1975, 1980, 1983, 1984, 1985, 1990, 1992, 1993, 1994, 1995, 1996, 2007, 2019, 2023, 2024, 2025]:
    add(f"dep_rec_{y}", (round(DEP.get(y, float('nan')), 2), round(REC.get(y, float('nan')), 2)), "% PIB")
add("hausse_rec_1974_2025_pts", round(REC[2025] - REC[1974], 2))
add("hausse_dep_1974_2025_pts", round(DEP[2025] - DEP[1974], 2))
add("ecart_dep_moins_rec_2025", round(DEP[2025] - REC[2025], 2))
add("hausse_rec_1985_2025_pts", round(REC[2025] - REC[1985], 2))
add("hausse_dep_1985_2025_pts", round(DEP[2025] - DEP[1985], 2))
add("hausse_rec_1974_1985_pts", round(REC[1985] - REC[1974], 2))
add("hausse_dep_1974_1993_pts", round(DEP[1993] - DEP[1974], 2), "part de la hausse 1974-2025 acquise en 1993 = %.0f %%" % (100 * (DEP[1993] - DEP[1974]) / (DEP[2025] - DEP[1974])))
add("dep_moyenne_1994_2025", round(sum(DEP[y] for y in range(1994, 2026)) / 32, 2), "min %.1f max %.1f" % (min(DEP[y] for y in range(1994, 2026)), max(DEP[y] for y in range(1994, 2026))))
add("rec_max_1985_2025", max(((y, round(REC[y], 1)) for y in range(1985, 2026)), key=lambda t: t[1]))
# dette en mois de production : ratio/100*12
for y in [2007, 2008, 2012, 2019, 2020, 2021, 2022, 2024, 2025]:
    add(f"dette_{y}_pctPIB", DET.get(y), "mois de production = %.2f" % (DET.get(y) * 12 / 100))
add("dette_2025_2024_croissance_%", round(100 * (debt_eur[2025] / debt_eur[2024] - 1), 2))
pib24 = debt_eur[2024] / DET[2024] * 100; pib25 = debt_eur[2025] / DET[2025] * 100
add("PIB_implicite_2024_2025_Md€", (round(pib24, 1), round(pib25, 1)), "dette Md€ / dette %PIB")
add("croissance_PIB_nominal_2025_implicite_%", round(100 * (pib25 / pib24 - 1), 2))
add("ratio_vitesse_dette_sur_PIB_2025", round((debt_eur[2025] / debt_eur[2024] - 1) / (pib25 / pib24 - 1), 2))
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["cle", "valeur", "note"]); w.writerows(rows)
