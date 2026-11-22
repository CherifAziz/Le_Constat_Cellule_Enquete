# -*- coding: utf-8 -*-
"""D09 - retéléchargement des pièces à leur adresse d'origine et comparaison des empreintes.

Pour chaque pièce : empreinte SHA-256 de la copie locale (contrôle d'intégrité contre le manifeste),
puis retéléchargement à l'adresse d'origine (curl -L, agent Mozilla), empreinte, verdict
« identique », « différente » ou « origine injoignable (code) ».
Les fichiers retéléchargés identiques sont supprimés ; les fichiers différents sont gardés
dans donnees/D09/_retelechargements/ pour comparaison.
Sortie : donnees/D09/D09_empreintes.csv
"""
import csv
import hashlib
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
OUT = ICI.parent.parent  # claude_approfondissements
DON = OUT / "donnees"
RACINE = OUT.parents[3]  # dossier Le_Constat_Cellule_Enquete (racine des worktrees)
PREMIERE = RACINE / "Le_Constat_Cellule_Enquete" / "resultats" / "donnees"
TMP = DON / "D09" / "_retelechargements"
TMP.mkdir(parents=True, exist_ok=True)

SEN = "https://www.senat.fr/rap/"
SS = "https://www.securite-sociale.fr/files/live/sites/SSFR/files/medias/CCSS/"
VP = "https://www.vie-publique.fr/files/rapport/pdf/"

# (affirmations, chemin local, adresse d'origine, empreinte du manifeste)
PIECES = [
    ("1;3", DON / "D02/sources/senat_i1980_1981_0102_03.pdf", SEN + "1980-1981/i1980_1981_0102_03.pdf",
     "f0ae1ff3a4f69732c13bd39e3127141b1cdc600b0aa50d44c213446455e0dab1"),
    ("2", DON / "D02/sources/CCSS-RAPPORT-JUILLET_1981.pdf", SS + "1981/RAPPORT/CCSS-RAPPORT-JUILLET_1981.pdf",
     "93c63b8a861cbed4665848d3357049c8bb8531899f2cada45eeb6c8645fe985f"),
    ("2", DON / "D02/sources/CCSS-RAPPORT-NOVEMBRE_1980.pdf", SS + "1980/RAPPORT/CCSS-RAPPORT-NOVEMBRE_1980.pdf",
     "62da5db8736b699b43f65c6cce1475c3e25b46d62b7d1064f7820ea95c9f9cb8"),
    ("4", DON / "D02/sources/CCSS-RAPPORT-NOVEMBRE_1981.pdf", SS + "1981/RAPPORT/CCSS-RAPPORT-NOVEMBRE_1981.pdf",
     "376c98978f97f90ab6ec241959ebdc94f807a362f023be5d212885b01ff299f9"),
    ("4", DON / "D02/sources/CCSS-RAPPORT-DECEMBRE_1982.pdf", SS + "1982/RAPPORT/CCSS-RAPPORT-DECEMBRE_1982.pdf",
     "484d969b2065dcc9eea32056bd3260686b019ce12c202f1627cbd5ee3d369e59"),
    ("4", DON / "D02/sources/ccss_rapport_juin_1982.pdf", SS + "1982/RAPPORT/CCSS-RAPPORT-JUIN_1982.pdf",
     "495b1c737b3069bc1535f79342712a9e5fe6fa7d0353820e2382eef36e3c2baa"),
    ("5", DON / "D02/sources/i1980_1981_0098_01.pdf", SEN + "1980-1981/i1980_1981_0098_01.pdf",
     "0311344a392f15092733abe0881ed92cdae7aaedb941e3101bf1ea27c9ccb67c"),
    ("1;6", DON / "D02/sources/senat_i1979_1980_0128.pdf", SEN + "1979-1980/i1979_1980_0128.pdf",
     "1eaa1748c95a03ee145bb74d49db23c27d74136d32192fdc3df95919b86fd988"),
    ("1", DON / "D02/sources/senat_i1979_1980_0054_04.pdf", SEN + "1979-1980/i1979_1980_0054_04.pdf",
     "aca692030f76437627053d314da8750c089c620a9af257b80ffd5dff71e0f97e"),
    ("6", DON / "D03/sources/senat_i1974_1975_0103_02.pdf", SEN + "1974-1975/i1974_1975_0103_02.pdf",
     "1773182301524d75c3cfe2cc1fe8ee4c66af54671892ac9d286e3c636fa76375"),
    ("6", DON / "D03/sources/senat_i1973_1974_0043_02.pdf", SEN + "1973-1974/i1973_1974_0043_02.pdf",
     "5f78d16870924549783a7bfb8fee6cb2c5e4358a535869f0d4fccf4993754b5e"),
    ("7", DON / "D03/sources/dgafp_series_longues_1980_1998.pdf",
     "https://www.fonction-publique.gouv.fr/files/files/ArchivePortailFP/www.fonction-publique.gouv.fr/files/files/statistiques/resulstats/resulstats_series-longues_2007.pdf",
     "40223cf08af64792e06538fdd2079054324a049771b46137539670a97de2d4a8"),
    ("7", PREMIERE / "S01/sources/senat/i1981_1982_0058_01.pdf", SEN + "1981-1982/i1981_1982_0058_01.pdf",
     "27b9dcd7060b191922329fbb7302a91b6bfc15816c6c61e65c47cd2ef17c25db"),
    ("7", PREMIERE / "S01/sources/senat/i1982_1983_0095_01.pdf", SEN + "1982-1983/i1982_1983_0095_01.pdf",
     "bbc60d5212efb4c7c834fa741eb0fc51393ae6e847cc5e3f812b296fd6865efc"),
    ("7", PREMIERE / "S01/sources/senat/i1983_1984_0062_01.pdf", SEN + "1983-1984/i1983_1984_0062_01.pdf",
     "67cc1e7add182f4c2fe53de2e5f949044a7b7f8b7ace0964e79c14935f22c78f"),
    ("8", DON / "D03/sources/drees_er572_depenses_sante_1950_2005.pdf",
     "https://drees.solidarites-sante.gouv.fr/sites/default/files/er572.pdf",
     "3562aa04c2e28220519a7edbcb76bb3c7096ed29896a2d31174e63f59bb41bd1"),
    ("9", PREMIERE / "A04/sources/AN_rapinfo_i2689_Carrez_2010.pdf",
     "https://www.assemblee-nationale.fr/13/pdf/rap-info/i2689.pdf",
     "7dcb2e278469fba09fb89b10af138b3eaf028b8761f1d46dcff7a79b8d4aab0f"),
    ("10", DON / "D05/sources/champsaur_cotis_avril2010_vp104000234.pdf", VP + "104000234.pdf",
     "740652c38fef13224b6b317522793b434a30fb97eba5d956b69fa0d56857fb06"),
    ("11", DON / "D05/sources/dgtresor_DT2009-13_Guyon_Sorbe.pdf",
     "https://www.tresor.economie.gouv.fr/Articles/d3b10342-c12e-444e-a1f0-831c4f82fe8b/files/2448f297-ef0a-4fbe-a068-be1a65f0b29d",
     "932543478e457b4cd5d92eff987796888fb6d52b08a1a71331e5240b25915c77"),
    ("12", DON / "D05/sources/cour_RSPFP_juin2010_vp104000325.pdf", VP + "104000325.pdf",
     "e44aa2e823015ceb45e165c6510016a955e567b8f8078e7f19cf16d013bd5fcd"),
    ("13", DON / "D07/sources/insee_EEC_T207_2025.xlsx",
     "https://www.insee.fr/fr/statistiques/fichier/8977303/EEC_T207.xlsx",
     "a6fbd4cc958970a61f92331d740bd6c2448438cc256d45098914f78f62a71554"),
    ("14", DON / "D07/sources/insee_es348a1_crepon_desplatz_2001.pdf",
     "https://www.insee.fr/fr/statistiques/fichier/1376044/es348a1.pdf",
     "fd1b9c134daa0852b94836f3bbe3b6fff4d6c257df5592d534e4cc70f17b0c33"),
    ("14", DON / "D07/sources/bozio_wasmer_rapport_2024.pdf", VP + "295596.pdf",
     "e95e0fbd73ef498e964e894c905f124abf13f676d1dc865a07a553c588ebc6ec"),
    ("15", DON / "D07/sources/an_r2436_rtt_2014.pdf", "https://www.assemblee-nationale.fr/14/pdf/rap-enq/r2436.pdf",
     "0b50927888c4ece05eb6850b446036e7b792c5ab1119f8bdac0fa3f71ead23b4"),
    ("15", DON / "D07/sources/fs_cice_rapport_2020.pdf",
     "https://www.strategie-plan.gouv.fr/files/files/Publications/2020/CICE/fs-2020-rapport-cice2020-16septembre-final18h.pdf",
     "3118138d2c2deda5a69260a7de52a3e5c9c54a7001ecfa6a7b0456bc65ff49d4"),
]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def telecharger(url: str, dest: Path):
    r = subprocess.run(
        ["curl", "-sS", "-L", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "--max-time", "180",
         "-o", str(dest), "-w", "%{http_code}", url],
        capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip()


def main():
    seul = set(sys.argv[1:])
    lignes = []
    for i, (aff, loc, url, sha_man) in enumerate(PIECES, 1):
        if seul and loc.name not in seul:
            continue
        sha_loc = sha(loc) if loc.exists() else "absente"
        integ = "conforme" if sha_loc == sha_man else "NON CONFORME"
        dest = TMP / loc.name
        code, err = telecharger(url, dest)
        if dest.exists() and code.startswith("2") and dest.stat().st_size > 0:
            s = sha(dest)
            taille = dest.stat().st_size
            if s == sha_man:
                verdict = "identique"
                dest.unlink()
            else:
                verdict = "différente"
        else:
            s, taille = "", 0
            verdict = f"origine injoignable (HTTP {code or 'aucun'}) {err[:80]}".strip()
            if dest.exists():
                dest.unlink()
        print(f"{loc.name}: local {integ}; origine {verdict}")
        lignes.append([aff, loc.name, url, sha_man, sha_loc, integ, code, s, taille, verdict])
    sortie = DON / "D09" / ("D09_empreintes.csv" if not seul else "D09_empreintes_complement.csv")
    with open(sortie, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["affirmations", "fichier", "url_origine", "sha256_manifeste", "sha256_local",
                    "integrite_locale", "http", "sha256_retelecharge", "taille_retelecharge", "verdict_origine"])
        w.writerows(lignes)


if __name__ == "__main__":
    main()
