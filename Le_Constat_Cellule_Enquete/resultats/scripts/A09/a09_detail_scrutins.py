"""A09 - Télécharge et analyse des pages de scrutin de l'Assemblée nationale (format /dyn/<leg>/scrutins/<n>)
et produit la répartition des votes par groupe.
Usage : python -I a09_detail_scrutins.py <dossier_sortie> <leg>:<num> [<leg>:<num> ...]
Sortie : <dossier_sortie>/an_scrutins_detail.csv (ajout), pages HTML dans <dossier_sortie>/an_scrutins/.
"""
import sys, os, re, csv, time
import requests
from bs4 import BeautifulSoup

OUT = sys.argv[1]
RAW = os.path.join(OUT, 'an_scrutins')
os.makedirs(RAW, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0'}
POS = ('Pour', 'Contre', 'Abstention', 'Non-votant', 'Non-votants')


def fetch(leg, num):
    p = os.path.join(RAW, f'scrutin_{leg}_{num}.html')
    if not os.path.exists(p):
        r = requests.get(f'https://www.assemblee-nationale.fr/dyn/{leg}/scrutins/{num}', headers=UA, timeout=60)
        r.raise_for_status()
        open(p, 'wb').write(r.content)
        time.sleep(0.5)
    return open(p, 'rb').read().decode('utf-8', errors='replace')


def analyse(html):
    s = BeautifulSoup(html, 'html.parser')
    toks = s.get_text('|', strip=True).split('|')
    full = ' '.join(toks)
    m = re.search(r'Scrutin public n.\s?\d+ (.*?) Synth', full)
    objet = m.group(1) if m else ''
    d = re.search(r'(Unique|Premi.re|Deuxi.me|Troisi.me|Quatri.me) s.ance du (\w+ \d+\w* \w+ \d{4})', full)
    date = d.group(2) if d else ''
    synth = re.search(r'Synth.se du vote (.*?) (L.Assembl.e nationale (n.a pas adopt.|a adopt.))', full)
    synthese = (synth.group(1) + ' ' + synth.group(2)) if synth else ''
    groupes = []
    try:
        i0 = toks.index('Répartition des votes par groupe')
    except ValueError:
        i0 = next(i for i, t in enumerate(toks) if t.startswith('R') and 'partition des votes par groupe' in t)
    i = i0 + 1
    cur = None
    while i < len(toks):
        t = toks[i]
        if re.match(r'^\((\d+) membres?\)$', t):
            cur = {'groupe': toks[i - 1], 'membres': int(re.match(r'^\((\d+)', t).group(1))}
            groupes.append(cur)
        elif t in ('Députés non inscrits', 'Non inscrits', 'Non-inscrits'):
            cur = {'groupe': 'Non inscrits', 'membres': 0}   # effectif non affiché sur la page
            groupes.append(cur)
        elif t == 'LCP':
            break
        elif cur is not None and t in POS and i + 1 < len(toks) and re.match(r'^:\s*\d+$', toks[i + 1]):
            cur[t.rstrip('s')] = int(toks[i + 1].split(':')[1])
        elif t.startswith('Mises au point') or t.startswith('Haut de page'):
            break
        i += 1
    # contrôle : la somme des « Pour » et des « Contre » par groupe doit égaler le total annoncé
    controle = []
    m = re.search(r'Pour l.adoption\s*:\s*(\d+)', synthese)
    if m:
        s = sum(g.get('Pour', 0) for g in groupes)
        if s != int(m.group(1)): print(f'   ATTENTION : somme des Pour {s} != total {m.group(1)}', file=sys.stderr); controle.append(f'Pour {s}/{m.group(1)}')
    m = re.search(r'Contre\s*:\s*(\d+)', synthese)
    if m:
        s = sum(g.get('Contre', 0) for g in groupes)
        if s != int(m.group(1)): print(f'   ATTENTION : somme des Contre {s} != total {m.group(1)}', file=sys.stderr); controle.append(f'Contre {s}/{m.group(1)}')
    return objet, date, synthese, groupes, ('ok' if not controle else ' ; '.join(controle))


def main():
    rows = []
    for arg in sys.argv[2:]:
        leg, num = arg.split(':')
        objet, date, synthese, groupes, ctrl = analyse(fetch(leg, num))
        print(f'== {leg}/{num} | {date} | {synthese}\n   {objet[:250]}')
        for g in groupes:
            print('   ', g)
            rows.append({'legislature': leg, 'numero': num, 'date': date, 'objet': objet[:300],
                         'synthese': synthese, 'groupe': g['groupe'], 'membres': g['membres'],
                         'pour': g.get('Pour', 0), 'contre': g.get('Contre', 0),
                         'abstention': g.get('Abstention', 0), 'non_votant': g.get('Non-votant', 0), 'controle_sommes': ctrl})
    p = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'an_scrutins_detail.csv')
    new = not os.path.exists(p)
    with open(p, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';')
        if new:
            w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main()
