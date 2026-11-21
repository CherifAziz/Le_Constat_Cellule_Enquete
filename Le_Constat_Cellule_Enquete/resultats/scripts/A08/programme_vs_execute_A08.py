# -*- coding: utf-8 -*-
"""A08 - Programme contre execute (travail n. 2).
Entrees (lecture seule) :
  donnees/A08/A08_trajectoires_programmees.csv          (vintages saisis, script vintages_A08.py)
  donnees/commun/base_insee_dep_rec_pctPIB.csv          (Insee base 2020, solde et depenses en % du PIB)
  donnees/A02/A02_series_1960_2000.csv                  (croissance du PIB en volume 1998-2000, piece d'A02)
  donnees/A03/table_annuelle_A03.csv                    (croissance du PIB en volume 2000-2025, Eurostat, piece d'A03)
Sorties :
  donnees/A08/A08_programme_vs_execute.csv   (une ligne par document x annee cible, ecarts)
  donnees/A08/A08_stats_par_horizon.csv      (moyennes, signes, tests)
  donnees/A08/A08_retour_sous_3_et_equilibre.csv
  donnees/A08/A08_sortie_tests.txt
Convention : ecart = execute - programme (en points de PIB) ; ecart < 0 = execution PIRE que le programme.
Horizon h : annee cible - annee de reference, l'annee de reference etant l'annee de publication si le
document parait avant septembre, l'annee suivante sinon (un programme de decembre N vise N+1 en h=0, comme une LFI).
Usage : python -I programme_vs_execute_A08.py
"""
import csv
import math
import pathlib
import statistics as st

R = pathlib.Path(__file__).resolve().parents[2]
D = R / 'donnees'
OUTD = D / 'A08'


def num(x):
    x = (x or '').strip().replace(',', '.')
    return float(x) if x not in ('', 'indisponible', 'NA') else None


# --- execution : Insee base 2020 (base commune)
solde, dep = {}, {}
with (D / 'commun' / 'base_insee_dep_rec_pctPIB.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        a = int(r['annee'])
        if r['serie'].startswith('Déficit au sens de Maastricht'):
            solde[a] = float(r['valeur'])
        elif r['serie'] == 'Dépenses':
            dep[a] = float(r['valeur'])

# --- croissance realisee (millesime actuel)
gr = {}
with (D / 'A02' / 'A02_series_1960_2000.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        gr[int(r['annee'])] = num(r['pib_vol_pct'])
with (D / 'A03' / 'table_annuelle_A03.csv').open(encoding='utf-8-sig') as f:
    for r in csv.DictReader(f, delimiter=';'):
        gr[int(r['annee'])] = num(r['croiss_vol_pct'])

# --- solde "d'epoque" (tel que publie peu apres l'exercice), pieces consultees par A08
#     1999-2007 : Senat l08-078 (etat des comptes connu en 2008, base 2000) ;
#     autres : premiere publication citee dans les pieces (HCFP note 2024-2, Senat).
epoque = {1999: -1.8, 2000: -1.5, 2001: -1.6, 2002: -3.2, 2003: -4.1, 2004: -3.6, 2005: -3.0, 2006: -2.4,
          2007: -2.7, 2013: -4.3, 2015: -3.5, 2017: -2.6, 2018: -2.5, 2019: -3.0, 2020: -9.2, 2022: -4.7,
          2023: -5.5, 2024: -5.8}
src_epoque = {**{a: 'Senat l08-078 (2008)' for a in range(1999, 2008)},
              2013: 'Senat r13-483 (Insee 31/3/2014)', 2015: 'Senat r15-550 (Insee 25/3/2016)',
              2017: 'Senat r17-438', 2018: 'Senat r18-468', 2019: 'HCFP note 2024-2 p.27',
              2020: 'Senat r20-555', 2022: 'HCFP note 2024-2 p.20', 2023: 'HCFP note 2024-2 p.20',
              2024: 'Senat r24-567'}

# Procedures de deficit excessif (dates : A03, F-A03-024, page Commission) : ouverture -> abrogation, en annees decimales
PDE = [(2003 + 5.0 / 12, 2007 + 0.5 / 12), (2009 + 3.0 / 12, 2018 + 5.5 / 12), (2024 + 6.5 / 12, 2100)]
rows = []
with (OUTD / 'A08_trajectoires_programmees.csv').open(encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter=';'):
        y, m = map(int, r['date_publication'].split('-'))
        ref = y + 1 if m >= 9 else y
        a = int(r['annee_cible'])
        h = a - ref
        sp = num(r['solde_programme_pctPIB'])
        gp = num(r['croissance_reelle_programme_pct'])
        dp = num(r['depense_programme_pctPIB'])
        se = solde.get(a)
        fen = set(range(y, a + 1))
        pub = y + (m - 0.5) / 12
        pde = any(d0 <= pub < d1 for d0, d1 in PDE)
        rows.append({
            'id_document': r['id_document'], 'type': r['type'], 'date_publication': r['date_publication'],
            'annee_cible': a, 'horizon': h,
            'solde_programme': sp, 'solde_execute_base2020': se,
            'ecart_solde_base2020': None if se is None or sp is None else round(se - sp, 2),
            'solde_execute_epoque': epoque.get(a), 'source_epoque': src_epoque.get(a, ''),
            'ecart_solde_epoque': None if a not in epoque or sp is None else round(epoque[a] - sp, 2),
            'croissance_programme': gp, 'croissance_realisee': gr.get(a),
            'ecart_croissance': None if gp is None or gr.get(a) is None else round(gr[a] - gp, 2),
            'depense_programme': dp, 'depense_executee_base2020': dep.get(a),
            'ecart_depense': None if dp is None or a not in dep else round(dep[a] - dp, 2),
            'fenetre_touche_crise': int(bool(fen & {2008, 2009, 2010, 2020, 2021})),
            'PDE_ouverte_a_publication': int(pde),
        })


def fmt(x):
    if x is None:
        return ''
    return str(x).replace('.', ',') if isinstance(x, float) else str(x)


with (OUTD / 'A08_programme_vs_execute.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(list(rows[0].keys()))
    for r in rows:
        w.writerow([fmt(v) for v in r.values()])

CRISES_ETROITES = {2009, 2020}
CRISES_LARGES = {2008, 2009, 2010, 2020, 2021}


def tstat(xs):
    if len(xs) < 3:
        return None
    s = st.stdev(xs)
    return None if s == 0 else st.mean(xs) / (s / math.sqrt(len(xs)))


def resume(sel, key):
    xs = [r[key] for r in sel if r[key] is not None]
    if not xs:
        return None
    # agregation par annee cible (les erreurs d'une meme annee cible sont correlees entre documents)
    par_annee = {}
    for r in sel:
        if r[key] is not None:
            par_annee.setdefault(r['annee_cible'], []).append(r[key])
    moy_annee = [st.mean(v) for v in par_annee.values()]
    return {
        'n': len(xs), 'n_annees': len(moy_annee), 'moyenne': round(st.mean(xs), 2),
        'mediane': round(st.median(xs), 2), 'part_pire': round(sum(1 for x in xs if x < 0) / len(xs), 2),
        't_naif': None if tstat(xs) is None else round(tstat(xs), 2),
        'moyenne_par_annee': round(st.mean(moy_annee), 2),
        't_par_annee': None if tstat(moy_annee) is None else round(tstat(moy_annee), 2),
    }


lignes = []
out = []
for key, lib in [('ecart_solde_base2020', 'solde (execution base 2020)'),
                 ('ecart_solde_epoque', 'solde (execution d epoque)'),
                 ('ecart_croissance', 'croissance reelle'),
                 ('ecart_depense', 'depense en % du PIB')]:
    for periode, filt in [('1999-2025', lambda r: True),
                          ('1999-2007', lambda r: r['annee_cible'] <= 2007),
                          ('2008-2025', lambda r: r['annee_cible'] >= 2008)]:
        for excl_lib, excl in [('toutes annees', set()), ('hors 2009 et 2020', CRISES_ETROITES),
                               ('hors 2008-2010 et 2020-2021', CRISES_LARGES),
                               ('hors fenetres touchant 2008-2010 ou 2020-2021', 'FEN'),
                               ('hors fenetres de crise, PDE ouverte', 'PDE1'),
                               ('hors fenetres de crise, pas de PDE', 'PDE0')]:
            for h in [0, 1, 2, 3, 4]:
                def ok(r):
                    if excl == 'FEN':
                        return not r['fenetre_touche_crise']
                    if excl in ('PDE1', 'PDE0'):
                        return (not r['fenetre_touche_crise']) and r['PDE_ouverte_a_publication'] == (excl == 'PDE1')
                    return r['annee_cible'] not in excl
                sel = [r for r in rows if filt(r) and ok(r) and
                       (r['horizon'] == h if h < 4 else r['horizon'] >= 4) and r['annee_cible'] <= 2025]
                res = resume(sel, key)
                if res:
                    lignes.append([lib, periode, excl_lib, h if h < 4 else '4+'] + list(res.values()))

with (OUTD / 'A08_stats_par_horizon.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['variable', 'periode_annees_cibles', 'exclusion', 'horizon', 'n', 'n_annees_cibles',
                'ecart_moyen', 'ecart_median', 'part_execution_pire', 't_naif', 'ecart_moyen_par_annee_cible',
                't_par_annee_cible'])
    for l in lignes:
        w.writerow([fmt(v) for v in l])

# --- persistance : annee annoncee de retour sous 3 % et a l'equilibre (|solde| <= 0,05)
pers = []
docs = {}
for r in rows:
    docs.setdefault(r['id_document'], []).append(r)
for i, rs in docs.items():
    rs.sort(key=lambda r: r['annee_cible'])
    sous3 = next((r['annee_cible'] for r in rs if r['solde_programme'] is not None and r['solde_programme'] > -3.0), None)
    equi = next((r['annee_cible'] for r in rs if r['solde_programme'] is not None and r['solde_programme'] >= -0.05), None)
    fin = rs[-1]
    s3e = solde.get(sous3) if sous3 else None
    s3p = epoque.get(sous3) if sous3 else None
    pers.append([i, rs[0]['date_publication'], fin['annee_cible'], fin['solde_programme'], sous3 or '', equi or '',
                 fin['solde_execute_base2020'] if fin['solde_execute_base2020'] is not None else '',
                 '' if s3e is None else s3e, '' if s3p is None else s3p,
                 '' if s3e is None else ('oui' if s3e > -3.0 else 'non'),
                 '' if s3p is None else ('oui' if s3p > -3.0 else 'non')])
with (OUTD / 'A08_retour_sous_3_et_equilibre.csv').open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['id_document', 'date_publication', 'derniere_annee', 'solde_programme_derniere_annee',
                'premiere_annee_annoncee_sous_3pct', 'premiere_annee_annoncee_a_l_equilibre',
                'solde_execute_derniere_annee_base2020', 'solde_execute_annee_sous3_base2020',
                'solde_execute_annee_sous3_epoque', 'sous_3_tenu_base2020', 'sous_3_tenu_epoque'])
    for p in pers:
        w.writerow([fmt(v) for v in p])

# --- ameliorations promises contre obtenues (h=0 -> h=3)
amel = []
for i, rs in docs.items():
    d = {r['horizon']: r for r in rs}
    if 0 in d and 3 in d and d[3]['solde_execute_base2020'] is not None and d[0]['solde_execute_base2020'] is not None:
        promis = d[3]['solde_programme'] - d[0]['solde_programme']
        obtenu = d[3]['solde_execute_base2020'] - d[0]['solde_execute_base2020']
        amel.append((i, d[0]['annee_cible'], d[3]['annee_cible'], round(promis, 2), round(obtenu, 2),
                     d[0]['PDE_ouverte_a_publication'], d[3]['fenetre_touche_crise']))

with (OUTD / 'A08_sortie_tests.txt').open('w', encoding='utf-8') as f:
    f.write('A08 - programme contre execute. Ecart = execute - programme ; < 0 = execution pire.\n\n')
    f.write('variable | periode | exclusion | h | n | n annees | moyenne | mediane | part pire | t naif | moy. par annee | t par annee\n')
    for l in lignes:
        f.write(' | '.join(str(v) for v in l) + '\n')
    f.write('\nAmelioration du solde promise entre h=0 et h=3 contre obtenue (base 2020), points de PIB :\n')
    for a in amel:
        f.write(f'{a[0]} ({a[1]}->{a[2]}) : promis {a[3]:+.2f} ; obtenu {a[4]:+.2f}\n')
    if amel:
        f.write(f'Moyenne promise {st.mean([a[3] for a in amel]):+.2f} ; moyenne obtenue {st.mean([a[4] for a in amel]):+.2f} '
                f'; n = {len(amel)}\n')
        hc = [a for a in amel if not ({a[1], a[2]} & CRISES_LARGES) and not any(y in CRISES_LARGES for y in range(a[1], a[2] + 1))]
        if hc:
            f.write(f'Hors fenetres touchant 2008-2010 et 2020-2021 : promis {st.mean([a[3] for a in hc]):+.2f} ; '
                    f'obtenu {st.mean([a[4] for a in hc]):+.2f} ; n = {len(hc)} ({", ".join(a[0] for a in hc)})\n')
    f.write('\nRetour annonce sous 3 % et a l equilibre :\n')
    for p in pers:
        f.write(' ; '.join(str(v) for v in p) + '\n')
print('ok', len(rows), 'lignes')
