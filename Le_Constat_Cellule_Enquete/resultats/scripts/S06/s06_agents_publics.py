# S06 - Cause 5 : masse salariale publique, comparaison européenne.
# Source : base commune, eurostat_gov_10a_main.csv (extraction 20/11/2026, Eurostat updated 2026-10-21), S13.
# Lancer : python -I s06_agents_publics.py
# Sortie : resultats/donnees/S06/c5_masse_salariale_comparaison.csv
import csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
src = os.path.join(R, "donnees", "commun", "eurostat_gov_10a_main.csv")
out = os.path.join(R, "donnees", "S06", "c5_masse_salariale_comparaison.csv")
d = {}
for r in csv.DictReader(open(src, encoding="utf-8")):
    if r["sector"] != "S13" or r["value"] in ("", None):
        continue
    d[(r["unit"], r["na_item"], r["geo"], r["time"])] = float(r["value"])

def pib(geo, y):
    # PIB dérivé de TE (dépense totale, ratio publié à 0,1 pt près sur ~57 % : erreur relative < 0,1 %),
    # plutôt que de B9 (ratio arrondi à 5,1 % : erreur relative jusqu'à 1 %). Contrôle : écarts TE/TR 2025
    # avec la ZE20 hors FR = 9,24 / 6,66 pts (vague1 §2.5 : 9,2 / 6,7).
    m = d.get(("MIO_EUR", "TE", geo, y)); p = d.get(("PC_GDP", "TE", geo, y))
    if m is None or not p:
        return None
    return m / p * 100

items = {"D1": ["D1PAY"], "D1+P2": ["D1PAY", "P2"], "D1+P2+D632": ["D1PAY", "P2", "D632PAY"]}
geos = ["FR", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT", "PT", "EL", "IE", "EA20"]
rows = []
for y in ["1995", "2007", "2017", "2019", "2024", "2025"]:
    for lab, its in items.items():
        vals = {}
        for g in geos:
            v = [d.get(("PC_GDP", i, g, y)) for i in its]
            vals[g] = sum(v) if None not in v else None
        # zone euro hors France, en montants (règle vague1 §2.5) ; avant 1999 les MIO_EUR sont en écus mais le ratio reste un rapport homogène
        try:
            num = sum(d[("MIO_EUR", i, "EA20", y)] - d[("MIO_EUR", i, "FR", y)] for i in its)
            den = pib("EA20", y) - pib("FR", y)
            exfr = num / den * 100
        except (KeyError, TypeError):
            exfr = None
        pibfr = pib("FR", y)
        for ref, v in [("EA20", vals["EA20"]), ("EA20_hors_FR", exfr)]:
            if vals["FR"] is None or v is None:
                continue
            ecart = vals["FR"] - v
            rows.append([y, lab, ref, round(vals["FR"], 2), round(v, 2), round(ecart, 2),
                         round(ecart * pibfr / 100 / 1000, 1) if pibfr else "", ""])
        for g in geos[1:-1]:
            if vals["FR"] is not None and vals[g] is not None:
                ecart = vals["FR"] - vals[g]
                rows.append([y, lab, g, round(vals["FR"], 2), round(vals[g], 2), round(ecart, 2),
                             round(ecart * pibfr / 100 / 1000, 1) if pibfr else "", ""])
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "agregat", "reference", "FR_pct_PIB", "ref_pct_PIB", "ecart_pts", "ecart_Mds_EUR_PIB_FR", "note"])
    w.writerows(rows)
print("PIB FR 2025 (Md€) :", round(pib("FR", "2025") / 1000, 1), "| B9 2025 :", d.get(("MIO_EUR", "B9", "FR", "2025")))
for r in rows:
    if r[0] in ("2025", "2017", "1995") and r[2] in ("EA20", "EA20_hors_FR", "DE", "IT", "ES", "NL", "SE", "DK", "BE"):
        print(r)
