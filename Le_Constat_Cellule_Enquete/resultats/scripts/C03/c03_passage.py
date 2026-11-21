# -*- coding: utf-8 -*-
"""C03 - table de passage entre l'effort de stabilisation d'A15 (5,168 pts) et celui de Codex (3,078 pts).

Moteur unique a interrupteurs. Avec les reglages A15 il reproduit a l'identique le calcul de
scripts\\A15\\a15_executer.py (lignes 39-136 : reference A en mode cible, rampe 2027-2030, bissection,
critere 'stabilisation' de la fonction atteint) ; avec les reglages Codex il reproduit scenarios.py
(fonction run et calibrate, objectif 'ratio stable en 2030'). Chaque interrupteur change UN parametre.
Les constantes et fonctions d'A15 sont importees de la COPIE scripts\\C03\\a15_modele.py (lecture seule).

Lancer : python -I -B c03_passage.py     Sorties : donnees\\C03\\C03_*.csv et C03_sortie_passage.txt
"""
import os, sys, csv, itertools, math
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import a15_modele as M15   # copie C03 (SORTIE redirigee) ; seules des lectures sont faites ici

OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\C03"
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

ANS = list(range(2026, 2031))

# ------------------------------------------------------------------ reglages
A15 = dict(def2027=6.5,        # deficit 2027 de reference : RESF « a politique inchangee » (A15) / Commission budget compris (Codex)
           g2027="A15",        # croissance reelle 2027 de la reference : 1,1 % sans mesures (A15) / 0,6 % Commission (Codex)
           cycle="A15",        # ecart de production de reference qui se referme d'ici 2030 (A15) / fige (Codex : aucun cycle)
           vieil="A15",        # cout du vieillissement : COR + Ageing Report (A15) / 0,08 pt par an (Codex)
           croiss="A15",       # croissance potentielle apres 2028 : 1,0 % (A15) / 1,2 % (Codex)
           defl="A15",         # deflateur : 1,9 / 1,6 / 1,75 (A15) / 2,0 (Codex)
           rm="A15",           # taux a l'emission apres 2027 : 4,8 % cale en 2028 puis convergence vers 4 % en 2032 (A15) / 4 % des 2028 (Codex)
           f=0.10,             # part de l'encours refinancee chaque annee : 0,10 (A15) / 1/8,5 (Codex)
           s=0.09,             # part indexee : 9 % (A15) / 0 (Codex)
           forme="A15",        # emprunt net de l'annee : demi-annee d'interets et entree au taux de marche (A15) / au coupon moyen, sans interet l'annee meme (Codex)
           mult=0.6,           # multiplicateur de l'effort : 0,6 (A15) / 0,8 (Codex)
           profil="phi",       # estompement : plein 2 ans, 0,5 de la 3e a la 5e, 0,2 ensuite (A15) / geometrique 0,5 par an (Codex)
           semi=0.57,          # semi-elasticite du solde : 0,57 (A15) / 0,50 (Codex)
           cible="tendance",   # stabiliser = deficit <= dette(t-1) x g tendanciel/(1+g) (A15) / ratio 2030 <= ratio 2029, PIB effectif (Codex)
           unites="effectif",  # reference et effort en % du PIB effectif (A15) / du PIB de reference (Codex)
           dette2026="A15",    # dette 2026 issue du modele (A15) / 119,2 % impose (Codex, Commission)
           sfa=0.0,            # ajustements stocks-flux : 0 dans les deux modeles
           budget=None)        # variante : budget 2027 modelise comme mesure (montant, multiplicateur, part expirante en 2028)
CODEX = dict(A15, def2027=5.4, g2027="codex", cycle="codex", vieil="codex", croiss="codex", defl="codex",
             rm="codex", f=1 / 8.5, s=0.0, forme="codex", mult=0.8, profil="geo", semi=0.50,
             cible="effective", unites="tendance", dette2026="codex")

# ------------------------------------------------------------------ chemins macro
GAP_A15 = {2026: -0.6, 2027: -0.7, 2028: -0.4, 2029: -0.2, 2030: 0.0}

def chemins(p):
    gapref = dict(GAP_A15)
    if p["cycle"] == "codex":
        for t in ANS:
            if t >= 2027:
                gapref[t] = gapref[2027]
    gpot = {t: (1.2 if t <= 2028 else 1.0) for t in ANS}
    if p["croiss"] == "codex":
        for t in ANS:
            if t >= 2028:
                gpot[t] = 1.2
    if p["g2027"] == "codex":
        # croissance reelle effective 2027 de la reference = 0,6 % (Commission), cycle inchange
        gpot[2027] = 100 * (1.006 * (1 + gapref[2026] / 100) / (1 + gapref[2027] / 100) - 1)
    defl = {2026: 1.8, 2027: 1.9, 2028: 1.6, 2029: 1.6, 2030: 1.6}
    if p["defl"] == "codex":
        for t in ANS:
            if t >= 2027:
                defl[t] = 2.0
    ipch = {2026: 2.6, 2027: 2.9, 2028: 2.1, 2029: 1.9, 2030: 1.9}
    return gapref, gpot, defl, ipch

def vieillissement(t, p):
    if p["vieil"] == "codex":
        return 0.08 * (t - 2027)
    return M15.vieillissement(t, "central")

def profil(age, p):
    if age < 0:
        return 0.0
    if p["profil"] == "geo":
        return 0.5 ** age
    return M15.phi(age)

_RM = {}
def taux_marche(p):
    k = (p["f"], p["s"], p["rm"])
    if k not in _RM:
        _RM[k] = _taux_marche(p)
    return _RM[k]

def _taux_marche(p):
    """rm 2026-2028 cales par la fonction d'A15 (copie) sur la Commission, avec f et s du reglage."""
    macro = M15.Macro()
    cal = M15.calibrer_rm(M15.Interets(f=p["f"], s=p["s"]), macro)
    rm = dict(cal)
    if p["rm"] == "A15":
        for a in (2029, 2030):
            rm[a] = cal[2028] + (4.0 - cal[2028]) * (a - 2028) / 4.0
    else:
        for a in (2028, 2029, 2030):
            rm[a] = 4.0
    return rm

# ------------------------------------------------------------------ projection
def projeter(p, X, S=None, fin=2030):
    """X : effort en points (rampe X/4 ... X de 2027 a 2030). S : soldes primaires structurels
    2026-2027 de la reference ; si None, mode cible (deficits 2026 = 5,5 et 2027 = def2027 imposes)."""
    gapref, gpot, defl, ipch = chemins(p)
    rm = taux_marche(p)
    f, s, rr = p["f"], p["s"], 0.5
    semi = p["semi"]
    eff = {t: (0.0 if t < 2027 else X * min(1.0, (t - 2026) / 4.0)) for t in ANS}
    cats = [(eff, p["mult"])]
    if p["budget"] and S is not None:   # le budget n'entre pas dans le calcul de la reference (mode cible)
        mont, mb, expire = p["budget"]
        bud = {t: (0.0 if t < 2027 else (mont if t == 2027 else mont - expire)) for t in ANS}
        cats.append((bud, mb))
    cible_mode = S is None
    S = {} if S is None else dict(S)
    D_prev, a_prev = M15.DETTE_2025, M15.TAUX_APP_2025
    P_prev = M15.PIB_2025 / (1 + 0.2 / 100.0)
    defl_idx = 1.0
    c_prev = None
    res = {}
    for t in ANS:
        if t > fin:
            break
        perte, Mtot = 0.0, 0.0
        for serie, m in cats:
            prec = 0.0
            for tau in range(2026, t + 1):
                v = serie.get(tau, 0.0)
                perte += m * (v - prec) * profil(t - tau, p)
                prec = v
            Mtot += serie.get(t, 0.0)
        P = P_prev * (1 + gpot[t] / 100.0)
        defl_idx *= (1 + defl[t] / 100.0)
        Yref = P * (1 + gapref[t] / 100.0) * defl_idx
        gap = gapref[t] - perte
        Y = Yref * (1 - perte / 100.0) if p["unites"] == "tendance" else P * (1 + gap / 100.0) * defl_idx
        pi = ipch[t]
        sfa = p["sfa"] * Y / 100.0
        # taux de l'encours de l'annee
        if p["forme"] == "codex" and t == 2027:
            # Codex : coupon 2027 tel que la charge 2027 vaille 3,0 % du PIB de reference
            base_rate = (3.0 * Yref / D_prev - s * (rr + pi)) / (1 - s)
        else:
            base_rate = (1 - f) * a_prev + f * rm[t]
        A = (1 - s) * D_prev * base_rate / 100.0 + s * D_prev * (rr + pi) / 100.0
        h = 0.5 * rm[t] / 100.0 if p["forme"] == "A15" else 0.0
        if cible_mode and t in (2026, 2027):
            dc = 5.5 if t == 2026 else p["def2027"]
            N = dc * Y / 100.0 + sfa
            I = A + h * N
            pb_eur = I - dc * Y / 100.0
            if p["unites"] == "tendance":
                S[t] = pb_eur / Yref * 100.0 - semi * gapref[t]
            else:
                S[t] = pb_eur / Y * 100.0 - semi * gap
        else:
            base = S[t] if t <= 2027 else S[2027] - vieillissement(t, p)
            if p["unites"] == "tendance":
                pb_eur = Yref * (base + semi * gapref[t] + Mtot) / 100.0 + semi * (Y - Yref)
            else:
                pb_eur = (base + semi * gap + Mtot) * Y / 100.0
            I = (A + h * (-pb_eur + sfa)) / (1 - h)
            N = I - pb_eur + sfa
        D = D_prev + N
        if t == 2026 and p["dette2026"] == "codex":
            D = 1.192 * Y          # Commission : 119,2 % en 2026
        if p["forme"] == "A15":
            a_new = ((1 - f) * a_prev * D_prev + f * rm[t] * D_prev + rm[t] * N) / D
        else:
            a_new = base_rate
        res[t] = dict(Y=Y, Yref=Yref, gap=gap, pb=pb_eur / Y * 100.0, I=I, i_pct=I / Y * 100.0,
                      deficit=(I - pb_eur) / Y * 100.0, D=D, d=D / Y * 100.0, rm=rm[t], M=Mtot)
        D_prev, a_prev, P_prev = D, a_new, P
    return res, S

def atteint(p, R):
    gapref, gpot, defl, ipch = chemins(p)
    if p["cible"] == "effective":
        return R[2030]["d"] <= R[2029]["d"]
    gn = (1 + gpot[2030] / 100.0) * (1 + defl[2030] / 100.0) - 1
    return R[2030]["deficit"] <= R[2029]["d"] * gn / (1 + gn)

def effort(p):
    _, S = projeter(p, 0.0, None)
    lo, hi = -5.0, 25.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if atteint(p, projeter(p, mid, S)[0]):
            hi = mid
        else:
            lo = mid
    X = hi
    R, _ = projeter(p, X, S)
    Rr, _ = projeter(p, 0.0, S)
    return X, R, Rr

def resume(nom, p):
    X, R, Rr = effort(p)
    gapref, gpot, defl, ipch = chemins(p)
    gn = (1 + gpot[2030] / 100.0) * (1 + defl[2030] / 100.0) - 1
    return dict(etape=nom, effort_2030_pts=X, deficit_ref_2027=Rr[2027]["deficit"], deficit_ref_2030=Rr[2030]["deficit"],
                interets_ref_2030=Rr[2030]["i_pct"], dette_ref_2030=Rr[2030]["d"],
                deficit_vise_2030=R[2030]["deficit"], dette_2029=R[2029]["d"], dette_2030=R[2030]["d"],
                croissance_nom_tendancielle_2030=100 * gn,
                croissance_nom_effective_2030=100 * (R[2030]["Y"] / R[2029]["Y"] - 1),
                interets_2030=R[2030]["i_pct"])

def ecrire(nom, lignes):
    cols = []
    for l in lignes:
        for k in l:
            if k not in cols:
                cols.append(k)
    with open(os.path.join(OUT, nom), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=cols, delimiter=";")
        w.writeheader()
        for l in lignes:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in l.items()})

# ------------------------------------------------------------------ 0. controles de reproduction
r15 = resume("A15 (reproduction)", A15)
rcx = resume("Codex (reproduction)", CODEX)
log(f"Reproduction A15 : {r15['effort_2030_pts']:.4f} (attendu 5,168) ; Codex : {rcx['effort_2030_pts']:.4f} (attendu 3,078)")
Rr15, _ = projeter(A15, 0.0, projeter(A15, 0.0, None)[1])
log("  ref A15 2026-2030 deficit :", [round(Rr15[t]["deficit"], 3) for t in ANS], "dette :", [round(Rr15[t]["d"], 2) for t in ANS])
Rrcx, _ = projeter(CODEX, 0.0, projeter(CODEX, 0.0, None)[1])
log("  ref Codex 2027-2030 deficit :", [round(Rrcx[t]["deficit"], 3) for t in ANS[1:]], "dette :", [round(Rrcx[t]["d"], 2) for t in ANS[1:]],
    "interets :", [round(Rrcx[t]["i_pct"], 3) for t in ANS[1:]])

# ------------------------------------------------------------------ 1. etapes (un parametre a la fois)
ETAPES = [  # (cle(s), libelle, groupe)
    (("def2027",), "Reference 2027 : deficit 6,5 % (sans mesures du budget) -> 5,4 % (Commission, budget compris)", "1 reference 2027"),
    (("g2027",), "Croissance reelle 2027 de la reference : 1,1 % (sans mesures) -> 0,6 % (Commission)", "1 reference 2027"),
    (("rm",), "Taux a l'emission : 4,8 % en 2028 convergeant vers 4 % en 2032 -> 4 % des 2028", "2 interets"),
    (("f",), "Part refinancee par an : 0,10 -> 1/8,5", "2 interets"),
    (("s",), "Part indexee de la dette : 9 % -> 0", "2 interets"),
    (("forme",), "Emprunt net de l'annee : au taux de marche (demi-annee) -> au coupon moyen", "2 interets"),
    (("croiss",), "Croissance potentielle 2029-2030 : 1,0 % -> 1,2 %", "3 croissance et deflateur"),
    (("defl",), "Deflateur 2027-2030 : 1,9 / 1,6 -> 2,0 %", "3 croissance et deflateur"),
    (("cycle",), "Ecart de production de reference : se referme de -0,7 a 0 en 2030 -> fige", "4 cycle de reference"),
    (("mult",), "Multiplicateur : 0,6 -> 0,8", "5 multiplicateur et retroaction"),
    (("profil",), "Estompement : profil A13 (1 ; 1 ; 0,5 x3 ; 0,2) -> geometrique 0,5", "5 multiplicateur et retroaction"),
    (("semi",), "Semi-elasticite du solde : 0,57 -> 0,50", "5 multiplicateur et retroaction"),
    (("cible",), "Stabiliser : deficit <= seuil a croissance tendancielle -> ratio 2030 <= ratio 2029 (PIB effectif)", "6 definition de stabiliser"),
    (("sfa",), "Ajustements stocks-flux : 0 -> 0", "7 ajustements stocks-flux"),
    (("vieil",), "Vieillissement : COR + Ageing Report (~0,02 pt/an) -> 0,08 pt/an", "8 vieillissement"),
    (("unites",), "Unites : % du PIB effectif -> % du PIB de reference", "9 unites et point de depart"),
    (("dette2026",), "Dette 2026 : issue du modele -> 119,2 % (Commission)", "9 unites et point de depart"),
]

def marche(depart, arrivee, etapes):
    p = dict(depart)
    lignes = [resume("depart", p)]
    for cles, lib, grp in etapes:
        for k in cles:
            p[k] = arrivee[k]
        r = resume(lib, p)
        r["groupe"] = grp
        r["contribution_pts"] = r["effort_2030_pts"] - lignes[-1]["effort_2030_pts"]
        lignes.append(r)
    return lignes

log("\n=== Marche aller : modele A15, un parametre a la fois vers les valeurs de Codex")
aller = marche(A15, CODEX, ETAPES)
for l in aller:
    log(f"  {l['effort_2030_pts']:7.3f}  {l.get('contribution_pts', 0):+7.3f}  ref30 {l['deficit_ref_2030']:5.2f} vise30 {l['deficit_vise_2030']:5.2f}  {l['etape']}")
ecrire("C03_marche_aller.csv", aller)

log("\n=== Marche retour : modele Codex, un parametre a la fois vers les valeurs d'A15 (meme ordre de liste, donc autre chemin)")
retour = marche(CODEX, A15, ETAPES)
for l in retour:
    log(f"  {l['effort_2030_pts']:7.3f}  {l.get('contribution_pts', 0):+7.3f}  {l['etape']}")
ecrire("C03_marche_retour.csv", retour)

# ------------------------------------------------------------------ 2. Shapley par groupe (independant de l'ordre)
GROUPES = {}
for cles, lib, grp in ETAPES:
    GROUPES.setdefault(grp, []).extend(cles)
noms = list(GROUPES)
cache = {}
def val(coal):
    key = frozenset(coal)
    if key not in cache:
        p = dict(A15)
        for g in coal:
            for k in GROUPES[g]:
                p[k] = CODEX[k]
        cache[key] = effort(p)[0]
    return cache[key]
n = len(noms)
shap = {}
for g in noms:
    autres = [x for x in noms if x != g]
    tot = 0.0
    for r in range(n):
        for coal in itertools.combinations(autres, r):
            w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
            tot += w * (val(set(coal) | {g}) - val(set(coal)))
    shap[g] = tot
log("\n=== Contributions de Shapley par groupe (A15 -> Codex), en points d'effort")
lig = []
for g in noms:
    fw = sum(l["contribution_pts"] for l in aller[1:] if l["groupe"] == g)
    bw = -sum(l["contribution_pts"] for l in retour[1:] if l["groupe"] == g)
    seul = val({g}) - val(set())
    dernier = val(set(noms)) - val(set(noms) - {g})
    lig.append(dict(groupe=g, shapley_pts=shap[g], marche_aller_pts=fw, marche_retour_pts=bw,
                    effet_seul_depuis_A15=seul, effet_en_dernier_vers_Codex=dernier))
    log(f"  {g:34s} Shapley {shap[g]:+.3f}  aller {fw:+.3f}  retour {bw:+.3f}  seul {seul:+.3f}  dernier {dernier:+.3f}")
tot = sum(shap.values())
log(f"  somme {tot:+.4f} ; ecart a expliquer {rcx['effort_2030_pts'] - r15['effort_2030_pts']:+.4f}")
ecrire("C03_shapley_groupes.csv", lig)

# ------------------------------------------------------------------ 3. budget 2027 modelise comme mesure (logique A15)
log("\n=== Variante : budget 2027 compte comme mesure dans le modele A15 (reference 6,5 %), effort mesure au-dela du budget")
var = []
for mont, mb, exp_, lib in ((1.4, 0.6, 0.0, "43 Md€ = 1,4 pt, multiplicateur A15 0,6, permanent"),
                            (1.4, 0.357, 0.0, "1,4 pt, multiplicateur 0,36 (effet de 0,5 pt sur la croissance, administration via HCFP § 36)"),
                            (1.4, 0.6, 0.3, "1,4 pt, mult 0,6, dont 0,3 pt expirant en 2028 [H : montant non chiffre par la Commission]"),
                            (1.1, 0.6, 0.0, "1,1 pt (6,5 - 5,4), multiplicateur 0,6, permanent")):
    p = dict(A15, budget=(mont, mb, exp_))
    X, R, Rr = effort(p)
    var.append(dict(variante=lib, effort_au_dela_du_budget_pts=X, effort_total_2030_pts=X + mont - exp_,
                    deficit_2027_avec_budget=Rr[2027]["deficit"], deficit_2028_avec_budget=Rr[2028]["deficit"],
                    deficit_2030_avec_budget=Rr[2030]["deficit"], dette_2028=Rr[2028]["d"]))
    log(f"  {lib:95s} effort au-dela {X:.3f} ; total {X + mont - exp_:.3f} ; deficit ref 2027 {Rr[2027]['deficit']:.2f} 2028 {Rr[2028]['deficit']:.2f} 2030 {Rr[2030]['deficit']:.2f}")
ecrire("C03_budget_comme_mesure.csv", var)

# ------------------------------------------------------------------ 4. controles contre la Commission (2027-2028)
log("\n=== References contre la Commission (2027 / 2028 : deficit 5,4 / 5,7 ; interets 3,0 / 3,3 ; dette 122,1 / 123,2)")
for nom, p in (("A15 reference A (6,5)", A15), ("A15 avec reference 5,4", dict(A15, def2027=5.4, g2027="codex")), ("Codex", CODEX)):
    Rr, _ = projeter(p, 0.0, projeter(p, 0.0, None)[1])
    log(f"  {nom:28s} 2027 def {Rr[2027]['deficit']:.2f} int {Rr[2027]['i_pct']:.2f} dette {Rr[2027]['d']:.1f} | 2028 def {Rr[2028]['deficit']:.2f} int {Rr[2028]['i_pct']:.2f} dette {Rr[2028]['d']:.1f} | 2030 def {Rr[2030]['deficit']:.2f} int {Rr[2030]['i_pct']:.2f} dette {Rr[2030]['d']:.1f}")

# ------------------------------------------------------------------ 5. dans le run de stabilisation d'A15, le ratio baisse-t-il en 2030 ?
X, R, Rr = effort(A15)
log(f"\nRun de stabilisation A15 : dette 2029 {R[2029]['d']:.3f} -> 2030 {R[2030]['d']:.3f} ; deficit 2030 {R[2030]['deficit']:.3f}")
X, R, Rr = effort(CODEX)
log(f"Run de stabilisation Codex : dette 2029 {R[2029]['d']:.3f} -> 2030 {R[2030]['d']:.3f} ; deficit 2030 {R[2030]['deficit']:.3f}")

# ------------------------------------------------------------------ 6. chiffres harmonises (memes questions, hypotheses de l'une ou l'autre equipe)
log("\n=== Chiffres harmonises")
HARM = [
    ("Hypotheses A15, reference Commission 5,4 % (budget compris), definition A15", dict(A15, def2027=5.4, g2027="codex")),
    ("Hypotheses A15, reference 5,4 %, definition Codex (ratio effectif 2030 <= 2029)", dict(A15, def2027=5.4, g2027="codex", cible="effective")),
    ("Hypotheses A15, reference 6,5 %, definition Codex", dict(A15, cible="effective")),
    ("Hypotheses Codex, reference 5,4 %, definition A15 (seuil a croissance tendancielle)", dict(CODEX, cible="tendance")),
    ("Hypotheses Codex, reference 6,5 % (sans budget), definition Codex", dict(CODEX, def2027=6.5, g2027="A15")),
    ("Hypotheses Codex, reference 6,5 %, definition A15", dict(CODEX, def2027=6.5, g2027="A15", cible="tendance")),
    ("Hypotheses A15, reference 5,0 % (cible du PLF 2027, RESF), definition A15", dict(A15, def2027=5.0)),
    ("Hypotheses Codex, reference 5,0 % (cible du PLF 2027), definition Codex", dict(CODEX, def2027=5.0)),
    ("A15 avec ecart de production ferme a -0,5 en 2030 seulement (RESF, scenario avec consolidation)", "gap05"),
]
harm = []
for lib, p in HARM:
    if p == "gap05":
        sauve = dict(GAP_A15)
        GAP_A15.update({2028: -0.6, 2029: -0.55, 2030: -0.5})
        r = resume(lib, A15)
        GAP_A15.clear(); GAP_A15.update(sauve)
    else:
        r = resume(lib, p)
    harm.append(r)
    log(f"  {r['effort_2030_pts']:6.3f}  {lib}")
ecrire("C03_chiffres_harmonises.csv", harm)

with open(os.path.join(OUT, "C03_sortie_passage.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
