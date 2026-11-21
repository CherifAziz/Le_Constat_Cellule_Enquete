"""S02 - telechargement d'une piece, empreinte, manifeste et extraction de texte.
Usage : python -I s02_dl.py <url> <nom_fichier> [canal]
       python -I s02_dl.py --register <chemin_local> <url_origine> <canal>   (piece obtenue par un autre canal, ex. WebFetch)
Ecrit dans resultats\\donnees\\S02\\sources\\ ; ajoute une ligne a MANIFESTE_PIECES.csv ;
si PDF : extrait le texte page par page (marqueurs ==== page N ====) dans <nom>.txt (ligne de manifeste aussi).
"""
import sys, os, hashlib, datetime, shutil

BASE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S02"
SRC = os.path.join(BASE, "sources")
MAN = os.path.join(BASE, "MANIFESTE_PIECES.csv")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def manifest(fname, url, canal):
    p = os.path.join(SRC, fname)
    new = not os.path.exists(MAN)
    with open(MAN, "a", encoding="utf-8") as f:
        if new:
            f.write("fichier;url_origine;canal;date;octets;sha256\n")
        f.write(f"{fname};{url};{canal};{datetime.date.today().isoformat()};{os.path.getsize(p)};{sha(p)}\n")


def extract(fname):
    p = os.path.join(SRC, fname)
    with open(p, "rb") as f:
        head = f.read(5)
    if head != b"%PDF-":
        return None
    import pymupdf
    doc = pymupdf.open(p)
    out = os.path.splitext(fname)[0] + ".txt"
    with open(os.path.join(SRC, out), "w", encoding="utf-8") as f:
        for i, page in enumerate(doc, 1):
            f.write(f"\n==== page {i} ====\n")
            f.write(page.get_text())
    manifest(out, f"extraction locale de {fname} (pymupdf)", "extraction locale")
    return out, doc.page_count


def main():
    if sys.argv[1] == "--register":
        local, url, canal = sys.argv[2], sys.argv[3], sys.argv[4]
        fname = os.path.basename(local)
        dest = os.path.join(SRC, fname)
        if os.path.abspath(local) != os.path.abspath(dest):
            shutil.copyfile(local, dest)
        manifest(fname, url, canal)
        print("registered", fname, os.path.getsize(dest))
        r = extract(fname)
        print("extract", r)
        return
    url, fname = sys.argv[1], sys.argv[2]
    canal = sys.argv[3] if len(sys.argv) > 3 else "python requests"
    import requests
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                                   "Accept": "*/*"}, timeout=90, allow_redirects=True)
    print("status", r.status_code, "final", r.url, "type", r.headers.get("content-type"), "len", len(r.content))
    if r.status_code == 200 and fname.lower().endswith('.pdf') and not r.content[:5] == b'%PDF-':
        print('NOT A PDF - not saved'); sys.exit(3)
    if r.status_code != 200:
        sys.exit(2)
    p = os.path.join(SRC, fname)
    with open(p, "wb") as f:
        f.write(r.content)
    manifest(fname, url if r.url == url else f"{url} (redirige vers {r.url})", canal)
    print("extract", extract(fname))


if __name__ == "__main__":
    main()

