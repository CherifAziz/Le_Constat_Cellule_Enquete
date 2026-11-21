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
