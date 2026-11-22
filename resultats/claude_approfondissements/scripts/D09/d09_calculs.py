# -*- coding: utf-8 -*-
"""D09 - recalcul des grandeurs dérivées des quinze affirmations.

Les valeurs des pièces numérisées (Sénat, Commission des comptes) sont celles lues sur image
(donnees/D09/images/) ; elles sont saisies ici en constantes, avec la page.
Les valeurs des pièces nativement numériques sont relues dans la pièce (xlsx, texte PDF).
Sortie : donnees/D09/D09_calculs.csv
"""
import csv
import re
from pathlib import Path

import fitz
import openpyxl

ICI = Path(__file__).resolve().parent
OUT = ICI.parent.parent
DON = OUT / "donnees"
PREMIERE = OUT.parents[3] / "Le_Constat_Cellule_Enquete" / "resultats" / "donnees"
lignes = []


def ajoute(aff, grandeur, valeur, calcul, source):
    lignes.append([aff, grandeur, valeur, calcul, source])


# Affirmation 2 : Commission des comptes, juillet 1981 (lu sur image, p.8, p.18 ; p.20 texte)
exc, cot = 10.669, 9.352
ajoute(2, "excédent RG 1980 hors 1 % (Md F)", round(exc - cot, 3), "10,669 - 9,352",
       "CCSS juillet 1981 p.20 (solde +10.669) et p.8 (9.352)")
ajoute(2, "part du 1 % dans l'excédent RG 1980 (%)", round(100 * cot / exc, 1), "9,352 / 10,669",
       "idem")

# Affirmation 3 : Sénat n°102 t.III p.22 (image) : branches 1981
ajoute(3, "déficit RG 1981 prévu (somme des branches, Md F)", round(-1.8 - 1.1 - 0.3, 1),
       "-1,8 - 1,1 - 0,3", "Sénat n°102 t.III (1980-81) p.22, image")

# Affirmation 7 : DGAFP, séries longues, p.10 (PDF natif)
doc = fitz.open(DON / "D03/sources/dgafp_series_longues_1980_1998.pdf")
t = " ".join(doc[9].get_text().split())
def ligne_annee(a):
    m = re.search(rf"\b{a} ((?:\d[\d ]*,\d ){{9}}\d[\d ]*,\d)", t)
    nums = re.findall(r"\d{1,3}(?: \d{3})*,\d", m.group(1))
    return [float(x.replace(" ", "").replace(",", ".")) for x in nums]
l80, l85 = ligne_annee(1980), ligne_annee(1985)
fpe, fpt, fph, tot = (l85[i] - l80[i] for i in (6, 7, 8, 9))
ajoute(7, "hausse fonction publique 1980-1985 (milliers)", round(tot, 1), "total 1985 - total 1980",
       "DGAFP p.10")
ajoute(7, "part FPT + FPH dans la hausse (%)", round(100 * (fpt + fph) / tot, 1), "(FPT+FPH)/total",
       "DGAFP p.10")
# Sénat n°58 t.I (1981-82) p.72 (image) : collectif 1981 et budget 1982
ajoute(7, "collectif 1981 + PLF 1982 (emplois)", 54000 + 61000, "54 000 + 61 000", "Sénat n°58 p.72, image")
ajoute(7, "dont à la charge de l'État (emplois)", 45000 + 61000,
       "45 000 (collectif, part État) + 61 000", "Sénat n°58 p.72, image")
ajoute(7, "1982 au seul budget général (emplois)", 41000, "lu", "Sénat n°58 p.72, image")

# Affirmation 9 : Carrez, AN n°2689, p.7 (PDF natif, lu aussi sur image)
ajoute(9, "fourchette basse : mesures nouvelles + périmètre (Md€)", round(68.3 + 32.9, 1), "68,3 + 32,9",
       "AN n°2689 p.7")
ajoute(9, "fourchette haute : mesures nouvelles + périmètre (Md€)", round(77.7 + 41.6, 1), "77,7 + 41,6",
       "AN n°2689 p.7")
ajoute(9, "part des mesures nouvelles (%)", f"{100*68.3/101.2:.1f} / {100*77.7/119.3:.1f}", "68,3/101,2 ; 77,7/119,3",
       "AN n°2689 p.7")
ajoute(9, "écart de déficit 2009 (points de PIB)", round(7.5 - 3.7, 1), "7,5 - 3,7", "AN n°2689 p.16")
ajoute(9, "écart de dette 2009 (points de PIB)", round(77.4 - 54.6, 1), "77,4 - 54,6", "AN n°2689 p.16")
# Contrôle : ligne « mesures de périmètre » p.7 identique à la ligne impôt sur le revenu p.10 ?
c = fitz.open(PREMIERE / "A04/sources/AN_rapinfo_i2689_Carrez_2010.pdf")
p7 = " ".join(c[6].get_text().split()).replace("—", "–")
p10 = " ".join(c[9].get_text().split()).replace("—", "–")
def serie(txt, debut, rang):
    seg = txt.split(debut, 1)[1]
    vals = re.findall(r"[–-]\s?\d+,\d", seg)
    return [v.replace("–", "-").replace(" ", "") for v in vals[rang * 10:(rang + 1) * 10]]
per_h = serie(p7, "Coût cumulé des mesures de périmètre", 0)
per_b = serie(p7, "Coût cumulé des mesures de périmètre", 1)
ir_h = serie(p10, "Coût cumulé des mesures nouvelles depuis 2000", 0)
ir_b = serie(p10, "Coût cumulé des mesures nouvelles depuis 2000", 1)
ajoute(9, "ligne « périmètre » p.7 = ligne IR p.10 (haute)", per_h == ir_h, " ".join(per_h), "AN n°2689 p.7 et p.10")
ajoute(9, "ligne « périmètre » p.7 = ligne IR p.10 (basse)", per_b == ir_b, " ".join(per_b), "AN n°2689 p.7 et p.10")

# Contrôle de la ligne « périmètre » : cumul de la ligne TOTAL annuelle de l'impôt sur le revenu (p.10, image)
ir_annuel = [-1.7, -6, -4.7, -1.7, -1.7, -2.4, -2.2, -7.4, -1.4, -3.7]
cum, s = [], 0.0
for x in ir_annuel:
    s += x
    cum.append(round(s, 1))
ajoute(9, "cumul de la ligne TOTAL annuelle IR (p.10)", " ".join(str(x) for x in cum), "somme courante",
       "égale, aux arrondis près, à la ligne « périmètre » basse de la p.7")
# Transferts de recettes nets (p.13, image) : 2001 à 2009
transferts = [-0.4, -0.2, -0.3, 10.3, -3.5, -21, -5.1, -5.9, -2.1]
ajoute(9, "cumul des transferts nets 2001-2009 (p.13, Md€)", round(sum(transferts), 1), "somme",
       "texte p.13 : « entre 1,5 % et 2 % de PIB »")

# Essai de reconstitution du contrefactuel (non unique ; le rapport ne donne pas la méthode)
mn_h = [-7.9, -20.4, -25.9, -31.8, -36.2, -40.0, -50.5, -65.6, -77.8, -77.7]
mn_b = [-7.9, -19.8, -25.2, -30.2, -32.5, -33.9, -41.6, -53.5, -61.7, -68.3]
pib09 = 101.2 / 0.053  # PIB 2009 implicite de la p.7 (101,2 Md€ = 5,3 % du PIB)
ajoute(9, "PIB 2009 implicite p.7 (Md€)", round(pib09), "101,2 / 0,053", "AN n°2689 p.7")
ajoute(9, "somme 2000-2009 du coût cumulé, haute / basse (Md€)", f"{-sum(mn_h):.1f} / {-sum(mn_b):.1f}",
       "somme des lignes p.7", "AN n°2689 p.7")
ajoute(9, "même somme en points de PIB 2009, haute / basse", f"{-100*sum(mn_h)/pib09:.1f} / {-100*sum(mn_b)/pib09:.1f}",
       "sans intérêts", "à comparer à l'écart de dette 22,8")
ajoute(9, "coût 2009 en points de PIB, haute / basse / milieu",
       f"{77.7/pib09*100:.2f} / {68.3/pib09*100:.2f} / {73.0/pib09*100:.2f}", "", "à comparer à l'écart de déficit 3,8")

# Affirmation 10 : Champsaur-Cotis p.18
ajoute(10, "écart taux de PO 2008 à législation 1999 / effectif (points)", round(45.3 - 42.5, 1), "45,3 - 42,5",
       "Champsaur-Cotis p.18")

# Affirmation 11 : DG Trésor DT 2009/13, tableau 3 p.18 (PDF natif)
d = fitz.open(DON / "D05/sources/dgtresor_DT2009-13_Guyon_Sorbe.pdf")
t3 = " ".join(d[17].get_text().split())
seg = t3.split("dont mesures nouvelles en PO", 1)[1]
mn = [float(x.replace(",", ".")) for x in re.findall(r"-?\d,\d", seg)[:9]]
ajoute(11, "mesures nouvelles en PO 2000-2008 (points)", " ".join(f"{x:+.1f}" for x in mn), "lu", "DT 2009/13 p.18")
ajoute(11, "cumul 2000-2008 (points)", round(sum(mn), 1), "somme", "DT 2009/13 p.18")

# Affirmation 13 : Insee T207
wb = openpyxl.load_workbook(DON / "D07/sources/insee_EEC_T207_2025.xlsx", data_only=True)
ws = wb["T207"]
rows = list(ws.iter_rows(values_only=True))
entete = [r for r in rows if r[1] == "Annuel"][0]
annees = [int(x) for x in entete[2:] if x is not None]
for r in rows:
    if r[0] == "Total" and r[1] and r[1].strip() in ("De 55 à 59 ans", "De 60 à 64 ans"):
        s = dict(zip(annees, r[2:]))
        amin = min(s, key=s.get)
        ajoute(13, f"{r[1].strip()} : 1975 / minimum (année) / 2025", f"{s[1975]} / {s[amin]} ({amin}) / {s[2025]}",
               "lu", "Insee T207")
ajoute(13, "note du tableau", [r[0] for r in rows if r[0] and str(r[0]).startswith("Note")][0], "lu", "Insee T207")

# Affirmation 15 : AN n°2436 p.115 : 12 600 + 22 500 + 9 900
ajoute(15, "FPH non médicaux 2002-2004 (emplois)", 12600 + 22500 + 9900, "somme", "AN n°2436 p.115")

with open(DON / "D09/D09_calculs.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["affirmation", "grandeur", "valeur", "calcul", "source"])
    w.writerows(lignes)
for l in lignes:
    print(l)
