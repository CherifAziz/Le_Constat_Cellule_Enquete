# S06 - Génère resultats/donnees/S06/MANIFESTE_PIECES.csv (fichier ; url_origine ; canal ; date ; octets ; sha256)
# Lancer : python -I s06_manifeste.py
import csv, hashlib, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S06"
SRC = os.path.join(R, "sources")
D = "2026-11-20"
ORIG = {
    "cour2019_synthese_fraude_PO.pdf": ("https://web.archive.org/web/20260107174123id_/https://www.ccomptes.fr/sites/default/files/2023-10/20191202-synthese-fraude-aux-prelevements-obligatoires.pdf", "curl via web.archive.org (ccomptes.fr injoignable ; vie-publique.fr renvoie une page anti-robot)"),
    "hcfips_2026_note_fraude_sociale.pdf": ("https://www.strategie-plan.gouv.fr/files/files/Publications/2026/2026-01-13%20-%20HCFiPS%20-%20note%20annuelle%20fraude%20sociale/Note%20annuelle%20de%20suivi%20et%20d%27%C3%A9valuation%20des%20fraudes%20sociales%20VF.pdf", "curl"),
    "fs2017_tdb_emploi_public.pdf": ("https://www.strategie.gouv.fr/files/2025-01/tdb-emploi-public-20-12-2017.pdf", "curl"),
    "solidaires_fp_2024_lettre_deputes.pdf": ("https://solidaires.org/documents/8251/240903_Solidaires_Finances_Publiques_Lettre_aux_d%C3%A9put%C3%A9s.pdf", "curl"),
    "dgfip_dp_bilan_controle_fiscal_2025_via_ifrap.pdf": ("https://www.ifrap.org/sites/default/files/documents/2026-04/540_-_dp_-_bilan_du_controle_fiscal_2025.pdf", "curl (copie du dossier de presse DGFiP hébergée par l'Ifrap : canal tiers)"),
    "ce_swd_2025_france_ST16801_ADD10.pdf": ("https://data.consilium.europa.eu/doc/document/ST-16801-2025-ADD-10/en/pdf", "curl"),
    "senat_l25-736-233_RS_affaires_europeennes_exec2025.pdf": ("https://www.senat.fr/rap/l25-736-233/l25-736-2331.pdf", "curl"),
    "senat_NP_affaires_europeennes_PLF2027.pdf": ("https://www.senat.fr/fileadmin/cru-1792598966/Commissions/Finances/2026-2027/PLF_2027/NP/NP_Affaires_europeennes_PLF_2027.pdf", "curl"),
    "ce_eu_budget_spending_revenue_2000-2025.xlsx": ("https://commission.europa.eu/document/download/9f334bee-d097-4b68-8f93-2225eabeb631_en?filename=eu_budget_spending_and_revenue_2000-2025.xlsx", "curl (URL trouvée par WebFetch sur la page Commission « spending and revenue »)"),
    "insee_2018-09-06_CP_revisions_deficit_dette_SNCFReseau.pdf": ("https://www.insee.fr/fr/statistiques/fichier/version-html/3607979/2018-09-06_CP_Insee_%20publication_rev_deficit_dette_APU.pdf", "curl"),
    "insee_revision_ratios_FP_B2020_mars2024.pdf": ("https://www.insee.fr/fr/statistiques/documentation/revision_ratios_finance_publique_B2020_mars_20240325.pdf", "curl"),
    "insee_IR165_dette_1T2023_EDF.pdf": ("https://www.insee.fr/fr/statistiques/fichier/version-html/7638614/IR165_Dette_1T23.pdf", "curl"),
    "an_QE31812_leg12_cout_defaisance_CDR.pdf": ("https://www.assemblee-nationale.fr/dyn/12/questions/QANR5L12QE31812.pdf", "curl"),
    "cepii_wp2018-04_impact_budgetaire_immigration.pdf": ("http://www.cepii.fr/PDF_PUB/wp/2018/wp2018-04.pdf", "curl"),
    "cepii_lettre394_2018.pdf": ("http://www.cepii.fr/PDF_PUB/lettre/2018/let394.pdf", "curl"),
    "cae_focus072_immigration.pdf": ("https://cae-eco.fr/static/pdf/cae-focus072.pdf", "curl"),
    "senat_l25-736-221_RS_CAS_PFE_exec2025.pdf": ("https://www.senat.fr/rap/l25-736-221/l25-736-2211.pdf", "curl"),
    "an_cr_cesecu2526030_immigration.pdf": ("https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/cesecu/l17cesecu2526030_compte-rendu.pdf", "curl"),
}
rows = []
for fn in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, fn)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    url, canal = ORIG.get(fn, ("INCONNU", "?"))
    rows.append([fn, url, canal, D, os.path.getsize(p), h])
with open(os.path.join(R, "MANIFESTE_PIECES.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["fichier", "url_origine", "canal", "date", "octets", "sha256"])
    w.writerows(rows)
for r in rows:
    print(r[0], r[4], r[1][:40])
