# 06 · Verdict final

**22 novembre 2026.** État de la V6 d'*Avant la ligne* après application des corrections de l'audit indépendant.

**Le texte est prêt pour un test ElevenLabs.** Les formulations bloquantes relevées par l'audit sont toutes remplacées, la voix seule concorde avec le script annoté, et le générateur produit des fichiers cohérents. Ce test est une première écoute, pas l'enregistrement définitif : la durée réelle et l'intelligibilité de trois passages restent à mesurer sur la voix.

Le verdict précédent, qui portait sur la version auditée et concluait qu'elle n'était pas prête, est archivé : [annexes/archive_924d875_verdict.md](annexes/archive_924d875_verdict.md).

---

## 1. Le verdict en cinq phrases

1. **La V6 est figée.** 3 744 mots, quatorze séquences, une ouverture et une conclusion. L'architecture et les révélations sont celles de la version auditée.
2. **Aucune erreur bloquante de l'audit ne subsiste.** Les quinze retouches de sa feuille sont appliquées ; aucune formulation bloquante n'a été gardée ([03](03_AUDIT_FACTUEL.md)).
3. **La conclusion ne généralise plus.** Elle distingue les crises qui creusent, les redressements qui réduisent et l'équilibre qui ne revient pas, puis montre trois décisions écrites qui ne se ressemblent pas ([07](07_CORRECTIONS_APPLIQUEES.md), §2).
4. **Le dernier acte avance.** Une séquence en moins, deux cents mots en moins, trois raccords refaits ([04](04_AUDIT_NARRATIF.md)).
5. **Le texte final n'a pas été relu par l'équipe indépendante.** Les corrections suivent sa feuille ; sept phrases vont au-delà et sont justifiées une à une ([03](03_AUDIT_FACTUEL.md), §3).

## 2. Les trois contrôles

| Contrôle | Ce qui a été vérifié | Résultat |
|---|---|---|
| **Factuel** | Les quinze retouches bloquantes de la feuille ; les quatorze corrections demandées par la direction éditoriale ; trente-quatre formulations écartées cherchées dans la voix ; les chiffres dits, recalculés sur les séries du dépôt | Conforme. Aucune formulation écartée ne subsiste ; tous les chiffres recalculés concordent |
| **Narratif** | Lecture continue de la voix ; les neuf éléments à préserver ; la progression séquence par séquence ; la conclusion | Conforme. Les neuf éléments sont intacts ; la dernière question est identique au caractère près |
| **Technique** | Régénération de 01 et de `durees.json` depuis 02 ; comparaison indépendante de la voix seule et du texte parlé du script annoté ; continuité de la feuille de temps | Conforme. 107 paragraphes dits identiques dans les deux fichiers ; les plages se suivent sans trou ; la dernière borne est le total |

Les trois programmes qui servent à ces contrôles sont dans `outils/` et se relancent tels quels :

```
python outils/construire_script.py . --ecrire
python outils/verifier_concordance.py .
python outils/controler_chiffres.py .
```

## 3. Ce qui a changé depuis la version auditée

| | Version auditée (`924d875`) | Version finale |
|---|---|---|
| Promesse de l'ouverture | Un pays qui se redresse « presque toujours dans la même situation » | Trois redressements dont on peut suivre les décisions dans les archives |
| Séquences | 15 | 14 : *L'écart* est supprimée |
| Acte IV | 1 099 mots | 896 mots |
| Conclusion | « Trois fois le même geste » ; « un problème avec les bonnes années » | Crises, redressements, pas de retour à l'équilibre ; trois décisions écrites, trois mécanismes |
| 2000 | « Elle a choisi de rendre l'argent » | Le déficit diminue encore ; une partie des recettes supplémentaires est rendue quand davantage pouvait aller à sa réduction |
| Trajectoires | Trente et une sur trente et une, sans règle de lecture | La règle est dite ; le décompte en années civiles aussi : trente et une sur trente-deux |
| Durée | 21 min 52, avec trois secondes de silence final absentes du cumul | 21 min 49 estimées par le calcul, carton de titre et silence final inscrits comme plages |
| Mots | 3 755 | 3 744 |

## 4. Ce qui fonctionne

| Force | Où |
|---|---|
| **Une première phrase que presque personne ne connaît** : « En 1980, la France est passée à deux doigts de l'équilibre » | Ouverture |
| **Un objet concret toutes les deux minutes** : la loi hospitalière, la fiche de paie à 30 francs, la page de novembre 1980, le projet de loi de 2000, les cinq dates | Séq. 2, 4, 5, 10, 12 |
| **Le film se retourne contre sa propre piste**, deux fois : la cotisation pèse moins d'un sixième ; garder toute la cagnotte couvrait au plus quatre dixièmes du déficit | Séq. 6, 10 |
| **L'aveu sur le motif de 1980**, joué comme un moment de méthode : « Ce que montrent les archives, c'est une décision. Pas un mobile » | Séq. 5 |
| **Le contraste entre 1980 et 2000** : un motif qu'on cherche, un motif imprimé | Séq. 10 |
| **Aucune majorité n'est blanchie ni chargée seule** : en 1981, « l'héritage et la gauche » ; les cinq dates annoncées par la gauche, la droite et le centre | Séq. 6, 12 |
| **Le film donne ses propres contre-exemples** : le déficit baisse en 2000 ; une cible sur trente-deux est tenue ; les baisses de 2018 sont votées avant la fin de la surveillance | Séq. 10, 12, 13 |
| **La dernière minute** : une date inscrite dans un texte, cinq trajectoires dépassées, puis la phrase du projet de budget 2027 sur son propre « caractère conventionnel » | Conclusion |

## 5. Ce qui reste faible

| Faiblesse | Gravité | Ce qu'il faudrait |
|---|---|---|
| **La conclusion est plus longue** : 387 mots contre 307. Le paragraphe sur la conjoncture est le plus abstrait | Moyenne | L'écouter. S'il pèse, le réduire à sa dernière phrase et laisser les chiffres à l'écran |
| **La séquence 2 reste le passage le plus abstrait**, à la deuxième minute | Moyenne | Au montage : montrer l'hôpital plus tôt |
| **Aucun enjeu d'aujourd'hui avant la dix-neuvième minute** | Moyenne | Assumé : l'audit recommande de garder le scrutin du 4 novembre 2026 pour la séquence 14 |
| **Le travail (séquence 8) est traité vite** | Faible | Assumé depuis la version auditée |
| **« Presque personne ne s'en souvient »** est invérifiable | Faible | Signalé par l'audit comme non bloquant. À couper si la phrase gêne à l'écoute |

## 6. Avant et après le test ElevenLabs

### Pour le test

| # | À faire |
|---|---|
| 1 | Donner à la voix le fichier [01_SCRIPT_V6.md](01_SCRIPT_V6.md), sans son bandeau. Les `(pause)` et `(silence)` sont des indications de réalisation, à traduire dans la syntaxe de l'outil ou à retirer |
| 2 | Mesurer la durée du fichier audio et la consigner à côté de l'estimation. Les 21 min 49 reposent sur une hypothèse de 182 mots par minute : ce n'est pas une mesure |
| 3 | Écouter sans l'écran trois passages : du régime général aux comptes de la France (séquence 4) ; du budget de l'État au déficit public (séquence 10) ; des prévisions à la dette (séquences 12 et 13). Si l'on a besoin du carton pour savoir de quoi parle un pourcentage, redire le périmètre dans la phrase |
| 4 | Vérifier la prononciation des nombres écrits en chiffres (« 0,4 % », « 3 000 francs », « 11 à 15 % », « 800 000 ») et des sigles (CSG, TVA) |

### Avant l'enregistrement définitif

| # | À faire |
|---|---|
| 5 | Reporter dans 02 toute retouche née de l'écoute, puis relancer les trois programmes de `outils/` |
| 6 | Faire relire par l'équipe indépendante les sept phrases qui vont au-delà de sa feuille ([03](03_AUDIT_FACTUEL.md), §3) et la conclusion |

### Avant le montage

| # | À faire |
|---|---|
| 7 | Obtenir le fac-similé du décret du 30 juillet 1979. S'il est trouvé, la phrase « on ne l'a pas retrouvé » disparaît |
| 8 | Trouver une une de presse de 2000 portant le mot « cagnotte » |
| 9 | Afficher 49 ou 64 millions selon la pièce montrée : projet du 26 avril ou loi du 13 juillet 2000 |
| 10 | Signaler par des crochets les coupes de la citation de novembre 1980 |
| 11 | Rassembler les couvertures des documents de programmation et les cinq pages qui annoncent l'équilibre |
| 12 | Sourcer et acquérir les archives audiovisuelles de 1975, 1981, 1997 et 2000 |

## 7. Ce que cette version n'est pas

- **Ce n'est pas un texte mesuré à l'oreille.** Aucune voix ne l'a encore lu. Les pauses sont des hypothèses.
- **Ce n'est pas un texte contre-expertisé dans son dernier état.** L'équipe indépendante a audité la version précédente. Ses corrections sont appliquées, mais elle n'a pas relu le résultat.
- **Ce n'est pas un film sur les solutions.** Il ne dit pas quoi faire. Il donne au spectateur une question à poser : *qu'est-ce qu'on en fait ?*

## 8. Fichiers du dossier

| Fichier | Rôle |
|---|---|
| [01_SCRIPT_V6.md](01_SCRIPT_V6.md) | Voix off finale, texte seul. Produit automatiquement |
| [02_SCRIPT_ANNOTE.md](02_SCRIPT_ANNOTE.md) | Version annotée finale : voix, images, archives. Seule source à modifier |
| [03_AUDIT_FACTUEL.md](03_AUDIT_FACTUEL.md) | Contrôle factuel de conformité à l'audit indépendant |
| [04_AUDIT_NARRATIF.md](04_AUDIT_NARRATIF.md) | Contrôle narratif final et durées estimées |
| [05_MODIFICATIONS_ARCHITECTURE.md](05_MODIFICATIONS_ARCHITECTURE.md) | Écarts entre l'architecture et le script final |
| [07_CORRECTIONS_APPLIQUEES.md](07_CORRECTIONS_APPLIQUEES.md) | Tableau des corrections appliquées, phrase par phrase |
| `durees.json` | Feuille de temps estimée, avec ses hypothèses |
| `outils/` | Générateur, vérification de concordance, contrôle des chiffres |
| `annexes/` | Archives : audits et verdict de la version auditée, relectures intermédiaires |
