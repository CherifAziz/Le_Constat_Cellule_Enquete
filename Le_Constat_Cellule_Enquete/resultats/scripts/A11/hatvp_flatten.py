# -*- coding: utf-8 -*-
"""A11 - Aplatit le repertoire HATVP (open data agora, telecharge le 20/11/2026)
en une ligne par fiche d'activite, puis filtre par mots-cles (dossiers A11).
Usage : python -I hatvp_flatten.py <json> <dossier_sortie>
Sorties : hatvp_activites_toutes.csv (toutes fiches) et hatvp_<dossier>.csv (filtrees).
Les mots-cles sont appliques a l'objet de la fiche et aux observations (insensible a la casse).
"""
import json, csv, sys, os, re

src, outdir = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))['publications']
rows = []
for p in d:
    org = p.get('denomination', '')
    cat = (p.get('categorieOrganisation') or {}).get('label', '') if isinstance(p.get('categorieOrganisation'), dict) else str(p.get('categorieOrganisation', ''))
    ident = p.get('identifiantNational', '')
    for e in p.get('exercices', []):
        pc = e.get('publicationCourante', {})
        deb, fin = pc.get('dateDebut', ''), pc.get('dateFin', '')
        dep = pc.get('montantDepense', '')
        for a in pc.get('activites', []) or []:
            ac = a.get('publicationCourante', {})
            objet = ac.get('objet', '')
            dom = ' | '.join(ac.get('domainesIntervention', []) or [])
            resp, dec, act, obs, tiers = set(), set(), set(), [], set()
            for x in ac.get('actionsRepresentationInteret', []) or []:
                resp.update(x.get('reponsablesPublics', []) or [])
                dec.update(x.get('decisionsConcernees', []) or [])
                act.update(x.get('actionsMenees', []) or [])
                tiers.update(x.get('tiers', []) or [])
                if x.get('observation'):
                    obs.append(x['observation'])
            rows.append({'organisation': org, 'categorie': cat, 'identifiant': ident,
                         'exercice_debut': deb, 'exercice_fin': fin, 'depenses_declarees': dep,
                         'fiche': ac.get('identifiantFiche', ''), 'date_publication': ac.get('publicationDate', ''),
                         'objet': objet, 'domaines': dom, 'responsables': ' | '.join(sorted(resp)),
                         'decisions': ' | '.join(sorted(dec)), 'actions': ' | '.join(sorted(act)),
                         'tiers': ' | '.join(sorted(tiers)), 'observations': ' || '.join(obs)})

cols = list(rows[0].keys())
with open(os.path.join(outdir, 'hatvp_activites_toutes.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, cols, delimiter=';'); w.writeheader(); w.writerows(rows)

FILTRES = {
    'CIR': r"cr[ée]dit d.imp[ôo]t (recherche|innovation)|\bCIR\b|\bCII\b",
    'TVA_restauration': r"(TVA|taxe sur la valeur ajout[ée]e).{0,80}(restaura|h[ôo]tel|caf[ée]s|10 ?%)|(restaura|h[ôo]tel).{0,80}(TVA|taux r[ée]duit)",
    'Dutreil': r"dutreil|787 ?B|transmission (d.entreprises?|familiale)|pacte de transmission",
    'autoroutes': r"autorout|concession(s)? (autoroutière|d.autoroute)|p[ée]age",
    'abattement_pensions': r"abattement de 10|abattement.{0,40}(pension|retrait)",
    'dividendes_cumcum': r"cum.?cum|arbitrage de dividendes|dividend.{0,60}(non.r[ée]sident|retenue [àa] la source)|retenue [àa] la source.{0,60}dividend",
    'conseil_cabinets': r"cabinets? de conseil|prestations? (intellectuelles|de conseil)|recours aux consultants",
    'aides_entreprises': r"aides publiques aux entreprises|conditionnalit[ée] des aides|commission d.enqu[êe]te.{0,40}aides",
    'GNR_TICPE_transport': r"gazole non routier|\bGNR\b|remboursement.{0,40}TICPE|TICPE.{0,60}(transport|routier)|accise.{0,40}gazole",
    'apprentissage': r"aide[s]? (exceptionnelle[s]? )?(à|a) l.apprentissage|aide[s]? (à|a) l.embauche (d.|des )?apprenti",
}
summary = []
for k, pat in FILTRES.items():
    rg = re.compile(pat, re.I)
    sel = [r for r in rows if rg.search(r['objet']) or rg.search(r['observations'])]
    with open(os.path.join(outdir, f'hatvp_{k}.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, cols, delimiter=';'); w.writeheader(); w.writerows(sel)
    orgs = sorted(set(r['organisation'] for r in sel))
    summary.append((k, len(sel), len(orgs)))
print('fiches totales', len(rows), 'organisations', len(d))
for s in summary:
    print(s)
