"""S13 : téléchargement des études, extraction du texte, manifeste.
Usage : python -I s13_telecharge.py <dossier_donnees_S13> [nom=url ...]
Sans liste, utilise PIECES ci-dessous. Ajoute au manifeste sans doublon.
"""
import sys, os, hashlib, datetime, requests, fitz

PIECES = {
    "nber_w18336_AFG2015_output_effect.pdf": "https://www.nber.org/system/files/working_papers/w18336/w18336.pdf",
    "nber_w24823_AFG2019_effects_of_austerity.pdf": "https://www.nber.org/system/files/working_papers/w24823/w24823.pdf",
    "nber_w23385_ABFGP2017_theory_evidence.pdf": "https://www.nber.org/system/files/working_papers/w23385/w23385.pdf",
    "nber_w19414_JordaTaylor_time_for_austerity.pdf": "https://www.nber.org/system/files/working_papers/w19414/w19414.pdf",
    "nber_w22374_FatasSummers_permanent_effects.pdf": "https://www.nber.org/system/files/working_papers/w22374/w22374.pdf",
    "nber_w23147_HPT_austerity_aftermath.pdf": "https://www.nber.org/system/files/working_papers/w23147/w23147.pdf",
    "nber_w17571_Perotti_austerity_myth.pdf": "https://www.nber.org/system/files/working_papers/w17571/w17571.pdf",
}

def main():
    out = sys.argv[1]
    pieces = dict(a.split("=", 1) for a in sys.argv[2:]) or PIECES
    src = os.path.join(out, "sources"); ext = os.path.join(out, "extraits")
    man = os.path.join(out, "MANIFESTE_PIECES.csv")
    if not os.path.exists(man):
        with open(man, "w", encoding="utf-8") as f:
            f.write("fichier;url_origine;canal;date;octets;sha256\n")
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for nom, url in pieces.items():
        p = os.path.join(src, nom)
        try:
            r = requests.get(url, headers=h, timeout=90)
            ok = r.status_code == 200 and r.content[:4] == b"%PDF"
            print(nom, r.status_code, len(r.content), "PDF" if ok else r.content[:60])
            if not ok:
                continue
            open(p, "wb").write(r.content)
        except Exception as e:
            print(nom, "ERREUR", e); continue
        d = fitz.open(p)
        with open(os.path.join(ext, nom[:-4] + ".txt"), "w", encoding="utf-8") as f:
            for i, pg in enumerate(d):
                f.write(f"\n=== page {i+1} ===\n" + pg.get_text())
        print("   pages", d.page_count)
        sha = hashlib.sha256(r.content).hexdigest()
        with open(man, "a", encoding="utf-8") as f:
            f.write(f"{nom};{url};python requests;{datetime.date.today()};{len(r.content)};{sha}\n")

if __name__ == "__main__":
    main()
