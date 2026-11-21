# -*- coding: utf-8 -*-
"""
S03 - Décomposition de la hausse des prestations de protection sociale / PIB, 1974-1985, par risque.

Relançable : python -I decomposition_prestations_1974_1985.py
Entrées (lecture seule, dans resultats\\donnees\\S03\\sources\\) :
  - drees_cps_1959_2024_v20261027.xlsx  (Drees, comptes de la protection sociale, prestations par risque, M EUR courants)
  - insee_bdm_CNA-2020-PIB_1959_1990.xml (Insee BDM SDMX, comptes nationaux base 2020)
  - insee_bdm_CNA-2020-CONSO-SI_1959_1990.xml (déflateur de la consommation individuelle des ménages)
  - insee_bdm_POPULATION-STRUCTURE_1959_1990.xml (population au 1er janvier par grand groupe d'âges)
  - insee_bdm_CHOMAGE-TRIM-NATIONAL_1959_1990.xml (chômeurs BIT, trimestriel, depuis 1975T1)
  - effectifs CNAV (recueil statistique 2019, titre III, p.4 et p.186) : saisis ci-dessous, en dur, avec leur page.
Sorties (dans resultats\\donnees\\S03\\) :
  - S03_series_annuelles.csv   : séries annuelles utilisées
  - S03_decomposition.csv      : table par risque en quatre termes (points de PIB), variantes I et II, fenêtres de tendance
Identité : R = P/Y = (N/POP) * b / y, avec b = P/(N*D) (prestation moyenne réelle par bénéficiaire, déflateur du PIB D)
et y = Y/(POP*D) (PIB réel par habitant). Donc dlnR = dln(N/POP) + dln b - dln y (exact).
Ventilation en points de PIB par la moyenne logarithmique (LMDI) : chaque terme log x (R1-R0)/ln(R1/R0). Exact, sans résidu.
Termes :
  T1 Dénominateur  = -(dln y - gy_pre*T)          : ralentissement du PIB réel par habitant par rapport à sa tendance d'avant 1974
  T2 Bénéficiaires = dln(N/POP)                   : part des bénéficiaires dans la population (démographie, chômage)
  T3a Dérive ancienne = (gb_pre - gy_pre)*T       : prolongation de l'écart d'avant 1974 entre prestation moyenne réelle et PIB/hab
  T3b Écart à la tendance = dln b - gb_pre*T      : accélération (ou freinage) de la prestation moyenne réelle par rapport à sa propre tendance
  Variante I  (prestation rigide en termes réels) : termes ci-dessus.
  Variante II (prestation qui suit le PIB/hab)    : T1 = 0 ; T3b' = dln b - (gb_pre - gy_pre + gy_obs)*T = T3b + T1.
  Variante III (prestation qui suit le PIB réel par emploi, approximation de la règle d'indexation sur le salaire moyen) :
              III_T1 = [dln q - dln y] - (gq_pre - gy_pre)*T  (baisse du ratio emploi/population, relative à sa tendance)
              III_T3b = dln b - gb_pre*T - (dln q - gq_pre*T) ; T3a inchangé ; q = PIB réel / emploi total.
T3b (ou T3b', III_T3b) est le plafond de ce qui peut être imputé à des décisions postérieures à 1974 ; la part non couverte
par des coûts publiés est le résidu (terme 4), calculée dans le dossier S03.md, pas ici.
"""
import csv
import math
import os
import re
import sys

import xml.etree.ElementTree as ET

import openpyxl

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
SRC = os.path.join(RACINE, "donnees", "S03", "sources")
OUT = os.path.join(RACINE, "donnees", "S03")

T0, T1 = 1974, 1985


def sdmx(fichier):
    # Lecture XML stricte : certaines séries vides sont auto-fermantes (<Series .../>), une regex les mélangerait.
    racine = ET.parse(os.path.join(SRC, fichier)).getroot()
    res = {}
    for s in racine.iter():
        if s.tag.endswith("Series"):
            obs = {o.get("TIME_PERIOD"): o.get("OBS_VALUE") for o in s if o.tag.endswith("Obs")}
            res[s.get("IDBANK")] = {p: float(v) for p, v in obs.items() if v not in (None, "NaN", "")}
    return res


def annuel(serie):
    return {int(k): v for k, v in serie.items() if re.fullmatch(r"\d{4}", k)}


# ---------- Insee ----------
pib = sdmx("insee_bdm_CNA-2020-PIB_1959_1990.xml")
Y = annuel(pib["011779992"])            # PIB valeur, M EUR
Yv = annuel(pib["011779991"])           # PIB volume prix chaînés, M EUR 2020
D = {a: Y[a] / Yv[a] for a in Y}        # déflateur implicite du PIB
conso = sdmx("insee_bdm_CNA-2020-CONSO-SI_1959_1990.xml")
Dc = annuel(conso["011783317"])         # indice de prix de la consommation individuelle des ménages

emp = sdmx("insee_bdm_CNA-2020-EMPLOI_1959_1990.xml")
EMP = {a: annuel(emp["011793486"])[a] + annuel(emp["011793739"])[a] for a in annuel(emp["011793486"])}  # emploi intérieur total, milliers
pop = sdmx("insee_bdm_POPULATION-STRUCTURE_1959_1990.xml")
def pop1j(idb):
    return {int(k[:4]): v for k, v in pop[idb].items()}
# France métropolitaine (seul champ disponible par âge avant 1982 dans la BDM) ; ratios N/POP homogènes.
p_tot = pop1j("000067670")              # population totale au 1er janvier, métropole (individus)
p_m20 = pop1j("001686809")              # moins de 20 ans
p_60 = pop1j("001686811")               # 60 ans et plus
p_75 = pop1j("001686812")               # 75 ans et plus
def moyenne_annuelle(s, a):             # moyenne des 1er janvier a et a+1, en milliers
    return (s[a] + s[a + 1]) / 2 / 1000
ANS = [a for a in range(1959, 1990)]
POP = {a: moyenne_annuelle(p_tot, a) for a in ANS}
P60 = {a: moyenne_annuelle(p_60, a) for a in ANS}
P20 = {a: moyenne_annuelle(p_m20, a) for a in ANS}
P75 = {a: moyenne_annuelle(p_75, a) for a in ANS}

ch = sdmx("insee_bdm_CHOMAGE-TRIM-NATIONAL_1959_1990.xml")
CHOM = {}
for a in range(1975, 1990):
    q = [ch["011818555"]["%d-Q%d" % (a, k)] for k in (1, 2, 3, 4)]   # chômeurs BIT, France entière, CVS, milliers
    CHOM[a] = sum(q) / 4
CHOM_1975T1 = ch["011818555"]["1975-Q1"]

# CNAV, retraités du régime général au 31 décembre (recueil statistique 2019, titre III)
# p.4 / p.120 (T3-02, A2-1) : total France ; p.186 (A3-8) : résidents de métropole, seule source pour 1974.
CNAV_TOTAL = {1970: 3321504, 1975: 4145276, 1980: 4988827, 1985: 6001908}
CNAV_METRO = {1974: 3742669, 1975: 3970964, 1980: 4742343, 1985: 5674032}
CNAV_TOTAL[1974] = CNAV_METRO[1974] * CNAV_TOTAL[1975] / CNAV_METRO[1975]   # dérivé (part métropole de 1975)

# ---------- Drees ----------
wb = openpyxl.load_workbook(os.path.join(SRC, "drees_cps_1959_2024_v20261027.xlsx"), read_only=True, data_only=True)
ws = wb["prestations_1959_2024"]
rows = list(ws.iter_rows(values_only=True))
hdr = rows[0]
col = {}
for j, h in enumerate(hdr):
    if isinstance(h, str) and re.match(r"\d{4}", h):
        col[int(h[:4])] = j
def ligne(libelle):
    for r in rows[1:]:
        if isinstance(r[0], str) and r[0].strip() == libelle:
            return {a: float(r[j]) for a, j in col.items() if r[j] is not None}
    raise KeyError(libelle)
PREST = {k: ligne(k) for k in ["Prestations de protection sociale", "Santé", "Maladie", "Invalidité", "AT-MP",
                                "Vieillesse-survie", "Vieillesse", "Survie", "Famille", "Emploi",
                                "Insertion et réinsertion professionnelles", "Chômage", "Logement",
                                "Pauvreté et exclusion sociale"]}

# ---------- Séries annuelles ----------
with open(os.path.join(OUT, "S03_series_annuelles.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "PIB_MEUR", "PIB_vol_MEUR2020", "deflateur_PIB", "prix_conso_menages", "pop_moy_milliers",
                "pop60p_milliers", "pop_m20_milliers", "pop75p_milliers", "chomeurs_BIT_milliers"] +
               ["%s_MEUR" % k for k in PREST] + ["%s_pctPIB" % k for k in PREST])
    for a in range(1959, 1990):
        w.writerow([a, Y[a], Yv[a], round(D[a], 6), Dc.get(a), round(POP[a], 1), round(P60[a], 1), round(P20[a], 1),
                    round(P75[a], 1), round(CHOM[a], 1) if a in CHOM else ""] +
                   [round(PREST[k][a], 1) if a in PREST[k] else "" for k in PREST] + [round(100 * PREST[k][a] / Y[a], 3) if a in PREST[k] else "" for k in PREST])

# ---------- Décomposition ----------
def g(s, a0, a1):
    return (math.log(s[a1]) - math.log(s[a0])) / (a1 - a0)

def decomp(nom, P, N, a0=T0, a1=T1, fen=(1964, 1974), Nlabel=""):
    T = a1 - a0
    R0, R1 = 100 * P[a0] / Y[a0], 100 * P[a1] / Y[a1]
    L = (R1 - R0) / math.log(R1 / R0)
    y = {a: Y[a] / (POP[a] * D[a]) for a in Y if a in POP}
    b = {a: P[a] / (N[a] * D[a]) for a in N if a in P}
    sh = {a: N[a] / POP[a] for a in N if a in POP}
    gy_pre = g(y, *fen)
    gb_pre = g(b, *fen) if fen[0] in b and fen[1] in b else None
    t_den = -(math.log(y[a1] / y[a0]) - gy_pre * T)
    t_ben = math.log(sh[a1] / sh[a0])
    if gb_pre is None:
        gb_pre = gy_pre  # pas de tendance propre : neutre
    t_drift = (gb_pre - gy_pre) * T
    t_acc = math.log(b[a1] / b[a0]) - gb_pre * T
    q = {a: Yv[a] / EMP[a] for a in EMP}           # PIB réel par emploi (approximation du salaire réel moyen, part salariale constante)
    gq_pre = g(q, *fen)
    t3_den = (math.log(q[a1] / q[a0]) - math.log(y[a1] / y[a0])) - (gq_pre - gy_pre) * T
    t3_acc = math.log(b[a1] / b[a0]) - gb_pre * T - (math.log(q[a1] / q[a0]) - gq_pre * T)
    assert abs(t3_den + t_drift + t3_acc - (math.log(b[a1] / b[a0]) - math.log(y[a1] / y[a0]))) < 1e-9
    tot = t_den + t_ben + t_drift + t_acc
    assert abs(tot - math.log(R1 / R0)) < 1e-9
    pts = lambda x: L * x
    return {
        "risque": nom, "beneficiaires": Nlabel, "periode": "%d-%d" % (a0, a1), "fenetre_tendance": "%d-%d" % fen,
        "R0_pctPIB": round(R0, 3), "R1_pctPIB": round(R1, 3), "hausse_pts": round(R1 - R0, 3),
        "gy_pre_pct": round(100 * gy_pre, 2), "gy_obs_pct": round(100 * math.log(y[a1] / y[a0]) / T, 2),
        "gb_pre_pct": round(100 * gb_pre, 2), "gb_obs_pct": round(100 * math.log(b[a1] / b[a0]) / T, 2),
        "gN_obs_pct": round(100 * math.log(N[a1] / N[a0]) / T, 2),
        "I_T1_denominateur": round(pts(t_den), 3), "I_T2_beneficiaires": round(pts(t_ben), 3),
        "I_T3a_derive_ancienne": round(pts(t_drift), 3), "I_T3b_ecart_tendance": round(pts(t_acc), 3),
        "II_T1_denominateur": 0.0, "II_T3b_ecart_tendance": round(pts(t_acc + t_den), 3),
        "gq_pre_pct": round(100 * gq_pre, 2), "gq_obs_pct": round(100 * math.log(q[a1] / q[a0]) / T, 2),
        "III_T1_denominateur_emploi": round(pts(t3_den), 3), "III_T3b_ecart_regle_productivite": round(pts(t3_acc), 3),
    }

RES = []
for fen in [(1964, 1974), (1969, 1974), (1959, 1974)]:
    RES.append(decomp("Vieillesse-survie", PREST["Vieillesse-survie"], P60, fen=fen, Nlabel="population 60 ans et plus"))
    RES.append(decomp("Santé (maladie, invalidité, AT-MP)", PREST["Santé"], POP, fen=fen, Nlabel="population totale"))
    RES.append(decomp("Famille", PREST["Famille"], P20, fen=fen, Nlabel="population de moins de 20 ans"))
    RES.append(decomp("Logement", PREST["Logement"], POP, fen=fen, Nlabel="population totale"))
    RES.append(decomp("Pauvreté-exclusion", PREST["Pauvreté et exclusion sociale"], POP, fen=fen, Nlabel="population totale"))
# Emploi : pas de chômeurs BIT avant 1975 -> tendance propre neutre ; 1975-1985 avec chômeurs BIT moyenne annuelle,
# et 1974-1985 avec le niveau de 1975T1 imputé à 1974 (minorant de l'effet bénéficiaires).
CH74 = dict(CHOM); CH74[1974] = CHOM_1975T1
for fen in [(1964, 1974), (1969, 1974), (1959, 1974)]:
    r = decomp("Emploi (chômage, préretraites, insertion)", PREST["Emploi"], CH74, fen=fen, Nlabel="chômeurs BIT (1974 := 1975T1)")
    RES.append(r)
RES.append(decomp("Emploi (chômage, préretraites, insertion)", PREST["Emploi"], CHOM, a0=1975, fen=(1964, 1974), Nlabel="chômeurs BIT, moyenne annuelle"))
# Variante vieillesse : retraités du régime général (CNAV) - pas de tendance avant 1974 disponible en annuel ; fenêtre 1970-1974 approchée
CNAV = {a: v / 1000 for a, v in CNAV_TOTAL.items()}
r = decomp("Vieillesse-survie (variante CNAV)", PREST["Vieillesse-survie"], CNAV, fen=(1970, 1974), Nlabel="retraités du régime général CNAV (31/12)")
RES.append(r)
# Total (somme des risques avec bénéficiaires = population totale) pour mémoire
RES.append(decomp("Total des prestations (bénéficiaires = population)", PREST["Prestations de protection sociale"], POP, fen=(1964, 1974), Nlabel="population totale"))

# Sous-périodes (fenêtre de tendance 1964-1974) : 1974-1980 (avant l'alternance), 1980-1985 (dont mesures de 1981-1982)
for (a0, a1) in [(1974, 1980), (1980, 1985), (1980, 1983)]:
    RES.append(decomp("Vieillesse-survie", PREST["Vieillesse-survie"], P60, a0=a0, a1=a1, Nlabel="population 60 ans et plus"))
    RES.append(decomp("Santé (maladie, invalidité, AT-MP)", PREST["Santé"], POP, a0=a0, a1=a1, Nlabel="population totale"))
    RES.append(decomp("Famille", PREST["Famille"], P20, a0=a0, a1=a1, Nlabel="population de moins de 20 ans"))
    RES.append(decomp("Logement", PREST["Logement"], POP, a0=a0, a1=a1, Nlabel="population totale"))
    RES.append(decomp("Pauvreté-exclusion", PREST["Pauvreté et exclusion sociale"], POP, a0=a0, a1=a1, Nlabel="population totale"))
    RES.append(decomp("Emploi (chômage, préretraites, insertion)", PREST["Emploi"], CH74, a0=a0, a1=a1, Nlabel="chômeurs BIT (1974 := 1975T1)"))
    RES.append(decomp("Total des prestations (bénéficiaires = population)", PREST["Prestations de protection sociale"], POP, a0=a0, a1=a1, Nlabel="population totale"))

champs = list(RES[0].keys())
with open(os.path.join(OUT, "S03_decomposition.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=champs, delimiter=";")
    w.writeheader()
    for r in RES:
        w.writerow(r)

# ---------- Affichage ----------
for r in RES:
    print(r["risque"][:42].ljust(42), r["periode"], r["fenetre_tendance"], "R0=%.2f R1=%.2f d=%.2f" % (r["R0_pctPIB"], r["R1_pctPIB"], r["hausse_pts"]),
          "| I: den %.2f ben %.2f der %.2f acc %.2f | II acc %.2f | III den %.2f acc %.2f" % (r["I_T1_denominateur"], r["I_T2_beneficiaires"], r["I_T3a_derive_ancienne"], r["I_T3b_ecart_tendance"], r["II_T3b_ecart_tendance"], r["III_T1_denominateur_emploi"], r["III_T3b_ecart_regle_productivite"]),
          "| gy pre/obs %.2f/%.2f gb pre/obs %.2f/%.2f gN %.2f" % (r["gy_pre_pct"], r["gy_obs_pct"], r["gb_pre_pct"], r["gb_obs_pct"], r["gN_obs_pct"]))
print("PIB 1974/1985 (M EUR):", Y[1974], Y[1985], " emploi (milliers):", round(EMP[1974]), round(EMP[1985]))
print("Prestations totales 1974/1985 (M EUR):", PREST["Prestations de protection sociale"][1974], PREST["Prestations de protection sociale"][1985])
print("CNAV 1974 dérivé:", round(CNAV_TOTAL[1974]))
print("Chômeurs BIT 1975T1, moy 1975, 1985:", CHOM_1975T1, round(CHOM[1975]), round(CHOM[1985]))
print("Pop 60+ 1974/1985:", round(P60[1974]), round(P60[1985]), " pop:", round(POP[1974]), round(POP[1985]))
print("Prix conso / déflateur PIB 1974->1985 (log diff, %/an):", round(100 * (math.log(Dc[1985] / Dc[1974]) - math.log(D[1985] / D[1974])) / 11, 3))
