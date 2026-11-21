"""A09 - Découpe un compte rendu de séance de l'AN (texte extrait du HTML) en interventions
et compte, pour chaque orateur principal (intervention > SEUIL caractères), les mentions de
familles de thèmes. Sert à lire ce que les explications de vote invoquent, pas à mesurer une
intention. Usage : python -I a09_explications_censure.py <fichier.txt> [debut_motif] [fin_motif]
Sortie : tableau sur stdout ; extraits « retraites » dans <fichier>_retraites.txt.
"""
import sys, re

SEUIL = 2500
THEMES = {
    'retraites': r'retraite|retraité|pension|indexation|d[ée]sindex|r[ée]forme des retraites|64 ans|62 ans|[âa]ge l[ée]gal',
    'sante_medic': r'm[ée]dicament|d[ée]rembours|h[ôo]pita|sant[ée]',
    'energie': r'[ée]lectricit|[ée]nergie|gaz\b|carburant',
    'impots': r'imp[ôo]t|fiscal|taxe|pr[ée]l[èe]vement',
    'dette_deficit': r'\bdette|d[ée]ficit|faillite|march[ée]s financiers|taux d.int[ée]r[êe]t|spread',
    'methode_493': r'49\.3|49-3|49, alin[ée]a 3|passage en force|m[ée]pris',
    'collectivites': r'collectivit|communes|d[ée]partements',
    'immigration': r'immigr|AME\b|aide m[ée]dicale',
}

path = sys.argv[1]
t = open(path, encoding='utf-8').read().replace('⁠', '').replace('\xa0', ' ')
if len(sys.argv) > 2:
    # motif@n : n-ième occurrence (1 = première) ; le sommaire contient souvent la première
    motif, _, n = sys.argv[2].partition('@')
    i = -1
    for _ in range(int(n or 1)):
        i = t.find(motif, i + 1)
    t = t[i:] if i >= 0 else t
if len(sys.argv) > 3:
    j = t.find(sys.argv[3]); t = t[:j] if j >= 0 else t
lines = t.split('\n')
speeches = []
cur = None
for k, l in enumerate(lines):
    if k + 1 < len(lines) and lines[k + 1].startswith("Partager l'intervention"):
        cur = {'orateur': l.strip(), 'texte': []}
        speeches.append(cur)
        continue
    if l.startswith("Partager l'intervention") or l == 'partager' or l.startswith(','):
        if l.startswith(',') and cur is not None:
            cur['orateur'] += ' ' + l.strip()
        continue
    if cur is not None and not l.startswith('('):
        cur['texte'].append(l)

agg = {}
for s in speeches:
    key = re.sub(r'\s+', ' ', s['orateur'])
    agg.setdefault(key, []).append(' '.join(s['texte']))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
print('orateur;caracteres;' + ';'.join(THEMES))
out = open(path.replace('.txt', '_retraites.txt'), 'w', encoding='utf-8')
for k, v in agg.items():
    txt = ' '.join(v)
    if len(txt) < SEUIL or k.startswith('Mme la présidente') or k.startswith('M. le président'):
        continue
    c = [len(re.findall(p, txt, re.I)) for p in THEMES.values()]
    print(f'{k[:70]};{len(txt)};' + ';'.join(map(str, c)))
    for m in re.finditer(THEMES['retraites'], txt, re.I):
        out.write(f'[{k[:60]}] ...{txt[max(0, m.start() - 250):m.end() + 250]}...\n')
out.close()
