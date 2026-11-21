# -*- coding: utf-8 -*-
"""Fusion mécanique des fiches d'exercice (A02, A03), des mesures relevées par S01
et de la table des majorités d'A09 en une chronologie 1974-2026.

Ne réécrit rien : chaque cellule renvoie à la fiche d'origine. Signale les cellules
vides, « indisponible » ou fondées sur un souvenir non vérifié [M].

Usage : python -I scripts/commun/fusionner_chronologie.py   (depuis resultats/)
Sorties : donnees/commun/chronologie_fusionnee.csv ; 01_chronologie_1974_2026.md
"""
import csv
import datetime as dt
import os
import re

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = [
    ("A02", os.path.join(R, "agents", "A02_annexe_fiches_1974_2000.md")),
    ("A03", os.path.join(R, "agents", "A03_annexe_fiches_2001_2026.md")),
    ("S01", os.path.join(R, "agents", "S01_annexe_mesures_par_exercice.md")),
]
CHAMPS = [  # (clé, motif dans l'intitulé du champ)
    ("pib", "pib nominal"),
    ("inflation_chomage", "inflation"),
    ("dep_rec_solde", "dépenses, recettes"),
    ("interets_primaire", "charge d'intérêts"),
    ("dette", "dette de maastricht"),
    ("sous_secteurs", "sous-secteur"),
    ("structurel", "solde structurel"),
    ("decomposition", "décomposition mécanique"),
    ("executif", "exécutif"),
    ("mesures", "lois de finances"),
    ("prevision", "prévision initiale"),
    ("contexte", "contexte externe"),
    ("rupture", "changement de convention"),
    ("lecture", "lecture causale"),
]
OBLIGATOIRES = ["pib", "dep_rec_solde", "dette", "contexte", "mesures"]  # critère de fin n° 2


def cle(intitule):
    i = intitule.lower().replace("’", "'")
    for k, motif in CHAMPS:
        if motif in i:
            return k
    return None


def lire_fiches(agent, chemin):
    """-> {annee: {cle: contenu}}"""
    d, an = {}, None
    for l in open(chemin, encoding="utf-8").read().split("\n"):
        m = re.match(r"^#{2,3} (\d{4})\b", l)
        if m:
            an = int(m.group(1))
            d.setdefault(an, {})
            continue
        if l.startswith("#"):
            an = None if not re.match(r"^#{2,3} \d{4}", l) else an
            continue
        if an and l.startswith("|") and not l.startswith("|---") and not l.startswith("| Champ"):
            c = l.strip().strip("|").split(" | ", 1)
            if len(c) == 2:
                k = cle(c[0])
                if k:
                    d[an][k] = c[1].strip()
    return d


def etat(txt):
    if not txt or not txt.strip():
        return "vide"
    t = txt.lower()
    if t.startswith("indisponible") or t.startswith("non disponible"):
        return "indisponible"
    drap = []
    if "indisponible" in t:
        drap.append("partiel")
    if "[m]" in t:
        drap.append("souvenir")
    return "+".join(drap) if drap else "présent"


def serie(fichier, nom, unite=None):
    d = {}
    for r in csv.DictReader(open(os.path.join(R, "donnees", "commun", fichier), encoding="utf-8-sig"), delimiter=";"):
        if r["serie"] == nom and (unite is None or r["unite"] == unite):
            try:
                d[int(r["annee"])] = float(r["valeur"])
            except ValueError:
                pass
    return d


fiches = {a: lire_fiches(a, p) for a, p in SRC}
dep = serie("base_insee_dep_rec_pctPIB.csv", "Dépenses")
rec = serie("base_insee_dep_rec_pctPIB.csv", "Recettes")
maj = {}
for r in csv.DictReader(open(os.path.join(R, "donnees", "A09", "a09_table_exercices_1975_2025.csv"), encoding="utf-8-sig"), delimiter=";"):
    maj[int(r["exercice"])] = r

lignes, manques = [], []
for an in range(1974, 2027):
    src = "A02" if an <= 2000 else "A03"
    f = fiches[src].get(an, {})
    s01 = fiches["S01"].get(an, {})
    for k, _ in CHAMPS:
        txt = f.get(k, "")
        e = etat(txt)
        if k in ("structurel", "decomposition", "prevision") and src == "A02" and not txt:
            e = "hors gabarit A02"
        if an == 2026 and not txt:
            e = "gabarit propre"  # exercice en cours : fiche rédigée en sections a à e, sans tableau
        lignes.append({"annee": an, "champ": k, "source": src, "etat": e, "contenu": txt})
        if k == "mesures" and s01.get("mesures"):
            lignes.append({"annee": an, "champ": "mesures_complement", "source": "S01", "etat": etat(s01["mesures"]), "contenu": s01["mesures"]})
        if k in OBLIGATOIRES and e in ("vide", "indisponible"):
            if not (k == "mesures" and s01.get("mesures")):
                manques.append((an, k, e, src))

os.makedirs(os.path.join(R, "donnees", "commun"), exist_ok=True)
with open(os.path.join(R, "donnees", "commun", "chronologie_fusionnee.csv"), "w", encoding="utf-8-sig", newline="") as fo:
    w = csv.DictWriter(fo, fieldnames=["annee", "champ", "source", "etat", "contenu"], delimiter=";")
    w.writeheader()
    w.writerows(lignes)

idx = {(l["annee"], l["champ"]): l for l in lignes}


def fr(x, n=1):
    return "—" if x is None else f"{x:.{n}f}".replace(".", ",")


def court(t, n=230):
    t = re.sub(r"\s+", " ", t.replace("|", "/"))
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " […]"


H = dt.datetime.now().strftime("%d/%m/%Y à %H h %M")
o = []
o.append("# Chronologie fusionnée des exercices 1974–2026")
o.append("")
o.append(f"**Fusion mécanique produite le {H} par `scripts\\commun\\fusionner_chronologie.py`.** Ce fichier n'ajoute aucun fait : il assemble les fiches d'A02 (1974–2000) et d'A03 (2001–2026), les mesures relevées par S01 et la table des majorités d'A09, et il signale les cellules manquantes. Les séries de dépenses et de recettes viennent de la base commune (Insee, base 2020, extraction du 20/11/2026). **Statut : dossiers sources passés en recette avec réserves, non contre-expertisés.** Le texte complet de chaque cellule est dans `donnees\\commun\\chronologie_fusionnee.csv` et dans les fiches d'origine.")
o.append("")
o.append("## 1. Couverture")
o.append("")
nb = {a: len([y for y in fiches[a] if 1974 <= y <= 2026]) for a in fiches}
o.append(f"- Fiches trouvées : A02, {nb['A02']} ; A03, {nb['A03']} ; compléments de mesures S01, {nb['S01']} exercices.")
tot = len([l for l in lignes if l['champ'] in OBLIGATOIRES])
ok = len([l for l in lignes if l['champ'] in OBLIGATOIRES and l['etat'] not in ('vide', 'indisponible')])
o.append(f"- Cellules obligatoires (PIB ; dépenses, recettes et solde ; dette ; contexte ; mesures) : {ok} renseignées sur {tot}, avant complément de S01.")
o.append(f"- Cellules obligatoires vides ou indisponibles après complément de S01 : **{len(manques)}** (liste en section 3).")
ns = len([l for l in lignes if 'souvenir' in l['etat']])
o.append(f"- Cellules contenant au moins un élément marqué comme souvenir non vérifié : {ns}.")
o.append("")
o.append("## 2. Tableau annuel")
o.append("")
o.append("Dépenses, recettes et solde en % du PIB (base commune). Majorité : type à la date du vote du budget, selon A09. Mesures : début de la cellule de la fiche ; « + S01 » signale un complément.")
o.append("")
o.append("| Exercice | Dépenses | Recettes | Solde | Majorité (A09) | Mesures principales (début de cellule) | Fiche |")
o.append("|---|---|---|---|---|---|---|")
for an in range(1974, 2027):
    src = "A02" if an <= 2000 else "A03"
    d, r_ = dep.get(an), rec.get(an)
    sol = None if d is None or r_ is None else r_ - d
    m = maj.get(an, {}).get("type_majorite", "—")
    mes = idx[(an, "mesures")]
    txt = court(mes["contenu"]) if mes["contenu"] else "**cellule vide**"
    if an == 2026:
        txt = "exercice en cours : loi de finances du 19 février 2026 (cible de −5,0 %) ; voir la fiche, sections a à e"
    if mes["etat"] == "indisponible":
        txt = "**indisponible dans la fiche**"
    if (an, "mesures_complement") in idx:
        txt += " **+ S01**"
    o.append(f"| {an} | {fr(d)} | {fr(r_)} | {fr(sol)} | {m} | {txt} | {src} |")
o.append("")
o.append("## 3. Cellules obligatoires manquantes")
o.append("")
if manques:
    o.append("| Exercice | Champ | État | Fiche |")
    o.append("|---|---|---|---|")
    for an, k, e, src in manques:
        o.append(f"| {an} | {k} | {e} | {src} |")
else:
    o.append("Aucune.")
o.append("")
o.append("## 4. État de chaque champ, par exercice")
o.append("")
cles = [k for k, _ in CHAMPS]
o.append("| Exercice | " + " | ".join(cles) + " |")
o.append("|---|" + "---|" * len(cles))
ab = {"présent": "oui", "vide": "**vide**", "indisponible": "**indisp.**", "partiel": "partiel", "souvenir": "oui (M)", "partiel+souvenir": "partiel (M)", "hors gabarit A02": "·", "gabarit propre": "voir fiche"}
for an in range(1974, 2027):
    o.append(f"| {an} | " + " | ".join(ab.get(idx[(an, k)]["etat"], idx[(an, k)]["etat"]) for k in cles) + " |")
o.append("")
o.append("Lecture : « partiel » = la cellule contient le mot « indisponible » pour une partie de son contenu ; « (M) » = au moins un élément de mémoire non vérifié ; « · » = champ absent du gabarit des fiches d'avant 2001.")
o.append("")
open(os.path.join(R, "01_chronologie_1974_2026.md"), "w", encoding="utf-8", newline="").write("\n".join(o))
print("fiches", nb, "| cellules", len(lignes), "| obligatoires ok", ok, "/", tot, "| manques", len(manques), "| souvenirs", ns)
for x in manques[:60]:
    print(x)
