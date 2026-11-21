# -*- coding: utf-8 -*-
"""Assemble audit_factuel_V5.md : audit de la cellule (A18, passe 2) croisé avec la
concordance établie par C01 avec l'audit de l'équipe Codex. N'ajoute aucun verdict :
là où C01 a tranché contre la cellule, la ligne est marquée « révisé » avec la pièce.
Aucune formulation de remplacement.

Usage : python -I scripts/commun/assembler_audit_final.py   (depuis resultats/)
Sorties : audit_factuel_V5.md ; donnees/commun/audit_V5_final.csv
"""
import collections
import csv
import datetime as dt
import os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
a18 = {x["identifiant"]: x for x in csv.DictReader(open(os.path.join(R, "donnees", "A18", "A18_audit_V5_passe2.csv"), encoding="utf-8-sig"), delimiter=";")}
c01 = list(csv.DictReader(open(os.path.join(R, "donnees", "C01", "C01_concordance_audit.csv"), encoding="utf-8-sig"), delimiter=";"))


def c(t, n=200):
    t = " ".join(str(t).replace("|", "/").split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " […]"


lignes = []
for x in c01:
    i = x["identifiant"]
    a = a18.get(i, {})
    v = x["verdict_cellule_M2_passe2"] or a.get("verdict_M2_passe2", "")
    tr = x["tranchage"]
    final, note = v, ""
    low = tr.lower()
    if x["concordance"] == "désaccord":
        if "faveur de codex" in low:
            final, note = "révisé après comparaison", "tranché en faveur de l'autre équipe"
        elif "faveur de la cellul" in low:
            note = "désaccord tranché en faveur de la cellule"
        elif low.startswith("non tranché"):
            note = "désaccord non tranché"
        elif "non contradictoire" in low or "faits compatibles" in low:
            note = "désaccord apparent : faits compatibles, verdict de la cellule maintenu"
        else:
            final, note = "à préciser après comparaison", c(tr, 110)
    elif x["concordance"] == "Codex seul":
        final, note = "non audité par la cellule", "relevé par l'autre équipe seulement"
    elif x["concordance"] == "cellule seule":
        note = "audité par la cellule seulement"
    lignes.append({"identifiant": i, "ligne_V5": x["ligne_V5"], "affirmation": x["affirmation"], "verdict_cellule": v, "accord_avec_autre_equipe": x["concordance"],
                   "verdict_apres_comparaison": final, "note": note, "piece": x["piece_qui_tranche_ou_trancherait"] or a.get("piece_reprise_A18", ""),
                   "motif_cellule": a.get("motif", ""), "niveau_preuve": a.get("niveau_preuve", "")})

os.makedirs(os.path.join(R, "donnees", "commun"), exist_ok=True)
with open(os.path.join(R, "donnees", "commun", "audit_V5_final.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(lignes)

cv = collections.Counter(x["verdict_cellule"] or "sans verdict" for x in lignes)
cf = collections.Counter(x["verdict_apres_comparaison"] or "sans verdict" for x in lignes)
ca = collections.Counter(x["accord_avec_autre_equipe"] for x in lignes)

o = ["# Audit factuel du script V5 du 13 novembre 2026",
     "",
     "**Fichier assemblé le " + dt.datetime.now().strftime("%d/%m/%Y à %H h %M") + " par `scripts\\commun\\assembler_audit_final.py`.** Il croise l'audit ligne à ligne de la cellule (A18 : première passe aveugle figée, puis confrontation) avec l'audit indépendant de l'équipe Codex, comparés par la mission C01. "
     "**Il ne propose aucune formulation de remplacement et ne prend aucune décision éditoriale.** Table complète : `donnees\\commun\\audit_V5_final.csv`.",
     "",
     "Limites : l'autre équipe écrit en prose, sans verdict par ligne ; l'accord ou le désaccord est une lecture de C01, à environ cinq lignes près. Les lignes en accord n'ont pas été recontrôlées à la source après la comparaison. « Exact » couvre aussi « exact sous condition » : la condition est dans la table.",
     "",
     "## 1. Décompte",
     "",
     "| | Nombre de lignes |",
     "|---|---|",
     f"| Lignes du fichier | {len(lignes)} |"]
for k, n in ca.most_common():
    o.append(f"| dont : {k} | {n} |")
o += ["", "| Verdict de la cellule | Lignes | | Après comparaison | Lignes |", "|---|---|---|---|---|"]
ks = sorted(set(cv) | set(cf), key=lambda z: -(cv.get(z, 0) + cf.get(z, 0)))
for k in ks:
    o.append(f"| {k} | {cv.get(k, 0)} | | {k} | {cf.get(k, 0)} |")


def bloc(titre, filtre, intro):
    sel = [x for x in lignes if filtre(x)]
    o.extend(["", "## " + titre + f" ({len(sel)})", "", intro, "", "| Ligne | Affirmation du script | Verdict de la cellule | Motif ou pièce | Autre équipe |", "|---|---|---|---|---|"])
    for x in sel:
        o.append(f"| {x['identifiant']} | {c(x['affirmation'], 150)} | {x['verdict_cellule']} | {c(x['motif_cellule'] or x['piece'], 210)} | {x['accord_avec_autre_equipe']}{' ; ' + x['note'] if x['note'] else ''} |")


bloc("2. Lignes révisées ou à préciser après la comparaison", lambda x: x["verdict_apres_comparaison"] in ("révisé après comparaison", "à préciser après comparaison"),
     "Lignes où la comparaison a donné tort, en tout ou en partie, à l'audit de la cellule. La pièce qui tranche est dans la table complète.")
bloc("3. Lignes classées inexactes par la cellule", lambda x: x["verdict_cellule"] == "inexact" and x["verdict_apres_comparaison"] == "inexact", "")
bloc("4. Lignes classées trop générales", lambda x: x["verdict_cellule"] == "trop général" and x["verdict_apres_comparaison"] == "trop général", "")
bloc("5. Lignes classées non démontrées", lambda x: x["verdict_cellule"] == "non démontré" and x["verdict_apres_comparaison"] == "non démontré", "")
bloc("6. Lignes non vérifiées", lambda x: x["verdict_cellule"] == "non vérifié", "")
bloc("7. Désaccords non tranchés entre les deux équipes", lambda x: x["note"] == "désaccord non tranché", "Cinq portent sur un jugement, deux sur une pièce non consultée.")
bloc("8. Lignes relevées par l'autre équipe seulement", lambda x: x["accord_avec_autre_equipe"] == "Codex seul", "")
o += ["", "## 9. Ce que cet audit ne fait pas", "",
      "- Il ne dit pas quoi écrire à la place : la charte l'interdit avant la synthèse éditoriale.",
      "- Il ne juge pas la thèse d'ensemble du documentaire : les phrases qui la portent sont classées une à une.",
      "- Il ne garantit pas les lignes « exactes » : une quinzaine reposent sur une source secondaire (voir `journal\\recette_A18_partie1.md`).", ""]
open(os.path.join(R, "audit_factuel_V5.md"), "w", encoding="utf-8", newline="").write("\n".join(o))
print(len(lignes), "lignes |", dict(ca), "|", dict(cf))
