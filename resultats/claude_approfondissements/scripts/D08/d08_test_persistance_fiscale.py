# -*- coding: utf-8 -*-
"""D08, test 2.6 : la succession des décisions fiscales explique-t-elle la persistance du déficit ?

CALCUL CONDITIONNEL, PAS UNE ESTIMATION CAUSALE.
On retire du déficit observé le cumul des « mesures nouvelles » en prélèvements obligatoires
depuis une année de départ, à dépenses, activité et taux d'intérêt inchangés. Deux variantes :
  - statique : solde_cf = solde + (-cumul des mesures) ;
  - avec intérêts : la dette évitée ne porte pas intérêt (taux apparent observé de l'année).
Ce calcul suppose que rien d'autre n'aurait changé (ni l'activité, ni les dépenses, ni les
hausses d'impôts ultérieures, qui ont en partie répondu aux baisses). Il donne un ordre de
grandeur comptable et sa sensibilité à l'année de départ ; rien de plus.

Série : D05_mesures_nouvelles_annuelles.csv (lignes « retenu = oui »), 2000-2025.
Ruptures de source : 2008/2009, 2011/2012, 2016/2017. Les années 2009-2011 sont hétérogènes :
on donne deux variantes pour 2010 (+0,1 point, estimation d'automne ; -0,4 point, Cour 2011).
Lancement : python d08_test_persistance_fiscale.py
"""
import csv
import os
import sys
import warnings

import openpyxl

warnings.filterwarnings("ignore")
def _racine_depot(depart):
    """Remonte depuis `depart` jusqu'au dossier qui contient la première enquête (indépendant de l'emplacement)."""
    p = os.path.abspath(depart)
    while True:
        if os.path.isdir(os.path.join(p, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "commun")):
            return p
        q = os.path.dirname(p)
        if q == p:
            raise SystemExit("racine du dépôt introuvable depuis " + depart)
        p = q


ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(ICI, "..", "..", "donnees", "D08"))
D05 = os.path.normpath(os.path.join(ICI, "..", "..", "donnees", "D05"))
RACINE = _racine_depot(ICI)
BASE = os.path.join(RACINE, "Le_Constat_Cellule_Enquete", "resultats", "donnees")


def num(x):
    x = (x or "").strip().replace(",", ".")
    return float(x) if x not in ("",) else None


# --- mesures nouvelles, une valeur par année, en points de PIB
mes = {}
for r in csv.DictReader(open(os.path.join(D05, "D05_mesures_nouvelles_annuelles.csv"), encoding="utf-8-sig"), delimiter=";"):
    if r["retenu"].strip() != "oui":
        continue
    a = int(r["annee"])
    v = num(r["mesures_pts_PIB_base2020"])
    if v is None:
        v = num(r["mesures_pts_PIB_source"])
    mes[a] = v
assert sorted(mes) == list(range(2000, 2026)), sorted(mes)
VARIANTES_2010 = {"2010_estimation_automne": mes[2010], "2010_Cour_2011": -0.4}

# --- comptes observés
pib, po = {}, {}
for r in csv.DictReader(open(os.path.join(BASE, "A04", "a04_po_recettes_1959_2025.csv"), encoding="utf-8-sig"), delimiter=";"):
    pib[int(r["annee"])] = float(r["PIB_implicite_Md_EUR"])
    po[int(r["annee"])] = float(r["PO_pctPIB"])
dette = {}
for r in csv.DictReader(open(os.path.join(BASE, "commun", "base_insee_dette_sous_secteurs.csv"), encoding="utf-8-sig"), delimiter=";"):
    if r["feuille"] == "Figure 1" and r["serie"] == "Ensemble":
        dette[int(r["annee"])] = float(r["valeur"])
wb = openpyxl.load_workbook(os.path.join(BASE, "commun", "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
L = list(wb.worksheets[0].iter_rows(values_only=True))
annees_l = L[2]


def ligne(debut, occ=0):
    vu = 0
    for r in L:
        if r and len(r) > 1 and r[1] is not None and str(r[1]).strip().startswith(debut):
            if vu == occ:
                return {int(str(a).strip()): v for a, v in zip(annees_l, r)
                        if a is not None and str(a).strip().isdigit() and isinstance(v, (int, float))}
            vu += 1
    raise SystemExit(debut)


solde = ligne("Capacité (+) ou besoin (-) de financement")
interets = ligne("Intérêts (D41)", 0)  # dépenses

# Bascule de 2019 : le crédit d'impôt pour la compétitivité et l'emploi, compté en dépense, est remplacé
# par une baisse de cotisations. La mesure de 2019 (-23,6 Md EUR) contient cette baisse ; D04 relève que
# 20,2 Md EUR sont classés « exceptionnels » (année double). Variante « neutralisée » : on retire 20,2 Md EUR
# de la mesure de 2019, c'est-à-dire qu'on ne compte pas comme perte de recettes ce qui remplace une dépense.
BASCULE_2019_PTS = 100 * 20.2 / pib[2019]
VARIANTES_BASCULE = {"bascule_2019_comptee": 0.0, "bascule_2019_neutralisee": BASCULE_2019_PTS}

lignes, synth = [], []
for nomvar, v2010, nombasc, corr in [(a, b, c, d) for a, b in VARIANTES_2010.items() for c, d in VARIANTES_BASCULE.items()]:
    m = dict(mes)
    m[2010] = v2010
    m[2019] = mes[2019] + corr
    for depart in (2000, 2003, 2007, 2012, 2017, 2018):
        cumul = 0.0
        dette_evitee = 0.0  # Md EUR
        n_exc = n_exc_i = n_prim = n_prim_i = 0
        for a in range(depart, 2026):
            cumul += m[a]
            recette_sup = -cumul * pib[a] / 100.0           # recettes en plus si aucune mesure depuis `depart`
            taux = interets[a] / dette[a - 1]
            eco_int = taux * dette_evitee                    # intérêts économisés sur la dette évitée
            s_obs = 100 * solde[a] / pib[a]
            prim_obs = 100 * (solde[a] + interets[a]) / pib[a]
            s_stat = s_obs - cumul
            s_int = s_stat + 100 * eco_int / pib[a]
            prim_stat = prim_obs - cumul
            dette_evitee = dette_evitee + recette_sup + eco_int
            n_exc += s_stat >= 0
            n_exc_i += s_int >= 0
            n_prim += prim_stat >= 0
            n_prim_i += prim_obs >= 0
            lignes.append({
                "variante_2010": nomvar, "variante_bascule": nombasc, "annee_de_depart": depart, "annee": a,
                "mesures_annee_pts": round(m[a], 2), "cumul_mesures_pts": round(cumul, 2),
                "solde_observe_pct": round(s_obs, 2), "solde_sans_mesures_statique_pct": round(s_stat, 2),
                "solde_sans_mesures_avec_interets_pct": round(s_int, 2),
                "solde_primaire_observe_pct": round(prim_obs, 2), "solde_primaire_sans_mesures_pct": round(prim_stat, 2),
                "dette_observee_pct": round(100 * dette[a] / pib[a], 1),
                "dette_sans_mesures_pct": round(100 * (dette[a] - dette_evitee) / pib[a], 1),
            })
        d = lignes[-1]
        nb = 2026 - depart
        synth.append({
            "variante_2010": nomvar, "variante_bascule": nombasc, "annee_de_depart": depart, "nb_annees": nb,
            "cumul_mesures_2025_pts": d["cumul_mesures_pts"],
            "variation_PO_observee_pts": round(po[2025] - po[depart - 1], 2),
            "evolution_spontanee_residuelle_pts": round(po[2025] - po[depart - 1] - d["cumul_mesures_pts"], 2),
            "solde_2025_observe": d["solde_observe_pct"],
            "solde_2025_sans_mesures_statique": d["solde_sans_mesures_statique_pct"],
            "solde_2025_sans_mesures_avec_interets": d["solde_sans_mesures_avec_interets_pct"],
            "dette_2025_observee": d["dette_observee_pct"], "dette_2025_sans_mesures": d["dette_sans_mesures_pct"],
            "annees_excedent_statique": int(n_exc), "annees_excedent_avec_interets": int(n_exc_i),
            "annees_excedent_primaire_sans_mesures": int(n_prim), "annees_excedent_primaire_observees": int(n_prim_i),
        })

for nom, tab in (("D08_persistance_fiscale_annuel.csv", lignes), ("D08_persistance_fiscale_synthese.csv", synth)):
    with open(os.path.join(OUT, nom), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(tab[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(tab)

sys.stdout.reconfigure(encoding="utf-8")
for s in synth:
    print(s["variante_2010"][5:14], s["variante_bascule"][13:], s["annee_de_depart"], "cumul", s["cumul_mesures_2025_pts"], "solde stat", s["solde_2025_sans_mesures_statique"], "avec int", s["solde_2025_sans_mesures_avec_interets"], "dette", s["dette_2025_sans_mesures"], "exc", s["annees_excedent_statique"], s["annees_excedent_avec_interets"], "prim", s["annees_excedent_primaire_sans_mesures"])
print("--- trajectoire, départ 2000, variante estimation d'automne")
for l in lignes:
    if False:
        print(l["annee"], l["cumul_mesures_pts"], l["solde_observe_pct"], l["solde_sans_mesures_statique_pct"],
              l["solde_sans_mesures_avec_interets_pct"], l["dette_observee_pct"], l["dette_sans_mesures_pct"])
