"""S13 — Effet d'une consolidation de 1 point de PIB sur le ratio de dette, selon le profil de perte d'activité.

C-S13-002 : formule de première année d'Eyraud et Weber (FMI WP/13/67, p. 7) :
    variation du ratio (points) ~ -1 + m*d + m*r
    m = multiplicateur de première année, d = dette/PIB, r = recettes/PIB.
C-S13-003 : extension simple sur 5 ans (approximation du premier ordre, relative à la référence) :
    ratio_t - ratio_ref_t ~ -sum_{s<=t}(1 - r*y_s) - i*sum(dette économisée) + d*y_t
    y_t = perte de PIB en % (niveau) l'année t pour une consolidation permanente de 1 point.
    Hypothèses S13 : effet d'actualisation et croissance de référence ignorés, i = taux apparent.
Données : d = 115,7 % et r = 52,24 % du PIB en 2025 (Insee base 2020, base commune
`donnees/commun/base_insee_dep_rec_pctPIB.csv`, extraction 20/11/2026).
Usage : python -I s13_dette_multiplicateur.py
"""
D = 1.157
R = 0.5224

PROFILS = {
    # perte de niveau de PIB (fraction) années 1..5 pour 1 point de consolidation permanent
    "estompement_0.6_hypothetique": [0.6, 0.3, 0.1, 0.0, 0.0],   # profil type A15 (hypothèse, non sourcé)
    "AFG2019_depense_approx": [0.25, 0.0, 0.0, 0.0, 0.0],        # « environ 1/4 de point, moins de deux ans » (JEP p.142), profil approché
    # Jordà-Taylor : réponses à un ÉPISODE (traitement 0,97 pt en an 1, qui prédit 0,51 / 0,28 / 0,17
    # de traitement ensuite : tableau A4 p. 45, note 12 p. 34). C-S13-004 : division par l'effort
    # cumulé attendu 0,97 x (1 ; 1,51 ; 1,79 ; 1,96 ; 1,96) pour approcher la perte PAR POINT d'effort
    # maintenu. Approximation S13 (linéarité, coefficient t+3 absent du tableau A4 : 0,17 porté à t+3).
    "JordaTaylor_AIPW_moyen_par_point": None,
    "JordaTaylor_AIPW_expansion_par_point": None,
    "multiplicateur_1.3_persistant": [1.3, 1.3, 1.3, 1.3, 1.3],   # haut de fourchette de crise (S07), persistant : cas extrême
}


JT_MOYEN = [0.24, 0.70, 0.75, 0.93, 1.23]      # tableau 8, p. 29 (PDF)
JT_EXPANSION = [0.33, 0.68, 0.36, 0.55, 0.56]  # tableau 9, p. 30 (PDF), non significatif au-delà de l'an 2
EFFORT_CUMULE = [0.97 * c for c in (1.0, 1.51, 1.79, 1.96, 1.96)]
PROFILS["JordaTaylor_AIPW_moyen_par_point"] = [round(a / e, 3) for a, e in zip(JT_MOYEN, EFFORT_CUMULE)]
PROFILS["JordaTaylor_AIPW_expansion_par_point"] = [round(a / e, 3) for a, e in zip(JT_EXPANSION, EFFORT_CUMULE)]


def premiere_annee(m, d=D, r=R):
    return -1 + m * d + m * r


def trajectoire(y, i=0.0, d=D, r=R):
    cumul, res = 0.0, []
    for t, yt in enumerate(y):
        cumul += (1 - r * yt) + i * cumul
        res.append(-cumul + d * yt)
    return res


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print("C-S13-002 première année (Eyraud-Weber), d=%.3f r=%.4f" % (D, R))
    for m in (0.3, 0.5, 0.6, 0.8, 1.0, 1.3):
        print("  m=%.1f : variation du ratio = %+.2f point" % (m, 100 * premiere_annee(m) / 100))
    print("  seuil de m au-delà duquel le ratio monte la 1re année : %.3f" % (1 / (D + R)))
    print("C-S13-004 profils Jordà-Taylor par point d'effort (perte de PIB, fraction) :")
    for k in ("JordaTaylor_AIPW_moyen_par_point", "JordaTaylor_AIPW_expansion_par_point"):
        print("  %-38s %s" % (k, PROFILS[k]))
    print("C-S13-003 trajectoires sur 5 ans (points de PIB, écart à la référence)")
    for i in (0.0, 0.03):
        print(" taux apparent i=%.0f %%" % (100 * i))
        for nom, y in PROFILS.items():
            tr = trajectoire(y, i)
            print("  %-32s " % nom + " ".join("%+.2f" % v for v in tr))
