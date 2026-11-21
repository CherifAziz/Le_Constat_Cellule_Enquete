# A06 - Extraction AMECO (vintage automne 2026, fichiers datés 16/11/2026, téléchargés le 20/11/2026)
# Source: https://ec.europa.eu/economy_finance/db_indicators/ameco/documents/ameco0.zip
# Usage: python -I 01_extract_ameco.py <dossier_ameco> <csv_sortie>
import sys, glob, os, csv

src, out = sys.argv[1], sys.argv[2]
COUNTRIES = ['FRA', 'DEU', 'NLD', 'SWE', 'ITA', 'ESP', 'GBR', 'EA20', 'DNK', 'BEL', 'USA']
CODES = {
    '1.1.0.0.OVGD': 'pib_volume_2020',
    '1.0.0.0.OVGDP': 'pib_potentiel_2020',
    '1.0.0.0.AVGDGP': 'ecart_production_pct_pot',
    '1.0.0.0.NPTD': 'population_cn_milliers',
    '1.0.0.0.NPAN': 'pop_15_64_milliers',
    '1.0.0.0.NPON': 'pop_65plus_milliers',
    '1.0.0.0.NETD': 'emploi_interieur_milliers',
    '1.0.0.0.NLHA': 'heures_par_emploi',
    '1.0.0.0.NLHT': 'heures_totales_millions',
    '1.0.0.0.ZUTN': 'taux_chomage',
    '1.0.0.0.NLTN': 'population_active_milliers',
    '1.0.0.0.UVGD': 'pib_courant_monnaie_nat',
    '1.0.212.0.UVGD': 'pib_courant_SPA_mrd',
    '1.1.0.0.UVG2': 'va_industrie_hors_constr_courant',
    '1.0.0.0.UVGM': 'va_manufacturier_courant',
    '1.0.0.0.UIGT': 'fbcf_totale_courant',
    '1.0.319.0.UIGG0': 'fbcf_apu_pct_pib',
    '1.0.319.0.UBLGAPS': 'solde_structurel_pct_pibpot',
    '1.0.319.0.UBLGCP': 'composante_conj_solde_pct_pibpot',
    '1.0.0.0.NETM': 'emploi_manufacturier_milliers',
    '1.0.319.0.UBLG': 'solde_apu_pct_pib',
    '1.0.319.0.UBLGAP': 'solde_cvs_cycle_pct_pibpot',
    '1.0.319.0.UBLGBP': 'solde_primaire_cvs_cycle_pct_pibpot',
    '3.1.0.0.PVGD': 'deflateur_pib_2020',
    '1.0.0.0.HWCDW': 'remuneration_par_salarie_milliers',
    '1.0.0.0.NWTD': 'salaries_interieur_milliers',
}
rows = []
hdr = None
for f in sorted(glob.glob(os.path.join(src, 'AMECO*.TXT'))):
    with open(f, encoding='latin-1') as fh:
        h = fh.readline().strip().split(';')
        years = [x for x in h[5:] if x.strip()]
        for line in fh:
            p = line.rstrip('\n').split(';')
            ctry, _, code = p[0].partition('.')
            if ctry in COUNTRIES and code in CODES:
                for y, v in zip(years, p[5:]):
                    v = v.strip()
                    if v and v not in ('NA',):
                        try:
                            rows.append([ctry, CODES[code], code, int(y), float(v)])
                        except ValueError:
                            pass
with open(out, 'w', newline='', encoding='utf-8') as fo:
    w = csv.writer(fo, delimiter=';')
    w.writerow(['pays', 'variable', 'code_ameco', 'annee', 'valeur'])
    w.writerows(rows)
print(len(rows), 'lignes écrites')
