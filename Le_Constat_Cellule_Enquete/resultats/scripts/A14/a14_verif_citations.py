"""Verifie que chaque citation entre guillemets francais de A14.md et de l'annexe figure mot pour mot
dans au moins une des pieces texte locales (normalisation des espaces, cesures, apostrophes).
Usage : python -I a14_verif_citations.py"""
import re, glob, unicodedata
def norm(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()
srcs = glob.glob("donnees/A14/sources/*.txt") + ["donnees/A03/sources/PLF2027_RESF.txt", "donnees/A07/sources/DP_BUDGET_2027.txt",
        "donnees/A04/sources/bozio_wasmer_2024_vp295596.txt", "donnees/A04/sources/ipp_note32_TVA_restauration_2018.txt",
        "donnees/A04/sources/hcfips_fraude_sociale_synthese_2026.txt", "donnees/A04/sources/PLF2026_VM_tome2.txt", "donnees/A04/sources/insee_ip/ip2106.txt",
        "donnees/A04/sources/cnepi_CIR_2021_vp280151.txt"]
corpus = {p: norm(open(p, encoding="utf-8", errors="replace").read()) for p in srcs}
corpus_nows = {p: t.replace(" ", "") for p, t in corpus.items()}
for f in ["agents/A14.md", "agents/A14_annexe_fiches_mesures.md"]:
    t = open(f, encoding="utf-8").read()
    for q in re.findall(r"«\s*(.+?)\s*»", t):
        nq = norm(q.replace("[…]", "…"))
        parts = [p.strip() for p in re.split(r"…|\[\.\.\.\]", nq) if p.strip()]
        ok = None
        for p, c in corpus_nows.items():
            if all(pt.replace(" ", "") in c for pt in parts):
                ok = p; break
        print(("OK  " if ok else "ABS ") + f.split('/')[-1][:12] + " | " + q[:110] + (" | " + ok.split('/')[-1] if ok else ""))
