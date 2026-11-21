# -*- coding: utf-8 -*-
"""C02 - Refaire, par un script propre, les quatre resultats propres a l'equipe Codex.

Entrees (lecture seule) :
  - base commune de la cellule : resultats/donnees/commun/insee_cn_t_3201.xlsx, insee_cn_t_3215.xlsx,
    base_insee_dette_sous_secteurs.csv
  - pieces retelechargees par C02 le 21/11/2026 (resultats/donnees/C02/sources/) :
    T_1112_fr.xlsx (CCF par secteur), t_3105_fr.xlsx, t_3106_fr.xlsx, t_3107_fr.xlsx, t_3108_fr.xlsx, ip2135.xlsx
Aucun fichier de l'equipe Codex n'est lu ni execute par ce script.
Sorties : resultats/donnees/C02/C02_verif_*.csv et impression des resultats.
Lancer : python -I C02_verifications.py
"""
import csv, os, sys, warnings
import openpyxl

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
COMMUN = os.path.join(RACINE, "donnees", "commun")
SRC = os.path.join(RACINE, "donnees", "C02", "sources")
OUT = os.path.join(RACINE, "donnees", "C02")


def lire_ligne_annees(path, sheet_idx, hdr_row, data_rows, label_col=1, sheet_name=None):
    """Retourne {numero_ligne: {annee: valeur}} pour une feuille Insee 'lignes x annees'."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet_name] if sheet_name else wb.worksheets[sheet_idx]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[hdr_row - 1]
    cols = {}
    for k, x in enumerate(hdr):
        try:
            a = int(float(str(x)))
            if 1900 < a < 2100:
                cols[k] = a
        except Exception:
            pass
    res = {}
    for n in data_rows:
        r = rows[n - 1]
        d = {}
        for k, a in cols.items():
            v = r[k] if k < len(r) else None
            try:
                d[a] = float(v)
            except Exception:
                d[a] = None
        res[n] = {"label": str(r[label_col]).strip(), "v": d}
    return res


def ecrire(nom, entete, lignes):
    p = os.path.join(OUT, nom)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(entete)
        w.writerows(lignes)
    print("  ecrit :", p)


# ---------------------------------------------------------------------------
# (a) Deficit et investissement net, 1975-2025
# ---------------------------------------------------------------------------
print("=== (a) Deficit contre investissement net, S13, 1975-2025 ===")
t3201 = lire_ligne_annees(os.path.join(COMMUN, "insee_cn_t_3201.xlsx"), 0, 3, [21, 23, 24, 56, 65, 66])
for n, d in t3201.items():
    print("  t_3201 ligne", n, ":", d["label"][:70])
ccf = lire_ligne_annees(os.path.join(SRC, "T_1112_fr.xlsx"), 0, 4, [8], label_col=1, sheet_name="T_1112")
print("  T_1112 ligne 8 :", ccf[8]["label"])

D9P, ANF, P51G, D9R, B8G, B9 = (t3201[n]["v"] for n in (21, 23, 24, 56, 65, 66))
P51C = ccf[8]["v"]
annees = list(range(1975, 2026))
lignes = []
cpt = {"deficit": 0, "def>inv_net": 0, "def>inv_brut": 0, "B8g>0": 0, "B8n>0": 0,
       "def>ANF_net": 0, "def>ANF+D9p_net": 0, "def>ANF+D9p-D9r_net": 0}
liste_def_le_invnet = []
for a in annees:
    deficit = -B9[a]
    inv_net = P51G[a] - P51C[a]
    anf_net = ANF[a] - P51C[a]
    large_net = ANF[a] + D9P[a] - P51C[a]
    large_net2 = ANF[a] + D9P[a] - D9R[a] - P51C[a]
    b8n = B8G[a] - P51C[a]
    cpt["deficit"] += deficit > 0
    cpt["def>inv_net"] += deficit > inv_net
    cpt["def>inv_brut"] += deficit > P51G[a]
    cpt["B8g>0"] += B8G[a] > 0
    cpt["B8n>0"] += b8n > 0
    cpt["def>ANF_net"] += deficit > anf_net
    cpt["def>ANF+D9p_net"] += deficit > large_net
    cpt["def>ANF+D9p-D9r_net"] += deficit > large_net2
    if not deficit > inv_net:
        liste_def_le_invnet.append(a)
    lignes.append([a, round(-B9[a], 4), round(P51G[a], 4), round(P51C[a], 4), round(inv_net, 4),
                   round(anf_net, 4), round(large_net, 4), round(large_net2, 4), round(B8G[a], 4), round(b8n, 4),
                   int(deficit > inv_net), int(deficit > P51G[a])])
print("  annees :", len(annees))
for k, v in cpt.items():
    print("  ", k, ":", v)
print("  annees ou le deficit NE depasse PAS l'investissement net :", liste_def_le_invnet)
print("  annees ou le deficit depasse l'investissement brut :",
      [a for a in annees if -B9[a] > P51G[a]])
print("  2025 : deficit %.3f ; P51g %.3f ; P51c %.3f ; inv. net %.3f ; B8g %.3f ; B8n %.3f"
      % (-B9[2025], P51G[2025], P51C[2025], P51G[2025] - P51C[2025], B8G[2025], B8G[2025] - P51C[2025]))
print("  annees B8n > 0 :", [a for a in annees if B8G[a] - P51C[a] > 0])
ecrire("C02_verif_a_investissement_net.csv",
       ["annee", "deficit_Md", "P51g", "P51c_CCF", "inv_net_P51g-P51c", "variante_ANF-P51c",
        "variante_ANF+D9p-P51c", "variante_ANF+D9p-D9r-P51c", "B8g", "B8n=B8g-P51c",
        "deficit>inv_net", "deficit>inv_brut"], lignes)

# ---------------------------------------------------------------------------
# (b) Reconciliation des comptes sociaux 2025 (3.108), consolidation (3.215), passage Etat (3.107)
# ---------------------------------------------------------------------------
print("\n=== (b) Comptes sociaux 2025 ===")
t3108 = lire_ligne_annees(os.path.join(SRC, "t_3108_fr.xlsx"), 0, 3, [5, 7, 20, 22, 23, 24, 25, 26, 28])
lb = []
for n, d in t3108.items():
    print("  3.108 l.%d %-75s 2024=%s 2025=%s" % (n, d["label"][:75], d["v"].get(2024), d["v"].get(2025)))
    lb.append(["3.108", n, d["label"], d["v"].get(2024), d["v"].get(2025)])
v = {n: t3108[n]["v"][2025] for n in t3108}
print("  controle : RG %.1f + corrections %.1f = %.1f (publie %.1f)" % (v[5], v[7], v[5] + v[7], v[20]))
print("  controle : RG Maastricht %.1f + autres %.1f = %.1f (publie ASSO %.1f)" % (v[20], v[22], v[20] + v[22], v[28]))
print("  controle : CADES+FRR+autres+ODASS = %.1f (publie %.1f)" % (v[23] + v[24] + v[25] + v[26], v[22]))

t3106 = lire_ligne_annees(os.path.join(SRC, "t_3106_fr.xlsx"), 0, 3, [5, 6, 7, 8, 9, 10, 29])
print("  3.106 ASSO 2025 :", t3106[10]["v"][2025], "; S13 :", t3106[5]["v"][2025],
      "; Etat :", t3106[7]["v"][2025], "; ODAC :", t3106[8]["v"][2025], "; APUL :", t3106[9]["v"][2025])

# 3.215 : consolidation
wb = openpyxl.load_workbook(os.path.join(COMMUN, "insee_cn_t_3215.xlsx"), read_only=True, data_only=True)
ws = wb.worksheets[0]
rows215 = list(ws.iter_rows(values_only=True))
print("  3.215, lignes contenant 'total' ou 'consolid' (2025 = derniere valeur numerique) :")
for i, r in enumerate(rows215):
    s = " ".join(str(x) for x in r[:3] if x is not None)
    if any(k in s.lower() for k in ("total des d", "total des r", "consolid", "dépenses", "recettes")):
        nums = [x for x in r if isinstance(x, (int, float))]
        print("    l.%d %s -> %s" % (i + 1, s[:90], nums[-1] if nums else None))
        lb.append(["3.215", i + 1, s[:120], None, nums[-1] if nums else None])

dep_ss = [r for r in rows215[6:17] if r[1] and "Dépenses" in str(r[1])]
nums_dep = [[x for x in r if isinstance(x, (int, float))][-1] for r in dep_ss]
print("  controle 3.215 : somme des depenses des 4 sous-secteurs (l.7,10,13,16) = %.3f ; APU consolide (l.20) = %.3f ; ecart de consolidation = %.3f"
      % (sum(nums_dep), [x for x in rows215[19] if isinstance(x, (int, float))][-1],
         sum(nums_dep) - [x for x in rows215[19] if isinstance(x, (int, float))][-1]))
rec_ss = [r for r in rows215[6:17] if r[1] and "Recettes" in str(r[1])]
nums_rec = [[x for x in r if isinstance(x, (int, float))][-1] for r in rec_ss]
print("  controle 3.215 : idem recettes = %.3f - %.3f = %.3f"
      % (sum(nums_rec), [x for x in rows215[20] if isinstance(x, (int, float))][-1],
         sum(nums_rec) - [x for x in rows215[20] if isinstance(x, (int, float))][-1]))
t3107 = lire_ligne_annees(os.path.join(SRC, "t_3107_fr.xlsx"), 0, 4, [5, 9, 14, 42, 66])
for n, d in t3107.items():
    print("  3.107 l.%d %-70s 2025=%s" % (n, d["label"][:70], d["v"].get(2025)))
    lb.append(["3.107", n, d["label"], d["v"].get(2024), d["v"].get(2025)])
s = sum(t3107[n]["v"][2025] for n in (5, 9, 14, 42))
print("  controle 3.107 : RE + (1) + (2) + (3) = %.1f (publie %.1f)" % (s, t3107[66]["v"][2025]))
ecrire("C02_verif_b_comptes_sociaux_2025.csv", ["tableau", "ligne", "libelle", "2024", "2025"], lb)

# ---------------------------------------------------------------------------
# (c) Patrimoine net des APU fin 2025 (Insee Premiere 2135)
# ---------------------------------------------------------------------------
print("\n=== (c) Patrimoine net des APU fin 2025 ===")
wb = openpyxl.load_workbook(os.path.join(SRC, "ip2135.xlsx"), read_only=True, data_only=True)
lc = []
for nom in ("Figure 1", "Figure 4", "Figure 5"):
    ws = wb[nom]
    rows = list(ws.iter_rows(values_only=True))
    for i, r in enumerate(rows):
        vals = [x for x in r if x is not None]
        if not vals:
            continue
        s0 = str(vals[0])
        if nom == "Figure 1" or "Administrations publiques" in s0 or "Patrimoine" in s0 or i < 6:
            print("  %s l.%d : %s" % (nom, i + 1, " | ".join(str(x)[:30] for x in vals)[:230]))
            lc.append([nom, i + 1] + [str(x) for x in vals][:12])
ws = wb["Figure 5"]
for r in ws.iter_rows(values_only=True):
    if r and r[0] and "Administrations publiques" in str(r[0]):
        net, nf, fin = r[1], r[3], r[5]
        print("  controle : non financier %s + financier net %s = %s (publie net %s)" % (nf, fin, nf + fin, net))
        print("  niveau 2024 implicite (811 / 1,081) : %.0f Md EUR" % (net / 1.081))
ecrire("C02_verif_c_patrimoine_APU.csv", ["figure", "ligne", "valeurs..."], lc)

# ---------------------------------------------------------------------------
# (d) Passage deficit-dette 2009 (3.105) et ajustements stock-flux en points de PIB
# ---------------------------------------------------------------------------
print("\n=== (d) Passage deficit-dette ===")
t3105 = lire_ligne_annees(os.path.join(SRC, "t_3105_fr.xlsx"), 0, 3, [5, 7, 8, 9, 10, 11, 12, 13, 15, 19, 24, 26, 28])
ld = []
for n, d in t3105.items():
    print("  3.105 l.%d %-70s 2008=%s 2009=%s 2010=%s" % (n, d["label"][:70], d["v"].get(2008), d["v"].get(2009), d["v"].get(2010)))
    ld.append(["3.105", n, d["label"], d["v"].get(2008), d["v"].get(2009), d["v"].get(2010)])
v9 = {n: t3105[n]["v"][2009] for n in t3105}
print("  controle 2009 : D + (1) + (2) + (3) + (4) + (5) = %.1f (publie %.1f)"
      % (v9[5] + v9[7] + v9[15] + v9[19] + v9[24] + v9[26], v9[28]))
print("  part des credits (F4) dans les acquisitions nettes 2009 : %.1f %%" % (100 * v9[10] / v9[7]))

# Dette (base commune, fichier 2830192), solde (t_3201), PIB (t_3106 ligne 29)
dette = {}
with open(os.path.join(COMMUN, "base_insee_dette_sous_secteurs.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f, delimiter=";"):
        if r["serie"] == "Ensemble" and "milliards" in r["unite"]:
            dette[int(r["annee"])] = float(r["valeur"])
PIB = t3106[29]["v"]
B9s = t3201[66]["v"]
I = lire_ligne_annees(os.path.join(COMMUN, "insee_cn_t_3201.xlsx"), 0, 3, [12])[12]["v"]
dec = []
for a in range(1979, 2026):
    A = dette[a] - dette[a - 1] + B9s[a]
    prim = -(B9s[a] + I[a]) / PIB[a] * 100       # contribution du deficit primaire
    inte = I[a] / PIB[a] * 100
    pibe = dette[a - 1] * (1 / PIB[a] - 1 / PIB[a - 1]) * 100
    sfa = A / PIB[a] * 100
    dd = (dette[a] / PIB[a] - dette[a - 1] / PIB[a - 1]) * 100
    dec.append([a, round(A, 3), round(prim, 3), round(inte, 3), round(pibe, 3), round(sfa, 3), round(dd, 3),
                round(prim + inte + pibe + sfa - dd, 6)])
ecrire("C02_verif_d_decomposition_dette.csv",
       ["annee", "SFA_Md", "deficit_primaire_pts", "interets_pts", "PIB_nominal_pts", "SFA_pts", "var_ratio_pts", "ecart_identite"], dec)
D = {r[0]: r for r in dec}


def somme(a0, a1, col):
    return sum(D[a][col] for a in range(a0, a1 + 1))


print("  fin 2007 - fin 2009 : primaire %.2f ; interets %.2f ; PIB %.2f ; SFA %.2f ; variation %.2f"
      % tuple(somme(2008, 2009, c) for c in (2, 3, 4, 5, 6)))
print("  SFA 2009 seul : %.1f Md EUR = %.2f pts ; 2008 : %.1f Md = %.2f pts ; 2010 : %.1f Md = %.2f pts"
      % (D[2009][1], D[2009][5], D[2008][1], D[2008][5], D[2010][1], D[2010][5]))
print("  SFA cumules (pts de PIB, somme des contributions annuelles) : 1979-1998 %.2f ; 1999-2025 %.2f ; 2008-2010 %.2f ; 1979-2025 %.2f"
      % (somme(1979, 1998, 5), somme(1999, 2025, 5), somme(2008, 2010, 5), somme(1979, 2025, 5)))
print("  dette 2008 %.1f, 2009 %.1f : hausse %.1f Md (3.105 : %.1f)" % (dette[2008], dette[2009], dette[2009] - dette[2008], v9[28]))
ecrire("C02_verif_d_passage_2009.csv", ["tableau", "ligne", "libelle", "2008", "2009", "2010"], ld)
