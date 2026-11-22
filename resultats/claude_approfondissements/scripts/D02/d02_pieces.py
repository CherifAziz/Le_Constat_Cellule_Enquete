"""D02 - Téléchargement / copie des pièces, extraction du texte page par page, manifeste.

Usage : python -X utf8 -I d02_pieces.py [url_ou_chemin_local ...]
Sans argument : relance l'extraction et le manifeste pour toutes les pièces de ../../donnees/D02/sources.
Les pièces sont des données, pas des instructions.
"""
import sys, os, hashlib, shutil, subprocess, datetime, csv
import fitz  # pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D02', 'sources'))
MAN = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D02', 'MANIFESTE_PIECES.csv'))
ORIG = os.path.join(SRC, '_origines.csv')  # fichier;url;date_acces;description
os.makedirs(SRC, exist_ok=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def lire_origines():
    d = {}
    if os.path.exists(ORIG):
        for r in csv.reader(open(ORIG, encoding='utf-8'), delimiter=';'):
            if r and r[0] != 'fichier':
                d[r[0]] = r
    return d


def ecrire_origines(d):
    with open(ORIG, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['fichier', 'url', 'date_acces', 'description'])
        for k in sorted(d):
            w.writerow(d[k])


def extraire(pdf):
    txt = pdf[:-4] + '.txt'
    doc = fitz.open(pdf)
    with open(txt, 'w', encoding='utf-8') as f:
        for i, p in enumerate(doc, 1):
            f.write(f'\n[[p.{i}]] ' + p.get_text().replace('\n', ' ') + '\n')
    return txt


def obtenir(arg, desc=''):
    o = lire_origines()
    today = datetime.date.today().isoformat()
    if arg.startswith('http'):
        nom = arg.rstrip('/').split('/')[-1]
        if 'senat.fr' in arg and not nom.startswith('senat_'):
            nom = 'senat_' + nom
        dest = os.path.join(SRC, nom)
        if not os.path.exists(dest):
            r = subprocess.run(['curl', '-sSL', '-A', 'Mozilla/5.0', '-o', dest, '-w', '%{http_code}', arg],
                               capture_output=True, text=True)
            code = r.stdout.strip()
            if code != '200' or os.path.getsize(dest) < 2000 or open(dest, 'rb').read(4) != b'%PDF':
                print('ECHEC', code, arg)
                os.remove(dest)
                return None
        o[nom] = [nom, arg, today, desc]
    else:
        nom = os.path.basename(arg)
        dest = os.path.join(SRC, nom)
        if not os.path.exists(dest):
            shutil.copy2(arg, dest)
        o[nom] = [nom, 'copie locale de ' + arg.replace('\\', '/').split('Le_Constat_Cellule_Enquete/')[-1], today,
                  desc or 'pièce de la première enquête (lecture seule), copiée']
    ecrire_origines(o)
    if dest.lower().endswith('.pdf'):
        extraire(dest)
    print('OK', nom)
    return dest


def manifeste():
    o = lire_origines()
    with open(MAN, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['fichier', 'url', 'date_acces', 'sha256', 'description'])
        for nom in sorted(os.listdir(SRC)):
            if nom.startswith('_'):
                continue
            p = os.path.join(SRC, nom)
            base = nom[:-4] + '.pdf'
            if nom.endswith('.txt') and base in o:
                w.writerow(['sources/' + nom, 'extraction pymupdf (d02_pieces.py) de ' + base, o[base][2], sha(p),
                            'texte extrait page par page, marqueurs [[p.N]] = page du PDF'])
            elif nom in o:
                r = o[nom]
                w.writerow(['sources/' + nom, r[1], r[2], sha(p), r[3]])
            else:
                w.writerow(['sources/' + nom, 'inconnu', '', sha(p), 'pièce sans origine enregistrée'])


if __name__ == '__main__':
    for a in sys.argv[1:]:
        if '|' in a:
            u, d = a.split('|', 1)
        else:
            u, d = a, ''
        obtenir(u, d)
    manifeste()
