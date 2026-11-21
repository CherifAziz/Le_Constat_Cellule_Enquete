"""A09 - Composition des législatures V à XIV (1973-2017) à leur ouverture, d'après les pages
« Tous les députés depuis 1958 » de l'Assemblée nationale (www2.assemblee-nationale.fr).
Chaque page liste les députés « à la date du » début de législature avec leur groupe politique.
On compte les membres et apparentés (préfixe « App. ») par sigle de groupe.
Usage : python -I a09_legislatures_an.py <dossier_sources> <fichier_csv_sortie>
(sortie utilisée : resultats/donnees/A09/a09_composition_legislatures_V_X.csv)
"""
import sys, os, re, csv, time, unicodedata
import requests
from bs4 import BeautifulSoup

SRC, OUTCSV = sys.argv[1], sys.argv[2]
D = os.path.join(SRC, 'an_legislatures'); os.makedirs(D, exist_ok=True)
BASE = 'https://www2.assemblee-nationale.fr/decouvrir-l-assemblee/histoire/la-ve-republique/tous-les-deputes-depuis-1958/'
LEGS = {
    5: 'Ve législature (2 avril 1973 - 2 avril 1978)',
    6: 'VIe législature (3 avril 1978 - 22 mai 1981)',
    7: 'VIIe législature (2 juillet 1981 - 1er avril 1986)',
    8: 'VIIIe législature (2 avril 1986 - 14 mai 1988)',
    9: 'IXe législature (23 juin 1988 - 1er avril 1993)',
    10: 'Xe législature (2 avril 1993 - 21 avril 1997)',
    11: 'XIe législature (1er juin 1997 - 18 juin 2002)',
    12: 'XIIe législature (19 juin 2002 - 19 juin 2007)',
    13: 'XIIIe législature (20 juin 2007 - 19 juin 2012)',
    14: 'XIVe législature (20 juin 2012 - 20 juin 2017)',
}


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


rows = []
for leg, lib in LEGS.items():
    url = BASE + slug(lib)
    p = os.path.join(D, f'leg{leg:02d}.html')
    if not os.path.exists(p) or os.path.getsize(p) < 70000:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=60)
        open(p, 'wb').write(r.content); time.sleep(0.5)
        print(leg, r.status_code, len(r.content), url)
    html = open(p, encoding='utf-8', errors='replace').read()
    toks = BeautifulSoup(html, 'html.parser').get_text('|', strip=True).split('|')
    try:
        i0 = next(i for i, t in enumerate(toks) if t.startswith('LISTE ALPHAB'))
    except StopIteration:
        print('liste absente', leg); continue
    date = next((t for t in toks if t.startswith('(à la date du')), '')
    counts = {}
    n = 0
    for t in toks[i0 + 1:]:
        if t.startswith('Haut de page') or t.startswith('Retour') or t.startswith('Imprimer'):
            break
        if len(t) == 1:
            continue  # lettres de l'alphabet
        m = re.match(r"^(.+?)\s+(App\.\s+)?([A-Z][A-Za-z0-9.\-/&']*(?:\s[A-Z]{1,6})?)\s+(\S.*)$", t)
        # repérage plus robuste : sigle = premier jeton entièrement en majuscules (avec . - /)
        parts = t.split()
        sig = None; app = False
        for k, w in enumerate(parts[1:], start=1):
            if w == 'App.':
                app = True; continue
            if re.fullmatch(r"[A-Z][A-Z0-9.\-/]*[A-Z.]|[A-Z]", w) and k >= 1:
                # éviter les initiales de prénoms comme « J.-P. »
                if re.fullmatch(r"[A-Z]\.(-[A-Z]\.)?", w):
                    continue
                sig = w; break
        if sig is None:
            continue
        n += 1
        key = sig
        counts.setdefault(key, [0, 0])
        counts[key][1 if app else 0] += 1
    # filtre : les jetons de pied de page (DATA, LEXIMPACT, SEMAINE…) apparaissent une fois ; on ne garde
    # que les sigles comptant au moins 5 députés, et seulement les législatures dont la page donne les groupes
    counts = {g: v for g, v in counts.items() if sum(v) >= 5}
    if not counts:
        print(leg, 'page sans groupes politiques (liste de noms seulement)'); continue
    for g, (mem, app) in sorted(counts.items(), key=lambda x: -sum(x[1])):
        rows.append({'legislature': leg, 'libelle': lib, 'date_liste': date, 'sigle': g,
                     'membres': mem, 'apparentes': app, 'total': mem + app, 'url': BASE + slug(lib)})
    print(leg, date, n, sorted(((g, sum(v)) for g, v in counts.items()), key=lambda x: -x[1])[:12])

with open(OUTCSV, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';')
    w.writeheader(); w.writerows(rows)
