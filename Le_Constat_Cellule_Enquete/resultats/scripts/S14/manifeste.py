"""Régénère donnees/S14/MANIFESTE_PIECES.csv (fichier ; url_origine ; canal ; date ; octets ; sha256).
Les URL d'origine sont tenues dans le dictionnaire ORIGINES ci-dessous.
Usage : python -I manifeste.py"""
import hashlib, os, csv

D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S14"
ORIGINES = {
    "TH_CPO_vIPP_synthese.pdf": "https://www.ipp.eu/wp-content/uploads/2023/12/TH_CPO_vIPP_synthese.pdf",
    "TH_CPO_vIPP_vdef_compressed.pdf": "https://www.ipp.eu/wp-content/uploads/2023/12/TH_CPO_vIPP_vdef_compressed.pdf",
    "suppression-taxe-habitation-et-reallocation-fiscalite-locale-ipp-octobre-2020.pdf": "https://www.ipp.eu/wp-content/uploads/2020/10/suppression-taxe-habitation-et-reallocation-fiscalite-locale-ipp-octobre-2020.pdf",
    "FPS2020-D2.pdf": "https://insee.fr/fr/statistiques/fichier/4797668/FPS2020-D2.pdf",
    "FPORSOC24-D1.pdf": "https://www.insee.fr/fr/statistiques/fichier/8242411/FPORSOC24-D1.pdf",
    "FPORSOC24-D1.xlsx": "https://www.insee.fr/fr/statistiques/fichier/8242411/FPORSOC24-D1.xlsx",
}
EXTRA = os.path.join(D, "origines_supplementaires.csv")  # nom;url ajoutés au fil de l'eau
if os.path.exists(EXTRA):
    for l in open(EXTRA, encoding="utf-8"):
        if ";" in l:
            n, u = l.strip().split(";", 1)
            ORIGINES[n] = u
src = os.path.join(D, "sources")
with open(os.path.join(D, "MANIFESTE_PIECES.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["fichier", "url_origine", "canal", "date", "octets", "sha256"])
    for n in sorted(os.listdir(src)):
        p = os.path.join(src, n)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        w.writerow([n, ORIGINES.get(n, "INCONNUE"), "curl -L -A Mozilla/5.0", "2026-11-21", os.path.getsize(p), h])
        print(n, ORIGINES.get(n, "INCONNUE")[:60])
