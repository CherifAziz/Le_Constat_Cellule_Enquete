# -*- coding: utf-8 -*-
"""
Controle de provenance par l'orchestrateur.
Re-telecharge a l'ORIGINE (independamment des agents) les pieces qui portent les
constats les plus lourds, puis compare taille et SHA-256 avec la copie locale de l'agent.
Pour les pages HTML (contenu variable), verifie la presence de chaines-cles.

Sortie : resultats/donnees/commun/controle_provenance/RAPPORT.csv
Usage  : python -I controle_provenance.py
"""
import csv
import datetime as dt
import hashlib
import os
import re
import sys

import requests

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
D = os.path.join(R, "donnees", "commun", "controle_provenance")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"}

# (identifiant, url d'origine, copie locale de l'agent, chaines a retrouver si HTML)
PIECES = [
    ("HCFP avis 2026-5 (via archive web)",
     "https://web.archive.org/web/20261021215439id_/http://www.hcfp.fr/sites/default/files/2026-10/Avis%20HCFP%202026-5%20-%20PLF-PLFSS%202027.pdf",
     r"donnees\A03\sources\HCFP_avis_2026-5.pdf", None),
    ("RESF annexe au PLF 2027 (Tresor)",
     "https://www.tresor.economie.gouv.fr/Articles/03454e04-445d-4ce6-832b-cff601a11485/files/56839f98-37fc-48d8-b502-81cac5a48cad",
     r"donnees\A03\sources\PLF2027_RESF.pdf", None),
    ("Cour des comptes juillet 2024 (via vie-publique.fr)",
     "https://www.vie-publique.fr/files/rapport/pdf/294882.pdf",
     r"donnees\A04\sources\cour_RSPFP_juillet2024_vp294882.pdf", None),
    ("COR rapport annuel 2026",
     "https://www.cor-retraites.fr/sites/default/files/2026-06/RA_2026_def.pdf",
     r"donnees\A06\sources\COR_RA_2026.pdf", None),
    ("Commission, previsions d'automne 2026",
     "https://economy-finance.ec.europa.eu/document/download/e6bb4d2e-5c46-44e6-a716-6624a57494f3_en?filename=ip348_en.pdf",
     r"donnees\A01\sources\ce_automne2026_ip348.pdf", None),
    ("Senat, synthese r24-153",
     "https://www.senat.fr/rap/r24-153/r24-153-syn.pdf",
     r"donnees\A03\sources\senat_r24-153_syn.pdf", None),
    ("Senat, rapport n 133 (1975-1976)",
     "https://www.senat.fr/rap/1975-1976/i1975_1976_0133.pdf",
     r"donnees\A02\sources\senat\i1975_1976_0133.pdf", None),
    ("Assemblee, seance du 4 novembre 2026 (HTML)",
     "https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/seance/session-ordinaire-de-2026-2027/deuxieme-seance-du-mercredi-04-novembre-2026",
     r"donnees\A03\sources\AN_CR_2e_seance_2026-11-04.html",
     [r"Pour l.adoption\s*0\s*Contre\s*458", r"5,9\s*%"]),
    ("Insee Premiere 2106 (HTML)",
     "https://www.insee.fr/fr/statistiques/8997691",
     r"donnees\A01\sources\insee_ip2106.html",
     [r"23,0\s*Md", r"152,5"]),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def texte_html(b):
    t = re.sub(rb"<[^>]+>", b" ", b)
    return re.sub(r"\s+", " ", t.decode("utf-8", "replace"))


def main():
    os.makedirs(D, exist_ok=True)
    horo = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lignes = []
    for nom, url, local, chaines in PIECES:
        chemin_local = os.path.join(R, local)
        loc = open(chemin_local, "rb").read() if os.path.exists(chemin_local) else None
        try:
            r = requests.get(url, headers=UA, timeout=120, allow_redirects=True)
            statut = r.status_code
            contenu = r.content if statut == 200 else b""
        except Exception as e:
            statut, contenu = f"ERREUR {type(e).__name__}", b""
        verdict = ""
        if not contenu:
            verdict = "origine non obtenue"
        elif loc is None:
            verdict = "copie locale absente"
        elif chaines is None:
            if sha(contenu) == sha(loc):
                verdict = "IDENTIQUE (meme SHA-256)"
            else:
                verdict = f"DIFFERENT (tailles {len(contenu)} / {len(loc)})"
        else:
            to, tl = texte_html(contenu), texte_html(loc)
            res = []
            for c in chaines:
                res.append(f"{c}: origine={'oui' if re.search(c, to) else 'NON'}, copie={'oui' if re.search(c, tl) else 'NON'}")
            verdict = "HTML ; " + " | ".join(res)
        if contenu:
            ext = ".html" if chaines else ".pdf"
            with open(os.path.join(D, re.sub(r"[^A-Za-z0-9]+", "_", nom)[:60] + ext), "wb") as f:
                f.write(contenu)
        lignes.append([nom, url, local, horo, statut, len(contenu), sha(contenu)[:16] if contenu else "",
                       len(loc) if loc else "", sha(loc)[:16] if loc else "", verdict])
        print(nom, "->", statut, "|", verdict)
    with open(os.path.join(D, "RAPPORT.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["piece", "url_origine", "copie_agent", "date_controle", "statut_http", "octets_origine",
                    "sha256_origine_16", "octets_copie", "sha256_copie_16", "verdict"])
        w.writerows(lignes)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
