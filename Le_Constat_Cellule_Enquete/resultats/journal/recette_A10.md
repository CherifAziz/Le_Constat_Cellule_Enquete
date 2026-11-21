# Recette du dossier A10 — Psychologie et économie comportementale

**Contrôle fait par l'orchestrateur le 20 novembre 2026, vers 11 h 32.** Durée de la mission A10 : 40 minutes, 214 appels d'outils.

## Verdict : recette passée pour l'inventaire des mécanismes, l'opinion française et la littérature sur la sanction électorale ; **partielle du côté des décideurs et de l'information**. Statut : non contre-expertisé.

## 1. Contrôle mécanique

17 titres obligatoires présents ; deux annexes (22 fiches d'études ; enquêtes d'opinion françaises avec question, date, échantillon) ; 65 pièces marquées consultées, 33 secondaires, 20 souvenirs non vérifiés, 23 recherches infructueuses ; 30 faits, 5 hypothèses, 4 calculs, 6 pistes ; 122 fichiers de données dont les microdonnées du baromètre de la Drees ; 4 scripts. Aucune URL écrite en clair dans le dossier : les adresses sont dans `donnees\A10\sources\journal_telechargements.csv`.

## 2. Relecture

Sections 11 à 15 lues intégralement par l'orchestrateur. Les annexes n'ont été lues que par sondage.

## 3. Sondage à la source

| Affirmation d'A10 | Contrôle | Résultat |
|---|---|---|
| Les séries d'opinion de la Drees sont recalculées à partir des microdonnées publiques | Script `drees_test_principe_mesure.py` relancé par l'orchestrateur | **Le script tourne** et régénère le tableau par année et par groupe (cette relance a réécrit le fichier de sortie d'A10 ; le contenu avant et après n'a pas été comparé) ; les valeurs 2025 n'ont pas été comparées une à une au texte |
| Sondage de juillet 2025 pour RTL : 1 006 personnes ; 73 % approuvent l'objectif de déficit | Copie locale du rapport de l'institut | **Confirmé** pour l'échantillon et les 73 % ; les 39 % (année blanche) et 30 % (jours fériés) sont dans des graphiques dont l'extraction de texte ne restitue pas les valeurs : non revérifiés |
| Les quatre étages de preuve sont tenus séparés ; les résultats non lus en texte intégral sont signalés | Relecture des sections 12 et 13 | **Conforme** : chaque affirmation de la V5 est rattachée à un étage ; une erreur de mémoire sur une référence est documentée et corrigée par l'agent |

Non revérifiés par l'orchestrateur : tailles d'effet des études étrangères ; expérience de la Drees sur le statu quo (27 % contre 56 % selon la formulation) ; biais d'optimisme des prévisions françaises de 1996 à 2011.

## 4. Ce que le dossier ne contient pas (reconnu par A10)

- Aucune mesure des croyances des parlementaires français sur le coût électoral d'un effort ; aucun test causal de la sanction électorale en France.
- Séries d'opinion antérieures à 2014 (baromètre du CEVIPOF, Eurobaromètre, enquête internationale sur le rôle de l'État) : jamais tentées.
- Plusieurs études lues en résumé seulement ; travaux de l'OCDE sur les citoyens et le budget inaccessibles.
- Évaluations du chiffrage public des programmes et des exercices participatifs : deux recherches seulement.

## 5. Portée à ne pas perdre

Le résultat le mieux établi est un fait d'opinion (soutien à l'objectif, rejet des mesures qui touchent le répondant). A10 précise lui-même qu'il ne prouve rien sur le vote des députés, et qu'aucune pièce psychologique n'est propre aux votes de 2024 à 2026.

## 6. Suites décidées

1. Seconde passe ciblée : séries d'opinion longues ; croyances des élus ; textes intégraux des études sur la sanction électorale.
2. Question transmise à A14 et A13 : rendement cumulé des mesures majoritaires dans l'opinion, face au besoin.
3. Question transmise à A09 : ce que les scrutins de 2024 à 2026 permettent d'attribuer, indépendamment des sondages.
