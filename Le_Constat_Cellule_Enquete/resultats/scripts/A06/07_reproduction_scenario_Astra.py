# A06 - Reproduction du scénario stylisé de capitalisation (contre-enquête Astra du 19/11/2026, §III.2, tableau « Scénarios de rédaction, fin 2026 »)
# Hypothèses reprises telles qu'énoncées par Astra (aucune donnée française observée) :
#  t = 1..27 (versements fin d'année 2000..2026) ; versement(t) = min(t/10,1)*0,50 pt PIB ; rente(t) = max(t-15,0)*0,02 pt PIB
#  croissance réelle 1,5 % ; coût réel de la dette 1 % ; rendement réel net du portefeuille 0 / 2 / 4 %
#  stock(t) = stock(t-1)*(1+r)/1,015 + versement(t) - rente(t) ; dette B : même récurrence au taux 1 %
# Variantes de sensibilité ajoutées par A06 (non présentes chez Astra) : croissance 1,0 %, coût de la dette 2 %, liquidation plus précoce.
import sys
def run(rp, rd=0.01, g=0.015, T=27, start_liq=15, slope=0.02, ramp=10, cap=0.50):
    S = D = 0.0
    for t in range(1, T + 1):
        v = min(t / ramp, 1) * cap
        a = max(t - start_liq, 0) * slope
        S = S * (1 + rp) / (1 + g) + v - a
        D = D * (1 + rd) / (1 + g) + v - a
    return S, D, v - a
out = []
for rp in (0.0, 0.02, 0.04):
    S, D, flux = run(rp)
    out.append(f'Astra base : rendement réel {rp:.0%} -> portefeuille {S:.1f} pts PIB ; dette de transition {D:.1f} pts ; besoin primaire année finale {flux:.2f} pt')
S30, D, _ = run(0.02)
out.append(f'Choc -30 % sur le portefeuille central à la liquidation : {S30*0.7:.1f} pts (Astra annonce 7,2)')
out.append('--- Sensibilités A06 ---')
for lab, kw in [('croissance réelle 1,0 %', dict(g=0.010)), ('coût réel dette 2 %', dict(rd=0.02)), ('coût réel dette 2 %, rendement 2 %, croissance 1 %', dict(rd=0.02, g=0.01)),
                ('liquidation dès t>10', dict(start_liq=10)), ('rendement réel 2 % net mais frais +0,5 pt', dict())]:
    rp = 0.015 if 'frais' in lab else 0.02
    S, D, flux = run(rp, **kw)
    out.append(f'{lab} : portefeuille {S:.1f} ; dette {D:.1f} ; besoin primaire final {flux:.2f}')
print('\n'.join(out))
open(sys.argv[1] if len(sys.argv) > 1 else 'resultats_07.txt', 'w', encoding='utf-8').write('\n'.join(out))
