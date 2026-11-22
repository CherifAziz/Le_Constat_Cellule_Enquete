"""Reproduire le passage entre payeurs et les comparaisons DREES, hors ligne."""

import csv
import json
from decimal import Decimal
from pathlib import Path


DOSSIER = Path(__file__).resolve().parent
MILLION = 1_000_000


def variation(ligne, debut, fin):
    return int(ligne[str(fin)]) - int(ligne[str(debut)])


def calculer():
    with (DOSSIER / "comptes.json").open(encoding="utf-8") as fichier:
        comptes = json.load(fichier, parse_float=Decimal)
    senat = comptes["senat"]
    for annee in ["2022", "2023"]:
        depenses = reprises = 0
        for departement, lignes in senat[annee].items():
            if "detail" in lignes:
                assert sum(lignes["detail"]) == lignes["reprises"]
            depenses += lignes["depense"]
            reprises += lignes["reprises"]
            print(annee, departement, "charge, reprises, net (EUR)",
                  lignes["depense"], lignes["reprises"], lignes["depense"] - lignes["reprises"])
        print(annee, "total", depenses, reprises, depenses - reprises,
              "taux de couverture", f"{100 * reprises / depenses:.2f} %")

    # Variation du net, à périmètre constant puis ajout du nouvel entrant.
    communs = senat["2022"].keys()
    variations = {
        poste: sum(senat["2023"][d][poste] - senat["2022"][d][poste] for d in communs)
        for poste in ["depense", "reprises"]
    }
    variation_net = variations["depense"] - variations["reprises"]
    print("2022-2023, 66 et 93, variation (EUR)", variations, "net", variation_net)
    print("Part de la baisse des ressources reprises dans la hausse du net, 66 et 93",
          f"{-100 * variations['reprises'] / variation_net:.1f} %")

    aude = comptes["aude"]
    ecarts = {poste: valeur - aude["2022"][poste] for poste, valeur in aude["2023"].items()}
    print("Aude, évolutions 2022-2023 (EUR)", {p: str(v) for p, v in ecarts.items()})
    part_fse = ecarts["B25_fonds_social_europeen"] / ecarts["B2_insertion_professionnelle"]
    print("Part de la ligne B25 dans la hausse de B2", f"{100 * part_fse:.1f} %")
    insertion = comptes["ssd"]["budget_2023_MEUR"] - comptes["ssd"]["budget_2021_MEUR"]
    print("93, seuil conditionnel (M EUR)", insertion, "soit",
          f"{100 * insertion * MILLION / senat['2023']['93']['depense']:.2f} % du RSA 2023")
    print("RAP 2025, métropole, exécution (M EUR)", comptes["rap_2025"]["execution_MEUR"])

    with (DOSSIER / "oarsa.csv").open(encoding="utf-8", newline="") as fichier:
        enquetes = {(r["tableau"], r["departement"]): r for r in csv.DictReader(fichier)}
    temoins = senat["eligibles_metropole_non_traites"]
    assert len(enquetes) == 2 * (len(temoins) + len(senat["date_entree"]))
    for t in ["B1", "B2"]:
        for d, entree in senat["date_entree"].items():
            debut = entree - 1
            gain = variation(enquetes[t, d], debut, 2024)
            ecarts = {c: gain - variation(enquetes[t, c], debut, 2024) for c in temoins}
            print(t, d, f"{debut}-2024", "variation propre", gain, "écarts aux témoins", ecarts,
                  "étendue", min(ecarts.values()), max(ecarts.values()))
    print("66, B2, avant le transfert, 2019-2021",
          variation(enquetes["B2", "66"], 2019, 2021), "points")
    for debut, fin in [(2019, 2022), (2020, 2022), (2022, 2024)]:
        contraste = variation(enquetes["B1", "09"], debut, fin) - variation(enquetes["B1", "11"], debut, fin)
        print("Ariège moins Aude, B1,", f"{debut}-{fin}", contraste, "points")


if __name__ == "__main__":
    calculer()
