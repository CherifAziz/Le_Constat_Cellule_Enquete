# -*- coding: utf-8 -*-
"""Produit 07_TEXTE_ELEVENLABS.md (texte balisé prêt à coller dans ElevenLabs v3/v4) à partir de
01_SCRIPT_VOIX_OFF.md, et vérifie qu'aucune balise susceptible de faire chuchoter n'y figure.

Usage : python preparer_elevenlabs.py <dossier script_documentaire_hybride> [--ecrire]

Le texte dit n'est pas modifié, sauf sur trois points :
- (pause) devient [short pause] et (silence) devient [long pause] ;
- les nombres que la synthèse lit mal sont écrits en toutes lettres (pourcentages, décimales,
  milliers, « 1er », « 49.3 ») ; les années et les petits entiers restent en chiffres ;
- chaque bloc commence par une balise de ton, toujours en voix pleine.
Bibliothèque standard seulement.
"""
import re
import sys

dossier = sys.argv[1]
ecrire = '--ecrire' in sys.argv
MAX_CARACTERES = 2800   # marge sous la limite d'une génération Eleven v3

# Balises interdites : tout ce qui peut faire baisser la voix, chuchoter ou souffler.
INTERDITES = ['whisper', 'soft', 'quiet', 'hush', 'murmur', 'breath', 'intimate', 'low voice',
              'mysterious', 'secret', 'sigh', 'exhale', 'asmr', 'gentle', 'sleepy', 'tired', 'sad',
              'somber', 'sombre', 'melanchol', 'fragile', 'trembl', 'nervous', 'cry', 'sob']

VOIX = 'steady, full-voiced male documentary narrator'
TONS = {
    'Ouverture': 'confident, engaging, clear',
    'Les ciseaux': 'clear, explanatory',
    'La remontée': 'clear, explanatory',
    'Trente francs': 'curious, investigative',
    'Novembre 1980': 'deliberate, reading an official document aloud',
    'Faisons le compte': 'matter-of-fact, firm',
    'Ce que ces années laissent': 'warm, explanatory',
    'Dos au mur': 'energetic, clear',
    'Printemps 2000': 'curious, investigative',
    'La colonne éteinte': 'matter-of-fact, firm',
    'Les promesses écrites': 'firm, slightly ironic',
    'Troisième fois': 'clear, brisk',
    'Le levier déjà tiré': 'direct, clear',
    "Où est l'argent": 'direct, clear',
    'Septembre 2023': 'direct, clear',
    "L'effort retiré": 'firm, matter-of-fact',
    'Le compte': 'measured, precise, clear',
    'Stockholm': 'engaged storytelling',
    'Le vent dans le dos': 'honest, matter-of-fact',
    'Ce qui se transpose': 'thoughtful, clear',
    'Une pension': 'concrete, conversational',
    'Une addition': 'concrete, conversational',
    'Deux personnes de soixante ans': 'concrete, warm',
    'Quatorze ans plus tard': 'firm, clear',
    'Conclusion': 'firm, measured, conclusive',
}

UNITES = ['zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze',
          'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf']
DIZAINES = {2: 'vingt', 3: 'trente', 4: 'quarante', 5: 'cinquante', 6: 'soixante'}


def moins_de_cent(n):
    if n < 20:
        return UNITES[n]
    d, u = divmod(n, 10)
    if d in (7, 9):
        base = 'soixante' if d == 7 else 'quatre-vingt'
        reste = 10 + u
        if d == 7 and u == 1:
            return 'soixante et onze'
        return base + '-' + UNITES[reste]
    if d == 8:
        return 'quatre-vingts' if u == 0 else 'quatre-vingt-' + UNITES[u]
    if u == 0:
        return DIZAINES[d]
    if u == 1:
        return DIZAINES[d] + ' et un'
    return DIZAINES[d] + '-' + UNITES[u]


def moins_de_mille(n):
    c, r = divmod(n, 100)
    if c == 0:
        return moins_de_cent(r)
    tete = 'cent' if c == 1 else UNITES[c] + (' cents' if r == 0 else ' cent')
    return tete if r == 0 else tete + ' ' + moins_de_cent(r)


def en_lettres(n):
    if n < 1000:
        return moins_de_mille(n)
    m, r = divmod(n, 1000)
    tete = 'mille' if m == 1 else moins_de_mille(m) + ' mille'
    return tete if r == 0 else tete + ' ' + moins_de_mille(r)


def decimale(e, d):
    return en_lettres(int(e)) + ' virgule ' + (' '.join(UNITES[int(c)] for c in d) if d.startswith('0') else en_lettres(int(d)))


def normaliser(t):
    t = t.replace(' ', ' ').replace(' ', ' ')
    t = re.sub(r'\b1er\b', 'premier', t)
    t = t.replace('49.3', 'quarante-neuf trois')
    # 7,5 milliards -> sept milliards et demi
    t = re.sub(r'\b(\d+),5 milliards', lambda m: en_lettres(int(m.group(1))) + ' milliards et demi', t)
    # pourcentages
    t = re.sub(r'\b(\d+),(\d+) ?%', lambda m: decimale(m.group(1), m.group(2)) + ' pour cent', t)
    t = re.sub(r'\b(\d{1,3}(?: \d{3})*) ?%', lambda m: en_lettres(int(m.group(1).replace(' ', ''))) + ' pour cent', t)
    # décimales restantes
    t = re.sub(r'\b(\d+),(\d+)\b', lambda m: decimale(m.group(1), m.group(2)), t)
    # milliers écrits avec espace (3 000, 1 300…)
    t = re.sub(r'\b(\d{1,3}) (\d{3})\b', lambda m: en_lettres(int(m.group(1) + m.group(2))), t)
    return t


def baliser(t):
    t = t.replace('(pause)', '[short pause]').replace('(silence)', '[long pause]')
    t = t.replace('…', ',')
    t = re.sub(r'  +', ' ', t).strip()
    # majuscule en début de phrase après une conversion en lettres (« premier août… »)
    return re.sub(r'(^|[.!?\]] )([a-zéè])', lambda m: m.group(1) + m.group(2).upper(), t)


# --- lecture de 01 ---------------------------------------------------------------------
src = open(dossier + '/01_SCRIPT_VOIX_OFF.md', encoding='utf-8').read()
corps = src[src.index('## Ouverture'):]
sequences = []
for ligne in corps.split('\n'):
    l = ligne.strip()
    if l.startswith('## ') and not l[3:].startswith('Acte'):
        sequences.append([l[3:].strip(), []])
    elif l.startswith('### '):
        sequences.append([l[4:].split('·', 1)[-1].strip(), []])
    elif l and l != '---' and not l.startswith('#') and sequences:
        sequences[-1][1].append(l)

blocs = []   # (titre, numéro de partie, texte)
for titre, paras in sequences:
    if titre not in TONS:
        sys.exit('Ton manquant pour la séquence : ' + titre)
    tete = '[%s] [%s]' % (VOIX, TONS[titre])
    paras = [baliser(normaliser(p)) for p in paras]
    courant, parties = [], []
    for p in paras:
        essai = '\n\n'.join([tete] + courant + [p])
        if courant and len(essai) > MAX_CARACTERES:
            parties.append(courant)
            courant = []
        courant.append(p)
    parties.append(courant)
    for i, ps in enumerate(parties, 1):
        blocs.append((titre, i if len(parties) > 1 else 0, '\n\n'.join([tete] + ps)))

# --- contrôles ---------------------------------------------------------------------------
erreurs = []
for titre, i, texte in blocs:
    for balise in re.findall(r'\[([^\]]+)\]', texte):
        for mot in INTERDITES:
            if mot in balise.lower():
                erreurs.append('%s : balise interdite [%s]' % (titre, balise))
    if len(texte) > MAX_CARACTERES:
        erreurs.append('%s : %d caractères' % (titre, len(texte)))
    for reste in re.findall(r'\d+ ?%|\d,\d|\d \d{3}|\(pause\)|\(silence\)', texte):
        erreurs.append('%s : non converti « %s »' % (titre, reste))
if erreurs:
    print('\n'.join(erreurs))
    sys.exit(1)
print('%d blocs, plus long : %d caractères. Aucune balise interdite, aucun nombre à risque.'
      % (len(blocs), max(len(b[2]) for b in blocs)))

if ecrire:
    s = ['# 07 · Texte ElevenLabs — *Avant la ligne* (version hybride)', '',
         'Extrait automatiquement de [01_SCRIPT_VOIX_OFF.md](01_SCRIPT_VOIX_OFF.md) par `outils/preparer_elevenlabs.py`. '
         'Ne pas modifier à la main : corriger 02, puis relancer `construire_script.py` et ce programme.', '',
         '## Réglages', '',
         '- **Modèle** : Eleven v3 (ou v4), le même pour tous les blocs.',
         '- **Voix** : voix masculine française de narration, la même pour tous les blocs.',
         '- **Stabilité** : « Natural ». Éviter « Creative », qui laisse plus de liberté d\'interprétation (chuchotements, souffle).',
         '- **Vitesse** : 1,0. La durée du script est calculée à 182 mots par minute ; noter la vitesse retenue.',
         '- **Un bloc par génération**, dans l\'ordre ; nommer chaque fichier par son numéro (`01_ouverture.mp3`…).',
         '- Si un bloc sort trop bas ou soufflé, le régénérer tel quel ; ne jamais ajouter de balise d\'émotion douce.', '',
         '## Ce qui a été fait au texte', '',
         '- Aucun mot dit n\'a été changé.',
         '- `(pause)` → `[short pause]` ; `(silence)` → `[long pause]`.',
         '- Pourcentages, décimales, milliers, « 1er » et « 49.3 » écrits en toutes lettres. Les années restent en chiffres.',
         '- Chaque bloc commence par `[%s]` puis une balise de ton.' % VOIX,
         '- **Balises exclues** (contrôle automatique) : tout ce qui contient ' + ', '.join('« %s »' % m for m in INTERDITES) + '. Pas de points de suspension.', '',
         '---', '']
    for n, (titre, i, texte) in enumerate(blocs, 1):
        nom = titre + (' (partie %d)' % i if i else '')
        s += ['## %02d · %s' % (n, nom), '', '```text', texte, '```', '']
    open(dossier + '/07_TEXTE_ELEVENLABS.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(s).rstrip() + '\n')
    print('écrit')
