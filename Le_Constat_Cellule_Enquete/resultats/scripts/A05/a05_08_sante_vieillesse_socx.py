# -*- coding: utf-8 -*-
"""A05 travaux 4-5 - tests de périmètre santé (OCDE SHA) et vieillesse (OCDE SOCX, programme TP01), éducation.
Entrées (A05/sources) :
  oecd_DF_SHA_resume.csv  : extrait filtré (FUNCTION=_T, PROVIDER=_T, MODE=_T ; régimes _T, HF1, HF11, HF121, HF122, HF2, HF3)
                            du fichier brut https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_SHA@DF_SHA,1.1/
                            FRA+DEU+ITA+ESP+NLD+BEL+SWE+DNK+FIN+AUT.A..........?startPeriod=2022&endPeriod=2023 (110 Mo, supprimé ; SHA-256 au manifeste)
  oecd_edu_perstud_resume.csv : extrait filtré (source _T, institutions toutes, DIR_EXP, USD_PPP_ST, prix courants)
                            du fichier brut .../DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.2/...?startPeriod=2019 (202 Mo, supprimé)
  oecd_DF_SOCX_AGG.csv    : SOCX agrégats, 10 pays + OCDE, depuis 2015
Sorties : A05_sante_SHA_regimes.csv ; A05_vieillesse_SOCX_public_prive.csv ; A05_education_depense_par_eleve.csv
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a05_commun import *
P = ["FRA", "DEU", "ITA", "ESP", "NLD", "BEL", "SWE", "DNK", "FIN", "AUT"]

# Santé : régimes de financement, % PIB et % dépense courante de santé
r = list(csv.DictReader(open(os.path.join(SRC, "oecd_DF_SHA_resume.csv"), encoding="utf-8")))
S = {(x["REF_AREA"], x["FINANCING_SCHEME"], x["UNIT_MEASURE"], x["TIME_PERIOD"]): float(x["OBS_VALUE"]) for x in r if x["OBS_VALUE"]}
out = []
for y in ("2022", "2023"):
    for p in P:
        row = [y, p]
        for f in ("_T", "HF1", "HF11", "HF121", "HF122", "HF2", "HF3"):
            row.append(S.get((p, f, "PT_B1GQ", y), ""))
        row.append((S.get((p, "HF11", "PT_B1GQ", y), 0) + S.get((p, "HF121", "PT_B1GQ", y), 0)) or "")
        row += [S.get((p, "_T", "EUR_PPP_PS", y), ""), S.get((p, "HF1", "EUR_PPP_PS", y), ""), S.get((p, "HF3", "PT_EXP_HLTH", y), "")]
        out.append(row)
ecrire_csv("A05_sante_SHA_regimes.csv", ["annee", "pays", "total_pctPIB", "HF1_public_et_obligatoire_pctPIB", "HF11_etat_pctPIB",
                                          "HF121_secu_sociale_pctPIB", "HF122_prive_obligatoire_pctPIB", "HF2_volontaire_pctPIB", "HF3_menages_pctPIB",
                                          "HF11_plus_HF121_public_strict_pctPIB", "total_EUR_PPA_hab", "HF1_EUR_PPA_hab", "HF3_part_pct"], out)

# Vieillesse et survivants (SOCX TP01), 2019
r = list(csv.DictReader(open(os.path.join(SRC, "oecd_DF_SOCX_AGG.csv"), encoding="utf-8")))
D = {(x["REF_AREA"], x["EXPEND_SOURCE"], x["PROGRAMME_TYPE"], x["TIME_PERIOD"]): float(x["OBS_VALUE"])
     for x in r if x["SPENDING_TYPE"] == "_T" and x["OBS_VALUE"]}
vo = []
for y in ("2019", "2021"):
    vals = {}
    for p in P:
        pub = D.get((p, "ES10", "TP01", y)); pm = D.get((p, "ES10_20", "TP01", y), pub); pr = D.get((p, "ES20_30", "TP01", y), 0.0)
        vals[p] = (pub, pm, pub + pr if pub is not None else None)
        vo.append([y, p, pub, pm, vals[p][2]])
    comp = [p for p in P if p != "FRA"]
    m = [sum(vals[p][i] for p in comp) / len(comp) for i in range(3)]
    vo.append([y, "moyenne9"] + m)
    vo.append([y, "ECART_FR_moins_moyenne9"] + [vals["FRA"][i] - m[i] for i in range(3)])
    for p in comp:
        vo.append([y, "ECART_FR_moins_" + p] + [vals["FRA"][i] - vals[p][i] for i in range(3)])
ecrire_csv("A05_vieillesse_SOCX_public_prive.csv", ["annee", "pays_ou_ecart", "TP01_public_ES10", "TP01_public_plus_prive_obligatoire_ES10_20",
                                                     "TP01_public_plus_tout_prive_ES10_plus_ES20_30"], vo)

# Education
r = list(csv.DictReader(open(os.path.join(SRC, "oecd_edu_perstud_resume.csv"), encoding="utf-8")))
E = {(x["REF_AREA"], x["EDUCATION_LEV"], x["TIME_PERIOD"]): x["OBS_VALUE"] for x in r}
ed = []
for lev in ("ISCED11_1", "ISCED11_2", "ISCED11_3", "ISCED11_5T8"):
    for p in P + ["OECD", "EU25"]:
        ed.append(["2023", lev, p, E.get((p, lev, "2023"), "")])
ecrire_csv("A05_education_depense_par_eleve.csv", ["annee", "niveau_CITE", "pays", "USD_PPA_par_eleve"], ed)

if __name__ == "__main__":
    for l in out:
        if l[0] == "2023" and l[1] in ("FRA", "DEU", "NLD"): print(l)
    for l in vo:
        if l[0] == "2019" and (l[1].startswith("ECART") or l[1] in ("FRA", "moyenne9")): print(["%.2f" % v if isinstance(v, float) else v for v in l])
