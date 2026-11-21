# -*- coding: utf-8 -*-
"""A18 - corrections apres relecture critique (20/11/2026, fin de session) :
T-07 (serie d'A03 non identifiee exactement), O4 (recherche sans plafond), V16/V17 (relu dans la copie pour une partie)."""
import csv
D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18"
def patch(f, key, col, new):
    p = D + "\\" + f
    rows = list(csv.reader(open(p, encoding="utf-8"), delimiter=";"))
    h = rows[0]; j = h.index(col); n = 0
    for r in rows[1:]:
        if r[0] == key:
            r[j] = new; n += 1
    assert n == 1, (f, key, n)
    with open(p, "w", encoding="utf-8", newline="") as o:
        csv.writer(o, delimiter=";", quoting=csv.QUOTE_ALL).writerows(rows)
patch("A18_arbitrage.csv", "T-07", "ce_que_dit_la_piece_ou_le_calcul",
      "AMECO fiscal retéléchargé par A18 (identique à la copie d'A09 ; date interne du zip 16/11/2026), libellés TITLE relus. Solde primaire corrigé du cycle UBLGBP 2003-2006 : -1,27 ; -1,39 ; -1,39 ; -1,18, soit +0,10 pt : pas de consolidation corrigée du cycle en 2004-2006. Les variations citées par A03 (+0,5 ; 0 ; +0,85) ne sortent d'aucune des quatre séries corrigées de l'AMECO (UBLGBP -0,12/-0,01/+0,22 ; UBLGB -0,14/-0,13/+0,03 ; UBLGAP -0,04/+0,08/+0,33 ; UBLGA -0,07/-0,05/+0,14). La plus proche est le solde primaire observé (Insee, calcul A18 : +0,46 ; -0,04 ; +0,74), le +0,85 restant non identifié exactement. A03 mêle donc probablement solde observé (épisode) et solde corrigé (2007 : -0,69). Consolidations corrigées de plus de 1 pt : 1993-1999 (+2,9) suivie de 2000 (-1,10) ; 2010-2016 (+2,3) suivie de 2017 (-0,49, sous le seuil) et 2019 (-0,97) ; 1994-1997 (+1,9) suivie de 1998 (+0,35). Définition A09 reproduite : 0 cas calculable sur 12 avec cumul fixe de 3 ans (1981 non calculable dans mon extraction, A09 le compte) ; variante meilleur gain : 3 sur 13 (3 ans), 4 sur 13 (5 ans). Les deux agents ne posent pas la même probabilité conditionnelle.")
patch("A18_arbitrage.csv", "O4", "ce_que_dit_la_piece_ou_le_calcul",
      "Recherche A18 sans plafond (décile, niveau de vie, portrait social, IFI, PFU, redistributif) dans A03, A04, A10, A15 et S04 : aucun profil par niveau de vie des baisses de 2018-2023. Seule indication : A04 F-A04-036, qualitative et pour une seule mesure (Cour, janvier 2025 : suppression de la taxe d'habitation, « effets anti-redistributifs »). A15 l.390 : « Ventilation par décile des combinaisons : non faite ». S04 porte sur les mesures proposées (IPP n°129, OFCE). Somme des bornes : -2,1 (2007-2009) +3,9 (2010-2014) -0,2 -2,29 (2018-2023) +0,89 (2024-2025), sources secondaires avant 2018.")
patch("A18_verification_25.csv", "V16", "verdict",
      "recalculé en partie (soldes) ; classement des majorités relu dans la copie d'A09, non revérifié sur les compositions de l'Assemblée : concordant")
patch("A18_verification_25.csv", "V17", "verdict",
      "recalculé en partie : soldes exécutés identiques par construction (même base) ; soldes programmés relus dans la copie d'A08 ; -2,08 concordant à l'arrondi ; dépend de la convention d'exclusion des crises")
patch("A18_verification_25.csv", "V24", "remarque",
      "AMECO fiscal daté du 16/11/2026 (date interne du zip), veille de la prévision d'automne")
print("ok")
