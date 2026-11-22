"""D03 : transcriptions sur pièces, avec contrôle automatique des citations.
Chaque ligne porte une courte citation qui doit figurer, après normalisation, dans le texte extrait de la pièce.
Écrit dans ../../donnees/D03/ :
  D03_montants_pieces.csv, D03_creations_emplois_lf.csv, D03_sante_rythmes.csv,
  D03_decisions_avant_1974.csv, D03_controles_citations.csv
Usage : python -I d03_tables.py
Pages = pages du fichier PDF (marqueur [[p.N]] du texte extrait), pas la pagination imprimée."""
import csv
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
OUT = ICI.parent.parent
DON = OUT / "donnees" / "D03"
RACINE = OUT.parents[3]  # dossier Le_Constat_Cellule_Enquete
DOSS = {
    "D03": DON / "sources",
    "D02": OUT / "donnees" / "D02" / "sources",
    "S01": RACINE / "Le_Constat_Cellule_Enquete" / "resultats" / "donnees" / "S01" / "sources" / "senat",
    "S10": RACINE / "Le_Constat_Cellule_Enquete" / "resultats" / "donnees" / "S10" / "sources",
}
_cache = {}


def norm(t):
    t = re.sub(r"(\w)­\s*(\w)", r"\1\2", t)
    t = re.sub(r"([a-zà-ÿ])- ([a-zà-ÿ])", r"\1\2", t)
    return " ".join(t.split())


def texte(ref):
    d, f = ref.split(":")
    if ref not in _cache:
        _cache[ref] = norm((DOSS[d] / f).read_text(encoding="utf-8", errors="replace"))
    return _cache[ref]


CTRL = []


def controle(table, id_, ref, cit):
    ok = norm(cit) in texte(ref)
    CTRL.append([table, id_, ref, cit, "ok" if ok else "ABSENT"])
    return ok


def ecrire(nom, ent, lignes):
    for l in lignes:
        assert len(l) == len(ent), (nom, l)
    with (DON / nom).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(ent)
        w.writerows(lignes)
    print(f"{nom} : {len(lignes)} lignes")


N99 = "D03:senat_i1974_1975_0099_01.txt"
N104 = "D03:senat_i1974_1975_0104_01.txt"
N103S = "D03:senat_i1974_1975_0103_02.txt"
N103SS = "D03:senat_i1974_1975_0103_04.txt"
N43 = "D03:senat_i1973_1974_0043_02.txt"
N65 = "S01:i1976_1977_0065_01.txt"
N88 = "S01:i1977_1978_0088_01.txt"
N50 = "S01:i1979_1980_0050_01.txt"
N98 = "S01:i1980_1981_0098_01.txt"
N58 = "S01:i1981_1982_0058_01.txt"
N95 = "S01:i1982_1983_0095_01.txt"
N62 = "S01:i1983_1984_0062_01.txt"
N69 = "S01:i1984_1985_0069_01.txt"
N96 = "S01:i1985_1986_0096_01.txt"
N32 = "D02:senat_i1982_1983_0032.txt"
N58A29 = "D02:senat_i1981_1982_0058_03_29.txt"
N69S = "D02:senat_i1976_1977_0069_04.txt"
N92S = "D02:senat_i1977_1978_0092_04.txt"
N78S = "D02:senat_i1978_1979_0078_04.txt"
N128 = "D02:senat_i1979_1980_0128.txt"
CC80 = "D02:CCSS-RAPPORT-NOVEMBRE_1980.txt"
CC81 = "D02:CCSS-RAPPORT-NOVEMBRE_1981.txt"
CC82 = "D02:CCSS-RAPPORT-DECEMBRE_1982.txt"
CC83 = "D02:ccss_rapport_juin_1982.txt"
ER572 = "D03:drees_er572_depenses_sante_1950_2005.txt"
S10T = "S10:dares_comptes_emploi_1984-1985_transcription.txt"

NOMS = {N99: "Sénat n° 99 t. I 1974-1975", N104: "Sénat n° 104 t. I 1974-1975", N103S: "Sénat n° 103 t. II 1974-1975",
        N103SS: "Sénat n° 103 t. IV 1974-1975", N43: "Sénat n° 43 t. II 1973-1974", N65: "Sénat n° 65 t. I 1976-1977",
        N88: "Sénat n° 88 t. I 1977-1978", N50: "Sénat n° 50 t. I 1979-1980", N98: "Sénat n° 98 t. I 1980-1981",
        N58: "Sénat n° 58 t. I 1981-1982", N95: "Sénat n° 95 t. I 1982-1983", N62: "Sénat n° 62 t. I 1983-1984",
        N69: "Sénat n° 69 t. I 1984-1985", N96: "Sénat n° 96 t. I 1985-1986", N32: "Sénat n° 32 1982-1983",
        N58A29: "Sénat n° 58 t. III annexe 29 1981-1982", N69S: "Sénat n° 69 t. IV 1976-1977",
        N92S: "Sénat n° 92 t. IV 1977-1978", N78S: "Sénat n° 78 t. IV 1978-1979", N128: "Sénat n° 128 1979-1980",
        CC80: "Commission des comptes de la sécurité sociale, novembre 1980",
        CC81: "Commission des comptes de la sécurité sociale, novembre 1981",
        CC82: "Commission des comptes de la sécurité sociale, décembre 1982",
        CC83: "Commission des comptes de la sécurité sociale, rapport de juin 1983 (fichier « juin 1982 »)",
        ER572: "Drees, Études et résultats n° 572 (2007)",
        S10T: "Comptes de l'emploi 1984-1985, transcription de S10"}

# id ; famille ; année ; valeur Md F ; libellé ; périmètre ; ex ante/post ; pièce ; page ; citation
MONTANTS = [
    ("M01", "emploi", 1975, 0.587, "extension en année pleine des créations d'emplois de la loi de finances 1974", "État, budget général", "ex ante", N99, "119", "prévues dans la loi de finances 1974 (587 millions"),
    ("M02", "emploi", 1975, 8.823, "extension en année pleine des hausses de rémunérations accordées en 1974", "État, budget général", "ex ante", N99, "119", "l'année 1974 (8 823 millions)"),
    ("M03", "emploi", 1977, 2.697, "extension en année pleine des hausses de rémunérations accordées en 1976", "État, budget général", "ex ante", N65, "61", "l'année 1976 (2 697 millions de francs)"),
    ("M04", "emploi", 1977, 0.498, "extension en année pleine des créations d'emplois de la loi de finances 1976", "État, budget général", "ex ante", N65, "61", "loi de finances 1976 (498 millions de francs"),
    ("M05", "emploi", 1984, 22.0, "« charge supplémentaire » de 220 000 emplois publics créés en deux ans (rapporteur)", "État", "commentaire, convention inconnue", N62, "116", "on crée 220 000 emplois publics en deux ans"),
    ("M06", "entreprises", 1975, 9.599, "contributions à l'exploitation : Houillères 1,627 + SNCF 6,747 + RATP 1,121 + navigation 0,104", "État, quatre entreprises", "ex ante (dotation 1975)", N99, "122", "1 627 6 747 1 121 104"),
    ("M07", "entreprises", 1977, 14.035, "contributions à l'exploitation : Houillères 2,507 + SNCF 9,900 (y c. retraites) + RATP 1,273 + Air Inter + ports + Corse", "État, six entreprises", "ex ante (dotation 1977)", N65, "64", "Houillères 2 507 + 940"),
    ("M08", "entreprises", 1980, 34.301, "concours aux entreprises publiques : déficits 18,084 + capital 2,180 + prêts FDES 1,700 + deux régimes sociaux 12,337", "État, tous concours", "ex ante (projet 1980)", N50, "86", "avec un montant de 34,3 milliards de francs"),
    ("M09", "entreprises", 1981, 36.7, "concours de l'État aux entreprises publiques", "État, tous concours", "loi de finances initiale 1981", N58, "81", "passe de 36,7 à 43,5 milliards de francs"),
    ("M10", "entreprises", 1982, 43.5, "concours de l'État aux entreprises publiques", "État, tous concours", "ex ante (projet 1982)", N58, "81", "passe de 36,7 à 43,5 milliards de francs"),
    ("M11", "entreprises", 1983, 56.835, "concours : exploitation 28,332 + charges de retraite 18,661 + capital 9,842", "État, tous concours", "loi de finances 1983", N62, "102", "28.332 18.661 9.842"),
    ("M12", "entreprises", 1984, 67.105, "concours : exploitation 31,375 + charges de retraite 20,809 + capital 14,921", "État, tous concours", "ex ante (projet 1984)", N62, "102", "31.375 20.809 14.921"),
    ("M13", "entreprises", 1983, 7.618, "crédits d'application des lois de nationalisation (contredit par 5,618 dans Sénat n° 95, p. 75)", "État", "ex ante", N62, "102", "6 980 millions en 1984 contre 7 618 millions en 1983"),
    ("M14", "entreprises", 1984, 6.980, "crédits d'application des lois de nationalisation", "État", "ex ante", N62, "102", "6 980 millions en 1984 contre 7 618 millions en 1983"),
    ("M15", "entreprises", 1981, 22.582, "aides à l'industrie, total par type d'aide (dont entreprises publiques 4,574)", "État", "loi de finances initiale 1981", N58, "92", "22 582 34 409"),
    ("M16", "entreprises", 1982, 34.409, "aides à l'industrie, total par type d'aide (dont entreprises publiques 5,733)", "État", "ex ante (projet 1982)", N58, "92", "22 582 34 409"),
    ("M17", "entreprises", 1982, 43.0, "indemnisation des nationalisations de 1982, « dépense » étalée dans le temps (rapporteur)", "État", "commentaire, montant total non annualisé", N62, "116", "dépense à hauteur de 43 milliards de francs environ"),
    ("M18", "collectivites", 1974, 17.001, "versement représentatif de la taxe sur les salaires (VRTS) aux collectivités", "État vers collectivités (transfert interne aux administrations)", "en cours d'exercice, avance de régularisation incluse", N104, "9", "porté à 17 001 millions de francs"),
    ("M19", "collectivites", 1970, 31.064, "dépenses réelles des communes (hors Paris)", "communes", "ex post", N104, "8", "Dépenses totales 31 064 34 120"),
    ("M20", "collectivites", 1973, 44.4, "dépenses réelles des communes (hors Paris), estimation", "communes", "estimation", N104, "8", "44 400 + 14 %"),
    ("M21", "collectivites", 1982, 99.7, "concours de l'État aux collectivités locales (tableau mal lu par la reconnaissance de caractères)", "État vers collectivités", "loi de finances initiale 1982", N95, "90", "Total 99,7 119,0"),
    ("M22", "collectivites", 1983, 119.0, "concours de l'État aux collectivités locales, y c. compensation des transferts de compétences", "État vers collectivités", "ex ante (projet 1983)", N95, "90", "Total 99,7 119,0"),
    ("M23", "collectivites", 1982, 51.9, "dotation globale de fonctionnement (DGF), qui remplace le VRTS en 1979", "État vers collectivités", "loi de finances initiale 1982", N95, "90", "Dotation globale de fonctionnement 51.9 58.7"),
    ("M24", "collectivites", 1983, 58.7, "dotation globale de fonctionnement (DGF)", "État vers collectivités", "ex ante (projet 1983)", N95, "90", "Dotation globale de fonctionnement 51.9 58.7"),
    ("M25", "collectivites", 1984, 94.365, "concours de l'État aux collectivités à structure constante (hors transferts de compétences)", "État vers collectivités", "ex ante", N69, "129", "99 125 millions de francs contre 94 365 millions en 1984"),
    ("M26", "collectivites", 1985, 99.125, "concours de l'État aux collectivités à structure constante (hors transferts de compétences)", "État vers collectivités", "ex ante (projet 1985)", N69, "129", "99 125 millions de francs contre 94 365 millions en 1984"),
    ("M27", "collectivites", 1985, 12.4, "dotation générale de décentralisation (7,9 en 1984), contrepartie de transferts de charges", "État vers collectivités", "ex ante (projet 1985)", N69, "129", "7,9 milliards de francs en 1984 à 12.4 milliards"),
    ("M28", "collectivites", 1975, 0.12844, "transferts de charges : nationalisation et étatisation des lycées municipaux, CEG et CES", "État", "ex ante", N104, "11", "soit, pour 1975, 128,44 millions de francs"),
    ("M29", "social", 1982, 21.3, "garantie de ressources (Unédic)", "assurance chômage", "prévision", N32, "18", "Garantie de ressources 21,3"),
    ("M30", "social", 1985, 29.0, "garantie de ressources (« près de 29 », coquille MF pour milliards)", "ensemble des financeurs", "ex post", S10T, "transcription", "pèse encore près de 29 MF"),
    ("M31", "social", 1980, 1.361, "subvention de l'État aux régimes des non-salariés non agricoles, tous risques (1,233 en 1979)", "État vers régimes", "ex post ou prévision", CC81, "22", "Non salariés non agricoles: 1.233 1.361"),
    ("M32", "social", 1980, 18.497, "subventions de l'État aux régimes spéciaux (16,213 en 1979)", "État vers régimes", "ex post ou prévision", CC81, "22", "Régimes spéciaux 16.213 18.497"),
    ("M33", "social", 1982, 1.30, "amélioration des pensions « avant-loi Boulin » et des pensions de réversion (mesure de 1982)", "régime général", "ex ante", N58A29, "44", "Amélioration des pensions «avant-loi Boulin » et des pensions de reversion 1 ,30"),
    ("M35", "entreprises", 1979, 10.763, "charges de retraite SNCF 6,120 + Charbonnages 4,643 (12,337 en 1980 : 7,100 + 5,237)", "État", "loi de finances 1979", N50, "85", "Total I 10 763 12 337"),
    ("M36", "sante", 1984, 25.0, "« près de 25 milliards d'économies » par contrôle des dépenses, tous secteurs (dont hôpital : taux directeurs, budget global)", "assurance maladie et autres", "appréciation du rapporteur, non ventilée", N69, "66", "un contrôle strict des dépenses a permis près de 25 milliards d'économies"),
    ("M34", "sante", 1971, 41.385, "dépenses globales de l'assurance maladie (nature 33,128 + indemnités journalières 8,257)", "assurance maladie, budget social de la Nation", "ex post", N43, "40", "s'élevaient à 41.385 millions"),
]

CREATIONS = [
    # année ; nombre ; nature ; pièce ; page ; citation
    (1974, 37000, "emplois nouveaux, budget de l'État (rappel en 1975)", N99, "167", "21 000 emplois nouveaux contre 37 000 un an auparavant"),
    (1975, 21000, "emplois nouveaux, budget de l'État (« chiffres provisoires »)", N99, "167", "21 000 emplois nouveaux contre 37 000 un an auparavant"),
    (1976, 44000, "créations, budget général (y c. titularisations)", N65, "62", "47 000 unités contre 44 000 il y a un an"),
    (1977, 47000, "créations, budget général, dont « pour la moitié » titularisations", N65, "62", "47 000 unités contre 44 000 il y a un an"),
    (1977, 21937, "créations nettes, budget général et budgets annexes (66 032 brutes dont 44 095 titularisations)", N88, "56", "Créations nettes d'emplois 21 937 26 174"),
    (1978, 26174, "créations nettes, budget général et budgets annexes (36 804 brutes)", N88, "56", "Créations nettes d'emplois 21 937 26 174"),
    (1980, 14500, "postes nouveaux, loi de finances 1980", N98, "78", "avait prévu l'ouverture de 14500 postes nouveaux"),
    (1981, 1890, "créations nettes, loi de finances initiale 1981", N98, "78", "les créations nettes d'emplois seront de 1 890"),
    (1981, 54000, "collectif de juillet 1981 : « plus de 54000 » dont près de 45 000 État et plus de 9 000 hôpitaux et établissements sanitaires et sociaux", N58, "72", "le collectif de 1981 avait créé plus de 54000 emplois"),
    (1982, 61000, "emplois publics à la charge totale ou partielle de l'État ; « 125 000 » en dix-huit mois avec le collectif", N58, "69", "(61000 en 1982 contre 1890 en 1981)"),
    (1982, 203500, "« offre d'emplois publics ou d'utilité collective » depuis début 1981, statistiques officielles citées : 80 800 en 1981 et 122 700 en 1982", N95, "88", "203 500 emplois, dont globalement 80 800 en 1981 et 122 700 en 1982"),
    (1983, 21000, "créations d'emplois publics, dont 13 000 emplois budgétaires (plus 12 500 régularisations)", N95, "88", "fixé à 21 000 dont 13 000 emplois budgétaires"),
    (1985, -5454, "solde des créations et suppressions d'emplois budgétaires (−0,2 %)", N69, "101", "solde négatif = 5 454 emplois"),
    (1986, -4330, "solde des créations et suppressions, effectifs budgétaires civils (−0,2 %)", N96, "91", "solde négatif de 4 330 emplois"),
]

SANTE = [
    # indicateur ; période ; valeur ; unité ; pièce ; page ; citation
    ("CSBM en volume, croissance annuelle moyenne", "1965-1970", 8.5, "% par an", ER572, "3", "1965-1970 8,5 5,4 -0,1"),
    ("CSBM en volume, croissance annuelle moyenne", "1970-1975", 8.8, "% par an", ER572, "3", "1970-1975 8,8 3,5 -1,5"),
    ("CSBM en volume, croissance annuelle moyenne", "1975-1980", 5.8, "% par an", ER572, "3", "1975-1980 5,8 3,3 -0,7"),
    ("CSBM en volume, croissance annuelle moyenne", "1980-1985", 5.5, "% par an", ER572, "3", "1980-1985 5,5 1,5 -1,4"),
    ("PIB en volume, croissance annuelle moyenne (même tableau)", "1970-1975", 3.5, "% par an", ER572, "3", "1970-1975 8,8 3,5 -1,5"),
    ("PIB en volume, croissance annuelle moyenne (même tableau)", "1975-1980", 3.3, "% par an", ER572, "3", "1975-1980 5,8 3,3 -0,7"),
    ("PIB en volume, croissance annuelle moyenne (même tableau)", "1980-1985", 1.5, "% par an", ER572, "3", "1980-1985 5,5 1,5 -1,4"),
    ("prix relatif de la santé, variation annuelle moyenne", "1970-1975", -1.5, "% par an", ER572, "3", "1970-1975 8,8 3,5 -1,5"),
    ("dépenses globales de l'assurance maladie, indice (1968 = 100), prévision 1974", "1968-1974", 270.0, "indice", N43, "40", "100 122,2 151,5 172,6 200,9 228,8 270,0"),
    ("hospitalisation publique à la charge du régime général, rythme annuel", "juillet 1979", 25.6, "% par an", CC80, "41", "un rythme annuel de 25,6 % au 31 juillet 1979"),
    ("hospitalisation publique à la charge du régime général, rythme annuel", "septembre 1980", 22.4, "% par an", CC80, "42", "soit 22,4 % , pour les dépenses d'hospitalisation publique"),
    ("frais de séjour hospitaliers, régime général", "1981", 17.4, "% sur un an", CC83, "41", "+ 20,1 % contre + 17,4 % en 1981"),
    ("frais de séjour hospitaliers, régime général", "1982", 20.1, "% sur un an", CC83, "41", "+ 20,1 % contre + 17,4 % en 1981"),
    ("frais de séjour publics, régime général (champ élargi)", "1982", 22.0, "% sur un an", CC83, "41", "(+ 22 % en 1982)"),
    ("taux moyen de couverture de la CSBM par la sécurité sociale", "1980", 80.0, "%", ER572, "6", "passe à 80 % de taux moyen de cou- verture en 1980"),
    ("couverture sociale de la quasi-totalité de la population", "1978", 1978.0, "année", ER572, "6", "à partir de 1978, la quasi-totalité de la population bénéficie d’une couverture sociale"),
    ("hôpital : « freinage puis quasi-suppression des créations d'emploi », budget global", "1983-1984", 0.0, "qualitatif", N69, "66", "freinage puis quasi-suppression des créations d'emploi"),
    ("part des frais de séjour hospitalier dans les prestations de l'assurance maladie", "1980", 55.0, "% (« plus de »)", CC80, "41", "représentent plus de 55 % des dépenses de prestations"),
]

# date ; texte ; décision ; mécanisme ; coût ultérieur ; année ; unité ; pct_PIB (via id de montant ou vide) ; pièce ; page ; citation ; marque
DECISIONS = [
    ("1966-07-12", "loi n° 66-509 du 12 juillet 1966", "assurance maladie obligatoire des non-salariés non agricoles",
     "régime à cotisants peu nombreux, subventionné par l'État", "non attribuable : la subvention de 1980 (1,361 Md F, M31) couvre tous les risques et tous les régimes de non-salariés", "", "", "", N69S, "11", "loi n° 66-509 du 12 juillet 1966", "C"),
    ("1970-12-31", "loi n° 70-1318 du 31 décembre 1970 portant réforme hospitalière", "carte sanitaire, groupements interhospitaliers ; article 52 : réforme du calcul du prix de journée prévue « dans le délai d'un an »",
     "le prix de journée reste la règle jusqu'à la dotation globale de 1984", "non chiffré ; rythme constaté : +25,6 % (juillet 1979), +22,4 % (septembre 1980) pour l'hospitalisation publique du régime général", "1979-1980", "% par an", "", N103S, "20", "était prévue dans le délai d'un an par l'article 52", "C"),
    ("1970-12-31", "loi n° 70-1318, article 52 (suite)", "réforme de la tarification encore renvoyée en décembre 1979",
     "même mécanisme", "non chiffré", "", "", "", N128, "22", "réforme de la tarification prévue par l'article 52 de la loi n° 70-1318 du 31 décembre 1970", "C"),
    ("1971-07-03", "loi n° 71-525 du 3 juillet 1971", "convention nationale entre les caisses et les syndicats de médecins, appliquée depuis novembre 1971",
     "tarifs conventionnels nationaux, paiement à l'acte", "non chiffré sur pièce", "", "", "", N103SS, "9", "loi n° 71-525 du 3 juillet 1971", "C"),
    ("1971-07-13", "loi du 13 juillet 1971", "allocation aux handicapés mineurs",
     "remplacée en 1975 par l'allocation d'éducation spéciale, acquise de droit aux anciens bénéficiaires", "non chiffré sur pièce", "", "", "", N69S, "6", "l'allocation instituée par la loi du 13 juillet 1971", "C"),
    ("1971-07-16", "loi du 16 juillet 1971 relative à l'allocation de logement", "allocation de logement en vigueur au 1er juillet 1972",
     "prestation sous condition de ressources, montée en charge après 1972", "non chiffré sur pièce", "", "", "", N43, "39", "loi du 16 juillet 1971 relative à l'allocation de logement", "C"),
    ("1971-12-31", "loi du 31 décembre 1971 (dite loi Boulin)", "durée maximale d'assurance relevée (« trente-cinq ans » selon le Sénat, à vérifier) ; inaptitude assouplie entre 60 et 65 ans",
     "pensions liquidées après 1972 plus élevées ; écart avec les pensions antérieures, corrigé ensuite par des relèvements forfaitaires (5 % en 1976, 5 % en 1977, mesure de 1982)",
     "coût direct non chiffré ; effet en retour : mesure de 1982 de 1,30 Md F, réversion comprise (M33)", "1982", "Md F", "M33", N69S, "8", "loi du 31 décembre 1971 qui a porté à trente-cinq ans", "C"),
    ("1971-12-31", "loi du 31 décembre 1971 (suite)", "inaptitude au travail assouplie",
     "pension au taux de 50 % entre 60 et 65 ans sans inaptitude totale", "non chiffré", "", "", "", N78S, "36", "la loi du 31 décembre 1971 a considérablement assoupli la notion d'inaptitude", "C"),
    ("1972-03-27 (date : S10)", "accord interprofessionnel de 1972 (garantie de ressources)", "garantie de ressources des salariés âgés licenciés, « économiques ou non (1972) »",
     "régime conventionnel étendu aux démissionnaires en 1977 ; montée en charge avec les départs", "21,3 Md F prévus en 1982 (tous bénéficiaires) ; près de 29 Md F en 1985 ; part de l'accord de 1972 non isolée sur pièce (environ la moitié selon S10)", "1982", "Md F", "M29", N32, "5", "licenciés économiques ou non (1972)", "C"),
    ("1972-12-29", "décret du 29 décembre 1972", "pension du régime général calculée sur les dix meilleures années",
     "salaire de référence plus élevé pour les pensions liquidées après 1973", "non chiffré sur pièce", "", "", "", N69S, "8", "décret du 29 décembre 1972, qui a prévu le calcul de la pension sur la base des dix meilleures années", "C"),
    ("1972-1973", "mesures d'assurance vieillesse intervenues en 1973 (texte de la loi non lu)", "généralisation des retraites complémentaires ; réversion ouverte dès 55 ans",
     "montée en charge des régimes complémentaires obligatoires ; pensions de réversion plus précoces", "non chiffré sur pièce (recettes de l'ARRCO : 33,1 Md F en 1979, taille du régime et non coût de la loi)", "", "", "", N43, "52", "la généralisation des retraites complémentaires", "C"),
    ("1973-06-15", "décret n° 73-530 du 15 juin 1973 (pensions minières)", "bonifications et « garantie supplémentaire d'évolution des retraites en fonction des salaires »",
     "indexation salariale des pensions d'un régime en déclin démographique, couvert par l'État", "non chiffré ; charges de retraite des Charbonnages couvertes par l'État : 4,643 Md F en 1979 (tous facteurs)", "1979", "Md F", "", N43, "52", "garantie supplémentaire d'évolution des retraites en fonction des salaires", "C"),
    ("1970-1971", "lois de finances pour 1971 et 1972", "prise en charge par le régime général des déficits maladie et maternité de régimes spéciaux",
     "transfert durable de charges vers le régime général, élargi par la compensation de 1974", "non chiffré sur pièce", "", "", "", N43, "44", "insérées dans les lois de finances pour 1971 et 1972", "C"),
    ("1973-12", "loi de finances pour 1974", "37 000 emplois nouveaux dans le budget de l'État",
     "extension en année pleine en 1975, puis coût permanent des emplois", "0,587 Md F en 1975 (extension en année pleine, dont 0,553 Éducation nationale)", "1975", "Md F", "M01", N99, "119", "prévues dans la loi de finances 1974 (587 millions", "C"),
    ("avant 1974 (date non vérifiée)", "régimes de retraite des entreprises nationales (SNCF, mines)", "charges de retraite couvertes par l'État",
     "règle antérieure + baisse des effectifs cotisants", "10,763 Md F en 1979 ; 12,337 en 1980 ; 18,661 en 1983 ; 20,809 en 1984 ; règle non datée sur pièce", "1979", "Md F", "M35", N50, "85", "Total I 10 763 12 337", "C"),
    ("avant 1974 (date non vérifiée)", "mensualisation des salaires (accords contractuels)", "maintien du salaire en arrêt maladie par l'employeur",
     "le rapporteur lie la hausse des indemnités journalières à l'absentéisme « favorisé par la mensualisation » ; la Commission des comptes signale l'impact des accords sur les prestations en espèces", "non chiffré (le rapporteur évalue à 1 à 2 Md F l'économie possible, pas le coût)", "", "", "", N65, "50", "l'absentéisme favorisé par la mensualisation", "C"),
    ("avant 1974 (date non vérifiée)", "versement représentatif de la taxe sur les salaires (VRTS)", "ressource affectée aux collectivités, indexée sur la taxe sur les salaires",
     "transfert à progression automatique (+13,82 % en 1974), remplacé par la DGF en 1979 ; neutre sur le solde de l'ensemble des administrations", "17,001 Md F en 1974 ; DGF 58,7 Md F en 1983 (autre règle)", "1974", "Md F", "M18", N104, "9", "porté à 17 001 millions de francs", "C"),
    ("avant 1974 (date non vérifiée)", "plan de nationalisation ou d'étatisation des lycées municipaux, CEG et CES", "l'État reprend des dépenses d'établissements locaux",
     "transfert de charges étalé sur plusieurs exercices", "0,128 Md F en 1975", "1975", "Md F", "M28", N104, "11", "soit, pour 1975, 128,44 millions de francs", "C"),
]


def main():
    import sys
    sys.path.insert(0, str(ICI))
    pib = {}
    with (DON / "sources" / "a04_po_recettes_1959_2025.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            pib[int(r["annee"])] = float(r["PIB_implicite_Md_EUR"])
    mont = []
    pct = {}
    for (i, fam, a, v, lib, per, ea, ref, pg, cit) in MONTANTS:
        controle("montants", i, ref, cit)
        p = round(100 * v / 6.55957 / pib[a], 3)
        pct[i] = p
        mont.append([i, fam, a, v, round(v / 6.55957, 3), round(pib[a], 3), p, lib, per, ea, NOMS[ref], ref, pg, cit,
                     "S" if ref.startswith("S10") else "C"])
    ecrire("D03_montants_pieces.csv", ["id", "famille", "annee", "Md_F", "Md_EUR", "PIB_Md_EUR", "pct_PIB", "libelle",
                                       "perimetre", "ex_ante_ou_post", "source", "fichier", "page_pdf", "citation", "marque"], mont)
    cre = []
    for (a, n, nat, ref, pg, cit) in CREATIONS:
        controle("creations", str(a), ref, cit)
        cre.append([a, n, nat, NOMS[ref], ref, pg, cit, "C"])
    ecrire("D03_creations_emplois_lf.csv", ["annee", "nombre", "nature", "source", "fichier", "page_pdf", "citation", "marque"], cre)
    san = []
    for (ind, per, v, u, ref, pg, cit) in SANTE:
        controle("sante", ind + " " + per, ref, cit)
        san.append([ind, per, v, u, NOMS[ref], ref, pg, cit, "C"])
    ecrire("D03_sante_rythmes.csv", ["indicateur", "periode", "valeur", "unite", "source", "fichier", "page_pdf", "citation", "marque"], san)
    dec = []
    for (d, t, de, mec, cout, a, u, mid, ref, pg, cit, mq) in DECISIONS:
        controle("decisions", t, ref, cit)
        dec.append([d, t, de, mec, cout, a, u, pct.get(mid, ""), NOMS[ref] + (f" (montant : {mid})" if mid else ""), pg, cit, mq])
    ecrire("D03_decisions_avant_1974.csv", ["date", "texte", "decision", "mecanisme_de_cout_differe", "cout_ulterieur",
                                            "annee", "unite", "pct_PIB", "source", "page", "citation", "marque"], dec)
    import hashlib
    refs = sorted({c[2] for c in CTRL})
    pc = []
    for ref in refs:
        d, f = ref.split(":")
        pdf = (DOSS[d] / f).with_suffix(".pdf")
        for q in [DOSS[d] / f, pdf]:
            if q.exists():
                pc.append([ref.split(":")[0], q.name, hashlib.sha256(q.read_bytes()).hexdigest()])
    ecrire("D03_pieces_citees.csv", ["dossier_origine", "fichier", "sha256"], pc)
    ecrire("D03_controles_citations.csv", ["table", "id", "fichier", "citation", "resultat"], CTRL)
    absents = [c for c in CTRL if c[-1] != "ok"]
    print(f"citations absentes : {len(absents)}")
    for c in absents:
        print("  ", c)


if __name__ == "__main__":
    main()
