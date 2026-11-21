# A06 - Croissance, emploi, heures, productivité : périodes et décomposition des écarts de niveau.
# Entrées : donnees/A06/ameco_series_A06.csv (AMECO automne 2026), donnees/A06/eurostat/*.csv
# Usage : python -I 03_analyse_croissance.py <racine_resultats>
import sys, csv, math, collections, os

R = sys.argv[1]
A = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(R, 'donnees/A06/ameco_series_A06.csv'), encoding='utf-8'), delimiter=';'):
    A[(r['pays'], r['variable'])][int(r['annee'])] = float(r['valeur'])

def g(c, v, y):
    return A[(c, v)].get(y)

def cagr(c, v, y0, y1):
    a, b = g(c, v, y0), g(c, v, y1)
    if a is None or b is None or a <= 0: return None
    return 100 * ((b / a) ** (1 / (y1 - y0)) - 1)

def ratio(c, num, den, y):
    a, b = g(c, num, y), g(c, den, y)
    return None if a is None or b is None or b == 0 else a / b

out = []
P = lambda *x: out.append(' '.join(str(i) for i in x))
f1 = lambda x: 'n.d.' if x is None else f'{x:.2f}'

# 1. France, croissance annuelle moyenne par période
P('=== 1. FRANCE : taux de croissance annuels moyens (%), AMECO automne 2026 ===')
periods = [(1960, 1974), (1974, 1984), (1984, 1992), (1992, 2000), (2000, 2007), (2007, 2013), (2013, 2019), (2019, 2025), (1974, 2025)]
P('periode | PIB vol | PIB pot | PIB/hab | heures tot | heures/emploi | emploi | prod horaire | prod/emploi | chomage moyen')
for y0, y1 in periods:
    c = 'FRA'
    pop = cagr(c, 'population_cn_milliers', y0, y1)
    gdp = cagr(c, 'pib_volume_2020', y0, y1)
    pot = cagr(c, 'pib_potentiel_2020', max(y0, 1965), y1)
    ht = cagr(c, 'heures_totales_millions', y0, y1)
    he = cagr(c, 'heures_par_emploi', y0, y1)
    em = cagr(c, 'emploi_interieur_milliers', y0, y1)
    ph = None if gdp is None or ht is None else 100 * ((1 + gdp / 100) / (1 + ht / 100) - 1)
    pe = None if gdp is None or em is None else 100 * ((1 + gdp / 100) / (1 + em / 100) - 1)
    gpc = None if gdp is None or pop is None else 100 * ((1 + gdp / 100) / (1 + pop / 100) - 1)
    u = [g(c, 'taux_chomage', y) for y in range(y0 + 1, y1 + 1) if g(c, 'taux_chomage', y) is not None]
    P(f'{y0}-{y1} | {f1(gdp)} | {f1(pot)} | {f1(gpc)} | {f1(ht)} | {f1(he)} | {f1(em)} | {f1(ph)} | {f1(pe)} | {f1(sum(u)/len(u) if u else None)}')

# 2. Comparateurs 1995-2025 et 2019-2025
P('\n=== 2. Comparateurs : croissance annuelle moyenne (%) ===')
for y0, y1 in [(1995, 2007), (2007, 2019), (2019, 2025), (1995, 2025)]:
    P(f'-- {y0}-{y1} -- pays | PIB vol | PIB/hab | prod horaire | heures/hab')
    for c in ['FRA', 'DEU', 'NLD', 'SWE', 'ITA', 'ESP', 'GBR', 'EA20', 'USA']:
        gdp = cagr(c, 'pib_volume_2020', y0, y1)
        pop = cagr(c, 'population_cn_milliers', y0, y1)
        ht = cagr(c, 'heures_totales_millions', y0, y1)
        ph = None if gdp is None or ht is None else 100 * ((1 + gdp / 100) / (1 + ht / 100) - 1)
        hp = None if ht is None or pop is None else 100 * ((1 + ht / 100) / (1 + pop / 100) - 1)
        gpc = None if gdp is None or pop is None else 100 * ((1 + gdp / 100) / (1 + pop / 100) - 1)
        P(f'{c} | {f1(gdp)} | {f1(gpc)} | {f1(ph)} | {f1(hp)}')

# 3. Décomposition des écarts de PIB par habitant (SPA courants)
for Y in (2019, 2024, 2025):
    P(f'\n=== 3. Décomposition log de l\'écart de PIB/hab en SPA, {Y} (écart = pays - France, en % log) ===')
    P('pays | PIB/hab SPA (k) | ecart total | prod horaire | heures/emploi | emploi/pop15-64 | pop15-64/pop | heures/hab')
    def comp(c):
        Y_ = g(c, 'pib_courant_SPA_mrd', Y); N = g(c, 'population_cn_milliers', Y); H = g(c, 'heures_totales_millions', Y)
        E = g(c, 'emploi_interieur_milliers', Y); W = g(c, 'pop_15_64_milliers', Y)
        if None in (Y_, N, H, E, W): return None
        return dict(ypc=Y_ * 1e9 / (N * 1e3), yh=Y_ * 1e9 / (H * 1e6), he=H * 1e6 / (E * 1e3), er=E / W, wr=W / N, hpc=H * 1e6 / (N * 1e3))
    fr = comp('FRA')
    for c in ['FRA', 'DEU', 'NLD', 'SWE', 'DNK', 'BEL', 'ITA', 'ESP', 'GBR', 'USA']:
        x = comp(c)
        if x is None or fr is None:
            P(c, 'données manquantes'); continue
        L = lambda k: 100 * math.log(x[k] / fr[k])
        P(f"{c} | {x['ypc']/1e3:.1f} | {L('ypc'):.1f} | {L('yh'):.1f} | {L('he'):.1f} | {L('er'):.1f} | {L('wr'):.1f} | {L('hpc'):.1f}")
    if fr: P(f"FRA niveaux : PIB/heure SPA {fr['yh']:.1f} ; heures/emploi {fr['he']:.0f} ; emploi/pop15-64 {fr['er']:.3f} ; pop15-64/pop {fr['wr']:.3f}")

# 4. Composante conjoncturelle du solde (AMECO, % du PIB potentiel) : France
P('\n=== 4. France : solde observé, composante conjoncturelle et solde corrigé du cycle (AMECO, %PIB pot.) ===')
P('annee | solde | ecart production | composante conj | solde CVC | solde primaire CVC')
for y in list(range(1974, 2026)) + [2026, 2027]:
    P(f"{y} | {f1(g('FRA','solde_apu_pct_pib',y))} | {f1(g('FRA','ecart_production_pct_pot',y))} | {f1(g('FRA','composante_conj_solde_pct_pibpot',y))} | {f1(g('FRA','solde_cvs_cycle_pct_pibpot',y))} | {f1(g('FRA','solde_primaire_cvs_cycle_pct_pibpot',y))}")
neg = [y for y in range(1975, 2026) if (g('FRA', 'solde_cvs_cycle_pct_pibpot', y) or 0) < 0]
P('Années 1975-2025 avec solde corrigé du cycle négatif :', len(neg), 'sur', len([y for y in range(1975, 2026) if g('FRA', 'solde_cvs_cycle_pct_pibpot', y) is not None]))
cc = [g('FRA', 'composante_conj_solde_pct_pibpot', y) for y in range(1975, 2026) if g('FRA', 'composante_conj_solde_pct_pibpot', y) is not None]
ac = [g('FRA', 'solde_apu_pct_pib', y) for y in range(1975, 2026) if g('FRA', 'solde_apu_pct_pib', y) is not None]
P(f'Moyenne 1975-2025 : solde {sum(ac)/len(ac):.2f} ; composante conjoncturelle {sum(cc)/len(cc):.2f}')

# 5. Industrie, investissement
P('\n=== 5. Part de l\'industrie manufacturière dans la VA (approx. VA manuf./PIB courant, %) et FBCF/PIB (%) ===')
for c in ['FRA', 'DEU', 'ITA', 'ESP', 'NLD', 'SWE', 'EA20']:
    s = []
    for y in (1975, 1990, 2000, 2007, 2019, 2024):
        m = ratio(c, 'va_manufacturier_courant', 'pib_courant_monnaie_nat', y)
        i = ratio(c, 'fbcf_totale_courant', 'pib_courant_monnaie_nat', y)
        s.append(f"{y}: {('n.d.' if m is None else f'{100*m:.1f}')}/{('n.d.' if i is None else f'{100*i:.1f}')}")
    P(c, ' ; '.join(s))

open(os.path.join(R, 'donnees/A06/resultats_03_croissance.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
