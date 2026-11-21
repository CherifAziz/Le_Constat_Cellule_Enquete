# -*- coding: utf-8 -*-
"""A11 - Fiches HATVP dont l'OBJET nomme explicitement le CIR (et non le seul CII/CIC).
Comptage par exercice et liste pour codage manuel du sens (fait a la main dans A11_annexe_dossier_CIR.md).
Usage : python -I hatvp_cir_strict.py <hatvp_CIR.csv> <sortie.csv>"""
import csv, sys, re, collections
sys.stdout.reconfigure(encoding='utf-8')
r = list(csv.DictReader(open(sys.argv[1], encoding='utf-8'), delimiter=';'))
pat = re.compile(r"\bCIR\b|cr[ée]dit d.imp[ôo]t (en faveur de la )?recherche|CREDIT D.IMPOT RECHERCHE|Cr[ée]dit Imp[ôo]t Recherche", re.I)
s = [x for x in r if pat.search(x['objet'])]
c = collections.Counter(x['exercice_debut'][-4:] for x in s)
o = collections.defaultdict(set)
for x in s: o[x['exercice_debut'][-4:]].add(x['organisation'])
print('fiches objet CIR explicite', len(s), 'organisations', len(set(x['organisation'] for x in s)))
for y in sorted(c): print(y, c[y], 'fiches', len(o[y]), 'organisations')
with open(sys.argv[2], 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['exercice', 'organisation', 'categorie', 'objet'])
    for x in sorted(s, key=lambda z: z['exercice_debut'][-4:]): w.writerow([x['exercice_debut'][-4:], x['organisation'], x['categorie'], x['objet'].replace('\n', ' ')])
