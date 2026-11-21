# -*- coding: utf-8 -*-
"""A15 - validation du module de dette sur 2015-2025 (rejeu).
Entrees observees : solde primaire, PIB nominal, inflation (IPC OCDE), taux a 10 ans et a
3 mois (table A07 construite sur donnees\\commun, Eurostat et OCDE). Le modele calcule la
charge d'interets et la dette ; on compare a l'observe.
Deux variantes : (a) ajustements stocks-flux observes ; (b) ajustements stocks-flux nuls,
comme dans les projections."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a15_modele import lire_table_france, Interets, SORTIE


def rejouer(tab, interets, w10=0.75, sfa_obs=True, debut=2015, fin=2025, ecart=0.0, plancher=True):
    a0 = tab[debut - 1]
    D_prev = a0["dette_mdeur"]
    a_prev = a0["taux_apparent_pct"]
    lignes = []
    for t in range(debut, fin + 1):
        r = tab[t]
        rm = w10 * r["taux10_FR"] + (1 - w10) * r["taux3m_FR"]
        if plancher:
            rm = max(0.0, rm)
        rm += ecart
        pi = r["ipc_ocde_pct"]
        pb = r["solde_primaire_mdeur"]
        I_obs = r["interets_verses_mdeur"]
        D_obs = r["dette_mdeur"]
        sfa = (D_obs - tab[t - 1]["dette_mdeur"]) - (I_obs - pb) if sfa_obs else 0.0
        I, N, a_new = interets.charge(D_prev, a_prev, rm, pi, pb, sfa)
        D = D_prev + N
        Y = r["pib_mdeur"]
        lignes.append(dict(annee=t, rm=rm, I_mod=I, I_obs=I_obs, err_I=I - I_obs,
                           i_mod_pct=I / Y * 100, i_obs_pct=I_obs / Y * 100,
                           D_mod=D, D_obs=D_obs, d_mod=D / Y * 100, d_obs=D_obs / Y * 100,
                           err_d=(D - D_obs) / Y * 100, sfa=sfa))
        D_prev, a_prev = D, a_new
    return lignes


def stats(L, a0, a1):
    e = [x["err_I"] for x in L if a0 <= x["annee"] <= a1]
    return (sum(v * v for v in e) / len(e)) ** 0.5, sum(e) / len(e)


def main():
    tab = lire_table_france()
    os.makedirs(SORTIE, exist_ok=True)
    resume = []
    for f in (0.10, 0.125, 0.15):
        for w in (0.6, 0.75, 0.9):
            for ec in (0.0, 0.5, 1.0, 1.5):
                L = rejouer(tab, Interets(f=f), w10=w, sfa_obs=True, ecart=ec)
                r_cal, b_cal = stats(L, 2015, 2019)
                r_val, b_val = stats(L, 2020, 2025)
                resume.append(dict(f=f, w10=w, ecart_pts=ec, rmse_I_2015_2019=round(r_cal, 2),
                                   biais_I_2015_2019=round(b_cal, 2), rmse_I_2020_2025=round(r_val, 2),
                                   biais_I_2020_2025=round(b_val, 2), err_ratio_2025=round(L[-1]["err_d"], 2)))
    with open(os.path.join(SORTIE, "A15_validation_grille.csv"), "w", newline="", encoding="utf-8") as h:
        w = csv.DictWriter(h, fieldnames=list(resume[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(resume)
    best = min(resume, key=lambda r: r["rmse_I_2015_2019"])
    print("calibrage 2015-2019 (meilleur) :", best)
    # variante retenue : meilleur calage sur 2015-2019 seulement ; 2020-2025 sert de test hors echantillon
    sel = best
    print("retenu :", sel)
    for sfa_obs, nom in ((True, "sfa_observes"), (False, "sfa_nuls")):
        L = rejouer(tab, Interets(f=sel["f"]), w10=sel["w10"], sfa_obs=sfa_obs, ecart=sel["ecart_pts"])
        with open(os.path.join(SORTIE, f"A15_validation_2015_2025_{nom}.csv"), "w", newline="", encoding="utf-8") as h:
            w = csv.DictWriter(h, fieldnames=list(L[0].keys()), delimiter=";")
            w.writeheader()
            for x in L:
                w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in x.items()})
        print("==", nom)
        for x in L:
            print(f"{x['annee']}  I mod {x['I_mod']:6.1f} obs {x['I_obs']:6.1f} ({x['i_mod_pct']:.2f}/{x['i_obs_pct']:.2f} %PIB)  "
                  f"dette mod {x['d_mod']:6.1f} obs {x['d_obs']:6.1f}  err {x['err_d']:+.2f}")
    return sel


if __name__ == "__main__":
    main()
