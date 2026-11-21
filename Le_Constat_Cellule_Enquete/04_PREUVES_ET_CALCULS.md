# Norme de preuve, comptabilité et protocole quantitatif

## I. Un registre pour chaque proposition
Attribuer un identifiant `F0001` à chaque résultat factuel, `H0001` à chaque hypothèse, `P0001` à chaque proposition politique, `C0001` à chaque résultat de calcul. Chaque entrée doit contenir :
- **Affirmation atomique** sans mélange de faits et de jugements.
- **Métrique** : unité, période, périmètre (État, S13, branche, ménage), prix courants/2015/2024, brut/net, projection/réalisé.
- **Source primaire exacte** : organisme/auteur, titre, date de publication, date d'observation, URL, page/tableau/ligne. Lien fonctionnel lors de la consultation.
- **Méthode** : observation, texte de loi, décomposition comptable, quasi-expérience, série corrigée des cycles, régression, simulation, déclaration d'acteur, enquête journalistique.
- **Réproduction** : formule, données brutes, scripts, hypothèses, dates de révision.
- **Critique** : meilleure objection, alternative interprétative, sensibilité, incertitude, lien vers contradicteur.
- **Statut** : confirmé, confirmé sous conditions, contesté, non vérifié, réfuté.
- **Effet éditorial** : infirme/soutient/affine la question centrale ; récit essentiel ou annexe.

## II. Ordre des preuves (indicatif, non automatique)
A. Pièce originale datée vérifiable : comptes définitifs, texte de loi, vote, archives, décisions de justice, chiffrage refait.
B. Étude empirique avec identification causale crédible, données et méthodes auditables.
C. Étude descriptive ou comparaison rigoureusement corrigée.
D. Simulation prospective avec hypothèses explicites et sensitivité.
E. Déclaration d'acteur, revendication, sondage interprété avec prudence.
F. Commentaire/tribune non corroborés. **Ne jamais promouvoir E/F en fait établi par répétition.**

## III. Tests comptables obligatoires
1. Les recettes et dépenses de toutes les administrations sont **consolidées** avant de les additionner ; virements intra-publics neutralisés.
2. Solde public = recettes – dépenses sur le bon exercice et périmètre ; déficit positif selon convention précisée.
3. Solde primaire = solde hors charge d'intérêts, pas « sans dette » ; intérêts bruts/net selon convention.
4. Ratio dette/PIB : distinguer hausse de la dette en euros et baisse éventuelle du ratio ; ajustements stock-flux.
5. Stabilisation de la dette : partir de la formule exacte et publier g nominal, dette initiale, horizon, i effectif, ajustements.
6. Écart avec moyenne zone euro : moyenne **incluant ou excluant France** ; fonctions COFOG parfois millésime inférieur à comptes totaux.
7. Ne pas rapprocher sans avertissement une économie régimes de retraite 2030, une économie toutes administrations 2027, une cible politique 2027 et le déficit 2025.
8. Dépense fiscale ≠ argent récupérable : réévaluer réactions des agents, suppression graduelle, chevauchements et assiettes.
9. Gain État ≠ gain public consolidé si coûts reportés aux collectivités, ASSO, ménages, complémentaires ou année suivante.
10. Ne pas chiffrer une « fraude » comme économie acquise sans rendement net et coût du contrôle.
11. Les scénarios historiques ne doivent pas ajouter des résultats interdépendants : une réforme modifie emploi, PIB, assiette, intérêts et dette.
12. Rebaser les séries sur révisions Insee/Eurostat ; conserver millésimes différents séparément.

## IV. Décomposition et modèle de dette
Dans la convention de déficit positif, si dette initiale/PIB = `d`, croissance nominale = `g`, le déficit total en % du PIB courant stabilisant ce ratio est environ `d * g / (1+g)`, en l'absence d'ajustements stocks-flux. À vérifier pour l'année et les conventions des données ; le déficit total effectif inclut les intérêts. Pour les simulations de longue période, utiliser une identité récurrente avec solde primaire, taux effectif, croissance nominale et ajustement stock-flux.

Pour chaque mesure, fournir **scénario sans réforme**, effets directs, effets sur PIB et recettes, effets de substitution, coûts administratifs, répartition, croissance, risques d'exécution, éventuelles dépenses reportées et trajectoires de dette à moyen terme.

### Tableau de sensibilité obligatoire
Croissance réelle : basse / centrale / haute ; inflation basse/haute ; taux d'intérêt +100/+200 points de base à maturité appropriée ; multiplicateurs faibles/forts ; emploi bas/haut ; coûts de vieillissement ; calendrier d'application. Afficher plages de résultats et ne pas confondre incertitudes différentes.

## V. Procédure de contradiction
- Chaque résultat de type A/B doit avoir une **vérification des unités et du périmètre** par A01/A18.
- Chaque hypothèse politique doit mentionner au moins une pièce qui **pourrait la falsifier**.
- Déclarer toutes les contradictions ; en cas d'impossibilité, donner les deux lectures avec leurs implications.
- Ne pas présumer qu'une personne ou institution a volontairement trompé : comparer note interne, diffusion, règles et réponse officielle ; une divergence de prévision ne prouve pas l'intention.
- Si deux sources se contredisent, rechercher leur **définition, millésime, effet de change, horizon et méthode**, et non choisir la source qui arrange le récit.

## VI. Santé épistémique de l'enquête
Maintenir `resultats/contradictions.md` et une colonne « manque de preuve ». Marquer explicitement « recherche infructueuse » après protocole documenté, plutôt que d'inventer ou de laisser croire que tout a été couvert. Produire aussi un dossier d'exonération de chaque accusation potentielle : l'explication innocente la plus robuste doit être recherchée et rapportée.
