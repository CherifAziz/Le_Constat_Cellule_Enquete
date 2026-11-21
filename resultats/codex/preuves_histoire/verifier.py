"""Calculs du dossier historique. Python 3, bibliothèque standard, sans réseau.

Les nombres sont transcrits des publications identifiées à côté de chaque
opération. Consulter histoire.md pour les liens, périmètres et millésimes.
Exécution : python verifier.py
"""
from decimal import Decimal as D
from pathlib import Path
import re


def resultat(libelle, valeur, unite, decimales=2):
    print(f"{libelle} = {valeur:.{decimales}f} {unite}")


def main():
    # HCFP 2025-2, graphique 1. Solde négatif = déficit.
    resultat("Amélioration S13 de 1975 à 1980", D("-0.4") - D("-2.9"), "points de PIB")

    # Parité irrévocable franc/euro, règlement UE 2866/98, article 1.
    francs_par_euro = D("6.55957")
    # Sénat, règlement 2000, partie I, II (collectif) et exécution, III.
    collectif = D("51.4") / francs_par_euro
    deficit_2000 = D("19.1")
    resultat("Révision du collectif de printemps 2000", collectif, "Md€")
    resultat("Déficit 2000 restant si toute la marge est conservée", deficit_2000 - collectif, "Md€")
    resultat("Part de l'écart 2000 couverte à activité fixe", 100 * collectif / deficit_2000, "%")

    # Cour, situation juin 2008, tableau 1. Mars 2011 France/Allemagne pp. 51-52.
    pib_2007 = D("1892")
    manque_2007 = pib_2007 * D("0.027")
    resultat("Écart 2007 au zéro à partir du ratio arrondi d'époque", manque_2007, "Md€")
    resultat("Écart 2007 après retrait des 12 Md€ d'allégements", manque_2007 - 12, "Md€")
    resultat("Ratio correspondant", 100 * (manque_2007 - 12) / pib_2007, "% du PIB")
    resultat("Loi TEPA 2007, rendement facial sur le PIB de l'année", 100 * D("1.6") / pib_2007, "point de PIB")

    # Cour des comptes, juin 2016, pp. 25-26. Variation totale et primaire.
    difference = D("1.3") - D("0.7")
    resultat("Contribution de la baisse de la charge d'intérêts, 2012–2015", difference, "point de PIB")
    resultat("Part de l'amélioration totale 2012–2015", 100 * difference / D("1.3"), "%")

    # Insee, comptes 2019 publiés en 2020, figure 1. Le calcul ne s'applique pas à la base 2020.
    resultat("Variation du solde 2018–2019, millésime 2020", D("-3.0") - D("-2.3"), "point de PIB")
    resultat("Variation neutralisant le chevauchement, même millésime",
             D("-3.0") + D("0.9") - D("-2.3"), "point de PIB")

    # Insee Première 1859 et 2106. CADES, documentation d'émission avril 2025.
    resultat("Activité partielle et fonds de solidarité en 2020", D("27.4") + D("15.9"), "Md€")
    resultat("CADES, dette restant à amortir fin 2024", D("396.5") - D("258.6"), "Md€")
    resultat("Réduction du déficit en valeur en 2025", D("169.1") - D("152.5"), "Md€")
    resultat("Deux contributions exceptionnelles dans les mesures nouvelles de 2025", 100 * 8 / D("23.0"), "%")

    # Contrôle d'intégrité de l'annexe (le fichier est lu sans être modifié).
    reperes = Path(__file__).with_name("reperes_annuels.md").read_text(encoding="utf-8")
    annees = [int(x) for x in re.findall(r"^\| (\d{4}) \|", reperes, re.MULTILINE)]
    assert annees == list(range(1974, 2027)), "Doublon ou année absente dans les repères"
    print("53 repères vérifiés, dont 51 exercices de 1975 à 2025.")


if __name__ == "__main__":
    main()
