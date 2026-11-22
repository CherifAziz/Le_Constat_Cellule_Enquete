"""Rejouer hors ligne avec Python 3.10+ : python calculs.py"""

import json
from hashlib import sha256
from math import prod
from pathlib import Path
from statistics import correlation


DOSSIER = Path(__file__).resolve().parent


def lire_eurostat(nom, dimension_pays, empreinte):
    contenu = (DOSSIER / nom).read_bytes()
    if sha256(contenu.replace(b"\r\n", b"\n")).hexdigest() != empreinte:
        raise ValueError(f"Empreinte de l'extrait Eurostat inattendue : {nom}")
    source = json.loads(contenu)
    dimensions = source["id"]
    axes = source["dimension"]
    if any(taille != 1 for axe, taille in zip(dimensions, source["size"])
           if axe not in (dimension_pays, "time")):
        raise ValueError("La requête contient une dimension supplémentaire.")
    series = {}
    for pays_brut, indice in axes[dimension_pays]["category"]["index"].items():
        pays = "EL" if pays_brut == "GR" else pays_brut
        serie = {}
        for annee, an in axes["time"]["category"]["index"].items():
            # JSON-stat stocke les observations par indice dans le produit des axes.
            position = 0
            for axe, taille in zip(dimensions, source["size"]):
                coord = {dimension_pays: indice, "time": an}.get(axe, 0)
                position = position * taille + coord
            serie[int(annee)] = source["value"][str(position)]
        series[pays] = serie
    return series


def evolution(serie, debut, fin, taux_annuels=False):
    if taux_annuels:
        ratio = prod(1 + serie[annee] / 100 for annee in range(debut + 1, fin + 1))
    else:
        ratio = serie[fin] / serie[debut]
    return 100 * (ratio - 1)


def rho_spearman(x, y):
    # Les six observations des séries examinées ont des rangs distincts.
    if len(set(x)) < len(x) or len(set(y)) < len(y):
        raise ValueError("Le calcul des rangs doit tenir compte des ex aequo.")
    return correlation([sorted(x).index(v) for v in x], [sorted(y).index(v) for v in y])


def main():
    exports = lire_eurostat("comext_exportations.json", "partner",
        "58af1d7c21869fb0f01b00290c664ffeea75886664423f372117bc1adbe8cd15")
    imports = lire_eurostat("eurostat_importations.json", "geo",
        "31f5877a676986ac4c28c4e49780d33e67150a5af88ba6127b319ca34ae22b89")
    ref = json.loads((DOSSIER / "hypotheses_et_modeles.json").read_text(encoding="utf-8"))
    effort = ref["effort_cumule_2011_2013_CE_tableau_4"]
    if exports.keys() != imports.keys() or exports.keys() != effort.keys():
        raise ValueError("Échantillons incompatibles.")
    pays_tries = sorted(effort, key=effort.get)
    print("Pays, ajustement 2011-13, variation des exportations FR en valeur et des importations totales en volume (%)")
    print("Pays  Effort   X07-10   X10-13   X13-15   M10-13")
    for pays in pays_tries:
        valeurs = [effort[pays], evolution(exports[pays], 2007, 2010),
                   evolution(exports[pays], 2010, 2013), evolution(exports[pays], 2013, 2015),
                   evolution(imports[pays], 2010, 2013, taux_annuels=True)]
        print(pays, *(f"{valeur:8.2f}" for valeur in valeurs))
    print("\nRangs des efforts 2011-13 et des variations sur chaque fenêtre")
    for nom, series, taux in (("X", exports, False), ("M", imports, True)):
        for debut, fin in ((2007, 2009), (2007, 2010), (2010, 2013), (2013, 2015)):
            def coef(pays_inclus):
                return rho_spearman([effort[p] for p in pays_inclus],
                                    [evolution(series[p], debut, fin, taux) for p in pays_inclus])
            sans_un = [coef([p for p in pays_tries if p != exclu]) for exclu in pays_tries]
            print(f"{nom} {debut}-{fin}  {coef(pays_tries):+.3f}  "
                  f"exclusion successive d'un pays [{min(sans_un):+.3f}, {max(sans_un):+.3f}]")
    total_exports = {annee: sum(serie[annee] for serie in exports.values()) for annee in (2010, 2013)}
    print(f"Exportations agrégées vers les six, variation 2010-13 : {evolution(total_exports, 2010, 2013):+.2f} %")
    print("\nDécomposition DG Trésor en points de niveau du PIB et part étrangère")
    eta = ref["semi_elasticite_france_millesime_2014"]
    for an, total, etranger in zip(ref["annees"], ref["tresor_impact_niveau_pib_total"],
                                   ref["tresor_impact_niveau_pib_etranger"]):
        if total is not None:
            print(f"{an} total {total:+.2f}, national {total-etranger:+.2f}, étranger {etranger:+.2f}, "
                  f"part {100*etranger/total:.1f} %, solde cyclique conditionnel (100 %) {eta*etranger:+.2f}")
    print("Hypothèses de part cyclique, en 2013 uniquement")
    for part in (0, 0.5, 1):
        effet_cyclique = 0.0 if part == 0 else eta * part * ref["tresor_impact_niveau_pib_etranger"][2]
        print(f"{part:.0%} : {effet_cyclique:+.2f} point de solde/PIB")
    solde_2013 = ref["quest_impact_solde_paquet_2011_2013"][2]
    print(f"QUEST 2013, ratio descriptif gain de solde du paquet / effort français : "
          f"{100 * solde_2013 / ref['quest_effort_francais_cumule_2011_2013']:.1f} %")


if __name__ == "__main__":
    main()
