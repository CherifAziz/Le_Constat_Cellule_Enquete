"""Joint les observations comptables et les archives de chaque exercice."""
import csv
import re
from pathlib import Path

root=Path(__file__).resolve().parent
reperes=(root/"preuves_histoire/reperes_annuels.md").read_text(encoding="utf-8")
records={}
for line in reperes.splitlines():
    m=re.match(r"\| (\d{4}) \| (.*?) \| (.*?) \|$",line)
    if m:
        records[int(m[1])]=(m[2],m[3])
assert sorted(records)==list(range(1974,2027))
refs="\n".join(line for line in reperes.splitlines() if re.match(r"^\[[^]]+\]:",line))
rows=list(csv.DictReader((root/"calculs/annuel.csv").open(encoding="utf-8-sig"),delimiter=";"))
parts=["# Chronologie annuelle des finances publiques françaises",
       "1974 sert de point de comparaison. Les 51 exercices suivants sont clos. Chaque fiche rapproche un compte réalisé et une pièce datée. L’écart de production et la contribution causale de chaque mesure demandent une estimation distincte.",
       "Montants en milliards d’euros courants, ratios en % du PIB. L’intérêt retenu est D41 versé consolidé. La croissance indiquée est celle du PIB en volume. Le fichier de données comporte aussi la croissance nominale, le déflateur du PIB, l’épargne, les soldes sectoriels et, dès 1978, l’emploi en équivalent temps plein. Le détail État et ODAC avant 1978 est inconciliable dans la table 3.106. Les millésimes et les conventions sont décrits dans la [réconciliation](02_comptabilite_reconciliee.md). [Données annuelles](calculs/annuel.csv) · [Insee, comptes nationaux](https://www.insee.fr/fr/statistiques/8988934)"]


def fr(row,k,n=1):
    if row[k]=="":
        return "n.d."
    return f"{float(row[k]):,.{n}f}".replace(","," ").replace(".",",").replace("-","−")


# Situation au 31 décembre, y compris les années d'alternance.
matignon={1974:"Jacques Chirac",1976:"Raymond Barre",1981:"Pierre Mauroy",1984:"Laurent Fabius",
          1986:"Jacques Chirac",1988:"Michel Rocard",1991:"Édith Cresson",1992:"Pierre Bérégovoy",
          1993:"Édouard Balladur",1995:"Alain Juppé",1997:"Lionel Jospin",2002:"Jean-Pierre Raffarin",
          2005:"Dominique de Villepin",2007:"François Fillon",2012:"Jean-Marc Ayrault",
          2014:"Manuel Valls",2016:"Bernard Cazeneuve",2017:"Édouard Philippe",2020:"Jean Castex",
          2022:"Élisabeth Borne",2024:"François Bayrou",2025:"Sébastien Lecornu"}
assemblee={1974:"majorité de droite et du centre",1981:"majorité de gauche",
           1986:"majorité de droite et du centre, première cohabitation",
           1988:"groupe socialiste en majorité relative",1993:"majorité de droite, deuxième cohabitation",
           1995:"majorité de droite",1997:"majorité de gauche plurielle, troisième cohabitation",
           2002:"majorité de droite",2012:"majorité de gauche",
           2017:"majorité présidentielle",2022:"coalition présidentielle en majorité relative",
           2024:"Assemblée sans majorité absolue de bloc"}
def en_fin_annee(series,year):
    return series[max(t for t in series if t<=year)]


parts.append("Le repère politique désigne la personne à Matignon et la configuration de l’Assemblée **au 31 décembre**. Ce choix ne lui impute pas les comptes votés ou engagés par ses prédécesseurs. [Gouvernement, chefs du gouvernement](https://www.info.gouv.fr/les-anciens-premiers-et-premieres-ministres-de-la-ve-republique) · [Assemblée, calendriers et cohabitations](https://www.assemblee-nationale.fr/elections/dates.asp) · [Composition des législatures](https://www.assemblee-nationale.fr/histoire/leg5repnew.asp) · [Effectifs des groupes](https://www2.assemblee-nationale.fr/instances/liste/groupes_politiques/effectif)")


for row in rows:
    year=int(row["annee"])
    record,mechanism=records[year]
    summary=f"PIB **{fr(row,'pib_edp')}** Md€, croissance réelle **{fr(row,'g_reel_pct')} %**. Recettes {fr(row,'rec')} Md€ ({fr(row,'rec_pct')} % du PIB), dépenses {fr(row,'dep')} Md€ ({fr(row,'dep_pct')} %). Solde **{fr(row,'b9_edp')} Md€**, soit **{fr(row,'b9_pct')} %**. Solde primaire {fr(row,'primaire_pct')} %, intérêts {fr(row,'interets_pct')} %."
    debt=f"Dette de Maastricht {fr(row,'dette_pct')} % du PIB." if row["dette_pct"] else "Dette de Maastricht indisponible dans la série retenue avant 1978."
    labour=(f" Taux d’emploi des 15–64 ans {fr(row,'emploi_15_64_pct')} %, chômage BIT en proportion des actifs {fr(row,'chomage_BIT_pct')} %." if year>=1975 else "")
    politics=f"Au 31 décembre, {en_fin_annee(matignon,year)} dirige le gouvernement. Assemblée nationale : {en_fin_annee(assemblee,year)}."
    parts += [f"## {year}",summary+" "+debt+labour,politics,record+" "+mechanism]
parts += ["## 2026 · Exercice en cours",records[2026][0]+" "+records[2026][1],
          "La Commission européenne projette le 17 novembre un déficit de 5,5 % du PIB, une dette de 119,2 % et une croissance réelle de 0,4 % en 2026. Les 5,4 % de déficit et 122,1 % de dette prévus pour 2027 sont des prévisions séparées. [Commission, prévisions d’automne, tableau France](https://economy-finance.ec.europa.eu/economic-surveillance-eu-member-states/country-pages-including-country-reports/france/economic-forecast-france_en)",refs]
(root/"01_chronologie_1974_2026.md").write_text("\n\n".join(parts)+"\n",encoding="utf-8")
