# A18 - calculs arithmétiques simples sur valeurs relevées dans les pièces (chaque entrée cite sa pièce)
import sys
sys.stdout.reconfigure(encoding="utf-8")
C = []
def c(cle, formule, val, piece):
    C.append((cle, formule, val, piece)); print(f"{cle} ; {formule} = {val} ; {piece}")
deficit25, dep25 = 151.592, 1714.1117      # Insee t_3201 base 2020 (comptes 2025 publiés mai 2026)
c("C-A18-001 part du déficit dans la dépense 2025", "151,592 / 1714,112", round(100 * deficit25 / dep25, 2), "Insee t_3201")
c("C-A18-002 déficit par jour 2025 (M€)", "151,592e3 / 365", round(deficit25 * 1000 / 365, 0), "Insee t_3201")
c("C-A18-002b déficit par jour 2025 avec IP2106 (M€)", "152,5e3 / 365", round(152.5 * 1000 / 365, 0), "Insee IP2106 fig. 3")
int26, pop26 = 79.2e9, 69.1e6               # HCFP avis 2026-5 §115 ; Insee Première 2087
c("C-A18-003 intérêts APU 2026 par habitant (€)", "79,2 Md€ / 69,1 M", round(int26 / pop26, 0), "HCFP 2026-5 p.38 ; Insee IP2087 p.1")
int25 = 65.7209e9
c("C-A18-003b intérêts APU 2025 (réalisé) par habitant (€)", "65,72 Md€ / 68,9 M (pop. 1/1/2025 = 69,1/1,0025)", round(int25 / (69.1e6 / 1.0025), 0), "Insee t_3201 ; IP2087")
for y, d in [(2007, 65.5), (2012, 91.7), (2019, 98.2), (2020, 114.9), (2025, 115.7)]:
    c(f"C-A18-004 dette {y} en mois de PIB", f"{d} x 12 / 100", round(d * 12 / 100, 2), "Insee série longue dette brute")
for y, d in [(2012, 79.8), (2013, 77.4), (2014, 74.4), (2019, 58.3)]:
    c(f"C-A18-005 dette Allemagne {y} en mois de PIB", f"{d} x 12 / 100", round(d * 12 / 100, 2), "Eurostat gov_10dd_edpt1")
c("C-A18-006 écart OAT-Bund mai 2024 / oct. 2026 (moyennes mensuelles)", "(4,89-3,416)/(3,03-2,518)", round((4.89 - 3.416) / (3.03 - 2.518), 2), "BCE IRS mensuel")
c("C-A18-007 voix manquantes motion 20/03/2023", "287 - 278", 287 - 278, "CR AN 20/03/2023")
c("C-A18-008 voix manquantes motion LFI 16/10/2025", "289 - 271 (majorité 577 sièges ; non lue dans le CR)", 289 - 271, "scrutin 3058")
c("C-A18-009 jours entre note du 7/12/2023 et promulgation LPFP 18/12/2023", "18 - 7", 11, "Sénat r24-153 p.5-6")
c("C-A18-010 mois entre censure Barnier 4/12/2024 et confiance Bayrou 8/9/2025", "sept. 2025 - déc. 2024", 9, "scrutins 519 et 3054")
c("C-A18-011 rapport intérêts / déficit 1993", "36,59 / 72,62", round(36.59 / 72.62, 3), "Insee t_3201")
c("C-A18-012 Suède/France déficit (OCDE 1993 / Insee 2025)", "10,70 / 5,1", round(10.70 / 5.1, 2), "OCDE EO ; Insee")
c("C-A18-012b Suède/France déficit (12 % cité / 5,1)", "12 / 5,1", round(12 / 5.1, 2), "V5 ; Insee")
c("C-A18-013 surplus de 2000 en Md€", "51,4 MdF / 6,55957", round(51.4 / 6.55957, 2), "Sénat rapport LFR 2000")
c("C-A18-014 charge de la dette État PLF 2027 - mission Défense PLF 2027 (Md€)", "72,93 - 63,4", round(72.93 - 63.4, 2), "DP Budget 2027 p.57 et p.88")
c("C-A18-015 coût d'un dixième de point (Md€) selon le DP 2027, années N / N+1 / N+2", "3/8/12 x 0,1", "0,3 / 0,8 / 1,2", "DP Budget 2027 p.27")
c("C-A18-016 dixième de point appliqué à toute la dette (Md€), État 2 822,7 / APU 3 460,5", "x 0,001", f"{2822.7 * 0.001:.2f} / {3460.5 * 0.001:.2f}", "Insee IP2106 fig. 5")
c("C-A18-017 prélèvements nécessaires pour combler le déficit 2025 (% PIB)", "46,0 + 5,1", 51.1, "Eurostat taxag ; Insee")
c("C-A18-018 dépense après comblement par la dépense (% PIB)", "57,3 - 5,1 vs ZE 49,8", 52.2, "Eurostat gov_10a_main")
