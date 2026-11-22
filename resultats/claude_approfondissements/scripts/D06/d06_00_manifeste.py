"""D06 - écrit donnees/D06/MANIFESTE_PIECES.csv (empreintes sha256 des pièces conservées).
Les pièces lues dans le dossier A06 (lecture seule) sont listées avec leur chemin d'origine."""
import csv, hashlib, os

def _racine_depot(depart):
    """Remonte depuis `depart` jusqu'au dossier qui contient la première enquête (indépendant de l'emplacement)."""
    p = os.path.abspath(depart)
    while True:
        if os.path.isdir(os.path.join(p, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "commun")):
            return p
        q = os.path.dirname(p)
        if q == p:
            raise SystemExit("racine du dépôt introuvable depuis " + depart)
        p = q


ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(ICI, "..", ".."))
SRC = os.path.join(OUT, "donnees", "D06", "sources")
A06 = os.path.normpath(os.path.join(_racine_depot(ICI), "Le_Constat_Cellule_Enquete", "resultats", "donnees", "A06", "sources"))
ACCES = "2026-11-22"

PIECES = [
    ("ameco_extrait_D06.csv", "extrait par scripts/D06/d06_01 des fichiers AMECO conservés par A06 (https://economy-finance.ec.europa.eu, téléchargés le 20/11/2026)", "AMECO, 8 pays + Allemagne de l'Ouest, codes utiles"),
    ("BCLDatabase_online_v2.7.xlsx", "http://www.longtermproductivity.com/download/BCLDatabase_online_v2.7.xlsx", "Bergeaud, Cette, Lecat, base de productivité à long terme v2.7 (février 2026)"),
    ("bcl_download.html", "http://www.longtermproductivity.com/download.html", "page de téléchargement BCL"),
    ("JSTdatasetR6.xlsx", "https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx", "Jordà-Schularick-Taylor Macrohistory release 6 (État central)"),
    ("BCL_ES474_2015_PIB_longue_periode.pdf", "https://www.cor-retraites.fr/sites/default/files/2019-06/doc-3188.pdf", "Bergeaud, Cette, Lecat, Économie et Statistique n°474 (2014/2015)"),
    ("CetteCordeLecat_ES494_2017.pdf", "https://www.insee.fr/fr/statistiques/fichier/3135045/494-495-496_Cette-Corde-Lecat-FR.pdf", "Cette, Corde, Lecat, Économie et Statistique n°494-496 (2017)"),
    ("CrepoLeclairRoux_ES376_2004_RTT.pdf", "https://www.insee.fr/fr/statistiques/fichier/1376466/es376377c.pdf", "Crépon, Leclair, Roux, RTT productivité et emploi, ES n°376-377"),
    ("BozioWasmer_2024_rapport_final.pdf", "https://vie-publique.fr/files/rapport/pdf/295596.pdf", "Bozio, Wasmer, Les politiques d'exonérations de cotisations sociales, octobre 2024"),
    ("Demmou_ES438_2011_emploi_industriel.pdf", "https://www.insee.fr/fr/statistiques/fichier/1377172/ES438R.pdf", "Demmou, Le recul de l'emploi industriel 1980-2007, ES n°438-440"),
    ("CPO_2025-09_cadre_fiscal_industrie.pdf", "https://www.vie-publique.fr/files/rapport/pdf/300295.pdf", "Conseil des prélèvements obligatoires, septembre 2025"),
    ("CPO_2025_RP1_PO_industrie.pdf", "https://www.vie-publique.fr/files/rapport/pdf/302106.pdf", "CPO, rapport particulier n°1, prélèvements obligatoires et réindustrialisation"),
    ("AutorDornHanson_2013_ChinaSyndrome.pdf", "https://www.ddorn.net/papers/Autor-Dorn-Hanson-ChinaSyndrome.pdf", "Autor, Dorn, Hanson, American Economic Review 2013"),
    ("Senat_r20-555_mono.html", "https://www.senat.fr/rap/r20-555/r20-555_mono.html", "Sénat, rapport d'information n°555 (2020-2021) sur le programme de stabilité 2021"),
    ("EC_DP098_2019_semi_elasticites.pdf", "https://economy-finance.ec.europa.eu/system/files/2019-05/dp098_en.pdf", "Mourre, Poissonnier, Lausegger, European Economy DP 098 (2019)"),
    ("Insee_DT_G2014-09_croissance_potentielle.pdf", "https://www.insee.fr/fr/statistiques/fichier/1381095/G2014-09.pdf", "Insee, document de travail G2014/09, croissance potentielle"),
    ("TresorEco131_2014.html", "https://www.tresor.economie.gouv.fr/Articles/2014/06/13/tresor-eco-n-131-le-decrochage-du-pib-par-habitant-en-france-depuis-40-ans-pourquoi", "page Trésor-Éco n°131 (non exploitée : PDF non trouvé)"),
]
PIECES_A06 = [
    ("CNP_2025_synthese.pdf", "Conseil national de productivité, synthèse 2025 (pièce A06)"),
    ("CNP_2026_rapport.pdf", "Conseil national de productivité, rapport juillet 2026 (pièce A06)"),
    ("COR_RA_2026.pdf", "Conseil d'orientation des retraites, rapport annuel juin 2026 (pièce A06)"),
    ("EC_AgeingReport2024_ip279.pdf", "Commission européenne, Ageing Report 2024 (pièce A06)"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


with open(os.path.join(OUT, "donnees", "D06", "MANIFESTE_PIECES.csv"), "w", encoding="utf-8", newline="") as h:
    w = csv.writer(h, delimiter=";")
    w.writerow(["fichier", "url", "date_acces", "sha256", "description"])
    for f, u, d in PIECES:
        p = os.path.join(SRC, f)
        if os.path.exists(p):
            w.writerow(["sources/" + f, u, ACCES, sha(p), d])
    for f, d in PIECES_A06:
        p = os.path.join(A06, f)
        if os.path.exists(p):
            w.writerow(["../../../../../Le_Constat_Cellule_Enquete/resultats/donnees/A06/sources/" + f, "voir manifeste A06", "2026-11-20", sha(p), d])
print("ok")
