# -*- coding: utf-8 -*-
"""A07 - Telechargement des bulletins mensuels de l'Agence France Tresor (fichiers PDF publics)
et de pieces budgetaires. Les pages HTML d'aft.gouv.fr refusent curl ; les fichiers /files/ repondent a requests.
Usage : python -I 06_telecharger_aft.py <dossier_sortie>
Journal : journal_telechargements.csv (meme format que 01).
"""
import sys, os, hashlib, datetime, csv, urllib.parse, requests
OUT = sys.argv[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
BASES = ["https://www.aft.gouv.fr/files/medias-aft/", "https://www.aft.gouv.fr/files/medias-aft/7_Publications/7.2_BM/"]
# numerotation observee : 429 = fevrier 2026 ; 410 = juillet 2024 ; 398 = juillet 2023 ; 367 = decembre 2020
def numero(annee, mois):
    return 429 + (annee - 2026) * 12 + (mois - 2)
WANT = [(2026, m) for m in range(3, 12)] + [(2026, 2), (2025, 12), (2024, 12), (2023, 12), (2022, 12), (2021, 12), (2020, 12), (2019, 12)]
if len(sys.argv) > 2:
    WANT = [tuple(map(int, x.split("-"))) for x in sys.argv[2:]]
log = os.path.join(OUT, "journal_telechargements.csv")
with open(log, "a", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    for a, m in WANT:
        n = numero(a, m)
        fname = f"{n}_Bulletin mensuel {MOIS[m-1]} {a}.pdf"
        got = False
        for nn in (n, n - 1, n + 1):
            fname = f"{nn}_Bulletin mensuel {MOIS[m-1]} {a}.pdf"
            for b in BASES:
                url = b + urllib.parse.quote(fname)
                ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                try:
                    r = requests.get(url, headers=UA, timeout=120)
                    code, data = r.status_code, r.content
                except Exception as e:
                    code, data = "ERR:" + type(e).__name__, b""
                ok = code == 200 and data[:4] == b"%PDF"
                w.writerow([f"AFT_BM_{a}_{m:02d}.pdf", url, ts, code, len(data), hashlib.sha256(data).hexdigest() if ok else ""])
                if ok:
                    open(os.path.join(OUT, f"AFT_BM_{a}_{m:02d}.pdf"), "wb").write(data)
                    print(a, m, "OK", url); got = True; break
            if got:
                break
        if not got:
            print(a, m, "introuvable")
