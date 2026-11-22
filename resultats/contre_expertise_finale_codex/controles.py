"""Recalcul indépendant sur les blobs épinglés. Usage détaillé dans le README."""
import argparse
import csv
import io
import json
import math
from pathlib import Path
from statistics import median
import subprocess

from openpyxl import load_workbook

PIN = "ffb03b64268b8012c0d54b4c8747bf64c1ca5b14"
ROOT = Path(__file__).resolve().parents[2]
CLAUDE = "resultats/claude_approfondissements/donnees/"
BASE = "Le_Constat_Cellule_Enquete/resultats/donnees/"
CODEX = "resultats/codex/donnees/"


def blob(path):
    return subprocess.check_output(["git", "show", f"{PIN}:{path}"], cwd=ROOT)


def rows(path):
    return list(csv.DictReader(io.StringIO(blob(path).decode("utf-8-sig")), delimiter=";"))


def sheet(path, name=None):
    wb = load_workbook(io.BytesIO(blob(path)), read_only=True, data_only=True)
    try:
        return list((wb[name] if name else wb.worksheets[0]).values)
    finally:
        wb.close()


def series(table, header, row):
    return {int(str(k).strip()): v for k, v in zip(table[header], row)
            if str(k).strip().isdigit() and isinstance(v, (int, float))}


def named(table, header, prefix, col=1):
    row = next(row for row in table if str(row[col]).strip().startswith(prefix))
    return series(table, header, row)


def pct(a, b):
    return 100 * (a / b - 1)


def annual(a, b, n):
    return 100 * ((b / a) ** (1 / n) - 1)


def check(value, reference, tolerance):
    if abs(value - float(reference)) > tolerance + 1e-10:
        raise ValueError(f"Écart hors tolérance : {value} / {reference}")


t = sheet(BASE + "commun/insee_cn_t_3201.xlsx")
spend = named(t, 2, "Total des dépenses")
receipts = named(t, 2, "Total des recettes")
balance = named(t, 2, "Capacité (+) ou besoin")
interest = named(t, 2, "Intérêts (D41)")
accounts = rows(BASE + "A04/a04_po_recettes_1959_2025.csv")
gdp = {int(r["annee"]): float(r["PIB_implicite_Md_EUR"]) for r in accounts}
po = {int(r["annee"]): float(r["PO_pctPIB"]) for r in accounts}
debt = {int(r["annee"]): float(r["valeur"]) for r in rows(BASE + "commun/base_insee_dette_sous_secteurs.csv")
        if r["feuille"] == "Figure 1" and r["serie"] == "Ensemble"}
observed = {y: 100 * v / gdp[y] for y, v in balance.items() if y in gdp}
inputs = [r for r in rows(CLAUDE + "D05/D05_mesures_nouvelles_annuelles.csv") if r["retenu"] == "oui"]
measures = {int(r["annee"]): float((r["mesures_pts_PIB_base2020"] or r["mesures_pts_PIB_source"]).replace(",", "."))
            for r in inputs}
assert len(inputs) == len(measures) == 26 and set(measures) == set(range(2000, 2026))


def budget(start, y2010, treatment, nominal=False):
    m = dict(measures)
    m[2010] = y2010
    if treatment == "D08-neutralise":
        m[2019] += 100 * 20.2 / gdp[2019]
    if treatment == "Cour-trois-flux":
        for y, signed_bn in {2019: -20.1, 2020: 14.4, 2021: 0.5}.items():
            m[y] -= 100 * signed_bn / gdp[y]
    gain = {}
    rates = {y: interest[y] / debt[y - 1] for y in range(start, 2026)}
    path = {}
    for y in rates:
        # Somme directe des impulsions et capitalisation de chaque flux passé.
        gain[y] = -sum(m[k] * (gdp[k] if nominal else gdp[y]) / 100 for k in range(start, y + 1))
        stock_open = sum(gain[k] * math.prod(1 + rates[j] for j in range(k + 1, y))
                         for k in range(start, y))
        static = observed[y] + 100 * gain[y] / gdp[y]
        with_interest = static + 100 * rates[y] * stock_open / gdp[y]
        stock_close = (1 + rates[y]) * stock_open + gain[y]
        path[y] = (static, with_interest, 100 * (debt[y] - stock_close) / gdp[y], -100 * gain[y] / gdp[y])
    static, with_interest, debt_cf, cumulative = path[2025]
    return path, dict(depart=start, annee2010=y2010, cice=treatment, report="euros" if nominal else "points",
                      cumul=cumulative, residu_PO=po[2025] - po[start - 1] - cumulative,
                      solde=static, solde_interets=with_interest, dette_interets=debt_cf,
                      annees_solde_positif=[y for y, v in path.items() if v[0] >= 0],
                      annees_positives_interets=[y for y, v in path.items() if v[1] >= 0],
                      annees_cumul_positif=[y for y, v in path.items() if v[3] > 1e-9])


def fiscal():
    scenarios = []
    annual_reference = rows(CLAUDE + "D08/D08_persistance_fiscale_annuel.csv")
    matched = 0
    for start in (2000, 2003, 2007, 2012, 2017, 2018):
        for high, y2010 in ((True, measures[2010]), (False, -0.4)):
            for treat in ("publie", "D08-neutralise", "Cour-trois-flux"):
                path, result = budget(start, y2010, treat)
                scenarios.append(result)
                if treat == "Cour-trois-flux":
                    continue
                selected = [r for r in annual_reference if int(r["annee_de_depart"]) == start
                            and r["variante_2010"].endswith("automne") == high
                            and r["variante_bascule"].endswith("comptee") == (treat == "publie")]
                assert len(selected) == len(path)
                for r in selected:
                    vals = path[int(r["annee"])]
                    for v, key, tolerance in zip(vals, ("solde_sans_mesures_statique_pct",
                            "solde_sans_mesures_avec_interets_pct", "dette_sans_mesures_pct", "cumul_mesures_pts"),
                            (.005, .005, .05, .005)):
                        check(v, r[key], tolerance)
                    matched += 1
    scenarios.append(budget(2000, measures[2010], "Cour-trois-flux", nominal=True)[1])
    return dict(annees_scenarios_verifiees=matched, impulsions=measures, scenarios=scenarios)


def history():
    raw = sheet(CODEX + "T_1101_1103_fr.xlsx", "T_1102 en niveau")
    volume = named(raw, 3, "B1GQ", 0)
    real = {y: spend[y] * volume[y] / gdp[y] for y in gdp if y in spend and y in volume}
    n = 11
    obs = 100 * spend[1985] / gdp[1985]
    base_ratio = 100 * spend[1974] / gdp[1974]
    out = []
    ref = rows(CLAUDE + "D01/D01_conventions_carre_2x2.csv")
    for start in (1960, 1965, 1968):
        gv = (volume[1973] / volume[start]) ** (1 / (1973 - start))
        gs = (real[1973] / real[start]) ** (1 / (1973 - start))
        va, sa = volume[1974] * gv ** n, real[1974] * gs ** n
        b, c, both = 100 * real[1985] / va, 100 * sa / volume[1985], 100 * sa / va
        # Partage symétrique des deux ordres de substitution à la tendance jointe.
        gd = ((obs - b) + (c - both)) / 2
        sd = ((obs - c) + (b - both)) / 2
        drift = both - base_ratio
        check(gd + sd + drift, obs - base_ratio, 1e-9)
        entry = dict(debut_ref=start, croissance_volume=100 * (gv - 1), croissance_dep=100 * (gs - 1),
                     part_PIB_seule=100 * (obs - b) / (obs - base_ratio), dep_seule=obs - c,
                     derive=drift, allocation_PIB=gd, allocation_dep=sd)
        if start != 1965:
            r = next(r for r in ref if r["agregat"] == "DEP" and r["horizon"] == "1985"
                     and r["fenetre_reference"].startswith(str(start)))
            for v,k in ((b,"r_b_PIB_tendance_depense_obs"),(c,"r_c_PIB_obs_depense_tendance_agregat"),
                        (both,"r_tendance_PIB_et_depense")):
                check(v, r[k], .00005)
        out.append(entry)
    return dict(reference=out, dep_observee=annual(real[1974], real[1985], n),
                PIB_observe=annual(volume[1974], volume[1985], n), variation_dep=obs-base_ratio,
                variation_rec=100 * (receipts[1985]/gdp[1985] - receipts[1974]/gdp[1974]),
                regimes_1980=dict(RG_net_MdF=10.669-9.352, part_RG=100*9.352/10.669,
                                  RG_pt=100*9.352/(gdp[1980]*6.55957),
                                  tous_annonce_pts=100*10/(gdp[1980]*6.55957)),
                soldes={y:observed[y] for y in (1970,1974,1975,1979,1980,1981,1985,1999,2000,2001,2002,2025)},
                deficits_avant_1975=[y for y in range(1960,1975) if observed[y]<0],
                soldes_primaires={y:100*(balance[y]+interest[y])/gdp[y] for y in (1979,1980,2000,2025)},
                deficits_1975_2025=sum(observed[y] < 0 for y in range(1975,2026)))


def labour():
    ameco = {r["CODE"]: r for r in rows(CLAUDE + "D06/sources/ameco_extrait_D06.csv")}
    def hours(country, y):
        def get(code):
            return float(ameco[f"{country}.1.0.0.0.{code}"][str(y)])
        return 1000 * get("NLHT") / get("NPAN")
    panel = ["DEU", "ITA", "ESP", "NLD", "SWE", "GBR", "USA"]
    ratios = []
    factor = hours("DEU",1991) / hours("D_W",1991)
    src = rows(CLAUDE + "D08/D08_heures_france_mediane.csv")
    for r in src:
        y = int(r["annee"])
        peers = {p: (hours("D_W",y)*factor if p=="DEU" and y<1991 else hours(p,y)) for p in panel}
        france = hours("FRA",y)
        m = median(peers.values())
        check(france,r["heures_France"],.051)
        check(m,r["mediane_autres"],.051)
        changes = {p:pct(france,median(v for k,v in peers.items() if k != p)) for p in peers}
        ratios.append(dict(annee=y, France=france, mediane=m, rang_croissant=1+sum(v < france for v in peers.values()), ecart=pct(france,m),
                           rattrapage=pct(m,france), sans_un_pays=changes))
    gap = ratios[-1]["rattrapage"]/100
    assert ratios[-1]["annee"] == 2025
    s = observed[2025]/100
    grid = []
    for h in (.01, .122, gap):
        for rho in (.46, 1):
            for tau in (.35, .459):
                for eco in (0, .2):
                    x = h*rho
                    grid.append(dict(heures_pct=100*h,rho=rho,tau=tau,eco=eco,
                                     gain_solde=100*x*(tau+eco-s)/(1+x)))
    etp = named(sheet(CODEX+"T_1109_fr.xlsx","T_1109 en niveau"),3,"S13",0)
    wages = named(sheet(CLAUDE+"D08/sources/T_1107_fr.xlsx","T_1107 en niveau"),3,"D11",0)
    social = named(t,2,"Cotisations sociales nettes (D61)")
    imputed = named(t,2,"dont (a) - Cotisations sociales imputées (D612)")
    bcl = sheet(CLAUDE + "D06/sources/BCLDatabase_online_v2.7.xlsx", "Labor Productivity")
    productivity = {}
    for a, b, c in ((1960,1973,1990), (1973,1990,2007), (1990,2007,2019), (2007,2019,2024)):
        change = {}
        for p in ["FRA"] + panel:
            col = bcl[0].index(p)
            data = {int(r[0]):r[col] for r in bcl[1:] if r[0] is not None}
            change[p] = 100*(math.log(data[c]/data[b])/(c-b) - math.log(data[b]/data[a])/(b-a))
        productivity[f"{a}/{b}/{c}"] = change["FRA"]-median(change[p] for p in panel)
    survey = sheet(CLAUDE + "D07/sources/insee_EEC_T207_2025.xlsx")
    seniors = {}
    for group in ("De 55 à 59 ans", "De 60 à 64 ans"):
        r = next(r for r in survey if r[0] == "Total" and str(r[1]).strip() == group)
        values = series(survey, 3, r)
        low = min(values, key=values.get)
        seniors[group] = {y:values[y] for y in (1975,low,2025)}
    return dict(heures=ratios, coefficient_raccord=factor, grille=grid, productivite_BCL=productivity, emploi_seniors=seniors,
                productivite_5pct_gain={str(phi):100*spend[2025]/gdp[2025]*(1-phi)*.05/1.05
                                       for phi in (1,.8,.5)},
                ETP_S13={y:etp[y] for y in (1980,1985)}, croissance_ETP=annual(etp[1980],etp[1985],5),
                cotisations_sur_D11={y:100*(social[y]-imputed[y])/wages[y] for y in (1993,1996,2018,2019,2025)})


def rounded(obj):
    if isinstance(obj, dict):
        return {k:rounded(v) for k,v in obj.items()}
    if isinstance(obj, list):
        return [rounded(v) for v in obj]
    return round(obj, 6) if isinstance(obj, float) else obj


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", action="store_true", help="Comparer au résultat versionné, sans écriture")
    args = parser.parse_args()
    transcriptions = dict(
        bareme_1980_premier_seuil=pct(17450,15850), bareme_1980_dernier_seuil=pct(250100,250100),
        nationalisations_1983_MdF=2+5.618, croissance_DGAFP_avec_PT=annual(4601.8,4969.4,5),
        croissance_DGAFP_hors_PT=annual(4119.8,4455.4,5), part_FPT_FPH=100*(133.2+85.3)/367.6)
    result = rounded(dict(commit_sources=PIN, fiscal=fiscal(), histoire=history(), travail=labour(), transcriptions=transcriptions))
    if args.verifier:
        expected = json.loads(Path(__file__).with_name("resultats.json").read_text(encoding="utf-8"))
        assert json.loads(json.dumps(result)) == expected, "Résultats différents de la copie versionnée"
        print("Résultats identiques à la copie versionnée.")
    else:
        print(json.dumps(result, ensure_ascii=True, indent=2, allow_nan=False))
