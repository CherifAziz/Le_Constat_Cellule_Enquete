# 03 · Audit factuel du script V6

> **Archive historique.** Ce document décrit le script au commit `924d875345e4216d9f5fd748ec380f4463236b21` ([version d'origine](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/03_AUDIT_FACTUEL.md)), avant l'audit indépendant. Il est conservé tel quel : ses citations du script, ses durées et ses conclusions ne décrivent pas la voix finale. Les liens relatifs qu'il contient renvoient à l'état de ce commit. Pour le texte final, voir [06_VERDICT.md](../06_VERDICT.md).

**22 novembre 2026.** Contrôle des affirmations du script [01](01_SCRIPT_V6.md), avec leurs sources et leurs incertitudes.

**Comment il a été fait.** Deux passes. La direction éditoriale a d'abord relu dans les pièces les trois appuis de la conclusion (§1). Un vérificateur indépendant a ensuite confronté 72 affirmations du script aux pièces et aux séries ; son rapport complet, ligne par ligne, est en annexe : [relecture_factuelle_agent.md](annexes/relecture_factuelle_agent.md). Ses corrections ont été appliquées au script (§3). Le tableau du §2 porte sur le texte **corrigé**.

**Verdict.** Avant corrections : 36 affirmations exactes, 24 exactes avec réserve, 6 trop fortes, 1 inexacte, 3 non sourcées, 2 non vérifiées. Toutes les corrections demandées ont été appliquées, puis une seconde série après une dernière relecture critique (§3). **Le texte corrigé n'a pas été recontrôlé par un tiers** : sept points restent à relire sur l'original avant enregistrement (§5). Le script ne prête aucune intention, ne donne aucune dette contrefactuelle, et ne laisse jamais entendre qu'une décision aurait ramené l'équilibre.

---

## 1. Les trois appuis de la conclusion, relus à la source

| Appui | Pièce relue | Résultat |
|---|---|---|
| Les trajectoires jamais tenues | Table des 38 documents de programmation (`donnees/A08/A08_programme_vs_execute.csv`), chaque valeur rattachée à une pièce ; Sénat, rapport n° 78 (2008-2009), tableau « Les programmations successives de solde public » | **Formulation corrigée.** 31 documents ont une cible à trois ans échue ; 31 manquées. Hors fenêtres de crise : 17 sur 17. Pour l'année suivante : 15 tenues sur 37. Sept documents visent 2026 à 2030 et ne peuvent pas encore être jugés |
| Les cinq dates de retour à l'équilibre | Même table ; Sénat n° 78 pour 2005, 2010 et 2012 ; programme de stabilité d'avril 2012 (tableau 2) pour 2016 ; Sénat n° 438 (2017-2018), p. 23, pour 2022 | **Établi, les cinq cibles relues dans les pièces.** Avril 2012 : « balanced public finances will be restored by 2016 » ; avril 2018 : solde de +0,3 en 2022. 2005 et 2010 sont des cibles à trois ans ; 2012, 2016 et 2022 à quatre ans. Soldes réalisés : −3,5 ; −7,2 ; −5,2 ; −3,8 ; −4,7 % du PIB. Trois échéances touchées par une crise (2010, 2012, 2022), deux non (2005, 2016) |
| La règle d'affectation des surplus | Cour des comptes, enquête sur la dette des entités publiques, annexée au rapport du Sénat n° 338 (2018-2019), p. 73-74 | **Formulation corrigée.** La règle date de la loi organique du 12 juillet 2005. La Cour écrit qu'elle « n'a pas eu d'effet notable sur la trajectoire de l'endettement » et que « les annexes budgétaires des projets de loi de règlement ne retracent aucune occurrence de mise en œuvre de la règle ». Une loi de finances rectificative peut la modifier « sans limite » |
| Les 42 budgets | `donnees/S12/s12_partieA_majorites_vote.csv` : 51 lignes. Décompte repris de la table et recompté ; les scrutins eux-mêmes n'ont pas été rouverts pour ce dossier | **Repris, avec deux réserves.** 22 budgets votés par un seul groupe, 20 par une coalition, 1 grâce à des non-inscrits (1987), 8 sans majorité absolue. Pour 36 exercices, la composition est relevée à la date la plus proche du vote. Le dossier prévient que ce décompte « ne départage rien » à lui seul |

## 2. Affirmations qui portent le film

Statuts : **É** établi sur pièce ou série · **C** vrai sous la condition dite dans le script · **I** interprétation du film (voir §4) · **G** connaissance générale, non sourcée dans le corpus.

| Séq. | Affirmation (texte corrigé) | Statut | Source |
|---|---|---|---|
| Ouv. | En 1980, il manque 0,4 % de ce que le pays produit ; jamais aussi près depuis | É | Série Insee, mai 2026 (`codex/calculs/annuel.csv`) : −0,43 % ; meilleur résultat ultérieur −1,31 % (2000) |
| Ouv. | Un rapport du Sénat de novembre 1980 annonce que la Sécurité sociale va replonger | É | Sénat n° 102 (1980-1981), t. III, page imprimée 23 |
| 1 | Six déficits entre 1960 et 1974 | É | Série Insee ; contre-expertise finale |
| 1 | Prime de 250 francs par enfant ; le budget de l'État avait basculé avant le plan | É | Sénat, bulletin des commissions, septembre 1975 ; Insee, note de conjoncture d'avril 1976 (lue par lien) |
| 2 | Dépense : un peu moins de 7 % par an, puis un peu moins de 5 ; croissance divisée par plus de deux | É | Insee, tableaux 3.201 et 1.102 : 6,71 puis 4,75 % ; 5,62 puis 2,20 % |
| 2 | Elle ralentit par rapport aux années soixante ; garde son rythme par rapport aux dernières années d'avant-crise | C | Contre-expertise : vrai contre 1960–1973 ; contre 1968–1973 elle dépasse légèrement sa tendance |
| 2 | Quatre cinquièmes de la montée faits dès 1985 | É | 12,84 points sur 15,97 |
| 2 | « Pour l'essentiel » des règles écrites avant la crise | C | Décomposition de convention : 13 à 32 % de la hausse des prestations vient de décisions postérieures à 1974 |
| 2 | Préretraites : huit fois plus en 1985 qu'en 1973 | É | 0,14 puis 1,14 point de PIB (dossier S10) |
| 2 | Hôpital : un an prévu, quatorze en réalité | É | Sénat n° 43 (1973-1974), p. 22 ; n° 103 (1974-1975), p. 20 ; n° 128 (1979-1980), p. 22 ; contre-expertise |
| 3 | De 1978 à 1980, l'État ne fait qu'un huitième du chemin environ | É | `D02_variations_soldes_par_periode.csv` : État 13,2 % du gain, Sécurité sociale 57,1 % |
| 3 | Près de 11 milliards de francs de déficit en 1978 | É | Sénat n° 102, t. III : −10,8 (régime général) |
| 3 | En 1980, avant intérêts, la France encaisse plus qu'elle ne dépense ; c'est rare | É | +0,80 % ; neuf années sur cinquante et une |
| 4 | Cotisation de 1 %, 30 francs sur 3 000, du 1er août 1979 au 31 janvier 1981 | É | Sénat n° 54 (1979-1980), t. IV, p. 31 et 46 ; n° 102, t. III, p. 9 |
| 4 | Le décret n'a pas été retrouvé | É | Fac-similé du décret n° 79-650 non obtenu |
| 4 | 88 % de l'excédent de la Sécu des salariés | É | 9,352 sur 10,669 milliards de francs (régime général) |
| 5 | Déficit de 3,2 milliards annoncé pour 1981 | É | Sénat n° 102, t. III, page imprimée 23 |
| 5 | Seule justification retrouvée : « en faveur de la consommation » | É | Sénat n° 98 (1980-1981), t. I, p. 107. Aucun document du gouvernement n'a été lu |
| 5 | Le déficit est multiplié par plus de cinq en 1981 | É | −0,43 puis −2,43 % |
| 6 | La fin de la cotisation pèse 11 à 15 % de la dégradation | C | Arithmétique sur neuf mois, à assiette inchangée (dossier D02) |
| 6 | La retraite à 60 ans entre en vigueur en 1983 | É | Dossier D07 ; le jour exact n'est pas dans le corpus |
| 6 | Chômeurs indemnisés : d'un million à près de 1,3 million entre le second semestre 1980 et le premier semestre 1981 | É | Sénat n° 32 (1982-1983), p. 14 : 1,01 puis 1,27 million |
| 6 | Plus de 5 milliards de francs sans recette en face ; les taux montaient déjà | É | Sénat n° 311 (1980-1981), p. 57 et p. 34 |
| 7 | « supprimée 9 mois plus tôt » | É | Commission des comptes de la Sécurité sociale, décembre 1982, p. 9 |
| 8 | 60–64 ans : quatre sur dix en 1975, un sur dix en 2001 | É | Insee, enquête Emploi : 40,5 puis 10,8 % |
| 8 | Heures : à peu près autant en 1974, 8 % de moins en 1990 | C | AMECO, médiane de sept pays ; en 1974 le signe dépend du panel |
| 9 | Intérêts multipliés par six de 1974 à 1996 | É | 0,59 puis 3,61 % du PIB |
| 9 | 1993 : pire déficit depuis le début de la série ; CSG plus que doublée | É | −6,40 % ; taux de 1,1 à 2,4 % |
| 9 | Passer sous 3 % en 1997 pour l'euro ; de justesse dans les comptes de l'époque | G / É | Critère général ; 3,0 % à l'époque, 3,7 % dans la série actuelle ; soulte de France Télécom (dossier de Codex) |
| 9 | 1998 à 2001 : excédent avant intérêts quatre années de suite | É | +0,99 ; +1,53 ; +1,65 ; +1,64 |
| 10 | 51 milliards de francs ; quatre cinquièmes en baisses d'impôts | É | Projet de loi n° 2335 ; Sénat n° 371 : « à hauteur de 80 %, soit 40,6 milliards » |
| 10 | Le mot « cagnotte » | É | Sénat, rapport sur le règlement du budget 2000 |
| 10 | Les deux citations du projet de loi | É | Projet n° 2335, exposé général. Le « niveau inchangé » est celui du budget de l'État |
| 10 | Une partie de la recette classée « exceptionnelle » | É | Projet n° 2335 : 15,4 milliards de recettes non fiscales exceptionnelles |
| 10 | La commission des finances du Sénat propose une autre voie | É | Sénat n° 371 : « par redéploiement » |
| 10 | Tout garder couvrait au maximum 41 % du déficit | C | 7,84 sur 19,1 milliards d'euros ; borne à activité inchangée |
| 10 | Les impôts venaient de beaucoup monter | É | Recettes : 50,1 % du PIB en 1993, 52,1 % en 1999 ; approfondissements, découverte 4.9 |
| 11 | Depuis vingt-quatre ans, aucun excédent avant intérêts ; 2006 frôle zéro | É | 2002 à 2025 ; −0,05 % en 2006 (une variante de l'Insee donne un léger excédent) |
| 11 | Italie : dix années sur dix | É | Comparaisons de Codex |
| 11 | « près de 3 points de PIB » | É | Rapport sur la situation des finances publiques, avril 2010 |
| 11 | 12 milliards d'euros de baisses nouvelles en 2007 | É | Cour des comptes, juin 2008 (dossier de Codex) ; 6,9 milliards viennent d'une réforme votée fin 2005 |
| 11 | Entre 2011 et 2013, les impôts remontent fortement | É | +2,4 points sur 2012–2016 |
| 12 | Quatre fois sur dix, aussi bien ou mieux que prévu pour l'année suivante | É | 15 sur 37 |
| 12 | Trente et une sur trente et une ; dix-sept sur dix-sept | É | Voir §1 |
| 12 | Gouvernements de gauche, de droite et du centre | G | Dates des programmes : décembre 2001, décembre 2006, novembre 2007, avril 2012, avril 2018 |
| 13 | Une marche d'au moins deux mois de production à chaque crise | É | Dette : +20,8 points de 2007 à 2010 ; +16,8 de 2019 à 2020 |
| 13 | Les mesures d'urgence et de relance coûtent encore plus de 80 milliards d'euros en 2021, 12 en 2023 | É | Cour des comptes, juillet 2024, via le dossier A03 : 72,5 ; 83,7 ; 34,9 ; 12,4 milliards de 2020 à 2023 |
| 13 | Sous surveillance européenne en 2011 ; la zone euro vacille | É / G | Procédure de déficit excessif de 2009 à 2018 ; contexte général |
| 13 | Plus des quatre cinquièmes par les impôts ; près de la moitié par les intérêts | É | 83 % sur 2011–2014 ; 46 % sur 2012–2015 |
| 13 | À partir de 2018, les impôts rebaissent | C | Cumul 2017–2025 négatif dans les deux conventions (−1,24 à −0,41 point) |
| 14 | Écart de 3 points en 1985, de 5 en 2025 | É | 54,2 contre 51,2 ; 57,3 contre 52,2 |
| 14 | Plus de la moitié de la dépense : retraites, santé, allocations | É | Structure de la dépense 2025 |
| 14 | 78 milliards d'euros d'allègements | É | 77,6 milliards en 2025 |
| 14 | Estimation de un à six ; aucune étude ne mesure le rendement pour les finances publiques | C | Vaut pour la première vague ; la contre-expertise confirme l'absence de rendement budgétaire mesuré |
| 15 | 458 contre, zéro pour | É | Assemblée nationale, 4 novembre 2026 |
| 15 | Des efforts sont retirés en séance | É | Audit de la V5, ligne 125, classée exacte |
| 15 | Quarante-deux sur cinquante et un | É | Voir §1 |
| Concl. | Sous les 3 % en 2029 ; « caractère conventionnel » ; au prochain gouvernement d'en définir une autre | É | Rapport annexé au projet de loi de finances pour 2027, p. 134 : « il appartiendra au prochain Gouvernement de définir une nouvelle trajectoire pluriannuelle après les élections » |

## 3. Corrections appliquées au script

| Séq. | Avant | Après | Raison |
|---|---|---|---|
| Ouv. | « dans une seule situation » | « presque toujours dans la même situation » | Trop fort |
| 1 | « La relance n'a pas creusé le trou » | « n'a pas ouvert le trou » | Contrefactuel : le plan a eu un coût |
| 2 | « Personne n'a appuyé sur l'accélérateur » | « Il n'y a pas eu de grand coup d'accélérateur » | Des décisions postérieures à 1974 ont compté |
| 3 | « à peine un huitième de l'effort » | « de 1978 à 1980, il ne fait qu'un huitième du chemin environ » | Période précisée ; source ajoutée |
| 3 | « rarissime » | « rare » | Neuf années sur cinquante et une |
| 4 | « tenait presque entièrement » | « tenait toutefois presque entièrement » | Citation tronquée |
| 6 | « Un septième, au mieux » | « Moins d'un sixième » | 15 % dépasse un septième |
| 6 | « Avant mai » | « L'essentiel de la hausse est là quand le nouveau pouvoir s'installe » | La moyenne du semestre inclut mai et juin |
| 6 | « Après l'élection, les taux d'intérêt s'envolent » | « Les taux d'intérêt, qui montaient déjà, grimpent encore après l'élection » | Ils montent avant et après |
| 9 | « La France y parvient de justesse » | « Dans les comptes de l'époque, la France y parvient de justesse » | 3,7 % dans la série actuelle |
| 10 | « Et pour le déficit ? […] à un niveau inchangé » | « Et le déficit du budget de l'État ? » | La citation porte sur le budget de l'État |
| 13 | « une marche d'une vingtaine de points » | « au moins deux mois de tout ce que le pays produit » | Unité absente ; 16,8 points en 2020 |
| 14 | « Les deux ont monté ensemble » | « La dépense a monté plus vite que les recettes » | +3,1 points contre +1,1 |
| 14 | « du simple au sextuple » | « Pour les premiers allègements […] de un à six » | Vaut pour la première vague seulement |
| 15 | « les votes un par un, au Journal officiel » | « les budgets un par un, avec la composition de l'Assemblée au moment du vote » | Méthode réelle |
| Concl. | « Et d'abord en prélevant plus » | « deux fois sur trois, presque uniquement en prélevant plus » | Dans les années 1990, la baisse du poids de la dépense compte aussi |
| Concl. | « 1981 : une recette qu'on laisse s'éteindre » | « 1980 : la Sécurité sociale est redevenue excédentaire, et on laisse s'éteindre la recette qui fait cet excédent » | La décision date de 1980, l'échéance de 1979 |
| Concl. | « 2018 : des impôts qu'on rebaisse » | « À partir de 2018 » | Mouvement étalé sur plusieurs années |
| **Seconde série, après relecture critique** | | | |
| 13 | « plus de 80 milliards d'euros de soutien sont retirés dès 2021 » | « En 2021, les mesures d'urgence et de relance du Covid coûtent encore plus de 80 milliards d'euros. Deux ans plus tard : 12 » | **Erreur de lecture** : 83,7 milliards est le montant dépensé en 2021, pas le montant retiré. L'erreur venait de la base factuelle |
| Ouv. | « a failli sortir du déficit » | « est passée à deux doigts de l'équilibre » | Les pièces établissent la proximité, pas une possibilité réelle d'atteindre zéro |
| 6 | « L'arrivant dépense sans financer » | « engage des dépenses qu'il ne finance qu'en partie » | 5,3 milliards de francs non financés, 7,7 financés par des taxes temporaires |
| 7, 9 | « La porte de 1980 se referme » ; « la ligne est de nouveau à portée » | « L'occasion de 1980 est passée » ; « s'est de nouveau rapprochée de la ligne » | Ne pas laisser entendre que l'équilibre était atteignable par une décision |
| 11 | « chaque année, le budget répond » | « pendant des années » | La Cour l'atteste pour 2010 à 2018 |
| 12 | « Cinq fois, la France a écrit… » | « à trois ou quatre ans de distance » | Trois des cinq cibles sont à quatre ans |
| 8, 14 | « le pays les finance d'abord sur le travail » ; « n'est jamais revenue au niveau » | « une grande partie […] est prélevée sur le travail » ; « reste plus étroite » | Formulations plus fortes que les pièces |
| Concl. | « presque uniquement en prélevant plus » | « surtout en prélevant plus » | 83 % en 2011–2014 |

## 4. Ce qui est une interprétation du film

Ces phrases ne sont pas des faits. Le script les présente comme la lecture de trois épisodes et le dit (« trois épisodes ne font pas une loi »).

| Phrase | Ce qui la soutient | Ce qui la limite |
|---|---|---|
| « Un pays qui sait très bien redresser ses comptes. Mais presque toujours dans la même situation » | Trois redressements documentés : 1975–1980, 1993–2000, 2010–2018 | Trois cas ; « dos au mur » qualifie des contextes différents (caisse en déficit, critère d'entrée dans l'euro, procédure européenne) |
| « Trois fois, le dos au mur » | 10,8 milliards de francs de déficit du régime général en 1978 ; année de qualification pour l'euro ; procédure de déficit excessif de 2009 à 2018 | La première enquête note que les seules cibles tenues l'ont été sous procédure européenne, et précise : coïncidence sur deux épisodes, pas causalité |
| « Elle a rendu une partie de ce qu'elle venait de gagner » | 1980 : recette non prolongée ; 2000 : le mot « restituer » est celui du projet de loi ; baisses à partir de 2018 | Aucun de ces gestes n'explique le déficit seul : 11 à 15 % en 1981, 41 % au plus en 2000. Le cumul des décisions fiscales change de signe selon l'année de départ |
| « La France a un problème avec les bonnes années » | Aucun excédent avant intérêts depuis 2002 alors que les aides de crise ont été retirées ; règle de 2005 sans effet | La France a aussi laissé filer des années ordinaires ; 2025, sans récession, est à −5,1 % |
| « Il la tient, au jour près. […] Il ne l'a jamais tenue » | Fin de la cotisation au 1er février 1981 ; cinq dates d'équilibre manquées | Les deux engagements ne sont pas de même nature : une échéance juridique d'un côté, une prévision de l'autre |
| « Un écart ancien, que chaque gouvernement a trouvé en arrivant. Et laissé en partant » | Écart de 3 points en 1985, de 5 en 2025 | Image : l'écart a varié, il a été presque refermé en 2000 (−1,3 %) |

## 5. À relire avant enregistrement

| # | Point | Pourquoi |
|---|---|---|
| 1 | Citation du Sénat n° 78 (2008-2009) : « contentées de décaler, chaque année ou presque, l'objectif de retour à l'équilibre » | Retrouvée dans le texte conservé après réparation de l'encodage ; le vérificateur ne l'a pas retrouvée par recherche simple. À lire sur la page d'origine |
| 2 | Les 38 documents de programmation | Les valeurs sont rattachées à des pièces, mais seule une partie a été relue pour ce dossier (2005, 2010, 2012 sur le tableau du Sénat ; 2027 à 2030 sur le budget 2027) |
| 3 | « au moment du vote » pour les 42 budgets | 36 compositions sont relevées à la date la plus proche, pas au jour exact. Trois exercices (1988, 2015, 2017) tiennent à zéro ou un siège |
| 4 | Jour d'entrée en vigueur de la retraite à 60 ans | Le corpus donne l'année, pas le jour |
| 5 | Fac-similé du décret du 30 juillet 1979 | Toujours absent ; le script le dit |
| 6 | Les trois Premiers ministres nommés et « de gauche, de droite et du centre » | Connaissance générale, à valider sur la liste des gouvernements conservée au dépôt |
| 7 | Une de presse avec le mot « cagnotte » | À trouver ; le mot lui-même est attesté par le Sénat |

**Limite de l'audit.** Le vérificateur et la rédaction sont le même modèle. Une relecture par l'équipe indépendante reste nécessaire avant diffusion, en priorité sur l'acte IV et la conclusion, écrits en dernier.
