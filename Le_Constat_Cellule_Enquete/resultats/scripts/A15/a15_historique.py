# -*- coding: utf-8 -*-
"""A15 - contrefactuels historiques bornes (1983, 1995, 2000, 2007, 2012, 2019), fenetre de taux bas
2015-2021 (question 13), contribution des baisses de prelevements par annee de reference (question 9,
T-04), verification des calculs d'Astra. Lancer : python -I a15_historique.py
Donnees : donnees\\A07\\table_france_1974_2025.csv (lecture seule) ; parametres cites dans le code."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a15_modele import lire_table_france, SORTIE, phi

T = lire_table_france()
FRF = 6.55957
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

def ecrire(nom, lignes):
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

SEMI = 0.57

def contrefactuel(nom, effet, m, annees, sens="amelioration"):
    """effet : dict annee -> amelioration directe du solde primaire (% PIB de l'annee).
    Retroaction : perte de PIB = m * sum(d effet * phi) ; le solde perd SEMI * perte.
    Dette : la dette evitee porte le taux apparent observe ; le PIB est reduit de la perte.
    Aucune capitalisation au-dela de la fenetre."""
    dD = 0.0
    prec = 0.0
    incr = {}
    out = []
    for a in annees:
        e = effet.get(a, 0.0)
        incr[a] = e - prec
        prec = e
        perte = m * sum(incr[t] * phi(a - t) for t in incr)
        dpb = e - SEMI * perte
        Y = T[a]["pib_mdeur"]
        i_app = T[a]["taux_apparent_pct"] / 100.0
        int_evites = -dD * i_app                     # interets economises sur la dette evitee fin a-1 (Md€)
        dD = dD * (1 + i_app) - dpb * Y / 100.0
        D_obs = T[a]["dette_mdeur"] if T[a]["dette_mdeur"] else None
        dsolde = dpb + int_evites / Y * 100.0
        ratio_obs = T[a]["dette_pct"]
        ratio_cf = ((D_obs + dD) / (Y * (1 - perte / 100.0)) * 100.0) if D_obs else None
        out.append(dict(contrefactuel=nom, annee=a, multiplicateur=m, effet_direct_pts=e, effet_net_primaire_pts=dpb,
                        interets_evites_pts=int_evites / Y * 100.0, effet_total_solde_pts=dsolde,
                        solde_observe=T[a]["solde_pct"], solde_contrefactuel=T[a]["solde_pct"] + dsolde,
                        dette_evitee_mdeur=-dD, ratio_observe=ratio_obs, ratio_contrefactuel=ratio_cf,
                        ecart_ratio_pts=(ratio_cf - ratio_obs) if ratio_cf else None))
    return out


RES = []
def lancer(nom, effet, annees, ms=(0.3, 0.5, 1.0)):
    blocs = {}
    for m in ms:
        L = contrefactuel(nom, effet, m, annees)
        RES.extend(L)
        blocs[m] = L
    fin = annees[-1]
    c = blocs[ms[1]][-1]
    lo = blocs[ms[-1]][-1]
    hi = blocs[ms[0]][-1]
    ans_eq = [x["annee"] for x in blocs[ms[1]] if x["solde_contrefactuel"] >= 0]
    log(f"{nom}: solde {annees[0]} {blocs[ms[1]][0]['solde_observe']:.2f} -> {blocs[ms[1]][0]['solde_contrefactuel']:.2f} ; "
        f"ecart de ratio en {fin} : {c['ecart_ratio_pts']:.2f} (m={ms[-1]} : {lo['ecart_ratio_pts']:.2f} ; m={ms[0]} : {hi['ecart_ratio_pts']:.2f}) ; "
        f"annees a l'equilibre (m central) : {ans_eq}")
    return blocs

# ---------------------------------------------------------------- 1983 : report de la retraite a 60 ans
# Cout allegue (AN, 24/07/1986, via S01 F-S01-012, niveau E) : 1,3 / 5,5 / 8,9 Md F (1983-1985), 13 Md F (1987).
cout_F = {1983: 1.3, 1984: 5.5, 1985: 8.9, 1986: 11.0, 1987: 13.0}
pct87 = 13.0 / FRF / T[1987]["pib_mdeur"] * 100.0
for subst, lab in ((0.0, "sans substitution"), (0.5, "substitution 50 %"), (0.7, "substitution 70 %")):
    eff = {}
    for a in range(1983, 1993):
        v = cout_F[a] / FRF / T[a]["pib_mdeur"] * 100.0 if a in cout_F else pct87
        eff[a] = v * (1 - subst)
    lancer(f"1983 report de la retraite a 60 ans ({lab})", eff, list(range(1983, 1993)), ms=(0.3, 0.5, 0.8))
log(f"  cout 1987 = {pct87:.2f} % du PIB")

# ---------------------------------------------------------------- 1995 : maintien du volet regimes speciaux (plan Juppe)
# Aucun chiffrage sur piece (A09 : abandon [M], cout [X]). Parametres [M]/[H] : masse concernee 1,0-2,0 % du PIB,
# economie atteignant 3 / 5 / 8 % de cette masse en 2003, rattrapee par les reformes de 2003 et 2008 (effet nul apres 2008).
for masse, part, lab in ((1.0, 0.03, "bas"), (1.5, 0.05, "central"), (2.0, 0.08, "haut")):
    eff = {}
    for a in range(1996, 2009):
        if a <= 2003:
            eff[a] = masse * part * (a - 1995) / 8.0
        else:
            eff[a] = masse * part * max(0.0, (2008 - a) / 5.0)
    lancer(f"1995 regimes speciaux maintenus ({lab}, [M])", eff, list(range(1996, 2009)), ms=(0.3, 0.5, 0.8))

# ---------------------------------------------------------------- 2000 : cagnotte (A02 C-A02-003, A04, A03)
# 2000 : collectif 1 non reaffecte 0,50 pt (A) ; + surplus du 2e collectif au solde 0,73 pt (B) ;
# 2001-2007 : baisses permanentes de 2000 evitees, 0,51 pt (A02).
for lab, e0 in (("A", 0.50), ("B", 0.73)):
    eff = {2000: e0}
    for a in range(2001, 2008):
        eff[a] = 0.51
    lancer(f"2000 cagnotte non reaffectee (scenario {lab})", eff, list(range(2000, 2008)))
# borne haute : aucune baisse d'impots d'Etat 2000-2002 (1,8 pt, Carrez via A03), baisses de 2003-2007 maintenues
eff = {2000: 0.6, 2001: 1.2}
for a in range(2002, 2008):
    eff[a] = 1.8
lancer("2000-2002 aucune baisse d'impots d'Etat (borne haute, Carrez)", eff, list(range(2000, 2008)))

# ---------------------------------------------------------------- 2007 : equilibre possible ? (A03 C-A03-005 ; A04)
# (a) aucune baisse d'impots d'Etat 2000-2007 : 1,8 pt (2000-2002) + 1,7 pt (2003-2007) ; Carrez : 53,5-65,6 Md€ en 2007
eff = {}
for a in range(2000, 2010):
    eff[a] = min(a - 1999, 3) * 0.6 + max(0, min(a, 2007) - 2002) * 0.34
lancer("2000-2007 aucune baisse d'impots d'Etat (Carrez)", eff, list(range(2000, 2010)))
# (b) loi TEPA non votee (aout 2007) : 1 Md€ en 2007 ; 12,9 Md€/an en regime de croisiere des 2008-2009 (Senat via A04) ;
# volets abroges en 2011-2012 : effet ramene a moitie a partir de 2012 [H]
eff = {2007: 1.0 / T[2007]["pib_mdeur"] * 100, 2008: 0.5 * 12.9 / T[2008]["pib_mdeur"] * 100}
for a in range(2009, 2013):
    v = 12.9 / T[a]["pib_mdeur"] * 100
    eff[a] = v if a < 2012 else v * 0.5
lancer("2007 loi TEPA non votee", eff, list(range(2007, 2013)))

# ---------------------------------------------------------------- 2012 : CICE non cree (decision de novembre 2012)
# cout : ≈ 18 Md€ en 2016 (France Strategie 2020, via A04 F-A04-030) ; taux 4 % (2013), 6 % (2014-2016), 7 % (2017), 6 % (2018) ;
# enregistre au fait generateur en base 2020 (A03). Retroaction : ≈ 100 000 emplois (FS 2020) -> 2,5 Md€ de recettes [H : 25 k€/emploi].
# Part non gagee : 50 a 100 % [H] (hausse de TVA de 2014 et economies annoncees non chiffrees sur piece : [M]).
taux = {2013: 4, 2014: 6, 2015: 6, 2016: 6, 2017: 7, 2018: 6}
for gage, lab in ((0.5, "moitie non gagee"), (1.0, "entierement non gage")):
    eff = {}
    for a in range(2013, 2019):
        cout = 18.0 * taux[a] / 6.0 * T[a]["pib_mdeur"] / T[2016]["pib_mdeur"]
        emplois = 2.5 * min(1.0, (a - 2012) / 4.0)
        eff[a] = (cout - emplois) * gage / T[a]["pib_mdeur"] * 100
    lancer(f"2012 CICE non cree ({lab})", eff, list(range(2013, 2019)))

# ---------------------------------------------------------------- 2019 : mesures d'urgence de decembre 2018 non adoptees
# 10,3 Md€ bruts, 6,4 Md€ nets en 2019 (Senat n° 232, via A09) ; maintien suppose en % du PIB jusqu'en 2025 [H]
v19 = 6.4 / T[2019]["pib_mdeur"] * 100
eff = {a: v19 for a in range(2019, 2026)}
lancer("2019 mesures d'urgence (MUES) non adoptees", eff, list(range(2019, 2026)), ms=(0.3, 0.5, 0.8))
eff = {2019: v19}
lancer("2019 MUES non adoptees, effet limite a 2019", eff, [2019], ms=(0.3, 0.5, 0.8))

ecrire("A15_contrefactuels.csv", RES)

# ---------------------------------------------------------------- question 13 : fenetre de taux bas 2015-2021
lig = []
cum_eco, cum_pb = 0.0, 0.0
a14 = T[2014]["taux_apparent_pct"]
pb14 = T[2014]["solde_primaire_pct"]
for a in range(2015, 2022):
    r = T[a]
    Dm1 = T[a - 1]["dette_mdeur"]
    eco = (a14 - r["taux_apparent_pct"]) / 100.0 * Dm1
    dpb = (r["solde_primaire_pct"] - pb14) * r["pib_mdeur"] / 100.0
    g = r["croiss_nominale_pct"] / 100.0
    i = r["taux_apparent_pct"] / 100.0
    pb_stab = T[a - 1]["dette_pct"] * (i - g) / (1 + g)   # excedent primaire stabilisant (> 0) ou deficit admissible (< 0)
    cum_eco += eco
    cum_pb += dpb
    lig.append(dict(annee=a, economie_interets_vs_taux_2014_mdeur=eco, variation_solde_primaire_vs_2014_mdeur=dpb,
                    solde_primaire_pct=r["solde_primaire_pct"], solde_primaire_stabilisant_pct=pb_stab,
                    ecart_au_stabilisant_pts=r["solde_primaire_pct"] - pb_stab,
                    cumul_economies=cum_eco, cumul_variation_primaire=cum_pb))
    log(f"Taux bas {a}: economie {eco:.1f} Md€ ; primaire vs 2014 {dpb:+.1f} Md€ ; primaire {r['solde_primaire_pct']:.2f} vs stabilisant {pb_stab:.2f}")
ecrire("A15_fenetre_taux_bas.csv", lig)
s1519 = [x for x in lig if x["annee"] <= 2019]
log(f"2015-2019 : economies cumulees {sum(x['economie_interets_vs_taux_2014_mdeur'] for x in s1519):.0f} Md€ ; "
    f"amelioration cumulee du primaire {sum(x['variation_solde_primaire_vs_2014_mdeur'] for x in s1519):.0f} Md€ ; "
    f"annees au-dessus du stabilisant : {[x['annee'] for x in s1519 if x['ecart_au_stabilisant_pts'] >= 0]}")
# contrefactuel norme : primaire maintenu chaque annee au niveau stabilisant (2015-2019)
dD = 0.0
for x in s1519:
    a = x["annee"]
    manque = max(0.0, -x["ecart_au_stabilisant_pts"]) * T[a]["pib_mdeur"] / 100.0
    dD = dD * (1 + T[a]["taux_apparent_pct"] / 100.0) + manque
log(f"  dette 2019 si le primaire avait atteint le niveau stabilisant chaque annee : -{dD:.0f} Md€ = -{dD / T[2019]['pib_mdeur'] * 100:.1f} pts (statique)")
# comparaison avec l'Allemagne (S02, F-S02-012 : 47 Md€ en 2016 = 1,5 % du PIB ; 240 Md€ cumules depuis 2008, Bundesbank)
a08 = T[2008]["taux_apparent_pct"]
cum08 = 0.0
for a in range(2009, 2017):
    eco = (a08 - T[a]["taux_apparent_pct"]) / 100.0 * T[a - 1]["dette_mdeur"]
    cum08 += eco
    if a == 2016:
        log(f"France, economie d'interets par rapport au taux apparent de 2008 : {eco:.0f} Md€ en 2016 ({eco / T[2016]['pib_mdeur'] * 100:.1f} % du PIB) ; cumul 2009-2016 {cum08:.0f} Md€")

# ---------------------------------------------------------------- question 9 / T-04 : baisses de prelevements par reference
# Mesures nouvelles de PO cumulees (pts de PIB), A04 C-A04-004 : Fipeco [S] avant 2018, Insee [C] apres.
MESURES = [("1999-2002", -2.7, 1999, 2002), ("2003-2006", 0.7, 2003, 2006), ("2007-2009", -2.1, 2007, 2009),
           ("2010-2014", 3.9, 2010, 2014), ("2015-2017", -0.2, 2015, 2017), ("2018-2023", -2.29, 2018, 2023),
           ("2024-2025", 0.89, 2024, 2025)]
t04 = []
for ref in (1999, 2006, 2017):
    tot, detail = 0.0, []
    for nom, v, a0, a1 in MESURES:
        if a1 <= ref:
            continue
        frac = 1.0 if a0 > ref else (a1 - ref) / (a1 - a0 + 1)
        tot += v * frac
        detail.append(f"{nom} x {frac:.2f}")
    po_ref = {1999: 44.3, 2006: None, 2017: 45.3}[ref]
    t04.append(dict(reference=ref, mesures_cumulees_pts=tot, contribution_au_deficit_2025_pts=-tot,
                    contribution_mdeur_2025=-tot * 29.91, part_du_deficit_2025=-tot / 5.068, periodes=" ; ".join(detail),
                    provenance="Fipeco [S] avant 2018, Insee [C] 2018-2025 (A04)"))
    log(f"T-04 reference {ref}: mesures cumulees {tot:+.2f} pt -> contribution au deficit 2025 {-tot:+.2f} pt ({-tot*29.91:+.0f} Md€, {-tot/5.068*100:.0f} % du deficit) [{'; '.join(detail)}]")
ecrire("A15_T04_baisses_prelevements.csv", t04)

# ---------------------------------------------------------------- verification d'Astra
ast = []
d, Y = 115.7, 2991.056
for g in (0.02, 0.03, 0.04):
    stab = d * g / (1 + g)
    ast.append(dict(calcul="deficit stabilisant", g=g, resultat_pct=stab, ecart_mdeur_depuis_5_1=(5.1 - stab) * Y / 100))
ast.append(dict(calcul="ramener a 3 %", resultat_mdeur=(5.1 - 3) * Y / 100, avec_5_068=(5.068 - 3) * Y / 100))
ast.append(dict(calcul="equilibre", resultat_mdeur=151.592))
for m in (0.5, 1.5, 2.0):
    gain = 10 - 0.5 * m * 10
    dY = -m * 10
    dratio = ((3460.1 - gain) / (Y + dY) - 3460.1 / Y) * 100
    ast.append(dict(calcul="illustration multiplicateur (10 Md€, retour 0,5)", multiplicateur=m, gain_solde_mdeur=gain,
                    variation_ratio_pts_1re_annee=dratio))
# seuil de multiplicateur au-dela duquel le ratio monte la 1re annee : 10(1-0,5m)/Y = d*m*10/Y
mstar = 1 / (0.5 + 3460.1 / Y)
ast.append(dict(calcul="seuil de multiplicateur (ratio inchange la 1re annee)", resultat=mstar))
# scenarios de capitalisation (Astra, hypotheses reproductibles) B et C
for rdt in (0.0, 0.02, 0.04):
    fonds, dette = 0.0, 0.0
    for t in range(1, 28):
        vers = min(t / 10, 1) * 0.50
        rente = max(t - 15, 0) * 0.02
        fonds = fonds * (1 + rdt) / 1.015 + vers - rente
        dette = dette * 1.01 / 1.015 + vers - rente
    ast.append(dict(calcul="capitalisation Astra B/C", rendement_reel=rdt, portefeuille_2026_pts=fonds, dette_transition_B_pts=dette,
                    besoin_final_pts=0.50 - 0.24))
ecrire("A15_verification_Astra.csv", ast)
for x in ast:
    log("Astra", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in x.items()})

with open(os.path.join(SORTIE, "A15_sortie_historique.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
