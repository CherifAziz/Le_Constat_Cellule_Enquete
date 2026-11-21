# -*- coding: utf-8 -*-
"""A07 - Calculs complementaires (reproduction des resultats cites dans A07.md, sections 3, 5, 6, 11, 12).
Usage : python -I 08_calculs_complementaires.py <dossier donnees>
Entrees : A07/table_france_1974_2025.csv (script 03), A07/comparaisons_pays_1995_2025.csv (script 05),
          A07/sources/* (Eurostat irt_lt_mcby_m, gov_10dd_ggd ; BCE PSPP/PEPP ; BCE IRS),
          commun/base_insee_solde_sous_secteurs.csv, commun/base_insee_dette_sous_secteurs.csv (lecture seule).
Sorties (A07/) :
  c03_arithmetique_interets.csv     : interets cumules, contrefactuels "interet nul" et "i = g"     (C-A07-003)
  c09_inflation_prix_volume.csv     : effet prix / volume sur le ratio 2021-2024                      (C-A07-009)
  c05_fenetre_2015_2019.csv         : economies d'interets 2015-2019, solde primaire moyen par pays   (C-A07-005/006)
  c01_moyennes_periodes.csv         : moyennes par periode (taux, inflation, taux reel apparent)        (F-A07-007)
  c11_ecarts_suede.csv              : ecarts SE-DE et FR-DE annuels 1987-1999                         (F-A07-041)
  c12_detenteurs_eurostat.csv       : dette des APU par secteur detenteur                              (F-A07-042)
  c13_eurosysteme_pays.csv          : portefeuille PSPP+PEPP par pays : pic, oct. 2026, variation       (R8)
  c14_stock_flux_sous_secteurs.csv  : residu stock-flux par sous-secteur 1979-2025 (dette + solde)      (§13)
  c15_contrefactuel_primaire_nul.csv: 2015-2019, ratio avec solde primaire nul                         (C-A07-006)
"""
import sys, os, csv, collections, datetime
D = sys.argv[1]; A = os.path.join(D, "A07"); S = os.path.join(A, "sources"); C = os.path.join(D, "commun")

def wcsv(name, rows):
    with open(os.path.join(A, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter=";"); w.writeheader(); w.writerows(rows)
    print("ecrit", name, len(rows))

T = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(A, "table_france_1974_2025.csv"), encoding="utf-8"), delimiter=";")}
f = lambda y, k: float(T[y][k])

# C-A07-003 arithmetique "interet nul" et "i = g"
rows = []
for a in (1974, 1979, 1999):
    rows.append(dict(depuis=a, interets_bruts_cumul_mdeur=round(sum(f(y, "interets_verses_mdeur") for y in range(a, 2026)), 1),
                     interets_nets_cumul_mdeur=round(sum(f(y, "interets_verses_mdeur") - f(y, "interets_recus_mdeur") for y in range(a, 2026)), 1),
                     solde_primaire_cumul_mdeur=round(sum(f(y, "solde_primaire_mdeur") for y in range(a, 2026)), 1),
                     solde_cumul_mdeur=round(sum(f(y, "solde_mdeur") for y in range(a, 2026)), 1)))
Dd = f(1978, "dette_mdeur"); sfa_cum = 0.0
for y in range(1979, 2026):
    sfa = f(y, "dette_mdeur") - f(y - 1, "dette_mdeur") + f(y, "solde_mdeur"); sfa_cum += sfa
    Dd = Dd - f(y, "solde_primaire_mdeur") + sfa
d_ig = 100 * f(1978, "dette_mdeur") / f(1978, "pib_mdeur") + sum(f(y, "contrib_solde_primaire_pts") + f(y, "contrib_sfa_pts") for y in range(1979, 2026))
rows.append(dict(depuis="contrefactuels 1979-2025", interets_bruts_cumul_mdeur=f"dette 2025 interet nul = {Dd:.0f} Md EUR ({100*Dd/f(2025,'pib_mdeur'):.1f} % PIB)",
                 interets_nets_cumul_mdeur=f"ratio 2025 si i=g chaque annee = {d_ig:.1f} % PIB",
                 solde_primaire_cumul_mdeur=f"stock-flux cumule = {sfa_cum:.0f} Md EUR", solde_cumul_mdeur=f"dette 1978 = {f(1978,'dette_mdeur')} ; 2025 = {f(2025,'dette_mdeur')}"))
wcsv("c03_arithmetique_interets.csv", rows)

# C-A07-009 prix / volume
rows = []
for y in range(2021, 2025):
    d0 = f(y - 1, "dette_mdeur") / f(y - 1, "pib_mdeur"); g = f(y, "croiss_nominale_pct") / 100; gr = f(y, "croiss_reelle_pct") / 100
    p = (1 + g) / (1 + gr) - 1
    rows.append(dict(annee=y, deflateur_pct=round(100 * p, 2), effet_prix_pts=round(-100 * d0 * p / (1 + g), 2),
                     effet_volume_pts=round(-100 * d0 * gr * (1 + p) / (1 + g), 2), interets_mdeur=T[y]["interets_verses_mdeur"], taux_apparent_pct=T[y]["taux_apparent_pct"]))
wcsv("c09_inflation_prix_volume.csv", rows)

# C-A07-005 fenetre 2015-2019
R = {(r["geo"], int(r["annee"])): r for r in csv.DictReader(open(os.path.join(A, "comparaisons_pays_1995_2025.csv"), encoding="utf-8"), delimiter=";")}
rows = []
for geo in ["FR", "DE", "IT", "ES", "BE", "PT", "NL", "AT", "SE", "EA20"]:
    g_ = lambda y, k: float(R[(geo, y)][k])
    i14 = g_(2014, "taux_apparent_pct") / 100
    e = sum((i14 - g_(y, "taux_apparent_pct") / 100) * g_(y - 1, "dette_mio") for y in range(2015, 2020)) / 1000
    ep = sum((i14 - g_(y, "taux_apparent_pct") / 100) * g_(y - 1, "dette_mio") / g_(y, "pib_mio") * 100 for y in range(2015, 2020))
    rows.append(dict(geo=geo, economie_2015_2019_md=round(e, 1), economie_pts_pib=round(ep, 2),
                     solde_primaire_moyen_2015_2019=round(sum(g_(y, "solde_primaire_pct") for y in range(2015, 2020)) / 5, 2),
                     dette_2014=g_(2014, "dette_pct"), dette_2019=g_(2019, "dette_pct"), dette_2025=g_(2025, "dette_pct")))
wcsv("c05_fenetre_2015_2019.csv", rows)

# C-A07-006 contrefactuel solde primaire nul 2015-2019 (France, statique)
snow = sum(f(y, "contrib_boule_de_neige_pts") for y in range(2015, 2020)); sf = sum(f(y, "contrib_sfa_pts") for y in range(2015, 2020))
prim = sum(f(y, "contrib_solde_primaire_pts") for y in range(2015, 2020))
wcsv("c15_contrefactuel_primaire_nul.csv", [dict(var_observee=round(snow + sf + prim, 2), contrib_primaire=round(prim, 2), boule_de_neige=round(snow, 2), stock_flux=round(sf, 2),
      var_si_primaire_nul_avec_sfa=round(snow + sf, 2), var_si_primaire_nul_hors_sfa=round(snow, 2),
      deficit_primaire_stabilisant_moyen_pct=round(snow / 5, 2))])

# F-A07-007 moyennes par periode
rows = []
for a, b in [(1974, 1978), (1979, 1983), (1984, 1990), (1991, 1993), (1994, 1997), (1998, 2001), (2002, 2007), (2008, 2009), (2010, 2014), (2015, 2019), (2020, 2020), (2021, 2023), (2024, 2025)]:
    def avg(k):
        v = [float(T[y][k]) for y in range(a, b + 1) if T[y].get(k) not in ("", None)]
        return round(sum(v) / len(v), 2) if v else ""
    rows.append(dict(periode=f"{a}-{b}", g_nominal=avg("croiss_nominale_pct"), g_reel=avg("croiss_reelle_pct"), deflateur=avg("deflateur_pib_pct"),
                     ipc=avg("ipc_ocde_pct"), taux10_FR=avg("taux10_FR"), taux10_DE=avg("taux10_DE"), taux3m_FR=avg("taux3m_FR"),
                     taux_apparent=avg("taux_apparent_pct"), taux_reel_apparent=avg("taux_reel_apparent_pct"),
                     interets_pct_pib=avg("interets_pct"), interets_pct_recettes=avg("interets_pct_recettes"), solde_primaire_pct=avg("solde_primaire_pct")))
wcsv("c01_moyennes_periodes.csv", rows)

# F-A07-041 Suede
m = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(S, "eurostat_irt_lt_mcby_m.csv"), encoding="utf-8")):
    m[r["time"]][r["geo"]] = float(r["value"])
rows = []
for y in range(1987, 2000):
    ms = [k for k in m if k.startswith(str(y)) and all(g in m[k] for g in ("SE", "DE", "FR"))]
    if ms:
        av = lambda g: sum(m[k][g] for k in ms) / len(ms)
        rows.append(dict(annee=y, SE=round(av("SE"), 2), DE=round(av("DE"), 2), FR=round(av("FR"), 2), SE_DE_pb=round(100 * (av("SE") - av("DE"))), FR_DE_pb=round(100 * (av("FR") - av("DE")))))
wcsv("c11_ecarts_suede.csv", rows)

# F-A07-042 detenteurs Eurostat
G = {}
for r in csv.DictReader(open(os.path.join(S, "eurostat_gov_10dd_ggd.csv"), encoding="utf-8")):
    if r["maturity"] == "TOTAL":
        G[(r["geo"], r["sector2"], int(r["time"]))] = float(r["value"])
rows = []
for (geo, sec, y), v in sorted(G.items()):
    if sec == "S1_S2":
        rows.append(dict(geo=geo, annee=y, total_pct_pib=v, banque_centrale=G.get((geo, "S121", y), ""), banques=G.get((geo, "S122_S123", y), ""),
                         autres_fin=G.get((geo, "S124-S129", y), ""), menages=G.get((geo, "S14_S15", y), ""), reste_du_monde=G.get((geo, "S2", y), ""),
                         part_reste_du_monde_pct=round(100 * G.get((geo, "S2", y), 0) / v, 1), part_bc_pct=round(100 * (G.get((geo, "S121", y)) or 0) / v, 1)))
wcsv("c12_detenteurs_eurostat.csv", rows)

# R8 Eurosysteme par pays (PSPP + PEPP), pic et octobre 2026 ; ecart a 10 ans contre DE au pic et en oct. 2026
def first_block(path, country):
    rr = list(csv.reader(open(path, encoding="utf-8-sig"))); hdr = rr[2]
    for r in rr[3:]:
        if r and r[0] == country:
            out = {}
            for h, v in zip(hdr[1:], r[1:]):
                if not h or "umulative" in h:
                    continue
                for fmt in ("%d/%m/%Y", "%b-%y"):
                    try:
                        d = datetime.datetime.strptime(h, fmt); out[f"{d.year}-{d.month:02d}"] = float(v.replace(",", "")) if v else 0.0; break
                    except ValueError:
                        pass
            return out
IRS = collections.defaultdict(dict)
for g in ["FR", "DE", "IT", "ES", "BE"]:
    for r in csv.DictReader(open(os.path.join(S, f"ecb_IRS_M_{g}.csv"), encoding="utf-8")):
        if r["OBS_VALUE"]:
            IRS[r["TIME_PERIOD"]][g] = float(r["OBS_VALUE"])
rows = []
for name, g in [("France", "FR"), ("Germany", "DE"), ("Italy", "IT"), ("Spain", "ES"), ("Belgium", "BE")]:
    p1 = first_block(os.path.join(S, "ecb_PSPP_breakdown_history.csv"), name); p2 = first_block(os.path.join(S, "ecb_PEPP_public_sector_breakdown_history.csv"), name)
    cum = 0.0; series = []
    for k in sorted(set(p1) | set(p2)):
        cum += p1.get(k, 0.0) + p2.get(k, 0.0); series.append((k, cum / 1000))
    pk = max(series, key=lambda x: x[1]); last = series[-1]
    gdp25 = float(R[(g, 2025)]["pib_mio"]) / 1000
    sp = lambda mo: round(100 * (IRS[mo][g] - IRS[mo]["DE"])) if g != "DE" else ""
    rows.append(dict(pays=g, pic_mois=pk[0], pic_mdeur=round(pk[1], 1), oct2026_mdeur=round(last[1], 1), variation_mdeur=round(last[1] - pk[1], 1),
                     variation_pct_du_pic=round(100 * (last[1] - pk[1]) / pk[1], 1), variation_pts_pib2025=round(100 * (last[1] - pk[1]) / gdp25, 1),
                     ecart_DE_pb_au_pic=sp(pk[0]), ecart_DE_pb_mai2024=sp("2024-05"), ecart_DE_pb_oct2026=sp(last[0])))
wcsv("c13_eurosysteme_pays.csv", rows)

# §13 residu stock-flux par sous-secteur (Insee, Md EUR) : sfa = dette_t - dette_{t-1} + solde_t
Sd = collections.defaultdict(dict); Dt = collections.defaultdict(dict)
for r in csv.reader(open(os.path.join(C, "base_insee_solde_sous_secteurs.csv"), encoding="utf-8-sig"), delimiter=";"):
    if len(r) > 5 and r[1] == "Figure 1":
        Sd[r[3]][int(r[4])] = float(r[5])
for r in csv.reader(open(os.path.join(C, "base_insee_dette_sous_secteurs.csv"), encoding="utf-8-sig"), delimiter=";"):
    if len(r) > 5 and r[1] == "Figure 1":
        Dt[r[3]][int(r[4])] = float(r[5])
rows = []
secs = ["État", "Organismes divers d'administration centrale", "Administrations publiques locales", "Administrations de sécurité sociale", "Ensemble"]
for a, b in [(1979, 1983), (1984, 1990), (1991, 1998), (1999, 2007), (2008, 2009), (2010, 2019), (2020, 2020), (2021, 2025), (1979, 2025)]:
    row = dict(periode=f"{a}-{b}")
    for s_ in secs:
        try:
            row[s_] = round(sum(Dt[s_][y] - Dt[s_][y - 1] + Sd[s_][y] for y in range(a, b + 1)), 1)
        except KeyError:
            row[s_] = ""
    rows.append(row)
wcsv("c14_stock_flux_sous_secteurs.csv", rows)
for r in rows:
    print(r)
