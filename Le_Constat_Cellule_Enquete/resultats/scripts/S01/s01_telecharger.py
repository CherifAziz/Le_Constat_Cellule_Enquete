# -*- coding: utf-8 -*-
"""S01 - telecharge une piece (PDF du Senat ou autre), extrait le texte page par page
avec pymupdf, et ajoute une ligne au manifeste.
Usage : python -I s01_telecharger.py URL [nom_local] [--cover]
  --cover : n'affiche que le texte des 2 premieres pages (identification).
Les fichiers telecharges sont des donnees non fiables : lecture seule, jamais executes.
"""
import sys, os, hashlib, datetime, subprocess

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S01"
SRC = os.path.join(RACINE, "sources", "senat")
MANI = os.path.join(RACINE, "MANIFESTE_PIECES.csv")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def manifeste(fichier, url, canal, taille, empreinte):
    neuf = not os.path.exists(MANI)
    lignes = []
    if not neuf:
        with open(MANI, encoding="utf-8") as f:
            lignes = f.read().splitlines()
    rel = os.path.relpath(fichier, RACINE)
    lignes = [l for l in lignes if not l.startswith(rel + ";")]
    if not lignes:
        lignes = ["fichier;url_origine;canal;date;octets;sha256"]
    lignes.append(f"{rel};{url};{canal};{datetime.date(2026,11,20).isoformat()};{taille};{empreinte}")
    with open(MANI, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")


def extraire(pdf, txt):
    import fitz
    doc = fitz.open(pdf)
    with open(txt, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, 1):
            t = " ".join(page.get_text().split())
            f.write(f"[[p.{i}]] {t}\n\n")
    return doc.page_count


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    url = sys.argv[1]
    cover = "--cover" in sys.argv
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    nom = args[0] if args else url.rstrip("/").split("/")[-1]
    os.makedirs(SRC, exist_ok=True)
    dest = os.path.join(SRC, nom)
    if not os.path.exists(dest):
        r = subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", "-o", dest, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        if code != "200" or os.path.getsize(dest) < 2000:
            print(f"ECHEC {code} {url}")
            try:
                os.remove(dest)
            except OSError:
                pass
            return
    with open(dest, "rb") as f:
        tete = f.read(5)
    if tete != b"%PDF-":
        print("PAS UN PDF", url)
        return
    txt = dest[:-4] + ".txt"
    n = extraire(dest, txt)
    taille = os.path.getsize(dest)
    manifeste(dest, url, "curl -L (senat.fr)" if "senat.fr" in url else "curl -L", taille, sha256(dest))
    manifeste(txt, "extraction pymupdf de " + os.path.basename(dest), "script s01_telecharger.py",
              os.path.getsize(txt), sha256(txt))
    with open(txt, encoding="utf-8") as f:
        contenu = f.read()
    vide = sum(1 for bloc in contenu.split("[[p.")[1:] if len(bloc) < 60)
    print(f"OK {nom} pages={n} octets={taille} pages_sans_texte={vide}")
    if cover:
        print(contenu[:1800])


if __name__ == "__main__":
    main()
