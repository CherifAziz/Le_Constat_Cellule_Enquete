# -*- coding: utf-8 -*-
"""A07 - Table annuelle France 1974-2025 et decomposition de la variation du ratio de dette.

Sources (lecture seule) :
  - commun/insee_cn_t_3201.xlsx : comptes S13 base 2020, Md EUR (D41 interets verses, B9, total depenses)
  - commun/insee_dep_rec_serie_longue.xlsx : depenses, recettes, dette brute en % du PIB
  - commun/insee_dette_par_sous_secteur.xlsx (Figure 1) : dette brute Maastricht Md EUR 1978-2025
  - A07/sources/eurostat_nama_10_gdp.csv : PIB nominal FR (CP_MEUR) 1975-2025, deflateur
  - A07/sources/oecd_finmark_A.csv : taux long (IRLT) et 3 mois (IR3TIB) FR, DE, IT
  - A07/sources/oecd_prices_A.csv : IPC (glissement annuel moyen)
Sortie : A07/table_france_1974_2025.csv et A07/decomposition_dette_periodes.csv

Convention : b = solde (B9, negatif = deficit) ; pb = b + interets ; d = dette/PIB.
Identite exacte (en ratio du PIB de l'annee t) :
   d_t - d_{t-1} = [(i_t - g_t)/(1+g_t)] d_{t-1}  - pb_t  + sfa_t
avec i_t = interets_t / dette_{t-1} (taux apparent), g_t = croissance nominale du PIB,
sfa_t = residu (ajustement stock-flux) = (dette_t - dette_{t-1} + B9_t) / PIB_t.
"""
import sys, os, csv, openpyxl

ROOT = sys.argv[1]  # ...\resultats\donnees
COM = os.path.join(ROOT, "commun")
A07 = os.path.join(ROOT, "A07")
SRC = os.path.join(A07, "sources")

def row_by_label(ws_rows, label_start, years_row=2):
    hdr = ws_rows[years_row]
    for r in ws_rows:
        lab = next((x for x in r[:3] if isinstance(x, str)), None)
        if lab and lab.strip().startswith(label_start):
            out = {}
            for h, v in zip(hdr, r):
                if isinstance(h, (int, float)) and isinstance(v, (int, float)):
                    out[int(h)] = float(v)
                elif isinstance(h, str) and h[:4].isdigit() and isinstance(v, (int, float)):
                    out[int(h[:4])] = float(v)  # annees marquees (sd) / (p)
            if out:
                return out
    raise KeyError(label_start)

wb = openpyxl.load_workbook(os.path.join(COM, "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
rows = list(wb.worksheets[0].iter_rows(values_only=True))
# recherche robuste : D41 depenses = premiere occurrence, D41 recettes = seconde
d41_rows = [r for r in rows if any(isinstance(x, str) and x.strip().startswith("Int") and "D41)" in x and "hors" not in x for x in r[:3])]
d41h_rows = [r for r in rows if any(isinstance(x, str) and x.strip().startswith("Int") and "hors correction" in x for x in r[:3])]
hdr = rows[2]
def todict(r):
    return {int(h): float(v) for h, v in zip(hdr, r) if isinstance(h, (int, float)) and isinstance(v, (int, float))}
INT_PAY = todict(d41_rows[0]); INT_REC = todict(d41_rows[1])
INT_PAY_HS = todict(d41h_rows[0])
TE = row_by_label(rows, "Total des d")
B9 = row_by_label(rows, "Capacit")

# series longues % PIB
wb2 = openpyxl.load_workbook(os.path.join(COM, "insee_dep_rec_serie_longue.xlsx"), read_only=True, data_only=True)
r2 = list(wb2.worksheets[0].iter_rows(values_only=True))
DEP_PCT = row_by_label(r2, "Dépenses", years_row=3)
REC_PCT = row_by_label(r2, "Recettes", years_row=3)
DET_PCT = row_by_label(r2, "Dette des administrations publiques (brute)", years_row=3)

# dette Md EUR (Figure 1, Ensemble)
DEBT = {}
for r in csv.reader(open(os.path.join(COM, "base_insee_dette_sous_secteurs.csv"), encoding="utf-8-sig"), delimiter=";"):
    if len(r) > 5 and r[1] == "Figure 1" and r[3] == "Ensemble":
        DEBT[int(r[4])] = float(r[5])

# PIB : Eurostat CP_MEUR (1975+) ; 1974 et controle : TE / depenses en % du PIB
GDP_EST, REAL, DEFL = {}, {}, {}
for r in csv.DictReader(open(os.path.join(SRC, "eurostat_nama_10_gdp.csv"), encoding="utf-8")):
    if r["geo"] == "FR" and r["unit"] == "CP_MNAC":
        GDP_EST[int(r["time"])] = float(r["value"]) / 1000.0
    if r["geo"] == "FR" and r["unit"] == "CLV_PCH_PRE":
        REAL[int(r["time"])] = float(r["value"])
GDP_IMPL = {y: TE[y] / DEP_PCT[y] * 100 for y in TE if y in DEP_PCT}
GDP = {y: GDP_IMPL[y] for y in GDP_IMPL}  # coherent avec la base Insee 2020 de la base commune
# deflateur implicite = (1+g nominal Eurostat CP_MNAC)/(1+g reel Eurostat CLV_PCH_PRE) - 1 (les deux en monnaie nationale)
for y in REAL:
    if y - 1 in GDP_EST:
        DEFL[y] = round(100 * ((GDP_EST[y] / GDP_EST[y - 1]) / (1 + REAL[y] / 100) - 1), 3)

OE = {}
for r in csv.DictReader(open(os.path.join(SRC, "oecd_finmark_A.csv"), encoding="utf-8-sig")):
    OE[(r["REF_AREA"], r["MEASURE"], int(r["TIME_PERIOD"]))] = float(r["OBS_VALUE"])
CPI = {}
for r in csv.DictReader(open(os.path.join(SRC, "oecd_prices_A.csv"), encoding="utf-8-sig")):
    CPI[(r["REF_AREA"], int(r["TIME_PERIOD"]))] = float(r["OBS_VALUE"])

out = []
for y in range(1974, 2026):
    g = GDP[y] / GDP[y - 1] - 1 if y - 1 in GDP else None
    pb = B9[y] + INT_PAY[y]
    row = dict(annee=y, pib_mdeur=round(GDP[y], 3), pib_eurostat_mdeur=round(GDP_EST.get(y, float("nan")), 3),
               croiss_nominale_pct=round(100 * g, 3) if g is not None else "",
               croiss_reelle_pct=REAL.get(y, ""), deflateur_pib_pct=DEFL.get(y, ""), ipc_ocde_pct=CPI.get(("FRA", y), ""),
               taux10_FR=OE.get(("FRA", "IRLT", y), ""), taux10_DE=OE.get(("DEU", "IRLT", y), ""),
               taux10_IT=OE.get(("ITA", "IRLT", y), ""), taux3m_FR=OE.get(("FRA", "IR3TIB", y), ""),
               depenses_pct=round(DEP_PCT[y], 3), recettes_pct=round(REC_PCT[y], 3),
               solde_mdeur=round(B9[y], 3), solde_pct=round(100 * B9[y] / GDP[y], 3),
               interets_verses_mdeur=round(INT_PAY[y], 3), interets_verses_hors_sifim_mdeur=round(INT_PAY_HS.get(y, float('nan')), 3),
               interets_recus_mdeur=round(INT_REC.get(y, float('nan')), 3),
               interets_pct=round(100 * INT_PAY[y] / GDP[y], 3),
               interets_pct_recettes=round(100 * INT_PAY[y] / (REC_PCT[y] * GDP[y] / 100), 3),
               solde_primaire_mdeur=round(pb, 3), solde_primaire_pct=round(100 * pb / GDP[y], 3),
               dette_mdeur=DEBT.get(y, ""), dette_pct=round(DET_PCT[y], 3) if y in DET_PCT else "")
    if y in DEBT and y - 1 in DEBT:
        i = INT_PAY[y] / DEBT[y - 1]
        d0 = DEBT[y - 1] / GDP[y - 1]; d1 = DEBT[y] / GDP[y]
        snow = (i - g) / (1 + g) * d0
        sfa = (DEBT[y] - DEBT[y - 1] + B9[y]) / GDP[y]
        row.update(taux_apparent_pct=round(100 * i, 3), ecart_i_moins_g_pts=round(100 * (i - g), 3),
                   taux_reel_apparent_pct=round(100 * ((1 + i) / (1 + DEFL[y] / 100) - 1), 3) if y in DEFL else "",
                   var_ratio_pts=round(100 * (d1 - d0), 3), contrib_boule_de_neige_pts=round(100 * snow, 3),
                   contrib_solde_primaire_pts=round(-100 * pb / GDP[y], 3), contrib_sfa_pts=round(100 * sfa, 3),
                   contrib_interets_pts=round(100 * i / (1 + g) * d0, 3),
                   contrib_croissance_pts=round(-100 * g / (1 + g) * d0, 3),
                   ratio_dette_calc_pct=round(100 * d1, 3))
    out.append(row)

keys = []
for r in out:
    for k in r:
        if k not in keys:
            keys.append(k)
with open(os.path.join(A07, "table_france_1974_2025.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=keys, delimiter=";"); w.writeheader(); w.writerows(out)

# Decomposition par sous-periodes (sommes des contributions annuelles)
PER = [(1979, 1983), (1984, 1990), (1991, 1993), (1994, 1997), (1998, 2001), (2002, 2007), (2008, 2009), (2010, 2014),
       (2015, 2019), (2020, 2020), (2021, 2023), (2024, 2025), (1979, 2025), (1979, 1998), (1999, 2025), (2015, 2021)]
by = {r["annee"]: r for r in out}
res = []
for a, b in PER:
    ys = [y for y in range(a, b + 1) if "var_ratio_pts" in by[y]]
    s = lambda k: round(sum(by[y][k] for y in ys), 2)
    res.append(dict(periode=f"{a}-{b}", annees=len(ys), dette_debut_pct=round(100 * DEBT[a - 1] / GDP[a - 1], 2),
                    dette_fin_pct=round(100 * DEBT[b] / GDP[b], 2), var_ratio=s("var_ratio_pts"),
                    solde_primaire=s("contrib_solde_primaire_pts"), boule_de_neige=s("contrib_boule_de_neige_pts"),
                    dont_interets=s("contrib_interets_pts"), dont_croissance=s("contrib_croissance_pts"),
                    stock_flux=s("contrib_sfa_pts"),
                    i_moyen=round(sum(by[y]["taux_apparent_pct"] for y in ys) / len(ys), 2),
                    g_moyen=round(sum(by[y]["croiss_nominale_pct"] for y in ys) / len(ys), 2)))
with open(os.path.join(A07, "decomposition_dette_periodes.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(res[0]), delimiter=";"); w.writeheader(); w.writerows(res)
for r in res:
    print(r)
print("controle PIB 2025 implicite vs Eurostat :", round(GDP[2025], 1), round(GDP_EST[2025], 1))
print("controle dette % 2025 calc vs Insee :", by[2025].get("ratio_dette_calc_pct"), by[2025]["dette_pct"])
