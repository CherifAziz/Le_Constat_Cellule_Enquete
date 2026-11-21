# A18 — Annexe : vérification indépendante (partie 2) et arbitrage des contradicteurs (partie 3)

Agent A18, session du 20 novembre 2026 (soir). Vérificateur et arbitre ; je n'appartiens à aucun camp. La partie 1 (audit de la V5) est dans `A18_annexe_audit_factuel_V5.md` et n'est pas modifiée ici.

**Ordre d'exécution** : partie 3 d'abord (elle conditionne la suite), partie 2 ensuite. Chaque section dit ce qui est fait et ce qui ne l'est pas.

**Périmètre** :
- Les versions de l'équipe Codex (A16, A17, A18 et les audits CX) prévues par l'ordre de mission ne sont **pas** dans mon périmètre aujourd'hui. Le dossier `C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\resultats\` (niveau supérieur) n'a été ni lu ni écrit. L'arbitrage ci-dessous porte donc sur les seules contre-expertises de la cellule Claude. La comparaison avec l'équipe Codex reste à faire.
- Je n'ai pas lu S06, qui est en cours d'écriture.

**Canaux de contrôle**, du plus fort au plus faible :
1. *retéléchargé à l'origine* : pièce téléchargée par moi à son adresse d'origine, empreinte comparée à la copie de l'agent ;
2. *rejoué sur copie* : script de l'agent copié sous `donnees\A18\`, puis relancé ;
3. *recalculé* : calcul fait par mon propre script sur la base commune ou sur une pièce retéléchargée ;
4. *relu dans la copie* : texte ou fichier de l'agent relu, sans retour à l'origine ;
5. *relu dans la sortie* : sortie de script relue, sans relance.

Manifeste des pièces de cette session : `donnees\A18\MANIFESTE_PIECES_P2.csv`. Le manifeste de la partie 1 n'est pas modifié.

---

# PARTIE 3 — Arbitrage des deux contre-expertises

## 3.0 Méthode

Pour chacune des 15 attaques ou objections (8 d'A16, 7 d'A17), voici ce que j'ai fait :
- j'ai ouvert le dossier visé à la ligne citée (numéros de ligne indiqués dans `A18_arbitrage.csv`) ;
- j'ai relu la pièce, ou je l'ai retéléchargée quand elle était décisive et joignable : Cour des comptes de juillet 2024, OFCE n° 149, AMECO ;
- j'ai rejoué sur copie le seul script dont dépend un verdict majeur (`a16_scenarios.py`).

Verdicts possibles :
- **fondée** : la cellule doit modifier ;
- **fondée en partie** : une reformulation suffit ;
- **non fondée** ;
- **indécidable** : la pièce manquante est alors nommée.

Les objections d'A17 ne sont pas encore inscrites dans `contradictions.md` : la section H s'arrête à K-110. Je les désigne par O1 à O7. **Je signale cet oubli à l'orchestrateur.**

Lecture des pré-enregistrements :
- **Les deux contradicteurs ont vu tomber plusieurs de leurs propres prédictions**, ce qui plaide pour leur bonne foi méthodologique :
  - A16 : PR3, PR6, PR7 ;
  - A17 : H-A17-005, H-A17-006, P3, P6.
- **Deux thèses d'A16 (T6, T7) ont été écrites en connaissant la cible**, il le dit lui-même. Je ne leur donne pas de valeur prédictive.
- Les prédictions chiffrées d'A17 reposent sur des souvenirs [M], ce qu'il déclare. Je ne leur donne aucune valeur de preuve.

## 3.1 Tableau des verdicts

| Id | Cible | Verdict | Modification demandée (résumé ; texte complet dans le CSV) |
|---|---|---|---|
| ATT-1 / K-103 | A15 R-A15-01 | **fondée en partie** | préciser « mesures chiffrées par A13 et A14 » ; donner le rythme de dépense équivalent avec sa plage de dates (2035, 2036 ou 2040 selon le multiplicateur) |
| ATT-2 / K-104 | A13 obj. 1 ; vague2 §7 | **fondée en partie** | « vieillesse et santé portent environ deux tiers de l'écart » ; écrire « non testé », pas « écarté » |
| ATT-3 / K-105 | PLAN_V2 §3.3 ; A12 R4 | **fondée** (déjà reçue) | maintenir « non départagée » ; ne tirer de A12 R4 aucune conclusion sur « la dépense d'abord » |
| ATT-4 / K-106 | A13 §5 ; A15 | **fondée en partie** | marquer l'ordre des multiplicateurs comme hypothèse ; citer OFCE 149 et AFG côte à côte ; publier la variante inversée |
| ATT-5 / K-107 | A11 R-A11-01 | **fondée en partie** | retirer la conséquence « ne peut pas expliquer le déficit » ; donner le coût brut à part, avec périmètre et année corrigés (6,8 à 10,4 %) |
| ATT-6 / K-108 | A09 R-A09-01 | **fondée en partie** | restreindre la conséquence au veto parlementaire ; inscrire « bien commun budgétaire : non testé » |
| ATT-7 / K-109 | A04 ; T-04 | **fondée en partie** (mineure) | « chiffrage ex ante, méthode non publiée » ; citer la phrase de la Cour sur 2022 **avec** son interprétation (« masquait ») |
| ATT-8 / K-110 | A06, A14, A15 | **fondée en partie** | emploi « non instruit », pas « écarté » ; T-06 reste ouverte |
| O1 | A15 R-A15-01 | **fondée en partie** | afficher 137 à 140 %, et jusqu'à 148 % (borne sans pièce) |
| O2 | A01 R3 | **fondée en partie** | « estimations officielles lues » au lieu de « toutes les estimations lues » ; alternative OFCE ≈ 84 % ; « structurel » ne veut pas dire « décidé » |
| O3 / K-008 | A14 R-A14-08 | **fondée en partie** | K-008 « instruite : jugement » ; retirer « quasi-nécessité » |
| O4 | A15 R-A15-08 ; « refus de l'effort » | **fondée** | composition des bornes par période ; dire que l'incidence des baisses de 2018–2023 n'est pas établie. Recherche A18 sans plafond dans A03, A04, A10 et A15 : seule indication, qualitative et pour une seule mesure, A04 F-A04-036 (Cour, janvier 2025 : suppression de la taxe d'habitation, « effets anti-redistributifs ») ; A15 l. 390 : « Ventilation par décile […] non faite » |
| O5 | A15 R-A15-04 | **fondée en partie** | fourchette : déficit 2030 de 6,5 à 7,2 % |
| O6 | lecture « cliquet » 2012–2019 | **fondée en partie** | contexte : consolidation par les recettes en croissance faible ; coût d'activité non mesuré |
| O7 | A01 R7 | **non fondée** | aucune (déjà traité par A01 et dominé par A15) |

**Décompte des 15 attaques** :
- fondées : 2 (ATT-3, O4) ;
- fondées en partie : 12 ;
- non fondée : 1 (O7) ;
- indécidables : 0 en tant qu'attaques.

Plusieurs **questions de fond** soulevées restent cependant indécidables sur les pièces accessibles (§3.4). « Fondée en partie » signifie presque toujours que le **calcul** de la cellule tient, mais que sa **portée** est énoncée plus largement que la pièce ne le permet.

**Aucune attaque n'infirme un chiffre de la cellule.**

## 3.2 Points d'arbitrage détaillés (ceux qui pèsent sur un verdict)

### ATT-1 / K-103 — « aucune combinaison n'atteint 3 % »

- **Rejeu.** J'ai rejoué `a16_scenarios.py` sur copie (`donnees\A18\rejeu_A16\`). La sortie est identique à l'octet : SHA-256 `236ACBCF…570C` des deux côtés, et le module `a15_modele_copie.py` est identique à celui d'A15 (`B567AEB9…2064`). Ce rejeu prouve la **reproductibilité**, pas la **validité**.
- **Validité dans le modèle.** Avec la trajectoire européenne en 2027–2029 puis une dépense stable en volume :

  | Multiplicateur | Déficit 2035 | Passage sous 3 % |
  |---|---|---|
  | 0,6 | 2,7 % | 2035 |
  | 0,8 (central d'A13 pour salaires et transferts, le plus pertinent pour une norme tenue en dépense) | 3,1 % | 2036 |
  | 0,6 avec effet persistant | 4,1 % | 2040 |

  « 3 % en 2035 » est donc un résultat **sur le fil**. Le vieillissement absorbé dans la norme ne pèse qu'environ 0,2 point en 2035 et ne décide de rien.
- **Écart avec la pièce.** L'avis HCFP 2025-3 (p. 20, relu dans la copie d'A08, non retéléchargé) dit que le Conseil a fixé la même trajectoire « in order to bringing French deficit below 3% by 2029 ». Le modèle ne passe sous 3 % qu'en 2035. Je n'ai **pas** décomposé cet écart. Trois explications sont plausibles, aucune n'est chiffrée :
  - une référence 2027 dégradée (6,5 % avant mesures) ;
  - des intérêts plus élevés ;
  - le rattrapage cumulé depuis 2023 exigé par le Conseil (p. 21 : « The requirements also cover the cumulative evolution of NEG since 2023 »), qu'A16 ne modélise pas. Ce dernier point rend sa version **moins** exigeante que l'engagement réel.
- **Portée.** A15 §14 écrit déjà que la seule voie vers 3 % passe par des mesures non documentées, dont une « dépense de plusieurs points ». Le litige porte sur le sens du mot « documentée », non sur le calcul. A15 et A16 sont vrais chacun dans sa définition (K-103 : **dépend d'une convention**). L'effort de la norme (5,9 points de PIB en 2035 contre la référence) est du même ordre que l'effort à voter d'A15 (5,4 points). **La norme ne réduit pas l'effort, elle le nomme autrement.**
- **Non vérifié ici** : l'affirmation C-A16-004 (« aucune période française de trois ans à volume nul hors artefacts depuis 1995 »). Voir partie 2, V22.

### ATT-4 contre O1 — multiplicateurs : opposition directe entre les contradicteurs

- **A16** : l'ordre retenu par A13 (transferts 0,8, prélèvements 0,5) est une hypothèse sans pièce, contraire à AFG. **Confirmé** pour le statut « H » (A13, l. 120). AFG n'a été lu qu'en résumé par toute la cellule.
- **A17** : les multiplicateurs forts sont soutenus par les pièces. Je l'ai vérifié sur l'OFCE n° 149, p. 5, retéléchargé à l'origine et identique à la copie d'A17. La pièce dit que les hausses d'impôts ciblées ont un multiplicateur d'« un peu moins de 0,5 à un an », et que les économies structurelles en dépense ont un multiplicateur « relativement élevé ».
- **Arbitrage** :
  - **à un an**, la seule pièce française lue va dans le sens de l'ordre d'A13, et contre A16 ;
  - **au-delà d'un an**, aucune pièce lue ne tranche : AFG porte sur des moyennes d'épisodes, et la persistance n'est mesurée nulle part.
  - → **Désaccord non tranché au-delà d'un an.**
  - Ce qui le trancherait : des multiplicateurs français par instrument à 3–5 ans (variantes Mésange du Trésor, OFCE), et une évaluation ex post de 2011–2014.
  - Dans les deux sens, **le verdict sur K1 et K5 ne change pas** (A16 C-A16-002 ; A17 C-A17-003).

### ATT-5 — capture

- L'arithmétique d'A16 est exacte (14,3 à 15,8 Md€ / 151,6 = 9,4 à 10,4 %). Elle surcompte pourtant sur trois points :
  - A11 (l. 122) limite l'évaluation défavorable du CIR **aux grandes entreprises**, qui reçoivent environ la moitié de la créance ;
  - les années sont mêlées : CIR 2026, Dutreil 2024 et TVA 2026, rapportés au déficit de 2025 ;
  - « influence déclarée » n'est pas « capture établie ».
- Avec la moitié du CIR, on obtient **10,3 à 12,0 Md€, soit 6,8 à 7,9 % du déficit**.
- Ce chiffre reste d'un autre ordre que les rendements de réforme (0,1 à 1 %). La conséquence de R-A11-01 (« ne peut pas être présentée comme une explication du déficit ») **excède** la mesure qui la fonde.

### ATT-7 — 62 Md€

Pièce retéléchargée à l'origine (Cour des comptes, juillet 2024, via vie-publique.fr ; identique à la copie d'A16) :
- p. 35 : « dont l'impact est estimé à 62 Md€ en 2023, soit 2,2 pts de PIB » ;
- même page : « Ce dynamisme spontané des recettes masquait encore, fin 2022, l'effet des baisses » ;
- en 2023, le taux de prélèvements baisse de 1,8 point, dont 1,6 point d'évolution spontanée ;
- p. 36 : « non compensées par des économies en dépenses ».

La Cour lit donc l'élasticité comme un **masque** de l'effet des baisses, non comme sa réduction. Le paragraphe ne permet pas de qualifier les 62 Md€ de « borne haute ». Seule l'étiquette « chiffrage ex ante, méthode non publiée » est fondée, et A04 l'avait déjà en substance.

### O2 — part structurelle de 2025

- L'OFCE n° 149, p. 4 (retéléchargé) donne bien « output-gap (estimé à -1,0 point de PIB en 2024) ».
- Le prolongement à −1,4 en 2025 est un calcul d'A17, non un chiffre de l'OFCE. Son arithmétique est exacte : 0,57 × 1,4 = 0,80 ; (5,07 − 0,80) / 5,07 = 84 %.
- A01 (l. 246) tire sa plage −4,7 à −5,2 des seules estimations officielles. « Toutes les estimations lues » est vrai pour A01, mais devient trompeur dès qu'une estimation indépendante existe.
- La conclusion « surtout structurel » tient : plus des quatre cinquièmes dans tous les cas.

## 3.3 Tensions et corrections arbitrées

**T-07 — un assouplissement suit-il chaque consolidation ? (A03 contre A09).** Verdict : **dépend d'une convention**, et d'une erreur de série chez A03.
- **Pièce.** J'ai retéléchargé l'AMECO fiscal à l'origine (`ameco17.zip`, ec.europa.eu, identique à la copie d'A09, SHA-256 `A61FDC11…B3B0`). Série retenue : solde primaire corrigé du cycle, sur le PIB potentiel (`UBLGBP`). Script : `scripts\A18\a18_p3_ameco_t07.py` ; sortie : `donnees\A18\a18_p3_t07_sortie.txt`.
- **2004–2006 n'est pas une consolidation au sens du solde corrigé du cycle** : −1,27 (2003) ; −1,39 ; −1,39 ; −1,18 (2006), soit +0,10 point.
  - Les variations citées par A03 (+0,5 ; environ 0 ; +0,85) ne sortent d'**aucune** des quatre séries corrigées du cycle de l'AMECO (libellés relus dans la colonne TITLE). Variations 2004 / 2005 / 2006 :

    | Série | 2004 | 2005 | 2006 |
    |---|---|---|---|
    | UBLGBP | −0,12 | −0,01 | +0,22 |
    | UBLGB (PIB tendanciel) | −0,14 | −0,13 | +0,03 |
    | UBLGAP | −0,04 | +0,08 | +0,33 |
    | UBLGA | −0,07 | −0,05 | +0,14 |

  - La série la plus proche est le solde primaire **observé**. Sur l'Insee, mon calcul donne +0,46 ; −0,04 ; +0,74, ce que confirme la sortie `tests_A03_sortie.txt` d'A03 (déficit primaire de 1,21 ; 0,75 ; 0,79 ; 0,05 % du PIB). Le +0,85 de 2006 reste **non identifié exactement**.
  - A03 mesure vraisemblablement l'épisode en solde observé, puis l'assouplissement de 2007 (−0,69) en solde corrigé du cycle. Cette **juxtaposition probable de deux séries** suffit à retirer 2004–2006 des consolidations corrigées du cycle.
  - Le millésime de l'AMECO retéléchargé est daté du 16/11/2026 (date interne du fichier zip), soit la veille de la prévision d'automne de la Commission. Cela compte pour V24, et pour 2017 : −0,49 ici, −0,51 chez A03 avec un autre millésime.
- **Grandes consolidations corrigées du cycle** :
  - 1993–1999 (+2,9) : suivie de 2000 (−1,10) ;
  - 2010–2016 (+2,3) : suivie de 2017 (−0,49, juste sous le seuil de 0,5) puis de 2019 (−0,97) ;
  - 1994–1997 (+1,9) : suivie de 1998 (+0,35, pas d'assouplissement immédiat).
  - Avant 2000, ces soldes sont de niveau D (règle 9).
- **A09 reproduit** :
  - avec le cumul fixe de trois ans, 0 cas sur les 12 calculables (1981, que A09 compte, n'est pas calculable dans mon extraction) ;
  - avec le meilleur gain sur une à trois ans, 3 cas sur 13 ; sur cinq ans, 4 cas sur 13, comme A09.
- **Les deux agents ne posent pas la même question** : A03 cherche s'il y a un assouplissement sachant qu'il y a eu consolidation (n = 2 ou 3) ; A09 cherche s'il y a eu consolidation sachant qu'il y a assouplissement (n = 13). Les deux résultats peuvent être vrais ensemble.
- **Modification demandée** : A03 R7 doit retirer 2004–2006, ou dire qu'il parle de solde observé, et se limiter à deux épisodes corrigés du cycle. Rien ne change pour A09.

**T-06 — emploi et solde.** **Indécidable sur les pièces accessibles.**
- L'écart statique de 0,8 à 2,7 points (A06) est un écart de long terme, pas le rendement d'une mesure.
- Pièces manquantes : évaluations ex post de l'assurance chômage 2019–2023 et des reculs d'âge (Dares, Unédic, COR) ; chiffrage Trésor par mesure.

**K-103 (A15 contre A16).** Voir ATT-1. **Dépend d'une convention** (mesures chiffrées contre norme d'ensemble). Ce n'est pas une contradiction de chiffres.

**Correction d'A17 sur le taux de 2,8 %.** **Fondée.**
- La sortie d'A15 elle-même (l. 76) donne une dette de 126 / 132 / 135 % en 2030 / 2035 / 2040 pour K5 : elle monte déjà entre 2035 et 2040.
- La sortie d'A17 donne 144 % en 2050 ; avec un déflateur de 2 %, 130 / 132 / 138.
- Aucune définition de la stabilisation n'est satisfaite.
- Canal : relu dans les deux sorties, non rejoué. La recette d'A15 a déjà été corrigée (19 h 11) ; la phrase de A15 §14 reste à supprimer dans le dossier.

## 3.4 Convergences et désaccords entre A16 et A17

**Convergences sans lecture mutuelle** (résultats plus robustes) :
1. Aucune combinaison **des mesures chiffrées** n'atteint 3 % avant 2035 : A16 le teste avec des multiplicateurs nuls ou négatifs, A17 avec des taux bas.
2. L'effort d'ensemble est d'environ 5 points de PIB : A16 en norme de dépense (5,1 à 5,9 points en 2035), A17 et A15 en stabilisation (5,2 points).
3. **La persistance de l'effet des consolidations sur l'activité est le paramètre décisif**, et personne ne l'a mesurée pour la France : A16 (ATT-1, objection 2 : « le résultat dépend de la persistance plus que du niveau ») ; A17 (O1 et §15). C'est la convergence la plus utile pour la suite de l'enquête.
4. 37 budgets de majorité absolue sur 37 en déficit ; aucun excédent primaire depuis 2002 ; aides de crise retirées.
5. « La dépense d'abord » n'est pas une nécessité démontrée pour la première tranche (A16 6 ter ; A17 O3).
6. Le budget 2025 a amélioré le solde primaire corrigé du cycle par les prélèvements, sans récession observée : chacun le cite comme contre-exemple à sa propre thèse.
7. Les deux désignent les **programmes de 2010 sur pièces** et le **résidu de dette d'avant 1999** comme lacunes qui comptent.
8. Aucun des deux ne défend un cliquet de dépense pur : A16 (1993) et A17 (2012–2019, consolidation par les recettes) le contestent par des voies différentes.

**Désaccords non tranchés** :

| Objet | A16 | A17 | Ce qui trancherait |
|---|---|---|---|
| Ordre et persistance des multiplicateurs au-delà d'un an | dépense plus faible (AFG, résumé) | dépense élevée (OFCE à un an, HCFP « proche de 1 ») | multiplicateurs français par instrument à 3–5 ans ; ex post 2011–2014 |
| Lecture de A12 R4 (la composition ne sépare pas réussites et échecs) | la croissance peut être un médiateur : indéterminé | résultat qui « résiste » | composition exécutée sur 15 épisodes ou plus avec la croissance ultérieure ; AFG et GLP en entier |
| Ce que mesure le « structurel » | non discuté | contient une perte de niveau non qualifiée | écarts de production multi-méthodes et multi-millésimes |

---

# PARTIE 2 — Vérification indépendante d'affirmations chiffrées centrales

## 2.0 Méthode

**Fichiers** :
- détail ligne à ligne : `donnees\A18\A18_verification_25.csv` (28 lignes, V01 à V28) ;
- scripts : `scripts\A18\a18_p2_inventaire.py`, `a18_p2_explore.py`, `a18_p2_telecharge.py`, `a18_p2_verif.py`, `a18_p2_cherche_pdf.py` ;
- sortie : `donnees\A18\a18_p2_verif_sortie.txt`.

**Méthode** :
- Aucun script d'agent n'a été réutilisé.
- Les calculs partent de la base commune : Insee base 2020, dont la table t_3201 en Md€ depuis 1959, et Eurostat. Ils partent aussi de pièces que j'ai retéléchargées à l'origine : COFOG en montants, PIB nama, AMECO, Cour 2024, OFCE n° 149.
- Les fichiers d'agents ne sont lus que lorsque c'est indiqué (« relu dans la copie »).

**Contrôles de construction** :
- le ratio de dette recalculé (dette en Md€ / PIB) égale le ratio publié en 1978, 1996 et 2025 (21,6 ; 60,6 ; 115,7) ;
- le solde 2025 de la table t_3201 (−151,6) égale celui de la Figure 1 (−151,592).

**Sélection** : priorité aux chiffres que l'orchestrateur n'avait pas recalculés. La colonne `deja_recalcule_par_orchestrateur_ou_autre` le dit ligne par ligne. Treize lignes n'avaient été recalculées par personne : V02, V07, V08, V09, V12, V14, V20, V22, V23, V24, V25, V26, V28.

## 2.1 Bilan

| Verdict | Nombre | Lignes |
|---|---|---|
| confirmé | 14 | V01, V02, V03, V06, V10, V11, V12, V13, V14, V15, V18, V21, V23, V27 |
| confirmé à l'arrondi | 4 | V04, V07, V09, V22 |
| recalculé en partie, relu dans la copie pour l'autre partie | 2 | V16 (soldes recalculés ; classement des majorités relu dans la copie d'A09), V17 (soldes exécutés recalculés, identiques par construction puisque même base ; soldes programmés relus dans la copie d'A08) |
| dépend d'une convention (laquelle : voir CSV) | 6 | V05 (moyenne avec ou sans la France), V08 (idem), V19 (taux de PO Insee ou agrégat Eurostat), V20 (année de base), V24 (PIB potentiel), V28 (périmètre des pays) |
| relu dans la copie (non vérifié à l'origine) | 2 | V25 (COR, copie d'A06, sans URL d'origine), V26 (enveloppes A13/A14, niveau D) |
| infirmé | 0 | — |
| non vérifiable | 0 parmi les 28 ; voir §2.3 pour ce qui n'a pas été tenté |

**Aucun chiffre central de la cellule n'est infirmé.** Les réserves portent sur des conventions qu'une synthèse doit nommer.

## 2.2 Constats utiles à la cellule

1. **V28 — « Seul pays étudié dont le ratio de dette monte en 2015–2019 »** (A07, vague1 §3.8). Dans la base commune (14 territoires), la Grèce monte aussi (179,6 → 183,2). L'énoncé n'est vrai que si l'on exclut la Grèce : nommer le périmètre.
2. **V20 — « +1,5 point de solde primaire contre −0,7 d'intérêts de 2015 à 2019 »**. C'est vrai avec 2014 pour base (cinq variations annuelles). Avec 2015 pour base, on obtient +1,0 et −0,5. La conclusion qualitative tient dans les deux cas.
3. **V13 — 1979–1990** : la hausse de 15 points ne vient pas de l'écart taux–croissance, qui est négatif (−2,7), mais du résidu inexpliqué (16,8). Cela confirme la consigne de la vague 1 : « ne pas le citer comme un fait ».
4. **V16** :
   - le classement 37 sur 37 est retrouvé exactement : parti seul 23 + coalition 14, et 43 sur 43 avec les deux variantes d'A09 ;
   - les neuf excédents primaires sont exactement les années citées ;
   - sous une coalition majoritaire absolue, on compte six excédents primaires (1979, 1980, 1998–2001). « Aucun excédent primaire sous la majorité absolue » n'est vrai que pour **un seul parti**, et c'est ce que dit A09.
5. **V22** confirme le fait sur lequel repose ATT-1. Depuis 1996, aucune période de trois ans à dépense primaire nulle ou négative en volume, même sans neutraliser le retrait des mesures d'urgence (2022 : −0,08 ; 2023 : −1,30 ; 2024 : +1,63).
6. **V19** : le « proche de 2017 » de la Cour vaut pour le taux de prélèvements obligatoires au sens Insee (−0,3 point entre 2017 et 2022). L'agrégat Eurostat élargi baisse de 0,8 point sur la même période. Les deux sont exacts dans leur définition.
7. **V24** : l'AMECO retéléchargé donne un solde structurel 2025 de −4,69 % du PIB potentiel, soit 92,5 % du déficit. Cela confirme la borne basse d'A01 pour l'estimation de la Commission. L'objection O2 porte sur ce qui reste hors de ces estimations.
8. **V25** : A06 n'a pas de `MANIFESTE_PIECES.csv`. L'URL d'origine du rapport du COR n'est consignée nulle part : la pièce ne peut pas être retéléchargée par un contrôleur. **Signalé à l'orchestrateur.**

## 2.3 Ce qui n'a pas été vérifié dans cette partie (dit en toutes lettres)

- **Canada, 76 à 90 % de l'amélioration par les dépenses (S02)** : non vérifié par A18. L'orchestrateur l'a recalculé sur le tableau de S02 ; aucune pièce canadienne n'a été retéléchargée par moi.
- **Référence d'A15 (6,5 % en 2027, RESF) et combinaisons K1–K5** : non vérifiées indépendamment. J'ai seulement rejoué sur copie le module d'A15 via `a16_scenarios.py`, avec une sortie identique. C'est de la reproductibilité, pas une vérification à la source.
- **Taux à 10 ans d'octobre 2026, charge de la dette de 72,4 Md€** : déjà vérifiés en partie 1 et par l'orchestrateur ; non refaits.
- **Prestations Drees de 1974–1985 (+7,8 points, S03)** : périmètre Drees non vérifié. Seul le périmètre des comptes des administrations publiques l'a été (V23).
- **Contrôle par sondage des étiquettes de provenance** (au moins trois citations par dossier, point 7 de l'ordre de mission) : **non fait** dans cette session, sauf pour les pièces relues ci-dessus (Cour 2024, OFCE 149, HCFP 2025-3, COR 2026, AMECO).
- **Baisses de prélèvements d'A04** (−2,29 points sur 2018–2023 ; −1,40 net fin 2025) et **bornes T-04 d'A15** (0,7 à 1,4 point depuis 2017 ; « rien depuis 2006 ») : **non recalculées**. Il faudrait les chiffrages de mesures nouvelles de l'Insee et la source secondaire d'avant 2018. Seule la citation de la Cour (62 Md€, 2,2 points) et le taux de prélèvements (V19) ont été vérifiés.
- **Pré-enregistrements d'A16 et d'A17** : lus par titres et tableaux de prédictions, pas en entier.
- **Millésime AMECO de K-094** (fichier d'A03 contre prévision d'automne) : non tranché. Mon fichier AMECO fiscal (date interne 16/11/2026) ne contient pas le solde effectif (code UBLG) pour la France.

---

# SYNTHÈSE DE L'ARBITRE

## (a) Statut des résultats de la cellule

**Établis** (pièce primaire ou identité recalculée par A18, niveau A, sauf mention) :
- 51 déficits consécutifs depuis 1975 ; 1974 en excédent de 0,1 % du PIB, quasi-équilibre (V01–V02).
- Déficit 2025 : 151,6 Md€, 5,1 % (V03).
- +16 points de dépenses et +11 points de recettes depuis 1974, dont 80 % de la hausse des dépenses acquise en 1985 (V04).
- Écarts avec la zone euro : 7,5 / 5,4 points avec la France, 9,2 / 6,7 sans elle ; les deux sont à donner (V05).
- Environ deux tiers de l'écart de dépense en protection sociale et santé (62 à 67 % selon l'année) ; vieillesse 2,5 à 3,1 points selon la moyenne (V07–V08).
- Aucun excédent primaire depuis 2002, sur les 14 pays de la base (V10).
- Décomposition de la dette 1979–2025 (94 = 60 + 8 + 26), 2001–2025 (56 / 54) et 1984–1997 (15,5 / 9,4) : identités (V11–V13).
- Mesures de crise retirées (Cour 2024) (V18).

**Établis en partie** : une moitié a été recalculée par A18, l'autre seulement relue dans la copie de l'agent :
- 37 exercices de majorité absolue sur 37 en déficit : soldes recalculés ; classement des majorités d'A09 relu, non revérifié sur les compositions de l'Assemblée (V16).
- Écart programmé–exécuté d'environ −2 points à trois ans hors crises : soldes programmés relus dans la copie d'A08 (V17).

**Simulations rejouées, non vérifiées à la source** (niveau D) :
- Aucune combinaison **des mesures chiffrées** n'atteint 3 % ni ne stabilise avant 2035. Le résultat est robuste aux multiplicateurs nuls (A16) et aux taux bas (A17). A18 n'a fait que rejouer le module sur copie : c'est une preuve de reproductibilité, la conclusion qualitative restant robuste.
- Effort d'environ 5 points de PIB : 5,4 points pour 3 % en 2030 et 5,2 points pour stabiliser selon A15 ; 5,9 points en 2035 pour la norme d'A16. **Les horizons diffèrent** (2030 contre 2035) : seul l'ordre de grandeur converge.

**Fragiles** (vrais sous une convention ou dans une portée plus étroite que celle affichée) :
- R-A15-01 tel qu'affiché : il manque la plage 137 à 140 %, et jusqu'à 148 % (O1), ainsi que le rythme de dépense équivalent (ATT-1).
- R-A15-04 « tout scénario revient à la référence » : c'est une fourchette (O5).
- A01 R3 « au moins 92 % dans toutes les estimations lues » : vrai pour les estimations officielles (O2 ; V24).
- A14 R-A14-08, seconde moitié (« quasi-nécessité ») : c'est un jugement (O3).
- A11 R-A11-01, conséquence « la capture ne peut pas expliquer le déficit » (ATT-5).
- A09 R-A09-01, conséquence étendue au-delà du veto parlementaire (ATT-6).
- A03 R7 (assouplissement après chaque consolidation) : 2004–2006 n'est pas une consolidation corrigée du cycle ; deux séries sont probablement mêlées (T-07).
- A07 « seul pays dont la dette monte en 2015–2019 » : la Grèce (V28).
- « 1,9 point de financements de l'État » pour les retraites : relu dans la copie ; il s'agit de contributions et subventions d'équilibre (V25).

**Non établis** (la cellule ne doit pas les présenter comme acquis, dans un sens ou dans l'autre) :
- l'existence ou l'absence d'économies « à résultat égal » (ATT-2) ;
- le rôle de la composition des consolidations (ATT-3) ;
- l'ordre et la persistance des multiplicateurs au-delà d'un an (ATT-4 / O1) ;
- la capture comme cause ;
- le bien commun budgétaire ;
- les effets d'emploi (T-06) ;
- l'incidence par niveau de vie des baisses de 2018–2023 (O4) ;
- la nature (choisie ou subie) de la perte de niveau post-2019 contenue dans le « structurel » (O2) ;
- le coût en activité de 2010–2014 (O6) ;
- la part décidée de la hausse de dépense de 1974–1985 (fourchette S03).

## (b) Les trois recherches manquantes les plus susceptibles de changer un verdict

Elles sont obtenues en croisant les listes d'A16 (§16) et d'A17 (§17 bis), classées par probabilité de changer un verdict, puis par coût.

1. **Effet des consolidations sur l'activité : niveau et persistance, mesurés sur pièces françaises et sur les programmes de 2010.**
   - Contenu : évaluation ex post de 2011–2014 (prévisions de 2011–2012 contre réalisé, efforts structurels annuels ; Trésor, Insee, OFCE) ; composition **exécutée** des programmes de la zone euro de 2010 ; texte intégral d'AFG et de GLP.
   - C'est la recherche n° 1 d'A17, et les n° 2 et 10 d'A16. **Les deux la désignent sans s'être lus.**
   - Elle trancherait ATT-1 (2035 ou 2040), ATT-3, ATT-4, O1 et O6.
   - Coût : moyen (pièces publiques ; l'AEA a refusé l'accès en 403).
2. **Exécution des normes de dépense, en France et à l'étranger.**
   - Contenu : historique de l'ONDAM et des normes de l'État ; exécution 2025–2026 de la trajectoire de dépense nette du Conseil ; épisodes étrangers de dépense stable en volume sur trois ans ou plus ; trajectoire du plan à moyen terme d'octobre 2024, pour expliquer « 2029 » (HCFP) contre « 2035 » (modèle).
   - C'est la recherche n° 1 d'A16, et elle recoupe O5 d'A17 (part de l'erreur de croissance dans la dérive).
   - Elle trancherait ATT-1 (faisabilité) et ATT-6 (bien commun budgétaire).
   - Coût : faible à moyen.
3. **Écart de production 2025 par plusieurs méthodes et millésimes, avec l'incidence par niveau de vie des baisses de 2018–2023.**
   - Contenu : OFCE 2026, Banque de France, millésimes AMECO successifs ; Insee *France, portrait social*, IPP.
   - Ce sont les recherches n° 2 et 3 d'A17. A16 n'en a pas d'équivalent ; il ne la conteste pas.
   - Elle trancherait O2 (part structurelle, « structurel » contre « décidé ») et O4 (refus de l'effort ou conflit sur sa répartition).
   - Coût : faible.
   - Je la place en troisième position parce qu'elle change la **qualification** du déficit, plus que les verdicts chiffrés.

Les revues d'efficience lues en entier (n° 3 d'A16) arrivent juste après : elles décident ATT-2, mais aucune pièce n'indique qu'elles changeraient un verdict chiffré de la cellule.

## (c) Ce que la cellule ne peut PAS conclure à ce stade

- Que 3 % ou la stabilisation sont **hors d'atteinte** : seulement qu'aucune des mesures chiffrées n'y suffit. Une norme d'ensemble y parvient dans le modèle vers 2035–2040, selon la persistance, mais elle n'a aucun précédent français sur trois ans (V22).
- Que l'ajustement doit passer **d'abord par la dépense**, au-delà d'un jugement de préférences (O3, ATT-3, ATT-4).
- Que la capture, le blocage parlementaire ou les incitations **expliquent ou n'expliquent pas** la persistance depuis 1975. Seul le veto parlementaire est écarté (37 sur 37), et la puissance du test est faible.
- Qu'une économie « à résultat égal » existe **ou n'existe pas** dans le tiers de l'écart hors protection sociale et santé.
- Que le déficit structurel de 2025 est **choisi** : « structurel » contient une perte de niveau d'origine non établie.
- Que les vetos de 2024–2026 traduisent un **refus de tout effort** plutôt qu'un conflit sur sa répartition (O4).
- Rien sur la comparaison avec l'équipe Codex : **hors périmètre aujourd'hui**.

## Modifications demandées à l'orchestrateur (registres)

- Inscrire O1 à O7 d'A17 dans `contradictions.md`, section H : elle s'arrête à K-110.
- Inscrire V28 (Grèce, 2015–2019) et le cas de 2004–2006 chez A03, qui n'est pas une consolidation corrigée du cycle (T-07).
- Demander à A06 un manifeste des pièces (URL du rapport du COR).
- Supprimer dans A15 §14 la phrase sur K5 à 2,8 % (déjà corrigée dans la recette).
