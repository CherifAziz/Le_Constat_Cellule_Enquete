# -*- coding: utf-8 -*-
"""Produit 01_SCRIPT_V6.md (voix seule) à partir de 02_SCRIPT_ANNOTE.md et mesure les durées.

Usage : python construire_script.py <dossier script_documentaire_v6> [--ecrire]
Convention de durée : 182 mots par minute ; (pause) = 1 s ; (silence) = 2,5 s ;
0,5 s de respiration entre deux paragraphes dits.
"""
import re
import sys
import json

dossier = sys.argv[1]
ecrire = '--ecrire' in sys.argv
src = open(dossier + '/02_SCRIPT_ANNOTE.md', encoding='utf-8').read()

debut = src.index('## Ouverture')
corps = src[debut:]

MOTS_MIN = 182.0
sequences = []  # (acte, titre, [paragraphes])
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


lignes_stats = []
total_mots = 0
total_sec = 0.0
for a, t, paras in sequences:
    texte = ' '.join(paras)
    n = mots(texte)
    pauses = len(re.findall(r'\(pause\)', texte))
    silences = len(re.findall(r'\(silence\)', texte))
    # les silences notés dans les indications (titre, fin) sont comptés à part
    sec = n / MOTS_MIN * 60 + pauses * 1.0 + silences * 2.5 + max(0, len(paras) - 1) * 0.5
    total_mots += n
    total_sec += sec
    lignes_stats.append((a, t, n, len(paras), pauses + silences, sec))

# silences hors voix : titre (4 s), fin (3 s)
hors_voix = 7.0
total_sec += hors_voix


def mmss(s):
    s = int(round(s))
    return '%d:%02d' % (s // 60, s % 60)


print('%-34s %6s %5s %6s %7s %8s' % ('séquence', 'mots', 'par.', 'pauses', 'durée', 'cumul'))
cumul = 0.0
out = []
for a, t, n, p, pa, sec in lignes_stats:
    debut_seq = cumul
    cumul += sec
    if t == 'Ouverture':
        cumul += 4.0
    print('%-34s %6d %5d %6d %7s %8s' % (t[:34], n, p, pa, mmss(sec), mmss(cumul)))
    out.append({'acte': a, 'titre': t, 'mots': n, 'duree_s': round(sec, 1), 'debut_s': round(debut_seq, 1), 'fin_s': round(cumul, 1)})
print('TOTAL mots', total_mots, 'durée', mmss(total_sec), '(voix seule à 182 mots/min :', mmss(total_mots / MOTS_MIN * 60), ')')

# chiffres dits par séquence (hors années et dates)
print()
for a, t, paras in sequences:
    texte = ' '.join(paras)
    texte = re.sub(r'\b(19|20)\d\d\b', '', texte)
    texte = re.sub(r'\b1er\b|\b\d{1,2} (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\b', '', texte)
    ch = re.findall(r'\d[\d ,]*\d|\d', texte)
    print('%-34s chiffres écrits en chiffres : %d %s' % (t[:34], len(ch), ch))

if ecrire:
    s = ['# 01 · Script V6 — *Avant la ligne*', '',
         '**22 novembre 2026. Première version complète de la voix off.** Texte seul, tel qu\'il est dit. '
         'Les indications d\'image et d\'archive sont dans [02_SCRIPT_ANNOTE.md](02_SCRIPT_ANNOTE.md), dont ce fichier est extrait automatiquement.', '',
         '`(pause)` : respiration marquée, environ une seconde. `(silence)` : deux à trois secondes sans voix.', '',
         '**%d mots. Durée estimée : %s** (182 mots par minute, pauses et respirations comprises).' % (total_mots, mmss(total_sec)), '', '---', '']
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
    json.dump({'total_mots': total_mots, 'total_s': round(total_sec, 1), 'sequences': out},
              open(dossier + '/durees.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('écrit')
