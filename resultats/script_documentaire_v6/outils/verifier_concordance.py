# -*- coding: utf-8 -*-
"""Vérifie que 01_SCRIPT_V6.md (voix seule) dit exactement le texte parlé de 02_SCRIPT_ANNOTE.md,
et que durees.json est cohérent. N'écrit rien.

Usage : python verifier_concordance.py <dossier script_documentaire_v6>

L'extraction est refaite ici, sans réutiliser construire_script.py : les deux fichiers sont
lus séparément, paragraphe par paragraphe, puis comparés caractère pour caractère.
"""
import json
import re
import sys

dossier = sys.argv[1]


def lire(nom):
    return open(dossier + '/' + nom, encoding='utf-8').read()


def blocs(texte):
    """Découpe en blocs séparés par des lignes vides."""
    return [b.strip() for b in re.split(r'\n\s*\n', texte) if b.strip()]


# --- 02 : tout ce qui suit « ## Ouverture » et n'est ni titre, ni filet, ni indication ---
annote = lire('02_SCRIPT_ANNOTE.md')
annote = annote[annote.index('\n## Ouverture'):]
parle_02, titres_02 = [], []
for b in blocs(annote):
    for ligne in b.split('\n'):
        ligne = ligne.strip()
        if ligne.startswith('#'):
            titres_02.append(ligne.lstrip('#').strip())
        elif ligne and not ligne.startswith('>') and ligne != '---':
            parle_02.append(ligne)

# --- 01 : tout ce qui suit le premier filet, hors titres et filets ----------------------
voix = lire('01_SCRIPT_V6.md')
entete, _, corps = voix.partition('\n---\n')
parle_01, titres_01 = [], []
for b in blocs(corps):
    for ligne in b.split('\n'):
        ligne = ligne.strip()
        if ligne.startswith('#'):
            titres_01.append(ligne.lstrip('#').strip())
        elif ligne and ligne != '---':
            parle_01.append(ligne)

erreurs = []
if titres_01 != titres_02:
    erreurs.append('Titres différents : %r / %r' % (titres_01, titres_02))
if len(parle_01) != len(parle_02):
    erreurs.append('Nombre de paragraphes dits : %d dans 01, %d dans 02' % (len(parle_01), len(parle_02)))
for i, (a, b) in enumerate(zip(parle_01, parle_02)):
    if a != b:
        erreurs.append('Paragraphe %d différent :\n  01 : %s\n  02 : %s' % (i + 1, a, b))
for marque in ('**IMAGE**', '**ARCHIVE**', '**MUR**', '**SON**'):
    if any(marque in p for p in parle_01):
        erreurs.append('Indication de réalisation dans la voix seule : ' + marque)
if any(p.startswith('>') for p in parle_01):
    erreurs.append('Ligne en retrait dans la voix seule')

# --- durees.json -------------------------------------------------------------------------
d = json.loads(lire('durees.json'))
seq = d['sequences']
titres_seq = [t for t in titres_02 if not t.startswith('Acte')]
if [s['titre'] for s in seq] != titres_seq:
    erreurs.append('Séquences de durees.json différentes des titres du script')

h = d['hypotheses']


def compte_mots(texte):
    t = re.sub(r'\((pause|silence)\)', ' ', texte)
    t = re.sub(r'[«»:;?!]', ' ', t)
    return len([m for m in t.split() if re.search(r'[A-Za-zÀ-ÿ0-9]', m)])


total_mots = compte_mots(' '.join(parle_01))
if total_mots != d['total_mots']:
    erreurs.append('Mots : %d recomptés, %d dans durees.json' % (total_mots, d['total_mots']))
if sum(s['mots'] for s in seq) != d['total_mots']:
    erreurs.append('La somme des mots par séquence ne donne pas le total')

# continuité : chaque seconde appartient à une plage, la dernière borne est le total
plages = sorted([(s['debut_s'], s['fin_s'], s['titre']) for s in seq] +
                [(p['debut_s'], p['fin_s'], p['titre']) for p in d['plages_hors_voix']])
if plages[0][0] != 0:
    erreurs.append('La feuille de temps ne commence pas à zéro')
for (d1, f1, t1), (d2, f2, t2) in zip(plages, plages[1:]):
    if abs(f1 - d2) > 0.11:   # tolérance d'arrondi au dixième
        erreurs.append('Trou ou recouvrement entre « %s » (%s) et « %s » (%s)' % (t1, f1, t2, d2))
if abs(plages[-1][1] - d['total_s']) > 0.11:
    erreurs.append('Dernière borne %s différente du total %s' % (plages[-1][1], d['total_s']))
if abs(d['fin_avec_silence_s'] - d['fin_derniere_sequence_s'] - h['silence_final_s']) > 0.11:
    erreurs.append('Le silence final n\'explique pas l\'écart entre les deux fins')
attendu = d['voix_seule_s']
if abs(total_mots / h['mots_par_minute'] * 60 - attendu) > 0.11:
    erreurs.append('Durée de voix seule incohérente avec le débit déclaré')
m = re.search(r'\*\*(\d+) mots\. Durée estimée par le calcul : (\d+):(\d\d)\*\*', entete)
if not m:
    erreurs.append('Bandeau de durée introuvable dans 01')
else:
    if int(m.group(1)) != d['total_mots']:
        erreurs.append('Nombre de mots du bandeau différent de durees.json')
    if int(m.group(2)) * 60 + int(m.group(3)) != int(round(d['total_s'])):
        erreurs.append('Durée du bandeau différente de durees.json')
if 'mesurée' not in entete:
    erreurs.append('Le bandeau ne dit pas que la durée est une estimation')

if erreurs:
    print('ÉCHEC')
    for e in erreurs:
        print('-', e)
    sys.exit(1)
print('Concordance vérifiée : %d paragraphes dits, %d mots, %d séquences, %d plages hors voix.'
      % (len(parle_01), total_mots, len(seq), len(d['plages_hors_voix'])))
print('Fin de la dernière séquence : %s s. Fin avec silence : %s s. Estimation calculée, non mesurée.'
      % (d['fin_derniere_sequence_s'], d['fin_avec_silence_s']))
