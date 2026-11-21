# S12 — Pré-enregistrement de la partie B (nombre de ministres dépensiers)

**Daté du 21 novembre 2026, écrit avant tout calcul sur les variables de la partie B, puis figé** (empreinte SHA-256 consignée dans `resultats\agents\S12.md`, § 5 B, et dans `resultats\donnees\S12\s12_preenregistrement_sha256.txt`). Avant d'écrire ce texte, j'ai seulement : lu la structure (en-têtes) du fichier data.gouv.fr des membres des gouvernements ; lu le tableau officiel de la réponse à la question écrite n° 19405 (effectifs à la formation de chaque gouvernement, 1959–2019) ; repéré les années de croissance négative dans la pièce Eurostat de S11 (1975, 1993, 2009, 2020). Je n'ai croisé aucune de ces données avec la dépense ou le solde.

## 1. Hypothèse et prédiction

Canal du « bien commun budgétaire » par le nombre de décideurs : chaque ministre dépensier internalise mal le coût fiscal de ses demandes ; plus ils sont nombreux, plus la dépense augmente.
- **Prédiction P1** : pente de la variation de la dépense primaire (points de PIB) sur le nombre de ministres dépensiers **positive**.
- **Prédiction P2** : pente de la variation du solde primaire (points de PIB) sur ce nombre **négative**.

## 2. Unités et variables

- **Unité** : l'exercice budgétaire, 1975 à 2025 (51 au plus). Chaque exercice est rattaché au gouvernement en fonction **à la date du vote de l'ensemble de la LFI en première lecture** (automne N-1 ; pour 2025, février 2025, gouvernement Bayrou). Règle de rattachement : le dernier gouvernement formé avant cette date.
- **Définition (mesure principale X1)** : « ministre dépensier » = ministre de plein exercice hors Premier ministre et hors ministres des finances et du budget. Mesure : nombre de **ministres d'État + ministres** à la formation du gouvernement (tableau officiel QE 19405, qui inclut dans « ministres » les « ministres auprès de ministres » : limite assumée), **moins 1** (le ministre de l'économie et des finances, toujours ministre de plein exercice). Le ministre du budget n'est retiré que s'il a rang de ministre : ce retrait ne peut être fait sur la pièce officielle (elle ne nomme pas les titulaires) ; il est traité dans la variante X3. Soustraire une constante ne change pas la pente ; l'erreur résiduelle est de 0 ou 1 par gouvernement.
- Gouvernements postérieurs à la pièce officielle (Castex 2020 ; Borne 2022 ; Bayrou 2024) : effectifs à la formation tirés du fichier data.gouv.fr (source secondaire **[S]**, publiée par un particulier), après contrôle de ce fichier contre la pièce officielle (§ 4).
- **Ministres délégués et secrétaires d'État** : exclus de X1 (ils n'arbitrent pas un budget propre en principe). **Variante X2** : tous les membres hors Premier ministre (ministres d'État + ministres + ministres délégués + secrétaires d'État) moins 1.
- **Variante X3** : effectif **à la date du vote** (et non à la formation), calculé sur le fichier data.gouv.fr : fonctions codées ministre d'État ou ministre, en fonction à la date du vote, hors Premier ministre, hors fonctions dont l'intitulé contient « économie », « finances », « budget » ou « comptes publics ».
- **Y1** : `d_depenses_primaires` ; **Y2** : `d_solde_primaire` (table d'A09, points de PIB, Insee).
- Date de vote : relevée sur pièce quand elle l'a été en partie A ; sinon le 20 novembre de N-1 (variante X3 seulement).

## 3. Tests

- **Test principal** : MCO de Y1 sur X1 et de Y2 sur X1, n = 51 ; pente, IC à 95 % (Student), effet minimal détectable à 80 % (MDE80), corrélation de Pearson, p de permutation (20 000 tirages, graine 11), Spearman. Puissance pour |r| = 0,3 à n = 51 (Fisher z), donnée avant lecture des résultats.
- **Effet minimal qui compterait** : **+0,05 point de PIB de dépense primaire par ministre dépensier supplémentaire** (soit +0,5 point pour dix ministres de plus, l'ordre de grandeur de l'écart entre gouvernements resserrés et gouvernements nombreux ; l'écart-type de Y1 est voisin de 1,5 point). Symétriquement −0,05 point de solde primaire.
- **Contrôles pré-enregistrés** : (a) hors années de récession (croissance du PIB en volume < 0, Eurostat `nama_10_gdp`, pièce de S11) et l'année suivante ; (b) régression multiple de Y sur X1 + indicatrice de récession + indicatrice « premier exercice d'un nouveau gouvernement » + indicatrice « exercice pré-électoral » (colonne d'A09) ; (c) variantes X2 et X3 ; (d) agrégation par gouvernement (moyenne de Y par gouvernement, un point par gouvernement) pour corriger la répétition de la même valeur de X sur plusieurs exercices.
- Les observations ne sont pas indépendantes (même X sur plusieurs années, autocorrélation) : l'IC du test principal est donc trop étroit ; le contrôle (d) est le garde-fou.

## 4. Contrôle de la source secondaire

Avant usage, compter dans le fichier data.gouv.fr les ministres d'État + ministres à la date de formation de chaque gouvernement 1974–2019 et comparer à la pièce officielle. Si l'écart dépasse 1 pour plus de 20 % des gouvernements, X3 est abandonnée et les trois gouvernements récents sont signalés comme mesure fragile.

## 5. Règle de décision (figée)

- **Canal soutenu** : pour Y1, pente principale > 0, IC 95 % excluant 0, estimation ≥ +0,05 ; et signe conservé dans le contrôle (a) et le contrôle (d).
- **Canal contredit** : pour Y1, borne haute de l'IC 95 % < +0,05 (on exclut un effet de la taille minimale), ou pente négative avec IC excluant 0 ; et même conclusion dans le contrôle (d).
- **Ni l'un ni l'autre** : tout autre cas, notamment un IC qui contient à la fois 0 et +0,05.
- Y2 sert de recoupement : un verdict « soutenu » sur Y1 avec une pente de Y2 de signe contraire à P2 est rapporté comme « soutenu sur la dépense, non sur le solde ».

## 6. Portée annoncée d'avance

Une corrélation n'est pas une cause : le nombre de ministres est choisi par le Premier ministre et le Président, en même temps que le programme ; un gouvernement nombreux peut être la conséquence d'une coalition large ou d'une volonté de dépenser, pas sa cause. Un résultat nul ne prouve pas l'absence d'effet : il borne seulement l'effet aux valeurs hors de l'intervalle. Avec 51 points (et environ 25 gouvernements), seuls des effets moyens à forts sont détectables.
