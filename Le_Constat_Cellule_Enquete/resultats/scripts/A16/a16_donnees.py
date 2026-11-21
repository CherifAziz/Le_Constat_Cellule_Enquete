# -*- coding: utf-8 -*-
"""A16 - calculs de contre-expertise sur la base commune (lecture seule).
Lancer : python -I a16_donnees.py
Entrees (lecture seule) :
  donnees\\commun\\eurostat_gov_10a_exp.csv, eurostat_gov_10a_main.csv, eurostat_gov_10a_taxag.csv
  donnees\\A07\\table_france_1974_2025.csv (serie construite par A07 sur la base commune)
Sorties : donnees\\A16\\a16_*.csv et a16_sortie_donnees.txt
"""
import csv, os, collections

R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
COM = os.path.join(R, "donnees", "commun")
OUT = os.path.join(R, "donnees", "A16")
LOG = []

def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)

def lire(f):
    with open(os.path.join(COM, f), encoding="utf-8-sig") as h:
        return list(csv.DictReader(h))

def ecrire(nom, lignes):
    cols = list(lignes[0].keys())
    with open(os.path.join(OUT, nom), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=cols, delimiter=";")
        w.writeheader()
        for l in lignes:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})

# ------------------------------------------------------------------ main (S13)
MAIN = collections.defaultdict(dict)   # (unit, sector, item, geo) -> {year: value}
for r in lire("eurostat_gov_10a_main.csv"):
    if r["value"] in ("", None):
        continue
    MAIN[(r["unit"], r["sector"], r["na_item"], r["geo"])][int(r["time"])] = float(r["value"])

def pib(geo, y):
    """PIB implicite (Md EUR) = TE en millions / TE en % du PIB."""
    a = MAIN[("MIO_EUR", "S13", "TE", geo)].get(y)
    b = MAIN[("PC_GDP", "S13", "TE", geo)].get(y)
    return a / b * 100 / 1000 if a and b else None

def ea_hors_fr_pct(item, y, sector="S13"):
    """Ratio de la zone euro hors France, pondere par le PIB : (EA - FR)/(PIB_EA - PIB_FR)."""
    ea = MAIN[("MIO_EUR", sector, item, "EA20")].get(y)
    fr = MAIN[("MIO_EUR", sector, item, "FR")].get(y)
    if ea is None or fr is None:
        return None
    return (ea - fr) / 1000 / (pib("EA20", y) - pib("FR", y)) * 100

# ------------------------------------------------------------------ 1. Ecarts par nature, 2024 et 2025
log("=== 1. Ecarts de depense par nature (S13), France contre zone euro hors France, % du PIB")
items = [("TE", "depense totale"), ("D1PAY", "remuneration des salaries"), ("P2", "consommation intermediaire"),
         ("D62PAY", "prestations sociales en especes"), ("D632PAY", "prestations sociales en nature (marchandes)"),
         ("D3PAY", "subventions"), ("P51G", "investissement"), ("D41PAY", "interets"), ("TR", "recettes totales")]
lignes = []
for y in (2019, 2024, 2025):
    for it, lib in items:
        fr = MAIN[("PC_GDP", "S13", it, "FR")].get(y)
        eh = ea_hors_fr_pct(it, y)
        ea = MAIN[("PC_GDP", "S13", it, "EA20")].get(y)
        if fr is None:
            continue
        lignes.append(dict(annee=y, poste=it, libelle=lib, france=fr, zone_euro_avec_FR=ea,
                           zone_euro_hors_FR=eh, ecart_hors_FR=(fr - eh) if eh is not None else None))
        log(f"  {y} {it:8s} {lib:45s} FR {fr:5.1f}  EA {ea if ea is None else round(ea,1)}  EA-horsFR {eh if eh is None else round(eh,2)}  ecart {None if eh is None else round(fr-eh,2)}")
ecrire("a16_ecarts_nature.csv", lignes)

# ------------------------------------------------------------------ 2. COFOG, ratios recales sur le PIB a jour
log("=== 2. Ecarts par fonction (COFOG), France contre zone euro hors France, % du PIB, ratios recales")
EXP = collections.defaultdict(dict)
for r in lire("eurostat_gov_10a_exp.csv"):
    if r["value"] in ("", None):
        continue
    EXP[(r["cofog99"], r["geo"])][int(r["time"])] = float(r["value"])
FONCT = {"GF01": "services generaux", "GF0107": " dont interets", "GF02": "defense", "GF03": "ordre et securite",
         "GF04": "affaires economiques", "GF05": "environnement", "GF06": "logement et equipements collectifs",
         "GF07": "sante", "GF08": "loisirs, culture, culte", "GF09": "enseignement", "GF10": "protection sociale",
         "GF1002": " dont vieillesse"}
lignes = []
for y in (2022, 2023, 2024):
    res = {}
    for geo in ("FR", "EA20"):
        # facteur de recalage : TE (main, a jour) / TOTAL (cofog)
        k = MAIN[("PC_GDP", "S13", "TE", geo)][y] / EXP[("TOTAL", geo)][y]
        res[geo] = {c: EXP[(c, geo)][y] * k for c in list(FONCT) + ["TOTAL"]}
    pf, pe = pib("FR", y), pib("EA20", y)
    tot_ecart = 0
    for c, lib in list(FONCT.items()) + [("TOTAL", "TOTAL")]:
        fr = res["FR"][c]
        eh = (res["EA20"][c] * pe - fr * pf) / (pe - pf)
        lignes.append(dict(annee=y, fonction=c, libelle=lib.strip(), france=fr, zone_euro_hors_FR=eh, ecart=fr - eh))
        if y == 2024:
            log(f"  {y} {c:7s} {lib:38s} FR {fr:5.2f}  EA-horsFR {eh:5.2f}  ecart {fr-eh:+5.2f}")
    # agregats
    d = {l["fonction"]: l["ecart"] for l in lignes if l["annee"] == y}
    hors_soc = d["TOTAL"] - d["GF10"] - d["GF07"]
    hors_soc_int = hors_soc - d["GF0107"]
    log(f"  {y} ecart total {d['TOTAL']:.2f} ; protection sociale + sante {d['GF10']+d['GF07']:.2f} "
        f"({(d['GF10']+d['GF07'])/d['TOTAL']*100:.0f} %) ; reste {hors_soc:.2f} ; reste hors interets {hors_soc_int:.2f} ; "
        f"services generaux hors interets + affaires economiques {d['GF01']-d['GF0107']+d['GF04']:.2f}")
ecrire("a16_ecarts_cofog.csv", lignes)

# ------------------------------------------------------------------ 3. Impot sur les societes
log("=== 3. Impots sur le revenu des societes (D51B, % du PIB), France et zone euro")
TAX = collections.defaultdict(dict)
for r in lire("eurostat_gov_10a_taxag.csv"):
    if r["value"] in ("", None):
        continue
    TAX[(r["na_item"], r["geo"])][int(r["time"])] = float(r["value"])
lignes = []
for y in range(2012, 2026):
    l = dict(annee=y)
    for geo in ("FR", "EA20", "DE"):
        for it in ("D51B", "D51A", "D2", "D61", "D2_D5_D91_D61_M_D995"):
            l[f"{it}_{geo}"] = TAX[(it, geo)].get(y)
    lignes.append(l)
    log(f"  {y} IS FR {l['D51B_FR']}  EA {l['D51B_EA20']}  DE {l['D51B_DE']} | prelevements FR {l['D2_D5_D91_D61_M_D995_FR']}")
ecrire("a16_impot_societes.csv", lignes)

# ------------------------------------------------------------------ 4. Table France (A07) : cliquet et volume
T = {}
with open(os.path.join(R, "donnees", "A07", "table_france_1974_2025.csv"), encoding="utf-8") as h:
    for r in csv.DictReader(h, delimiter=";"):
        d = {}
        for k, v in r.items():
            try:
                d[k] = float(v)
            except (ValueError, TypeError):
                d[k] = None
        T[int(r["annee"])] = d

def prim(y):
    """Depense primaire en % du PIB = depenses - interets verses."""
    x = T[y]
    return x["depenses_pct"] - x["interets_verses_mdeur"] / x["pib_mdeur"] * 100

log("=== 4a. Test du cliquet : depense primaire et recettes (% du PIB) autour des crises")
lignes = []
for c in (1975, 1993, 2009, 2020):
    for off in (-1, 0, 3, 5):
        y = c + off
        if y in T and y <= 2025:
            lignes.append(dict(crise=c, annee=y, decalage=off, depense_primaire=prim(y), recettes=T[y]["recettes_pct"],
                               solde_primaire=T[y]["solde_primaire_pct"]))
    sub = {l["decalage"]: l for l in lignes if l["crise"] == c}
    s = f"  crise {c}: "
    for off in (-1, 0, 3, 5):
        if off in sub:
            s += f"t{off:+d} dep.prim {sub[off]['depense_primaire']:.1f} rec {sub[off]['recettes']:.1f} | "
    log(s)
ecrire("a16_cliquet.csv", lignes)

log("=== 4b. Croissance en volume de la depense primaire (deflateur du PIB), 1976-2025")
lignes = []
for y in range(1976, 2026):
    a, b = T[y], T[y - 1]
    if a["deflateur_pib_pct"] is None:
        continue
    dp = prim(y) * a["pib_mdeur"]
    dp0 = prim(y - 1) * b["pib_mdeur"]
    nom = (dp / dp0 - 1) * 100
    vol = ((1 + nom / 100) / (1 + a["deflateur_pib_pct"] / 100) - 1) * 100
    lignes.append(dict(annee=y, depense_primaire_pct=prim(y), croiss_nominale_dep_prim=nom, deflateur=a["deflateur_pib_pct"],
                       croiss_volume_dep_prim=vol, croiss_reelle_pib=a["croiss_reelle_pct"]))
ecrire("a16_volume_depense_primaire.csv", lignes)
for l in lignes:
    if l["annee"] >= 1995:
        log(f"  {l['annee']} vol {l['croiss_volume_dep_prim']:+.2f} %  PIB reel {l['croiss_reelle_pib']}  ratio {l['depense_primaire_pct']:.1f}")
def moy(a, b):
    v = [l["croiss_volume_dep_prim"] for l in lignes if a <= l["annee"] <= b]
    return sum(v) / len(v)
for a, b in ((1976, 1985), (1986, 1995), (1996, 2007), (2010, 2019), (2011, 2017), (2015, 2019), (2022, 2025)):
    log(f"  moyenne {a}-{b} : {moy(a,b):+.2f} %/an")
n0 = [l["annee"] for l in lignes if l["annee"] >= 1995 and l["croiss_volume_dep_prim"] <= 0.0]
n5 = [l["annee"] for l in lignes if l["annee"] >= 1995 and l["croiss_volume_dep_prim"] <= 0.5]
log("  annees 1995-2025 avec volume <= 0 :", n0)
log("  annees 1995-2025 avec volume <= 0,5 % :", n5)

log("=== 4c. Meme calcul, hors mesures d'urgence et de relance 2020-2024 (Cour des comptes, juillet 2024, via A03 :")
log("    72,5 / 83,7 / 34,9 / 12,4 Md EUR en 2020-2023 ; 2024 pris a 0, l'energie etant quasi nulle en net, K-025)")
URG = {2019: 0.0, 2020: 72.5, 2021: 83.7, 2022: 34.9, 2023: 12.4, 2024: 0.0, 2025: 0.0}
for y in range(2020, 2026):
    a, b = T[y], T[y - 1]
    dp = prim(y) * a["pib_mdeur"] / 100 - URG[y]
    dp0 = prim(y - 1) * b["pib_mdeur"] / 100 - URG[y - 1]
    vol = ((dp / dp0) / (1 + a["deflateur_pib_pct"] / 100) - 1) * 100
    log(f"  {y} volume hors urgence {vol:+.2f} %")
log("  NB : 2013-2019 contiennent le CICE en depense (jusqu'a 1,74 pt en 2017, A05) : 2018 (-0,72 %) est pour l'essentiel")
log("  un artefact de reclassement (regle de donnees n° 6) ; non neutralise faute de serie annuelle du CICE dans la cellule.")

with open(os.path.join(OUT, "a16_sortie_donnees.txt"), "w", encoding="utf-8") as h:
    h.write("\n".join(LOG))
