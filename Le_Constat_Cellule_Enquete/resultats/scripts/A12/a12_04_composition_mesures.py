"""A12 - composition des mesures de consolidation (C-A12-030).

Source : Devries, Guajardo, Leigh, Pescatori, "A New Action-based Dataset of Fiscal Consolidation",
IMF Working Paper 11/128, juin 2011 (PDF lu localement : donnees\\A12\\sources\\imf_wp11128_devries_et_al_2011.pdf ;
extrait automatique : extrait_devries2011_episodes.md). Valeurs = phrase d'en-tete de chaque entree
pays-annee (« Fiscal consolidation totaled X percent of GDP, with spending cuts of Y and tax hikes of Z »),
transcrites a la main par A12 ; page = rang approximatif dans le PDF.
Mesures = effets budgetaires ex ante des decisions motivees par la reduction du deficit (pas les resultats).
Sortie : donnees\\A12\\A12_composition_mesures_devries2011.csv
Usage : python -I a12_04_composition_mesures.py
"""
import csv, os

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(RACINE, "donnees", "A12", "A12_composition_mesures_devries2011.csv")

# (episode, pays, annee, depenses, impots, page PDF approx.) ; valeurs en % du PIB
T = [
    ("E1", "Suede", 1993, 1.39, 0.42, 73), ("E1", "Suede", 1994, 0.59, 0.19, 73), ("E1", "Suede", 1995, 2.10, 1.40, 73),
    ("E1", "Suede", 1996, 1.20, 0.80, 74), ("E1", "Suede", 1997, 0.90, 0.60, 74), ("E1", "Suede", 1998, 0.60, 0.40, 74),
    ("E2", "Canada", 1994, 0.45, 0.04, 26), ("E2", "Canada", 1995, 0.81, 0.18, 27), ("E2", "Canada", 1996, 0.88, 0.09, 27),
    ("E2", "Canada", 1997, 0.47, 0.01, 28),
    ("E3", "Danemark", 1983, 1.85, 0.92, 30), ("E3", "Danemark", 1984, 1.71, 0.67, 30), ("E3", "Danemark", 1985, 0.77, 0.77, 31),
    ("E4", "Belgique", 1992, 0.80, 0.99, 18), ("E4", "Belgique", 1993, 0.49, 0.43, 18), ("E4", "Belgique", 1994, 0.60, 0.55, 19),
    ("E4", "Belgique", 1996, 0.50, 0.50, 20), ("E4", "Belgique", 1997, 0.50, 0.41, 20),
    ("E5", "Italie", 1991, 1.08, 1.69, 50), ("E5", "Italie", 1992, 1.90, 1.60, 51), ("E5", "Italie", 1993, 2.49, 2.00, 51),
    ("E5", "Italie", 1994, 1.70, -0.27, 52), ("E5", "Italie", 1995, 1.79, 2.41, 52), ("E5", "Italie", 1996, 1.08, -0.74, 52),
    ("E5", "Italie", 1997, 0.93, 0.89, 53), ("E5", "Italie", 1998, 0.67, 0.01, 53),
    ("E6", "Allemagne", 2003, 0.00, 0.74, 45), ("E6", "Allemagne", 2004, 1.10, -0.70, 45), ("E6", "Allemagne", 2006, 0.50, 0.00, 46),
    ("E6", "Allemagne", 2007, 0.40, 0.50, 46),
    ("E10", "Japon", 1997, 0.45, 0.975, 57), ("E10", "Japon", 1998, 0.15, 0.325, 58), ("E10", "Japon", 2003, 0.48, 0.00, 58),
    ("E11b", "Irlande", 1987, 1.12, 0.53, 48), ("E11b", "Irlande", 1988, 1.95, 0.00, 49),
    ("E11d", "Finlande", 1992, 0.91, 0.00, 32), ("E11d", "Finlande", 1993, 3.71, 0.00, 32), ("E11d", "Finlande", 1994, 2.77, 0.69, 33),
    ("E11d", "Finlande", 1995, 2.28, -0.63, 33), ("E11d", "Finlande", 1996, 1.47, 0.00, 34), ("E11d", "Finlande", 1997, 0.93, -0.70, 34),
    ("E11e", "Pays-Bas", 1983, 2.75, 0.49, 62), ("E11e", "Pays-Bas", 1984, 1.76, 0.00, 62), ("E11e", "Pays-Bas", 1985, 1.24, 0.00, 62),
    ("E11e", "Pays-Bas", 1986, 1.74, 0.00, 62), ("E11e", "Pays-Bas", 1987, 0.00, 1.48, 63), ("E11e", "Pays-Bas", 1988, 0.75, -0.69, 63),
]


def main():
    rows = []
    for e, p, a, dep, imp, pg in T:
        rows.append({"episode": e, "pays": p, "annee": a, "depenses_pct_PIB": dep, "impots_pct_PIB": imp,
                     "total_pct_PIB": round(dep + imp, 3), "page_pdf": pg, "type": "annee"})
    for e in sorted({r["episode"] for r in rows}, key=lambda x: (len(x), x)):
        sub = [r for r in rows if r["episode"] == e and r["type"] == "annee"]
        dep = sum(r["depenses_pct_PIB"] for r in sub); imp = sum(r["impots_pct_PIB"] for r in sub)
        rows.append({"episode": e, "pays": sub[0]["pays"], "annee": "%d-%d" % (sub[0]["annee"], sub[-1]["annee"]),
                     "depenses_pct_PIB": round(dep, 2), "impots_pct_PIB": round(imp, 2), "total_pct_PIB": round(dep + imp, 2),
                     "page_pdf": "", "type": "cumul ; part depenses = %.0f %%" % (100 * dep / (dep + imp))})
    with open(OUT, "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(rows)
    for r in rows:
        if r["type"] != "annee":
            print(r)


if __name__ == "__main__":
    main()
