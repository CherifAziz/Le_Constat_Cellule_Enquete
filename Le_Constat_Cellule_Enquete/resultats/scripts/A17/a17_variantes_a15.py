# -*- coding: utf-8 -*-
"""A17 - variantes keynesiennes du modele d'A15, sur COPIE.
Lancer : python -I a17_variantes_a15.py   (depuis scripts\\A17)
Prerequis : scripts\\A17\\a15_modele.py et a15_executer.py sont des copies conformes des scripts d'A15
(empreinte de a15_executer.py identique ; a15_modele.py ne differe que par SORTIE, redirige vers
donnees\\A17\\a15_rejeu). La relance de la copie reproduit A15_sortie_executer.txt octet pour octet.
L'import de a15_executer rejoue toute la chaine d'A15 (ecrit dans donnees\\A17\\a15_rejeu, jamais dans donnees\\A15).

Variantes :
 V1  seuil de taux a l'emission de long terme (rm_lt) au-dela duquel K1 et K5 ne stabilisent plus le ratio
     (dette 2040 <= dette 2035), avec le deflateur d'A15 (1,75 % apres 2030) et avec 2,0 % (cible de la BCE).
 V2  grille rm_lt x deflateur : effort de stabilisation et de 3 % a l'horizon 2030 ; dette 2035 et 2050 sous K1 et K5.
 V3  test de credibilite d'A08 sans la part de l'ecart due a l'optimisme de croissance (0,6 a 0,9 pt sur 2,1 a h=3,
     A08 R3) : derive d'execution reduite a 57 % ou 71 % de la derive totale ; version plafonnee comme A15.
 V4  multiplicateurs forts et persistants appliques a K5 (A15 ne le fait que pour K1).
"""
import os, sys, copy, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a15_executer as X   # rejoue la chaine d'A15 (sorties redirigees)
from a15_modele import projeter, ANNEES

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
SORTIE = os.path.join(RACINE, "donnees", "A17")
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

def macro_k(rm_lt, defl_lt=1.75):
    m = X.macro_var(rm_lt=rm_lt)
    m.choc_taux = 0.0
    for a in ANNEES:
        if a >= 2031:
            m.defl[a] = defl_lt
            m.ipch[a] = 1.9 + (defl_lt - 1.75)
    return m

K = {c["nom"][:2]: c["ids"] for c in X.COMBIS}

def traj(ids, m, mv=1, persistant=False):
    mes, mult = X.mesures_de(ids, "central", None, mult_var=mv)
    return projeter(m, mes, mult, ref=X.REF, interets=X.INT, persistant=persistant)

log("=== Controle : K1 et K5 centrales, parametres d'A15 (doit redonner A15) ===")
for k in ("K1", "K5"):
    R = traj(K[k], macro_k(4.0))
    A = R["annees"]
    log(f"{k}: deficit 2030 {A[2030]['deficit']:.2f} 2035 {A[2035]['deficit']:.2f} ; dette 2035 {A[2035]['d']:.1f} 2040 {A[2040]['d']:.1f} 2050 {A[2050]['d']:.1f} ; g_nom 2040 {A[2040]['g_nom']:.2f}")

# ------------------------------------------------------------------ V1 seuil de stabilisation
log("=== V1 : seuil de rm_lt pour que la dette 2040 <= dette 2035 ===")
v1 = []
for defl in (1.75, 2.0):
    for k in ("K1", "K5"):
        def stable(r):
            A = traj(K[k], macro_k(r, defl))["annees"]
            return A[2040]["d"] <= A[2035]["d"]
        lo, hi = 0.5, 6.0
        if not stable(lo):
            seuil = None
        else:
            for _ in range(40):
                mid = (lo + hi) / 2
                if stable(mid):
                    lo = mid
                else:
                    hi = mid
            seuil = lo
        A = traj(K[k], macro_k(4.0, defl))["annees"]
        gl = A[2040]["g_nom"]
        v1.append(dict(deflateur_long_terme=defl, combinaison=k, seuil_rm_lt=seuil, croissance_nominale_2040=gl,
                       seuil_moins_g=(seuil - gl) if seuil is not None else None))
        log(f"deflateur {defl}: {k} stabilise (2035-2040) si rm_lt <= {seuil if seuil is None else round(seuil,2)} % ; g_nom long terme {gl:.2f} % ; "
            f"ecart admissible r-g = {('n.d.' if seuil is None else round(seuil-gl,2))} pt (hypothese A15 : 4,0 - 2,77 = +1,23)")

# ------------------------------------------------------------------ V2 grille
log("=== V2 : grille rm_lt x deflateur ===")
v2 = []
for defl in (1.75, 2.0):
    for r in (2.8, 3.2, 3.6, 4.0, 4.4):
        m = macro_k(r, defl)
        s_stab, _ = X.effort("stabilisation", 2030, macro_=m, maintien_jusqua=2035)
        s_3, _ = X.effort("trois", 2030, macro_=m, maintien_jusqua=2035)
        A1 = traj(K["K1"], m)["annees"]; A5 = traj(K["K5"], m)["annees"]
        R0 = projeter(m, ref=X.REF, interets=X.INT)["annees"]
        l = dict(deflateur_long_terme=defl, rm_lt=r, effort_stab_2030_pts=s_stab[2030], effort_3pct_2030_pts=s_3[2030],
                 ref_dette_2035=R0[2035]["d"], K1_deficit_2035=A1[2035]["deficit"], K1_dette_2035=A1[2035]["d"], K1_dette_2050=A1[2050]["d"],
                 K5_deficit_2035=A5[2035]["deficit"], K5_dette_2035=A5[2035]["d"], K5_dette_2040=A5[2040]["d"], K5_dette_2050=A5[2050]["d"])
        v2.append(l)
        log(f"defl {defl} rm_lt {r}: effort stab 2030 {s_stab[2030]:.2f} pts ; 3 % 2030 {s_3[2030]:.2f} ; ref dette 2035 {R0[2035]['d']:.0f} ; "
            f"K1 def 2035 {A1[2035]['deficit']:.1f} dette 2035 {A1[2035]['d']:.0f} 2050 {A1[2050]['d']:.0f} ; "
            f"K5 def 2035 {A5[2035]['deficit']:.1f} dette 2035 {A5[2035]['d']:.0f} 2040 {A5[2040]['d']:.0f} 2050 {A5[2050]['d']:.0f}")

# ------------------------------------------------------------------ V3 derive A08 sans la part croissance
log("=== V3 : credibilite A08, part 'croissance' retiree (version plafonnee, comme R-A15-04) ===")
v3 = []
for part_exec in (1.0, 0.71, 0.57):
    for dn in ("hors crises",):
        dv = X.DERIVES[dn]; lg = X.LONG[dn]
        der = {y: (dv.get(y, lg) * part_exec if y >= 2027 else 0.0) for y in ANNEES}
        for k in ("K1", "K5"):
            mes, mult = X.mesures_de(K[k])
            tot = {y: sum(sv[y] for sv in mes.values()) for y in ANNEES}
            kk = {y: (max(0.0, 1 + der[y] / tot[y]) if tot[y] > 0 else 1.0) for y in ANNEES}
            mes2 = {i: {y: v * kk[y] for y, v in sv.items()} for i, sv in mes.items()}
            R = projeter(X.macro, mes2, mult, ref=X.REF, interets=X.INT)["annees"]
            B = projeter(X.macro, mes, mult, ref=X.REF, interets=X.INT)["annees"]
            v3.append(dict(part_execution_de_la_derive=part_exec, derive=dn, combinaison=k,
                           taux_execution_2030=kk[2030], deficit_2030_programme=B[2030]["deficit"], deficit_2030_derive=R[2030]["deficit"],
                           dette_2035_programme=B[2035]["d"], dette_2035_derive=R[2035]["d"], dette_2035_reference=X.REF["annees"][2035]["d"]))
            log(f"part {part_exec:.2f} {dn} {k}: mesures executees en 2030 a {100*kk[2030]:.0f} % ; deficit 2030 {B[2030]['deficit']:.1f} -> {R[2030]['deficit']:.1f} "
                f"(ref {X.REF['annees'][2030]['deficit']:.1f}) ; dette 2035 {B[2035]['d']:.0f} -> {R[2035]['d']:.0f} (ref {X.REF['annees'][2035]['d']:.0f})")

# ------------------------------------------------------------------ V4 multiplicateurs forts et persistants sur K5
log("=== V4 : multiplicateurs forts et persistants ===")
v4 = []
for k in ("K1", "K5"):
    for lab, mv, pers in (("central", 1, False), ("forts", 2, False), ("forts et persistants", 2, True)):
        A = traj(K[k], X.macro, mv=mv, persistant=pers)["annees"]
        v4.append(dict(combinaison=k, multiplicateurs=lab, deficit_2030=A[2030]["deficit"], deficit_2035=A[2035]["deficit"],
                       dette_2035=A[2035]["d"], dette_2050=A[2050]["d"], gain_dette_2035_vs_ref=X.REF["annees"][2035]["d"] - A[2035]["d"]))
        log(f"{k} {lab:22s}: deficit 2030 {A[2030]['deficit']:.1f} 2035 {A[2035]['deficit']:.1f} ; dette 2035 {A[2035]['d']:.0f} 2050 {A[2050]['d']:.0f} ; "
            f"gain de dette en 2035 contre la reference {X.REF['annees'][2035]['d'] - A[2035]['d']:.1f} pts")

def ecrire(nom, lignes):
    with open(os.path.join(SORTIE, nom), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(lignes[0].keys()), delimiter=";")
        w.writeheader()
        for l in lignes:
            w.writerow({kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in l.items()})
ecrire("a17_V1_seuil_taux.csv", v1)
ecrire("a17_V2_grille_taux_deflateur.csv", v2)
ecrire("a17_V3_credibilite_sans_croissance.csv", v3)
ecrire("a17_V4_multiplicateurs.csv", v4)
with open(os.path.join(SORTIE, "a17_sortie_variantes_a15.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
