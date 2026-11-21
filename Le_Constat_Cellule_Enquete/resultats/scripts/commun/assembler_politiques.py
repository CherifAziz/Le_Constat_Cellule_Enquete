# -*- coding: utf-8 -*-
"""Assemble politiques.md à partir des tables des agents, sans rien ajouter :
mesures d'A13 et d'A14, appartenance aux combinaisons d'A15, incidence de S04,
objectifs et horizons d'A15, trajectoires des combinaisons.

Usage : python -I scripts/commun/assembler_politiques.py   (depuis resultats/)
Sortie : politiques.md
"""
import csv
import datetime as dt
import os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def lire(*chemin):
    return list(csv.DictReader(open(os.path.join(R, "donnees", *chemin), encoding="utf-8-sig"), delimiter=";"))


def fr(x, n=1):
    try:
        return f"{float(x):.{n}f}".replace(".", ",")
    except (ValueError, TypeError):
        return "—"


def c(t, n=140):
    t = " ".join(str(t).replace("|", "/").split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " […]"


a13, a14 = lire("A13", "A13_table_mesures.csv"), lire("A14", "A14_table_mesures.csv")
harm = {x["id"]: x for x in lire("A15", "A15_mesures_harmonisees.csv")}
inc = {x["id"]: x for x in lire("S04", "S04_table_incidence.csv")}
comb = lire("A15", "A15_combinaisons.csv")
obj = lire("A15", "A15_objectifs_horizons.csv")


def combis(i):
    h = harm.get(i)
    return "—" if not h else " ".join(k[-2:] for k in ("dans_K1", "dans_K2", "dans_K3", "dans_K4", "dans_K5") if h.get(k) == "oui") or "aucune"


def payeur(i):
    x = inc.get(i)
    if not x:
        return "non instruit par S04 (moins de 1 Md€ ou hors enveloppe centrale)"
    noms = [("p_retraites", "retraités"), ("p_autres_menages", "autres ménages"), ("p_menages_non_ventiles", "ménages non ventilés"),
            ("p_agents_publics", "agents publics"), ("p_entreprises", "entreprises"), ("p_collectivites", "collectivités"), ("p_non_ventile", "non ventilé")]
    out = []
    for k, n in noms:
        try:
            v = float(x.get(k) or 0)
        except ValueError:
            v = 0
        if v > 0.005:
            out.append(f"{n} {round(v * 100)} %")
    s = ", ".join(out) or "non ventilé"
    if x.get("top10_bas") and x.get("bas50_bas"):
        s += f" ; dixième aisé {fr(float(x['top10_bas']) * 100, 0)}–{fr(float(x['top10_haut'] or x['top10_bas']) * 100, 0)} %, moitié modeste {fr(float(x['bas50_bas']) * 100, 0)}–{fr(float(x['bas50_haut'] or x['bas50_bas']) * 100, 0)} %"
    return s


o = ["# Politiques de redressement : mesures, combinaisons, payeurs",
     "",
     "**Table assemblée le " + dt.datetime.now().strftime("%d/%m/%Y à %H h %M") + " par `scripts\\commun\\assembler_politiques.py`.** Elle n'ajoute aucun chiffre : elle rapproche les tables d'A13 (dépense), d'A14 (recettes), d'A15 (combinaisons et objectifs) et de S04 (qui paie). "
     "**Ce n'est ni une recommandation ni un programme** : la charte interdit à la cellule de prescrire. Statut : dossiers passés en recette avec réserves ; arbitrage dans `corrections_demandees.md`, qui fait foi. "
     "Rendements en milliards d'euros de 2025, nets des effets en retour estimés par chaque agent ; les deux portefeuilles n'emploient pas la même méthode de passage du brut au net.",
     "",
     "## 1. Ce que les objectifs demandent (A15)",
     "",
     "Effort à voter contre la trajectoire sans aucune mesure (déficit de 6,5 % en 2027 avant le budget, 7,3 % en 2030). **Trois grandeurs à ne pas confondre** : cet effort ; l'écart à un instant (62 Md€ entre le déficit de 2025 et 3 %) ; le rendement d'un portefeuille.",
     "",
     "**Selon le point de départ et le modèle (réconciliation C03)** : pour stabiliser la dette, 4,3 à 5,5 points de PIB en partant d'une trajectoire sans aucune mesure ; 3,0 à 3,8 points au-delà du budget 2027 s'il est adopté tel quel (il ne l'est pas au 21 novembre 2026). Le tableau ci-dessous est celui du modèle de la cellule, sans le budget 2027.",
     "",
     "| Objectif | Horizon | Mesures nécessaires à l'horizon (points de PIB) | En Md€ de 2025 | Dette à l'horizon (% du PIB) |",
     "|---|---|---|---|---|"]
for x in obj:
    if x["reference"].startswith("A"):
        h = x["horizon"]
        nom = {'equilibre': 'équilibre', 'trois': 'déficit à 3 %', 'stabilisation': 'stabilisation de la dette', 'baisse': 'baisse du ratio de dette'}.get(x['objectif'], x['objectif'])
        o.append(f"| {nom} | {h} | {fr(x.get('mesures_' + h + '_pts'), 1)} | {fr(x['mesures_horizon_mdeur_echelle2025'], 0)} | {fr(x['dette_horizon'], 0)} |")
o += ["",
      "## 2. Combinaisons sans double compte (A15)",
      "",
      "Lecture corrigée par l'arbitrage : aucune combinaison **des mesures déjà chiffrées** n'atteint 3 % ni ne stabilise la dette avant 2035, même avec un taux à l'émission de 2,8 % ; une dépense primaire stable en volume y parviendrait vers 2035 dans le même modèle, sans qu'aucune période française de trois ans l'ait tenue.",
      "",
      "| Combinaison | Mesures | Rendement 2030 (Md€) | Déficit 2030 | Déficit 2035 | Dette 2035 |",
      "|---|---|---|---|---|---|"]
for x in comb:
    o.append(f"| {c(x['combinaison'].replace(' | ', ' — '))} | {x['n_mesures']} | {fr(x['statique_2030_mdeur_ech2025'], 0)} | {fr(x.get('deficit_2030'))} | {fr(x.get('deficit_2035'))} | {fr(x.get('dette_2035'), 0)} |")
o += ["",
      "K1 : enveloppes centrales, retraites par le gel. K2 : par la fin de l'abattement. K3 : K1 sans les mesures rejetées au Parlement. K4 : prudente. K5 : ambitieuse.",
      "",
      "## 3. Mesures du portefeuille « dépense » (A13)",
      "",
      "| Id | Mesure | Net 2030 si adoptée | Net 2030 après décote | Combinaisons | Qui paie (S04) | Preuve |",
      "|---|---|---|---|---|---|---|"]
for x in a13:
    o.append(f"| {x['id']} | {c(x['mesure'])} | {fr(x['net_si_adopte_central_2030'])} | {fr(x['net_apres_decote_central_2030'])} | {combis(x['id'])} | {c(payeur(x['id']), 170)} | {c(x['niveau_preuve'], 40)} |")
o += ["",
      "## 4. Mesures du portefeuille « recettes » (A14)",
      "",
      "| Id | Mesure | Net 2030 | Statut | Combinaisons | Qui paie (S04) | Preuve |",
      "|---|---|---|---|---|---|---|"]
for x in a14:
    o.append(f"| {x['id']} | {c(x['nom'])} | {fr(x['net_central_2030'])} | {c(x['statut'], 50)} | {combis(x['id'])} | {c(payeur(x['id']), 170)} | {c(x['niveau_preuve'], 40)} |")
o += ["",
      "## 5. Limites à garder avec cette table",
      "",
      "- Un profil par niveau de vie n'est publié que pour un cinquième des montants de chaque portefeuille ; les parts par dixième et par moitié sont des calculs de S04 à partir d'effets publiés.",
      "- Les décotes d'exécution d'A13 sont un jugement chiffré calé sur cinq précédents ; A14 applique à la place un test parlementaire.",
      "- L'ordre des multiplicateurs (transferts au-dessus des impôts) est une hypothèse ; le multiplicateur d'ensemble de 0,6 n'est pas validé sur le passé.",
      "- Aucune mesure d'emploi, d'efficience ou d'impôt large non chiffrée par A13 ou A14 ne figure ici.",
      ""]
open(os.path.join(R, "politiques.md"), "w", encoding="utf-8", newline="").write("\n".join(o))
print("mesures A13:", len(a13), "| A14:", len(a14), "| combinaisons:", len(comb), "| objectifs:", len([x for x in obj if x['reference'].startswith('A')]))
