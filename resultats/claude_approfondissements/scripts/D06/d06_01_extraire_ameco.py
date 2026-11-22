"""D06 - étape 1 : extrait d'AMECO les lignes utiles aux huit pays.

Source : fichiers AMECO en vrac téléchargés par l'agent A06 le 20/11/2026
(lecture seule, dépôt principal). L'extrait est conservé sous donnees/D06/sources
pour que les calculs suivants ne dépendent que de pièces conservées sous OUT.
Relancer seulement si l'on veut refaire l'extrait depuis la pièce A06.
"""
import csv, hashlib, os, glob

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
# OUT = .../.worktrees/claude-approfondissements/resultats/claude_approfondissements
RACINE = _racine_depot(ICI)
SRC = os.path.join(RACINE, "Le_Constat_Cellule_Enquete", "resultats", "donnees", "A06", "sources", "ameco")
DEST = os.path.join(OUT, "donnees", "D06", "sources", "ameco_extrait_D06.csv")

PAYS = ["FRA", "DEU", "D_W", "ITA", "ESP", "NLD", "SWE", "GBR", "USA"]
CODES = [
    "1.1.0.0.OVGD", "1.0.0.0.NLHT", "1.0.0.0.NLHA", "1.0.0.0.NPAN", "1.0.0.0.NPTD",
    "1.1.0.0.RVGDP", "1.0.0.0.NETD", "1.0.0.0.NETM", "1.1.0.0.UVGM", "1.0.0.0.UVGM",
    "1.1.0.0.UVG0", "1.1.0.0.OVGM", "1.1.0.0.OVG0",
    "1.0.319.0.UBLGE", "1.0.319.0.UBLGAP", "1.0.319.0.UBLGAPS",
    "1.0.0.0.OVGDP", "1.0.0.0.AVGDGP", "3.0.0.0.ZVGDF",
]

def main():
    fichiers = sorted(glob.glob(os.path.join(SRC, "AMECO*.TXT")))
    lignes, entete = [], None
    for f in fichiers:
        with open(f, encoding="utf-8", errors="replace") as h:
            r = csv.reader(h, delimiter=";")
            e = next(r)
            entete = entete or e
            for row in r:
                if not row:
                    continue
                code = row[0]
                p, _, reste = code.partition(".")
                if p in PAYS and reste in CODES:
                    lignes.append(row)
    with open(DEST, "w", encoding="utf-8", newline="") as h:
        w = csv.writer(h, delimiter=";")
        w.writerow(entete)
        w.writerows(lignes)
    print(len(lignes), "lignes ->", DEST)
    for f in fichiers:
        print(os.path.basename(f), hashlib.sha256(open(f, "rb").read()).hexdigest())

if __name__ == "__main__":
    main()
