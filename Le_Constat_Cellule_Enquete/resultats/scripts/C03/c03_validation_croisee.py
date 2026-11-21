# -*- coding: utf-8 -*-
"""C03 - validation du plus gros terme dans le code d'origine (copies, dossiers de sortie propres) :
(1) copie d'a15_executer.py avec CIBLES_REF[2027] = 5,4 (reference Codex) -> scripts\\C03\\val54\\, sorties donnees\\C03\\val_ref54\\
(2) copie de scenarios.py (Codex) avec PRIMARY_2027 = -3,5 (deficit 6,5 - interets 3,0) -> donnees\\C03\\copies_codex_val65\\
(3) copie de scenarios.py avec PRIMARY_2027 = -2,0 (deficit 5,0, cible du PLF - interets 3,0) -> donnees\\C03\\copies_codex_val50\\
Les fichiers d'origine ne sont que lus. Lancer : python -I -B c03_validation_croisee.py"""
import os, shutil, subprocess, sys
RAC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
CDX = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\resultats\codex\scenarios.py"
V = os.path.join(RAC, "scripts", "C03", "val54")
os.makedirs(V, exist_ok=True)
os.makedirs(os.path.join(RAC, "donnees", "C03", "val_ref54"), exist_ok=True)
m = open(os.path.join(RAC, "scripts", "A15", "a15_modele.py"), encoding="utf-8").read()
old = 'SORTIE = os.path.join(DON, "A15")\n'
assert m.count(old) == 1
open(os.path.join(V, "a15_modele.py"), "w", encoding="utf-8").write(
    m.replace(old, 'SORTIE = os.path.join(DON, "C03", "val_ref54")   # C03 : copie de validation\n'))
e = open(os.path.join(RAC, "scripts", "A15", "a15_executer.py"), encoding="utf-8").read()
old = "CIBLES_REF = {2026: 5.5, 2027: 6.5}"
assert e.count(old) == 1
open(os.path.join(V, "a15_executer.py"), "w", encoding="utf-8").write(
    e.replace(old, "CIBLES_REF = {2026: 5.5, 2027: 5.4}  # C03 : reference Codex (Commission, budget compris)"))
subprocess.run([sys.executable, "-I", "-B", os.path.join(V, "a15_executer.py")], stdout=subprocess.DEVNULL, check=True)
for l in open(os.path.join(RAC, "donnees", "C03", "val_ref54", "A15_objectifs_horizons.csv"), encoding="utf-8"):
    if ";stabilisation;2030;" in l and l.startswith("A "):
        print("A15 d'origine, reference 5,4 : stabilisation 2030 =", l.split(";")[4])

c = open(CDX, encoding="utf-8").read()
old = "PRIMARY_2027 = -2.4"
assert c.count(old) == 1
for nom, val in (("copies_codex_val65", "-3.5"), ("copies_codex_val50", "-2.0")):
    D = os.path.join(RAC, "donnees", "C03", nom)
    os.makedirs(D, exist_ok=True)
    P = os.path.join(D, "scenarios.py")
    open(P, "w", encoding="utf-8").write(c.replace(old, "PRIMARY_2027 = " + val + "   # C03 : variante"))
    out = subprocess.run([sys.executable, "-I", "-B", P], capture_output=True, cwd=D).stdout.decode("utf-8", "replace")
    for l in out.splitlines():
        if l.startswith("ratio stable en 2030"):
            print("Codex d'origine, PRIMARY_2027 =", val, ":", l[:60])
