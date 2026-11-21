# A18 - charges d'intérêts et solde S13, Insee tableau 3.201 (base 2020, Md€), base commune
# Usage : python -I a18_03_interets_insee.py <insee_cn_t_3201.xlsx> <insee_dep_rec_serie_longue.xlsx>
import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], data_only=True); ws = wb.worksheets[0]
rows = list(ws.iter_rows(values_only=True))
years = rows[2][2:]
def line(label_start):
    for r in rows:
        if r[1] and str(r[1]).strip().startswith(label_start):
            return dict(zip(years, r[2:]))
D41 = line("Intérêts (D41)")          # première occurrence = dépenses
D41G = line("Intérêts hors correction")
TE = line("Total des dépenses"); TR = line("Total des recettes")
B9 = line("Capacité (+) ou besoin (-) de financement")
# recettes d'intérêts (2e occurrence)
occ = [r for r in rows if r[1] and str(r[1]).strip().startswith("Intérêts (D41)")]
D41R = dict(zip(years, occ[1][2:]))
print("annee;D41_dep;D41G_dep;D41_rec;B9;interets_nets;part_D41_dans_deficit;part_D41G_dans_deficit;solde_primaire(B9+D41)")
for y in [1974, 1975, 1980, 1985, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 2019, 2024, 2025]:
    if y in B9 and B9[y]:
        print(f"{y};{D41[y]:.2f};{D41G[y]:.2f};{D41R[y]:.2f};{B9[y]:.2f};{D41[y]-D41R[y]:.2f};{-D41[y]/B9[y]:.3f};{-D41G[y]/B9[y]:.3f};{B9[y]+D41[y]:.2f}")
# PIB implicite pour 1993 et 2025 via le classeur série longue (solde %PIB) : PIB = -B9 / (deficit%/100)
wb2 = openpyxl.load_workbook(sys.argv[2], data_only=True); r2 = list(wb2.worksheets[0].iter_rows(values_only=True))
hdr = r2[3]
import re
dep = {int(re.match(r"\s*(\d{4})", str(h)).group(1)): v for h, v in zip(hdr[1:], r2[4][1:]) if h is not None and re.match(r"\s*(\d{4})", str(h))}
pib = {y: TE[y] / dep[y] * 100 for y in TE if y in dep and isinstance(dep[y], (int, float))}
for y in [1993, 2025]:
    print(y, "PIB implicite (TE/dep pct) Md€ = %.1f ; D41 %%PIB = %.2f ; solde primaire %%PIB = %.2f" % (pib[y], 100 * D41[y] / pib[y], 100 * (B9[y] + D41[y]) / pib[y]))
