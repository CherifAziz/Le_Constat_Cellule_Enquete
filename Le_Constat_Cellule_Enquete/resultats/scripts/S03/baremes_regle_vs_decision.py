# -*- coding: utf-8 -*-
"""
S03 - Test « règle en vigueur » contre « décision » sur les barèmes, 1974-1985.

Relançable : python -I baremes_regle_vs_decision.py
Entrées (resultats\\donnees\\S03\\sources\\, extraits texte des tables IPP enregistrées le 20/11/2026) :
  ipp_revalo_pensions_rg_extrait.txt        coefficients de revalorisation des pensions du régime général
  ipp_minimum_vieillesse_avts_extrait.txt   AVTS, montant annuel personne seule
  ipp_minimum_vieillesse_as_extrait.txt     allocation supplémentaire (FNS), montant annuel personne seule
  ipp_bmaf_extrait.txt                      base mensuelle des allocations familiales
  + séries Insee (même lecture que decomposition_prestations_1974_1985.py) : PIB valeur, emploi, prix de consommation.
Méthode : indice en escalier mensuel (valeur en vigueur au 1er de chaque mois), moyenne annuelle ; comparaison des
taux de croissance logarithmiques annuels moyens avec (a) les prix de la consommation des ménages, (b) le PIB nominal
par emploi (approximation du salaire moyen nominal, part salariale supposée constante), (c) le PIB nominal par habitant.
Sortie : resultats\\donnees\\S03\\S03_baremes.csv ; affichage des écarts et du coût borné du minimum vieillesse.
"""
import csv
import math
import os
import re
import xml.etree.ElementTree as ET

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
SRC = os.path.join(RACINE, "donnees", "S03", "sources")
OUT = os.path.join(RACINE, "donnees", "S03")
F_PAR_EUR = 6.55957


def lire_ipp(fichier, col):
    """Renvoie [(date(a,m,j), valeur)] trié, colonne `col` (0 = date)."""
    res = []
    for l in open(os.path.join(SRC, fichier), encoding="utf-8"):
        c = [x.strip() for x in l.split("|")]
        m = re.fullmatch(r"(\d\d)/(\d\d)/(\d{4})", c[0]) if c else None
        if not m or len(c) <= col:
            continue
        v = c[col].replace("FRF", "").replace("€", "").replace(" ", "").replace(",", ".")
        if not v or "€" in c[col]:
            continue
        try:
            res.append(((int(m.group(3)), int(m.group(2)), int(m.group(1))), float(v)))
        except ValueError:
            pass
    return sorted(res)


def niveau_mensuel(points, a, mois):
    v = None
    for (aa, mm, jj), x in points:
        if (aa, mm) <= (a, mois):
            v = x
    return v


def moyenne_annuelle(points, a):
    return sum(niveau_mensuel(points, a, m) for m in range(1, 13)) / 12


def indice_coefficients(coefs):
    """Coefficients multiplicatifs datés -> niveau d'indice cumulé (base 1 avant le premier)."""
    pts, niv = [], 1.0
    for d, c in coefs:
        niv *= c
        pts.append((d, niv))
    return pts


coef = [(d, c) for d, c in lire_ipp("ipp_revalo_pensions_rg_extrait.txt", 1) if (1958, 1, 1) <= d <= (1986, 12, 31)]
# Ligne ambiguë : 01/07/1983 = 1,04 sans arrêté, et la ligne 01/01/1983 dit « à titre exceptionnel, ce coefficient est
# fixé à 4 % toute l'année ». Variante A : 1,04 appliqué deux fois en 1983 ; variante B : une seule fois.
coefA = coef
coefB = [(d, c) for d, c in coef if d != (1983, 7, 1)]
pensA = indice_coefficients(coefA)
pensB = indice_coefficients(coefB)
avts = lire_ipp("ipp_minimum_vieillesse_avts_extrait.txt", 1)
as_ = lire_ipp("ipp_minimum_vieillesse_as_extrait.txt", 1)
mv = []
for d in sorted(set([d for d, _ in avts] + [d for d, _ in as_])):
    if (1970, 1, 1) <= d <= (1986, 12, 31):
        a = niveau_mensuel(avts, d[0], d[1]); s = niveau_mensuel(as_, d[0], d[1])
        if a is not None and s is not None:
            mv.append((d, a + s))
bmaf = [(d, v) for d, v in lire_ipp("ipp_bmaf_extrait.txt", 1) if (1970, 1, 1) <= d <= (1986, 12, 31)]


def sdmx(fichier):
    racine = ET.parse(os.path.join(SRC, fichier)).getroot()
    res = {}
    for s in racine.iter():
        if s.tag.endswith("Series"):
            res[s.get("IDBANK")] = {o.get("TIME_PERIOD"): float(o.get("OBS_VALUE")) for o in s
                                    if o.tag.endswith("Obs") and o.get("OBS_VALUE") not in (None, "NaN", "")}
    return res


pib = sdmx("insee_bdm_CNA-2020-PIB_1959_1990.xml")
Y = {int(k): v for k, v in pib["011779992"].items()}
emp = sdmx("insee_bdm_CNA-2020-EMPLOI_1959_1990.xml")
EMP = {int(k): emp["011793486"][k] + emp["011793739"][k] for k in emp["011793486"]}
cons = sdmx("insee_bdm_CNA-2020-CONSO-SI_1959_1990.xml")
PC = {int(k): v for k, v in cons["011783317"].items()}
pop = sdmx("insee_bdm_POPULATION-STRUCTURE_1959_1990.xml")
P1J = {int(k[:4]): v for k, v in pop["000067670"].items()}
POP = {a: (P1J[a] + P1J[a + 1]) / 2 for a in range(1959, 1990)}

ANS = list(range(1959, 1987))
lignes = []
for a in ANS:
    lignes.append({"annee": a,
                   "pension_RG_indice_A": round(moyenne_annuelle(pensA, a), 5),
                   "pension_RG_indice_B": round(moyenne_annuelle(pensB, a), 5),
                   "minimum_vieillesse_seul_FRF": round(moyenne_annuelle(mv, a), 1) if a >= 1971 else "",
                   "BMAF_FRF": round(moyenne_annuelle(bmaf, a), 2) if a >= 1971 else "",
                   "prix_conso": PC[a], "PIB_nominal_par_emploi_EUR": round(Y[a] / EMP[a] * 1000, 1),
                   "PIB_nominal_par_habitant_EUR": round(Y[a] * 1e6 / POP[a], 1)})
with open(os.path.join(OUT, "S03_baremes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()), delimiter=";")
    w.writeheader()
    for l in lignes:
        w.writerow(l)

L = {l["annee"]: l for l in lignes}
def g(k, a0, a1):
    return 100 * math.log(L[a1][k] / L[a0][k]) / (a1 - a0)

print("Croissance annuelle moyenne (log, %/an)")
cles = ["pension_RG_indice_A", "pension_RG_indice_B", "minimum_vieillesse_seul_FRF", "BMAF_FRF", "prix_conso",
        "PIB_nominal_par_emploi_EUR", "PIB_nominal_par_habitant_EUR"]
for (a0, a1) in [(1974, 1980), (1980, 1985), (1974, 1985), (1980, 1983), (1983, 1985)]:
    print("%d-%d " % (a0, a1) + " ".join("%s=%.2f" % (k.split("_")[0] + k[-2:], g(k, a0, a1)) for k in cles))

# Écart cumulé 1974-1985 de chaque barème au PIB nominal par emploi (règle « salaire moyen ») et aux prix
for k in ["pension_RG_indice_A", "pension_RG_indice_B", "minimum_vieillesse_seul_FRF", "BMAF_FRF"]:
    for ref in ["PIB_nominal_par_emploi_EUR", "prix_conso"]:
        for (a0, a1) in [(1974, 1980), (1980, 1985), (1974, 1985)]:
            e = math.log(L[a1][k] / L[a0][k]) - math.log(L[a1][ref] / L[a0][ref])
            print("écart log %s vs %s %d-%d : %+.3f" % (k, ref, a0, a1, e))

# Coût borné du « surplus » de minimum vieillesse par rapport au PIB nominal par emploi, en 1985
N_MV = 1.9e6  # titulaires, Conseil des ministres du 9 février 1983 (vie-publique, lu via web.archive.org)
Y85_FRF = Y[1985] * 1e6 * F_PAR_EUR
for (a0, a1) in [(1974, 1980), (1980, 1985), (1974, 1985)]:
    e = math.log(L[a1]["minimum_vieillesse_seul_FRF"] / L[a0]["minimum_vieillesse_seul_FRF"]) - math.log(L[a1]["PIB_nominal_par_emploi_EUR"] / L[a0]["PIB_nominal_par_emploi_EUR"])
    # montant 1985 imputable au surplus : MV1985 * (1 - exp(-e)) par titulaire, plafond : tous au montant plein
    sup = N_MV * L[1985]["minimum_vieillesse_seul_FRF"] * (1 - math.exp(-e))
    print("Surplus MV %d-%d : écart %.3f ; borne haute 1985 = %.1f Md F = %.3f %% du PIB 1985 ; borne basse (moitié, allocation différentielle) = %.3f %%"
          % (a0, a1, e, sup / 1e9, 100 * sup / Y85_FRF, 50 * sup / Y85_FRF))
print("PIB 1985 en Md F :", round(Y85_FRF / 1e9, 1), " PIB 1981 en Md F :", round(Y[1981] * 1e6 * F_PAR_EUR / 1e9, 1))
print("MV personne seule (FRF/an) janv. 1974, janv. 1981, janv. 1983, janv. 1985 :",
      niveau_mensuel(mv, 1974, 1), niveau_mensuel(mv, 1981, 1), niveau_mensuel(mv, 1983, 1), niveau_mensuel(mv, 1985, 1))
print("Contrôle : hausse MV mai 1981 -> janv. 1983 = %.1f %% (Conseil des ministres du 9/2/1983 : 56 %%)"
      % (100 * (niveau_mensuel(mv, 1983, 1) / niveau_mensuel(mv, 1981, 5) - 1)))
print("Contrôle : revalorisation pensions RG mai 1981 -> janv. 1983 = %.1f %% (A) (Conseil des ministres : 26,6 %% RG et alignés)"
      % (100 * (niveau_mensuel(pensA, 1983, 1) / niveau_mensuel(pensA, 1981, 5) - 1)))
print("Prix conso 1981->1983 (moyennes annuelles) : %.1f %%" % (100 * (PC[1983] / PC[1981] - 1)))

# ---- Test de la montée en charge (« noria » + couverture) : dépense vieillesse-survie par personne de 60 ans et plus
# (nominale) rapportée à l'indice de revalorisation des pensions du RG. Lit la sortie du script de décomposition.
SER = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(OUT, "S03_series_annuelles.csv"), encoding="utf-8"), delimiter=";")}
def vs60(a):
    return float(SER[a]["Vieillesse-survie_MEUR"]) / float(SER[a]["pop60p_milliers"])
print("Dépense vieillesse-survie par personne de 60+ (nominale) moins revalorisation RG (indice A), %/an :")
for (a0, a1) in [(1960, 1964), (1964, 1969), (1969, 1974), (1964, 1974), (1974, 1980), (1980, 1985), (1974, 1985)]:
    d = 100 * (math.log(vs60(a1) / vs60(a0)) - math.log(L[a1]["pension_RG_indice_A"] / L[a0]["pension_RG_indice_A"])) / (a1 - a0)
    rv = 100 * math.log(L[a1]["pension_RG_indice_A"] / L[a0]["pension_RG_indice_A"]) / (a1 - a0)
    q = 100 * math.log((Y[a1] / EMP[a1]) / (Y[a0] / EMP[a0])) / (a1 - a0)
    print("  %d-%d : dérive = %.2f ; revalorisation = %.2f ; PIB nominal par emploi = %.2f ; prix = %.2f"
          % (a0, a1, d, rv, q, 100 * math.log(PC[a1] / PC[a0]) / (a1 - a0)))

# ---- Test de masse : dépense vieillesse-survie totale (sans effectif) rapportée à l'indice de revalorisation, et
# croissance de la population de 60+ ; la dérive par personne de 60+ = masse/indice - effectif.
print("Masse vieillesse-survie / indice de revalorisation RG (A), et population 60+, %/an :")
for (a0, a1) in [(1960, 1964), (1964, 1969), (1969, 1974), (1964, 1974), (1974, 1980), (1980, 1985), (1974, 1985)]:
    m = 100 * (math.log(float(SER[a1]["Vieillesse-survie_MEUR"]) / float(SER[a0]["Vieillesse-survie_MEUR"]))
               - math.log(L[a1]["pension_RG_indice_A"] / L[a0]["pension_RG_indice_A"])) / (a1 - a0)
    n = 100 * math.log(float(SER[a1]["pop60p_milliers"]) / float(SER[a0]["pop60p_milliers"])) / (a1 - a0)
    print("  %d-%d : masse/indice = %.2f ; pop 60+ = %.2f ; dérive par personne de 60+ = %.2f" % (a0, a1, m, n, m - n))

# ---- Rythme des effectifs de retraités du régime général (Cnav, recueil 2019, titre III, p.4 T3-02, au 31/12) ----
CNAV = {1960: 2344492, 1965: 2678619, 1970: 3321504, 1975: 4145276, 1980: 4988827, 1985: 6001908}
print("Retraités du RG (Cnav), croissance annuelle moyenne par blocs de 5 ans :")
ks = sorted(CNAV)
for a0, a1 in zip(ks[:-1], ks[1:]):
    print("  %d-%d : %.2f %%/an" % (a0, a1, 100 * math.log(CNAV[a1] / CNAV[a0]) / (a1 - a0)))
print("  (variations annuelles publiées p.4 : 1975 +6,1 % ; 1980 +2,9 % ; 1985 +5,0 %)")
