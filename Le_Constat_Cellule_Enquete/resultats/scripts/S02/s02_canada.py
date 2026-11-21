"""S02 - Canada 1994-1999 : decomposition du redressement par niveau d'administration et par poste.
Entrees :
 - Finance Canada, Fiscal Reference Tables, sept. 2019 (donnees\\S02\\sources\\can_fiscal_reference_tables_2019.pdf),
   tableaux 36 a 45 (Statistique Canada, Government Finance Statistics, tableau 10-10-0015-01), millions de CAD,
   transcrits depuis le PDF par s02_pdf_rows.py (pages PDF 41-50) ;
 - PIB nominal : OCDE Economic Outlook 119 (copie de la piece d'A12, donnees\\S02\\copies_A12\\oecd_eo119_macro.csv).
Sortie : donnees\\S02\\S02_canada_decomposition.csv
Methode : ratio au PIB ; variation du ratio decomposee en effet nominal ((X1-X0)/Y1) et effet de denominateur (X0/Y1 - X0/Y0).
Reserve : millesime FRT 2019 pour les flux, millesime OCDE 2026 pour le PIB (revision du PIB nominal non controlee).
"""
import csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S02"
YEARS = [1993, 1994, 1995, 1996, 1997, 1998, 1999]
# (niveau, poste) -> valeurs 1993..1999 (millions CAD) ; tableau FRT
D = {
 ("federal", "recettes_totales"): [130281, 133398, 142163, 150423, 167166, 172154, 182799],          # T36
 ("federal", "impots_revenus"): [70883, 72774, 79088, 86962, 97176, 102531, 111940],               # T36
 ("federal", "cotisations_sociales"): [18619, 19940, 19497, 18824, 20212, 19005, 18659],           # T36
 ("federal", "depenses_totales"): [169209, 168163, 173993, 170149, 161697, 165643, 174376],        # T37
 ("federal", "dont_transferts_autres_adm"): [38509, 37809, 40131, 36024, 32365, 33556, 39586],     # T37 grants expense
 ("federal", "dont_prestations_sociales"): [47062, 45638, 44042, 43942, 43427, 43822, 44824],      # T37
 ("federal", "dont_remunerations"): [18647, 18607, 18675, 17738, 17184, 17444, 18400],             # T37
 ("federal", "dont_interets"): [39489, 40425, 46579, 45667, 43735, 44250, 44028],                  # T37
 ("federal", "capacite_financement"): [-40198, -35543, -32064, -18216, 6313, 7477, 8940],          # T38
 ("provinces", "recettes_totales"): [163244, 173488, 182589, 186288, 190076, 197437, 216332],      # T39
 ("provinces", "dont_transferts_recus"): [32866, 31908, 33853, 29686, 26108, 26942, 33187],        # T39 grants revenue
 ("provinces", "depenses_totales"): [185609, 187897, 192042, 189418, 192443, 204284, 211635],      # T40
 ("provinces", "dont_remunerations"): [50098, 49792, 49746, 48815, 49428, 50412, 52840],           # T40
 ("provinces", "dont_interets"): [23451, 25337, 27063, 26915, 26811, 28127, 28123],                # T40
 ("provinces", "capacite_financement"): [-23090, -15221, -10630, -4022, -2481, -7269, 5749],       # T41
 ("local", "recettes_totales"): [73517, 75029, 76977, 75771, 77418, 84129, 84939],                 # T42
 ("local", "dont_transferts_recus"): [33479, 34476, 35632, 33822, 33698, 39401, 37902],            # T42
 ("local", "depenses_totales"): [72722, 73743, 74813, 74322, 75354, 79332, 80945],                 # T43
 ("local", "capacite_financement"): [-1823, -1721, -1244, -1137, -73, 2826, 1730],                 # T44
 ("RPC_RRQ", "cotisations"): [12208, 12931, 14456, 14761, 15600, 18280, 21000],                    # T45
 ("RPC_RRQ", "prestations"): [18332, 19680, 20609, 21716, 22751, 23723, 24419],                    # T45
 ("RPC_RRQ", "capacite_financement"): [-908, -1666, -1028, -2186, -2708, -1173, 787],              # T45
 ("APU", "recettes_totales"): [318536, 334013, 352005, 368789, 395231, 410116, 438251],            # T33
 ("APU", "depenses_totales"): [379942, 383567, 392152, 392382, 392773, 406828, 420350],            # T34
 ("APU", "dont_interets"): [67539, 70277, 78254, 77112, 74862, 76392, 75947],                      # T34
 ("APU", "dont_remunerations"): [110805, 110800, 110987, 109110, 108879, 110526, 114763],          # T34
 ("APU", "dont_prestations_sociales"): [89629, 89849, 89347, 88983, 88537, 89868, 91134],          # T34
 ("APU", "capacite_financement"): [-66019, -54151, -44966, -25561, 1051, 1861, 17206],             # T35
}
# PIB nominal OCDE
gdp = {}
with open(os.path.join(R, "copies_A12", "oecd_eo119_macro.csv"), encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["REF_AREA"] == "CAN" and row["MEASURE"] == "GDP":
            gdp[int(row["TIME_PERIOD"])] = float(row["OBS_VALUE"]) / 1e6
# controle d'additivite
for i, y in enumerate(YEARS):
    s = sum(D[(n, "capacite_financement")][i] for n in ["federal", "provinces", "local", "RPC_RRQ"])
    assert abs(s - D[("APU", "capacite_financement")][i]) <= 2, (y, s)
out = os.path.join(R, "S02_canada_decomposition.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["niveau", "poste"] + [f"pctPIB_{y}" for y in YEARS] +
               ["d_1994_1997", "effet_nominal_1994_1997", "effet_denominateur_1994_1997", "d_1994_1999",
                "effet_nominal_1994_1999", "effet_denominateur_1994_1999", "var_nominale_pct_1994_1997"])
    for (n, p), v in D.items():
        r = [round(x / gdp[y] * 100, 2) for x, y in zip(v, YEARS)]
        res = [n, p] + r
        for t1 in (1997, 1999):
            x0, x1 = v[1], v[YEARS.index(t1)]
            y0, y1 = gdp[1994], gdp[t1]
            res += [round((x1 / y1 - x0 / y0) * 100, 2), round((x1 - x0) / y1 * 100, 2), round((x0 / y1 - x0 / y0) * 100, 2)]
        res.append(round((v[4] / v[1] - 1) * 100, 1))
        w.writerow(res)
print("PIB nominal (Md CAD):", {y: round(gdp[y] / 1e3, 1) for y in YEARS})
print("croissance PIB nominal 1994-1997 %:", round((gdp[1997] / gdp[1994] - 1) * 100, 1), " 1994-1999:", round((gdp[1999] / gdp[1994] - 1) * 100, 1))
for line in open(out, encoding="utf-8"):
    print(line.strip())
