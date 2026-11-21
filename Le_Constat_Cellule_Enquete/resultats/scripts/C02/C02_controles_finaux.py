# -*- coding: utf-8 -*-
"""C02 - Controles complementaires : niveaux du ratio de dette apres crises ; marges de (a) ; 2019 primaire en % PIB ; rapprochement K06.
Lancer : python -I C02_controles_finaux.py"""
import sys, os, csv, warnings, io, contextlib
warnings.filterwarnings("ignore"); sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_o = sys.stdout
sys.stdout = open(os.devnull, "w", encoding="utf-8")
import C02_verifications as V
sys.stdout.close(); sys.stdout = _o
r = {a: V.dette[a] / V.PIB[a] * 100 for a in range(1978, 2026)}
print("=== Ratio de dette (% PIB, dette base commune / PIB t_3106 l.29) ===")
for ref in (1980, 1992, 2007, 2019):
    after = [a for a in range(ref + 1, 2026) if r[a] <= r[ref]]
    print("niveau %d = %.1f ; annees ulterieures a un niveau <= : %s" % (ref, r[ref], after if after else "aucune"))
print("min 1993-2025 : %.1f (%d)" % min((r[a], a) for a in range(1993, 2026)))
print("\n=== Marges de (a) : deficit - investissement net (Md EUR) ===")
for a in (1975, 1976, 1977, 1978, 1979, 1980, 1981):
    d = -V.B9[a]; inv = V.P51G[a] - V.P51C[a]
    print(a, "deficit %.3f ; inv net %.3f ; marge %.3f" % (d, inv, d - inv))
print("\n=== 2019 ===")
print("primaire D41 2019 = %.2f Md EUR = %.2f %% du PIB (PIB %.1f)" % (V.B9[2019] + V.I[2019], (V.B9[2019] + V.I[2019]) / V.PIB[2019] * 100, V.PIB[2019]))
print("\n=== K06 : rapprochement zone euro avec / sans France (poids 18,8 %) ===")
for x in (7.7, 7.8, 2.5):
    print("%.1f / (1 - 0,188) = %.2f" % (x, x / (1 - 0.188)))
