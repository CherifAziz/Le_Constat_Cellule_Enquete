# -*- coding: utf-8 -*-
"""S01 - corrections de la table apres relecture (20/11/2026) :
1. retraite a 60 ans : niveaux annuels convertis en increments ; ligne d'annonce 1985 classee agregat ;
2. 1975 : ajout de la part non executee des credits de soutien (reportee sur 1976 et 1977) ;
3. 1986-1990 : lignes IR melant indexation et baisses -> classees « detail » ; les enveloppes
   d'allegements nets (hors indexation) 1987-1988, 1989, 1990 deviennent les mesures comptees ;
   1987 : allegement de 3 % isole ;
4. 1983 : majoration d'IR de mars classee agregat (recouvrement possible avec la majoration de la LFI) ;
5. ajout de la hausse d'un point de TVA de juillet 1982 (montant indisponible).
Usage : python -I s01_corrections_v1.py  (idempotent)
"""
import os, glob

L = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S01\lots"


def sub(fichier, debut, champ, valeur, ajout_remarque=None):
    p = os.path.join(L, fichier)
    lignes = open(p, encoding="utf-8").read().splitlines()
    n = 0
    for i, l in enumerate(lignes):
        if l.startswith(debut):
            c = l.split(";")
            c[champ] = valeur
            if ajout_remarque and ajout_remarque not in c[13]:
                c[13] = (c[13] + " | " if c[13] else "") + ajout_remarque
            lignes[i] = ";".join(c)
            n += 1
    assert n == 1, (fichier, debut, n)
    open(p, "w", encoding="utf-8").write("\n".join(lignes) + "\n")


# colonnes : 0 annee 1 texte 2 date 3 mesure 4 sens 5 annonce 6 unite 7 constate 8 perimetre 9 temp 10 source 11 page 12 prov 13 remarque
F = "lot_1979_1982.csv"
sub(F, "1982;Ordonnance n° 82-270 du 26/03/1982", 9, "agregat", "annonce pour 1985 (niveau) : non sommée, voir les incréments 1983-1985")
sub(F, "1984;Ordonnance n° 82-270 (effet 1984)", 7, "4,2", "incrément = 5,5 (niveau 1984) - 1,3 (niveau 1983)")
sub(F, "1985;Ordonnance n° 82-270 (effet 1985)", 5, "indisponible", "annoncé 3 à 5 Md F en niveau 1985 (ligne 1982)")
sub(F, "1985;Ordonnance n° 82-270 (effet 1985)", 7, "3,4", "incrément = 8,9 - 5,5")
sub("lot_1982_1984.csv", "1983;Plan de rigueur de mars 1983;1983-03;Majoration de l'IR", 9, "agregat",
    "peut recouvrir la majoration exceptionnelle de 5,2 Md F de la LFI 1983 : non sommée")
G = "lot_1985_1999.csv"
sub(G, "1986;LFI 1986;1985-12;Indexation des tranches", 9, "indexation", "part de l'allègement de 3 % non séparée")
sub(G, "1987;LFI 1987;1986-12;IR : indexation", 9, "detail", "comprise dans l'enveloppe d'allègements nets 1987-1988 (69 Md F) pour sa part hors indexation")
sub(G, "1987;LFI 1987;1986-12;Suppression de l'impôt sur les grandes", 9, "detail", "supposée comprise dans l'enveloppe 1987-1988")
sub(G, "1987;LFI 1987;1986-12;Réduction de 16 %", 9, "detail", "supposée comprise dans l'enveloppe 1987-1988")
sub(G, "1988;LFI 1988;1987-12;IR : indexation", 9, "detail", "comprise dans l'enveloppe 1987-1988 pour sa part hors indexation")
sub(G, "1989;LFI 1989;1988-12;IR : élargissement", 9, "detail", "indexation et minoration mêlées : voir l'enveloppe 1989")
sub(G, "1990;LFI 1990;1989-12;IR : barème", 9, "detail", "voir l'enveloppe 1990")
sub(G, "1990;LFI 1990;1989-12;Taux majoré de TVA", 9, "detail", "voir l'enveloppe 1990")
sub(G, "1987;LFI 1987 et LFI 1988 (bilan)", 9, "permanent", "enveloppe hors indexation comptée comme mesure (affectée conventionnellement à 1987 : seules les sommes 1986-1988 ont un sens)")
sub(G, "1989;LFI 1989;1988-12;Enveloppe", 9, "permanent", "enveloppe hors indexation comptée comme mesure")
sub(G, "1990;LFI 1990 (bilan)", 9, "permanent", "enveloppe hors indexation comptée comme mesure")

ajout = os.path.join(L, "lot_corrections_v1.csv")
open(ajout, "w", encoding="utf-8").write("\n".join([
    "1975;Exécution des LFR de soutien (loi de règlement 1975);1977-06;Part des crédits de soutien de 1975 non consommée en 1975 et reportée sur 1976 et 1977;depense -;indisponible;Md F;9,7;État;temporaire;Sénat n° 378 (1976-1977), réponse de la Cour;PDF p.54;[C];6 budget général + 0,2 budgets annexes + 3,5 comptes spéciaux | corrige les montants votés de 1975",
    "1976;Exécution des LFR de soutien de 1975;1977-06;Crédits de soutien de 1975 consommés en 1976;depense +;indisponible;Md F;6,8;État;temporaire;Sénat n° 378 (1976-1977);PDF p.54;[C];9,7 reportés moins ≈ 2,9 encore reportés sur 1977 (titres V-VI)",
    "1977;Exécution des LFR de soutien de 1975;1977-06;Crédits de soutien de 1975 consommés en 1977;depense +;indisponible;Md F;2,9;État;temporaire;Sénat n° 378 (1976-1977);PDF p.54;[C];« voisins de 2,9 milliards » reportés à la gestion 1977",
    "1987;LFI 1987 (allègement isolé);1986-12;Allègement de 3 % de l'IR (partie de la ligne IR 1987);recette -;5,5;Md F;indisponible;État;detail;Sénat n° 67 tome I (1986-1987);PDF p.96;[C];compris dans l'enveloppe 1987-1988",
    "1982;Hausse des taux de TVA de juillet 1982 (texte non lu);1982-07;Relèvement d'un point du taux normal et du taux intermédiaire de la TVA;recette +;indisponible;Md F;indisponible;État;permanent;Sénat n° 69 tome I (1984-1985);PDF p.113;[C] (mention seulement);montant non lu | LFR 1982 non lue",
]) + "\n")
print("ok")
