"""Télécharge une pièce dans donnees/S10/sources, ajoute une ligne au manifeste,
extrait le texte (PDF -> .txt page par page). Usage : python -I get_piece.py URL NOM [--grep mot1,mot2]"""
import sys, os, hashlib, datetime, requests, re

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S10"
SRC = os.path.join(RACINE, "sources")
MAN = os.path.join(RACINE, "MANIFESTE_PIECES.csv")

def main():
    url, nom = sys.argv[1], sys.argv[2]
    grep = sys.argv[4].split(",") if len(sys.argv) > 4 and sys.argv[3] == "--grep" else []
    os.makedirs(SRC, exist_ok=True)
    chemin = os.path.join(SRC, nom)
    canal = "requests (python)"
    if not os.path.exists(chemin):
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
        r.raise_for_status()
        with open(chemin, "wb") as f:
            f.write(r.content)
    else:
        canal = "curl -L -A Mozilla/5.0"  # fichier déjà déposé par curl
    deja = os.path.exists(MAN) and any(l.startswith(nom + ";") for l in open(MAN, encoding="utf-8"))
    if not deja:
        data = open(chemin, "rb").read()
        sha = hashlib.sha256(data).hexdigest()
        neuf = not os.path.exists(MAN)
        with open(MAN, "a", encoding="utf-8") as f:
            if neuf:
                f.write("fichier;url_origine;canal;date;octets;sha256\n")
            f.write(f"{nom};{url};{canal};{datetime.date(2026,11,21)};{len(data)};{sha}\n")
    print("OK", chemin, os.path.getsize(chemin))
    if nom.lower().endswith(".pdf"):
        import fitz
        doc = fitz.open(chemin)
        txt = os.path.join(SRC, nom[:-4] + ".txt")
        with open(txt, "w", encoding="utf-8") as f:
            for i, p in enumerate(doc):
                f.write(f"\n=== PAGE {i+1} ===\n")
                f.write(p.get_text())
        print("pages", len(doc), "->", txt)
        if grep:
            for i, p in enumerate(doc):
                t = p.get_text()
                for line in t.splitlines():
                    if any(g.lower() in line.lower() for g in grep):
                        print(f"p{i+1}: {line.strip()[:200]}")

if __name__ == "__main__":
    main()
