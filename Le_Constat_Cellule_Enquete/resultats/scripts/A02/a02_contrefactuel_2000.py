# -*- coding: utf-8 -*-
"""A02 - test C3 : la France pouvait-elle etre a l'equilibre en 2000, et pour combien d'annees ?
Contrefactuel borne, ex ante, sans retroaction macroeconomique (multiplicateur nul), sauf variante.
Pieces : Senat n 371 (1999-2000) et n 50 (2001-2002) pour les montants en francs ; Insee base 2020 (solde, PIB) ;
AMECO 17/11/2026 (composante cyclique, ecart de production, solde corrige 2000-2003).
"""
import csv, os, sys
R = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
F = 6.55957
S = os.path.join(R, "donnees", "A02", "sources")

def ameco(fname, code):
    with open(os.path.join(S, "ameco", fname), encoding="latin-1") as fh:
        rd = csv.reader(fh, delimiter=";"); hdr = next(rd)
        for r in rd:
            if r[0] == code:
                return {int(h): float(v) for h, v in zip(hdr[5:], r[5:]) if h.strip().isdigit() and v not in ("", "NA")}
    return {}

pib2000 = 1473.517           # Md EUR, Insee T_1101
def2000 = -19.3422           # Md EUR, Insee 3.201 B9
cyc = ameco("AMECO17.TXT", "FRA.1.0.319.0.UBLGCP")
cab = ameco("AMECO17.TXT", "FRA.1.0.319.0.UBLGAP")
og = ameco("AMECO6.TXT", "FRA.1.0.0.0.AVGDGP")
bal = {y: cab[y] + cyc[y] for y in cab if y in cyc}   # solde effectif reconstitue = solde corrige + composante cyclique (AMECO, % PIB potentiel)

# Premier collectif 2000 (Senat n 371 et n 50), Md F
TH, IR, TVA2000, TVA_AP, DEP = 11.0, 11.6, 18.45, 31.05, 10.0
part_tva_payee_par_apu = 0.15   # Senat n 371 : "15 % de la TVA sont payes par les administrations"
lfr1_etat = TH + IR + TVA2000 + DEP                        # cout pour l'Etat en 2000
lfr1_s13 = TH + IR + TVA2000 * (1 - part_tva_payee_par_apu) + DEP   # cout ex ante pour S13 (TH : degrevement paye par l'Etat)
# Second collectif : recettes fiscales +28,5 Md F nettes des mesures, deficit reduit de 5,8 Md F seulement (Senat n 50)
lfr2_non_affecte = 28.5 - 5.8   # borne haute de ce qui aurait pu reduire le deficit (usage exact non etabli)

def pct(mdf):
    return 100 * mdf / F / pib2000

print("Solde S13 2000 effectif : %.2f Md EUR = %.2f %% du PIB" % (def2000, 100 * def2000 / pib2000))
print("Collectif 1 : cout Etat %.2f Md F (%.2f %% PIB) ; cout S13 ex ante %.2f Md F (%.2f %% PIB)" % (lfr1_etat, pct(lfr1_etat), lfr1_s13, pct(lfr1_s13)))
sA = 100 * def2000 / pib2000 + pct(lfr1_s13)
sB = sA + pct(lfr2_non_affecte)
print("Scenario A (aucune reaffectation du 1er collectif) : solde %.2f %% du PIB" % sA)
print("Scenario B (A + surplus du 2e collectif entierement au solde, borne haute) : solde %.2f %% du PIB" % sB)
print("Effort supplementaire pour l'equilibre en 2000 : A %.2f pt ; B %.2f pt" % (-sA, -sB))
for m in (0.5, 1.0):
    # variante avec retroaction : un gain ex ante g reduit le PIB de m*g et le solde de 0,5*m*g (semi-elasticite ~0,5)
    print("  variante multiplicateur %.1f : gain net du scenario B = %.2f pt au lieu de %.2f" % (m, (sB - 100 * def2000 / pib2000) * (1 - 0.5 * m), sB - 100 * def2000 / pib2000))
print("Cout du point de TVA en annee pleine : %.2f Md F = %.2f Md EUR = %.2f %% du PIB 2000" % (TVA_AP, TVA_AP / F, pct(TVA_AP)))
print("\nAMECO 17/11/2026 : annee, solde effectif, composante cyclique, solde corrige, ecart de production")
for y in range(1998, 2004):
    print(y, round(bal.get(y, float("nan")), 2), round(cyc.get(y, float('nan')), 2), round(cab.get(y, float('nan')), 2), round(og.get(y, float('nan')), 2))
print("Solde corrige du cycle du scenario B en 2000 : %.2f %% du PIB potentiel (B - composante cyclique 2000)" % (sB - cyc[2000]))
for y in (2001, 2002, 2003):
    # si le scenario B etait reconduit (memes mesures evitees, en annee pleine pour la TVA), solde = solde effectif + gain
    # seules les mesures permanentes du 1er collectif sont reconduites (TVA en annee pleine, IR, TH) ; les 10 Md F de depenses
    # etaient presentees comme exceptionnelles et le surplus du 2e collectif ne se reconduit pas (15 Md F reportes ameliorent 2001)
    gain = pct(TH + IR + TVA_AP * (1 - part_tva_payee_par_apu))
    print("  %d : solde effectif AMECO %.2f ; avec baisses d'impots permanentes de 2000 evitees (annee pleine, sans retroaction, en %% du PIB 2000) %.2f" % (y, bal[y], bal[y] + gain))
