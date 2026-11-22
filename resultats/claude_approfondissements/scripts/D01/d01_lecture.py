# -*- coding: utf-8 -*-
"""D01 - lecture des pièces (lecture seule).

Tous les chemins sont déduits de l'emplacement de ce script.
Aucune donnée n'est saisie à la main ici, sauf les tables de taux et de barème
explicitement signalées (transcriptions de pièces lues par S01).
"""
import csv
import warnings
from pathlib import Path

import openpyxl

warnings.filterwarnings("ignore")

ICI = Path(__file__).resolve().parent            # OUT/scripts/D01
OUT = ICI.parents[1]                              # OUT = .../claude_approfondissements
SORTIES = OUT / "donnees" / "D01"
SOURCES_D01 = SORTIES / "sources"


def _racine():
    """Remonte jusqu'au dossier qui contient la première enquête et Codex."""
    for p in [ICI] + list(ICI.parents):
        if (p / "Le_Constat_Cellule_Enquete" / "resultats" / "donnees" / "commun").is_dir() and \
           (p / "resultats" / "codex" / "calculs").is_dir():
            return p
    raise SystemExit("ERREUR : racine du dépôt introuvable depuis " + str(ICI))


RACINE = _racine()
ENQ = RACINE / "Le_Constat_Cellule_Enquete" / "resultats"
DON = ENQ / "donnees"
COMMUN = DON / "commun"
CODEX = RACINE / "resultats" / "codex"


def _exige(p):
    p = Path(p)
    if not p.exists():
        raise SystemExit("ERREUR : pièce manquante : " + str(p))
    return p


def _num(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", ".").replace("\xa0", "")
    try:
        return float(s)
    except ValueError:
        return None


def _an(v):
    """Année d'un en-tête (int, '1978', '2024 sd', '2025 p')."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip()[:4]
    return int(s) if s.isdigit() else None


def _feuille(path, nom=None):
    wb = openpyxl.load_workbook(_exige(path), read_only=True, data_only=True)
    ws = wb[nom] if nom else wb.worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def _serie(rows, hdr_idx, row_num, col_lab, attendu, col0=2):
    """Série {année: valeur} de la ligne row_num (1-based), avec contrôle du libellé."""
    r = rows[row_num - 1]
    lab = str(r[col_lab])
    if attendu not in lab:
        raise SystemExit(f"ERREUR : ligne {row_num} : attendu « {attendu} », lu « {lab} »")
    hdr = rows[hdr_idx]
    out = {}
    for j in range(col0, len(r)):
        a = _an(hdr[j])
        v = _num(r[j])
        if a is not None and v is not None:
            out[a] = v
    return out


# --------------------------------------------------------------------------
# Insee 3.201 : dépenses et recettes des APU (S13), Md EUR courants, base 2020
# (numéros de ligne Excel, libellé attendu)
T3201_LIGNES = {
    # dépenses
    "DEP_fonct": (5, "Dépenses de fonctionnement"),
    "P2": (6, "(P2)"),
    "D1": (7, "(D1)"),
    "D29": (8, "(D29)"),
    "D4hD41_dep": (9, "(D4 hors D41)"),
    "D5_dep": (10, "(D5)"),
    "D41": (12, "Intérêts (D41)"),
    "D41G_dep": (13, "(D41G)"),
    "DEP_transf": (15, "Prestations et autres transferts"),
    "D62": (16, "(D62)"),
    "D632": (17, "(D632)"),
    "D3": (18, "(D3)"),
    "D73_dep": (19, "(D73)"),
    "D7_dep": (20, "(D7 hors D73)"),
    "D9p": (21, "(D9p hors D995p)"),
    "DEP_anf": (23, "Acquisitions moins cessions"),
    "P51g": (24, "(P51g)"),
    "P5autres": (25, "(P52, P53, NP)"),
    "DEP_tot": (27, "Total des dépenses"),
    "D122_dep": (28, "(D122)"),
    "DEP_hors_imput": (31, "Dépenses hors éléments imputés"),
    # recettes
    "REC_prod": (34, "Recettes de production"),
    "P11": (35, "(P11)"),
    "P12": (36, "(P12)"),
    "P13p": (37, "Paiements partiels"),
    "D39": (38, "(D39)"),
    "REC_propr": (40, "Revenus de la propriété"),
    "D41_rec": (41, "Intérêts (D41)"),
    "D4hD41_rec": (43, "(D4 hors D41)"),
    "REC_impcot": (45, "Impôts et cotisations sociales"),
    "D2": (46, "(D2)"),
    "D5": (47, "(D5)"),
    "D91r": (48, "(D91r)"),
    "D733": (49, "(D733)"),
    "D61": (50, "(D61)"),
    "D995r": (51, "(D995r)"),
    "REC_autres": (53, "Autres transferts"),
    "D73_rec": (54, "(D73 hors D733)"),
    "D7_rec": (55, "(D7 hors D73)"),
    "D9r": (56, "(D9r hors D91r, D995r)"),
    "REC_tot": (58, "Total des recettes"),
    "D612": (59, "(D612)"),
    "REC_hors_imput": (62, "Recettes hors éléments imputés"),
    "B8g": (65, "(B8g)"),
    "B9NF": (66, "(B9NF)"),
}


def lire_3201():
    rows = _feuille(COMMUN / "insee_cn_t_3201.xlsx")
    # libellés mal encodés dans le fichier : on compare sur une version sans accents
    def norm(s):
        import unicodedata
        s = str(s)
        s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
        return s.replace("�", "").lower()
    out = {}
    hdr = rows[2]
    for k, (n, att) in T3201_LIGNES.items():
        r = rows[n - 1]
        a = norm(att)
        lab = norm(r[1])
        # tolère les caractères perdus : compare sans accents et sans caractères non ASCII
        a2 = "".join(c for c in a if c.isascii())
        l2 = "".join(c for c in lab if c.isascii())
        ok = a2.replace(" ", "") in l2.replace(" ", "") or \
            all(tok in l2 for tok in a2.replace("(", " ").replace(")", " ").split() if len(tok) > 3)
        if not ok:
            raise SystemExit(f"ERREUR 3.201 ligne {n} : attendu « {att} », lu « {r[1]} »")
        out[k] = {int(hdr[j]): float(r[j]) for j in range(2, len(r)) if isinstance(hdr[j], int) and _num(r[j]) is not None}
    return out


def lire_pib_a04():
    p = _exige(DON / "A04" / "a04_po_recettes_1959_2025.csv")
    out, dep, rec = {}, {}, {}
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            a = int(r["annee"])
            out[a] = float(r["PIB_implicite_Md_EUR"])
            if r.get("depenses_pctPIB"):
                dep[a] = float(r["depenses_pctPIB"])
                rec[a] = float(r["recettes_pctPIB"])
    return out, dep, rec


def lire_serie_longue():
    rows = _feuille(COMMUN / "insee_dep_rec_serie_longue.xlsx")
    hdr = rows[3]
    res = {}
    for n, k in ((5, "dep"), (7, "rec")):
        r = rows[n - 1]
        res[k] = {_an(hdr[j]): _num(r[j]) for j in range(1, len(r)) if _an(hdr[j]) and _num(r[j]) is not None}
    return res


def lire_t1101_1103():
    """PIB nominal, PIB en volume (euros 2020 chaînés), consommation des ménages (prix)."""
    p = CODEX / "donnees" / "T_1101_1103_fr.xlsx"
    nom = _feuille(p, "T_1101 en niveau")
    vol = _feuille(p, "T_1102 en niveau")
    res = {}
    for k, (n, code) in {"B1GQ": (7, "B1GQ"), "P3_S14B": (12, "S14B"), "P3_S13": (13, "S13")}.items():
        res[k + "_nom"] = _serie(nom, 3, n, 0, code)
        res[k + "_vol"] = _serie(vol, 3, n, 0, code)
    return res


def lire_t7301():
    rows = _feuille(CODEX / "donnees" / "T_7301_fr.xlsx", "T_7301")
    spec = {
        "P2": 12, "D1": 21, "D11": 22, "D12": 23, "D121": 24, "D122": 25,
        "D2": 36, "D211": 38, "D212": 39, "D214": 40, "D29": 41, "D291": 42,
        "D5": 73, "D51": 74, "D59": 75, "D61": 76, "D611": 77, "D612": 78, "D613": 79,
        "D613CE": 80, "D613NSI": 81, "D62": 99, "D621": 100, "D622": 101, "D623": 102,
        "D63": 152, "D631": 153, "D632": 154, "P51G": 142,
    }
    res = {k: _serie(rows, 3, n, 0, k) for k, n in spec.items()}
    # subventions versées (inscrites en ressources négatives) et autres transferts courants versés
    spec2 = {"D3_vers": (44, "D3"), "D31_vers": (45, "D31"), "D39_vers": (46, "D39"), "D391_vers": (47, "D391"),
             "D392_vers": (48, "D392"), "D399_vers": (49, "D399"), "D7_vers": (103, "D7"), "D71_vers": (105, "D71"),
             "D72_vers": (106, "D72"), "D74_vers": (111, "D74"), "D75_vers": (112, "D75"), "D76_vers": (115, "D76")}
    for k, (n, code) in spec2.items():
        s = _serie(rows, 3, n, 0, code)
        if rows[n - 1][0] != code:
            raise SystemExit(f"ERREUR T_7301 ligne {n} : code {rows[n-1][0]} au lieu de {code}")
        res[k] = {a: (-v if k.startswith("D3") else v) for a, v in s.items()}
    return res


def lire_t1109():
    rows = _feuille(CODEX / "donnees" / "T_1109_fr.xlsx", "T_1109 en niveau")
    return {"S13": _serie(rows, 3, 8, 0, "S13"), "S1": _serie(rows, 3, 16, 0, "S1")}


def lire_t1105():
    rows = _feuille(SOURCES_D01 / "T_1105_fr.xlsx", "T_1105 en niveau")
    return {"B1GQ": _serie(rows, 3, 6, 0, "B1GQ"), "B1G": _serie(rows, 3, 7, 0, "B1G"),
            "D1": _serie(rows, 3, 16, 0, "D1")}


def lire_t6211():
    rows = _feuille(SOURCES_D01 / "T_6211_fr.xlsx", "T_6211 en niveau")
    return {"OQ": _serie(rows, 3, 48, 0, "A5_OQ"), "OZ": _serie(rows, 3, 49, 0, "A38_OZ"),
            "PZ": _serie(rows, 3, 50, 0, "A38_PZ"), "TOT": _serie(rows, 3, 53, 0, "_T")}


def lire_t3101():
    rows = _feuille(CODEX / "donnees" / "t_3101_fr.xlsx", "T_3101")
    return {"dette": _serie(rows, 3, 7, 0, "S13"), "pib_3101": _serie(rows, 3, 22, 1, "PIB")}


def lire_ameco(code, fichier="AMECO15.TXT"):
    p = _exige(DON / "A06" / "sources" / "ameco" / fichier)
    with open(p, encoding="utf-8", errors="replace") as f:
        hdr = f.readline().rstrip("\n").split(";")
        for line in f:
            if line.startswith(code + ";"):
                c = line.rstrip("\n").split(";")
                return {int(hdr[j]): float(c[j]) for j in range(5, min(len(c), len(hdr)))
                        if hdr[j].strip().isdigit() and c[j] not in ("NA", "")}
    raise SystemExit("ERREUR : série AMECO absente : " + code)


def lire_ocde():
    p = _exige(SOURCES_D01 / "ocde_recettes_fiscales_FRA_1973_1986.csv")
    res = {}
    with open(p, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["MEASURE"] == "TAX_REV" and r["SECTOR"] == "S13" and r["CTRY_SPECIFIC_REVENUE"] == "_T" \
                    and r["OBS_VALUE"] not in ("", None):
                k = (r["STANDARD_REVENUE"], r["UNIT_MEASURE"])
                res.setdefault(k, {})[int(r["TIME_PERIOD"])] = float(r["OBS_VALUE"])
    return res


def lire_codex_ponts():
    p = _exige(CODEX / "calculs" / "ponts_points_pib.csv")
    with open(p, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def lire_codex_annuel():
    p = _exige(CODEX / "calculs" / "annuel.csv")
    with open(p, encoding="utf-8-sig") as f:
        return {int(r["annee"]): r for r in csv.DictReader(f, delimiter=";")}


def lire_csv(p, sep=";"):
    with open(_exige(p), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=sep))


# --------------------------------------------------------------------------
# Transcriptions (signalées comme telles au §8 du dossier)
#
# Taux de cotisation sous plafond, régime général + Unédic, par date d'effet
# (année décimale, taux en % du salaire brut). Reprise à l'identique de la table
# `comp` de scripts/S01/s01_agreger.py (lecture S01 des Barèmes IPP), avec la
# cotisation chômage séparée en part employeur / part salarié d'après
# donnees/S01/S01_taux_cotisations_ipp_1970_2000.csv (premier taux = tranche A).
# Maladie salarié et vieillesse salarié avant 1976 : valeur S01 (1967), absente
# de l'extrait IPP conservé -> marque [S].
TAUX_EMPLOYEUR = {
    "maladie_empl": [(1971.0, 12.45), (1976.0, 12.95), (1976.75, 13.45), (1984.0, 12.6)],
    "vieil_empl": [(1974.0, 7.25), (1976.0, 7.5), (1976.75, 7.7), (1979.0, 8.2)],
    "famille_empl": [(1970.58, 10.5), (1974.25, 9.0)],
    "chomage_empl": [(1973.0, 0.56), (1974.0, 0.64), (1975.0, 1.44), (1975.5, 1.92), (1977.0, 1.76),
                     (1978.0, 1.92), (1978.33, 2.40), (1979.25, 2.76), (1982.85, 3.48), (1983.5, 4.08),
                     (1984.25, 2.88), (1985.5, 4.08), (1985.83, 3.07)],
}
TAUX_SALARIE = {
    "maladie_sal": [(1967.75, 3.5), (1976.0, 4.0), (1976.75, 4.5), (1979.58, 5.5)],
    "vieil_sal": [(1967.75, 3.0), (1976.0, 3.25), (1976.75, 3.45), (1979.0, 4.7), (1984.0, 5.7)],
    "chomage_sal": [(1973.0, 0.14), (1974.0, 0.16), (1975.0, 0.36), (1975.5, 0.48), (1977.0, 0.44),
                    (1978.0, 0.48), (1978.33, 0.60), (1979.25, 0.84), (1982.85, 1.32), (1983.5, 1.72),
                    (1984.25, 1.12), (1985.5, 2.12), (1985.83, 1.51)],
}

# Barème de l'IR : relèvement des limites de tranches voté en loi de finances
# pour l'année N (revenus de N-1), en %, (plus fort, plus faible), d'après les
# lignes de donnees/S01/S01_mesures_1975_1999.csv (pièces Sénat lues par S01).
# None = absent des pièces lues (non établi).
BAREME_IR = {
    1975: None, 1976: None,
    1977: (9.5, 0.0),   # S01 ligne 29 : 9,5 % des 4 premières ... dernière inchangée
    1978: (7.5, 5.0),   # S01 ligne 45
    1979: (9.0, 5.0),   # S01 ligne 51
    1980: (8.0, 0.0),   # S01 ligne 56 : rien pour les trois dernières
    1981: (13.3, 8.0),  # S01 ligne 60
    1982: (13.5, 13.5),  # S01 ligne 72 : indexé de 13,5 %
    1983: (12.3, 12.3),  # S01 ligne 86 : indexé de 12,3 %
    1984: None,          # S01 ligne 96 : « élargissement des tranches », taux non donné
    1985: None,          # S01 ligne 103 : allègement de 10 Md F, taux non donné
}

# Majorations exceptionnelles (temporaires) d'IR, Md F, d'après S01_mesures_1975_1999.csv
# (année d'encaissement supposée = année de la mesure, comme dans S01).
MAJORATIONS_IR = {
    1974: 2.65,  # S01 ligne 2 : LFR du 16/07/1974, majorations exceptionnelles d'IR
    1976: 2.25,  # S01 ligne 18 : plan Barre, majoration exceptionnelle progressive
    1981: 3.4,   # S01 ligne 68 : LFR du 03/08/1981
    1982: 6.0,   # S01 ligne 73 : LFI 1982, au profit de l'Unédic
    1983: 7.0,   # S01 ligne 90 : plan de mars 1983 (S01 : « agrégat », recouvrement possible)
}
