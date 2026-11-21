"""Relecture A18 indépendante des programmes de production, tableurs sources en entrée."""
import csv
from functools import lru_cache
import json
from pathlib import Path
import warnings

from openpyxl import load_workbook

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "donnees"
OUT = Path(__file__).resolve().parent
YEARS = range(1975, 2026)
warnings.filterwarnings("ignore", message="Workbook contains no default style")


@lru_cache()
def sheet(name, index):
    book = load_workbook(RAW / name, read_only=True, data_only=True)
    values = list(book.worksheets[index].values)
    book.close()
    return values


def series(name, index, header, row):
    table = sheet(name, index)
    return {int(year): value for year, value in zip(table[header-1], table[row-1])
            if str(year).isdigit() and 1900 < int(year) < 2100}


def c(row):
    return series("t_3201_fr.xlsx", 0, 3, row)


def s(row):
    return series("t_3106_fr.xlsx", 0, 3, row)


def d(row):
    return series("t_3101_fr.xlsx", 1, 4, row)


@lru_cache()
def load_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def value(path, **keys):
    data = load_json(path)
    idx = 0
    for dim, size in zip(data["id"], data["size"]):
        choices = data["dimension"][dim]["category"]["index"]
        if dim not in keys and len(choices) != 1:
            raise ValueError(dim)
        key = keys.get(dim, next(iter(choices)))
        idx = idx * size + choices[key]
    return data["value"][str(idx)]


def write(name, rows):
    with (OUT/name).open("w", encoding="utf-8-sig", newline="") as file:
        output = csv.DictWriter(file, rows[0], delimiter=";")
        output.writeheader()
        output.writerows(rows)


gdp = s(29)
volume = series("T_1101_1103_fr.xlsx", 3, 4, 7)
fixed = series("T_1112_fr.xlsx", 1, 4, 8)
rows = []
for year in range(1959, 2026):
    balance, spend, revenue = c(66)[year], c(27)[year], c(58)[year]
    assert abs(balance - (revenue - spend)) < 0.00051
    assert abs(balance - s(5)[year]) < 0.0006
    p = gdp[year]
    rows.append(dict(annee=year, b9=balance, pib=p, pib_volume=volume[year],
        croissance_volume=(volume[year]/volume[year-1]-1)*100,
        dep=spend, rec=revenue, dep_pct=100*spend/p, rec_pct=100*revenue/p,
        solde_pct=100*balance/p, d41=c(12)[year], primaire_d41=balance+c(12)[year],
        primaire_d41g=balance+c(13)[year], primaire_d41_net=balance+c(12)[year]-c(41)[year],
        b8g=c(65)[year], b8n=c(65)[year]-fixed[year], fbcf=c(24)[year],
        ccf=fixed[year], fbcf_nette=c(24)[year]-fixed[year],
        dette=d(7).get(year), dette_pct=(100*d(7)[year]/d(22)[year] if year in d(7) else None)))
write("serie_recalculee.csv", rows)
r = {row["annee"]: row for row in rows}

for label, condition in {
    "primaire D41":lambda t:t["primaire_d41"]>0,
    "primaire D41G":lambda t:t["primaire_d41g"]>0,
    "primaire D41 net":lambda t:t["primaire_d41_net"]>0,
    "épargne brute":lambda t:t["b8g"]>0,
    "épargne nette":lambda t:t["b8n"]>0,
    "déficit > investissement net":lambda t:-t["b9"]>t["fbcf_nette"],
    "déficit > FBCF":lambda t:-t["b9"]>t["fbcf"],
}.items():
    yes=[y for y in YEARS if condition(r[y])]
    print(label,len(yes),yes if len(yes)<20 else ["exceptions",*[y for y in YEARS if y not in yes]])
for y in (1974,1975,1976,1977,1978):
    print("rapprochement",y,s(6)[y],s(7)[y],s(8)[y],s(7)[y]+s(8)[y]-s(6)[y],
        [series("T_1113_fr.xlsx",1,4,n)[y] for n in (9,10,11)])
for y in (1974,1975,1985,1993,2000,2007,2009,2012,2018,2019,2020,2023,2024,2025):
    print(y,[round(r[y][n],3) if r[y][n] is not None else None for n in
        ("b9","dep_pct","rec_pct","solde_pct","croissance_volume","dette_pct","d41")])
print("croissance (TCAM)",[(a,b,100*((volume[b]/volume[a])**(1/(b-a))-1)) for a,b in [(1958,1973),(1959,1974),(1974,1993),(1974,2025)]])
print("fraction hausse 1993", (r[1993]["dep_pct"]-r[1974]["dep_pct"])/(r[2025]["dep_pct"]-r[1974]["dep_pct"]))
print("fourchette depuis 1993",min(r[y]["dep_pct"] for y in range(1993,2026)),max(r[y]["dep_pct"] for y in range(1993,2026)))
print("dette vs PIB",[(r[2025][k]/r[2024][k]-1)*100 for k in ("dette","pib")])
print("2025, déficit/dépenses, millions/jour",-100*r[2025]["b9"]/r[2025]["dep"],-1000*r[2025]["b9"]/365)
print("points de départ et de fin dette en mois",[(y,.12*r[y]["dette_pct"]) for y in (2007,2008,2012,2013,2019,2020,2025)])
print("part des intérêts 1993",-c(12)[1993]/c(66)[1993]*100)
print("max nominal déficit",min(YEARS,key=lambda y:r[y]["b9"]))
print("2026 intérêts par résident",79.2e9/69082000)
print("Suède programme",66.2/125.5*100,59.3/125.5*100)
print("seuil modèle",1/(1.21565751+.5))

ea19minusfr = "BE DE EE IE EL ES HR IT CY LV LT LU MT NL AT PT SI SK FI".split()
def amount(file, geo, **more):
    return value(RAW / file,geo=geo, **more)
def ratio(group, func):
    spending = sum(amount("cofog_2024.json", g, cofog99=func) for g in group)
    denominator = sum(amount("pib_2024.json", g) for g in group)
    return 100 * spending / denominator
cofog=[]
for func in ("TOTAL","GF07","GF10","GF1002"):
    out={"fonction":func}
    for geo in ("FR","EA20"):
        out[geo+"_direct"]=amount("cofog_pct_2024.json",geo,cofog99=func)
        out[geo+"_recalcul"]=ratio([geo],func)
    out["EA_hors_FR_recalcul"]=ratio(ea19minusfr,func)
    cofog.append(out)
write("cofog_recalcule.csv",cofog)
for row in cofog: print(row)
ext=BASE/"preuves_comparaisons"
for geo in ("FR","IT","DE"):
    for year in ((2013,2014,2015,2016,2017,2018,2019,2025) if geo=="DE" else (2025,)):
        debt=value(ext/"dette.json",geo=geo,time=str(year),na_item="GD")
        fiscal=[value(ext/"finances.json",geo=geo,time=str(year),na_item=k) for k in ("TE","TR","B9","D41PAY")]
        print(geo,year,debt,*fiscal)
