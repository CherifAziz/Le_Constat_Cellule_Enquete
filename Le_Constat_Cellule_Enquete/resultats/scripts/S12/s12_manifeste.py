# -*- coding: utf-8 -*-
"""Écrit donnees/S12/MANIFESTE_PIECES.csv (fichier ; url_origine ; canal ; date ; octets ; sha256)."""
import os, hashlib, csv
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'donnees', 'S12'))
W2 = 'https://www2.assemblee-nationale.fr/decouvrir-l-assemblee/histoire/la-ve-republique/tous-les-deputes-depuis-1958/'
U = {
 'an_www2_Ve_legislature_liste.html': W2 + 've-legislature-2-avril-1973-2-avril-1978',
 'an_www2_VIe_legislature_liste.html': W2 + 'vie-legislature-3-avril-1978-22-mai-1981',
 'an_www2_VIIe_legislature_liste.html': W2 + 'viie-legislature-2-juillet-1981-1er-avril-1986',
 'an_www2_Xe_legislature_liste.html': W2 + 'xe-legislature-2-avril-1993-21-avril-1997',
 'an_modif5_Ve_modifications.html': 'http://www.assemblee-nationale.fr/5/modif5.asp',
 'an_Ve_tables_analytiques_HO.pdf': 'https://archives.assemblee-nationale.fr/5/tanalytique/1973-1978_tmatieres_HO.pdf',
 'jo_an_1974-11-20_3e_seance_LFI1975.pdf': 'https://archives.assemblee-nationale.fr/5/cri/1974-1975-ordinaire1/066.pdf',
 'jo_an_1977-11-18_3e_seance_LFI1978.pdf': 'https://archives.assemblee-nationale.fr/5/cri/1977-1978-ordinaire1/060.pdf',
 'jo_an_1986-11-14_3e_seance_LFI1987.pdf': 'https://archives.assemblee-nationale.fr/8/cri/1986-1987-ordinaire1/075.pdf',
 'jo_an_1987-11-13_2e_seance_LFI1988.pdf': 'https://archives.assemblee-nationale.fr/8/cri/1987-1988-ordinaire1/070.pdf',
 'jo_an_1987-11-13_3e_seance_LFI1988_partiel.pdf': 'https://archives.assemblee-nationale.fr/8/cri/1987-1988-ordinaire1/071.pdf',
 'jo_an_1992-11-17_LFI1993.pdf': 'https://archives.assemblee-nationale.fr/9/cri/1992-1993-ordinaire1/078.pdf',
 'jo_an_2001-10-23_LFI2002_1re_partie.pdf': 'https://archives.assemblee-nationale.fr/11/cri/2001-2002-ordinaire1/028.pdf',
 'an_scrutin_XII_1031.html': 'https://www.assemblee-nationale.fr/12/scrutins/jo1031.asp',
 'an_scrutin_XIII_0818.html': 'https://www.assemblee-nationale.fr/13/scrutins/jo0818.asp',
 'an_fiche56_votes.pdf': 'https://www.assemblee-nationale.fr/dyn/contenu/telechargement/629143/file/Fiche%2056%20-%20Votes.pdf',
}
for n in (62, 698, 955, 1177, 1189, 1352):
    U['an_scrutin_XIV_%d.html' % n] = 'https://www.assemblee-nationale.fr/dyn/14/scrutins/%d' % n
for n in (300, 1400, 2250, 2350, 3200, 4100):
    U['an_scrutin_XV_%d.html' % n] = 'https://www.assemblee-nationale.fr/dyn/15/scrutins/%d' % n
EXTRA = {}  # complété pour la partie B
p = os.path.join(R, 'sources_B_urls.csv')
if os.path.exists(p):
    for row in csv.reader(open(p, encoding='utf-8'), delimiter=';'):
        if row and row[0] != 'fichier': U[row[0]] = row[1]
rows = []
for f in sorted(os.listdir(os.path.join(R, 'sources'))):
    b = open(os.path.join(R, 'sources', f), 'rb').read()
    rows.append([f, U.get(f, 'INCONNUE'), 'curl -L -A Mozilla/5.0', '2026-11-21', str(len(b)), hashlib.sha256(b).hexdigest()])
with open(os.path.join(R, 'MANIFESTE_PIECES.csv'), 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter=';'); w.writerow(['fichier', 'url_origine', 'canal', 'date', 'octets', 'sha256']); w.writerows(rows)
print(len(rows), 'lignes ;', sum(r[1] == 'INCONNUE' for r in rows), 'sans URL')
