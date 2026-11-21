# -*- coding: utf-8 -*-
"""C02 - Annees d'excedent primaire S13 selon trois conventions (t_3201 base commune), et ligne CICE 2017-2020.
Lancer : python -I C02_excedents_primaires.py"""
import sys, os, warnings
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from C02_verifications import lire_ligne_annees, COMMUN  # noqa (le module recalcule (a)-(d) a l'import)
t = lire_ligne_annees(os.path.join(COMMUN, "insee_cn_t_3201.xlsx"), 0, 3, [12, 13, 30, 41, 61, 66])
B9, D41, D41G, D41R, CIdep, CIrec = (t[n]["v"] for n in (66, 12, 13, 41, 30, 61))
A = range(1975, 2026)
c1 = [a for a in A if B9[a] + D41[a] > 0]
c2 = [a for a in A if B9[a] + D41G[a] > 0]
c3 = [a for a in A if B9[a] + D41[a] - D41R[a] > 0]
print("\n=== Excedents primaires 1975-2025 ===")
print("D41 verses (l.12) :", len(c1), c1)
print("D41 hors SIFIM (l.13) :", len(c2), c2)
print("D41 verses - D41 recus (l.12-l.41) :", len(c3), c3)
print("Apres 2001 :", [a for a in c1 + c2 + c3 if a > 2001])
for a in (2001, 2002, 2017, 2018, 2019, 2020):
    print(a, "primaire D41 = %.2f ; D41G = %.2f ; net = %.2f ; credits d'impot en depense %.2f / en recette %.2f"
          % (B9[a] + D41[a], B9[a] + D41G[a], B9[a] + D41[a] - D41R[a], CIdep[a], CIrec[a]))
