# -*- coding: utf-8 -*-
"""A08 - Saisie des trajectoires programmees (programmes de stabilite, lois de programmation,
RESF/PLF, PSMT) telles que lues dans les pieces. Une ligne = (document, annee cible).
Chaque valeur renvoie a une piece de resultats\\donnees\\A08\\sources\\ (colonne source).
Ecrit : resultats\\donnees\\A08\\A08_trajectoires_programmees.csv
Convention : solde en % du PIB, signe negatif = deficit.
Usage : python -I vintages_A08.py
"""
import csv
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / 'donnees' / 'A08' / 'A08_trajectoires_programmees.csv'

S_SEN08 = ('senat_l08-07810.html (Senat, rapport n. 78 2008-2009, P. Marini, art. 2 du PLPFP 2009-2012, '
           'tableau "Les programmations successives de solde public")')
D = []


def add(i, t, lib, d, sc, data, src, rem=''):
    D.append((i, t, lib, d, sc, data, src, rem))


add('PS1998', 'PSTAB', 'Programme de stabilite 1999-2002 (Senat : PS 2000-2002)', '1998-12', 'prudent (2,5 %)',
    {1999: (-2.3, 2.4, None), 2000: (-2.0, 2.5, None), 2001: (-1.6, 2.5, None), 2002: (-1.2, 2.5, 51.5)},
    'pstab/fr_1999-02-16_recommendation_en.pdf p.3 (Commission IP/99/113, Key figures) ; ' + S_SEN08,
    'Favorable : -1,7/-1,2/-0,8. Croissance 2000-2002 = moyenne. Depense 2002 = borne haute de 50,6-51,5. '
    'Le Senat imprime "1,2" sans signe pour 2002 ; la Commission ecrit deficit de 0,8 a 1,2.')
add('PS2000', 'PSTAB', 'Programme de stabilite actualise 2000-2003 (Senat : PS 2001-2003)', '2000-01', 'prudent (2,5 %)',
    {2000: (-1.7, 3.0, None), 2001: (-1.3, 2.5, None), 2002: (-0.9, 2.5, None), 2003: (-0.5, 2.5, None)},
    'pstab/fr_2000-03-08_recommendation_en.pdf p.1-2 (Commission, Key figures) ; ' + S_SEN08,
    'Transmis le 28/1/2000. Favorable : -1,2/-0,7/-0,3. Croissance 2000 : "at least 3%". Estimation 1999 : -2,1.')
add('PS2000b', 'PSTAB', 'Programme de stabilite actualise 2001-2004 (Senat : PS 2002-2004)', '2000-12',
    'central (3 %) sauf 2004 prudent',
    {2001: (-1.0, None, None), 2002: (-0.6, 3.0, None), 2003: (-0.4, 3.0, None), 2004: (-0.5, 2.5, 50.6)},
    'pstab/fr_2001-01-24_recommendation_en.pdf p.3 (Key figures) ; pstab/fr_2000-12-01_sp_en.pdf ; ' + S_SEN08,
    '2002-2003 : seul le scenario central (3 %) est chiffre ; 2004 central = +0,2 (depense 49,8). Hors recettes UMTS.')
add('PS2001', 'PSTAB', 'Programme de stabilite 2002-2005 (Senat : PS 2003-2005)', '2001-12', 'prudent (2,5 %)',
    {2002: (-1.4, 2.5, None), 2003: (-1.3, 2.5, None), 2004: (-0.5, 2.5, None), 2005: (0.0, 2.5, None)},
    S_SEN08 + ' ; pstab/fr_2001-12-01_sp_annex_en.pdf p.2 (scenario 2,5 % de 2002 a 2005)', '')
add('PS2002', 'PSTAB', 'Programme de stabilite 2003-2006 (Senat : PS 2004-2006)', '2002-12', 'prudent (2,5 %)',
    {2003: (-2.6, None, None), 2004: (-2.1, 2.5, None), 2005: (-1.6, 2.5, None), 2006: (-1.0, 2.5, None)},
    S_SEN08 + ' ; pstab/fr_2002-12-13_sp_en.pdf ; pstab/fr_2003-01-07_ta_en.pdf', 'Croissance 2003 non relevee.')
add('PS2003', 'PSTAB', 'Programme de stabilite 2004-2007 (Senat : PS 2005-2007)', '2003-12', 'prudent (2,5 %)',
    {2004: (-3.6, 1.7, None), 2005: (-2.9, 2.5, None), 2006: (-2.2, 2.5, None), 2007: (-1.5, 2.5, None)},
    S_SEN08 + ' (2004 : -3,55) ; pstab/fr_2004-02-10_ta_en.pdf Table 1 (croissance)', 'Estimation 2003 : -4,0 (non saisie).')
add('PS2004', 'PSTAB', 'Programme de stabilite 2005-2008 (Senat : PS 2006-2008)', '2004-12', 'unique (2,5 %)',
    {2005: (-2.9, 2.5, 53.6), 2006: (-2.2, 2.5, 53.0), 2007: (-1.6, 2.5, 52.4), 2008: (-0.9, 2.5, 51.7)},
    S_SEN08 + ' ; pstab/fr_2005-02-15_ta_en.pdf Table 1 et Table 4', 'Premier programme a scenario unique (TA 2005, note 4).')
add('PS2005', 'PSTAB', 'Programme de stabilite 2006-2009 (Senat : PS 2007-2009)', '2005-12', 'unique (2,25 %)',
    {2006: (-2.9, 2.25, None), 2007: (-2.6, 2.25, None), 2008: (-1.9, 2.25, None), 2009: (-1.0, 2.25, None)},
    S_SEN08, 'Programme lui-meme non telecharge (archive en echec). Croissance = hypothese de moyen terme indiquee par le Senat.')
add('PS2006', 'PSTAB', 'Programme de stabilite 2007-2010 (Senat : PS 2008-2010)', '2006-12', 'unique (2,25 %)',
    {2007: (-2.5, 2.25, 52.9), 2008: (-1.8, 2.25, 52.0), 2009: (-0.9, 2.25, 51.1), 2010: (0.0, 2.25, 50.4)},
    S_SEN08 + ' ; pstab/2007-02-27_fr_ta_en.pdf Table 6', '')
add('PS2007', 'PSTAB', 'Programme de stabilite 2009-2012', '2007-11', 'unique (2,5 %)',
    {2008: (-2.3, 2.5, 52.6), 2009: (-1.7, 2.5, 51.9), 2010: (-1.2, 2.5, 51.2), 2011: (-0.6, 2.5, 50.6), 2012: (0.0, 2.5, 49.9)},
    S_SEN08 + ' ; pstab/2008-02-12_fr_ta_en.pdf Table 7', 'Estimation 2007 : -2,4.')
add('PLPFP2009', 'LPFP', 'Projet de loi de programmation 2009-2012 (texte depose)', '2008-09', 'unique',
    {2009: (-2.7, None, None), 2010: (-2.0, None, None), 2011: (-1.2, None, None), 2012: (-0.5, None, None)},
    S_SEN08 + ' (article 2 du projet)', 'Version deposee ; texte promulgue (loi 2009-135) non lu. Estimation 2008 : -2,7.')
add('PS2008', 'PSTAB', 'Programme de stabilite 2009-2012 (actualisation de decembre 2008)', '2008-12', 'unique',
    {2009: (-3.9, None, 53.5), 2010: (-2.7, None, 52.7), 2011: (-1.9, None, 52.0), 2012: (-1.1, None, 51.3)},
    'pstab/fr_2009-03-04_ta_en.pdf (tableau Composition of the budgetary adjustment, colonnes SP)', 'Estimation 2008 : -2,9.')
add('PS2010', 'PSTAB', 'Programme de stabilite 2010-2013', '2010-01', 'unique',
    {2010: (-8.2, None, 55.8), 2011: (-6.0, None, 54.6), 2012: (-4.6, None, 53.7), 2013: (-3.0, None, 52.8)},
    'pstab/fr_2010-03-31_ta_en.pdf (Table 5, colonnes SP)', 'Estimation 2009 : -7,9.')
add('LPFP2011', 'LPFP', 'Loi de programmation 2011-2014 (decembre 2010)', '2010-12', 'unique',
    {2011: (-6.0, None, None), 2012: (-4.6, None, None), 2013: (-3.0, None, None), 2014: (-2.0, None, None)},
    'pstab/fr_2011-05-03_sp_en.pdf p.7-8 (note 1 et phrase "in accordance with the 2011-2014 LPFP")',
    '2011 = 6,0 % dans la LPFP (note 1) ; 2012-2014 deduits de la phrase de conformite ; texte de loi non lu.')
add('PS2011', 'PSTAB', 'Programme de stabilite 2011-2014', '2011-04', 'unique',
    {2011: (-5.7, None, None), 2012: (-4.6, None, None), 2013: (-3.0, None, None), 2014: (-2.0, None, None)},
    'pstab/fr_2011-05-03_sp_en.pdf p.7', 'Estimation 2010 : -7,0.')
add('PS2012', 'PSTAB', 'Programme de stabilite 2012-2016', '2012-04', 'unique',
    {2012: (-4.4, None, 55.8), 2013: (-3.0, None, 55.1), 2014: (-2.0, 2.0, 54.2), 2015: (-1.0, 2.0, 53.4), 2016: (0.0, 2.0, 52.6)},
    'pstab/fr_2012-05-04_sp_en.pdf Table 2 (Multiyear public finance trajectory)', 'Estimation 2011 : -5,2.')
S13 = 'senat/senat_r13-4831.pdf Tableau 9 (Senat, rapport n. 483 2013-2014)'
add('LPFP2012', 'LPFP', 'Loi de programmation 2012-2017 (31/12/2012)', '2012-12', 'unique',
    {2012: (-4.5, None, None), 2013: (-3.0, None, None), 2014: (-2.2, None, None), 2015: (-1.3, None, None),
     2016: (-0.6, None, None), 2017: (-0.3, None, None)}, S13, '')
add('PS2013', 'PSTAB', 'Programme de stabilite 2013-2017', '2013-04', 'unique',
    {2013: (-3.7, None, None), 2014: (-2.9, None, None), 2015: (-2.0, None, None), 2016: (-1.2, None, None),
     2017: (-0.7, None, None)}, S13, 'Estimation 2012 : -4,8.')
add('RESF2014', 'PLF-RESF', 'Trajectoire du RESF annexe au PLF 2014', '2013-09', 'unique',
    {2014: (-3.6, None, None), 2015: (-2.8, None, None), 2016: (-1.7, None, None), 2017: (-1.2, None, None)},
    S13, 'Estimation 2013 : -4,1.')
add('PS2014', 'PSTAB', 'Programme de stabilite 2014-2017', '2014-04', 'unique',
    {2014: (-3.8, None, None), 2015: (-3.0, None, None), 2016: (-2.2, None, None), 2017: (-1.3, None, None)},
    S13, 'Execution 2013 publiee : -4,3.')
S14 = 'senat/senat_r14-6011.pdf Tableaux 4 et 15 (Senat, rapport n. 601 2014-2015)'
S15 = 'senat/senat_r15-5501.pdf p.14 Tableau 4 (Senat, rapport n. 550 2015-2016)'
add('LPFP2014', 'LPFP', 'Loi de programmation 2014-2019 (29/12/2014)', '2014-12', 'unique',
    {2015: (-4.1, None, None), 2016: (-3.6, None, None), 2017: (-2.7, None, None),
     2018: (-1.7, None, None), 2019: (-0.7, None, None)}, S14 + ' ; ' + S15, 'Estimation 2014 : -4,4.')
add('PS2015', 'PSTAB', 'Programme de stabilite 2015-2018', '2015-04', 'unique',
    {2015: (-3.8, None, None), 2016: (-3.3, None, None), 2017: (-2.7, None, None), 2018: (-1.9, None, None)},
    S14 + ' ; ' + S15, 'Estimation 2014 : -4,0.')
add('PLF2016', 'PLF-RESF', 'Trajectoire du PLF 2016', '2015-09', 'unique',
    {2016: (-3.3, None, None), 2017: (-2.7, None, None), 2018: (-1.9, None, None), 2019: (-1.3, None, None)},
    S15, 'Estimation 2015 : -3,8.')
add('PS2016', 'PSTAB', 'Programme de stabilite 2016-2019', '2016-04', 'unique',
    {2016: (-3.3, 1.5, None), 2017: (-2.7, 1.5, None), 2018: (-1.9, 1.75, None), 2019: (-1.2, 1.9, None)},
    S15 + ' et p.13 (croissance)', 'Execution 2015 publiee : -3,5.')
add('PS2017', 'PSTAB', 'Programme de stabilite 2017-2020', '2017-04', 'unique',
    {2017: (-2.8, None, 55.7), 2018: (-2.3, None, 55.3), 2019: (-1.6, None, 54.4), 2020: (-1.3, None, 53.5)},
    'pstab/CE_assessment_SP2017_fr.pdf Table 2 (Commission, Assessment of the 2017 Stability Programme for France)', '')
S17 = 'senat/senat_r17-4381.pdf p.23 (Senat, rapport n. 438 2017-2018, Evolution de la trajectoire budgetaire du Gouvernement)'
add('LPFP2018', 'LPFP', 'Loi de programmation 2018-2022 (22/1/2018)', '2018-01', 'unique',
    {2018: (-2.8, None, 54.0), 2019: (-2.9, None, 53.4), 2020: (-1.5, None, 52.6), 2021: (-0.9, None, 51.9),
     2022: (-0.3, None, 51.1)}, S17,
    'Depense publique (*) selon la definition du tableau du Senat (renvoi non lu). Estimation 2017 : -2,9.')
add('PS2018', 'PSTAB', 'Programme de stabilite 2018-2022', '2018-04', 'unique',
    {2018: (-2.3, None, 54.4), 2019: (-2.4, None, 53.5), 2020: (-0.9, None, 52.6), 2021: (-0.3, None, 51.9),
     2022: (0.3, None, 51.1)}, S17, 'Execution 2017 publiee : -2,6.')
S18 = 'senat/senat_r18-4681.pdf p.20 (Senat, rapport n. 468 2018-2019, tableau PLF 19 / Pstab)'
add('PLF2019', 'PLF-RESF', 'Trajectoire du PLF 2019', '2018-09', 'unique',
    {2019: (-2.8, None, 54.0), 2020: (-1.4, None, 53.3), 2021: (-0.7, None, 52.5), 2022: (-0.3, None, 51.8)},
    S18, 'Estimation 2018 : -2,6.')
add('PS2019', 'PSTAB', 'Programme de stabilite 2019-2022', '2019-04', 'unique',
    {2019: (-3.1, None, 54.0), 2020: (-2.0, None, 53.5), 2021: (-1.6, None, 53.0), 2022: (-1.2, None, 52.3)},
    S18, 'Execution 2018 publiee : -2,5. 2019 inclut la double charge CICE (base 2014).')
add('PS2021', 'PSTAB', 'Programme de stabilite 2021-2027', '2021-04', 'unique',
    {2021: (-9.0, None, 60.4), 2022: (-5.3, None, 56.0), 2023: (-4.4, None, 54.8), 2024: (-3.9, None, 54.2),
     2025: (-3.5, None, 53.8), 2026: (-3.2, None, 53.4), 2027: (-2.8, None, 53.1)},
    'senat/senat_r20-5551.pdf (Senat, rapport n. 555 2020-2021, tableau d apres le programme de stabilite 2021)',
    'Execution 2020 publiee : -9,2.')
add('PS2022', 'PSTAB', 'Programme de stabilite 2022-2027', '2022-07', 'unique',
    {2022: (-5.0, None, None), 2023: (-5.0, None, None), 2024: (-4.6, None, None), 2025: (-4.0, None, None),
     2026: (-3.4, None, None), 2027: (-2.9, None, None)},
    'hcfp/HCFP_avis_2022-3_PSTAB2022.pdf Tableau 3 (via web.archive.org)', '')
add('PLPFP2023', 'LPFP', 'Projet de loi de programmation 2023-2027 (depose le 26/9/2022)', '2022-09', 'unique',
    {2023: (-5.0, None, None), 2024: (-4.5, None, None), 2025: (-4.0, None, None), 2026: (-3.4, None, None),
     2027: (-2.9, None, None)},
    'hcfp/HCFP_opinion_2022-5_PLPFP2023-2027_EN.pdf (tableau Government balance, via web.archive.org)', '')
add('PS2023', 'PSTAB', 'Programme de stabilite 2023-2027', '2023-04', 'unique',
    {2023: (-4.9, 1.0, None), 2024: (-4.4, 1.6, None), 2025: (-3.7, 1.7, None), 2026: (-3.2, 1.7, None),
     2027: (-2.7, 1.8, None)},
    'hcfp/HCFP_avis_2023-6_PSTAB2023.pdf Tableau 3 ; fipeco/fipeco_Pstab2023-2027.pdf p.2 (croissance)',
    'Estimation 2022 : -4,7.')
add('LPFP2023', 'LPFP', 'Loi de programmation 2023-2027 (loi n. 2023-1195 du 18/12/2023)', '2023-12', 'unique',
    {2024: (-4.4, 1.4, None), 2025: (-3.7, 1.7, None), 2026: (-3.2, 1.7, None), 2027: (-2.7, 1.8, None)},
    'viepublique/VP_loi_286456_LPFP2023.html (fiche vie-publique de la loi, via web.archive.org)',
    'Estimation 2023 dans la loi : -4,9 (non comptee : annee echue de fait). Adoption definitive 15/11/2023 ; DC 2023-857 du 14/12/2023.')
add('PS2024', 'PSTAB', 'Programme de stabilite 2024-2027', '2024-04', 'unique',
    {2024: (-5.1, None, None), 2025: (-4.1, None, None), 2026: (-3.6, None, None), 2027: (-2.9, None, None)},
    'hcfp/HCFP_avis_2024-2_PSTAB2024.pdf Tableau 5 ; senat/senat_r23-5591.pdf p.13', 'Execution 2023 publiee : -5,5.')
add('PSMT2024', 'PSMT', 'Plan budgetaire et structurel a moyen terme 2025-2029', '2024-10', 'unique',
    {2025: (-5.0, None, None), 2026: (-4.6, None, None), 2027: (-4.0, None, None), 2028: (-3.3, None, None),
     2029: (-2.8, None, None)},
    'hcfp/HCFP_opinion_2025-3_RAA2025_EN.pdf Table 9 (via web.archive.org)', 'Estimation 2024 : -6,1 ; 2030 : -2,2 ; 2031 : -1,7.')
add('RAA2025', 'PSMT', 'Rapport annuel d avancement du PSMT (avril 2025)', '2025-04', 'unique',
    {2025: (-5.4, None, None), 2026: (-4.6, None, None), 2027: (-4.1, None, None), 2028: (-3.4, None, None),
     2029: (-2.8, None, None)},
    'hcfp/HCFP_opinion_2025-3_RAA2025_EN.pdf Table 9 ; senat/senat_r24-5671.pdf', 'Execution 2024 publiee : -5,8.')
add('RESF2027', 'PLF-RESF', 'Trajectoire du RESF annexe au PLF 2027', '2026-10', 'unique',
    {2026: (-5.4, None, None), 2027: (-5.0, None, None), 2028: (-3.9, None, None), 2029: (-2.8, None, None),
     2030: (-2.4, None, None)},
    'donnees/A03/sources/PLF2027_RESF.pdf p.134 Tableau 21 (piece d A03)',
    'Trajectoire 2028-2030 de "caractere conventionnel" (RESF). Aucune execution disponible.')


def fmt(x):
    return '' if x is None else str(x).replace('.', ',')


with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['id_document', 'type', 'intitule', 'date_publication', 'scenario', 'annee_cible',
                'solde_programme_pctPIB', 'croissance_reelle_programme_pct', 'depense_programme_pctPIB',
                'source', 'remarque'])
    for i, t, lib, d, sc, data, src, rem in D:
        for a in sorted(data):
            s, g, dep = data[a]
            w.writerow([i, t, lib, d, sc, a, fmt(s), fmt(g), fmt(dep), src, rem])
print(OUT, len(D), 'documents')
