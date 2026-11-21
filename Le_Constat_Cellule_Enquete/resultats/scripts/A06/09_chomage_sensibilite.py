# A06 - C-A06-007 : sensibilité statique du solde APU à 1 point de chômage (hypothèses H-A06-001 à 004, cf. script 05)
# Population active 2025 : AMECO NLTN ; PIB 2025 : Eurostat (base commune) ; PIB par emploi : script 05.
import sys
L, PIB, YE = 33675.0, 2991.056, 97.6e3
for lab, pr, tx, pe, di in [('basse', .5, .35, 3000, .3), ('centrale', .7, .42, 8000, .2), ('haute', .9, .5, 15000, .1)]:
    n = L * 1e3 * 0.01; dy = n * YE * pr / 1e9; rec = dy * tx; net = rec + n * pe / 1e9 - rec * di
    print(f'{lab} : {n/1e3:.0f} milliers de personnes ; PIB +{dy:.1f} Md€ ; solde +{net:.1f} Md€ = {100*net/PIB:.2f} pt PIB')
