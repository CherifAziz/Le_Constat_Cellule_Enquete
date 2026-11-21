r"""S02 - Taux de risque de pauvrete (seuil 60 % du revenu median, apres transferts), Eurostat ilc_li02, API JSON.
Telecharge le JSON brut dans donnees\S02\sources\eurostat_ilc_li02.json (manifeste via s02_dl.py --register) et ecrit
donnees\S02\S02_pauvrete_ilc_li02.csv (DE, BE, IT, FR, EA20 ; total population ; 1995-2025 si disponible).
Rupture : avant 2005 (DE) / 2004 (BE, IT, FR) = ECHP ou sources nationales selon Eurostat ; signalee par le statut 'b'."""
import json, os, csv, requests, sys
B = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S02"
url = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_li02?format=JSON&lang=EN"
       "&unit=PC&rskpovth=B_60&statinfo=MED_EI&sex=T&age=TOTAL&geo=DE&geo=BE&geo=IT&geo=FR&geo=EA20")
r = requests.get(url, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
print(r.status_code, len(r.content))
r.raise_for_status()
raw = os.path.join(B, "sources", "eurostat_ilc_li02.json")
open(raw, "wb").write(r.content)
j = r.json()
geo = j["dimension"]["geo"]["category"]["index"]; tim = j["dimension"]["time"]["category"]["index"]
sizes = j["size"]; ids = j["id"]
ng, nt = sizes[ids.index("geo")], sizes[ids.index("time")]
rows = []
for g, gi in geo.items():
    for t, ti in tim.items():
        k = str(gi * nt + ti)
        if k in j["value"]:
            rows.append([g, t, j["value"][k], j.get("status", {}).get(k, "")])
with open(os.path.join(B, "S02_pauvrete_ilc_li02.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["geo", "annee", "taux_pauvrete_60pct", "statut"]); w.writerows(rows)
for g in geo:
    print(g, [(t, v, s) for gg, t, v, s in rows if gg == g])
