"""Conservation des pieces de D04 dans la limite de taille (20 Mo par fichier, 120 Mo au total).
Pour chaque rapport de la Commission des comptes de la securite sociale (CCSS) cite :
 - extrait PDF des pages citees (+/- 1 page), ecrit dans ../../donnees/D04/sources/ ;
 - texte integral extrait (pymupdf, marqueurs '=== PAGE PDF N ===') copie a cote ;
 - empreintes SHA-256 de l'original telecharge, de l'extrait et du texte, dans MANIFESTE_PIECES.csv.
Usage : python -I d04_pieces.py <dossier_des_originaux_telecharges>
Les originaux sont telechargeables a l'adresse indiquee (site securite-sociale.fr)."""
import os, sys, hashlib, shutil, csv, glob
import pymupdf

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, '..', '..', 'donnees', 'D04', 'sources')
BASE = 'https://www.securite-sociale.fr/files/live/sites/SSFR/files/medias/'
DATE = '2026-11-22'
PIECES = [  # (fichier original, chemin URL, pages citees)
    ('CCSS-RAPPORT-NOVEMBRE_1983.pdf', 'CCSS/1983/RAPPORT/CCSS-RAPPORT-NOVEMBRE_1983.pdf', [97, 98, 99, 100, 101]),
    ('CCSS-RAPPORT-DECEMBRE_1985.pdf', 'CCSS/1985/RAPPORT/CCSS-RAPPORT-DECEMBRE_1985.pdf', [74, 124]),
    ('CCSS-RAPPORT-DECEMBRE_1986.pdf', 'CCSS/1986/RAPPORT/CCSS-RAPPORT-DECEMBRE_1986.pdf', [17, 27]),
    ('CCSS-RAPPORT-DECEMBRE_1987.pdf', 'CCSS/1987/RAPPORT/CCSS-RAPPORT-DECEMBRE_1987.pdf', [24]),
    ('CCSS-RAPPORT-NOVEMBRE_1989.pdf', 'CCSS/1989/RAPPORT/CCSS-RAPPORT-NOVEMBRE_1989.pdf', [14, 19, 20, 21]),
    ('CCSS-RAPPORT-FEVRIER_1991.pdf', 'CCSS/1991/RAPPORT/CCSS-RAPPORT-FEVRIER_1991.pdf', [9, 17, 18, 19, 20, 21]),
    ('CCSS-RAPPORT-JUIN_1991.pdf', 'CCSS/1991/RAPPORT/CCSS-RAPPORT-JUIN_1991.pdf', [26, 37]),
    ('CCSS-RAPPORT-JUILLET_1992.pdf', 'CCSS/1992/RAPPORT/CCSS-RAPPORT-JUILLET_1992.pdf', [89, 98]),
    ('CCSS-RAPPORT-DECEMBRE_1993.pdf', 'CCSS/1993/RAPPORT/CCSS-RAPPORT-DECEMBRE_1993.pdf', [13, 14, 17, 40]),
    ('CCSS-RAPPORT-OCTOBRE_1994.pdf', 'CCSS/1994/RAPPORT/CCSS-RAPPORT-OCTOBRE_1994.pdf', [89]),
    ('CCSS-RAPPORT-OCTOBRE_1995.pdf', 'CCSS/1995/RAPPORT/CCSS-RAPPORT-OCTOBRE_1995.pdf', [36, 108, 111, 112]),
    ('CCSS-RAPPORT-SEPTEMBRE_1996.pdf', 'CCSS/1996/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_1996.pdf', [94, 99, 337]),
    ('CCSS-RAPPORT-SEPTEMBRE_1997.pdf', 'CCSS/1997/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_1997.pdf', [151, 159]),
    ('CCSS-RAPPORT-SEPTEMBRE_1998.pdf', 'CCSS/1998/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_1998.pdf', [26, 27, 46, 48, 49, 74, 127, 276]),
    ('CCSS-RAPPORT-SEPTEMBRE_2000.pdf', 'CCSS/2000/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_2000.pdf', [32, 57, 58, 93, 114, 115]),
    ('CCSS-RAPPORT-SEPTEMBRE_2003-PARTIE_1.pdf', 'CCSS/2003/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_2003-PARTIE_1.pdf', [97]),
    ('CCSS-RAPPORT-SEPTEMBRE_2006-PARTIE_1.pdf', 'CCSS/2006/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_2006-PARTIE_1.pdf', [13, 38, 104, 105]),
    ('CCSS-RAPPORT-OCTOBRE_2009.pdf', 'CCSS/2009/RAPPORT/CCSS-RAPPORT-OCTOBRE_2009.pdf', [58, 92]),
    ('CCSS-RAPPORT-OCTOBRE_2012.pdf', 'CCSS/2012/RAPPORT/CCSS-RAPPORT-OCTOBRE_2012.pdf', [49, 50, 62, 66]),
    ('CCSS-RAPPORT-SEPTEMBRE_2015.pdf', 'CCSS/2015/RAPPORT/CCSS-RAPPORT-SEPTEMBRE_2015.pdf', [45]),
    ('CCSS_RAPPORT-SEPTEMBRE_2018.pdf', 'CCSS/2018/CCSS_RAPPORT-SEPTEMBRE%202018.pdf', [6, 12, 34, 35, 38, 59]),
    ('CCSS_SEPT_2019.pdf', 'CCSS/2019/CCSS%20SEPT%2019%20DEF.pdf', [20, 22, 52, 65]),
    ('Rapport_CCSS-Septembre2021.pdf', 'CCSS/2021/Rapport%20CCSS-Septembre2021.pdf', [65]),
    ('CCSS-octobre_2024.pdf', 'CCSS/2024/CCSS-octobre%202024.pdf', [54, 121]),
    ('CCSS-octobre-2026_assemble_VDEF.pdf', 'CCSS/2026/CCSS-octobre-2026_assemble_VDEF.pdf', [67, 68, 69, 70]),
]

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def trouver(dossier, nom):
    r = glob.glob(os.path.join(dossier, '**', nom), recursive=True)
    return r[0] if r else None

def main(dossier):
    os.makedirs(OUT, exist_ok=True)
    man = []
    for nom, chemin, pages in PIECES:
        src = trouver(dossier, nom)
        if not src:
            print('absent :', nom); continue
        doc = pymupdf.open(src)
        garder = sorted({p for q in pages for p in (q - 1, q, q + 1) if 1 <= p <= len(doc)})
        ext = pymupdf.open()
        for p in garder:
            ext.insert_pdf(doc, from_page=p - 1, to_page=p - 1)
        base = nom[:-4]
        out_pdf = os.path.join(OUT, base + '_extrait.pdf')
        ext.save(out_pdf, garbage=4, deflate=True)
        out_txt = os.path.join(OUT, base + '.txt')
        shutil.copyfile(src[:-4] + '.txt', out_txt)
        url = BASE + chemin
        man.append([base + '_extrait.pdf', url, DATE, sha(out_pdf),
                    f"extrait des pages PDF {','.join(map(str, garder))} (pages citees +/- 1) ; original de {len(doc)} pages, "
                    f"{os.path.getsize(src)} octets, SHA-256 {sha(src)}"])
        man.append([base + '.txt', url, DATE, sha(out_txt), 'texte integral extrait par pymupdf (d04_extraire.py) de l\'original'])
        print(nom, garder, os.path.getsize(out_pdf))
    return man

if __name__ == '__main__':
    lignes = main(sys.argv[1])
    autres = os.path.join(ICI, '..', '..', 'donnees', 'D04', 'MANIFESTE_autres.csv')
    if os.path.exists(autres):
        with open(autres, encoding='utf-8') as h:
            for l in list(csv.reader(h, delimiter=';'))[1:]:
                p = os.path.join(ICI, '..', '..', 'donnees', 'D04', l[0])
                if l[3] == 'voir fichier' and os.path.exists(p):
                    l[3] = sha(p)
                lignes.append(l)
    with open(os.path.join(ICI, '..', '..', 'donnees', 'D04', 'MANIFESTE_PIECES.csv'), 'w', encoding='utf-8', newline='') as h:
        w = csv.writer(h, delimiter=';')
        w.writerow(['fichier', 'url', 'date_acces', 'sha256', 'description'])
        w.writerows(lignes)
