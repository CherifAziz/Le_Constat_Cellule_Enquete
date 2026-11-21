# -*- coding: utf-8 -*-
"""Reconstitue un manifeste pour les dossiers de la vague 1 qui n'en ont pas (A01, A02, A04, A06).

Pour chaque fichier de donnees/<agent>/ : taille, date, empreinte SHA-256, et l'adresse d'origine
quand elle se retrouve sans ambiguïté dans le texte du dossier (ligne citant le nom du fichier
et une seule adresse). Sinon : « non retrouvée ». Ne modifie aucun fichier d'agent.

Usage : python -I scripts/commun/reconstituer_manifestes.py   (depuis resultats/)
Sortie : donnees/<agent>/MANIFESTE_RECONSTITUE.csv ; journal/manifestes_reconstitues.md
"""
import csv
import datetime as dt
import glob
import hashlib
import os
import re

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENTS = ["A01", "A02", "A04", "A06"]
URL = re.compile(r"https?://[^\s)\]>`|\"']+")
bilan = []
for a in AGENTS:
    d = os.path.join(R, "donnees", a)
    if os.path.exists(os.path.join(d, "MANIFESTE_PIECES.csv")):
        bilan.append((a, "manifeste d'agent déjà présent", 0, 0))
        continue
    texte = ""
    for p in glob.glob(os.path.join(R, "agents", a + "*.md")):
        texte += open(p, encoding="utf-8").read() + "\n"
    for p in glob.glob(os.path.join(R, "scripts", a, "*.py")):
        texte += open(p, encoding="utf-8", errors="replace").read() + "\n"
    lignes = texte.split("\n")
    fichiers = [f for f in glob.glob(os.path.join(d, "**", "*"), recursive=True) if os.path.isfile(f) and not os.path.basename(f).startswith("MANIFESTE")]
    rows, trouves = [], 0
    for f in sorted(fichiers):
        nom = os.path.basename(f)
        urls = set()
        for l in lignes:
            if nom in l:
                urls.update(u.rstrip(".,;") for u in URL.findall(l))
        if len(urls) == 1:
            origine, canal = urls.pop(), "retrouvée dans le texte du dossier ou des scripts"
            trouves += 1
        elif len(urls) > 1:
            origine, canal = "ambiguë (" + str(len(urls)) + " adresses sur les lignes citant ce fichier)", "non tranchée"
        else:
            origine, canal = "non retrouvée", "fichier dérivé ou adresse donnée ailleurs dans le texte"
        b = open(f, "rb").read()
        rows.append({"fichier": os.path.relpath(f, d).replace("\\", "/"), "url_origine": origine, "canal": canal,
                     "date": dt.datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d %H:%M"),
                     "octets": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    with open(os.path.join(d, "MANIFESTE_RECONSTITUE.csv"), "w", encoding="utf-8-sig", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["fichier", "url_origine", "canal", "date", "octets", "sha256"], delimiter=";")
        w.writeheader()
        w.writerows(rows)
    bilan.append((a, "reconstitué", len(rows), trouves))

o = ["# Manifestes reconstitués pour la vague 1",
     "",
     "**Produit le " + dt.datetime.now().strftime("%d/%m/%Y à %H h %M") + " par `scripts\\commun\\reconstituer_manifestes.py`.** "
     "Les dossiers A01, A02, A04 et A06 ont été écrits avant que le manifeste soit obligatoire. Ce script fige l'empreinte de chaque fichier conservé et retrouve l'adresse d'origine quand elle figure sans ambiguïté sur une ligne du dossier ou d'un script citant le fichier. "
     "**Une empreinte prise aujourd'hui ne prouve pas que le fichier est identique à celui du téléchargement** : elle permet seulement de détecter toute modification ultérieure.",
     "",
     "| Agent | État | Fichiers | Adresse d'origine retrouvée |",
     "|---|---|---|---|"]
for a, e, n, t in bilan:
    o.append(f"| {a} | {e} | {n} | {t} |")
o.append("")
open(os.path.join(R, "journal", "manifestes_reconstitues.md"), "w", encoding="utf-8", newline="").write("\n".join(o))
for x in bilan:
    print(x)
