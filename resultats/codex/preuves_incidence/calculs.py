"""Contre-enquête du Constat. Exécuter avec Python 3, sans dépendance ni réseau.

Affiche les contrôles et les sensibilités. Les niveaux monétaires sont exprimés
en millions d'euros sauf mention contraire. Les sources et les limites de chaque
calcul sont documentées dans ../incidence.md aux identifiants correspondants.
"""

from itertools import product


def pct(numerateur, denominateur):
    return 100 * numerateur / denominateur


def indexation(assiette, fraction_eligible, ecart_indexation, perte_recettes,
               multiplicateur, sensibilite_solde, mise_en_oeuvre):
    """Choc relatif sur la pension de référence, retour fiscal direct puis demande."""
    brut = assiette * fraction_eligible * ecart_indexation
    revenu_disponible_perdu = brut * (1 - perte_recettes)
    net = revenu_disponible_perdu * (1 - multiplicateur * sensibilite_solde)
    return brut, net - mise_en_oeuvre


if __name__ == "__main__":
    print("C4101 | 2019 corrigé et variation contre 2018 (points de PIB)")
    print(round(3.0 - 0.9, 2), round((3.0 - 0.9) - 2.3, 2))

    print("C4102 | Pinel, reste cumulé estimé après fin 2023 (Md€)")
    print([round(total - 7.3, 1) for total in (10, 12)])

    print("C4103 | part de la hausse 2019–2020 des embauches, comité, graphique p.6")
    print(round(pct(80000, 629600 - 478800), 1))

    print("C4104 | deux reports sociaux, Md€ et % des économies de pensions attendues")
    for invalidite in (1.2, 1.5):
        total = invalidite + 0.6
        print(round(total, 2), round(pct(total, 14), 1))

    print("C4105 | variation observée des patients dentaires 2019–2021 (%)")
    print(round(pct(5.16 - 4.75, 4.75), 1))

    print("C4106 | ranibizumab, gain mécanique sur base des volumes 2024 (M€)")
    for conversion in (0.10, 0.25, 0.50):
        print(conversion, round(243.3 * 0.25 * conversion, 2))

    print("C4107 | calibration des pensions, brut et net partiel année pleine (M€)")
    assiette_cnav = 120437.5
    jeux = {
        "défavorable": (0.4, 0.22, 1.2, 0.5, 15),
        "intermédiaire": (0.6, 0.15, 0.7, 0.45, 10),
        "favorable": (0.8, 0.08, 0.3, 0.4, 5),
    }
    for nom, (eligible, direct, mult, sensibilite, gestion) in jeux.items():
        for taux in (0.005, 0.01):
            brut, net = indexation(assiette_cnav, eligible, taux, direct, mult,
                                   sensibilite, gestion)
            print(nom, taux, round(brut, 1), round(net, 1))
    print("C4108 | cas intermédiaire, gain annuel net de l'option à 0,5 %,")
    print("avec 0/50/100 % d'écart déjà présent dans la trajectoire de référence")
    for inclus in (0, 0.5, 1.0):
        if inclus == 1:
            net = 0.0  # Pas de modification, pas de frais nouveaux.
        else:
            _, net = indexation(assiette_cnav, 0.6, 0.005 * (1-inclus),
                                0.15, 0.7, 0.45, 10)
        print(inclus, round(net, 1))

    print("C4109 | stress croisé de toutes les hypothèses, amplitude (M€)")
    combinaisons = product((0.4, 0.6, 0.8), (0.08, 0.15, 0.22),
                           (0.3, 0.7, 1.2), (0.4, 0.45, 0.5), (5, 10, 15))
    nets = [indexation(assiette_cnav, e, 0.005, d, m, s, c)[1]
            for e, d, m, s, c in combinaisons]
    print(len(nets), round(min(nets), 1), round(max(nets), 1))

    print("C4110 | parcours hospitaliers, gain en M€ au régime atteint à quatre ans")
    for fraction_deployee, fraction_liberable in ((0.25, 0.4), (0.5, 0.7), (0.8, 0.9)):
        gain = 1300 * fraction_deployee * fraction_liberable
        print(fraction_deployee, fraction_liberable, round(gain, 1))
    print("C4111 | croissance PIB, emploi et productivité par tête, écart")
    print("de rythme 1974–1991 moins 1962–1973, en points par an")
    print([round(nouveau - ancien, 1) for ancien, nouveau in
           ((5.7, 2.6), (0.7, 0.5), (5.0, 2.1))])

    assert round((3.0 - 0.9) - 2.3, 2) == -0.20
    assert round(pct(80000, 629600 - 478800), 1) == 53.1
    assert round(pct(2.1, 14), 2) == 15.0
    assert abs(243.3 * 0.25 * 0.50 - 30.4125) < 1e-9
    assert len(nets) == 243 and max(nets) < assiette_cnav * 0.8 * 0.005
    assert abs(1300 * 0.5 * 0.7 - 455) < 1e-9
