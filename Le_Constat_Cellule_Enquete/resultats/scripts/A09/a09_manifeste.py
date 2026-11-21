"""A09 - Construit resultats/donnees/A09/MANIFESTE_PIECES.csv : une ligne par fichier de sources/,
avec fichier ; url_origine ; canal ; date ; octets ; sha256.
Les fichiers .txt sont des extractions locales (python -I, bs4 ou pymupdf) du fichier de même nom.
Usage : python -I a09_manifeste.py <racine_resultats>
"""
import sys, os, re, hashlib, csv, urllib.parse

R = sys.argv[1]
S = os.path.join(R, 'donnees', 'A09', 'sources')
AN = 'https://www.assemblee-nationale.fr'
LEGBASE = 'https://www2.assemblee-nationale.fr/decouvrir-l-assemblee/histoire/la-ve-republique/tous-les-deputes-depuis-1958'
LEGSLUG = {5: 've-legislature-2-avril-1973-2-avril-1978', 6: 'vie-legislature-3-avril-1978-22-mai-1981',
           7: 'viie-legislature-2-juillet-1981-1er-avril-1986', 8: 'viiie-legislature-2-avril-1986-14-mai-1988',
           9: 'ixe-legislature-23-juin-1988-1er-avril-1993', 10: 'xe-legislature-2-avril-1993-21-avril-1997',
           11: 'xie-legislature-1er-juin-1997-18-juin-2002', 12: 'xiie-legislature-19-juin-2002-19-juin-2007',
           13: 'xiiie-legislature-20-juin-2007-19-juin-2012', 14: 'xive-legislature-20-juin-2012-20-juin-2017'}
REQ = {'MOC': {'typeScrutin': 'MOC'}, 'PLF2025': {'dossierLegislatif': 'DLR5L17N50198'},
       'PLF2026': {'dossierLegislatif': 'DLR5L17N52428'}, 'PLF2027': {'dossierLegislatif': 'DLR5L17N54629'},
       'PLFSS2025': {'dossierLegislatif': 'DLR5L17N50588'}, 'PLFSS2026': {'dossierLegislatif': 'DLR5L17N52922'},
       'PLFSS2027': {'dossierLegislatif': 'DLR5L17N54951'}}
FIXE = {
    'an_scrutins_17_p1.html': AN + '/dyn/17/scrutins?page=1&limit=100',
    'an_scrutin_17_519.html': AN + '/dyn/17/scrutins/519',
    'an_scrutins/recherche_d%C3%A9clara.html': AN + '/dyn/17/scrutins?rechercheTextuelle=d%C3%A9claration+de+politique+g%C3%A9n%C3%A9rale&page=1&limit=100',
    'an_scrutins/recherche_article+49%2.html': AN + '/dyn/17/scrutins?rechercheTextuelle=article+49%2C+alin%C3%A9a+1&page=1&limit=100',
    'an_scrutins/rech15_motion_de_censure.html': AN + '/dyn/15/scrutins?rechercheTextuelle=motion+de+censure&page=1&limit=100',
    'an_scrutins/rech15_premi_C3_A8re_partie.html': AN + '/dyn/15/scrutins?rechercheTextuelle=premi%C3%A8re+partie+du+projet+de+loi+de+finances+pour+2018&page=1&limit=100',
    'an_scrutins/rech15_syst_C3_A8me_univers.html': AN + '/dyn/15/scrutins?rechercheTextuelle=syst%C3%A8me+universel+de+retraite&page=1&limit=100',
    'an_scrutins/rech15_urgence__C3_A9conomi.html': AN + '/dyn/15/scrutins?rechercheTextuelle=urgence+%C3%A9conomiques+et+sociales&page=1&limit=100',
    'an_scrutins/arch_11_index_leg.html': AN + '/11/scrutins/index-11leg.asp',
    'an_legislatures/index.html': LEGBASE,
    'an_legislatures/leg1.html': LEGBASE + '/iere-legislature-9-decembre-1958-9-octobre-1962',
    'an_legislatures/12_seance_STATS2002-12.pdf': AN + '/12/seance/STATS2002-12.pdf',
    'an_legislatures/connaissance_rapactiv2002_4-5.pdf': AN + '/connaissance/rapactiv2002/4-5.pdf',
    'an_legislatures/connaissance_rapactiv2007_rapactiv2007-08-09.pdf': AN + '/connaissance/rapactiv2007/rapactiv2007-08-09.pdf',
    'datagouv/gouvernements_pm.csv': 'https://www.data.gouv.fr/api/1/datasets/r/5e8c4460-11a6-433b-b48a-694ab7a0357d',
    'datagouv/presidents.csv': 'https://www.data.gouv.fr/api/1/datasets/r/0492fc8f-da9f-4c43-a899-66583a626b24',
    'ameco/ameco17.zip': 'https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco17.zip',
    'ameco/AMECO17.TXT': 'extrait de ameco/ameco17.zip (https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco17.zip)',
    'mobilisation/insee_7767085.html': 'https://www.insee.fr/fr/statistiques/7767085',
    'electorat/insee_ip1929_6658143.html': 'https://www.insee.fr/fr/statistiques/6658143',
    'senat/l18-2321.pdf': 'https://www.senat.fr/rap/l18-232/l18-2321.pdf',
    'senat/r13-543-1-syn.pdf': 'https://www.senat.fr/rap/r13-543-1/r13-543-1-syn.pdf',
    'motions/MotionCensure_LFI_20241202.pdf': 'https://www2.assemblee-nationale.fr/static/17/motions_censure/MotionCensure_LFI_20241202.pdf',
    'motions/MotionCensure_RN_20241202.pdf': 'https://www2.assemblee-nationale.fr/static/17/motions_censure/MotionCensure_RN_20241202.pdf',
    'an_cr/seance-du-mardi-14-octobre-2025.html': AN + '/dyn/17/comptes-rendus/seance/session-ordinaire-de-2025-2026/seance-du-mardi-14-octobre-2025',
    'an_archives_10/cri_1995-1996_071.pdf': 'https://archives.assemblee-nationale.fr/10/cri/1995-1996-ordinaire1/071.pdf',
    'mobilisation/ECRT2024_F4.7.xlsx': 'https://www.insee.fr/fr/statistiques/fichier/7767085/ECRT2024_F4.7.xlsx',
    'an_scrutins/rech14_plf2014.html': AN + '/dyn/14/scrutins?rechercheTextuelle=premi%C3%A8re+partie+du+projet+de+loi+de+finances+pour+2014&page=1&limit=100',
    'an_scrutins/rech14_plf2015.html': AN + '/dyn/14/scrutins?rechercheTextuelle=premi%C3%A8re+partie+du+projet+de+loi+de+finances+pour+2015&page=1&limit=100',
    'an_scrutins/rech14_plf2016.html': AN + '/dyn/14/scrutins?rechercheTextuelle=premi%C3%A8re+partie+du+projet+de+loi+de+finances+pour+2016&page=1&limit=100',
    'an_scrutins/rech15_plf2020.html': AN + '/dyn/15/scrutins?rechercheTextuelle=premi%C3%A8re+partie+du+projet+de+loi+de+finances+pour+2020&page=1&limit=100',
}


def origine(rel):
    if rel in FIXE:
        return FIXE[rel], ('curl' if not rel.endswith('.TXT') else 'extraction locale (zipfile)')
    if rel.endswith('.txt') and not rel.endswith('_retraites.txt'):
        base = rel[:-4]
        for ext in ('.html', '.pdf'):
            if os.path.exists(os.path.join(S, base + ext)):
                u, _ = origine(base + ext)
                return f'extraction texte de {base + ext} ({u})', 'extraction locale python -I (bs4 / pymupdf)'
    if rel.endswith('_retraites.txt'):
        return 'dérivé local de ' + rel.replace('_retraites.txt', '.txt') + ' par a09_explications_censure.py', 'calcul local'
    m = re.match(r'an_scrutins/scrutin_(\d+)_(\d+)\.html$', rel)
    if m: return f'{AN}/dyn/{m.group(1)}/scrutins/{m.group(2)}', 'requests (a09_detail_scrutins.py)'
    m = re.match(r'an_scrutins/liste_(\d+)_(\w+?)_p(\d+)\.html$', rel)
    if m:
        q = dict(REQ[m.group(2)]); q.update({'page': m.group(3), 'limit': 100})
        return f'{AN}/dyn/{m.group(1)}/scrutins?' + urllib.parse.urlencode(q), 'requests (a09_scrutins_an.py)'
    m = re.match(r'an_scrutins/arch_(\d+)_jo(\d+)\.html$', rel)
    if m: return f'{AN}/{m.group(1)}/scrutins/jo{m.group(2)}.asp', 'curl / requests (a09_scrutins_archives.py)'
    m = re.match(r'an_scrutins/arch_(\d+)_index\.html$', rel)
    if m: return f'{AN}/{m.group(1)}/documents/index-scrutins.asp', 'curl'
    m = re.match(r'an_cr/(CRSANR5L(\d+)S\w+)\.html$', rel)
    if m: return f'{AN}/dyn/{m.group(2)}/comptes-rendus/seance/{m.group(1)}', 'curl'
    m = re.match(r'an_legislatures/leg(\d+)\.html$', rel)
    if m: return f'{LEGBASE}/{LEGSLUG[int(m.group(1))]}', 'curl / requests (a09_legislatures_an.py)'
    return 'INCONNU', ''


rows = []
for dp, dn, fn in os.walk(S):
    for f in sorted(fn):
        p = os.path.join(dp, f); rel = os.path.relpath(p, S).replace('\\', '/')
        u, canal = origine(rel)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rows.append({'fichier': rel, 'url_origine': u, 'canal': canal, 'date': '20/11/2026',
                     'octets': os.path.getsize(p), 'sha256': h})
rows.sort(key=lambda r: r['fichier'])
with open(os.path.join(R, 'donnees', 'A09', 'MANIFESTE_PIECES.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter=';'); w.writeheader(); w.writerows(rows)
print(len(rows), 'fichiers ;', sum(r['url_origine'] == 'INCONNU' for r in rows), 'sans origine')
for r in rows:
    if r['url_origine'] == 'INCONNU': print('  ', r['fichier'])
