# -*- coding: utf-8 -*-
"""A08 - Travail n. 8 : les exercices d'annee electorale different-ils des autres ?
Entrees (lecture seule) : base commune Insee (solde) ; A02_series_1960_2000.csv et table_annuelle_A03.csv
(solde primaire corrige du cycle AMECO, estimations Commission millesime 2026, niveau D).
Annees d'election nationale (presidentielle ou legislatives generales) : liste saisie, a verifier (voir dossier).
Sortie : donnees/A08/A08_calendrier_electoral.txt
Usage : python -I calendrier_electoral_A08.py
"""
import csv
import math
import pathlib
import statistics as st

R = pathlib.Path(__file__).resolve().parents[2]
D = R / 'donnees'

solde = {}
with (D / 'commun' / 'base_insee_dep_rec_pctPIB.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        if r['serie'].startswith('Déficit au sens de Maastricht'):
            solde[int(r['annee'])] = float(r['valeur'])


def num(x):
    x = (x or '').strip().replace(',', '.')
    try:
        return float(x)
    except ValueError:
        return None


pcab = {}
with (D / 'A02' / 'A02_series_1960_2000.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        pcab[int(r['annee'])] = num(r['solde_primaire_cvs_ameco'])
with (D / 'A03' / 'table_annuelle_A03.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        v = num(r['ameco_primaire_CA_pct'])
        if v is not None:
            pcab[int(r['annee'])] = v

# Elections nationales generales 1975-2025 [M : liste a verifier ; A08 n'a pas relu chaque date sur piece]
PRES = {1981, 1988, 1995, 2002, 2007, 2012, 2017, 2022}
LEGIS_SEULES = {1978, 1986, 1993, 1997, 2024}
ELEC = PRES | LEGIS_SEULES


def diff(series, a):
    return None if a not in series or a - 1 not in series or series[a] is None or series[a - 1] is None else series[a] - series[a - 1]


def welch(x, y):
    mx, my = st.mean(x), st.mean(y)
    vx, vy = st.variance(x), st.variance(y)
    return (mx - my) / math.sqrt(vx / len(x) + vy / len(y))


lines = []
for nom, ser in [('solde effectif (Insee base 2020)', solde), ('solde primaire corrige du cycle (AMECO)', pcab)]:
    for lib, groupe in [('annee d election (toutes)', ELEC), ('annee de presidentielle', PRES),
                        ('annee precedant une election', {a - 1 for a in ELEC})]:
        ans = [a for a in range(1976, 2026)]
        x = [diff(ser, a) for a in ans if a in groupe and diff(ser, a) is not None]
        y = [diff(ser, a) for a in ans if a not in groupe and diff(ser, a) is not None]
        y_hc = [diff(ser, a) for a in ans if a not in groupe and a not in {2009, 2020, 2021} and diff(ser, a) is not None]
        x_hc = [diff(ser, a) for a in ans if a in groupe and a not in {2009, 2020, 2021} and diff(ser, a) is not None]
        lines.append(f'{nom} | {lib} | variation moyenne {st.mean(x):+.2f} (n={len(x)}) contre {st.mean(y):+.2f} (n={len(y)}) '
                     f'| t Welch {welch(x, y):+.2f} | hors 2009, 2020, 2021 : {st.mean(x_hc):+.2f} contre {st.mean(y_hc):+.2f}, '
                     f't {welch(x_hc, y_hc):+.2f}')
    det = ', '.join(f'{a}:{diff(ser, a):+.2f}' for a in sorted(ELEC) if diff(ser, a) is not None)
    lines.append(f'{nom} | detail des annees d election : {det}')

# erreurs de prevision en h=0 / h=1 par annee cible (table A08)
err = {}
with (D / 'A08' / 'A08_programme_vs_execute.csv').open(encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        e = num(r['ecart_solde_base2020'])
        if e is not None and r['horizon'] in ('0', '1'):
            err.setdefault((int(r['annee_cible']), r['horizon']), []).append(e)
for h in ('0', '1'):
    x = [st.mean(v) for (a, hh), v in err.items() if hh == h and a in ELEC and a not in {2009, 2020, 2021}]
    y = [st.mean(v) for (a, hh), v in err.items() if hh == h and a not in ELEC and a not in {2008, 2009, 2010, 2020, 2021}]
    lines.append(f'Ecart execute - programme, h={h}, annees cibles electorales hors crises : {st.mean(x):+.2f} (n={len(x)}) '
                 f'contre autres hors crises {st.mean(y):+.2f} (n={len(y)}) ; t Welch {welch(x, y):+.2f}')

out = D / 'A08' / 'A08_calendrier_electoral.txt'
out.write_text('A08 - calendrier electoral (variation annuelle en points de PIB ; + = amelioration)\n' + '\n'.join(lines) + '\n', encoding='utf-8')
print('\n'.join(lines))
