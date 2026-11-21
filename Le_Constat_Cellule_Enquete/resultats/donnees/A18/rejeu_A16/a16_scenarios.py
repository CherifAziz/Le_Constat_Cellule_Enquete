# -*- coding: utf-8 -*-
"""A16 - test adverse liberal du resultat R-A15-01 / C-A15-005 d'A15
("aucune combinaison documentee n'atteint 3 % ni ne stabilise la dette avant 2035").

Le modele est celui d'A15, importe depuis une COPIE non modifiee (a15_modele_copie.py,
meme empreinte SHA-256 que scripts\\A15\\a15_modele.py). Rien n'est ecrit dans donnees\\A15.
La reference est reconstruite exactement comme dans scripts\\A15\\a15_executer.py
(calage des taux sur la Commission, convergence vers 4 % en 2032, cibles 5,5 % en 2026 et 6,5 % en 2027).

Scenarios ajoutes (regles de depense, non chiffrees par A13/A14) :
  N0   : norme "zero volume" de la depense primaire de toutes les APU a partir de 2027
         (la depense primaire croit comme le deflateur ; le vieillissement est absorbe dans la norme)
  N05  : norme "+0,5 % en volume par an" (ordre de grandeur de la moyenne francaise 2015-2019 : +0,68 %, CICE compris)
  G2   : gel en valeur en 2027 et 2028 (style Canada, S02), puis zero volume
Rendement statique a l'annee t (points de PIB) contre la reference A (ratio de depense primaire
constant + vieillissement) : X_t = P0 * (1 - prod_{u=2027..t} (1+v_u)/(1+g_u)) + vieillissement(t)
avec P0 = depense primaire 2025 = 55,1 % du PIB (table A07, calcul a16_donnees.py), g = croissance
potentielle reelle (et deflateur pour le gel), v = croissance en volume autorisee.
Multiplicateurs testes : 0 ; 0,3 ; 0,6 (composite d'A15) ; 0,8 (transferts et salaires, central d'A13).
Variante prime de risque : taux d'emission de long terme 3,5 % au lieu de 4 % (retour partiel de l'ecart
avec l'Allemagne, A07 : 51 pb en mai 2024, 147 en octobre 2026).
Sorties : donnees\\A16\\a16_scenarios.csv, a16_sortie_scenarios.txt
"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a15_modele_copie import Macro, Interets, projeter, calibrer_rm, vieillissement, ANNEES

OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18\rejeu_A16"
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)

def construire(rm_lt=4.0):
    INT = Interets()
    macro = Macro()
    rm_cal = calibrer_rm(INT, macro)
    macro.rm = dict(rm_cal)
    for a in (2029, 2030, 2031):
        macro.rm[a] = rm_cal[2028] + (rm_lt - rm_cal[2028]) * (a - 2028) / 4.0
    macro.rm_lt = rm_lt
    REF = projeter(macro, ref=None, cibles_ref={2026: 5.5, 2027: 6.5}, interets=INT)
    return INT, macro, REF

P0 = 55.1

def serie_norme(macro, v_vol, gel_annees=(), nominal=None):
    """nominal : dict annee -> croissance NOMINALE imposee (ex. trajectoire de depense nette du Conseil de l'UE,
    21/1/2025 : +1,2 % en 2026-2028, +1,1 % en 2029, F-A08-021 [C via A08]). Approximation : appliquee a la depense
    primaire totale (la depense nette du reglement deduit aussi les mesures nouvelles de recettes : borne haute de
    l'effort en depense)."""
    nominal = nominal or {}
    s, cum = {}, 1.0
    for t in ANNEES:
        if t < 2027:
            s[t] = 0.0
            continue
        g = macro.gpot[t] / 100.0
        if t in nominal:
            cum *= (1 + nominal[t]) / ((1 + g) * (1 + macro.defl[t] / 100.0))
        elif t in gel_annees:
            # gel en valeur : la depense ne suit ni les prix ni le volume
            cum *= 1.0 / ((1 + g) * (1 + macro.defl[t] / 100.0))
        else:
            cum *= (1 + v_vol) / (1 + g)
        s[t] = P0 * (1 - cum) + vieillissement(t)
    return s

def resume(nom, R, serie, m, persist):
    A = R["annees"]
    sous3 = next((t for t in ANNEES if A[t]["deficit"] <= 3.0), None)
    pic = max(ANNEES, key=lambda t: A[t]["d"] if t <= 2040 else -1)
    # stabilisation : ratio de dette en baisse d'une annee sur l'autre
    stab = next((t for t in ANNEES if t > 2027 and A[t]["d"] <= A[t - 1]["d"]), None)
    # stabilisation au sens d'A15 (a15_executer.py, fonction atteint) : deficit <= dette(t-1) x gn/(1+gn),
    # gn = croissance nominale tendancielle (potentiel x deflateur)
    def stab_A15(t):
        gn = (1 + MACRO[0].gpot[t] / 100.0) * (1 + MACRO[0].defl[t] / 100.0) - 1
        return A[t]["deficit"] <= A[t - 1]["d"] * gn / (1 + gn)
    stab15 = next((t for t in ANNEES if t >= 2028 and stab_A15(t)), None)
    l = dict(scenario=nom, multiplicateur=m, effet_persistant=persist,
             mesure_statique_2030=serie.get(2030, 0), mesure_statique_2035=serie.get(2035, 0),
             deficit_2027=A[2027]["deficit"], deficit_2030=A[2030]["deficit"], deficit_2035=A[2035]["deficit"],
             dette_2030=A[2030]["d"], dette_2035=A[2035]["d"], dette_2050=A[2050]["d"],
             premiere_annee_sous_3=sous3, premiere_annee_ratio_en_baisse=stab,
             premiere_annee_stabilisation_def_A15=stab15,
             annee_pic_dette_fenetre_2026_2040=(pic if pic < 2040 else "aucun pic avant 2040"))
    log(f"{nom:34s} m={m:<4} pers={str(persist):5s} stat30 {l['mesure_statique_2030']:.2f} stat35 {l['mesure_statique_2035']:.2f} | "
        f"def 27/30/35 {A[2027]['deficit']:.1f}/{A[2030]['deficit']:.1f}/{A[2035]['deficit']:.1f} | dette 30/35/50 "
        f"{A[2030]['d']:.0f}/{A[2035]['d']:.0f}/{A[2050]['d']:.0f} | <3% en {sous3} | ratio en baisse des {stab} | stab. A15 {stab15} | pic {l['annee_pic_dette_fenetre_2026_2040']}")
    return l

lignes = []
MACRO = [None]
for rm_lt in (4.0, 3.5):
    INT, macro, REF = construire(rm_lt)
    MACRO[0] = macro
    log(f"--- taux d'emission de long terme {rm_lt} %")
    lignes.append(resume(f"Reference A (rm_lt {rm_lt})", REF, {}, "-", False))
    scen = {"N0 zero volume": serie_norme(macro, 0.0),
            "N025 +0,25 % volume": serie_norme(macro, 0.0025),
            "N05 +0,5 % volume": serie_norme(macro, 0.005),
            "G2 gel valeur 2027-28 puis N0": serie_norme(macro, 0.0, gel_annees=(2027, 2028)),
            "UE trajectoire 2027-29 puis N0": serie_norme(macro, 0.0, nominal={2027: 0.012, 2028: 0.012, 2029: 0.011}),
            "UE trajectoire 2027-29 puis N05": serie_norme(macro, 0.005, nominal={2027: 0.012, 2028: 0.012, 2029: 0.011})}
    for nom, s in scen.items():
        for m in (0.0, 0.3, 0.6, 0.8):
            for persist in ((False, True) if m in (0.6,) else (False,)):
                R = projeter(macro, {"norme": s}, {"norme": m}, ref=REF, interets=INT, persistant=persist)
                l = resume(f"{nom} (rm_lt {rm_lt})", R, s, m, persist)
                lignes.append(l)

cols = list(lignes[1].keys())
with open(os.path.join(OUT, "a16_scenarios.csv"), "w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=cols, delimiter=";")
    w.writeheader()
    for l in lignes:
        w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})
with open(os.path.join(OUT, "a16_sortie_scenarios.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
