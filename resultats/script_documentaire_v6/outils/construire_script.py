# -*- coding: utf-8 -*-
"""Produit 01_SCRIPT_V6.md (voix seule) et durees.json à partir de 02_SCRIPT_ANNOTE.md.

Usage : python construire_script.py <dossier script_documentaire_v6> [--ecrire]

02_SCRIPT_ANNOTE.md est la seule source. Sa date, sa version et son état sont lus dans
le bloc « METADONNEES » placé en tête du fichier : rien n'est figé dans ce programme.

Les durées sont des ESTIMATIONS CALCULÉES, pas des durées mesurées sur un enregistrement.
Hypothèses (constantes ci-dessous) : débit de lecture en mots par minute ; durée d'une
(pause) et d'un (silence) dits dans la voix ; respiration entre deux paragraphes ; carton
de titre après l'ouverture et silence final, tous deux hors voix.
"""
import re
import sys
import json

MOTS_MIN = 182.0          # hypothèse de débit, à remplacer par la mesure du fichier audio
PAUSE_S = 1.0             # (pause)
SILENCE_S = 2.5           # (silence) placé dans le texte dit
RESPIRATION_S = 0.5       # entre deux paragraphes dits
CARTON_TITRE_S = 4.0      # hors voix, après l'ouverture
SILENCE_FINAL_S = 3.0     # hors voix, après la dernière phrase

dossier = sys.argv[1]
ecrire = '--ecrire' in sys.argv
src = open(dossier + '/02_SCRIPT_ANNOTE.md', encoding='utf-8').read()

# --- métadonnées lues dans le script annoté -------------------------------------------
meta = {}
bloc = re.search(r'<!--\s*METADONNEES.*?\n(.*?)-->', src, re.S)
if bloc:
    for ligne in bloc.group(1).split('\n'):
        if ':' in ligne:
            cle, valeur = ligne.split(':', 1)
            meta[cle.strip()] = valeur.strip()
for cle in ('titre', 'version', 'date', 'etat'):
    if cle not in meta:
        sys.exit('Métadonnée manquante dans 02_SCRIPT_ANNOTE.md : ' + cle)

# --- extraction du texte dit ----------------------------------------------------------
debut = src.index('## Ouverture')
corps = src[debut:]

sequences = []  # [acte, titre, [paragraphes]]
acte = ''
courant = None
for ligne in corps.split('\n'):
    l = ligne.rstrip()
    if l.startswith('## '):
        titre = l[3:].strip()
        if titre.startswith('Acte'):
            acte = titre
            courant = None
        else:
            acte = titre
            courant = [acte, titre, []]
            sequences.append(courant)
        continue
    if l.startswith('### '):
        courant = [acte, l[4:].strip(), []]
        sequences.append(courant)
        continue
    if not l or l.startswith('>') or l.strip() == '---':
        continue
    if courant is not None:
        courant[2].append(l)


def mots(texte):
    t = re.sub(r'\((pause|silence)\)', ' ', texte)
    t = t.replace('«', ' ').replace('»', ' ').replace(':', ' ').replace(';', ' ').replace('?', ' ').replace('!', ' ')
    return len([m for m in t.split() if re.search(r'[A-Za-zÀ-ÿ0-9]', m)])


def mmss(s):
    s = int(round(s))
    return '%d:%02d' % (s // 60, s % 60)


def fr(x):
    return ('%g' % x).replace('.', ',')


# --- durées par séquence --------------------------------------------------------------
stats = []
total_mots = 0
for a, t, paras in sequences:
    texte = ' '.join(paras)
    n = mots(texte)
    pauses = len(re.findall(r'\(pause\)', texte))
    silences = len(re.findall(r'\(silence\)', texte))
    sec = n / MOTS_MIN * 60 + pauses * PAUSE_S + silences * SILENCE_S + max(0, len(paras) - 1) * RESPIRATION_S
    total_mots += n
    stats.append((a, t, n, len(paras), pauses + silences, sec))

# --- feuille de temps : chaque seconde appartient à une plage nommée -------------------
plages = []       # toutes les plages, voix et hors voix, dans l'ordre
seq_json = []
hors_voix = []
cumul = 0.0
for a, t, n, p, pa, sec in stats:
    plages.append({'type': 'voix', 'titre': t, 'debut_s': cumul, 'fin_s': cumul + sec})
    seq_json.append({'acte': a, 'titre': t, 'mots': n, 'duree_s': round(sec, 1),
                     'debut_s': round(cumul, 1), 'fin_s': round(cumul + sec, 1)})
    cumul += sec
    if t == 'Ouverture':
        h = {'titre': 'Carton de titre (hors voix)', 'debut_s': round(cumul, 1), 'fin_s': round(cumul + CARTON_TITRE_S, 1)}
        hors_voix.append(h)
        plages.append({'type': 'hors voix', 'titre': h['titre'], 'debut_s': cumul, 'fin_s': cumul + CARTON_TITRE_S})
        cumul += CARTON_TITRE_S
fin_derniere_sequence = cumul
h = {'titre': 'Silence final (hors voix)', 'debut_s': round(cumul, 1), 'fin_s': round(cumul + SILENCE_FINAL_S, 1)}
hors_voix.append(h)
plages.append({'type': 'hors voix', 'titre': h['titre'], 'debut_s': cumul, 'fin_s': cumul + SILENCE_FINAL_S})
cumul += SILENCE_FINAL_S
total_sec = cumul

# contrôles : les plages se suivent sans trou, la dernière borne est le total
for avant, apres in zip(plages, plages[1:]):
    assert abs(avant['fin_s'] - apres['debut_s']) < 1e-9, (avant, apres)
assert abs(plages[-1]['fin_s'] - total_sec) < 1e-9
assert abs(sum(s[5] for s in stats) + CARTON_TITRE_S + SILENCE_FINAL_S - total_sec) < 1e-6

voix_seule = total_mots / MOTS_MIN * 60

print('%-34s %6s %5s %6s %7s %8s %8s' % ('plage', 'mots', 'par.', 'pauses', 'durée', 'début', 'fin'))
par_titre = {s[1]: s for s in stats}
for pl in plages:
    if pl['type'] == 'voix':
        a, t, n, p, pa, sec = par_titre[pl['titre']]
        print('%-34s %6d %5d %6d %7s %8s %8s' % (t[:34], n, p, pa, mmss(sec), mmss(pl['debut_s']), mmss(pl['fin_s'])))
    else:
        print('%-34s %6s %5s %6s %7s %8s %8s' % (pl['titre'][:34], '', '', '', mmss(pl['fin_s'] - pl['debut_s']), mmss(pl['debut_s']), mmss(pl['fin_s'])))
print('TOTAL mots', total_mots, '| fin de la dernière séquence', mmss(fin_derniere_sequence),
      '| fin avec silence', mmss(total_sec), '| voix seule à %g mots/min : %s' % (MOTS_MIN, mmss(voix_seule)))
print('Estimation calculée, non mesurée sur un enregistrement.')

# chiffres dits par séquence (hors années et dates). Ne détecte pas les nombres écrits en lettres.
print()
for a, t, paras in sequences:
    texte = ' '.join(paras)
    texte = re.sub(r'\b(19|20)\d\d\b', '', texte)
    texte = re.sub(r'\b1er\b|\b\d{1,2} (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b', '', texte)
    ch = re.findall(r'\d[\d ,]*\d|\d', texte)
    print('%-34s chiffres écrits en chiffres : %d %s' % (t[:34], len(ch), ch))

if ecrire:
    convention = ('hypothèse de %s mots par minute ; (pause) = %s s ; (silence) = %s s ; %s s entre deux paragraphes ; '
                  '%s s de carton de titre et %s s de silence final hors voix'
                  % (fr(MOTS_MIN), fr(PAUSE_S), fr(SILENCE_S), fr(RESPIRATION_S), fr(CARTON_TITRE_S), fr(SILENCE_FINAL_S)))
    s = ['# 01 · Script V6 — *%s*' % meta['titre'], '',
         '**%s. %s.** Texte seul, tel qu\'il est dit. '
         'Les indications d\'image et d\'archive sont dans [02_SCRIPT_ANNOTE.md](02_SCRIPT_ANNOTE.md), dont ce fichier est extrait automatiquement.'
         % (meta['date'], meta['etat']), '',
         '`(pause)` : respiration marquée, environ une seconde. `(silence)` : deux à trois secondes sans voix.', '',
         '**%d mots. Durée estimée par le calcul : %s** (%s). Ce n\'est pas une durée mesurée sur un enregistrement.'
         % (total_mots, mmss(total_sec), convention), '', '---', '']
    acte_prec = None
    for a, t, paras in sequences:
        if a != acte_prec and a != t:
            s += ['## ' + a, '']
        acte_prec = a
        if a == t:
            s += ['## ' + t, '']
        else:
            s += ['### ' + t, '']
        for p in paras:
            s += [p, '']
        if a == t:
            s += ['---', '']
    open(dossier + '/01_SCRIPT_V6.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(s).rstrip() + '\n')
    sortie = {
        'titre': meta['titre'], 'version': meta['version'], 'date': meta['date'],
        'nature': 'estimation calculée, non mesurée sur un enregistrement',
        'hypotheses': {'mots_par_minute': MOTS_MIN, 'pause_s': PAUSE_S, 'silence_s': SILENCE_S,
                       'respiration_entre_paragraphes_s': RESPIRATION_S,
                       'carton_titre_s': CARTON_TITRE_S, 'silence_final_s': SILENCE_FINAL_S},
        'total_mots': total_mots,
        'voix_seule_s': round(voix_seule, 1),
        'fin_derniere_sequence_s': round(fin_derniere_sequence, 1),
        'fin_avec_silence_s': round(total_sec, 1),
        'total_s': round(total_sec, 1),
        'sequences': seq_json,
        'plages_hors_voix': hors_voix,
    }
    with open(dossier + '/durees.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(sortie, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('écrit')
