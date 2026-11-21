"""A12 - grille commune des episodes (C-A12-010 a C-A12-030).

Entrees : donnees\\A12\\sources\\oecd_eo119_finpub.csv, oecd_eo119_macro.csv (OCDE EO 119).
Sorties : donnees\\A12\\A12_episodes_grille.csv (une ligne par episode et horizon)
          donnees\\A12\\A12_episodes_verdicts.csv (une ligne par episode, criteres fixes au sec. 0 du dossier)
Criteres (fixes avant calcul, dossier A12 sec. 0) :
  R : dprim(t0->t0+5) >= 3 ET dette(t0+5) < dette(t0) ET dette(t0+10) < dette(t0)
      ET prim(t0+10) - prim(t0) >= 0,5 * dprim(t0->t0+5)
  E : dette(t0+5) - dette(t0) > 10 OU dprim(t0->t0+5) < 1
  P : autres cas
  prim = NLGXQ (solde primaire OCDE, hors interets nets, % PIB) ; dette = AMECO UDGGL (dette Maastricht, serie
  raccordee, % PIB) ; a defaut OCDE GGFLQ (engagements financiers bruts, concept plus large). Effort structurel = NLGXQA (primaire corrige du cycle, %
  PIB potentiel), quand disponible.
Usage : python -I a12_02_episodes.py
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a12_ameco_commun import lire_ameco

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(RACINE, "donnees", "A12", "sources")
OUT = os.path.join(RACINE, "donnees", "A12")

EPISODES = [  # (id, pays, t0, libelle, zone euro a t0+1)
    ("E1", "SWE", 1993, "Suede 1994-1998", "non"),
    ("E2", "CAN", 1994, "Canada 1995-1998", "non"),
    ("E3", "DNK", 1982, "Danemark 1983-1986", "non"),
    ("E4", "BEL", 1992, "Belgique 1993-2007", "non (euro 1999)"),
    ("E5", "ITA", 1991, "Italie 1992-2019", "non (euro 1999)"),
    ("E6", "DEU", 2002, "Allemagne 2003-2019", "oui"),
    ("E7", "GBR", 2009, "Royaume-Uni 2010-2019", "non"),
    ("E8", "PRT", 2009, "Portugal 2010-2019", "oui"),
    ("E9", "GRC", 2009, "Grece 2010-2018", "oui"),
    ("E10", "JPN", 1996, "Japon 1997", "non"),
    ("E11a", "ESP", 2009, "Espagne 2010-2019", "oui"),
    ("E11b", "IRL", 1986, "Irlande 1987-1989", "non"),
    ("E11c", "IRL", 2009, "Irlande 2010-2014", "oui"),
    ("E11d", "FIN", 1993, "Finlande 1994-2000", "non (euro 1999)"),
    ("E11e", "NLD", 1982, "Pays-Bas 1983-1990", "non"),
    ("REF1", "FRA", 1993, "France 1994-2000 (reference)", "non (euro 1999)"),
    ("REF2", "FRA", 2010, "France 2011-2019 (reference)", "oui"),
]
HORIZONS = [0, 3, 5, 10]


def charger():
    d = {}
    am = lire_ameco({"1.0.319.0.UDGGL", "1.0.319.0.UBLGI", "1.0.319.0.UIGG0"})
    for code, v in am.items():
        pays, reste = code.split(".", 1)
        d[(pays, "AMECO_" + reste.split(".")[-1])] = v["serie"]
    for f in ("oecd_eo119_finpub.csv", "oecd_eo119_macro.csv", "oecd_eo119_interets.csv"):
        with open(os.path.join(SRC, f), encoding="utf-8") as h:
            for r in csv.DictReader(h):
                try:
                    d.setdefault((r["REF_AREA"], r["MEASURE"]), {})[int(r["TIME_PERIOD"])] = float(r["OBS_VALUE"])
                except (ValueError, KeyError):
                    pass
    return d


def g(d, p, m, a):
    return d.get((p, m), {}).get(a)


def moy(vals):
    vals = [v for v in vals if v is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def r1(x):
    return "" if x is None else round(x, 1)


def main():
    d = charger()
    grille, verdicts = [], []
    for eid, p, t0, lib, ze in EPISODES:
        for h in HORIZONS:
            a = t0 + h
            gdp = g(d, p, "GDP", a)
            inv = g(d, p, "IGAA", a)
            grille.append({
                "episode": eid, "pays": p, "libelle": lib, "t0": t0, "horizon": h, "annee": a,
                "solde_NLGQ": r1(g(d, p, "NLGQ", a)), "primaire_NLGXQ": r1(g(d, p, "NLGXQ", a)),
                "primaire_cycl_NLGXQA": r1(g(d, p, "NLGXQA", a)),
                "dette_GGFLQ": r1(g(d, p, "GGFLQ", a)), "dette_maastricht": r1(g(d, p, "GGFLMQ", a)), "dette_AMECO_UDGGL": r1(g(d, p, "AMECO_UDGGL", a)),
                "invest_public_AMECO_UIGG0": r1(g(d, p, "AMECO_UIGG0", a)),
                "chomage_UNR": r1(g(d, p, "UNR", a)), "taux_long_IRL": r1(g(d, p, "IRL", a)),
                "taux_court_IRS": r1(g(d, p, "IRS", a)),
                "inflation_IPC": r1(g(d, p, "CPI_YTYPCT", a)),
                "invest_public_pct_PIB": "" if not (gdp and inv) else round(100 * inv / gdp, 2),
                "change_par_USD_EXCH": "" if g(d, p, "EXCH", a) is None else round(g(d, p, "EXCH", a), 4),
                "compte_courant_pct_PIB": r1(g(d, p, "CBGDPR", a)),
                "croissance_moy_t0+1_a_annee": moy([g(d, p, "GDPV_ANNPCT", y) for y in range(t0 + 1, a + 1)]) if h else "",
                "marches_export_croiss_moy": moy([(g(d, p, "XMKT", y) / g(d, p, "XMKT", y - 1) - 1) * 100
                                                  if g(d, p, "XMKT", y) and g(d, p, "XMKT", y - 1) else None
                                                  for y in range(t0 + 1, a + 1)]) if h else "",
            })
        pr = {h: g(d, p, "NLGXQ", t0 + h) for h in HORIZONS}
        src_dette = "AMECO UDGGL" if all(g(d, p, "AMECO_UDGGL", t0 + h) is not None for h in HORIZONS) else "OCDE GGFLQ"
        cle = "AMECO_UDGGL" if src_dette == "AMECO UDGGL" else "GGFLQ"
        de = {h: g(d, p, cle, t0 + h) for h in HORIZONS}
        dm = {h: g(d, p, "GGFLMQ", t0 + h) for h in HORIZONS}
        pa = {h: g(d, p, "NLGXQA", t0 + h) for h in HORIZONS}
        best = max((g(d, p, "NLGXQ", t0 + k) for k in range(1, 6) if g(d, p, "NLGXQ", t0 + k) is not None), default=None)
        dp5 = None if pr[0] is None or pr[5] is None else pr[5] - pr[0]
        dpmax = None if pr[0] is None or best is None else best - pr[0]

        def juger(de):
            if dp5 is None or de.get(0) is None or de.get(5) is None:
                return "non calculable", "", False
            garde = None if pr[10] is None else pr[10] - pr[0]
            fragile = abs(dp5 - 3) < 0.3 or abs(de[5] - de[0]) < 1.0 or (de.get(10) is not None and abs(de[10] - de[0]) < 1.0)                 or abs(de[5] - de[0] - 10) < 1.0 or abs(dp5 - 1) < 0.3
            if dp5 >= 3 and de[5] < de[0] and de.get(10) is not None and de[10] < de[0] and garde is not None and garde >= 0.5 * dp5:
                return "R", "primaire +%.1f, dette en baisse a 5 et 10 ans, amelioration conservee" % dp5, fragile
            if de[5] - de[0] > 10 or dp5 < 1:
                return "E", (("dette +%.1f pts a 5 ans" % (de[5] - de[0])) if de[5] - de[0] > 10 else ("primaire +%.1f seulement a 5 ans" % dp5)), fragile
            manques = []
            if dp5 < 3: manques.append("primaire +%.1f < 3" % dp5)
            if de[5] >= de[0]: manques.append("dette a 5 ans non en baisse (%+.1f)" % (de[5] - de[0]))
            if de.get(10) is not None and de[10] >= de[0]: manques.append("dette a 10 ans non en baisse (%+.1f)" % (de[10] - de[0]))
            if garde is not None and garde < 0.5 * dp5: manques.append("amelioration non conservee a 10 ans")
            return "P", " ; ".join(manques), fragile

        verdict, raison, fragile = juger(de)
        de_ocde = {h: g(d, p, "GGFLQ", t0 + h) for h in HORIZONS}
        verdict_ocde, _, _ = juger(de_ocde)
        # Decomposition de la variation de dette t0 -> t0+5 (identite) : dd = deficit primaire + interets - effet croissance + residu
        dec = {"primaire": 0.0, "interets": 0.0, "croissance_nominale": 0.0}
        ok = True
        for y in range(t0 + 1, t0 + 6):
            nl, itv, dprev = g(d, p, "NLGQ", y), g(d, p, "GGINTP", y), g(d, p, cle, y - 1)
            g1, g0 = g(d, p, "GDP", y), g(d, p, "GDP", y - 1)
            if None in (nl, itv, dprev, g1, g0):
                ok = False; break
            it = 100 * itv / g1
            gr = g1 / g0 - 1
            dec["primaire"] += -(nl + it)
            dec["interets"] += it
            dec["croissance_nominale"] += -gr / (1 + gr) * dprev
        if ok and de.get(5) is not None and de.get(0) is not None:
            dd = de[5] - de[0]
            dec["residu_stock_flux"] = dd - sum(dec.values())
            dec["variation"] = dd
        else:
            dec = {}
        verdicts.append({
            "episode": eid, "pays": p, "libelle": lib, "t0": t0, "zone_euro": ze,
            "prim_t0": r1(pr[0]), "prim_t5": r1(pr[5]), "prim_t10": r1(pr[10]), "dprim_t0_t5": r1(dp5), "dprim_max_1_5": r1(dpmax),
            "prim_cycl_t0": r1(pa[0]), "prim_cycl_t5": r1(pa[5]),
            "dprim_cycl_t0_t5": "" if pa[0] is None or pa[5] is None else r1(pa[5] - pa[0]),
            "source_dette_verdict": src_dette, "dette_t0": r1(de[0]), "dette_t3": r1(de[3]), "dette_t5": r1(de[5]), "dette_t10": r1(de[10]),
            "dette_OCDE_GGFLQ_t0": r1(g(d, p, "GGFLQ", t0)), "dette_OCDE_GGFLQ_t5": r1(g(d, p, "GGFLQ", t0 + 5)),
            "dette_pic_t0_t10": r1(max([v for v in [g(d, p, cle, t0 + k) for k in range(0, 11)] if v is not None], default=None)),
            "chomage_t0": r1(g(d, p, "UNR", t0)), "chomage_t3": r1(g(d, p, "UNR", t0 + 3)), "chomage_t5": r1(g(d, p, "UNR", t0 + 5)),
            "verdict_grille": verdict, "raison": raison, "verdict_si_dette_OCDE_GGFLQ": verdict_ocde,
            "fragile": "oui" if fragile else "non",
            "dd_t0_t5": r1(dec.get("variation")), "contrib_primaire": r1(dec.get("primaire")), "contrib_interets": r1(dec.get("interets")),
            "contrib_croissance_nominale": r1(dec.get("croissance_nominale")), "contrib_residu": r1(dec.get("residu_stock_flux")),
        })
    for nom, rows in (("A12_episodes_grille.csv", grille), ("A12_episodes_verdicts.csv", verdicts)):
        with open(os.path.join(OUT, nom), "w", newline="", encoding="utf-8") as h:
            w = csv.DictWriter(h, fieldnames=list(rows[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(rows)
    print("ok", len(verdicts), "episodes")


if __name__ == "__main__":
    main()
