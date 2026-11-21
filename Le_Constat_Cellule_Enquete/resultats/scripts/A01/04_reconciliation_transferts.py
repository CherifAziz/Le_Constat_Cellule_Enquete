"""A01 - Réconciliation des sous-secteurs et transferts entre administrations, 1978-2025.
Entrée : resultats/donnees/A01/A01_t32xx_long.csv (script 02), insee_cn_t_3216.xlsx (impôts affectés aux ASSO).
Sorties (resultats/donnees/A01) :
  A01_reconciliation_sous_secteurs.csv : par année, contrôles d'additivité et décomposition de l'écart
      (somme non consolidée des dépenses APUC+APUL+ASSO) - (dépense consolidée S13)
      = somme D73 versés + D9 inter-APU + D41 inter-APU + résidu ; même chose pour les recettes.
  A01_flux_d73_par_sous_secteur.csv : D73 versés / reçus, D733 reçus, D9 versés/reçus par sous-secteur (Md€).
  A01_attribution_conventions.csv : solde par sous-secteur selon 5 conventions (voir docstring de chaque) ;
      contrôle : chaque convention somme au B9 de S13.
Niveaux : niveau 1 = APUC (S1311), APUL (S1313), ASSO (S1314) ; niveau 2 = État (S13111) / ODAC (S13112) au sein d'APUC.
Relançable : python -I 04_reconciliation_transferts.py
"""
import os, csv, openpyxl, sys
from collections import defaultdict

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
A01 = os.path.join(RACINE, "resultats", "donnees", "A01")

CLES = {  # (section, préfixe du libellé) -> code
    ("DEPENSES", "Total des dépenses"): "dep", ("RECETTES", "Total des recettes"): "rec",
    ("SOLDES", "Capacité (+) ou besoin (-)"): "b9",
    ("DEPENSES", "Intérêts (D41)"): "d41p", ("RECETTES", "Intérêts (D41)"): "d41r",
    ("DEPENSES", "Transferts courants entre administrations publiques"): "d73p",
    ("RECETTES", "Transferts courants entre administrations publiques"): "d73r",
    ("RECETTES", "Transferts de recettes fiscales"): "d733r",
    ("DEPENSES", "Transferts en capital à payer"): "d9p",
    ("RECETTES", "Transferts en capital"): "d9r",
}
V = defaultdict(dict)
with open(os.path.join(A01, "A01_t32xx_long.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter=";"):
        for (sec, pre), code in CLES.items():
            if r["section"] == sec and r["poste"].strip().startswith(pre):
                try:
                    V[(r["secteur"], code)][int(r["annee"])] = float(r["valeur_mdeur"])
                except ValueError:
                    pass
# garde-fou : chaque clé doit exister pour les secteurs utilisés
for s in ["S13", "S1311", "S13111", "S13112", "S1313", "S1314"]:
    for code in set(CLES.values()):
        if not V[(s, code)]:
            sys.exit(f"ERREUR : aucune valeur pour {s}/{code} (libellé non reconnu)")

# impôts (hors cotisations) des ASSO, prélèvements obligatoires t_3216 ligne 13 (Md€)
ws = openpyxl.load_workbook(os.path.join(COMMUN, "insee_cn_t_3216.xlsx"), read_only=True, data_only=True).worksheets[0]
rows = list(ws.iter_rows(values_only=True))
IMPOTS_ASSO = {int(an): rows[12][j] for j, an in enumerate(rows[2]) if isinstance(an, (int, float)) and isinstance(rows[12][j], (int, float))}
COTIS_ASSO = {int(an): rows[13][j] for j, an in enumerate(rows[2]) if isinstance(an, (int, float)) and isinstance(rows[13][j], (int, float))}

def v(s, c, a):
    return V[(s, c)].get(a, 0.0)

N1 = ["S1311", "S1313", "S1314"]
rec_rows, flux_rows, conv_rows = [], [], []
for a in range(1978, 2026):
    # --- additivité des soldes
    b9_sum1 = sum(v(s, "b9", a) for s in N1)
    b9_sum2 = v("S13111", "b9", a) + v("S13112", "b9", a)
    # --- écart dépenses / recettes non consolidées
    gap_dep = sum(v(s, "dep", a) for s in N1) - v("S13", "dep", a)
    gap_rec = sum(v(s, "rec", a) for s in N1) - v("S13", "rec", a)
    d73p = sum(v(s, "d73p", a) for s in N1) - v("S13", "d73p", a)
    d73r = sum(v(s, "d73r", a) for s in N1) - v("S13", "d73r", a)
    d9_inter_p = sum(v(s, "d9p", a) for s in N1) - v("S13", "d9p", a)
    d9_inter_r = sum(v(s, "d9r", a) for s in N1) - v("S13", "d9r", a)
    d41_inter_p = sum(v(s, "d41p", a) for s in N1) - v("S13", "d41p", a)
    d41_inter_r = sum(v(s, "d41r", a) for s in N1) - v("S13", "d41r", a)
    d733 = sum(v(s, "d733r", a) for s in N1) - v("S13", "d733r", a)
    resid_dep = gap_dep - d73p - d9_inter_p - d41_inter_p
    resid_rec = gap_rec - d73r - d9_inter_r - d41_inter_r - d733
    # niveau 2 : État + ODAC vs APUC
    gap_dep2 = v("S13111", "dep", a) + v("S13112", "dep", a) - v("S1311", "dep", a)
    gap_rec2 = v("S13111", "rec", a) + v("S13112", "rec", a) - v("S1311", "rec", a)
    rec_rows.append([a, round(v("S13", "b9", a), 3), round(b9_sum1, 3), round(b9_sum1 - v("S13", "b9", a), 4),
                     round(v("S1311", "b9", a), 3), round(b9_sum2, 3), round(b9_sum2 - v("S1311", "b9", a), 4),
                     round(v("S13", "dep", a), 3), round(gap_dep, 3), round(d73p, 3), round(d9_inter_p, 3), round(d41_inter_p, 3), round(resid_dep, 3),
                     round(v("S13", "rec", a), 3), round(gap_rec, 3), round(d73r, 3), round(d9_inter_r, 3), round(d41_inter_r, 3), round(d733, 3), round(resid_rec, 3),
                     round(gap_dep2, 3), round(gap_rec2, 3)])
    # --- flux par sous-secteur
    for s in ["S13111", "S13112", "S1311", "S1313", "S1314"]:
        flux_rows.append([a, s, round(v(s, "d73p", a), 3), round(v(s, "d73r", a), 3), round(v(s, "d73r", a) - v(s, "d73p", a), 3),
                          round(v(s, "d733r", a), 3), round(v(s, "d9p", a), 3), round(v(s, "d9r", a), 3),
                          round(v(s, "d41p", a), 3), round(v(s, "d41r", a), 3)])
    # --- conventions d'attribution (niveau 1)
    b9 = {s: v(s, "b9", a) for s in N1}
    netd73 = {s: v(s, "d73r", a) - v(s, "d73p", a) for s in N1}
    d733s = {s: v(s, "d733r", a) for s in N1}
    # C1 : tel que publié
    c1 = dict(b9)
    # C2 : neutralisation des transferts courants entre APU (D73 hors D733) : solde - D73 nets reçus.
    #      La somme des D73 nets étant nulle (à l'écart de consolidation près), le total reste B9(S13).
    c2 = {s: b9[s] - netd73[s] for s in N1}
    # C3 : C2 + neutralisation des transferts de recettes fiscales D733 (enregistrés en impôts négatifs chez le payeur)
    c3 = {s: c2[s] - d733s[s] for s in N1}
    # C4 : C3 + D9 inter-APU attribués en totalité à APUC -> APUL (borne : hypothèse que tout transfert en capital
    #      inter-APU va de l'administration centrale aux APUL ; non vérifiable dans les tableaux)
    c4 = dict(c3)
    c4["S1313"] -= d9_inter_r
    c4["S1311"] += d9_inter_r
    # C5 : C3 + impôts affectés aux ASSO (CSG, TVA et autres impôts, t_3216 l.13) reclassés comme ressources de l'APUC :
    #      convention « régimes financés par leurs seules cotisations et ressources propres ». Convention extrême, illustrative.
    imp = IMPOTS_ASSO.get(a)
    c5 = dict(c3)
    if imp is not None:
        c5["S1314"] -= imp
        c5["S1311"] += imp
    for nom, c in [("C1_publie", c1), ("C2_sans_D73", c2), ("C3_sans_D73_D733", c3), ("C4_C3_plus_D9_inter_vers_APUL", c4), ("C5_C3_impots_ASSO_rattaches_APUC", c5)]:
        tot = sum(c.values())
        avert = ""
        if nom == "C2_sans_D73" and a < 2010:
            avert = "NON INTERPRETABLE avant 2010 : D733 fige 1978-2009 dans t_3203/t_3205 (F-A01-010) ; utiliser C3"
        if nom == "C4_C3_plus_D9_inter_vers_APUL":
            avert = "borne : hypothese non verifiable (tout D9 inter-APU vers les APUL)"
        if nom == "C5_C3_impots_ASSO_rattaches_APUC":
            avert = "convention extreme, illustrative"
        conv_rows.append([a, nom] + [round(c[s], 3) for s in N1] + [round(tot, 3), round(tot - v("S13", "b9", a), 4),
                         "" if imp is None or nom != "C5_C3_impots_ASSO_rattaches_APUC" else round(imp, 3), avert])

def ecrire(nom, entete, lignes):
    with open(os.path.join(A01, nom), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";"); w.writerow(entete); w.writerows(lignes)

ecrire("A01_reconciliation_sous_secteurs.csv",
       ["annee", "b9_S13", "somme_b9_APUC_APUL_ASSO", "ecart_additivite_n1", "b9_APUC", "somme_b9_Etat_ODAC", "ecart_additivite_n2",
        "dep_S13_consolidee", "ecart_dep_non_consolidee_n1", "dont_D73_verses", "dont_D9_inter_APU_verses", "dont_D41_inter_APU_verses", "residu_dep",
        "rec_S13_consolidee", "ecart_rec_non_consolidee_n1", "dont_D73_recus", "dont_D9_inter_APU_recus", "dont_D41_inter_APU_recus", "dont_D733", "residu_rec",
        "ecart_dep_Etat_plus_ODAC_moins_APUC", "ecart_rec_Etat_plus_ODAC_moins_APUC"], rec_rows)
ecrire("A01_flux_d73_par_sous_secteur.csv",
       ["annee", "secteur", "D73_verses", "D73_recus", "D73_net_recu", "D733_recu", "D9_verses", "D9_recus", "D41_verses", "D41_recus"], flux_rows)
ecrire("A01_attribution_conventions.csv",
       ["annee", "convention", "APUC_S1311", "APUL_S1313", "ASSO_S1314", "total", "ecart_au_B9_S13", "impots_ASSO_reclasses", "avertissement"], conv_rows)
mx = max(abs(r[3]) for r in rec_rows), max(abs(r[6]) for r in rec_rows), max(abs(r[12]) for r in rec_rows), max(abs(r[19]) for r in rec_rows)
print("max écart additivité n1, n2, résidu dép, résidu rec :", mx)
print("max écart conventions au B9 :", max(abs(r[6]) for r in conv_rows))
