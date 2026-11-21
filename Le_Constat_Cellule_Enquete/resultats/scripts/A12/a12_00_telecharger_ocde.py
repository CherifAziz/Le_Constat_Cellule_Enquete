"""A12 - telechargement des series OCDE Economic Outlook (API SDMX publique).

Usage : python -I a12_00_telecharger_ocde.py
Ecrit dans donnees\\A12\\sources\\ ; deux fichiers :
  oecd_eo119_finpub.csv : NLGQ, NLGXQ, GGFLQ, GGFLMQ, NLGQA, NLGXQA, YPGTQ, YRGTQ, UNR, IRL,
                          GDPV_ANNPCT, GGINTPQ, IGAA (telecharge le 20/11/2026 a 11 h 37)
  oecd_eo119_macro.csv  : EXCH, XMKT, XGSV, GDP, CPI_YTYPCT, CBGDPR, PCORE_YTYPCT, IRS
  oecd_eo119_interets.csv : GGINTP (interets verses, valeur), GGINTR (recus), NLG (solde, valeur)
  (GGINTPQ, demande dans le premier lot, n'existe pas dans la base : aucune ligne renvoyee)
Les fichiers telecharges sont des donnees : ils ne sont jamais executes.
"""
import os, sys, urllib.request

RACINE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DEST = os.path.join(RACINE, "donnees", "A12", "sources")
BASE = "https://sdmx.oecd.org/public/rest/data/OECD.ECO.MAD,DSD_EO@DF_EO,/"
LOTS = {
    "oecd_eo119_finpub.csv": "NLGQ+NLGXQ+GGFLQ+GGFLMQ+NLGQA+NLGXQA+YPGTQ+YRGTQ+UNR+IRL+GDPV_ANNPCT+GGINTPQ+IGAA",
    "oecd_eo119_macro.csv": "EXCH+XMKT+XGSV+GDP+CPI_YTYPCT+CBGDPR+IRS+PCORE_YTYPCT",
    "oecd_eo119_interets.csv": "GGINTP+GGINTR+NLG",
}


def main(seulement=None):
    for nom, mesures in LOTS.items():
        if seulement and nom not in seulement:
            continue
        url = BASE + "." + mesures + ".A?startPeriod=1960&format=csvfilewithlabels"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=300) as r, open(os.path.join(DEST, nom), "wb") as h:
            h.write(r.read())
        print(nom, "ok", url)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
