"""Recalculer les écarts H09 à partir des seuls tableaux publics transcrits."""

import json
from pathlib import Path


def cour(data):
    print("Séjours longs en 2024 | aval implicite (M€) | seuil (%) | aval par jour hospitalier (€)")
    jours_total = 0
    brut_total = 0
    net_total = 0
    for champ, jours, cout_moyen, brut, net in data["lignes"]:
        aval = brut - net
        seuil = 100 * aval / brut
        print(f"{champ}: {aval} | {seuil:.1f} | {1_000_000 * aval / jours:.1f}")
        jours_total += jours
        brut_total += brut
        net_total += net
    assert [jours_total, brut_total, net_total] == data["total_publie_jours_brut_net"]
    aval_total = brut_total - net_total
    print(f"Ensemble: {aval_total} | {100 * aval_total / brut_total:.1f} | "
          f"{1_000_000 * aval_total / jours_total:.1f}")
    print(f"Gain aux deux extrêmes du scénario (M€): {-aval_total} à {net_total}")


def tinland(data):
    print("\nUn Chez-soi d’abord | différence des moyennes intervention − habituel à deux ans")
    for indicateur, intervention, habituel, rr, bas, haut in data["lignes"]:
        print(f"{indicateur}: {intervention - habituel:+.2f} | RR publié {rr:.2f} [{bas:.2f} ; {haut:.2f}]")
    print(f"Différence annoncée séparément par le résumé: {data['ecart_total_annonce_resume_euros']} €")


def diva(data):
    print("\nDiVa-1 | différence de remboursement moyen intensif − habituel à deux ans")
    ecarts = {}
    for parcours, poste, intensif, habituel, p in data["lignes"]:
        ecarts[parcours, poste] = intensif - habituel
        print(f"{parcours}, {poste}: {intensif - habituel:+} € | p publié {p:.4f}")
    for parcours in data["effectifs_tableaux_couts_deux_ans_tous_bras"]:
        assert ecarts[parcours, "Total"] == ecarts[parcours, "Hôpital"] + ecarts[parcours, "Ville"]
    taux = data["hospitalisations_completes_non_programmees_deux_ans"]
    print(f"Réhospitalisations non programmées, deux pathologies, différence en points: "
          f"{taux['intensif_pourcent'] - taux['habituel_pourcent']:+.1f} | "
          f"p publié {taux['p_comparaison_publiee']:.4f}")


if __name__ == "__main__":
    observations = json.loads(Path(__file__).with_name("observations.json").read_text(encoding="utf-8"))
    cour(observations["cour"])
    tinland(observations["tinland"])
    diva(observations["diva"])
    projet = observations["hotels"]["montpellier"]
    print(f"\nMontpellier, solde du projet 2017–18: {projet['recettes'] - projet['depenses']:+} €")
