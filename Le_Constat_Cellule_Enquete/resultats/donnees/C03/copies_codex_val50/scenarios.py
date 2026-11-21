"""Trajectoires conditionnelles, en unités de PIB 2026 = 100. Python standard."""
import csv
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / "calculs"
OUTPUT.mkdir(exist_ok=True)
DEBT_2026 = 119.2      # Commission, 17-11-2026, prévision, France
PRIMARY_2027 = -2.0   # C03 : variante    # solde prévu -5,4 + intérêts prévus 3,0
CASES = {
    # variations par rapport aux hypothèses centrales, par dimension
    "central":{}, "activité basse":{"growth_shift":-.007}, "activité haute":{"growth_shift":.007},
    "déflateur bas":{"inflation":.01}, "déflateur haut":{"inflation":.03},
    "taux +100 pb":{"rate_shift":.01}, "taux +200 pb":{"rate_shift":.02},
    "multiplicateur faible":{"mult":.3}, "multiplicateur élevé":{"mult":1.3},
    "vieillissement fort":{"aging":.16}, "retard de deux ans":{"start":2029},
    "emploi bas, productivité donnée":{"growth_shift":-.004}, "emploi haut, productivité donnée":{"growth_shift":.004},
    "stress combiné":{"growth_shift":-.007,"inflation":.01,"mult":1.3,"rate_shift":.02,"aging":.16},
}


def run(effort, *, growth_shift=0, inflation=.02, rate_shift=0, mult=.8, aging=.08, start=2027, profile=None):
    """Effort ex ante cumulé en points de PIB tendanciel, quatre tranches."""
    base_gdp = gdp = 100.
    debt = DEBT_2026
    gap = previous_effort = 0.
    # Convention centrale : 3 unités d'intérêts par 100 de PIB 2027 avant nouvelles mesures.
    coupon = 3*(1.006*1.02)/DEBT_2026
    refi_share = 1/8.5
    lagged_rates = 0.
    rows = []
    for year in range(2027,2051):
        share = min(1,max(0,(year-start+1)/4))
        new_effort = effort*share if profile is None else profile(year)
        real_growth = (.006 if year==2027 else .012)+growth_shift
        base_gdp *= (1+real_growth)*(1+inflation)
        gap = .5*gap - mult*(new_effort-previous_effort)/100
        previous_effort = new_effort
        previous_gdp, previous_debt = gdp,debt
        gdp = base_gdp*(1+gap)
        if year>2027:
            coupon += refi_share*(.04-coupon)
        lagged_rates += refi_share*(rate_shift-lagged_rates)
        interest = (coupon+lagged_rates)*previous_debt
        baseline_p = PRIMARY_2027 - aging*(year-2027)
        primary = base_gdp*(baseline_p+new_effort)/100 + .50*(gdp-base_gdp)
        balance = primary-interest
        debt -= balance     # Ajustement stock-flux posé nul en projection.
        debt_ratio = 100*debt/gdp
        change_ratio = debt_ratio-100*previous_debt/previous_gdp
        assert abs((debt-previous_debt)+balance)<1e-9
        rows.append(dict(annee=year,effort_brut_pts=new_effort,pib_indice=gdp,
            perte_niveau_pib_pct=100*gap,croissance_nominale_pct=100*(gdp/previous_gdp-1),
            interets_pts=100*interest/gdp,primaire_pts=100*primary/gdp,
            solde_pts=100*balance/gdp,dette_pts=debt_ratio,variation_dette_pts=change_ratio))
    return rows


def calibrate(test):
    low,high=0.,12.
    assert test(run(low)[3])<0<test(run(high)[3])
    for _ in range(55):
        mid=(low+high)/2
        if test(run(mid)[3])>0:
            high=mid
        else:
            low=mid
    return (low+high)/2


plans = {"référence":0.,
         "ratio stable en 2030": calibrate(lambda r:-r["variation_dette_pts"]),
         "ratio en baisse de 1 pt en 2030":calibrate(lambda r:-1-r["variation_dette_pts"]),
         "solde nul en 2030":calibrate(lambda r:r["solde_pts"])}
path = []
for plan,effort in plans.items():
    for case,settings in CASES.items():
        for row in run(effort,**settings):
            path.append({"objectif":plan,"hypothese":case,**row})
def combined(year, overlap=.5, additional_tax_share=1.):
    # Équivalence de taille à l'échelle 2025 : hypothèse de taux d'effort / PIB constant.
    fraction=(.5,.75,.9,1.)[min(year-2027,3)]
    tax = (7.5+8.95*.95-2.-1.)*fraction-.4
    hospital = .455*(1-overlap)*min(1,(year-2026)/4)
    return (additional_tax_share*tax+hospital)/29.910559


for name,overlap,tax_share in [("central si recettes nouvelles",.5,1.),
        ("hôpital déjà prévu",1.,1.),("demi-additionnalité fiscale",.5,.5),("sans recoupement",0.,1.)]:
    for row in run(0,profile=lambda year:combined(year,overlap,tax_share)):
        path.append({"objectif":"portefeuille TVA-CSG et hôpital","hypothese":name,**row})
with (OUTPUT/"scenarios.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=path[0],delimiter=";")
    w.writeheader()
    for row in path:
        w.writerow({k:round(v,6) if isinstance(v,float) else v for k,v in row.items()})
for plan,effort in plans.items():
    print(plan,round(effort,3),[(r["annee"], round(r["solde_pts"],2),round(r["dette_pts"],2)) for r in run(effort) if r["annee"] in (2027,2030,2035,2050)])

# Épreuve demandée par les contradicteurs : même effort, même calendrier.
matched=[]
for lever in ("aval hospitalier","TVA avec compensation"):
    for multiplier in (.3,.8,1.3):
        # Md€ à l'échelle 2025. La recette TVA est nette des achats taxés des APU.
        direct=.455 if lever=="aval hospitalier" else .1*7.5-.295
        horizon=run(0,mult=multiplier,profile=lambda y:direct*min(1,(y-2026)/4)/29.910559)
        ref=run(0)
        for i,r in enumerate(horizon[:4]):
            matched.append(dict(levier=lever,multiplicateur=multiplier,annee=r["annee"],
                effort_direct_Md_base_2025=round(direct*(i+1)/4,6),
                variation_solde_vs_temoin_pts=round(r["solde_pts"]-ref[i]["solde_pts"],8),
                variation_dette_vs_temoin_pts=round(r["dette_pts"]-ref[i]["dette_pts"],8)))
with (OUTPUT/"effort_egal.csv").open("w",encoding="utf-8-sig",newline="") as f:
    w=csv.DictWriter(f,fieldnames=matched[0],delimiter=";")
    w.writeheader()
    w.writerows(matched)
