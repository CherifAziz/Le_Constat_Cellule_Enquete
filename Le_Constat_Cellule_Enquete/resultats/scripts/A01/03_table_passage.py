"""A01 - Table de passage 1974-2025 : S13 et sous-secteurs (État, ODAC, APUC, APUL, ASSO).
Entrées (lecture seule, resultats/donnees/commun) :
  - A01_t32xx_long.csv (produit par 02_extraire_t32xx.py à partir de insee_cn_t_3201..3214.xlsx)
  - insee_cn_t_3215.xlsx (dépenses/recettes par sous-secteur, Md€ et % PIB -> PIB implicite)
  - insee_cn_t_3216.xlsx (prélèvements obligatoires Md€ et % PIB -> PIB implicite 1959-2025)
  - base_insee_solde_sous_secteurs.csv, base_insee_dette_sous_secteurs.csv, base_insee_dep_rec_pctPIB.csv
Sorties (resultats/donnees/A01) :
  - A01_table_passage_1974_2025.csv  (une ligne par année x secteur ; cellules vides = indisponible, colonne 'indisponible')
  - A01_controles_passage.csv         (contrôles : R-D=B9, cohérence avec fichiers 'solde' et 'série longue', PIB)
Conventions : solde = capacité(+)/besoin(-) de financement B9 ; solde primaire = B9 + intérêts versés D41 (bruts,
  y compris intérêts versés à d'autres APU dans les tableaux de sous-secteurs) ; solde primaire 'net' = B9 + D41 versés - D41 reçus.
Relançable : python -I 03_table_passage.py
"""
import os, csv, openpyxl
from collections import defaultdict

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
A01 = os.path.join(RACINE, "resultats", "donnees", "A01")

# ---------- t_32xx long ----------
T = defaultdict(dict)  # (secteur, section, poste_court) -> {annee: valeur}
POSTES = {
    ("DEPENSES", "Total des dépenses"): "dep",
    ("RECETTES", "Total des recettes"): "rec",
    ("SOLDES", "Capacité (+) ou besoin (-) de financement (B9NF)"): "b9",
    ("DEPENSES", "Intérêts (D41)"): "d41p",
    ("RECETTES", "Intérêts (D41)"): "d41r",
    ("DEPENSES", "Dépenses hors éléments imputés (a, b et c) (***)"): "dep_hei",
    ("RECETTES", "Recettes hors éléments imputés (a,b et c') (***)"): "rec_hei",
    ("DEPENSES", "Transferts courants entre administrations publiques (D73)"): "d73p",
    ("RECETTES", "Transferts courants entre administrations publiques  (D73 hors D733)"): "d73r",
    ("RECETTES", "Transferts courants entre administrations publiques (D73 hors D733)"): "d73r",
    ("RECETTES", "Transferts de recettes fiscales  (D733)"): "d733r",
    ("RECETTES", "Transferts de recettes fiscales (D733)"): "d733r",
    ("DEPENSES", "Transferts en capital à payer (D9p hors D995p)"): "d9p",
    ("RECETTES", "Transferts en capital  (D9r hors D91r, D995r)"): "d9r",
    ("RECETTES", "Transferts en capital (D9r hors D91r, D995r)"): "d9r",
}
with open(os.path.join(A01, "A01_t32xx_long.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter=";"):
        k = (r["section"], r["poste"].strip())
        if k in POSTES:
            try:
                T[(r["secteur"], POSTES[k])][int(r["annee"])] = float(r["valeur_mdeur"])
            except ValueError:
                pass

import sys
for _s in ["S13", "S1311", "S13111", "S13112", "S1313", "S1314"]:
    for _c in set(POSTES.values()):
        if not T[(_s, _c)]:
            sys.exit(f"ERREUR : aucune valeur pour {_s}/{_c} (libellé non reconnu)")

# ---------- PIB implicite ----------
def pib_implicite(fichier, lig_md, lig_pct):
    ws = openpyxl.load_workbook(os.path.join(COMMUN, fichier), read_only=True, data_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[2]
    out = {}
    for j, an in enumerate(hdr):
        if isinstance(an, (int, float)) and 1900 < an < 2100:
            a, b = rows[lig_md - 1][j], rows[lig_pct - 1][j]
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b:
                out[int(an)] = a / b * 100
    return out
PIB_3216 = pib_implicite("insee_cn_t_3216.xlsx", 5, 18)    # PO total Md€ / PO % PIB
PIB_3215 = pib_implicite("insee_cn_t_3215.xlsx", 20, 39)   # dépenses APU Md€ / % PIB

# ---------- fichiers 'séries longues' ----------
def lire_base(fichier):
    d = defaultdict(dict)
    with open(os.path.join(COMMUN, fichier), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            try:
                d[(r["feuille"], r["serie"])][int(r["annee"])] = float(r["valeur"])
            except ValueError:
                pass
    return d
SOLDE = lire_base("base_insee_solde_sous_secteurs.csv")
DETTE = lire_base("base_insee_dette_sous_secteurs.csv")
LONG = lire_base("base_insee_dep_rec_pctPIB.csv")

NOMS = {"S13": "Ensemble", "S1311": "Administration publique centrale", "S13111": "État",
        "S13112": "Organismes divers d'administration centrale", "S1313": "Administrations publiques locales",
        "S1314": "Administrations de sécurité sociale"}

def g(sec, k, an):
    return T[(sec, k)].get(an)

lignes, controles = [], []
for an in range(1974, 2026):
    pib = PIB_3216.get(an)
    for sec, nom in NOMS.items():
        dep, rec, b9 = g(sec, "dep", an), g(sec, "rec", an), g(sec, "b9", an)
        d41p, d41r = g(sec, "d41p", an), g(sec, "d41r", an)
        b9_fichier_solde = SOLDE[("Figure 1", nom)].get(an)
        dette = DETTE[("Figure 1", nom)].get(an)
        dette_pct = DETTE[("Figure 2", nom)].get(an)
        b9_retenu = b9 if b9 is not None else b9_fichier_solde
        # Garde-fou K-013 : avant 1978, les soldes État et ODAC du fichier Insee ne s'additionnent pas à l'APUC
        # (écart jusqu'à -6,5 Md€) : valeurs NON reprises dans la table de passage.
        exclu_k013 = sec in ("S13111", "S13112") and b9 is None
        if exclu_k013:
            b9_retenu = None
        prim = (b9 + d41p) if (b9 is not None and d41p is not None) else None
        prim_net = (b9 + d41p - d41r) if (prim is not None and d41r is not None) else None
        indispo = [n for n, v in [("depenses", dep), ("recettes", rec), ("interets", d41p), ("dette", dette)] if v is None]
        if exclu_k013:
            indispo.append("solde (Etat/ODAC non additifs avant 1978, K-013)")
        pc = lambda x: round(x / pib * 100, 3) if (x is not None and pib) else ""
        lignes.append({
            "annee": an, "secteur": sec, "libelle": nom,
            "depenses_mdeur": dep, "recettes_mdeur": rec,
            "solde_b9_mdeur": b9_retenu,
            "source_solde": "t_32xx" if b9 is not None else ("" if exclu_k013 else ("insee_solde_par_sous_secteur (Fig.1)" if b9_fichier_solde is not None else "")),
            "interets_verses_d41_mdeur": d41p, "interets_recus_d41_mdeur": d41r,
            "solde_primaire_mdeur": prim, "solde_primaire_net_interets_recus_mdeur": prim_net,
            "dette_maastricht_mdeur": dette, "pib_mdeur": round(pib, 3) if pib else "",
            "depenses_pct_pib": pc(dep), "recettes_pct_pib": pc(rec), "solde_pct_pib": pc(b9_retenu),
            "interets_pct_pib": pc(d41p), "solde_primaire_pct_pib": pc(prim),
            "dette_pct_pib_insee": dette_pct,
            "indisponible": ",".join(indispo),
        })
        # contrôles
        if dep is not None and rec is not None and b9 is not None:
            controles.append([an, sec, "recettes-depenses-B9 (Md€)", round(rec - dep - b9, 4)])
        if b9 is not None and b9_fichier_solde is not None:
            controles.append([an, sec, "B9 t_32xx - B9 fichier solde (Md€)", round(b9 - b9_fichier_solde, 4)])
    if an in PIB_3215 and pib:
        controles.append([an, "PIB", "PIB(3215)-PIB(3216) Md€", round(PIB_3215[an] - pib, 3)])
    # série longue % PIB vs t_3201
    for nomL, k in [("Dépenses", "dep"), ("Recettes", "rec")]:
        v = LONG[("Données", nomL)].get(an)
        x = g("S13", k, an)
        if v is not None and x is not None and pib:
            controles.append([an, "S13", f"{nomL} % PIB série longue - t_3201/PIB", round(v - x / pib * 100, 3)])

cols = list(lignes[0].keys())
with open(os.path.join(A01, "A01_table_passage_1974_2025.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
    w.writeheader()
    for l in lignes:
        w.writerow({k: ("" if v is None else (round(v, 4) if isinstance(v, float) else v)) for k, v in l.items()})
with open(os.path.join(A01, "A01_controles_passage.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "secteur", "controle", "ecart"])
    w.writerows(controles)
# résumé console
import statistics
for c in sorted(set(x[2] for x in controles)):
    e = [abs(x[3]) for x in controles if x[2] == c]
    print(f"{c}: n={len(e)} max|ecart|={max(e):.4f}")
print("PIB 1974..1977 (3216):", {a: round(PIB_3216[a], 2) for a in range(1974, 1978)})
print("PIB 2025 3216/3215:", round(PIB_3216[2025], 3), round(PIB_3215[2025], 3))
