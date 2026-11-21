"""A12 - manifeste des pieces (consignes communes v1.1, sec. 5).

Ecrit donnees\\A12\\MANIFESTE_PIECES.csv : fichier ; url_origine ; canal ; date ; octets ; sha256
une ligne par fichier de donnees\\A12\\sources\\ (sous-dossiers compris). Les origines sont tenues a la main
ci-dessous (journal de la mission) ; un fichier sans origine connue est signale "origine non renseignee".
Usage : python -I a12_99_manifeste.py
"""
import csv, hashlib, os, datetime

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(RACINE, "donnees", "A12", "sources")
OUT = os.path.join(RACINE, "donnees", "A12", "MANIFESTE_PIECES.csv")
EO = "https://sdmx.oecd.org/public/rest/data/OECD.ECO.MAD,DSD_EO@DF_EO,/"
ORIG = {
    "oecd_eo119_finpub.csv": (EO + ".NLGQ+NLGXQ+GGFLQ+GGFLMQ+NLGQA+NLGXQA+YPGTQ+YRGTQ+UNR+IRL+GDPV_ANNPCT+GGINTPQ+IGAA.A?startPeriod=1960&format=csvfilewithlabels", "curl (API SDMX OCDE)", "2026-11-20"),
    "oecd_eo119_macro.csv": (EO + ".EXCH+XMKT+XGSV+GDP+CPI_YTYPCT+CBGDPR+IRS+PCORE_YTYPCT.A?startPeriod=1960&format=csvfilewithlabels", "python urllib (a12_00)", "2026-11-20"),
    "oecd_eo119_interets.csv": (EO + ".GGINTP+GGINTR+NLG.A?startPeriod=1960&format=csvfilewithlabels", "curl (API SDMX OCDE)", "2026-11-20"),
    "imf_cr98124_sweden_selected_issues.pdf": ("https://www.imf.org/external/pubs/ft/scr/1998/cr98124.pdf", "WebFetch (curl 403) ; PDF scanne lu en images", "2026-11-20"),
    "persson_1995_kcfed_JH95.pdf": ("https://www.kansascityfed.org/documents/6818/Persson_JH95.PDF", "WebFetch (curl : echec de connexion)", "2026-11-20"),
    "persson_1995_kcfed_JH95.txt": ("extrait local de persson_1995_kcfed_JH95.pdf (pymupdf)", "extraction locale", "2026-11-20"),
    "oecd_PUMA_SBO_98_5_REV1.pdf": ("https://one.oecd.org/document/PUMA/SBO(98)5/REV1/en/pdf (lu via https://web.archive.org/web/20240224130141id_/https://one.oecd.org/document/PUMA/SBO(98)5/REV1/en/pdf)", "curl sur Wayback (one.oecd.org : 403 curl et WebFetch)", "2026-11-20"),
    "oecd_PUMA_SBO_98_5_REV1.txt": ("extrait local de oecd_PUMA_SBO_98_5_REV1.pdf", "extraction locale", "2026-11-20"),
    "swe_skr_2025_26_76.pdf": ("https://www.government.se/contentassets/afd79a1ff8954c78b7681f6a8fa6c8e1/the-fiscal-policy-framework-skr.-20252676.pdf", "curl", "2026-11-20"),
    "swe_skr_2025_26_76.txt": ("extrait local de swe_skr_2025_26_76.pdf", "extraction locale", "2026-11-20"),
    "swe_convergence_programme_1998_2001.pdf": ("https://regeringen.se/contentassets/bb70ca16dc184a3eaa49bccdb9d2389c/swedens-convergence-programme-1998-2001", "WebFetch", "2026-11-20"),
    "swe_convergence_programme_1998_2001.txt": ("extrait local de swe_convergence_programme_1998_2001.pdf", "extraction locale", "2026-11-20"),
    "imf_wp11128_devries_et_al_2011.pdf": ("https://www.imf.org/external/pubs/ft/wp/2011/wp11128.pdf", "WebFetch", "2026-11-20"),
    "imf_wp11128_devries_et_al_2011.txt": ("extrait local de imf_wp11128_devries_et_al_2011.pdf", "extraction locale", "2026-11-20"),
    "extrait_devries2011_episodes.md": ("extrait automatique A12 de imf_wp11128_devries_et_al_2011.txt", "extraction locale", "2026-11-20"),
    "ec_pt_201611_executive_summary.pdf": ("https://ec.europa.eu/dgs/economy_finance/evaluation/pdf/pt_201611_executive_summary_en.pdf", "curl", "2026-11-20"),
    "ec_pt_201611_executive_summary.txt": ("extrait local de ec_pt_201611_executive_summary.pdf", "extraction locale", "2026-11-20"),
    "imf_wp1301_blanchard_leigh_2013.pdf": ("https://www.imf.org/external/pubs/ft/wp/2013/wp1301.pdf", "WebFetch", "2026-11-20"),
    "imf_wp1301_blanchard_leigh_2013.txt": ("extrait local de imf_wp1301_blanchard_leigh_2013.pdf", "extraction locale", "2026-11-20"),
    "nber_w19414_jorda_taylor.pdf": ("https://www.nber.org/system/files/working_papers/w19414/w19414.pdf", "curl", "2026-11-20"),
    "nber_w19414_jorda_taylor.txt": ("extrait local de nber_w19414_jorda_taylor.pdf", "extraction locale", "2026-11-20"),
    "imf_cr13156_greece_ex_post.pdf": ("https://www.imf.org/external/pubs/ft/scr/2013/cr13156.pdf", "WebFetch", "2026-11-20"),
    "imf_cr13156_greece_ex_post.txt": ("extrait local de imf_cr13156_greece_ex_post.pdf", "extraction locale", "2026-11-20"),
    "afg_jep_2019.pdf": ("https://pubs.aeaweb.org/doi/pdfplus/10.1257/jep.33.2.141", "curl : 403, page HTML d'erreur conservee (ce n'est PAS l'article)", "2026-11-20"),
}


def main():
    rows = []
    for dp, _, fs in os.walk(SRC):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, SRC).replace("\\", "/")
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            if rel.startswith("imf_pages/"):
                o = ("rendu local (pymupdf) d'une page de imf_cr98124_sweden_selected_issues.pdf", "extraction locale", "2026-11-20")
            else:
                o = ORIG.get(rel, ("origine non renseignee", "", datetime.date.fromtimestamp(os.path.getmtime(p)).isoformat()))
            rows.append({"fichier": rel, "url_origine": o[0], "canal": o[1], "date": o[2], "octets": os.path.getsize(p), "sha256": h})
    with open(OUT, "w", newline="", encoding="utf-8") as hh:
        w = csv.DictWriter(hh, fieldnames=list(rows[0].keys()), delimiter=";"); w.writeheader(); w.writerows(rows)
    print("ok", len(rows), "; sans origine :", [r["fichier"] for r in rows if r["url_origine"] == "origine non renseignee"])


if __name__ == "__main__":
    main()
