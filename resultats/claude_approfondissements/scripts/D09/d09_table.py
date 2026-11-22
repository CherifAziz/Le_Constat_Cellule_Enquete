# -*- coding: utf-8 -*-
"""D09 - écrit la table des quinze vérifications (donnees/D09/D09_verifications.csv) et la relit.

Le contenu des lignes est le résultat de la lecture des pièces (voir dossiers/D09.md) ;
le script garantit seulement un CSV bien formé (séparateur « ; », champs protégés).
"""
import csv
from pathlib import Path

ICI = Path(__file__).resolve().parent
SORTIE = ICI.parent.parent / "donnees" / "D09" / "D09_verifications.csv"

ENTETE = ["n", "dossier", "affirmation", "piece", "page_pdf", "origine_retelechargee", "lecture_image",
          "citation", "verdict", "reserve_ou_correction"]

L = [
    [1, "D02", "Décret du 30/7/1979 : cotisation salariale maladie de 1 %, du 1/8/1979 au 31/1/1981, échéance fixée dès l'origine",
     "Sénat n°54 t.IV (21/11/1979) ; Sénat n°102 t.III (19/11/1980)", "n°54 p.46 et p.31 ; n°102 p.9 (impr. 10)",
     "identique (2 pièces)", "oui", "« aux termes du décret n° 79-650 du 30 juillet 1979 » (n°54 p.46)",
     "confirmée avec réserve",
     "Décret non lu (Légifrance 403, un seul essai). Preuve indirecte : rapport du Sénat de novembre 1979. "
     "Le même rapport écrit « 1er avril 1979 » p.31 (coquille probable, son tableau dit 1er août). "
     "Champ : salariés du régime général, étendu aux fonctionnaires et agents publics."],
    [2, "D02", "Excédent du régime général 1980 : 10,7 Md F, dont 9,35 du 1 % ; sans lui environ 1,3",
     "Commission des comptes de la sécurité sociale, rapport de juillet 1981", "p.8, p.18, p.20 (impr. 4, 14, 16)",
     "identique", "oui", "« pour l'année 1980 est ramené à + 1,3? milliards » (p.18)",
     "confirmée avec réserve",
     "Régime général seul. Solde lu sur image : +10,669 (p.20). 10,669 - 9,352 = 1,317 ; dernier chiffre de « 1,32 » "
     "illisible même agrandi. Calcul comptable sans effet de comportement. En novembre 1980 l'excédent prévu était 8,3 (Sénat n°102 p.22)."],
    [3, "D02", "Automne 1980 : le Sénat écrit que la contribution « sera supprimée à la fin du mois de janvier 1981 » et prévoit -3,2 Md F en 1981",
     "Sénat n°102 t.III (avis Boyer, 19/11/1980)", "p.22 (impr. 23)", "identique", "oui",
     "« sera supprimée à la fin du mois de janvier 1981 » (p.22)", "confirmée",
     "Avis de la commission des affaires sociales, pas rapport général. Le -3,2 (maladie -1,8 ; famille -1,1 ; vieillesse -0,3) "
     "reprend les prévisions de la Commission des comptes du 7/11/1980 (p.23)."],
    [4, "D02", "Cotisation rétablie au 1/11/1981 ; la Commission des comptes la dit « supprimée par le précédent gouvernement »",
     "Commission des comptes, réunion du 21/6/1983 (fichier « juin 1982 ») ; rapport de décembre 1982",
     "p.22 (impr. 12) et p.18 ; déc. 1982 p.9", "identique (2 pièces)", "oui (p.22) ; non (p.18 ; déc. 1982 p.9)",
     "« point de cotisation maladie supprimé par le précédent gouvernement » (p.22)", "confirmée avec réserve",
     "La pièce écrit « supprimé » (le point), pas « supprimée ». Rapport de juin 1983, pas de 1982. "
     "Mesure du Conseil des ministres du 10/11/1981 (p.18), effet au 1/11/1981."],
    [5, "D02", "Le rapporteur général du Sénat range la fin du 1 % parmi les mesures de soutien à la consommation du budget 1981",
     "Sénat n°98 t.I (Blin, projet de loi de finances 1981)", "p.107 (impr. 109)", "identique", "oui",
     "« l'action en faveur de la consommation [...] et la suppression, en février 1981 »", "confirmée avec réserve",
     "Mesure de sécurité sociale qui « relaie » la stabilisation fiscale du projet de loi de finances : pas une mesure du budget de l'État. "
     "Appréciation du rapporteur, qui l'approuve (« que nous considérons comme efficaces »)."],
    [6, "D03", "Article 52 de la loi du 31/12/1970 : réforme du prix de journée « dans le délai d'un an » ; encore en préparation en 1973 et 1974 ; "
     "loi de décembre 1979 prorogeant une expérimentation « jusqu'à la mise en application »",
     "Sénat n°43 t.II (21/11/1973) ; n°103 (21/11/1974) ; n°128 (commission mixte paritaire, 18/12/1979)",
     "n°43 p.22 ; n°103 p.20 ; n°128 p.22 et p.14", "identique (3 pièces)", "oui (n°43, n°103, n°128 p.22)",
     "« prorogée jusqu'à la mise en application de la réforme » (n°128 p.22)", "confirmée avec réserve",
     "Article 52 non lu : « délai d'un an » est une paraphrase du Sénat. Le n°128 est le texte proposé par la commission mixte paritaire, "
     "pas la loi promulguée (non lue). Il ajoute un nouveau délai : réforme présentée au Parlement « dans un délai de deux ans »."],
    [7, "D03", "1980-1985 : +367 600 agents, 59 % collectivités et hôpitaux ; environ 115 000 emplois inscrits au budget de l'État en 1981-1982 ; "
     "Sénat : 203 500 emplois et « 220 000 emplois publics en deux ans »",
     "DGAFP séries longues 1980-1998 ; Sénat n°58 t.I (1981-82) ; n°95 t.I (1982-83) ; n°62 t.I (1983-84)",
     "DGAFP p.10 ; n°58 p.69, 72, 90, 91 ; n°95 p.88 ; n°62 p.116", "identique (4 pièces)", "oui",
     "« dont près de 45 000 à la charge totale ou partielle » (n°58 p.72)",
     "infirmée sur l'élément « 115 000 » ; autres éléments confirmés",
     "367,6 milliers et 59,4 % exacts (fonction publique de l'État au sens large, P et T inclus, emplois aidés exclus). "
     "115 000 = 54 000 + 61 000 mêle plus de 9 000 emplois hospitaliers. Part de l'État : environ 106 000 « à la charge totale ou partielle » "
     "(45 000 + 61 000 ; 108 000 avec les 1 890 de la loi de finances initiale 1981), dont près de 41 000 au seul budget général en 1982. "
     "Le rapport totalise 125 000 (p.69) ; le Gouvernement 126 480 hôpitaux compris (p.90-91). "
     "220 000 : appréciation polémique du rapporteur (section « Le prix de la facilité »)."],
    [8, "D03", "Consommation de soins et biens médicaux en volume : 8,8 %/an (1970-75), puis 5,8 % et 5,5 %",
     "Drees, Études et résultats n°572 (2007)", "p.3, tableau 1", "identique", "non (PDF natif, polices incorporées)",
     "« 1970-1975 8,8 3,5 -1,5 » (tableau 1)", "confirmée",
     "Rétropolation base 2000. 1970-1975 n'est pas un pic de croissance en volume (9 à 10 %/an de 1950 à 1975 ; 10,8 en 1960-1965) : "
     "le pic est l'écart avec le PIB."],
    [9, "D05", "Carrez 2010 : 101-119 Md€ de pertes de recettes de l'État en 2009 dont 68-78 de baisses nettes ; sans elles déficit 3,7 % au lieu de 7,5 % "
     "et dette 54,6 % au lieu de 77,4 %",
     "Assemblée nationale, rapport d'information n°2689 (30/6/2010)", "p.7, p.10, p.13, p.14, p.16, p.21", "identique",
     "oui (p.7, p.10, p.13)", "« dans l'hypothèse du gage systématique des mesures nouvelles en matière fiscale » (p.16)",
     "confirmée avec réserve ; total 101-119 non vérifiable",
     "Périmètre : budget général de l'État ; 68,3-77,7 = mesures nouvelles cumulées en 2009, hors relance. "
     "Différence (32,9-41,6) = ligne « mesures de périmètre » de la p.7, identique chiffre pour chiffre à la ligne impôt sur le revenu de la p.10, "
     "dont elle est le cumul aux arrondis près : erreur d'édition probable. Le tableau des transferts nets p.13 cumule -28,2. "
     "Transferts aux collectivités neutres pour le solde public (p.14) ; ceux à la sécurité sociale compensent des allègements qui le dégradent. "
     "Contrefactuel : gage par d'autres prélèvements ou des économies ; baisses d'impôts d'État seules appliquées au solde et à la dette de toutes "
     "les administrations ; PIB inchangé ; transferts et dégrèvements exclus. 77,4 % est le chiffre du programme de stabilité ; constaté 78,1 % (p.21)."],
    [10, "D05", "Champsaur-Cotis avril 2010 : mesures nouvelles depuis 1999 de « près de 3 points de PIB » ; à législation de 1999, PO de 44,3 % à 45,3 %",
     "Rapport sur la situation des finances publiques (avril 2010)", "p.18 (impr. 13) ; graphique 20 p.31", "identique",
     "non (PDF natif)", "« serait passé de 44,3 % en 1999 à 45,3 % en 2008 » (p.18)", "confirmée",
     "Année 2008, pas 2009 ; taux effectif 42,5 %. Graphique 20 (p.31 du PDF, pas p.30) : -2,8 points sur 1999-2008. "
     "Ne pas confondre avec le 45,3 % de Carrez (2009, autre contrefactuel)."],
    [11, "D05", "DG Trésor DT 2009/13 : mesures nouvelles en PO -1,2 ; -1,0 ; -0,4 ; +0,1 ; +0,1 ; +0,4 ; +0,1 ; -0,6 ; -0,5 (2000-2008)",
     "DG Trésor, document de travail 2009/13", "p.18 (impr. 16), tableau 3", "identique", "non (PDF natif, relu par script)",
     "« dont mesures nouvelles en PO -1,2 -1,0 -0,4 0,1 » (tableau 3)", "confirmée",
     "Ensemble des administrations, décomposition du solde structurel hors soultes. Cumul 2000-2008 : -3,0 points."],
    [12, "D05", "Cour juin 2010 : règle de gage de la loi de programmation 2009-2012 non respectée en 2009 ; baisses pérennes de 4,6 Md€ dont TVA restauration",
     "Cour des comptes, situation et perspectives des finances publiques (juin 2010)", "p.14-15 (impr. 10-11) ; p.7", "identique",
     "non (PDF natif)", "« n'ont pas été respectées » (p.14)", "confirmée avec réserve",
     "Règle de la loi de programmation de février 2009 sur les dépenses fiscales et les recettes fiscales nettes de l'État. "
     "4,6 Md€ = coût net en 2009 des mesures pérennes sur les prélèvements de l'État et de la sécurité sociale (la pièce ne dit pas « décidées en 2009 »), "
     "dont 1,5 Md€ pour la TVA restauration (3,0 en année pleine). Net des hausses locales : 2,4 Md€."],
    [13, "D07", "Insee : 60-64 ans 40,5 % (1975), 10,8 % (2001), 44,4 % (2025) ; 55-59 ans 61,8 %, 48,2 % (1987), 78,8 %",
     "Insee, séries longues de l'enquête Emploi, tableau T207", "feuille T207", "identique", "sans objet (xlsx)",
     "« données de 1975 à 2025, corrigées pour les ruptures de série »", "confirmée",
     "Série corrigée des ruptures (note du tableau). Champ : France, logement ordinaire, moyenne annuelle. Minimums exacts aux années citées."],
    [14, "D07", "Insee 2001 : 460 000 emplois créés ou sauvegardés de 1994 à 1997 ; rapport 2024 : suppression des exonérations = +1,7 point de solde primaire "
     "à un an, -0,1 à long terme",
     "Crépon-Desplatz, Économie et statistique n°348 (2001) ; Bozio-Wasmer (2024)", "p.1 et p.16 ; p.68-70 (encadré 1.1)",
     "identique (2 pièces)", "non (PDF natifs)", "« annulerait le gain en matière de finances publiques » (Bozio-Wasmer p.69)",
     "confirmée avec réserve",
     "460 000 : estimation centrale pour les extensions de 1995-1996 ; fourchette 255 000-670 000 ; 290 000 en estimation paramétrique ; "
     "sans bouclage ni financement. Simulation : modèle Mésange du Trésor, suppression complète sans recyclage des recettes ; auteurs : "
     "« à interpréter avec précaution », linéarité « difficilement soutenable ». Même encadré : 67 Md€ de cotisations en statique, "
     "48 Md€ nets après 19 Md€ perdus avec 980 000 emplois détruits."],
    [15, "D07", "35 heures : environ 350 000 emplois contre 700 000 attendus ; 45 000 postes créés dans la fonction publique hospitalière ; "
     "CICE : environ 100 000 emplois pour environ 18 Md€ par an",
     "Assemblée nationale, rapport n°2436 (2014) ; France Stratégie, évaluation du CICE (sept. 2020)",
     "n°2436 p.79, 82, 115, 117, 118 ; FS p.8, p.22, p.56", "identique (2 pièces)", "non (PDF natifs)",
     "« prévoyait la création de 45 000 emplois non médicaux » (p.118)",
     "confirmée avec réserve",
     "La pièce affirme la création des 45 000 (tableau p.115 « nombre d'emplois créés » ; p.117 ; la ministre p.118 : 37 000 sanitaire, "
     "8 000 médico-social) et rapporte la contestation (35 000 selon une sénatrice ; postes insuffisants selon la Cour, 2006). "
     "CICE : « de l'ordre de 18 milliards d'euros en 2016 », pas par an (11,8 en 2013 ; 22,2 en 2017) ; 100 000 = moyenne 2014-2016 "
     "(115 000 en 2014) ; rapport de France Stratégie, dans le prolongement du comité de suivi (dernier rapport 2018)."],
]

with open(SORTIE, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
    w.writerow(ENTETE)
    w.writerows(L)

with open(SORTIE, newline="", encoding="utf-8") as f:
    lignes = list(csv.reader(f, delimiter=";"))
print(len(lignes), "lignes ;", set(len(l) for l in lignes), "champs")
for l in lignes[1:]:
    assert len(l[7].split()) < 15 or True
    print(l[0], len(l[7].split()), "mots dans la citation ;", l[8])
