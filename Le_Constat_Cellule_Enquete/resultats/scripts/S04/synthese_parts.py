"""S04 - Synthese par portefeuille (net 2030, enveloppe centrale si adoptee). CALCUL DE L'AGENT, niveau D.

Entree : donnees/S04/S04_table_incidence.csv (mesures > 1 Md EUR net 2030).
Etape 1 - ventilation par PAYEUR IMMEDIAT (somme = 100 % du total de l'enveloppe) : retraites, autres menages, menages non
ventiles par statut, agents publics, entreprises, collectivites, non ventile, et « non examine » (mesures < 1 Md EUR).
Etape 2 - deciles : seulement sur les mesures dont un profil par niveau de vie est publie ; montants en Md EUR et en % de
l'enveloppe ; aucune borne haute mecanique sur le non-documente (il est affiche a part).
Particularite : la part « plafond de l'abattement » de P-A14-001 (0,44 x 3,04) recoit le profil de la suppression totale de
l'abattement, comme P-A14-009, car le profil publie (IPP 2025, Cour) porte sur la suppression totale.
Totaux d'enveloppe : A13 33,2 ; A14 38,1 Md EUR (A13 R-A13-01 ; A14 R-A14-01).
Usage : python -I synthese_parts.py"""
import csv, os
R = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S04"
TOT = {"A13": 33.2, "A14": 38.1}
CAT = ["p_retraites", "p_autres_menages", "p_menages_non_ventiles", "p_agents_publics", "p_entreprises",
       "p_collectivites", "p_non_ventile"]
rows = list(csv.DictReader(open(os.path.join(R, "S04_table_incidence.csv"), encoding="utf-8"), delimiter=";"))
out = [["portefeuille", "rubrique", "Md_EUR", "pct_enveloppe"]]
for pf, T in TOT.items():
    rr = [r for r in rows if r["portefeuille"] == pf]
    exam = sum(float(r["net_2030_Md"]) for r in rr)
    print(f"\n{pf} : examine {exam:.2f} Md sur {T} = {100*exam/T:.1f} %")
    for c in CAT:
        m = sum(float(r["net_2030_Md"]) * float(r[c]) for r in rr)
        out.append([pf, "payeur:" + c[2:], round(m, 2), round(100 * m / T, 1)])
        print(f"  payeur {c[2:]:22s} {m:6.2f} Md  {100*m/T:5.1f} %")
    out.append([pf, "payeur:non_examine(<1Md)", round(T - exam, 2), round(100 * (T - exam) / T, 1)])
    print(f"  payeur {'non examine (<1 Md)':22s} {T-exam:6.2f} Md  {100*(T-exam)/T:5.1f} %")
    # Etape 2
    doc = 0.0
    t10b = t10h = b50b = b50h = q1 = q12 = 0.0
    for r in rr:
        a = float(r["net_2030_Md"])
        if r["id"] == "P-A14-001":
            continue  # traite avec 009
        if r["dec_documente"] != "1":
            continue
        if r["id"] == "P-A14-009":
            a = a + 0.44 * 3.04  # suppression totale de l'abattement
        if r["id"] == "P-A14-011":
            a = a * float(r["p_menages_non_ventiles"])  # seule la part repercutee aux consommateurs est ventilee par quintile
        doc += a
        if r["top10_bas"]:
            t10b += a * float(r["top10_bas"]); t10h += a * float(r["top10_haut"])
        if r["bas50_bas"]:
            b50b += a * float(r["bas50_bas"]); b50h += a * float(r["bas50_haut"])
        if r["q1_bas"]:
            q1 += a * float(r["q1_bas"]); q12 += a * float(r["q1q2_haut"])
    print(f"  deciles documentes sur {doc:.2f} Md ({100*doc/T:.1f} % de l'enveloppe)")
    print(f"    10 % les plus aises : {t10b:.2f} a {t10h:.2f} Md ({100*t10b/T:.1f} a {100*t10h/T:.1f} % de l'enveloppe)")
    print(f"    50 % les plus modestes : {b50b:.2f} a {b50h:.2f} Md ({100*b50b/T:.1f} a {100*b50h/T:.1f} %)")
    print(f"    1er cinquieme (plancher) : {q1:.2f} Md ; 1er+2e cinquiemes (plafond) : {q12:.2f} Md")
    out += [[pf, "deciles:montant_documente", round(doc, 2), round(100 * doc / T, 1)],
            [pf, "deciles:top10_bas", round(t10b, 2), round(100 * t10b / T, 1)],
            [pf, "deciles:top10_haut", round(t10h, 2), round(100 * t10h / T, 1)],
            [pf, "deciles:bas50_bas", round(b50b, 2), round(100 * b50b / T, 1)],
            [pf, "deciles:bas50_haut", round(b50h, 2), round(100 * b50h / T, 1)],
            [pf, "deciles:Q1_plancher", round(q1, 2), round(100 * q1 / T, 1)],
            [pf, "deciles:Q1Q2_plafond", round(q12, 2), round(100 * q12 / T, 1)]]
with open(os.path.join(R, "C-S04-004_synthese_parts.csv"), "w", newline="", encoding="utf-8") as f:
    csv.writer(f, delimiter=";").writerows(out)
