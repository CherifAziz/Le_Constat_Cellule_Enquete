# -*- coding: utf-8 -*-
"""A07 - Manifeste de toutes les pieces conservees dans donnees/A07/sources (nom, taille, SHA-256, origine).
Usage : python -I 09_manifeste_sources.py <dossier A07/sources>
L'origine (URL et canal) est reprise du journal de telechargement quand elle y figure, sinon d'une table
ecrite a la main ci-dessous pour les pieces obtenues par WebFetch ou derivees (texte extrait, PNG rendu).
"""
import sys, os, csv, hashlib
S = sys.argv[1]
ORIG = {
    "budget_gouv_33772.pdf": ("https://www.budget.gouv.fr/documentation/file-download/33772", "requests (Python)"),
    "ec_autumn2026_ip348.pdf": ("https://economy-finance.ec.europa.eu/document/download/e6bb4d2e-5c46-44e6-a716-6624a57494f3_en?filename=ip348_en.pdf", "requests"),
    "ec_DSM2025_ip332.pdf": ("https://economy-finance.ec.europa.eu/document/download/39b3b61d-42c1-46d7-8088-0aad82e8731e_en?filename=ip332_en.pdf", "requests"),
    "bdf_RA2025_presentation.pdf": ("https://www.banque-france.fr/fr/system/files/2026-03/Rapport-annuel_2025_presentation.pdf", "WebFetch (binaire enregistre par l'outil, copie)"),
    "ecb_letter_Aubry_20210528.pdf": ("https://www.ecb.europa.eu/pub/pdf/other/ecb.mepletter210528_Aubry~7f065130cc.en.pdf", "WebFetch (binaire enregistre par l'outil, copie)"),
    "ecb_letter_Aubry_20210205_fr.pdf": ("https://www.ecb.europa.eu/ecb/access_to_documents/document/correspondence/shared/data/ecb.dr.cor20210205Aubry.fr.pdf", "requests"),
    "bnpp_cout_annulation_dette_20210219.pdf": ("https://economic-research.bnpparibas.com/pdf/fr-FR/cout-annulation-dette-publique-debat-suscite-19/02/2021,41805", "requests"),
    "senat_ta1972_1973_0007.pdf": ("https://www.senat.fr/leg/1972-1973/ta1972_1973_0007.pdf", "requests"),
    "senat_ta1972_1973_0043.pdf": ("https://www.senat.fr/leg/1972-1973/ta1972_1973_0043.pdf", "requests"),
    "senat_i1992_1993_0404.pdf": ("https://www.senat.fr/rap/1992-1993/i1992_1993_0404.pdf", "requests"),
    "laviedesidees_20140701_etat_livre_aux_financiers.pdf": ("https://laviedesidees.fr/IMG/pdf/20140701_l_etat_livre_aux_financiers__.pdf", "requests"),
    "floden_2012_cepr_dp9095.pdf": ("https://martinfloden.net/files/Floden%20M%20-%20CEPR%202012%20DP%209095.pdf", "requests"),
    "ecb_PSPP_breakdown_history.csv": ("https://www.ecb.europa.eu/mopo/pdf/PSPP_breakdown_history.csv", "requests"),
    "ecb_PEPP_public_sector_breakdown_history.csv": ("https://www.ecb.europa.eu/mopo/pdf/PEPP_public_sector_securities_breakdown_history.csv", "requests"),
    "ecb_pepp_page.html": ("https://www.ecb.europa.eu/mopo/implement/pepp/html/index.en.html", "requests"),
    "ecb_app_page.html": ("https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html", "requests"),
    "eurostat_gov_10dd_ggd.json": ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10dd_ggd?format=JSON&lang=EN&geo=FR&geo=IT&geo=DE&geo=ES&geo=BE&unit=PC_GDP&sector=S13&na_item=GD", "requests"),
    "aft_key_figures_archive.html": ("https://web.archive.org/web/20251009044338id_/https://www.aft.gouv.fr/en/debt-key-figures", "requests (archive d'octobre 2025)"),
}
journal = {}
jp = os.path.join(S, "journal_telechargements.csv")
if os.path.exists(jp):
    for r in csv.reader(open(jp, encoding="utf-8")):
        if len(r) >= 4 and str(r[3]) == "200":
            journal[r[0]] = (r[1], "requests (journal)")
rows = []
for fn in sorted(os.listdir(S)):
    p = os.path.join(S, fn)
    if not os.path.isfile(p) or fn == "MANIFESTE_A07.csv":
        continue
    b = open(p, "rb").read()
    base = fn
    if fn.endswith(".txt") or fn.endswith(".csv") and fn.startswith("eurostat_") or fn.endswith(".png"):
        src = ("derive localement (texte extrait par pymupdf, CSV converti par le script 02, ou rendu PNG)", "derive")
    else:
        src = ORIG.get(fn) or journal.get(fn) or ("voir journal_telechargements.csv / extraits_pieces_web.md", "")
    if fn.startswith("AFT_BM_") and fn.endswith(".pdf"):
        src = journal.get(fn, ("https://www.aft.gouv.fr/files/medias-aft/...", "requests"))
    rows.append([fn, len(b), hashlib.sha256(b).hexdigest(), src[0], src[1]])
with open(os.path.join(S, "MANIFESTE_A07.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["fichier", "octets", "sha256", "origine", "canal"]); w.writerows(rows)
print(len(rows), "pieces")
