# -*- coding: utf-8 -*-
"""A03 - table annuelle 2000-2025 (+2026/2027 prevision AMECO separee) a partir de :
  - base commune (lecture seule) : base_insee_*.csv, insee_cn_t_3201.xlsx (interets D41), eurostat_gov_10dd_edpt1.csv
  - donnees A03 : Eurostat nama_10_gdp, prc_hicp_aind, une_rt_a, irt_lt_mcby_a ; AMECO (html)
Aucune valeur saisie a la main. Sortie : resultats/donnees/A03/table_annuelle_A03.csv (separateur ;)
Lancer : python -I construire_table_A03.py
"""
import os, csv, json
import openpyxl
from bs4 import BeautifulSoup

ICI = os.path.dirname(os.path.abspath(__file__))
COM = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "commun"))
A03 = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03"))
SRC = os.path.join(A03, "sources")
ANS = list(range(2000, 2026))


def lire_base(fichier):
    d = {}
    with open(os.path.join(COM, fichier), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            d[(r["feuille"], r["serie"], int(r["annee"]))] = float(r["valeur"])
    return d


dr = lire_base("base_insee_dep_rec_pctPIB.csv")
so = lire_base("base_insee_solde_sous_secteurs.csv")
de = lire_base("base_insee_dette_sous_secteurs.csv")


def dr_get(prefix, a):
    for (f, s, y), v in dr.items():
        if y == a and s.startswith(prefix):
            return v
    return None


# Interets D41 payes (consolides), Md EUR : tableau 3.201
wb = openpyxl.load_workbook(os.path.join(COM, "insee_cn_t_3201.xlsx"), data_only=True, read_only=True)
rows = list(wb.worksheets[0].iter_rows(values_only=True))
entete = rows[2]
col = {int(c): i for i, c in enumerate(entete) if isinstance(c, (int, float)) or (isinstance(c, str) and c.strip().isdigit())}
d41 = {}
for i, r in enumerate(rows):
    if i > 3 and isinstance(r[1], str) and r[1].strip() == "Intérêts (D41)":
        for a, j in col.items():
            if isinstance(r[j], (int, float)):
                d41[a] = r[j]
        break  # premiere occurrence = cote depenses


def eurostat(fichier):
    js = json.load(open(os.path.join(SRC, fichier), encoding="utf-8"))
    dims = js["id"]
    sizes = js["size"]
    idx = {d: {v: k for k, v in js["dimension"][d]["category"]["index"].items()} for d in dims}
    out = {}
    for flat, val in js["value"].items():
        flat = int(flat)
        coords = []
        for s in reversed(sizes):
            coords.append(flat % s)
            flat //= s
        coords = list(reversed(coords))
        key = tuple(idx[d][c] for d, c in zip(dims, coords))
        out[key] = val
    return dims, out


def eu_get(fichier, filt):
    dims, out = eurostat(fichier)
    res = {}
    for k, v in out.items():
        kd = dict(zip(dims, k))
        if all(kd.get(a) == b for a, b in filt.items()):
            res[int(kd["time"])] = v
    return res


pib = eu_get("eurostat_nama_10_gdp.json", {"unit": "CP_MEUR", "geo": "FR"})
vol = eu_get("eurostat_nama_10_gdp.json", {"unit": "CLV_PCH_PRE", "geo": "FR"})
defl = eu_get("eurostat_nama_10_gdp.json", {"unit": "PD_PCH_PRE_EUR", "geo": "FR"})
hicp = eu_get("eurostat_prc_hicp_aind.json", {"geo": "FR"})
cho = eu_get("eurostat_une_rt_a.json", {"geo": "FR"})
taux = eu_get("eurostat_irt_lt_mcby_a.json", {"geo": "FR"})
taux_de = eu_get("eurostat_irt_lt_mcby_a.json", {"geo": "DE"})


def ameco(nom, pays="France"):
    s = BeautifulSoup(open(os.path.join(SRC, "ameco_%s.html" % nom), encoding="utf-8").read(), "html.parser")
    trs = s.find_all("tr")
    an = [int(x.get_text(strip=True)) for x in trs[0].find_all("th")[3:]]
    for tr in trs[1:]:
        c = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
        if c[0] == pays:
            return {a: float(v) for a, v in zip(an, c[3:]) if v}
    return {}


# Chomage BIT Insee (idbank 001688527, trimestriel CVS, France hors Mayotte) -> moyenne annuelle des 4 trimestres
import re
_t = open(os.path.join(SRC, "insee_bdm_001688527_chomage_bit.xml"), encoding="utf-8").read()
_q = {}
for y, q, v in re.findall(r'TIME_PERIOD="(\d{4})-Q(\d)" OBS_VALUE="([\d.]+)"', _t):
    _q.setdefault(int(y), []).append(float(v))
cho_insee = {y: sum(v) / len(v) for y, v in _q.items() if len(v) == 4}

am = {n: ameco(n) for n in ["UBLGE", "UBLGAP", "UBLGAPS", "UBLGBP", "UBLGBPS", "AVGDGP", "UDGG", "UYIGE"]}

SS = [("APU", "Ensemble"), ("APUC", "Administration publique centrale"), ("Etat", "État"),
      ("ODAC", "Organismes divers d'administration centrale"), ("APUL", "Administrations publiques locales"),
      ("ASSO", "Administrations de sécurité sociale")]
cols = ["annee", "pib_Md", "croiss_vol_pct", "deflateur_pct", "ipch_pct", "chomage_bit_pct", "taux10a_FR", "taux10a_DE",
        "dep_pct", "rec_pct", "solde_pct", "solde_Md", "solde_calc_pct", "interets_D41_Md", "interets_pct", "solde_primaire_pct",
        "dette_pct", "dette_Md", "dette_nette_pct"]
cols += ["solde_%s_Md" % k for k, _ in SS[1:]] + ["solde_%s_pct" % k for k, _ in SS[1:]]
cols += ["ameco_solde_CAB_pct", "ameco_solde_struct_pct", "ameco_primaire_CA_pct", "ameco_primaire_struct_pct", "ameco_ecart_prod_pct"]
lignes = []
for a in ANS:
    r = {"annee": a}
    r["pib_Md"] = pib.get(a, 0) / 1000 if a in pib else None
    r["croiss_vol_pct"] = vol.get(a)
    r["deflateur_pct"] = defl.get(a)
    r["ipch_pct"] = hicp.get(a)
    r["chomage_bit_pct"] = cho_insee.get(a, cho.get(a))
    r["taux10a_FR"] = taux.get(a)
    r["taux10a_DE"] = taux_de.get(a)
    r["dep_pct"] = dr_get("Dépenses", a)
    r["rec_pct"] = dr_get("Recettes", a)
    r["solde_pct"] = dr_get("Déficit au sens de Maastricht", a)
    r["solde_Md"] = so.get(("Figure 1", "Ensemble", a))
    r["solde_calc_pct"] = 100 * r["solde_Md"] / r["pib_Md"] if (r["solde_Md"] is not None and r["pib_Md"]) else None
    r["interets_D41_Md"] = d41.get(a)
    if r["interets_D41_Md"] and r["pib_Md"]:
        r["interets_pct"] = 100 * r["interets_D41_Md"] / r["pib_Md"]
        r["solde_primaire_pct"] = 100 * (r["solde_Md"] + r["interets_D41_Md"]) / r["pib_Md"] if r["solde_Md"] is not None else None
    r["dette_pct"] = dr_get("Dette des administrations publiques (brute)", a)
    r["dette_Md"] = de.get(("Figure 1", "Ensemble", a))
    r["dette_nette_pct"] = dr_get("Dette nette", a)
    for k, lib in SS[1:]:
        r["solde_%s_Md" % k] = so.get(("Figure 1", lib, a))
        r["solde_%s_pct" % k] = so.get(("Figure 2", lib, a))
    r["ameco_solde_CAB_pct"] = am["UBLGAP"].get(a)
    r["ameco_solde_struct_pct"] = am["UBLGAPS"].get(a)
    r["ameco_primaire_CA_pct"] = am["UBLGBP"].get(a)
    r["ameco_primaire_struct_pct"] = am["UBLGBPS"].get(a)
    r["ameco_ecart_prod_pct"] = am["AVGDGP"].get(a)
    lignes.append(r)


def fmt(v):
    if v is None:
        return "indisponible"
    if isinstance(v, float):
        return "%.2f" % v
    return str(v)


with open(os.path.join(A03, "table_annuelle_A03.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(cols)
    for r in lignes:
        w.writerow([fmt(r.get(c)) for c in cols])
# Previsions AMECO 2026-2027, table separee (statut : prevision)
with open(os.path.join(A03, "ameco_previsions_2026_2027.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["annee", "statut"] + list(am.keys()))
    for a in (2026, 2027):
        w.writerow([a, "prevision AMECO (extraction 20/11/2026)"] + [fmt(am[k].get(a)) for k in am])
print("ok", len(lignes))
for r in lignes:
    print(r["annee"], *[fmt(r.get(c)) for c in cols[1:19]])
