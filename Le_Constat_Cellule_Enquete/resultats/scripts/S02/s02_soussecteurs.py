"""S02 - Qui a porte l'effort : soldes et postes par sous-secteur (Eurostat gov_10a_main, base commune de la cellule,
lecture seule : resultats\\donnees\\commun\\eurostat_gov_10a_main.csv, extraction du 20/11/2026), % du PIB.
Pays et fenetres : DE 2002->2007 et 2002->2019 ; BE 1995->2000->2007 (Eurostat commence en 1995 ; t0 d'A12 = 1992 non couvert) ;
IT 1995->2000 et 1995->2019 (t0 d'A12 = 1991 non couvert).
Sortie : donnees\\S02\\S02_soussecteurs_DE_BE_IT.csv
Postes : B9 solde ; TR recettes ; TE depenses ; D41PAY interets ; P51G FBCF ; D1PAY remunerations ; D62PAY prestations en especes.
Secteurs : S13 APU ; S1311 Etat central ; S1312 Etats federes ; S1313 administrations locales ; S1314 securite sociale.
Les transferts entre sous-secteurs ne sont pas neutralises (non consolide) : un gain d'un niveau peut etre une perte d'un autre.
"""
import csv, os
B = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
SRC = os.path.join(B, "commun", "eurostat_gov_10a_main.csv")
OUT = os.path.join(B, "S02", "S02_soussecteurs_DE_BE_IT.csv")
win = {"DE": [2002, 2005, 2007, 2012, 2019], "BE": [1995, 2000, 2003, 2007, 2019], "IT": [1995, 1997, 2000, 2007, 2019]}
items = ["B9", "TR", "TE", "D41PAY", "P51G", "D1PAY", "D62PAY"]
d = {}
with open(SRC, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["unit"] == "PC_GDP" and r["geo"] in win and r["na_item"] in items and r["value"] not in ("", ":"):
            d[(r["geo"], r["sector"], r["na_item"], int(r["time"]))] = float(r["value"])
rows = []
for g, ys in win.items():
    for s in ["S13", "S1311", "S1312", "S1313", "S1314"]:
        for it in items:
            vals = [d.get((g, s, it, y)) for y in ys]
            if all(v is None for v in vals):
                continue
            rows.append([g, s, it] + ["" if v is None else v for v in vals] +
                        [("" if None in (vals[0], vals[2]) else round(vals[2] - vals[0], 2)),
                         ("" if None in (vals[0], vals[4]) else round(vals[4] - vals[0], 2))])
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["pays", "secteur", "poste", "a1", "a2", "a3", "a4", "a5", "d_a1_a3", "d_a1_a5"])
    for g, ys in win.items():
        w.writerow([g, "annees", ""] + ys + ["", ""])
    w.writerows(rows)
for g, ys in win.items():
    print(g, ys)
for r in rows:
    print(";".join(str(x) for x in r))
