# -*- coding: utf-8 -*-
"""
Controle de couverture des manifestes (orchestrateur).
Pour chaque agent : chaque fichier de donnees/Axx/sources/ a-t-il une ligne de manifeste
donnant une URL d'origine ? Les extractions de texte (.txt) derivees d'un PDF ou d'un HTML
de meme nom sont rattachees a leur piece.

Usage : python -I controle_manifestes.py A03 A05 A06 A07 A10
"""
import csv
import glob
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def lire_manifestes(agent):
    """Retourne {nom_de_fichier: url} a partir de tous les CSV de type manifeste/journal de l'agent."""
    d = os.path.join(R, "donnees", agent)
    m = {}
    fichiers = []
    for motif in ("**/*anifest*.csv", "**/*ANIFEST*.csv", "**/journal_telechargements*.csv"):
        fichiers += glob.glob(os.path.join(d, motif), recursive=True)
    for f in sorted(set(fichiers)):
        brut = open(f, encoding="utf-8-sig", errors="replace").read()
        sep = ";" if brut.count(";") > brut.count(",") else ","
        for ligne in csv.reader(brut.splitlines(), delimiter=sep):
            urls = [c for c in ligne if re.match(r"https?://", c.strip())]
            if not urls:
                continue
            for c in ligne:
                c = c.strip()
                if c and not c.startswith("http") and re.search(r"\.[A-Za-z0-9]{2,5}$", c):
                    m[os.path.basename(c.replace("\\", "/"))] = urls[0]
    return m, [os.path.relpath(f, d) for f in sorted(set(fichiers))]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for agent in sys.argv[1:]:
        src = os.path.join(R, "donnees", agent, "sources")
        manifeste, fichiers_m = lire_manifestes(agent)
        tous = [p for p in glob.glob(os.path.join(src, "**", "*"), recursive=True) if os.path.isfile(p)]
        pieces, derives, sans = [], [], []
        noms = {os.path.basename(p) for p in tous}
        for p in tous:
            n = os.path.basename(p)
            if re.search(r"(?i)manifest|journal_telechargements|extraits_pieces", n):
                continue
            racine = re.sub(r"(_clean|_p\d+-\d+|_page\d+)?\.(txt|png)$", "", n)
            est_derive = n.lower().endswith((".txt", ".png")) and any(
                o != n and o.startswith(racine) and not o.lower().endswith((".txt", ".png")) for o in noms)
            if est_derive:
                derives.append(n)
            elif n in manifeste:
                pieces.append(n)
            else:
                sans.append(os.path.relpath(p, src))
        print(f"### {agent}")
        print(f"- Manifestes trouvés : {', '.join(fichiers_m) if fichiers_m else 'AUCUN'}")
        print(f"- Fichiers dans sources\\ : {len(tous)} ; pièces avec URL d'origine : {len(pieces)} ; extractions dérivées : {len(derives)} ; **sans URL d'origine : {len(sans)}**")
        if sans:
            print("- Sans URL : " + " ; ".join(sans[:25]) + (" ; …" if len(sans) > 25 else ""))
        print()


if __name__ == "__main__":
    main()
