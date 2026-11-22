"""Extrait le texte des PDF de ../../donnees/D03/sources (une page par ligne, marqueur [[p.N]])
et met à jour MANIFESTE_PIECES.csv (fichier;url;date_acces;sha256;description).
Les adresses et descriptions viennent de ../../donnees/D03/sources/_origines.csv (fichier;url;description).
Usage : python -I d03_extraire.py"""
import csv
import hashlib
from pathlib import Path

import fitz  # pymupdf

ICI = Path(__file__).resolve().parent
SRC = ICI.parent.parent / "donnees" / "D03" / "sources"
MAN = SRC.parent / "MANIFESTE_PIECES.csv"
DATE = "2026-11-22"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    orig = {}
    of = SRC / "_origines.csv"
    if of.exists():
        with of.open(encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter=";"):
                orig[r["fichier"]] = r
    rows = []
    for pdf in sorted(SRC.glob("*.pdf")):
        txt = pdf.with_suffix(".txt")
        if not txt.exists():
            doc = fitz.open(pdf)
            lines = []
            for i, page in enumerate(doc, 1):
                t = " ".join(page.get_text().split())
                lines.append(f"[[p.{i}]] {t}")
            txt.write_text("\n".join(lines), encoding="utf-8")
        o = orig.get(pdf.name, {})
        rows.append([f"sources/{pdf.name}", o.get("url", ""), DATE, sha(pdf), o.get("description", "")])
        rows.append([f"sources/{txt.name}", f"extraction pymupdf (d03_extraire.py) de {pdf.name}", DATE, sha(txt),
                     "texte extrait, une page par ligne, marqueur [[p.N]] = page du PDF"])
    for other in sorted(SRC.iterdir()):
        if other.suffix.lower() == ".pdf" or other.name == "_origines.csv":
            continue
        if other.suffix.lower() == ".txt" and other.with_suffix(".pdf").exists():
            continue
        o = orig.get(other.name, {})
        rows.append([f"sources/{other.name}", o.get("url", ""), DATE, sha(other), o.get("description", "")])
    with MAN.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["fichier", "url", "date_acces", "sha256", "description"])
        w.writerows(rows)
    print(f"{len(rows)} lignes au manifeste")


if __name__ == "__main__":
    main()
