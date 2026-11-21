# A18 - retéléchargement des pièces primaires à leur adresse d'origine (ou archive) + comparaison d'empreinte
# Usage : python -I a18_06_telecharge_pieces.py <dossier_sources_A18> <manifeste.csv> <racine_donnees> <liste.tsv>
# liste.tsv : fichier \t url \t copie_existante_relative (facultatif)
import sys, os, hashlib, datetime, requests, time
src, man, racine, liste = sys.argv[1:5]
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
with open(man, "a", encoding="utf-8") as m:
    for line in open(liste, encoding="utf-8"):
        if not line.strip() or line.startswith("#"): continue
        parts = line.rstrip("\n").split("\t")
        fn, url = parts[0], parts[1]
        copie = parts[2] if len(parts) > 2 else ""
        p = os.path.join(src, fn)
        if os.path.exists(p):
            print("deja", fn); continue
        try:
            r = requests.get(url, headers=H, timeout=180)
            b = r.content; st = r.status_code
        except Exception as ex:
            print("ECHEC", fn, ex); m.write(f"{fn};{url};ECHEC {type(ex).__name__};{datetime.datetime.now():%Y-%m-%d %H:%M};0;\n"); continue
        if st != 200 or len(b) < 1000:
            print("ECHEC", fn, st, len(b)); m.write(f"{fn};{url};ECHEC HTTP {st};{datetime.datetime.now():%Y-%m-%d %H:%M};{len(b)};\n"); continue
        open(p, "wb").write(b)
        h = hashlib.sha256(b).hexdigest()
        comp = ""
        if copie:
            cp = os.path.join(racine, copie)
            if os.path.exists(cp):
                hc = hashlib.sha256(open(cp, "rb").read()).hexdigest()
                comp = " ; copie cellule %s %s" % (copie, "IDENTIQUE" if hc == h else "DIFFERENTE (%d o)" % os.path.getsize(cp))
        canal = "requests HTTP 200" + comp
        m.write(f"{fn};{url};{canal};{datetime.datetime.now():%Y-%m-%d %H:%M};{len(b)};{h}\n")
        print(fn, st, len(b), comp)
        time.sleep(1)
