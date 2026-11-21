# -*- coding: utf-8 -*-
"""
S03 - Synthèse T-02 : table par risque de la hausse 1974-1985 des prestations / PIB en quatre termes
(dénominateur, bénéficiaires, prestation moyenne [inertie de montée en charge | décisions datées chiffrées], résidu).

Ordre de relance : decomposition_prestations_1974_1985.py, puis baremes_regle_vs_decision.py, puis ce script.
Entrées : resultats\\donnees\\S03\\S03_series_annuelles.csv, S03_baremes.csv, S03_decomposition.csv
Sortie  : resultats\\donnees\\S03\\S03_table_finale.csv (+ affichage)

Conventions (toutes en points de PIB, ventilation logarithmique LMDI, R = prestations Drees tous régimes / PIB Insee) :
- Vieillesse-survie : règle de revalorisation OBSERVÉE (coefficients RG, IPP). Identité exacte :
  dlnR = dln(N60/POP) + [dln reval - dln(Y/EMP)] + dln(dérive) + [dln(Y/EMP) - dln(Y/POP)]
  où dérive = dépense par personne de 60+ / indice de revalorisation (montée en charge, noria, couverture, extensions).
  Dénominateur = dernier crochet (le ralentissement du PIB par emploi est transmis aux pensions par l'indexation
  sur le salaire moyen ; seule la baisse du ratio emploi/population ne l'est pas).
  Inertie de montée en charge = rythme de la dérive sur la fenêtre de référence avant 1974.
  Décisions datées chiffrées = écart revalorisation/salaire (règle appliquée ou freinée) + surplus du minimum vieillesse
  (borné) + retraite à 60 ans (coûts publiés, S01). Résidu = reste de l'excès de dérive.
- Autres risques : règle approchée par le PIB nominal par emploi (variante III de decomposition_prestations), aucune
  décision chiffrée sur pièce consultée -> l'écart à la règle est entièrement en résidu.
"""
import csv
import math
import os

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
OUT = os.path.join(RACINE, "donnees", "S03")
F_PAR_EUR = 6.55957
A0, A1 = 1974, 1985

SER = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(OUT, "S03_series_annuelles.csv"), encoding="utf-8"), delimiter=";")}
BAR = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(OUT, "S03_baremes.csv"), encoding="utf-8"), delimiter=";")}
DEC = list(csv.DictReader(open(os.path.join(OUT, "S03_decomposition.csv"), encoding="utf-8"), delimiter=";"))

f = lambda d, k, a: float(d[a][k])
Y85_FRF = f(SER, "PIB_MEUR", 1985) * 1e6 * F_PAR_EUR

# ---- Vieillesse-survie, règle observée ----
def vieillesse(fen, reval="pension_RG_indice_A", mv=(0.188, 0.375), ans60=(3.0, 8.9), conv="par60"):
    R0 = 100 * f(SER, "Vieillesse-survie_MEUR", A0) / f(SER, "PIB_MEUR", A0)
    R1 = 100 * f(SER, "Vieillesse-survie_MEUR", A1) / f(SER, "PIB_MEUR", A1)
    L = (R1 - R0) / math.log(R1 / R0)
    sh = lambda a: f(SER, "pop60p_milliers", a) / f(SER, "pop_moy_milliers", a)
    spend60 = lambda a: f(SER, "Vieillesse-survie_MEUR", a) / f(SER, "pop60p_milliers", a)
    rv = lambda a: f(BAR, reval, a)
    der = lambda a: spend60(a) / rv(a)
    q = lambda a: f(BAR, "PIB_nominal_par_emploi_EUR", a)
    yh = lambda a: f(BAR, "PIB_nominal_par_habitant_EUR", a)
    T = A1 - A0
    t_ben = math.log(sh(A1) / sh(A0))
    t_regle = math.log(rv(A1) / rv(A0)) - math.log(q(A1) / q(A0))
    t_den = math.log(q(A1) / q(A0)) - math.log(yh(A1) / yh(A0))
    d_pre = math.log(der(fen[1]) / der(fen[0])) / (fen[1] - fen[0])
    t_inert = d_pre * T
    if conv == "masse":
        # Contrefactuel : le volume (masse / indice de revalorisation) garde son rythme d'avant 1974, quelle que soit
        # la démographie des 60+ ; l'inertie absorbe alors la croissance observée de N60 (le terme T2 reste inchangé).
        masse = lambda a: f(SER, "Vieillesse-survie_MEUR", a) / rv(a)
        m_pre = math.log(masse(fen[1]) / masse(fen[0])) / (fen[1] - fen[0])
        t_inert = m_pre * T - math.log(f(SER, "pop60p_milliers", A1) / f(SER, "pop60p_milliers", A0))
        d_pre = m_pre
    t_exces = math.log(der(A1) / der(A0)) - t_inert
    # contrôle de l'identité (écart dû aux arrondis des CSV seulement)
    ecart = (t_ben + t_regle + t_den + t_inert + t_exces) - math.log(R1 / R0)
    res = {"hausse": R1 - R0, "den": L * t_den, "ben": L * t_ben, "inertie": L * t_inert, "regle": L * t_regle,
           "exces": L * t_exces, "controle_log": ecart, "d_pre_pct": 100 * d_pre,
           "d_obs_pct": 100 * math.log(der(A1) / der(A0)) / T}
    lo = res["regle"] + mv[0] + 100 * ans60[0] * 1e9 / Y85_FRF
    hi = res["regle"] + mv[1] + 100 * ans60[1] * 1e9 / Y85_FRF
    res["decisions_bas"], res["decisions_haut"] = lo, hi
    res["residu_si_dec_bas"] = res["exces"] - (lo - res["regle"])
    res["residu_si_dec_haut"] = res["exces"] - (hi - res["regle"])
    return res

print("=== Vieillesse-survie 1974-1985, règle de revalorisation observée ===")
VIE = {}
for fen in [(1964, 1974), (1969, 1974), (1960, 1974)]:
  for conv in ["par60", "masse"]:
    for reval in ["pension_RG_indice_A", "pension_RG_indice_B"]:
        r = vieillesse(fen, reval, conv=conv)
        VIE[(fen, reval, conv)] = r
        print("[%s] fenêtre %d-%d %s : hausse %.2f | dénominateur %.2f | bénéficiaires %.2f | inertie (dérive %.2f%%/an) %.2f | règle %.2f | excès de dérive %.2f (dérive obs. %.2f%%/an) | décisions chiffrées %.2f à %.2f | résidu %.2f à %.2f | ctrl %.1e"
              % (conv, fen[0], fen[1], reval[-1], r["hausse"], r["den"], r["ben"], r["d_pre_pct"], r["inertie"], r["regle"], r["exces"], r["d_obs_pct"],
                 r["decisions_bas"], r["decisions_haut"], r["residu_si_dec_haut"], r["residu_si_dec_bas"], r["controle_log"]))

# ---- Autres risques (variante III, règle approchée) ----
def autre(risque, fen, periode="1974-1985", ratio_constant=False):
    for r in DEC:
        if r["risque"] == risque and r["fenetre_tendance"] == fen and r["periode"] == periode:
            if ratio_constant:
                # Contrefactuel « ratio constant » : pas de prolongation de la dérive d'avant 1974 (utile pour la famille,
                # dont la tendance 1964-74 est une érosion) ; le dénominateur est pris brut de tendance (variante III).
                h = float(r["hausse_pts"]); den = float(r["III_T1_denominateur_emploi"]); ben = float(r["I_T2_beneficiaires"])
                return {"hausse": h, "den": den, "ben": ben, "inertie": 0.0, "regle": 0.0, "exces": h - den - ben,
                        "decisions_bas": 0.0, "decisions_haut": 0.0}
            return {"hausse": float(r["hausse_pts"]), "den": float(r["III_T1_denominateur_emploi"]),
                    "ben": float(r["I_T2_beneficiaires"]), "inertie": float(r["I_T3a_derive_ancienne"]),
                    "regle": 0.0, "exces": float(r["III_T3b_ecart_regle_productivite"]),
                    "decisions_bas": 0.0, "decisions_haut": 0.0}
    raise KeyError((risque, fen))

AUTRES = ["Santé (maladie, invalidité, AT-MP)", "Famille", "Logement", "Pauvreté-exclusion", "Emploi (chômage, préretraites, insertion)"]
lignes = []
SYNTH = []
for conv in ["par60", "masse"]:
  for fam_rc in [False, True]:
    for fen in [(1964, 1974), (1969, 1974), (1959, 1974)]:
        fs = "%d-%d" % fen
        fv = fen if fen != (1959, 1974) else (1960, 1974)
        v = vieillesse(fv, "pension_RG_indice_A", conv=conv)
        v["risque"] = "Vieillesse-survie"
        rows = [v] + [dict(autre(k, fs, ratio_constant=(fam_rc and k == "Famille")), risque=k) for k in AUTRES]
        tot = {k: sum(r[k] for r in rows) for k in ["hausse", "den", "ben", "inertie", "regle", "exces", "decisions_bas", "decisions_haut"]}
        tag = "vieillesse=%s ; famille=%s ; fenêtre=%s" % (conv, "ratio constant" if fam_rc else "tendance", fs)
        print("\n=== %s (vieillesse : %d-%d, revalorisation A) ===" % (tag, fv[0], fv[1]))
        print("%-45s %7s %7s %7s %7s %7s %13s %13s" % ("risque", "hausse", "dénom.", "bénéf.", "inertie", "règle", "décis. chiff.", "résidu"))
        for r in rows + [dict(tot, risque="TOTAL")]:
            dec_lo, dec_hi = r["decisions_bas"], r["decisions_haut"]
            res_lo = r["hausse"] - r["den"] - r["ben"] - r["inertie"] - dec_hi
            res_hi = r["hausse"] - r["den"] - r["ben"] - r["inertie"] - dec_lo
            print("%-45s %7.2f %7.2f %7.2f %7.2f %7.2f %6.2f à %4.2f %6.2f à %4.2f" % (r["risque"][:45], r["hausse"], r["den"], r["ben"], r["inertie"], r["regle"], dec_lo, dec_hi, res_lo, res_hi))
            lignes.append({"convention_vieillesse": conv, "convention_famille": "ratio constant" if fam_rc else "tendance",
                           "fenetre": fs, "risque": r["risque"], "hausse_pts": round(r["hausse"], 3), "T1_denominateur": round(r["den"], 3),
                           "T2_beneficiaires": round(r["ben"], 3), "T3_inertie_montee_en_charge": round(r["inertie"], 3),
                           "T3_dont_ecart_revalorisation_regle": round(r["regle"], 3),
                           "T3_decisions_chiffrees_bas": round(dec_lo, 3), "T3_decisions_chiffrees_haut": round(dec_hi, 3),
                           "T4_residu_bas": round(res_lo, 3), "T4_residu_haut": round(res_hi, 3)})
        inert = tot["den"] + tot["ben"] + tot["inertie"]
        H = tot["hausse"]
        p_in = 100 * inert / H; p_dlo = 100 * tot["decisions_bas"] / H; p_dhi = 100 * tot["decisions_haut"] / H
        p_rlo = 100 * (H - inert - tot["decisions_haut"]) / H; p_rhi = 100 * (H - inert - tot["decisions_bas"]) / H
        print("Parts de la hausse %.2f pts : inertie identifiée %.0f %% ; décisions chiffrées %.0f à %.0f %% ; résidu %.0f à %.0f %% ; part décidée maximale (décisions + résidu positif) %.0f %%"
              % (H, p_in, p_dlo, p_dhi, p_rlo, p_rhi, 100 - p_in))
        SYNTH.append((tag, p_in, p_dlo, p_dhi, p_rlo, p_rhi, 100 - p_in))

print("\n=== Récapitulatif des conventions ===")
for t in SYNTH:
    print("%-70s inertie %3.0f %% | décisions chiffrées %2.0f-%2.0f %% | résidu %3.0f-%3.0f %% | plafond décidé %3.0f %%" % t)
print("Fourchette sur toutes conventions : inertie %.0f-%.0f %% ; plafond de la part décidée %.0f-%.0f %%"
      % (min(t[1] for t in SYNTH), max(t[1] for t in SYNTH), min(t[6] for t in SYNTH), max(t[6] for t in SYNTH)))

with open(os.path.join(OUT, "S03_table_finale.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(lignes[0].keys()), delimiter=";")
    w.writeheader()
    for l in lignes:
        w.writerow(l)
print("\nPIB 1985 = %.1f Md F ; retraite à 60 ans 3 / 8,9 Md F = %.3f / %.3f pt de PIB" % (Y85_FRF / 1e9, 100 * 3e9 / Y85_FRF, 100 * 8.9e9 / Y85_FRF))
