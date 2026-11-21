# C01 — table des chiffres centraux communs (cellule contre Codex). Écrit donnees\C01\C01_chiffres_centraux.csv
# Valeurs relevées à la main dans les pièces citées ; les recalculs de C01 viennent de c01_03_recalcul_codex.py
# (copie de codex\calculs\annuel.csv) et de la base commune.
import csv
O = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\C01\C01_chiffres_centraux.csv"
H = ["n", "chiffre", "valeur_cellule", "ou_cellule", "valeur_codex", "ou_codex", "ecart", "cause_ecart", "classement", "remarque_C01"]
R = [
["01", "Déficit public 2025 (S13, B9)", "151,6 Md€ ; 5,1 % du PIB (152,5 Md€ = millésime de mai 2026)", "vague1 §2 règle 1 ; A18_verification_25 V03 (151,592)",
 "151,592 Md€ ; 5,07 % ; 152,532 Md€ dans l'Insee Première de mai", "02_comptabilite_reconciliee (tableau « hors intérêts ») ; audit l.25",
 "0", "aucune ; les deux équipes datent les deux millésimes (mai / août 2026)", "accord", "Codex localise la révision de 0,94 Md€ dans la seule composante ASSO"],
["02", "Dernier excédent", "1974 : +0,1 % du PIB (+0,199 Md€) ; 51 déficits 1975-2025", "A18_verification_25 V01 ; vague1 §3.1",
 "1974 : +0,199 Md€, +0,096 % ; déficits antérieurs 1967-1969, 1971, 1973", "audit l.7 ; rapport_integral §1",
 "0", "aucune", "accord", "Les deux équipes signalent que la série « hors éléments imputés » ou la base 2005 change le signe ou le niveau autour de 1974 (cellule) / que l'excédent disparaît à l'entier (Codex)"],
["03", "Écart de dépenses avec la zone euro", "2025 : 7,5 pts (EA20 avec la France) ; 9,24 pts hors France. 2024 (fonctions) : 7,77 avec la France, 9,61 hors France", "vague1 §2 règles 4 et 5 ; A18_verification_25 V05-V06",
 "2025 : 7,5 pts (publiés). 2024 (fonctions) : 7,77 recalculé avec EA20, 9,61 hors France ; mais 8,1 (ratios diffusés) dans l'audit l.51", "audit l.51 ; 02_comptabilite_reconciliee §« Quel voisin » ; calculs\\fonctions_2024.csv",
 "0 sur 2025 publié ; 0,00 à 0,01 sur 2024 recalculé ; Codex ne donne pas 2025 hors France", "méthode identique (montants / PIB recalculé) ; le 8,1 de l'audit Codex est le ratio diffusé, que les deux équipes jugent incohérent (PIB d'un millésime antérieur)", "accord",
 "Concordance à la deuxième décimale (7,77 ; 9,61) obtenue indépendamment. Incohérence interne chez Codex : audit 8,1 contre comptabilité 7,77"],
["04", "Écart de recettes avec la zone euro", "2025 : 5,4 pts en recettes totales ; 6,66 hors France ; 4,7 pts en impôts et cotisations (46,0 - 41,3)", "vague1 §2 règle 5 ; A18 B3-23",
 "2025 : 5,4 pts en recettes totales ; « les recettes totales incluent des ressources autres que les prélèvements »", "audit l.51",
 "0 sur le concept commun", "périmètre : Codex ne calcule ni l'écart hors France ni l'écart en impôts et cotisations", "accord (Codex partiel)", ""],
["05", "Solde primaire 2025", "-2,87 % (Insee) ; -2,9 % (Eurostat) ; aucun excédent primaire 2002-2025 ; 9 excédents primaires depuis 1975", "A18 B5-44 ; A18_verification_25 V10, V16",
 "-85,871 Md€ = -2,87 % (D41 versés) ; variantes -86,940 (D41G) et -89,344 (intérêts nets) ; 9, 11 ou 7 années d'excédent primaire selon la convention", "02_comptabilite_reconciliee ; calculs\\frequences.csv",
 "0", "aucune ; Codex ajoute deux conventions (D41G, intérêts nets)", "accord", "Les 9 années citées par la cellule (V16) sont exactement celles de Codex (1979, 1980, 1987, 1989, 1990, 1998-2001)"],
["06", "Part structurelle du déficit 2025", "« surtout structurel » : au moins 92 % dans les estimations officielles lues (-4,7 Commission à -5,2 Gouvernement) ; alternative OFCE environ 84 % (correction O2)", "corrections_demandees O2 (fait foi) ; vague1 §3.6 (formulation restreinte depuis)",
 "Solde structurel 2025 -5,2 % du PIB potentiel (cadre du projet, conjoncturel +0,1) ou -4,9 % (potentiel de la LPFP, conjoncturel -0,1), HCFP avis 2026-5 tableau 14 et annexe 3 ; Codex ne calcule pas de part", "codex\\agents\\A17.md (Codex)",
 "Codex -4,9 / -5,2 inclus dans la fourchette de la cellule -4,7 / -5,2", "source : Codex a lu l'avis du HCFP (hcfp.fr, injoignable pour la cellule) ; la cellule a en plus l'OFCE", "accord sur l'ordre de grandeur",
 "Part implicite chez Codex : 4,9/5,07 = 97 % à 5,2/5,07 > 100 %. Codex n'examine pas d'estimation non officielle (OFCE) : la borne basse de 84 % est propre à la cellule"],
["07", "Effort pour revenir à 3 % (statique)", "environ 62 Md€ (5,1 -> 3 % au PIB 2025) ; effort à voter contre la trajectoire sans mesures : environ 5,4 pts de PIB pour 3 % en 2030", "vague1 §3.7 (A01) ; recette_A15 §4",
 "non calculé en statique ; simulations : ratio stable en 2030 = 3,08 pts de PIB tendanciel d'effort cumulé ; solde nul en 2030 = 7,49 pts ; portefeuille chiffré 0,43 pt", "rapport_integral §6 ; copie de scenarios.py et calculs\\scenarios.csv (lus par C01)",
 "non comparable", "objet ET référence différents : Codex vise la stabilisation ou l'équilibre et part d'un témoin ancré sur la prévision de la Commission (-5,4 % en 2027, mesures du budget 2027 comprises) ; la cellule vise 3 % contre une trajectoire sans aucune mesure (6,5 % en 2027)", "point traité par une seule équipe (3 %)", "Ne pas juxtaposer 5,4 pts (cellule, 3 % en 2030) et 3,08 pts (Codex, stabilisation en 2030) : voir ligne 13"],
["08", "Effort pour stabiliser la dette", "67 à 87 Md€ (d = 115,7 %, g = 2,5 à 1,9 %, sans ajustement stock-flux) ; 50,8 Md€ à g = 3 % (Astra : 52)", "vague1 §3.7 ; A01 C-A01-009 ; corrections O7",
 "91,13 Md€ (rétrospectif : ratio de fin 2024 112,63 %, croissance nominale observée 2025 1,90 %, stock-flux observé 2,41 Md€) ; environ 52 Md€ à 3 % (reproduction d'Astra)", "rapport_integral §6 ; codex\\agents\\A17.md",
 "4 à 24 Md€ selon g", "méthode et date : Codex calcule l'effort qui aurait stabilisé le ratio EN 2025 (point de départ fin 2024, stock-flux compris) ; la cellule l'effort POUR l'année suivante (départ fin 2025, sans stock-flux). Recalcul C01 sur les données de Codex : convention de la cellule -> 87,1 / 77,1 / 67,2 / 50,8 Md€ (identique) ; convention Codex sans stock-flux -> 88,7", "accord sur les méthodes une fois la convention fixée", ""],
["09", "Charge d'intérêts", "2025 : 2,20 % du PIB (65,7 Md€, D41 S13) ; maximum 1996 3,61 % ; 2026 prévu 79,2 Md€ (S13) ; État 2027 : 72,4 Md€ en crédits, 74,9 en comptabilité nationale", "A18_verification_25 V14 ; A18 B1-11 ; vague1 §3.8",
 "2025 : 65,7209 Md€ = 2,20 des 5,07 pts de déficit ; 1993 : 3,22 % ; 2026 prévu 79,2 Md€ (Sénat) ; programme 117 en 2027 : 72,37 Md€", "rapport_integral §3 ; audit l.11 et l.133",
 "0", "aucune ; la cellule distingue en plus crédits et comptabilité nationale pour 2027", "accord", ""],
["10", "Décomposition de la hausse de la dette", "1979-2025 : +94 pts = 60 déficits primaires + 8 écart taux-croissance + 26 ajustements (20 avant 1999) ; 2001-2025 : +56 = 54 primaires, -3,7 taux-croissance, +5,4 résidu", "vague1 §3.8 et §3.6 ; A18_verification_25 V11-V12",
 "Fenêtres propres seulement (1998-2001, 2007-2009, 2015-2019, 2019-2020, 2020-2023, 2023-2025), bornes = fins d'année. Recalcul C01 avec l'identité de Codex sur ses données, flux 1979 à 2025 (bornes fin 1978 - fin 2025) : +94,1 = 60,22 primaires + 8,06 (intérêts 115,38 - PIB nominal 107,32) + 25,82 stock-flux ; flux 2001-2025 : +55,96 = 54,27 - 3,71 + 5,40", "02_comptabilite_reconciliee ; calculs\\decomposition_dette.csv ; c01_03_recalcul_codex.py",
 "0 (à la deuxième décimale)", "aucune : la cellule nomme ses fenêtres par années de flux, Codex par bornes de fin d'année ; un premier recalcul de C01 bornes 1979-2025 donnait 60,9 / 9,6 / 23,6 en omettant les flux de 1979 (stock-flux 1979 = 8,68 Md€ = 2,2 pts)", "accord exact",
 "Le résidu « inexpliqué » de 20-26 pts avant 1999 reste chez les deux équipes ; Codex ne l'explique pas non plus. Même convention à surveiller pour « 2015-2019 » (vague1 §3.8 : flux 2015-2019 = bornes fin 2014 - fin 2019)"],
["11", "Hausse des dépenses et des recettes 1974-2025", "+16 / +11 pts (15,97 / 10,80) ; 12,8 des 16 pts acquis en 1985", "A18_verification_25 V04",
 "+15,97 / +10,80 ; dépenses : prestations et transferts 13,01, fonctionnement 1,94, intérêts 1,61, actifs non financiers -0,59", "audit l.41-43 ; rapport_integral §3 ; calculs\\ponts_points_pib.csv",
 "0", "aucune", "accord", "Codex apporte une ventilation par nature que la cellule ne transmet pas sous cette forme"],
["12", "Part de la protection sociale et de la santé dans l'écart de dépenses (2024)", "64,7 % hors France ; vieillesse 2,50 (avec la France) / 3,10 (hors France)", "A18_verification_25 V07-V08",
 "64,7 % hors France (4,42 + 1,80 sur 9,61) ; vieillesse 3,10 hors France, 2,50 avec EA20", "02_comptabilite_reconciliee ; calculs\\fonctions_2024.csv",
 "0", "aucune", "accord", "Concordance exacte obtenue indépendamment"],
["13", "Trajectoire de référence (sans effort additionnel)", "déficit 7,3 % en 2030, dette 154 % en 2035 (aucune mesure votée, même celles du budget 2027 ; taux d'émission 4 %) ; corrections O5 : fourchettes pour R-A15-04", "recette_A15 §3-4 ; corrections_demandees O1, O5",
 "déficit 6,32 % en 2030, 7,75 % en 2035 ; dette 128,1 % en 2030, 143,1 % en 2035 (témoin central)", "copie de scenarios.py (PRIMARY_2027 = -2,4 = -5,4 + 3,0, Commission du 17/11/2026 ; dette 2026 119,2 ; coupon convergeant vers 4 % au rythme de 1/8,5 ; dérive primaire de 0,08 pt/an) et calculs\\scenarios.csv",
 "environ 1 pt de déficit en 2030 et 11 pts de dette en 2035", "référence : Codex ancre son témoin sur la prévision de la Commission, qui inclut les mesures du budget 2027 ; la cellule (A15) n'inclut aucune mesure. Les deux sont des repères conditionnels, non des prévisions", "divergence de périmètre (référence)",
 "Tout effort exprimé « contre la référence » diffère d'autant entre les deux équipes"],
]
with open(O, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(H); w.writerows(R)
print(len(R), "lignes écrites")
