# -*- coding: utf-8 -*-
"""A13 - portefeuille de redressement par la depense : economies nettes, trois enveloppes,
tests adverses, sensibilites et couverture des objectifs.

Entree : resultats/donnees/A13/A13_mesures.csv (construit par a13_construire_mesures.py)
Sorties (meme dossier) :
  A13_table_mesures.csv   livrable par mesure : brut ; net si adopte ; net apres decote d'execution
  A13_enveloppes.csv      totaux par enveloppe, horizon, statut d'additionnalite, nature SEC
  A13_tests_adverses.csv  tests sur l'enveloppe centrale si adoptee
  A13_sensibilites.csv    tableau de sensibilite (norme 04 §IV)
  A13_couverture.csv      part des objectifs couverte (reference tendancielle d'abord, puis base 2025 d'A01)
Usage : python -I a13_portefeuille.py

Definitions :
  net si adopte   = brut x (1 - retour PO direct) x part transmise au solde x (1 - report APU)
                    - 0,57 x multiplicateur x estompement x depense retiree + supplement d'emploi (age)
  net apres decote = idem avec un taux d'execution selon le risque politique (test, pas definition du net)
"""
import csv, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "donnees", "A13")
IN = os.path.join(ROOT, "A13_mesures.csv")
HORIZONS = (2027, 2030, 2035)
SEMI_ELAST = 0.57      # C : RESF 2027 (semi-elasticite du solde a l'ecart de production)

def pib_path(g_after=0.025):
    P = {2025: 2991.06}                  # C : Eurostat, notification d'octobre 2026
    P[2026] = P[2025] * 1.020            # C : RESF 2027, activite en valeur 2026
    P[2027] = P[2026] * 1.027            # C : RESF 2027, activite en valeur 2027
    for y in range(2028, 2036):
        P[y] = P[y - 1] * (1 + g_after)  # H
    return P

# Multiplicateurs (bas, central, haut) par categorie. Ancrage : HCFP avis 2026-5 §36 ; AFG 2019 ;
# Blanchard-Leigh via Astra. Valeurs par categorie = hypotheses A13.
MULT = {"salaires_publics": (0.5, 0.8, 1.2), "demande_publique": (0.6, 1.0, 1.5),
        "transferts_menages": (0.4, 0.8, 1.2), "pensions": (0.3, 0.5, 0.8), "sante_rembt": (0.3, 0.6, 1.0),
        "PO_entreprises": (0.3, 0.5, 0.8), "subventions": (0.3, 0.5, 0.8), "local_invest": (0.6, 1.0, 1.5),
        "offre": (0, 0, 0), "-": (0, 0, 0)}
MIDX = {"P": 2, "C": 1, "A": 0}
# Decote d'execution (test) : H ancree sur les precedents (gel PLFSS 2026 retire a 100 % ; 8 Md EUR locaux
# retires le 4/11/2026 ; CSG 2018 ; objectif d'emplois LPFP 2023-2027 manque ; -2,1 pts a 3 ans, A08).
EXEC = {"P": {"faible": 0.8, "moyen": 0.6, "eleve": 0.3},
        "C": {"faible": 0.9, "moyen": 0.75, "eleve": 0.5},
        "A": {"faible": 1.0, "moyen": 0.9, "eleve": 0.8}}

def fade(s, slow=False):
    if s < 0: return 0.0
    if s <= 1: return 1.0
    if s <= 4: return 0.8 if slow else 0.5
    return 0.4 if slow else 0.2

def f(x):
    try: return float(str(x).replace(",", "."))
    except ValueError: return 0.0

def load():
    with open(IN, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=";"))

def net_measure(r, env, year, opt=None):
    """Retourne (net, charge reportee hors APU, brut retenu)."""
    opt = opt or {}
    if r["variante_de"] or env not in r["enveloppes"]:
        return 0.0, 0.0, 0.0
    start = int(r["annee_debut"]) + opt.get("delay", 0)
    brut = f(r["brut_%d" % year]) * opt.get("brut_factor", 1.0)
    if opt.get("delay"):
        if year < start:
            brut = 0.0
        elif r["id"] == "P-A13-002" and year == 2030:
            brut *= 2 / 3                                     # une annee de regle en moins
    if r["id"] in opt.get("inflation_ids", ()):
        brut *= opt.get("inflation_factor", 1.0)
    brut_retenu = brut
    if r["deja_net_PO"] != "oui":
        brut *= (1 - f(r["retour_PO"]))
    risk = r["risque_politique"]
    ex = EXEC[env].get(risk, 1.0) if opt.get("decote") else 1.0
    if opt.get("recul"):
        ex *= {"eleve": 0.0, "moyen": 0.5}.get(risk, 1.0)
    pt = f(r["pass_through_" + env])
    if opt.get("report_integral") and r["assiette_groupe"] == "TRANSFERTS_LOCAUX":
        pt = 0.0
    rep = f(r["report_APU"])
    if opt.get("emploi_bas") and r["assiette_groupe"] == "AGE_DUREE":
        rep = max(rep, 0.3)
    executed = brut * ex
    consolidated = executed * pt * (1 - rep)
    cat = r["cat_multiplicateur"]
    m = MULT.get(cat, (0, 0, 0))[MIDX[env]]
    if opt.get("mult_high"):
        m = max(MULT.get(cat, (0, 0, 0))[2], 1.7 if cat in ("salaires_publics", "demande_publique", "transferts_menages", "local_invest") else 0)
    if year in opt.get("mult_years", ()):
        m *= opt.get("mult_factor", 1.0)
    macro = SEMI_ELAST * m * fade(year - start, opt.get("mult_high", False)) * executed * pt
    bonus = 0.0
    if year == 2035 and env in ("C", "A") and not (opt.get("delay") and year < start):
        bonus = f(r["bonus_emploi_2035_" + env]) * ex * opt.get("brut_factor", 1.0)
        if opt.get("emploi_bas"): bonus = 0.0
        if opt.get("emploi_haut"): bonus = f(r["bonus_emploi_2035_A"]) * ex
    netv = consolidated - macro + bonus
    hors = consolidated if r["report_hors_APU"].startswith("100") else 0.0
    return netv, hors, brut_retenu

def totals(rows, env, opt=None, P=None):
    P = P or pib_path()
    out = {}
    for y in HORIZONS:
        d = dict(net=0.0, hors=0.0, PO=0.0, PLF=0.0, Cour=0.0, nouveau=0.0, brut=0.0)
        for r in rows:
            n, h, b = net_measure(r, env, y, opt)
            d["net"] += n; d["hors"] += h; d["brut"] += b
            share = f(r["part_dans_PLF_PLFSS_2027"])
            d["PLF"] += n * share
            if r["statut_source"].lower().startswith("nouveau"): d["nouveau"] += n * (1 - share)
            else: d["Cour"] += n * (1 - share)
            if r["nature_SEC"].strip().startswith("PO"): d["PO"] += n
        d["pct"] = 100 * d["net"] / P[y]
        out[y] = d
    return out

def needs(P, g=0.027):
    stab = 100 * 1.193 * g / (1 + g)            # dette fin 2026 (RESF) ; deficit stabilisant
    tend = {2027: 6.5, 2030: 6.5 + 0.9, 2035: 6.5 + 2.4}   # RESF p.94 ; +0,3 pt/an des 2028 (RESF p.134), H au-dela
    base = {k: 100 * v / P[2025] for k, v in (("3 % (A01, base 2025)", 62), ("stabilisation basse (A01)", 67),
                                               ("stabilisation haute (A01)", 87), ("equilibre (A01)", 152))}
    return stab, tend, base

def main():
    rows = load(); P = pib_path()
    ENVS = ("P", "C", "A")
    adopte = {e: totals(rows, e, {}) for e in ENVS}
    decote = {e: totals(rows, e, {"decote": True}) for e in ENVS}
    # 1. table par mesure
    with open(os.path.join(ROOT, "A13_table_mesures.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["id", "mesure", "nature_SEC", "statut_additionnalite", "part_PLF_PLFSS_2027", "brut_2027", "brut_2030", "brut_2035",
                    "net_si_adopte_central_2027", "net_si_adopte_central_2030", "net_si_adopte_central_2035",
                    "net_apres_decote_central_2027", "net_apres_decote_central_2030", "net_apres_decote_central_2035",
                    "net_si_adopte_prudent_2030", "net_si_adopte_ambitieux_2030", "report_vers_autre_APU", "report_hors_APU",
                    "perdants", "niveau_preuve", "source", "provenance"])
        for r in rows:
            na = [net_measure(r, "C", y)[0] for y in HORIZONS]
            nd = [net_measure(r, "C", y, {"decote": True})[0] for y in HORIZONS]
            rep = r["report_APU"]
            if r["assiette_groupe"] == "TRANSFERTS_LOCAUX":
                rep = "collectivites : %.2f non transmis au solde (central)" % (1 - f(r["pass_through_C"]))
            w.writerow([r["id"], r["mesure"], r["nature_SEC"].strip(), r["statut_source"], r["part_dans_PLF_PLFSS_2027"],
                        r["brut_2027"], r["brut_2030"], r["brut_2035"]] + ["%.2f" % x for x in na + nd] +
                       ["%.2f" % net_measure(r, "P", 2030)[0], "%.2f" % net_measure(r, "A", 2030)[0], rep, r["report_hors_APU"],
                        r["perdants"], r["niveau_preuve"], r["source"], r["provenance"]])
    # 2. enveloppes
    with open(os.path.join(ROOT, "A13_enveloppes.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["enveloppe", "annee", "brut", "net_si_adopte", "pct_PIB_si_adopte", "net_apres_decote", "pct_PIB_apres_decote",
                    "dont_PLF_PLFSS_si_adopte", "dont_Cour_Senat_inspections_si_adopte", "dont_nouveau_si_adopte",
                    "dont_PO_SEC_si_adopte", "charge_reportee_menages_complementaires_si_adopte"])
        for e in ENVS:
            for y in HORIZONS:
                a, d = adopte[e][y], decote[e][y]
                w.writerow([e, y, "%.1f" % a["brut"], "%.1f" % a["net"], "%.2f" % a["pct"], "%.1f" % d["net"], "%.2f" % d["pct"],
                            "%.1f" % a["PLF"], "%.1f" % a["Cour"], "%.1f" % a["nouveau"], "%.1f" % a["PO"], "%.1f" % a["hors"]])
    # 3. tests adverses (enveloppe centrale si adoptee)
    tests = [("T0 centrale si adoptee", {}),
             ("T1 multiplicateurs eleves (1,7 demande, salaires, transferts, local ; effet persistant)", {"mult_high": True}),
             ("T2 rendement brut inferieur de moitie (supplement d'emploi compris)", {"brut_factor": 0.5}),
             ("T3 report integral des transferts locaux", {"report_integral": True}),
             ("T4 contestation : risque eleve retire, risque moyen a moitie", {"recul": True}),
             ("T4b decote d'execution centrale (precedents)", {"decote": True}),
             ("T5 recession 2027-2028 : multiplicateurs x2 en 2027 et 2030, gel 2027 a 40 %", {"mult_factor": 2.0, "mult_years": (2027, 2030), "inflation_factor": 0.4, "inflation_ids": ("P-A13-001",)}),
             ("T6 cumul T2 + T4", {"brut_factor": 0.5, "recul": True})]
    with open(os.path.join(ROOT, "A13_tests_adverses.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["test", "net_2027", "net_2030", "net_2035", "pct_PIB_2030", "ecart_2030_pct"])
        base30 = adopte["C"][2030]["net"]
        for name, opt in tests:
            res = totals(rows, "C", opt)
            w.writerow([name] + ["%.1f" % res[y]["net"] for y in HORIZONS] + ["%.2f" % res[2030]["pct"], "%.0f" % (100 * (res[2030]["net"] / base30 - 1))])
            print(name, [round(res[y]["net"], 1) for y in HORIZONS])
    # 4. sensibilites (norme §IV), enveloppe centrale si adoptee
    sens = [("croissance nominale 1,9 % apres 2027", {}, 0.019), ("croissance nominale 2,5 % (reference)", {}, 0.025),
            ("croissance nominale 3,0 % apres 2027", {}, 0.030),
            ("inflation basse : gel 2027 a 40 %", {"inflation_factor": 0.4, "inflation_ids": ("P-A13-001",)}, 0.025),
            ("calendrier decale d'un an", {"delay": 1}, 0.025),
            ("emploi bas (report 30 %, pas de supplement)", {"emploi_bas": True}, 0.025),
            ("emploi haut (supplement maximal de la Cour)", {"emploi_haut": True}, 0.025),
            ("multiplicateurs bas (jeu ambitieux)", None, 0.025), ("multiplicateurs hauts (jeu prudent)", None, 0.025)]
    with open(os.path.join(ROOT, "A13_sensibilites.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["variante", "net_2027", "net_2030", "net_2035", "pct_PIB_2030", "pct_PIB_2035", "besoin_3pc_tendanciel_2030_pts", "besoin_stabilisation_2030_pts"])
        for name, opt, g in sens:
            Pg = pib_path(g)
            if opt is None:
                # multiplicateurs seulement : on reutilise le jeu de l'enveloppe A (bas) ou P (haut) sur le contenu central
                idx = 0 if "bas" in name else 2
                saved = dict(MIDX); MIDX["C"] = idx
                res = totals(rows, "C", {}, Pg); MIDX.update(saved)
            else:
                res = totals(rows, "C", opt, Pg)
            stab, tend, _ = needs(Pg, g if g != 0.025 else 0.027)
            w.writerow([name] + ["%.1f" % res[y]["net"] for y in HORIZONS] + ["%.2f" % res[2030]["pct"], "%.2f" % res[2035]["pct"],
                        "%.2f" % (tend[2030] - 3.0), "%.2f" % (tend[2030] - stab)])
        w.writerow(["taux +100 / +200 pb", "rendement inchange", "", "", "", "", "besoin accru (charge d'interets)", "non calcule par A13 (A07, A15)"])
        w.writerow(["couts administratifs ; effet sur la dette", "non estimes", "", "", "", "", "", ""])
    # 5. couverture
    stab, tend, base = needs(P)
    with open(os.path.join(ROOT, "A13_couverture.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["enveloppe", "annee", "variante", "net_pct_PIB", "objectif", "besoin_pts", "part_couverte_pct"])
        for e in ENVS:
            for lab, res in (("si adopte", adopte[e]), ("apres decote", decote[e])):
                for y in HORIZONS:
                    p = res[y]["pct"]
                    for k, v in (("3 % depuis le tendanciel", tend[y] - 3.0), ("stabilisation depuis le tendanciel", tend[y] - stab),
                                 ("equilibre depuis le tendanciel", tend[y])):
                        w.writerow([e, y, lab, "%.2f" % p, k + (" (H)" if y > 2027 else ""), "%.2f" % v, "%.0f" % (100 * p / v)])
                    for k, v in base.items():
                        w.writerow([e, y, lab, "%.2f" % p, k + " - borne haute", "%.2f" % v, "%.0f" % (100 * p / v)])
    print("deficit stabilisant", round(stab, 2))
    for e in ENVS:
        for lab, res in (("adopte", adopte[e]), ("decote", decote[e])):
            print(e, lab, {y: (round(res[y]["brut"], 1), round(res[y]["net"], 1), round(res[y]["pct"], 2), "PLF", round(res[y]["PLF"], 1),
                              "Cour", round(res[y]["Cour"], 1), "new", round(res[y]["nouveau"], 1), "PO", round(res[y]["PO"], 1),
                              "hors", round(res[y]["hors"], 1)) for y in HORIZONS})
    # controle : recoupement des mesures de la Cour avec le PLF (doit tomber dans 11-14 Md EUR)
    rec = sum(f(r["brut_2027"]) * f(r["part_dans_PLF_PLFSS_2027"]) for r in rows
              if r["statut_source"].startswith("Cour") and not r["variante_de"])
    print("recoupement Cour x PLF (brut 2027, mesures Cour du portefeuille) :", round(rec, 1))

if __name__ == "__main__":
    main()
