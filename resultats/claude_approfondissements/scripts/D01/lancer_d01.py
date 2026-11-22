# -*- coding: utf-8 -*-
"""D01 - point d'entrée unique : régénère toutes les tables et le manifeste.

Usage : python lancer_d01.py   (depuis n'importe quel répertoire)
"""
import csv
import hashlib
import runpy
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import d01_lecture as L  # noqa: E402

runpy.run_path(str(ICI / "d01_calculs.py"), run_name="__main__")

DATE = "2026-11-22"
PIECES = [
    # pièces téléchargées par D01 (conservées dans donnees/D01/sources)
    (L.SOURCES_D01 / "T_1105_fr.xlsx", "https://www.insee.fr/fr/statistiques/fichier/8988797/T_1105_fr.xlsx",
     "Insee, comptes nationaux base 2020, tableau 1.105 : PIB, trois approches (D1 de l'économie, valeur ajoutée)"),
    (L.SOURCES_D01 / "T_6211_fr.xlsx", "https://www.insee.fr/fr/statistiques/fichier/8988823/T_6211_fr.xlsx",
     "Insee, base 2020, tableau 6.211 : emploi salarié par branche en équivalents temps plein (depuis 1949)"),
    (L.SOURCES_D01 / "ocde_recettes_fiscales_FRA_1973_1986.csv",
     "https://sdmx.oecd.org/public/rest/data/OECD.CTP.TPS,DSD_REV_COMP_OECD@DF_RSOECD,1.0/FRA......?startPeriod=1973&endPeriod=1986",
     "OCDE, Statistiques des recettes publiques, France 1973-1986 (code 1110 impôt sur le revenu des personnes physiques)"),
    # pièces locales lues en lecture seule
    (L.COMMUN / "insee_cn_t_3201.xlsx", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/commun/",
     "Insee 3.201, dépenses et recettes des APU par nature, base 2020"),
    (L.COMMUN / "insee_dep_rec_serie_longue.xlsx", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/commun/",
     "Insee, série longue dépenses et recettes en % du PIB (contrôle de raccord)"),
    (L.DON / "A04" / "a04_po_recettes_1959_2025.csv", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/A04/",
     "PIB base 2020 (colonne PIB_implicite_Md_EUR), dénominateur imposé par les consignes"),
    (L.CODEX / "donnees" / "T_1101_1103_fr.xlsx", "lecture seule : resultats/codex/donnees/", "Insee 1.101-1.103 : PIB et consommation en valeur et en volume"),
    (L.CODEX / "donnees" / "T_7301_fr.xlsx", "lecture seule : resultats/codex/donnees/", "Insee 7.301 : compte des APU (sous-détail D11, D121, D611, D613, D62x, D7x)"),
    (L.CODEX / "donnees" / "T_1109_fr.xlsx", "lecture seule : resultats/codex/donnees/", "Insee 1.109 : emploi par secteur, ETP (S13 depuis 1978)"),
    (L.CODEX / "donnees" / "t_3101_fr.xlsx", "lecture seule : resultats/codex/donnees/", "Insee 3.101 : dette de Maastricht (depuis 1978)"),
    (L.CODEX / "calculs" / "ponts_points_pib.csv", "lecture seule : resultats/codex/calculs/", "Ponts de Codex en points de PIB"),
    (L.CODEX / "calculs" / "annuel.csv", "lecture seule : resultats/codex/calculs/", "Table annuelle de Codex (contrôle de la dette)"),
    (L.DON / "A06" / "sources" / "ameco" / "AMECO15.TXT", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/A06/sources/ameco/",
     "AMECO : UWSH (salaires bruts reçus par les ménages), UWCH (rémunérations reçues)"),
    (L.DON / "A05" / "A05_nature_contrib_periodes.csv", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/A05/", "Rapprochement A05"),
    (L.DON / "S03" / "S03_decomposition.csv", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/S03/", "Rapprochement S03 (Drees)"),
    (L.DON / "S01" / "S01_taux_cotisations_ipp_1970_2000.csv", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/S01/",
     "Taux de cotisation (Barèmes IPP, lecture S01) : transcrits dans d01_lecture.py"),
    (L.DON / "S01" / "S01_mesures_1975_1999.csv", "lecture seule : Le_Constat_Cellule_Enquete/resultats/donnees/S01/",
     "Barème de l'IR et majorations exceptionnelles (pièces Sénat lues par S01) : transcrits dans d01_lecture.py"),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


with open(L.SORTIES / "MANIFESTE_PIECES.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["fichier", "url", "date_acces", "sha256", "description"])
    for pth, url, desc in PIECES:
        try:
            rel = pth.relative_to(L.SORTIES).as_posix()
        except ValueError:
            rel = pth.name
        w.writerow([rel, url, DATE, sha(pth), desc])
print("Manifeste écrit :", L.SORTIES / "MANIFESTE_PIECES.csv")
