# Ordre de mission C03 — Réconcilier les deux modèles de trajectoire : 5,2 ou 3,1 points de PIB ?

**Suite de la synthèse éditoriale (inconnue de rang 4).** Exécutant : Opus 5.5, effort élevé. Écrit le 21 novembre 2026.

Racine de la cellule (écritures uniquement ici) : `C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\`. Consignes : `resultats\missions\00_CONSIGNES_COMMUNES.md`.
Dossier de l'équipe Codex, **en lecture seule stricte** : `C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\resultats\codex\`. Rien n'y est créé, modifié, déplacé, supprimé ni exécuté ; copier d'abord sous `resultats\donnees\C03\copies_codex\`.

## Ce qu'on cherche

Pourquoi l'effort à voter pour stabiliser la dette vaut environ **5,2 points de PIB** dans le modèle de la cellule (A15) et **3,1 points** dans celui de Codex, et quel chiffre vaut pour quelle question. Décomposer l'écart de 2,1 points en termes nommés : mesures du budget 2027 comptées ou non dans la référence ; trajectoire des intérêts et taux à l'émission ; croissance et déflateur ; rétroaction de l'effort sur l'activité (multiplicateur) ; définition de « stabiliser » (année, dette constante ou variation nulle) ; ajustements stocks-flux ; reste.

## Pourquoi c'est important

Le documentaire donne des ordres de grandeur ; la synthèse éditoriale dit que l'effort se situe « entre 3,1 et 5,2 points selon le point de départ », sans pouvoir dire d'où vient l'écart. Tant que les deux modèles ne sont pas réconciliés, aucun chiffre d'effort ne peut être cité seul.

## Déjà établi (ne pas refaire)

- Modèle de la cellule : `resultats\scripts\A15\` (quatre scripts, rejoués à l'identique), sorties dans `resultats\donnees\A15\` ; hypothèses dans `resultats\agents\A15.md` (sections 2, 5 et 11 à 15) ; `resultats\journal\recette_A15.md` ; variantes d'A16 et d'A17 (`resultats\donnees\A16\`, `resultats\donnees\A17\`).
- Modèle de Codex : `scenarios.py`, `calculs\scenarios.csv`, `politiques.md` (lignes 38 à 55) dans son dossier ; lecture par C02 (`resultats\agents\C02.md`, conclusions K19 à K21).
- Pièces communes : prévision d'automne de la Commission (copie dans `resultats\donnees\A03\sources\`), rapport économique pour 2027.

## Méthode imposée

- Ne modifier aucun script existant : travailler sur des copies placées sous `resultats\scripts\C03\` et `resultats\donnees\C03\`.
- Faire tourner le modèle de la cellule **avec la référence de Codex** (déficit de 5,4 % en 2027, mesures du budget comprises) et, si possible, la logique de Codex avec la référence de la cellule ; changer un paramètre à la fois ; tenir une table de passage de 5,2 à 3,1.
- Dire, pour chaque terme, si c'est une convention (les deux chiffres sont justes pour des questions différentes), une hypothèse (laquelle des deux est la mieux étayée par une pièce) ou une erreur (de qui).
- Vérifier au passage : les mesures du budget 2027 valent-elles bien environ 1,1 à 1,4 point ? Sont-elles adoptées, rejetées, en discussion à la date du 21 novembre 2026 (pièce) ?

## Conditions de clôture

- Une table de passage dont les termes somment à l'écart (reste inférieur à 0,2 point, ou reste expliqué).
- Une phrase par chiffre : « 5,2 points répond à la question … ; 3,1 points répond à la question … ».
- Les erreurs éventuelles de l'un ou l'autre modèle, pièce ou calcul à l'appui.

## Livrables

`resultats\agents\C03.md` (17 titres, écrit au fil de l'eau), `resultats\donnees\C03\` avec `MANIFESTE_PIECES.csv` et la table de passage en CSV, `resultats\scripts\C03\`. Message de fin de moins de 400 mots.
