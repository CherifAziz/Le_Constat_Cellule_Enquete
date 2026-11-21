# -*- coding: utf-8 -*-
"""Rattache les pièces de la vague 1 (A01, A02, A04, A06) à leur adresse d'origine PAR PREUVE :
retélécharge chaque adresse citée dans le dossier ou ses scripts, calcule l'empreinte SHA-256
et la compare à celle des fichiers conservés. Une correspondance prouve que le fichier conservé
est identique à ce que l'adresse sert aujourd'hui. Ne modifie aucun fichier d'agent.

Usage : python -I scripts/commun/rattacher_origines.py   (depuis resultats/)
Sorties : donnees/<agent>/MANIFESTE_RATTACHE.csv ; section ajoutée à journal/manifestes_reconstitues.md
"""
import csv
import datetime as dt
import glob
import hashlib
import os
import re
import sys

import requests

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENTS = ["A01", "A02", "A04", "A06"]
URL = re.compile(r"https?://[^\s)\]>`|\"'«»]+")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"}
MAXO = 60 * 1024 * 1024
bilan = []
for a in AGENTS:
    d = os.path.join(R, "donnees", a)
    locaux = {}
    for f in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isfile(f) and not os.path.basename(f).startswith("MANIFESTE"):
            locaux.setdefault(hashlib.sha256(open(f, "rb").read()).hexdigest(), []).append(os.path.relpath(f, d).replace("\\", "/"))
    texte = ""
    for p in glob.glob(os.path.join(R, "agents", a + "*.md")) + glob.glob(os.path.join(R, "scripts", a, "*.py")):
        texte += open(p, encoding="utf-8", errors="replace").read() + "\n"
    urls = sorted({u.rstrip(".,;:") for u in URL.findall(texte)})
    rows, ok, ko = [], 0, 0
    for u in urls:
        try:
            r = requests.get(u, headers=UA, timeout=35, stream=True)
            b = b""
            for chunk in r.iter_content(1 << 16):
                b += chunk
                if len(b) > MAXO:
                    break
            h = hashlib.sha256(b).hexdigest()
            if h in locaux and len(b) <= MAXO:
                ok += 1
                for f in locaux[h]:
                    rows.append({"fichier": f, "url_origine": u, "canal": "retéléchargé le " + dt.datetime.now().strftime("%d/%m/%Y") + " : empreinte identique", "octets": len(b), "sha256": h})
            else:
                ko += 1
        except Exception:
            ko += 1
    with open(os.path.join(d, "MANIFESTE_RATTACHE.csv"), "w", encoding="utf-8-sig", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["fichier", "url_origine", "canal", "octets", "sha256"], delimiter=";")
        w.writeheader()
        w.writerows(rows)
    nf = sum(len(v) for v in locaux.values())
    rattaches = len({r["fichier"] for r in rows})
    bilan.append((a, nf, len(urls), ok, rattaches))
    print(a, "fichiers", nf, "| adresses citées", len(urls), "| adresses servant un fichier conservé", ok, "| fichiers rattachés", rattaches, flush=True)

p = os.path.join(R, "journal", "manifestes_reconstitues.md")
t = open(p, encoding="utf-8").read()
MARQ = "\n## Rattachement par preuve"
if MARQ in t:
    t = t[:t.index(MARQ)]
t = t.rstrip("\n") + "\n" + MARQ + " (" + dt.datetime.now().strftime("%d/%m/%Y, %H h %M") + ")\n\n"
t += ("Par `scripts\\commun\\rattacher_origines.py` : chaque adresse citée dans le dossier ou ses scripts a été retéléchargée et son empreinte comparée à celles des fichiers conservés. "
      "Un fichier « rattaché » est **identique octet pour octet** à ce que son adresse sert aujourd'hui. Un fichier non rattaché n'est pas pour autant douteux : fichier dérivé (table, extraction de texte), "
      "interface de données dont la réponse a changé depuis, adresse absente du texte, ou site qui refuse les requêtes automatiques.\n\n"
      "| Agent | Fichiers conservés | Adresses citées | Adresses servant un fichier conservé | Fichiers rattachés par preuve |\n|---|---|---|---|---|\n")
for a, nf, nu, ok, ra in bilan:
    t += f"| {a} | {nf} | {nu} | {ok} | {ra} |\n"
open(p, "w", encoding="utf-8", newline="").write(t)
print("fini", flush=True)
