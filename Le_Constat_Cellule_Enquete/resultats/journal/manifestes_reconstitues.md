# Manifestes reconstitués pour la vague 1

**Produit le 21/11/2026 à 09 h 25 par `scripts\commun\reconstituer_manifestes.py`.** Les dossiers A01, A02, A04 et A06 ont été écrits avant que le manifeste soit obligatoire. Ce script fige l'empreinte de chaque fichier conservé et retrouve l'adresse d'origine quand elle figure sans ambiguïté sur une ligne du dossier ou d'un script citant le fichier. **Une empreinte prise aujourd'hui ne prouve pas que le fichier est identique à celui du téléchargement** : elle permet seulement de détecter toute modification ultérieure.

| Agent | État | Fichiers | Adresse d'origine retrouvée |
|---|---|---|---|
| A01 | reconstitué | 52 | 1 |
| A02 | reconstitué | 65 | 3 |
| A04 | reconstitué | 62 | 0 |
| A06 | reconstitué | 62 | 1 |

## Rattachement par preuve (21/11/2026, 10 h 32)

Par `scripts\commun\rattacher_origines.py` : chaque adresse citée dans le dossier ou ses scripts a été retéléchargée et son empreinte comparée à celles des fichiers conservés. Un fichier « rattaché » est **identique octet pour octet** à ce que son adresse sert aujourd'hui. Un fichier non rattaché n'est pas pour autant douteux : fichier dérivé (table, extraction de texte), interface de données dont la réponse a changé depuis, adresse absente du texte, ou site qui refuse les requêtes automatiques.

| Agent | Fichiers conservés | Adresses citées | Adresses servant un fichier conservé | Fichiers rattachés par preuve |
|---|---|---|---|---|
| A01 | 52 | 11 | 7 | 7 |
| A02 | 65 | 16 | 5 | 5 |
| A04 | 62 | 23 | 16 | 16 |
| A06 | 62 | 2 | 1 | 1 |
