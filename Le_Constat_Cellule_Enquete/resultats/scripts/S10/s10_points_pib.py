"""S10 — conversion en points de PIB du coût des sept décisions sociales de 1974-1982.

Entrées (lecture seule) :
  - resultats/donnees/S03/S03_series_annuelles.csv : PIB_MEUR (Insee base 2020, M EUR courants)
Sorties :
  - resultats/donnees/S10/S10_table_decisions.csv
  - resultats/donnees/S10/S10_total_1985.csv
Conventions :
  - 1 EUR = 6,55957 F (conversion légale) ; PIB en Md F = PIB_MEUR * 6,55957 / 1000.
  - Variante « PIB d'époque » pour 1985 : 171,5 Md F / 3,7 % (Dares/SES 1986, p. 2) ≈ 4 635 Md F.
  - Report en 1985 d'un coût connu une autre année : on suppose que la mesure garde
    la même part du PIB (convention « part constante », notée PC) ; une mesure supprimée
    ou absorbée avant 1985 vaut 0 en 1985 (notée ABS).
Chaque montant renvoie à un identifiant F-S10-nnn du dossier S10.md.
"""
import csv, os

RAC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats"
F_S03 = os.path.join(RAC, "donnees", "S03", "S03_series_annuelles.csv")
OUT = os.path.join(RAC, "donnees", "S10")
EUR_F = 6.55957

pib_mdf = {}
with open(F_S03, encoding="utf-8", errors="replace") as f:
    for row in csv.DictReader(f, delimiter=";"):
        pib_mdf[int(row["annee"])] = float(row["PIB_MEUR"]) * EUR_F / 1000.0
PIB85_EPOQUE = 171.5 / 0.037

def pts(mdf, annee):
    return 100.0 * mdf / pib_mdf[annee]

def report85(mdf, annee):
    """Part constante du PIB : montant de l'année `annee` reporté en 1985 (Md F)."""
    return mdf / pib_mdf[annee] * pib_mdf[1985]

# --- montants (Md F courants) -------------------------------------------------
# 1. ASA (accord 14/10/1974) : coût constaté/prévu 1978, supprimée en 1979, nulle en 1985 (ABS)
asa_1978_total = 6.7           # F-S10-016 (ASA entière, Assedic + aide publique, prévision 1978)
asa_1978_complement = 1.3 * 2  # F-S10-017 (complément d'attente, 1er semestre 1978 doublé)
# 2. Loi du 30/12/1975 : coût annoncé « de l'ordre de 900 M F » (régime général) + 315 M F
#    (complémentaires) ; année pleine supposée 1977 ; absorbée par la retraite à 60 ans (1983)
loi75 = 0.900 + 0.250 + 0.065  # F-S10-030
# 3. Garantie de ressources et préretraites, coût constaté 1985
rub_B_1985 = 56.2026           # F-S10-001
gr_1985 = 29.0                 # F-S10-002 (« près de 29 »)
cs_1985 = 10.0                 # F-S10-002 (contrats de solidarité, « plus de 10 ») -> poste 7
part_demission = 164300 / (164300 + 171700)  # F-S10-011 (1er semestre 1982)
# 4. Complément familial : coût net annoncé, année d'effet 1978
cf_net_bas, cf_net = 2.6, 3.7  # F-S10-021
cf_brut_1982 = 15.136          # F-S10-022 (masse brute Cnaf 1982, pour le plafond extrême)
# 5. Généralisation 1978 : coût non évalué à l'époque (F-S10-031). Borne haute calculée :
#    1,2 million de personnes non couvertes x prestation santé moyenne par habitant 1985
non_couverts = 1.2e6           # F-S10-031
# santé Drees 1985 (S03_series_annuelles, colonne Santé_MEUR) / population
# 6. AF et AL 1981-1982 : surcoût annoncé 1982
af81_1982 = 7.86               # F-S10-023 (mesures 1981, ensemble des régimes, 1982)
af82_1982 = 4.05               # F-S10-024 (revalorisation 1982 et amélioration des PF)
# 7. Contrats de solidarité (préretraite), part État + Unédic, constaté 1985 ; 39 h et
#    cinquième semaine : hors prestations, non chiffrés (introuvable)

with open(F_S03, encoding="utf-8", errors="replace") as f:
    rows = {int(r["annee"]): r for r in csv.DictReader(f, delimiter=";")}
cle_sante = [k for k in rows[1985] if k.startswith("Sant") and k.endswith("_MEUR")][0]
sante_par_tete_85 = float(rows[1985][cle_sante]) * EUR_F * 1e6 / (float(rows[1985]["pop_moy_milliers"]) * 1e3)
gen_borne = non_couverts * sante_par_tete_85 / 1e9

# (bas, central, haut) en Md F 1985
postes = [
  ("1 ASA 1974", "6,7 (ASA entière) ; 2,6 (complément)", 1978, pts(asa_1978_total, 1978),
   (0.0, 0.0, report85(asa_1978_complement, 1978)),
   "ABS [M] : suppression en 1979 et fusion de l'allocation spéciale en 1984 non établies sur pièce ; haut = complément d'attente 1978 en PC", "D (prévision 1978)"),
  ("2 Loi 30/12/1975", f"{loi75:.3f} annoncé", 1977, pts(loi75, 1977),
   (0.0, 0.0, report85(loi75, 1977)), "ABS (retraite à 60 ans, comptée par S01/S03) ; haut = PC", "B (annonce, coût maximal)"),
  ("3 GR et préretraites", f"{rub_B_1985:.1f} rubrique B ; {gr_1985} GR", 1985, pts(gr_1985, 1985),
   (gr_1985 * part_demission, gr_1985, rub_B_1985 - cs_1985),
   "bas = GR démission (clé effectifs 1982) ; central = GR ; haut = rubrique B hors contrats de solidarité", "B (constaté provisoire)"),
  ("4 Complément familial", f"{cf_net} net annoncé (2,6 initial)", 1978, pts(cf_net, 1978),
   (report85(cf_net_bas, 1978), report85(cf_net, 1978), report85(cf_net, 1978)), "PC", "B (annonce) ; constaté net introuvable"),
  ("5 Généralisation 1978", "non évalué à l'époque", 1978, float("nan"),
   (0.0, 0.0, gen_borne), "haut = borne calculée (1,2 M pers. x santé/hab. 1985)", "E (borne)"),
  ("6 AF et AL 1981-1982", f"{af81_1982} + {af82_1982}", 1982, pts(af81_1982 + af82_1982, 1982),
   (report85(af81_1982, 1982), report85(af81_1982 + af82_1982, 1982), report85(af81_1982 + af82_1982, 1982)),
   "PC (surestime 1985 : BMAF sous-indexée après 1982)", "B (annonce)"),
  ("7 Contrats de solidarité (39 h, 5e semaine : non chiffrés)", f"> {cs_1985} constaté", 1985, pts(cs_1985, 1985),
   (cs_1985, cs_1985, cs_1985), "constaté 1985 ; 39 h et 5e semaine hors prestations, introuvables", "B (constaté provisoire)"),
]

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "S10_table_decisions.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["decision", "cout_source_MdF", "annee", "pts_PIB_annee_source",
                "MdF_1985_bas", "MdF_1985_central", "MdF_1985_haut",
                "pts_1985_bas", "pts_1985_central", "pts_1985_haut", "convention", "niveau"])
    for d, c, a, p, (b, m, h), conv, niv in postes:
        w.writerow([d, c, a, f"{p:.3f}", f"{b:.2f}", f"{m:.2f}", f"{h:.2f}",
                    f"{pts(b,1985):.3f}", f"{pts(m,1985):.3f}", f"{pts(h,1985):.3f}", conv, niv])
        print(f"{d:45s} src {a} {p:6.3f} pt | 1985 Md F {b:6.2f} {m:6.2f} {h:6.2f} | pts {pts(b,1985):.3f} {pts(m,1985):.3f} {pts(h,1985):.3f}")

tot = [sum(x[4][i] for x in postes) for i in range(3)]
# plafond extrême : masses brutes (rubrique B entière, complément familial brut reporté, etc.)
extreme = rub_B_1985 + report85(cf_brut_1982, 1982) + report85(af81_1982 + af82_1982, 1982) \
          + report85(loi75, 1977) + gen_borne + report85(asa_1978_total, 1978)  # ASA entière reportée (PC)
print(f"PIB 1985 base 2020 = {pib_mdf[1985]:.0f} Md F ; époque = {PIB85_EPOQUE:.0f} Md F")
print(f"santé par habitant 1985 = {sante_par_tete_85:.0f} F ; borne généralisation = {gen_borne:.2f} Md F")
print("TOTAL 1985 Md F bas/central/haut:", [round(x, 1) for x in tot])
print("TOTAL 1985 pts (base 2020):", [round(pts(x, 1985), 2) for x in tot])
print("TOTAL 1985 pts (PIB d'époque):", [round(100 * x / PIB85_EPOQUE, 2) for x in tot])
print(f"Plafond extrême (masses brutes) : {extreme:.1f} Md F = {pts(extreme,1985):.2f} pt (base 2020), {100*extreme/PIB85_EPOQUE:.2f} pt (époque)")
print(f"Pour info : ASA 1978 complément = {pts(asa_1978_complement,1978):.3f} pt ; part démission GR = {part_demission:.3f}")
# Sensibilité « hors liste » (angle mort) : décisions postérieures à 1974 non comprises dans les sept
aah_1982 = 8.1     # CCSS juin 1983, p. 16 imprimée : allocations aux adultes handicapés (Cnaf) 1982 — F-S10-026
fne_1985 = 9.7     # F-S10-002 : allocations spéciales du FNE (instrument de 1963, élargi après 1974)
sider_1985 = 4.3   # F-S10-002 : mesures d'âge sidérurgie (1979, 1984)
hors = report85(aah_1982, 1982) + fne_1985 + sider_1985
aah85 = report85(aah_1982, 1982)
print(f"Hors liste (AAH reportée PC + FNE + sidérurgie) : {hors:.1f} Md F = {pts(hors,1985):.2f} pt ; "
      f"central + hors liste = {pts(tot[1]+hors,1985):.2f} pt")
# La variante haute et le plafond extrême contiennent déjà FNE et sidérurgie (rubrique B) : on n'ajoute que l'AAH
print(f"Haut + AAH = {pts(tot[2] + aah85,1985):.2f} pt ; extrême + AAH = {pts(extreme + aah85,1985):.2f} pt "
      f"({100*(extreme+aah85)/PIB85_EPOQUE:.2f} pt au PIB d'époque)")
with open(os.path.join(OUT, "S10_total_1985.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["variante", "MdF_1985", "pts_PIB_base2020", "pts_PIB_epoque", "seuil_S03_pts"])
    for nom, x in zip(["bas", "central", "haut"], tot):
        w.writerow([nom, f"{x:.1f}", f"{pts(x,1985):.3f}", f"{100*x/PIB85_EPOQUE:.3f}", "3"])
    w.writerow(["plafond_extreme_masses_brutes", f"{extreme:.1f}", f"{pts(extreme,1985):.3f}", f"{100*extreme/PIB85_EPOQUE:.3f}", "3"])
