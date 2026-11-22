"""D03 : conversions et petits calculs sur pièces conservées.
Lit ../../donnees/D03/ (tables transcrites et sources) ; écrit ../../donnees/D03/D03_*.csv.
Usage : python -I d03_calculs.py
Conventions : 1 EUR = 6,55957 F ; PIB = colonne PIB_implicite_Md_EUR d'A04 (base 2020, Insee).
Aucune estimation n'est ajoutée : seules des conversions d'unité, des sommes de lignes d'une même pièce
et des taux de croissance sont calculés."""
import csv
import math
from pathlib import Path

import openpyxl

ICI = Path(__file__).resolve().parent
DON = ICI.parent.parent / "donnees" / "D03"
SRC = DON / "sources"
F_EUR = 6.55957


def lire_csv(p):
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def ecrire(nom, entetes, lignes):
    with (DON / nom).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(entetes)
        w.writerows(lignes)
    print(f"{nom} : {len(lignes)} lignes")


def pib():
    return {int(r["annee"]): float(r["PIB_implicite_Md_EUR"]) for r in lire_csv(SRC / "a04_po_recettes_1959_2025.csv")}


def montants(P):
    out = []
    for r in lire_csv(DON / "D03_montants_pieces.csv"):
        a = int(r["annee"])
        v = float(r["valeur"])
        assert r["unite"] == "Md F", r
        eur = v / F_EUR
        out.append([r["id"], r["famille"], a, v, round(eur, 3), round(P[a], 3), round(100 * eur / P[a], 3),
                    r["libelle"], r["perimetre"], r["ex_ante_ou_post"], r["source"], r["page_pdf"], r["marque"]])
    ecrire("D03_montants_pct_pib.csv",
           ["id", "famille", "annee", "Md_F", "Md_EUR", "PIB_Md_EUR", "pct_PIB", "libelle", "perimetre",
            "ex_ante_ou_post", "source", "page_pdf", "marque"], out)


def controle_emploi():
    """Vérifie que chaque chaîne de contrôle figure dans le texte de la pièce, puis calcule les rythmes."""
    rows = lire_csv(DON / "D03_emploi_public_pieces.csv")
    ctrl = []
    for r in rows:
        txt = (SRC / r["source_fichier"]).read_text(encoding="utf-8")
        ok = r["chaine_controle"] in " ".join(txt.split())
        ctrl.append([r["id"], r["source_fichier"], "ok" if ok else "ABSENT"])
    ecrire("D03_controles_emploi.csv", ["id", "fichier", "chaine_trouvee"], ctrl)
    v = {(r["annee"], r["champ"].split(" (")[0]): float(r["effectif_milliers"]) for r in rows}
    out = []
    for champ in ["FPE au sens large", "FPT", "FPH", "total fonction publique"]:
        a, b = v[("1980", champ)], v[("1985", champ)]
        out.append([champ, "1980-1985 (31-12)", a, b, round(b - a, 1), round(100 * ((b / a) ** (1 / 5) - 1), 2)])
    a, b = v[("1975", "salariés de l'État, défense comprise")], v[("1982", "salariés de l'État, défense comprise")]
    out.append(["salariés de l'État, défense comprise", "mi-1975 à fin 1982 (7,5 ans)", a, b, round(b - a, 1),
                round(100 * ((b / a) ** (1 / 7.5) - 1), 2)])
    # total hors P et T (comparaison avec le champ S13 de D01, qui exclut les P et T)
    a = v[("1980", "total fonction publique")] - v[("1980", "P et T")]
    b = v[("1985", "total fonction publique")] - v[("1985", "P et T")]
    out.append(["total fonction publique hors P et T", "1980-1985 (31-12)", round(a, 1), round(b, 1), round(b - a, 1),
                round(100 * ((b / a) ** 0.2 - 1), 2)])
    for champ in ["FPE au sens large", "FPT", "FPH", "total fonction publique"]:
        for (d0, d1) in (("1980", "1982"), ("1982", "1985")):
            x0, x1 = v[(d0, champ)], v[(d1, champ)]
            out.append([champ, f"{d0}-{d1} (31-12)", x0, x1, round(x1 - x0, 1),
                        round(100 * ((x1 / x0) ** (1 / (int(d1) - int(d0))) - 1), 2)])
    ecrire("D03_emploi_public_rythmes.csv",
           ["champ", "periode", "debut_milliers", "fin_milliers", "variation_milliers", "taux_annuel_pct"], out)
    tot = v[("1985", "total fonction publique")] - v[("1980", "total fonction publique")]
    parts = [[c, round(100 * (v[("1985", c)] - v[("1980", c)]) / tot, 1)] for c in ["FPE au sens large", "FPT", "FPH"]]
    ecrire("D03_emploi_public_parts_hausse_1980_1985.csv", ["champ", "part_de_la_hausse_pct"], parts)


def feuille(nom):
    wb = openpyxl.load_workbook(SRC / nom, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def apul(P):
    rows = feuille("insee_cn_t_3205.xlsx")
    ann = rows[2]
    idx = {int(a): i for i, a in enumerate(ann) if a and str(a).isdigit()}
    voulu = ["Rémunération des salariés (D1)", "Consommation intermédiaire (P2)", "Formation brute de capital fixe (P51g)",
             "Transferts courants entre administrations publiques (D73) ", "Total des dépenses",
             "Impôts sur la production et les importations (D2)", "Impôts courants sur le revenu et le patrimoine (D5)"]
    out = []
    for r in rows:
        lib = r[1]
        if lib in voulu:
            for a in (1978, 1980, 1985):
                x = float(r[idx[a]])
                out.append([lib.strip(), a, round(x, 3), round(100 * x / P[a], 3)])
    ecrire("D03_apul_1978_1985.csv", ["ligne_insee_3205", "annee", "Md_EUR", "pct_PIB"], out)


def po_apul():
    rows = feuille("insee_cn_t_3216.xlsx")
    ann = rows[2]
    idx = {int(a): i for i, a in enumerate(ann) if a and str(a).isdigit()}
    out = []
    pct_vu = False
    for r in rows:
        if r[1] and str(r[1]).startswith("En % du produit"):
            pct_vu = True
        if pct_vu and r[1] and str(r[1]).startswith("S1313"):
            for a in (1970, 1973, 1974, 1975, 1978, 1980, 1983, 1985):
                out.append(["prélèvements obligatoires des APUL (S1313)", a, round(float(r[idx[a]]), 3)])
    ecrire("D03_po_apul_1970_1985.csv", ["serie_insee_3216", "annee", "pct_PIB"], out)


def asso(P):
    """Sous-secteur des administrations de sécurité sociale (inclusion des hôpitaux publics : non vérifiée sur la note)."""
    rows = feuille("insee_cn_t_3212.xlsx")
    ann = rows[2]
    idx = {int(a): i for i, a in enumerate(ann) if a and str(a).isdigit()}
    voulu = ["Rémunération des salariés (D1)", "Consommation intermédiaire (P2)",
             "Transferts sociaux en nature de produits marchands (D632)", "Formation brute de capital fixe (P51g)",
             "Total des dépenses"]
    out = []
    for r in rows[:30]:
        if r[1] in voulu:
            for a in (1978, 1980, 1985):
                x = float(r[idx[a]])
                out.append([r[1].strip(), a, round(x, 3), round(100 * x / P[a], 3)])
    ecrire("D03_asso_1978_1985.csv", ["ligne_insee_3212", "annee", "Md_EUR", "pct_PIB"], out)


def concours_composantes(P):
    """Composantes des concours de l'État aux entreprises publiques (Md F, ex ante), lignes des pièces M08, M11, M12
    (citations contrôlées par d03_tables.py). Périmètres : 1980 inclut des prêts du FDES ; 1983-1984 n'en mentionnent pas."""
    comp = [
        (1980, "exploitation (couverture des déficits)", 18.084, "M08"), (1980, "dotations en capital", 2.180, "M08"),
        (1980, "prêts du FDES", 1.700, "M08"), (1980, "charges de retraite (deux régimes sociaux)", 12.337, "M08"),
        (1983, "exploitation (couverture des déficits)", 28.332, "M11"), (1983, "dotations en capital", 9.842, "M11"),
        (1983, "charges de retraite (deux régimes sociaux)", 18.661, "M11"),
        (1984, "exploitation (couverture des déficits)", 31.375, "M12"), (1984, "dotations en capital", 14.921, "M12"),
        (1984, "charges de retraite (deux régimes sociaux)", 20.809, "M12"),
    ]
    out = [[a, c, v, round(v / F_EUR, 3), round(100 * v / F_EUR / P[a], 3), m] for (a, c, v, m) in comp]
    ecrire("D03_concours_entreprises_composantes.csv", ["annee", "composante", "Md_F", "Md_EUR", "pct_PIB", "id_montant"], out)


def ecarts_sante():
    rows = lire_csv(DON / "D03_sante_rythmes.csv")
    cs = {r["periode"]: float(r["valeur"]) for r in rows if r["indicateur"].startswith("CSBM en volume")}
    pb = {r["periode"]: float(r["valeur"]) for r in rows if r["indicateur"].startswith("PIB en volume")}
    out = [[per, cs[per], pb[per], round(cs[per] - pb[per], 1)] for per in sorted(pb)]
    ecrire("D03_sante_ecart_csbm_pib.csv", ["periode", "CSBM_volume_pct_an", "PIB_volume_pct_an", "ecart_points"], out)


def deltas_comptes():
    out = []
    for nom in ("D03_apul_1978_1985.csv", "D03_asso_1978_1985.csv"):
        rows = lire_csv(DON / nom)
        cle = rows[0].keys().__iter__().__next__()
        d = {}
        for r in rows:
            d.setdefault(r[cle], {})[int(r["annee"])] = float(r["pct_PIB"])
        for lib, s in d.items():
            out.append([nom, lib, round(s[1980] - s[1978], 3), round(s[1985] - s[1980], 3), round(s[1985] - s[1978], 3)])
    po = {int(r["annee"]): float(r["pct_PIB"]) for r in lire_csv(DON / "D03_po_apul_1970_1985.csv")}
    out.append(["D03_po_apul_1970_1985.csv", "PO APUL, 1973-1985 (1974 écarté)", "", "", round(po[1985] - po[1973], 3)])
    ecrire("D03_deltas_comptes.csv", ["table", "ligne", "d_1978_1980", "d_1980_1985", "d_total"], out)


def main():
    P = pib()
    ecarts_sante()
    concours_composantes(P)
    controle_emploi()
    apul(P)
    po_apul()
    asso(P)
    deltas_comptes()


if __name__ == "__main__":
    main()
