# -*- coding: utf-8 -*-
"""A18 partie 3 - arbitrage T-07 (un assouplissement suit-il chaque consolidation ?).
Lit l'AMECO fiscal (ameco17.zip, retelecharge par A18 a l'origine, ec.europa.eu, 20/11/2026)
et applique les deux definitions (A03 : episodes de consolidation -> annee suivante ;
A09 : annees d'assouplissement <= -0,5 pt -> consolidation > +1 pt dans les 3 / 5 ans precedents)
a la meme serie : solde primaire corrige du cycle (code AMECO choisi d'apres son libelle).
Sortie : donnees\\A18\\a18_p3_t07_sortie.txt"""
import zipfile, io, sys
ZIP = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18\sources\p2\ameco\ameco17.zip"
OUT = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\A18\a18_p3_t07_sortie.txt"
L = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)

z = zipfile.ZipFile(ZIP)
name = [n for n in z.namelist() if n.upper().endswith(".TXT")][0]
txt = z.read(name).decode("latin-1")
lines = txt.splitlines()
head = lines[0].split(";")
years = [h.strip() for h in head]
rows = {}
for ln in lines[1:]:
    p = ln.split(";")
    if len(p) < 6:
        continue
    code = p[0].strip()
    if code.startswith("FRA.") and (".UBLGB" in code or ".UBLGA" in code or code.endswith(".UBLG") or ".UBLGI" in code):
        rows[code] = p
log("Fichier", name, "; date interne du zip :", z.getinfo(name).date_time, "; colonnes", head[:6], "...", head[-3:])
for c, p in rows.items():
    log(c, "| TITLE :", p[3].strip()[:120], "|", p[4].strip() if len(p) > 4 else "")
# variations 2004-2006 de toutes les series candidates (pour identifier la serie citee par A03 : +0,5 ; ~0 ; +0,85)
for c, p in rows.items():
    vv = {}
    for i, y in enumerate(years):
        if y in ("2003", "2004", "2005", "2006", "2007"):
            try:
                vv[int(y)] = float(p[i])
            except ValueError:
                pass
    if len(vv) == 5:
        log("  variations", c, {y: round(vv[y] - vv[y - 1], 2) for y in (2004, 2005, 2006, 2007)})

# choix : solde primaire corrige du cycle, base PIB potentiel, en % du PIB potentiel
cand = [c for c in rows if ".UBLGBP" in c or ".UBLGIE" in c]
log("Candidats primaire CAPB :", cand)
def serie(code):
    p = rows[code]
    s = {}
    for i, y in enumerate(years):
        if y.isdigit() and i < len(p):
            v = p[i].strip()
            try:
                s[int(y)] = float(v)
            except ValueError:
                pass
    return s
for code in cand:
    s = serie(code)
    log("\n=== Serie", code, rows[code][2].strip()[:90])
    log("Niveaux 2002-2008 :", {y: s.get(y) for y in range(2002, 2009)})
    d = {y: s[y] - s[y - 1] for y in s if y - 1 in s}
    # A09 : annees d'assouplissement
    ass = [y for y in sorted(d) if 1976 <= y <= 2025 and d[y] <= -0.5]
    log("Annees d'assouplissement (delta <= -0,5) :", [(y, round(d[y], 2)) for y in ass])
    # definition exacte d'A09 (C-A09-003) : cumul FIXE des 3 annees precedentes = s[y-1] - s[y-4]
    det9 = [(y, round(s[y - 1] - s[y - 4], 2), (s[y - 1] - s[y - 4]) > 1.0) for y in ass if (y - 4) in s]
    log("Definition A09 (cumul fixe 3 ans) :", sum(1 for x in det9 if x[2]), "sur", len(det9), det9)
    for w in (3, 5):
        n = 0
        det = []
        for y in ass:
            cum3 = s[y - 1] - s[y - 1 - 3] if (y - 4) in s else None
            best = max((s[y - 1] - s[y - 1 - k]) for k in range(1, w + 1) if (y - 1 - k) in s) if (y - 2) in s else None
            ok = best is not None and best > 1.0
            n += ok
            det.append((y, round(best, 2) if best is not None else None, ok))
        log(f"Variante A18 (meilleur gain sur 1..{w} ans) : {n} assouplissements sur {len(ass)} precedes d'un gain > 1 pt :", det)
    # A03 : episodes de consolidation (gain cumule > +1 pt sur 3 ans glissants, fin d'episode) -> delta suivant
    log("Episodes A03 et annee suivante :")
    for (a, b, nxt) in ((2003, 2006, 2007), (2010, 2016, 2017), (2010, 2016, 2019), (1993, 1999, 2000), (1994, 1997, 1998)):
        if a in s and b in s and nxt in d:
            log(f"  consolidation {a}->{b} : {s[b]-s[a]:+.2f} pt ; delta {nxt} : {d[nxt]:+.2f}")
    log("Deltas annuels 2003-2008 :", {y: round(d[y], 2) for y in range(2003, 2009) if y in d})
with open(OUT, "w", encoding="utf-8") as h:
    h.write("\n".join(L))
