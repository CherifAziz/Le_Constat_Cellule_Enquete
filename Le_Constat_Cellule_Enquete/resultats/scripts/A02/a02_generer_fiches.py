# -*- coding: utf-8 -*-
"""A02 - genere l'annexe des 27 fiches annuelles (1974-2000) au gabarit impose.
Colonnes chiffrees : donnees/A02/A02_series_1960_2000.csv et A02_decompositions.csv (produits par script).
Champs qualitatifs : scripts/A02/a02_fiches_qualitatif.txt (redige par A02, sources dans le texte).
Ecrit l'annexe bloc par bloc (1974-1978, 1979-1983, 1984-1988, 1989-1993, 1994-1998, 1999-2000).
Usage : python -I a02_generer_fiches.py <racine_resultats>
"""
import csv, os, re, sys

R = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
D = os.path.join(R, "donnees", "A02")
ser = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(D, "A02_series_1960_2000.csv"), encoding="utf-8"), delimiter=";")}
dec = {int(r["annee"]): r for r in csv.DictReader(open(os.path.join(D, "A02_decompositions.csv"), encoding="utf-8"), delimiter=";")}
qtxt = open(os.path.join(R, "scripts", "A02", "a02_fiches_qualitatif.txt"), encoding="utf-8").read()
qual = {}
for blk in re.split(r"^=== ", qtxt, flags=re.M)[1:]:
    year = int(blk[:4])
    fields = {}
    for part in re.split(r"^--- ", blk, flags=re.M)[1:]:
        key, _, body = part.partition("\n")
        fields[key.strip()] = " ".join(l.strip() for l in body.strip().splitlines() if l.strip())
    qual[year] = fields


def fv(x, n=1):
    if x in (None, ""):
        return None
    return ("%.*f" % (n, float(x))).replace(".", ",")


def cell(*parts):
    parts = [p for p in parts if p]
    return " ; ".join(parts) if parts else "indisponible"


def g(y, k, n=1, src=ser):
    return fv(src.get(y, {}).get(k), n)

SRC = {
    "pib": "[C] Insee, comptes nationaux annuels base 2020, T_1101 et T_1102 (fichier T_1101_1103_fr.xlsx créé le 21/05/2026, téléchargé le 20/11/2026)",
    "ipc": "[C] Insee BDM 011813530, coefficient de transformation de la monnaie, base 2025, mis à jour le 05/02/2026 (variation des moyennes annuelles)",
    "cho": "[C] Insee, Emploi, chômage, revenus du travail 2026, fig. 2 (ECRT2026_F8.xlsx), taux BIT, France, moyenne annuelle",
    "apu": "[C] base commune, Insee série longue 2381414 et 2381402, base 2020, extraction du 20/11/2026",
    "int": "[C] base commune, Insee tableau 3.201 (D41 versés, consolidés), rapporté au PIB T_1101 ; solde primaire = B9 + D41 versés",
    "dette": "[C] base commune, Insee 2381414 (ratio) et 2830192 (Md€)",
    "ss": "[C] base commune, Insee 2381402 (Md€ et % du PIB)",
    "ameco": "AMECO, Commission européenne, millésime du 17/11/2026 (AVGDGP, UBLGCP, UBLGAP)",
}


def fiche(y):
    s = ser[y]
    q = qual.get(y, {})
    d = dec.get(y, {})
    lines = ["### %d" % y, "", "| Champ | Contenu |", "|---|---|"]
    # PIB
    pibtxt = None
    if s.get("pib_md"):
        pibtxt = "PIB nominal %s Md€ ; croissance en volume %s %%" % (g(y, "pib_md", 1), g(y, "pib_vol_pct", 1))
        if g(y, "deflateur_pib_pct"):
            pibtxt += " ; prix du PIB %s %%" % g(y, "deflateur_pib_pct")
        pibtxt += ". " + SRC["pib"]
    lines.append("| PIB nominal (Md€) et croissance en volume (%%) | %s |" % (pibtxt or "indisponible"))
    # inflation chomage
    infl = ("inflation (prix à la consommation) %s %%" % g(y, "ipc_pct")) if g(y, "ipc_pct") else "inflation : indisponible"
    cho = ("chômage BIT %s %%" % g(y, "chomage_bit_pct")) if g(y, "chomage_bit_pct") else "chômage BIT : indisponible (série Insee à partir de 1975)"
    lines.append("| Inflation (%%) ; taux de chômage (%%) | %s ; %s. %s ; %s |" % (infl, cho, SRC["ipc"], SRC["cho"]))
    # APU
    lines.append("| Dépenses, recettes, solde des APU (%% du PIB ; solde en Md€) | dépenses %s %% ; recettes %s %% ; solde %s %% du PIB (%s %% recalculé B9/PIB) ; solde %s Md€. %s |" % (
        g(y, "dep_pct"), g(y, "rec_pct"), g(y, "solde_pct"), fv(d.get("solde_pct"), 2) or "n.d.", g(y, "solde_md_insee", 3), SRC["apu"]))
    # interets
    lines.append("| Charge d'intérêts et solde primaire (%% du PIB) | intérêts versés %s %% (nets des intérêts reçus %s %%) ; solde primaire %s %%. %s |" % (
        g(y, "interets_payes_pct", 2), g(y, "interets_nets_pct", 2), g(y, "solde_primaire_pct", 2), SRC["int"]))
    # dette
    if s.get("dette_pct"):
        dt = "%s %% du PIB ; %s Md€. %s" % (g(y, "dette_pct"), g(y, "dette_md", 1), SRC["dette"])
    else:
        dt = "indisponible (série de dette de Maastricht à partir de 1978 dans la base commune)"
    lines.append("| Dette de Maastricht (%% du PIB, Md€) | %s |" % dt)
    # sous-secteurs
    if y >= 1978:
        ss = "État %s %% (%s Md€) ; ODAC %s %% (%s Md€) ; APUL %s %% (%s Md€) ; ASSO %s %% (%s Md€). %s" % (
            g(y, "solde_etat_pct"), g(y, "solde_etat_md", 2), g(y, "solde_odac_pct"), g(y, "solde_odac_md", 2),
            g(y, "solde_apul_pct"), g(y, "solde_apul_md", 2), g(y, "solde_asso_pct"), g(y, "solde_asso_md", 2), SRC["ss"])
    else:
        ss = ("État : indisponible ; ODAC : indisponible (valeurs publiées incohérentes à la source, voir §12 du dossier) ; "
              "administration centrale (État + ODAC) %s %% (%s Md€) ; APUL %s %% (%s Md€) ; ASSO %s %% (%s Md€). %s") % (
            g(y, "solde_apuc_pct"), g(y, "solde_apuc_md", 2), g(y, "solde_apul_pct"), g(y, "solde_apul_md", 2),
            g(y, "solde_asso_pct"), g(y, "solde_asso_md", 2), SRC["ss"])
    lines.append("| Solde par sous-secteur (État, ODAC, APUL, ASSO) | %s |" % ss)
    lines.append("| Exécutif et majorité | %s |" % (q.get("exec") or "indisponible"))
    lines.append("| Lois de finances et mesures principales | %s |" % (q.get("lois") or "indisponible"))
    lines.append("| Contexte externe | %s |" % (q.get("contexte") or "indisponible"))
    lines.append("| Changement de convention ou rupture statistique | %s |" % (q.get("convention") or "aucun identifié"))
    # lecture causale : chiffres de decomposition + texte
    dd = ""
    if d:
        dd = ("Décomposition comptable (script a02_decompositions.py, niveau D) : variation du solde %s pt ; composante cyclique AMECO %s pt ; "
              "effet de la charge d'intérêts %s pt ; résidu (≈ variation du solde primaire corrigé du cycle) %s pt ; écart de production AMECO %s %% ; "
              "solde corrigé du cycle AMECO %s %% du PIB potentiel. ") % (
            fv(d.get("d_solde"), 2), fv(d.get("d_cyclique"), 2) or "n.d.", fv(d.get("d_interets_effet_solde"), 2), fv(d.get("residu_primaire_cvs"), 2) or "n.d.",
            g(y, "ecart_production_ameco", 1) or "n.d.", g(y, "solde_cvs_ameco_pctpot", 2) or "n.d.")
    lines.append("| Lecture causale de la variation du solde | %s%s |" % (dd, q.get("lecture") or "indisponible"))
    lines.append("")
    return "\n".join(l.replace("\n", " ") for l in lines)


ENTETE = """# A02 — Annexe : 27 fiches annuelles 1974–2000

**Agent A02, cellule Le Constat. Date de travail : 20 novembre 2026.** Fichier généré par `resultats\\scripts\\A02\\a02_generer_fiches.py` à partir des séries produites par `a02_construire_series.py` et `a02_decompositions.py` (dans `resultats\\donnees\\A02\\`) et du texte qualitatif `a02_fiches_qualitatif.txt`. Ne pas éditer à la main : modifier les sources puis relancer.

**Conventions.**
- Solde positif = capacité de financement ; « point » = point de PIB.
- Les chiffres de finances publiques viennent de la base commune Insee base 2020, extraite le 20/11/2026. Ils peuvent différer des chiffres publiés à l'époque (voir 1997).
- La décomposition « cyclique / intérêts / résidu » est une identité comptable appliquée à une estimation (AMECO, Commission européenne, 17/11/2026). Elle est de niveau D : le résidu n'est **pas** une mesure des décisions discrétionnaires.
- Les montants des lois de finances sont en francs courants (1 € = 6,55957 F).
- Étiquettes de provenance : [C] pièce consultée, [S] source secondaire citant une pièce non consultée, [M] souvenir du modèle non vérifié (piste), [X] recherche infructueuse.
- Pièces parlementaires abrégées (toutes [C], lues en PDF ou HTML sur senat.fr le 20/11/2026, copies dans `donnees\\A02\\sources\\senat\\`) :
  - Sénat n° 504 (1974-1975), rapport Coudé du Foresto sur la 3e LFR 1975, 11/09/1975 ;
  - n° 133 (1975-1976), rapport Monory sur la 4e LFR 1975, 11/12/1975 ;
  - n° 26 (1976-1977), rapport Monory sur la LFR d'octobre 1976 ;
  - n° 121 (1981-1982), rapport Blin sur la LFR de fin 1981 ;
  - n° 405 (1982-1983), rapport Blin sur le règlement 1981 ;
  - n° 329 (1992-1993), rapport Arthuis sur la LFR 1993 ;
  - n° 391 (1994-1995), rapport Lambert sur la LFR 1995 ;
  - n° 168 (1997-1998), rapport Lambert sur la LFR 1997 ;
  - n° 371 (1999-2000), rapport Marini sur la LFR 2000 ;
  - n° 50 (2001-2002), rapport Marini sur le règlement 2000.
- Les rapporteurs du Sénat appartiennent souvent à l'opposition au gouvernement concerné. Leurs jugements sont de niveau E ; leurs chiffres reprennent les documents budgétaires du gouvernement (niveau A, ex ante).

**Fiche complète** : toutes les cellules renseignées, dont des mesures chiffrées sur pièce. **Fiche partielle** : cellules chiffrées complètes mais mesures non chiffrées ou non vérifiées. Le décompte figure en fin d'annexe.
"""

BLOCS = [(1974, 1978), (1979, 1983), (1984, 1988), (1989, 1993), (1994, 1998), (1999, 2000)]
dest = os.path.join(R, "agents", "A02_annexe_fiches_1974_2000.md")
with open(dest, "w", encoding="utf-8") as f:
    f.write(ENTETE + "\n")
for a, b in BLOCS:
    with open(dest, "a", encoding="utf-8") as f:
        f.write("\n## Bloc %d–%d\n\n" % (a, b))
        for y in range(a, b + 1):
            f.write(fiche(y) + "\n")
PIED = """
## Décompte de complétude (établi par A02, 20/11/2026)

- **Aucune fiche n'est complète au sens strict.** La cellule « majorité à l'Assemblée » repose partout sur la mémoire du modèle [M] : aucune pièce consolidée sur les législatures n'a été obtenue (page de l'Assemblée en 404, recherches infructueuses).
- **Complètes pour les chiffres et pour les mesures chiffrées sur pièce (7)**, réserve faite de la majorité : 1975, 1976, 1981, 1993, 1995, 1997, 2000.
- **Partielles, quelques décisions ou exécutions sur pièce (5)** : 1974, 1977, 1980, 1992, 1999.
- **Partielles, mesures indisponibles ou seulement [M] (15)** : 1978, 1979, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1994, 1996, 1998.
- **Cellules structurellement indisponibles** : dette de Maastricht 1974–1977 (série à partir de 1978) ; chômage BIT 1974 (série à partir de 1975) ; solde de l'État et des ODAC 1974–1977 (incohérent à la source).
- **Absentes** : aucune.
"""
with open(dest, "a", encoding="utf-8") as f:
    f.write(PIED)
print("ecrit", dest)
