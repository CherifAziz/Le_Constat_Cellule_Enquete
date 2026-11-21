# Tableau de bord de la cellule d'enquête « 51 ans de déficits »

**Dernière mise à jour : 21 novembre 2026, 14 h 22.** Tenu par l'orchestrateur (Fable 5.2). Ce fichier dit ce qui est réellement fait. Un dossier n'est « remis » que lorsque le fichier existe et a passé le contrôle de recette de l'orchestrateur ; le message de fin d'un agent n'est pas une preuve.

## 1. Où en est l'enquête

- **Phase** : fin de la quatrième session (21 novembre 2026). Tous les livrables prévus sont produits ; verdict de la synthèse : **modifier la thèse centrale**, inchangé après cinq compléments (S11, S12, S13, S14, C03). **34 dossiers remis et contrôlés, plus le rapport intégral ; aucun agent en cours. État : « recherche incomplète » au sens des critères de fin ; ce qui manque n'est pas accessible ou ne peut plus guère changer le verdict ; aucune décision éditoriale prise.**
- **Interruptions** : la limite d'usage du compte a arrêté les agents deux fois, vers 11 h 40 (quatre agents de la vague 2, relancés à 12 h 51) et vers 14 h 25 (A15 et A18, alors à l'état de squelette, relancés à 18 h 15). Aucun travail écrit n'a été perdu.
- Faits : lecture intégrale du paquet ; base de données commune ; 18 ordres de mission, 5 ordres de seconde passe, 1 ordre de comparaison ; 5 missions Codex écrites ; 24 comptes rendus de recette pour 23 dossiers ; contrôle de provenance ; rapports de transmission des vagues 1 et 2 ; matrice de couverture et plan version 2 ; chronologie fusionnée par script ; audit de la V5 (208 lignes) ; deux contre-expertises (15 attaques) ; arbitrage ; vérification de 28 chiffres (24 entièrement refaits) ; fichier des corrections demandées.
- Pas faits, faute de données publiées ou accessibles : bénéficiaire final des baisses d'impôts des entreprises ; compensations de l'État à la sécurité sociale et aux collectivités, décision par décision ; effet d'une consolidation au-delà de deux ans mesuré sur la France ; compositions de l'Assemblée au jour exact du vote pour 36 exercices ; adresses d'origine de 212 fichiers de la première vague. Reste à l'auteur : les décisions éditoriales.

## 2. Ressources vérifiées le 20/11/2026

| Ressource | État | Preuve |
|---|---|---|
| Sous-agents Opus 5.5, effort high | disponibles | test à blanc `journal\smoke_test_sous_agent.md` |
| Recherche web et lecture de pages par les sous-agents | disponibles | idem : page Insee, PDF du Sénat, notification Eurostat du 21/10/2026, séance de l'Assemblée du 04/11/2026 lus |
| Lecture de PDF | en deux temps (téléchargement puis `pypdf` ou `pymupdf`) | idem |
| Python 3.12 | `requests`, `openpyxl`, `xlrd`, `pypdf`, `pymupdf`, `numpy`, `bs4` ; **pas** de `pandas` ni `matplotlib` | contrôle direct |
| insee.fr, Eurostat (API), senat.fr, assemblee-nationale.fr, vie-publique.fr, cor-retraites.fr, web.archive.org, tresor.economie.gouv.fr, banque-france.fr, hatvp.fr, fipeco.fr | joignables | contrôle direct (HTTP 200) |
| **ccomptes.fr, hcfp.fr** | **injoignables** (connexion refusée, avec ou sans en-tête de navigateur) | contrôle direct et test à blanc |
| legifrance.gouv.fr, imf.org, oecd.org, aft.gouv.fr | refus des requêtes `curl` (403) ; lecture par un autre canal à tenter au cas par cas | contrôle direct |
| Équipe Codex (GPT-6.2 Astra) | lancée séparément par le commanditaire ; **déjà active** | fichiers en cours d'écriture depuis 10 h 33 dans `…\Le_Constat_Cellule_Enquete\resultats\codex\` (niveau supérieur) |

**Conséquence** : toute pièce de la Cour des comptes ou du HCFP est lue par un canal tiers (vie-publique.fr, archive web, rapport parlementaire qui la reproduit) et marquée comme telle. Les pièces les plus récentes (novembre 2026) risquent de ne pas être archivées : à surveiller à la recette.

## 3. Base de données commune

`resultats\donnees\commun\` — 21 fichiers Insee bruts (séries longues et comptes des APU, base 2020), 4 jeux Eurostat (JSON et CSV), 3 mises à plat, manifeste avec URL, date d'extraction (20/11/2026, 09 h 37 UTC) et SHA-256. Scripts : `resultats\scripts\commun\`. C'est le millésime de référence de la cellule.

## 4. Agents

États possibles : *ordre écrit* → *en cours* → *message de fin reçu* → *recette passée* (ou *recette refusée, complément demandé*) → *contre-expertisé*.

| Agent | Rôle | Chantiers | Vague | Exécutant | Ordre de mission | État |
|---|---|---|---|---|---|---|
| A01 | Architecte comptable | C01, C05 | 1 | Opus 5.5 high | `missions\A01.md` | **recette passée avec réserves** (11 h 25) — `journal\recette_A01.md` ; non contre-expertisé |
| A02 | Historien 1974–2000 | C02 | 1 | Opus 5.5 high | `missions\A02.md` | **recette passée avec réserves** — `journal\recette_A02.md` ; mesures indisponibles pour 15 exercices ; non contre-expertisé |
| A03 | Historien 2001–2026 | C02 | 1 | Opus 5.5 high | `missions\A03.md` | **recette passée avec réserves** — `journal\recette_A03.md` ; fiches partielles pour 11 exercices ; non contre-expertisé |
| A04 | Fiscaliste, recettes | C04 | 1 | Opus 5.5 high | `missions\A04.md` | **recette passée avec réserves** (11 h 26) — `journal\recette_A04.md` ; lacune 1975–1988 ; non contre-expertisé |
| A05 | Dépenses et qualité des services | C03 | 1 | Opus 5.5 high | `missions\A05.md` | **recette passée avec réserves** — `journal\recette_A05.md` ; efficience non instruite ; non contre-expertisé |
| A06 | Travail, croissance, démographie, retraites, santé | C06, C07 | 1 | Opus 5.5 high | `missions\A06.md` | **recette passée avec réserves** — `journal\recette_A06.md` ; emploi, santé, immigration partiels ; non contre-expertisé |
| A07 | Dette et monnaie | C08 | 1 | Opus 5.5 high | `missions\A07.md` | **recette passée avec réserves** — `journal\recette_A07.md` ; prime de risque et BCE partiels ; non contre-expertisé |
| A08 | Juriste budgétaire, institutions | C09 | 2 | Opus 5.5 high | `missions\A08.md` | **recette passée avec réserves** (13 h 44) — `journal\recette_A08.md` ; règles européennes et littérature partielles ; non contre-expertisé |
| A09 | Politiste, historien des choix | C10 | 2 | Opus 5.5 high | `missions\A09.md` | **recette passée avec réserves** (13 h 38) — `journal\recette_A09.md` ; cas d'avant 2013 partiels ; non contre-expertisé |
| A10 | Psychologie, économie comportementale | C11 | 2 (anticipé) | Opus 5.5 high | `missions\A10.md` | **recette passée avec réserves** — `journal\recette_A10.md` ; décideurs partiels ; non contre-expertisé |
| A11 | Flux d'argent, contrôle public | C12 | 2 | Opus 5.5 high | `missions\A11.md` | **recette passée avec réserves** (13 h 11) — `journal\recette_A11.md` ; infractions non instruites ; non contre-expertisé |
| A12 | Comparatiste | C13 | 2 | Opus 5.5 high | `missions\A12.md` | **recette passée avec fortes réserves** (13 h 26) — `journal\recette_A12.md` ; un seul épisode étranger instruit entièrement ; non contre-expertisé |
| S01 | Complément de seconde passe : mesures de recettes et de dépenses 1975–1992 et 1998–1999 | C02, C04 | seconde passe | Opus 5.5 high | `missions\S01.md` | **recette passée avec réserves** (13 h 30) — `journal\recette_S01.md` ; part décidée de la dépense de 1974–1985 toujours indéterminée ; non contre-expertisé |
| S02 | Complément de seconde passe : épisodes étrangers sur pièces et règles budgétaires étrangères | C13, C09 | seconde passe | Opus 5.5 high | `missions\S02.md` | **recette passée avec réserves** (18 h 15) — `journal\recette_S02.md` ; quatre épisodes sur pièces sur six demandés ; non contre-expertisé |
| S03 | Complément de seconde passe : protection sociale 1974–1985, décisions ou inertie (tension T-02) | C02, C03 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S03.md` | **recette passée avec réserves** (18 h 50) — `journal\recette_S03.md` ; 4 sorties rejouées à l'identique ; « inertie » = poursuite des rythmes d'avant 1974 ; non contre-expertisé |
| S04 | Complément de seconde passe : qui paie, répartition de l'effort des deux portefeuilles (questions 18 et 20) | C14, C15 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S04.md` | **recette passée avec réserves** (18 h 44) — `journal\recette_S04.md` ; profil par niveau de vie pour un cinquième des montants seulement ; non contre-expertisé |
| A13 | Réformateur des dépenses | C14 | 3 | Opus 5.5 high | `missions\A13.md` | **recette passée avec réserves** (14 h 19) — `journal\recette_A13.md` ; études d'efficience en résumé ; non contre-expertisé |
| A14 | Réformateur recettes et croissance | C15 | 3 | Opus 5.5 high | `missions\A14.md` | **recette passée avec réserves** (14 h 16) — `journal\recette_A14.md` ; rendements nets en partie hypothétiques ; non contre-expertisé |
| A15 | Modélisateur contrefactuel | C16 | 3 | Opus 5.5 high | `missions\A15.md` | **recette passée avec réserves** (18 h 42) — `journal\recette_A15.md` ; 24 sorties rejouées à l'identique ; taux de long terme et multiplicateur posés par hypothèse ; non contre-expertisé |
| A16 | Contradicteur libéral | C17 | 3 | Opus 5.5 high **et** Codex (CX-02), séparément | `missions\A16.md` | **recette passée avec réserves** (19 h 09) — `journal\recette_A16.md` ; 8 attaques, non arbitrées ; lecture incomplète de 7 dossiers |
| A17 | Contradicteur keynésien et institutionnaliste | C17 | 3 | Opus 5.5 high **et** Codex (CX-03), séparément | `missions\A17.md` | **recette passée avec réserves** (19 h 11) — `journal\recette_A17.md` ; 7 objections, non arbitrées ; lecture incomplète de 11 dossiers |
| A18 | Vérificateur indépendant, arbitre | tous | 3 | Opus 5.5 high **et** audit aveugle Codex (CX-01) | `missions\A18.md` | **trois parties remises, recettes passées avec réserves** — `journal\recette_A18_partie1.md`, `journal\recette_A18_parties2et3.md` ; 208 lignes d'audit ; 28 vérifications dont 24 entièrement refaites, aucune infirmée ; 15 attaques arbitrées ; versions de Codex hors périmètre |
| S06 | Complément de seconde passe : cinq causes souvent avancées et jamais examinées (test de saturation, question 22) | tous | seconde passe, plan v2 | Opus 5.5 medium | `missions\S06.md` | **recette passée avec réserves** (19 h 29) — `journal\recette_S06.md` ; aucune des cinq causes démontrée comme cause de la dégradation ; deux sans série récente ; non contre-expertisé |
| C01 | Comparaison avec les travaux indépendants de l'équipe Codex (lecture seule) | C17 | contre-expertise croisée | Opus 5.5 high | `missions\C01_comparaison_codex.md` | **recette passée avec réserves** (20 h 10) — `journal\recette_C01.md` ; 174 accords et 17 désaccords entre les deux audits ; aucun écart de fait sur 13 chiffres centraux ; conclusions non comparées |
| C02 | Comparaison des conclusions avec celles de Codex ; vérification de quatre résultats propres à Codex | C17 | contre-expertise croisée | Opus 5.5 high | `missions\C02_conclusions_codex.md` | **recette passée avec réserves** (21/11, 09 h 45) — `journal\recette_C02.md` ; 14 accords, aucune divergence de fait, 7 divergences de convention ou de jugement ; quatre résultats de Codex confirmés |
| S05 | Complément : dépense et résultats, études d'efficience en texte intégral (question 11) | C03, C14 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S05.md` | **recette passée avec réserves** (21/11, 09 h 39) — `journal\recette_S05.md` ; aucune économie à résultat égal établie, quatre suggérées ; cinq études lues en entier |
| S07 | Complément : consolidations de 2010–2015 sur pièces, composition exécutée et coût en activité | C13, C16 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S07.md` | **recette passée avec réserves** (21/11, 09 h 51) — `journal\recette_S07.md` ; consolidation de 2011–2014 faite à 83 % par les recettes ; multiplicateur non établi au-delà de deux ans ; coûts simulés, non mesurés |
| S08 | Complément : incidence des baisses de prélèvements de 2018–2023 ; exécution des normes de dépense | C04, C09 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S08.md` | **recette passée avec réserves** (21/11, 09 h 58) — `journal\recette_S08.md` ; aucune norme « zéro volume » tenue plus de quatre ans ; 80 % du gain des réformes du capital aux 10 % les plus aisés ; séries de l'État en bornes basses |
| S10 | Complément : coût publié de sept décisions sociales de 1974–1982 (test de renversement de S03) | C02, C03 | seconde passe, plan v2 | Opus 5.5 medium | `missions\S10.md` | **recette passée avec réserves** (21/11, 10 h 06) — `journal\recette_S10.md` ; sept décisions : 1,27 point de PIB en 1985 (0,81 à 1,99) ; le verdict de S03 tient ; décisions postérieures à 1974 : 13 à 32 % de la hausse |
| R01 | Rapport intégral : état de ce qui est établi, non établi et disputé (aucune recherche nouvelle) | tous | consolidation | Opus 5.5 high | — | **accepté** (21/11, 10 h 22) — `journal\recette_R01.md` ; lu en entier ; 50 affirmations contrôlées en transcription |
| — | Synthèse éditoriale : verdict sur la thèse du script V5 | tous | en dernier | orchestrateur (Fable 5.2) | — | **écrite** (21/11, 10 h 22) — `synthese_editoriale.md` ; verdict « modifier » ; non aveugle au verdict de Codex ; décisions listées, non prises |
| S11 | Test de l'hypothèse du « bien commun budgétaire » (inconnue de rang 1 de la synthèse) | C10, C11 | suites de la synthèse | Opus 5.5 high | `missions\S11.md` | **recette passée avec réserves** (21/11, 10 h 54) — `journal\recette_S11.md` ; hypothèse du bien commun budgétaire : ni soutenue ni contredite ; majorités éclatées pas pires ; canal du financement non testable |
| C03 | Réconciliation des deux modèles de trajectoire : 5,2 ou 3,1 points | C16, C17 | suites de la synthèse | Opus 5.5 high | `missions\C03_reconciliation_modeles.md` | **recette passée avec réserves** (21/11, 10 h 56) — `journal\recette_C03.md` ; les deux modèles sont réconciliés : reste nul ; 1,5 point d'écart vient du budget 2027 compté ou non, le reste d'hypothèses ; aucune erreur de calcul |
| S13 | Effet d'une consolidation au-delà de deux ans et composition : études en texte intégral | C13, C16 | suites de la synthèse | Opus 5.5 medium | `missions\S13.md` | **recette passée avec réserves** (21/11, 10 h 51) — `journal\recette_S13.md` ; persistance non tranchée ; « la dépense coûte moins » majoritaire mais contesté, une seule base de données ; effet sur la dette non significatif en moyenne |
| S12 | Majorités vérifiées à la date de chaque vote ; nombre de ministres dépensiers (dernier canal testable du bien commun budgétaire) | C10 | suites de la synthèse | Opus 5.5 medium | `missions\S12.md` | **recette passée avec réserves** (21/11, 11 h 28) — `journal\recette_S12.md` ; 42 budgets sur 51 votés par une majorité absolue ; « tous en déficit » ne discrimine pas ; ministres dépensiers : résultat nul sans puissance |
| S14 | Bénéficiaires de la taxe d'habitation, de l'impôt sur les sociétés et des impôts de production (2018–2023) | C04 | suites de la synthèse | Opus 5.5 medium | `missions\S14.md` | **recette passée avec réserves** (21/11, 14 h 22) — `journal\recette_S14.md` ; taxe d'habitation chiffrée par dixième ; bénéficiaire final des baisses des entreprises non mesuré |

Consignes communes à tous : `missions\00_CONSIGNES_COMMUNES.md`.

## 5. Missions préparées pour Codex (lancement séparé par le commanditaire)

Dossier : `resultats\codex\missions\`. Mode d'emploi : `CX-00_LISEZ-MOI.md`.

| Mission | Objet | Peut démarrer | État |
|---|---|---|---|
| CX-01 | Audit aveugle, ligne à ligne, de la V5 | maintenant | écrite, non lancée par la cellule |
| CX-02 | Contradicteur libéral (A16), phase 1 de pré-enregistrement | maintenant | écrite, non lancée |
| CX-03 | Contradicteur keynésien (A17), phase 1 | maintenant | écrite, non lancée |
| CX-04 | Réplication quantitative au format d'échange | maintenant | écrite, non lancée |
| CX-05 | Contre-expertise des dossiers de la vague 1 | **maintenant** : recette passée pour A01 à A07 et A10 | écrite, non lancée par la cellule |

Le travail propre de Codex n'a été **ni modifié ni fusionné**. Les missions C01 (20 novembre) et C02 (21 novembre) l'ont lu en lecture seule : audit de la V5, calculs, quatre fichiers de recherche, puis rapport intégral, politiques, contradictions et synthèse éditoriale. Contrôle du 21 novembre à 9 h 44 : 113 fichiers, aucun modifié depuis le 20 novembre à 11 h 09.

## 6. Couverture des chantiers

Le point de départ est `10_DIAGNOSTIC_INITIAL.md`. Colonne « avancement » : ce que la cellule a elle-même établi, pas ce qu'Astra apporte.

| Chantier | Responsable | Sources primaires visées | Avancement | Lacune principale | Priorité |
|---|---|---|---|---|---|
| C01 Définitions et mesures | A01 | Insee, Eurostat, SEC 2010 | dossier remis, recette passée | bases antérieures à 2005 ; estimations FMI et OCDE de 2025 | haute |
| C02 Histoire annuelle | A02, A03, S01 | lois de finances, rapports parlementaires, Insee | 53 fiches ; **chronologie fusionnée par script** (`01_chronologie_1974_2026.md`) : 253 cellules obligatoires renseignées sur 265 ; 5 manquantes (dette de 1974 à 1977, série Insee commençant en 1978 ; mesures de 2016) | mesures partielles pour 17 exercices ; 90 cellules avec un élément de mémoire non vérifié | haute |
| C03 Dépenses | A05 | comptes des APU, COFOG, Drees | dossier remis, recette passée | efficience, coûts unitaires, fonctions avant 1995 | haute |
| C04 Recettes et niches | A04, S01 | annexes budgétaires, évaluations, rapports du Sénat | dossiers remis, recettes passées ; mesures de l'État de 1975 à 1991 relevées | comptes de la sécurité sociale 1975–1985 ; impôts locaux ; séries primaires 1989–2017 | **très haute** |
| C05 Sous-secteurs et transferts | A01 | tableaux Insee 3.2xx | réconciliation faite depuis 1978 | détail des transferts État → sécurité sociale | **très haute** |
| C06 Croissance, emploi | A06 | Insee, Eurostat, OCDE, Dares | dossier remis, recette passée | évaluations des politiques de l'emploi ; immigration | **très haute** |
| C07 Retraites, santé | A06 (avec A05) | COR, Drees, évaluations | retraites instruites ; santé partielle | santé, dépendance, effets distributifs | haute |
| C08 Dette, monnaie | A07 | BCE, Banque de France, AFT | dossier remis, recette passée | résidu de dette d'avant 1999 ; prime de risque ; effet des achats de la BCE | haute |
| C09 Institutions | A08 | programmes de stabilité, lois de programmation, rapports de l'Assemblée | dossier remis, recette passée : 38 documents programmés contre exécutés | règles européennes ; Sénat ; littérature ; cas néerlandais | haute |
| C10 Coalitions et vetos | A09 | scrutins, comptes rendus, listes de l'Assemblée | dossier remis, recette passée : 8 cas sur pièces (2013–2026), 10 partiels | scrutins de 1975 à 2007 ; 1983 ; mobilisations ; répartition de l'effort | **très haute** |
| C11 Psychologie | A10 | études, enquêtes d'opinion | dossier remis, recette passée | croyances des élus ; séries d'opinion d'avant 2014 | **très haute** |
| C12 Intérêts, opacité | A11 | Cour, Parlement, HATVP, justice | dossier remis, recette passée : 5 dossiers instruits, 2 partiels | infractions et condamnations ; arbitrage de dividendes ; loi de finances 2026 | **très haute** |
| C13 Comparaisons | A12, S02 | Eurostat, FMI, OCDE, archives, banques centrales | dossiers remis, recettes passées : singularité testée ; cinq épisodes sur pièces (Suède, Canada, Allemagne, Belgique, Italie) ; règles étrangères et leurs coûts | échecs étrangers sur séries seulement | atteint le critère de fin |
| C14 Réformes de dépenses | A13 | contribution de la Cour de novembre 2026, vagues 1 et 2 | dossier remis, recette passée : 22 mesures, 6 règles, 3 enveloppes | études d'efficience en texte intégral ; chômage, dépendance ; répartition par revenu | haute |
| C15 Recettes et croissance | A14 | budget 2027, Cour, évaluations | dossier remis, recette passée : 25 mesures, 3 enveloppes | élasticités françaises ; répartition par revenu ; sensibilités | haute |
| C16 Scénarios | A15 | A13, A14, base commune, Commission, budget 2027 | dossier remis, recette passée : modèle, référence, 5 combinaisons, sensibilités, chocs, 6 contrefactuels | taux à terme ; prime de risque ; règle d'or ; bloc d'activité non validé | haute |
| C17 Contre-enquête | A16, A17, A18, C01, C02, Codex | tout | audit, contre-expertises, arbitrage, vérifications, comparaison avec Codex (audits, chiffres, 30 conclusions) : remis et contrôlés | réconciliation des deux modèles de trajectoire ; six thèmes non comparés | moyenne |

## 7. Blocages et points de vigilance

1. **Deux arborescences de résultats.** Le paquet est imbriqué : les fichiers de cadrage sont dans `…\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\`, et la cellule écrit dans le `resultats\` de ce dossier, comme le prévoit le README. Codex écrit dans `…\Le_Constat_Cellule_Enquete\resultats\codex\`, un niveau au-dessus. Rien ne se chevauche ; un regroupement éventuel est une décision du commanditaire, à prendre après les contre-expertises.
2. **Cour des comptes et HCFP injoignables** depuis ce poste (voir §2).
3. **Tension de séquencement relevée** : `10_DIAGNOSTIC_INITIAL.md` classe C11 et C12 en priorité de première vague, `02_AGENTS.md` place A10 et A11 en vague 2. Arbitrage : vague 1 = A01–A07 comme prévu ; A10 lancé par anticipation (aucune dépendance comptable) ; A11 attend l'inventaire d'A04.
4. **Risque de volume** pour A02 et A03 (27 et 26 fiches annuelles chacun) : si un dossier revient incomplet, un complément ciblé sera lancé ; il ne sera pas déclaré complet.
5. **Anomalie de la source Insee** (instruite par A01) : de 1959 à 1977, les soldes de l'État et des ODAC ne redonnent pas celui de l'administration centrale ; le solde total n'est pas touché. La signaler à l'Insee est une décision du commanditaire.
6. **Provenance** : les sondages de recette ont été faits dans les copies des pièces conservées par les agents. Sept pièces ont ensuite été retéléchargées à l'origine et trouvées identiques (`journal\controle_provenance.md`) ; les autres restent « relues dans la copie de l'agent ».
7. **Traçabilité inégale** : A01, A02, A04 et A06 n'avaient pas de manifeste. Le 21 novembre : empreintes figées pour 241 fichiers ; puis **rattachement par preuve** (chaque adresse citée retéléchargée, empreintes comparées) : **29 fichiers identiques à leur origine** (A01 : 7 ; A02 : 5 ; A04 : 16 ; A06 : 1). Les autres sont des fichiers dérivés, des réponses d'interfaces de données qui ont changé, ou des pièces dont l'adresse n'est pas dans le texte ; A06 ne cite que deux adresses (`journal\manifestes_reconstitues.md`).
8. **Recettes légères** : pour A05, A06 et A07, seules les sections 11 à 15 ont été relues par l'orchestrateur.
9. **Limite d'usage** : deux fenêtres épuisées. Depuis 18 h 15 : quatre agents au plus en parallèle, effort moyen pour la recherche documentaire, lecture des dossiers limitée aux sections utiles, usage relevé avant chaque lot (12 % de la fenêtre à 18 h 12).
10. **Répertoire de travail** : depuis la reprise de 18 h 07, le répertoire de travail de la session est le dossier de niveau supérieur, celui où Codex écrit. Tous les ordres donnent la racine imbriquée en chemin absolu et interdisent le dossier de Codex aux agents de la cellule.

## 8. Désaccords

Voir `contradictions.md` (102 lignes, dont la section H : attaques des contradicteurs) et `corrections_demandees.md` (19 arbitrages et 7 corrections reçues ; fait foi là où il diffère d'un dossier). Désaccords non tranchés : multiplicateurs au-delà d'un an ; composition des ajustements ; emploi et solde (T-06) ; séries récentes sur l'immigration et la fraude.

## 9. Registres

- `hypotheses.md` : registre initial des hypothèses concurrentes.
- `preuves.md` : index des preuves (faits de contrôle de l'orchestrateur ; les faits des agents y entreront après recette, avec le statut « non contre-expertisé »).
- `contradictions.md` : index des contradictions.
- `journal\journal_orchestration.md` : journal horodaté des actions.
