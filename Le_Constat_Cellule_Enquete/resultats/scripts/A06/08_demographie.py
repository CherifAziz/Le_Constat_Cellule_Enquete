# A06 - Fécondité, espérance de vie, structure par âge (Eurostat demo_find, demo_mlexpec, demo_pjanind ; extraction 20/11/2026)
# Usage : python -I -X utf8 08_demographie.py <racine_resultats>
import sys, csv, os, collections
R = sys.argv[1]; E = os.path.join(R, 'donnees/A06/eurostat')
def load(f):
    d = collections.defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(E, f), encoding='utf-8'), delimiter=';'):
        key = tuple(r[k] for k in r if k not in ('time', 'value', 'status', 'freq', 'unit'))
        d[key][r['time']] = r['value']
    return d
out = []
YRS = ('1975', '1990', '2000', '2010', '2019', '2023', '2024', '2025')
for f in ('demo_find.csv', 'demo_mlexpec.csv', 'demo_pjanind.csv'):
    d = load(f)
    out.append('== ' + f)
    for k in sorted(d):
        if k[-1] in ('FR', 'DE', 'SE', 'IT', 'EU27_2020'):
            out.append(' '.join(k) + ' : ' + ' '.join(f'{y}={d[k].get(y, "nd")}' for y in YRS))
open(os.path.join(R, 'donnees/A06/resultats_08_demographie.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
