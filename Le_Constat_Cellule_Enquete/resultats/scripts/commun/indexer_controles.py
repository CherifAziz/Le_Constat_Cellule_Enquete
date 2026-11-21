# -*- coding: utf-8 -*-
"""Ajoute à preuves.md un index de tous les contrôles faits par l'orchestrateur,
extrait des tables de contrôle des comptes rendus de recette (journal/recette_*.md).
N'ajoute aucun fait : recopie les lignes de contrôle avec leur dossier.

Usage : python -I scripts/commun/indexer_controles.py   (depuis resultats/)
"""
import datetime as dt
import glob
import os
import re

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MARQ = "\n## D. Index des contrôles de l'orchestrateur, par dossier (généré)"
titres = re.compile(r"^## .*(sondage|contrôles? de l'orchestrateur|rejeu|recalcul|contrôles)", re.I)
lignes, n = [], 0
for f in sorted(glob.glob(os.path.join(R, "journal", "recette_*.md"))):
    nom = os.path.basename(f)
    m = re.match(r"recette_([A-Z]\d\d)(.*)\.md", nom)
    if not m:
        continue
    code = m.group(1) + (" " + m.group(2).strip("_").replace("_", " ") if m.group(2) else "")
    dedans, bloc = False, []
    for l in open(f, encoding="utf-8").read().split("\n"):
        if l.startswith("## "):
            dedans = bool(titres.match(l))
            continue
        if dedans and l.startswith("| ") and not l.startswith("|---") and not re.match(r"^\| (Affirmation|Élément|Élément |Affirmation d)", l):
            c = [x.strip() for x in l.strip().strip("|").split(" | ")]
            if len(c) >= 3:
                bloc.append((c[0], c[1], c[-1]))
    for a, b, c in bloc:
        n += 1
        lignes.append(f"| {code} | {a} | {b} | {c} |")

p = os.path.join(R, "preuves.md")
t = open(p, encoding="utf-8").read()
if MARQ in t:
    t = t[:t.index(MARQ)]
t = t.rstrip("\n") + "\n" + MARQ + "\n\n"
t += ("**Généré le " + dt.datetime.now().strftime("%d/%m/%Y à %H h %M") + " par `scripts\\commun\\indexer_controles.py`** à partir des comptes rendus de recette. "
      f"{n} contrôles. Les sections A à C ci-dessus datent de la première vague (20 novembre, 12 h 56) et ne sont pas tenues à jour : **cet index et `corrections_demandees.md` font foi.** "
      "Un contrôle « relu dans la copie » porte sur la pièce conservée par l'agent, non sur l'original.\n\n")
t += "| Dossier | Élément contrôlé | Contrôle | Résultat |\n|---|---|---|---|\n" + "\n".join(lignes) + "\n"
open(p, "w", encoding="utf-8", newline="").write(t)
print(n, "contrôles indexés depuis", len(glob.glob(os.path.join(R, "journal", "recette_*.md"))), "fichiers")
