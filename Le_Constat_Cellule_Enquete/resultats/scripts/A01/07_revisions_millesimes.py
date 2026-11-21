"""A01 - Révisions entre millésimes / bases des séries Insee de solde, dépenses et recettes des APU.
Entrées :
  - copies Wayback Machine des fichiers Insee (resultats/donnees/A01/sources/wayback/, lues comme données) :
      deficit_euro_2022-12.xlsx, deficit_pib_2022-12.xlsx  (base 2014, capturés le 11/12/2022)
      deficit_euro_2020-11.xlsx (base 2014, capturé le 06/11/2020)
      recdep_2022-04.xlsx (base 2014, capturé le 27/04/2022) ; recdep_2025-07.xlsx (base 2020, capturé le 24/07/2025)
  - base commune (base 2020, août 2026) : base_insee_solde_sous_secteurs.csv, base_insee_dep_rec_pctPIB.csv
Sorties : resultats/donnees/A01/A01_revisions_millesimes.csv (année ; série ; valeurs par millésime ; écarts)
          resultats/donnees/A01/A01_revisions_sup_0_2pt.csv (années où |révision| > 0,2 pt de PIB)
Relançable : python -I 07_revisions_millesimes.py
"""
import os, csv, openpyxl
from collections import defaultdict

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
A01 = os.path.join(RACINE, "resultats", "donnees", "A01")
WB = os.path.join(A01, "sources", "wayback")

def lire_xlsx(f):
    ws = openpyxl.load_workbook(os.path.join(WB, f), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = next(r for r in rows if sum(isinstance(c, int) and 1900 < c < 2100 for c in r) > 5)
    d = defaultdict(dict)
    for r in rows:
        if r is hdr or not isinstance(r[0], str):
            continue
        for j, an in enumerate(hdr):
            if isinstance(an, int) and j < len(r) and isinstance(r[j], (int, float)):
                d[r[0].strip()][an] = float(r[j])
    return d

def lire_csv(f):
    d = defaultdict(dict)
    with open(os.path.join(COMMUN, f), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            try:
                d[(r["feuille"], r["serie"].strip())][int(r["annee"])] = float(r["valeur"])
            except ValueError:
                pass
    return d

B14_EUR_2022 = lire_xlsx("deficit_euro_2022-12.xlsx")
B14_PIB_2022 = lire_xlsx("deficit_pib_2022-12.xlsx")
B14_EUR_2020 = lire_xlsx("deficit_euro_2020-11.xlsx")
B14_RD_2022 = lire_xlsx("recdep_2022-04.xlsx")
B20_RD_2025 = lire_xlsx("recdep_2025-07.xlsx")
SOL = lire_csv("base_insee_solde_sous_secteurs.csv")
RD = lire_csv("base_insee_dep_rec_pctPIB.csv")

def cle(d, debut):
    return next(k for k in d if k.startswith(debut))

lignes = []
for an in range(1949, 2026):
    b14e = B14_EUR_2022[cle(B14_EUR_2022, "Ensemble")].get(an)
    b14e20 = B14_EUR_2020[cle(B14_EUR_2020, "Ensemble")].get(an)
    b14p = B14_PIB_2022[cle(B14_PIB_2022, "Ensemble")].get(an)
    b20e = SOL[("Figure 1", "Ensemble")].get(an)
    b20p = SOL[("Figure 2", "Ensemble")].get(an)
    b20p_2025 = B20_RD_2025[cle(B20_RD_2025, "Déficit")].get(an)
    b14p_rd = B14_RD_2022[cle(B14_RD_2022, "Déficit")].get(an)
    dep14 = B14_RD_2022[cle(B14_RD_2022, "Dépenses")].get(an)
    rec14 = B14_RD_2022[cle(B14_RD_2022, "Recettes")].get(an)
    dep20_25 = B20_RD_2025[cle(B20_RD_2025, "Dépenses")].get(an)
    rec20_25 = B20_RD_2025[cle(B20_RD_2025, "Recettes")].get(an)
    dep20 = RD[("Données", "Dépenses")].get(an)
    rec20 = RD[("Données", "Recettes")].get(an)
    def e(a, b):
        return round(a - b, 3) if a is not None and b is not None else ""
    lignes.append([an, b14e20, b14e, b20e, b14p, b20p_2025, b20p, e(b20p, b14p), e(b20p, b20p_2025),
                   dep14, dep20_25, dep20, e(dep20, dep14), rec14, rec20_25, rec20, e(rec20, rec14),
                   ("+" if b14e and b14e > 0 else "-" if b14e and b14e < 0 else "0/nd") + "/" + ("+" if b20e and b20e > 0 else "-" if b20e and b20e < 0 else "0/nd")])
ent = ["annee", "solde_Md€_base2014_cap2020-11", "solde_Md€_base2014_cap2022-12", "solde_Md€_base2020_aout2026",
       "solde_pct_base2014_cap2022-12", "solde_pct_base2020_cap2025-07", "solde_pct_base2020_aout2026", "revision_solde_pct_b2020_vs_b2014", "revision_solde_pct_2026_vs_2025",
       "depenses_pct_b2014", "depenses_pct_b2020_cap2025-07", "depenses_pct_b2020_aout2026", "revision_depenses_b2020_vs_b2014",
       "recettes_pct_b2014", "recettes_pct_b2020_cap2025-07", "recettes_pct_b2020_aout2026", "revision_recettes_b2020_vs_b2014", "signe_solde_b2014/b2020"]
with open(os.path.join(A01, "A01_revisions_millesimes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(ent); w.writerows(lignes)
sup = []
for l in lignes:
    for idx, nom in [(7, "solde b2020 vs b2014"), (8, "solde août 2026 vs juillet 2025"), (12, "dépenses b2020 vs b2014"), (16, "recettes b2020 vs b2014")]:
        if l[idx] != "" and abs(l[idx]) > 0.2 + 1e-9:
            sup.append([l[0], nom, l[idx]])
with open(os.path.join(A01, "A01_revisions_sup_0_2pt.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["annee", "serie", "revision_pts_PIB"]); w.writerows(sup)
# dette brute % PIB : base 2014 (cap. 04/2022), base 2020 (cap. 07/2025), base 2020 (août 2026)
dette = []
for an in range(1995, 2026):
    a = B14_RD_2022[cle(B14_RD_2022, "Dette des administrations publiques (brute)")].get(an)
    b = B20_RD_2025[cle(B20_RD_2025, "Dette des administrations publiques (brute)")].get(an)
    c = RD[("Données", "Dette des administrations publiques (brute)2")].get(an)
    dette.append([an, a, b, c, round(c - a, 2) if a is not None and c is not None else "", round(c - b, 2) if b is not None and c is not None else ""])
with open(os.path.join(A01, "A01_revisions_dette.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "dette_pct_b2014_cap2022-04", "dette_pct_b2020_cap2025-07", "dette_pct_b2020_aout2026", "rev_2026_vs_b2014", "rev_2026_vs_2025"])
    w.writerows(dette)
print("dette, révisions > 0,2 pt :", [(r[0], r[4], r[5]) for r in dette if (r[4] != "" and abs(r[4]) > 0.2) or (r[5] != "" and abs(r[5]) > 0.2)])
# ---- base 2005 : t_3106.xls capturé le 16/04/2012 (Wayback) ----
import xlrd
b05 = xlrd.open_workbook(os.path.join(WB, "t_3106_base2005_cap2012-04.xls")).sheet_by_index(0)
ans05 = [int(x) for x in b05.row_values(2) if isinstance(x, float)]
col05 = {int(x): j for j, x in enumerate(b05.row_values(2)) if isinstance(x, float)}
def r05(i):
    return {a: b05.cell_value(i, j) for a, j in col05.items() if isinstance(b05.cell_value(i, j), float)}
S13_05, APUC_05, ETAT_05, ODAC_05, PCT_05 = r05(9), r05(4), r05(5), r05(6), r05(17)
b05_rows = []
for an in range(1959, 2011):
    b20 = SOL[("Figure 1", "Ensemble")].get(an)
    b20p = SOL[("Figure 2", "Ensemble")].get(an)
    b20_etat = SOL[("Figure 1", "État")].get(an)
    b20_odac = SOL[("Figure 1", "Organismes divers d'administration centrale")].get(an)
    b05_rows.append([an, S13_05.get(an), PCT_05.get(an) and round(PCT_05[an], 2), b20, b20p,
                     round(b20p - PCT_05[an], 2) if an in PCT_05 and b20p is not None else "",
                     round(ETAT_05[an] + ODAC_05[an] - APUC_05[an], 3) if (an in ETAT_05 and an in ODAC_05 and an in APUC_05) else "N.D. (État/ODAC non publiés)",
                     ETAT_05.get(an), ODAC_05.get(an), b20_etat, b20_odac])
with open(os.path.join(A01, "A01_revisions_base2005_vs_base2020.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "solde_S13_Md€_base2005", "solde_S13_pct_base2005", "solde_S13_Md€_base2020", "solde_S13_pct_base2020",
                "revision_pct_b2020_vs_b2005", "additivite_Etat+ODAC-APUC_base2005", "Etat_base2005", "ODAC_base2005", "Etat_base2020", "ODAC_base2020"])
    w.writerows(b05_rows)
print("base 2005 vs 2020, 1959-1982 (Md€ b2005 / b2020 | % b2005 / b2020 | additivité b2005) :")
for r in b05_rows:
    if r[0] <= 1982:
        print(r[0], r[1], r[3], "|", r[2], r[4], "|", r[6])
print("révisions solde > 0,2 pt b2020 vs b2005 :", [(r[0], r[5]) for r in b05_rows if r[5] != "" and abs(r[5]) > 0.2])
print("signes 1965-1982 (b2014 cap.2022 / b2014 cap.2020 / b2020) en Md€ :")
for l in lignes:
    if 1965 <= l[0] <= 1982:
        print(l[0], l[1], l[2], l[3], "| % :", l[4], l[6])
from collections import Counter
print(Counter(s[1] for s in sup))
