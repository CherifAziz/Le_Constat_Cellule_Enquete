"""A12 - test de singularite des "51 deficits" (C-A12-001 a C-A12-004).

Entree : donnees\\A12\\sources\\oecd_eo119_finpub.csv (OCDE, Economic Outlook 119, API SDMX,
         telecharge le 20/11/2026) ; AMECO (donnees\\A06\\sources\\ameco) pour controle.
Sorties (donnees\\A12\\) :
  A12_singularite_1975_2025.csv   une ligne par pays
  A12_soldes_longs_OCDE.csv       series annuelles (format long) utilisees
  A12_controle_ameco_ocde.csv     ecarts OCDE / AMECO / Insee sur annees communes
Regles (fixees avant calcul, dossier A12 sec. 0) :
  - deficit = solde NLGQ < 0 ; variante "au dixieme" : solde arrondi a 0,1 < 0 (une annee a -0,04 compte
    alors comme equilibre).
  - plus longue serie : nombre maximal d'annees consecutives de deficit dans 1975-2025.
  - excedent primaire = NLGXQ > 0 (OCDE : solde hors interets NETS ; convention differente de l'Insee).
  - pays retenu pour le test complet seulement si NLGQ couvre les 51 annees 1975-2025 sans trou.
Usage : python -I a12_01_singularite.py
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a12_ameco_commun import lire_ameco, SORTIE

SRC = os.path.join(SORTIE, "sources", "oecd_eo119_finpub.csv")


def charger_ocde():
    data = {}
    noms = {}
    with open(SRC, encoding="utf-8") as h:
        for r in csv.DictReader(h):
            try:
                v = float(r["OBS_VALUE"])
            except (ValueError, KeyError):
                continue
            data.setdefault((r["REF_AREA"], r["MEASURE"]), {})[int(r["TIME_PERIOD"])] = v
            noms[r["REF_AREA"]] = r["Reference area"]
    return data, noms


def plus_longue_serie(annees_def):
    best = cur = 0
    best_fin = None
    prev = None
    for a in sorted(annees_def):
        cur = cur + 1 if prev is not None and a == prev + 1 else 1
        if cur > best:
            best, best_fin = cur, a
        prev = a
    return best, (best_fin - best + 1 if best_fin else None), best_fin


def main():
    data, noms = charger_ocde()
    pays = sorted({p for (p, m) in data if m == "NLGQ"})
    # Raccord : annees 1975-2025 absentes de l'OCDE mais presentes dans AMECO UBLG (France 1975-1977)
    am0 = lire_ameco({"1.0.319.0.UBLG", "1.0.319.0.UBLGI"})
    raccord = {}
    for code, v in am0.items():
        pz = code.split(".")[0]
        var = "NLGQ" if code.endswith(".UBLG") else "NLGXQ"
        if (pz, var) in data:
            for a, x in v["serie"].items():
                if 1975 <= a <= 2025 and a not in data[(pz, var)]:
                    data[(pz, var)][a] = x
                    raccord.setdefault(pz, set()).add((var, a))
    lignes = []
    longs = []
    for p in pays:
        s = data.get((p, "NLGQ"), {})
        prim = data.get((p, "NLGXQ"), {})
        dette = data.get((p, "GGFLQ"), {})
        dettem = data.get((p, "GGFLMQ"), {})
        annees = [a for a in range(1975, 2026) if a in s]
        complet = len(annees) == 51
        defs = [a for a in annees if s[a] < 0]
        defs_dix = [a for a in annees if round(s[a], 1) < 0]
        exc = [a for a in annees if s[a] >= 0]
        lg, deb, fin = plus_longue_serie(defs)
        pa = [a for a in range(1975, 2026) if a in prim]
        pexc = [a for a in pa if prim[a] > 0]
        def val(d, a):
            return "" if a not in d else round(d[a], 1)
        prem_dette = min((a for a in dette if a >= 1975), default=None)
        lignes.append({
            "pays": p, "nom": noms.get(p, ""),
            "source": "OCDE EO 119" + ("" if p not in raccord else " + AMECO " + ",".join("%s %d" % t for t in sorted(raccord[p]))),
            "premiere_annee_solde": min(s) if s else "",
            "annees_couvertes_1975_2025": len(annees), "serie_complete_1975_2025": "oui" if complet else "non",
            "nb_deficits": len(defs), "nb_deficits_au_dixieme": len(defs_dix),
            "nb_excedents_ou_equilibre": len(exc),
            "annees_excedent": " ".join(str(a) for a in exc),
            "dernier_excedent": max(exc) if exc else "",
            "plus_longue_serie_deficits": lg, "serie_debut": deb or "", "serie_fin": fin or "",
            "deficit_en_cours_2025": "oui" if 2025 in s and s[2025] < 0 else "non",
            "annees_primaire_couvertes": len(pa), "nb_excedents_primaires": len(pexc),
            "dernier_excedent_primaire": max(pexc) if pexc else "",
            "solde_moyen_1975_2025": round(sum(s[a] for a in annees) / len(annees), 2) if annees else "",
            "solde_2025": val(s, 2025),
            "dette_GGFLQ_premiere_annee": prem_dette or "", "dette_GGFLQ_premiere_valeur": val(dette, prem_dette) if prem_dette else "",
            "dette_GGFLQ_1995": val(dette, 1995), "dette_GGFLQ_2007": val(dette, 2007), "dette_GGFLQ_2025": val(dette, 2025),
            "dette_maastricht_1995": val(dettem, 1995), "dette_maastricht_2025": val(dettem, 2025),
        })
        for a in sorted(s):
            longs.append({"pays": p, "annee": a, "solde_NLGQ": round(s[a], 3),
                          "primaire_NLGXQ": "" if a not in prim else round(prim[a], 3),
                          "dette_GGFLQ": "" if a not in dette else round(dette[a], 2),
                          "dette_GGFLMQ": "" if a not in dettem else round(dettem[a], 2)})
    champs = list(lignes[0].keys())
    with open(os.path.join(SORTIE, "A12_singularite_1975_2025.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=champs, delimiter=";")
        w.writeheader()
        for l in sorted(lignes, key=lambda x: (x["serie_complete_1975_2025"] != "oui", -int(x["nb_deficits"]))):
            w.writerow(l)
    with open(os.path.join(SORTIE, "A12_soldes_longs_OCDE.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(longs[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(longs)

    # Controle : OCDE contre AMECO (UBLG, % PIB) sur annees communes
    am = lire_ameco({"1.0.319.0.UBLG"})
    iso = {c.split(".")[0]: v["serie"] for c, v in am.items()}
    ctrl = []
    for p in pays:
        if p not in iso:
            continue
        s = data.get((p, "NLGQ"), {})
        com = [a for a in range(1975, 2026) if a in s and a in iso[p]]
        if not com:
            continue
        ecarts = [abs(s[a] - iso[p][a]) for a in com]
        signe = [a for a in com if (s[a] < 0) != (iso[p][a] < 0)]
        ctrl.append({"pays": p, "annees_communes": f"{min(com)}-{max(com)}", "n": len(com),
                     "ecart_abs_moyen_pts": round(sum(ecarts) / len(ecarts), 2), "ecart_abs_max_pts": round(max(ecarts), 2),
                     "annees_signe_different": " ".join(str(a) for a in signe)})
    with open(os.path.join(SORTIE, "A12_controle_ameco_ocde.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(ctrl[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(ctrl)
    # Controle UE : dernier excedent primaire (AMECO UBLGI, solde hors interets bruts, % PIB, 1995-2025)
    ue = ["BEL","BGR","CZE","DNK","DEU","EST","IRL","GRC","ESP","FRA","HRV","ITA","CYP","LVA","LTU","LUX","HUN","MLT","NLD","AUT","POL","PRT","ROM","SVN","SVK","FIN","SWE"]
    lig = []
    for c, v in am0.items():
        pz = c.split(".")[0]
        if pz in ue and c.endswith(".UBLGI"):
            sx = {a: x for a, x in v["serie"].items() if 1995 <= a <= 2025}
            exc = [a for a in sx if sx[a] > 0]
            lig.append({"pays": pz, "annees": "%d-%d" % (min(sx), max(sx)), "nb_excedents_primaires_1995_2025": len(exc),
                        "dernier_excedent_primaire": max(exc) if exc else "aucun",
                        "excedent_primaire_depuis_2002": "oui" if any(a >= 2002 for a in exc) else "non"})
    lig.sort(key=lambda x: str(x["dernier_excedent_primaire"]))
    with open(os.path.join(SORTIE, "A12_UE_excedents_primaires_AMECO.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(lig[0].keys()), delimiter=";")
        w.writeheader(); w.writerows(lig)
    print("ok", len(lignes), "pays ;", len(ctrl), "controles ;", len(lig), "pays UE (AMECO)")


if __name__ == "__main__":
    main()
