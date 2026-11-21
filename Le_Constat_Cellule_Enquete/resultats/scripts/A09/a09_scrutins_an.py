"""A09 - Récupère les listes de scrutins de l'Assemblée nationale (17e et 16e législatures)
filtrées par type (motions de censure) ou par dossier législatif (budgets), puis
extrait pour chaque scrutin : numéro, date, objet, décompte.
Usage : python -I a09_scrutins_an.py <dossier_sortie>
Les pages HTML sont conservées dans <dossier_sortie>/an_scrutins/.
"""
import sys, os, re, csv, time, urllib.parse
import requests
from bs4 import BeautifulSoup

OUT = sys.argv[1]
RAW = os.path.join(OUT, 'an_scrutins')
os.makedirs(RAW, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0'}
BASE = 'https://www.assemblee-nationale.fr'

REQUETES = [
    # (législature, libellé, paramètres)
    (17, 'MOC', {'typeScrutin': 'MOC'}),
    (16, 'MOC', {'typeScrutin': 'MOC'}),
    (17, 'PLF2025', {'dossierLegislatif': 'DLR5L17N50198'}),
    (17, 'PLF2026', {'dossierLegislatif': 'DLR5L17N52428'}),
    (17, 'PLF2027', {'dossierLegislatif': 'DLR5L17N54629'}),
    (17, 'PLFSS2025', {'dossierLegislatif': 'DLR5L17N50588'}),
    (17, 'PLFSS2026', {'dossierLegislatif': 'DLR5L17N52922'}),
    (17, 'PLFSS2027', {'dossierLegislatif': 'DLR5L17N54951'}),
]


def get(url, fname):
    p = os.path.join(RAW, fname)
    if not os.path.exists(p):
        r = requests.get(url, headers=UA, timeout=60)
        r.raise_for_status()
        open(p, 'wb').write(r.content)
        time.sleep(0.5)
    return open(p, 'rb').read().decode('utf-8', errors='replace')


def parse_list(html, leg):
    s = BeautifulSoup(html, 'html.parser')
    rows = []
    for li in s.select('li'):
        a = li.find('a', href=re.compile(r'/dyn/%d/scrutins/\d+$' % leg))
        if not a:
            continue
        txt = li.get_text(' ', strip=True)
        num = re.search(r'/scrutins/(\d+)$', a['href']).group(1)
        rows.append((num, txt))
    return rows


def main():
    out = []
    for leg, lab, params in REQUETES:
        page = 1
        vus = set()
        while True:
            q = dict(params); q.update({'page': page, 'limit': 100})
            url = f'{BASE}/dyn/{leg}/scrutins?' + urllib.parse.urlencode(q)
            html = get(url, f'liste_{leg}_{lab}_p{page}.html')
            rows = parse_list(html, leg)
            nouv = [r for r in rows if r[0] not in vus]
            if not nouv:
                break
            for num, txt in nouv:
                vus.add(num)
                out.append({'legislature': leg, 'requete': lab, 'numero': num,
                            'url': f'{BASE}/dyn/{leg}/scrutins/{num}', 'texte_liste': txt[:600]})
            page += 1
            if page > 10:
                break
    with open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'an_scrutins_listes.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter=';')
        w.writeheader(); w.writerows(out)
    print(len(out), 'lignes')


if __name__ == '__main__':
    main()
