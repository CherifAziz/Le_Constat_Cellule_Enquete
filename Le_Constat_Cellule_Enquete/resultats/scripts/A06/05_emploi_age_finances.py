# A06 - Taux d'emploi par âge (Eurostat EFT lfsa_ergan/lfsa_egan, maj 30/10/2026) et traduction prudente en finances publiques.
# Usage : python -I 05_emploi_age_finances.py <racine_resultats> [annee]
# Toutes les hypothèses sont en tête de fichier et balayées en fourchette ; aucun effet d'équilibre général n'est simulé.
import sys, csv, os, collections, itertools
R = sys.argv[1]
YEAR = sys.argv[2] if len(sys.argv) > 2 else '2025'
E = os.path.join(R, 'donnees/A06/eurostat')
rate = collections.defaultdict(dict); emp = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(E, 'lfsa_ergan.csv'), encoding='utf-8'), delimiter=';'):
    rate[(r['geo'], r['sex'], r['age'])][r['time']] = float(r['value'])
for r in csv.DictReader(open(os.path.join(E, 'lfsa_egan.csv'), encoding='utf-8'), delimiter=';'):
    emp[(r['geo'], r['age'])][r['time']] = float(r['value'])
out = []; P = out.append
GEOS = ['FR', 'DE', 'NL', 'SE', 'DK', 'BE', 'IT', 'ES', 'EU27_2020', 'EA20']
AGES = ['Y15-24', 'Y25-54', 'Y55-59', 'Y60-64', 'Y55-64', 'Y20-64', 'Y15-64']
P(f'=== Taux d emploi {YEAR} (%), EFT Eurostat, sexe T / H / F ===')
P('age | ' + ' | '.join(GEOS))
for s in ['T', 'M', 'F']:
    for a in AGES:
        P(f'{s} {a} | ' + ' | '.join(str(rate[(g, s, a)].get(YEAR, 'n.d.')) for g in GEOS))
P('\nFrance, évolution (T) : ' + ' ; '.join(f"{a} " + '/'.join(str(rate[('FR','T',a)].get(y,'nd')) for y in ('1995','2000','2007','2013','2019','2025')) for a in ['Y15-24','Y25-54','Y55-64','Y60-64']))
# Populations par âge reconstituées = emploi / taux
pop = {a: emp[('FR', a)][YEAR] / (rate[('FR', 'T', a)][YEAR] / 100) for a in ['Y15-24', 'Y25-54', 'Y55-59', 'Y60-64']}
P('\nPopulation FR reconstituée (milliers) : ' + ', '.join(f'{a}={v:.0f}' for a, v in pop.items()))
P('\n=== Emplois supplémentaires si la France avait les taux par âge du comparateur (milliers), à démographie française ===')
P('comparateur | 15-24 | 25-54 | 55-59 | 60-64 | total')
gaps = {}
for g in ['DE', 'NL', 'SE', 'DK', 'EU27_2020', 'EA20']:
    d = {a: max(0.0, (rate[(g, 'T', a)].get(YEAR, 0) - rate[('FR', 'T', a)][YEAR]) / 100 * pop[a]) for a in pop}
    gaps[g] = d
    P(f"{g} | {d['Y15-24']:.0f} | {d['Y25-54']:.0f} | {d['Y55-59']:.0f} | {d['Y60-64']:.0f} | {sum(d.values()):.0f}")

# Traduction finances publiques (ordre de grandeur, statique) -----------------------------------
# PIB 2025 (Eurostat notification oct. 2026, base commune) et emploi intérieur (AMECO)
PIB = 2991.056  # Md€
A = {}
for r in csv.DictReader(open(os.path.join(R, 'donnees/A06/ameco_series_A06.csv'), encoding='utf-8'), delimiter=';'):
    if r['pays'] == 'FRA' and r['annee'] == '2025':
        A[r['variable']] = float(r['valeur'])
y_par_emploi = PIB * 1e9 / (A['emploi_interieur_milliers'] * 1e3)  # € par emploi
P(f'\nPIB 2025 par emploi intérieur : {y_par_emploi/1e3:.1f} k€ (PIB {PIB} Md€ / emploi AMECO {A["emploi_interieur_milliers"]:.0f} milliers)')
# Hypothèses
PROD_REL = {'basse': 0.5, 'centrale': 0.7, 'haute': 0.9}       # H-A06-001 : productivité relative de l'emploi additionnel (Trésor/Rexecode supposent 1,0 ; CNP 2026 : vieillissement de la main-d'oeuvre défavorable à la productivité)
TAUX_PREL = {'basse': 0.35, 'centrale': 0.42, 'haute': 0.50}   # H-A06-002 : recettes APU induites par € de PIB additionnel (46 % = ratio impôts+cotisations Eurostat 2025 ; ~0,50 implicite dans Rexecode, Cour fév. 2025 tab. 5 : (10,9+5,5)/(1,1 % du PIB))
PREST_EVIT = {'basse': 3000, 'centrale': 8000, 'haute': 15000}  # H-A06-003 : € par emploi additionnel (chômage, minima, pension différée) - hypothèse sans pièce directe
DEP_INDUITES = {'basse': 0.30, 'centrale': 0.20, 'haute': 0.10}  # H-A06-004 : part des recettes induites rendue en droits futurs et dépenses induites (ordre de grandeur : Drees/Dares ≈ 20 % des économies brutes, Cour fév. 2025 p. 67)
P('\nScénario | comparateur | emplois (milliers) | PIB induit (Md€, %PIB) | recettes induites | prestations évitées | dépenses induites | solde net (Md€, %PIB)')
for g in ['DE', 'NL', 'SE', 'EU27_2020']:
    n = sum(gaps[g].values()) * 1e3
    for sc in ['basse', 'centrale', 'haute']:
        dy = n * y_par_emploi * PROD_REL[sc] / 1e9
        rec = dy * TAUX_PREL[sc]
        pe = n * PREST_EVIT[sc] / 1e9
        di = rec * DEP_INDUITES[sc]
        net = rec + pe - di
        P(f'{sc} | {g} | {n/1e3:.0f} | {dy:.0f} ({100*dy/PIB:.1f}) | {rec:.0f} | {pe:.0f} | {di:.0f} | {net:.0f} ({100*net/PIB:.1f})')
# Seniors seuls (55-64) vers taux allemand
n = (gaps['DE']['Y55-59'] + gaps['DE']['Y60-64']) * 1e3
P(f'\nSeniors 55-64 seuls au taux allemand : {n/1e3:.0f} milliers d emplois')
for sc in ['basse', 'centrale', 'haute']:
    dy = n * y_par_emploi * PROD_REL[sc] / 1e9; rec = dy * TAUX_PREL[sc]; pe = n * PREST_EVIT[sc] / 1e9; di = rec * DEP_INDUITES[sc]
    P(f'  {sc} : PIB +{dy:.0f} Md€ ({100*dy/PIB:.1f} %), solde +{rec+pe-di:.0f} Md€ ({100*(rec+pe-di)/PIB:.2f} pt PIB)')
# Version en équivalent durée du travail (correction demandée : l'écart en personnes surestime l'écart en heures)
H = {}
for r in csv.DictReader(open(os.path.join(R, 'donnees/A06/ameco_series_A06.csv'), encoding='utf-8'), delimiter=';'):
    if r['annee'] == '2025' and r['variable'] in ('heures_totales_millions', 'pop_15_64_milliers', 'emploi_interieur_milliers', 'heures_par_emploi'):
        H[(r['pays'], r['variable'])] = float(r['valeur'])
P('\n=== Équivalent heures (AMECO 2025) : emplois FR à durée française nécessaires pour atteindre les heures par personne de 15-64 ans du comparateur ===')
fte = {}
for c in ['DEU', 'NLD', 'SWE']:
    hpw_c = H[(c, 'heures_totales_millions')] / H[(c, 'pop_15_64_milliers')]
    hpw_f = H[('FRA', 'heures_totales_millions')] / H[('FRA', 'pop_15_64_milliers')]
    extra_h = (hpw_c - hpw_f) * H[('FRA', 'pop_15_64_milliers')]  # millions d'heures
    fte[c] = extra_h * 1e6 / H[('FRA', 'heures_par_emploi')] / 1e3
    P(f'{c} : heures/pers. 15-64 {hpw_c*1e3:.0f} vs FR {hpw_f*1e3:.0f} -> {fte[c]:.0f} milliers d emplois FR équivalents')
P('Cour des comptes (avril 2025, p. 20) : alignement sur le taux allemand = 3,6 M en personnes, ≈ 1,5 M en tenant compte de la durée du travail')
P('\nScénario | volume (milliers ETP) | PIB induit | solde net (Md€, %PIB)')
for lab, n in [('DE ETP Cour', 1500), ('DE heures AMECO', fte['DEU']), ('Seniors 55-64 au taux DE (personnes)', (gaps['DE']['Y55-59'] + gaps['DE']['Y60-64']))]:
    for sc in ['basse', 'centrale', 'haute']:
        dy = n * 1e3 * y_par_emploi * PROD_REL[sc] / 1e9; rec = dy * TAUX_PREL[sc]; pe = n * 1e3 * PREST_EVIT[sc] / 1e9; di = rec * DEP_INDUITES[sc]
        P(f'{lab} {sc} | {n:.0f} | {dy:.0f} Md€ ({100*dy/PIB:.1f} %) | {rec+pe-di:.0f} ({100*(rec+pe-di)/PIB:.1f})')
open(os.path.join(R, 'donnees/A06/resultats_05_emploi_age.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))
