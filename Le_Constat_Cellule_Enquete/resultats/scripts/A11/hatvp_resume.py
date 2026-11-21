# -*- coding: utf-8 -*-
"""A11 - Resume par dossier des fiches HATVP filtrees (hatvp_<dossier>.csv) :
nombre de fiches, d'organisations, repartition par exercice et par categorie, et
part des fiches dont l'objet vise le maintien / la defense / la stabilite du dispositif.
Usage : python -I hatvp_resume.py <dossier_hatvp>"""
import csv, sys, os, re, collections
d = sys.argv[1]
sys.stdout.reconfigure(encoding='utf-8')
MAINT = re.compile(r"maint|pr[ée]serv|sanctuar|stabilit|d[ée]fend|s.opposer|[ée]viter|emp[êe]cher|p[ée]renn|prot[ée]g|sacralis|ne pas (r[ée]former|limiter|supprimer)|conserver|alerter", re.I)
REFORME = re.compile(r"r[ée]form|recentr|supprim|condition|fl[ée]ch|plafonn|renforcer le pacte|allong|exclure .* somptuaires|restreindre", re.I)
out = []
for k, pat in [('CIR', None), ('Dutreil', r'dutreil|787'), ('TVA_restauration', r'restaura|h[ôo]tel'),
               ('autoroutes', r'concession|soci[ée]t[ée]s? (concessionnaires|d.autoroutes)|SCA'),
               ('dividendes_cumcum', None), ('aides_entreprises', r'aides publiques aux entreprises|conditionnalit[ée] des aides aux entreprises|bénéficiaires d.aides'),
               ('conseil_cabinets', r'cabinets? de conseil')]:
    rows = list(csv.DictReader(open(os.path.join(d, f'hatvp_{k}.csv'), encoding='utf-8'), delimiter=';'))
    if pat:
        rows = [r for r in rows if re.search(pat, r['objet'] + ' ' + r['observations'], re.I)]
    orgs = set(r['organisation'] for r in rows)
    ans = collections.Counter(r['exercice_debut'][-4:] for r in rows)
    cats = collections.Counter(r['categorie'] for r in rows)
    m = sum(1 for r in rows if MAINT.search(r['objet']))
    f = sum(1 for r in rows if REFORME.search(r['objet']) and not MAINT.search(r['objet']))
    out.append([k, len(rows), len(orgs), m, f, dict(sorted(ans.items())), dict(cats.most_common(4))])
    print(k, 'fiches', len(rows), 'orgs', len(orgs), 'objet maintien/defense', m, 'objet reforme sans maintien', f)
    print('   par exercice', dict(sorted(ans.items())))
    print('   categories', dict(cats.most_common(5)))
with open(os.path.join(d, 'hatvp_resume_par_dossier.csv'), 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter=';')
    w.writerow(['dossier', 'fiches', 'organisations', 'objet_maintien_defense', 'objet_reforme_sans_maintien', 'par_exercice', 'categories_top4'])
    w.writerows(out)
