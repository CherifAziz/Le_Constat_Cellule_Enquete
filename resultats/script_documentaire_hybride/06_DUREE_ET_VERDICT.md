# 06 · Durée estimée et verdict éditorial

**22 novembre 2026.** Version hybride d'*Avant la ligne*, titre de travail. Script : [02_SCRIPT_ANNOTE.md](02_SCRIPT_ANNOTE.md) ; voix seule : [01_SCRIPT_VOIX_OFF.md](01_SCRIPT_VOIX_OFF.md).

## 1. Durée

**4 824 mots dits, durée estimée à 28:42.** Ce chiffre est un calcul : aucun enregistrement n'a été mesuré. Il repose sur les hypothèses suivantes :

- 182 mots par minute ;
- 1 s par (pause) et 2,5 s par (silence) ;
- 0,5 s entre deux paragraphes ;
- 25 s de lecture d'archives sans voix ;
- 4 s de carton de titre et 3 s de silence final.

La voix seule, sans pauses, représente 26:30. Le détail par séquence est dans `durees.json` ; pour le reproduire : `python outils/construire_script.py .`

| Partie | Début | Durée | Part du film |
|---|---|---|---|
| Ouverture et titre | 0:00 | 1:22 | 5 % |
| I · Comment elle s'est enfermée (séq. 1–6) | 1:22 | 6:25 | 22 % |
| II · Les occasions (séq. 7–11) | 7:47 | 4:52 | 17 % |
| III · Le mur (séq. 12–16) | 12:39 | 4:31 | 16 % |
| IV · Ce qui pourrait marcher (séq. 17–23) | 17:10 | 9:07 | 32 % |
| Conclusion et silence final | 26:17 | 2:25 | 8 % |

Les trois questions se partagent le film à peu près ainsi :

- 27 % pour la première (ouverture et acte I) ;
- 33 % pour la deuxième (actes II et III) ;
- 40 % pour la troisième (acte IV et conclusion).

La V6 consacrait tout son temps aux deux premières.

**Écart à la cible.** Le film dure 42 s de plus que les 28 minutes du commanditaire et 52 s de plus que les 27:50 proposées par Astra. La durée réelle dépendra du débit de la voix générée.

Si l'essai de voix confirme le dépassement, voici les coupes possibles, dans l'ordre et sans toucher aux scènes obligatoires :

| Ordre | Coupe | Gain estimé |
|---|---|---|
| 1 | Séq. 11 : les deux dates de décembre 2017 et juin 2018, avec leur image | ≈ 13 s |
| 2 | Séq. 9 : réduire l'Italie à deux phrases (« De 2010 à 2019, avant intérêts, l'Italie est dans le vert dix années sur dix. La France, aucune. ») | ≈ 10 s |
| 3 | Séq. 19 : garder seulement « La méthode suédoise ne promet pas le résultat suédois. » et couper la phrase qui suit | ≈ 6 s |
| 4 | Lectures d'archives : ramener celles de 4 s à 3 s, sauf la page de 1980 | ≈ 2 s |
| 5 | Conclusion : « Quant au rythme… des coûts qu'on subit » (Astra voulait ce passage : c'est le dernier recours) | ≈ 15 s |

Les coupes 1 à 4 ramènent l'estimation vers 28:10. Avec la cinquième, on arrive vers 27:55. La phrase sur la transmission de la TVA aux prix (séq. 21) n'est pas coupable : la consigne exige les mécanismes de transmission.

## 2. Ce que la version contient

- Les trois questions sont posées à l'ouverture, traitées dans l'ordre, puis résumées en conclusion.
- Toutes les scènes demandées sont présentes :
  - l'accroche au présent ;
  - le retournement de 1980 ;
  - la cotisation de 1979 et la page du Sénat ;
  - le démenti des 11 à 15 % ;
  - le printemps 2000 et sa contre-proposition ;
  - septembre 2023 ;
  - la règle de 2005 et les 31 cibles ;
  - la Suède et ses contreparties ;
  - quatre situations concrètes ;
  - la position et son prix.
- Le raisonnement budgétaire d'Astra remplace la jauge :
  - besoin de 135 à 165 Md€, daté et borné ;
  - pente de la dette à +3,8 / +2,0 / +2,6 points ;
  - « ralentit sans stabiliser » ;
  - trois cibles distinctes (stabiliser, 3 %, équilibre).
- La réponse à la question que la V6 laissait ouverte. Pour changer de trajectoire, il faut :
  - freiner les gros postes en nommant ce qui change ;
  - fermer des avantages fiscaux avant les impôts larges, et dire qui sera protégé ;
  - aider ceux qui peuvent rester en emploi ;
  - publier chaque année l'écart entre promesse et exécution.

  Le tout est présenté d'un bloc, avec les payeurs nommés, comme la méthode suédoise. C'est une position, sans proportions ni promesse de résultat.

## 3. Ce qui reste à faire avant l'enregistrement

| Point | Responsable | Bloquant pour l'enregistrement ? |
|---|---|---|
| Sort du PLF et du PLFSS 2027 : si les textes changent, rejouer ensemble le besoin, le portefeuille et la pente ; mettre à jour les cartons datés | Cellule, modèle A15 | **Oui**, si le budget est adopté avant l'enregistrement |
| Relire la page 416 du discours de Persson (objectif du 94 %) et arrêter la traduction des pages 414 et 416 ; la voix suit la traduction | Rédaction | Oui (quelques minutes) |
| Sourcer la une de presse « cagnotte » et la référence de décembre 2018 | Production | Non (image) |
| Mesurer la durée réelle sur l'essai de voix ElevenLabs ; appliquer les coupes du §1 si nécessaire | Production | — |
| Faire passer à un auditeur les trois tests de compréhension d'Astra : la ligne zéro, les payeurs de la TVA et de la CSG, l'objet du 94 % | Production | Recommandé |
| Remplacer les personnages d'illustration par de vrais témoins, si possible | Production | Non |
| Relecture du script complet par l'équipe indépendante (Astra) | Commanditaire | À décider |

## 4. Verdict éditorial

**Première version complète et cohérente, prête pour un essai de voix. Elle n'est pas encore prête pour l'enregistrement définitif.**

Le film tient sa promesse : il raconte comment la France s'est enfermée, pourquoi elle n'en sort pas, et ce qui paraît possible. Chaque révélation importante est appuyée sur une pièce que la contre-expertise valide. Il le fait sans se transformer en rapport : il compte 25 séquences, et chacune dit au plus trois ou quatre chiffres, sans compter les âges et les dates, à l'exception de la séquence 21.

**Plus forte que la V6** :

- le présent dès la première seconde ;
- l'acte III, qui montre ce qui coince aujourd'hui ;
- une réponse concrète à la question de la trajectoire.

**Plus prudente que la V5** :

- pas de « pays qui prélève le plus » en accroche ;
- pas de « deux tiers de coupes » ;
- pas de jauge à trois niveaux ;
- pas de Suède transposée.

**Les trois risques à surveiller** :

1. La densité des séquences 16 et 21. Seul un essai d'écoute dira si elles passent.
2. Le millésime : les chiffres de 2027 bougeront avec le budget.
3. La durée, environ 40 à 50 s au-dessus de la cible.

Aucun de ces risques n'exige de reconstruire le film.
