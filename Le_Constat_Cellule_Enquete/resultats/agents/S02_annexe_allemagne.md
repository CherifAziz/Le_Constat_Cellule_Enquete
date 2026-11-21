# S02 — Annexe Allemagne 2003–2019 (épisode E6 d'A12)

Rédigée le 20/11/2026. Pièces : `donnees\S02\sources\` (manifeste). Calculs : `scripts\S02\s02_test_c.py` (OCDE, copies des fichiers d'A12) et `scripts\S02\s02_soussecteurs.py` (Eurostat, base commune). Verdict d'A12 conservé : **P** (primaire +4,0 pts à cinq ans ; dette en hausse à 5 et 10 ans, t0+10 = 2012 après la crise). La règle elle-même (frein à l'endettement) est instruite dans `S02_annexe_regles.md`.

## 0. Bilan d'instruction

| Point | État | Pièces |
|---|---|---|
| 1. Départ | **pièces** | programme de stabilité de déc. 2003 ; procès-verbal du Conseil du 25/11/2003 ; séries |
| 2. Mesures votées / exécutées | **pièces partielles** : mesures 2003–2004 et 2006–2007 (Conseil 2003, programme 2003, Commission 2006) ; exécution par les comptes (Eurostat, OCDE) ; pas de bilan ex post des mesures | idem + Devries (via A12) |
| 3. Environnement | séries (A12) ; économies d'intérêts (Bundesbank 2017) | |
| 4. Qui a porté l'effort | **séries** par sous-secteur (Eurostat) ; transferts non consolidés | Eurostat gov_10a_main |
| 5. Coûts sociaux | chômage, investissement : séries ; pauvreté : **série Eurostat avec rupture** | Eurostat ilc_li02 |
| 6. Conditions politiques | **pièces** pour 2009 et 2025 (votes) ; 2003–2005 non documenté sur pièce | bpb |
| 7. Inférence | §7 | |

## 1. Point de départ (2002–2003)

- Déficit des APU de 4,1 % du PIB en 2002 (Eurostat, base commune), 4 % en 2003 selon le programme de stabilité de décembre 2003 (« the deficit of -4 % of GDP registered in 2003 », p. 18 de la pièce, [C]) ; solde primaire −1,5 % (OCDE, A12) ; dette 59,8 % (AMECO, A12) ; chômage 8,6 %.
- **Le gouvernement fédéral choisit en décembre 2003 de ne pas revenir sous 3 % en 2004** : « Reduction to or even below the reference figure of -3 % is not a realistic proposition » ; il avance au contraire à 2004 l'étape 2005 de la réforme de l'impôt sur le revenu, qui coûte ½ point de PIB en 2004 (programme de stabilité, déc. 2003, pp. 5, 18 [C]).
- **Procédure européenne suspendue** : le 25/11/2003, le Conseil Ecofin rejette les recommandations de la Commission au titre des art. 104(8) et 104(9) (majorité non atteinte), adopte des conclusions qui reportent la correction à 2005 et « agrees to hold the Excessive Deficit Procedure for Germany in abeyance for the time being » (procès-verbal ST 15272/03 EXT 3, pp. 5–8 [C]). Le Conseil note des mesures de 2003 évaluées par la Commission à **1 % du PIB** et demande −0,6 pt de solde corrigé du cycle en 2004 et au moins −0,5 en 2005 (même pièce). La BCE juge que ces conclusions « carry serious dangers » (communiqué du 25/11/2003 [C]). L'arrêt de la Cour de justice du 13/07/2004 (C-27/04) n'a pas pu être lu : EUR-Lex (réponse 202 vide), Curia (redirection), BAILII (filtre anti-robots) [X].
- Part ponctuelle du déficit de départ : non documentée par pièce.

## 2. Mesures votées et exécutées

**Votées (pièces lues)** : 2003, ≈ 1 % du PIB (Commission, citée par le Conseil) ; 2004 : loi d'accompagnement budgétaire (plafonnement de l'indemnité kilométrique, suppression de la prime à l'accession à la propriété pour les nouveaux bénéficiaires, réduction de primes spéciales de la fonction publique), en même temps que l'avancement de baisses d'impôt (programme 2003, p. 18 [C]) ; 2006–2007 : hausse du taux normal de TVA de 16 à 19 % et de la taxe sur les assurances (« up to 1% of GDP »), baisse du taux de cotisation chômage de 6,5 à 4,5 % (≈ 0,6 % du PIB), cotisation retraite de 19,5 à 19,9 %, réforme des retraites de 2005, masse salariale publique contenue (Commission, évaluation technique du programme de stabilité, 9/06/2006, encadré 2, p. 19 [C]). Devries et al. (via A12) : 2,5 pts sur 2003–2007, 79 % en dépenses.

**Exécutées (comptes, Eurostat 2026, % du PIB, 2002 → 2007 ; `S02_soussecteurs_DE_BE_IT.csv`, C-S02-020)** : solde +4,3 (−4,1 → +0,2) ; recettes **−0,5** ; dépenses **−4,7**, dont prestations sociales en espèces −2,1, rémunérations −0,9, intérêts −0,3, investissement (FBCF) −0,4. Test C (OCDE, 2002 → 2007) : solde primaire +3,9 pts, **111 % par la baisse du ratio de dépenses primaires** (recettes −0,45) ; dépenses primaires **+3,2 % en valeur en cinq ans** pour un PIB nominal de +14,3 % ; l'OCDE attribue +1,2 pt au cycle (niveau D). Comme au Canada, il s'agit d'un **gel en valeur**, pas d'une baisse nominale ; mais la croissance nominale allemande n'est que de 2,7 % par an : **c'est le cas de gel transposable** à une économie à croissance nominale faible (calcul C-S02-050 : le même gel avec 2¼ % de croissance nominale par an aurait réduit le ratio de 3,5 pts au lieu de 4,4).

**Écart voté / exécuté** : la hausse de TVA (≈ 1 pt de PIB) n'apparaît pas dans le ratio de recettes (−0,5 pt sur 2002–2007), parce qu'elle est compensée par des baisses de cotisations (−1,8 pt de recettes de la sécurité sociale) et d'impôt sur le revenu (réforme avancée en 2004). Le redressement exécuté est donc **entièrement en dépenses** dans les ratios, alors que les mesures votées de 2006–2007 étaient surtout fiscales : la « composition » change selon l'objet mesuré (constat d'A12, §15.3, confirmé ici).

## 3. Environnement

Grille d'A12 : croissance réelle moyenne 1,65 % (2003–2007) ; marchés d'exportation +8,0 % par an ; compte courant 1,8 → 6,6 % du PIB ; taux long 4,8 → 4,2 %. **Après 2008**, la Bundesbank chiffre l'allègement des intérêts dû à la baisse des taux par rapport au niveau de 2007 à **47 Md€ (1½ % du PIB) en 2016** et à **240 Md€ cumulés depuis 2008 (7½ % du PIB)** pour l'ensemble des administrations ; pour le seul Bund, 30 Md€ en 2016 et 155 Md€ cumulés (Bundesbank, *Monatsbericht*, juillet 2017, article sur les dépenses d'intérêts, pp. 6 et 9 de la pièce [C]). Les excédents de 2014–2019 (+0,7 à +1,9 % du PIB, Eurostat, base commune : 0,7 ; 0,9 ; 1,1 ; 1,3 ; 1,9 ; 1,3) sont donc contemporains d'une économie d'intérêts annuelle du même ordre.

## 4. Qui a porté l'effort (2002 → 2007, Eurostat, non consolidé, C-S02-020)

| Sous-secteur | Δ solde | Δ recettes | Δ dépenses | dont |
|---|---|---|---|---|
| Bund (S1311) | +1,1 | +0,3 | −0,8 | intérêts −0,3 |
| Länder (S1312) | **+1,7** | +0,3 | −1,3 | rémunérations −0,6 |
| Communes (S1313) | +0,7 | +0,6 | −0,2 | FBCF −0,2 |
| Sécurité sociale (S1314) | +0,7 | −1,8 | −2,6 | **prestations en espèces −2,2** |
| **APU** | **+4,3** | −0,5 | −4,7 | |

Lecture : les Länder portent la plus forte amélioration ; la sécurité sociale baisse ses prestations en espèces de 2,2 pts de PIB (période des lois Hartz et de la réforme des retraites ; attribution poste par poste **non établie** par une pièce) tout en perdant 1,8 pt de recettes (baisses de cotisations). L'investissement des communes, premier investisseur public, recule.

## 5. Résultats et coûts sociaux

- Chômage 8,6 % (2002) → 11,0 % (2005) → 8,6 % (2007) (A12). Investissement public 2,6 → 2,2 % du PIB (2002 → 2007, Eurostat).
- **Pauvreté monétaire** (Eurostat ilc_li02, seuil 60 % du revenu médian, [C] API, `S02_pauvrete_ilc_li02.csv`) : 10–11 % en 1998–2001 (panel ECHP), **12,2 % en 2005 (rupture de série, EU-SILC) → 15,2 % en 2007** (dans EU-SILC, l'enquête de l'année N mesure les revenus de N−1 : ces chiffres portent sur les revenus de 2004 à 2006), 16,1 % en 2012–2013, 14,8 % en 2019. La hausse 2005–2007 coïncide avec la consolidation et les réformes du marché du travail ; **aucune pièce lue n'établit le lien causal**, et les premières années d'EU-SILC en Allemagne sont un point de rupture signalé par Eurostat (statut « b » en 2005).
- Investissement et infrastructures après 2009 : voir `S02_annexe_regles.md` (frein à l'endettement), notamment le retard d'investissement communal déclaré de 160 Md€ (KfW, cité par la contribution du DIW au *Wirtschaftsdienst* 2019).

## 6. Conditions politiques

- 2003–2005 : gouvernement SPD-Verts ; conflit ouvert avec la Commission (pièces ci-dessus). 2005–2009 : grande coalition (hausse de TVA de 2007) — **la composition de la coalition n'est pas documentée par une pièce lue** (souvenir [M]).
- **Frein à l'endettement** : révision constitutionnelle votée par le Bundestag le 29/05/2009 par 418 voix pour, 109 contre, 48 abstentions (majorité des deux tiers), approuvée par le Bundesrat le 12/06/2009, en vigueur le 1/08/2009 (Agence fédérale pour l'éducation civique, bpb, « Vor zehn Jahren: Einführung der Schuldenbremse », 2019 [C]).
- **Réforme de 2025** : votée le 18/03/2025 par le Bundestag sortant (512 pour, 206 contre ; 489 requis), parce que la nouvelle assemblée élue le 23/02/2025 n'offrait plus de majorité des deux tiers ; Bundesrat le 21/03/2025 (bpb, 2025 [C]).

## 7. Inférence pour un pays de la zone euro à dette élevée et croissance faible

- **Permet** : (i) une consolidation de 4 points en cinq ans **dans la zone euro, sans dévaluation**, est possible par un gel en valeur des dépenses primaires (+3,2 % en cinq ans), avec un effort réparti entre Länder, communes et sécurité sociale ; (ii) le non-respect assumé d'une règle (2003) n'a pas empêché la correction ultérieure.
- **Ne permet pas** : (i) de séparer l'effet des mesures de celui de la demande extérieure (compte courant +4,8 pts) — canal non disponible pour tous les pays à la fois ; (ii) d'attribuer les excédents de 2014–2019 à la seule discipline : 1½ pt de PIB d'intérêts économisés en 2016 (Bundesbank) ; (iii) de transposer : la dette de départ (60 %) est deux fois plus basse que celle de la France de 2025.
- **Contradiction avec A12 ?** Non pour le verdict P. **Précision** : la composition des mesures (79 % dépenses, Devries) et la composition observée (≈ 100 % dépenses dans les ratios) concordent en direction, mais les mesures fiscales de 2007 ont servi à financer des baisses de cotisations plutôt qu'à réduire le déficit.
