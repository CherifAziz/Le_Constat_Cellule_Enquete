"""A12 - lecture des fichiers AMECO (copie de la cellule, donnees\\A06\\sources\\ameco\\).

Usage : importe par les autres scripts A12. Lecture seule. Les fichiers AMECO sont des donnees
telechargees : on les lit comme texte, sans rien executer.
Format : CODE;COUNTRY;SUB-CHAPTER;TITLE;UNIT;1960;...;2028;
CODE = PAYS.1.0.<unite>.<ref>.<VARIABLE>, unite 319 = % du PIB (definition PDE), 0 = monnaie nationale.
"""
import os

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
AMECO_DIR = os.path.join(RACINE, "donnees", "A06", "sources", "ameco")
SORTIE = os.path.join(RACINE, "donnees", "A12")


def lire_ameco(codes_voulus, fichiers=None):
    """Renvoie {code_complet: {"pays":..., "titre":..., "unite":..., "serie": {annee: valeur}}}
    pour les codes dont le suffixe (apres le pays) est dans codes_voulus."""
    res = {}
    if fichiers is None:
        fichiers = sorted(f for f in os.listdir(AMECO_DIR) if f.upper().startswith("AMECO") and f.upper().endswith(".TXT"))
    for f in fichiers:
        with open(os.path.join(AMECO_DIR, f), encoding="latin-1") as h:
            entete = h.readline().rstrip("\n").split(";")
            annees = [int(a) for a in entete[5:] if a.strip().isdigit()]
            for ligne in h:
                c = ligne.rstrip("\n").split(";")
                if len(c) < 6:
                    continue
                code = c[0]
                suffixe = code.split(".", 1)[1] if "." in code else code
                if suffixe not in codes_voulus:
                    continue
                serie = {}
                for a, v in zip(annees, c[5:5 + len(annees)]):
                    v = v.strip()
                    if v and v != "NA":
                        try:
                            serie[a] = float(v)
                        except ValueError:
                            pass
                res[code] = {"pays": c[1], "titre": c[3].strip(), "unite": c[4].strip(), "fichier": f, "serie": serie}
    return res


def pays_de(code):
    return code.split(".", 1)[0]
