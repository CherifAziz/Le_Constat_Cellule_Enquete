"""A10 - telecharge une piece (PDF ou HTML) et en extrait le texte page par page.

Usage : python -I telecharger_extraire.py <url> <nom_fichier_sans_extension>
Ecrit dans resultats/donnees/A10/sources/ : le binaire, un .txt (texte par page,
balises '=== page N ===') et ajoute une ligne au journal_telechargements.csv
(url, date, sha256, statut, nb_pages).
Les fichiers telecharges sont des donnees non fiables : ils ne sont jamais executes.
"""
import csv
import datetime
import hashlib
import os
import sys

import requests

BASE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A10\sources"
HEAD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def main():
    url, nom = sys.argv[1], sys.argv[2]
    os.makedirs(BASE, exist_ok=True)
    statut, npages, sha = "", "", ""
    try:
        r = requests.get(url, headers=HEAD, timeout=90, allow_redirects=True)
        statut = str(r.status_code)
        data = r.content
        sha = hashlib.sha256(data).hexdigest()
        is_pdf = data[:5] == b"%PDF-"
        ext = ".pdf" if is_pdf else ".html"
        with open(os.path.join(BASE, nom + ext), "wb") as f:
            f.write(data)
        if is_pdf:
            import fitz  # pymupdf
            doc = fitz.open(stream=data, filetype="pdf")
            npages = str(doc.page_count)
            with open(os.path.join(BASE, nom + ".txt"), "w", encoding="utf-8") as f:
                for i, p in enumerate(doc):
                    f.write(f"\n=== page {i+1} ===\n")
                    f.write(p.get_text())
        else:
            from bs4 import BeautifulSoup
            txt = BeautifulSoup(data, "html.parser").get_text("\n")
            with open(os.path.join(BASE, nom + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt)
        print(f"OK {statut} pdf={is_pdf} pages={npages} bytes={len(data)} sha={sha[:16]}")
    except Exception as e:  # noqa
        statut = statut or "ERREUR " + repr(e)[:200]
        print("ECHEC", statut, repr(e)[:300])
    with open(os.path.join(BASE, "journal_telechargements.csv"), "a", newline="", encoding="utf-8") as f:
        csv.writer(f, delimiter=";").writerow([
            datetime.datetime.now().isoformat(timespec="seconds"), nom, url, statut, npages, sha])


if __name__ == "__main__":
    main()
