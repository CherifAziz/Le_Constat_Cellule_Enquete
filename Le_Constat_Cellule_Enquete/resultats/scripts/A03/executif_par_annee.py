# -*- coding: utf-8 -*-
"""A03 - extrait du jeu data.gouv.fr « Historique des Gouvernements de la Vème République » (mis à jour le 13/03/2025,
téléchargé le 20/11/2026) les Premiers ministres, ministres de l'économie/finances et du budget/comptes publics en
fonction pendant chaque année 2001-2025. Sortie : donnees/A03/executif_2001_2025.csv. Couverture : jusqu'au gouvernement
Bayrou (début 13/12/2024) ; les changements postérieurs au 13/03/2025 ne figurent pas dans la source.
"""
import os, csv, re, datetime
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03", "sources"))
OUT = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03", "executif_2001_2025.csv"))
MOIS = {m: i + 1 for i, m in enumerate(["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                                        "septembre", "octobre", "novembre", "décembre"])}


def d(s):
    m = re.search(r"(\d{1,2})(?:er)? (\w+) (\d{4})", s or "")
    return datetime.date(int(m.group(3)), MOIS[m.group(2)], int(m.group(1))) if m else None


rows = list(csv.DictReader(open(os.path.join(SRC, "datagouv_gouvernements_membres.csv"), encoding="utf-8-sig"), delimiter=";"))
cles = re.compile(r"(Premier ministre$|[ée]conomie|[Ff]inances|[Bb]udget|[Cc]omptes publics|[Aa]ction et des comptes)", re.I)
out = []
for a in range(2001, 2026):
    deb, fin = datetime.date(a, 1, 1), datetime.date(a, 12, 31)
    for r in rows:
        f = r["fonction"]
        if not cles.search(f):
            continue
        if "Premier ministre" in f and not f.startswith("Premier ministre"):
            continue
        d0, d1 = d(r["date_debut_fonction"]), d(r["date_fin_fonction"]) or datetime.date(2099, 1, 1)
        if d0 and d0 <= fin and d1 >= deb:
            out.append([a, r["gouvernement"], r["prenom"] + " " + r["nom"], f, r["date_debut_fonction"], r["date_fin_fonction"]])
with open(OUT, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["annee", "gouvernement", "personne", "fonction", "debut", "fin"])
    w.writerows(out)
print(len(out))
