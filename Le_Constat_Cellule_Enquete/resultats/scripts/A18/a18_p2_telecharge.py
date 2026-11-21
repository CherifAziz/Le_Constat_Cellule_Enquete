# -*- coding: utf-8 -*-
"""A18 partie 2 - telechargement a l'origine (API Eurostat) des series absentes de la base commune.
Ecrit les JSON bruts dans donnees\\A18\\sources\\p2\\ et ajoute une ligne par fichier au manifeste
donnees\\A18\\MANIFESTE_PIECES_P2.csv (fichier ; url_origine ; canal ; date ; octets ; sha256)."""
import requests, hashlib, os, datetime
D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18"
S = os.path.join(D, "sources", "p2")
os.makedirs(S, exist_ok=True)
B = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
REQ = {
    "eurostat_nama_10_gdp_FR_EA20_B1GQ.json":
        B + "nama_10_gdp?format=JSON&lang=EN&na_item=B1GQ&unit=CP_MEUR&unit=CLV20_MEUR&unit=CLV10_MEUR&unit=PD20_EUR&unit=PD10_EUR&geo=FR&geo=EA20",
    "eurostat_gov_10a_exp_MIOEUR_FR_EA20_2022_2024.json":
        B + "gov_10a_exp?format=JSON&lang=EN&unit=MIO_EUR&sector=S13&na_item=TE&geo=FR&geo=EA20&time=2022&time=2023&time=2024",
    "eurostat_gov_10a_main_FR_D41_TE_TR_B9_1978_2025.json":
        B + "gov_10a_main?format=JSON&lang=EN&unit=PC_GDP&unit=MIO_EUR&sector=S13&na_item=D41PAY&na_item=TE&na_item=TR&na_item=B9&geo=FR",
}
man = os.path.join(D, "MANIFESTE_PIECES_P2.csv")
new = not os.path.exists(man)
with open(man, "a", encoding="utf-8") as m:
    if new:
        m.write("fichier;url_origine;canal;date;octets;sha256\n")
    for f, u in REQ.items():
        r = requests.get(u, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
        print(f, r.status_code, len(r.content))
        if r.status_code != 200:
            continue
        p = os.path.join(S, f)
        with open(p, "wb") as h:
            h.write(r.content)
        sha = hashlib.sha256(r.content).hexdigest()
        m.write(f"sources\\p2\\{f};{u};requests API Eurostat (HTTP 200);{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')};{len(r.content)};{sha}\n")
