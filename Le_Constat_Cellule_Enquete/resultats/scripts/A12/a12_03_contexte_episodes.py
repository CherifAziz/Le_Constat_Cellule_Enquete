"""A12 - contexte annuel de chaque episode, de t0-2 a t0+10 (C-A12-020).

Entrees : AMECO (copie de la cellule) : XUNNQ / XUNRQ (taux de change effectifs nominal et reel,
          37 pays industriels, double ponderation des exportations, 2020 = 100), ILN et ILRV (taux longs
          nominal et reel, deflateur du PIB), UBLG (solde APU, % PIB, SEC 2010), UIGG0 (FBCF des APU, % PIB),
          UDGGL (dette, % PIB) ; OCDE EO 119 : GDPV_ANNPCT, UNR, XMKT, IGAA, GDP, NLGQ, NLGXQ.
Sortie : donnees\\A12\\A12_contexte_episodes.csv (format long : episode ; annee ; variables)
Usage : python -I a12_03_contexte_episodes.py
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a12_ameco_commun import lire_ameco, SORTIE
import a12_02_episodes as ep


def main():
    d = ep.charger()
    am = lire_ameco({"3.0.30.437.XUNNQ", "3.0.30.437.XUNRQ", "1.1.0.0.ILN", "1.1.0.0.ILRV", "1.0.319.0.UBLG", "1.0.319.0.UIGG0"})
    for code, v in am.items():
        pays, reste = code.split(".", 1)
        d[(pays, "AM_" + reste.split(".")[-1])] = v["serie"]
    rows = []
    for eid, p, t0, lib, ze in ep.EPISODES:
        for a in range(t0 - 2, t0 + 11):
            def gv(m):
                return d.get((p, m), {}).get(a)
            x1, x0 = gv("XMKT"), d.get((p, "XMKT"), {}).get(a - 1)
            gdp, inv = gv("GDP"), gv("IGAA")
            r = {"episode": eid, "pays": p, "annee": a, "t": a - t0,
                 "croissance_PIB_vol": gv("GDPV_ANNPCT"), "chomage": gv("UNR"),
                 "marches_export_croiss": None if not (x1 and x0) else 100 * (x1 / x0 - 1),
                 "TCEN_37pays_2020_100": gv("AM_XUNNQ"), "TCER_CUS_37pays": gv("AM_XUNRQ"),
                 "taux_long_nominal_AMECO": gv("AM_ILN"), "taux_long_reel_AMECO": gv("AM_ILRV"),
                 "solde_OCDE": gv("NLGQ"), "solde_AMECO_SEC2010": gv("AM_UBLG"), "primaire_OCDE": gv("NLGXQ"),
                 "invest_public_OCDE_pct_PIB": None if not (gdp and inv) else 100 * inv / gdp,
                 "invest_public_AMECO_UIGG0": gv("AM_UIGG0"), "dette_AMECO": gv("AMECO_UDGGL")}
            rows.append({k: ("" if v is None else (round(v, 2) if isinstance(v, float) else v)) for k, v in r.items()})
    with open(os.path.join(SORTIE, "A12_contexte_episodes.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    print("ok", len(rows))


if __name__ == "__main__":
    main()
