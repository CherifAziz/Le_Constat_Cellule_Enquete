"""A01 - Vérification des calculs du dossier Astra (19/11/2026) et des chiffres comptables de la V5 (13/11/2026).
Entrées : base commune (Eurostat gov_10dd_edpt1, gov_10a_main, gov_10a_exp, gov_10a_taxag ; Insee) + tables A01.
Sortie : resultats/donnees/A01/A01_verifications_astra_v5.csv  (id;objet;valeur_source_texte;valeur_recalculee;ecart;commentaire)
         resultats/donnees/A01/A01_ecarts_FR_zone_euro.csv (2025 main et 2024 COFOG ; moyenne avec et sans France)
         resultats/donnees/A01/A01_stabilisation_dette_sensibilite.csv
Relançable : python -I 06_verifications_astra_v5.py
"""
import os, csv
from collections import defaultdict

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
A01 = os.path.join(RACINE, "resultats", "donnees", "A01")

def charge(fichier, cles):
    d = {}
    with open(os.path.join(COMMUN, fichier), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                d[tuple(r[k] for k in cles) + (int(r["time"]),)] = float(r["value"])
            except ValueError:
                pass
    return d
EDP = charge("eurostat_gov_10dd_edpt1.csv", ["unit", "na_item", "geo"])
MAIN = charge("eurostat_gov_10a_main.csv", ["unit", "sector", "na_item", "geo"])
COF = charge("eurostat_gov_10a_exp.csv", ["cofog99", "geo"])
TAX = charge("eurostat_gov_10a_taxag.csv", ["na_item", "geo"])

chk = []
def add(i, objet, src, val, com=""):
    try:
        e = round(float(val) - float(src), 3)
    except (TypeError, ValueError):
        e = ""
    chk.append([i, objet, src, val if not isinstance(val, float) else round(val, 4), e, com])

# ---------- Base 2025 ----------
B9 = -EDP[("MIO_EUR", "B9", "FR", 2025)] / 1000
GD = EDP[("MIO_EUR", "GD", "FR", 2025)] / 1000
GD24 = EDP[("MIO_EUR", "GD", "FR", 2024)] / 1000
Y = GD / EDP[("PC_GDP", "GD", "FR", 2025)] * 100  # approximation ; PIB exact Insee t_3106 = 2991.06
Y_INSEE = 2991.056  # t_3216/t_3215 (identique à t_3106 'Série de PIB utilisée')
Y24 = 2935.24
add("A01", "Déficit 2025 Md€ (Eurostat 21/10/2026)", 151.592, B9)
add("A02", "Déficit 2025 % PIB non arrondi", 5.1, B9 / Y_INSEE * 100, "5,068 % ; arrondi 5,1")
add("A03", "Dette 2025 % PIB non arrondi", 115.7, GD / Y_INSEE * 100)
add("A04", "Point de PIB 2025 (Md€)", 29.91, Y_INSEE / 100)
add("A05", "Hausse dette brute 2025 (Md€)", 154.0, GD - GD24)
add("A06", "Hausse dette - déficit (Md€)", 2.4, GD - GD24 - B9, "= ajustement stocks-flux ; Insee t_3105 donne 154,0 - 151,6")
I25 = EDP[("MIO_EUR", "D41PAY", "FR", 2025)] / 1000
add("A07", "Intérêts D41 versés 2025 (Md€, y.c. Sifim)", 64.7, I25, "Astra cite 64,7 = Insee IP2106 hors Sifim ; D41 y.c. Sifim = 65,721")
add("A08", "Déficit primaire 2025 (Md€), millésime oct. 2026, D41 y.c. Sifim", 87.8, B9 - I25, "Astra : 152,5 - 64,7 (millésime mai, intérêts hors Sifim)")
add("A09", "Déficit primaire 2025 (Md€), oct. 2026, intérêts hors Sifim (64,652)", 87.8, B9 - 64.652)
add("A10", "Déficit primaire 2025 % PIB", 2.9, (B9 - I25) / Y_INSEE * 100)
add("A11", "Baisse du déficit 2024-2025 (Md€)", 17.5, EDP[("MIO_EUR", "B9", "FR", 2025)] / 1000 - EDP[("MIO_EUR", "B9", "FR", 2024)] / 1000)
add("A12", "Variation dette 2022->2023 (Md€) début", 2956, EDP[("MIO_EUR", "GD", "FR", 2022)] / 1000)
add("A13", "Variation dette 2022->2023 (Md€) fin", 3103, EDP[("MIO_EUR", "GD", "FR", 2023)] / 1000)

# ---------- Stabilisation de la dette (formule Astra / 04_PREUVES §IV) ----------
rows_stab = []
for d_lbl, d in [("115,7 arrondi", 1.157), ("115,682 non arrondi", GD / Y_INSEE)]:
    for g in [0.01, 0.02, 0.03, 0.04]:
        s = d * g / (1 + g)
        for def_lbl, defi in [("5,1 arrondi", 0.051), ("5,068 non arrondi", B9 / Y_INSEE)]:
            rows_stab.append([d_lbl, g, round(s * 100, 3), def_lbl, round((defi - s) * Y_INSEE, 1),
                              round((defi - s) * Y_INSEE * 1.0 , 1)])
with open(os.path.join(A01, "A01_stabilisation_dette_sensibilite.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["dette_initiale", "croissance_nominale", "deficit_stabilisant_pct_PIB_t+1", "deficit_de_depart", "ecart_Md€_au_PIB_2025", "note"])
    for r in rows_stab:
        w.writerow(r[:5] + ["écart exprimé au PIB 2025 ; le déficit stabilisant est en % du PIB de l'année suivante"])
s3 = 1.157 * 0.03 / 1.03
add("S01", "Déficit stabilisant d=115,7 g=3 % (% PIB)", 3.37, s3 * 100)
add("S02", "Écart 5,1 -> stabilisant g=3 % (Md€)", 52, (0.051 - s3) * Y_INSEE)
add("S03", "Écart g=2 % (Md€)", 85, (0.051 - 1.157 * 0.02 / 1.02) * Y_INSEE)
add("S04", "Écart g=4 % (Md€)", 19, (0.051 - 1.157 * 0.04 / 1.04) * Y_INSEE)
add("S05", "Écart à 3 % (Md€)", 63, (0.051 - 0.03) * Y_INSEE, "avec 5,068 non arrondi : 61,9")
add("S06", "Écart à 3 % non arrondi (Md€)", 63, (B9 / Y_INSEE - 0.03) * Y_INSEE)
add("S07", "Écart g=3 % non arrondi (Md€)", 52, (B9 / Y_INSEE - (GD / Y_INSEE) * 0.03 / 1.03) * Y_INSEE)
# Excédent primaire stabilisant (formule Astra) avec i apparent 2025
i_app = I25 / GD24
for g in [0.02, 0.03]:
    add(f"S08_g{g}", f"Solde primaire stabilisant (i apparent {i_app*100:.2f} %, g={g}) % PIB", "", (GD / Y_INSEE) * (i_app - g) / (1 + g) * 100,
        "négatif = un déficit primaire est compatible avec la stabilité")

# Croissances nominales ancrées sur des pièces : 2025 observée (Insee, PIB 2935,24 -> 2991,056) ;
# 2026 et 2027 : Commission, prévisions d'automne 2026 (IP 348, tableau III.8.1 p. 123) : PIB réel +0,4 % / +0,6 %,
# déflateur du PIB +1,8 % / +1,9 %.
G_PIECES = [("2025 observé (Insee)", Y_INSEE / Y24 - 1), ("2026 Commission (0,4 % ; 1,8 %)", 1.004 * 1.018 - 1),
            ("2027 Commission (0,6 % ; 1,9 %)", 1.006 * 1.019 - 1)]
d_nr = GD / Y_INSEE
for lib, g in G_PIECES:
    s = d_nr * g / (1 + g)
    add(f"S09 {lib}", f"g={g*100:.2f} % : déficit stabilisant (% PIB) / écart au déficit 2025 non arrondi (Md€)", "",
        f"{s*100:.2f} % / {(B9 / Y_INSEE - s) * Y_INSEE:.1f} Md€")
    add(f"S10 {lib}", f"g={g*100:.2f} % : solde primaire stabilisant (% PIB) avec i apparent 2025 {i_app*100:.2f} %", "",
        round(d_nr * (i_app - g) / (1 + g) * 100, 2))

# ---------- France - zone euro 2025 (gov_10a_main) ----------
ez = []
def pc(geo, item, an, sec="S13"):
    return MAIN.get(("PC_GDP", sec, item, geo, an))
def mio(geo, item, an, sec="S13"):
    return MAIN.get(("MIO_EUR", sec, item, geo, an))
for an in (2024, 2025):
    yFR = mio("FR", "TE", an) / pc("FR", "TE", an) * 100
    yEA = mio("EA20", "TE", an) / pc("EA20", "TE", an) * 100
    for item in ["TE", "TR", "B9", "D41PAY", "D62PAY", "D632PAY", "D1PAY", "P51G", "D2REC", "D5REC", "D61REC"]:
        fr, ea = mio("FR", item, an), mio("EA20", item, an)
        if fr is None or ea is None:
            continue
        ex = (ea - fr) / (yEA - yFR) * 100
        ez.append([an, "gov_10a_main", item, round(fr / yFR * 100, 2), round(ea / yEA * 100, 2), round(ex, 2),
                   round(fr / yFR * 100 - ea / yEA * 100, 2), round(fr / yFR * 100 - ex, 2), round(yFR / yEA * 100, 1)])
add("Z01", "FR dépenses 2025 % PIB", 57.3, pc("FR", "TE", 2025))
add("Z02", "EA20 dépenses 2025 % PIB", 49.8, pc("EA20", "TE", 2025))
add("Z03", "FR recettes 2025", 52.2, pc("FR", "TR", 2025))
add("Z04", "EA20 recettes 2025", 46.8, pc("EA20", "TR", 2025))
add("Z05", "Écart dépenses - écart recettes 2025 (pts)", 2.1, (pc("FR", "TE", 2025) - pc("EA20", "TE", 2025)) - (pc("FR", "TR", 2025) - pc("EA20", "TR", 2025)),
    "identité : = écart de solde (EA20 inclut la France)")
add("Z06", "Écart de solde FR-EA20 2025 (pts)", 2.1, pc("EA20", "B9", 2025) - pc("FR", "B9", 2025))

# ---------- COFOG 2024 ----------
FONCS = [("TOTAL", "Total"), ("GF10", "Protection sociale"), ("GF1002", "dont vieillesse"), ("GF07", "Santé"), ("GF04", "Affaires économiques"),
         ("GF09", "Enseignement"), ("GF06", "Logement et équipements collectifs"), ("GF02", "Défense"), ("GF01", "Services généraux"),
         ("GF0107", "dont transactions dette publique"), ("GF03", "Ordre et sécurité"), ("GF05", "Environnement"), ("GF08", "Loisirs, culture, culte")]
for c, lib in FONCS:
    vals = [COF.get((c, g, 2024)) for g in ("FR", "EA20", "DE", "SE")]
    ez.append([2024, "gov_10a_exp COFOG", f"{c} {lib}", vals[0], vals[1], "", round(vals[0] - vals[1], 2) if None not in vals[:2] else "", "", ""])
cg = lambda c: COF[(c, "FR", 2024)] - COF[(c, "EA20", 2024)]
add("K01", "COFOG FR total 2024", 57.3, COF[("TOTAL", "FR", 2024)], "statut p ; gov_10a_main TE 2024 = %s" % pc("FR", "TE", 2024))
add("K02", "Écart total COFOG FR-EA20 2024 (pts)", 8.1, cg("TOTAL"))
add("K03", "Écart protection sociale (pts)", 3.7, cg("GF10"))
add("K04", "Écart santé (pts)", 1.5, cg("GF07"))
add("K05", "Part (protection sociale + santé) dans l'écart COFOG", 64, (cg("GF10") + cg("GF07")) / cg("TOTAL") * 100)
add("K06", "Écart vieillesse (pts)", 2.5, cg("GF1002"))
add("K07", "Même part rapportée à l'écart main 2024 (TE)", 64, (cg("GF10") + cg("GF07")) / (pc("FR", "TE", 2024) - pc("EA20", "TE", 2024)) * 100,
    "mélange de sources : illustratif")
add("K08", "Part rapportée à l'écart 2025 (7,5 pts) comme le fait la V5", 64, (cg("GF10") + cg("GF07")) / (pc("FR", "TE", 2025) - pc("EA20", "TE", 2025)) * 100,
    "mélange 2024/2025 : contresens d'année")

# ---------- Impôts et cotisations : rang 2025 parmi les territoires du fichier ----------
for item, lib in [("D2_D5_D91_D61_M_D995", "impôts + cotisations nettes"), ("D2_D5_D91_D61_M_D612_M_D614_M_D995", "hors cotisations imputées"),
                  ("D2_D5_D91", "impôts seuls")]:
    pays = sorted(((TAX[(item, g, 2025)], g) for (it, g, an) in TAX if it == item and an == 2025 and g not in ("EA20", "EU27_2020")), reverse=True)
    add(f"T_{item}", f"Rang 2025 ({lib}) : 1er = {pays[0][1]} {pays[0][0]} ; 2e = {pays[1][1]} {pays[1][0]} ; FR = {TAX[(item,'FR',2025)]}",
        "", [g for v, g in pays].index("FR") + 1, f"{len(pays)} pays présents dans le fichier commun (pas les 27)")

# ---------- V5 ----------
add("V01", "Part des dépenses 2025 financée par l'emprunt (%)", 9, B9 / 1714.112 * 100)
add("V02", "Déficit par jour 2025 (M€)", 400, B9 / 365 * 1000)
add("V03", "Croissance dette 2025 / croissance PIB nominal 2025 (ratio)", 2, ((GD / GD24) - 1) / (Y_INSEE / Y24 - 1))
add("V04", "Dette 2007 en mois de PIB", 8, 65.477 * 12 / 100)
add("V05", "Dette 2025 en mois de PIB", 14, GD / Y_INSEE * 12)
add("V06", "Hausse 2007->2012 en mois de PIB", 3, (91.742 - 65.477) * 12 / 100)
add("V07", "Hausse 2019->2020 en mois de PIB", 2, (114.907 - 98.158) * 12 / 100)
add("V08", "Part des intérêts dans le déficit 1993 (%)", 50, 36.583 / 72.623 * 100)
for an in range(2014, 2020):
    add(f"V09_{an}", f"Allemagne solde {an} % PIB", "", EDP[("PC_GDP", "B9", "DE", an)])
add("V10", "Allemagne dette 2013 en mois de PIB", 10, EDP[("PC_GDP", "GD", "DE", 2013)] * 12 / 100)
add("V11", "Allemagne dette 2019 en mois de PIB", 7, EDP[("PC_GDP", "GD", "DE", 2019)] * 12 / 100)
add("V12", "Italie solde primaire 2025 % PIB", "", EDP[("PC_GDP", "B9", "IT", 2025)] + EDP[("PC_GDP", "D41PAY", "IT", 2025)])
add("V13", "France solde primaire 2025 % PIB", -3, -(B9 - I25) / Y_INSEE * 100)
add("V14", "Combler par l'impôt : impôts+cotisations FR 2025 + déficit (% PIB)", "", TAX[("D2_D5_D91_D61_M_D995", "FR", 2025)] + B9 / Y_INSEE * 100)
add("V15", "Combler par la dépense : dépenses FR 2025 - déficit vs EA20 49,8", "", pc("FR", "TE", 2025) - B9 / Y_INSEE * 100)
add("V16", "Dixième de point de taux sur la dette 2025 (Md€/an, à refinancement complet)", 4, 0.001 * GD, "dette APU ; horizon = refinancement complet")

with open(os.path.join(A01, "A01_verifications_astra_v5.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["id", "objet", "valeur_texte", "valeur_recalculee", "ecart", "commentaire"])
    w.writerows(chk)
with open(os.path.join(A01, "A01_ecarts_FR_zone_euro.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "source", "poste", "FR_pct_PIB", "EA20_pct_PIB", "EA20_hors_FR_pct_PIB", "ecart_FR_EA20", "ecart_FR_EA20_hors_FR", "poids_FR_dans_EA20_pct"])
    w.writerows(ez)
for r in chk:
    print(";".join(str(x) for x in r))
