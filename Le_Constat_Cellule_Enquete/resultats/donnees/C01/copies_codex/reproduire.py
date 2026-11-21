"""Recalcul hors ligne. Python 3.10+ et openpyxl en lecture seule."""
import csv
import hashlib
import itertools
import json
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "donnees"
OUT = ROOT / "calculs"
OUT.mkdir(exist_ok=True)


def export(name, records):
    records = list(records)
    with (OUT / (name + ".csv")).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=records[0], delimiter=";")
        writer.writeheader()
        for record in records:
            writer.writerow({k: round(v, 6) if isinstance(v, float) else v for k, v in record.items()})


def sheet(filename, index=0):
    book = load_workbook(DATA / (filename + "_fr.xlsx"), read_only=True, data_only=True)
    values = list(book.worksheets[index].values)
    book.close()
    return values


def extract(table, header, mapping):
    dates = table[header-1]
    return {int(year): {name: (table[row-1][i] if isinstance(table[row-1][i], (float, int)) else None)
                        for name, row in mapping.items()}
            for i, year in enumerate(dates) if str(year).isdigit() and 1900 < int(year) < 2100}


apu = extract(sheet("t_3201"), 3, dict(dep=27, rec=58, b9=66, interets=12, interets_d41g=13,
    interets_recus=41, fbcf=24, epargne_brute=65, fonctionnement=5, transferts_prestations=15,
    actifs_non_financiers=23, salaires=7, prestations_especes=16, transferts_nature_marchands=17,
    subventions=18, transferts_capital_payes=21, transferts_capital_recus=56,
    credits_impots_dep=30, credits_impots_rec=61))
gdp = extract(sheet("T_1101_1103",1),4,dict(pib=7))
real = extract(sheet("T_1101_1103",3),4,dict(pib_volume=7))
ccf = extract(sheet("T_1112",1),4,dict(ccf=8))
accounts = extract(sheet("T_7301",1),4,dict(ccf_compte=14, epargne_nette_compte=127, b9_compte=145))
sectors = extract(sheet("t_3106"),3,dict(b9_edp=5, centre=6, etat=7, odac=8, apul=9, asso=10, pib_edp=29))
stocks = extract(sheet("t_3101",1),4,dict(dette=7, ratio_officiel=15))
etp = extract(sheet("T_1109",1),4,dict(etp_total_milliers=16,etp_apu_milliers=8))
hours = extract(sheet("T_6213",1),4,dict(heures_millions=53))
productivity = extract(sheet("T_6215",1),4,dict(productivite_horaire_va_variation_pct=53))
survey=load_workbook(DATA/"ip2096.xlsx",read_only=True,data_only=True)
labour={int(v[0]):dict(emploi_15_64_pct=v[4],emploi_50_64_pct=v[3]) for v in survey["Figure 1"].values if str(v[0]).isdigit()}
for v in survey["Figure 5"].values:
    if str(v[0]).isdigit():
        labour[int(v[0])]["chomage_BIT_pct"]=v[1]
survey.close()
gross = extract(sheet("t_3215"),3,dict(etat_d=7,etat_r=8,odac_d=10,odac_r=11,apul_d=13,apul_r=14,asso_d=16,asso_r=17))


def make_history():
    data = {}
    for year in range(1974,2026):
        row = {"annee":year}
        for table in (apu,gdp,real,ccf,accounts,sectors,stocks,etp,hours,productivity,labour,gross):
            row.update(table.get(year,dict.fromkeys(next(iter(table.values())))))
        p = row["pib_edp"]
        row["g_nominal_pct"] = 100*(p/sectors[year-1]["pib_edp"]-1)
        row["g_reel_pct"] = 100*(row["pib_volume"]/real[year-1]["pib_volume"]-1)
        row["deflateur_pct"] = 100*((1+row["g_nominal_pct"]/100)/(1+row["g_reel_pct"]/100)-1)
        row["primaire"] = row["b9"]+row["interets"]
        row["primaire_d41g"] = row["b9"]+row["interets_d41g"]
        row["primaire_interets_nets"] = row["primaire"]-row["interets_recus"]
        row["investissement_net"] = row["fbcf"]-row["ccf"]
        row["b9_plus_fbcf"] = row["b9"]+row["fbcf"]
        row["b9_plus_invest_net"] = row["b9"]+row["investissement_net"]
        row["dep_primaires"] = row["dep"]-row["interets"]
        row["dep_rec_reconciliation"] = row["rec"]-row["dep"]-row["b9_edp"]
        row["residu_sous_secteurs"] = row["b9_edp"]-row["centre"]-row["apul"]-row["asso"]
        for name in ["dep","rec","b9","interets","primaire","dep_primaires","dette","fbcf",
                     "investissement_net","epargne_brute","fonctionnement","transferts_prestations","actifs_non_financiers"]:
            row[name+"_pct"] = 100*row[name]/p if row[name] is not None else None
        row["consolidation_dep"] = sum(row[k+"_d"] for k in ("etat","odac","apul","asso"))-row["dep"] if year in gross else None
        row["consolidation_rec"] = sum(row[k+"_r"] for k in ("etat","odac","apul","asso"))-row["rec"] if year in gross else None
        row["dette_variation_pts"] = row["effet_croissance_pts"] = row["sfa"] = row["sfa_pts"] = None
        if year-1 in stocks:
            past = stocks[year-1]["dette"]
            past_ratio = 100*past/sectors[year-1]["pib_edp"]
            row["sfa"] = row["dette"]-past+row["b9"]
            row["sfa_pts"] = 100*row["sfa"]/p
            row["effet_croissance_pts"] = 100*past/p-past_ratio
            row["dette_variation_pts"] = row["dette_pct"]-past_ratio
            assert abs(row["dette_variation_pts"]-(-row["primaire_pct"]+row["interets_pct"]+row["effet_croissance_pts"]+row["sfa_pts"])) < 1e-8
        assert abs(row["dep_rec_reconciliation"]) < .003 and abs(row["residu_sous_secteurs"]) < .003
        assert abs(row["b9"]-row["b9_compte"]) < .003
        row["ecart_brut_etat_odac_centre"] = row["etat"]+row["odac"]-row["centre"]
        if year < 1978:
            # 3.106 donne des composantes incompatibles avec S1311. 1.113 les laisse vides.
            row["etat"] = row["odac"] = None
        else:
            assert abs(row["etat"]+row["odac"]-row["centre"]) < .003
        assert abs(row["dep"]-sum(row[k] for k in ("fonctionnement","interets","transferts_prestations","actifs_non_financiers"))) < .003
        data[year] = row
    return data


history = make_history()
export("annuel",history.values())
windows = [(1974,1975),(1975,1980),(1980,1985),(1985,1993),(1993,2000),(1994,1998),(2000,2007),
           (2007,2009),(2011,2015),(2015,2019),(2019,2020),(2020,2023),(2023,2024),(2024,2025),(1974,2025)]
bridges = []
for start,end in windows:
    a,b = history[start],history[end]
    dif = {key:b[key+"_pct"]-a[key+"_pct"] for key in
           ("b9","rec","dep_primaires","interets","fonctionnement","transferts_prestations","actifs_non_financiers")}
    assert abs(dif["b9"]-dif["rec"]+dif["dep_primaires"]+dif["interets"]) < 1e-7
    bridges.append({"debut":start,"fin":end,**dif})
export("ponts_points_pib",bridges)
waterfalls=[]
for start,end in [(1998,2001),(2007,2009),(2015,2019),(2019,2020),(2020,2023),(2023,2025)]:
    rows=[history[y] for y in range(start+1,end+1)]
    waterfalls.append(dict(debut=start,fin=end,delta_dette=sum(r["dette_variation_pts"] for r in rows),
        deficit_primaire=-sum(r["primaire_pct"] for r in rows),interets=sum(r["interets_pct"] for r in rows),
        croissance_nominale=sum(r["effet_croissance_pts"] for r in rows),stock_flux=sum(r["sfa_pts"] for r in rows)))
export("decomposition_dette",waterfalls)
macro=[]
for start,end in [(1978,1990),(1990,2007),(2007,2019),(2019,2025)]:
    def annual_rate(key):
        return (history[end][key]/history[start][key])**(1/(end-start))
    output,employment,hour=annual_rate("pib_volume"),annual_rate("etp_total_milliers"),annual_rate("heures_millions")
    macro.append(dict(debut=start,fin=end,pib_reel_pct_an=100*(output-1),etp_pct_an=100*(employment-1),
        pib_reel_par_etp_pct_an=100*(output/employment-1),heures_pct_an=100*(hour-1),
        pib_reel_par_heure_pct_an=100*(output/hour-1)))
export("emploi_production",macro)


def count_test(name, eligible, condition):
    years = [y for y,r in history.items() if y>=1975 and eligible(r)]
    valid = [y for y in years if condition(history[y])]
    return dict(test=name, nombre=len(valid), observables=len(years), annees=" ".join(map(str,valid)))


tests = {"solde négatif":lambda r:r["b9"]<0,"croissance réelle positive":lambda r:r["g_reel_pct"]>0,
         "primaire D41 positif":lambda r:r["primaire"]>0,"primaire D41G positif":lambda r:r["primaire_d41g"]>0,
         "primaire intérêts nets positif":lambda r:r["primaire_interets_nets"]>0,
         "déficit supérieur à FBCF brute":lambda r:r["b9_plus_fbcf"]<0,
         "déficit supérieur à FBCF nette":lambda r:r["b9_plus_invest_net"]<0,
         "épargne brute positive":lambda r:r["epargne_brute"]>0,
         "épargne nette positive (B8g moins CCF)":lambda r:r["epargne_brute"]-r["ccf"]>0}
counts = [count_test(name,lambda r:True,func) for name,func in tests.items()]
counts += [count_test("ratio de dette en baisse (niveaux recalculés)",lambda r:r["dette_variation_pts"] is not None,lambda r:r["dette_variation_pts"]<0)]
export("frequences",counts)

# Le tableau intersectoriel conserve le millésime commun de mai, y compris pour S13.
private = extract(sheet("T_1113",1),4,dict(snf=6,sf=7,apu_mai=8,menages=14,isblsm=15,nation=16))
sector_rows = []
for year in history:
    r = private[year]
    domestic_private = r["snf"]+r["sf"]+r["menages"]+r["isblsm"]
    residual = domestic_private+r["apu_mai"]-r["nation"]
    assert abs(residual) < .003
    sector_rows.append(dict(annee=year,**r,prive_resident=domestic_private,residu=residual))
export("contreparties_mai",sector_rows)


def passage(file, header, mapping):
    series = extract(sheet(file),header,mapping)
    return [dict(annee=year,**r) for year,r in series.items() if year<=2025]


export("passage_etat",passage("t_3107",4,dict(execution=5,financieres=9,droits_constates=14,non_budgetaires=42,etat_maastricht=66)))
export("passage_asso",passage("t_3108",3,dict(regime_general=5,corrections=7,regime_general_cn=20,
    hors_regime_general=22,cades=23,frr=24,autres_regimes=25,organismes_dependants=26,asso=28)))
export("passage_dette",passage("t_3105",3,dict(deficit=5,acquisitions_actifs=7,passif_hors_dette=15,
    volumes_et_valorisation=19,autres_comptes=24,ecart_statistique=26,variation_dette=28)))


def jsonstat(file):
    j = json.loads((DATA / (file+".json")).read_text(encoding="utf-8-sig"))
    dimensions = [j["dimension"][k]["category"]["index"] for k in j["id"]]
    codes = [sorted(dim,key=dim.get) for dim in dimensions]
    data = {}
    for index,keys in enumerate(itertools.product(*codes)):
        value = j["value"].get(str(index))
        if value is not None:
            data[tuple(keys)] = value
    return j,lambda **q:data[tuple(q[d] for d in j["id"])]


partners = "AT BE CY DE EE EL ES FI HR IE IT LT LU LV MT NL PT SI SK".split()
co,get_co = jsonstat("cofog_2024")
gp,get_gp = jsonstat("pib_2024")
_,get_published = jsonstat("cofog_pct_2024")


def gdp_eu(geo):
    return get_gp(freq="A",unit="CP_MEUR",na_item="B1GQ",geo=geo,time="2024")


def cof(geo,function):
    return get_co(freq="A",unit="MIO_EUR",na_item="TE",sector="S13",geo=geo,time="2024",cofog99=function)


funcs = ["TOTAL"]+["GF%02d"%i for i in range(1,11)]+["GF1002"]
co_rows = []
for f in funcs:
    others = 100*sum(cof(c,f) for c in partners)/sum(gdp_eu(c) for c in partners)
    fr = 100*cof("FR",f)/gdp_eu("FR")
    ea = 100*cof("EA20",f)/gdp_eu("EA20")
    native = {c:get_published(freq="A",unit="PC_GDP",na_item="TE",sector="S13",geo=c,time="2024",cofog99=f) for c in ("FR","EA20")}
    co_rows.append(dict(fonction=f,libelle=co["dimension"]["cofog99"]["category"]["label"][f],fr=fr,
        partenaires_19=others,ecart_fr_19=fr-others,ea20_recalculee=ea,ecart_fr_ea20=fr-ea,
        fr_ratio_diffuse=native["FR"],ea20_ratio_diffuse=native["EA20"]))
export("fonctions_2024",co_rows)
long_meta,long_value=jsonstat("cofog_fr_long")
long_rows=[]
for year in range(1995,2025):
    for function in funcs:
        amount=long_value(freq="A",unit="MIO_EUR",na_item="TE",sector="S13",geo="FR",time=str(year),cofog99=function)
        long_rows.append(dict(annee=year,fonction=function,
            libelle=long_meta["dimension"]["cofog99"]["category"]["label"][function],
            depense_MdEUR=amount/1000,part_pib_pct=amount/10/history[year]["pib_edp"]))
export("fonctions_fr_1995_2024",long_rows)

source_rows = []
for p in sorted(DATA.glob("*")):
    if p.suffix==".xlsx":
        key=p.name.lower()
        publication=("8988797" if key.startswith("t_1") else "8988843" if key.startswith("t_31")
            else "8988845" if key.startswith("t_32") else "8988823" if key.startswith("t_6")
            else "8901327" if key=="ip2096.xlsx" else "8988833")
        url=f"https://www.insee.fr/fr/statistiques/fichier/{publication}/{p.name}"
    elif p.name=="cofog_2024.json":
        url="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_exp?lang=fr&freq=A&unit=MIO_EUR&sector=S13&na_item=TE&time=2024"
    elif p.name=="pib_2024.json":
        url="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?lang=fr&freq=A&unit=CP_MEUR&na_item=B1GQ&time=2024"
    elif p.name=="cofog_pct_2024.json":
        url="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_exp?lang=fr&freq=A&unit=PC_GDP&sector=S13&na_item=TE&time=2024&geo=FR&geo=EA20"
    elif p.name=="cofog_fr_long.json":
        url="https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_exp?lang=fr&freq=A&unit=MIO_EUR&sector=S13&na_item=TE&geo=FR&sinceTimePeriod=1995&untilTimePeriod=2024"
    else:
        continue
    source_rows.append(dict(fichier=p.name,url=url,consultation="2026-11-20",octets=p.stat().st_size,
                            sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
export("sources_et_empreintes",source_rows)
print(f"{len(history)} exercices. {len(bridges)} ponts. {len(counts)} tests. {len(source_rows)} pièces.")
