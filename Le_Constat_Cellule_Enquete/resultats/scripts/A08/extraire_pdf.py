# A08 - extraction texte de PDF (pymupdf), page par page, marqueurs [[p.N]]
# usage : python -I extraire_pdf.py <dossier>
import sys, pathlib, pymupdf
d = pathlib.Path(sys.argv[1])
for f in sorted(d.glob('*.pdf')):
    out = f.with_suffix('.txt')
    if out.exists():
        continue
    try:
        doc = pymupdf.open(f)
        out.write_text('\n'.join(f'[[p.{i+1}]]\n' + p.get_text() for i, p in enumerate(doc)), encoding='utf8')
        print(f.name, doc.page_count)
    except Exception as e:
        print('ERREUR', f.name, e)
