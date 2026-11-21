# -*- coding: utf-8 -*-
"""Produit corrections_demandees.md à partir de l'arbitrage d'A18.
Les dossiers des agents ne sont pas réécrits : ce fichier fait foi pour le rapport intégral.
Usage : python -I scripts/commun/extraire_corrections.py   (depuis resultats/)
"""
import csv
import datetime as dt
import os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = list(csv.DictReader(open(os.path.join(R, "donnees", "A18", "A18_arbitrage.csv"), encoding="utf-8-sig"), delimiter=";"))


def c(t):
    return " ".join(t.replace("|", "/").split())


o = ["# Corrections demandées aux dossiers de la cellule",
     "",
     "**Produit le " + dt.datetime.now().strftime("%d/%m/%Y à %H h %M") + " par `scripts\\commun\\extraire_corrections.py`**, à partir de l'arbitrage d'A18 (`donnees\\A18\\A18_arbitrage.csv`). "
     "Les dossiers des agents ne sont pas réécrits : là où un dossier et ce fichier diffèrent, **ce fichier fait foi** pour le rapport intégral. "
     "Statut : arbitrage interne à la cellule ; les audits de la V5 et les chiffres centraux ont été comparés à ceux de l'équipe Codex (C01), pas encore les conclusions.",
     "",
     "| Réf. | Contradicteur | Résultat visé | Verdict de l'arbitre | Modification demandée | Ce qui trancherait ou manque |",
     "|---|---|---|---|---|---|"]
for x in rows:
    o.append("| " + " | ".join(c(x[k]) for k in ("id", "contradicteur", "resultat_vise", "verdict", "modification_demandee_a_la_cellule", "piece_manquante_ou_ce_qui_trancherait")) + " |")
o += ["",
      "## Corrections reçues hors arbitrage (sondages de l'orchestrateur, audit, comparaison avec Codex)",
      "",
      "| Objet | Correction | Origine |",
      "|---|---|---|",
      "| Pouvoir d'amendement sur les dépenses (A08, transmission de la vague 2) | Un député peut déplacer des crédits entre programmes d'une même mission ; il ne peut pas augmenter le total d'une mission | A18, partie 1 ; rapport n° 1891, p. 99, relu à l'origine |",
      "| Budget de la Défense (vague 1) | 73,15 Md€ pensions comprises dans le projet de budget 2027 : la phrase de la V5 sur la charge de la dette tient | A18, partie 1 ; pièce relue à l'origine |",
      "| Nombre de recours à l'article 49.3 pour le budget de 2026 (A03) | Trois, non deux | A09, A18 |",
      "| Compte rendu de recette d'A15 (taux de 2,8 %) | Aucune combinaison ne stabilise la dette, même à 2,8 % | A17 ; sorties relues |",
      "| Plan version 2, causes « écartées » | La composition des ajustements n'est pas écartée : elle n'est pas départagée | A16 |",
      "| Part des dépenses dans le redressement canadien (S02) | Fourchette de 76 à 90 % selon la fenêtre, non « 82 % » | recalcul de l'orchestrateur |",
      "| « La France est le seul pays étudié dont la dette monte de 2015 à 2019 » | La Grèce aussi | A18, partie 2 ; recalcul de l'orchestrateur |",
      "| Audit de la V5, citation du HCFP « semble peu plausible » (classée inexacte) | La phrase a été prononcée en audition à l'Assemblée le 1er octobre 2026 par un membre du Haut Conseil ; elle n'est pas dans l'avis écrit | C01 ; compte rendu relu par l'orchestrateur dans la copie |",
      "| Audit de la V5 et A07 : taux à dix ans au-dessus de 5 % « le 21 et non le 22 octobre » | Objection non établie : la valeur quotidienne de la Banque de France passe 5 % le 22 (4,985 puis 5,126) | C01 ; page relue à l'origine par l'orchestrateur |",
      "| Audit de la V5 : « il faut désormais les voix d'un adversaire » (classée exacte) | Trop général : des abstentions peuvent suffire ; vrai pour le vote du budget de la Sécurité sociale de décembre 2025 | C01 ; non recontrôlé |",
      "| Suède 1993 : « un déficit deux fois plus profond », « environ 12 % » | « Deux fois » est exact en comptes actuels (10,7 % contre 5,07 % : 2,1 fois) ; « environ 12 % » est le chiffre des comptes de l'époque (12¼ %). Le « 1,8 fois hors aide aux banques » relevé par C01 mêle deux millésimes : il n'est pas retenu comme correction (rectifié le 21 novembre après relecture critique) | A12, C01 ; rapport recalculé par l'orchestrateur |",
      "| Transmission de la vague 1, décomposition de la dette | La fenêtre d'années doit être écrite : les deux équipes obtiennent 60 / 8 / 26 points à fenêtres identiques | C01 |",
      "| A05, A13, transmission : « aucune économie à résultat égal n'est établie » | Formule complétée : aucune n'est établie ; quatre sont suggérées sur pièce (santé et apprentissage avec un montant, logement et administration sans), aucune ne montre un résultat maintenu | S05 ; trois citations relues à l'origine par l'orchestrateur |",
      "| A12, transmission de la vague 2 : « aucun excédent primaire depuis 2002 », « ne dépend pas de la convention d'intérêts » | Le résultat tient avec les intérêts versés, à un milliard près : −1,0 Md€ en 2006 (0,05 % du PIB). Une variante de l'Insee (hors correction des services bancaires) fait de 2006 un excédent de 0,4 Md€. Formule exacte : aucun excédent primaire net depuis 2002, quasi-équilibre en 2006 | C02 ; recalcul de l'orchestrateur sur la base commune |",
      "| A15, contradicteurs, synthèse, rapport : « l'effort est d'environ 5 points », puis « entre 3,1 et 5,2 selon le point de départ » | Les deux formules sont inexactes. Réconciliation faite (C03) : 3,0 à 3,8 points de PIB au-delà du budget 2027 s\'il est adopté tel quel, 4,3 à 5,5 points en partant d\'une trajectoire sans aucune mesure, selon le modèle. Le budget 2027 compté ou non explique 1,5 des 2,1 points d'écart ; le reste tient à des hypothèses (croissance, prix, cycle, multiplicateur), sans erreur de calcul d'aucun côté | C03 ; table de passage refaite par l'orchestrateur |",
      "| A07, A01 : résidu de dette « non expliqué » de 26 points | La part d'après 1999 est en partie ventilée par instrument (2009 : 95,6 Md€ d'acquisitions d'actifs) ; le résidu d'avant 1999 (20 points) reste entier | C02, d'après un résultat de Codex ; non recontrôlé |",
      "| A15 : multiplicateur d'ensemble de 0,6 | Vaut pour une conjoncture normale à un ou deux ans ; en bas de cycle les pièces soutiennent 0,8 à 1,3 ; au-delà de deux ans rien n'est établi : les trajectoires se donnent en fourchette | S07 ; trois citations relues par l'orchestrateur |",
      "| A03, A12 : consolidation de 2011–2014 | Faite à 83 % par les recettes (lois de règlement) ; son coût en activité est simulé, non mesuré ; elle ne renseigne pas sur une consolidation par la dépense en conjoncture normale | S07 ; non recontrôlé |",
      "| A16, A15 : dépense primaire stable en volume comme chemin vers 3 % | Arithmétiquement juste, sans précédent d'exécution : la seule norme tenue dix ans autorisait +1,4 % par an en volume ; les normes de l'État ont tenu deux à quatre ans, surtout par changements de cible ou de périmètre ; aucune période de trois ans de baisse en volume depuis 1976 | S08 ; fenêtres recalculées par l'orchestrateur |",
      "| A04, S04 : baisses de prélèvements de 2018–2023, bénéficiaires | Réformes du capital : 80 % du gain aux 10 % les plus aisés (3,4 Md€) ; ensemble des mesures pour les ménages de 2017 à 2022, hausses et prestations comprises : 17 % aux 5 % les plus aisés ; taxe d'habitation, impôt sur les sociétés et impôts de production : part non publiée | S08 ; deux citations relues par l'orchestrateur |",
      "| S03 : décisions postérieures à 1974 = 3 à 7 % de la hausse des prestations de 1974–1985 | Fourchette instruite : 13 à 32 %, au plus 40 % ; le verdict (surtout des règles antérieures à 1974) tient ; premier poste décidé : préretraites et garantie de ressources, de 0,14 point de PIB en 1973 à 1,14 en 1985 | S10 ; page relue en image et total refait par l'orchestrateur |",
      "| S03 : garantie de ressources des licenciés datée de 1974 | Elle date de l'accord de 1972 ; la part décidée après 1974 est inférieure au coût total du poste | S10 ; non recontrôlé |",
      "| A15, A13, synthèse : « la dépense d'abord » et estompement de l'effet sur l'activité | Jugement étayé par une famille d'études (0,25 à 0,43 point de perte par point d'effort pour la dépense, 1,3 à plus de 2 pour l'impôt, à un ou deux ans), toutes sur la même base, contredites pour 2010–2014 ; l'estompement au-delà de deux ans n'est pas établi : donner une variante sans estompement (0,4 à 0,65 point à trois-cinq ans) | S13 ; deux citations relues par l'orchestrateur |",
      "| A15 : effet d'une consolidation sur le ratio de dette | Les consolidations ne réduisent pas le ratio de dette en moyenne (FMI, avril 2023) ; en France, à un multiplicateur de 0,6, le ratio est inchangé la première année (seuil 0,596) | S13 ; citation relue et seuil recalculé par l'orchestrateur |",
      "| Synthèse, A09 : « ce qui manque, c'est un accord sur l'effort » au sens large (hypothèse H0040) | Testée : ni soutenue ni contredite. Les majorités plus éclatées n'ont pas fait pire (13 législatures, test faible) ; la procédure budgétaire de l'État était la plus centralisée de 12 pays au début des années 1990 ; le canal du financement éclaté n'est pas testable ; le nombre de ministres dépensiers n'est pas testé. La phrase reste une interprétation | S11 ; pré-enregistrement et rejeu contrôlés par l'orchestrateur |",
      "| A09, arbitrage, synthèse, rapport : « les 37 budgets de majorité absolue sont tous en déficit » employé comme test | La phrase ne prouve rien par comparaison : les 51 exercices sont en déficit. Formule exacte : 42 budgets sur 51 ont été votés par une majorité absolue (22 par un seul groupe, 20 par une coalition) et le déficit a persisté ; les excédents primaires ne sont pas plus fréquents sous majorité absolue (6 sur 42) que sans (3 sur 9) ; aucun sous la majorité absolue d'un seul groupe. Erreur de raisonnement partagée par la cellule, l'arbitre et l'orchestrateur | S12 ; décomptes refaits par l'orchestrateur |",
      "| S08 : taxe d'habitation, « part des 10 % les plus aisés non publiée » | Chiffrée : 21,2 % du gain cumulé de 2018 à 2023 au dixième le plus aisé, 36,6 % aux deux derniers dixièmes, 27,3 % à la moitié la plus modeste ; deux phases de sens opposé. Impôt sur les sociétés et impôts de production : gain relatif croissant avec la taille ; bénéficiaire final non mesuré | S14 ; tableau de l'Insee retéléchargé et parts refaites par l'orchestrateur |",
      ""]
open(os.path.join(R, "corrections_demandees.md"), "w", encoding="utf-8", newline="").write("\n".join(o))
print(len(rows), "lignes d'arbitrage ->", "corrections_demandees.md")
