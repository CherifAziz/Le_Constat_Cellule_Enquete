# A10 — Annexe : enquêtes d'opinion françaises sur le déficit, la dette et l'acceptation des mesures

Règle : une enquête n'entre dans le tableau des faits que si l'on dispose de l'institut, du commanditaire, des dates de terrain, de la question exacte et de l'échantillon. Sinon elle va en §13 du dossier principal. Niveau de preuve d'un sondage : E (échelle A–F de `04_PREUVES_ET_CALCULS.md`), même quand il est bien fait ; il mesure une opinion déclarée, pas un comportement.

---

## O-1. Baromètre d'opinion de la DREES (2000-2025) — source institutionnelle principale

- **Commanditaire** : DREES (ministères sociaux). **Institut** : BVA puis Ipsos bva (vague 25, 2025) ; changement d'institut entre 2002 et 2004, pas d'enquête en 2003 (Baudouin, Guillaud & Zemmour 2022, PDF p. 6, note 4).
- **Mode et échantillon (vague 2025)** : face à face assisté par tablette (CAPI), **4 002 personnes** de 18 ans et plus, quotas sexe-âge-profession de la personne de référence, stratification région × catégorie d'agglomération, terrain **du 13 octobre au 18 décembre 2025** ; quatre sous-échantillons aléatoires d'environ 1 000 personnes pour les questions à versions multiples (note méthodologique Ipsos bva 2025, p. 4-5). Description générale DREES : enquête annuelle depuis 2000, au moins 3 000 personnes, face à face, France métropolitaine (métadonnées du jeu de données).
- **Provenance** : [C] microdonnées `barometre2000_2025_diff.csv` (52,7 Mo, sha256 b7ad24a2…), dictionnaires des variables et des libellés 2025, questionnaire 2025 (75 p.), note méthodologique 2025 (82 p.), « read me » du 3 juillet 2026, téléchargés le 20/11/2026 par l'API data.drees.solidarites-sante.gouv.fr (jeu 431_le-barometre-d-opinion), copies dans `resultats\donnees\A10\sources\drees_barometre\`. Les pages HTML et PDF de drees.solidarites-sante.gouv.fr ont renvoyé une page de défi JavaScript : [X].
- **Calcul** : script `resultats\scripts\A10\drees_barometre_series.py` ; parts pondérées (variable `poids`) parmi les personnes à qui la question a été posée, non-réponse gardée comme modalité ; sortie `resultats\donnees\A10\drees_series_ponderees.csv`. Ces parts sont recalculées par A10 ; elles peuvent différer au dixième des publications DREES (traitement des non-concernés).
- **Limites** : sondage par quotas (pas d'intervalle de confiance au sens strict ; à N ≈ 4 000, l'ordre de grandeur de l'aléa d'échantillonnage est ±1,5 point, à N ≈ 1 000 ±3 points) ; pas un panel ; questions en modules d'années paires/impaires ; changement d'institut ; selon Baudouin et al., l'usage recommandé par la DREES est de commenter les **évolutions** plutôt que les niveaux (Baudouin et al. 2022, PDF p. 16).

### Questions exactes et résultats recalculés (parts pondérées, %)

**OG04_5** — « Pour chacun des sujets suivants, dites-moi s'il VOUS préoccupe VOUS PERSONNELLEMENT beaucoup, assez, peu ou pas du tout ? … La dette de la France » (item depuis 2014, ordre des items aléatoire).

| Année | Beaucoup | Assez | Peu | Pas du tout | N |
|---|---:|---:|---:|---:|---:|
| 2014 | 41,6 | 29,9 | 17,0 | 11,4 | 3 009 |
| 2015 | 34,3 | 32,6 | 20,4 | 12,7 | 3 023 |
| 2016 | 31,3 | 31,8 | 21,1 | 15,7 | 3 038 |
| 2017 | 24,8 | 34,8 | 25,1 | 15,0 | 3 009 |
| 2018 | 20,6 | 34,8 | 25,8 | 18,0 | 3 037 |
| 2019 | 18,7 | 33,7 | 27,9 | 19,2 | 3 030 |
| 2020 | 22,3 | 35,9 | 25,2 | 15,7 | 4 002 |
| 2021 | 18,7 | 34,1 | 26,8 | 19,7 | 4 002 |
| 2022 | 19,8 | 33,8 | 27,1 | 19,0 | 4 002 |
| 2023 | 18,9 | 33,1 | 29,4 | 17,8 | 4 002 |
| 2024 | 26,6 | 37,3 | 23,7 | 12,0 | 4 002 |
| 2025 | 33,6 | 36,1 | 21,6 | 8,5 | 4 002 |

**PS16** — « Pour vous, quel est le plus important : 1. Prendre des mesures pour réduire le déficit de la Sécurité sociale ; 2. Maintenir au niveau actuel les prestations sociales et les remboursements d'assurance maladie » (module années impaires 2015 ; 2020-2021 ; socle depuis 2023).

| Année | Réduire le déficit | Maintenir les prestations | NSP | N |
|---|---:|---:|---:|---:|
| 2015 | 46,9 | 52,2 | 1,0 | 3 023 |
| 2017 | 40,8 | 58,0 | 1,2 | 3 009 |
| 2019 | 37,3 | 59,5 | 3,2 | 3 030 |
| 2020 | 34,7 | 60,8 | 4,5 | 2 001 |
| 2021 | 36,4 | 59,8 | 3,8 | 2 002 |
| 2023 | 38,5 | 57,2 | 4,2 | 4 002 |
| 2024 | 42,3 | 54,3 | 3,4 | 4 002 |
| 2025 | 47,2 | 50,1 | 2,7 | 4 002 |

**PS03** — « La France consacre environ le tiers du revenu national au financement de la protection sociale. Considérez-vous que c'est … ? Excessif / Normal / Insuffisant ». Part « excessif » : 12,7 (2000) ; 16,1 (2007) ; 11,3 (2009) ; 20,1 (2013) ; 21,6 (2014) ; 13,6 (2017) ; 14,9 (2020) ; 15,8 (2023) ; 19,4 (2024) ; **23,1 (2025)**. « Normal » entre 50,5 et 66,9 sur toute la période ; « insuffisant » de 29,8 (2000) à 12,8 (2025).

**PS15_3** — « Notre système de sécurité sociale coûte trop cher à la société » (tout à fait + plutôt d'accord) : 66,9 (2014) ; 54,4 (2019) ; 56,1 (2021) ; 60,5 (2022) ; 59,9 (2023) ; 64,0 (2024) ; **68,3 (2025)**.

**SA08** — « Voici différentes mesures qui viseraient à réduire le déficit de la branche maladie de la Sécurité sociale s'il devenait trop important. Pour chacune de ces mesures, dites-moi si vous y seriez plutôt favorable ou plutôt opposé.e ? » (part « plutôt favorable »)

| Mesure | 2005 | 2010 | 2013 | 2017 | 2019 | 2021 | 2023 | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Limiter le remboursement pour certaines prestations | 48,3 | 42,8 | 52,2 | 40,4 | 34,8 | 35,2 | 31,5 | 38,8 |
| Réduire la prise en charge des longues maladies (depuis 2009) | – | 15,2 | 17,1 | 13,3 | 15,2 | 16,2 | 15,0 | 17,3 |
| Taxer davantage les fabricants de médicaments (depuis 2014) | – | – | – | 78,4 | 80,7 | 80,8 | 82,7 | 80,2 |
| Augmenter les prélèvements sur les revenus des ménages (cotisations salariées, CSG) (libellé depuis 2023) | – | – | – | – | – | – | 12,4 | 12,4 |
| Augmenter les cotisations employeurs (depuis 2023) | – | – | – | – | – | – | 47,5 | 38,7 |

**ME02 (2025, expérience à quatre versions tirées au sort, ≈1 000 répondants chacune)** — préambule commun « En France, le déficit de la sécurité sociale a atteint 15 milliards d'euros en 2024. » puis : A sans ajout ; B « Actuellement, 28 % du budget de la sécurité sociale est financé par la TVA. » ; C idem + « en contrepartie des allègements des cotisations sur les bas salaires » ; D « La TVA est un prélèvement qui pèse davantage sur le budget des ménages les plus modestes… ». Question : « Seriez-vous favorable à mettre en place une TVA sociale, c'est-à-dire une hausse de la TVA pour réduire le déficit de la sécurité sociale ? » (questionnaire 2025, p. 48-49). Part favorable (tout à fait + plutôt) : **A 27,2 ; B 27,1 ; C 28,2 ; D 28,8**. Les écarts entre versions (≤ 1,7 point) sont inférieurs à l'aléa d'échantillonnage : **aucun effet mesurable de l'information ni du cadrage distributif sur ce sujet**.

**PS13** — prestations qu'il serait acceptable de **diminuer** « en échange d'une baisse des impôts ou des cotisations » (versions A/B) ou qu'il serait nécessaire d'**augmenter** « même si cela implique une augmentation des impôts ou des cotisations » (versions C/D). Retraites : acceptent de diminuer (oui tout à fait + plutôt) 8,9 % en 2020, 11,9 % en 2024, 13,9 % en 2025 ; jugent nécessaire d'augmenter même avec hausse d'impôts 54,5 % (2020, version D), 63,7 % (2023, D), 53,1 % (2025, D). Assurance maladie : acceptent de diminuer 14,6 % (2020), 18,4 % (2025).

**RE09BIS / RE09** — « Compte tenu des réformes engagées ces dernières années, pensez-vous que pour préserver le système de retraite par répartition tel qu'il existe… les réformes déjà effectuées sont suffisantes / des réformes supplémentaires sont nécessaires » : « réformes supplémentaires nécessaires » 71,7 (2016), 73,1 (2017), 57,2 (2020), 53,4 (2022), 54,8 (2023), 53,3 (2024), **66,6 (2025)**. Puis, parmi ceux-là, solution préférée (2025, N = 2 669) : cotisations employeurs 26,5 ; allonger la durée de cotisation 20,3 ; relever l'âge minimal 17,7 ; contribution des retraités (gel des pensions, CSG) 5,7 ; cotisations salariales 4,9 ; autre réforme 20,5.

**ME01 (2025)** — « Selon l'idée que vous vous en faites, diriez-vous que le niveau des impôts et des cotisations sociales payés par chacune des populations suivantes est… trop élevé / pas assez élevé / juste ? » : les 10 % les plus aisés « pas assez élevé » 69,8 % ; les classes moyennes « trop élevé » 60,5 % ; les retraités « trop élevé » 55,0 %.

### Ce que ces séries établissent et n'établissent pas
1. **Écart entre principe et mesure, mesuré dans la même enquête** (pas supposé) : en 2025, 47,2 % jugent plus important de réduire le déficit de la Sécurité sociale que de maintenir les prestations, et 68,3 % estiment que le système « coûte trop cher » ; mais seuls 12,4 % acceptent une hausse des prélèvements sur les ménages, 17,3 % une moindre prise en charge des longues maladies, 38,8 % une limitation de certains remboursements, 27-29 % une TVA sociale. Les mesures qui recueillent une majorité font payer un tiers identifié comme extérieur (fabricants de médicaments 80,2 %). Ce sont des répondants différents d'une question à l'autre uniquement pour ME02 ; pour PS16, PS15 et SA08, ce sont les mêmes répondants, mais le croisement individuel n'a pas été calculé ici (piste en §13).
2. **La préoccupation pour la dette varie dans le temps** : elle baisse de 2014 à 2019-2023 (« beaucoup » de 41,6 à 18,7-19,8 %) puis remonte en 2024-2025 (26,6 puis 33,6 %). La préférence pour la réduction du déficit (PS16) suit le même profil (34,7 % en 2020 → 47,2 % en 2025). Ces mouvements sont compatibles avec un effet de saillance médiatique et politique (débats budgétaires 2024-2025), mais **aucune cause n'est isolée** : un sondage annuel ne permet pas de dater la réaction à un épisode.
3. Ces séries portent sur la **Sécurité sociale et la protection sociale**, pas sur le budget de l'État ni sur le déficit public total.

## O-2. Expérience de formulation dans le baromètre DREES 2020 (Baudouin, Guillaud & Zemmour, 2022)

- **Pièce** : Florian Baudouin, Elvire Guillaud, Michaël Zemmour, « Les déterminants du soutien au financement de la protection sociale : une étude sur les données du baromètre DREES », version du 15-17 mars 2022, document n° 4 de la séance plénière du COR du 24 mars 2022 « Les opinions sur les retraites », document de travail « rapport préliminaire – merci de demander aux auteurs avant de citer ». [C] PDF 30 p. (`cor_2022_doc04_soutien_financement.pdf`, sha256 30135721…), canal cor-retraites.fr.
- **Méthode** : en 2020, l'échantillon de 4 000 personnes est divisé aléatoirement en quatre versions de ≈1 000 : A « Accepteriez-vous une baisse de la prestation suivante en échange d'une baisse de vos impôts ou de vos cotisations ? » ; B « Accepteriez-vous une hausse de vos impôts ou de vos cotisations pour financer l'augmentation des prestations suivantes ? » ; C « En contrepartie d'une baisse des impôts ou des cotisations, trouveriez-vous acceptable de diminuer les prestations suivantes ? » ; D « Parmi les prestations suivantes, lesquelles vous semble-t-il nécessaire d'augmenter, même si cela implique une augmentation des impôts ou des cotisations ? » (PDF p. 7).
- **Résultats** (PDF p. 8-12) : B → D fait passer le soutien de 18 % à 36 % pour l'assurance maladie et de **27 % à 56 % pour les retraites** (changement de majorité par la seule formulation). Opposition à la baisse : 85 % (maladie), 86-91 % (retraites). Opposition à la hausse (B) : 82 % (maladie), 73 % (retraites). En combinant A et B sous hypothèse de non-contradiction : maladie 15 % pour une baisse conjointe, 18 % pour une hausse conjointe, **67 % statu quo** ; retraites 14 %, 26 %, **60 % statu quo**. Les auteurs concluent à un « fort biais en faveur du statu quo » qui conduit à rejeter une réforme « quelle qu'en soit la direction », sans pouvoir dire si c'est un effet de questionnaire ou une préférence ancrée (résumé, PDF p. 3).
- **Tendance longue** (PDF p. 16) : part totalement opposée à une baisse des pensions en échange d'une baisse des prélèvements : environ 50 % dans les années 2000, plus de 80 % en fin de période ; favorables à une baisse : environ 30 % au début des années 2000, à peine plus de 10 % en fin de période. Aucune trace de « révolte fiscale » sur la protection sociale.
- Note PDF p. 15 : à la question « réduire le déficit » contre « maintenir les prestations » (maladie), 63 % (2020) et 61 % (2019) choisissent le maintien des prestations — cohérent avec la série PS16 recalculée ci-dessus (60,8 % et 59,5 %).
- **Étage** : E1 (expérience à échantillons aléatoires) au sein d'une enquête française E2. C'est la seule mesure directe, trouvée par A10, d'un biais de statu quo et d'un effet de formulation sur des questions budgétaires françaises.

## O-3. Baromètre des prélèvements obligatoires du Conseil des prélèvements obligatoires (CPO), vague 2 (2023)

- **Commanditaire** : CPO (rattaché à la Cour des comptes). **Institut** : Harris Interactive (Toluna). **Terrain** : en ligne, **du 1er au 19 septembre 2023**. **Échantillon** : **2 049 personnes** de 18 ans et plus, quotas et redressement sexe, âge, CSP, région, taille d'agglomération (rapport, p. 3).
- **Provenance** : [C] rapport Toluna Harris « Baromètre des prélèvements obligatoires – Vague 2 – Septembre 2023 », 63 p., hébergé sur tolunacorporate.com (`cpo_toluna_harris_barometre_PO.pdf`, sha256 5f25acbe…). La note du CPO elle-même (ccomptes.fr) est inaccessible depuis l'environnement : [X].
- **Connaissance des ordres de grandeur (illusion fiscale mesurée)** — « Quel est selon vous, en %, le niveau général des prélèvements obligatoires (impôts et cotisations sociales) en France, par rapport à l'ensemble des richesses produites dans le pays en une année ? » : moins de 10 % : 5 ; 10-19 % : 12 ; 20-29 % : 17 ; 30-39 % : 15 ; **40-49 % : 15** ; 50-59 % : 7 ; 60 % ou plus : 5 ; ne sait pas : 24 (p. 8). **49 % sous-estiment (moins de 40 %)**, 15 % répondent dans la tranche que l'institut juge correcte (40-49 %), 12 % surestiment (50 % ou plus). A10 n'a pas vérifié lui-même le taux de prélèvements obligatoires 2023 ; le dossier Astra donne 43,6 % pour 2025 en convention nationale Insee ([S], à contrôler par A01), ce qui est compatible avec la tranche retenue.
- « Pensez-vous que vous payez la Contribution Sociale Généralisée (CSG) ? » : oui 67, non 17, ne sait pas 15 (p. 19) ; 40 % seulement des 18-24 ans et 51 % des revenus faibles pensent la payer. La CSG est prélevée sur la quasi-totalité des revenus d'activité, de remplacement et du capital : une partie des répondants ignore un prélèvement qu'elle acquitte (lecture A10 ; les exonérations de CSG sur certains revenus de remplacement modestes rendent une partie des « non » exacts, ce que l'enquête ne permet pas de séparer).
- Classement des recettes : 41 % placent la TVA en premier (p. 12).
- Acceptation : impôts « trop élevés » 73 % (p. 26) ; cotisations « trop élevées » 74 % (p. 28) ; « payer ses impôts et cotisations sociales est un acte citoyen » 80 % d'accord (p. 30).
- Usage : satisfaits de la manière dont l'argent public est utilisé 34 %, pas satisfaits 65 % (p. 36). Missions de l'État : réduire 45 %, maintenir 38 %, augmenter 17 % (p. 37). « Il est possible d'améliorer la qualité des services publics… à condition d'augmenter les prélèvements » 7 %, « en conservant le niveau » 46 %, « même en baissant » 41 %, impossible 5 % (p. 39).
- **Arbitrage par poste avec information sur le coût** (une question par domaine) : « Pour 1 000 € d'argent public dépensé, les dépenses publiques de [domaine] représentent [x] €. Accepteriez-vous une baisse des dépenses publiques de ce domaine en échange d'une baisse de vos impôts ou de vos cotisations sociales ? » (p. 42). Oui / non : défense (31 €) 45 / 42 ; lutte contre la pauvreté (21 €) 40 / 47 ; éducation (95 €) 34 / 54 ; justice et sécurité (29 €) 32 / 55 ; santé (195 €) 30 / 59 ; **retraites (262 €) 28 / 59**.
- Équité : les 10 % les plus aisés paient « pas assez » pour 63 % ; les 50 % intermédiaires paient « trop » pour 58 % (p. 47). 2 % seulement des répondants se placent dans les 10 % les plus aisés (p. 45).
- **Expérience d'information** : la moitié de l'échantillon (1 028) a vu une courte vidéo sur le rôle de la Cour et des chambres régionales des comptes, l'autre moitié (1 021) non ; moitiés « appariées » sur sexe, âge, CSP, région (le rapport ne dit pas explicitement que l'affectation est aléatoire) (p. 22). Satisfaction sur l'usage de l'argent public : 37 % chez ceux qui ont vu la vidéo, 32 % chez les autres (p. 36) ; effet « faible en général » selon l'institut (p. 22).
- **Vague 3 (2025)** : publiée le 27 novembre 2025 selon vie-publique.fr ([S] résultat de recherche ; page [X] non lue, contenu vide via WebFetch). Les chiffres 2025 circulant (72 % d'insatisfaits de l'usage de l'argent public contre 65 % en 2021 et 68 % en 2023 ; confiance dans l'État 22 % contre 33 % en 2023 ; acceptation d'une baisse des dépenses de retraites 28 %) sont connus par la Fondation iFRAP ([S], page lue par WebFetch) qui présente des incohérences internes (satisfaction 28 % dans un tableau, 10,5 % dans un autre) : **non retenus comme faits**. Institut, dates et échantillon 2025 : non établis.

## O-4. Sondages d'instituts sur des mesures précises (2023 et 2025)

### O-4a. Elabe pour BFMTV, « Les Français et la réforme des retraites », publié le 11 janvier 2023
- Terrain : Internet, **10 janvier 2023**, intégralement après la conférence de presse d'Élisabeth Borne ; **1 002 personnes**, quotas (p. 2). [C] PDF 40 p. (`elabe_20230111_retraites.pdf`, sha256 5b953d0c…).
- « Au global, diriez-vous que vous êtes favorable ou opposé à la réforme des retraites telle qu'annoncée par la Première ministre Elisabeth Borne ? » (après rappel du contenu) : favorable 41, opposé **59** ; actifs opposés 67, retraités favorables 60 (p. 5).
- Mesure par mesure (p. 6) : « L'augmentation de l'âge légal de départ à la retraite à 64 ans (contre 62 ans actuellement), à un rythme de 3 mois supplémentaires par an » : favorable **33**, opposé **67** ; accélération de la durée de cotisation à 43 ans en 2027 : 42 / 58 ; minimum de pension à 1 200 € : 88 / 12 ; suppression des régimes spéciaux pour les nouveaux embauchés : 65 / 35 (ordre des items lu sur la page ; les deux mesures de « travailler plus longtemps » sont les seules rejetées).
- Réforme jugée injuste 58 %, inefficace 51 %, nécessaire 47 % (p. 7). Soutien ou sympathie à la mobilisation : 60 % (p. 9).

### O-4b. Elabe pour Les Échos, « Les Français et le Budget 2026 », 5 juin 2025
- Terrain : Internet, **3-4 juin 2025**, **1 000 personnes**, quotas (p. 2). [C] PDF 19 p. (`elabe_20250605_budget2026.pdf`, sha256 1ca65652…).
- Question exacte (p. 9) : « Habituellement, les versements aux collectivités locales (communes, départements, régions) et aux particuliers (retraites, remboursements santé, allocations familiales, allocations chômage, APL, RSA, etc.) sont systématiquement revalorisés en fonction de l'inflation. Pour faire des économies, certaines personnalités politiques ont évoqué l'idée d'une « année blanche » … c'est-à-dire que les versements faits par l'Etat … en 2026 ne tiendraient pas compte de l'inflation (augmentation des prix) et seraient identiques à ceux de 2025. Pour information, les prévisions d'inflation sont de 1,3% en 2025 et 1,6% en 2026. Etes-vous favorable ou opposé à une « année blanche » … pour les versements de l'Etat aux… ? » : particuliers favorables **45**, opposés **54** ; collectivités 51 / 48.
- **Conditions d'acceptation d'un effort** (p. 10) — « Pour le prochain budget 2026, si un effort vous était demandé, à quelles conditions seriez-vous prêt à l'accepter ? » (trois réponses) : plus de « gaspillage » d'argent public 59 ; lutte contre la fraude fiscale et sociale 49 ; effort mieux réparti selon les moyens de chacun 40 ; suppression ou forte réduction de niches fiscales 35 ; hausse des salaires nets 35 ; amélioration des services publics 21 ; effort temporaire (un ou deux ans) 17 ; « ce n'est pas acceptable, quelles que soient les conditions » **8**.

### O-4c. Toluna Harris Interactive pour RTL, « Réactions des Français après la conférence de presse de François Bayrou sur le budget 2026 de l'État », juillet 2025
- Terrain : en ligne, **15 juillet 2025**, juste après l'allocution ; **1 006 personnes**, quotas et redressement (p. 3). [C] PDF 12 p. (`toluna_202507_reactions_bayrou.pdf`, sha256 44e37879…).
- **Même échantillon, même jour** : « L'objectif de François Bayrou est de ramener le déficit public à 2,8% en 2029. Etes-vous favorable ou opposé(e) à cet objectif ? » : favorable **73**, opposé 27 (p. 7). Puis, mesure par mesure (p. 8) : contribution de solidarité payée par les plus aisés 78 / 22 ; suppression ou fusion d'agences 74 / 26 ; gel des dépenses de l'État 2026 hors défense et intérêts 70 / 30 ; non-remplacement d'un fonctionnaire sur trois 57 / 43 ; « « année blanche », c'est-à-dire le gel des prestations sociales (retraites, aides, …) pour l'année 2026 » **39 / 61** ; suppression de deux jours fériés **30 / 70**. Mesures jugées injustes 68 %, inefficaces 67 % (p. 10-11). Préoccupés par la dette publique 85 % (79 % en mars 2025) (p. 4).
- **C'est la mesure la plus directe trouvée de l'écart entre soutien de principe et rejet des mesures** : 73 % approuvent l'objectif de déficit ; les deux mesures qui touchent directement l'ensemble des ménages (gel des prestations, jours fériés) sont rejetées par 61 % et 70 %. Les mesures approuvées font payer un tiers (les plus aisés, l'administration, les agences).

### O-4d. Elabe pour BFMTV, « Les Français, le budget et la Défense », 16 juillet 2025
- Terrain : Internet, **15-16 juillet 2025**, **1 002 personnes** (p. 2). [C] PDF 40 p. (`elabe_20250716_budget_defense.pdf`, sha256 c77ea7a8…).
- Accord avec « Notre pronostic vital comme Etat est engagé » : **65** % (p. 9). Mesures (p. 10, « y êtes-vous favorable ou opposé ? ») : lutte contre la fraude 90 % favorables ; suppression de niches profitant aux plus aisés et grandes entreprises 87 % ; année blanche pour les prestations, les salaires des fonctionnaires et le barème de l'impôt sur le revenu 45 / 54 ; suppression de l'abattement de 10 % pour les retraités les plus aisés 50 / 49 (actifs favorables 55 %, retraités opposés 61 %) ; suppression de deux jours fériés et doublement du plafond des franchises médicales « massivement rejetés » (28 % et 24 % de favorables pour ces deux items, l'attribution exacte de chaque chiffre à chaque item n'étant pas lisible dans le texte extrait) (p. 4-5, 10).
- « Même s'il faut réduire la dette, les efforts demandés sont trop importants » **60** % contre « … ils sont nécessaires pour réduire la dette » 38 % (p. 11). Projet jugé injuste 68 %.

### Lecture d'ensemble (O-3, O-4)
- Le soutien à l'objectif (73 %) et le diagnostic d'urgence (65 %) coexistent avec le rejet des mesures qui touchent tout le monde (61-70 %) et avec un « trop d'efforts » majoritaire (60 %). L'écart est **mesuré dans le même échantillon** (O-4c), pas supposé.
- Les mesures approuvées font payer des tiers perçus comme extérieurs ou fautifs (fraude, « gaspillage », plus aisés, agences, laboratoires). La condition d'acceptation la plus citée n'est pas l'équité au sens distributif (40 %) mais l'absence de « gaspillage » (59 %) — une croyance sur l'efficacité de la dépense que ces enquêtes ne vérifient pas.
- Limites : panels en ligne par quotas, un seul jour de terrain pour O-4a et O-4c ; formulations différentes d'un institut à l'autre (l'année blanche passe de 39 % à 45 % favorables selon qu'elle vise « les prestations sociales (retraites, aides) » ou un ensemble incluant les salaires des fonctionnaires et le barème de l'impôt) ; aucune de ces enquêtes ne mesure un comportement.
