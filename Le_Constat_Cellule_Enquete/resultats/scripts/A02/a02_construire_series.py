# -*- coding: utf-8 -*-
"""A02 - assemble les colonnes chiffrees des fiches annuelles 1960-2000.

Entrees (lecture seule) :
  resultats/donnees/commun/base_insee_dep_rec_pctPIB.csv      (Insee base 2020, serie longue 2381414)
  resultats/donnees/commun/base_insee_solde_sous_secteurs.csv (Insee 2381402)
  resultats/donnees/commun/base_insee_dette_sous_secteurs.csv (Insee 2830192)
  resultats/donnees/commun/insee_cn_t_3201.xlsx               (Insee CN base 2020, tableau 3.201, Md EUR)
  resultats/donnees/A02/sources/insee_T_1101_1103_fr.xlsx     (Insee CN base 2020, PIB valeur/volume/prix)
  resultats/donnees/A02/sources/insee_bdm_011813530_coef_monnaie.xml (Insee BDM, coefficient de transformation de la monnaie, base 2025)
  resultats/donnees/A02/sources/insee_ECRT2026_F8_chomage.xlsx (Insee, taux de chomage BIT 1975-2025, fig. 2)
Sortie :
  resultats/donnees/A02/A02_series_1960_2000.csv (separateur ;)
Usage : python -I a02_construire_series.py <racine_resultats>
"""
import csv, re, sys, os
import openpyxl

R = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
C = os.path.join(R, "donnees", "commun")
S = os.path.join(R, "donnees", "A02", "sources")
YEARS = range(1959, 2001)


def read_flat(name):
    out = {}
    with open(os.path.join(C, name), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            try:
                out[(row["feuille"], row["serie"].strip(), int(row["annee"]))] = float(row["valeur"])
            except ValueError:
                pass
    return out


deprec = read_flat("base_insee_dep_rec_pctPIB.csv")
solde = read_flat("base_insee_solde_sous_secteurs.csv")
dette = read_flat("base_insee_dette_sous_secteurs.csv")


def g(d, feuille, serie, y):
    return d.get((feuille, serie, y))

# --- tableau 3.201 (S13, Md EUR)
wb = openpyxl.load_workbook(os.path.join(C, "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
rows = list(wb.worksheets[0].iter_rows(values_only=True))
hdr = list(rows[2])
t3201 = {}
seen = {}
for r in rows[3:66]:
    lab = (r[1] or "").strip()
    if not lab:
        continue
    seen[lab] = seen.get(lab, 0) + 1
    key = lab if seen[lab] == 1 else lab + " #%d" % seen[lab]
    for j, y in enumerate(hdr):
        if isinstance(y, int) and isinstance(r[j], (int, float)):
            t3201[(key, y)] = float(r[j])
# premiere occurrence "Interets (D41)" = depenses ; deuxieme = recettes
LAB_INT = [k for k in {k for k, _ in t3201} if k.startswith("Int") and "(D41)" in k and "hors" not in k]
int_paid_key = [k for k in LAB_INT if "#" not in k][0]
int_rec_key = [k for k in LAB_INT if "#2" in k][0]
dep_tot_key = [k for k, _ in t3201 if k.startswith("Total des d")][0]
rec_tot_key = [k for k, _ in t3201 if k.startswith("Total des recettes")][0]
b8g_key = [k for k, _ in t3201 if k.startswith("Epargne brute")][0]
b9_key = [k for k, _ in t3201 if k.startswith("Capacit")][0]
prest_key = [k for k, _ in t3201 if k.startswith("Prestations sociales autres")][0]
d1_key = [k for k, _ in t3201 if k.startswith("R") and "(D1)" in k][0]
fbcf_key = [k for k, _ in t3201 if k.startswith("Formation brute")][0]

# --- PIB (T_1101, T_1102 evolution, T_1103 evolution)
wb2 = openpyxl.load_workbook(os.path.join(S, "insee_T_1101_1103_fr.xlsx"), read_only=True, data_only=True)


def sheet_row(sheetname, code, label_start=None):
    ws = wb2[sheetname]
    rr = list(ws.iter_rows(values_only=True))
    yrs = rr[3]
    for r in rr:
        if r[0] == code and (label_start is None or (r[1] or "").strip().startswith(label_start)):
            return {int(yrs[j]): float(r[j]) for j in range(2, len(r)) if r[j] not in (None, "")}
    raise KeyError(code)

pib = sheet_row("T_1101 en niveau", "B1GQ")
pib_vol = sheet_row("T_1102 en \u00e9volution", "B1GQ")
defl = sheet_row("T_1103 en \u00e9volution", "B1GQ")
defl_conso_men = sheet_row("T_1103 en \u00e9volution", "S14B", "M\u00e9nages")

# --- IPC via coefficient de transformation de la monnaie (BDM 011813530)
s = open(os.path.join(S, "insee_bdm_011813530_coef_monnaie.xml"), encoding="utf-8").read()
coef = {int(a): float(b) for a, b in re.findall(r'TIME_PERIOD="(\d{4})" OBS_VALUE="([^"]+)"', s)}
ipc = {y: (coef[y] / coef[y - 1] - 1) * 100 for y in coef if y - 1 in coef}

# --- chomage BIT (fig. 2)
wb3 = openpyxl.load_workbook(os.path.join(S, "insee_ECRT2026_F8_chomage.xlsx"), data_only=True)
chom = {}
for r in wb3["Figure 2"].iter_rows(values_only=True):
    if isinstance(r[0], int) and isinstance(r[3], (int, float)):
        chom[r[0]] = float(r[3])

# --- AMECO (Commission europeenne, millesime 17/11/2026), chapitres 6 et 17
def ameco(fname, code):
    path = os.path.join(S, "ameco", fname)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="latin-1") as fh:
        rd = csv.reader(fh, delimiter=";")
        hdr = next(rd)
        for r in rd:
            if r[0] == code:
                return {int(h): float(v) for h, v in zip(hdr[5:], r[5:]) if h.strip().isdigit() and v not in ("", "NA")}
    return {}

ogap = ameco("AMECO6.TXT", "FRA.1.0.0.0.AVGDGP")
ca_bal = ameco("AMECO17.TXT", "FRA.1.0.319.0.UBLGAP")
cyc = ameco("AMECO17.TXT", "FRA.1.0.319.0.UBLGCP")
capb = ameco("AMECO17.TXT", "FRA.1.0.319.0.UBLGBP")

F1, F2 = "Figure 1", "Figure 2"
cols = ["annee", "ecart_production_ameco", "solde_cvs_ameco_pctpot", "composante_cyclique_ameco", "solde_primaire_cvs_ameco",
        "pib_md", "pib_vol_pct", "deflateur_pib_pct", "prix_conso_menages_cn_pct", "ipc_pct", "chomage_bit_pct",
        "dep_pct", "rec_pct", "solde_pct", "solde_md_insee", "dep_md_3201", "rec_md_3201", "b9_md_3201",
        "interets_payes_md", "interets_recus_md", "interets_payes_pct", "interets_nets_pct", "solde_primaire_pct",
        "epargne_brute_md", "epargne_brute_pct", "prestations_D62_pct", "remun_D1_pct", "fbcf_pct",
        "dette_pct", "dette_md",
        "solde_etat_md", "solde_odac_md", "solde_apuc_md", "solde_apul_md", "solde_asso_md",
        "solde_etat_pct", "solde_odac_pct", "solde_apuc_pct", "solde_apul_pct", "solde_asso_pct",
        "solde_etat_md_brut_incoherent", "solde_odac_md_brut_incoherent", "solde_etat_pct_brut_incoherent", "solde_odac_pct_brut_incoherent"]
out = []
for y in YEARS:
    P = pib.get(y)
    def pct(x):
        return None if (x is None or P is None) else 100 * x / P
    ip = t3201.get((int_paid_key, y)); ir = t3201.get((int_rec_key, y))
    sp = g(deprec, "Donn\u00e9es", "D\u00e9ficit au sens de Maastricht", y)
    row = {
        "ecart_production_ameco": ogap.get(y), "solde_cvs_ameco_pctpot": ca_bal.get(y),
        "composante_cyclique_ameco": cyc.get(y), "solde_primaire_cvs_ameco": capb.get(y),
        "annee": y, "pib_md": P, "pib_vol_pct": pib_vol.get(y), "deflateur_pib_pct": defl.get(y),
        "prix_conso_menages_cn_pct": defl_conso_men.get(y), "ipc_pct": ipc.get(y), "chomage_bit_pct": chom.get(y),
        "dep_pct": g(deprec, "Donn\u00e9es", "D\u00e9penses", y), "rec_pct": g(deprec, "Donn\u00e9es", "Recettes", y),
        "solde_pct": sp, "solde_md_insee": g(solde, F1, "Ensemble", y),
        "dep_md_3201": t3201.get((dep_tot_key, y)), "rec_md_3201": t3201.get((rec_tot_key, y)), "b9_md_3201": t3201.get((b9_key, y)),
        "interets_payes_md": ip, "interets_recus_md": ir, "interets_payes_pct": pct(ip),
        "interets_nets_pct": pct(ip - ir) if (ip is not None and ir is not None) else None,
        "solde_primaire_pct": (pct(t3201.get((b9_key, y))) + pct(ip)) if (ip is not None and t3201.get((b9_key, y)) is not None and P) else None,
        "epargne_brute_md": t3201.get((b8g_key, y)), "epargne_brute_pct": pct(t3201.get((b8g_key, y))),
        "prestations_D62_pct": pct(t3201.get((prest_key, y))), "remun_D1_pct": pct(t3201.get((d1_key, y))), "fbcf_pct": pct(t3201.get((fbcf_key, y))),
        "dette_pct": g(deprec, "Donn\u00e9es", "Dette des administrations publiques (brute)2", y), "dette_md": g(dette, F1, "Ensemble", y),
        "solde_etat_md": g(solde, F1, "\u00c9tat", y), "solde_odac_md": g(solde, F1, "Organismes divers d'administration centrale", y),
        "solde_apuc_md": g(solde, F1, "Administration publique centrale", y), "solde_apul_md": g(solde, F1, "Administrations publiques locales", y),
        "solde_asso_md": g(solde, F1, "Administrations de s\u00e9curit\u00e9 sociale", y),
        "solde_etat_pct": g(solde, F2, "\u00c9tat", y), "solde_odac_pct": g(solde, F2, "Organismes divers d'administration centrale", y),
        "solde_apuc_pct": g(solde, F2, "Administration publique centrale", y), "solde_apul_pct": g(solde, F2, "Administrations publiques locales", y),
        "solde_asso_pct": g(solde, F2, "Administrations de s\u00e9curit\u00e9 sociale", y),
    }
    # Anomalie a la source (Insee 2381402 et t_3106) : avant 1978, Etat + ODAC != APUC (ex. 1974 : -4,82 contre +1,68 Md EUR)
    # alors que APUC + APUL + ASSO = Ensemble. Valeurs Etat/ODAC 1959-1977 neutralisees ; brutes conservees a part.
    if y < 1978:
        for k in ["solde_etat_md", "solde_odac_md", "solde_etat_pct", "solde_odac_pct"]:
            row[k + "_brut_incoherent"] = row[k]
            row[k] = None
    out.append(row)

dest = os.path.join(R, "donnees", "A02", "A02_series_1960_2000.csv")
with open(dest, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=";")
    w.writeheader()
    for row in out:
        w.writerow({k: ("" if v is None else (round(v, 4) if isinstance(v, float) else v)) for k, v in row.items()})
print("ecrit", dest)
print("cles 3.201 :", int_paid_key, "|", int_rec_key, "|", b8g_key, "|", b9_key)
# controles
for row in out:
    if row["annee"] >= 1972:
        chk = None
        if row["b9_md_3201"] is not None and row["pib_md"]:
            chk = 100 * row["b9_md_3201"] / row["pib_md"]
        print(row["annee"], "PIB", row["pib_md"], "solde%", None if row["solde_pct"] is None else round(row["solde_pct"], 2),
              "B9/PIB", None if chk is None else round(chk, 2), "solde Md insee", row["solde_md_insee"], "B9 3201", row["b9_md_3201"])
