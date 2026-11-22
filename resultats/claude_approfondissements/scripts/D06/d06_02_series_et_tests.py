"""D06 - étape 2 : séries comparées (8 pays) et tests (a) et (b) déclarés à l'avance.

Entrées (conservées sous donnees/D06/sources) :
  - ameco_extrait_D06.csv (extrait AMECO, voir d06_01)
  - BCLDatabase_online_v2.7.xlsx (Bergeaud, Cette, Lecat, version février 2026)
  - JSTdatasetR6.xlsx (Jordà-Schularick-Taylor, release 6 ; État central, table séparée)
Sorties (donnees/D06) :
  - D06_series_comparees.csv
  - D06_test_a_ralentissements.csv, D06_test_a_synthese.csv
  - D06_test_b_nuages.csv, D06_test_b_spearman.csv
  - D06_test_b_JST_etat_central_1975_1995.csv (convention différente, jamais mêlée)
  - D06_desindustrialisation.csv
Le protocole est décrit au §0 du dossier D06.md (écrit avant le premier calcul).
"""
import csv, math, os
import numpy as np
import openpyxl

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(ICI, "..", ".."))
SRC = os.path.join(OUT, "donnees", "D06", "sources")
DST = os.path.join(OUT, "donnees", "D06")
PAYS = ["FRA", "DEU", "ITA", "ESP", "NLD", "SWE", "GBR", "USA"]
ANS = list(range(1960, 2026))  # 2026-2028 = prévisions, exclues
SEUIL = 0.2  # point de pourcentage par an


def lire_ameco():
    d = {}
    with open(os.path.join(SRC, "ameco_extrait_D06.csv"), encoding="utf-8") as h:
        r = csv.reader(h, delimiter=";")
        e = next(r)
        annees = [int(x) for x in e[5:] if x.strip().isdigit()]
        for row in r:
            p, _, code = row[0].partition(".")
            serie = {}
            for a, v in zip(annees, row[5:5 + len(annees)]):
                v = v.strip()
                if v not in ("", "NA") and a <= 2025:
                    serie[a] = float(v)
            d[(p, code)] = serie
    return d


def chainer(dw, de, lien=1991):
    """Raccorde une série Allemagne de l'Ouest (dw) à l'Allemagne (de) en taux de croissance."""
    s = dict(de)
    if lien in dw and lien in de and dw[lien]:
        k = de[lien] / dw[lien]
        for a, v in dw.items():
            if a < lien:
                s[a] = v * k
    return s


def ratio(a, b):
    return {t: a[t] / b[t] for t in a if t in b and b[t]}


def serie_ameco(A, p, code):
    if p == "DEU":
        return chainer(A.get(("D_W", code), {}), A.get(("DEU", code), {}))
    return A.get((p, code), {})


def lire_bcl():
    wb = openpyxl.load_workbook(os.path.join(SRC, "BCLDatabase_online_v2.7.xlsx"), read_only=True, data_only=True)
    out = {}
    for feuille in ("Labor Productivity", "L per capita", "GDP per capita"):
        rows = list(wb[feuille].iter_rows(values_only=True))
        h = rows[0]
        out[feuille] = {}
        for p in PAYS:
            j = h.index(p)
            out[feuille][p] = {int(r[0]): float(r[j]) for r in rows[1:] if r[0] is not None and r[j] is not None}
    return out


def g(s, a, b):
    if a in s and b in s and s[a] > 0 and s[b] > 0:
        return 100 * math.log(s[b] / s[a]) / (b - a)
    return None


def moy(s, ans):
    v = [s[a] for a in ans if a in s]
    return sum(v) / len(v) if len(v) == len(ans) else None


def spearman(x, y):
    pts = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pts) < 5:
        return None, len(pts)
    def rang(v):
        o = np.argsort(v)
        r = np.empty(len(v))
        r[o] = np.arange(len(v))
        # ex aequo : rang moyen
        for val in set(v):
            idx = [i for i, w in enumerate(v) if w == val]
            if len(idx) > 1:
                r[idx] = np.mean(r[idx])
        return r
    a = rang([p[0] for p in pts]); b = rang([p[1] for p in pts])
    return float(np.corrcoef(a, b)[0, 1]), len(pts)


def ecrire(nom, entete, lignes):
    with open(os.path.join(DST, nom), "w", encoding="utf-8", newline="") as h:
        w = csv.writer(h, delimiter=";")
        w.writerow(entete)
        for l in lignes:
            w.writerow(["" if x is None else (round(x, 4) if isinstance(x, float) else x) for x in l])


def main():
    A = lire_ameco()
    B = lire_bcl()
    S = {}
    for p in PAYS:
        pib = serie_ameco(A, p, "1.1.0.0.OVGD") if p != "DEU" else chainer(A[("D_W", "1.1.0.0.OVGD")], A[("DEU", "1.1.0.0.OVGD")])
        heures = serie_ameco(A, p, "1.0.0.0.NLHT")
        pop1564 = A[(p, "1.0.0.0.NPAN")]
        hpa = ratio(serie_ameco(A, p, "1.0.0.0.NLHT"), pop1564) if p != "DEU" else None
        if p == "DEU":
            hpa = chainer(ratio(A[("D_W", "1.0.0.0.NLHT")], A[("D_W", "1.0.0.0.NPAN")]),
                          ratio(A[("DEU", "1.0.0.0.NLHT")], A[("DEU", "1.0.0.0.NPAN")]))
        uvgm = A.get((p, "1.0.0.0.UVGM"), {})
        uvg0 = A.get((p, "1.1.0.0.UVG0"), {})
        netm = A.get((p, "1.0.0.0.NETM"), {})
        netd = A.get((p, "1.0.0.0.NETD"), {})
        if p == "DEU":  # parts : niveaux de l'Ouest avant 1991, sans raccord (rupture signalée)
            uvgm = {**A[("D_W", "1.0.0.0.UVGM")], **uvgm}
            uvg0 = {**A[("D_W", "1.1.0.0.UVG0")], **uvg0}
            netm = {**A[("D_W", "1.0.0.0.NETM")], **netm}
            netd = {**{a: v for a, v in A[("D_W", "1.0.0.0.NETD")].items() if a < 1991}, **netd}
        S[p] = {
            "pib_heure_bcl": B["Labor Productivity"][p],
            "pib_heure_ameco": ratio(pib, heures),
            "heures_par_15_64": {a: 1000 * v for a, v in hpa.items()},  # NLHT (millions) / NPAN (milliers) -> heures par personne
            "pib_hab_volume": serie_ameco(A, p, "1.1.0.0.RVGDP"),
            "part_manuf_va_courant": {a: 100 * v for a, v in ratio(uvgm, uvg0).items()},
            "part_manuf_emploi": {a: 100 * v for a, v in ratio(netm, netd).items()},
            "solde_apu": A.get((p, "1.0.319.0.UBLGE"), {}),
            "solde_cvc": A.get((p, "1.0.319.0.UBLGAP"), {}),
            "ecart_production": serie_ameco(A, p, "1.0.0.0.AVGDGP"),
        }
    vars_ = list(S["FRA"].keys())
    lignes = []
    for p in PAYS:
        for a in ANS:
            row = [p, a] + [S[p][v].get(a) for v in vars_]
            row.append("Allemagne de l'Ouest avant 1991 (raccord en croissance pour PIB/heure et heures ; parts en niveau, rupture)" if p == "DEU" and a < 1991 else "")
            lignes.append(row)
    ecrire("D06_series_comparees.csv", ["pays", "annee"] + vars_ + ["note"], lignes)

    # ---------------- Test (a)
    fen = {
        "principal": [("R1 1974", (1960, 1973), (1973, 1990)), ("R2 annees 1990", (1973, 1990), (1990, 2007)),
                      ("R3 2008", (1990, 2007), (2007, 2019)), ("R4 2019", (2007, 2019), (2019, 2025))],
        "robustesse": [("R1' 1974", (1960, 1974), (1974, 1989)), ("R2' annees 1990", (1980, 1990), (1995, 2007)),
                       ("R3' 2008", (1995, 2007), (2010, 2019)), ("R4' 2019", (2015, 2019), (2019, 2025))],
    }
    det, syn = [], []
    for jeu, liste in fen.items():
        for nom, av, ap in liste:
            for src in ("pib_heure_bcl", "pib_heure_ameco"):
                ap2 = ap
                if src == "pib_heure_bcl" and ap[1] == 2025:
                    ap2 = (ap[0], 2024)  # BCL s'arrête en 2024
                ral = {}
                for p in PAYS:
                    s = S[p][src]
                    ga, gp = g(s, *av), g(s, *ap2)
                    r = None if ga is None or gp is None else gp - ga
                    ral[p] = (ga, gp, r)
                autres = [ral[p][2] for p in PAYS if p != "FRA" and ral[p][2] is not None]
                apres_autres = [ral[p][1] for p in PAYS if p != "FRA" and ral[p][1] is not None]
                fr = ral["FRA"]
                if fr[2] is None or len(autres) < 5:
                    syn.append([jeu, nom, src, f"{av[0]}-{av[1]}", f"{ap2[0]}-{ap2[1]}", fr[0], fr[1], fr[2], None, None, None, None, len(autres), "non calculable"])
                    for p in PAYS:
                        det.append([jeu, nom, src, p, *ral[p]])
                    continue
                med = float(np.median(autres)); ecart = fr[2] - med
                verdict = "plus fort" if ecart < -SEUIL else ("plus faible" if ecart > SEUIL else "egal")
                classes = sorted([(ral[p][2], p) for p in PAYS if ral[p][2] is not None])
                rang = [p for _, p in classes].index("FRA") + 1
                syn.append([jeu, nom, src, f"{av[0]}-{av[1]}", f"{ap2[0]}-{ap2[1]}", fr[0], fr[1], fr[2], med, ecart,
                            float(np.median(apres_autres)), f"{rang}/{len(classes)}", len(autres), verdict])
                for p in PAYS:
                    det.append([jeu, nom, src, p, *ral[p]])
    ecrire("D06_test_a_ralentissements.csv", ["jeu", "rupture", "source", "pays", "croissance_avant_pct_an", "croissance_apres_pct_an", "ralentissement_pts"], det)
    ecrire("D06_test_a_synthese.csv", ["jeu", "rupture", "source", "fenetre_avant", "fenetre_apres", "FRA_avant", "FRA_apres", "FRA_ralentissement",
                                       "mediane_7_ralentissement", "ecart_FRA_moins_mediane", "mediane_7_croissance_apres", "rang_FRA_1_plus_fort", "n_autres", "verdict"], syn)

    # ---------------- Test (b)
    per = [(1995, 2007), (2007, 2019), (2019, 2025), (1995, 2025)]
    nu, sp = [], []
    for a, b in per:
        X = {k: [] for k in ("d_solde", "d_solde_cvc", "g_pib_hab", "d_part_manuf", "g_heures_1564")}
        for p in PAYS:
            s, c = S[p]["solde_apu"], S[p]["solde_cvc"]
            if (a, b) == (2019, 2025):
                ds = s[b] - s[a] if a in s and b in s else None
                dc = c[b] - c[a] if a in c and b in c else None
            else:
                m1, m2 = moy(s, [a, a + 1, a + 2]), moy(s, [b - 2, b - 1, b])
                ds = None if m1 is None or m2 is None else m2 - m1
                c1, c2 = moy(c, [a, a + 1, a + 2]), moy(c, [b - 2, b - 1, b])
                dc = None if c1 is None or c2 is None else c2 - c1
            pm = S[p]["part_manuf_va_courant"]
            dpm = pm[b] - pm[a] if a in pm and b in pm else None
            row = [ds, dc, g(S[p]["pib_hab_volume"], a, b), dpm, g(S[p]["heures_par_15_64"], a, b)]
            for k, v in zip(X, row):
                X[k].append(v)
            nu.append([f"{a}-{b}", p, *row])
        for y in ("d_solde", "d_solde_cvc"):
            for x in ("g_pib_hab", "d_part_manuf", "g_heures_1564"):
                rho, n = spearman(X[x], X[y])
                lecture = None if rho is None else ("association descriptive marquee" if abs(rho) >= 0.6 else "pas d'association nette")
                sp.append([f"{a}-{b}", y, x, rho, n, lecture])
    ecrire("D06_test_b_nuages.csv", ["periode", "pays", "var_solde_apu_pts_pib", "var_solde_cvc_pts_pib_potentiel", "croissance_pib_hab_pct_an",
                                     "var_part_manuf_va_pts", "croissance_heures_par_15_64_pct_an"], nu)
    ecrire("D06_test_b_spearman.csv", ["periode", "variable_solde", "variable_rapprochee", "rho_spearman", "n_pays", "lecture_declaree"], sp)

    # ---------------- Version longue, convention JST (État central), table séparée
    wb = openpyxl.load_workbook(os.path.join(SRC, "JSTdatasetR6.xlsx"), read_only=True, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True)); h = rows[0]
    ix = {k: h.index(k) for k in ("year", "iso", "revenue", "expenditure", "gdp")}
    J = {}
    for r in rows[1:]:
        if r[ix["iso"]] in PAYS and r[ix["revenue"]] is not None and r[ix["expenditure"]] is not None and r[ix["gdp"]]:
            J.setdefault(r[ix["iso"]], {})[int(r[ix["year"]])] = 100 * (r[ix["revenue"]] - r[ix["expenditure"]]) / r[ix["gdp"]]
    jl = []
    X = {k: [] for k in ("d", "gh", "dm", "hh")}
    a, b = 1975, 1995
    for p in PAYS:
        s = J.get(p, {})
        m1, m2 = moy(s, [a, a + 1, a + 2]), moy(s, [b - 2, b - 1, b])
        d = None if m1 is None or m2 is None else m2 - m1
        pm = S[p]["part_manuf_va_courant"]
        dm = pm[b] - pm[a] if a in pm and b in pm else None
        gh = g(B["GDP per capita"][p], a, b)
        hh = g(S[p]["heures_par_15_64"], a, b)
        jl.append([f"{a}-{b}", p, m1, m2, d, gh, dm, hh])
        for k, v in zip(X, (d, gh, dm, hh)):
            X[k].append(v)
    for k, lab in (("gh", "croissance PIB/hab BCL"), ("dm", "var part manuf VA"), ("hh", "croissance heures/15-64")):
        rho, n = spearman(X[k], X["d"])
        jl.append(["spearman", lab, None, None, rho, n, None, None])
    ecrire("D06_test_b_JST_etat_central_1975_1995.csv", ["periode", "pays", "solde_etat_central_moy_1975_77", "solde_etat_central_moy_1993_95",
                                                         "variation_pts", "croissance_pib_hab_pct_an", "var_part_manuf_va_pts", "croissance_heures_par_15_64_pct_an"], jl)

    # ---------------- Désindustrialisation (descriptif)
    dl = []
    for p in PAYS:
        va, em = S[p]["part_manuf_va_courant"], S[p]["part_manuf_emploi"]
        dl.append([p] + [va.get(t) for t in (1970, 1974, 1980, 1990, 2000, 2007, 2019, 2024)] +
                  [em.get(t) for t in (1970, 1974, 1980, 1990, 2000, 2007, 2019, 2024)])
    ecrire("D06_desindustrialisation.csv", ["pays"] + [f"va_{t}" for t in (1970, 1974, 1980, 1990, 2000, 2007, 2019, 2024)] +
           [f"emploi_{t}" for t in (1970, 1974, 1980, 1990, 2000, 2007, 2019, 2024)], dl)
    print("ok")


if __name__ == "__main__":
    main()
