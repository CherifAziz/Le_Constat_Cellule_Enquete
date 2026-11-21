"""C03 - relevé d'empreintes SHA-256 (lecture seule) d'un dossier.
Usage : python -I c03_empreintes.py <dossier> <sortie.csv>
N'écrit que le fichier de sortie (à placer sous resultats\\donnees\\C03\\empreintes\\).
"""
import hashlib, os, sys

def main():
    racine, sortie = sys.argv[1], sys.argv[2]
    lignes = []
    for d, _, fs in os.walk(racine):
        for f in fs:
            p = os.path.join(d, f)
            h = hashlib.sha256()
            with open(p, 'rb') as fh:
                for bloc in iter(lambda: fh.read(1 << 20), b''):
                    h.update(bloc)
            st = os.stat(p)
            lignes.append((os.path.relpath(p, racine), st.st_size, int(st.st_mtime), h.hexdigest()))
    lignes.sort()
    with open(sortie, 'w', encoding='utf-8', newline='') as o:
        o.write('fichier;octets;mtime;sha256\n')
        for l in lignes:
            o.write(';'.join(str(x) for x in l) + '\n')
    print(len(lignes), 'fichiers ->', sortie)

if __name__ == '__main__':
    main()
