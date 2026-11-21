# -*- coding: utf-8 -*-
"""S12 partie B : nombre de ministres dépensiers et variation de la dépense / du solde primaires.
Suit le pré-enregistrement figé (agents/S12_annexe_preenregistrement.md, SHA-256 322e0998...).
Lancer : python -I s12_partieB_tests.py   (numpy, sans pandas)
Entrées (lecture seule) : donnees/S12/sources/datagouv_liste_membres_gouvernements_5e.csv ;
tableau officiel QE 19405 transcrit ci-dessous (pièce donnees/S12/sources/an_QE19405_reponse_membres_gouvernements.pdf) ;
donnees/A09/a09_table_exercices_1975_2025.csv ; donnees/S11/sources/eurostat_nama_10_gdp_FR_CLV_PCH_PRE.json.
Sorties : donnees/S12/s12_partieB_serie.csv, s12_partieB_controle_source.csv, s12_partieB_sortie.txt
"""
import csv, json, math, os, re, datetime as dt
import numpy as np, sys
sys.stdout.reconfigure(encoding="utf-8")

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
D = os.path.join(R, 'donnees')
OUT = os.path.join(D, 'S12')
LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s); LOG.append(s)

# ---------- outils statistiques (repris de scripts/S11/s11_tests.py, méthode identique) ----------
def betainc(a, b, x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2): return front * cf(a, b, x) / a
    return 1 - front * cf(b, a, 1 - x) / b
def cf(a, b, x):
    tiny = 1e-30; c, d = 1.0, 1 - (a + b) * x / (a + 1); d = 1 / (d if abs(d) > tiny else tiny); h = d
    for m in range(1, 300):
        m2 = 2 * m; aa = m * (b - m) * x / ((a + m2 - 1) * (a + m2))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny); c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny; h *= d * c
        aa = -(a + m) * (a + b + m) * x / ((a + m2) * (a + m2 + 1))
        d = 1 + aa * d; d = 1 / (d if abs(d) > tiny else tiny); c = 1 + aa / c if abs(1 + aa / c) > tiny else tiny
        de = d * c; h *= de
        if abs(de - 1) < 1e-12: break
    return h
def t_ppf(p, df):
    def cdf(t):
        x = df / (df + t * t); ib = betainc(df / 2.0, 0.5, x)
        return 1 - 0.5 * ib if t > 0 else 0.5 * ib
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if cdf(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
def ols_multi(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float); n, k = X.shape
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b; s2 = res @ res / (n - k)
    cov = s2 * np.linalg.inv(X.T @ X); se = np.sqrt(np.diag(cov)); tq = t_ppf(0.975, n - k); t80 = t_ppf(0.80, n - k)
    return dict(n=n, b=b, se=se, lo=b - tq * se, hi=b + tq * se, mde80=(tq + t80) * se)
def ols(x, y):
    o = ols_multi(np.column_stack([np.ones(len(x)), x]), y)
    return dict(n=o['n'], pente=o['b'][1], se=o['se'][1], ic_bas=o['lo'][1], ic_haut=o['hi'][1], mde80=o['mde80'][1], r=float(np.corrcoef(x, y)[0, 1]))
def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y)); return float(np.corrcoef(rx, ry)[0, 1])
def power_r(rho, n, z975=1.959964):
    z = abs(math.atanh(rho)) * math.sqrt(n - 3); phi = lambda u: 0.5 * (1 + math.erf(u / math.sqrt(2)))
    return phi(z - z975) + phi(-z - z975)
def perm_p(x, y, n_perm=20000, seed=11):
    rng = np.random.default_rng(seed); x = np.asarray(x, float); y = np.asarray(y, float)
    r0 = abs(np.corrcoef(x, y)[0, 1]); c = sum(abs(np.corrcoef(x, rng.permutation(y))[0, 1]) >= r0 for _ in range(n_perm))
    return (c + 1) / (n_perm + 1)

# ---------- 1. Tableau officiel QE 19405 (JO 25/06/2019, p. 5817) : effectifs à la formation, hors PM ----------
# cle : (id data.gouv, date du JO du décret, total, ministres d'État, ministres (y c. auprès), ministres délégués, secrétaires d'État)
OFF = [
 ('511', '1974-05-28', 36, 1, 14, 0, 21), ('512', '1976-08-26', 35, 3, 13, 1, 18), ('513', '1977-03-30', 39, 0, 13, 1, 25),
 ('514', '1978-04-04', 37, 0, 19, 0, 18), ('515', '1981-05-22', 42, 5, 19, 6, 12), ('516', '1981-06-23', 43, 5, 21, 8, 9),
 ('517', '1983-03-23', 42, 0, 14, 8, 20), ('518', '1984-07-18', 42, 1, 15, 6, 20), ('519', '1986-03-21', 37, 1, 13, 8, 15),
 ('520', '1988-05-11', 41, 4, 14, 8, 15), ('521', '1988-06-24', 49, 4, 17, 11, 17), ('522', '1991-05-16', 45, 5, 14, 10, 16),
 ('523', '1992-04-03', 41, 3, 17, 6, 15), ('524', '1993-03-30', 29, 4, 19, 6, 0), ('525', '1995-05-18', 42, 0, 26, 2, 14),
 ('526', '1995-11-08', 32, 0, 16, 11, 5), ('527', '1997-06-03', 26, 0, 14, 2, 10), ('528', '2002-05-07', 27, 0, 15, 6, 6),
 ('529', '2002-06-18', 38, 0, 15, 11, 12), ('530', '2004-03-31', 43, 1, 16, 13, 13), ('531', '2005-06-01', 31, 1, 15, 15, 0),
 ('532', '2007-05-19', 20, 1, 14, 0, 5), ('533', '2007-06-19', 31, 1, 14, 0, 16), ('534', '2010-11-16', 30, 2, 20, 0, 8),
 ('535', '2012-05-16', 34, 0, 18, 16, 0), ('536', '2012-06-19', 38, 0, 20, 18, 0), ('537', '2014-04-01', 30, 0, 16, 0, 14),
 ('538', '2014-08-26', 33, 0, 16, 0, 17), ('539', '2016-12-07', 37, 0, 17, 0, 20), ('540', '2017-05-16', 22, 3, 15, 0, 4),
 ('541', '2017-06-22', 29, 2, 17, 0, 10),
]
OFF_PHILIPPE_MAI2019 = (35, 1, 19, 0, 15)  # « effectifs au 27 mai 2019 »
D = os.path.join(R, 'donnees')
MOIS = {m: i + 1 for i, m in enumerate(['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'])}
def pdate(s):
    s = (s or '').strip().lower().replace('1er', '1')
    m = re.search(r'(\d{1,2})\s+([a-zéû]+)\s+(\d{4})', s)
    return dt.date(int(m.group(3)), MOIS[m.group(2)], int(m.group(1))) if m else None

rows = list(csv.DictReader(open(os.path.join(OUT, 'sources', 'datagouv_liste_membres_gouvernements_5e.csv'), encoding='utf-8-sig'), delimiter=';'))
for r in rows:
    r['d0'] = pdate(r['date_debut_fonction']); r['d1'] = pdate(r['date_fin_fonction'])
GOV = {}
for r in rows:
    GOV.setdefault(r['id'], {'nom': r['gouvernement'], 'm': []})['m'].append(r)
for g in GOV.values():
    pm = [x['d0'] for x in g['m'] if x['code_fonction'] == 'PM' and x['d0']]
    g['debut'] = min(pm) if pm else min(x['d0'] for x in g['m'] if x['d0'])  # Barnier, Bayrou : pas de ligne PM dans le fichier
    g['n_lignes'] = len(g['m'])
order = sorted(GOV, key=lambda k: GOV[k]['debut'])
FIN = re.compile(r'(?i)(économie|economie|finances|budget|comptes publics)')
def actifs(gid, d, codes, excl_fin=False):
    n = 0
    for x in GOV[gid]['m']:
        if x['code_fonction'] in codes and x['d0'] and x['d0'] <= d and (x['d1'] is None or x['d1'] > d):
            if excl_fin and FIN.search(x['fonction']): continue
            n += 1
    return n

# ---------- 2. Contrôle de la source secondaire (pré-enregistrement § 4) ----------
log('code_fonction présents :', sorted(set(r['code_fonction'] for r in rows)))
ctrl = []; ecarts = 0
for gid, djo, tot, me, mi, md, se in OFF:
    d0 = GOV[gid]['debut'] + dt.timedelta(days=2)  # lendemain du décret de composition (marge de 2 jours)
    v = actifs(gid, d0, {'ME', 'M'}); vt = actifs(gid, d0, {'ME', 'M', 'MD', 'SE', 'HC', 'MC'})
    e = v - (me + mi); ecarts += abs(e) > 1
    ctrl.append(dict(id=gid, gouvernement=GOV[gid]['nom'], jo=djo, debut_datagouv=GOV[gid]['debut'], off_ME_M=me + mi, datagouv_ME_M=v, ecart=e, off_total=tot, datagouv_total=vt))
log('Contrôle data.gouv / pièce officielle : %d gouvernements, écart |ME+M| > 1 : %d (%.0f %%)' % (len(ctrl), ecarts, 100 * ecarts / len(ctrl)))
for c in ctrl: log('   %s %-28s off=%2d datagouv=%2d écart=%+d | total off=%2d dg=%2d' % (c['id'], c['gouvernement'], c['off_ME_M'], c['datagouv_ME_M'], c['ecart'], c['off_total'], c['datagouv_total']))
X3_OK = ecarts / len(ctrl) <= 0.20
log('Variante X3 retenue (règle § 4) :', X3_OK)
with open(os.path.join(OUT, 's12_partieB_controle_source.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(ctrl[0].keys()), delimiter=';'); w.writeheader(); w.writerows(ctrl)

# ---------- 3. Série des 51 exercices ----------
VOTE = {1975: '1974-11-20', 1976: '1975-11-19', 1977: '1976-11-20', 1978: '1977-11-18', 1987: '1986-11-14', 1988: '1987-11-13',
        2007: '2006-11-21', 2011: '2010-11-17', 2012: '2011-11-16', 2013: '2012-11-20', 2014: '2013-11-19', 2015: '2014-11-18',
        2016: '2015-11-17', 2017: '2016-11-22', 2025: '2025-02-05'}
def vdate(y):
    return dt.date.fromisoformat(VOTE[y]) if y in VOTE else dt.date(y - 1, 11, 20)
def gov_at(d):
    g = None
    for k in order:
        if GOV[k]['debut'] <= d: g = k
    return g
OFFD = {o[0]: o for o in OFF}
a09 = {int(r['exercice']): r for r in csv.DictReader(open(os.path.join(D, 'A09', 'a09_table_exercices_1975_2025.csv'), encoding='utf-8'), delimiter=';')}
g = json.load(open(os.path.join(D, 'S11', 'sources', 'eurostat_nama_10_gdp_FR_CLV_PCH_PRE.json'), encoding='utf-8'))
tix = g['dimension']['time']['category']['index']; gdp = {int(y): float(g['value'][str(i)]) for y, i in tix.items() if str(i) in g['value']}
neg = sorted(y for y, v in gdp.items() if v < 0); crise = set(neg) | {y + 1 for y in neg}
log('Années de récession (Eurostat, pièce S11) :', neg, '; exclues avec l\'année suivante :', sorted(crise))

serie = []; prev = None
for y in range(1975, 2026):
    d = vdate(y); gid = gov_at(d)
    if gid in OFFD:
        _, djo, tot, me, mi, md, se = OFFD[gid]
        if gid == '541' and d >= dt.date(2019, 5, 27):
            tot, me, mi, md, se = OFF_PHILIPPE_MAI2019; src = 'officiel (effectifs 27/05/2019)'
        else: src = 'officiel (formation)'
        x1 = me + mi - 1; x2 = tot - 1
    else:
        # data.gouv fusionne Borne 1 (mai 2022) et Borne 2 (4 juillet 2022) : formation retenue = dernière nomination
        # du Premier ministre avant le vote (règle de rattachement du pré-enregistrement). Corrige un premier codage
        # (lot d'entrées le plus nombreux, qui désignait Borne 1) : correction signalée dans S12.md.
        pm = [x['d0'] for x in GOV[gid]['m'] if x['code_fonction'] == 'PM' and x['d0'] and x['d0'] <= d]
        d0 = max(pm) if pm else GOV[gid]['debut']
        dd = d0 + dt.timedelta(days=2)
        x1 = actifs(gid, dd, {'ME', 'M'}) - 1; x2 = actifs(gid, dd, {'ME', 'M', 'MD', 'SE', 'HC', 'MC'}) - 1
        src = 'data.gouv [S] (formation %s)' % d0
    x3 = actifs(gid, d, {'ME', 'M'}, excl_fin=True)
    nouveau = int(prev is not None and gid != prev); prev = gid
    serie.append(dict(exercice=y, date_vote=d, gouvernement=GOV[gid]['nom'], source_X1=src, X1=x1, X2=x2, X3=x3,
                      d_dep_prim=float(a09[y]['d_depenses_primaires']), d_solde_prim=float(a09[y]['d_solde_primaire']),
                      recession=int(y in neg), crise_ou_suivante=int(y in crise), premier_exercice_gouv=nouveau,
                      pre_electoral=int(a09[y]['annee_pre_electorale'])))
with open(os.path.join(OUT, 's12_partieB_serie.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(serie[0].keys()), delimiter=';'); w.writeheader(); w.writerows(serie)

# ---------- 4. Tests pré-enregistrés ----------
A = lambda k, s=serie: np.array([r[k] for r in s], float)
X1 = A('X1'); Y1 = A('d_dep_prim'); Y2 = A('d_solde_prim')
log('\nX1 : min %d, max %d, moyenne %.1f, écart-type %.2f ; Y1 écart-type %.2f ; Y2 écart-type %.2f' % (X1.min(), X1.max(), X1.mean(), X1.std(ddof=1), Y1.std(ddof=1), Y2.std(ddof=1)))
r_eq = 0.05 * X1.std(ddof=1) / Y1.std(ddof=1)
ngov = len(set(r['gouvernement'] for r in serie))
log('Puissance (bilatérale, 5 %%) : r=0,3 n=51 -> %.2f ; r=0,3 n=%d gouvernements -> %.2f' % (power_r(0.3, 51), ngov, power_r(0.3, ngov)))
log('Effet minimal +0,05 pt/ministre <=> r équivalent = %.3f ; puissance n=51 -> %.2f ; n=%d -> %.2f' % (r_eq, power_r(r_eq, 51), ngov, power_r(r_eq, ngov)))
def rep(lab, x, y):
    o = ols(x, y)
    log('%-55s n=%2d pente=%+.4f IC95=[%+.4f ; %+.4f] MDE80=%.4f r=%+.3f Spearman=%+.3f p_perm=%.3f' % (lab, o['n'], o['pente'], o['ic_bas'], o['ic_haut'], o['mde80'], o['r'], spearman(x, y), perm_p(x, y)))
    return o
log('\n--- Test principal ---')
o1 = rep('Y1 (Δ dépense primaire) ~ X1', X1, Y1)
o2 = rep('Y2 (Δ solde primaire) ~ X1', X1, Y2)
log('\n--- Contrôle (a) hors récessions et années suivantes ---')
s_a = [r for r in serie if not r['crise_ou_suivante']]
oa1 = rep('Y1 ~ X1 hors crise', A('X1', s_a), A('d_dep_prim', s_a)); oa2 = rep('Y2 ~ X1 hors crise', A('X1', s_a), A('d_solde_prim', s_a))
log('\n--- Contrôle (b) régression multiple : X1 + récession + premier exercice du gouvernement + pré-électoral ---')
Xm = np.column_stack([np.ones(51), X1, A('recession'), A('premier_exercice_gouv'), A('pre_electoral')])
for lab, y in (('Y1', Y1), ('Y2', Y2)):
    o = ols_multi(Xm, y)
    log('%s : pente X1=%+.4f IC95=[%+.4f ; %+.4f] ; récession=%+.2f ; premier=%+.2f ; pré-élect.=%+.2f' % (lab, o['b'][1], o['lo'][1], o['hi'][1], o['b'][2], o['b'][3], o['b'][4]))
log('\n--- Contrôle (c) variantes de mesure ---')
rep('Y1 ~ X2 (tous les membres)', A('X2'), Y1); rep('Y2 ~ X2', A('X2'), Y2)
if X3_OK:
    rep('Y1 ~ X3 (à la date du vote, data.gouv [S])', A('X3'), Y1); rep('Y2 ~ X3', A('X3'), Y2)
log('\n--- Contrôle (d) un point par gouvernement (moyenne des exercices) ---')
gg = {}
for r in serie: gg.setdefault(r['gouvernement'], []).append(r)
xs = np.array([v[0]['X1'] for v in gg.values()], float)
od1 = rep('Y1 moyen ~ X1, par gouvernement', xs, np.array([np.mean([r['d_dep_prim'] for r in v]) for v in gg.values()]))
od2 = rep('Y2 moyen ~ X1, par gouvernement', xs, np.array([np.mean([r['d_solde_prim'] for r in v]) for v in gg.values()]))

# ---------- 5. Règle de décision figée ----------
MIN = 0.05
def verdict(o, od, oa, sign=+1):
    p, lo, hi = sign * o['pente'], *(sorted([sign * o['ic_bas'], sign * o['ic_haut']]))
    pd_, lod, hid = sign * od['pente'], *(sorted([sign * od['ic_bas'], sign * od['ic_haut']]))
    if p > 0 and lo > 0 and p >= MIN and sign * oa['pente'] > 0 and pd_ > 0: return 'soutenu'
    if (hi < MIN or (p < 0 and hi < 0)) and (hid < MIN or (pd_ < 0 and hid < 0)): return 'contredit'
    return 'ni l\'un ni l\'autre'
v1 = verdict(o1, od1, oa1, +1); v2 = verdict(o2, od2, oa2, -1)
log('\nVERDICT (règle figée) : dépense (Y1) -> %s ; solde (Y2, recoupement) -> %s' % (v1, v2))

# ---------- 6. Ajouté après gel (post hoc, signalé) : taille en début / fin de mandat ----------
log('\n--- POST HOC (ajouté après gel) : écart entre effectif au vote (X3) et à la formation (X1) ---')
gap = A('X3') - X1
log('écart X3 - X1 : moyenne %+.2f, min %+d, max %+d' % (gap.mean(), gap.min(), gap.max()))
o = ols_multi(np.column_stack([np.ones(51), X1, gap]), Y1)
log('Y1 ~ X1 + (X3-X1) : pente X1=%+.4f IC95=[%+.4f ; %+.4f] ; pente écart=%+.4f IC95=[%+.4f ; %+.4f]' % (o['b'][1], o['lo'][1], o['hi'][1], o['b'][2], o['lo'][2], o['hi'][2]))
log('\n--- POST HOC : sans les exercices 2021-2025 (gouvernements mesurés sur data.gouv [S]) et sans 1996 (Juppé 2 formé le 7/11/1995) ---')
s_b = [r for r in serie if r['exercice'] < 2021]
rep('Y1 ~ X1, 1975-2020', A('X1', s_b), A('d_dep_prim', s_b))
s_c = [r for r in serie if r['exercice'] != 1996]
rep('Y1 ~ X1, sans 1996', A('X1', s_c), A('d_dep_prim', s_c))
open(os.path.join(OUT, 's12_partieB_sortie.txt'), 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')
