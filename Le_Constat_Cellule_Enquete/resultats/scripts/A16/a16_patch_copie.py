# -*- coding: utf-8 -*-
"""A16 - fabrique a15_executer_copie.py a partir de la copie brute de scripts\\A15\\a15_executer.py :
1) redirige SORTIE vers donnees\\A16\\rejeu_A15 (aucune ecriture dans donnees\\A15) ;
2) ajoute en fin de fichier les tests adverses d'A16 (K1 et K5, multiplicateurs de depense nuls ou negatifs).
Lancer une seule fois apres la copie : python -I a16_patch_copie.py"""
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a15_executer_copie.py")
s = open(P, encoding="utf-8").read()
if "A16 : sorties redirigees" in s:
    raise SystemExit("deja patche")
marker = "PIB_2025, DETTE_2025, SOLDE_2025, DON, SORTIE, SEMI_ELAST)\n"
assert "from a15_modele_copie import" in s and marker in s
s = s.replace(marker, marker + "# A16 : sorties redirigees hors du dossier d'A15 (copie de contre-expertise)\n"
              "SORTIE = r\"C:\\Users\\oussa\\Downloads\\Le_Constat_Cellule_Enquete\\Le_Constat_Cellule_Enquete\\resultats\\donnees\\A16\\rejeu_A15\"\n", 1)
s += r'''

# ====================================================================== A16 : tests adverses ajoutes
log("")
log("=== A16 : K1 et K5 avec multiplicateurs de depense nuls ou negatifs")
DEP_CATS = {"salaires_publics", "demande_publique", "transferts_menages", "pensions", "sante_rembt", "subventions", "local_invest"}
a16 = []
for K in (COMBIS[0], COMBIS[4]):
    for m_dep, m_po in ((None, None), (0.0, None), (-0.3, None), (-0.5, None), (0.0, 0.0), (-0.5, 0.0)):
        mes, mult = mesures_de(K["ids"], "central", None, mult_var=1)
        for i in list(mult):
            cat = TOUTES[i]["cat"]
            if m_dep is not None and cat in DEP_CATS:
                mult[i] = m_dep
            if m_po is not None and cat in ("PO", "PO_entreprises"):
                mult[i] = m_po
        R = projeter(macro, mes, mult, ref=REF, interets=INT)
        A = R["annees"]
        sous3 = next((t for t in ANNEES if A[t]["deficit"] <= 3.0), None)
        MACRO_OBJ[0] = macro
        stab = next((t for t in ANNEES if t >= 2028 and atteint("stabilisation", R, t)), None)
        part_dep = sum(mes[i][2030] for i in mes if TOUTES[i]["cat"] in DEP_CATS) / max(1e-9, sum(mes[i][2030] for i in mes))
        l = dict(combinaison=K["nom"], mult_depense=("A13 central" if m_dep is None else m_dep),
                 mult_prelevements=("A14/A13 central" if m_po is None else m_po), part_depense_statique_2030=part_dep,
                 deficit_2030=A[2030]["deficit"], deficit_2035=A[2035]["deficit"], dette_2035=A[2035]["d"],
                 premiere_annee_sous_3=sous3, premiere_annee_stabilisation_def_A15=stab)
        a16.append(l)
        log(f"{K['nom'][:26]:26s} m_dep={str(l['mult_depense']):11s} m_PO={str(l['mult_prelevements']):15s} part dep {part_dep:.2f} "
            f"def30 {A[2030]['deficit']:.2f} def35 {A[2035]['deficit']:.2f} dette35 {A[2035]['d']:.1f} <3% {sous3} stab {stab}")
ecrire("A16_K_multiplicateurs_nuls_negatifs.csv", a16)
with open(os.path.join(SORTIE, "A16_sortie_tests.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
'''
open(P, "w", encoding="utf-8").write(s)
print("patch applique")
