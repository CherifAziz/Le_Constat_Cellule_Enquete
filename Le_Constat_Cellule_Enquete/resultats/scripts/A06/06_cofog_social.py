# A06 - Dépenses COFOG (base commune Eurostat gov_10a_exp, extraction 20/11/2026, lecture seule) : vieillesse, chômage, santé, maladie-invalidité
# Usage : python -I 06_cofog_social.py <racine_resultats>
import sys, csv, os, collections
R = sys.argv[1]
d = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(R, 'donnees/commun/eurostat_gov_10a_exp.csv'), encoding='utf-8-sig')):
    if r['unit'] == 'PC_GDP' and r['sector'] == 'S13' and r['na_item'] == 'TE' and r['value']:
        d[(r['cofog99'], r['geo'])][r['time']] = float(r['value'])
F = {'GF1002': 'vieillesse', 'GF1005': 'chomage', 'GF07': 'sante', 'GF1001': 'maladie-invalidite', 'GF10': 'protection sociale', 'TOTAL': 'total'}
out = []
for code, lab in F.items():
    out.append(f'== {code} {lab} (% PIB) ==')
    for g in ['FR', 'DE', 'NL', 'SE', 'IT', 'ES', 'EA20']:
        s = d.get((code, g), {})
        out.append(g + ' ' + ' '.join(f"{y}:{s.get(y,'nd')}" for y in ('1995', '2000', '2007', '2010', '2015', '2019', '2022', '2023', '2024')))
open(os.path.join(R, 'donnees/A06/resultats_06_cofog_social.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
