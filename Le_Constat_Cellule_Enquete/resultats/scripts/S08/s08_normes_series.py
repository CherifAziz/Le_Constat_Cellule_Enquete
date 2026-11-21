# -*- coding: utf-8 -*-
"""S08 - Partie B : table des normes de dépense et séries maximales d'années tenues.

Entrées :
  - table saisie à la main depuis les pièces (voir S08.md §3), écrite ici en dur
    pour que chaque valeur soit traçable à une ligne du dossier ;
  - resultats/donnees/A16/a16_volume_depense_primaire.csv (lecture seule).
Sorties (resultats/donnees/S08/) :
  - S08_B_table_normes.csv
  - S08_B_series_max.csv
  - S08_B_calculs.txt
Règle : une année sans pièce (statut 'NE' = non établi) ROMPT la série.
Usage : python -I s08_normes_series.py
"""
import csv, os, sys

RAC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
OUT = os.path.join(RAC, "donnees", "S08")
sys.stdout.reconfigure(encoding="utf-8")

# Colonnes : norme ; annee ; cible ; execution ; ecart ; unite ;
#   t_init  (exécution <= cible initiale LFI/LFSS/LPFP selon la norme)
#   t_rev   (exécution <= cible révisée en cours d'année, si elle existe)
#   t_cour  (après retraitements de la Cour, si publiés)
#   moyen (vocabulaire fermé, voir §2) ; source (identifiant de pièce) ; fait (F-S08-nnn)
# Valeurs de test : O (tenu), N (non tenu), NE (non établi sur pièce), SO (sans objet)
T = [
 # ---------- ONDAM (cible = ONDAM voté en LFSS initiale)
 ("ONDAM",1997,"","","","Md€","NE","NE","NE","dépassements « systématiques » avant 2010 selon le Sénat ; aucune valeur annuelle lue","P02","F-S08-001"),
 ("ONDAM",2008,"","","","Md€","N","NE","NE","sous-objectif établissements dépassé en 2008 et 2009 (Sénat 2019 p. 32) ; pas de valeur globale lue","P02","F-S08-001"),
 ("ONDAM",2009,"","","","Md€","N","NE","NE","idem","P02","F-S08-001"),
 ("ONDAM",2010,"","161.8","-0.64","Md€","O","NE","NE","sous-exécution (volumes ralentis, effet base)","P02;P20","F-S08-002"),
 ("ONDAM",2011,"167.1","166.3","-0.8","Md€","O","NE","NE","sous-exécution ; mises en réserve hospitalières non déléguées 2011-2014","P02;P20","F-S08-002"),
 ("ONDAM",2012,"171.2","170.8","-0.35","Md€","O","NE","NE","estimation de novembre 2012","P20","F-S08-002"),
 ("ONDAM",2013,"","","","Md€","O","NE","NE","soins de ville dépassés, compensés par gels et annulations hospitalières","P05;P02","F-S08-003"),
 ("ONDAM",2014,"","","","Md€","O","NE","NE","idem","P05;P02","F-S08-003"),
 ("ONDAM",2015,"","","","Md€","O","NE","NE","idem ; soins de ville sur-exécutés depuis 2015 (Sénat)","P05;P02","F-S08-003"),
 ("ONDAM",2016,"","","","Md€","O","NE","NE","idem","P05;P02","F-S08-003"),
 ("ONDAM",2017,"","","","Md€","O","NE","NE","chaque sous-objectif atteint selon la Cour (divergence Sénat, §12)","P05;P02","F-S08-003"),
 ("ONDAM",2018,"","","","Md€","O","NE","NE","idem","P05;P02","F-S08-003"),
 ("ONDAM",2019,"","","","Md€","O","NE","NE","idem (Cour p. 119)","P05","F-S08-003"),
 ("ONDAM",2020,"","","","Md€","N","NE","NE","crise sanitaire","P05","F-S08-004"),
 ("ONDAM",2021,"","","","Md€","N","NE","NE","crise sanitaire, Ségur","P05","F-S08-004"),
 ("ONDAM",2022,"236.8","247.2","+10.4","Md€","N","NE","NE","covid, mesures inflation, revalorisations en cours d'année (soclées)","P21;P05","F-S08-004"),
 ("ONDAM",2023,"","","","Md€","N","NE","NE","revalorisations salariales en cours d'année, soins de ville","P05","F-S08-004"),
 ("ONDAM",2024,"","256.4","+1.5","Md€","N","NE","NE","soins de ville","P04;P05","F-S08-004"),
 ("ONDAM",2025,"265.9","265.4","-0.5","Md€","O","O","NE","alerte de juin 2025, économies d'urgence, gels sur établissements ; soins de ville +0,5","P05;P03","F-S08-005"),
 # ---------- État (norme de la loi de finances ; cible = LFI)
 ("ETAT_zero_volume_BG",2002,"","273.5","vol +2.2 %","Md€","NE","NE","NE","pas de norme identifiée sur pièce pour 2002 ; LFR d'été","P06","F-S08-010"),
 ("ETAT_zero_volume_BG",2003,"","273.8","vol -0.9 %","Md€","O","NE","NE","exécution au niveau voté (rapporteur général) ; périmètre -2,4","P06","F-S08-010"),
 ("ETAT_zero_volume_BG",2004,"","283.7","vol -0.2 %","Md€","O","NE","NE","périmètre +5,8","P06","F-S08-010"),
 ("ETAT_zero_volume_BG",2005,"","288.6","vol +0.1 %","Md€","O","NE","NE","périmètre -0,4 ; volume légèrement positif","P06","F-S08-010"),
 ("ETAT_zero_volume_BG",2006,"","266.1","vol -0.1 %","Md€","O","NE","NE","périmètre -27,3 dont 17,1 de compensations d'allègements passées en moindres recettes","P06","F-S08-010"),
 ("ETAT_zero_volume_BG",2007,"266.9","","","Md€","NE","NE","NE","cible -1 % en volume ; exécution non lue","P06","F-S08-011"),
 ("ETAT_zero_valeur",2012,"279.45","278.06","-1.39","Md€ format 2013","O","NE","NE","non détaillé dans la pièce","P11","F-S08-012"),
 ("ETAT_zero_valeur",2013,"279.40","279.25","-0.14","Md€","O","NE","NE","exclusion d'« exceptionnels » (PSR UE 1,79 ; MES 6,5 ; BEI 1,6) ; annulations 1,1 gageant le PSR UE","P11","F-S08-013"),
 ("ETAT_zero_valeur",2015,"282.6","283.9","+1.4","Md€","N","O","N","LFR relève la norme (+1,4) ; contournements 3,0 Md€","P07","F-S08-014"),
 ("ETAT_zero_volume",2012,"370.50","366.79","-3.71","Md€ format 2013","O","NE","NE","non détaillé","P11","F-S08-012"),
 ("ETAT_zero_volume",2013,"371.53","368.07","-3.45","Md€","O","NE","NE","économie de constatation : dette -2,01, pensions -1,30 (inflation)","P11","F-S08-013"),
 ("ETAT_zero_volume",2015,"372.7","371.6","-1.1","Md€","O","O","N","économie de constatation sur la dette -2,2 ; contournements","P07","F-S08-014"),
 ("ETAT_pilotables",2018,"257.9","256.5","-1.4","Md€","O","SO","O","cible LFI fixée +4,1 au-dessus de l'exécution 2017 (sincérisation) ; contournements 0,6","P08","F-S08-015"),
 ("ETAT_pilotables",2019,"262.9","261.8","-1.0","Md€","O","N","NE","LFI +4 Md€ au-dessus de la LPFP ; +0,5 vs PStab ; +3,0 vs LPFP","P09","F-S08-016"),
 ("ETAT_ODETE",2018,"425.4","425.4","-0.1","Md€","O","SO","O","","P08","F-S08-015"),
 ("ETAT_ODETE",2019,"432.0","431.3","-0.7","Md€","O","SO","NE","charge d'intérêts plus faible","P09","F-S08-016"),
 ("ETAT_PDE",2024,"491.9","484.7","-7.2","Md€","O","SO","NE","annulations 16,9 ; reports 11,6 sur 2025 ; ponctions de trésorerie 2,7 + CAS PFE 1,5 ; reports d'appels à projets","P10","F-S08-017"),
 ("ETAT_PDE",2025,"487.8","488.2","+0.4","Md€","N","SO","NE","PSR collectivités +0,7 ; régulation tardive","P12;P14","F-S08-018"),
 # ---------- Collectivités (contrats de Cahors, 321 collectivités ciblées, DRF budgets principaux)
 ("CAHORS_321",2018,"116.5","114.9","-1.6","Md€","O","SO","NE","modération des DRF ; budgets annexes hors champ ; investissement +5,2 %","P13;P01","F-S08-020"),
 ("CAHORS_321",2019,"117.9","116.0","-1.9","Md€","O","SO","NE","investissement +13,7 % ; objectif de besoin de financement (-2,6 Md€/an) non atteint","P13;P01","F-S08-020"),
 ("CAHORS_321",2020,"119.3","116.6","-2.7","Md€","SO","SO","SO","dispositif suspendu en mars 2020","P13","F-S08-020"),
 # ---------- LPFP 2023-2027 : dépense des APUL (valeur) et dépense publique (volume, IPCHT)
 ("LPFP23_APUL",2023,"+4.8 %","+7.0 %","+2.2 pt","%","N","SO","NE","","P01","F-S08-021"),
 ("LPFP23_APUL",2024,"+2.0 %","+4.7 %","+2.7 pt","%","N","SO","NE","","P01","F-S08-021"),
 ("LPFP23_APUL",2025,"+1.5 %","+1.5 %","0","%","O","SO","NE","","P01","F-S08-021"),
 ("LPFP23_depense_volume",2024,"","","écart","%","N","SO","SO","« plus dynamique que prévu » (HCFP)","P14","F-S08-022"),
 ("LPFP23_depense_volume",2025,"+0.8 %","+1.6 %","+0.8 pt","%","N","SO","SO","inflation plus faible : valeur 2,5 % < 2,8 % prévu","P14","F-S08-022"),
 # ---------- UE : dépense primaire nette (recommandation du Conseil du 21/01/2025)
 ("UE_DPN",2025,"+0.8 %","+0.8 %","0","%","O","SO","SO","23 Md€ de hausses de PO dont surtaxe IS temporaire 7,5 ; sans elle +1,2 %","P14;P15","F-S08-023"),
]

HDR = ["norme","annee","cible","execution","ecart","unite","t_init","t_rev","t_cour","moyen","pieces","fait"]
with open(os.path.join(OUT, "S08_B_table_normes.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(HDR); w.writerows(T)

def series_max(rows, col):
    """Plus longue série d'années CONSÉCUTIVES au statut 'O'. Année absente ou NE/N/SO = rupture."""
    by = {r[1]: r[HDR.index(col)] for r in rows}
    best, cur, start, bstart = 0, 0, None, None
    for y in range(min(by), max(by) + 1):
        if by.get(y) == "O":
            if cur == 0: start = y
            cur += 1
            if cur > best: best, bstart = cur, start
        else:
            cur = 0
    return best, (f"{bstart}-{bstart+best-1}" if best else "")

res = []
for n in sorted(set(r[0] for r in T)):
    rows = [r for r in T if r[0] == n]
    for col in ("t_init", "t_rev", "t_cour"):
        b, per = series_max(rows, col)
        nO = sum(1 for r in rows if r[HDR.index(col)] == "O")
        nN = sum(1 for r in rows if r[HDR.index(col)] == "N")
        nNE = sum(1 for r in rows if r[HDR.index(col)] == "NE")
        res.append((n, col, b, per, nO, nN, nNE))

# Test complémentaire : dépense primaire APU en volume <= 0 (CSV d'A16, déflateur du PIB)
a16 = os.path.join(RAC, "donnees", "A16", "a16_volume_depense_primaire.csv")
vol = {}
with open(a16, encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter=";"):
        vol[int(r["annee"])] = (float(r["croiss_volume_dep_prim"]), float(r["deflateur"]))
rows = [("A16_dep_prim_vol_le0", y, "", str(v[0]), "", "%", "O" if v[0] <= 0 else "N", "SO", "SO", f"deflateur {v[1]}", "A16", "C-S08-002") for y, v in sorted(vol.items()) if y >= 1976]
b, per = series_max(rows, "t_init")
res.append(("A16_dep_prim_vol_le0 (1976-2025)", "t_init", b, per, sum(1 for r in rows if r[6]=="O"), sum(1 for r in rows if r[6]=="N"), 0))
annees_le0 = [r[1] for r in rows if r[6] == "O"]

with open(os.path.join(OUT, "S08_B_series_max.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["norme","test","serie_max","periode","nb_O","nb_N","nb_NE"]); w.writerows(res)

# C-S08-001 : ONDAM 2010-2019 en volume (déflateur du PIB d'A16) - calcul de l'agent
d = [vol[y][1] for y in range(2010, 2020)]
defl_moy = sum(d) / len(d)
ondam_val = 2.3  # Cour, RALFSS mai 2026, p. 115 : +2,3 %/an fin 2009-fin 2019
lines = []
lines.append(f"C-S08-001 deflateur PIB moyen 2010-2019 (A16) = {defl_moy:.3f} % ; ONDAM 2,3 %/an en valeur => ~{ondam_val-defl_moy:.2f} %/an en volume (approx. additive)")
lines.append(f"C-S08-002 annees ou la depense primaire APU baisse en volume (A16, 1976-2025) : {annees_le0} ; serie max {b} ({per})")
for y in annees_le0:
    lines.append(f"   {y} : volume {vol[y][0]} % ; deflateur {vol[y][1]} %")
# C-S08-003 : cumuls glissants (3 et 5 ans) de la croissance en volume de la dépense primaire (A16)
ys = sorted(vol)
for k in (3, 5):
    cum = []
    for i in range(len(ys) - k + 1):
        win = ys[i:i+k]
        if win[-1] - win[0] != k - 1: continue
        c = 1.0
        for y in win: c *= 1 + vol[y][0] / 100
        cum.append(((c - 1) * 100, win[0], win[-1]))
    cum.sort()
    lines.append(f"C-S08-003 cumul {k} ans, 5 plus faibles : " + " ; ".join(f"{a}-{b}: {v:+.2f} %" for v, a, b in cum[:5]))
    nb_le0 = [f"{a}-{b}" for v, a, b in cum if v <= 0]
    lines.append(f"   fenêtres de {k} ans à cumul <= 0 : {nb_le0}")
# C-S08-004 : volume moyen de la dépense primaire APU pendant les séries tenues
for (a, b, lab) in ((2003, 2006, "Etat zero volume BG"), (2010, 2019, "ONDAM"), (2012, 2013, "Etat zero valeur"), (2018, 2019, "Etat pilotables / Cahors")):
    m = sum(vol[y][0] for y in range(a, b + 1)) / (b - a + 1)
    lines.append(f"C-S08-004 dépense primaire APU en volume, moyenne {a}-{b} ({lab}) : {m:+.2f} %/an")
for r in res:
    lines.append("SERIE " + " | ".join(str(x) for x in r))
txt = "\n".join(lines)
open(os.path.join(OUT, "S08_B_calculs.txt"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
