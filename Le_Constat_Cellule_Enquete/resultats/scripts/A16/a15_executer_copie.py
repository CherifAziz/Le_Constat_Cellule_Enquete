# -*- coding: utf-8 -*-
"""A15 - execution de bout en bout : reference 2026-2050, objectifs x horizons,
combinaison des portefeuilles A13 et A14 sans double compte, sensibilites, chocs,
test de credibilite A08. Lancer : python -I a15_executer.py
Sorties : donnees\\A15\\A15_*.csv et A15_sortie_executer.txt"""
import csv, os, sys, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a15_modele_copie import (Macro, Interets, projeter, calibrer_rm, vieillissement, ANNEES,
                        PIB_2025, DETTE_2025, SOLDE_2025, DON, SORTIE, SEMI_ELAST)
# A16 : sorties redirigees hors du dossier d'A15 (copie de contre-expertise)
SORTIE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A16\rejeu_A15"

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

def ecrire(nom, lignes):
    if not lignes:
        return
    cols = []
    for l in lignes:
        for k in l:
            if k not in cols:
                cols.append(k)
    with open(os.path.join(SORTIE, nom), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=cols, delimiter=";")
        w.writeheader()
        for l in lignes:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})

def fl(x):
    try:
        return float(str(x).replace(",", "."))
    except ValueError:
        return 0.0

PT = PIB_2025 / 100.0   # 1 point de PIB 2025 = 29,9 Md€

# ====================================================================== 1. macro et reference
INT = Interets()                     # f = 0,10 (calage 2015-2019), s = 9 %, rr = 0,5 %
macro = Macro()
rm_cal = calibrer_rm(INT, macro)
RM_LT = 4.0                          # H : taux moyen a l'emission de long terme (croissance nominale 2,8 % + 1,2 pt)
macro.rm = dict(rm_cal)
for a in (2029, 2030, 2031):         # convergence lineaire de la valeur calee 2028 vers le long terme en 2032
    macro.rm[a] = rm_cal[2028] + (RM_LT - rm_cal[2028]) * (a - 2028) / 4.0
macro.rm_lt = RM_LT
log("Taux de marche moyen a l'emission cales sur la Commission :", {k: round(v, 2) for k, v in rm_cal.items()})

CIBLES_REF = {2026: 5.5, 2027: 6.5}  # Commission 2026 [C] ; RESF 2027 a politique inchangee [C]
REF = projeter(macro, ref=None, cibles_ref=CIBLES_REF, interets=INT)

def ligne_traj(nom, R, annees=(2026, 2027, 2028, 2030, 2035, 2040, 2050)):
    A = R["annees"]
    out = {"scenario": nom}
    for a in annees:
        if a in A:
            out[f"deficit_{a}"] = A[a]["deficit"]
            out[f"dette_{a}"] = A[a]["d"]
            out[f"interets_{a}"] = A[a]["i_pct"]
    return out

traj = []
for a in ANNEES:
    x = REF["annees"][a]
    traj.append(dict(annee=a, PIB_mdeur=x["Y"], croissance_nominale=x["g_nom"], ecart_production=x["gap"],
                     solde_primaire=x["pb"], interets_pct=x["i_pct"], interets_mdeur=x["I"], deficit=x["deficit"],
                     dette_pct=x["d"], taux_moyen_encours=x["a"], taux_emission=x["rm"]))
ecrire("A15_reference_2026_2050.csv", traj)
log("Reference : pb structurel 2026/2027 =", round(REF["pb_struct"][2026], 2), round(REF["pb_struct"][2027], 2))
for a in (2026, 2027, 2028, 2030, 2035, 2040, 2050):
    x = REF["annees"][a]
    log(f"  ref {a}: deficit {x['deficit']:.2f}  interets {x['i_pct']:.2f}  dette {x['d']:.1f}  g_nom {x['g_nom']:.2f}")

# ====================================================================== 2. objectifs x horizons
MC = {"effort": 0.6}                  # multiplicateur composite (moitie depenses, moitie recettes) [H]

def serie_rampe(X, h, fixe=None):
    s = {}
    for t in ANNEES:
        if t < 2027:
            s[t] = 0.0
        elif t <= h:
            s[t] = X * (t - 2026) / (h - 2026)
        else:
            s[t] = fixe.get(t, X) if fixe else X
    return s

def atteint(obj, R, t):
    A = R["annees"]
    if obj == "equilibre":
        return A[t]["deficit"] <= 0.0
    if obj == "trois":
        return A[t]["deficit"] <= 3.0
    # stabilisation et baisse : definies sur la croissance nominale TENDANCIELLE (potentiel x deflateur),
    # pour ne pas confondre l'objectif avec l'effet de denominateur de l'annee (voir C-A15-009)
    prev = A[t - 1]["d"] if t - 1 in A else 115.682
    gn = (1 + MACRO_OBJ[0].gpot[t] / 100.0) * (1 + MACRO_OBJ[0].defl[t] / 100.0) - 1
    stab = prev * gn / (1 + gn)
    if obj == "stabilisation":
        return A[t]["deficit"] <= stab
    if obj == "baisse":
        return A[t]["deficit"] <= stab - 1.0
    raise ValueError(obj)

def bissection(fn, lo=-5.0, hi=25.0, it=40):
    for _ in range(it):
        mid = (lo + hi) / 2
        if fn(mid):
            hi = mid
        else:
            lo = mid
    return hi

MACRO_OBJ = [macro]

def effort(obj, h, mult=None, macro_=None, vieil="central", maintien_jusqua=2050, ref=None, emploi=0.0):
    mult = mult or MC
    macro_ = macro_ or macro
    ref = ref or REF
    MACRO_OBJ[0] = macro_
    P = lambda s, fin: projeter(macro_, {"effort": s}, mult, ref=ref, interets=INT, vieil=vieil, fin=fin, emploi=emploi)
    X = bissection(lambda x: atteint(obj, P(serie_rampe(x, h), h), h))
    serie = serie_rampe(X, h)
    # maintien de la cible chaque annee apres l'horizon (mesures recalculees annee par annee)
    for t in range(h + 1, maintien_jusqua + 1):
        def ok(x, t=t):
            s = dict(serie)
            for u in range(t, 2051):
                s[u] = x
            return atteint(obj, P(s, t), t)
        xt = bissection(ok)
        for u in range(t, 2051):
            serie[u] = xt
    R = P(serie, 2050)
    return serie, R

# Reference B : solde primaire structurel de 2025 maintenu (aucune derive 2025-2027 ; meme vieillissement)
PBS25 = -2.871 - SEMI_ELAST * 0.2
REFB = {"pb_struct": {2026: PBS25, 2027: PBS25}}
RB = projeter(macro, ref=REFB, interets=INT)
for a in (2026, 2027, 2030, 2035, 2050):
    x = RB["annees"][a]
    log(f"  refB {a}: deficit {x['deficit']:.2f}  interets {x['i_pct']:.2f}  dette {x['d']:.1f}")
ecrire("A15_reference_B_2025_maintenu.csv", [dict(annee=a, deficit=RB["annees"][a]["deficit"], dette=RB["annees"][a]["d"],
                                                  interets=RB["annees"][a]["i_pct"]) for a in ANNEES])

obj_lignes = []
for refnom, refd in (("A : 2027 a politique inchangee (6,5 %)", REF), ("B : solde primaire structurel 2025 maintenu", REFB)):
  for obj in ("equilibre", "trois", "stabilisation", "baisse"):
    for h in (2027, 2030, 2035):
        serie, R = effort(obj, h, ref=refd)
        Rref = projeter(macro, ref=refd, interets=INT)
        A = R["annees"]
        l = dict(reference=refnom, objectif=obj, horizon=h,
                 mesures_2027_pts=serie[2027], mesures_2030_pts=serie[2030], mesures_2035_pts=serie[2035],
                 mesures_2050_pts=serie[2050],
                 mesures_horizon_mdeur_echelle2025=serie[h] * PT,
                 mesures_horizon_mdeur_courants=serie[h] * A[h]["Y"] / 100.0,
                 deficit_reference_horizon=Rref["annees"][h]["deficit"],
                 deficit_horizon=A[h]["deficit"], dette_horizon=A[h]["d"], dette_2050=A[2050]["d"],
                 interets_2050=A[2050]["i_pct"], solde_primaire_2050=A[2050]["pb"])
        obj_lignes.append(l)
        log(f"[{refnom[:1]}] Objectif {obj:13s} h={h}: mesures {serie[2027]:.2f}/{serie[2030]:.2f}/{serie[2035]:.2f}/{serie[2050]:.2f} pts "
            f"(horizon {serie[h]*PT:.0f} Md€ ech. 2025) ; dette h {A[h]['d']:.1f}, 2050 {A[2050]['d']:.1f}")
ecrire("A15_objectifs_horizons.csv", obj_lignes)

# cible intergenerationnelle definie : dette ramenee a 100 % du PIB en 2045, mesures en rampe jusqu'en 2030 puis
# constantes en % du PIB (aucun ajustement ulterieur pour le vieillissement)
def d2045(x):
    return projeter(macro, {"effort": serie_rampe(x, 2030)}, MC, ref=REF, interets=INT)["annees"][2045]["d"] <= 100.0
Xi = bissection(d2045)
Ri = projeter(macro, {"effort": serie_rampe(Xi, 2030)}, MC, ref=REF, interets=INT)
log(f"Cible intergenerationnelle (100 % en 2045) : mesures {Xi:.2f} pts en 2030 ({Xi*PT:.0f} Md€), deficit 2030 {Ri['annees'][2030]['deficit']:.2f}, dette 2050 {Ri['annees'][2050]['d']:.1f}")
ecrire("A15_cible_intergenerationnelle.csv", [dict(definition="dette a 100 % du PIB en 2045 ; rampe 2027-2030 puis constant",
                                                   mesures_pts=Xi, mesures_mdeur_ech2025=Xi * PT,
                                                   deficit_2030=Ri["annees"][2030]["deficit"], deficit_2035=Ri["annees"][2035]["deficit"],
                                                   dette_2035=Ri["annees"][2035]["d"], dette_2050=Ri["annees"][2050]["d"])])

# ecarts statiques depuis 2025 (A01) et depuis 2027 a politique inchangee
stat = []
d0 = 115.682
for g in (0.019, 0.025, 0.03):
    stab = d0 * g / (1 + g)
    stat.append(dict(base="2025 observe (5,068 %)", g_nominale=g, deficit_stabilisant=stab,
                     ecart_3pct_mdeur=(5.068 - 3) * PT, ecart_stab_mdeur=(5.068 - stab) * PT, ecart_equilibre_mdeur=5.068 * PT))
Y27 = REF["annees"][2027]["Y"]
d27 = REF["annees"][2026]["d"]
for g in (0.025, 0.027):
    stab = d27 * g / (1 + g)
    stat.append(dict(base="2027 a politique inchangee (6,5 %)", g_nominale=g, deficit_stabilisant=stab,
                     ecart_3pct_mdeur=(6.5 - 3) * Y27 / 100, ecart_stab_mdeur=(6.5 - stab) * Y27 / 100,
                     ecart_equilibre_mdeur=6.5 * Y27 / 100))
ecrire("A15_ecarts_statiques.csv", stat)
for s_ in stat:
    log("Ecart statique", s_["base"], "g", s_["g_nominale"], "stab", round(s_["deficit_stabilisant"], 2),
        "3% :", round(s_["ecart_3pct_mdeur"]), "stab :", round(s_["ecart_stab_mdeur"]), "equ :", round(s_["ecart_equilibre_mdeur"]))

# ====================================================================== 3. portefeuilles
def pib13(y):
    return PIB_2025 * 1.02 * 1.027 * 1.025 ** (y - 2027) if y >= 2027 else PIB_2025 * 1.02

MULT13 = {"salaires_publics": (0.5, 0.8, 1.2), "demande_publique": (0.6, 1.0, 1.5),
          "transferts_menages": (0.4, 0.8, 1.2), "pensions": (0.3, 0.5, 0.8), "sante_rembt": (0.3, 0.6, 1.0),
          "PO_entreprises": (0.3, 0.5, 0.8), "subventions": (0.3, 0.5, 0.8), "local_invest": (0.6, 1.0, 1.5),
          "offre": (0.0, 0.0, 0.0), "-": (0.0, 0.0, 0.0)}           # repris de scripts\A13\a13_portefeuille.py
MULT14 = (0.3, 0.5, 1.0)                                            # A14 C-A14-006
EXEC = {"faible": 0.9, "moyen": 0.75, "eleve": 0.5}                 # decote centrale d'A13, appliquee une seule fois

def interp(points, y):
    pts = sorted(points)
    if y <= pts[0][0]:
        return pts[0][1] if y == pts[0][0] else 0.0
    for (a0, v0), (a1, v1) in zip(pts, pts[1:]):
        if a0 <= y <= a1:
            return v0 + (v1 - v0) * (y - a0) / (a1 - a0)
    return pts[-1][1]

def charger_A13():
    f = os.path.join(DON, "A13", "A13_mesures.csv")
    out = []
    with open(f, encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            if r["variante_de"] or r["nature_SEC"] == "regle":
                continue
            sy = int(r["annee_debut"])
            anc = {2027: fl(r["brut_2027"]), 2030: fl(r["brut_2030"]), 2035: fl(r["brut_2035"])}
            if max(anc.values()) == 0:
                continue
            pts = [(2026, 0.0)]
            for a, v in sorted(anc.items()):
                if a < sy:
                    continue
                pts.append((a, v))
            if pts[1][0] > sy:
                pts.insert(1, (sy - 1, 0.0))
            retour = 0.0 if r["deja_net_PO"] == "oui" else fl(r["retour_PO"])
            rep = fl(r["report_APU"])
            series = {}
            for var, pt_key, bonus_key in (("bas", "pass_through_P", None), ("central", "pass_through_C", "bonus_emploi_2035_C"),
                                            ("haut", "pass_through_A", "bonus_emploi_2035_A")):
                pt = fl(r[pt_key])
                b35 = anc[2035]
                bonus35 = fl(r[bonus_key]) if bonus_key else 0.0
                s = {}
                for y in ANNEES:
                    if y < sy:
                        s[y] = 0.0
                        continue
                    yy = min(y, 2035)
                    brut = interp(pts, yy)
                    bon = bonus35 * (brut / b35) if b35 else 0.0
                    val = (brut * (1 - retour) * pt * (1 - rep) + bon) / pib13(yy) * 100.0
                    s[y] = val
                series[var] = s
            out.append(dict(id=r["id"], src="A13", nom=r["mesure"], nature=r["nature_SEC"], groupe=r["assiette_groupe"],
                            env=r["enveloppes"], cat=r["cat_multiplicateur"], mult=MULT13.get(r["cat_multiplicateur"], (0, 0, 0)),
                            risque=r["risque_politique"], series=series, plf=fl(r["part_dans_PLF_PLFSS_2027"])))
    return out

REJETES = {"P-A13-001", "P-A13-003", "P-A13-016", "P-A13-017", "P-A14-001", "P-A14-007", "P-A14-009", "P-A14-010"}
RISQUE14 = {"P-A14-001": "eleve", "P-A14-007": "eleve", "P-A14-009": "eleve", "P-A14-010": "eleve"}

def charger_A14():
    f = os.path.join(DON, "A14", "A14_table_mesures.csv")
    out = []
    with open(f, encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            anc = {2027: fl(r["net_central_2027"]), 2030: fl(r["net_central_2030"]),
                   2035: fl(r["net_central_2035"]), 2050: fl(r["net_central_2050"])}
            c = fl(r["net_plein_central"])
            kb = fl(r["net_plein_bas"]) / c if c else 1.0
            kh = fl(r["net_plein_haut"]) / c if c else 1.0
            pts = [(2026, 0.0)] + sorted(anc.items())
            series = {}
            for var, k in (("bas", kb), ("central", 1.0), ("haut", kh)):
                series[var] = {y: interp(pts, y) * k / PT for y in ANNEES}
            out.append(dict(id=r["id"], src="A14", nom=r["nom"], nature="PO", groupe=r["groupe"], env=r["enveloppes"],
                            cat="PO", mult=MULT14, risque=RISQUE14.get(r["id"], "moyen"), series=series,
                            plf=1.0 if r["statut"].startswith("PLF") else 0.0, statut=r["statut"]))
    return out

M13 = charger_A13()
M14 = charger_A14()
TOUTES = {m["id"]: m for m in M13 + M14}
log("Mesures chargees : A13", len(M13), "A14", len(M14))

# --- matrice des recoupements (regles appliquees)
MATRICE = [
    dict(groupe="Allegements generaux (Cour n° 13, PLFSS 2027)", A13="P-A13-013 (gel, assiette, IEG, forfait social : 7,2 Md€ bruts 2027)",
         A14="P-A14-002 (4,4 bruts) + P-A14-010 (forfait social 0,8) ; P-A14-017 et 018 (2028-2035)",
         nature="memes textes, meme assiette (cotisations employeurs)",
         regle="exclure P-A13-013 ; garder 002 + 010 (mesures par rapport a 2027 a politique inchangee, emplois perdus deduits) ; 017-018 additifs (prolongation)"),
    dict(groupe="Revenu des retraites (Cour n° 1, alternatives)", A13="P-A13-001 (gel 2027) + P-A13-002 (inflation - 0,4, 2028-2032)",
         A14="P-A14-009 (suppression de l'abattement au-dela du plafond) ; P-A14-001 (plafond du PLF, conserve)",
         nature="memes beneficiaires ; variantes exclusives selon la Cour",
         regle="branche 'gel' (001 + 002, sans 009) OU branche 'abattement' (009, sans 001 ni 002)"),
    dict(groupe="Credit d'impot recherche", A13="P-A13-015 (jeunes docteurs, Frascati)", A14="P-A14-019 (calcul au niveau du groupe)",
         nature="meme credit d'impot, parametres differents, interaction inconnue",
         regle="combinaisons strictes : 019 seul ; combinaison large : les deux"),
    dict(groupe="Sante : assures et complementaires", A13="P-A13-007 (tickets moderateurs, franchises : 100 % menages et complementaires)",
         A14="P-A14-003 (surtaxe des complementaires, temporaire)", nature="instruments differents, meme payeur final",
         regle="additifs (pas de double compte de rendement) ; cumul de charge signale"),
    dict(groupe="Indemnites journalieres", A13="P-A13-005 (remplacement, carence)", A14="P-A14-001 (fiscalisation des IJ AT-MP et ALD)",
         nature="instruments differents, memes beneficiaires", regle="additifs ; cumul signale"),
    dict(groupe="Age de depart", A13="P-A13-003 (annulation de la suspension), P-A13-004 (65 ans)", A14="P-A14-028 (hors totaux d'A14)",
         nature="meme mesure (003 = 028)", regle="compte une fois, cote A13"),
    dict(groupe="Mesures du PLF/PLFSS 2027", A13="parts PLF (16,0 Md€ en 2030 si adopte)", A14="P-A14-001 a 006 (9,3 Md€ en 2030)",
         nature="depense d'un cote, prelevements de l'autre ; un seul recoupement (allegements, regle ci-dessus)",
         regle="mesurees contre 2027 a politique inchangee (6,5 %) ; jamais contre 2025"),
    dict(groupe="Perennisations (surtaxe IS, CDHR)", A13="-", A14="P-A14-007, 008",
         nature="deja dans le solde 2025 ; absentes de 2027 a politique inchangee",
         regle="comptees contre 2027 a politique inchangee ; zero contre 2025"),
]
ecrire("A15_matrice_recoupements.csv", MATRICE)

def combinaison(nom, ids_exclus=(), env13="C", env14="C", branche="gel", cir="strict", sans_rejetes=False, ajout=()):
    sel = []
    for m in M13:
        if env13 not in m["env"]:
            continue
        sel.append(m["id"])
    for m in M14:
        if env14 not in (m["env"] or ""):
            continue
        sel.append(m["id"])
    sel = [i for i in sel if i != "P-A13-013"]
    if branche == "gel":
        sel = [i for i in sel if i != "P-A14-009"]
    else:
        sel = [i for i in sel if i not in ("P-A13-001", "P-A13-002")]
        if "P-A14-009" not in sel:
            sel.append("P-A14-009")
    if cir == "strict":
        sel = [i for i in sel if i != "P-A13-015"]
    if sans_rejetes:
        sel = [i for i in sel if i not in REJETES]
    sel = [i for i in sel if i not in ids_exclus] + list(ajout)
    return dict(nom=nom, ids=sel)

COMBIS = [
    combinaison("K1 centrale, branche gel"),
    combinaison("K2 centrale, branche abattement", branche="abattement"),
    combinaison("K3 centrale gel, sans mesures rejetees", sans_rejetes=True),
    combinaison("K4 prudente", env13="P", env14="P"),
    combinaison("K5 ambitieuse large", env13="A", env14="A", cir="large"),
]

def mesures_de(ids, var="central", execution=None, decale=0, mult_var=1):
    mes, mult = {}, {}
    for i in ids:
        m = TOUTES[i]
        s = m["series"][var]
        k = EXEC[m["risque"]] if execution == "decote" else 1.0
        if decale:
            s = {y: (s.get(y - decale, 0.0) if y - decale >= 2026 else 0.0) for y in ANNEES}
        mes[i] = {y: v * k for y, v in s.items()}
        mult[i] = m["mult"][mult_var]
    return mes, mult

def total_statique(ids, y, var="central", execution=None):
    mes, _ = mesures_de(ids, var, execution)
    return sum(s[y] for s in mes.values())

comb_lignes, comb_traj = [], []
for K in COMBIS:
    for execu in (None, "decote"):
        lab = K["nom"] + (" | decote d'execution A13" if execu else " | si adopte")
        res = {}
        for var, mv in (("central", 1), ("bas", 2), ("haut", 0)):
            mes, mult = mesures_de(K["ids"], var, execu, mult_var=mv)
            res[var] = projeter(macro, mes, mult, ref=REF, interets=INT)
        C = res["central"]["annees"]
        l = dict(combinaison=lab, n_mesures=len(K["ids"]))
        for y in (2027, 2030, 2035):
            l[f"statique_{y}_pts"] = total_statique(K["ids"], y, "central", execu)
            l[f"statique_{y}_mdeur_ech2025"] = l[f"statique_{y}_pts"] * PT
        for y in (2027, 2030, 2035, 2050):
            l[f"deficit_{y}"] = C[y]["deficit"]
            l[f"deficit_{y}_bas"] = res["bas"]["annees"][y]["deficit"]
            l[f"deficit_{y}_haut"] = res["haut"]["annees"][y]["deficit"]
            l[f"dette_{y}"] = C[y]["d"]
            l[f"dette_{y}_bas"] = res["bas"]["annees"][y]["d"]
            l[f"dette_{y}_haut"] = res["haut"]["annees"][y]["d"]
        l["gain_ex_post_2030_pts"] = REF["annees"][2030]["deficit"] - C[2030]["deficit"]
        comb_lignes.append(l)
        for y in ANNEES:
            comb_traj.append(dict(combinaison=lab, annee=y, deficit=C[y]["deficit"], dette=C[y]["d"],
                                  deficit_bas=res["bas"]["annees"][y]["deficit"], deficit_haut=res["haut"]["annees"][y]["deficit"],
                                  dette_bas=res["bas"]["annees"][y]["d"], dette_haut=res["haut"]["annees"][y]["d"]))
        log(f"{lab:60s} statique {l['statique_2027_pts']:.2f}/{l['statique_2030_pts']:.2f}/{l['statique_2035_pts']:.2f} pts "
            f"({l['statique_2030_mdeur_ech2025']:.0f} Md€ 2030) ; deficit 2027 {C[2027]['deficit']:.1f} 2030 {C[2030]['deficit']:.1f} "
            f"[{res['bas']['annees'][2030]['deficit']:.1f}-{res['haut']['annees'][2030]['deficit']:.1f}] 2035 {C[2035]['deficit']:.1f} ; "
            f"dette 2030 {C[2030]['d']:.0f} 2035 {C[2035]['d']:.0f} 2050 {C[2050]['d']:.0f}")
ecrire("A15_combinaisons.csv", comb_lignes)
ecrire("A15_combinaisons_trajectoires.csv", comb_traj)
ecrire("A15_combinaisons_composition.csv", [dict(combinaison=K["nom"], mesures=" ".join(K["ids"])) for K in COMBIS])

# double compte evite : somme naive des enveloppes centrales contre K1
naif = sum(total_statique([m["id"] for m in M13 if "C" in m["env"]], y) for y in (2030,)) + \
       sum(total_statique([m["id"] for m in M14 if "C" in (m["env"] or "")], y) for y in (2030,))
log(f"Somme naive des enveloppes centrales (statique, 2030) : {naif:.2f} pts = {naif*PT:.0f} Md€ ; K1 : "
    f"{total_statique(COMBIS[0]['ids'], 2030):.2f} pts = {total_statique(COMBIS[0]['ids'], 2030)*PT:.0f} Md€")
# detail par mesure (central, statique)
det = []
for m in M13 + M14:
    det.append(dict(id=m["id"], source=m["src"], nature=m["nature"], groupe=m["groupe"], enveloppes=m["env"], risque=m["risque"],
                    rejete=("oui" if m["id"] in REJETES else "non"),
                    statique_2027_pts=m["series"]["central"][2027], statique_2030_pts=m["series"]["central"][2030],
                    statique_2035_pts=m["series"]["central"][2035],
                    statique_2030_mdeur_ech2025=m["series"]["central"][2030] * PT,
                    dans_K1=("oui" if m["id"] in COMBIS[0]["ids"] else "non"),
                    dans_K2=("oui" if m["id"] in COMBIS[1]["ids"] else "non"),
                    dans_K3=("oui" if m["id"] in COMBIS[2]["ids"] else "non"),
                    dans_K4=("oui" if m["id"] in COMBIS[3]["ids"] else "non"),
                    dans_K5=("oui" if m["id"] in COMBIS[4]["ids"] else "non")))
ecrire("A15_mesures_harmonisees.csv", det)

# ====================================================================== 4. sensibilites
def macro_var(**kw):
    m = copy.deepcopy(macro)
    for k, v in kw.items():
        if k == "dg":
            for a in ANNEES:
                if a >= 2028:
                    m.gpot[a] += v
        elif k == "dpi":
            for a in ANNEES:
                if a >= 2028:
                    m.defl[a] += v
                    m.ipch[a] += v
        elif k == "rm_lt" and v is not None:
            for a in (2029, 2030, 2031):
                m.rm[a] = m.rm[2028] + (v - m.rm[2028]) * (a - 2028) / 4.0
            m.rm_lt = v
        elif k == "rm_lt" and v is None:
            for a in ANNEES:
                if a > 2028:
                    m.rm[a] = m.rm[2028]
            m.rm_lt = m.rm[2028]
        else:
            setattr(m, k, v)
    return m

K1 = COMBIS[0]["ids"]
VARS = [
    ("centrale", {}, {}),
    ("croissance basse (-0,5 pt/an des 2028)", {"dg": -0.5}, {}),
    ("croissance haute (+0,5 pt/an des 2028)", {"dg": +0.5}, {}),
    ("inflation basse (deflateur 1,0-1,25 %, taux inchanges)", {"dpi": -0.6}, {}),
    ("inflation haute (deflateur 2,35-2,5 %, taux inchanges)", {"dpi": +0.75}, {}),
    ("taux +100 pb des 2027", {"choc_taux": 1.0}, {}),
    ("taux +200 pb des 2027", {"choc_taux": 2.0}, {}),
    ("taux d'emission maintenu a la valeur calee 2028 (4,8 %)", {"rm_lt": None}, {}),
    ("croissance haute et inflation haute (renversement, sect. 14)", {"dg": +0.5, "dpi": +0.75}, {}),
    ("taux d'emission de long terme 2,8 % (= croissance nominale, sect. 14)", {"rm_lt": 2.8}, {}),
    ("multiplicateurs faibles", {}, {"mv": 0}),
    ("multiplicateurs forts", {}, {"mv": 2}),
    ("multiplicateurs forts et persistants", {}, {"mv": 2, "persistant": True}),
    ("emploi bas (PIB -0,5 % en niveau en 2035)", {}, {"emploi": -0.5}),
    ("emploi haut (PIB +1 % en niveau en 2035)", {}, {"emploi": 1.0}),
    ("vieillissement nul", {}, {"vieil": "nul"}),
    ("vieillissement haut", {}, {"vieil": "haut"}),
    ("calendrier : mesures decalees d'un an", {}, {"decale": 1}),
    ("calendrier : mesures decalees de deux ans", {}, {"decale": 2}),
]
sens = []
for nom, mk, opt in VARS:
    m_ = macro_var(**mk)
    if "choc_taux" not in mk:
        m_.choc_taux = 0.0
    R0 = projeter(m_, ref=REF, interets=INT, vieil=opt.get("vieil", "central"), emploi=opt.get("emploi", 0.0))
    mes, mult = mesures_de(K1, "central", None, decale=opt.get("decale", 0), mult_var=opt.get("mv", 1))
    R1 = projeter(m_, mes, mult, ref=REF, interets=INT, vieil=opt.get("vieil", "central"), emploi=opt.get("emploi", 0.0),
                  persistant=opt.get("persistant", False))
    l = dict(variante=nom)
    for lab, R in (("ref", R0), ("K1", R1)):
        for y in (2027, 2030, 2035, 2050):
            l[f"{lab}_deficit_{y}"] = R["annees"][y]["deficit"]
            l[f"{lab}_dette_{y}"] = R["annees"][y]["d"]
    sens.append(l)
    log(f"Sens. {nom:55s} ref def 2030 {R0['annees'][2030]['deficit']:.1f} dette 2035 {R0['annees'][2035]['d']:.0f} 2050 {R0['annees'][2050]['d']:.0f} | "
        f"K1 def 2030 {R1['annees'][2030]['deficit']:.1f} 2035 {R1['annees'][2035]['deficit']:.1f} dette 2035 {R1['annees'][2035]['d']:.0f} 2050 {R1['annees'][2050]['d']:.0f}")
ecrire("A15_sensibilites.csv", sens)
# section 14 : K5 et multiplicateurs nuls / taux bas
m_ = macro_var(rm_lt=2.8)
mes5, mult5 = mesures_de(COMBIS[4]["ids"])
R5 = projeter(m_, mes5, mult5, ref=REF, interets=INT)
log(f"Sect. 14 : K5 avec taux de long terme 2,8 % : deficit 2030 {R5['annees'][2030]['deficit']:.1f} 2035 {R5['annees'][2035]['deficit']:.1f} ; dette 2030 {R5['annees'][2030]['d']:.0f} 2035 {R5['annees'][2035]['d']:.0f} 2040 {R5['annees'][2040]['d']:.0f}")
mult0 = {i: 0.0 for i in mult5}
R50 = projeter(macro, mes5, mult0, ref=REF, interets=INT)
log(f"Sect. 14 : K5 multiplicateurs nuls : deficit 2030 {R50['annees'][2030]['deficit']:.1f} 2035 {R50['annees'][2035]['deficit']:.1f}")

# effort de stabilisation (horizon 2030) sous chaque variante macro
sens_eff = []
for nom, mk, opt in VARS:
    if opt.get("decale") or opt.get("mv") is not None or opt.get("persistant"):
        continue
    m_ = macro_var(**mk)
    if "choc_taux" not in mk:
        m_.choc_taux = 0.0
    s_, R_ = effort("stabilisation", 2030, macro_=m_, vieil=opt.get("vieil", "central"), maintien_jusqua=2035, emploi=opt.get("emploi", 0.0))
    s3, R3 = effort("trois", 2030, macro_=m_, vieil=opt.get("vieil", "central"), maintien_jusqua=2035, emploi=opt.get("emploi", 0.0))
    sens_eff.append(dict(variante=nom, stab_2030_pts=s_[2030], stab_2035_pts=s_[2035], trois_2030_pts=s3[2030], trois_2035_pts=s3[2035]))
    log(f"  effort {nom:55s} stabilisation 2030 {s_[2030]:.2f} (2035 {s_[2035]:.2f}) ; 3 % 2030 {s3[2030]:.2f} (2035 {s3[2035]:.2f})")
for mv, nom in ((0.3, "multiplicateur composite 0,3"), (1.0, "multiplicateur composite 1,0")):
    s_, R_ = effort("stabilisation", 2030, mult={"effort": mv}, maintien_jusqua=2035)
    s3, R3 = effort("trois", 2030, mult={"effort": mv}, maintien_jusqua=2035)
    sens_eff.append(dict(variante=nom, stab_2030_pts=s_[2030], stab_2035_pts=s_[2035], trois_2030_pts=s3[2030], trois_2035_pts=s3[2035]))
    log(f"  effort {nom:55s} stabilisation 2030 {s_[2030]:.2f} (2035 {s_[2035]:.2f}) ; 3 % 2030 {s3[2030]:.2f} (2035 {s3[2035]:.2f})")
ecrire("A15_sensibilites_effort.csv", sens_eff)

# ====================================================================== 5. chocs
CHOCS = {
    "1975": {0: dict(gap=-2.5, disc=1.6), 1: dict(gap=-1.5, disc=0.5), 2: dict(gap=-0.5)},
    "1993": {0: dict(gap=-2.6, disc=0.3), 1: dict(gap=-2.5, disc=0.3), 2: dict(gap=-1.5), 3: dict(gap=-0.5)},
    "2008-2009": {0: dict(gap=-4.5, disc=1.0, sfa=2.5, defl=-1.5), 1: dict(gap=-3.5, disc=0.7, sfa=1.0), 2: dict(gap=-2.5),
                  3: dict(gap=-1.5), 4: dict(gap=-0.5)},
    "2020": {0: dict(gap=-6.5, disc=3.1, sfa=3.0), 1: dict(gap=-2.0, disc=3.3), 2: dict(gap=-0.5, disc=1.3), 3: dict(disc=0.4)},
}
choc_lignes = []
cibles_choc = [("reference", None), ("K1", COMBIS[0]["ids"]), ("K2", COMBIS[1]["ids"]), ("K3", COMBIS[2]["ids"]),
               ("K4", COMBIS[3]["ids"]), ("K5", COMBIS[4]["ids"])]
for cn, ids in cibles_choc:
    mes, mult = mesures_de(ids) if ids else ({}, {})
    base = projeter(macro, mes, mult, ref=REF, interets=INT)
    for sn, prof in CHOCS.items():
        ch = {2028 + k: v for k, v in prof.items()}
        R = projeter(macro, mes, mult, chocs=ch, ref=REF, interets=INT)
        pic = max(R["annees"][y]["deficit"] for y in range(2028, 2033))
        l = dict(trajectoire=cn, choc=sn, deficit_pic_2028_2032=pic,
                 deficit_2028_sans_choc=base["annees"][2028]["deficit"],
                 dette_2030=R["annees"][2030]["d"], dette_2030_sans_choc=base["annees"][2030]["d"],
                 dette_2035=R["annees"][2035]["d"], dette_2035_sans_choc=base["annees"][2035]["d"],
                 dette_2050=R["annees"][2050]["d"], dette_2050_sans_choc=base["annees"][2050]["d"],
                 surcroit_dette_2035_pts=R["annees"][2035]["d"] - base["annees"][2035]["d"])
        choc_lignes.append(l)
        log(f"Choc {sn:9s} sur {cn:9s}: deficit pic {pic:.1f} ; dette 2035 {R['annees'][2035]['d']:.0f} (sans choc {base['annees'][2035]['d']:.0f}, +{l['surcroit_dette_2035_pts']:.0f})")
ecrire("A15_chocs.csv", choc_lignes)

# ====================================================================== 6. credibilite (A08)
DERIVES = {"hors crises": {2027: -0.9, 2028: -1.5, 2029: -2.1}, "toutes annees": {2027: -1.55, 2028: -2.5, 2029: -3.2}}
LONG = {"hors crises": -2.8, "toutes annees": -3.4}
cred = []
for K in COMBIS:
    mes, mult = mesures_de(K["ids"])
    base = projeter(macro, mes, mult, ref=REF, interets=INT)
    for dn, dv in DERIVES.items():
        for plaf in (False, True):
            der = {y: (dv.get(y, LONG[dn]) if y >= 2027 else 0.0) for y in ANNEES}
            if plaf:
                # execution partielle : les mesures ne sont executees qu'a hauteur de (mesures - derive), multiplicateurs compris
                tot = {y: sum(sv[y] for sv in mes.values()) for y in ANNEES}
                k = {y: (max(0.0, 1 + der[y] / tot[y]) if tot[y] > 0 else 1.0) for y in ANNEES}
                mes2 = {i: {y: v * k[y] for y, v in sv.items()} for i, sv in mes.items()}
                R = projeter(macro, mes2, mult, ref=REF, interets=INT)
            else:
                R = projeter(macro, mes, mult, ref=REF, interets=INT, derive_pb=der)
            l = dict(combinaison=K["nom"], derive=dn, plafonnee_aux_mesures=("oui" if plaf else "non"))
            for y in (2027, 2030, 2035):
                l[f"deficit_{y}_programme"] = base["annees"][y]["deficit"]
                l[f"deficit_{y}_derive"] = R["annees"][y]["deficit"]
            l["dette_2035_programme"] = base["annees"][2035]["d"]
            l["dette_2035_derive"] = R["annees"][2035]["d"]
            l["dette_2035_reference"] = REF["annees"][2035]["d"]
            cred.append(l)
            log(f"Credibilite {K['nom']:40s} {dn:13s} plafond={plaf}: deficit 2030 {base['annees'][2030]['deficit']:.1f} -> {R['annees'][2030]['deficit']:.1f} ; dette 2035 {base['annees'][2035]['d']:.0f} -> {R['annees'][2035]['d']:.0f} (ref {REF['annees'][2035]['d']:.0f})")
ecrire("A15_credibilite_A08.csv", cred)

# ====================================================================== 7. deux references (2025 et 2027 PI)
x26, x27 = REF["annees"][2026], REF["annees"][2027]
decomp = dict(deficit_2025=5.068, deficit_2027_PI=x27["deficit"],
              hausse_interets_pts=x27["i_pct"] - 2.197,
              effet_cycle_pts=-SEMI_ELAST * (x27["gap"] - 0.2),
              primaire_structurel_pts=-(REF["pb_struct"][2027] - (-2.871 - SEMI_ELAST * 0.2)))
ecrire("A15_deux_references.csv", [decomp])
log("Passage 2025 -> 2027 PI :", {k: round(v, 2) for k, v in decomp.items()})

with open(os.path.join(SORTIE, "A15_sortie_executer.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))


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
