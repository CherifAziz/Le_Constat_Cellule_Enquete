"""Recontrole des citations de D02 reprises par D04 : chaque citation est recherchee
(espaces et coupures de ligne normalises) dans le texte extrait de la piece de D02.
Sortie : ../../donnees/D04/D04_verif_citations_D02.csv"""
import os, re, csv
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ICI, '..', '..', 'donnees', 'D02', 'sources')
OUT = os.path.join(ICI, '..', '..', 'donnees', 'D04', 'D04_verif_citations_D02.csv')

CITATIONS = [
    ('senat_i1976_1977_0069_04.txt', '6 milliards de recettes supplémentaires escomptées en 1976'),
    ('senat_i1977_1978_0092_04.txt', 'procuré au régime général une recette supplémentaire de 7,4 milliards'),
    ('senat_i1979_1980_0054_04.txt', 'besoin de financement de l\'ordre de 15 milliards'),
    ('senat_i1980_1981_0102_03.txt', 'dix-huit mois allant du 1 sr août 1979 au 31 janvier 1981'),  # coquille de reconnaissance « 1 sr »
    ('CCSS-RAPPORT-JUILLET_1981.txt', '9.352 millions'),
    ('senat_i1979_1980_0054_04.txt', 'de l\'ordre de 1,4 milliard'),
    ('senat_i1981_1982_0058_03_29.txt', 'Un point supplémentaire déplafonné'),
    ('senat_i1982_1983_0032.txt', 'rendement sera de 4,6 milliards'),
    ('ccss_rapport_juin_1982.txt', 'contribution de 1 % sur l\'ensemble des revenus imposables'),
    ('CCSS-RAPPORT-DECEMBRE_1982.txt', 'exclut tout relèvement des cotisations dans le régime général'),
]

def norm(s):
    s = s.replace('’', "'").replace('-\n', '').replace('\n', ' ')
    return re.sub(r'\s+', ' ', s).lower()

lignes = []
for f, c in CITATIONS:
    t = norm(open(os.path.join(SRC, f), encoding='utf-8', errors='replace').read())
    k = t.find(norm(c))
    lignes.append([f, c, 'oui' if k >= 0 else 'non'])
with open(OUT, 'w', encoding='utf-8', newline='') as h:
    w = csv.writer(h, delimiter=';')
    w.writerow(['piece_D02', 'citation', 'retrouvee'])
    w.writerows(lignes)
for l in lignes:
    print(l)
