"""A10 - Series ponderees du Barometre d'opinion de la DREES (2000-2025) sur le deficit,
le financement et l'acceptation de mesures.

Source : DREES, jeu de donnees « Le barometre d'opinion » (data.drees.solidarites-sante.gouv.fr,
dataset 431_le-barometre-d-opinion), fichier barometre2000_2025_diff.csv, telecharge le 20/11/2026
(sha256 b7ad24a2...). Lecture seule ; le fichier n'est jamais execute.

Sortie : resultats/donnees/A10/drees_series_ponderees.csv (annee ; variable ; split ; modalite ;
part ponderee en % ; effectif non pondere des repondants a la question).
Ponderation : variable 'poids' (poids de redressement fourni par la DREES).
Les non-reponses (999999999, vide) sont gardees comme modalite 'NSP' ; les parts sont calculees
sur l'ensemble des personnes a qui la question a ete posee (valeur non vide).
"""
import csv
import os
from collections import defaultdict

BASE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A10"
SRC = os.path.join(BASE, "sources", "drees_barometre", "barometre2000_2025_diff.csv")
OUT = os.path.join(BASE, "drees_series_ponderees.csv")

VARS = ["og04_5", "ps03", "ps15_3", "ps16", "re09bis", "re09", "re03",
        "sa08_1", "sa08_2", "sa08_3", "sa08_5", "sa08_6", "sa08_7", "sa08_9", "sa08_10",
        "me02_a_2025", "me02_b_2025", "me02_c_2025", "me02_d_2025",
        "ps13_ab_1", "ps13_ab_2", "ps13_ab_3", "ps13_ab_4", "ps13_ab_5", "ps13_ab_6", "ps13_ab_7",
        "ps13_cd_1", "ps13_cd_2", "ps13_cd_3", "ps13_cd_4", "ps13_cd_5", "ps13_cd_6", "ps13_cd_7",
        "de11", "me01_2025_1", "me01_2025_2", "me01_2025_3", "me01_2025_5", "pe10", "me05_2025"]
SPLIT_VARS = {"ps13_ab_1", "ps13_ab_2", "ps13_cd_1", "ps13_cd_2"}  # aussi ventilees par sous-echantillon


def lire():
    for enc in ("utf-8", "latin-1"):
        try:
            with open(SRC, encoding=enc, newline="") as f:
                f.readline()
            return enc
        except UnicodeDecodeError:
            continue
    return "latin-1"


def main():
    enc = lire()
    w = defaultdict(float)      # (annee, var, split, modalite) -> somme poids
    tot = defaultdict(float)    # (annee, var, split) -> somme poids
    n = defaultdict(int)        # (annee, var, split) -> effectif
    with open(SRC, encoding=enc, newline="") as f:
        rd = csv.DictReader(f, delimiter=";")
        present = [v for v in VARS if v in rd.fieldnames]
        absent = [v for v in VARS if v not in rd.fieldnames]
        for row in rd:
            an = row["annee"]
            try:
                p = float(row["poids"].replace(",", "."))
            except ValueError:
                continue
            sp = row.get("sdsplit", "")
            for v in present:
                val = (row.get(v) or "").strip()
                if val == "":
                    continue
                mod = "NSP" if val in ("999999999", "999999999.0") else val
                for s in (["tous"] + ([sp] if v in SPLIT_VARS and sp else [])):
                    w[(an, v, s, mod)] += p
                    tot[(an, v, s)] += p
                    n[(an, v, s)] += 1
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["annee", "variable", "sous_echantillon", "modalite", "part_ponderee_pct", "n_non_pondere"])
        for (an, v, s, mod), val in sorted(w.items()):
            wr.writerow([an, v, s, mod, round(100 * val / tot[(an, v, s)], 1), n[(an, v, s)]])
    print("encodage", enc, "| variables absentes du fichier :", absent)
    print("ecrit", OUT)


if __name__ == "__main__":
    main()
