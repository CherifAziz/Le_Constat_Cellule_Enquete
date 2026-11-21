# -*- coding: utf-8 -*-
"""A11 - C-A11-001 : ordres de grandeur des dossiers rapportes au deficit S13 2025.
Deficit 2025 = 151,592 Md EUR (Eurostat gov_10dd_edpt1, B9, S13, FR, extraction commune du 20/11/2026) ;
PIB 2025 = 2 991,056 Md EUR (meme notification, citee par A04/Astra ; 1 pt PIB = 29,91 Md).
Chaque ligne est un objet DIFFERENT (cout affiche, rendement chiffre d'une reforme, montant non recurrent...) :
la colonne 'rapportable_au_deficit_annuel' dit si l'on peut la sommer avec d'autres. Aucun total n'est calcule pour les lignes non additionnables.
Usage : python -I a11_ordres_de_grandeur.py <sortie.csv>"""
import csv, sys
DEF, PIB = 151.592, 2991.056
L = [
 # dossier, objet, bas, haut, nature, additionnable, source
 ("D2 autoroutes", "Indexation de la TAT (LFI 2020) : cout pour les SCA, net d'IS", 1.0, 1.0, "recette deja acquise (cumul sur la duree, pas annuel)", "non", "IGF-CGEDD 2021 synthese p.2"),
 ("D2 autoroutes", "Recettes potentielles perdues lors de la privatisation de 2006 (valeur 2020)", 7.8, 7.8, "manque a gagner ponctuel 2006", "non", "Senat r19-709 synthese p.2"),
 ("D2 autoroutes", "Revenus supplementaires des SCA jusqu a l echeance des concessions (ART, cite par le Senat 2024 : jusqu a 40 Md)", 40.0, 40.0, "cumul pluriannuel jusqu a l echeance (2031-2036), non annuel ; objet distinct des ~40 Md de dividendes post-2022 du Senat 2020", "non", "Senat r24-065 synthese p.2"),
 ("D2 autoroutes", "Dividendes attendus apres 2022 (expertise commandee par le rapporteur, Senat 2020)", 40.0, 40.0, "cumul pluriannuel projete, flux prive, pas une perte publique", "non", "Senat r19-709 synthese p.6"),
 ("D6 conseil", "Depenses de conseil de l'Etat 2021 (ministeres 893,9 + 44 operateurs 171,9)", 1.0658, 1.0658, "depense brute annuelle (2021), pas une economie", "non", "Senat r21-578 synthese p.1"),
 ("D6 conseil", "Montant saisi a titre conservatoire (McKinsey) selon la presse citant le PNF - procedure en cours ; le prejudice (~68 M) est un calcul A11 (65,2/0,96)", 0.065, 0.065, "allegation au stade de l'enquete, montant cumule", "non", "[S] Consultor 04/09/2026 citant le PNF"),
 ("D4 aides", "Aides aux entreprises 2023, perimetre 1 (HCSP)", 82.0, 82.0, "stock de dispositifs, cout brut", "non", "HCSP juillet 2026"),
 ("D4 aides", "Aides aux entreprises 2023, perimetre 2 (HCSP)", 187.0, 187.0, "idem, inclut le perimetre 1", "non", "HCSP juillet 2026"),
 ("D4 aides", "Aides aux entreprises 2023 au sens large (Senat)", 211.0, 211.0, "idem, perimetre plus large", "non", "Senat r24-808 synthese p.7"),
 ("D3 CIR", "Cout de la depense fiscale 2026", 8.041, 8.041, "cout affiche", "non", "PLF 2026 VM II"),
 ("D3 CIR", "Rendement des mesures LFI 2025 (assiette)", 0.37, 0.44, "rendement annuel de reformes votees", "oui (rendement annuel vote)", "VM II 2026 tableau des mesures ; QE 5756"),
 ("D3 CIR", "Plafonnement par groupe (CPO 2021) : 0,47 Md (critere de detention 95 %) a 0,96 Md (critere 50 %)", 0.47, 0.96, "rendement ex ante d'une reforme non votee", "oui (rendement annuel, scenario non vote)", "IGF 2024 fiche 7 citant le CPO"),
 ("D5 Dutreil", "Cout de la depense fiscale", 4.0, 5.7, "cout affiche / estime", "non", "VM II 2026 ; IPP n°62"),
 ("D5 Dutreil", "Deux mesures IGF 2024 : Dutreil limite aux actifs professionnels + alignement du regime IR/IS au depart en retraite ('au moins une centaine de millions')", 0.1, 0.1, "rendement ex ante minimal pour DEUX mesures", "oui (rendement annuel, scenario non vote)", "IGF 2024 note de synthese p.8"),
 ("D7 TVA restauration", "Cout part Etat 2026", 2.275, 2.275, "cout affiche (part Etat)", "non", "VM II 2026"),
 ("D7 TVA restauration", "Suppression de cinq taux reduits (restauration, hotellerie, services de television, enceintes sportives, eaux en bouteille) - part restauration non isolee ; perimetre Etat/total TVA non verifie", 4.0, 4.0, "rendement ex ante pour cinq secteurs, avant effets de prix ; perimetre (part Etat ou TVA totale) non verifie", "non (perimetre non verifie)", "IGF 2024 note de synthese p.9"),
]
rows = []
for d, o, b, h, n, a, s in L:
    if a.startswith('oui'):
        rows.append([d, o, b, h, round(100*b/DEF, 2), round(100*h/DEF, 2), round(100*b/PIB, 3), round(100*h/PIB, 3), n, a, s])
    else:  # stock, cumul pluriannuel, ponctuel ou cout affiche : pas de ratio a un deficit annuel
        rows.append([d, o, b, h, '', '', '', '', n, a, s])
scen = [r for r in rows if r[9].startswith('oui (scenario)')]
sb, sh = sum(r[2] for r in scen), sum(r[3] for r in scen)
with open(sys.argv[1], 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['dossier', 'objet', 'bas_Md', 'haut_Md', 'bas_pct_deficit2025', 'haut_pct_deficit2025', 'bas_pct_PIB', 'haut_pct_PIB', 'nature', 'rapportable_au_deficit_annuel', 'source'])
    w.writerows(rows)
    w.writerow(['NB : aucune somme n est calculee : les rendements ont des perimetres (IS, DMTG, TVA part Etat ou totale), des horizons et des statuts (vote / non vote) differents'])
sys.stdout.reconfigure(encoding='utf-8')
for r in rows: print(r[:8])

