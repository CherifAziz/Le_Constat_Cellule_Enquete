# -*- coding: utf-8 -*-
"""A03 - telechargement des series macroeconomiques (non presentes dans la base commune).
Sources : API Eurostat (dissemination 1.0) et AMECO (Commission europeenne).
Ecrit les reponses brutes dans resultats/donnees/A03/sources/ et un journal MANIFESTE_A03.csv.
Lancer avec : python -I telecharger_macro.py
"""
import os, hashlib, datetime, csv, requests

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03", "sources"))
os.makedirs(OUT, exist_ok=True)
EU = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
REQ = {
    # PIB : prix courants (Md EUR) et variation en volume (%)
    "eurostat_nama_10_gdp.json": EU + "nama_10_gdp?format=JSON&lang=EN&freq=A&na_item=B1GQ&unit=CP_MEUR&unit=CLV_PCH_PRE&unit=PD_PCH_PRE_EUR&geo=FR&geo=DE&geo=IT&geo=EA20",
    # IPCH, taux annuel moyen
    "eurostat_prc_hicp_aind.json": EU + "prc_hicp_aind?format=JSON&lang=EN&freq=A&unit=RCH_A_AVG&coicop=CP00&geo=FR&geo=DE&geo=EA",
    # Chomage BIT 15-74 ans, % population active
    "eurostat_une_rt_a.json": EU + "une_rt_a?format=JSON&lang=EN&freq=A&age=Y15-74&sex=T&unit=PC_ACT&geo=FR&geo=DE&geo=EA20",
    # Taux a long terme (critere de convergence), annuel
    "eurostat_irt_lt_mcby_a.json": EU + "irt_lt_mcby_a?format=JSON&lang=EN&freq=A&int_rt=MCBY&geo=FR&geo=DE&geo=IT",
    "eurostat_irt_lt_mcby_m.json": EU + "irt_lt_mcby_m?format=JSON&lang=EN&freq=M&int_rt=MCBY&geo=FR&geo=DE&geo=IT&sinceTimePeriod=2023-01",
    # Chomage BIT Insee, trimestriel CVS, France hors Mayotte
    "insee_bdm_001688527_chomage_bit.xml": "https://bdm.insee.fr/series/sdmx/data/SERIES_BDM/001688527?startPeriod=1999",
}
AMECO = "https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable={v}&countries=FRA,DEU&years=1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027&defaultCountries=0&Lang=EN"
for nom, var in [("ameco_UBLGAPS.html", "1.0.319.0.UBLGAPS"),   # solde structurel, % PIB potentiel
                 ("ameco_UBLGBPS.html", "1.0.319.0.UBLGBPS"),   # solde primaire structurel
                 ("ameco_AVGDGP.html", "1.0.0.0.AVGDGP"),       # ecart de production
                 ("ameco_UBLGIE.html", "1.0.319.0.UBLGIE"),   # solde primaire (EDP)
                 ("ameco_UBLGAP.html", "1.0.319.0.UBLGAP"),   # solde corrige du cycle
                 ("ameco_UBLGBP.html", "1.0.319.0.UBLGBP"),   # solde primaire corrige du cycle
                 ("ameco_UYIGE.html", "1.0.0.0.UYIGE"),       # interets APU, Md
                 ("ameco_UDGG.html", "1.0.319.0.UDGG"),       # dette brute % PIB
                 ("ameco_UBLGE.html", "1.0.319.0.UBLGE")]:    # solde APU (EDP), % PIB   # solde primaire
    REQ[nom] = AMECO.format(v=var)

H = {"User-Agent": "Mozilla/5.0 (research script)"}
journal = []
for nom, url in REQ.items():
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        r = requests.get(url, headers=H, timeout=90)
        b = r.content
        with open(os.path.join(OUT, nom), "wb") as f:
            f.write(b)
        journal.append([nom, url, t, r.status_code, len(b), hashlib.sha256(b).hexdigest()])
        print(nom, r.status_code, len(b))
    except Exception as e:
        journal.append([nom, url, t, "ERREUR " + repr(e)[:120], 0, ""])
        print(nom, "ERREUR", e)
with open(os.path.join(OUT, "..", "MANIFESTE_A03.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if True:
        w.writerow(["fichier", "url", "date_utc", "statut", "octets", "sha256"])
    w.writerows(journal)
