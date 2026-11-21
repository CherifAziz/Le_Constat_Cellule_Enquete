"""A10 - Test propre a la France sur microdonnees DREES (barometre d'opinion) :
(1) ecart individuel entre principe et mesure : parmi les personnes qui jugent plus important
    de « prendre des mesures pour reduire le deficit de la Securite sociale » (PS16 = 1), part
    favorable a chaque mesure SA08 et a une baisse des retraites contre baisse d'impots (PS13_AB_2) ;
(2) interet personnel : PS16, PS13_AB_2, SA08_2 et OG04_5 selon que la personne est retraitee ou non
    (SDSITUA = 6) ;
(3) evolution 2015-2025 de PS16 par statut (retraite / non retraite).

Source : barometre2000_2025_diff.csv (DREES, telecharge le 20/11/2026). Ponderation 'poids'.
Sortie : resultats/donnees/A10/drees_test_principe_mesure.csv
"""
import csv
import os
from collections import defaultdict

BASE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A10"
SRC = os.path.join(BASE, "sources", "drees_barometre", "barometre2000_2025_diff.csv")
OUT = os.path.join(BASE, "drees_test_principe_mesure.csv")

FAV = {  # modalites comptees comme « accepte / favorable »
    "sa08_1": {"1"}, "sa08_2": {"1"}, "sa08_3": {"1"}, "sa08_7": {"1"}, "sa08_10": {"1"},
    "ps13_ab_2": {"1", "2"}, "ps13_ab_1": {"1", "2"},
    "me02_a_2025": {"1", "2"}, "me02_b_2025": {"1", "2"}, "me02_c_2025": {"1", "2"}, "me02_d_2025": {"1", "2"},
    "ps16": {"1"}, "og04_5": {"1"}, "ps15_3": {"1", "2"},
}


def main():
    num = defaultdict(float)
    den = defaultdict(float)
    n = defaultdict(int)
    with open(SRC, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter=";"):
            an = row["annee"]
            if an not in ("2015", "2017", "2019", "2020", "2021", "2023", "2024", "2025"):
                continue
            try:
                p = float(row["poids"].replace(",", "."))
            except ValueError:
                continue
            ret = "retraite" if row.get("sdsitua", "").strip() == "6" else "non_retraite"
            ps16 = (row.get("ps16") or "").strip()
            groupes = ["ensemble", ret]
            if ps16 == "1":
                groupes.append("ps16_reduire_deficit")
            elif ps16 == "2":
                groupes.append("ps16_maintenir_prestations")
            for v, ok in FAV.items():
                val = (row.get(v) or "").strip()
                if val == "":
                    continue
                for g in groupes:
                    k = (an, v, g)
                    den[k] += p
                    n[k] += 1
                    if val in ok:
                        num[k] += p
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["annee", "variable", "groupe", "part_favorable_ou_modalite_cible_pct", "n_non_pondere"])
        for k in sorted(den):
            wr.writerow([k[0], k[1], k[2], round(100 * num[k] / den[k], 1), n[k]])
    print("ecrit", OUT)


if __name__ == "__main__":
    main()
