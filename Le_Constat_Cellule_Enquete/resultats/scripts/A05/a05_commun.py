# -*- coding: utf-8 -*-
"""A05 - fonctions communes de lecture (Insee 32xx, Eurostat JSON-stat, CSV base commune).
Lecture seule de resultats/donnees/commun ; écritures dans resultats/donnees/A05.
Exécuter avec : python -I <script>.py  (depuis n'importe quel dossier)."""
import csv, json, os, itertools

RACINE = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete"
COMMUN = os.path.join(RACINE, "resultats", "donnees", "commun")
A05 = os.path.join(RACINE, "resultats", "donnees", "A05")
SRC = os.path.join(A05, "sources")


def lire_insee_32xx(num):
    """Retourne (annees, {libelle_normalise: {annee: valeur}}) pour la première feuille
    du tableau insee_cn_t_<num>.xlsx. Les libellés en double reçoivent un suffixe #2, #3."""
    import openpyxl
    f = os.path.join(COMMUN, "insee_cn_t_%s.xlsx" % num)
    wb = openpyxl.load_workbook(f, read_only=True, data_only=True)
    ws = wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = None
    for r in rows[:6]:
        if any(isinstance(c, int) and 1940 < c < 2100 for c in r):
            hdr = r
            break
    cols = [(j, c) for j, c in enumerate(hdr) if isinstance(c, int)]
    out, vus = {}, {}
    for r in rows:
        lab = r[1] if len(r) > 1 else None
        if not isinstance(lab, str) or not lab.strip():
            continue
        lab = " ".join(lab.split())
        vals = {}
        for j, an in cols:
            v = r[j] if j < len(r) else None
            if isinstance(v, (int, float)):
                vals[an] = float(v)
        if not vals:
            continue
        n = vus.get(lab, 0) + 1
        vus[lab] = n
        key = lab if n == 1 else "%s #%d" % (lab, n)
        out[key] = vals
    return [c for _, c in cols], out


def lire_jsonstat(path):
    """Eurostat JSON-stat 2.0 -> liste de dicts {dim: code, ..., 'value': float, 'status': str}."""
    d = json.load(open(path, encoding="utf-8"))
    ids = d["id"]
    sizes = d["size"]
    cats = []
    for dim in ids:
        idx = d["dimension"][dim]["category"]["index"]
        inv = sorted(idx.items(), key=lambda kv: kv[1])
        cats.append([k for k, _ in inv])
    vals = d.get("value", {})
    stat = d.get("status", {}) or {}
    res = []
    # strides
    strides = []
    acc = 1
    for s in reversed(sizes):
        strides.insert(0, acc)
        acc *= s
    for k, v in vals.items():
        k = int(k)
        rec = {}
        rem = k
        for dim, st, cs in zip(ids, strides, cats):
            q, rem = divmod(rem, st)
            rec[dim] = cs[q]
        rec["value"] = float(v)
        rec["status"] = stat.get(str(k), "")
        res.append(rec)
    return res


def lire_csv_commun(nom):
    return list(csv.DictReader(open(os.path.join(COMMUN, nom), encoding="utf-8-sig")))


def ecrire_csv(nom, entetes, lignes, dossier=None):
    p = os.path.join(dossier or A05, nom)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(entetes)
        for l in lignes:
            w.writerow([("%.4f" % x) if isinstance(x, float) else x for x in l])
    return p
