"""Contrôles H12. Exécution hors ligne depuis tout répertoire, Python 3."""

import csv
from decimal import Decimal
from pathlib import Path


def lire_donnees():
    valeurs = {}
    with Path(__file__).with_name("donnees.csv").open(encoding="utf-8", newline="") as fichier:
        for ligne in csv.DictReader(fichier):
            serie = valeurs.setdefault(ligne["serie"], {})
            cle = ligne["cle"]
            if cle in serie:
                raise ValueError(f"Doublon dans {ligne['serie']} : {cle}")
            serie[cle] = Decimal(ligne["valeur"])
    return valeurs


def main():
    valeurs = lire_donnees()
    lievin = valeurs["lievin"]
    total = lievin["indemnisation_ancienne_charpente"]
    assert sum(v for k, v in lievin.items() if k.startswith("part_")) == 100
    part_commune = total * lievin["part_entretien_et_vetuste"] / 100
    print(f"Liévin, fraction conjointe entretien et vétusté : {part_commune:.2f} EUR")
    print("Sur ce seul poste, la ventilation interne entre les deux causes est inconnue.")

    brionne = valeurs["brionne"]
    ecart_annonce = brionne["montant_annonce_2021"] - brionne["estimation_2019"]
    print(f"Brionne, chantier annoncé moins estimation initiale : {ecart_annonce:+} EUR (hors comparaison des loyers)")

    pont = valeurs["bonheur"]
    km_annuels = pont["vehicules_par_jour"] * pont["detour_par_franchissement"] * 365
    print(f"Pont du Bonheur, scénario de détour : {km_annuels} véhicules-km/an")
    print(f"Sur la durée de fermeture supposée : {km_annuels * pont['fermeture_modelee']} véhicules-km")

    crc = valeurs["seine_marne"]
    somme = crc["fonctionnement_2023"] + crc["investissement_2023"]
    ecart = somme - crc["total_publie_2023"]
    print(f"CRC 77, tableau 10, 2023 : lignes = {somme} M EUR, écart au total publié = {ecart} M EUR")

    for region in ("wf", "wnf", "df", "dnf"):
        obs = valeurs[f"fhwa_{region}"]
        ecart_ans = obs["duree_traitees"] - obs["duree_temoins"]
        print(f"FHWA {region.upper()} : {ecart_ans:+} ans, "
              f"{obs['sections_traitees']} sections traitées et {obs['sections_temoins']} témoins")


if __name__ == "__main__":
    main()
