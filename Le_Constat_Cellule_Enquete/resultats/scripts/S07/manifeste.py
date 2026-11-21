"""S07 - écrit MANIFESTE_PIECES.csv (fichier;url_origine;canal;date;octets;sha256)
pour chaque fichier de sources\\ et copies_codex\\.
Usage : python -I manifeste.py <dossier_donnees_S07>"""
import sys, os, hashlib, csv

base = sys.argv[1]
URL = {
 "cour_rspfp_2016-06.pdf": ("https://web.archive.org/web/2016id_/https://www.ccomptes.fr/sites/default/files/EzPublish/20160629-rapport-situation-perspectives-finances-publiques.pdf", "curl via web.archive.org (Cour lue via un tiers)"),
 "imf_wp1301_blanchard_leigh.pdf": ("https://web.archive.org/web/2013id_/https://www.imf.org/external/pubs/ft/wp/2013/wp1301.pdf", "curl via web.archive.org"),
 "ec_ip040_portugal_expost.pdf": ("https://economy-finance.ec.europa.eu/system/files/2022-08/ip040_en.pdf", "curl"),
 "senat_l13-716-11_PLR2013.pdf": ("https://www.senat.fr/rap/l13-716-1/l13-716-11.pdf", "curl"),
 "an_r2069-tI_PLR2013.pdf": ("https://www.assemblee-nationale.fr/14/pdf/rapports/r2069-tI.pdf", "curl"),
 "an_r1210-tI_PLR2012.pdf": ("https://www.assemblee-nationale.fr/14/pdf/rapports/r1210-tI.pdf", "curl"),
 "an_r0075-tI_PLR2011.pdf": ("https://www.assemblee-nationale.fr/14/pdf/rapports/r0075-tI.pdf", "curl"),
 "an_r2921-tI_PLR2014.pdf": ("https://www.assemblee-nationale.fr/14/pdf/rapports/r2921-tI.pdf", "curl (texte non extractible)"),
 "senat_l14-604-11_PLR2014.pdf": ("https://www.senat.fr/rap/l14-604-1/l14-604-11.pdf", "curl"),
 "ofce_blog_quel_impact.html": ("https://web.archive.org/web/2016id_/http://www.ofce.sciences-po.fr/blog/quel-impact-de-la-politique-budgetaire-sur-la-croissance-francaise/", "curl via web.archive.org"),
 "ofce_blog_contretemps.html": ("https://web.archive.org/web/2016id_/http://www.ofce.sciences-po.fr/blog/des-politiques-budgetaires-restrictives-a-contretemps/", "curl via web.archive.org"),
 "ofce_2016-FR-01.pdf": ("https://ofce.sciences-po.fr/pdf/ouvrage/2016-FR-01.pdf", "curl"),
 "ofce_2015-FR-01.pdf": ("https://ofce.sciences-po.fr/pdf/ouvrage/2015-FR-01.pdf", "curl"),
 "ec_ecp506_intveld_2013.pdf": ("https://ec.europa.eu/economy_finance/publications/economic_paper/2013/pdf/ecp506_en.pdf", "curl"),
 "ec_ip004_ireland_expost.pdf": ("https://ec.europa.eu/dgs/economy_finance/evaluation/pdf/ex-post_ireland_en.pdf", "curl"),
 "imf_cr13156_greece_expost.pdf": ("https://web.archive.org/web/2013id_/https://www.imf.org/external/pubs/ft/scr/2013/cr13156.pdf", "curl via web.archive.org"),
 "ec_ip019_spain_expost.pdf": ("https://ec.europa.eu/dgs/economy_finance/evaluation/pdf/spain_final_report_en.pdf", "curl"),
 "insee_G2010-03_mesange.pdf": ("https://insee.fr/en/statistiques/fichier/1380858/G2010-03.pdf", "curl"),
 "glp.pdf": ("copie de C:\\Users\\oussa\\Downloads\\Le_Constat_Cellule_Enquete\\resultats\\codex\\preuves_audit\\glp.pdf (origine IMF WP/11/158)", "copie locale lecture seule"),
 "imf_wp11158_glp_archive.pdf": ("https://web.archive.org/web/2011id_/https://www.imf.org/external/pubs/ft/wp/2011/wp11158.pdf", "curl via web.archive.org"),
}
for k in ("pib_vol_pct", "dette_pct_pib", "depenses_pct_pib", "recettes_pct_pib", "solde_pct_pib"):
    URL[f"eurostat_{k}.json"] = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ (voir scripts\\S07\\eurostat_programmes.py pour les paramètres)", "requests (API Eurostat)")
rows = []
for sub in ("sources", "copies_codex"):
    dd = os.path.join(base, sub)
    if not os.path.isdir(dd):
        continue
    for fn in sorted(os.listdir(dd)):
        fp = os.path.join(dd, fn)
        b = open(fp, "rb").read()
        u, c = URL.get(fn, ("?", "?"))
        rows.append([f"{sub}\\{fn}", u, c, "2026-11-21", len(b), hashlib.sha256(b).hexdigest()])
with open(os.path.join(base, "MANIFESTE_PIECES.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["fichier", "url_origine", "canal", "date", "octets", "sha256"])
    w.writerows(rows)
for r in rows:
    print(r[0], r[4], r[5][:16])
