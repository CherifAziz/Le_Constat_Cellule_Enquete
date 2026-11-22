# Pièces consultées et reproduction

## Refaire le contrôle

Depuis la racine de ce dépôt, avec Git, Python 3.12 et openpyxl 3.1.5 (versions de vérification), exécuter les commandes suivantes. La première rend le commit source disponible dans un clone qui ne contiendrait que la branche de contre-expertise. Le script lit **le hash inscrit dans son code** à travers `git show`. Les valeurs attendues de D08 sont utilisées uniquement pour vérifier les écarts après calcul.

```sh
git fetch origin claude/approfondissements
python -m pip install openpyxl==3.1.5
python resultats/contre_expertise_finale_codex/controles.py --verifier
```

Sans `--verifier`, le script écrit le JSON calculé sur la sortie standard. Avec cette option, il compare toutes les valeurs à [la copie publiée](resultats.json) et s’arrête en erreur en cas d’écart. Le classeur Insee peut provoquer un avertissement openpyxl sur le style par défaut. Le contrôle porte sur les valeurs numériques. [Script indépendant](controles.py)

**Unités.** Les soldes sont signés, en pourcentage du PIB. Les écarts de soldes sont en **points** de PIB. Les heures sont des heures par résident de 15 à 64 ans. Le rapport d’heures entre deux pays est exprimé en pourcentage. Les comptes historiques du régime général sont en francs courants. La conversion légale utilisée est 6,55957 francs par euro. Les six décimales du JSON facilitent la comparaison informatique.

## Corpus épinglé

La référence de lecture est le [commit de Claude du 22 novembre](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/ffb03b64268b8012c0d54b4c8747bf64c1ca5b14/resultats/claude_approfondissements). Le dossier des enquêtes Codex complémentaires est pris à [a337dd3](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/a337dd362251ad9ef72d815d3e60c9378a7043e8/resultats/enquetes_complementaires_codex). Voici les entrées de calcul principales. Les identifiants abrégés sont ceux des blobs Git dans le commit source.

| Donnée | Fichier ou feuille | Identifiant |
|---|---|---|
| Dépense, recettes, intérêts payés D41, B9 et cotisations S13 | Insee 3.201, première feuille, libellés de lignes | `306c8f9a` |
| PIB courant et taux de PO | A04, `a04_po_recettes_1959_2025.csv` | `e789aaac` |
| Dette de Maastricht en milliards d’euros | `base_insee_dette_sous_secteurs.csv`, figure 1, ensemble | `fa8020a8` |
| Mesures nouvelles, une observation retenue par année | `D05_mesures_nouvelles_annuelles.csv`, comparaisons et pages incluses | `c03682af` |
| PIB en volume | Insee T_1102 en niveau, ligne B1GQ | `624d8971` |
| Emploi en ETP | Insee T_1109 en niveau, ligne S13 | `f281af5c` |
| Salaires bruts | Insee T_1107 en niveau, ligne D11 | `19b535a5` |
| Heures intérieures / population de 15–64 ans | AMECO, NLHT en millions / NPAN en milliers × 1 000 | `344c7f36` |
| Productivité par heure | Bergeaud–Cette–Lecat v2.7, Labor Productivity | `c14c41b3` |
| Taux d’emploi en France | Insee Enquête Emploi, T207 (2025), total par âge | `cee15a4f` |

Le registre ci-dessous relie les neuf demandes explicites du §6 aux contrôles réalisés et aux preuves encore nécessaires. Les liens primaires complémentaires figurent auprès de chaque conclusion dans les deux annexes.

| §6 | Sources consultées et décision |
|---|---|
| 1. Persistance fiscale | Trésor DT 2009/13, tableau 3, PDF p. 18. Cour, juin 2010, pp. 14–15 et juin 2011, p. 28. RESF pour 2011, p. 78, pour 2014, pp. 66 et 69 et pour 2016, p. 62. Mesures Insee 2019–2020, Cour 2022 et exécution 2023. Reproduction des 24 combinaisons, retrait de trois flux et sensibilité au report en euros. [Pièces D05](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/ffb03b64268b8012c0d54b4c8747bf64c1ca5b14/resultats/claude_approfondissements/donnees/D05/sources) · [Cour, exercice 2023](https://ccomptes.fr/fr/documents/69436) |
| 2. Décomposition | Insee 3.201 et 1.102. Recalcul à partir du niveau réel du PIB et des dépenses en euros. Confrontation au carré D01 et contrôle par troisième fenêtre et deux ordres de substitution. [Pièces D01](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/tree/ffb03b64268b8012c0d54b4c8747bf64c1ca5b14/resultats/claude_approfondissements/donnees/D01) |
| 3. Cotisation | Sénat n° 54 (novembre 1979), n° 102 et n° 98 (novembre 1980). CCSS juillet 1981, pages PDF 8, 18, 20, lecture du résultat sur le fac-similé p. 18. CCSS juin 1983 pour le rétablissement. IPP pour la publication du décret. Reste le JO lois et décrets du 31 juillet 1979 et le pont RG/ASSO/S13. La recherche par date de Légifrance et par référence n’a pas livré de texte authentifié dans cette consultation. La BnF décrit l’accès aux collections, ce qui rend le contrôle d’archive réalisable. [Guide de la BnF](https://bnf.libguides.com/c.php?g=659907&p=4659963) · [DILA, accès aux pages des JO numérisés](https://www.dila.gouv.fr/institution/presentation/histoire/actualites/toutes-les-actualites/missions-regaliennes/article/consultation-journal-officiel-nouveaute-legifrance) |
| 4. Heures et raccord allemand | AMECO, séries FRA et sept comparateurs, y compris D_W et DEU. Recalcul du raccord, des médianes, des rangs et retrait successif de chaque pays. BCL comme source distincte pour les variations de productivité. Les métadonnées de la Commission distinguent séries anciennes prolongées et données harmonisées plus récentes. [Notice AMECO](https://economy-finance.ec.europa.eu/document/download/ae8a3bbf-7a9c-446c-a91e-e4e4f721c21d_en?filename=Reference+Metadata+AMECO_September+2022.pdf) |
| 5. Cotisations/salaires | Insee 3.201 et 1.107, définition D613, D04 et image CCSS de septembre 2000. Évolution agrégée reproduite. Quantification de la part des compensations, des prestations de remplacement et de la composition des cohortes encore ouverte. [Insee, D613](https://www.insee.fr/fr/metadonnees/definition/c2275) |
| 6. Effectifs | Tableau Insee 1.109, D03 et fac-similé DGAFP, p. 10. Les deux séries DGAFP, avec et sans P et T, et la variation des trois versants sont distinguées. L’explication de l’écart au niveau S13 exige un tableau de passage. [DGAFP, image conservée](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/ffb03b64268b8012c0d54b4c8747bf64c1ca5b14/resultats/claude_approfondissements/donnees/D09/images/a7_dgafp_p10.png) |
| 7. Transcriptions | Contrôles ciblés sur deux lois de finances (seuils d’IR), barème maladie, scans CCSS 1980 et 2000 et crédits des nationalisations. Les deux scans originaux de crédits sont aux pages PDF 75 et 102. Le bulletin des commissions fixe le niveau de départ de 1982. Les autres transcriptions manuelles, dont le total des taux sous plafond et les anciens tableaux de CCSS, gardent le degré de preuve de leurs pièces individuelles. [Annexe historique](histoire_et_fiscalite.md#transcriptions-et-décisions-politiques) |
| 8. Inventaire D05 | LFR 2000, création de la prime pour l’emploi en 2001, LFR 2002, règlement du budget et rapport Carrez. Pour les trois mesures prioritaires, vérification du vote, de l’assiette ou de l’exercice et du périmètre. Le coût d’une année de montée en charge ne doit pas être reporté comme coût de l’année du vote. Les autres champs, en particulier incidence économique finale et contrepartie de chaque mesure, restent à vérifier ligne à ligne. [Rapport Carrez, n° 2689](https://www.assemblee-nationale.fr/13/pdf/rap-info/i2689.pdf) |
| 9. Études d’emploi | Lecture des estimations dans l’étude Delalande et de la méthode Alsace-Moselle confrontée à sa réplication. Ajout de trois évaluations primaires sur Fillon, la bascule de 2019 et l’apprentissage. L’absence d’un chiffrage du rendement budgétaire national reste un constat sur le corpus examiné. [Évaluations et liens directs](travail_et_confrontation.md#ce-que-mesurent-les-évaluations-demploi) |

**Portée de la vérification D09.** Le rapport Carrez chiffre les baisses nettes d’impôts de l’État en 2009, hors relance, à 68–78 Md€. La fourchette élargie de 101–119 Md€ inclut des changements de périmètre. D09 montre la répétition d’une ligne entre les pages 7 et 10. **Validée sous condition** pour l’estimation plus étroite, **indécidable** pour la reconstitution du total large sur ce seul tableau. Le scénario de gage systématique de Carrez rapporte 54,6 % de dette contre 77,4 % estimés alors et un déficit de 3,7 % en 2009. D’autres recettes ou une dépense moindre auraient constitué le gage. Ce scénario diffère du retrait des mesures de toutes les APU opéré dans D08 jusqu’en 2025. Les chiffres de Champsaur–Cotis et de la Cour sur les années 2000 confortent le sens général de l’impulsion fiscale, avec d’autres conventions. Trois rapports officiels ne constituent pas trois expériences indépendantes. [Pages 7, 10, 13 et 16 du rapport Carrez](https://www.assemblee-nationale.fr/13/pdf/rap-info/i2689.pdf) · [D09, contrôle des pièces](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/ffb03b64268b8012c0d54b4c8747bf64c1ca5b14/resultats/claude_approfondissements/dossiers/D09.md)
