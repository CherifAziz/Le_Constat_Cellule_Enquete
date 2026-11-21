# A06 - Vitesse de la dépense publique en volume vs croissance du PIB (effectif et potentiel), France 1960-2025.
# Dépense et recettes en % du PIB : base commune Insee (base 2020, extraction 20/11/2026, lecture seule).
# PIB nominal, déflateur, PIB potentiel : AMECO automne 2026.
# Volume de dépense = dépense nominale / déflateur du PIB (convention « volume au prix du PIB », pas un indice de volume de services).
# Usage : python -I 04_depense_vs_croissance.py <racine_resultats>
import sys, csv, os, collections
R = sys.argv[1]
ins = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(R, 'donnees/commun/base_insee_dep_rec_pctPIB.csv'), encoding='utf-8-sig'), delimiter=';'):
    ins[r['serie']][int(r['annee'])] = float(r['valeur'])
A = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(R, 'donnees/A06/ameco_series_A06.csv'), encoding='utf-8'), delimiter=';'):
    if r['pays'] == 'FRA':
        A[r['variable']][int(r['annee'])] = float(r['valeur'])
dep, rec = ins['Dépenses'], ins['Recettes']
Y, D, Q, P = A['pib_courant_monnaie_nat'], A['deflateur_pib_2020'], A['pib_volume_2020'], A['pib_potentiel_2020']
out = []
def cg(s, a, b):
    return 100 * ((s[b] / s[a]) ** (1 / (b - a)) - 1)
vol_dep = {y: dep[y] / 100 * Y[y] / D[y] for y in dep if y in Y and y in D}
vol_rec = {y: rec[y] / 100 * Y[y] / D[y] for y in rec if y in Y and y in D}
out.append('periode | dep %PIB debut->fin | rec %PIB debut->fin | croiss. vol. depense | croiss. vol. recettes | croiss. PIB | croiss. PIB potentiel | ecart dep-PIB (pts/an)')
for a, b in [(1960, 1974), (1974, 1985), (1985, 1993), (1993, 2000), (2000, 2007), (2007, 2013), (2013, 2019), (2019, 2025), (1974, 2025), (1993, 2025)]:
    pot = cg(P, max(a, 1965), b) if max(a, 1965) in P else float('nan')
    out.append(f'{a}-{b} | {dep[a]:.1f}->{dep[b]:.1f} | {rec[a]:.1f}->{rec[b]:.1f} | {cg(vol_dep,a,b):.2f} | {cg(vol_rec,a,b):.2f} | {cg(Q,a,b):.2f} | {pot:.2f} | {cg(vol_dep,a,b)-cg(Q,a,b):.2f}')

# Contrefactuel mécanique (borne, non causal) : si la dépense en volume avait ralenti au même rythme que le PIB
# après 1974 (même écart dépense-PIB qu'en 1960-1974), quel ratio en 1985 et 1993 ?
gap6074 = cg(vol_dep, 1960, 1974) - cg(Q, 1960, 1974)
for b in (1985, 1993, 2025):
    ratio = dep[1974]
    for y in range(1975, b + 1):
        gq = Q[y] / Q[y - 1] - 1
        ratio = ratio * (1 + gq + gap6074 / 100) / (1 + gq)  # deflateur identique numérateur/dénominateur
    out.append(f'Contrefactuel mécanique : dépense/PIB en {b} si écart dépense-PIB = celui de 1960-74 ({gap6074:.2f} pt/an) : {ratio:.1f} % (observé {dep[b]:.1f} %)')
# Variante : dépense en volume = tendance 1960-74 du PIB (5,5%/an) => mesure de « droits bâtis sur 5 % »
open(os.path.join(R, 'donnees/A06/resultats_04_depense_croissance.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
