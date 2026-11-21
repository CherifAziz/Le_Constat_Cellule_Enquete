"""A09 - Test : la VARIATION du solde primaire (effectif, et corrigé du cycle par AMECO) et celle des
dépenses primaires et des recettes diffèrent-elles selon le type de majorité, la cohabitation, la
proximité d'une élection, l'alternance et la fragmentation ? Exercices 1975-2025.

Entrées (lecture seule) :
 - base commune : insee_cn_t_3201.xlsx (B9NF, D41 versés, total des dépenses en Md€) ;
   base_insee_dep_rec_pctPIB.csv (dépenses et recettes en % du PIB ; PIB nominal reconstitué) ;
 - AMECO, ameco17.zip (millésime du 17/11/2026, retéléchargé par A09) : FRA.1.0.319.0.UBLGBP,
   solde primaire corrigé du cycle en % du PIB potentiel (estimation rétrospective, à partir de 1978) ;
 - a09_composition_majorites.csv : composition de chaque législature sur pièces de l'Assemblée.
Rattachement : l'exercice t appartient à la législature qui a voté sa loi de finances initiale à
l'automne t-1 (variante : législature en place au 1er juillet de t).
Variables non établies sur pièce et marquées [M] : étiquette de camp des groupes (gauche/droite/centre),
cohabitation (couleur politique du président), alternance.
Usage : python -I a09_test_majorites.py <racine_resultats>
"""
import sys, os, csv, random, math, statistics as st
import openpyxl

R = sys.argv[1]
COM = os.path.join(R, 'donnees', 'commun'); OUT = os.path.join(R, 'donnees', 'A09')
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------- 1. Comptes publics ----------
wb = openpyxl.load_workbook(os.path.join(COM, 'insee_cn_t_3201.xlsx'), read_only=True, data_only=True)
rows = list(wb.worksheets[0].iter_rows(values_only=True))
years = [int(x) for x in rows[2][2:] if x is not None]
def line(i): return {y: float(v) for y, v in zip(years, rows[i][2:]) if v is not None}
assert 'Intérêts (D41)' in str(rows[11][1]) and 'Total des dépenses' in str(rows[26][1]) and 'B9NF' in str(rows[65][1])
D41, DEP, B9 = line(11), line(26), line(65)
pct = {}
for r in csv.DictReader(open(os.path.join(COM, 'base_insee_dep_rec_pctPIB.csv'), encoding='utf-8-sig'), delimiter=';'):
    if r['serie'] in ('Dépenses', 'Recettes'):
        pct.setdefault(r['serie'], {})[int(r['annee'])] = float(r['valeur'])
PIB = {y: DEP[y] / pct['Dépenses'][y] * 100 for y in DEP if y in pct['Dépenses']}
solde = {y: B9[y] / PIB[y] * 100 for y in PIB}
prim = {y: (B9[y] + D41[y]) / PIB[y] * 100 for y in PIB}
interets = {y: D41[y] / PIB[y] * 100 for y in PIB}
dep_prim = {y: pct['Dépenses'][y] - interets[y] for y in PIB}
rec = {y: pct['Recettes'][y] for y in PIB}

ameco = {}
for l in open(os.path.join(OUT, 'sources', 'ameco', 'AMECO17.TXT'), encoding='utf-8', errors='replace'):
    if l.startswith('FRA.1.0.319.0.UBLGBP;'):
        p = l.rstrip('\n').split(';')
        for y, v in zip(range(1960, 1960 + len(p) - 5), p[5:]):
            try: ameco[y] = float(v)
            except ValueError: pass

# ---------- 2. Classement politique à partir de la composition sur pièces ----------
comp = {r['legislature']: r for r in csv.DictReader(open(os.path.join(OUT, 'a09_composition_majorites.csv'), encoding='utf-8'), delimiter=';')}
ordre = ['V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII']
debut = {k: int(comp[k]['election_legislative']) for k in ordre}
def leg_vote(t):  # législature en place à l'automne t-1 (toutes les élections ont lieu avant l'automne)
    return [k for k in ordre if debut[k] <= t - 1][-1]
def leg_mid(t):   # législature en place au 1er juillet de t (élections d'avril-juin ; 2024 : juillet, compté en XVII à partir de 2025)
    return [k for k in ordre if debut[k] < t or (debut[k] == t and t != 2024)][-1]
def typ(leg, t_vote):
    ty = comp[leg]['type_majorite']
    if leg == 'XV':  # LREM 314 (2017), 304 (oct. 2019), 271 (oct. 2020) : F-A09-031
        return 'parti_seul' if t_vote <= 2019 else 'coalition'
    return ty
# effectif de groupes (Laakso-Taagepera) sur les sièges des groupes à l'ouverture
def enp(leg):
    seats = []
    for part in comp[leg]['groupes_effectifs'].split('/'):
        toks = part.strip().split()
        nums = [x for x in toks if x.isdigit()]
        if nums: seats.append(int(nums[0]))
    tot = sum(seats); return 1 / sum((s / tot) ** 2 for s in seats)
ENP = {k: enp(k) for k in ordre}

COHAB = set(range(1987, 1989)) | set(range(1994, 1996)) | set(range(1998, 2003))   # [M] couleur du président
PRES = {1974, 1981, 1988, 1995, 2002, 2007, 2012, 2017, 2022}   # data.gouv (début de mandat présidentiel)
LEGI = {debut[k] for k in ordre} | {1981}
ELEC = PRES | LEGI
ALTER = {1982, 1987, 1989, 1994, 1998, 2003, 2013, 2018}                                 # [M] camp
CAMP = {'V': 'droite', 'VI': 'droite', 'VII': 'gauche', 'VIII': 'droite', 'IX': 'gauche', 'X': 'droite', 'XI': 'gauche',
        'XII': 'droite', 'XIII': 'droite', 'XIV': 'gauche', 'XV': 'centre', 'XVI': 'centre', 'XVII': 'centre_minoritaire'}  # [M]

def d(dic, t): return round(dic[t] - dic[t - 1], 3) if t in dic and t - 1 in dic else ''
table = []
for t in range(1975, 2026):
    lv, lm = leg_vote(t), leg_mid(t)
    table.append({'exercice': t, 'legislature_vote_LFI': lv, 'type_majorite': typ(lv, t - 1),
                  'legislature_mi_annee': lm, 'type_majorite_mi_annee': typ(lm, t),
                  'nb_effectif_groupes': round(ENP[lv], 2), 'camp_M': CAMP[lv], 'cohabitation_M': int(t in COHAB),
                  'annee_electorale': int(t in ELEC), 'annee_pre_electorale': int((t + 1) in ELEC and t not in ELEC),
                  'premier_exercice_apres_alternance_M': int(t in ALTER),
                  'solde_pct': round(solde[t], 3), 'solde_primaire_pct': round(prim[t], 3), 'd_solde_primaire': d(prim, t),
                  'd_depenses_primaires': d(dep_prim, t), 'd_recettes': d(rec, t),
                  'spcc_ameco': ameco.get(t, ''), 'd_spcc_ameco': d(ameco, t)})
with open(os.path.join(OUT, 'a09_table_exercices_1975_2025.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(table[0].keys()), delimiter=';'); w.writeheader(); w.writerows(table)

# ---------- 3. Comparaisons ----------
random.seed(20261120)
def perm_p(a, b, n=4000):
    if len(a) < 2 or len(b) < 2: return float('nan')
    obs = abs(st.mean(a) - st.mean(b)); pool = a + b; k = 0
    for _ in range(n):
        random.shuffle(pool)
        if abs(st.mean(pool[:len(a)]) - st.mean(pool[len(a):])) >= obs - 1e-12: k += 1
    return k / n
def mde(a, b):  # plus petite différence détectable (alpha 5 % bilatéral, puissance 80 %), sous indépendance
    if len(a) < 2 or len(b) < 2: return float('nan')
    sd = st.pstdev(a + b); return 2.80 * sd * math.sqrt(1 / len(a) + 1 / len(b))

ABS = {'parti_seul', 'coalition'}; NONABS = {'relative', 'sans_majorite'}; INCERT = {'coalition_non_etablie', 'coalition_etroite'}
VARIANTES = [((), 'toutes années'), ((1975, 1993, 2009, 2010, 2020, 2021), 'hors récessions et rebonds (1975, 1993, 2009, 2010, 2020, 2021)')]
L = []
for var in ['d_solde_primaire', 'd_spcc_ameco', 'd_depenses_primaires', 'd_recettes']:
    for excl, lab in VARIANTES:
        L.append(f'\n### {var} — {lab}')
        for cle in ['type_majorite', 'type_majorite_mi_annee', 'cohabitation_M', 'annee_electorale', 'annee_pre_electorale',
                    'premier_exercice_apres_alternance_M', 'camp_M']:
            g = {}
            for x in table:
                if x[var] == '' or x['exercice'] in excl: continue
                g.setdefault(x[cle], []).append(x[var])
            L.append(f' par {cle}')
            for k in sorted(g, key=str):
                v = g[k]
                L.append(f'   {str(k):24s} n={len(v):2d}  moyenne={st.mean(v):+.2f}  mediane={st.median(v):+.2f}  [{min(v):+.2f} ; {max(v):+.2f}]')
            if cle.startswith('type_majorite'):
                a = [x for k in ABS for x in g.get(k, [])]; b = [x for k in NONABS for x in g.get(k, [])]
                c = a + [x for k in INCERT for x in g.get(k, [])]
                L.append(f'   absolue (seule/coalition) n={len(a)} moy={st.mean(a):+.2f} contre relative/sans n={len(b)} moy={st.mean(b):+.2f} : p={perm_p(a, b):.2f} ; plus petite différence détectable ≈ {mde(a, b):.2f} pt')
                L.append(f'   variante incertains comptés absolus : n={len(c)} moy={st.mean(c):+.2f} ; p={perm_p(c, b):.2f}')
                ps = g.get('parti_seul', []); co = g.get('coalition', [])
                L.append(f'   parti seul n={len(ps)} moy={st.mean(ps):+.2f} contre coalition absolue n={len(co)} moy={st.mean(co):+.2f} : p={perm_p(ps, co):.2f}')
            elif cle != 'camp_M':
                a, b = g.get(1, []), g.get(0, [])
                L.append(f'   1 contre 0 : écart {st.mean(a) - st.mean(b):+.2f} ; p={perm_p(a, b):.2f} ; plus petite différence détectable ≈ {mde(a, b):.2f} pt')
# fragmentation : corrélation de rang simple entre nombre effectif de groupes et variation
def spearman(x, y):
    rx = {v: i for i, v in enumerate(sorted(range(len(x)), key=lambda i: x[i]))}
    ry = {v: i for i, v in enumerate(sorted(range(len(y)), key=lambda i: y[i]))}
    n = len(x); dd = sum((rx[i] - ry[i]) ** 2 for i in range(n)); return 1 - 6 * dd / (n * (n * n - 1))
for var in ['d_solde_primaire', 'd_spcc_ameco']:
    xs = [x for x in table if x[var] != '']
    L.append(f'\n### Fragmentation : rho de Spearman (nombre effectif de groupes, {var}) = {spearman([x["nb_effectif_groupes"] for x in xs], [x[var] for x in xs]):+.2f} (n={len(xs)} ; valeurs du nombre effectif peu nombreuses : 13 législatures)')

# ---------- 4. Par législature ----------
L.append('\n### Par législature (exercices dont la LFI a été votée par la législature)')
L.append('legislature;exercices;type;n;nb_effectif_groupes;primaire_annee_avant;primaire_fin;var_cumulee_primaire;spcc_avant;spcc_fin;var_cumulee_spcc;var_dep_primaires;var_recettes')
par = {}
for x in table: par.setdefault(x['legislature_vote_LFI'], []).append(x)
for leg in ordre:
    ds = par[leg]; a, b = ds[0]['exercice'], ds[-1]['exercice']
    s0, s1 = ameco.get(a - 1), ameco.get(b)
    vs = f'{s1 - s0:+.2f}' if s0 is not None and s1 is not None else 'n.d.'
    L.append(f"{leg};{a}-{b};{'/'.join(sorted(set(x['type_majorite'] for x in ds)))};{len(ds)};{ENP[leg]:.2f};{prim[a - 1]:+.2f};{prim[b]:+.2f};{prim[b] - prim[a - 1]:+.2f};{s0 if s0 is not None else 'n.d.'};{s1};{vs};{dep_prim[b] - dep_prim[a - 1]:+.2f};{rec[b] - rec[a - 1]:+.2f}")

# ---------- 5. Épisodes d'assouplissement (question de la vague 1) ----------
L.append("\n### Années d'assouplissement (variation du solde primaire corrigé du cycle <= -0,5 pt) et contexte")
L.append('exercice;d_spcc;cumul_spcc_3_ans_avant;consolidation_prealable(cumul>+1);legislature_vote;premier_ou_second_exercice_apres_alternance_M;annee_electorale')
for x in table:
    if x['d_spcc_ameco'] != '' and x['d_spcc_ameco'] <= -0.5:
        t = x['exercice']; cum = sum(ameco[u] - ameco[u - 1] for u in range(t - 3, t) if u in ameco and u - 1 in ameco)
        alt = int(t in ALTER or (t - 1) in ALTER)
        L.append(f"{t};{x['d_spcc_ameco']:+.2f};{cum:+.2f};{int(cum > 1)};{x['legislature_vote_LFI']};{alt};{x['annee_electorale']}")
txt = '\n'.join(L)
open(os.path.join(OUT, 'a09_test_majorites_sortie.txt'), 'w', encoding='utf-8').write(txt)
print(txt)
print('\nContrôle : solde 2025 =', round(solde[2025], 2), '; primaire 2025 =', round(prim[2025], 2), '; PIB 2025 =', round(PIB[2025], 1),
      '; ENP :', {k: round(v, 2) for k, v in ENP.items()})
