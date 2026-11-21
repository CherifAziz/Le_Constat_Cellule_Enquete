"""A09 - Analyse des scrutins des législatures XI à XIII (pages d'archives .asp de l'Assemblée nationale).
Usage : python -I a09_scrutins_archives.py <dossier_sources> <leg>:<num> ...  (num sur 4 chiffres, ex. 12:0310)
Sortie : stdout + ajout à <dossier_sources>/../an_scrutins_archives_detail.csv
"""
import sys, os, re, csv, time
import requests
from bs4 import BeautifulSoup

SRC = sys.argv[1]
D = os.path.join(SRC, 'an_scrutins'); os.makedirs(D, exist_ok=True)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
rows = []
for arg in sys.argv[2:]:
    leg, num = arg.split(':')
    url = f'https://www.assemblee-nationale.fr/{leg}/scrutins/jo{num}.asp'
    p = os.path.join(D, f'arch_{leg}_jo{num}.html')
    if not os.path.exists(p):
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        open(p, 'wb').write(r.content); time.sleep(0.5)
    t = BeautifulSoup(open(p, 'rb').read(), 'html.parser').get_text(' ', strip=True)
    t = re.sub(r'\s+', ' ', t)
    i = t.find('ANALYSE DU SCRUTIN', 200)
    i = t.find('ANALYSE DU SCRUTIN') if i < 0 else i
    head = t[i:i + 600]
    tot = re.search(r'Nombre de votants\s*:\s*(\d+).*?exprim.s\s*:\s*(\d+).*?Pour l.adoption\s*:\s*(\d+)(?:\s*Contre\s*:\s*(\d+))?', t[i:])
    print(f'== {leg}/{num} {head[:330]}')
    for m in re.finditer(r"(GROUPE\s+[^()]{2,90}?|NON[- ]INSCRITS?)\s*\((\d+)\)(.*?)(?=GROUPE\s|NON[- ]INSCRIT|Mises au point|$)", t[i:]):
        g, n, body = m.group(1).strip(), int(m.group(2)), m.group(3)
        c = {k: int(v) for k, v in re.findall(r'(POUR|CONTRE|ABSTENTIONS?|NON-VOTANTS?)\s*:\s*(\d+)', body)}
        print('   ', g[:60], n, c)
        rows.append({'legislature': leg, 'numero': num, 'url': url, 'entete': head[:300], 'groupe': g[:80], 'effectif': n,
                     'pour': c.get('POUR', 0), 'contre': c.get('CONTRE', 0),
                     'abstention': c.get('ABSTENTION', c.get('ABSTENTIONS', 0)),
                     'non_votant': c.get('NON-VOTANT', c.get('NON-VOTANTS', 0))})
out = os.path.join(os.path.dirname(os.path.abspath(SRC)), 'an_scrutins_archives_detail.csv')
new = not os.path.exists(out)
with open(out, 'a', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';')
    if new: w.writeheader()
    w.writerows(rows)
