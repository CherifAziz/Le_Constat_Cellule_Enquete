# 07 · Texte ElevenLabs — *Avant la ligne* (version hybride)

Extrait automatiquement de [01_SCRIPT_VOIX_OFF.md](01_SCRIPT_VOIX_OFF.md) par `outils/preparer_elevenlabs.py`. Ne pas modifier à la main : corriger 02, puis relancer `construire_script.py` et ce programme.

## Réglages

- **Modèle** : Eleven v3 (ou v4), le même pour tous les blocs.
- **Voix** : voix masculine française de narration, la même pour tous les blocs.
- **Stabilité** : « Natural ». Éviter « Creative », qui laisse plus de liberté d'interprétation (chuchotements, souffle).
- **Vitesse** : 1,0. La durée du script est calculée à 182 mots par minute ; noter la vitesse retenue.
- **Un bloc par génération**, dans l'ordre ; nommer chaque fichier par son numéro (`01_ouverture.mp3`…).
- Si un bloc sort trop bas ou soufflé, le régénérer tel quel ; ne jamais ajouter de balise d'émotion douce.

## Ce qui a été fait au texte

- Aucun mot dit n'a été changé.
- `(pause)` → `[short pause]` ; `(silence)` → `[long pause]`.
- Pourcentages, décimales, milliers, « 1er » et « 49.3 » écrits en toutes lettres. Les années restent en chiffres.
- Chaque bloc commence par `[steady, full-voiced male documentary narrator]` puis une balise de ton.
- **Balises exclues** (contrôle automatique) : tout ce qui contient « whisper », « soft », « quiet », « hush », « murmur », « breath », « intimate », « low voice », « mysterious », « secret », « sigh », « exhale », « asmr », « gentle », « sleepy », « tired », « sad », « somber », « sombre », « melanchol », « fragile », « trembl », « nervous », « cry », « sob ». Pas de points de suspension.

---

## 01 · Ouverture

```text
[steady, full-voiced male documentary narrator] [confident, engaging, clear]

Cinquante et un ans. [short pause] Depuis 1975, pas une seule année, les comptes publics de la France n'ont été à l'équilibre. Ni sous la gauche, ni sous la droite, ni sous le centre.

En 2025, sur 100 euros de dépense publique, près de 9 n'étaient pas couverts par les recettes.

Et le 4 novembre 2026, à l'Assemblée, la partie recettes du budget de l'année suivante a été rejetée en première lecture. 458 voix contre. [short pause] Zéro pour.

On entend souvent que ce pays ne sait pas faire. Que ses comptes dérivent depuis toujours.

Alors regarde cette barre-là. 1980. Il ne manque presque rien à la France pour être à l'équilibre : zéro virgule quatre pour cent de ce qu'elle produit en un an. Depuis, elle n'est jamais repassée aussi près.

Et dans les archives du Sénat, il y a une page, imprimée en novembre 1980, qui annonce que les comptes de la Sécurité sociale vont replonger. Elle dit même pourquoi. [short pause] On va la lire ensemble.

Ce documentaire cherche à répondre à trois questions. Comment la France s'est enfermée dans cinquante et un ans de déficits. Pourquoi elle n'arrive pas à en sortir. Et ce qui pourrait marcher, à quel prix. [short pause] Sur la dernière, on ne s'arrêtera pas à une liste. On dira ce qui nous paraît le plus crédible. Et pourquoi.
```

## 02 · Les ciseaux

```text
[steady, full-voiced male documentary narrator] [clear, explanatory]

1974. Les comptes publics sont encore très légèrement excédentaires. C'est la dernière fois. En 1975, avec la récession qui suit le premier choc pétrolier, ils plongent.

L'explication la plus répandue : après le choc, l'État aurait ouvert les vannes. Les comptes disent autre chose. Dans les années soixante, la dépense publique progresse d'un peu moins de sept pour cent par an, inflation déduite. Après le choc, d'un peu moins de 5. [short pause] Elle n'accélère pas. Par rapport aux dernières années d'avant-crise, elle garde simplement son rythme.

Ce qui casse, c'est la croissance. Elle est divisée par plus de deux.

Une dépense lancée, une économie qui freine : les deux lignes s'écartent. Depuis 1974, la dépense publique prend une part de plus en plus grande de la richesse du pays. Et les quatre cinquièmes de cette montée, jusqu'à aujourd'hui, sont faits dès 1985.

D'où vient cet élan ? Plusieurs règles de prestations avaient été écrites avant la crise, quand l'argent rentrait tout seul. D'autres décisions s'y ajoutent. Un exemple : les préretraites. L'accord qui les lance date de 1972. En 1973, elles ne pèsent presque rien dans les comptes. En 1985 : huit fois plus.
```

## 03 · La remontée

```text
[steady, full-voiced male documentary narrator] [clear, explanatory]

Avec une dépense sur sa lancée et une croissance cassée, le trou devrait se creuser chaque année. C'est l'inverse. De 1975 à 1980, la France refait presque tout le chemin.

Comment ? Regarde la Sécurité sociale. Son régime général, celui des salariés, finit 1978 avec près de 11 milliards de francs de déficit. Quatre plans en quatre ans, et à chaque fois, on relève les cotisations. Par décret. Sur la dernière ligne droite, de 1978 à 1980, les administrations de sécurité sociale font plus de la moitié du redressement. L'État, environ un huitième.

En 1980, si l'on met de côté les intérêts de la dette, la France encaisse plus qu'elle ne dépense. [short pause] Elle sait donc se redresser. Elle l'a fait en prélevant plus. Et une partie de ce redressement tient à une recette qui a une date de fin.
```

## 04 · Trente francs

```text
[steady, full-voiced male documentary narrator] [curious, investigative]

Été 1979. Le gouvernement de Raymond Barre annonce un nouveau plan pour la Sécurité sociale. Dedans, une cotisation maladie supplémentaire : un pour cent du salaire. Le Sénat a conservé le tableau qui montre ce que ça change. Pour une paie de trois mille francs par mois : 30 francs de moins.

Mais ce n'est pas le montant qui compte. C'est ce qui est écrit au-dessus du tableau. [long pause] Premier août 1979. 31 janvier 1981. Cette cotisation est créée pour dix-huit mois. Sa fin est écrite le jour de sa naissance.

Le décret lui-même, on ne l'a pas retrouvé. Mais deux rapports du Sénat le citent, avec son numéro et ses dates.

1980. La Sécurité sociale des salariés, dans le rouge deux ans plus tôt, termine l'année avec un excédent d'un peu moins de 11 milliards de francs. D'où vient-il ? La Commission des comptes de la Sécurité sociale l'écrit un an plus tard : ce résultat « tenait toutefois presque entièrement à la cotisation exceptionnelle ». On a refait le calcul : quatre-vingt-huit pour cent de cet excédent-là. L'excédent du régime général, pas tout le redressement du pays.

Mais l'année où la France passe le plus près de l'équilibre, le matelas de sa Sécurité sociale tient à une recette qui va s'arrêter. Et la date approche.
```

## 05 · Novembre 1980

```text
[steady, full-voiced male documentary narrator] [deliberate, reading an official document aloud]

Novembre 1980. L'élection présidentielle est dans six mois. Au Sénat, on examine les comptes de la Sécurité sociale. Voici la page. [long pause]

« Cette contribution des salariés sera supprimée à la fin du mois de janvier 1981. Dans ces conditions, l'exercice 1981 devrait se traduire par un déficit de trois virgule deux milliards de francs. »

C'est imprimé. Chiffré. Public. Le retour du déficit de la Sécu n'est pas une surprise de 1981. C'est une prévision de 1980.

Prolonger la cotisation, c'était possible : depuis cinq ans, on relevait les cotisations par décret. Ça n'est pas fait. Pourquoi ? On n'a trouvé qu'une ligne, dans le rapport du Sénat sur le budget de 1981 : la fin de la cotisation y est rangée parmi les mesures « en faveur de la consommation ».

À six mois d'une présidentielle, tu penses peut-être à autre chose. Aucun document ne le dit, et on ne le dira pas à sa place. Ce que montrent les archives, c'est une décision. Pas un mobile.

Le premier février 1981, la cotisation s'arrête. Au jour dit. À la fin de l'année, le déficit de la France a été multiplié par plus de cinq.

On tient le coupable ? [long pause]
```

## 06 · Faisons le compte

```text
[steady, full-voiced male documentary narrator] [matter-of-fact, firm]

Non. [short pause] Faisons le compte. Si l'on compte simplement les neuf mois de recette perdus, la fin de la cotisation représente 11 à quinze pour cent de la dégradation des comptes de 1981. Moins d'un sixième. Elle a compté. Elle n'a pas fait plonger la France.

Alors c'est la gauche, arrivée en mai ? Depuis quarante ans, on répète : la relance, la retraite à 60 ans. Regarde les dates. La retraite à 60 ans du régime général entre en vigueur le premier avril 1983. Elle ne peut pas avoir creusé le déficit de 1981.

Le chômage, lui, montait déjà en 1980. Et le nouveau gouvernement engage, dès juin, des dépenses dont une partie n'a aucune recette en face. Ce n'est donc pas l'héritage ou la gauche. C'est l'héritage et la gauche, dans une économie qui se dégrade. Quelle part pour chacun ? Les comptes de l'époque ne permettent pas de le dire.

Un dernier détail. En novembre 1981, le gouvernement de Pierre Mauroy rétablit la cotisation. [short pause] Neuf mois après.
```

## 07 · Ce que ces années laissent

```text
[steady, full-voiced male documentary narrator] [warm, explanatory]

Ces années laissent deux héritages. Ils pèsent encore aujourd'hui.

Le premier, c'est un homme de 57 ans, en 1982. Son usine réduit ses effectifs. On lui propose de partir, avec un revenu garanti jusqu'à la retraite. Pour lui, c'est une protection. Pour un pays où le chômage explose, ça ressemble à une solution.

Maintenant, multiplie cet homme à l'échelle du pays. En 1975, quatre Français sur dix âgés de 60 à 64 ans ont un emploi. En 2001 : un sur dix. Or ce qui finance les retraites, la santé et les allocations est en grande partie prélevé sur le travail. Cette base-là s'est rétrécie. [short pause] Garde cet homme en tête. On le retrouvera.

Le second héritage, c'est la facture. Les déficits contribuent à augmenter la dette, et la dette se paie en intérêts. Entre 1974 et 1996, le poids des intérêts dans la richesse du pays est multiplié par six.

Voilà comment elle s'enferme. Une croissance qui casse, une dépense qui garde son élan. Un redressement réel, mais par les prélèvements, et en partie grâce à une recette provisoire. Et des intérêts qui, chaque année, rendent l'année suivante un peu plus difficile.
```

## 08 · Dos au mur

```text
[steady, full-voiced male documentary narrator] [energetic, clear]

1993. Récession. Le déficit le plus élevé depuis 1975, du moins jusque-là. Et contrairement à la légende d'un pays qui ne fait jamais rien, il se passe des choses. En pleine récession, on fait plus que doubler la CSG, ce prélèvement qui touche presque tous les revenus. On allonge la durée de cotisation pour la retraite. Puis vient une échéance : l'entrée dans l'euro.

Mets de côté les intérêts, comme pour 1980. 1998, 1999, 2000, 2001 : la France encaisse plus qu'elle ne dépense, quatre années de suite. Ce qui la maintient dans le rouge, c'est la facture du passé. [short pause] Vingt ans après 1980, elle s'approche de nouveau de la ligne. Et cette fois, l'argent tombe du ciel.
```

## 09 · Printemps 2000

```text
[steady, full-voiced male documentary narrator] [curious, investigative]

Printemps 2000. L'économie tourne à plein régime. Le gouvernement de Lionel Jospin revoit les recettes de l'État à la hausse : 51 milliards de francs de plus que prévu. On l'appelle la cagnotte.

Qu'est-ce qu'on en fait ? En 1980, il a fallu chercher le motif. En 2000, il est imprimé. Le projet de loi du 26 avril traduit, je cite, « la volonté du Gouvernement de restituer aux Français une partie des fruits de la croissance ». [long pause]

Les quatre cinquièmes partent en baisses d'impôts : la TVA perd un point, l'impôt sur le revenu et la taxe d'habitation baissent. Le reste, en dépenses. Le déficit du budget de l'État est maintenu, dit le texte, « à un niveau inchangé ». Et une partie de cette recette y est classée exceptionnelle : elle ne reviendra pas.

Une autre voie existait. Elle est imprimée aussi. Au Sénat, la commission des finances, tenue par l'opposition, propose de financer les dépenses nouvelles par des économies, et de réduire le déficit. Le dernier mot revient à l'Assemblée. La proposition reste sur le papier.

Alors, est-ce là que la France a raté l'équilibre ? [short pause] Non. Si le gouvernement avait tout gardé, jusqu'au dernier franc, la somme aurait couvert environ quatre euros sur dix du déficit public de l'année. Même pas la moitié. Et encore, à activité inchangée. Cette année-là, le déficit a d'ailleurs encore diminué.

Mais le gouvernement a choisi de rendre une partie de la bonne surprise, quand il pouvait en consacrer davantage à réduire le déficit. Un choix défendable : en six ans, le poids des recettes publiques avait nettement monté. Mais un choix. Daté. Signé. [short pause] Et cette question, qu'est-ce qu'on fait d'une bonne surprise, la France va bientôt se la reposer. Par écrit.
```

## 10 · La colonne éteinte

```text
[steady, full-voiced male documentary narrator] [matter-of-fact, firm]

Deux ans plus tard, la croissance est retombée. En 2002, avant même de payer les intérêts de sa dette, la France dépense de nouveau plus qu'elle n'encaisse. Et cette fois, dans notre série, elle n'en ressort plus. Une seule année est pratiquement à zéro : 2006. [short pause] Vingt-quatre ans.

Et ça n'a rien d'automatique. Prends l'Italie. De 2010 à 2019, avant intérêts, elle est dans le vert dix années sur dix. La France, aucune. L'Italie n'est pas un modèle : sa dette est plus lourde et sa croissance à l'arrêt. Mais justement : même avec ce poids-là, on peut encaisser plus qu'on ne dépense, avant intérêts. Sa dette, pourtant, a continué de monter.
```

## 11 · Les promesses écrites

```text
[steady, full-voiced male documentary narrator] [firm, slightly ironic]

La question du printemps 2000, la France se l'est donc reposée. Par écrit. En 2005, elle inscrit au sommet de son droit budgétaire une règle : chaque budget dira à l'avance ce qu'on fera des impôts qui rentrent mieux que prévu. Et pendant des années, la réponse est la même : ils iront réduire le déficit.

En 2019, la Cour des comptes va voir ce que cette règle a donné. Dans les documents qu'elle examine, elle ne trouve « aucune occurrence de mise en œuvre ». [short pause] Une simple loi votée en cours d'année suffit à passer outre.

Il y a d'autres engagements écrits. Depuis fin 1998, la France annonce régulièrement, à Bruxelles et à son Parlement, où en sera son déficit trois exercices après l'année du budget qu'elle présente. Trente et une de ces cibles sont arrivées à échéance. [short pause] Les trente et une ont été manquées.

Et voici cinq années annoncées pour revenir au moins à l'équilibre, par des gouvernements de gauche, de droite et du centre. 2005. 2010. 2012. 2016. 2022. [short pause] Aucune n'a été tenue.

Un écart ne dit pas pourquoi il s'est produit. Une prévision trop optimiste, une crise, une décision nouvelle : tout s'y mélange. Mais une chose est établie. Écrire un engagement ne suffit pas à le tenir.
```

## 12 · Troisième fois

```text
[steady, full-voiced male documentary narrator] [clear, brisk]

2011. La zone euro vacille. La France est sous surveillance européenne. Dos au mur, troisième fois. Et troisième redressement. Comment ? Comme à la fin des années soixante-dix, d'abord par les recettes : de 2011 à 2014, elles font environ quatre cinquièmes de l'effort budgétaire mesuré.

Puis deux dates. Décembre 2017 : le Parlement vote des baisses d'impôts pour 2018. Juin 2018 : la procédure européenne prend fin. [short pause] Les baisses d'impôts étaient votées avant même la fin de la surveillance.

Cinquante et un ans, trois redressements. À chaque fois, une contrainte : un régime général dans le rouge, l'euro, la surveillance européenne. Et deux fois sur trois, surtout en prélevant plus. [short pause] Alors pourquoi ne pas recommencer ?
```

## 13 · Le levier déjà tiré

```text
[steady, full-voiced male documentary narrator] [direct, clear]

En partie, parce que c'est déjà fait. Pour 2025, de nouveau sous procédure européenne, la France annonce 23 milliards d'euros de mesures de recettes. Dont une contribution sur les bénéfices des grandes entreprises.

Et elle part de haut. En 2025, avec quarante-six pour cent de sa richesse en impôts et cotisations, elle est au premier rang des vingt-sept pays de l'Union. Refermer tout le déficit de cette année-là par les seuls prélèvements la porterait autour de cinquante et un pour cent. Par la seule dépense, sa dépense publique resterait au-dessus de la moyenne de la zone euro.

Ni l'un ni l'autre n'est impossible sur le papier. Mais chacun fait porter tout l'effort sur un seul côté du budget. Regardons donc où va l'argent.
```

## 14 · Où est l'argent

```text
[steady, full-voiced male documentary narrator] [direct, clear]

On pense d'abord au train de vie de l'État, aux agences. Le Sénat a fait le calcul pour les fonctions support des opérateurs de l'État : en les réduisant d'un cinquième, on économiserait au mieux un demi-milliard. [short pause] L'argent est ailleurs. En 2024, sur 100 euros de dépense publique, 57 vont à la santé et à la protection sociale. Les retraites en tête.

Toute économie importante touche donc quelqu'un. Un retraité, un malade, une famille. Et ce quelqu'un le sait tout de suite.
```

## 15 · Septembre 2023

```text
[steady, full-voiced male documentary narrator] [direct, clear]

Exemple : la réforme des retraites de 2023, qui repousse l'âge de départ de 62 à 64 ans. Regarde le calendrier. Dès septembre, ceux qui comptaient partir doivent attendre. Eux savent tout de suite ce qu'ils perdent. Le gain, lui, monte lentement : pour les régimes de retraite, il n'atteint une dizaine de milliards par an qu'en 2030, d'après les chiffrages cités par la Cour des comptes. [short pause] Le prix politique se paie tout de suite. Le gain chiffré, sept ans plus tard. Après l'élection suivante.

La réforme passe sans vote à l'Assemblée, avec le quarante-neuf trois. La motion de censure qui suit échoue à neuf voix.

Et fin 2025, sa montée en charge est suspendue. Jusqu'en 2028. Après la présidentielle.
```

## 16 · L'effort retiré

```text
[steady, full-voiced male documentary narrator] [firm, matter-of-fact]

On accuse souvent le blocage. Et il pèse. Le 4 novembre 2026, avant le vote qu'on a vu au début, les députés avaient réécrit la partie recettes du budget. Selon le ministre, sur 26 milliards de dégradation du texte, 16 venaient de prélèvements retirés en séance.

Mais le recul n'a pas besoin d'une Assemblée divisée. Décembre 2018, au plus fort de la crise des gilets jaunes. Le gouvernement dispose d'une majorité absolue. En quelques jours, il renonce à la hausse de la taxe sur les carburants, à une partie de la hausse de CSG des retraités, et ajoute des dépenses nouvelles. Coût prévu pour 2019 : plus de 6 milliards, une fois déduites les compensations annoncées.

Et pour quarante-deux de nos cinquante et un budgets, le camp du gouvernement est classé majoritaire à l'Assemblée, seul ou avec ses alliés. Les quarante-deux années ont fini en déficit. [short pause] Le blocage complique le problème d'aujourd'hui. Il n'a pas créé celui d'hier.
```

## 17 · Le compte

```text
[steady, full-voiced male documentary narrator] [measured, precise, clear]

Alors, quelle est la taille du problème ? Prenons un objectif modeste : qu'en 2030, la dette cesse de grossir plus vite que l'économie. Pas la rembourser. Juste arrêter la hausse de son poids. En partant d'un scénario sans nouvelles mesures, il faudrait que les décisions prises d'ici là rapportent, en 2030, entre 135 et 165 milliards d'euros par an, à la taille de l'économie de 2025. [short pause] Pas 165 milliards de plus chaque année. Un niveau, atteint par étapes. Puis tenu.

Attention : stabiliser la dette, ce n'est ni passer sous trois pour cent de déficit, ni revenir à l'équilibre. Ce sont d'autres cibles. L'équilibre coûterait bien davantage.

Maintenant, prenons les mesures chiffrées qu'on a pu rassembler, dans le projet de budget, chez la Cour des comptes, dans nos dossiers. Sans les compter deux fois, on les fait passer dans un même modèle. Regarde une seule chose : de combien la dette monte entre 2029 et 2030. Le but, c'est zéro.

Sans nouvelles mesures : près de quatre points de PIB, en une seule année. [short pause] Avec tout le portefeuille central, appliqué jusqu'au bout : deux points. Et dans une hypothèse où une partie seulement est appliquée : environ deux et demi. [long pause]

Ce ne sont pas des prédictions. Ce sont des simulations, avec leurs hypothèses. Mais elles disent une chose importante. Ces mesures ne sont pas rien : elles ralentissent nettement la hausse. Et pourtant, même appliquées jusqu'au bout, la dette continue de monter. [short pause] Le compte n'y est pas encore.

Alors une question devient inévitable. Un pays démocratique, dirigé par un gouvernement minoritaire, a-t-il déjà réussi un effort de cette ampleur ? [short pause] Oui. Et il visait plus haut que nous ici : pas seulement arrêter la hausse de sa dette, mais revenir à l'équilibre.
```

## 18 · Stockholm

```text
[steady, full-voiced male documentary narrator] [engaged storytelling]

La Suède, au début des années quatre-vingt-dix. Une crise bancaire, une récession brutale. En 1993, son déficit public dépasse dix pour cent de sa richesse. Plus du double du déficit français de 2025.

Octobre 1994. Göran Persson devient ministre des Finances d'un gouvernement social-démocrate minoritaire. Un de ses conseillers racontera plus tard un détail. Dans le bureau du ministre, comme dans celui du Premier ministre, un téléviseur reste allumé sur une page de télétexte : l'écart entre les taux suédois et allemands à cinq ans, mis à jour minute par minute. [short pause] Le prix de la défiance, en direct.

Le plan mêle économies et hausses d'impôts. Et Persson ne promet pas qu'il sera indolore. Sa consigne, il la donnera lui-même devant des banquiers centraux : « Ne dites jamais que ça ne fera pas mal. »

Son gouvernement n'a pas la majorité. À partir du printemps 1995, il s'appuie sur le Parti du centre, un parti de l'autre bloc. En août 1995, Persson affirme que quatre-vingt-quatorze pour cent du Parlement soutiennent l'objectif de redressement. [short pause] L'objectif. Pas chaque coupe. On se dispute sur les moyens. Pas sur le but.

Le programme est renforcé plusieurs fois. En avril 1996, il atteint huit pour cent de la richesse du pays : à peu près moitié en économies, moitié en recettes. En 1997 s'appliquent les premiers plafonds de dépenses, votés à l'avance. [short pause] En 1998, les comptes suédois sont en excédent.
```

## 19 · Le vent dans le dos

```text
[steady, full-voiced male documentary narrator] [honest, matter-of-fact]

Mais la Suède n'a pas fait ça seule. En novembre 1992, sa monnaie a été laissée flottante. Elle a perdu environ un cinquième de sa valeur. Ses produits deviennent moins chers à l'étranger, au moment où ses marchés extérieurs grossissent d'environ 7 à dix pour cent par an. Et une partie du déficit de départ venait du sauvetage des banques : une dépense ponctuelle, qui s'éteint d'elle-même.

Et ces années sont dures. Le chômage reste au-dessus de dix pour cent jusqu'en 1997. L'emploi des jeunes recule fortement au cours de la décennie : crise et plan sont mêlés, impossible de faire la part de chacun. Ce que le conseiller de Persson attribue au plan : quand les budgets locaux sont comprimés, les collectivités locales coupent dans l'école, les soins, la garde des enfants. En 1998, le parti de Persson perd près de neuf points aux élections, sans qu'on sache quelle part revient aux coupes. Il reste au pouvoir.

Une précision, contre une idée répandue. La célèbre réforme suédoise des retraites entre en vigueur en 1999. Ses effets sur les pensions versées viennent après ce redressement.

Et la France n'a pas de couronne à laisser glisser : elle est dans l'euro. Elle ne commande ni les taux de la Banque centrale européenne, ni la croissance de ses voisins. Et elle part d'une dette bien plus lourde.
```

## 20 · Ce qui se transpose

```text
[steady, full-voiced male documentary narrator] [thoughtful, clear]

Alors qu'est-ce qui reste, quand on retire le vent ? Une méthode. Persson en donnait trois conditions. Un effort réparti équitablement. Un plan présenté d'un seul bloc, pour que chacun voie qu'il n'est pas le seul à payer. Et tout mettre sur la table : les hypothèses, les calculs, les mauvaises nouvelles.

Et les fameux plafonds de dépenses ? Ils s'appliquent quand l'essentiel de l'amélioration est déjà fait. Ce n'est donc pas leur application qui a fait l'essentiel du redressement. Ils ont servi d'outil de suivi pour la suite.

La méthode suédoise ne promet pas le résultat suédois. Elle montre comment on peut demander un effort à tout un pays, sans que chacun le défasse dans son coin. [short pause] Retour en France. Quatre situations. Pour chacune, trois questions : qui paie ? Quand est-ce que ça rapporte ? Et comment saura-t-on que c'est tenu ? Puis la meilleure objection.
```

## 21 · Une pension

```text
[steady, full-voiced male documentary narrator] [concrete, conversational]

Première situation : une pension de mille trois cents euros par mois. Imagine qu'une année, elle ne soit pas revalorisée, alors que les prix montent de deux pour cent. Sur le bulletin, rien ne change. Au supermarché, elle perd environ 26 euros de pouvoir d'achat chaque mois. Et sauf rattrapage, ce retard se garde les années suivantes.

Pour les comptes publics, c'est une économie rapide : elle joue dès le premier versement. Un gel d'un an des pensions de base et de plusieurs prestations rapporterait de l'ordre de quatre milliards et demi par an en 2030, s'il n'est ni retiré, ni rattrapé.

Qui paie ? Les retraités, bien sûr. Mais pas d'abord les plus aisés. Prends un gel des seules pensions, simulé par l'Institut des politiques publiques. D'après nos calculs sur ses résultats, si l'on range les ménages du plus modeste au plus aisé, selon leur niveau de vie : près de quatre euros sur dix de l'effort pèsent sur la moitié la plus modeste. Et près d'un euro sur deux, sur les quatre dixièmes juste au-dessus.

Une autre règle épargnerait les petites pensions : ne freiner, plusieurs années de suite, que les pensions au-dessus d'environ mille deux cent soixante euros. Elle rapporterait autour de deux milliards en 2030, à la taille de l'économie de 2025.

Attention aussi aux fausses économies : moins rembourser un soin, c'est souvent déplacer la dépense vers les ménages et leurs mutuelles. Et baisser la dotation d'une commune n'économise rien si la commune ne dépense pas moins. [short pause] La meilleure objection, enfin, c'est l'histoire récente : ces gels ont déjà été retirés, ou rattrapés. Une économie qu'on défait l'année suivante n'en est pas une. Pour le savoir, il faudra regarder les bulletins des années suivantes.
```

## 22 · Une addition

```text
[steady, full-voiced male documentary narrator] [concrete, conversational]

Deuxième situation : une addition de restaurant. La TVA y est réduite, à dix pour cent. C'est un avantage fiscal, et la Cour des comptes a chiffré son retour au taux normal, avec celui de certains services à la personne. Si tout était répercuté, un repas de 30 euros passerait à près de 33.

Mais rien ne dit que tout le serait. Quand cette TVA avait été baissée, en 2009, une étude a estimé qu'environ cinquante-six pour cent du gain était allé aux propriétaires des restaurants, pas aux clients. [short pause] Ce qui ne dit pas ce que ferait une hausse. Ça se mesure après coup : sur les prix des cartes, mais aussi sur les marges et les salaires.

Fermer ces avantages un par un rapporte en général quelques milliards à chaque fois. Si l'on veut davantage, on arrive aux impôts de tout le monde. Et il faut savoir lequel, parce qu'ils ne frappent pas les mêmes.

Prends un ticket de caisse. Un point de plus sur le seul taux normal de TVA rapporterait environ sept milliards et demi d'euros, en année pleine. Les commerçants la collectent ; selon la concurrence, elle se partage entre les prix, les marges, les salaires. Si elle passe dans les prix, un ménage qui dépense presque tout ce qu'il gagne la sent davantage, en proportion de son revenu.

Prends maintenant une fiche de paie. La CSG y est prélevée, comme sur les pensions et les revenus du capital. Sur deux mille euros soumis à la CSG, un demi-point de plus, c'est 10 euros de moins par mois. Et pour les comptes publics, en théorie, un montant du même ordre que la TVA. Une pension exonérée peut rester protégée ; les revenus du capital concentrent davantage l'effort chez les plus aisés. Mais les salariés modestes, eux, paient.

On peut compenser : un versement ciblé vers les ménages modestes coûte environ deux milliards dans notre exemple, à condition qu'il les atteigne vraiment. [short pause] Et la meilleure objection est là : dans les deux cas, une partie du rendement se perd en route. Moins de consommation, des prix qui montent et des prestations qui suivent, une activité qui ralentit. Personne ne sait d'avance combien il en restera.
```

## 23 · Deux personnes de soixante ans

```text
[steady, full-voiced male documentary narrator] [concrete, warm]

Troisième situation. Tu te souviens de l'homme de 57 ans, en 1982, à qui l'on proposait de partir ? Aujourd'hui, c'est l'inverse. Entre 60 et 64 ans, un peu plus de quatre Français sur dix ont un emploi. En Allemagne, près de sept sur dix.

Plus de gens en emploi, c'est plus de cotisations, plus d'impôts, moins de prestations. Et il y a une preuve, ce qui est rare. Après la réforme de 2010, qui a reculé l'âge de 60 à 62 ans, la probabilité d'être en emploi à 60 ans a gagné entre 16 et 17 points pour les premières générations concernées.

Mais regarde les deux personnes. La première avait un poste : elle le garde plus longtemps. C'est de là que vient une grande partie de l'effet. La seconde avait déjà perdu le sien, ou ne pouvait plus le tenir : pour elle, reculer l'âge, c'est prolonger le chômage ou l'inactivité. [short pause] L'âge se vote. Un poste adapté, une santé qui tient, un employeur qui garde ses salariés âgés : ça ne se vote pas.

C'est pour ça qu'on ne peut pas inscrire ce levier comme une recette garantie. Il rapporte en années, pas en mois. Et il se mesure au nombre de personnes qui restent réellement en poste, aux heures, au chômage, à l'invalidité. Pas à l'âge écrit dans la loi.
```

## 24 · Quatorze ans plus tard

```text
[steady, full-voiced male documentary narrator] [firm, clear]

Quatrième situation : une promesse, et le jour où on la contrôle. Tu la connais : la règle de 2005 sur les bonnes surprises. En 2019, quatorze ans plus tard, la Cour des comptes n'en trouve aucune mise en œuvre dans les documents qu'elle examine.

Tenir un engagement, ça ne se décrète pas. Mais ça se vérifie. Et pas tous les quatorze ans : chaque année. Depuis 2012, un mécanisme oblige déjà à expliquer un écart important. Pas à le combler. Imagine un document public, avant chaque vote du budget : ce qui était promis, ce qui a été fait, l'écart, et ce qu'on décide pour le combler. Derrière, un plafond de dépenses voté pour plusieurs années, avec une marge pour les chocs, et une règle connue d'avance pour les recettes surprises. Avec la Sécurité sociale et les collectivités dedans, pour qu'aucune charge ne se cache en changeant de caisse.

Est-ce que ça rapporte ? [short pause] Pas un euro. Une règle n'économise rien par elle-même. Elle permet de savoir si les autres euros sont au rendez-vous. Et sa limite est connue : en France, une loi votée plus tard peut défaire une programmation. Sans accord sur le but, aucun tableau ne tiendra.
```

## 25 · Conclusion

```text
[steady, full-voiced male documentary narrator] [firm, measured, conclusive]

Alors, qu'avons-nous trouvé ?

La France s'est enfermée quand sa croissance a cassé et que sa dépense a gardé son élan. Elle s'est redressée trois fois, sous contrainte, souvent en prélevant plus, sans jamais repasser la ligne. Et ses engagements écrits n'ont pas tenu.

Aujourd'hui, aucun levier ne suffit seul sans faire payer toujours les mêmes. Et même les trente-huit mesures du portefeuille central, réunies, ralentissent dans nos simulations la hausse de la dette sans encore l'arrêter.

Voici ce qui nous paraît le plus crédible. C'est une position, pas un calcul.

Freiner les gros postes, en disant chaque fois quel revenu ou quel service change. Fermer des avantages fiscaux avant de toucher aux impôts de tous, et si on y touche, dire qui sera protégé, et comment. Aider ceux qui peuvent rester en emploi, sans faire comme si l'âge suffisait. Et publier chaque année l'écart entre ce qui a été promis et ce qui a été fait. [short pause] Et la méthode, c'est ce que la Suède a de transposable : un effort réparti, présenté d'un bloc, avec tout sur la table. On peut se disputer sur les moyens. Pas sur le but.

Pourquoi tout à la fois ? Parce que le rendement de chaque levier est incertain, et qu'en les combinant, on répartit le risque. Et on répartit le prix. [short pause] Dans quelles proportions ? Les preuves ne le disent pas. Ça, c'est un choix politique.

Quant au rythme : aller trop vite peut freiner l'activité, et donc les recettes ; aller trop lentement laisse les intérêts courir. Il n'y a pas de chemin sans coût. Il y a des coûts qu'on choisit, et des coûts qu'on subit.

Ce chemin coûtera à des retraités, à des contribuables, à des entreprises. Et rien ne garantit qu'il suffise.

Le projet de budget pour 2027 vise un déficit sous trois pour cent en 2029. Et quelques lignes plus loin, il écrit que cette trajectoire « revêt un caractère conventionnel du fait des échéances électorales de 2027 ». [long pause]

En 1979, une date de fin avait été écrite. Elle a été tenue au jour près. Les dates de retour à l'équilibre, jamais. [short pause] Alors la prochaine fois qu'on te présente un plan pour les finances publiques, de n'importe quel camp, pose trois questions.

Qui paie ? [short pause] Quand est-ce que ça rapporte ? [short pause] Et comment saura-t-on que c'est tenu ? [long pause]
```
