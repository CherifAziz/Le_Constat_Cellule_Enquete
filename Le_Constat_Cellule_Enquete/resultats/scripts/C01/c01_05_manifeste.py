# C01 — manifeste des pièces (sources téléchargées et copies du dossier Codex)
import hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
B = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\C01"
CX = "C:/Users/oussa/Downloads/Le_Constat_Cellule_Enquete/resultats/codex/"
meta = {
 "sources/an_audition_hcfp_CRCANR5L17S2027PO59048N002.html": ("https://www.assemblee-nationale.fr/dyn/opendata/CRCANR5L17S2027PO59048N002.html", "curl (2e essai, --http1.1), HTTP 200"),
 "sources/elysee_adresse_2020-03-12.html": ("https://www.elysee.fr/emmanuel-macron/2020/03/12/adresse-aux-francais", "curl, HTTP 200"),
 "sources/eurostat_irt_lt_mcby_a.json": ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_lt_mcby_a?format=JSON&lang=EN&time=2021&time=2022&time=2023&time=2024&time=2025", "curl, API Eurostat, HTTP 200"),
 "sources/vp293446_cour_energie_2024-03.pdf": ("https://www.vie-publique.fr/files/rapport/pdf/293446.pdf", "curl, HTTP 200 (sha256 identique à la copie d'A18)"),
 "sources/swe_budget_statement_1997-98.pdf": ("https://regeringen.se/contentassets/7d86681d640044bdb24c7abb4ee7e545/the-budget-statement", "curl, HTTP 200 (sha256 identique à la copie d'A18)"),
 "sources/bdf_indices_obligataires_2026-10-22.html": ("https://www.banque-france.fr/fr/statistiques/taux-et-cours/indices-obligataires-2026-10-22", "curl HTTP 403 : page de refus sans contenu ; valeurs lues par WebFetch, non conservables"),
}
rows = []
for root, _, fs in os.walk(B):
    for f in fs:
        p = os.path.relpath(os.path.join(root, f), B).replace(os.sep, "/")
        if not (p.startswith("sources/") or p.startswith("copies_codex/")):
            continue
        b = open(os.path.join(B, p), "rb").read()
        if p in meta:
            u, c = meta[p]
        else:
            rel = p[len("copies_codex/"):]
            if rel.startswith("calculs/") or rel.endswith(".py"):
                u = CX + rel
            else:
                u = CX + "preuves_audit/" + rel
            c = "copie (cp) d'un fichier du dossier Codex, lecture seule à l'origine"
        rows.append((p, u, c, "2026-11-20", str(len(b)), hashlib.sha256(b).hexdigest()))
with open(os.path.join(B, "MANIFESTE_PIECES.csv"), "w", encoding="utf-8-sig", newline="") as w:
    w.write("fichier;url_origine;canal;date;octets;sha256\n")
    for r in sorted(rows):
        w.write(";".join(r) + "\n")
print(len(rows), "pièces")
