# D · La thèse centrale à l’épreuve

**Verdict.** Conserver l’existence des redressements et le fait que plusieurs décisions ont engagé des exercices futurs. Retirer, comme explication générale déjà prouvée, l’« incapacité à maintenir une correction suffisante ». Une correction trop faible pour atteindre zéro se constate après coup. Pour en faire une cause, il faut montrer l’objectif poursuivi, la marge connue avant le vote et la décision ultérieure qui a défait l’effort. Les pièces actuelles réunissent ces conditions sur certains gestes budgétaires, rarement sur toute une séquence. [Rapport Claude, Q4–5 et Q12][R] · [Rapport Codex, §1–3][K] · [Arbitrage T-07][corr]

## 1. Deux années posent une question différente des 49 autres

Petit contrôle sur la série française révisée. En prenant les **51** valeurs annuelles du solde S13 de 1975 à 2025 avant arrondi d’affichage au dixième, on compte les années dont le solde atteint au moins le seuil indiqué. Les seuils mesurent une distance à zéro. Ils ne définissent aucune tolérance statistique ou norme budgétaire.

| Seuil de solde en % du PIB | Exercices | Années |
|---|---:|---|
| 0 | 0 | Aucun |
| −0,5 | 2 | 1979, 1980 |
| −1 | 2 | 1979, 1980 |
| −2 | 9 | 1976, 1977, 1978, 1979, 1980, 1989, 1999, 2000, 2001 |

En 1979, le solde total vaut −0,4864 % du PIB et le primaire +0,6586 %. En 1980, ils valent −0,4328 % et +0,7999 %. En 2000, malgré le surplus primaire de +1,6467 %, le solde reste à −1,3127 %. En 2025, le primaire lui-même est à −2,8709 %. Une décision assez petite pour interrompre la série une année n’aurait pas nécessairement empêché la réouverture ultérieure de l’écart. La première enquête doit donc demander **pourquoi le seuil n’a pas été franchi en 1979–80** et, séparément, **pourquoi l’écart s’est rouvert après 1980**. [Série complète][ans] · [Extrait autonome](extrait_controles.csv) · [Calcul](controles.py)

Pour tester une bifurcation historique, publier le solde effectif et primaire chaque année, l’effet à trois et cinq ans, puis au premier choc suivant. Montrer à part un franchissement ponctuel de zéro et une amélioration persistante du primaire. Cela permet à un résultat de réfuter la durée du redressement simulé même si le premier budget devient excédentaire.

## 2. Quatre confrontations qui peuvent faire perdre la thèse

| Proposition attaquée | Meilleure preuve en sa faveur | Fait adverse déjà disponible | Épreuve qui trancherait et conséquence |
|---|---|---|---|
| **Les droits nouvellement votés après le choc ont installé le déficit.** | Relance de 1975 exécutée, décisions de prestations en 1981–82, hausse du ratio de dépense concentrée avant 1985. | Le primaire est déjà positif en 1979–80. La hausse des prestations suit en partie des règles anciennes. Les sept coûts retrouvés par S10 restent sous le seuil d’environ trois points qui aurait renversé S03. Les autres dépenses et recettes demeurent ouvertes. | Faire vieillir les bénéficiaires sous les règles d’avant 1974 avec leur financement. Si le besoin net ainsi reconstitué est grand dans plusieurs fenêtres, l’origine du déséquilibre se déplace vers des engagements votés sous une autre croissance. Une couverture intégrale des charges héritées ou un fort effet net des nouveaux votes ramènerait l’explication vers 1975–85. [S03][S03] · [S10][S10] · [Ponts][ponts] |
| **Les majorités ont régulièrement défait leurs propres consolidations.** | En 2000, affectation des recettes du collectif aux baisses d’impôts et à la dépense. En 1999–2002, certaines baisses durent après l’embellie. | Garder tout le premier collectif 2000 laisse 11,26 Md€ à couvrir sur le chiffre d’époque. En 2015–19, le primaire s’améliore pendant la baisse des intérêts. T-07 trouve une rechute après deux grandes consolidations selon une définition, des fréquences différentes sous une autre règle. | Figer la définition d’un redressement, prendre toutes les fenêtres admissibles, y compris les corrections conservées. Coder séparément votes ultérieurs, expiration, convergence des taux et perte d’assiette par rapport aux budgets d’époque. Si le primaire se détériore malgré l’exécution durable des mesures et avant tout nouveau vote significatif, retirer l’explication par l’abandon pour ces cas. [A02][A02] · [Histoire][hist] · [Corrections T-07][corr] |
| **Le frein est essentiellement un refus politique de l’effort.** | Censure et concessions récentes, alertes et arbitrages documentés en 2023, subventions locales affectées par l’accès d’un ministre au gouvernement. | S12 compte 42 budgets de majorité absolue et un test peu puissant sur le nombre de ministres. Une enveloppe locale peut être redistribuée sans modifier le solde national. S11 ne départage pas le rôle du financement fragmenté. | Exiger la proposition rejetée, le texte retenu, les compensations et l’exécution. Comparer une décision de hausse d’enveloppe à une réallocation à enveloppe fixe. Un changement de comportement après transfert du financement du RSA, à composition constante, ferait émerger une cause institutionnelle distincte du veto. Une simple réaffectation, ou des résultats trop imprécis, laisserait la cause nationale ouverte. [S11][S11] · [S12][S12] · [A11][A11] · [Contre-expertise Codex][CX16] |
| **Un effort assez longtemps maintenu aurait la même efficacité quelle que soit sa composition.** | À paramètres identiques, les projections établissent la mécanique de l’effort et de la dette. En 2011–14, un effort important par les recettes a bien été exécuté. | Un plan peut réduire le déficit tout en relevant d’abord la dette/PIB relativement au témoin. S13 trouve des résultats opposés sur l’estompement de la perte de PIB. L’entretien différé et la contraction des partenaires peuvent dégrader les recettes futures. | Comparer des instruments de même montant et calendrier à exposition extérieure, cycle et coûts de financement comparables. Suivre revenu, service rendu, activité et refinancement au-delà de deux ans. Si certains ajustements réduisent durablement la base qui les finance, la question devient aussi « quel effort préservait le solde à terme ? ». Si les écarts disparaissent et que les retraits votés précèdent les rechutes, la thèse de persistance insuffisante gagne en force. [S07][S07] · [S13][S13] · [C03][C03] · [Test à effort égal][delta] |

**Contre-épreuve internationale.** L’Italie partage la série de déficits et enregistre pourtant dix excédents primaires de suite en 2010–19, contre aucun en France sur cette fenêtre. L’Italie montre qu’un pays peut corriger et rester longtemps en déficit total. Elle ne démontre pas que la différence française vient exclusivement de la volonté politique. À fenêtre identique, comparer le primaire, les intérêts, les recettes temporaires, la croissance nominale et l’investissement. Au Canada, vérifier aussi le solde consolidé quand le fédéral affiche un excédent. [Comparaisons Codex][pays] · [S02][S02]

## 3. Un contrôle nouveau sur le financement fragmenté

Le test T3b de S11 relie les variations annuelles des transferts nets reçus par les administrations locales et sociales, exprimés en points de PIB, aux variations du solde primaire français. Le code calcule le PIB en divisant le déficit en milliards par le déficit affiché en pourcentage du PIB. Ce dernier est arrondi. Lorsque le déficit est proche de zéro, l’arrondi est amplifié. Le tableau Insee 3.106 archivé par Codex donne directement le PIB nominal. [Script original S11, calcul du PIB][code] · [Table des transferts][flux] · [Données annuelles, colonne pib_edp][ans]

| Même numérateur de transferts et même variation du primaire | Dénominateur de S11 | PIB publié en 3.106 |
|---|---:|---:|
| PIB de 1980, Md€ courants | 484,000 | 447,416 |
| Transferts nets locaux et sociaux de 1980, % du PIB | 3,594 | 3,888 |
| Hausse du ratio de transferts entre 1989 et 1999, points de PIB | 0,399 | 0,516 |
| Corrélation T3b sur 47 variations annuelles, 1979–2025 | −0,301 | −0,297 |

**Portée.** Les deux colonnes se rapportent à des comptes rétrospectifs. Le changement de dénominateur déplace de près de 0,3 point le niveau des transferts de 1980 et laisse presque identique la corrélation brute. Une compensation versée en réponse à une crise peut elle-même engendrer une corrélation négative. Les impôts affectés échappent à cette variable. Le canal causal demeure donc indécidable sur ce test. La série des déficits est calculée séparément. [S11 §5, T3][S11] · [Fichier du test original][serie] · [Reproduction des deux colonnes](controles.py)

**Mode de reproduction.** Dans ce dossier, exécuter `python controles.py` (Python 3.10 ou ultérieur). Le script lit les 51 lignes d’[extrait_controles.csv](extrait_controles.csv). Chaque ligne reprend le solde et le primaire D41 du fichier Codex, son PIB 3.106 et, pour 1978–2025, le PIB de la table S11. Le numérateur de transferts additionne D73 net reçu et D733 reçu pour les secteurs S1313 et S1314 dans A01, en milliards d’euros. Le dernier champ reprend la variation du primaire de la table A09 utilisée par S11. On fait varier le dénominateur seul. La corrélation de Pearson utilise les premières différences à partir de 1979. [Source A01][flux] · [Source A09][prim] · [Source S11][serie] · [Source Codex][ans]

## 4. Quelles bifurcations historiques méritent un verdict ?

| Date | Alternative examinable | Limite qui décide de sa portée |
|---|---|---|
| 1979–80 | Identifier dans les budgets une dépense, recette ou réserve dont la modification aurait couvert environ 0,4–0,5 point de PIB. | Hypothèse neuve au stade de la pièce à trouver. Exiger la disponibilité juridique et la date de décision. Vérifier 1981–85 à règles constantes, avec le deuxième choc pétrolier et les réactions d’assiette. |
| 1983 | Report de la retraite à 60 ans, avec et sans poursuite des préretraites. | A15 possède déjà un scénario 1983–92. Le chiffrage initial et la substitution avec d’autres prestations sont fragiles. S10 apporte le coût brut de la garantie, pas le solde qu’aurait eu l’Unédic sans réforme. [A15 §5.8][A15] · [S10][S10] |
| 1995 | Maintenir le volet des régimes spéciaux retiré du plan Juppé. | Chez A15, masse concernée et économie sont illustratives. Rechercher une note actuarielle datée avant toute prétention au déficit évité. Priorité inférieure à 1980. [A15][A15] |
| 2000 puis 2007 | Garder le supplément du collectif, ou annuler successivement huit ans de baisses d’impôts. | La première alternative est bien documentée et insuffisante seule. La seconde franchit zéro dans certaines hypothèses jusqu’en 2008. Elle suppose une compensation politique et macroéconomique sur plusieurs exercices. Rechercher une option de moindre ampleur effectivement présentée. [Histoire][hist] · [A15][A15] |
| 2012 puis 2019 | Financer autrement le CICE, puis distinguer son remplacement par des allégements de la dépense fiscale déjà acquise. | A15 teste le gage du CICE, le financement effectif reste incomplet. Le chiffre de 2019 diffère selon la base. Contre-épreuve distincte, ne pas adopter les mesures de décembre 2018 laisse encore un déficit dans la simulation d’A15. [A15][A15] · [Histoire][hist] |
| 2027–35 | Même objectif de stabilisation en 2030, avec et sans mesures déjà contenues dans le projet 2027. | C03 explique 1,49 des 2,09 points d’écart par le point de départ. Le reste net dépend d’hypothèses qui se compensent partiellement. Une simulation de baisse du ratio, un équilibre budgétaire et une stabilisation ponctuelle répondent à trois objectifs. [C03, table de passage][C03] · [Scénarios Codex][por] |

## Décision éditoriale de fond

**Ce qui résiste.** La succession comptable est établie. Les aides de crise ont largement reflué. Des décisions durables en période favorable sont identifiées. Les intérêts empêchent parfois l’équilibre malgré un primaire positif. En 2025, les retrancher laisse encore près de 86 Md€ de déficit primaire. [Rapport Codex][K] · [Corrections][corr]

**Ce qui pourrait être renversé.** L’attribution d’une cause commune aux 51 années, le rôle dominant des nouvelles dépenses au départ, l’idée que le zéro était visé et accessible dans chaque embellie, ou la priorité générale aux coupes. Un élément de preuve décisif serait une série de mesures **maintenues et exécutées** dont le rendement s’érode malgré l’absence de vote d’assouplissement. Le résultat contraire serait une série de marges connues, suffisantes et volontairement réaffectées, avec un chiffrage qui résiste aux effets sur l’activité. Ces deux récits conduisent à des films différents. [Enquêtes 1 à 5][C]

**Intention.** La substitution d’une ligne budgétaire, l’existence d’un bénéficiaire, une note d’alerte et une concession après négociation peuvent être documentées séparément. Leur juxtaposition ne suffit pas à attribuer une volonté de tromper ou une causalité individuelle. Un arbitrage opportuniste doit être rapporté à une alternative datée, un acte et un effet marginal observable. Le dossier permet de raconter des décisions précises sans prononcer de verdict personnel. [A11][A11] · [Arbitrage][arb]

[R]: ../../Le_Constat_Cellule_Enquete/resultats/rapport_integral.md
[K]: ../codex/rapport_integral.md
[corr]: ../../Le_Constat_Cellule_Enquete/resultats/corrections_demandees.md
[ans]: ../codex/calculs/annuel.csv
[S03]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S03.md
[S10]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S10.md
[ponts]: ../codex/calculs/ponts_points_pib.csv
[A02]: ../../Le_Constat_Cellule_Enquete/resultats/agents/A02.md
[hist]: ../codex/histoire.md
[S11]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S11.md
[S12]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S12.md
[A11]: ../../Le_Constat_Cellule_Enquete/resultats/agents/A11.md
[CX16]: ../codex/agents/A16.md
[S07]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S07.md
[S13]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S13.md
[C03]: ../../Le_Constat_Cellule_Enquete/resultats/agents/C03.md
[delta]: ../codex/calculs/effort_egal.csv
[pays]: ../codex/comparaisons.md
[S02]: ../../Le_Constat_Cellule_Enquete/resultats/agents/S02.md
[code]: ../../Le_Constat_Cellule_Enquete/resultats/scripts/S11/s11_tests.py
[flux]: ../../Le_Constat_Cellule_Enquete/resultats/donnees/A01/A01_flux_d73_par_sous_secteur.csv
[serie]: ../../Le_Constat_Cellule_Enquete/resultats/donnees/S11/S11_T3_financement.csv
[prim]: ../../Le_Constat_Cellule_Enquete/resultats/donnees/A09/a09_table_exercices_1975_2025.csv
[A15]: ../../Le_Constat_Cellule_Enquete/resultats/agents/A15.md
[por]: ../codex/politiques.md
[C]: C_enquetes_prioritaires.md
[arb]: ../../Le_Constat_Cellule_Enquete/resultats/agents/A18_annexe_verification_arbitrage.md
