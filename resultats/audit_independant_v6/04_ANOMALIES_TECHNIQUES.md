# Concordance des versions et chronométrage

**Les cinq observations sont confirmées, avec deux nuances.** Les trois secondes existent dans le générateur comme silence de fin. Et seules certaines informations de l’en-tête sont figées. Ces anomalies concernent la préparation de la prise et la traçabilité des versions. Elles ne modifient aucun chiffre des comptes publics.

| Observation | Contrôle au commit 924d875 | Correction exacte proposée à la production | Gravité · blocage avant enregistrement |
|---|---|---|---|
| 21:52 dans le total, 21:49 en fin de dernière séquence | Le JSON donne 1 311,9 secondes au total et 1 308,9 à la fin de « Conclusion ». Le générateur ajoute 4 secondes de titre et 3 secondes de fin au total. Dans la boucle de cumul, seules les 4 secondes d’ouverture ont une case. L’ouverture a 56,1 secondes de durée propre et finit à 60,1. | Inscrire une plage explicite « Silence final » de 1 308,9 à 1 311,9 dans la feuille de montage, ou publier deux champs « fin de dernière séquence » et « fin avec silence ». Distinguer de la même façon le titre de l’ouverture. Vérifier après génération que la dernière borne de la feuille complète concorde avec le total. | **Mineure · non bloquant** pour la voix. |
| En-tête figé du générateur | La date « 22 novembre 2026 », l’état « Première version complète » et le libellé « 182 mots par minute » sont littéraux dans la construction du Markdown. La constante MOTS_MIN pilote le calcul. Nombre de mots et durée totale du bandeau sont interpolés. | Prendre la date et la version dans les métadonnées du script annoté, imprimer la valeur effective de MOTS_MIN et donner la convention de pauses. Après la prise, consigner séparément la durée du fichier audio. | **Mineure · non bloquant**. Risque de millésime trompeur lors de la prochaine génération. |
| Verdict de Claude, ouverture obsolète | Le verdict cite « En 1980, la France a failli sortir du déficit ». Les deux scripts au commit de référence commencent par « En 1980, la France est passée à deux doigts de l’équilibre. » | Dans le verdict de production suivant, remplacer la première citation par la seconde, indiquer le commit visé. La version auditée reste une archive. | **Mineure · non bloquant**. |
| Historique des modifications | Au §5 de 05, la colonne intitulée « Script » reproduit également « a failli sortir ». Au §1, le texte présente l’écart recettes/dépenses comme « le même qu’en 1985 », alors que la voix dit 3 puis 5 points. Au §4, il reste « presque uniquement en prélevant plus », contre « surtout » dans la voix. Les anciennes phrases identifiées comme telles dans la colonne « Architecture » sont normales. | Corriger la colonne d’arrivée dans une nouvelle note de production. Écrire « environ 3 points en 1985 et 5 en 2025 », et lier directement à la conclusion finalement approuvée. | **Mineure · non bloquant** si l’équipe prend 01 et 02 comme références de prise. |
| Annexes de relecture antérieures au dernier état | Leur premier enregistrement apparaît à 2739559. La dernière modification dans le dossier des annexes est à da258e6, avant 1b2ef02 et 924d875. La relecture narrative annonce **3 595 mots** et reproduit l’ancienne ouverture. La factuelle commente encore « avant mai ». Le dernier commit révise les scripts, les audits, le verdict et le générateur. Il ne met pas les annexes à jour. | Étiqueter les deux annexes « relectures intermédiaires », avec leur commit. Joindre au dossier de prise le verdict indépendant sur l’état 924d875 et vérifier la liste des retouches sur le futur texte enregistré. | **Modérée · non bloquant** comme archive. Ne les employer comme visa de la voix corrigée qu’après une concordance explicite. |

**Contrôle des deux scripts.** L’exécution dans un répertoire temporaire sur le fichier 02 épinglé a reproduit à l’octet près le fichier 01 et le JSON de la V6. Le calcul compte 3 755 mots. Le décalage de trois secondes ne provient donc pas d’un morceau de texte perdu. Les indications entre parenthèses et les pauses hors voix sont des hypothèses d’édition. Une conversion du nombre de mots en minutes ne fournit pas la durée définitive. Le comptage automatique des chiffres écrits en chiffres ne détecte pas les nombres écrits en lettres. [Générateur](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/outils/construire_script.py) · [JSON](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/durees.json) · [Note d’architecture](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/05_MODIFICATIONS_ARCHITECTURE.md) · [Verdict de Claude](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/06_VERDICT.md)

## Vérification reproductible, sans écrire chez Claude

Exécuter ce bloc Python depuis la racine du dépôt après avoir récupéré la branche de référence. Toutes les écritures aboutissent dans un répertoire temporaire. L’appel avec l’option d’écriture reste limité à ce répertoire.

```python
import json
import pathlib
import subprocess
import sys
import tempfile

pin = "924d875345e4216d9f5fd748ec380f4463236b21"
folder = "resultats/script_documentaire_v6/"
def blob(name):
    return subprocess.check_output(["git", "show", f"{pin}:{folder}{name}"])

with tempfile.TemporaryDirectory() as temporary:
    out = pathlib.Path(temporary)
    (out / "02_SCRIPT_ANNOTE.md").write_bytes(blob("02_SCRIPT_ANNOTE.md"))
    script = out / "construire_script.py"
    script.write_bytes(blob("outils/construire_script.py"))
    subprocess.run([sys.executable, str(script), str(out), "--ecrire"], check=True)
    for name in ("01_SCRIPT_V6.md", "durees.json"):
        assert (out / name).read_bytes() == blob(name)
    duration = json.loads(blob("durees.json"))
    assert duration["total_mots"] == 3755
    assert round(duration["total_s"] - duration["sequences"][-1]["fin_s"], 1) == 3
```

Pour dater les annexes, consulter l’historique limité à leur chemin, puis les fichiers effectivement modifiés au commit final. [Annexe factuelle](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/annexes/relecture_factuelle_agent.md) · [Annexe narrative](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/blob/924d875345e4216d9f5fd748ec380f4463236b21/resultats/script_documentaire_v6/annexes/relecture_narrative_agent.md) · [Diff de la dernière révision](https://github.com/CherifAziz/Le_Constat_Cellule_Enquete/commit/924d875345e4216d9f5fd748ec380f4463236b21)
