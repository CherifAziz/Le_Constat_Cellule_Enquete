# -*- coding: utf-8 -*-
"""
Cellule d'enquete Le Constat - infrastructure commune (orchestrateur).
Telecharge les fichiers bruts officiels (Insee, Eurostat) dans resultats/donnees/commun/
et ecrit un manifeste (URL, date d'extraction UTC, taille, SHA-256, statut HTTP).

Aucune transformation n'est faite sur les fichiers Insee (xlsx conserves tels quels).
Les reponses Eurostat (JSON-stat 2.0) sont conservees brutes ET aplaties en CSV.

Usage :  python telecharger_series_communes.py
Reproductible : relancer le script cree un nouveau manifeste date ; les fichiers
precedents sont ecrases (les millesimes sont identifies par la date d'extraction).
"""
import csv
import datetime as dt
import hashlib
import itertools
import json
import os
import sys

import requests

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "donnees", "commun"))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) recherche-documentaire"}

INSEE = {
    # nom local : URL
    "insee_dep_rec_serie_longue.xlsx": "https://www.insee.fr/fr/statistiques/fichier/2381414/econ-fin-pub-rec-dep.xlsx",
    "insee_solde_par_sous_secteur.xlsx": "https://www.insee.fr/fr/statistiques/fichier/2381402/econ-fin-pub-deficit-secteur.xlsx",
    "insee_dette_par_sous_secteur.xlsx": "https://www.insee.fr/fr/statistiques/fichier/2830192/econ-fin-pub-dette-adm-pub.xlsx",
    "insee_ip2106_compte_apu_2025.xlsx": "https://www.insee.fr/fr/statistiques/fichier/8997691/ip2106.xlsx",
}
for n in range(3201, 3218):
    INSEE[f"insee_cn_t_{n}.xlsx"] = f"https://www.insee.fr/fr/statistiques/fichier/8988845/t_{n}_fr.xlsx"

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
GEO = ["FR", "DE", "IT", "ES", "NL", "BE", "SE", "DK", "FI", "AT", "PT", "EL", "IE", "EA20", "EU27_2020"]
EUROSTAT = {
    # Notification PDE : solde, dette, PIB, interets (toutes annees disponibles)
    "eurostat_gov_10dd_edpt1": ("gov_10dd_edpt1", {"sector": ["S13"], "geo": GEO}),
    # Comptes principaux des APU : depenses, recettes, solde, interets, par sous-secteur
    "eurostat_gov_10a_main": ("gov_10a_main", {
        "geo": GEO,
        "sector": ["S13", "S1311", "S1312", "S1313", "S1314"],
        "na_item": ["TE", "TR", "B9", "D41PAY", "D62PAY", "D632PAY", "D1PAY", "P2", "P51G", "D3PAY", "D2REC", "D5REC", "D61REC", "D91REC"],
        "unit": ["PC_GDP", "MIO_EUR"],
    }),
    # COFOG : depenses par fonction (niveau 1 et 2), en % du PIB
    "eurostat_gov_10a_exp": ("gov_10a_exp", {"geo": GEO, "sector": ["S13"], "na_item": ["TE"], "unit": ["PC_GDP"]}),
    # Impots et cotisations sociales (indicateurs agreges)
    "eurostat_gov_10a_taxag": ("gov_10a_taxag", {"geo": GEO, "sector": ["S13_S212"], "unit": ["PC_GDP"]}),
}


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def aplatir_jsonstat(js):
    """JSON-stat 2.0 -> liste de dict (une ligne par observation)."""
    ids = js["id"]
    tailles = js["size"]
    dims = []
    for d in ids:
        cat = js["dimension"][d]["category"]
        index = cat["index"]
        if isinstance(index, dict):
            codes = sorted(index, key=lambda k: index[k])
        else:
            codes = list(index)
        dims.append(codes)
    valeurs = js.get("value", {})
    statuts = js.get("status", {})
    lignes = []
    for pos, combo in enumerate(itertools.product(*dims)):
        cle = str(pos)
        if isinstance(valeurs, dict):
            if cle not in valeurs:
                continue
            v = valeurs[cle]
        else:
            v = valeurs[pos]
            if v is None:
                continue
        ligne = dict(zip(ids, combo))
        ligne["value"] = v
        ligne["status"] = statuts.get(cle, "") if isinstance(statuts, dict) else ""
        lignes.append(ligne)
    assert len(dims) == len(tailles)
    return lignes


def main():
    os.makedirs(RACINE, exist_ok=True)
    horodatage = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifeste = []

    for nom, url in INSEE.items():
        chemin = os.path.join(RACINE, nom)
        try:
            r = requests.get(url, headers=UA, timeout=90)
            statut = r.status_code
            if statut == 200:
                with open(chemin, "wb") as f:
                    f.write(r.content)
                manifeste.append([nom, url, horodatage, statut, len(r.content), sha256(chemin), r.headers.get("Last-Modified", "")])
            else:
                manifeste.append([nom, url, horodatage, statut, 0, "", ""])
        except Exception as e:  # consigner l'echec, ne rien inventer
            manifeste.append([nom, url, horodatage, f"ERREUR {type(e).__name__}", 0, "", ""])
        print(manifeste[-1][:5])

    for nom, (code, filtres) in EUROSTAT.items():
        params = [("format", "JSON"), ("lang", "EN"), ("freq", "A")]
        for k, vals in filtres.items():
            for v in vals:
                params.append((k, v))
        chemin_json = os.path.join(RACINE, nom + ".json")
        chemin_csv = os.path.join(RACINE, nom + ".csv")
        try:
            r = requests.get(EUROSTAT_BASE + code, params=params, headers=UA, timeout=180)
            statut = r.status_code
            url_finale = r.url
            if statut == 200:
                with open(chemin_json, "wb") as f:
                    f.write(r.content)
                js = r.json()
                lignes = aplatir_jsonstat(js)
                champs = list(js["id"]) + ["value", "status"]
                with open(chemin_csv, "w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=champs)
                    w.writeheader()
                    w.writerows(lignes)
                maj = js.get("updated", "")
                manifeste.append([nom + ".json", url_finale, horodatage, statut, len(r.content), sha256(chemin_json), f"Eurostat updated={maj}"])
                manifeste.append([nom + ".csv", "derive de " + nom + ".json", horodatage, "derive", os.path.getsize(chemin_csv), sha256(chemin_csv), f"{len(lignes)} observations"])
            else:
                manifeste.append([nom + ".json", url_finale, horodatage, statut, 0, "", r.text[:200].replace("\n", " ")])
        except Exception as e:
            manifeste.append([nom + ".json", EUROSTAT_BASE + code, horodatage, f"ERREUR {type(e).__name__}: {e}"[:200], 0, "", ""])
        print(manifeste[-1][:5])

    with open(os.path.join(RACINE, "MANIFESTE.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fichier", "url", "date_extraction_utc", "statut_http", "taille_octets", "sha256", "info_millesime"])
        w.writerows(manifeste)
    echecs = [m for m in manifeste if m[3] not in (200, "derive")]
    print(f"\n{len(manifeste)} entrees, {len(echecs)} echec(s). Manifeste : {os.path.join(RACINE, 'MANIFESTE.csv')}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
