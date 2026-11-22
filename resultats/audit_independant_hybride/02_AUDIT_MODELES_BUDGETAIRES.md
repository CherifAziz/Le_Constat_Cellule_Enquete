# Combien faudrait-il pour arrêter la hausse du ratio de dette en 2030 ?

**Verdict sur la séquence 17 — Réfutée pour la jauge proposée.** Le point bas de 130 Md€ autorise encore une hausse de la dette rapportée au PIB effectivement produit. Le point haut impose sa stabilité effective. Les deux autres fourchettes décrivent deux sélections de mesures avec deux hypothèses de réalisation. On peut montrer ce qu'elles changent en simulant la même grandeur dans le même modèle. La comparaison recommandée figure au §5.

## 1. Définir ce que voit le spectateur

On prend toutes les administrations publiques consolidées (État et organismes centraux, collectivités, sécurité sociale). On note **d** le rapport entre l'encours de dette et le PIB nominal, **g** la croissance annuelle du PIB nominal, **f** le déficit total de l'année compté positivement et divisé par le PIB courant, et **a** les acquisitions d'actifs et autres ajustements stocks-flux nets rapportés au même PIB. L'identité est **dₜ = dₜ₋₁/(1+g) + fₜ + aₜ**. À ratio stable, le déficit admissible vaut **dₜ₋₁ × g/(1+g) − aₜ**. La cible équivalente pour le solde primaire, compté positivement en cas d'excédent, est **(i−g) × dₜ₋₁/(1+g) + aₜ**, avec i le taux effectif sur le stock d'ouverture. Les intérêts sont déjà dans f. Les ajouter à nouveau surestime le besoin.

**Validée.** Avec d = 125 %, g = 2,4 % et a = 0, un déficit de 2,93 % stabilise le ratio. À g = 3,1 %, le seuil passe à 3,76 %. La dette nominale augmente dans les deux cas. Un déficit de 3 % est un objectif distinct. L'équilibre est un déficit nul. Stabiliser entre 2029 et 2030 ne garantit ni une baisse depuis 2025, ni la stabilité après 2030. Les deux modèles mettent a à zéro en projection. Un ajustement positif de 1 % du PIB abaisse d'un point le déficit compatible cette année-là. [Définitions et trajectoires A15](../../Le_Constat_Cellule_Enquete/resultats/agents/A15.md)

**Validée sous conditions.** Le point de départ observé de cette édition est 2025, PIB 2 991,056 Md€, dette 3 460,1 Md€, déficit 151,592 Md€, intérêts 65,721 Md€. Le scénario de référence conserve les mesures antérieures et leurs extinctions prévues. Il fixe le déficit 2026 à 5,5 %, puis, hors mesures du projet pour 2027, à 6,5 % en 2027. Il ne reconduit ni le déficit ni le PIB de 2025. A15 projette ensuite 7,275 % de déficit et 132,086 % de dette en 2030. [Paramètres et données de départ](../../Le_Constat_Cellule_Enquete/resultats/scripts/C03/a15_modele.py) · [Référence annuelle](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_reference_2026_2050.csv)

## 2. Refaire le besoin avec la même définition aux deux bornes

Les deux calibrages recherchent une marche de mesures permanentes qui atteint son plein niveau en 2030. La simulation teste un quart de ce niveau en 2027, la moitié en 2028, trois quarts en 2029 et le plein effet direct en 2030. Une marche finale de 5,512 points signifie donc environ 1,378 point de décisions additionnelles à chaque étape. Une fois atteint, le niveau doit être maintenu. « Trouver 165 milliards nouveaux chaque année » quadruplerait l'effort au terme des quatre ans. **Réfutée** dans ce sens.

| Cible en 2030, depuis 6,5 % en 2027 sans le projet | Codex, points de PIB et Md€ à l'échelle 2025 | Cellule A15, mêmes unités |
|---|---:|---:|
| Seuil de déficit calculé avec la croissance tendancielle | 4,330 · 129,5 | 5,168 · 154,6 |
| Ratio de dette effectif 2030 égal à celui de 2029 | 4,498 · 134,6 | 5,512 · 164,9 |
| Déficit de 3,00 % | 5,422 · 162,2 | 5,411 · 161,8 |
| Déficit nul | 8,904 · 266,3 | 9,208 · 275,4 |

Un point vaut **29,91056 Md€ à la taille de l’économie de 2025**. Les nombres ne sont ni des encaissements nominaux de 2030 ni une simple conversion aux prix constants de 2025. Exemple A15 avec son critère tendanciel, 154,6 Md€ à l'échelle 2025 correspondent à 173,3 Md€ courants dans la trajectoire 2030. Les points Codex sont des mesures en proportion du PIB de référence et A15 les exprime sur son PIB effectif. Le critère observable est commun sur la deuxième ligne, les conventions de mesure de l'effort restent propres aux modèles. [Table de passage C03](../../Le_Constat_Cellule_Enquete/resultats/donnees/C03/C03_chiffres_harmonises.csv) · [Objectifs et euros courants](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_objectifs_horizons.csv)

**Validée sous conditions** pour « environ 135 à 165 Md€ de mesures annuelles au niveau atteint en 2030, dans deux simulations sans les mesures du projet 2027 ». Les bornes décrivent deux cas centraux, sans probabilité. Dans le modèle Codex au seuil tendanciel, la dette monte de 125,660 à 125,794 % entre 2029 et 2030. Dans A15 au seuil tendanciel, elle monte de 125,203 à 125,437 %. Au critère effectif, elle est stable à respectivement 125,55 et 125,00 %. Le déficit autorisé est alors de 3,78 % et de 2,92 %. Voilà pourquoi, dans A15, atteindre exactement 3 % peut demander légèrement moins d'effort que stabiliser. [Rejeu de réconciliation et définitions](../../Le_Constat_Cellule_Enquete/resultats/donnees/C03/C03_sortie_passage.txt)

**Hypothèses qui déplacent le chiffre.** A15 retient, pour 2029–30, un potentiel réel de +1 % par an et un déflateur de +1,6 %, un écart de production se refermant en 2030, une semi-élasticité du solde de 0,57 et un multiplicateur de 0,6 sur les nouvelles tranches. L'effet de demande est plein deux ans, puis amorti. Codex retient +1,2 % et +2 %, un écart de référence figé, 0,50 et 0,8, avec un effet divisé par deux chaque année. A15 renouvelle 10 % du stock par an, avec 9 % indexés, un taux d'émission calibré à 4,83 % en 2028, puis convergeant vers 4 %. Codex refinance 1/8,5 du stock, avec 4 % dès 2028 et sans bloc indexé distinct. Les coûts de vieillissement et l'encours 2026 diffèrent aussi. Dans A15, 1 point de mesure primaire donne au premier ordre 1 − 0,57 × 0,6 = 0,658 point de solde la première année avant intérêts et effet de dénominateur. Le modèle transforme une hypothèse de comportement en trajectoire. [Paramétrage comparé](../../Le_Constat_Cellule_Enquete/resultats/scripts/C03/c03_passage.py)

### Budget 2027 et sensibilités

**Réfutée** pour l'équivalence « 90–115 au-delà du budget adopté tel quel ». La prévision de la Commission avec les mesures annoncées donne **5,4 %** de déficit en 2027. La cible gouvernementale du projet est **5,0 %**. Au point de départ Commission, les bornes à **critère effectif commun** sont 3,078–3,784 points, soit **92–113 Md€**. Les variantes C03 ancrées sur 5,0 % donnent, dans les définitions natives distinctes, 3,122 et 2,567 points. Elles ne constituent pas une prévision de l'effet de la loi définitive. Sur les calculs natifs initiaux, le traitement de la référence 2027 explique environ 1,49 des 2,09 points d'écart dans la décomposition C03. Ce n'est pas le rendement constaté de la loi. [Commission, prévisions d’automne 2026](https://economy-finance.ec.europa.eu/document/download/e6bb4d2e-5c46-44e6-a716-6624a57494f3_en) · [HCFP, avis sur les projets 2027](https://www.hcfp.fr/liste-avis/avis-ndeg2026-5-lois-de-finances-2027) · [Passage, références et variantes](../../Le_Constat_Cellule_Enquete/resultats/donnees/C03/C03_sortie_passage.txt)

Au **22 novembre 2026**, la première partie du PLF a été rejetée à l'Assemblée le 4 novembre, le texte est devant le Sénat en première lecture. PLF et PLFSS ont des dispositions et des parcours distincts. Le rejet d'un texte ne rend pas définitive la suppression de chacune de ses lignes. Pour actualiser, dater les deux textes, identifier article par article les mesures maintenues, amendées, temporaires ou abandonnées, déplacer celles inscrites en droit dans la référence, puis relancer cibles **et** portefeuilles sur cette même référence. Ne jamais retrancher les 43 Md€ annoncés d'un total déjà net du projet. Dans C03, modéliser explicitement 1,4 point permanent à multiplicateur 0,6 donne 3,565 points supplémentaires, ou 3,906 si 0,3 point expire en 2028. [Dossier législatif au Sénat](https://www.senat.fr/dossier-legislatif/pjlf2027.html) · [Budget traité comme mesure](../../Le_Constat_Cellule_Enquete/resultats/donnees/C03/C03_budget_comme_mesure.csv)

**Validée sous conditions.** Test un facteur à la fois, besoin A15 pour son **seuil tendanciel 2030**, référence centrale **5,168 points**. Croissance réelle à partir de 2028 diminuée/augmentée de 0,5 point par an → **5,990 / 4,363**. Déflateur bas/haut à taux inchangés → **6,058 / 4,085**. Taux d'émission +100/+200 points de base dès 2027 → **5,828 / 6,495**. Multiplicateur 0,3/1,0 → **4,385 / 6,787**. Ces sensibilités peuvent sortir de l'intervalle intermodèles. Une inflation plus forte gonfle le dénominateur mais renchérit rapidement la dette indexée, plus tard les prestations et rémunérations selon les règles. Une inflation plus faible réduit aussi ce que rapporte une désindexation. Le test du seul déflateur tient les rendements des gels fixes. Un choc sur les taux se diffuse à mesure du refinancement. [Variantes A15, distinguer les colonnes 2030/2035](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_sensibilites_effort.csv)

## 3. Refaire les paniers et la décote

Recalcul à partir des entrées A13 et A14 et des identifiants retenus. Pour A13, partir du brut courant de 2030, retrancher les moindres prélèvements s'ils ne sont pas déjà intégrés, appliquer transmission au solde public et report sur d'autres administrations, ajouter le bonus d'emploi spécifié, puis ramener à l'échelle de 2025. A14 fournit un net direct, incluant certaines réponses comportementales, aux assiettes de référence. La boucle générale sur l'activité intervient ensuite, une seule fois. Les 33,2 Md€ d'A13 publiés en valeur courante après sa propre boucle et les 38 Md€ d'A14 n'ont pas vocation à s'additionner.

| Sélection de mesures de la cellule | Lignes | Entièrement appliquée | Avec décote centrale | Avec les deux autres grilles de risque A13 |
|---|---:|---:|---:|---:|
| K1 centrale, gel | 38 | 62,231 | 40,843 | 30,40 à 53,79 |
| K2 centrale, abattement | 37 | 59,970 | 39,713 | 29,72 à 51,98 |
| K3 centrale, retraits parlementaires exclus | 31 | 41,288 | 30,372 | 24,12 à 37,04 |
| K4 prudente | 24 | 44,854 | 27,919 | 20,10 à 38,18 |
| K5 ambitieuse, périmètre large publié | 42 | 70,787 | 47,260 | 35,53 à 61,49 |

Montants directs annuels en 2030, Md€ à l'échelle 2025. « 60–70 » et « 40–50 » sont **validées sous conditions comme arrondis de K1 et K5**. La première borne haute exacte dépasse 70. Ces fourchettes excluent les autres sélections, certaines lignes à rendement 2030 nul sont comptées dans les 38/42, et K5 demande une correction de droit ci-dessous. Les impôts larges ne figurent pas comme hausses générales de taux dans les paniers, mais K5 comporte déjà une réforme de la déductibilité de la CSG. [Composition des cinq paniers](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_combinaisons_composition.csv) · [Lignes et rendements](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_mesures_harmonisees.csv)

**Décote historique prédictive — Insuffisamment démontrée.** Les coefficients de réalisation faible/moyen/fort risque sont 90/75/50 %. Pour K1, le résultat est 2,899 × 0,90 + 34,272 × 0,75 + 25,060 × 0,50 ≈ **40,84**. K5 a 42,828 en risque moyen et les mêmes deux autres masses, soit **47,26**. Effort conservé 65,6 % et 66,8 %. Les cinq ancrages d'A13 sont le retrait du gel PLFSS, les transferts locaux de novembre 2026, le recul de CSG en 2018, les objectifs d'effectifs de programmation et l'erreur moyenne des trajectoires. Ils mélangent abandon, exécution et erreur de prévision. Absence de dénominateur de mesures comparables, de fréquence estimée, de validation hors échantillon et de traitement des vetos communs. Les grilles 80/60/30 et 100/90/80 produisent les extrêmes du tableau, sans leur attribuer de probabilités. Le coût négatif du recyclage emploi est lui aussi réduit par la décote, hypothèse à vérifier si la compensation est garantie même en cas de rendement décevant. K3 seul est un autre test, son montant entier ressemble par coïncidence à K1 décoté. [Paramètres et cinq précédents, A13 §5](../../Le_Constat_Cellule_Enquete/resultats/agents/A13.md)

## 4. Où se trouvent les doubles comptes ?

- **Validée pour les exclusions identifiables.** En repartant des listes centrales brutes harmonisées, environ 73,93 Md€ moins 6,870 (allègements A13-013), 4,400 (abattement A14-009 alternatif au gel) et 0,425 (CIR A13-015) donnent 62,23. Le retour sur la suspension de l'âge apparaît une seule fois. K2 remplace le gel et la sous-indexation par l'abattement. Les 4,4 Md€ de cette suppression viennent en supplément des 1,4 de plafonnement déjà inclus dans la ligne fiscale composite. [Matrice des recoupements](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_matrice_recoupements.csv)
- **Réfutée pour un K5 intégralement nouveau et sans recoupement.** La ligne P-A13-015 réintroduit la suppression du dispositif « jeunes docteurs » et la baisse du forfait de fonctionnement de 43 à 40 %, déjà adoptées en février 2025. Son éventuel reliquat de périmètre n'est pas ventilé. K5 inclut aussi P-A14-019, le calcul du CIR au niveau du groupe. À titre prudent, réserver toute la première ligne (0,425 Md€), retenir **70,36** directs et **46,94** avec décote, en attendant un chiffrage marginal du reliquat. K1 l'exclut déjà. L'erreur est réelle même si elle ne modifie pas l'arrondi à la dizaine. [Mesure source A13](../../Le_Constat_Cellule_Enquete/resultats/donnees/A13/A13_mesures.csv) · [Loi de finances 2025, art. 55](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000051168706) · [Application par la DGFiP](https://bofip.impots.gouv.fr/bofip/14709-PGP.html/ACTU-2025-00105)
- **Validée sous conditions pour les transferts.** La réduction d'une dotation de l'État et la perte correspondante des collectivités s'annulent en comptes consolidés. Seule leur baisse effective de dépense ou leur recette supplémentaire contribue. A13 suppose notamment 65 % et 80 % de transmission pour deux lignes locales. Un déremboursement peut améliorer le solde public en déplaçant la charge vers ménages et complémentaires, avec renoncements aux soins possibles. La perte de recette sur un revenu de remplacement réduit, l'assiette plus faible de CSG sur les pensions et le cumul des franchises et primes restent à simuler conjointement. [A13](../../Le_Constat_Cellule_Enquete/resultats/agents/A13.md) · [Contre-exemple documenté du RSA](../enquetes_complementaires_codex/H06_RSA/rapport.md)
- **Insuffisamment démontrée pour une addition ultérieure.** En cas de TVA normale relevée et de reclassement de la restauration, recalculer le produit sur les bases finales. Les allègements d'employeurs affectent les recettes et l'emploi. Les gains d'activité des réformes d'âge sont déjà partiellement intégrés. Reprendre les niches et le recouvrement sur des bases communes, traiter conjointement les modifications du barème d'IR, du quotient conjugal et de la déductibilité CSG. Compter les majorations temporaires d'IS uniquement contre leur extinction prévue. Une norme globale de dépense inclut les lignes qui en assurent l'exécution. [Entrées fiscales A14](../../Le_Constat_Cellule_Enquete/resultats/donnees/A14/A14_table_mesures.csv)

## 5. Le graphique recommandé en séquence 17

**Deux lectures successives.** En premier, un carton « En 2030, stabiliser la dette par rapport à 2029 », ordre de grandeur 135–165, scénario de départ à 6,5 % en 2027, équivalent à la taille de 2025. Ensuite une image avec **une seule variable mesurable**, le changement du ratio entre 2029 et 2030, en points de PIB. Une ligne zéro indique l'arrêt de la hausse. Voici les valeurs à mettre à disposition du montage.

| France, modèle cellule, même référence | Dette 2029 en % du PIB | Dette 2030 en % du PIB | Hausse en points | Déficit 2030 en % du PIB |
|---|---:|---:|---:|---:|
| Sans les mesures du projet ni portefeuille | 128,332 | 132,086 | +3,754 | 7,275 |
| K1, toutes les mesures | 125,066 | 127,073 | +2,007 | 5,392 |
| K1, exécution partielle hypothétique | 126,221 | 128,834 | +2,613 | 6,042 |
| K5 publié, toutes les mesures | 124,779 | 126,564 | +1,785 | 5,145 |
| K5 publié, exécution partielle hypothétique | 126,005 | 128,451 | +2,446 | 5,857 |

**À l'écran, retenir les trois premières lignes**, arrondies à +3,8, +2,0 et +2,6. Le commentaire peut constater que le portefeuille central ralentit la hausse et que le ratio continue d'augmenter. Ainsi l'inventaire, l'exécution et l'objectif conservent chacun leur sens. Les trajectoires K5 sont celles du fichier gelé avant correction du CIR. Le gain de déficit K1 est 7,275 − 5,392 = 1,883 point, soit 56,3 Md€ à l'échelle 2025, contre 62,2 directs. En 2035, le déficit de référence est 8,68 %, K1 entier 5,47 %, K1 partiel 6,61 %. Le niveau et la pente peuvent raconter des choses différentes. [Trajectoires des paniers](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_combinaisons_trajectoires.csv) · [Référence annuelle](../../Le_Constat_Cellule_Enquete/resultats/donnees/A15/A15_reference_2026_2050.csv)

**« Au mieux la moitié » — Réfutée comme borne générale.** La division brute 70,787 / 129,5 dépasse 54 % et croise deux modèles. À l'intérieur du modèle A15, 70,787 / 164,9 ≈ 43 % est un rapport de mesures directes à une rampe conventionnelle. Sur la pente effective, K5 publié efface (3,754 − 1,785) / 3,754 ≈ **52 %** de la hausse de cette année. Ces questions donnent des réponses différentes. Aucune division n'établit un plafond des solutions envisageables.

## 6. Calculs reproductibles

Depuis la racine du commit audité, exécuter séparément ces deux blocs avec Python 3 standard. Le premier reconstitue les deux moteurs sur 2027–30 sans importer leur code, conditionnellement à leurs hypothèses et aux valeurs annuelles publiées arrondies. L'écart d'arrondi sur A15 à l'équilibre est de 0,001 point. Le second utilise les fiches d'entrée et les listes de sélection, sans utiliser les totaux d'A15.

```python
from pathlib import Path
import csv

data = Path("Le_Constat_Cellule_Enquete/resultats/donnees/A15")
with (data/"A15_reference_2026_2050.csv").open(encoding="utf-8-sig") as f:
    ref = {int(r["annee"]):r for r in csv.DictReader(f, delimiter=";")}
def val(y,k):
    return float(ref[y][k])

def proj(effort,modele):
    # Toutes les sommes sont en Md courants. Les taux dans les CSV sont en %.
    a15 = modele == "A15"
    yref = val(2026,"PIB_mdeur")
    dette = yref * (val(2026,"dette_pct")/100 if a15 else 1.192)
    coupon = val(2026,"taux_moyen_encours")/100
    ratios = []
    for n in range(1,5):
        t = 2026+n
        if a15:
            yref = val(t,"PIB_mdeur")
            perte = .6*effort/4 * sum([1,1,.5,.5][:n])
            y = yref*(1-perte/(100+val(t,"ecart_production")))
            primaire = y*(val(t,"solde_primaire")+n*effort/4-.57*perte)/100
            taux = val(t,"taux_emission")/100
            coupon = .9*coupon+.1*taux
            ipc = [2.9,2.1,1.9,1.9][n-1]
            charge_stock = dette*(.91*coupon+.09*(.5+ipc)/100)
            emprunt = (charge_stock-primaire)/(1-taux/2)
            coupon = (coupon*dette+taux*emprunt)/(dette+emprunt)
        else:
            # Croissance de référence 2027 sans les mesures du projet.
            yref *= (1.012*.993/.994 if n==1 else 1.012)*1.02
            perte = .8*effort/4*sum(.5**k for k in range(n))
            y = yref*(1-perte/100)
            primaire = yref*(-3.5-.08*(n-1)+n*effort/4-.5*perte)/100
            coupon = .03*yref/dette if n==1 else (1-1/8.5)*coupon+.04/8.5
            emprunt = dette*coupon-primaire
        dette += emprunt
        ratios.append(100*dette/y)
    return ratios[-1]-ratios[-2], 100*emprunt/y, ratios[-1]

for modele in ("Codex","A15"):
    for objectif in ("ratio","3 %","equilibre"):
        bas, haut = 0, 15
        for _ in range(50):
            m = (bas+haut)/2
            variation, deficit, dette = proj(m,modele)
            ecart = variation if objectif=="ratio" else deficit-(3 if objectif=="3 %" else 0)
            if ecart > 0:
                bas = m
            else:
                haut = m
        print(modele,objectif,round(haut,3),round(haut*29.91056,1),round(dette,2))
```

```python
from pathlib import Path
import csv

data = Path("Le_Constat_Cellule_Enquete/resultats/donnees")
def read(folder, file):
    with (data / folder / file).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))

pib25 = 2991.056
a13 = {r["id"]: r for r in read("A13", "A13_mesures.csv")}
a14 = {r["id"]: r for r in read("A14", "A14_table_mesures.csv")}
def montant(i):
    if i in a14:
        return float(a14[i]["net_central_2030"])
    r = a13[i]
    brut, fin = float(r["brut_2030"]), float(r["brut_2035"])
    retour = 0 if r["deja_net_PO"] == "oui" else float(r["retour_PO"])
    bonus = float(r["bonus_emploi_2035_C"]) * brut / fin if fin else 0
    net = brut * (1-retour) * float(r["pass_through_C"]) * (1-float(r["report_APU"]))
    return (net+bonus) / (1.02 * 1.027 * 1.025**3)

def risque(i):
    if i in a13:
        return a13[i]["risque_politique"]
    return "eleve" if i[-3:] in {"001","007","009","010"} else "moyen"

for r in read("A15", "A15_combinaisons_composition.csv"):
    ids = r["mesures"].split()
    assert len(ids) == len(set(ids))
    groupes = [sum(montant(i) for i in ids if risque(i) == k)
               for k in ("faible","moyen","eleve")]
    produits = [sum(a*b for a,b in zip(groupes,poids))
                for poids in [(1,1,1),(.9,.75,.5),(.8,.6,.3),(1,.9,.8)]]
    print(r["combinaison"][:2],len(ids),[round(x,3) for x in groupes+produits])
```
