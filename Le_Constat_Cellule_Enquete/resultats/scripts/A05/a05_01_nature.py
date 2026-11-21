# -*- coding: utf-8 -*-
"""A05 travail 1 - Dépense des APU (S13, consolidée) par nature, 1959-2025, base 2020.
Sources : insee_cn_t_3201.xlsx (base commune, extrait 20/11/2026) ;
          PIB courant, volume, prix : insee T_1101_1103_fr.xlsx (A05/sources, téléchargé 20/11/2026,
          fichier créé par l'Insee le 2026-05-21).
Sorties (A05/) :
  A05_nature_pctPIB.csv              niveaux en % du PIB par nature et par année
  A05_nature_contrib_periodes.csv    variation du ratio par nature sur des périodes
  A05_nature_volume_periodes.csv     croissance réelle annuelle moyenne (déflateur du PIB) par nature
  A05_denominateur_1974_1993.csv     décomposition de la hausse du ratio : dépense réelle vs PIB réel
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *
import openpyxl

ans, t = lire_insee_32xx("3201")

# --- PIB Insee (T_1101 niveau, T_1102 volume chaîné, T_1103 prix) ---
wb = openpyxl.load_workbook(os.path.join(SRC, "insee_T_1101_1103_fr.xlsx"), read_only=True, data_only=True)
def serie(onglet, code="B1GQ"):
    rows = list(wb[onglet].iter_rows(values_only=True))
    hdr = rows[3]
    for r in rows:
        if r[0] == code:
            return {int(h): float(v) for h, v in zip(hdr, r) if h and isinstance(v, (int, float))}
pib = serie("T_1101 en niveau")
pibv = serie("T_1102 en niveau")
defl = serie("T_1103 en niveau")
conso_menages_prix = serie("T_1103 en niveau", "S14B")

NATURES = [
    ("Remunerations_D1", ["Rémunération des salariés (D1)"]),
    ("Conso_intermediaires_P2", ["Consommation intermédiaire (P2)"]),
    ("Prestations_especes_D62", ["Prestations sociales autres que transferts sociaux en nature (D62)"]),
    ("Prestations_nature_marchandes_D632", ["Transferts sociaux en nature de produits marchands (D632)"]),
    ("Interets_D41", ["Intérêts (D41)"]),
    ("Subventions_D3", ["Subventions (D3)"]),
    ("Autres_transferts_courants_D7", ["Autres transferts courants (D7 hors D73)"]),
    ("Transferts_capital_D9", ["Transferts en capital à payer (D9p hors D995p)"]),
    ("FBCF_P51g", ["Formation brute de capital fixe (P51g)"]),
    ("Autres_D29_D4_D5_P52_NP", ["Autres impôts sur la production (D29)",
                                 "Revenus de la propriété autres que les intérêts (D4 hors D41)",
                                 "Impôts courants sur le revenu et le patrimoine (D5)",
                                 "Autres acquisitions moins cessions d'actifs non financiers (P52, P53, NP)"]),
]
TOTAL = "Total des dépenses"
IMPUT = [" dont (a) - Cotisations sociales imputées (D122)", "dont (a) - Cotisations sociales imputées (D122)"]

def get(lab, y):
    return t[lab].get(y)

annees = [y for y in ans if y in pib]
lignes = []
niv = {}
for y in annees:
    row = [y, pib[y]]
    s = 0.0
    for nom, labs in NATURES:
        v = sum(get(l, y) or 0.0 for l in labs)
        s += v
        niv[(nom, y)] = v
        row.append(100 * v / pib[y])
    tot = get(TOTAL, y)
    niv[("Total", y)] = tot
    row += [100 * tot / pib[y], 100 * (tot - s) / pib[y]]
    # éléments imputés
    ci = [k for k in t if "Crédits d'impôts enregistrés en dépenses" in k]
    cs = [k for k in t if "Cotisations sociales imputées (D122)" in k]
    cp = [k for k in t if "Capitalisation de la production pour emploi final propre" in k]
    row += [100 * (t[cs[0]].get(y, 0)) / pib[y], 100 * (t[cp[0]].get(y, 0)) / pib[y], 100 * (t[ci[0]].get(y, 0)) / pib[y]]
    lignes.append(row)
ecrire_csv("A05_nature_pctPIB.csv",
           ["annee", "PIB_Mdeur_courants"] + [n for n, _ in NATURES] +
           ["Total_depenses", "ecart_controle_somme", "dont_cotis_imputees_D122", "dont_prod_compte_propre_P51g", "dont_credits_impot_en_depense"],
           lignes)

# --- contributions par période ---
PER = [(1960, 1974), (1974, 1985), (1985, 1993), (1974, 1993), (1993, 2000), (2000, 2007), (2007, 2009),
       (2009, 2019), (2007, 2019), (2019, 2020), (2019, 2025), (1993, 2025), (1974, 2025)]
cl = []
for a, b in PER:
    tot_a = 100 * niv[("Total", a)] / pib[a]; tot_b = 100 * niv[("Total", b)] / pib[b]
    for nom, _ in NATURES + [("Total", None)]:
        ra = 100 * niv[(nom, a)] / pib[a]; rb = 100 * niv[(nom, b)] / pib[b]
        part = (rb - ra) / (tot_b - tot_a) * 100 if nom != "Total" and abs(tot_b - tot_a) > 1e-9 else ""
        cl.append(["%d-%d" % (a, b), nom, ra, rb, rb - ra, part])
ecrire_csv("A05_nature_contrib_periodes.csv",
           ["periode", "nature", "ratio_debut_pctPIB", "ratio_fin_pctPIB", "variation_points", "part_de_la_variation_totale_pct"], cl)

# --- volumes : déflaté par le prix du PIB ---
vl = []
for a, b in PER:
    n = b - a
    gy = (pibv[b] / pibv[a]) ** (1 / n) - 1
    for nom, _ in NATURES + [("Total", None)]:
        ra = niv[(nom, a)] / defl[a]; rb = niv[(nom, b)] / defl[b]
        g = (rb / ra) ** (1 / n) - 1 if ra > 0 and rb > 0 else float("nan")
        # même chose déflatée par les prix de consommation des ménages
        rc_a = niv[(nom, a)] / conso_menages_prix[a]; rc_b = niv[(nom, b)] / conso_menages_prix[b]
        gc = (rc_b / rc_a) ** (1 / n) - 1 if rc_a > 0 and rc_b > 0 else float("nan")
        vl.append(["%d-%d" % (a, b), nom, 100 * g, 100 * gc, 100 * gy])
ecrire_csv("A05_nature_volume_periodes.csv",
           ["periode", "nature", "croissance_reelle_annuelle_moy_deflateur_PIB_pct",
            "croissance_reelle_annuelle_moy_deflateur_conso_menages_pct", "croissance_PIB_volume_annuelle_moy_pct"], vl)

# --- dénominateur : 1974-1993 contre 1960-1974 ---
def taux(x, a, b):
    return (x[b] / x[a]) ** (1 / (b - a)) - 1
Ereal = {y: niv[("Total", y)] / defl[y] for y in annees}
den = []
for (a, b) in [(1960, 1974), (1974, 1985), (1974, 1993), (1985, 1993), (1993, 2025), (1993, 2007), (2007, 2019), (2019, 2025)]:
    gE = taux(Ereal, a, b); gY = taux(pibv, a, b)
    r0 = 100 * niv[("Total", a)] / pib[a]; r1 = 100 * niv[("Total", b)] / pib[b]
    den.append(["%d-%d" % (a, b), r0, r1, 100 * gE, 100 * gY, 100 * (gE - gY)])
# contrefactuels mécaniques
gE_6074 = taux(Ereal, 1960, 1974); gY_6074 = taux(pibv, 1960, 1974)
gE_7493 = taux(Ereal, 1974, 1993); gY_7493 = taux(pibv, 1974, 1993)
r74 = 100 * niv[("Total", 1974)] / pib[1974]
# Le déflateur relatif est neutralisé : on raisonne en dépense réelle/PIB réel (prix du PIB).
cf_A = r74 * ((1 + gE_7493) / (1 + gY_6074)) ** 19   # PIB au rythme 1960-74, dépense réelle observée
cf_B = r74 * ((1 + gE_6074) / (1 + gY_7493)) ** 19   # dépense au rythme 1960-74, PIB observé
cf_C = r74 * ((1 + gY_7493 + (gE_6074 - gY_6074)) / (1 + gY_7493)) ** 19  # écart dépense-PIB maintenu à celui de 1960-74
den.append(["CF_A_1993_PIB_au_rythme_1960_74_depense_observee", r74, cf_A, 100 * gE_7493, 100 * gY_6074, ""])
den.append(["CF_B_1993_depense_au_rythme_1960_74_PIB_observe", r74, cf_B, 100 * gE_6074, 100 * gY_7493, ""])
den.append(["CF_C_1993_ecart_dep_PIB_de_1960_74_maintenu", r74, cf_C, "", 100 * gY_7493, 100 * (gE_6074 - gY_6074)])
ecrire_csv("A05_denominateur_1974_1993.csv",
           ["periode_ou_scenario", "ratio_debut", "ratio_fin_ou_contrefactuel", "croissance_depense_reelle_pct_an",
            "croissance_PIB_volume_pct_an", "ecart_pts_an"], den)
print("OK", len(lignes), "années")
for r in den: print(r)

# ---------------------------------------------------------------------------
# Compléments (après revue) :
# (1) décomposition annuelle du ratio : d(ratio) ~ ratio_{t-1} * (gE - gY) / (1 + gY), gE et gY réels (prix du PIB)
# (2) variante sommet à sommet (1974, 1979, 1990, 2000, 2007, 2019 : années hautes du cycle, choix A05 à discuter)
# (3) consommation finale des APU (P3 S13) : vrai partage volume / prix relatif (T_1102, T_1103, lignes S13)
# ---------------------------------------------------------------------------
pv_s13 = serie("T_1102 en niveau", "S13")
pp_s13 = serie("T_1103 en niveau", "S13")
pc_s13 = serie("T_1101 en niveau", "S13")
an_l = []
for y in annees[1:]:
    if y - 1 not in annees:
        continue
    gE = (niv[("Total", y)] / defl[y]) / (niv[("Total", y - 1)] / defl[y - 1]) - 1
    gY = pibv[y] / pibv[y - 1] - 1
    r0 = 100 * niv[("Total", y - 1)] / pib[y - 1]; r1 = 100 * niv[("Total", y)] / pib[y]
    gEp = ((niv[("Total", y)] - niv[("Interets_D41", y)]) / defl[y]) / ((niv[("Total", y - 1)] - niv[("Interets_D41", y - 1)]) / defl[y - 1]) - 1
    an_l.append([y, r1, r1 - r0, 100 * gE, 100 * gEp, 100 * gY, r0 * (gE - gY) / (1 + gY)])
ecrire_csv("A05_ratio_annuel_depense_vs_PIB.csv",
           ["annee", "ratio_depense_pctPIB", "variation_points", "croissance_depense_reelle_pct", "croissance_depense_primaire_reelle_pct",
            "croissance_PIB_volume_pct", "variation_approx_points"], an_l)

pk = []
for a, b in [(1974, 1979), (1979, 1990), (1974, 1990), (1990, 2000), (2000, 2007), (2007, 2019), (1974, 2007), (1990, 2019)]:
    gE = taux(Ereal, a, b); gY = taux(pibv, a, b)
    pk.append(["%d-%d" % (a, b), 100 * niv[("Total", a)] / pib[a], 100 * niv[("Total", b)] / pib[b], 100 * gE, 100 * gY])
ecrire_csv("A05_ratio_sommet_a_sommet.csv", ["periode", "ratio_debut", "ratio_fin", "croissance_depense_reelle_pct_an", "croissance_PIB_volume_pct_an"], pk)

cs = []
for a, b in [(1960, 1974), (1974, 1993), (1993, 2007), (2007, 2019), (2019, 2025), (1974, 2025)]:
    n = b - a
    gv = (pv_s13[b] / pv_s13[a]) ** (1 / n) - 1
    gp_rel = ((pp_s13[b] / defl[b]) / (pp_s13[a] / defl[a])) ** (1 / n) - 1
    gY = (pibv[b] / pibv[a]) ** (1 / n) - 1
    cs.append(["%d-%d" % (a, b), 100 * pc_s13[a] / pib[a], 100 * pc_s13[b] / pib[b], 100 * gv, 100 * gp_rel, 100 * gY])
ecrire_csv("A05_conso_APU_volume_prix.csv", ["periode", "conso_APU_pctPIB_debut", "conso_APU_pctPIB_fin", "volume_conso_APU_pct_an",
                                              "prix_relatif_conso_APU_vs_PIB_pct_an", "PIB_volume_pct_an"], cs)
for r in cs: print("conso", r)
for r in pk: print("pic", r)
for r in an_l:
    if 1973 <= r[0] <= 1994: print("an", [round(x, 2) if isinstance(x, float) else x for x in r])
