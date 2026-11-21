# -*- coding: utf-8 -*-
"""A07 - Telechargement des series de taux, inflation, PIB, dette (sources primaires).
Usage : python -I 01_telecharger_series.py <dossier_sortie>
Chaque fichier est enregistre brut ; un journal (journal_telechargements.csv) consigne URL, date UTC,
code HTTP, taille, SHA-256. Aucune donnee n'est retraitee ici.
"""
import sys, os, hashlib, datetime, csv, time
import requests

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}
ECB = "https://data-api.ecb.europa.eu/service/data/"
EST = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"

JOBS = []
# 1. Taux longs de convergence (BCE, IRS), mensuels, 10 ans
for g in ["FR", "DE", "IT", "ES", "PT", "BE", "NL", "AT", "IE", "GR", "FI", "SE", "DK", "GB"]:
    JOBS.append((f"ecb_IRS_M_{g}.csv", ECB + f"IRS/M.{g}.L.L40.CI.0000.EUR.N.Z?format=csvdata"))
# 2. Taux courts : Euribor 3 mois (BCE, FM) ; taux de la facilite de depot et refi (BCE, FM)
JOBS.append(("ecb_FM_euribor3m_M.csv", ECB + "FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=csvdata"))
JOBS.append(("ecb_FM_DFR_B.csv", ECB + "FM/B.U2.EUR.4F.KR.DFR.LEV?format=csvdata"))
JOBS.append(("ecb_FM_MRR_B.csv", ECB + "FM/B.U2.EUR.4F.KR.MRR_FR.LEV?format=csvdata"))
# 3. Eurostat : rendements de convergence quotidiens et mensuels ; taux courts nationaux ; taux longs annuels
JOBS.append(("eurostat_irt_lt_mcby_d.json", EST + "irt_lt_mcby_d?format=JSON&lang=EN&geo=FR&geo=DE&geo=IT&geo=ES&geo=PT&geo=BE&geo=NL&sinceTimePeriod=2024-01-01"))
JOBS.append(("eurostat_irt_lt_mcby_m.json", EST + "irt_lt_mcby_m?format=JSON&lang=EN&geo=FR&geo=DE&geo=IT&geo=ES&geo=PT&geo=BE&geo=NL&geo=SE"))
JOBS.append(("eurostat_irt_lt_mcby_a.json", EST + "irt_lt_mcby_a?format=JSON&lang=EN"))
JOBS.append(("eurostat_irt_st_a.json", EST + "irt_st_a?format=JSON&lang=EN"))
JOBS.append(("eurostat_irt_lt_gby10_a.json", EST + "irt_lt_gby10_a?format=JSON&lang=EN"))
# 4. PIB nominal et reel, deflateur (Eurostat nama_10_gdp)
JOBS.append(("eurostat_nama_10_gdp.json", EST + "nama_10_gdp?format=JSON&lang=EN&na_item=B1GQ&unit=CP_MEUR&unit=CLV_PCH_PRE&unit=PD_PCH_PRE_EUR&unit=CP_MNAC&geo=FR&geo=DE&geo=IT&geo=ES&geo=PT&geo=BE&geo=NL&geo=SE&geo=EA20"))
# 5. Inflation IPCH annuelle (Eurostat)
JOBS.append(("eurostat_prc_hicp_aind.json", EST + "prc_hicp_aind?format=JSON&lang=EN&coicop=CP00&unit=RCH_A_AVG&geo=FR&geo=DE&geo=IT&geo=ES&geo=EA20&geo=SE"))
# 6. Dette par detenteurs / instruments (Eurostat, comptes financiers des APU)
# (premiere tentative sans filtre sector/na_item : HTTP 413 ; requete filtree effectivement utilisee :)
JOBS.append(("eurostat_gov_10dd_ggd.json", EST + "gov_10dd_ggd?format=JSON&lang=EN&geo=FR&geo=IT&geo=DE&geo=ES&geo=BE&unit=PC_GDP&sector=S13&na_item=GD"))
# Note : irt_lt_mcby_d (quotidien) renvoie 404 "not available for dissemination" ; conserve pour trace.
# 7. OCDE (SDMX) : taux courts 3 mois, taux longs, taux au jour le jour ; IPC annuel
OECD = "https://sdmx.oecd.org/public/rest/data/"
JOBS.append(("oecd_finmark_A.csv", OECD + "OECD.SDD.STES,DSD_STES@DF_FINMARK,4.0/FRA+DEU+ITA+ESP+SWE+GBR+BEL+PRT.A.IR3TIB+IRLT+IRSTCI.PA.....?startPeriod=1960&format=csvfilewithlabels"))
JOBS.append(("oecd_finmark_M.csv", OECD + "OECD.SDD.STES,DSD_STES@DF_FINMARK,4.0/FRA+DEU+ITA+SWE.M.IR3TIB+IRLT.PA.....?startPeriod=1970&format=csvfilewithlabels"))
JOBS.append(("oecd_prices_A.csv", OECD + "OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/FRA+DEU+ITA+SWE+ESP.A.N.CPI.PA._T.N.GY?startPeriod=1960&format=csvfilewithlabels"))

def run():
    log = os.path.join(OUT, "journal_telechargements.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(["fichier", "url", "date_utc", "http", "octets", "sha256"])
        for fname, url in JOBS:
            if len(sys.argv) > 2 and sys.argv[2] not in fname:
                continue
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            try:
                r = requests.get(url, headers=UA, timeout=180)
                code, data = r.status_code, r.content
            except Exception as e:
                code, data = "ERR:" + type(e).__name__, b""
            sha = hashlib.sha256(data).hexdigest() if data else ""
            if data and code == 200:
                with open(os.path.join(OUT, fname), "wb") as f:
                    f.write(data)
            w.writerow([fname, url, ts, code, len(data), sha])
            print(fname, code, len(data))
            time.sleep(0.5)

if __name__ == "__main__":
    run()
