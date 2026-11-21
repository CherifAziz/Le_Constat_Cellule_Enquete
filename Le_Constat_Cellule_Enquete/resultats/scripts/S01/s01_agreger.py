# -*- coding: utf-8 -*-
"""S01 - agregation des mesures (S01_mesures_1975_1999.csv) en points de PIB et comparaison
avec les variations observees (base commune Insee base 2020, extraction 20/11/2026).

Conventions (voir S01.md, section 2) :
- montant retenu = montant constate s'il est numerique, sinon montant annonce (ex ante) ;
  les deux colonnes sont aussi agregees separement.
- effet sur le solde : recette + => +, recette - => -, depense + => -, depense - => +.
- categories exclues des sommes de « decisions » : agregat, ajustement, transfert ;
  tresorerie et retour (reports d'impot et leur encaissement) comptes a part ;
  lignes de bareme de l'IR (indexation) comptees a part : convention A04
  (« une indexation n'est pas une mesure »), alors que le REF de l'epoque les compte
  comme « amenagement des droits ».
- cumul 1974-1985 : seules les mesures « permanent » s'additionnent d'une annee a l'autre
  (hypothese : leur poids en points de PIB reste constant) ; les mesures « temporaire »
  ne comptent que l'annee de leur effet.
- PIB : Insee base 2020 (A02_series_1960_2000.csv, colonne pib_md, Md EUR) x 6,55957.
Sorties : donnees/S01/S01_agregats_par_exercice.csv, S01_agregats_sortie.txt
"""
import csv, os, sys, re
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RES = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
S01 = os.path.join(RES, "S01")
out = []


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    out.append(s)


def num(x):
    x = (x or "").strip().replace(",", ".")
    try:
        return float(x)
    except ValueError:
        return None


# --- PIB et ratios observes
pib = {}
for r in csv.DictReader(open(os.path.join(RES, "A02", "A02_series_1960_2000.csv"), encoding="utf-8"), delimiter=";"):
    if r.get("pib_md"):
        pib[int(r["annee"])] = float(r["pib_md"]) * 6.55957  # Md F
ratios = defaultdict(dict)
for r in csv.DictReader(open(os.path.join(RES, "commun", "base_insee_dep_rec_pctPIB.csv"), encoding="utf-8-sig"), delimiter=";"):
    ratios[r["serie"]][int(r["annee"])] = float(r["valeur"])
po = {}
for r in csv.DictReader(open(os.path.join(RES, "A04", "a04_po_recettes_1959_2025.csv"), encoding="utf-8"), delimiter=";"):
    po[int(r["annee"])] = {k: float(r[k]) for k in ("PO_pctPIB", "PO_APUC_pctPIB", "PO_APUL_pctPIB", "PO_ASSO_pctPIB") if r[k]}

# --- table des mesures
rows = list(csv.DictReader(open(os.path.join(S01, "S01_mesures_1975_1999.csv"), encoding="utf-8"), delimiter=";"))


def categorie(r):
    t = r["temporaire_ou_permanent"].strip()
    if r["sens"].strip() == "transfert":
        return "transfert"
    if t in ("agregat", "ajustement", "tresorerie", "retour", "detail", "indexation"):
        return t
    if "Barème de l'IR" in r["mesure"] or r["mesure"].startswith("IR :") or "Indexation des tranches" in r["mesure"] or "indexé" in r["mesure"]:
        return "indexation"
    return t  # permanent / temporaire


def perim(r):
    s = r["perimetre"].lower()
    if "sécurité sociale" in s or "unédic" in s:
        return "ASSO"
    if s.startswith("collectivités"):
        return "APUL"
    return "Etat"


signe = {"recette +": 1, "recette -": -1, "depense +": -1, "depense -": 1}
par_an = defaultdict(lambda: defaultdict(float))
detail = []
for r in rows:
    an = int(r["annee"][:4])
    cat = categorie(r)
    a, c = num(r["montant_annonce"]), num(r["montant_constate"])
    m = c if c is not None else a
    if m is None or r["sens"].strip() not in signe or an not in pib:
        continue
    pt = 100 * m / pib[an]
    s = signe[r["sens"].strip()]
    nature = "rec" if r["sens"].startswith("recette") else "dep"
    key = f"{cat}|{nature}|{perim(r)}"
    par_an[an][key] += pt * (1 if nature == "rec" else 1) * (1 if s > 0 else -1) if nature == "rec" else pt * (1 if r["sens"].strip() == "depense +" else -1)
    detail.append((an, cat, nature, perim(r), round(pt, 3), r["mesure"][:70]))

# par_an[an][key] : pour les recettes, points de PIB signes (+ = hausse) ; pour les depenses, + = hausse de depense
p("=== Mesures par exercice, points de PIB de l'annee (recettes : + = hausse ; depenses : + = hausse) ===")
cats = ["permanent", "temporaire", "indexation", "tresorerie", "retour"]
lignes_csv = ["annee;pib_MdF;categorie;nature;perimetre;points_PIB"]
for an in sorted(par_an):
    items = sorted(par_an[an].items())
    p(f"{an} (PIB {pib[an]:.0f} Md F) : " + " ; ".join(f"{k}={v:+.2f}" for k, v in items if k.split('|')[0] in cats))
    for k, v in items:
        c, n, pe = k.split("|")
        lignes_csv.append(f"{an};{pib[an]:.1f};{c};{n};{pe};{v:.4f}")
with open(os.path.join(S01, "S01_agregats_par_exercice.csv"), "w", encoding="utf-8") as g:
    g.write("\n".join(lignes_csv) + "\n")

# --- sommes separees : annonce seul / constate seul (decisions permanentes et temporaires)
p("\n=== Sommes séparées par exercice (Md F) : annoncé (ex ante) / constaté, décisions seulement ===")
for an in sorted({int(r["annee"][:4]) for r in rows}):
    sa = sum(num(r["montant_annonce"]) for r in rows if int(r["annee"][:4]) == an and categorie(r) in ("permanent", "temporaire") and num(r["montant_annonce"]) is not None and r["sens"].strip() in signe)
    sc = sum(num(r["montant_constate"]) for r in rows if int(r["annee"][:4]) == an and categorie(r) in ("permanent", "temporaire") and num(r["montant_constate"]) is not None and r["sens"].strip() in signe)
    p(f"{an} : annoncé (valeurs absolues) {sa:.1f} ; constaté (valeurs absolues) {sc:.1f}")

# --- cumul 1975-1985 des decisions datees (permanent cumule ; temporaire de l'annee 1985 seulement)
def cumul(an0, an1, nature, perim_=None):
    perm = sum(v for an in par_an if an0 <= an <= an1 for k, v in par_an[an].items()
               if k.startswith("permanent|" + nature) and (perim_ is None or k.endswith(perim_)))
    temp_fin = sum(v for k, v in par_an.get(an1, {}).items()
                   if k.startswith("temporaire|" + nature) and (perim_ is None or k.endswith(perim_)))
    return perm, temp_fin


p("\n=== T-02 : cumul 1975-1985 des mesures datees retrouvees sur piece (points de PIB) ===")
for nat, lab in (("dep", "Dépenses"), ("rec", "Recettes")):
    for pe in (None, "Etat", "ASSO", "APUL"):
        perm, tf = cumul(1975, 1985, nat, pe)
        p(f"{lab:9s} perimetre={pe or 'tous':5s} : permanentes cumulées {perm:+.2f} ; temporaires encore actives en 1985 {tf:+.2f}")
obs_dep = ratios["Dépenses"][1985] - ratios["Dépenses"][1974]
obs_rec = ratios["Recettes"][1985] - ratios["Recettes"][1974]
p(f"Observé (base commune) : dépenses {ratios['Dépenses'][1974]:.2f} -> {ratios['Dépenses'][1985]:.2f} ({obs_dep:+.2f}) ; recettes {ratios['Recettes'][1974]:.2f} -> {ratios['Recettes'][1985]:.2f} ({obs_rec:+.2f})")
for k in ("PO_pctPIB", "PO_APUC_pctPIB", "PO_APUL_pctPIB", "PO_ASSO_pctPIB"):
    p(f"  {k} : {po[1974][k]:.2f} -> {po[1985][k]:.2f} ({po[1985][k]-po[1974][k]:+.2f})")
perm_dep, _ = cumul(1975, 1985, "dep")
p(f"Dépenses : part de la variation observée rattachée à des mesures permanentes datées {100*perm_dep/obs_dep:.0f} % ; reste non rattaché {obs_dep-perm_dep:+.2f} (ce n'est pas « la conjoncture »)")
p("PO par sous-secteur selon l'année de base (1974 suspecte : saut APUC/APUL) :")
for b in (1973, 1974, 1975):
    p("  base %d -> 1985 : " % b + " ; ".join(f"{k.split('_')[1]} {po[1985][k]-po[b][k]:+.2f}" for k in ("PO_pctPIB", "PO_APUC_pctPIB", "PO_APUL_pctPIB", "PO_ASSO_pctPIB")))
for pe, k in (("Etat", "PO_APUC_pctPIB"), ("ASSO", "PO_ASSO_pctPIB"), ("APUL", "PO_APUL_pctPIB")):
    m, _ = cumul(1975, 1985, "rec", pe)
    lo, hi = sorted([po[1985][k] - po[b][k] for b in (1973, 1974, 1975)])[0], sorted([po[1985][k] - po[b][k] for b in (1973, 1974, 1975)])[-1]
    p(f"  {pe} : mesures permanentes documentées {m:+.2f} pour une variation observée de {lo:+.2f} à {hi:+.2f}")

# conventions pour les recettes de l'Etat 1975-1985
acc = re.compile(r"TIPP|alcool|tabac|vignette|boissons|timbre|carburant|produits pétroliers|bateaux", re.I)
convA = convB = convC = 0.0
for r in rows:
    an = int(r["annee"][:4])
    if not (1975 <= an <= 1985) or perim(r) != "Etat" or not r["sens"].startswith("recette"):
        continue
    cat = categorie(r)
    a, c = num(r["montant_annonce"]), num(r["montant_constate"])
    m = c if c is not None else a
    if m is None:
        continue
    v = 100 * m / pib[an] * (1 if r["sens"].strip() == "recette +" else -1)
    if cat == "permanent":
        convA += v
        convB += v
        if not acc.search(r["mesure"]):
            convC += v
    elif cat == "indexation":
        convB += v
p(f"Recettes de l'État 1975-1985, mesures permanentes cumulées : convention A04 (barème exclu) {convA:+.2f} ; convention REF (barème inclus) {convB:+.2f} ; barème ET actualisations d'accises exclus {convC:+.2f}")

# --- sous-periodes
p("\n=== Sous-périodes : mesures permanentes + temporaires de chaque année (somme des effets annuels, points) ===")
for a0, a1 in ((1974, 1974), (1975, 1975), (1976, 1980), (1981, 1983), (1984, 1985), (1986, 1988), (1989, 1992), (1998, 1999)):
    d = sum(v for an in par_an if a0 <= an <= a1 for k, v in par_an[an].items() if k.split("|")[0] in ("permanent", "temporaire") and "|dep|" in k)
    r_ = sum(v for an in par_an if a0 <= an <= a1 for k, v in par_an[an].items() if k.split("|")[0] in ("permanent", "temporaire") and "|rec|" in k)
    idx = sum(v for an in par_an if a0 <= an <= a1 for k, v in par_an[an].items() if k.startswith("indexation"))
    od = ratios["Dépenses"].get(a1, float("nan")) - ratios["Dépenses"].get(a0 - 1, float("nan"))
    orr = ratios["Recettes"].get(a1, float("nan")) - ratios["Recettes"].get(a0 - 1, float("nan"))
    p(f"{a0}-{a1} : mesures dépenses {d:+.2f} (obs. {od:+.2f}) ; mesures recettes {r_:+.2f} (obs. {orr:+.2f}) ; barème IR à part {idx:+.2f}")

# --- T-01 : 1975, voté contre exécuté (Md F)
p("\n=== T-01 : plans de soutien de 1975, voté contre exécuté (budget de l'État, Md F) ===")
vote_cp, decrets, recettes_prev = 23.8, 2.9, 14.1
report_76 = 6.0 + 0.2 + 3.5
recettes_const = 7.4 + 1.0
p(f"Crédits votés (3 LFR) {vote_cp} + décrets d'avances {decrets} = {vote_cp+decrets:.1f} ; reportés sur 1976 ≈ {report_76:.1f} ({100*report_76/(vote_cp+decrets):.0f} %) ; exécutés en 1975 ≈ {vote_cp+decrets-report_76:.1f}")
p(f"Pertes de recettes prévues {recettes_prev} ; constatées en 1975 ≈ {recettes_const:.1f} (reports IS 5,0 + IR 2,4 ; aide fiscale ≈ 1,0) ({100*recettes_const/recettes_prev:.0f} %)")
tot_v, tot_e = vote_cp + decrets + recettes_prev, vote_cp + decrets - report_76 + recettes_const
p(f"Total plans : voté/prévu {tot_v:.1f} ; exécuté en 1975 ≈ {tot_e:.1f} ({100*tot_e/tot_v:.0f} %) ; déficit d'exécution 1975 : 37,8 (règlement) ; part de l'exécuté : {100*tot_e/37.8:.0f} %")
p(f"Dont trésorerie pure (reports d'impôt rendus en 1976) : 7,4 ; hors trésorerie, exécuté ≈ {tot_e-7.4:.1f} soit {100*(tot_e-7.4)/37.8:.0f} % du déficit d'exécution ; en points de PIB 1975 : {100*tot_e/pib[1975]:.2f} (dont {100*(tot_e-7.4)/pib[1975]:.2f} hors trésorerie)")

# --- taux de cotisation (IPP) : taux global sous plafond, moyenne annuelle
p("\n=== Taux de cotisation sous plafond, régime général + Unédic (employeur + salarié), moyenne annuelle (Barèmes IPP) ===")
# (date effet, taux) par composante, d'après S01_taux_cotisations_ipp_1970_2000.csv (lecture manuelle des tables)
comp = {
    "maladie_empl": [(1971.0, 12.45), (1976.0, 12.95), (1976.75, 13.45), (1984.0, 12.6), (1992.0, 12.8)],
    "maladie_sal": [(1967.75, 3.5), (1976.0, 4.0), (1976.75, 4.5), (1979.58, 5.5), (1987.5, 5.9), (1991.5, 6.8)],
    "vieil_empl": [(1974.0, 7.25), (1976.0, 7.5), (1976.75, 7.7), (1979.0, 8.2)],
    "vieil_sal": [(1967.75, 3.0), (1976.0, 3.25), (1976.75, 3.45), (1979.0, 4.7), (1984.0, 5.7), (1986.58, 6.4), (1987.5, 6.6), (1989.0, 7.6)],
    "famille_empl": [(1970.58, 10.5), (1974.25, 9.0)],
    "chomage": [(1973.0, 0.70), (1974.0, 0.80), (1975.0, 1.80), (1975.5, 2.40), (1977.0, 2.20), (1978.0, 2.40), (1978.33, 3.00), (1979.25, 3.60), (1982.85, 4.80), (1983.5, 5.80), (1984.25, 4.00), (1985.5, 6.20), (1985.83, 4.58)],
}


def taux(c, t):
    v = None
    for d, x in comp[c]:
        if d <= t + 1e-9:
            v = x
    return v


moy = {}
for an in range(1974, 1986):
    tot = 0
    for c in comp:
        tot += sum(taux(c, an + m / 12) for m in range(12)) / 12
    moy[an] = tot
p(" ".join(f"{an}:{moy[an]:.2f}" for an in moy))
p(f"1974 -> 1985 : {moy[1974]:.2f} -> {moy[1985]:.2f} points de salaire brut sous plafond ({moy[1985]-moy[1974]:+.2f} ; x{moy[1985]/moy[1974]:.3f})")
p("Hors champ : régimes complémentaires (ARRCO/AGIRC), fonction publique, non-salariés, accidents du travail, déplafonnements (maladie 1981-1984), assiette au-dessus du plafond.")

# --- part des hausses de taux dans la hausse des cotisations effectives (ordre de grandeur, niveau D)
import openpyxl  # noqa: E402
wb = openpyxl.load_workbook(os.path.join(RES, "commun", "insee_cn_t_3201.xlsx"), read_only=True, data_only=True)
rows3201 = list(wb.worksheets[0].iter_rows(values_only=True))
ci = {str(v): i for i, v in enumerate(rows3201[2]) if v}
ser = {}
for r in rows3201:
    lab = str(r[1]) if r[1] else ""
    for code in ("(D61)", "(D612)", "(D2)", "(D91r)"):
        if code in lab and code not in ser:
            ser[code] = {y: float(r[ci[str(y)]]) for y in (1974, 1985)}
    if "(D5)" in lab and float(r[ci["1974"]] or 0) > 1:
        ser["(D5)"] = {y: float(r[ci[str(y)]]) for y in (1974, 1985)}
pib_eur = {y: pib[y] / 6.55957 for y in (1974, 1985)}
pct = {k: {y: 100 * v[y] / pib_eur[y] for y in v} for k, v in ser.items()}
eff = {y: pct["(D61)"][y] - pct["(D612)"][y] for y in (1974, 1985)}
p("\n=== Recettes 1974-1985 par nature (Insee 3.201, base 2020 ; % du PIB) ===")
for k in ("(D2)", "(D5)", "(D61)", "(D612)"):
    p(f"{k} : {pct[k][1974]:.2f} -> {pct[k][1985]:.2f} ({pct[k][1985]-pct[k][1974]:+.2f})")
p(f"Cotisations effectives (D61 - D612) : {eff[1974]:.2f} -> {eff[1985]:.2f} ({eff[1985]-eff[1974]:+.2f})")
effet_taux = eff[1974] * (moy[1985] / moy[1974] - 1)
p(f"Effet « taux » si tous les taux effectifs avaient suivi le taux légal sous plafond RG+Unédic (x{moy[1985]/moy[1974]:.3f}) à assiette/PIB constante : {effet_taux:+.2f} point, soit {100*effet_taux/(eff[1985]-eff[1974]):.0f} % de la hausse des cotisations effectives ; reste (assiette, déplafonnements, autres régimes) {eff[1985]-eff[1974]-effet_taux:+.2f}")

with open(os.path.join(S01, "S01_agregats_sortie.txt"), "w", encoding="utf-8") as g:
    g.write("\n".join(out) + "\n")
