"""Eurostat JSON-stat, contrôle des comptes et réplication des tableaux A12 et A14.

python reproduire.py            # calcul hors connexion à partir des archives
python reproduire.py --actualiser  # interroge à nouveau Eurostat (modifie le millésime)
"""
import argparse
import csv
import hashlib
import itertools
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

ICI = Path(__file__).resolve().parent
PAYS = ("BE", "DE", "DK", "ES", "FR", "IT", "NL", "PT")
ANNEES = range(1995, 2026)
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
REQUETES = {
    "finances": ("gov_10a_main", dict(unit="PC_GDP", sector="S13", na_item=["B9", "TE", "TR", "D41PAY", "P51G"])),
    "finances_mio": ("gov_10a_main", dict(unit="MIO_NAC", sector="S13", na_item=["B9", "D41PAY"])),
    "dette": ("gov_10dd_edpt1", dict(unit="PC_GDP", sector="S13", na_item="GD")),
    "chomage": ("une_rt_a", dict(unit="PC_ACT", sex="T", age="Y15-74")),
    "croissance": ("nama_10_gdp", dict(unit="CLV_PCH_PRE", na_item="B1GQ")),
    "part65": ("demo_pjanind", dict(indic_de="PC_Y65_MAX")),
}


def consulter(item, actualiser):
    cle, (jeu, filtres) = item
    url = BASE + jeu + "?" + urlencode(dict(lang="en", freq="A", geo=PAYS, sinceTimePeriod=1995, untilTimePeriod=2025, **filtres), doseq=True)
    chemin = ICI / (cle + ".json")
    if actualiser:
        with urlopen(url, timeout=90) as reponse:
            donnees = reponse.read()
        obj = json.loads(donnees)
        assert obj.get("value") and len(obj["value"]) > 30, (jeu, obj.get("error"))
        chemin.write_bytes(donnees)
    donnees = chemin.read_bytes()
    obj = json.loads(donnees)
    axes = obj["id"]
    codes = []
    for axe in axes:
        ordre = obj["dimension"][axe]["category"]["index"]
        codes.append(sorted(ordre, key=ordre.get) if isinstance(ordre, dict) else ordre)
    lignes = {}
    for i, coord in enumerate(itertools.product(*codes)):
        case = dict(zip(axes, coord))
        if str(i) not in obj["value"]:
            continue
        libelle = cle
        if cle in ("finances", "finances_mio"):
            libelle = case["na_item"] + ("_MIO_NAC" if cle == "finances_mio" else "")
        lignes[(case["geo"], int(case["time"]), libelle)] = obj["value"][str(i)]
    meta = dict(jeu=jeu, url=url, updated=obj["updated"], sha256=hashlib.sha256(donnees).hexdigest())
    return lignes, meta


def enregistrer(nom, champs, lignes):
    with (ICI / nom).open("w", encoding="utf-8", newline="") as f:
        ecrivain = csv.DictWriter(f, champs)
        ecrivain.writeheader()
        ecrivain.writerows(lignes)


def panel(actualiser):
    d, provenance = {}, []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for lignes, meta in pool.map(lambda item: consulter(item, actualiser), REQUETES.items()):
            d.update(lignes)
            provenance.append(meta)
    enregistrer("provenance.csv", provenance[0], provenance)
    variables = ["B9", "TR", "TE", "D41PAY", "P51G", "dette", "chomage", "croissance", "part65", "B9_MIO_NAC", "D41PAY_MIO_NAC"]
    annuelles = []
    for p, t in itertools.product(PAYS, ANNEES):
        ligne = dict(pays=p, an=t, **{c: d.get((p, t, c)) for c in variables})
        if all(ligne[c] is not None for c in ("B9", "TR", "TE")):
            assert abs(ligne["B9"] - ligne["TR"] + ligne["TE"]) <= 0.101, ligne
        annuelles.append(ligne)
    enregistrer("panel.csv", annuelles[0], annuelles)
    fenetres = []
    for an, p in itertools.product((1995, 2007, 2009, 2011), PAYS):
        def val(annee, variable):
            return d[p, annee, variable]
        def delta(variable):
            return round(val(an+10, variable)-val(an, variable), 1)
        primaires = [val(t, "B9_MIO_NAC")+val(t, "D41PAY_MIO_NAC") for t in range(an+1, an+11)]
        chomage = [d.get((p, t, "chomage")) for t in range(an, an+11)]
        ligne = dict(pays=p, debut=an, **{"B9_plus_"+str(t):val(an+t,"B9") for t in (0,3,5,10)},
                     delta_rec=delta("TR"), delta_dep=delta("TE"), delta_interets=delta("D41PAY"),
                     delta_invest=delta("P51G"), dette_depart=d.get((p, an, "dette")),
                     delta_dette=delta("dette") if (p, an, "dette") in d else None,
                     nb_primaire_pos_10_ans=sum(v>0 for v in primaires),
                     nb_B9_pos_10_ans=sum(val(t,"B9_MIO_NAC")>0 for t in range(an+1,an+11)),
                     part65_depart=d.get((p,an,"part65")), part65_fin=d.get((p,an+10,"part65")),
                     chomage_depart=chomage[0], chomage_max=max(chomage) if None not in chomage else None,
                     chomage_fin=chomage[-1], croissance_cumulee=round((produit_croissance(p, an, d)-1)*100,1))
        fenetres.append(ligne)
    enregistrer("fenetres.csv", fenetres[0], fenetres)


def produit_croissance(pays, an, donnees):
    cumul = 1
    for t in range(an+1, an+11):
        cumul *= 1 + donnees[pays,t,"croissance"]/100
    return cumul


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actualiser", action="store_true")
    panel(parser.parse_args().actualiser)
