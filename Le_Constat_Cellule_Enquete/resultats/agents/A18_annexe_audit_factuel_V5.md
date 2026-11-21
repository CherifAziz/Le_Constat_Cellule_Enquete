# A18 — Annexe : audit factuel ligne à ligne du script V5 (13/11/2026)

Agent A18, vérificateur indépendant et arbitre scientifique. Date de travail : 20 novembre 2026. Objet : `sources\script_V5_2026-11-13.txt` (blocs B1 à B6, 161 lignes).
Mandat : signaler les erreurs, ne pas reformuler. **Aucune formulation de remplacement n'est proposée.**

## 0. Méthode

- **Passe 1, aveugle** (section 1). Je l'ai écrite sans ouvrir `resultats\agents\` (sauf mes fichiers), `resultats\transmissions\`, `contradictions.md`, `preuves.md`, `journal\`, `codex\` ni la contre-enquête Astra. Je n'ai pas non plus ouvert le dossier `resultats\` de niveau supérieur.
- **Matériaux de la cellule utilisés.** Seulement la base commune (classeurs Insee et JSON Eurostat bruts, empreintes conformes au `MANIFESTE.csv`) et des pièces brutes de la cellule, que j'ai **retéléchargées à leur adresse d'origine**. La comparaison des empreintes est en §0.2.
- **Découpage.** Une ligne par chiffre, date, citation, comparaison ou lien causal : **200 affirmations atomiques**, identifiées `V5-Bx-nn`. La ligne du script est donnée dans la colonne « L. ».
- **Deux échelles de verdict dans le même fichier.**
  - Colonne `verdict`, échelle de l'ordre de mission : exact / exact sous condition / imprécis / trompeur par périmètre ou juxtaposition / faux / non vérifiable à ce jour.
  - Colonne `verdict_M2`, échelle du plan v2 du coordinateur : exact / inexact / trop général / non démontré / non vérifié.
  - Niveau de preuve A à F selon `04_PREUVES_ET_CALCULS.md` §II. Provenance : [C], [S], [X], [M].
- **Fichiers.**
  - `resultats\donnees\A18\A18_audit_V5_passe1.csv` (séparateur « ; », 16 colonnes : les 14 demandées plus `verdict_M2` et `niveau_preuve`).
  - Pièces dans `resultats\donnees\A18\sources\`, manifeste dans `MANIFESTE_PIECES.csv`, extractions texte dans `textes\`.
  - Scripts dans `resultats\scripts\A18\` : a18_01 à a18_12.

### 0.1 Scripts et calculs livrés

| Script | Objet | Sortie |
|---|---|---|
| a18_01_explore_insee.py | structure et empreintes des classeurs Insee | console |
| a18_02_series_insee.py | soldes, dépenses, recettes, dette (1974, 1985, 1993, 2025), dette en mois, vitesse dette/PIB | donnees\A18\a18_02_series_insee.csv |
| a18_03_interets_insee.py | intérêts / déficit 1993, solde primaire 2025 (tableau 3.201) | a18_03_interets_insee.txt |
| a18_04_telecharge_eurostat.py | téléchargement Eurostat (taxag UE 27, COFOG et comptes en Md€ de la zone euro, PIB, Suède) | sources\eurostat_*.json |
| a18_05_comparaisons_eurostat.py | rang des prélèvements, écarts à la zone euro avec et hors France, COFOG, Allemagne, Italie, Suède | a18_05_comparaisons_eurostat.txt |
| a18_06 / a18_07 / a18_08 | retéléchargement avec empreinte ; extraction texte (pages PDF réelles) ; recherche mot pour mot | sources\, textes\ |
| a18_09_pib_volume.py | croissance 1960-1974, 1975-1985, 2000 (Insee BDM et Eurostat) | a18_09_pib_volume.txt |
| a18_10_calculs_simples.py | €/habitant, M€/jour, part empruntée, mois de PIB, ratio des écarts de taux, voix manquantes, sensibilité aux taux | a18_10_calculs_simples.txt |
| a18_11_compare_empreintes.py | comparaison pièce A18 / copie de la cellule | A18_comparaison_empreintes.csv |
| a18_12_construit_passe1.py | construction du CSV et des tableaux de passe 1 | A18_audit_V5_passe1.csv |

### 0.2 Vérification des copies de la cellule

J'ai retéléchargé 40 pièces dont la cellule détient une copie et comparé les SHA-256 :

- **34 copies sont identiques** : RESF, avis HCFP 2026-5, rapports de la Cour de juillet 2024, mars 2024, février 2025 et novembre 2026, rapports du Sénat, scrutins, comptes rendus de l'AN, Persson 1995, programme suédois de 1998, données BCE, etc.
- **5 copies diffèrent :**
  - rapport annuel 2026 du COR : deux versions en ligne, juin et juillet 2026. Les ratios cités sont identiques dans les deux ;
  - deux pages bpb (pages web dynamiques) ;
  - ordonnance 82-270 : capture d'archive différente, contenu concordant ;
  - texte du PLF 2027 : PDF officiel de l'AN contre fichier « .raw » de la cellule.
- **1 pièce n'a pas pu être retéléchargée** : page vie-publique de la LPFP 2023, réponse vide. J'ai utilisé la décision du Conseil constitutionnel à la place.

Détail : `donnees\A18\A18_comparaison_empreintes.csv`.

## 1. Passe 1 — aveugle (figée, voir §1.9)

### 1.1 Répartition des verdicts (200 affirmations)

| Échelle mission initiale | n | Échelle M2 | n |
|---|---|---|---|
| exact | 114 | exact | 163 |
| exact sous condition | 48 | inexact | 8 |
| imprécis | 16 | trop général | 10 |
| trompeur par périmètre ou juxtaposition | 5 | non démontré | 15 |
| faux | 2 | non vérifié | 4 |
| non vérifiable à ce jour | 15 | | |

Par bloc (M2) :

| Bloc | Affirmations | exact | inexact | trop général | non démontré | non vérifié |
|---|---|---|---|---|---|---|
| B1 | 17 | 16 | 0 | 0 | 1 | 0 |
| B2 | 16 | 14 | 0 | 0 | 1 | 1 |
| B3 | 37 | 31 | 0 | 2 | 4 | 0 |
| B4 | 40 | 34 | 3 | 1 | 2 | 0 |
| B5 | 53 | 41 | 3 | 3 | 4 | 2 |
| B6 | 37 | 27 | 2 | 4 | 3 | 1 |

### 1.2 Les dix affirmations les plus fragiles (passe 1)

1. **V5-B5-49**, charge de la dette « autant que tout le budget de la Défense : 72 milliards ». La charge de la dette de l'État (programmes 117 et 355) est de 72,93 Md€ au PLF 2027. La mission Défense est de 63,4 Md€ hors CAS Pensions. La comparaison est fausse de 9,5 Md€ (DP Budget 2027, p.57 et p.88).
2. **V5-B5-50**, « chaque dixième de point ... 4 milliards ». Selon le PAP 117, un choc de +100 pb coûte 3,4 Md€ la 1re année et environ 19 Md€ la 5e, soit 0,34 puis environ 1,9 Md€ par dixième de point. Même appliqué à tout le stock, un dixième ne coûte que 2,8 Md€ (État) ou 3,5 Md€ (APU). Le chiffre est surestimé d'environ un facteur 2.
3. **V5-B5-51**, « plus que tout le budget de la Culture » (3,4 Md€). La comparaison tombe avec le chiffre corrigé du point 2.
4. **V5-B4-39**, HCFP « semble peu plausible ». L'avis 2026-5 écrit « rendent très peu vraisemblable sa concrétisation ». Les guillemets ne sont pas conformes à la pièce relative au budget 2027.
5. **V5-B5-48**, « les interrogations sur la situation politique en France ». La formule est introuvable dans le RESF, le DP Budget 2027, le PLF 2027, le PAP 117, le PLFG 2026 et le bulletin AFT d'octobre. Le HCFP écrit « l'incertitude quant à la situation politique ».
6. **V5-B6-31**, juxtaposition « 10 / 44 / 150 ». Elle rapproche une économie du seul système de retraite en 2030, un effort toutes administrations en 2026 incluant la hausse militaire, et le déficit réalisé en 2025. C'est le cas exact que vise la norme 04 §III.7.
7. **V5-B5-40**, OAT au-dessus de 5 % « le 22 octobre ». Aucune série quotidienne officielle n'a été obtenue. La moyenne BCE d'octobre est de 4,89 % et la presse hésite entre le 21 et le 22.
8. **V5-B6-06**, Suède « environ 12 % » en 1993. La série OCDE actuelle donne -10,7 % ; Persson (1995) cite 10 % pour 1994. Le chiffre de 12 % ne se trouve que dans la presse (Reuters 2025, « at worst »).
9. **V5-B4-34**, LPFP « votée en novembre ». Elle a été adoptée en lecture définitive sans vote, par l'article 49.3 (Conseil constitutionnel 2023-857 DC, saisine du 16/11/2023).
10. **V5-B3-22 et V5-B3-21**, écarts à la zone euro. La moyenne inclut la France ; hors France, l'écart de dépense est de 9,3 pts et non 7,5. Les « deux tiers » sont calculés sur la COFOG 2024 (écart de 8,1 pts) alors que l'écart cité est celui de 2025.

### 1.3 Erreurs de logique relevées

- **Identité comptable présentée comme cause** :
  - V5-B3-05 (« le trou, c'est cette différence ») ;
  - V5-B3-28 (« exactement » les 2 points) ;
  - V5-B6-29, où le trou est attribué à la seule dépense alors que B3-30 établit 62 Md€ de baisses d'impôts non compensées.
- **Changement de périmètre ou d'année en cours de raisonnement** :
  - V5-B3-22 (COFOG 2024 contre écart 2025) ;
  - V5-B1-11 (intérêts de 2026, prévision, et non réalisé 2025 : 953 €/hab.) ;
  - V5-B5-49 (charge de la dette de l'État contre mission Défense hors pensions) ;
  - V5-B6-31.
- **Juxtaposition de grandeurs non comparables** : V5-B6-31 et V5-B5-51.
- **Généralisation à partir d'un ou deux cas** :
  - V5-B4-18 (« deux majorités, le même réflexe ») ;
  - V5-B5-30 (la survie de Lecornu attribuée à la suspension) ;
  - V5-B6-36 (transposition de la Suède : monnaie propre, croissance de 4 %).
- **Contrefactuel non testé** : V5-B3-36 (« elle monterait doucement »).
- **Confusion déficit / dette** : V5-B6-30 (« chaque crise l'a creusé »).

### 1.4 Chiffres-clés refaits à la source (35)

Chaque chiffre est recalculé ou relu dans une pièce primaire ; les scripts sont en §0.1.

| N° | V5 | Recalcul A18 | Pièce | Script |
|---|---|---|---|---|
| K01 | 51 ans de déficit | 51/51 exercices 1975-2025 < 0 | Insee fig. 2 | a18_02 |
| K02 | excédent 1974 « minuscule » | +0,1 % du PIB, +0,2 Md€ | Insee | a18_02 |
| K03 | > 1 100 €/hab. d'intérêts | 1 146 € (prévision 2026, APU) ; 953 € en 2025 réalisé | HCFP, Insee IP2087, t_3201 | a18_10 |
| K04 | FR plus cher que l'Italie | 4,89 contre 4,68 % (oct. 2026) | BCE IRS | a18_10 |
| K05 | 458 contre, 0 pour | 458/0, 2 abstentions | AN scrutin 9759 | — |
| K06 | 152 Md€ | 151,6 (t_3201) / 152,5 (IP2106) | Insee | a18_03 |
| K07 | 9 sur 100 | 8,8 | Insee t_3201 | a18_10 |
| K08 | > 400 M€/jour | 415 | Insee | a18_10 |
| K09 | 207 Md€ record | 207,1 (2020) | Insee | a18_02 |
| K10 | 41 % en 1974 | 41,3 / 41,4 | Insee | a18_02 |
| K11 | 52 % / 57 % | 52,2 / 57,3 | Insee | a18_02 |
| K12 | +11 / +16 points | +10,8 / +16,0 | Insee | a18_02 |
| K13 | 1985 : +1 / +3 en 40 ans | +1,06 / +3,12 | Insee | a18_02 |
| K14 | 56 % en 1993 | 56,5 % (95 % de la hausse 1974-2025) | Insee | a18_02 |
| K15 | moitié du trou 1993 = intérêts | 50,4 % bruts, 42 % nets | Insee t_3201 | a18_03 |
| K16 | 24 € sur 100 | 24,3 % (COR 2025) ; 23,4 % (COFOG 2024) | COR, Eurostat | a18_05 |
| K17 | 3 postes > moitié | 56,9 % | Eurostat COFOG | a18_05 |
| K18 | 7,5 pts de plus que la ZE | 7,5 (ZE avec France), 9,3 (hors France) | Eurostat | a18_05 |
| K19 | près des 2/3 | 64 % (65 % hors France), COFOG 2024 | Eurostat | a18_05 |
| K20 | prélevé un peu plus de 5 pts | 5,4 en recettes ; 4,7 en PO | Eurostat | a18_05 |
| K21 | 2,1 / 1,8 / 1,3 cotisant par retraité | identiques | COR RA 2026 p.74 | — |
| K22 | 62 Md€ | 62 Md€ en 2023, « non compensées » | Cour, juillet 2024, p.35-36 | — |
| K23 | 150 Md€ d'impôts → record UE | 51,1 % contre BE 44,7 | Eurostat | a18_10 |
| K24 | dette 8 mois (2007), près de 14 (auj.) | 7,9 / 13,9 | Insee | a18_10 |
| K25 | Allemagne près de 10 → 7 mois | 9,3 (2013) ou 8,9 (2014) → 7,0 | Eurostat | a18_10 |
| K26 | 36 Md€ de boucliers | 36 Md€ nets État 2021-2024 | Cour, mars 2024, p.9 | — |
| K27 | cagnotte 50 MdF | 51,4 MdF ; 40,6 en baisses d'impôts | Sénat PLFR 2000 | a18_10 |
| K28 | 2,7 % ; 4,9 → 5,2 ; 5,4 | identiques | Cour 2024 p.109 ; Sénat r24-153 p.6 ; Insee | — |
| K29 | 9 voix (2023) | 287 − 278 = 9 | CR AN 20/03/2023 | a18_10 |
| K30 | 364 contre (Bayrou) | 364 contre, 194 pour | AN scrutin 3054 | — |
| K31 | suspension ≈ 2 Md€ en 2027 ; 3,5 M de personnes | 1,8 Md€ ; 3,5 M | CR AN 14/10/2025 ; COR 2026 | — |
| K32 | écart avec l'Allemagne 0,5 → près de ×3 | 0,51 → 1,47 (×2,9) | BCE IRS | a18_10 |
| K33 | charge 72 Md€ = Défense | 72,93 contre 63,4 | DP Budget 2027 | a18_10 |
| K34 | 0,1 pt = 4 Md€ | 0,34 (an 1) / ≈ 1,9 (an 5) | PAP 117 p.22 | a18_10 |
| K35 | Suède 12 %, 1998, 2/3, 8 % et 12 %, 94 % | 10,7 % ; +0,8 % ; « almost two-thirds » ; 8,1 + 4,5 ; 94 % | OCDE, Eurostat, Persson 1995, Prop. 1997/98:150 | a18_05 |

### 1.5 Révisions intervenues depuis le 13 novembre 2026 (date du script)

Recherches menées le 20/11/2026 :

- **Eurostat.** Prélèvements obligatoires mis à jour le 05/11, comptes et notification le 21/10 : antérieurs au script, intégrés.
- **Insee.** Aucune nouvelle publication des comptes des APU trouvée entre le 13 et le 20/11. L'écart 152,5 / 151,6 Md€ pour 2025 vient de deux publications du printemps 2026.
- **PLFG 2026** (n° 3434, signé le 4/11/2026) : le déficit 2026 est maintenu à 5,4 %.
- **PLF 2027.** La première partie a été rejetée le 4/11, et le texte transmis au Sénat est le texte initial du gouvernement. Le « 5,9 % » (V5-B5-33) ne concerne donc qu'un texte rejeté. Ce n'est pas une révision, mais le chiffre est devenu sans objet.
- **Sénat, PLFSS 2027.** Votes rapportés par la presse les 13 et 18/11 [S] ; ils ne touchent aucun chiffre de la V5.
- **BCE.** La moyenne de novembre des taux à 10 ans n'est pas publiée le 20/11.
- **HCFP.** Je n'ai pas pu lister les avis postérieurs : archive web.archive.org « temporarily offline » lors de l'interrogation CDX.

Conclusion : **aucune révision postérieure au 13/11 qui invalide un chiffre de la V5 n'a été identifiée**. La recherche est incomplète pour le HCFP.

### 1.6 Affirmations non vérifiées (M2 « non vérifié » : 4)

- **V5-B2-07**, citation « Quoi qu'il en coûte » : pièce non recherchée.
- **V5-B5-40**, OAT au-dessus de 5 % le 22/10 : pas de série quotidienne officielle.
- **V5-B5-48**, « les interrogations sur la situation politique en France » : source introuvable.
- **V5-B6-02**, voyage de Persson à New York « peu après » octobre 1994 : date non établie, source secondaire seulement.

S'y ajoutent les 15 affirmations « non démontré ». Ce sont des jugements ou des causalités non testées, sans pièce possible : B1-10, B2-16, B3-09, B3-11, B3-34, B3-36, B4-05, B4-19, B5-28, B5-30, B5-39, B5-53, B6-29, B6-32, B6-36.

### 1.7 Ce qui n'a pas pu être vérifié à la source primaire

- Fillon 2007 : lu dans une reprise de la dépêche AFP [S].
- Anecdote de l'hôtel à New York : Reuters [S].
- Titre du rapport Pébereau : cité par l'AN et le Sénat [S], le PDF de vie-publique étant tronqué.
- Décret de dissolution de 2024 ; texte de la loi TEPA, article par article ; article de la LFSS 2026 sur la suspension (attestée par le COR) ; mot « cagnotte » ; date de mars 2000.
- Ampleur de la chute de la couronne en 1992.
- Cotisations du CAS Pensions de la Défense, qui permettraient de tester l'égalité « 72 Md€ ».

### 1.8 Tableaux détaillés par bloc

Colonnes : identifiant, ligne du script, affirmation, valeur du script, valeur trouvée, source (page) et provenance, verdict selon l'échelle initiale, verdict M2, niveau de preuve, motif. Les URL complètes sont dans le CSV.

### Bloc B1

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B1-01 | 5 | La France est le pays de l'UE qui prélève le plus d'impôts et de cotisations | rang 1 UE | 2025 : FR 46,0 % du PIB (1er), BE 44,7, DK 44,3 ; 2024 : BE 45,2 > FR 45,1 ; hors cotisations imputées 2025 : FR 44,3 vs DK 44,2 | Eurostat gov_10a_taxag (D2_D5_D91_D61_M_D995) (série S13_S212) [C] | exact sous condition | exact | A | Vrai pour 2025 ; faux pour 2024 (Belgique 1re) ; écart de 0,1 pt avec le Danemark hors cotisations imputées : affirmation fragile au millésime près |
| V5-B1-02 | 5 | en déficit depuis 51 ans | 51 ans | 51 exercices 1975-2025 en besoin de financement (solde < 0) | Insee, solde APU par sous-secteur, fig. 2 (Figure 2, ligne Ensemble) [C] | exact | exact | A | Aucun solde ≥ 0 entre 1975 et 2025 |
| V5-B1-03 | 7 | La dernière fois que nos comptes publics ont fini l'année en excédent, c'était en 1974 | 1974 | 1974 : +0,1 % du PIB (+0,199 Md€) ; excédents antérieurs 1958-1966, 1972 | Insee, solde APU par sous-secteur, fig. 1 et 2 (Figures 1-2) [C] | exact | exact | A |  |
| V5-B1-04 | 7 | Un excédent minuscule | minuscule | +0,1 % du PIB, 0,2 Md€ | Insee fig. 1-2 (Figures 1-2) [C] | exact | exact | A |  |
| V5-B1-05 | 7 | L'année suivante, la récession qui suit le premier choc pétrolier fait plonger les comptes | 1975 récession, plongée | PIB 1975 : -0,9 % (Eurostat) / -0,95 % (Insee base 2014) ; solde 1974 +0,1 → 1975 -2,9 % du PIB | Eurostat nama_10_gdp ; Insee BDM 010565708 ; Insee fig. 2 (-) [C] | exact sous condition | exact | A | Coïncidence datée exacte ; la part du plan de relance de 1975 dans la dégradation n'est pas isolée (cause plausible non isolée) |
| V5-B1-06 | 7 | Et depuis, chaque année, sans exception, ils sont dans le rouge. 51 années de suite | 51 | 51/51 | Insee fig. 2 (Figure 2) [C] | exact | exact | A |  |
| V5-B1-07 | 7 | Gauche, droite, centre : aucun gouvernement n'a ramené les comptes à l'équilibre. Pas une seule année | aucune année | aucun solde ≥ 0 de 1975 à 2025 | Insee fig. 2 (Figure 2) [C] | exact | exact | A | Vrai pour les APU (S13) ; le meilleur solde est -1,3 % en 2000 |
| V5-B1-08 | 9 | Le 4 novembre, les députés ont voté sur la partie recettes du budget 2027 | 4 novembre 2026 | Scrutin n° 9759 sur la première partie du PLF 2027 (1re lecture), 2e séance du mercredi 4 novembre 2026 | Assemblée nationale, scrutin 9759 (Synthèse du vote) [C] | exact | exact | A |  |
| V5-B1-09 | 9 | 458 voix contre. Zéro pour | 458 / 0 | 460 votants, 458 exprimés, 0 pour, 458 contre | AN scrutin 9759 (Synthèse du vote) [C] | exact | exact | A | Deux abstentions (460 votants) |
| V5-B1-10 | 9 | À force d'être modifié par chaque camp, le texte ne convenait plus à personne | motif du rejet | Explications de vote hétérogènes : rejet de principe (oppositions), « budget mosaïque » (LIOT), dégradation à 5,9 % (gouvernement, rapporteur) | Compte rendu de la 2e séance du 4/11/2026 (explications de vote) [C] | imprécis | non démontré | E | Motif collectif inféré ; certains groupes rejetaient aussi la version initiale |
| V5-B1-11 | 11 | Cette année, rien que les intérêts de notre dette coûtent plus de 1 100 euros par habitant | > 1 100 €/hab. | 2026 (prévision) : 79,2 Md€ / 69,1 M hab. = 1 146 € ; 2025 (réalisé) : 65,7 Md€ ≈ 953 € | HCFP avis 2026-5 §115 ; Insee Première 2087 ; Insee t_3201 ; calcul C-A18-003 (HCFP p.38 ; IP2087 p.1) [C] | exact sous condition | exact | D | Vrai sur la prévision 2026 des APU ; pas sur le réalisé 2025 (953 €) ni sur la seule charge de l'État |
| V5-B1-12 | 11 | Et aujourd'hui, la France emprunte plus cher que l'Italie | FR > IT | Taux de long terme (convergence) moyenne d'octobre 2026 : FR 4,89 %, IT 4,68 % ; sept. 4,44 vs 4,36 ; août 4,00 vs 3,99 | BCE, IRS mensuel M.FR / M.IT (TIME_PERIOD 2026-10) [C] | exact sous condition | exact | A | Vrai en moyenne mensuelle d'octobre ; donnée de novembre non disponible le 20/11/2026 |
| V5-B1-13 | 13 | Un pays riche. Qui prélève plus que tous ses voisins | plus que tous les voisins | 2025 : FR 46,0 ; BE 44,7 ; IT 43,0 ; autres voisins UE plus bas | Eurostat gov_10a_taxag (-) [C] | exact sous condition | exact | A | Vrai en 2025 ; faux en 2024 (Belgique) |
| V5-B1-14 | 13 | Et qui connaît son problème depuis des décennies | décennies | Rapport Pébereau 2005 (« Rompre avec la facilité de la dette publique ») ; déclaration Fillon 2007 | AN rapport n° 2844 (12e lég.) ; AFP 22/09/2007 (p.4) [C]/[S] | exact | exact | B |  |
| V5-B1-15 | 15 | une note interne de Bercy qui recommandait de ne pas communiquer un chiffre | note de Bercy | Note DG Trésor + DB du 7/12/2023 : 5,2 % au lieu de 4,9 %, « recommande de ne pas communiquer sur ce chiffre, encore entouré de nombreux aléas » | Sénat, rapport d'information n° 153 (2024-2025) (p.6) [C] rapport / [S] note | exact | exact | A | Note elle-même non consultée : lue via le Sénat |
| V5-B1-16 | 17 | un pays dont le déficit était deux fois plus profond que le nôtre | x 2 | Suède 1993 : -10,7 % (OCDE, millésime actuel) ; « 12 % au pire » (Reuters 2025) ; France 2025 : -5,1 % → rapport 2,1 (2,35 avec 12 %) | OCDE Perspectives économiques (SDMX DF_EO) ; Insee (NLGQ 1993) [C] | exact sous condition | exact | A | Comparaison 1993 (Suède) / 2025 (France) ; vrai quel que soit le millésime |
| V5-B1-17 | 17 | Il s'en est sorti en cinq ans | 1993 → 1998 | Solde suédois 1998 : +0,8 % (Eurostat, OCDE) ; « budget surplus for the first time in eight years » (programme de convergence 1998) | Eurostat gov_10a_main SE ; OCDE ; Gouvernement suédois (SWE98 p.11) [C] | exact | exact | A | Retour à l'excédent ; la dette restait élevée |

### Bloc B2

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B2-01 | 25 | 152 milliards d'euros. C'est ce qui a manqué à la France l'an dernier | 152 Md€ | 2025 : 151,6 Md€ (tableau 3.201 et fig. 1 sous-secteurs, comptes de mai 2026) ; 152,5 Md€ (Insee Première 2106, fig. 3) | Insee t_3201 ; Insee IP2106 (B9NF 2025 ; fig. 3) [C] | exact | exact | A | Écart de 0,9 Md€ entre deux publications Insee de 2026 (révision) ; 152 reste l'arrondi correct |
| V5-B2-02 | 25 | Sur 100 euros dépensés par l'État, la Sécurité sociale et les collectivités, 9 ont été empruntés | 9 / 100 | 151,6 / 1 714,1 = 8,8 % | Insee t_3201 ; calcul C-A18-001 (Total des dépenses / B9NF) [C] | exact | exact | A |  |
| V5-B2-03 | 25 | Plus de 400 millions d'euros. Chaque jour | > 400 M€/jour | 415 M€/jour (418 avec IP2106) | Insee ; calcul C-A18-002 (-) [C] | exact | exact | A |  |
| V5-B2-04 | 27 | 1975 : la récession après le choc pétrolier | récession 1975 | PIB -0,9 % | Eurostat nama_10_gdp (-) [C] | exact | exact | A |  |
| V5-B2-05 | 27 | 1993 : une autre récession | récession 1993 | PIB -0,4 % | Eurostat nama_10_gdp (-) [C] | exact | exact | A |  |
| V5-B2-06 | 27 | 2009 : la crise financière | 2009 | PIB -2,8 % ; solde -7,4 % | Eurostat ; Insee (-) [C] | exact | exact | A |  |
| V5-B2-07 | 27 | 2020 : le Covid. « Quoi qu'il en coûte » | citation | Formule non relue dans une pièce primaire pendant la mission | - (-) [X] non recherchée faute de temps ; [M] allocution du 12/03/2020 | non vérifiable à ce jour | non vérifié | - | Citation non attribuée dans la V5 ; aucune pièce consultée |
| V5-B2-08 | 27 | 207 milliards de déficit en une seule année, le record | 207 Md€, record | 2020 : 207,1 Md€ ; record en Md€ courants et en % du PIB (8,9 %) | Insee fig. 1 et 2 (Figures 1-2) [C] | exact | exact | A | Record en euros courants ; en % du PIB aussi (8,9 % > 7,4 % en 2009) |
| V5-B2-09 | 29 | En 2000, la croissance dépasse 4 % | > 4 % | +4,1 % | Eurostat nama_10_gdp (-) [C] | exact | exact | A | Chiffre sensible au millésime (base 2020) |
| V5-B2-10 | 29 | Les impôts rentrent tellement mieux que prévu qu'on parle d'une « cagnotte » | surplus, « cagnotte » | Surplus de recettes 51,4 MdF (35,6 MdF fiscales + 15,4 non fiscales) dans le PLFR 2000 | Sénat, rapport sur le PLFR 2000 (l99-371) (exposé général) [C] | exact sous condition | exact | A | Le surplus est attesté ; le mot « cagnotte » n'apparaît pas dans la pièce lue ; 15,4 MdF sont des recettes non fiscales reportées, pas des impôts |
| V5-B2-11 | 29 | La courbe remonte… et s'arrête sous la ligne | solde < 0 | 2000 : -1,3 % (meilleur solde de 1975-2025) | Insee IP2106 fig. 2 (Figure 2) [C] | exact | exact | A |  |
| V5-B2-12 | 31 | Même chose en 2018 | 2018 < 0 | 2018 : -2,3 % | Eurostat edpt1 ; Insee (-) [C] | exact | exact | A |  |
| V5-B2-13 | 31 | Et l'an dernier, sans aucune crise, il manquait encore l'équivalent de 5 % de toute la richesse produite | 5 % | -5,1 % ; PIB 2025 +0,8 % | Insee IP2106 fig. 1 ; Eurostat (Figure 1) [C] | exact | exact | A |  |
| V5-B2-14 | 33 | Un État n'a pas besoin d'être à zéro : il peut rester en déficit tant que sa dette grossit moins vite que son économie | condition | Identité : le ratio dette/PIB baisse si la dette croît moins vite que le PIB nominal | 04_PREUVES_ET_CALCULS.md §IV ; identité (-) [C] | exact | exact | A | Identité comptable correcte (PIB nominal) |
| V5-B2-15 | 33 | l'an dernier, notre dette a grossi plus de deux fois plus vite que notre économie | > x 2 | Dette +4,66 % (3 306,1 → 3 460,5 Md€) ; PIB nominal implicite +1,85 % ; rapport 2,5 | Insee IP2106 fig. 5 ; série longue ; script a18_02 (Figure 5) [C] | exact | exact | A |  |
| V5-B2-16 | 35 | Le trou n'est pas un accident. Il est dans la machine elle-même | thèse | Énoncé de jugement ; aucun test | - (-) [C] | non vérifiable à ce jour | non démontré | F | Jugement présenté comme conclusion (catégorie « jugement ») |

### Bloc B3

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B3-01 | 41 | Cette année-là [1974], nos dépenses publiques et nos recettes pèsent chacune 41 % de la richesse produite. Elles s'équilibrent | 41 % / 41 % | Dépenses 41,3 % ; recettes 41,4 % | Insee série longue dépenses-recettes (ligne Dépenses / Recettes) [C] | exact | exact | A |  |
| V5-B3-02 | 41 | Aujourd'hui, les recettes sont à 52 % | 52 % | 2025 : 52,2 % | Insee série longue ; IP2106 (-) [C] | exact | exact | A |  |
| V5-B3-03 | 41 | Mais les dépenses, elles, sont à 57 % | 57 % | 2025 : 57,3 % | Insee (-) [C] | exact | exact | A |  |
| V5-B3-04 | 41 | En 51 ans, les recettes ont pris 11 points. Les dépenses, 16 | +11 / +16 | +10,8 / +16,0 points (1974 → 2025) | Insee ; script a18_02 (-) [C] | exact | exact | A |  |
| V5-B3-05 | 41 | Le trou d'aujourd'hui, c'est cette différence | 16 - 11 = 5 | 16,0 - 10,8 = 5,2 ≈ déficit 5,1 | identité (-) [C] | exact | exact | A | Identité comptable (1974 équilibré), pas une explication causale |
| V5-B3-06 | 43 | presque toute cette hausse des dépenses s'est faite en vingt ans : dès 1993, elles sont déjà à 56 % | 56 % en 1993 | 1993 : 56,5 % ; 95 % de la hausse 1974-2025 acquise en 1993 ; mais 1990 : 51,6 % | Insee série longue (-) [C] | exact sous condition | exact | A | 1993 est une année de récession (pic conjoncturel du ratio) ; avant la récession (1990) le ratio était de 51,6 % |
| V5-B3-07 | 43 | Depuis trente ans, elles tournent autour de ce niveau | ≈ 56 % | Moyenne 1994-2025 : 56,2 % ; min 52,6 (2000) ; max 61,7 (2020) | Insee ; script a18_02 (-) [C] | exact sous condition | exact | A | Amplitude de 9 points autour de la moyenne |
| V5-B3-08 | 45 | En 1974, la France sort de quinze ans de croissance à plus de 5 % par an | > 5 %/an | 1960-1974 : 5,7 %/an (moyenne géométrique) | Insee BDM 010565708 (PIB trimestriel volume, base 2014, série arrêtée) ; script a18_09 (-) [C] | exact | exact | A |  |
| V5-B3-09 | 45 | Ses retraites, sa santé, ses allocations ont été bâties sur ce rythme | causalité historique | Aucune pièce consultée | - (-) [C] | non vérifiable à ce jour | non démontré | F | Interprétation historique non étayée dans la V5 |
| V5-B3-10 | 45 | Puis vient le choc pétrolier : la croissance tombe autour de 2 % | ≈ 2 % | 1975-1985 : 2,2 %/an (Eurostat et Insee) | Eurostat ; Insee ; script a18_09 (-) [C] | exact | exact | A |  |
| V5-B3-11 | 45 | Les droits, eux, continuent sur leur lancée | causalité | Aucune mesure des « droits » dans la V5 ni dans les pièces consultées | - (-) [C] | non vérifiable à ce jour | non démontré | F |  |
| V5-B3-12 | 45 | Le chômage de masse s'installe | chômage de masse | Taux de chômage 1974 : 2,5 % → 1985 : 9,1 % | OCDE Perspectives économiques (UNR) (-) [C] | exact | exact | A |  |
| V5-B3-13 | 45 | En 1982, on décide la retraite à 60 ans | 1982 | Ordonnance n° 82-270 du 26 mars 1982 relative à l'abaissement de l'âge de la retraite | Légifrance (capture archive.org 04/04/2023) (-) [C] | exact | exact | A | Entrée en vigueur au 1er avril 1983 (non relue dans la pièce) |
| V5-B3-14 | 45 | Pendant dix ans, on monte les impôts et les cotisations pour suivre | hausse 1974-1985 | Recettes totales 41,4 % (1974) → 51,2 % (1985) : +9,7 points | Insee série longue (-) [C] | exact sous condition | exact | A | Mesuré en recettes totales, non en prélèvements obligatoires ; « pour suivre » est une interprétation |
| V5-B3-15 | 45 | Vers 1985, ils plafonnent : en quarante ans, les recettes n'ont pris qu'un point de plus. Les dépenses, trois | +1 / +3 | 1985 → 2025 : recettes +1,1 point (51,2 → 52,2) ; dépenses +3,1 (54,2 → 57,3) ; recettes entre 49,1 (1989) et 54,3 (2017) | Insee série longue (-) [C] | exact sous condition | exact | A | Comparaison de deux points : les recettes ont varié de 5 points entre-temps (« plafonnent » à nuancer) |
| V5-B3-16 | 45 | en 1993, la moitié du trou, ce sont déjà les intérêts des trous d'avant | 50 % | Intérêts D41 consolidés 36,6 Md€ / besoin de financement 72,6 Md€ = 50,4 % ; intérêts nets des intérêts reçus : 42 % | Insee t_3201 ; script a18_03 (lignes D41 et B9NF, 1993) [C] | exact sous condition | exact | A | Vrai en intérêts bruts versés ; 42 % en intérêts nets |
| V5-B3-17 | 49 | Premier arrêt : la retraite. 24 euros. Un sur quatre | 24 % | COR : dépenses de retraite 422 Md€ = 24,3 % des dépenses publiques en 2025 ; COFOG vieillesse (GF1002) 2024 : 23,4 % | COR, rapport annuel juin 2026 ; Eurostat COFOG (COR p.11 et p.67) [C] | exact | exact | A |  |
| V5-B3-18 | 49 | la santé ... Puis les allocations ... À elles trois, plus de la moitié de la dépense | > 50 % | Protection sociale (GF10) 41,4 % + santé (GF07) 15,5 % = 56,9 % de la dépense 2024 | Eurostat gov_10a_exp ; script a18_05 (-) [C] | exact | exact | A |  |
| V5-B3-19 | 49 | L'école, l'armée, la police, la justice, les routes et les ministères se partagent le reste | reste | Le reste (43 %) comprend aussi : affaires économiques 9,9 % (subventions, transports), intérêts 3,5 %, logement-environnement, culture | Eurostat COFOG 2024 (-) [C] | imprécis | trop général | A | Énumération incomplète : les intérêts et les aides économiques sont omis |
| V5-B3-20 | 49 | Le cœur de la dépense, ce n'est pas le train de vie de l'État. C'est la protection sociale | protection sociale | GF10 = 41,4 % ; GF10 + GF07 = 56,9 % | Eurostat COFOG 2024 (-) [C] | exact | exact | A |  |
| V5-B3-21 | 51 | L'an dernier, la France a dépensé 7 points et demi de richesse de plus que cette moyenne [zone euro] | 7,5 pts | 2025 : 57,3 vs 49,8 (ZE20 y compris la France) = 7,5 ; vs ZE hors France : 9,3 | Eurostat gov_10a_main ; script a18_05 (-) [C] | exact sous condition | exact | A | Moyenne incluant la France (poids ≈ 18 %) ; hors France l'écart est 9,3 points |
| V5-B3-22 | 51 | Près des deux tiers de cet écart, c'est la protection sociale et la santé, et d'abord la vieillesse | ≈ 2/3 | COFOG 2024 : (GF10+GF07) 5,2 / 8,1 = 64 % (65 % vs ZE hors France) ; vieillesse +2,5 pts, premier poste | Eurostat gov_10a_exp (-) [C] | trompeur par périmètre ou juxtaposition | exact | A | Part juste mais calculée sur l'écart COFOG 2024 (8,1 pts, total 57,3) alors que « cet écart » désigne l'écart 2025 (7,5) ; la conclusion ne change pas |
| V5-B3-23 | 51 | Elle a prélevé plus aussi : un peu plus de 5 points | > 5 pts | Recettes totales 52,2 vs 46,8 = 5,4 ; prélèvements obligatoires 46,0 vs 41,3 = 4,7 | Eurostat gov_10a_main ; gov_10a_taxag (-) [C] | exact sous condition | exact | A | Vrai en recettes totales ; en prélèvements obligatoires l'écart est sous 5 points |
| V5-B3-24 | 51 | Les 2 points qui manquent, c'est exactement l'écart entre notre déficit et celui de la zone euro | 2 pts | Solde FR -5,1 vs ZE -3,0 = 2,1 | Eurostat ; identité (-) [C] | exact | exact | A | Identité comptable |
| V5-B3-25 | 53 | En 2002, il y avait 2,1 cotisants pour un retraité | 2,1 | 2,1 en 2002 | COR RA 2026 (p.74) [C] | exact | exact | A |  |
| V5-B3-26 | 53 | Les enfants du baby-boom sont arrivés à la retraite | cause | « en particulier sous l'effet du vieillissement des générations du baby-boom » | COR RA 2026 (p.74) [C] | exact | exact | A |  |
| V5-B3-27 | 53 | Aujourd'hui, on n'en est plus qu'à 1,8 | 1,8 | 1,8 en 2025 | COR RA 2026 (p.74) [C] | exact | exact | A |  |
| V5-B3-28 | 53 | En 2070, d'après le COR, environ 1,3 | 1,3 | 1,3 dans le scénario de référence | COR RA 2026 (p.74) [C] | exact | exact | D | Projection |
| V5-B3-29 | 53 | Si tu as trente ans aujourd'hui, c'est pendant ta retraite qu'on en sera là | horizon | Né en 1996 : départ vers 2060-2063 ; ratio 1,3 donné pour 2070 | COR RA 2026 (âge moyen 64,6 ans après 2040) (p.13) [C] | exact sous condition | exact | D | Approximation acceptable |
| V5-B3-30 | 55 | D'après la Cour des comptes, les baisses d'impôts décidées depuis 2018 coûtaient 62 milliards en 2023, sans économies en face | 62 Md€ ; non compensées | « impact estimé à 62 Md€ en 2023, soit 2,2 pts de PIB » ; « Ces baisses de prélèvements, non compensées par des économies en dépenses » | Cour des comptes, situation et perspectives des finances publiques, juillet 2024 (via vie-publique.fr, capture archive.org) (p.35-36) [C] | exact | exact | A | Pièce de la Cour lue via un tiers (vie-publique, archive) |
| V5-B3-31 | 55 | Baisser les impôts sans baisser les dépenses, c'est emprunter la différence | identité | Identité comptable toutes choses égales | - (-) [C] | exact | exact | A | Identité ; ignore l'effet sur l'assiette |
| V5-B3-32 | 57 | Tout combler par l'impôt, ce serait 150 milliards de prélèvements en plus : aucun pays de l'Union ne prélève autant | 51 % du PIB | 46,0 + 5,1 = 51,1 % ; maximum ailleurs : BE 44,7 % | Eurostat taxag ; calcul C-A18-017 (-) [C] | exact sous condition | exact | A | Calcul statique, sans effet de comportement ni de croissance |
| V5-B3-33 | 57 | Tout combler par la dépense nous laisserait encore au-dessus de la moyenne de la zone euro | 52 > 50 | 57,3 - 5,1 = 52,2 % vs 49,8 % | Eurostat gov_10a_main ; C-A18-018 (-) [C] | exact sous condition | exact | A | Statique |
| V5-B3-34 | 57 | Avec les prélèvements les plus élevés de l'Union, la France ne refermera pas son déficit sans toucher à la dépense | conclusion | Prescription ; dépend d'hypothèses non exposées (élasticités, croissance) | - (-) [C] | non vérifiable à ce jour | non démontré | F | Jugement présenté comme conséquence logique |
| V5-B3-35 | 59 | Or elle monte par marches | marches | Dette/PIB : 65,5 (2007) → 91,7 (2012) → 98,2 (2019) → 114,9 (2020) → 109,5 (2023) → 115,7 (2025) | Insee série longue (ligne dette brute) [C] | exact | exact | A |  |
| V5-B3-36 | 59 | Si c'était seulement ça [un modèle trop cher], elle monterait doucement, régulièrement | contrefactuel | Contrefactuel non testé | - (-) [C] | non vérifiable à ce jour | non démontré | F | Un déficit structurel combiné à des récessions produit aussi des marches |
| V5-B3-37 | 59 | Comme si, à chaque crise, quelque chose l'empêchait de redescendre | ne redescend pas | Le ratio a baissé : 62,1 (1998) → 59,3 (2001) ; 68,2 (2005) → 65,4 (2006) ; 114,9 (2020) → 109,5 (2023), sans revenir au niveau d'avant crise | Insee série longue (-) [C] | imprécis | trop général | A | Il redescend en partie après chaque crise, jamais jusqu'au point de départ |

### Bloc B4

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B4-01 | 65 | « Je suis à la tête d'un État qui est en situation de faillite sur le plan financier. » | citation | Mot pour mot dans la dépêche AFP du 22/09/2007 : « Je suis à la tête d'un Etat qui est en situation de faillite sur le plan financier, (…) » | Dépêche AFP reprise par WMC (22/09/2007) (-) [S] AFP | exact sous condition | exact | E | Lue via une reprise de dépêche ; aucun enregistrement ni texte officiel consulté |
| V5-B4-02 | 65 | Septembre 2007. C'est le Premier ministre qui parle | sept. 2007, PM | « a déclaré vendredi en Corse le chef du gouvernement » (vendredi 21/09/2007) | AFP via WMC (-) [S] AFP | exact | exact | E |  |
| V5-B4-03 | 65 | À ce moment-là, notre dette représente 8 mois de toute la production du pays | 8 mois | 2007 : 65,5 % du PIB = 7,9 mois (64,2 % selon l'AFP en 2007) | Insee série longue ; C-A18-004 (-) [C] | exact | exact | A |  |
| V5-B4-04 | 65 | Aujourd'hui : près de 14 | ≈ 14 mois | 2025 : 115,7 % = 13,9 mois | Insee ; C-A18-004 (-) [C] | exact | exact | A |  |
| V5-B4-05 | 67 | Notre dette fonctionne comme ça [une clé à cliquet] | mécanisme | Métaphore d'un mécanisme non testé | - (-) [C] | non vérifiable à ce jour | non démontré | F | Cause plausible non isolée |
| V5-B4-06 | 69 | 2008 : la crise financière. Les recettes chutent, l'État lance un plan de relance | recettes en baisse | Recettes APU 1 010,5 Md€ (2008) → 979,8 (2009), -3 % ; plan de relance non relu dans une pièce | Insee t_3201 (Total des recettes) [C] | exact sous condition | exact | A | Plan de relance non vérifié dans une pièce |
| V5-B4-07 | 69 | En cinq ans, la dette gagne l'équivalent de trois mois de production | +3 mois | 2007 → 2012 : 65,5 → 91,7 % = +3,1 mois | Insee ; C-A18-004 (-) [C] | exact | exact | A |  |
| V5-B4-08 | 69 | La dette ne redescend pas : de 2012 à 2019, sans récession, elle continue même de monter un peu | hausse | 91,7 → 98,2 % (+0,8 mois) ; croissance positive chaque année 2012-2019 (0,2 à 2,1 %) | Insee ; Eurostat (-) [C] | exact | exact | A |  |
| V5-B4-09 | 71 | 2020 : le Covid ... La dette prend encore deux mois de production | +2 mois | 98,2 → 114,9 % = +2,0 mois | Insee (-) [C] | exact | exact | A |  |
| V5-B4-10 | 71 | Puis viennent les boucliers sur l'énergie : 36 milliards nets de 2021 à 2024 | 36 Md€ nets | « besoin de financement net de l'État atteignant 36 Md€ sur les années 2021 à 2024 » ; « de plus de 36 Md€ » | Cour des comptes, Les mesures exceptionnelles de lutte contre la hausse des prix de l'énergie, mars 2024 (via vie-publique, capture archive.org) (p.9 et p.86-87) [C] | exact sous condition | exact | A | Coût net pour l'État seul ; 2024 estimé en mars 2024 |
| V5-B4-11 | 71 | des aides « sans ciblage particulier », note la Cour des comptes | citation | « boucliers et remises – qui soutiennent les consommations d'énergie des ménages sans ciblage particulier ni limite en volumes » ; la Cour ajoute que c'est « nettement moins » critiquable pour l'électricité | Cour des comptes, mars 2024 (p.9 et p.112) [C] | exact sous condition | exact | A | Citation exacte mais tronquée ; nuance de la Cour sur l'électricité omise |
| V5-B4-12 | 75 | En mars [2000], le gouvernement chiffre le surplus de recettes à 50 milliards de francs | 50 MdF, mars | PLFR 2000 : 51,4 MdF de surplus (35,6 fiscales + 15,4 non fiscales reportées) | Sénat, rapport sur le PLFR 2000 (exposé général) [C] | exact sous condition | exact | A | Montant exact à l'arrondi ; le mois de mars n'est pas confirmé par la pièce lue |
| V5-B4-13 | 75 | Une partie sert à baisser les impôts : la TVA perd un point | TVA -1 pt | Article 2 du PLFR 2000 : baisse d'un point du taux normal ; 40,6 MdF (80 %) en baisses d'impôts, 10 MdF en dépenses, 49 MF de baisse du déficit | Sénat, rapport PLFR 2000 (art. 2 et exposé) [C] | exact sous condition | exact | A | « Une partie » minore : 80 % du surplus va aux baisses d'impôts, le reste à des dépenses |
| V5-B4-14 | 75 | Ça n'aurait pas suffi à refermer le trou | insuffisant | 51,4 MdF = 7,8 Md€ ≈ 0,5 % du PIB, pour un déficit 2000 de 1,3 % du PIB | Sénat ; Insee ; C-A18-013 (-) [C] | exact | exact | A |  |
| V5-B4-15 | 75 | Le déficit, lui, reste là | inchangé | Baisse du déficit prévue par le PLFR : 49 MF | Sénat, rapport PLFR 2000 (-) [C] | exact | exact | A |  |
| V5-B4-16 | 77 | Août 2007. Une nouvelle majorité, et sa loi phare de l'été baisse plusieurs impôts | août 2007 | Loi n° 2007-1223 du 21 août 2007 en faveur du travail, de l'emploi et du pouvoir d'achat (JO du 22/08/2007) | Sénat, dossier législatif pjl06-390 (-) [C] | exact sous condition | exact | A | Contenu fiscal de la loi non relu article par article |
| V5-B4-17 | 77 | Un mois plus tard, c'est son Premier ministre qui parle de faillite | 1 mois | 21/08/2007 → 21/09/2007 | Sénat ; AFP (-) [C] | exact | exact | A |  |
| V5-B4-18 | 79 | Deux majorités opposées, le même réflexe | généralisation | Deux cas (2000, 2007) | - (-) [C] | imprécis | trop général | F | Généralisation à partir de deux cas |
| V5-B4-19 | 79 | retirer une aide, c'est la reprendre à quelqu'un ... Alors l'aide dure, la baisse reste | mécanisme | Mécanisme d'économie politique non testé ; contre-exemples dans la V5 elle-même (fin des boucliers) | - (-) [C] | non vérifiable à ce jour | non démontré | F |  |
| V5-B4-20 | 79 | Et même quand l'aide finit par s'arrêter, la dette qui l'a payée, elle, ne repart pas | stock | Identité : la dette ne baisse qu'avec des excédents | - (-) [C] | exact | exact | A | Identité comptable |
| V5-B4-21 | 81 | De 2014 à 2019, [l'Allemagne] dégage un excédent chaque année. Six années de suite | 6 ans | Excédents 2014-2019 (0,7 à 1,9 %) ; déjà +0,1 % en 2013 : sept années de suite | Eurostat gov_10dd_edpt1 (B9 DE) [C] | exact sous condition | exact | A | La série excédentaire commence en 2013 |
| V5-B4-22 | 81 | Sa dette passe de près de 10 mois de production à 7 | ≈10 → 7 | Fin 2013 : 77,4 % = 9,3 mois ; fin 2014 : 74,4 % = 8,9 ; 2019 : 58,3 % = 7,0 | Eurostat edpt1 ; C-A18-005 (GD DE) [C] | imprécis | inexact | A | « Près de 10 » surestime (9,3 ou 8,9 selon le point de départ) |
| V5-B4-23 | 81 | La France, sur ces six années ? Pas un seul excédent | 0 | Soldes FR 2014-2019 : -4,6 à -2,3 % | Eurostat edpt1 (B9 FR) [C] | exact | exact | A |  |
| V5-B4-24 | 81 | un frein à l'endettement inscrit dans sa Constitution en 2009 | 2009 | Bundesrat : approbation de la révision de la Loi fondamentale le 12 juin 2009 | Bundeszentrale für politische Bildung, 11/06/2019 (-) [C] | exact | exact | B |  |
| V5-B4-25 | 81 | et elle a profité de taux très bas | taux bas | Taux à 10 ans DE : 1,76 % (janv. 2014) ; -0,15 % (juil. 2016) ; -0,65 % (août 2019) | BCE IRS M.DE (-) [C] | exact | exact | A |  |
| V5-B4-26 | 81 | des économistes allemands lui reprochent des investissements repoussés | critique | Débat publié : « Schuldenbremse – Investitionshemmnis oder Vorbild für Europa? » (Wirtschaftsdienst, 2019) | Wirtschaftsdienst 2019 (Fuest et al.) (p.1 (307)) [C] | exact sous condition | exact | C | Débat contradictoire, pas un consensus |
| V5-B4-27 | 81 | et en 2025, l'Allemagne l'a assoupli | 2025 | Réforme du frein à l'endettement par révision constitutionnelle votée le 18 mars 2025 (défense, fonds spécial de 500 Md€, Länder) | bpb, 28/03/2025 (-) [C] | exact | exact | B |  |
| V5-B4-28 | 83 | Chez nous, la roue avance à chaque crise et ne revient jamais à son point de départ | jamais | Le ratio n'est jamais revenu au niveau d'avant crise (1993, 2008, 2020) | Insee série longue (-) [C] | exact | exact | A |  |
| V5-B4-29 | 83 | Décembre 2023 : une loi promet un déficit ramené à 2,7 % en 2027 | 2,7 % en 2027 | LPFP 2023-2027 promulguée le 18/12/2023 ; cible 2027 : 2,7 % | Sénat r24-153 (p.5) ; Cour des comptes juillet 2024 (p.109) (p.5 ; p.109) [C] | exact | exact | A |  |
| V5-B4-30 | 83 | Le budget 2027 vise… 5 % | 5 % | PLF 2027 : solde public -5,0 % en 2027 ; « 5 % du produit intérieur brut avec la version initiale » | HCFP avis 2026-5 tableau 12 ; CR AN 4/11/2026 (M. Amiel) (HCFP p.29) [C] | exact | exact | A |  |
| V5-B4-31 | 85 | Le 7 décembre 2023, une note interne alerte : le déficit de l'année ne serait pas de 4,9 %, comme prévu, mais de 5,2 | 4,9 → 5,2 | Note DG Trésor + DB du 7/12/2023 : 5,2 % « contre 4,9 % prévus » | Sénat r24-153 (p.6) [C] rapport / [S] note | exact | exact | A | Note lue via le Sénat |
| V5-B4-32 | 85 | Elle recommande de ne pas communiquer sur ce chiffre, encore trop incertain | citation paraphrasée | « recommande de ne pas communiquer sur ce chiffre, encore entouré de nombreux aléas » | Sénat r24-153 (p.6) [C] | exact | exact | A |  |
| V5-B4-33 | 85 | Le Parlement, qui vote alors le budget suivant, n'en est pas informé | non informé | « aucune information n'a à l'époque été donnée ni au Parlement, ni aux Français » | Sénat r24-153 (p.6) [C] | exact | exact | A |  |
| V5-B4-34 | 85 | Onze jours plus tard, la loi des 2,7 %, votée en novembre sur les anciens chiffres, est promulguée telle quelle | 11 jours ; votée en novembre | Promulgation 18/12/2023 (11 jours) ; adoption en lecture définitive par engagement de responsabilité (art. 49.3), Conseil constitutionnel saisi le 16/11/2023, décision 2023-857 DC du 14/12/2023 | Sénat r24-153 ; Conseil constitutionnel (p.5 ; § 6) [C] | imprécis | inexact | A | Texte adopté sans vote sur le fond (49.3) avant le 16 novembre ; « votée » est impropre |
| V5-B4-35 | 85 | C'est le Sénat qui a tout reconstitué | Sénat | Mission d'information de la commission des finances du Sénat (rapport n° 153, 2024-2025) | Sénat r24-153 (-) [C] | exact sous condition | exact | A | D'autres enquêtes parlementaires existent (AN) ; « tout » est un raccourci |
| V5-B4-36 | 85 | Le ministre de l'époque a répondu que cette note ne justifiait pas de corriger le budget | réponse | B. Le Maire et T. Cazenave : « aucun ajustement sur le PLF 2024 ne pouvait être envisagé sur la base de la note du 7 décembre 2023 » | Sénat r24-153 (p.6 et p.65) [C] | exact | exact | A | Deux ministres ; le Sénat juge l'argument « factuellement faux » pour 2024 |
| V5-B4-37 | 85 | Au final, ce sera pire que la note : 5,4 % | 5,4 % | Solde 2023 : -5,4 % (base 2020 actuelle ; 5,5 % à la première publication de mars 2024) | Insee IP2106 fig. 1 (Figure 1) [C] | exact | exact | A | Chiffre révisé depuis la première estimation |
| V5-B4-38 | 87 | Aujourd'hui, la promesse a seulement changé de date : repasser sous les 3 % en 2029 | 3 % en 2029 | « Le Gouvernement a indiqué qu'au-delà de 2027, il est toujours prévu de ramener le déficit sous 3 % du PIB en 2029 » | HCFP avis 2026-5 ; RESF PLF 2027 p.105 (HCFP p.3) [C] | exact | exact | A |  |
| V5-B4-39 | 87 | Pour le HCFP, cet objectif « semble peu plausible » | citation | Avis 2026-5 : « rendent très peu vraisemblable sa concrétisation, sauf évolutions conjoncturelles très favorables » ; « peu plausible » absent de l'avis | HCFP avis n° 2026-5 (PLF et PLFSS 2027), via archive.org (p.3) [C] | imprécis | inexact | A | Citation non conforme à l'avis sur le budget 2027 (sens proche, plus sévère) ; autres avis 2026 non consultés (archive HCFP hors service) |
| V5-B4-40 | 89 | Dès 2005, un rapport remis au gouvernement s'intitulait déjà : « Rompre avec la facilité de la dette publique » | titre 2005 | Commission présidée par Michel Pébereau, « Rompre avec la facilité de la dette publique. Pour des finances publiques au service de notre croissance économique et de notre cohésion sociale », La Documentation française, 2005 | AN rapport n° 2844 (12e législature) ; Sénat r05-345 (AN p.4) [S] | exact | exact | B | Rapport lui-même non téléchargé (PDF tronqué) |

### Bloc B5

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B5-01 | 99 | Mars 2023. Le gouvernement veut repousser l'âge de la retraite de 62 à 64 ans | 62 → 64 | Âge légal de 62 à 64 ans à partir du 1er septembre 2023 | Cour des comptes, retraites, février 2025 ; CR AN 20/03/2023 (p.58) [C] | exact | exact | A |  |
| V5-B5-02 | 99 | La retraite : ... le poste le plus lourd de la dépense publique | 1er poste | Vieillesse (GF1002) 23,4 % de la dépense 2024, premier groupe COFOG | Eurostat COFOG ; COR (-) [C] | exact | exact | A |  |
| V5-B5-03 | 101 | Dès septembre, ceux qui comptaient partir à l'automne doivent attendre | sept. 2023 | Entrée en vigueur au 1er septembre 2023 | Cour des comptes, février 2025 (p.58) [C] | exact | exact | A |  |
| V5-B5-04 | 101 | D'après la Cour des comptes, la réforme commence même par coûter, à cause des mesures qui l'accompagnent | surcoût initial | « se traduit d'abord par un surcoût en 2024 en raison des mesures d'accompagnement de la réforme » | Cour des comptes, février 2025 (p.25) [C] | exact | exact | A |  |
| V5-B5-05 | 101 | Son gain n'atteint une dizaine de milliards par an qu'en 2030 | ≈10 Md€ en 2030 | « estimés autour de 10 Md€, à horizon 2030 » (système de retraite) ; + 8 à 14 Md€ pour les autres APU | Cour des comptes, février 2025 (p.10) [C] | exact sous condition | exact | A | Périmètre retraite seul ; effet sur l'ensemble des APU plus large |
| V5-B5-06 | 101 | Le bénéfice plein, sept ans plus tard. Après la prochaine élection | 2030 | Effet maximal sur le nombre de retraités en 2032 selon la Cour | Cour des comptes, février 2025 (p.10) [C] | exact sous condition | exact | A | « Plein » approximatif (pic en 2032) |
| V5-B5-07 | 103 | la Première ministre fait passer la réforme sans vote, avec le 49.3 | 49.3 | « en annonçant votre onzième 49.3 sur cette réforme des retraites » (jeudi 16/03/2023) | CR AN 20/03/2023 (-) [C] | exact | exact | A | Le motif « faute d'être sûre d'avoir les voix » n'est pas vérifié |
| V5-B5-08 | 103 | Quatre jours plus tard, son gouvernement échappe à la censure. À neuf voix | 9 voix | 20/03/2023 : majorité requise 287, pour 278 → 9 voix ; scrutin n° 1240 | CR AN 20/03/2023 ; scrutin 16/1240 (-) [C] | exact | exact | A |  |
| V5-B5-09 | 105 | Un an plus tard, en juin 2024, l'Assemblée est dissoute | juin 2024 | Dissolution de juin 2024 évoquée par le Sénat (« le pari de la dissolution ») ; décret non consulté | Sénat r24-153 (p.3) [C] | exact sous condition | exact | B | 15 mois après mars 2023 ; décret non relu |
| V5-B5-10 | 105 | Depuis, aucun camp n'a la majorité | pas de majorité | « sans majorité absolue » (Premier ministre, 14/10/2025) ; motions et votes 2024-2026 | CR AN 14/10/2025 (-) [C] | exact sous condition | exact | B | Répartition des sièges non relue |
| V5-B5-11 | 109 | Michel Barnier, passe en force : 49.3 sur un budget de la Sécurité sociale qui réduit et retarde la hausse des pensions | 49.3 PLFSS ; pensions | Engagement de responsabilité sur l'ensemble du PLFSS 2025 (CMP) ; motion : « désindexation partielle et différée des pensions de retraites » | AN scrutin 519 ; motion LFI du 2/12/2024 (-) [C] | exact | exact | A |  |
| V5-B5-12 | 109 | Le 4 décembre 2024, des députés que tout oppose votent la même motion de censure | 4/12/2024 | Scrutin 519 : 331 voix pour, motion adoptée (NFP et RN) | AN scrutin 519 (-) [C] | exact | exact | A |  |
| V5-B5-13 | 109 | elle lui reproche, entre autres, de faire payer les retraités | retraités | « taxation des retraités par la désindexation partielle et différée des pensions » | Motion de censure du 2/12/2024 (p.1) [C] | exact | exact | A |  |
| V5-B5-14 | 109 | Pour la première fois depuis 1962, les députés renversent un gouvernement | 1962 | « le seul premier ministre à être censuré depuis Georges Pompidou en 1962 » ; motion du 5 octobre 1962 | CR AN 4/12/2024 (-) [C] | exact | exact | A |  |
| V5-B5-15 | 111 | Son plan : près de 44 milliards d'euros d'effort | ≈44 Md€ | « Effort total 43,8 milliards d'euros en intégrant l'objectif de la loi de programmation militaire actualisée » | Gouvernement, dossier de presse « Le moment de vérité », 15/07/2025 (p.3) [C] | exact sous condition | exact | B | L'effort inclut le financement de la hausse militaire |
| V5-B5-16 | 111 | dont une « année blanche » où les pensions et les allocations ne suivent plus les prix | année blanche | « En 2026, année blanche (7,1 milliards d'euros) » ; prestations et retraites non revalorisées | Dossier de presse 15/07/2025 (p.5) [C] | exact | exact | B |  |
| V5-B5-17 | 111 | Il demande la confiance des députés, sur un discours consacré à un seul sujet : la dette | un seul sujet | Déclaration du 8/09/2025 centrée sur la dette et le surendettement mais traitant aussi production, éducation | CR AN 8/09/2025 (-) [C] | imprécis | trop général | A | Le discours n'est pas mono-thématique |
| V5-B5-18 | 111 | 364 voix contre | 364 | 573 votants, 558 exprimés, 194 pour, 364 contre | AN scrutin 3054 (-) [C] | exact | exact | A |  |
| V5-B5-19 | 111 | Neuf mois après Barnier, il tombe à son tour | 9 mois | 4/12/2024 → 8/09/2025 | scrutins 519 et 3054 (-) [C] | exact | exact | A |  |
| V5-B5-20 | 113 | En octobre 2025, une partie de l'opposition fait de la suspension de la réforme des retraites la condition pour ne pas le renverser | condition | M. Vallaud (PS) : annonce « nécessaire pour commencer le débat budgétaire et éviter la censure immédiate » | CR AN 14/10/2025 (-) [C] | exact sous condition | exact | B | Lecture d'une intervention ; pas de document d'accord |
| V5-B5-21 | 113 | Il la propose, jusqu'après la présidentielle | jusqu'après 2027 | « que nous suspendions la réforme de 2023 sur les retraites jusqu'à l'élection présidentielle » ; « jusqu'à janvier 2028 » | CR AN 14/10/2025 (-) [C] | exact | exact | A |  |
| V5-B5-22 | 113 | et promet de renoncer au 49.3 | 49.3 | « L'Assemblée voulait que je n'utilise pas le 49.3 : je m'y suis engagé » | CR AN 14/10/2025 (-) [C] | exact | exact | A |  |
| V5-B5-23 | 113 | Il n'est pas renversé | non censuré | 16/10/2025 : motions à 271 (n° 3058) et 144 voix (n° 3059), non adoptées | AN scrutins 3058-3059 (-) [C] | exact | exact | A |  |
| V5-B5-24 | 113 | En décembre, le budget de la Sécurité sociale est voté. Sans 49.3 | voté en déc. | Scrutin 4758, lecture définitive du PLFSS 2026, 16/12/2025 : 247 pour, 232 contre | AN, liste des scrutins PLFSS 2026 (-) [C] | exact | exact | A |  |
| V5-B5-25 | 113 | Avec la suspension dedans | suspension | COR 2026 : projections « en tenant compte de la suspension de la réforme des retraites de 2023 » (générations 1964 et début 1965) | COR RA 2026 (p.13) [C] | exact sous condition | exact | B | Article de la LFSS 2026 non relu |
| V5-B5-26 | 115 | trois millions et demi de Français, d'après le Premier ministre | 3,5 M | « Cette suspension profitera, à terme, à 3,5 millions de Français » | CR AN 14/10/2025 (-) [C] | exact | exact | E | Déclaration d'acteur |
| V5-B5-27 | 115 | La suspension coûtera près de 2 milliards d'euros à l'ensemble du système de retraite en 2027 | ≈2 Md€ en 2027 | PM : 0,4 Md€ en 2026 et 1,8 Md€ en 2027 ; COR 2026 : 1,8 Md€ en moyenne en année pleine jusqu'en 2032 (Drees) | CR AN 14/10/2025 ; COR RA 2026 (COR p.9) [C] | exact | exact | D |  |
| V5-B5-28 | 117 | pour survivre, le gouvernement a desserré le levier de la retraite, au lieu de le tirer | interprétation | Interprétation | - (-) [C] | non vérifiable à ce jour | non démontré | F |  |
| V5-B5-29 | 119 | Barnier et Bayrou demandaient un effort, pensions comprises : ils sont tombés. Lecornu a suspendu la réforme : il est toujours en place | faits | Lecornu Premier ministre au 4/11/2026 (PLFG 2026 signé ce jour) ; chutes de 2024 et 2025 avérées | PLFG 2026 n° 3434 ; scrutins 519 et 3054 (-) [C] | exact | exact | A | Faits exacts |
| V5-B5-30 | 119 | [juxtaposition implicite] la suspension explique le maintien de Lecornu | causalité | Autres facteurs non examinés (renonciation au 49.3 puis trois 49.3 en janvier-février 2026, compromis budgétaires) | - (-) [C] | trompeur par périmètre ou juxtaposition | non démontré | F | Juxtaposition de deux cas suggérant une causalité |
| V5-B5-31 | 121 | Le budget de l'État, lui, ne passe qu'en février. Avec trois 49.3, malgré la promesse d'octobre | février ; trois 49.3 | 49.3 sur la 1re partie (motions rejetées 23/01/2026), sur la 2e partie et l'ensemble (27/01/2026), en lecture définitive (motions rejetées 2/02/2026) | AN, liste des motions de censure 17e législature (-) [C] | exact | exact | A |  |
| V5-B5-32 | 123 | En séance, les députés réécrivent le budget : des taxes sont ajoutées, des efforts retirés, dont un qui touchait encore les retraités | taxes ajoutées, efforts retirés | Ministre : baisse nette de 16 Md€ de prélèvements (suppression de la contribution exceptionnelle des grandes entreprises, annulation du plafonnement de l'abattement sur les pensions, baisses de TVA), « partiellement compensées » par deux taxes ; +8 Md€ vers les collectivités | CR AN 4/11/2026 (art. liminaire, 2e délibération) [C] | imprécis | trop général | A | Les taxes ajoutées sont minoritaires : la dégradation vient surtout de baisses d'impôts et de transferts |
| V5-B5-33 | 123 | d'après le ministre des Comptes publics, le déficit prévu n'est plus de 5 %, mais de 5,9 | 5 → 5,9 | « se serait élevé à 5 % ... À l'issue de l'examen de la première partie, il s'élèverait à 5,9 % » | CR AN 4/11/2026 (M. Amiel) (-) [C] | exact | exact | A | Estimation sur un texte ensuite rejeté |
| V5-B5-34 | 123 | Comme en 2024, comme en 2025, la partie recettes est rejetée. Trois automnes de suite | 3 rejets | 12/11/2024 : 192 pour, 362 contre (n° 438) ; 21/11/2025 : 1 pour, 404 contre (n° 4241) ; 4/11/2026 : 0-458 (n° 9759) | AN scrutins 438, 4241, 9759 (-) [C] | exact | exact | A |  |
| V5-B5-35 | 125 | On trouve une majorité pour retirer un effort. Pas pour voter le budget qui en résulte | constat | Cohérent avec les votes du 4/11/2026 | CR et scrutin 9759 (-) [C] | exact sous condition | exact | B | Formule de synthèse |
| V5-B5-36 | 127 | Dans le rapport qui accompagne le budget 2027, le gouvernement maintient sa promesse : sous les 3 % en 2029 | 3 % en 2029 | RESF : objectif « retour du déficit sous 3 % du PIB en 2029 » (recommandation du Conseil) ; HCFP : « toujours prévu » | RESF PLF 2027 ; HCFP 2026-5 (p.105) [C] | exact | exact | A |  |
| V5-B5-37 | 127 | cette trajectoire « revêt un caractère conventionnel du fait des échéances électorales de 2027 » | citation | « Cette trajectoire pluriannuelle revêt un caractère conventionnel du fait des échéances électorales de 2027 » | RESF annexé au PLF 2027 (p.134) [C] | exact | exact | A | Mot pour mot |
| V5-B5-38 | 127 | Ce sera au prochain gouvernement d'en écrire une autre | prochain gouvernement | « il appartiendra au prochain Gouvernement de définir une nouvelle trajectoire pluriannuelle après les élections » | RESF (p.134) [C] | exact | exact | A |  |
| V5-B5-39 | 127 | Comme la suspension des retraites : ce qui coûte des voix est renvoyé après l'élection | interprétation | Jugement | - (-) [C] | non vérifiable à ce jour | non démontré | F |  |
| V5-B5-40 | 129 | Le 22 octobre, le taux auquel la France emprunte à dix ans a dépassé 5 % | > 5 % le 22/10 | Moyenne d'octobre 2026 : 4,89 % (BCE) ; presse : passage au-dessus de 5 % le 21 ou le 22 octobre | BCE IRS mensuel ; presse (Saxo, Journal du Coin) (2026-10) [C] BCE / [S] presse | non vérifiable à ce jour | non vérifié | E | Aucune série quotidienne officielle obtenue ; dates contradictoires dans la presse |
| V5-B5-41 | 129 | Plus que l'Italie | FR > IT | Octobre 2026 : 4,89 vs 4,68 | BCE IRS (2026-10) [C] | exact sous condition | exact | A | Moyenne mensuelle |
| V5-B5-42 | 129 | L'Italie est pourtant plus endettée que nous | IT > FR | 2025 : 136,7 % vs 115,7 % | Eurostat edpt1 (GD) [C] | exact | exact | A |  |
| V5-B5-43 | 129 | Mais avant de payer ses intérêts, elle dégage un excédent | solde primaire IT > 0 | Italie 2025 : solde -3,1 + intérêts 3,8 = +0,7 % | Eurostat gov_10a_main (B9, D41PAY) [C] | exact | exact | A |  |
| V5-B5-44 | 129 | La France, un déficit de près de 3 % de sa richesse | ≈3 % | Solde primaire 2025 : -2,9 % (Eurostat) / -2,87 % (Insee) ; 2026 prévu : -2,8 % | Eurostat ; Insee t_3201 ; HCFP (-) [C] | exact | exact | A |  |
| V5-B5-45 | 131 | depuis 2022, les taux ont monté partout | hausse | DE 10 ans : -0,38 % (déc. 2021) → 2,09 % (déc. 2022) → 3,42 % (oct. 2026) | BCE IRS (-) [C] | exact | exact | A |  |
| V5-B5-46 | 131 | À la veille de la dissolution, un demi-point | 0,5 pt | Écart FR-DE moyenne de mai 2024 : 0,51 ; juin 2024 : 0,67 | BCE IRS ; C-A18-006 (2024-05) [C] | exact sous condition | exact | A | Moyenne mensuelle, pas le point du 7 juin |
| V5-B5-47 | 131 | Fin octobre, près de trois fois plus | ≈ x 3 | Octobre 2026 : 1,47 pt (x 2,9) | BCE IRS ; C-A18-006 (2026-10) [C] | exact sous condition | exact | A | Moyenne mensuelle |
| V5-B5-48 | 131 | le gouvernement cite lui-même « les interrogations sur la situation politique en France » | citation | Formule absente du RESF, du DP Budget 2027, du PLF, du PAP 117, du PLFG 2026 ; le HCFP parle d'« incertitude quant à la situation politique » | RESF ; DP ; PAP 117 ; PLF ; PLFG ; HCFP (p.14) (-) [X] | non vérifiable à ce jour | non vérifié | - | Source de la citation non identifiée |
| V5-B5-49 | 133 | L'an prochain, rien que pour l'État, la charge de la dette pèsera autant que tout le budget de la Défense : 72 milliards d'euros | 72 = Défense | PLF 2027 : charge de la dette (programmes 117 et 355) 72,93 Md€ ; mission « Défense » 63,4 Md€ (hors CAS Pensions) : écart de 9,5 Md€ | Dossier de presse Budget 2027 (p.57 et p.88) [C] | faux | inexact | A | La charge dépasse la Défense ; l'égalité n'est possible qu'en ajoutant les pensions militaires (non vérifié) |
| V5-B5-50 | 133 | chaque dixième de point de taux qui dure finit par coûter 4 milliards de plus par an | 4 Md€ / 0,1 pt | +100 pb → +3,4 Md€ la 1re année, ≈ 19 Md€ la 5e (PAP 117) ; → 0,34 puis ≈ 1,9 Md€ par dixième ; plafond tout stock : 2,8 (État) à 3,5 Md€ (APU) | PAP programme 117 PLF 2027 ; DP Budget 2027 p.27 ; C-A18-015/016 (PAP p.22) [C] | faux | inexact | A | Surestimation d'environ un facteur 2 à l'horizon de 5 ans |
| V5-B5-51 | 133 | Plus que tout le budget de la Culture | > Culture | Mission « Culture » PLF 2027 : 3,4 Md€ ; or le coût d'un dixième à 5 ans ≈ 1,9 Md€ | DP Budget 2027 (p.57 et p.77) [C] | trompeur par périmètre ou juxtaposition | inexact | A | Comparaison fausse avec le chiffre corrigé |
| V5-B5-52 | 135 | Cet écart-là, c'est le jugement des prêteurs sur elle | interprétation | L'écart reflète aussi liquidité, offre de titres, politique de la BCE | - (-) [C] | imprécis | trop général | F |  |
| V5-B5-53 | 135 | Le blocage a un prix. Il se paie à chaque nouvel emprunt | causalité | HCFP : « l'incertitude quant à la situation politique » est un aléa ; aucune mesure de la part politique de l'écart | HCFP 2026-5 (p.14) [C] | non vérifiable à ce jour | non démontré | C | Cause plausible non isolée |

### Bloc B6

| Id | L. | Affirmation | Script | Trouvé | Source (page) | Verdict | M2 | Niv. | Motif |
|---|---|---|---|---|---|---|---|---|---|
| V5-B6-01 | 143 | Octobre 1994. Göran Persson devient ministre des Finances de la Suède | oct. 1994 | « The new government that took office in October 1994 » (discours de G. Persson, 1995) | Persson, Jackson Hole 1995 ; Reuters 2025 (p.3) [C] / [S] | exact sous condition | exact | B | Titre de ministre non écrit dans la pièce primaire ; confirmé par Reuters |
| V5-B6-02 | 143 | Peu après, il s'envole pour New York ... convaincre des investisseurs de Wall Street de continuer à acheter la dette | voyage | Reuters (23/10/2025) : voyage « during the country's early 1990s financial crisis », d'après le livre de Persson (1997) ; date non précisée | Reuters via The Financial Express (-) [S] | non vérifiable à ce jour | non vérifié | E | « Peu après octobre 1994 » non établi ; livre de 1997 non consulté |
| V5-B6-03 | 143 | Il dort dans un hôtel bon marché, infesté de cafards : son ministère interdit toute dépense superflue | anecdote | « stayed in a budget hotel infested with cockroaches » ; politique « absolutely no extravagance » | Reuters via The Financial Express (-) [S] | exact sous condition | exact | E | Témoignage autobiographique cité par un tiers |
| V5-B6-04 | 145 | Une crise bancaire, une récession brutale | crise | « deepest recession since the 1930s » ; crise financière (Riksbank) | Persson 1995 ; Riksbank (p.2) [C] | exact | exact | B |  |
| V5-B6-05 | 145 | En novembre 1992, sa monnaie a dû flotter, et elle a plongé | nov. 1992 | « On 19 November, the fixed exchange rate was scrapped and the Swedish krona was allowed to float » | Riksbank, frise historique (-) [C] | exact sous condition | exact | B | Ampleur de la chute non relue dans la pièce |
| V5-B6-06 | 145 | En 1993, son déficit public atteint environ 12 % de sa richesse | ≈12 % | OCDE (millésime 2026) : -10,7 % en 1993, -8,7 % en 1994 ; Persson (1995) : 10 % en 1994 ; Reuters : « at worst ... 12 per cent » | OCDE Perspectives économiques ; Persson 1995 ; Reuters (NLGQ 1993) [C] | imprécis | inexact | A | 12 % excède les séries actuelles (10,7 %) ; dépend du millésime |
| V5-B6-07 | 145 | Plus du double du nôtre aujourd'hui | > x 2 | 10,7 / 5,1 = 2,1 | OCDE ; Insee ; C-A18-012 (-) [C] | exact | exact | A |  |
| V5-B6-08 | 145 | Cinq ans plus tard, en 1998, ses comptes sont en excédent | 1998 > 0 | +0,8 % (Eurostat, OCDE) | Eurostat gov_10a_main SE ; OCDE (-) [C] | exact | exact | A |  |
| V5-B6-09 | 147 | Avec un plan massif lancé à l'automne 1994 | automne 1994 | Programme de consolidation de 7,5 % du PIB du gouvernement entré en fonction en octobre 1994 | Persson 1995 (p.3) [C] | exact | exact | B |  |
| V5-B6-10 | 147 | presque deux tiers des mesures sont des baisses de dépenses, d'après le ministre lui-même | ≈ 2/3 | « Almost two-thirds of the measures are spending cuts » | Persson 1995 (p.3) [C] | exact | exact | E | Déclaration d'acteur |
| V5-B6-11 | 147 | Sa consigne : « Ne dites jamais que ça ne fera pas mal. » | citation | « Never say that it won't hurt. » | Persson 1995 (p.2) [C] | exact sous condition | exact | B | Traduction de l'anglais |
| V5-B6-12 | 147 | En 1996, le chômage est encore à 8 %, et à plus de 12 % en comptant les personnes en programmes d'emploi | 8 % ; > 12 % | 1996 : chômage déclaré 8,1 % + programmes conjoncturels 4,5 % = 12,6 % ; OCDE harmonisé : 11,7 % | Gouvernement suédois, Prop. 1997/98:150, tableau ; OCDE (p.7) [C] | exact sous condition | exact | A | Définition nationale de l'époque ; colonnes du tableau attribuées à 1991-2001 par déduction |
| V5-B6-13 | 147 | Et la Suède avait un atout que la France n'a plus : sa propre monnaie | monnaie | Couronne flottante depuis le 19/11/1992 | Riksbank (-) [C] | exact | exact | B |  |
| V5-B6-14 | 149 | En 1995, il raconte que l'objectif de revenir à l'équilibre est soutenu par 94 % du Parlement | 94 % | « This goal is supported by 94 percent in Parliament » (objectif : 3 % en 1997 et équilibre en 1998) | Persson 1995 (p.4) [C] | exact | exact | E |  |
| V5-B6-15 | 149 | Les Suédois se disputent sur les moyens. Pas sur le but | généralisation | Déduit du seul chiffre de 94 % | Persson 1995 (p.4) [C] | imprécis | trop général | E |  |
| V5-B6-16 | 149 | son gouvernement l'écrira : sans la coopération avec le Parti du centre ... ce redressement n'aurait pas été possible | citation | « It would not have been possible without co-operation during recent years between the Social-Democrats and the centre party » | Gouvernement suédois, Prop. 1997/98:150, Budget Statement (p.4) [C] | exact | exact | A | « Un parti de l'autre bloc » non relu dans une pièce |
| V5-B6-17 | 151 | on sait ce qu'il faut faire, alors pourquoi ne le fait-on pas ? Sa réponse : c'est une question politique | citation | « if we know what has to be done, why do we not do it? This is a political question. » | Persson 1995 (p.1) [C] | exact | exact | B |  |
| V5-B6-18 | 153 | La première : un effort réparti équitablement | condition 1 | « the burdens of consolidation are shared fairly » | Persson 1995 (p.2) [C] | exact | exact | B |  |
| V5-B6-19 | 153 | La deuxième : un plan présenté d'un seul bloc, pour que chacun voie qu'il n'est pas le seul à qui on demande des sacrifices | condition 2 | « comprehensive package ... they are not the only ones asked to make sacrifices » | Persson 1995 (p.2) [C] | exact | exact | B |  |
| V5-B6-20 | 153 | Chez nous, les efforts se retirent un par un | constat | Cohérent avec l'automne 2026 (CR 4/11) ; non généralisable sans autre pièce | CR AN 4/11/2026 (-) [C] | imprécis | trop général | C |  |
| V5-B6-21 | 153 | La troisième : tout mettre sur la table, les hypothèses, les calculs, les mauvaises nouvelles | condition 3 | « transparent ... always clarify assumptions and calculations ... never play down the effects » | Persson 1995 (p.2) [C] | exact sous condition | exact | B | « Les mauvaises nouvelles » est une paraphrase |
| V5-B6-22 | 153 | À cette date, il n'a jamais eu à corriger une prévision de déficit dans le mauvais sens | jamais | « So far, I have never had to revise a budget deficit estimate in the wrong direction » | Persson 1995 (p.4) [C] | exact | exact | E | Déclaration d'acteur |
| V5-B6-23 | 153 | La Suède y ajoute un verrou : le Parlement vote d'abord le total des dépenses | cadre | Résolution du Parlement : volume total et par domaine fixés en début de procédure ; plafonds de dépenses depuis le budget 1997 | Persson 1995 ; programme de convergence 1998 (p.4-5 ; p.6) [C] | exact | exact | A |  |
| V5-B6-24 | 153 | Résultat, d'après le ministre : il ne peut plus sortir un budget plus déséquilibré que celui qu'on lui a présenté | citation | « Parliament cannot pass a budget that is weaker than the one presented by the government » | Persson 1995 (p.5) [C] | exact | exact | B |  |
| V5-B6-25 | 153 | Chez nous, un député n'a pas le droit d'ajouter une dépense | art. 40 | Art. 40 : irrecevabilité de la création ou de l'aggravation d'une charge publique ; redéploiements entre programmes d'une mission possibles (LOLF, non relue) | AN, rapport d'information n° 1891 sur la recevabilité financière (p.40 et suiv.) [C] | imprécis | trop général | A | Formulation trop absolue |
| V5-B6-26 | 153 | Mais il peut retirer une économie | suppression | « Un amendement de suppression d'un article est toujours recevable » | AN rapport n° 1891 (p.40) [C] | exact | exact | A |  |
| V5-B6-27 | 153 | C'est ce qui s'est passé cet automne | automne 2026 | Annulation du plafonnement de l'abattement sur les pensions et des économies sur les collectivités ; mais aussi baisses de TVA et suppression d'une contribution | CR AN 4/11/2026 (-) [C] | exact sous condition | exact | A | Partiellement : la dégradation vient aussi de baisses d'impôts |
| V5-B6-28 | 155 | Ce n'est pas faute de savoir : les alertes s'empilent depuis vingt ans | 20 ans | Pébereau 2005 ; Fillon 2007 ; HCFP depuis 2013 | AN r2844 ; AFP (-) [C] | exact sous condition | exact | B |  |
| V5-B6-29 | 155 | Le trou vient d'une dépense qui a pris de l'avance il y a plus de trente ans, et que personne n'a rattrapée : ni en dépensant moins, ni en prélevant assez | cause | Dépense 56,5 % dès 1993 ; mais baisses d'impôts 2018-2023 (62 Md€) citées par la V5 elle-même | Insee ; Cour 2024 (-) [C] | trompeur par périmètre ou juxtaposition | non démontré | C | Identité comptable présentée comme cause ; omet le rôle des baisses de recettes établi en B3 |
| V5-B6-30 | 155 | Chaque crise l'a creusé un peu plus | crises | Dette en marches (1993, 2008, 2020) ; le déficit, lui, s'est réduit après chaque crise | Insee (-) [C] | imprécis | trop général | A | Confusion entre « trou » (déficit) et dette |
| V5-B6-31 | 157 | La réforme des retraites ... : une dizaine de milliards par an, en 2030. Le plan que portait Bayrou ... : 44. Le trou : 150 | 10 / 44 / 150 | 10 Md€ (retraites, 2030) ; 43,8 Md€ (effort 2026 avec LPM) ; 151,6 Md€ (déficit 2025) | Cour 2025 ; DP 15/07/2025 ; Insee (-) [C] | trompeur par périmètre ou juxtaposition | inexact | A | Rapprochement de grandeurs d'années et de périmètres différents (norme 04 §III.7) |
| V5-B6-32 | 159 | Ce qui manque à la France, ce n'est pas le calcul. C'est un accord sur l'effort. Sur la dépense d'abord | jugement | Prescription | - (-) [C] | non vérifiable à ce jour | non démontré | F | Jugement présenté comme conclusion |
| V5-B6-33 | 159 | La Suède l'a trouvé au pied du mur, quand il fallait aller convaincre les prêteurs | interprétation | Cohérent avec Persson 1995 (dépendance aux marchés) | Persson 1995 (p.5) [C] | exact sous condition | exact | E |  |
| V5-B6-34 | 159 | quand un État doit emprunter à ce point, le pouvoir passe des élus à ceux qui lui prêtent | citation paraphrasée | « power was shifted from the elected representatives to the owners of capital » | Persson 1995 (p.5) [C] | exact | exact | B |  |
| V5-B6-35 | 159 | Mais elle emprunte déjà plus cher que l'Italie | FR > IT | Octobre 2026 : 4,89 vs 4,68 | BCE IRS (2026-10) [C] | exact sous condition | exact | A |  |
| V5-B6-36 | 159 | [généralisation] La leçon suédoise s'applique à la France | transposition | Suède : monnaie propre dévaluée, croissance de 4 % en 1994-1995 et 1998, cadre institutionnel nouveau ; cas unique | Eurostat ; Riksbank (-) [C] | imprécis | non démontré | C | Généralisation à partir d'un cas ; la V5 signale la monnaie mais pas la croissance |
| V5-B6-37 | 161 | Sur le registre, 51 pages sont rouges | 51 | 51 exercices en déficit | Insee (-) [C] | exact | exact | A |  |

### 1.9 Gel de la passe 1

Passe 1 figée le **2026-11-20 18:48:58 +0100** (horloge de la machine), **avant toute lecture** des fichiers de la cellule (transmissions, contradictions, preuves, journal, dossiers d'agents) et de la contre-enquête Astra.

- Fichier : resultats\donnees\A18\A18_audit_V5_passe1.csv, 81460 octets.
- SHA-256 : d8832d185aee3ceae07c43f8174a0a26606c579688444ec4fd80dd0a814e0db2

Ce fichier n'est plus modifié. Les écarts constatés en passe 2 sont consignés à part (section 2 et A18_audit_V5_passe2.csv).

## 2. Passe 2 — confrontation

La passe 2 a été ouverte après le gel. J'ai lu, dans l'ordre fixé par le plan v2 :
1. `transmissions\vague1.md` et `transmissions\vague2.md`, en entier, dont les §5 ;
2. `contradictions.md` (v3) et `preuves.md` (v1) ;
3. `journal\recette_*.md`, par recherche des mentions de la V5 ;
4. la contre-enquête Astra du 19/11/2026, en entier : les lignes 191-246 ne contiennent que les liens.

Aucun dossier d'agent n'a été ouvert. Pour chaque divergence, j'ai repris la pièce primaire. Trois copies de la cellule ont été lues sans que je les retélécharge :
- Commission IP 348 et rapport du Sénat n° 133 (1975-1976) : leur identité avec l'original a été vérifiée par l'orchestrateur ;
- avis du HCFP 2026-2 : copie d'A01, **non vérifiée**.

Fichier : `resultats\donnees\A18\A18_audit_V5_passe2.csv`. Il contient les 200 affirmations de la passe 1 avec leur verdict final, la colonne « changement », la pièce et l'URL de passe 1. S'y ajoutent :
- six lignes du script sans ligne en passe 1 (contrôle de couverture) ;
- deux corrections de motif ;
- la révision du 17/11 ;
- le signalement S02.

### 2.1 Bilan

**Huit verdicts changés sur 200.**

| Ligne | Passe 1 | Passe 2 |
|---|---|---|
| B1-05 | exact sous condition | imprécis (M2 trop général) |
| B3-23 | exact sous condition | imprécis (M2 inexact) |
| B4-19 | non vérifiable | faux (M2 inexact) |
| B5-47 | exact sous condition | exact |
| B5-49 | **faux** | **exact sous condition** |
| B5-50 | **faux** | **exact sous condition** |
| B5-51 | trompeur | imprécis (M2 non démontré) |
| B6-27 | exact sous condition | imprécis (M2 trop général) |

**Deux erreurs d'A18 en passe 1, corrigées ici :**
- Défense : il fallait lire l'état B du PLF 2027, pensions comprises.
- Dixième de point : il fallait lire le graphique du PAP 117 et pas seulement son texte.

**Autres corrections.**
- La passe 1 affirmait que 2000 était le meilleur solde depuis 1975. C'est faux : 1980 est à -0,4 %. Le motif des lignes B1-07 et B2-11 est corrigé, leur verdict ne change pas.
- La passe 1 datait de mai le chiffre de 151,6 Md€ ; il date du 28 août 2026.
- Sur l'écart COFOG, le chiffre de 8,1 points cité en passe 1 doit être remplacé par 7,7 à 7,8.

**Révision postérieure au script manquée en passe 1.** Prévision de la Commission du 17/11/2026 : 5,5 % en 2026 et 5,4 % en 2027.

**Répartition finale (200 affirmations).**
- Échelle initiale : exact 115 ; exact sous condition 46 ; imprécis 20 ; trompeur 4 ; faux 1 ; non vérifiable 14.
- Échelle M2 : exact 162 ; inexact 7 ; trop général 12 ; non démontré 15 ; non vérifié 4.
- **Parmi les 162 « exact » M2, 46 sont sous condition**, et une dizaine reposent sur une source secondaire ou ont un élément non vérifié : Fillon, hôtel, Pébereau, décret de dissolution, « mars 2000 », contenu de la loi TEPA, article de la LFSS 2026.

### 2.2 Qui a raison

- **La cellule a raison contre la passe 1 d'A18 :**
  - « prélevé un peu plus de 5 points » : 4,7 points en impôts et cotisations ;
  - « l'aide dure » : aides de crise passées de 83,7 Md€ en 2021 à 12,4 en 2023 (Cour, juillet 2024, p.42-43) ;
  - 1975 : plans de soutien d'environ 36 MdF sur 45,7 MdF de déficit prévu (Sénat 1975, p.4) ;
  - l'écart COFOG est de 7,7 à 7,8 points ;
  - le dixième de point vaut 3,3 Md€ la 10e année (A07).
- **A18 corrige la cellule :**
  - **Défense pensions comprises : 73,2 Md€ en CP (état B)**, contre 72,4 Md€ de charge de la dette. La phrase de la V5 est exacte ; la cellule la laissait « non vérifiée ».
  - Le rapport n° 1891 de l'AN (p.99) permet au député le redéploiement entre programmes d'une même mission, ce qu'A08 n'indique pas.
  - Trois 49.3 sont attestés pour le budget 2026, contre deux selon A03.
- **A18 apporte des pièces sur cinq points que la cellule laissait non vérifiés :**
  - chômage suédois de 1996 et Parti du centre : Prop. 1997/98:150, p.7 et p.4 ;
  - « depuis 1962 » : compte rendu de l'AN du 4/12/2024 ;
  - titre du rapport Pébereau : AN et Sénat, [S] ;
  - hôtel de Persson : Reuters, [S].
- **Citations.** Le balayage complet des pièces confirme l'absence de « semble peu plausible » dans les avis HCFP 2026-5 et 2026-2. L'expression figure dans la Cour des comptes de juillet 2024 (p.109), à propos du programme de stabilité de 2024. « Les interrogations sur la situation politique » reste introuvable ; le lien entre écart de taux et situation politique est fait par la Commission (p.47, en anglais) et par le HCFP.
- **Astra.** Concordance sur la Suède à 12¼ % : chiffre du compte de l'époque, 10,7 % en comptes harmonisés. Concordance aussi sur « 10 / 44 / 150 », sur le périmètre des 10 Md€ et sur les deux tiers attribués au ministre. La part bancaire d'environ 3 points n'a pas été relue : le PDF du FMI de 1998 est scanné, sans texte. Astra numérote les lignes d'une autre version de la V5 ; les correspondances ont été faites sur le texte.

### 2.3 Les dix affirmations les plus fragiles après confrontation

1. **B6-31**, « 10 / 44 / 150 » : juxtaposition de périmètres et d'années différents.
2. **B4-39**, HCFP « semble peu plausible » : citation non conforme.
3. **B5-48**, « les interrogations sur la situation politique en France » : introuvable, attribution non étayée.
4. **B4-19**, « l'aide dure » : contredit par la Cour.
5. **B3-23**, « un peu plus de 5 points » prélevés : 4,7 en impôts et cotisations.
6. **B6-06**, Suède « environ 12 % » : 10,7 % en comptes harmonisés.
7. **B5-40**, plus de 5 % « le 22 octobre » : non vérifié, la presse dit le 21.
8. **B4-22**, Allemagne « près de 10 mois » : 8,9 à 9,3.
9. **B4-34**, LPFP « votée » : adoptée par le 49.3.
10. **B3-21 et B3-22**, moyenne de la zone euro incluant la France ; COFOG 2024 contre écart 2025.

### 2.4 Tableau des lignes confrontées

| Id | Passe 1 (M2) | Confrontation | Position | Pièce reprise par A18 | Passe 2 (M2) | Changé | Qui a raison | Motif |
|---|---|---|---|---|---|---|---|---|
| V5-B1-05 | exact sous condition (exact) | cellule (vague 1 T-01, contradictions K-050 ; A02, S01) | Les plans de soutien de 1975 pèsent environ 36 MdF sur 45,7 de déficit prévu de l'État ; 48 à 67 % du déficit exécuté | Sénat, rapport n° 133 (1975-1976), p.3-4 : plans de soutien « proches de 36 milliards de francs », déficit prévu 45 698 MF (copie de la base commune, identité vérifiée par l'orchestrateur, non retéléchargée par A18) | imprécis (trop général) | oui | cellule | La V5 attribue la plongée de 1975 à la seule récession ; les plans de relance votés pèsent autant (budget de l'État ; part pour l'ensemble des APU non établie) |
| V5-B3-23 | exact sous condition (exact) | cellule (K-007, A01) | « Un peu plus de 5 points » sont des recettes totales ; en impôts et cotisations, 4,7 | Eurostat gov_10a_taxag 2025 : FR 46,0 vs ZE20 41,3 = 4,7 (extraction A18) | imprécis (inexact) | oui | cellule | La V5 emploie « prélever » au sens d'impôts et cotisations (B1, l.5) : sur ce périmètre l'écart est inférieur à 5 points. A18 avait accepté la lecture « recettes totales » en passe 1 |
| V5-B4-19 | non vérifiable à ce jour (non démontré) | cellule (K-025, A03) | Mesures d'urgence et de relance : 83,7 Md€ en 2021, 34,9 en 2022, 12,4 en 2023 | Cour des comptes, juillet 2024, p.42-43, tableau (pièce retéléchargée par A18) | faux (inexact) | oui | cellule | « L'aide dure » est contredit pour les aides de crise : elles ont été retirées en deux ans ; la phrase reste vraie pour la dette accumulée (B4-20) |
| V5-B5-50 | faux (inexact) | cellule (K-023, A07) | 0,3 Md€ la 1re année, 1,9 à 5 ans, 3,3 à 10 ans pour l'État ; « vrai seulement à dix ans ou plus » | PAP 117 PLF 2027, graphique p.23 du document (page 22 du PDF, rendue en image par A18) : choc de +100 pb → 3,4 ; 8,1 ; 12,0 ; 15,7 ; 19,2 ; 22,5 ; 25,5 ; 28,1 ; 30,7 ; 33,0 Md€ de 2027 à 2036, encore croissant | exact sous condition (exact) | oui | cellule (A07) ; passe 1 d'A18 erronée | 3,3 Md€ par dixième de point la 10e année et en hausse : « finit par coûter 4 Md€ » est un ordre de grandeur atteint au-delà de dix ans (État, comptabilité maastrichtienne). La passe 1 n'avait lu que le texte (années 1 et 5) et concluait à tort à « faux » |
| V5-B5-49 | faux (inexact) | cellule (K-021) | 72,4 Md€ en crédits (programme 117) : exact ; Défense 63,4 hors pensions : égalité « non vérifiée » | PLF 2027 n° 3210, état B (p.246-247) : mission Défense, CP 73 153 440 797 € (titre 2 et contributions au CAS Pensions compris) ; programme 117 « Charge de la dette et trésorerie de l'État » : 72 373 000 000 € | exact sous condition (exact) | oui | A18 (pièce trouvée ; passe 1 erronée) | En crédits de paiement de l'état B, pensions comprises, la Défense pèse 73,2 Md€ contre 72,4 Md€ de charge de la dette : « autant » est exact. Le « faux » de passe 1 reposait sur le seul chiffre hors pensions du dossier de presse |
| V5-B5-51 | trompeur par périmètre ou juxtaposition (inexact) | cellule (non traité) | - | PLF 2027 état B : mission Culture, CP 3 649 196 894 € ; DP : 3,4 Md€ hors pensions ; un dixième de point : 3,3 Md€ à 10 ans (PAP 117) | imprécis (non démontré) | oui | A18 | Le dixième de point ne dépasse la mission Culture (3,4 à 3,65 Md€) qu'au-delà de l'horizon de dix ans de la simulation officielle |
| V5-B4-39 | imprécis (inexact) | cellule (K-020, A03) | « semble peu plausible » absent de l'avis 2026-5 | Balayage A18 : absent des avis HCFP 2026-5 et 2026-2 (copie A01 extraite par A18) ; « peu plausible » figure dans Cour des comptes, juillet 2024, p.109, au sujet de la trajectoire du programme de stabilité 2024 | imprécis (inexact) | non | concordant | Guillemets non conformes ; confusion possible avec la Cour (2024) |
| V5-B5-47 | exact sous condition (exact) | cellule (preuves.md A07 §12) et Astra | Commission : écart français au-delà de 160 pb fin octobre | Commission européenne, prévisions d'automne 2026 (IP 348), p.47 : « the French spread exceeded 160 bps », « up from 65 bps in early May » (copie de la base commune, identité vérifiée par l'orchestrateur) | exact (exact) | oui | cellule (pièce supplémentaire) | Passe 1 reposait sur des moyennes mensuelles ; la Commission donne le point de fin octobre : ×3,2 par rapport à 0,5 |
| V5-B6-27 | exact sous condition (exact) | cellule (K-062, A08) | Le 4 novembre, 16 des 26 Md€ de dégradation viennent de prélèvements supprimés | CR AN 4/11/2026 (M. Amiel) : 16 Md€ de PO + 8 Md€ collectivités + 2 Md€ crédits d'impôt | imprécis (trop général) | oui | cellule | « C'est ce qui s'est passé cet automne » illustre le retrait d'une économie, alors que l'essentiel du retrait est fiscal |
| V5-B1-03 | exact (exact) | cellule (K-012, A01, A02 ; règle de données 3) | Dernier excédent tenu dans trois bases ; excédent de 1974 divisé par deux entre bases ; la série « hors éléments imputés » met 1974 en déficit | Calcul A18 sur le classeur Insee base 2020 : lignes « hors éléments imputés » 1974 = 39,23 - 39,90 = -0,67 ; ces lignes ne mesurent pas le solde (règle 3) | exact (exact) | non | concordant | Le solde officiel (+0,1 %) est la bonne mesure ; verdict maintenu |
| V5-B1-07 | exact (exact) | preuves.md F-ORC-012 | Meilleur solde depuis 1975 : -0,4 % (1980) | Insee fig. 2 : 1980 = -0,4 (calcul A18) | exact (exact) | non (motif corrigé) | orchestrateur | Erreur d'A18 en passe 1 : le motif disait « meilleur solde -1,3 % en 2000 » ; c'est -0,4 % en 1980. Verdict inchangé |
| V5-B2-11 | exact (exact) | preuves.md F-ORC-012 | Meilleur solde : 1980 | Insee fig. 2 | exact (exact) | non (motif corrigé) | orchestrateur | Le motif de passe 1 (« meilleur solde de 1975-2025 » pour 2000) est faux ; 2000 est le meilleur solde depuis 1981 |
| V5-B1-M1 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | sans objet (-) | oui (ajout) | - | Méthode du documentaire, non vérifiable par pièce |
| V5-B4-M1 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | non vérifiable à ce jour (non démontré) | oui (ajout) | - | Jugement |
| V5-B5-M1 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | exact sous condition (exact) | oui (ajout) | - | Conséquence arithmétique de l'absence de majorité (CR AN 14/10/2025 : « sans majorité absolue ») |
| V5-B5-M2 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | exact (exact) | oui (ajout) | - | Barnier, Bayrou, Lecornu (scrutins 519 et 3054 ; PLFG 2026 signé par S. Lecornu) |
| V5-B5-M3 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | exact sous condition (exact) | oui (ajout) | - | Répétition de V5-B1-16 et V5-B1-17 |
| V5-B6-M1 | (manquée en passe 1) (-) | contrôle de couverture A18 | - | voir motif | exact sous condition (exact) | oui (ajout) | - | Répétition de V5-B1-13 (vrai en 2025, faux en 2024) |
| V5-B3-22 | trompeur par périmètre ou juxtaposition (exact) | cellule (règle de données 4, K-016) et Astra (8,1 points) | Les ratios COFOG d'Eurostat reposent sur un PIB périmé (57,3 au lieu de 57,0) : écart 2024 de 7,7-7,8 points, non 8,1 | Recalcul A18 en montants (script a18_05, §4b) : FR 56,96 ; part protection sociale + santé 65 % (hors France) | trompeur par périmètre ou juxtaposition (exact) | non | cellule contre Astra (et contre la passe 1 d'A18 sur le chiffre 8,1) | Le « près des deux tiers » de la V5 tient (64-65 %) ; le chiffre de 8,1 cité en passe 1 doit être remplacé par 7,7-7,8 |
| V5-B3-21 | exact sous condition (exact) | cellule (règle 5, C-A01-009) | Hors France : 9,2 points de dépenses, 6,7 de recettes | Recalcul A18 : 9,28 et 6,72 (PIB nama, a18_05) | exact sous condition (exact) | non | concordant | Écart de 0,1 dû au dénominateur |
| V5-B5-31 | exact (exact) | cellule (vague 1 : A03 « deux attestés » ; vague 2 : A09 « trois ») | Désaccord interne à la cellule | AN, liste des motions de censure : motions sur la 1re partie (23/01/2026), la 2e partie et l'ensemble (27/01), la lecture définitive (2/02) | exact (exact) | non | A09 et A18 contre A03 | Trois engagements de responsabilité attestés sur pièce primaire |
| V5-B4-34 | imprécis (inexact) | cellule (K-067, A08) | Adoption définitive le 15 novembre 2023 ; promulgation le 18 décembre | Décision 2023-857 DC : adoption par 49.3 en lecture définitive | imprécis (inexact) | non | A18 (précision non relevée par la cellule) | La date de la cellule est compatible (saisine le 16/11) ; « votée » reste impropre |
| V5-B5-40 | non vérifiable à ce jour (non vérifié) | cellule (K-022) ; Astra | Clôture au-dessus de 5 % dès le 21 selon deux dépêches ; Commission : « around 5% at the end of October » | Commission IP 348 p.47 ; BCE (moyenne 4,89) | non vérifiable à ce jour (non vérifié) | non | concordant | Si les dépêches disent vrai, la date de la V5 est décalée d'un jour ; aucune série quotidienne officielle |
| V5-B5-48 | non vérifiable à ce jour (non vérifié) | cellule (K-024, K-010) | Citation non retrouvée ; la Commission fait le lien | Balayage A18 de toutes les pièces extraites (RESF, DP, PLF, PAP 117, PLFG 2026, AFT, HCFP 2026-5 et 2026-2) : absente. Commission IP 348 p.47 : « market perceptions of uncertainty surrounding the country's medium-term fiscal outlook and the broader policy environment ahead of the forthcoming national elections » ; HCFP p.14 : « l'incertitude quant à la situation politique » | non vérifiable à ce jour (non vérifié) | non | concordant | Attribution au gouvernement non étayée : le lien est fait par la Commission (en anglais) et le HCFP |
| V5-B6-25 | imprécis (trop général) | cellule (vague 2 §3.1, A08) | « Il ne peut pas créer une dépense, même compensée » | AN rapport n° 1891, p.99 : « il est donc possible pour un député d'augmenter les crédits d'un programme à condition de diminuer d'au moins autant les crédits d'un autre programme de la même mission » (« dérogation majeure à l'article 40 ») | imprécis (trop général) | non | A18 contre A08 | La formule de la V5 (et celle d'A08) omet la faculté de redéploiement au sein d'une mission |
| V5-B6-12 | exact sous condition (exact) | cellule (K-064, A12 : « non vérifiés ») | Chômage suédois de 1996 non vérifié ; série harmonisée 11,7 % | Prop. 1997/98:150, tableau p.7 : chômage déclaré 8,1 % et programmes 4,5 % en 1996 ; OCDE 11,7 % | exact sous condition (exact) | non | A18 (pièce trouvée) | Vérifié en définition nationale de l'époque |
| V5-B6-16 | exact (exact) | cellule (K-064) | Mention écrite du Parti du centre non vérifiée | Prop. 1997/98:150, p.4 : « It would not have been possible without co-operation ... between the Social-Democrats and the centre party » | exact (exact) | non | A18 (pièce trouvée) |  |
| V5-B6-03 | exact sous condition (exact) | cellule (K-064) ; Astra (« détail de l'hôtel ») | Hôtel non vérifié | Reuters 23/10/2025 citant le livre de Persson (1997) | exact sous condition (exact) | non | A18 (source secondaire) | Reste [S] : livre non consulté |
| V5-B5-14 | exact (exact) | cellule (K-066 : « 1962 non vérifié ») | Comparaison avec 1962 non vérifiée | CR AN 4/12/2024 : « le seul premier ministre à être censuré depuis Georges Pompidou en 1962 » ; référence à la motion du 5 octobre 1962 | exact (exact) | non | A18 (pièce trouvée) |  |
| V5-B4-40 | exact (exact) | cellule (K-034 : titre non vérifié) | Titre Pébereau non vérifié | AN rapport n° 2844 (12e lég.), p.4 ; Sénat r05-345 | exact (exact) | non | A18 (source secondaire officielle) | PDF original tronqué |
| V5-B6-06 | imprécis (inexact) | Astra (12¼ % dans le compte de l'époque, dont ≈3 pts bancaires) ; cellule (règle 12 : 10,7 % harmonisé) | Le 12 % existe dans un compte de 1998 ; 10,7 % en comptes harmonisés ; ≈3 pts de soutien bancaire | OCDE (A18) : 10,7 ; FMI 1998 : PDF scanné illisible sans OCR, non vérifié par A18 | imprécis (inexact) | non | concordant (explication par le millésime) | Écart expliqué par la comptabilité de l'époque, non par une invention ; la comparaison avec la France doit se faire en comptes harmonisés |
| V5-B1-16 | exact sous condition (exact) | Astra | Hors soutien bancaire, 9¼ % < 2 × 5,1 : la comparaison « deux fois » disparaît | OCDE 10,7 (tout compris) / 5,1 = 2,1 | exact sous condition (exact) | non | partagé | Exact en solde publié ; le pic comprend une dépense ponctuelle de sauvetage bancaire (≈3 pts selon Astra, non relu par A18) |
| V5-B6-10 | exact (exact) | Astra ; cellule (K-073) | Programme élargi : 52,7 % de coupes (OCDE) ; ministre : presque deux tiers (programme initial) | Persson 1995, p.3 | exact (exact) | non | concordant | La V5 attribue le chiffre au ministre ; exact comme citation, pas comme bilan final |
| V5-B5-05 | exact sous condition (exact) | Astra ; cellule (K-004) | 10 Md€ pour les retraites ; 20 à 24 Md€ toutes APU (Cour, tableau 5) | Cour, février 2025, p.10 (+8 à 14 Md€ hors retraites) | exact sous condition (exact) | non | concordant | Périmètre retraite seul |
| V5-B6-31 | trompeur par périmètre ou juxtaposition (inexact) | Astra ; cellule (K-005) | 10 / 44 / 150 : objets non comparables | Cour 2025 ; DP 15/07/2025 ; Insee | trompeur par périmètre ou juxtaposition (inexact) | non | concordant |  |
| V5-B3-30 | exact (exact) | cellule (K-032) | Méthode de la Cour non publiée ; « sans économies » affirmé, non démontré | Cour juillet 2024, p.35-36 | exact (exact) | non | concordant (nuance) | Exact comme attribution à la Cour ; la Cour n'expose pas le calcul |
| V5-B3-16 | exact sous condition (exact) | cellule (K-029) | « Des trous d'avant » omet l'effet des taux réels élevés | Insee t_3201 | exact sous condition (exact) | non | concordant (nuance) |  |
| V5-B5-29 | exact (exact) | cellule (K-060) | Barnier : un grief parmi sept ; Bayrou : gel des pensions nommé par aucun orateur | Motion du 2/12/2024 ; DP Bayrou 15/07/2025 | exact (exact) | non | concordant | Les faits sont exacts ; la causalité suggérée reste « non démontrée » (B5-30) |
| V5-B2-01 | exact (exact) | cellule (règle 1, K-011) | 151,6 Md€ depuis le compte du 28 août 2026 ; 152,5 en mai | Insee t_3201 (A18 l'avait daté par erreur de mai) | exact (exact) | non | cellule (date) | Correction de la date de millésime dans la passe 1 |
| V5-B3-11 | non vérifiable à ce jour (non démontré) | cellule (S03, recette) | « Les droits continuent sur leur lancée » : exact pour le nombre de retraités et la règle d'indexation, inexact si les pensions ont ignoré le ralentissement | Pièces de S03 non relues par A18 | non vérifiable à ce jour (non démontré) | non | non tranché |  |
| V5-B4-30/B5-33 (révision) | exact (exact) | Astra ; cellule (K-094) | Commission, 17/11/2026 : 5,5 % en 2026 et 5,4 % en 2027 | Commission IP 348, p.139 : « expected to rise to 5.5% of GDP in 2026 » (copie vérifiée par l'orchestrateur) | exact (exact) | oui (ajout) | Astra et cellule | Révision postérieure au script que la passe 1 n'avait pas trouvée : la cible de 5 % reste exacte comme objectif, mais la prévision indépendante la plus récente est 5,4 % |
| S02 Canada | - (-) | plan v2, point 4 | Vérifier les unités de s02_canada.py si la V5 cite le Canada | Lecture de la V5 : aucune mention du Canada | - (-) | sans objet | - | Script S02 non audité : la V5 ne cite pas le Canada (signalement seulement) |
