# -*- coding: utf-8 -*-
"""S01 - telecharge les tables IPP (baremes.ipp.eu) des taux de cotisation du regime general
et de l'assurance chomage, et extrait les lignes (date d'effet, taux, reference) de 1970 a 2000.
Sortie : donnees/S01/S01_taux_cotisations_ipp_1970_2000.csv ; pages HTML dans sources/ipp/.
Usage : python -I s01_ipp_taux.py
"""
import os, re, sys, subprocess, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S01"
SRC = os.path.join(R, "sources", "ipp")
os.makedirs(SRC, exist_ok=True)
BASE = "https://baremes.ipp.eu/parameters/prelevements-sociaux/prelevements_sociaux.{}/table"
PARAMS = [
    "cotisations_securite_sociale_regime_general.mmid.employeur.maladie",
    "cotisations_securite_sociale_regime_general.mmid.salarie.maladie",
    "cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_plafonnee",
    "cotisations_securite_sociale_regime_general.cnav.employeur.vieillesse_deplafonnee",
    "cotisations_securite_sociale_regime_general.cnav.salarie.vieillesse_plafonnee",
    "cotisations_securite_sociale_regime_general.cnav.salarie.vieillesse_deplafonnee",
    "cotisations_securite_sociale_regime_general.famille.employeur.famille",
    "cotisations_regime_assurance_chomage.chomage.employeur.chomage",
    "cotisations_regime_assurance_chomage.chomage.salarie.chomage",
]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s01_telecharger import manifeste, sha256  # noqa: E402

lignes = ["parametre;date_effet;valeurs;reference;url"]
for p in PARAMS:
    url = BASE.format(p)
    dest = os.path.join(SRC, p.replace(".", "_") + ".html")
    if not os.path.exists(dest):
        subprocess.run(["curl", "-s", "-L", "-A", "Mozilla/5.0", "-o", dest, url])
    manifeste(dest, url, "curl -L (baremes.ipp.eu)", os.path.getsize(dest), sha256(dest))
    t = open(dest, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    s = re.sub(r"<[^>]+>", " | ", s)
    s = re.sub(r"(\s*\|\s*)+", " | ", s)
    s = re.sub(r"\s+", " ", s)
    # blocs commencant par une date d'effet jj/mm/aaaa
    blocs = re.split(r"\|\s(?=\d\d/\d\d/(?:19|20)\d\d\s\|)", s)
    for b in blocs:
        m = re.match(r"(\d\d/\d\d/(\d{4}))\s\|(.*)", b)
        if not m:
            continue
        an = int(m.group(2))
        if 1970 <= an <= 2000:
            corps = m.group(3).strip(" |")
            vals = re.findall(r"-?\d+(?:,\d+)?\s?%", corps)
            ref = re.sub(r"-?\d+(?:,\d+)?\s?%", "", corps)
            ref = re.sub(r"\s*\|\s*", " / ", ref).strip(" /")[:160].replace(";", ",")
            lignes.append(f"{p};{m.group(1)};{' '.join(vals)};{ref};{url}")
            print(p.split(".")[-2] + "." + p.split(".")[-1], m.group(1), vals, ref[:90])
with open(os.path.join(R, "S01_taux_cotisations_ipp_1970_2000.csv"), "w", encoding="utf-8") as g:
    g.write("\n".join(lignes) + "\n")
