# -*- coding: utf-8 -*-
"""S01 - assemble les lots (donnees/S01/lots/lot_*.csv) en une table unique
S01_mesures_1975_1999.csv, en controlant 14 colonnes par ligne.
Usage : python -I s01_assembler.py
"""
import os, glob, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S01"
ENTETE = "annee;texte;date;mesure;sens;montant_annonce;unite;montant_constate;perimetre;temporaire_ou_permanent;source;page;provenance;remarque"
lignes = [ENTETE]
erreurs = 0
for f in sorted(glob.glob(os.path.join(R, "lots", "lot_*.csv"))):
    for i, l in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        if not l.strip():
            continue
        n = len(l.split(";"))
        if n != 14:
            print(f"ERREUR {os.path.basename(f)} ligne {i} : {n} colonnes -> {l[:120]}")
            erreurs += 1
        lignes.append(l)
lignes = [lignes[0]] + sorted(lignes[1:], key=lambda x: x.split(";")[0])
with open(os.path.join(R, "S01_mesures_1975_1999.csv"), "w", encoding="utf-8") as g:
    g.write("\n".join(lignes) + "\n")
print(f"{len(lignes)-1} lignes, {erreurs} erreurs")
