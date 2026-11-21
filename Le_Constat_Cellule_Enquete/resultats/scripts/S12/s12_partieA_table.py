# -*- coding: utf-8 -*-
"""S12 partie A : table des 51 exercices, majorité à la date du vote (relevés faits sur pièces AN),
comparaison avec A09, recomptes. Lancer : python -I s12_partieA_table.py
Entrées : relevés codés ci-dessous (chaque relevé renvoie à une pièce de donnees/S12/sources),
table A09 (lecture seule) pour le solde, le solde primaire et le classement d'A09.
Sorties : donnees/S12/s12_partieA_majorites_vote.csv, donnees/S12/s12_partieA_resultats.txt
"""
import csv, os, hashlib
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
A09 = os.path.join(R, 'donnees', 'A09', 'a09_table_exercices_1975_2025.csv')
OUT = os.path.join(R, 'donnees', 'S12')

# Relevés par point de mesure (date, pièce, sièges camp gouvernemental, sièges pourvus, groupe principal, voix pour)
# seuil = sièges pourvus // 2 + 1 (Fiche 56 AN : majorités calculées sur les sièges effectivement pourvus)
P = {
 'V_1974':  dict(date='1974-11-20', piece='jo_an_1974-11-20_3e_seance_LFI1975.pdf (JO p. 6891, 6905)', camp=None, pourvus=490, princ=None, pour=297, note='LFI 1975 ensemble 1re lecture : 297 pour, 182 contre ; applaudissements UDR, RI, Réformateurs-centristes-démocrates sociaux ; groupes non chiffrés dans la pièce ; sièges pourvus = 490 [hypothèse, 491 sièges]'),
 'V_1975':  dict(date='1975-11-19', piece='jo_an_1975-11-19_3e_seance_LFI1976.pdf (scrutin n° 258, p. 8746)', camp=None, pourvus=490, princ=None, pour=299, note='LFI 1976 ensemble 1re lecture : 299 pour, 183 contre'),
 'V_1976':  dict(date='1976-11-20', piece='jo_an_1976-11-20_seance_LFI1977.pdf (scrutin n° 405, p. 8557)', camp=None, pourvus=490, princ=None, pour=281, note='LFI 1977 ensemble 1re lecture, vote bloqué (art. 44) : 281 pour, 183 contre'),
 'V_1977':  dict(date='1977-11-18', piece='jo_an_1977-11-18_3e_seance_LFI1978.pdf (scrutin n° 498)', camp=None, pourvus=490, princ=None, pour=285, note='LFI 1978 ensemble 1re lecture : 285 pour, 176 contre'),
 'VI_1978': dict(date='1978-04-03', piece='an_www2_VIe_legislature_liste.html (composition d\'ouverture ; A09 : RPR 155 + UDF 124)', camp=279, pourvus=491, princ=155, pour=None, note='composition la plus proche : ouverture ; recompte partiel S12 des liens : RPR 141 + UDF 118 = 259 (borne basse, liste incomplète)'),
 'VII_1981':dict(date='1981-07-01', piece='an_www2_VIIe_legislature_liste.html (ouverture ; A09 : S 287)', camp=287, pourvus=491, princ=287, pour=None, note='composition la plus proche : ouverture ; recompte partiel S12 : S >= 282'),
 'VIII_1986':dict(date='1986-11-14', piece='jo_an_1986-11-14_3e_seance_LFI1987.pdf (scrutin n° 467)', camp=158+129, pourvus=576, princ=158, pour=290, note='S 211, RPR 158 (pour 156 + 2 non-votants ; OCR « 168 »), UDF 129, FN 33, C 35, NI 10 ; adopté 290 contre 282 grâce à 6 NI'),
 'VIII_1987':dict(date='1987-11-13', piece='jo_an_1987-11-13_2e_seance_LFI1988.pdf (scrutins n° 821-825)', camp=157+132, pourvus=577, princ=157, pour=None, note='S 214, RPR 157, UDF 132 (vérifiés par la somme des votes des scrutins 822-825), FN 33, C 35, NI 6 (OCR « 8 » corrigé par la somme des votes) ; vote sur l\'ensemble non retrouvé (pièce 3e séance tronquée)'),
 'IX_1992': dict(date='1992-11-17', piece='jo_an_1992-11-17_LFI1993.pdf (scrutin n° 717)', camp=267, pourvus=572, princ=267, pour=None, note='S 267 (pour 262 + 5 NV ; OCR « 287 » corrigé sur image), RPR 125, UDF 88, UDC 40, C 28, NI 24'),
 'X_1993':  dict(date='1993-04-03', piece='an_www2_Xe_legislature_liste.html', camp=257+214, pourvus=577, princ=257, pour=None, note='recompte S12 identique à A09 : RPR 257, UDF 214'),
 'XI_2001': dict(date='2001-10-23', piece='jo_an_2001-10-23_LFI2002_1re_partie.pdf (scrutin n° 357)', camp=250+35+30, pourvus=565, princ=250, pour=None, note='SOC 250, COM 35, RCV 30, RPR 136, UDF 68, DL 42, NI 4'),
 'XII_2006':dict(date='2006-11-21', piece='an_scrutin_XII_1031.html', camp=362, pourvus=575, princ=362, pour=356, note='UMP 362, SOC 150, UDF 29, CR 22, NI 12'),
 'XIII_2011':dict(date='2011-11-16', piece='an_scrutin_XIII_0818.html', camp=307, pourvus=562, princ=307, pour=315, note='UMP 307, SRC 197, GDR 25, NC 24, NI 9'),
 'XIV_2012':dict(date='2012-11-20', piece='an_scrutin_XIV_62.html', camp=296+16, pourvus=574, princ=296, pour=317, note='SRC 296, UMP 194, UDI 29, ECOLO 17, RRDP 16, GDR 15, NI 7'),
 'XIV_2013':dict(date='2013-11-19', piece='an_scrutin_XIV_698.html', camp=292+16, pourvus=577, princ=292, pour=320, note='SRC 292, UMP 199, UDI 30, ECOLO 17, RRDP 16, GDR 15, NI 8'),
 'XIV_2014':dict(date='2014-11-18', piece='an_scrutin_XIV_955.html', camp=288+17, pourvus=574, princ=288, pour=266, note='SRC 288, UMP 197, UDI 30, ECOLO 18, RRDP 17, GDR 15, NI 9 ; ATTENTION : LFI adoptée par 266 voix seulement (seuil 288) : un seul groupe en sièges, pas en voix'),
 'XIV_2015':dict(date='2015-11-17', piece='an_scrutin_XIV_1189.html (et 1177 du 20/10/2015)', camp=287+18, pourvus=577, princ=287, pour=290, note='SRC 287, LR 199, UDI 30, ECOLO 18, RRDP 18, GDR 15, NI 10 ; camp SRC+RRDP : présence du RRDP au Gouvernement [M] ; statut absolu établi indépendamment par 290 voix pour >= 289 [C]'),
 'XIV_2016':dict(date='2016-11-22', piece='an_scrutin_XIV_1352.html', camp=288+18, pourvus=573, princ=288, pour=287, note='SER 288, LR 199, UDI 27, RRDP 18, GDR 15, NI 26'),
 'XV_2017': dict(date='2017-11-23', piece='an_scrutin_XV_300.html', camp=312+47, pourvus=576, princ=312, pour=None, note='LREM 312, MODEM 47 ; total listé 576'),
 'XV_2018': dict(date='2018-11-13', piece='an_scrutin_XV_1400.html', camp=308+46, pourvus=576, princ=308, pour=None, note='LREM 308, MODEM 46'),
 'XV_2019': dict(date='2019-10-31', piece='an_scrutin_XV_2250.html (et 2350 du 11/12/2019 : LREM 303)', camp=304+46, pourvus=576, princ=304, pour=None, note='LREM 304, MODEM 46'),
 'XV_2020': dict(date='2020-11-19', piece='an_scrutin_XV_3200.html', camp=271+56+20, pourvus=576, princ=271, pour=None, note='LREM 271, MODEM 56, Agir 20'),
 'XV_2021': dict(date='2021-11-03', piece='an_scrutin_XV_4100.html', camp=268+57+22, pourvus=570, princ=268, pour=None, note='LREM 268, MODEM 57, Agir 22 ; total listé 570'),
 'XVI_2022':dict(date='2022-07-11', piece='A09 : scrutin n° 1 XVIe (non relu par S12)', camp=250, pourvus=577, princ=172, pour=None, note='RE+DEM+HOR 250 ; budget adopté par 49.3'),
 'XVI_2023':dict(date='2022-07-11', piece='A09 : scrutin n° 1 XVIe (non relu par S12)', camp=250, pourvus=577, princ=172, pour=None, note='composition la plus proche relevée : juillet 2022 ; marge -39'),
 'XVII_2024':dict(date='2024-10-08', piece='A09 : scrutin n° 1 XVIIe (non relu par S12)', camp=211, pourvus=577, princ=95, pour=None, note='EPR+DEM+HOR+DR 211 ; budget 2025 adopté en février 2025 par 49.3'),
}
# exercice -> point de mesure (vote de l'automne N-1 ; 2025 voté en février 2025)
M = {}
for y in (1975,): M[y] = ('V_1974', 'mesure')
M[1976] = ('V_1975', 'mesure'); M[1977] = ('V_1976', 'mesure')
M[1978] = ('V_1977', 'mesure')
for y in (1979, 1980, 1981): M[y] = ('VI_1978', 'plus proche (ouverture)')
for y in range(1982, 1987): M[y] = ('VII_1981', 'plus proche (ouverture)')
M[1987] = ('VIII_1986', 'mesure'); M[1988] = ('VIII_1987', 'mesure')
for y in range(1989, 1993): M[y] = ('IX_1992', 'plus proche (nov. 1992)')
M[1993] = ('IX_1992', 'mesure')
for y in range(1994, 1998): M[y] = ('X_1993', 'plus proche (ouverture)')
for y in range(1998, 2003): M[y] = ('XI_2001', 'plus proche (oct. 2001)' if y != 2002 else 'mesure (1re partie)')
for y in range(2003, 2008): M[y] = ('XII_2006', 'plus proche (nov. 2006)' if y != 2007 else 'mesure')
for y in range(2008, 2013): M[y] = ('XIII_2011', 'plus proche (nov. 2011)' if y != 2012 else 'mesure')
M[2013] = ('XIV_2012', 'mesure'); M[2014] = ('XIV_2013', 'mesure'); M[2015] = ('XIV_2014', 'mesure')
M[2016] = ('XIV_2015', 'mesure'); M[2017] = ('XIV_2016', 'mesure')
M[2018] = ('XV_2017', 'plus proche (23/11/2017 ; date du vote non relevée)'); M[2019] = ('XV_2018', 'plus proche (13/11/2018 ; date du vote non relevée)'); M[2020] = ('XV_2019', 'plus proche (31/10/2019 ; date du vote non relevée)')
M[2021] = ('XV_2020', 'plus proche (19/11/2020 ; date du vote non relevée)'); M[2022] = ('XV_2021', 'plus proche (03/11/2021 ; date du vote non relevée)')
M[2023] = ('XVI_2022', 'plus proche (ouverture)'); M[2024] = ('XVI_2023', 'plus proche (ouverture)'); M[2025] = ('XVII_2024', 'plus proche (ouverture)')

VOTE = {1975:'1974-11-20', 1976:'1975-11-19', 1977:'1976-11-20', 1978:'1977-11-18', 1987:'1986-11-14', 1988:'1987-11-13 (jour du vote, scrutin d ensemble non lu)',
 2007:'2006-11-21', 2011:'2010-11-17', 2012:'2011-11-16', 2013:'2012-11-20', 2014:'2013-11-19', 2015:'2014-11-18', 2016:'2015-11-17', 2017:'2016-11-22'}

def classe(p):
    seuil = p['pourvus'] // 2 + 1
    if p['camp'] is None:  # V : seules les voix pour sont connues
        return seuil, ('coalition' if p['pour'] >= seuil else 'inconnu'), 'voix pour >= seuil'
    if p['princ'] is not None and p['princ'] >= seuil and p['camp'] == p['princ']:
        return seuil, 'parti_seul', ''
    if p['princ'] is not None and p['princ'] >= seuil:
        return seuil, 'parti_seul', 'groupe principal seul au-dessus du seuil'
    if p['camp'] >= seuil:
        return seuil, 'coalition', ''
    if p['pour'] is not None and p['pour'] >= seuil:
        return seuil, 'appoint', 'groupes du camp sous le seuil, voix pour au-dessus avec des non-inscrits'
    return seuil, 'relative_ou_sans', ''

a09 = {int(r['exercice']): r for r in csv.DictReader(open(A09, encoding='utf-8'), delimiter=';')}
ABS = {'parti_seul', 'coalition'}
A09ABS = {'parti_seul', 'coalition'}
rows = []
for y in range(1975, 2026):
    k, how = M[y]; p = P[k]
    seuil, typ, why = classe(p)
    # variante seuil nominal 289 (577 sièges) ou 246 (491)
    nominal = 289 if p['pourvus'] > 491 else 246
    typ_nom = typ
    if typ == 'parti_seul' and p['princ'] < nominal: typ_nom = 'coalition' if p['camp'] >= nominal else 'relative_ou_sans'
    t9 = a09[y]['legislature_vote_LFI'], a09[y]['type_majorite']
    rows.append(dict(exercice=y, date_vote_1re_lecture=VOTE.get(y,'non relevée'), point=k, date_mesure=p['date'], rapport_au_vote=how, piece=p['piece'],
        sieges_camp=p['camp'] if p['camp'] is not None else '', sieges_groupe_principal=p['princ'] if p['princ'] is not None else '',
        voix_pour=p['pour'] if p['pour'] is not None else '', sieges_pourvus=p['pourvus'], seuil=seuil,
        type_S12=typ, type_S12_seuil_nominal=typ_nom, type_A09=t9[1],
        accord_A09=('oui' if (typ in ABS) == (t9[1] in A09ABS) and (typ == 'parti_seul') == (t9[1] == 'parti_seul') else 'NON'),
        solde_pct=a09[y]['solde_pct'], solde_primaire_pct=a09[y]['solde_primaire_pct'], note=p['note'] + (' ; ' + why if why else '')))

with open(os.path.join(OUT, 's12_partieA_majorites_vote.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';'); w.writeheader(); w.writerows(rows)

def cnt(key, vals): return [r['exercice'] for r in rows if r[key] in vals]
out = []
out.append('Exercices en déficit (solde < 0) : %d sur %d' % (sum(float(r['solde_pct']) < 0 for r in rows), len(rows)))
for lab, key in (('S12 (seuil sièges pourvus)', 'type_S12'), ('S12 variante seuil nominal', 'type_S12_seuil_nominal'), ('A09', 'type_A09')):
    ab = cnt(key, ABS); ps = cnt(key, {'parti_seul'})
    out.append('%s : majorité absolue %d ; dont parti seul %d ; déficits parmi elles %d ; excédents primaires sous parti seul %s ; excédents primaires sous majorité absolue %s' % (
        lab, len(ab), len(ps), sum(float(r['solde_pct']) < 0 for r in rows if r['exercice'] in ab),
        [r['exercice'] for r in rows if r['exercice'] in ps and float(r['solde_primaire_pct']) > 0],
        [r['exercice'] for r in rows if r['exercice'] in ab and float(r['solde_primaire_pct']) > 0]))
out.append('Avec appoint (1987) compté comme absolu : %d' % (len(cnt('type_S12', ABS | {'appoint'}))))
out.append('Lignes en désaccord avec A09 : ' + ', '.join('%d (%s -> %s)' % (r['exercice'], r['type_A09'], r['type_S12']) for r in rows if r['accord_A09'] == 'NON'))
out.append('Lignes différentes sous seuil nominal : ' + ', '.join('%d' % r['exercice'] for r in rows if r['type_S12'] != r['type_S12_seuil_nominal']))
out.append('Lignes mesurées à la date du vote (ou le jour même) : %d ; composition la plus proche : %d' % (sum(r['rapport_au_vote']=='mesure' or r['rapport_au_vote'].startswith('mesure') for r in rows), sum(not r['rapport_au_vote'].startswith('mesure') for r in rows)))
for lab, sel in (('majorité absolue', ABS), ('autres', {'appoint','relative_ou_sans'})):
    yy=[r for r in rows if r['type_S12'] in sel]; out.append('Excédents primaires sous %s : %d sur %d' % (lab, sum(float(r['solde_primaire_pct'])>0 for r in yy), len(yy)))
out.append('Excédents primaires (tous exercices) : ' + str([(r['exercice'], r['type_S12']) for r in rows if float(r['solde_primaire_pct']) > 0]))
txt = '\n'.join(out); print(txt)
open(os.path.join(OUT, 's12_partieA_resultats.txt'), 'w', encoding='utf-8').write(txt + '\n')
