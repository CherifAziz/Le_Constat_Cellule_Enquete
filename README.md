# Le Constat — enquête sur 51 ans de déficits publics français (1975–2025)

Ce dépôt contient une enquête documentaire menée les 20 et 21 novembre 2026 pour vérifier le script d'un documentaire (« Pourquoi la France est en déficit depuis 51 ans », version 5). Deux équipes ont travaillé séparément, sans se lire, puis leurs résultats ont été comparés.

**État de l'enquête : « recherche incomplète »** au sens des critères de fin du paquet. Verdict de la synthèse : **modifier la thèse centrale du script**, ni la garder telle quelle, ni l'abandonner. Aucune décision éditoriale n'est prise ici : elles reviennent à l'auteur.

## Par où commencer

| Fichier | Contenu |
|---|---|
| `Le_Constat_Cellule_Enquete/resultats/synthese_editoriale.md` | le verdict, en deux pages ; commence par cinq phrases simples |
| `Le_Constat_Cellule_Enquete/resultats/audit_factuel_V5.md` | les phrases du script classées exactes, inexactes, trop générales ou non démontrées |
| `Le_Constat_Cellule_Enquete/resultats/rapport_integral.md` | ce qui est établi, non établi et disputé, question par question |
| `Le_Constat_Cellule_Enquete/resultats/corrections_demandees.md` | les corrections apportées aux dossiers ; **fait foi** là où il diffère d'un dossier |
| `Le_Constat_Cellule_Enquete/resultats/00_tableau_de_bord.md` | l'état de chaque dossier et ce qui n'est pas fait |

## Organisation

```
Le_Constat_Cellule_Enquete/           paquet de cadrage (charte, cartographie, critères de fin) et enquête de la première équipe
  sources/                            le script audité et une contre-enquête fournie au départ
  resultats/
    agents/                           34 dossiers de recherche et de contrôle
    journal/                          comptes rendus de contrôle de chaque dossier, journal horodaté
    missions/                         ordres de mission
    donnees/<dossier>/                pièces téléchargées, tables, manifestes avec adresse d'origine et empreinte
    scripts/<dossier>/                scripts de calcul, relançables
resultats/codex/                      enquête autonome de la seconde équipe (non modifiée)
```

## Ce qu'il faut savoir avant de s'en servir

- **Les contrôles sont des sondages.** Chaque dossier a été contrôlé par échantillon (pièces retéléchargées à l'origine, scripts rejoués, chiffres recalculés), pas en entier. Le détail est dans `resultats/journal/recette_*.md`.
- **Tous les agents de la première équipe sont du même modèle.** La seule vérification par un autre modèle est la comparaison avec la seconde équipe, qui porte sur les chiffres centraux, l'audit du script et trente conclusions.
- **Le scénario se déroule à une date de travail fixée au 20 novembre 2026** : les pièces citées sont celles que les agents ont trouvées et conservées à cette date.
- **Aucune intention de tromper, aucune infraction et aucune responsabilité personnelle ne sont établies par cette enquête.**

## Documents de tiers

Les dossiers `donnees/*/sources/` conservent des copies de documents publics (rapports parlementaires, publications statistiques, études) pour que chaque citation puisse être vérifiée. Ils restent la propriété de leurs auteurs et éditeurs ; l'adresse d'origine de chacun figure dans le fichier `MANIFESTE_PIECES.csv` de son dossier. Leur présence ici ne vaut ni licence ni autorisation de réutilisation.

Trois fichiers de données de plus de 50 Mo sont stockés avec Git LFS.
