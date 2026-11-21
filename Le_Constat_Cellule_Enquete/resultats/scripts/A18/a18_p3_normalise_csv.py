# -*- coding: utf-8 -*-
"""A18 - normalise les deux CSV de sortie (separateur ';', champs entre guillemets).
Les separateurs de colonnes ne sont jamais suivis d'une espace ; les ' ; ' internes au texte le sont.
Controle : meme nombre de champs que l'en-tete sur chaque ligne, sinon arret."""
import csv, re, sys
D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18"
for f in ("A18_arbitrage.csv", "A18_verification_25.csv"):
    p = D + "\\" + f
    lines = open(p, encoding="utf-8").read().splitlines()
    rows = [re.split(r";(?! )", ln) for ln in lines if ln.strip()]
    n = len(rows[0])
    bad = [(i, len(r)) for i, r in enumerate(rows) if len(r) != n]
    if bad:
        sys.exit(f"{f} : lignes non conformes {bad}")
    rows = [[c.strip() for c in r] for r in rows]
    with open(p, "w", encoding="utf-8", newline="") as h:
        csv.writer(h, delimiter=";", quoting=csv.QUOTE_ALL).writerows(rows)
    back = list(csv.reader(open(p, encoding="utf-8"), delimiter=";"))
    print(f, "colonnes", n, "lignes", len(back), "toutes conformes :", all(len(r) == n for r in back))
