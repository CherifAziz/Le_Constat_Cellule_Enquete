# H10 · La consolidation des partenaires européens et le solde français, 2011–2015

## Faisabilité de l’identification causale

**Le commerce fournit une épreuve du mécanisme. Le rendement de l’effort français demanderait une autre comparaison.** Entre 2010 et 2013, les destinations qui ont le plus consolidé ont généralement moins acheté de biens français. Cette relation existait déjà sur la fenêtre 2007–2010. Une étude sur des décisions budgétaires documentées avant 2010 apporte un appui empirique au canal commercial. Pour la France de 2011–2015, les estimations du manque à gagner en activité reposent sur des modèles. L’effet sur le rendement propre d’une mesure française demeure indéterminé.

Appelons B(f,e) le solde de l’ensemble des administrations publiques françaises en points de PIB, à une date donnée. La lettre f indique la présence (1) ou l’absence (0) du programme français, la lettre e celle des programmes étrangers. Les interventions, le calendrier, la réaction monétaire et le traitement de la crise bancaire doivent être spécifiés dans chaque comparaison.

| Question | Comparaison nécessaire | Ce que les pièces permettent |
|---|---|---|
| Les efforts étrangers abaissent-ils l’activité française à effort français donné ? | PIB(1,1) − PIB(1,0) | Estimation conditionnelle par la DG Trésor jusqu’en 2013. Le commerce bilatéral permet de confronter son signe aux observations. |
| L’environnement étranger a-t-il dégradé le solde français à effort national donné ? | B(1,1) − B(1,0) | Le calcul budgétaire disponible porte sur le paquet d’ensemble. La semi-élasticité du solde permet une sensibilité conditionnelle pour sa seule composante cyclique. |
| Le même programme français rapporte-t-il moins si ses partenaires consolident ? | [B(1,1) − B(0,1)] − [B(1,0) − B(0,0)] | Il faudrait les quatre soldes sous des hypothèses communes, ou une identification exogène équivalente. Même si les partenaires dégradent le solde français, une retombée purement additive s’annule dans cette différence. |

Le dossier S07 établissait déjà l’effort exécuté, le scénario conjoint de la Commission et le frein extérieur calculé par l’OFCE. S13 décrit les dépenses dont le calendrier déplace les coûts. C03 traite des arbitrages budgétaires prospectifs. Aucun de ces travaux ne fournit les quatre soldes historiques requis. L’apport ici est la décomposition française publiée par le Trésor, son contrôle contre un autre modèle et la confrontation aux échanges observés. [Rapport C de l’audit](../../audit_final_angles_morts/C_enquetes_prioritaires.md) · [S07](../../../Le_Constat_Cellule_Enquete/resultats/agents/S07.md) · [S13](../../../Le_Constat_Cellule_Enquete/resultats/agents/S13.md) · [C03](../../../Le_Constat_Cellule_Enquete/resultats/agents/C03.md)

## Ce que les partenaires achetaient effectivement

Nous retenons **tous les partenaires de la France que QUEST modélise individuellement**. L’Allemagne, l’Espagne, la Grèce, l’Irlande, l’Italie et le Portugal ont ainsi une mesure individuelle d’effort dans le tableau 4 de l’étude source. Le reste de la zone euro y figure en bloc. L’indicateur est la variation cumulée du solde structurel primaire, estimée au printemps 2013 et encore prévisionnelle pour cette dernière année. Il approche le resserrement, avec les erreurs de mesure liées au PIB potentiel. [Commission européenne, in ’t Veld, tableau 4, p. 8](https://ec.europa.eu/economy_finance/publications/economic_paper/2013/pdf/ecp506_en.pdf#page=11)

| Destination | Ajustement 2011–13, points de PIB potentiel | Exportations françaises de biens 2007–10 | Exportations 2010–13 | Exportations 2013–15 | Importations totales du partenaire 2010–13 |
|---|---:|---:|---:|---:|---:|
| Allemagne | 2,61 | +2,2 % | +11,6 % | +1,5 % | +8,2 % |
| Italie | 3,95 | −12,9 % | −2,7 % | +5,1 % | −10,8 % |
| Irlande | 4,04 | −28,3 % | +16,0 % | +8,3 % | +10,3 % |
| Espagne | 4,45 | −22,5 % | +0,4 % | +12,7 % | −6,7 % |
| Portugal | 6,73 | −16,1 % | −2,5 % | +6,5 % | −8,0 % |
| Grèce | 8,91 | −27,9 % | −13,5 % | −8,4 % | −17,8 % |

Les trois colonnes d’exportations expriment des variations entre deux niveaux nominaux annuels en euros courants. La dernière colonne compose les variations annuelles en volume des importations de biens **et services**, toutes origines. Les différences entre colonnes reflètent aussi les prix, les produits, la part française dans les importations et les différences de champ. Le périmètre du déclarant France dans Comext intègre Mayotte à partir de 2014. [Eurostat, extrait Comext](comext_exportations.json) · [Eurostat, extrait des comptes nationaux](eurostat_importations.json)

**Un gradient existe, mais il précède le traitement.** La corrélation de rang entre la sévérité du resserrement et les ventes françaises est de −0,54 en 2010–2013. Elle reste négative lorsqu’on retire tour à tour un pays (de −0,90 à −0,20). Les variations des importations en volume classent les six pays dans le même ordre que les ventes françaises en valeur sur cette fenêtre. Elles donnent donc le même coefficient. Le total des ventes françaises aux six partenaires **augmente de 4,9 % en valeur**. Pour savoir combien de commandes la France a perdues, il faudrait connaître les achats qui auraient eu lieu sans la consolidation. [Calculs](calculs.py)

La corrélation avec les exportations était déjà de −0,60 en 2007–2010, et de −0,14 en 2007–2009. La première fenêtre comprend le début d’ajustements de crise, dont celui de la Grèce, et le rebond inégal de 2010. Aucune n’offre de tendance commune assurée. En 2013–2015, la corrélation entre les anciens efforts et la croissance des ventes tombe à −0,03, et l’Espagne connaît la plus forte hausse. Ces six destinations n’offrent ni affectation aléatoire ni groupe témoin épargné. Le risque souverain, le crédit, la spécialisation française et la demande privée peuvent déterminer ensemble les plans et les flux. Une régression ajustée sur six pays donnerait une précision trompeuse. [Données utilisées et calcul](calculs.py)

L’étude d’Antoine Goujard fournit une comparaison indépendante sur 1978–2009. Elle associe les décisions de consolidation retracées dans les textes budgétaires des pays importateurs aux échanges bilatéraux, en tenant compte des particularités de chaque paire et des chocs annuels communs aux destinations d’un même exportateur (équation 5). Pour un point de PIB de consolidation, le tableau 3 donne −1,367 point de croissance des exportations bilatérales, avec un effet additionnel de −2,286 en union monétaire, soit environ −3,7 au total. L’échantillon couvre 561 paires et 14 521 observations. La sélection narrative réduit la causalité inverse liée à la conjoncture. La réaction à des tensions financières et la transposition d’une moyenne historique à 2011–2015 restent des objections. Le coefficient concerne les exportations bilatérales, grandeur très différente du PIB ou du solde français. [OCDE, document de travail 1099, § 46–49 et tableau 3](https://www.oecd.org/content/dam/oecd/en/publications/reports/2013/12/cross-country-spillovers-from-fiscal-consolidations_g17a2435/5k3txn1mbw8x-en.pdf)

## Quelle fraction du frein français vient des partenaires ?

La **DG Trésor** applique en 2016 les coefficients de QUEST aux ajustements structurels primaires recalculés avec les prévisions européennes d’automne 2015. Dans cet exercice, la part imputée aux partenaires passe de 23 % en 2011 à **47 % en 2013**. Le calcul utilise les deux colonnes du même tableau. Les niveaux annuels incluent les effets passés et ne s’additionnent pas. [Trésor-Éco 163, encadré 2, tableau 1, p. 6](https://www.tresor.economie.gouv.fr/Articles/a5a22495-83b8-41ee-9eb2-3ec2828f8b65/files/4c1ee581-0deb-4e73-ba76-b328e16d719f#page=6)

| Écart au niveau du PIB français de référence, en points | 2011 | 2012 | 2013 |
|---|---:|---:|---:|
| Effet total modélisé | −1,10 | −2,43 | −3,54 |
| Dont retombées des partenaires | −0,25 | −0,89 | −1,67 |
| Part nationale obtenue par différence | −0,85 | −1,54 | −1,87 |

La simulation suppose un effort partagé à parts égales entre recettes et dépenses, et une politique monétaire qui ne compense pas le choc initial. Or S07 trouve que les prélèvements ont porté l’essentiel de l’effort français. La hausse des primes de risque, la composition des plans, les importations évincées et le calendrier de réaction de la BCE peuvent modifier la taille des retombées. Le Trésor reprend les coefficients de la Commission. Ces deux sources constituent une même famille de modèles. [Trésor-Éco 163, encadré 2](https://www.tresor.economie.gouv.fr/Articles/a5a22495-83b8-41ee-9eb2-3ec2828f8b65/files/4c1ee581-0deb-4e73-ba76-b328e16d719f#page=6) · [S07, composition de l’effort exécuté](../../../Le_Constat_Cellule_Enquete/resultats/agents/S07.md)

Deux autres simulations isolent la **croissance annuelle**. Les périmètres étrangers, les dates de prévision, les multiplicateurs et le traitement des effets passés diffèrent.

| Frein extérieur à la croissance française, points de croissance annuelle | 2011 | 2012 | 2013 | 2014 | 2015 |
|---|---:|---:|---:|---:|---:|
| OFCE, demande adressée à la France, prévision d’avril 2015 | −0,3 | −0,7 | −0,5 | −0,2 | −0,2 |
| FMI, projections de fin 2012, 20 économies, scénario central | — | −0,2 | −0,1 | −0,1 | — |
| FMI, mêmes projections, multiplicateur plus fort | — | −0,3 | −0,2 | −0,2 | — |

Le FMI attribue environ un quart de point de croissance cumulée sur 2012–2014 aux seuls Allemagne, Italie et Espagne. Le chiffre de l’OFCE pour 2015 était une prévision en cours d’année. L’accord sur le signe, malgré des amplitudes différentes, crédibilise le mécanisme. La dispersion entre ces exercices ne définit aucune borne statistique. [OFCE, Péléraux et Plane, tableau 1, p. 9](https://ofce.sciences-po.fr/pdf/ouvrage/2016-FR-01.pdf#page=5) · [FMI, France, rapport 13/3, p. 20–21](https://www.imf.org/external/pubs/ft/scr/2013/cr1303.pdf)

## Du PIB au déficit

Dans le millésime Eurostat de S07, le solde public français observé passe de −7,2 % du PIB en 2010 à −5,3 % en 2011, −5,2 % en 2012, −4,9 % en 2013, −4,6 % en 2014 et −3,9 % en 2015. Cette amélioration de 3,3 points en cinq ans mélange politiques, cycle, taux d’intérêt et éléments exceptionnels. [Eurostat, extrait S07, S13/B9 en % du PIB](../../../Le_Constat_Cellule_Enquete/resultats/donnees/S07/sources/eurostat_solde_pct_pib.json)

Dans le **QUEST d’origine** (efforts mesurés au printemps 2013), les simulations françaises pour l’ensemble du paquet 2011–2013 sont les suivantes. Les deux dernières colonnes prolongent ce paquet initial sous les hypothèses de reprise du modèle et n’incorporent pas les nouvelles décisions effectivement prises en 2014–2015. [Commission européenne, in ’t Veld, tableaux 4–5, p. 8 et 10](https://ec.europa.eu/economy_finance/publications/economic_paper/2013/pdf/ecp506_en.pdf#page=13)

| Écart simulé à la trajectoire sans le paquet | 2011 | 2012 | 2013 | 2014 | 2015 |
|---|---:|---:|---:|---:|---:|
| Niveau du PIB français, % | −1,39 | −2,93 | −4,78 | −2,68 | −1,28 |
| Solde français des administrations publiques, points de PIB | +0,87 | +1,29 | +1,88 | +2,82 | +3,84 |

Ainsi, dans ce scénario, le solde français s’améliore malgré le recul de l’activité. Le ratio descriptif de 1,88 point de gain de solde pour 3,68 points d’ajustement primaire français cumulé annoncé dans le tableau 4 vaut environ 51 %. Il associe, au numérateur, les effets de toute la zone et, au dénominateur, une mesure structurelle en PIB potentiel. **Attribuer les 49 % restants aux partenaires serait une erreur.** L’exercice français standardisé à 1 % par an de l’annexe de QUEST suit un autre calendrier d’efforts. Le comparer directement aux −4,78 % de la simulation historique ne permet pas d’isoler l’étranger. [Commission européenne, tableaux 2, 4 et 5](https://ec.europa.eu/economy_finance/publications/economic_paper/2013/pdf/ecp506_en.pdf)

**Sensibilité conditionnelle du solde cyclique en 2013.** Avec la semi-élasticité française de 0,603 (méthode européenne millésime 2014), supposons qu’une fraction q de l’effet extérieur de −1,67 point de PIB calculé par le Trésor représente, au premier ordre, une variation de l’écart de production. Le solde cyclique rapporté au PIB varie alors d’environ 0,603 × q × (−1,67). Pour q de 0 %, 50 % ou 100 %, on obtient respectivement 0, −0,50 ou −1,01 point de PIB en 2013. Les extrêmes ne bornent **que cette composante dans cette convention**. Ni la part q ni la réaction spécifique des assiettes fiscales à un choc d’exportation ne sont observées. La variation du potentiel, les intérêts, les décisions correctrices et les effets de composition peuvent déplacer le solde total hors de cet intervalle. Aucun montant en euros ni budget « perdu » n’en découle. [Commission européenne, méthode de correction du cycle](https://ec.europa.eu/economy_finance/publications/economic_paper/2014/ecp536_en.htm) · [Sénat, valeur française de 0,603 et mode d’emploi](https://www.senat.fr/rap/l18-147-1/l18-147-10.html)

## Conclusion et test décisif

Les achats extérieurs constituent un canal empiriquement documenté. Pour la France, l’enquête retrouve une estimation officielle du frein importé, particulièrement marqué au creux de 2013. Les données commerciales écartent la version littérale d’une chute générale des exportations françaises vers les six partenaires. Elles affaiblissent aussi l’idée de lire l’effet causal directement dans les écarts entre destinations. Les scénarios autorisent simultanément un PIB plus bas et un déficit moindre que dans l’économie sans le paquet de mesures. **La baisse d’activité d’origine étrangère rend crédible une dégradation du solde à programme français donné. L’ampleur réalisée en 2011–2015 et la perte de rendement de chaque euro d’effort français restent ouvertes.**

Le prochain test empirique demanderait de dater les décisions budgétaires étrangères inattendues, distinguer leur composition et vérifier leur indépendance des crises bancaires dans chaque destination. Une exposition par branche ou territoire français, calculée à partir des parts d’exportation antérieures à la crise, permettrait de comparer commandes, valeur ajoutée et assiettes fiscales différemment exposées, avec contrôles sectoriels et tests de tendances préalables. Les retombées sur les zones moins exposées et les prélèvements nationaux limiteraient encore l’agrégation. Pour tester **le rendement**, il faudrait en outre une variation crédible de l’effort propre ou, à défaut, publier les quatre trajectoires de solde B(f,e) des mêmes modèles, avec impulsions identiques par instrument, réaction monétaire, prime de risque et hypothèses de potentiel explicites.

## Rejouer et contrôler les données

Depuis ce dossier, exécuter `python -X utf8 calculs.py` avec Python 3.10 ou ultérieur. Aucun paquet ni connexion n’est nécessaire. Le programme contrôle les empreintes des deux réponses JSON-stat, compose les taux en volume, calcule les rangs, retire chaque pays à tour de rôle et restitue les décompositions budgétaires. Les rangs utilisent des observations nationales équipondérées, la variation agrégée des ventes utilise les montants en euros.

- Les deux fichiers Eurostat sont les réponses brutes récupérées le 22 novembre 2026. Leurs métadonnées indiquent des mises à jour au 13 novembre pour Comext et au 11 novembre pour les comptes nationaux. La Grèce porte le code GR dans Comext et EL dans les comptes. Les 54 flux en euros et les 48 taux des comptes nationaux sont tous renseignés. [Requête officielle Comext](https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409?lang=EN&freq=A&reporter=FR&partner=DE&partner=ES&partner=IT&partner=GR&partner=PT&partner=IE&product=TOTAL&flow=2&indicators=VALUE_IN_EUROS&sinceTimePeriod=2007&untilTimePeriod=2015) · [Requête officielle sur les importations en volume](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?lang=EN&freq=A&unit=CLV_PCH_PRE&na_item=P7&geo=DE&geo=ES&geo=IT&geo=EL&geo=PT&geo=IE&sinceTimePeriod=2008&untilTimePeriod=2015)
- Les valeurs numériques des études et les paramètres de sensibilité sont transcrits dans un fichier distinct. Les références et les numéros de tableaux figurent auprès des résultats correspondants ci-dessus. Le dossier S07 conserve aussi les deux PDF d’origine pour la Commission (QUEST) et l’OFCE. [Transcriptions](hypotheses_et_modeles.json) · [PDF de QUEST déjà archivé](../../../Le_Constat_Cellule_Enquete/resultats/donnees/S07/sources/ec_ecp506_intveld_2013.pdf) · [PDF de l’OFCE déjà archivé](../../../Le_Constat_Cellule_Enquete/resultats/donnees/S07/sources/ofce_2016-FR-01.pdf)
