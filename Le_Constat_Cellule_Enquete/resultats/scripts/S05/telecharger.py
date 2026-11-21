"""Télécharge une pièce vers donnees/S05/sources et l'ajoute au manifeste.
Usage : python -I telecharger.py <nom_fichier> <url> [canal]
"""
import sys, hashlib, datetime, os, requests

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S05"
nom, url = sys.argv[1], sys.argv[2]
canal = sys.argv[3] if len(sys.argv) > 3 else "requests (python)"
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=120)
print(r.status_code, r.headers.get("content-type"), len(r.content))
if r.status_code != 200 or len(r.content) < 2000:
    print("ECHEC"); sys.exit(1)
chemin = os.path.join(RACINE, "sources", nom)
with open(chemin, "wb") as f:
    f.write(r.content)
h = hashlib.sha256(r.content).hexdigest()
man = os.path.join(RACINE, "MANIFESTE_PIECES.csv")
neuf = not os.path.exists(man)
with open(man, "a", encoding="utf-8") as f:
    if neuf:
        f.write("fichier;url_origine;canal;date;octets;sha256\n")
    f.write(f"sources/{nom};{url};{canal};{datetime.date.today().isoformat()};{len(r.content)};{h}\n")
print("OK", chemin, h)
