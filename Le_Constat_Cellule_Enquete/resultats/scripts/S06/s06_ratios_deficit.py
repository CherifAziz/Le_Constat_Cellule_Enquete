# S06 - Rapport de chaque estimation au déficit 2025 (151,6 Md€) ; calculs C-S06-001, 003, 004.
# Lancer : python -I s06_ratios_deficit.py
# Entrées : base commune (Eurostat gov_10a_main.csv, Insee t_3201.xlsx), sources S06 (xlsx Commission).
# Sortie : resultats/donnees/S06/synthese_ratios_deficit.csv
import csv, os, sys, warnings
warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import openpyxl
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
COM = os.path.join(R, "donnees", "commun")
SRC = os.path.join(R, "donnees", "S06", "sources")
OUT = os.path.join(R, "donnees", "S06", "synthese_ratios_deficit.csv")

# C-S06-001 : PIB 2025 = TE (Md€) / TE (% PIB) ; TE plutôt que B9 car le ratio B9 (5,1 %) est arrondi
# (erreur relative jusqu'à 1 %) alors que TE (57,3 %) donne une erreur < 0,1 %.
d = {}
for r in csv.DictReader(open(os.path.join(COM, "eurostat_gov_10a_main.csv"), encoding="utf-8")):
    if r["sector"] == "S13" and r["geo"] == "FR" and r["na_item"] in ("TE", "B9") and r["value"]:
        d[(r["unit"], r["na_item"], r["time"])] = float(r["value"])
pib = {y: d[("MIO_EUR", "TE", y)] / d[("PC_GDP", "TE", y)] * 100 / 1000 for y in ("2017", "2019", "2025")}
DEF = 151.6
SEUIL = 0.10 * DEF
print(f"PIB 2025 (via TE) = {pib['2025']:.1f} Md€ ; B9 2025 = {d[('MIO_EUR','B9','2025')]/1000:.1f} Md€ ; déficit = {DEF/pib['2025']*100:.2f} % PIB ; seuil 10 % = {SEUIL:.2f} Md€ = {SEUIL/pib['2025']*100:.2f} pt PIB")

# C-S06-003 : UE, données Commission (feuilles 2017, 2019, 2025 ; colonne FR)
wb = openpyxl.load_workbook(os.path.join(SRC, "ce_eu_budget_spending_revenue_2000-2025.xlsx"), read_only=True, data_only=True)
ue = {}
for y in ("2017", "2019", "2025"):
    rows = list(wb[y].iter_rows(values_only=True))
    j = [k for k, c in enumerate(rows[2]) if c == "FR"][0]
    vals = {}
    for r in rows:
        lab = " ".join(" ".join(str(c) for c in r[:2] if c is not None).split())
        vals.setdefault(lab, r[j])
    exp = vals.get("TOTAL EXPENDITURE")
    if y == "2025":
        contrib = sum(vals[k] for k in ["Own resources based on VAT", "Own resources based on GNI", "Gross reduction in the annual GNI-based contribution granted to certain Member States", "Own resources based on plastic packaging waste not recycled", "TOTAL Balances and adjustments"])
        gni = vals.get("Gross National Income (GNI), EUR million****")
        ngeu = vals.get("TOTAL NGEU")
    else:
        contrib = vals.get("TOTAL national contribution")
        gni = [v for k, v in vals.items() if k.startswith("Gross National Income")][0]
        ngeu = 0
    ue[y] = (exp / 1000, contrib / 1000, gni / 1000, (ngeu or 0) / 1000)
    print(f"UE {y}: dépenses en FR {exp/1000:.2f} ; contribution nationale {contrib/1000:.2f} ({contrib/gni*100:.2f} % RNB) ; solde {(exp-contrib)/1000:.2f} ; NGEU {(ngeu or 0)/1000:.2f}")

# Insee 3.201 : transferts en capital versés (D9p hors D995p)
ws = openpyxl.load_workbook(os.path.join(COM, "insee_cn_t_3201.xlsx"), read_only=True, data_only=True).active
rows = list(ws.iter_rows(values_only=True))
years = rows[2]
for r in rows:
    if r[1] and str(r[1]).startswith("Transferts en capital") and "payer" in str(r[1]):
        print("D9p hors D995p :", {years[k]: round(r[k], 1) for k in range(len(r)) if years[k] in (2015, 2016, 2017, 2018, 2019, 2025)})

# Estimations (Md€ ou % PIB d'origine) -> % du déficit 2025
P = pib["2025"]
est = [
    # cause, id, libellé, montant_Md€ (positif = aggrave le déficit), note
    ("immigration", "F-S06-001", "OCDE niv.1 (+1 pt PIB, excédent)", -0.01 * P, "transposé : % PIB 2006-2017 x PIB 2025"),
    ("immigration", "F-S06-002", "OCDE niv.2 (≈0)", 0.0, ""),
    ("immigration", "F-S06-003", "OCDE niv.3 (-0,9 pt PIB, tout imputé)", 0.009 * P, "transposé"),
    ("immigration", "F-S06-005", "OID 40 Md€", 40.0, "niveau de preuve E"),
    ("immigration", "F-S06-006", "Cepii référence 2011 (-0,49 % PIB)", 0.0049 * P, "transposé ; année la plus défavorable"),
    ("immigration", "F-S06-006b", "Cepii 2nd génération 1989 (-1,01 % PIB)", 0.0101 * P, "transposé ; année la moins défavorable du scénario"),
    ("immigration", "F-S06-006c", "Cepii 2nd génération 2011 (-1,64 % PIB)", 0.0164 * P, "transposé"),
    ("immigration", "F-S06-006d", "Cepii 2nd gén. + biens publics aux natifs 2011 (-0,96 % PIB)", 0.0096 * P, "transposé"),
    ("immigration", "F-S06-006e", "Cepii biens publics aux natifs 2011 (+0,02 % PIB)", -0.0002 * P, "transposé"),
    ("immigration", "F-S06-008", "OCDE : gain emploi aligné", 4.6, "récupérable"),
    ("fraude", "F-S06-010", "Solidaires bas (80)", 80.0, "niveau de preuve E"),
    ("fraude", "F-S06-010b", "Solidaires haut (100)", 100.0, "niveau de preuve E"),
    ("fraude", "F-S06-011", "TVA Cour-Insee (15)", 15.0, "enquête 2019"),
    ("fraude", "F-S06-012", "Écart TVA Commission 2023 (12)", 12.0, ""),
    ("fraude", "F-S06-015", "Fraude sociale HCFiPS (14)", 14.0, ""),
    ("fraude", "C-S06-006", "Somme basse TVA Commission + social HCFiPS", 26.0, "partielle : hors IR, IS"),
    ("fraude", "C-S06-007", "Somme haute Solidaires + social", 114.0, ""),
    ("fraude", "F-S06-018", "Fiscal notifié 2025", 17.1, "notifié"),
    ("fraude", "F-S06-019", "Fiscal encaissé 2025", 11.4, "déjà dans les recettes"),
    ("fraude", "F-S06-020", "Social recouvré 2024", 0.68, "déjà dans les recettes"),
    ("UE", "F-S06-030", "PSR-UE brut 2025", 23.0, ""),
    ("UE", "F-S06-031", "PSR-UE prévision 2026", 28.118, "rapporté au déficit 2025"),
    ("UE", "F-S06-034", "Solde net comptable 2025", 9.5, ""),
    ("UE", "C-S06-003", "Dépenses en FR - contribution nationale 2025", ue["2025"][1] - ue["2025"][0], "hors douane, hors NGEU"),
    ("UE", "C-S06-003b", "idem avec NGEU", ue["2025"][1] - ue["2025"][0] - ue["2025"][3], ""),
    ("UE", "C-S06-003c", "Dégradation du solde 2017-2025", (ue["2025"][1] - ue["2025"][0]) - (ue["2017"][1] - ue["2017"][0]), "variation"),
    ("reprises", "F-S06-043", "Areva/Orano 2017", 4.8, "ponctuel 2017"),
    ("reprises", "F-S06-045", "Crédit lyonnais haut (non actualisé)", 14.3, "cumul ~1995-2010"),
    ("reprises", "F-S06-045b", "Crédit lyonnais Cour 2000", 20.0, "cumul, bilan patrimonial"),
    ("reprises", "F-S06-042", "Reprise SNCF Réseau 35 Md€ (effet base 2020)", 0.0, "intra-S13"),
    ("agents", "C-S06-002a", "D1 : écart ZE20 hors FR (+2,93 pt)", 87.6, "script s06_agents_publics.py"),
    ("agents", "C-S06-002b", "D1 : écart DE (+3,9 pt)", 116.7, ""),
    ("agents", "C-S06-002c", "D1+P2+D632 : écart ZE20 hors FR (+2,82 pt)", 84.5, ""),
    ("agents", "C-S06-002d", "D1+P2+D632 : écart DE (+0,2 pt)", 6.0, ""),
    ("agents", "C-S06-002e", "D1 : variation 1995-2025 (-1,1 pt)", -0.011 * P, "baisse"),
]
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["cause", "id", "libelle", "montant_Mds_EUR", "pct_deficit_2025", "au_dessus_seuil_10pct", "note"])
    for c, i, lab, m, note in est:
        pct = m / DEF * 100
        flag = "non comparable (cumul pluriannuel)" if "cumul" in note else ("oui" if m > SEUIL else "non")
        w.writerow([c, i, lab, round(m, 2), round(pct, 1), flag, note])
        print(f"{c:11s} {i:11s} {lab:48s} {m:8.2f} Md€ {pct:6.1f} %")
