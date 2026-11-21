"""S07 - calculs : composition de l'effort français 2011-2014, multiplicateurs implicites
des pièces, profils de persistance, ratios bruts des programmes.
Usage : python -I calculs_S07.py <eurostat_programmes.csv> <sortie_txt>
Toutes les entrées chiffrées en dur ci-dessous sont recopiées des pièces citées (page en commentaire)."""
import sys, csv, collections

eu_csv, out = sys.argv[1], sys.argv[2]
L = []
def p(*a):
    L.append(" ".join(str(x) for x in a))

# C-S07-001 : effort structurel exécuté France (pts de PIB), millésime de chaque loi de règlement
# 2011 : AN n°75 p.84 (0,9 dont impôts 0,7) ; 2012 : AN n°1210 p.21 ; 2013 : AN n°2069 p.22 ;
# 2014 : Sénat n°604 p.14 (PO 0,2 ; dépenses 0,4 ; clef CI -0,1 ; total 0,5)
eff = {2011: (0.7, 0.2),  # 2011 : depenses 0,2 = residu 0,9 - 0,7 (non publie tel quel)
       2012: (1.1, 0.1), 2013: (1.4, 0.0), 2014: (0.2, 0.4)}
tot_r = sum(v[0] for v in eff.values()); tot_d = sum(v[1] for v in eff.values())
p("C-S07-001 France effort discretionnaire execute 2011-2014")
for y, (r, d) in eff.items():
    p(f"  {y}: recettes {r:.1f} depenses {d:.1f} total {r+d:.1f}")
p(f"  cumul: recettes {tot_r:.1f} depenses {tot_d:.1f} total {tot_r+tot_d:.1f} ; part recettes {tot_r/(tot_r+tot_d):.0%}")
p("  (clef credit d'impot 2014 -0,1 et contrecoup du plan de relance 2011 +0,6 hors effort)")
eff_tot = tot_r + tot_d

# C-S07-002 : multiplicateurs implicites
p("\nC-S07-002 Multiplicateurs implicites (perte de PIB / effort)")
# OFCE 2016 (Peleraux-Plane, tableau 1) : impact sur la croissance, effet direct national et total
direct = {2011: 0.7, 2012: 0.6, 2013: 1.0, 2014: 0.8}
total = {2011: 1.1, 2012: 1.3, 2013: 1.5, 2014: 1.0}
p(f"  OFCE 2016 : somme effet direct national 2011-14 = {sum(direct.values()):.1f} pt ; total (avec partenaires) = {sum(total.values()):.1f} pt")
p("    [NON COMPARABLE : numerateur OFCE (impulsion OFCE, e-mod), denominateur = effort du gouvernement ; indicatif seulement]")
p(f"    rapporte a l'effort execute du gouvernement ({eff_tot:.1f}) : direct {sum(direct.values())/eff_tot:.2f} ; total {sum(total.values())/eff_tot:.2f}")
p(f"    avec contrecoup de la relance (+0,6) au denominateur : direct {sum(direct.values())/(eff_tot+0.6):.2f}")
# OFCE 2015 (Heyer-Peleraux p.7 et 12) : impulsions 2011-13 et freinage total
imp15 = {2011: 1.8, 2012: 1.4, 2013: 1.1}; frein15 = {2011: 1.5, 2012: 2.1, 2013: 1.9}
p(f"  OFCE 2015 : impulsion 2011-13 = {sum(imp15.values()):.1f} ; freinage total = {sum(frein15.values()):.1f} ; ratio total/impulsion = {sum(frein15.values())/sum(imp15.values()):.2f}")
p(f"    meme impulsion, effet direct OFCE 2016 sur 2011-13 ({direct[2011]+direct[2012]+direct[2013]:.1f}) : ratio {(direct[2011]+direct[2012]+direct[2013])/sum(imp15.values()):.2f} (millesimes melanges, indicatif)")
# Commission QUEST (in 't Veld 2013, tableaux 2, 4, 5)
alone = [0.82, 1.67, 2.49, 1.54, 0.82, 0.39, 0.10, -0.11]  # France seule, 1 pt/an pendant 3 ans (effort cumule 1,2,3,3,...)
effcum = [1, 2, 3, 3, 3, 3, 3, 3]
p("  QUEST France seule, perte de PIB par point d'effort cumule (annees 1 a 8): " + ", ".join(f"{a/e:.2f}" for a, e in zip(alone, effcum)))
simul = [1.39, 2.93, 4.78]; effFR = [1.37, 2.38, 3.68]
p("  QUEST 2011-13 simultane (avec retombees) : " + ", ".join(f"{a/e:.2f}" for a, e in zip(simul, effFR)))
# Blanchard-Leigh : multiplicateur suppose ~0,5 (p.20) + |beta|
for lab, b in (("prev. 2010 (2010-11)", 1.095), ("panel 2009-12", 0.667), ("prev. 2011", 0.467), ("prev. 2012", 0.357)):
    p(f"  Blanchard-Leigh {lab}: 0,5 + {b} = {0.5+b:.2f} (lecture conditionnelle a un multiplicateur suppose de 0,5 ; les auteurs excluent d'en tirer une estimation ponctuelle, p.13)")
# GLP (p.26) a deux ans
g_dep, g_rec, g_moy = 0.43, 1.29, 0.62
p(f"  GLP a 2 ans : moyenne {g_moy} ; depenses {g_dep} ; recettes {g_rec}")
p(f"    pondere composition France 2011-14 ({tot_r/eff_tot:.0%} recettes) : {(tot_r*g_rec+tot_d*g_dep)/eff_tot:.2f}")
p(f"    pondere composition 50/50 (hypothese A15) : {(g_rec+g_dep)/2:.2f}")

# Mesange 2010 (Insee G2010/03, p.71 et p.100 du document) : horizons 1, 2, 3, 5, 10 ans, long terme
mes_po = [0.3, 0.6, 0.8, 1.0, 1.1, 1.3]; mes_inv = [1.12, 1.32, 1.33, 1.03, 0.74, 0.19]
p("  Mesange 2010, horizons 1,2,3,5,10 ans, LT : hausse generique des PO de 1 pt -> PIB " + ", ".join(f"-{x}" for x in mes_po)
  + " ; investissement public +1 pt -> PIB " + ", ".join(str(x) for x in mes_inv) + " (variantes naives, taux reels exogenes)")

# C-S07-003 : profil de persistance A15 contre QUEST (France seule), pour 1 pt permanent introduit en annee 1
p("\nC-S07-003 Persistance : perte de PIB pour 1 pt d'effort permanent")
a15 = [0.6, 0.6, 0.3, 0.3, 0.3, 0.12, 0.12, 0.12]
# QUEST : reponse a un choc unique non publiee ; on n'a que le profil de 3 chocs successifs -> on ne deconvolue pas
p("  A15 (multiplicateur 0,6 x profil A13) : " + ", ".join(str(x) for x in a15))
p("  QUEST : seul le profil de 3 efforts successifs est publie (ci-dessus) ; retour a 0 en annee 7-8 sous hypothese de credibilite pleine en annee 4")

# C-S07-004 : programmes, series Eurostat (extraction S07 du 21/11/2026)
d = collections.defaultdict(dict)
for r in csv.DictReader(open(eu_csv, encoding="utf-8"), delimiter=";"):
    d[(r["geo"], r["serie"])][int(r["annee"])] = float(r["valeur"])
p("\nC-S07-004 Programmes : croissance cumulee et dette (Eurostat)")
win = {"EL": (2010, 2013), "PT": (2011, 2014), "IE": (2011, 2013), "ES": (2012, 2014), "FR": (2011, 2014)}
for g, (a, b) in win.items():
    lvl = 1.0
    for y in range(a, b + 1):
        lvl *= 1 + d[(g, "pib_vol_pct")][y] / 100
    dette0 = d[(g, "dette_pct_pib")][a - 1]; dette1 = d[(g, "dette_pct_pib")][b]
    pic = max((v, y) for y, v in d[(g, "dette_pct_pib")].items() if y <= 2019)
    dr = d[(g, "recettes_pct_pib")][b] - d[(g, "recettes_pct_pib")][a - 1]
    dd = d[(g, "depenses_pct_pib")][b] - d[(g, "depenses_pct_pib")][a - 1]
    p(f"  {g} {a}-{b}: PIB volume cumule {100*(lvl-1):+.1f} % ; dette {dette0:.1f} -> {dette1:.1f} ({dette1-dette0:+.1f} pts) ; pic {pic[0]:.1f} en {pic[1]} ; d recettes {dr:+.1f} ; d depenses {dd:+.1f} (ratios observes, non mesures)")

open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
