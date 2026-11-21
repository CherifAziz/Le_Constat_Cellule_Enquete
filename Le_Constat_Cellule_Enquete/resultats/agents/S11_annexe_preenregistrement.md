# S11 — Pré-enregistrement du test de l'hypothèse H0040 (« bien commun budgétaire »)

**Rédigé le 21 novembre 2026 entre 10 h 36 et 10 h 50, avant tout calcul. Figé à l'écriture : ce fichier n'est plus modifié. Son empreinte SHA-256 et l'heure du gel sont notées dans `S11.md` §5. Tout écart ultérieur au protocole est consigné dans `S11.md` §5, rubrique « Écarts au pré-enregistrement », jamais ici.**

## 0. Formulation testée

H0040, telle qu'inscrite dans `resultats\hypotheses.md` : « chaque acteur (ministère, caisse, collectivité, groupe parlementaire) reçoit tout le bénéfice d'une dépense et ne paie qu'une part de son coût ; la fragmentation du financement, et non le veto, entretient le déficit ».

Deux mécanismes sont distingués, parce qu'ils ne laissent pas les mêmes traces :
- **H-a, fragmentation des décideurs** (loi du 1/n, nombre de ministres dépensiers, nombre de partis de la majorité) : plus il y a de décideurs dont chacun internalise une part faible du coût, plus la dépense (ou le déficit) est élevée.
- **H-b, fragmentation du financement** (écart vertical, « payeur différent du décideur ») : quand un sous-secteur décide une dépense financée par un autre (transferts de l'État aux collectivités, compensation par l'État d'exonérations, dépassement de l'ONDAM couvert par dette sociale), la dépense de ce sous-secteur dérive et le solde d'ensemble se dégrade.

**Explication rivale R** : la persistance vient de décisions assumées par des majorités capables de décider, notamment des baisses de prélèvements générales et des surplus rendus ; le décideur et le payeur sont alors le même (la majorité nationale).

H et R ne s'excluent pas. Un résultat mixte est rapporté test par test, sans moyenne, et conduit au verdict « ni l'une ni l'autre » sauf règle contraire du §4.

## 1. Ce que je savais avant d'écrire ce fichier (exposition aux résultats)

Lus avant le gel (synthèse, corrections, A09, A08, S08, A01) : 37 budgets de majorité absolue sur 37 en déficit ; test d'A09 sur le nombre effectif de groupes de toute l'Assemblée, au niveau des législatures (rho +0,19 sur le solde primaire, n = 13 ; −0,01 corrigé du cycle, n = 12) ; ONDAM tenu dix ans (2010–2019) contre sa cible initiale, dépassements « systématiques » avant 2010, non tenu 2020–2024 ; normes de l'État tenues quatre ans au plus, surtout par périmètre, cible ou charge de la dette ; contrats de Cahors tenus deux ans ; « cagnotte » de 2000 à 80 % en baisses d'impôts ; consolidation 2011–2014 à 83 % par les recettes ; aucune trajectoire de solde tenue à trois ans (A08) ; un député ne peut pas créer une dépense (A08 R4) ; anomalie D733 avant 2010 et flux D73 par sous-secteur (A01). Je n'ai calculé aucune des statistiques ci-dessous ni regardé les séries annuelles qu'elles utilisent.

Conséquence : **T4 (normes par sous-secteur) est descriptif et non confirmatoire**, son résultat étant pour l'essentiel connu (S08 §11). T2 est partiellement exposé (deux épisodes connus). T1 complète un test déjà fait par A09.

## 2. Faits qui ne départagent pas

Les deux explications prédisent : un déficit persistant ; des trajectoires pluriannuelles non tenues ; des majorités absolues en déficit ; un État en déficit plus que les autres sous-secteurs (l'État est le compensateur : les soldes par sous-secteur sont mesurés après transferts). Ces faits sont rapportés sans être comptés pour ou contre H.

## 3. Tests, prédictions, seuils (plus petit effet d'intérêt, PPEI)

Règle générale : un test **soutient** H si l'intervalle de confiance à 95 % exclut zéro dans le sens prédit ; il **contredit** H seulement si cet intervalle exclut le PPEI dans le sens prédit (une absence d'effet non significative ne contredit rien) ; sinon il est **non concluant**. La puissance de chaque test est calculée et rapportée. Une corrélation ne prouve pas une cause : un test favorable atteint au mieux le niveau C.

### T1 — Fragmentation de la majorité (H-a, acteurs atteints : groupes parlementaires)
- Donnée : `donnees\A09\a09_composition_majorites.csv` et `a09_table_exercices_1975_2025.csv`. Variable : nombre de groupes composant le camp gouvernemental (et, si calculable sans pièce nouvelle, nombre effectif de partis de la majorité, Laakso–Taagepera sur les seuls groupes de la majorité). Unité d'analyse : **la législature** (la variable ne change qu'aux élections ; n ≈ 13).
- Prédiction H : pente négative entre la fragmentation de la majorité et la variation annuelle moyenne du solde primaire (et du solde primaire corrigé du cycle, AMECO, quand il existe) ; pente positive avec la variation des dépenses primaires.
- Prédiction R : pas de pente ; les dégradations dépendent du calendrier électoral et des décisions de recettes, quelle que soit la composition.
- PPEI : −0,3 point de PIB par an par groupe (ou parti effectif) supplémentaire dans la majorité.
- Limite déclarée d'avance : canal le plus faible de H, puisque les députés ne peuvent pas créer de dépense ; un résultat nul ne dit rien des ministères, caisses ou collectivités. Avec n ≈ 13, un « contredit » est presque impossible : défaut attendu « non concluant ».

### T2 — Composition des dégradations hors crise (H-a et H-b agrégés ; acteurs : toutes APU)
- Donnée : `a09_table_exercices_1975_2025.csv` (variations du solde primaire, des dépenses primaires et des recettes, points de PIB). Années de dégradation : Δ solde primaire ≤ −0,5 point. Années de crise exclues : année de croissance du PIB en volume négative et l'année suivante, d'après une série officielle téléchargée (Eurostat `nama_10_gdp`, ou Insee) ; à défaut, liste de repli 1975, 1993, 2008–2009, 2020–2021, déclarée comme telle.
- Statistique : part de la dégradation cumulée venant de la hausse du ratio de dépense primaire, S = ΣΔdep / Σ(Δdep − Δrec) sur ces années ; et la même chose sur toutes les années de dégradation (crises comprises), pour information.
- Prédiction H (version « dépense » du bien commun) : S ≥ 0,5. Prédiction R : S < 0,5 (dégradations surtout par les recettes).
- Classement des baisses de recettes, fixé d'avance : une dégradation par les recettes ne compte **contre H** que si elle vient de mesures générales (barème de l'IR, taux de TVA ou d'IS, suppression générale d'un impôt local, baisse générale de cotisations) ; une niche ciblée sur une catégorie organisée est elle-même un bien commun du côté des recettes et compte **pour H**. Les ratios agrégés ne permettent pas ce classement : sauf pièce par année, un S < 0,5 est rapporté comme « non favorable à la version dépense de H », non comme une contradiction. Le ratio de dépense monte aussi mécaniquement quand la croissance ralentit : limite rapportée.

### T3 — Fragmentation du financement des collectivités et de la sécurité sociale (H-b ; acteurs : collectivités surtout, caisses en partie)
- Donnée : `donnees\A01\A01_flux_d73_par_sous_secteur.csv` (lecture seule) et tableaux Insee t_3203, t_3205, t_3212 (base 2020). Seule la somme D73 + D733 est utilisée avant 2010 (anomalie signalée par A01).
- Indice F_t : transferts courants nets reçus d'autres APU (D73 + D733) par APUL + ASSO, en points de PIB, et en part de leurs dépenses.
- **T3a (sens de la hausse de F)** : sur 1978–2025 et par décennie, décomposer la variation de F en variation des dépenses d'APUL + ASSO et variation de leurs ressources propres (impôts et cotisations, D2 + D5 + D91 + D61 nets), en points de PIB. Prédiction H : hausse de F « tirée par la dépense » (dépense des sous-secteurs bénéficiaires en hausse d'au moins ΔF, ressources propres stables ou en hausse). Prédiction R : hausse de F « par substitution » (ressources propres en baisse d'au moins la moitié de ΔF : l'État a supprimé un prélèvement local ou social et le compense). Une hausse par substitution relève de R et ne compte pas pour H.
- **T3b (lien avec le solde d'ensemble)** : corrélation entre ΔF et Δ solde primaire S13 (différences premières, n ≈ 47). Prédiction H : corrélation négative. PPEI : r = −0,3. Contredit si la borne basse de l'intervalle à 95 % de r est au-dessus de −0,3.
- Limite déclarée : les impôts affectés directement aux ASSO (CSG, fractions de TVA) n'entrent pas dans D73 ; F sous-estime donc le financement de la sécurité sociale par des décisions de l'État. T3 parle surtout des collectivités.
- T3c (descriptif, non départageant) : soldes cumulés par sous-secteur selon les conventions C1 et C3 d'A01.

### T4 — Tenue des normes par sous-secteur (H-b ; acteurs : caisses, collectivités, État) — descriptif, non confirmatoire
- Donnée : `donnees\S08\S08_B_table_normes.csv`. Critère retenu : `t_init` (exécution ≤ cible initiale) ; `t_cour` donné à côté quand il existe.
- Familles : ASSO = ONDAM ; APUL = CAHORS_321, LPFP23_APUL ; État = ETAT_*.
- Prédiction H : part des années tenues plus faible pour ASSO et APUL que pour l'État. Prédiction R : pas d'ordre systématique.
- Limite : cibles non comparables (ONDAM rebasé chaque année à environ +2,3 % en valeur ; normes de l'État tenues par périmètre). Aucune puissance inférentielle.

### T5 — La procédure budgétaire française est-elle plus éclatée que celle des voisins ? (H-a ; acteurs : ministres, procédure)
- Donnée : indices publiés de centralisation de la procédure (Hallerberg, Strauch, von Hagen ; von Hagen ; OCDE ; base de gouvernance budgétaire de la Commission), lus dans le texte.
- Règle fixée d'avance : la position française compte **contre** H-a (version procédurale) si la France est classée parmi les procédures centralisées (État « de délégation » avec ministre des Finances fort, ou au-dessus de la médiane de l'indice de centralisation de la phase gouvernementale) ; **pour** H-a si elle est sous la médiane ou classée « fragmentée ». Un indice de règles numériques seul ne compte pas (il ne mesure pas la fragmentation).
- La comparaison Eurostat de l'écart vertical (part des dépenses des APUL + ASSO non couvertes par leurs impôts) est abandonnée comme test : le fichier commun n'a pas le poste D73 et l'attribution des impôts partagés fausse l'indicateur (n ≈ 13) ; elle peut être donnée en description.

### Littérature
Au moins quatre études lues en entier (PDF enregistré, parcouru jusqu'aux limites reconnues par les auteurs), dont deux qui ne trouvent pas d'effet ou le bornent. Pour chacune : la France est-elle dans l'échantillon ? Y a-t-il un résultat propre à la France ? Les auteurs donnent-ils un résultat nul ou une borne ?

## 4. Règle de verdict (fixée d'avance)

- **Soutenue** : au moins un test sur données françaises (T1, T3a, T3b) favorable selon le §3, aucun test français défavorable, et une littérature qui trouve l'effet avec la France dans l'échantillon. Niveau de preuve au mieux C (corrélation, petit n).
- **Contredite (dans les formes testées)** : au moins deux tests français défavorables selon leurs critères (T1 : intervalle excluant le PPEI ; T3a : hausse de F par substitution ; T3b : intervalle excluant le PPEI ; T2 : seulement si S < 0,5 ET mesures de recettes générales documentées), et aucun test favorable. Une contradiction dans les formes testées ne ferme pas les canaux non atteints (ministères, bénéficiaires organisés).
- **Ni l'une ni l'autre** : tests non concluants, ou résultats de sens opposés.
- **Non testable** : si aucun test n'atteint les acteurs nommés par H faute de donnée ; dire laquelle.

**Résultat qui me ferait conclure contre l'hypothèse** : une hausse de la part des collectivités et de la sécurité sociale financée par l'État qui s'explique surtout par la suppression de leurs ressources propres décidée par l'État (substitution), sans lien négatif avec le solde d'ensemble (borne de r au-dessus de −0,3), avec des dégradations hors crise surtout par des baisses générales de recettes, et une procédure française classée centralisée.
