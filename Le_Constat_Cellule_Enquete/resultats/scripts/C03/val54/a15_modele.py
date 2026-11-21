# -*- coding: utf-8 -*-
"""A15 - modele de dette des APU (S13) : identite recurrente, taux apparent avec
renouvellement progressif de l'encours, retroaction des mesures sur l'activite.
Python standard + numpy. Lancer via a15_executer.py (python -I).

Conventions
- Toutes les grandeurs de solde sont en points de PIB de l'annee (solde > 0 = excedent).
- Mesures : rendement "statique" ex ante (avant retroaction macro), en % du PIB.
- Retroaction : perte de production = somme_k m_k * dM_k(tau) * phi(t - tau) ;
  effet sur le solde = semi-elasticite (0,57, RESF 2027) * ecart de production.
"""
import csv, os, math

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
DON = os.path.join(RACINE, "donnees")
SORTIE = os.path.join(DON, "C03", "val_ref54")   # C03 : copie de validation

# ---------------------------------------------------------------- donnees
def lire_table_france():
    """Serie 1974-2025 construite par A07 a partir de donnees\\commun (Insee base 2020,
    Eurostat) et OCDE/BCE pour les taux. Lecture seule."""
    f = os.path.join(DON, "A07", "table_france_1974_2025.csv")
    out = {}
    with open(f, encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter=";"):
            a = int(r["annee"])
            d = {}
            for k, v in r.items():
                if k == "annee":
                    continue
                try:
                    d[k] = float(v)
                except (ValueError, TypeError):
                    d[k] = None
            out[a] = d
    return out

# ---------------------------------------------------------------- parametres
SEMI_ELAST = 0.57          # RESF 2027, note de tableau (copie A03) [C]
PIB_2025 = 2991.056        # Eurostat 21/10/2026 [C]
DETTE_2025 = 3460.1        # idem [C]
I_2025 = 65.721            # Insee D41 (table A07) [C]
SOLDE_2025 = -151.592      # [C]
PB_2025_PCT = -2.871       # [C] calcul
TAUX_APP_2025 = 1.988      # I_2025 / D_2024 [C]

# Profil d'estompement de l'effet d'activite (A13, hypothese reprise et harmonisee)
def phi(age):
    if age < 0:
        return 0.0
    if age <= 1:
        return 1.0
    if age <= 4:
        return 0.5
    return 0.2

def phi_persistant(age):
    return 1.0 if age >= 0 else 0.0

# ---------------------------------------------------------------- module d'interets
class Interets:
    """Encours conventionnel au taux moyen a ; une fraction f est refinancee chaque
    annee au taux de marche r_m ; l'emprunt net de l'annee paie r_m sur une demi-annee
    puis entre dans l'encours ; une part s est indexee (taux reel rr + inflation)."""
    def __init__(self, f=0.10, s=0.09, rr=0.5):
        self.f, self.s, self.rr = f, s, rr

    def charge(self, D_prev, a_prev, r_m, pi, pb_eur, sfa_eur):
        """Renvoie (interets, emprunt net, nouveau taux moyen). Taux en %."""
        f, s = self.f, self.s
        A = (1 - s) * D_prev * ((1 - f) * a_prev + f * r_m) / 100.0 \
            + s * D_prev * (self.rr + pi) / 100.0
        h = 0.5 * r_m / 100.0
        I = (A + h * (-pb_eur + sfa_eur)) / (1 - h)
        N = I - pb_eur + sfa_eur
        D = D_prev + N
        a_new = ((1 - f) * a_prev * D_prev + f * r_m * D_prev + r_m * N) / D if D > 0 else a_prev
        return I, N, a_new

# ---------------------------------------------------------------- scenario de projection
ANNEES = list(range(2026, 2051))

class Macro:
    """Hypotheses macro de reference (centrales) ; chaque champ est un dict annee->valeur."""
    def __init__(self, **kw):
        # croissance potentielle (%), deflateur (%), ecart de production de reference (pts)
        self.gpot = {}
        for a in ANNEES:
            self.gpot[a] = 1.2 if a <= 2028 else 1.0     # RESF 2027 tableau 1 [C] puis H
        self.defl = {2026: 1.8, 2027: 1.9}               # Commission automne 2026 [C]
        for a in ANNEES:
            if a >= 2028:
                self.defl[a] = 1.6 if a <= 2030 else 1.75  # RESF 2028-2030 [C] ; H ensuite
        self.ipch = {2026: 2.6, 2027: 2.9, 2028: 2.1}    # Commission [C]
        for a in ANNEES:
            self.ipch.setdefault(a, 1.9)                   # H
        # ecart de reference : 2025 +0,2 (RESF) ; 2026 croissance 0,4 (CE) ;
        # 2027 croissance sans mesures = 0,6 (CE) + 0,5 (effet des mesures, HCFP) = 1,1
        self.gap = {2026: -0.6, 2027: -0.7, 2028: -0.4, 2029: -0.2}
        for a in ANNEES:
            self.gap.setdefault(a, 0.0)
        # taux de marche moyen a l'emission (%) : calibre 2026-2028 (voir calibrer_rm), H ensuite
        self.rm = {}
        self.rm_lt = None
        self.choc_taux = 0.0           # points de % ajoutes a r_m a partir de 2027
        for k, v in kw.items():
            setattr(self, k, v)

def vieillissement(annee, variante="central"):
    """Hausse du cout des pensions + sante + dependance, en pts de PIB depuis 2027.
    Central : COR RA 2026 (14,1 en 2025 et 2030 ; 14,2 en 2045 ; 15,3 en 2070) [C via A06]
    + Ageing Report 2024 sante +0,3 et dependance +0,7 de 2022/2025 a 2070 [C via A06]."""
    def pens(a):
        pts = [(2025, 14.1), (2030, 14.1), (2045, 14.2), (2070, 15.3)]
        for (a0, v0), (a1, v1) in zip(pts, pts[1:]):
            if a0 <= a <= a1:
                return v0 + (v1 - v0) * (a - a0) / (a1 - a0)
        return pts[-1][1]
    if variante == "nul":
        return 0.0
    sante = 1.0 * (annee - 2027) / 43.0
    p = pens(annee) - pens(2027)
    if variante == "bas":
        return 0.5 * sante
    if variante == "haut":
        # risque sante AR (+1,1 au lieu de +0,3) et moitie de l'ecart de mortalite COR (1,2 pt en 2070)
        return p + (1.8 * (annee - 2027) / 43.0) + 0.6 * (annee - 2027) / 43.0
    return p + sante


def projeter(macro, mesures=None, mult=None, chocs=None, ref=None, interets=None,
             cibles_ref=None, vieil="central", emploi=0.0, persistant=False,
             derive_pb=None, fin=2050):
    """Projection 2026-2050.
    mesures : dict categorie -> dict annee -> rendement statique (% PIB, niveau cumule)
    mult : dict categorie -> multiplicateur
    chocs : dict annee -> dict(gap=..., disc=..., sfa=..., defl=...)
    ref : resultats de la reference (pour pb structurel) ; si None, mode cible.
    cibles_ref : dict annee -> deficit cible (% PIB) pour le mode cible (2026, 2027).
    emploi : effet de niveau de PIB en 2035 (%), phase de 2028 a 2035 (variante emploi).
    derive_pb : dict annee -> derive du solde primaire (% PIB), par exemple test A08.
    """
    mesures = mesures or {}
    mult = mult or {}
    chocs = chocs or {}
    derive_pb = derive_pb or {}
    interets = interets or Interets()
    ph = phi_persistant if persistant else phi
    res = {}
    D_prev, a_prev = DETTE_2025, TAUX_APP_2025
    Y_prev_reel = PIB_2025
    gap_prev = 0.2
    P_prev = PIB_2025 / (1 + gap_prev / 100.0)   # potentiel en euros 2025
    defl_idx = 1.0
    pbs = {}
    for t in ANNEES:
        if t > fin:
            break
        # --- perte de production due aux mesures
        perte = 0.0
        Mtot = 0.0
        for cat, serie in mesures.items():
            m = mult.get(cat, 0.5)
            prec = 0.0
            for tau in range(2026, t + 1):
                v = serie.get(tau, 0.0)
                dM = v - prec
                prec = v
                perte += m * dM * ph(t - tau)
            Mtot += serie.get(t, 0.0)
        ch = chocs.get(t, {})
        g_emp = 0.0
        if emploi:
            g_emp = emploi * min(1.0, max(0.0, (t - 2027) / 8.0))
        gap = macro.gap[t] - perte + ch.get("gap", 0.0) + g_emp
        P = P_prev * (1 + macro.gpot[t] / 100.0)
        defl = macro.defl[t] + ch.get("defl", 0.0)
        defl_idx *= (1 + defl / 100.0)
        Y = P * (1 + gap / 100.0) * defl_idx
        rm = macro.rm.get(t, macro.rm_lt) + (macro.choc_taux if t >= 2027 else 0.0)
        pi = macro.ipch[t] + ch.get("defl", 0.0)
        sfa = ch.get("sfa", 0.0) * Y / 100.0
        if ref is None and cibles_ref and t in cibles_ref:
            # mode cible : deficit impose, on deduit le solde primaire
            def_cible = cibles_ref[t]
            # resolution : I depend de N = deficit*Y + sfa
            f, s = interets.f, interets.s
            A = (1 - s) * D_prev * ((1 - f) * a_prev + f * rm) / 100.0 + s * D_prev * (interets.rr + pi) / 100.0
            N = def_cible * Y / 100.0 + sfa
            I = A + 0.5 * rm / 100.0 * N
            pb_eur = I - def_cible * Y / 100.0
            D = D_prev + N
            a_new = ((1 - f) * a_prev * D_prev + f * rm * D_prev + rm * N) / D
            pb = pb_eur / Y * 100.0
            pbs[t] = pb - SEMI_ELAST * gap
        else:
            src = ref["pb_struct"] if ref is not None else pbs
            if t <= 2027:
                base = src[t]
            else:
                # politique inchangee : structurel primaire 2027 constant, moins le vieillissement
                base = src[2027] - vieillissement(t, vieil)
            if ref is None:
                pbs[t] = base
            pb = base + SEMI_ELAST * gap + Mtot - ch.get("disc", 0.0) + derive_pb.get(t, 0.0)
            pb_eur = pb * Y / 100.0
            I, N, a_new = interets.charge(D_prev, a_prev, rm, pi, pb_eur, sfa)
            D = D_prev + N
        res[t] = dict(Y=Y, gap=gap, pb=pb, I=I, i_pct=I / Y * 100.0, deficit=(I - pb_eur) / Y * 100.0,
                      D=D, d=D / Y * 100.0, a=a_new, M=Mtot, rm=rm, g_nom=(Y / (Y_prev_reel) - 1) * 100.0)
        D_prev, a_prev, P_prev, Y_prev_reel = D, a_new, P, Y
    out = {"annees": res, "pb_struct": pbs if ref is None else ref["pb_struct"]}
    return out


def calibrer_rm(interets, macro):
    """Taux de marche 2026-2028 tels que le modele reproduise la charge d'interets de la
    Commission (2,6 ; 3,0 ; 3,3 % du PIB) avec ses deficits (5,5 ; 5,4 ; 5,7) et sa
    croissance nominale (0,4+1,8 ; 0,6+1,9 ; 1,4+2,4). Prevision Commission automne 2026 [C]."""
    ce = {2026: (5.5, 2.6, 0.4, 1.8, 2.6), 2027: (5.4, 3.0, 0.6, 1.9, 2.9), 2028: (5.7, 3.3, 1.4, 2.4, 2.1)}
    D_prev, a_prev, Y = DETTE_2025, TAUX_APP_2025, PIB_2025
    rms = {}
    for t in (2026, 2027, 2028):
        dfc, ipct, gr, de, pi = ce[t]
        Y = Y * (1 + gr / 100.0) * (1 + de / 100.0)
        lo, hi = -2.0, 15.0
        for _ in range(80):
            mid = (lo + hi) / 2
            f, s = interets.f, interets.s
            A = (1 - s) * D_prev * ((1 - f) * a_prev + f * mid) / 100.0 + s * D_prev * (interets.rr + pi) / 100.0
            N = dfc * Y / 100.0
            I = A + 0.5 * mid / 100.0 * N
            if I / Y * 100.0 > ipct:
                hi = mid
            else:
                lo = mid
        rm = (lo + hi) / 2
        rms[t] = rm
        f = interets.f
        N = dfc * Y / 100.0
        D = D_prev + N
        a_prev = ((1 - f) * a_prev * D_prev + f * rm * D_prev + rm * N) / D
        D_prev = D
    return rms


def sensibilite_choc_100pb(interets, D0=2896.0, def_part=0.05, annees=5):
    """Supplement de charge pour +100 pb sur toute la courbe, encours de l'Etat 2 896 Md€
    (AFT, sept. 2026). A comparer a : +3 / +8 / +12 Md€ (N, N+1, N+2 ; dossier de presse
    PLF 2027) et +3,4 Md€ la 1re annee, ~19 Md€ la 5e (PAP 117). [C via A07]"""
    f, s = interets.f, interets.s
    out = []
    D = D0
    rep = 0.0         # part de l'encours de depart deja refinancee
    nouv = 0.0        # emprunts nouveaux cumules
    for k in range(1, annees + 1):
        N = def_part * D
        rep = 1 - (1 - f) ** k
        # surcout : (1-s)*(part refinancee de l'encours initial) + emprunts nouveaux (moitie l'annee courante)
        surc = (1 - s) * D0 * rep * 0.01 + nouv * 0.01 + 0.5 * N * 0.01
        out.append(surc)
        nouv += N
        D += N
    return out
