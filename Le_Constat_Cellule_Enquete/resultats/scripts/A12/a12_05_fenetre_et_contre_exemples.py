"""A12 - (a) fenetre 2015-2019 comparee (question d'A07) ; (b) table des contre-exemples
(niveau de depense contre solde, 1995-2025 et 2015-2019).

Entrees : OCDE EO 119 (oecd_eo119_finpub.csv, oecd_eo119_macro.csv, oecd_eo119_interets.csv) ; AMECO (dette UDGGL).
Sorties : donnees\\A12\\A12_fenetre_2015_2019.csv ; donnees\\A12\\A12_contre_exemples_depense_solde.csv
Identite (par annee) : d_t - d_{t-1} = -(solde_t + interets_t) + interets_t - g_t/(1+g_t) d_{t-1} + residu_t
  (solde, interets bruts en % du PIB de t ; g croissance du PIB nominal ; d dette Maastricht AMECO)
Usage : python -I a12_05_fenetre_et_contre_exemples.py
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a12_02_episodes as ep

OUT = ep.OUT
PAYS_F = ["FRA", "DEU", "ITA", "ESP", "BEL", "PRT", "NLD", "AUT", "SWE", "FIN", "DNK", "GBR", "IRL", "GRC"]


def main():
    d = ep.charger()
    g = lambda p, m, a: d.get((p, m), {}).get(a)
    rows = []
    for p in PAYS_F:
        dec = {"primaire": 0.0, "interets": 0.0, "croissance": 0.0}
        prims = []
        ok = True
        for y in range(2015, 2020):
            nl, itv, dprev, g1, g0 = g(p, "NLGQ", y), g(p, "GGINTP", y), g(p, "AMECO_UDGGL", y - 1), g(p, "GDP", y), g(p, "GDP", y - 1)
            if None in (nl, itv, dprev, g1, g0):
                ok = False; break
            it = 100 * itv / g1; gr = g1 / g0 - 1
            dec["primaire"] += -(nl + it); dec["interets"] += it; dec["croissance"] += -gr / (1 + gr) * dprev
            prims.append(nl + it)
        if not ok:
            continue
        d14, d19 = g(p, "AMECO_UDGGL", 2014), g(p, "AMECO_UDGGL", 2019)
        res = (d19 - d14) - sum(dec.values())
        rows.append({"pays": p, "dette_2014": round(d14, 1), "dette_2019": round(d19, 1), "variation": round(d19 - d14, 1),
                     "solde_primaire_moyen_2015_2019_(interets_bruts)": round(sum(prims) / 5, 2),
                     "primaire_2014": round(g(p, "NLGQ", 2014) + 100 * g(p, "GGINTP", 2014) / g(p, "GDP", 2014), 2),
                     "primaire_2019": round(prims[-1], 2),
                     "contrib_primaire": round(dec["primaire"], 1), "contrib_interets": round(dec["interets"], 1),
                     "contrib_croissance_nominale": round(dec["croissance"], 1), "residu": round(res, 1),
                     "croissance_nominale_moy": round(100 * ((g(p, "GDP", 2019) / g(p, "GDP", 2014)) ** 0.2 - 1), 2),
                     "depense_moy_2015_2019": round(sum(g(p, "YPGTQ", y) for y in range(2015, 2020)) / 5, 1)})
    with open(os.path.join(OUT, "A12_fenetre_2015_2019.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()), delimiter=";"); w.writeheader(); w.writerows(rows)
    # Contre-exemples : moyennes 1995-2025 de la depense (YPGTQ), des recettes (YRGTQ), du solde (NLGQ)
    pays = sorted({p for (p, m) in d if m == "YPGTQ"})
    ce = []
    for p in pays:
        an = [a for a in range(1995, 2026) if g(p, "YPGTQ", a) is not None and g(p, "NLGQ", a) is not None and g(p, "YRGTQ", a) is not None]
        if len(an) < 25 or len(p) != 3:
            continue
        dep = sum(g(p, "YPGTQ", a) for a in an) / len(an); rec = sum(g(p, "YRGTQ", a) for a in an) / len(an)
        sol = sum(g(p, "NLGQ", a) for a in an) / len(an)
        exc = sum(1 for a in an if g(p, "NLGQ", a) >= 0)
        ce.append({"pays": p, "annees": "%d-%d" % (an[0], an[-1]), "n": len(an), "depense_moy": round(dep, 1), "recettes_moy": round(rec, 1),
                   "solde_moy": round(sol, 2), "nb_excedents": exc, "depense_2024": "" if g(p, "YPGTQ", 2024) is None else round(g(p, "YPGTQ", 2024), 1),
                   "solde_2024": "" if g(p, "NLGQ", 2024) is None else round(g(p, "NLGQ", 2024), 1)})
    ce.sort(key=lambda x: -x["depense_moy"])
    with open(os.path.join(OUT, "A12_contre_exemples_depense_solde.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(ce[0].keys()), delimiter=";"); w.writeheader(); w.writerows(ce)
    print("ok", len(rows), len(ce))


if __name__ == "__main__":
    main()
