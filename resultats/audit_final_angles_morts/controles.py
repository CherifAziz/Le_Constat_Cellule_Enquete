"""Deux contrôles de lecture des séries archivées. Python 3.10+, bibliothèque standard."""
import csv
from pathlib import Path
from statistics import correlation


def main():
    with Path(__file__).with_name("extrait_controles.csv").open(encoding="utf-8", newline="") as fichier:
        annuel = {int(ligne["annee"]): ligne for ligne in csv.DictReader(fichier, delimiter=";")}
    for seuil in (0, 0.5, 1, 2):
        proches = [a for a in range(1975, 2026) if float(annuel[a]["solde_s13_pct"]) >= -seuil]
        print(f"Solde >= {-seuil} % du PIB : {len(proches)}/51 {proches}")

    annees = range(1978, 2026)
    d_solde = [float(annuel[a]["variation_primaire_a09_pts"]) for a in annees[1:]]
    for origine, colonne in (
        ("dénominateur de S11", "pib_s11_mdeur"),
        ("PIB publié, tableau Insee 3.106", "pib_3106_mdeur"),
    ):
        pib = {a: float(annuel[a][colonne]) for a in annees}
        part = {a: 100 * float(annuel[a]["transferts_nets_s11_mdeur"]) / pib[a] for a in annees}
        d_part = [part[a] - part[a - 1] for a in annees[1:]]
        print(f"{origine} : PIB 1980 = {pib[1980]:.3f} Md EUR, transferts 1980 = {part[1980]:.3f} %")
        print(f"Variation 1989-1999 = {part[1999] - part[1989]:.3f} point, r sur 47 variations = {correlation(d_part, d_solde):.3f}")


if __name__ == "__main__":
    main()
