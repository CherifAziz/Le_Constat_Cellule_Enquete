# -*- coding: utf-8 -*-
"""C03 - copie les quatre scripts d'A15 dans scripts\\C03 et redirige leurs sorties vers
donnees\\C03\\rejeu_A15 (aucune ecriture dans donnees\\A15). Seule la ligne SORTIE de la copie
de a15_modele.py est changee ; les trois autres scripts importent SORTIE de ce module.
Lancer une fois : python -I c03_patch_copie.py"""
import os, shutil
RAC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
SRC = os.path.join(RAC, "scripts", "A15")
DST = os.path.join(RAC, "scripts", "C03")
OUT = os.path.join(RAC, "donnees", "C03", "rejeu_A15")
os.makedirs(OUT, exist_ok=True)
for n in ("a15_modele.py", "a15_executer.py", "a15_validation.py", "a15_historique.py"):
    shutil.copy2(os.path.join(SRC, n), os.path.join(DST, n))   # lecture seule de la source
P = os.path.join(DST, "a15_modele.py")
s = open(P, encoding="utf-8").read()
old = 'SORTIE = os.path.join(DON, "A15")\n'
assert s.count(old) == 1
s = s.replace(old, 'SORTIE = os.path.join(DON, "C03", "rejeu_A15")   # C03 : sorties redirigees (copie)\n')
open(P, "w", encoding="utf-8").write(s)
print("copies faites, SORTIE ->", OUT)
