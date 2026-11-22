# -*- coding: utf-8 -*-
"""Contrôle final de la voix : formulations écartées par l'audit indépendant et chiffres dits.

Usage : python controler_chiffres.py <dossier script_documentaire_v6>

Deux contrôles, sans rien écrire :
1. aucune des formulations jugées bloquantes par l'audit indépendant ne subsiste dans 01 ;
2. les chiffres dits dans la voix sont recalculés à partir des séries du dépôt, lues au commit
   de la version auditée (git show, sans changer de branche).

Bibliothèque standard seulement. À lancer depuis un clone qui contient le commit 924d875.
"""
import csv
import io
import subprocess
import sys

dossier = sys.argv[1]
SHA = '924d875345e4216d9f5fd748ec380f4463236b21'
DONNEES = 'Le_Constat_Cellule_Enquete/resultats/donnees/'


def table(chemin):
    brut = subprocess.check_output(['git', 'show', '%s:%s' % (SHA, chemin)])
    return list(csv.DictReader(io.StringIO(brut.decode('utf-8-sig')), delimiter=';'))


def nombre(s):
    return float(s.replace(',', '.'))


# --- 1. formulations écartées -----------------------------------------------------------
voix = open(dossier + '/01_SCRIPT_V6.md', encoding='utf-8').read()
voix = voix[voix.index('## Ouverture'):]
ECARTEES = [
    'presque toujours', 'même geste', 'problème avec les bonnes', 'problème avec les mauvaises',
    'chaque fois que le mur', 'caisse est vide', 'à sec', 'Tout le monde perd', "plus qu'ailleurs",
    'chez nos voisins', 'définitives', '41 %', 'quatre fois sur dix', 'ne redescend pas',
    "qu'entre deux crises", 'adoptés par une majorité absolue', 'avaient les voix',
    "L'essentiel de la hausse", 'fait tomber 1975', "Pour l'essentiel", 'Tout se joue à côté',
    'crédit', 'ménage', 'Chaque camp', 'impôts rentrent bien', 'seule baisse des taux', 'rebaissent',
    'trois ou quatre ans', 'balayées par une crise', 'dernier budget à l', 'Il ne l\'a jamais tenue',
    'connu au milliard', 'de un à six', 'toutes les fois où une crise',
]
restantes = [f for f in ECARTEES if f.lower() in voix.lower()]
assert not restantes, 'Formulations écartées encore présentes : %r' % restantes

# la dernière question est celle de la version auditée, au caractère près
ref = subprocess.check_output(['git', 'show', SHA + ':resultats/script_documentaire_v6/01_SCRIPT_V6.md']).decode('utf-8')
fin = lambda t: [l for l in t.strip().split('\n') if l.strip() and l.strip() != '---'][-2:]
assert fin(voix) == fin(ref), 'La dernière question a changé'
assert fin(voix)[-1] == "Qu'est-ce qu'on en fait ?"

# --- 2. chiffres dits -------------------------------------------------------------------
an = {int(r['annee']): r for r in table('resultats/codex/calculs/annuel.csv')}


def v(annee, cle):
    return nombre(an[annee][cle])


serie = range(1975, 2026)
# ouverture et séquence 1
assert round(v(1974, 'b9_pct'), 2) == 0.10                      # 1974 encore légèrement excédentaire
assert all(v(a, 'b9_pct') < 0 for a in serie)                   # « c'est la dernière fois » ; 51 déficits
assert round(v(1980, 'b9_pct'), 2) == -0.43                     # « 0,4 % »
assert max(serie, key=lambda a: v(a, 'b9_pct')) == 1980         # jamais aussi près depuis
assert round(v(1979, 'b9_pct'), 2) == -0.49                     # image de l'ouverture
assert v(1981, 'b9_pct') / v(1980, 'b9_pct') > 5                # « multiplié par plus de cinq »
# solde avant intérêts
positifs = [a for a in serie if v(a, 'primaire_pct') > 0]
assert positifs == [1979, 1980, 1987, 1989, 1990, 1998, 1999, 2000, 2001]   # « c'est rare »
assert all(v(a, 'primaire_pct') < 0 for a in range(2002, 2026))  # « dans notre série, elle ne revient pas »
assert round(v(2006, 'primaire_pct'), 2) == -0.05               # « pratiquement à zéro »
assert len(range(2002, 2026)) == 24                             # « vingt-quatre ans »
assert v(2018, 'primaire_pct') < 0                              # séquence 13
# 2000 : le déficit diminue encore
assert v(1997, 'b9_pct') < v(1998, 'b9_pct') < v(1999, 'b9_pct') < v(2000, 'b9_pct') < 0
# intérêts multipliés par six
assert 6 < v(1996, 'interets_pct') / v(1974, 'interets_pct') < 6.5
# crises : la courbe plonge
for a in (1975, 1993, 2009, 2020):
    assert v(a, 'b9_pct') < v(a - 1, 'b9_pct') - 1.5, a
assert min(range(1975, 1994), key=lambda a: v(a, 'b9_pct')) == 1993   # pire déficit depuis le début
# dette rapportée au PIB : deux bonds, descente partielle, remontée
assert v(2010, 'dette_pct') - v(2007, 'dette_pct') > 100 / 6          # au moins deux mois de production
assert v(2020, 'dette_pct') - v(2019, 'dette_pct') > 100 / 6
assert v(2023, 'dette_pct') < v(2020, 'dette_pct')                    # « redescend en partie »
assert 11 < v(2023, 'dette_pct') - v(2019, 'dette_pct') < 11.6        # « environ onze points »
assert v(2023, 'dette_pct') < v(2024, 'dette_pct') < v(2025, 'dette_pct')   # « depuis, elle remonte »

# trajectoires : 31 sur 31 à l'horizon budgétaire, 31 sur 32 en années civiles, 17 hors crises
cibles = table(DONNEES + 'A08/A08_trajectoires_programmees.csv')
CRISES = {2008, 2009, 2010, 2020, 2021}


def selection(budgetaire=True, exclure=()):
    lignes = []
    for r in cibles:
        annee, mois = map(int, r['date_publication'].split('-'))
        cible = int(r['annee_cible'])
        depart = annee + int(budgetaire and mois >= 9)
        if cible > 2025 or cible != depart + 3:
            continue
        if set(range(annee, cible + 1)) & set(exclure):
            continue
        lignes.append((r['id_document'], cible, nombre(r['solde_programme_pctPIB']), v(cible, 'b9_pct')))
    return lignes


h = selection()
assert len(h) == 31 and all(reel < prevu for _, _, prevu, reel in h)
c = selection(budgetaire=False)
tenues = [(doc, cible) for doc, cible, prevu, reel in c if reel >= prevu]
assert len(c) == 32 and tenues == [('PS1998', 2001)]                  # « la toute première, celle de 2001 »
s = selection(exclure=CRISES)
assert len(s) == 17 and all(reel < prevu for _, _, prevu, reel in s)
equilibre = sorted({int(r['annee_cible']) for r in cibles
                    if int(r['annee_cible']) <= 2025 and nombre(r['solde_programme_pctPIB']) >= 0})
assert equilibre == [2005, 2010, 2012, 2016, 2022]
assert all(v(a, 'b9_pct') < -3 for a in equilibre)

# majorités : 42 budgets classés majoritaires
sieges = table(DONNEES + 'S12/s12_partieA_majorites_vote.csv')
types = [r['type_S12'] for r in sieges]
assert len(types) == 51
assert types.count('parti_seul') + types.count('coalition') == 42 and types.count('appoint') == 1
# poids des recettes publiques : « en six ans […] nettement monté » (séquence 10)
assert v(1999, 'rec_pct') - v(1993, 'rec_pct') > 1.5
print('Classement S12 :', {t: types.count(t) for t in sorted(set(types))})

# conclusion : années de croissance supérieure à 2 %, solde primaire observé et corrigé du cycle
cycle = table(DONNEES + 'A09/a09_table_exercices_1975_2025.csv')
var = {int(r['exercice']): nombre(r['d_spcc_ameco']) for r in cycle if r['d_spcc_ameco']}
fortes = [a for a in var if v(a, 'g_reel_pct') > 2]
observe = sum(v(a, 'primaire_pct') > v(a - 1, 'primaire_pct') for a in fortes)
corrige = sum(var[a] > 0 for a in fortes)
assert (len(fortes), observe, corrige) == (22, 16, 8)     # conclusion : « une fois sur trois environ » (8 sur 22)
assert var[2000] < -1                                     # 2000 : le solde corrigé se dégrade

print('Formulations écartées : aucune ne subsiste (%d cherchées).' % len(ECARTEES))
print('Dernière question : identique à la version auditée.')
print('Chiffres recalculés : conformes à la voix.')
print('Croissance > 2 %% depuis 1979 : %d années, solde primaire amélioré %d fois, corrigé du cycle %d fois.'
      % (len(fortes), observe, corrige))
