# -*- coding: utf-8 -*-
"""A03 - genere l'annexe des fiches annuelles 2001-2025 (+ fiche 2026) en fusionnant :
  - les colonnes chiffrees de resultats/donnees/A03/table_annuelle_A03.csv (construite par construire_table_A03.py)
  - le texte qualitatif de resultats/donnees/A03/fiches_narratif.md (ecrit a la main, avec pieces et etiquettes)
Format du narratif :  '## AAAA' puis '### champ' puis le texte. Champs : executif, lois, prevision, contexte,
convention, structurel, lecture. Champ absent -> 'indisponible'. La fiche 2026 est entierement narrative ('## 2026').
Lancer : python -I generer_fiches_A03.py
"""
import os, csv, re

ICI = os.path.dirname(os.path.abspath(__file__))
A03 = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03"))
OUT = os.path.abspath(os.path.join(ICI, "..", "..", "agents", "A03_annexe_fiches_2001_2026.md"))

T = {}
with open(os.path.join(A03, "table_annuelle_A03.csv"), encoding="utf-8-sig") as f:
    for r in csv.DictReader(f, delimiter=";"):
        T[int(r["annee"])] = r

N = {}
p = os.path.join(A03, "fiches_narratif.md")
if os.path.exists(p):
    an, champ = None, None
    for ligne in open(p, encoding="utf-8").read().splitlines():
        m = re.match(r"^## (\d{4})\s*$", ligne)
        if m:
            an, champ = int(m.group(1)), None
            N.setdefault(an, {})
            continue
        m = re.match(r"^### (\w+)\s*$", ligne)
        if m and an:
            champ = m.group(1)
            N[an][champ] = []
            continue
        if an and champ:
            N[an][champ].append(ligne)
    for a in N:
        for c in N[a]:
            N[a][c] = "\n".join(N[a][c]).strip()


def v(a, c, suf=""):
    x = T.get(a, {}).get(c, "indisponible")
    return x if x == "indisponible" else x.replace(".", ",") + suf


def delta(a, c):
    try:
        return ("%+.2f" % (float(T[a][c]) - float(T[a - 1][c]))).replace(".", ",")
    except Exception:
        return "indisponible"


def nar(a, c):
    return N.get(a, {}).get(c) or "indisponible"


SRC_INSEE = "Insee, comptes nationaux base 2020 (base commune, fichiers extraits le 20/11/2026)"
ENTETE = """# A03 — Annexe : fiches annuelles 2001–2025 et fiche 2026 (exercice en cours)

Généré par `resultats\\scripts\\A03\\generer_fiches_A03.py` à partir de `resultats\\donnees\\A03\\table_annuelle_A03.csv` (chiffres, produits par script) et de `resultats\\donnees\\A03\\fiches_narratif.md` (texte, pièces et étiquettes). **Ne pas éditer cette annexe à la main** : modifier le narratif et relancer.

**Sources des colonnes chiffrées** (toutes [C], extraction 20/11/2026) :
- PIB nominal, croissance en volume, déflateur : Eurostat `nama_10_gdp` (B1GQ, CP_MEUR, CLV_PCH_PRE, PD_PCH_PRE_EUR), mise à jour Eurostat consultée le 20/11/2026 — données transmises par l'Insee (base 2020).
- Inflation : IPCH, taux annuel moyen, Eurostat `prc_hicp_aind` (CP00, RCH_A_AVG). L'IPC Insee n'a pas été extrait.
- Chômage : Insee, taux de chômage BIT France hors Mayotte, idbank 001688527 (CVS, trimestriel), moyenne des quatre trimestres calculée par A03.
- Taux à 10 ans : Eurostat `irt_lt_mcby_a` (critère de convergence), France et Allemagne.
- Dépenses, recettes, solde (% PIB), dette brute et nette (% PIB) : Insee série longue `econ-fin-pub-rec-dep.xlsx` (base commune, `base_insee_dep_rec_pctPIB.csv`). Le solde en % y est **arrondi au dixième** ; la colonne « solde recalculé » = solde Md€ / PIB nominal.
- Solde en Md€ et par sous-secteur : Insee `econ-fin-pub-deficit-secteur.xlsx` (base commune). Dette en Md€ : Insee `econ-fin-pub-dette-adm-pub.xlsx`.
- Charge d'intérêts : **D41 payés, consolidés, y compris correction SIFIM** (Insee tableau 3.201 ; identique à Eurostat `D41PAY` de la base commune). Solde primaire = (solde + D41) / PIB, calculé par A03. Une variante D41G (hors SIFIM) existe dans le même tableau ; elle donne 64,65 Md€ en 2025 contre 65,72 Md€.
- Solde corrigé du cycle (CAB), solde structurel (hors mesures ponctuelles, disponible seulement depuis 2010), écart de production : **Commission européenne, AMECO**, variables UBLGAP, UBLGAPS, UBLGBP, UBLGBPS, AVGDGP, extraction du 20/11/2026 ; millésime AMECO non affiché par l'interface — voir A03.md §5. Ces grandeurs sont des **estimations** révisables (catégorie « cause plausible non isolée »).

**Statut des fiches** : aucune fiche n'est complète au sens strict du gabarit. Il manque partout les références complètes des LFI, LFSS et lois de programmation, le niveau de la prévision initiale avant 2008 et l'explication officielle de l'écart. Le tableau ci-dessous distingue les fiches dont chaque champ porte au moins une pièce [C] et celles où un champ en est dépourvu. Les montants annuels d'IR 2001–2007 viennent d'un tableau du rapport Carrez mis à plat par extraction texte (alignement des colonnes non vérifié).
"""


def fiche(a):
    L = []
    L.append("\n## %d\n" % a)
    L.append("| Champ | Contenu |\n|---|---|")
    L.append("| PIB nominal (Md€) ; croissance en volume (%%) | %s Md€ ; %s %% (déflateur %s %%) — Eurostat nama_10_gdp [C] |" % (v(a, "pib_Md"), v(a, "croiss_vol_pct"), v(a, "deflateur_pct")))
    L.append("| Inflation (%%) ; chômage (%%) | IPCH %s %% (Eurostat) ; chômage BIT %s %% (Insee 001688527, moyenne annuelle) [C] |" % (v(a, "ipch_pct"), v(a, "chomage_bit_pct")))
    L.append("| Dépenses, recettes, solde APU | Dépenses %s %% ; recettes %s %% ; solde %s %% du PIB (recalculé %s %%) ; **%s Md€** ; variation du solde %s pt — %s [C] |" % (
        v(a, "dep_pct"), v(a, "rec_pct"), v(a, "solde_pct"), v(a, "solde_calc_pct"), v(a, "solde_Md"), delta(a, "solde_calc_pct"), SRC_INSEE))
    L.append("| Charge d'intérêts ; solde primaire | Intérêts D41 %s Md€ = %s %% du PIB ; solde primaire %s %% du PIB (variation %s pt) — Insee 3.201 + calcul A03 [C] |" % (
        v(a, "interets_D41_Md"), v(a, "interets_pct"), v(a, "solde_primaire_pct"), delta(a, "solde_primaire_pct")))
    L.append("| Dette de Maastricht | %s %% du PIB ; %s Md€ ; dette nette %s %% — Insee (base commune) [C] |" % (v(a, "dette_pct"), v(a, "dette_Md"), v(a, "dette_nette_pct")))
    L.append("| Solde par sous-secteur (Md€ ; %% PIB) | État %s (%s %%) ; ODAC %s (%s %%) ; APUL %s (%s %%) ; ASSO %s (%s %%) — Insee [C] |" % (
        v(a, "solde_Etat_Md"), v(a, "solde_Etat_pct"), v(a, "solde_ODAC_Md"), v(a, "solde_ODAC_pct"),
        v(a, "solde_APUL_Md"), v(a, "solde_APUL_pct"), v(a, "solde_ASSO_Md"), v(a, "solde_ASSO_pct")))
    st = "Commission (AMECO, extr. 20/11/2026) : solde corrigé du cycle %s %% du PIB potentiel (variation %s pt) ; solde structurel %s ; primaire corrigé du cycle %s %% (variation = effort hors intérêts %s pt) ; écart de production %s %% [C]" % (
        v(a, "ameco_solde_CAB_pct"), delta(a, "ameco_solde_CAB_pct"), v(a, "ameco_solde_struct_pct", " %"), v(a, "ameco_primaire_CA_pct"), delta(a, "ameco_primaire_CA_pct"), v(a, "ameco_ecart_prod_pct"))
    autre = nar(a, "structurel")
    if autre != "indisponible":
        st += "<br>Autres estimations : " + autre.replace("\n", "<br>")
    L.append("| Solde structurel et effort structurel | %s |" % st)
    try:
        cur, pre = T[a], T[a - 1]
        cyc = lambda r: float(r["solde_calc_pct"]) - float(r["ameco_solde_CAB_pct"])
        dsol = float(cur["solde_calc_pct"]) - float(pre["solde_calc_pct"])
        dint = -(float(cur["interets_pct"]) - float(pre["interets_pct"]))
        dcyc = cyc(cur) - cyc(pre)
        dpca = float(cur["ameco_primaire_CA_pct"]) - float(pre["ameco_primaire_CA_pct"])
        dec = ("Variation du solde %+.2f pt = intérêts %+.2f + composante cyclique %+.2f + primaire corrigé du cycle %+.2f (+ résidu %+.2f dû au mélange PIB effectif / potentiel). "
               "Calcul A03 (`generer_fiches_A03.py`) sur Insee + AMECO ; identité comptable, non causale ; le primaire corrigé du cycle mêle mesures discrétionnaires et effets non discrétionnaires (élasticités, recettes hors PO) [C]"
               % (dsol, dint, dcyc, dpca, dsol - dint - dcyc - dpca)).replace(".", ",", 0)
        dec = re.sub(r"(\d)\.(\d)", r"\1,\2", dec)
    except Exception:
        dec = "indisponible"
    L.append("| Décomposition mécanique de la variation du solde | %s |" % dec)
    for lib, c in [("Exécutif et majorité", "executif"), ("Lois de finances, LFSS, programmation, mesures", "lois"),
                   ("Prévision initiale du solde et exécution", "prevision"), ("Contexte externe", "contexte"),
                   ("Changement de convention / rupture", "convention"), ("Lecture causale de la variation du solde", "lecture")]:
        L.append("| %s | %s |" % (lib, nar(a, c).replace("\n", "<br>")))
    return "\n".join(L)


def statut(a):
    """Champ qualitatif 'documenté' = présent, ne commence pas par 'Indisponible' et porte au moins une pièce [C].
    Exécutif : la majorité parlementaire n'est sourcée qu'en [M] avant 2024 -> signalé à part."""
    manq = []
    for c in ["executif", "lois", "prevision", "contexte", "lecture"]:
        t = nar(a, c)
        ok_preuve = ("[C" in t) or (c == "lecture" and "Preuve" in t)
        if t == "indisponible" or t.lower().startswith("indisponible") or not ok_preuve:
            manq.append(c)
    maj = "majorité [M]" if "[M" in nar(a, "executif") else ""
    if not manq:
        return "chaque champ étayé par au moins une pièce" + (" (sauf %s)" % maj if maj else "") + " ; partielle au sens du gabarit"
    return "partielle — non documenté sur pièce : %s%s" % (", ".join(manq), ("; " + maj) if maj else "")


corps = [ENTETE, "\n## Tableau d'état des fiches\n", "| Année | État |\n|---|---|"]
for a in range(2001, 2026):
    corps.append("| %d | %s |" % (a, statut(a)))
corps.append("| 2026 | %s |" % ("rédigée (voir fiche)" if 2026 in N else "absente"))
for a in range(2001, 2026):
    corps.append(fiche(a))
corps.append("\n## 2026 — exercice en cours (aucun chiffre « réalisé »)\n")
if 2026 in N:
    for c, txt in N[2026].items():
        corps.append("### %s\n\n%s\n" % (c, txt))
else:
    corps.append("indisponible")
open(OUT, "w", encoding="utf-8").write("\n".join(corps) + "\n")
print("ecrit", OUT, "| narratif pour", sorted(N))
