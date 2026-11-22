# -*- coding: utf-8 -*-
"""D07 - Manifeste des pieces conservees (empreinte sha256)."""
import csv
import hashlib
import os

ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07', 'sources'))
OUT = os.path.normpath(os.path.join(ICI, '..', '..', 'donnees', 'D07'))
DATE = '2026-11-22'
E = 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/'
P = {
    'insee_EEC_T207_2025.xlsx': ('https://www.insee.fr/fr/statistiques/fichier/8977303/EEC_T207.xlsx', "Insee, series longues enquete Emploi, taux d'emploi par sexe et age quinquennal 1975-2025, corrige des ruptures"),
    'ilostat_emp_dwap_age_FR_DE_NL_SE.csv': ('https://rplumber.ilo.org/data/indicator/?id=EMP_DWAP_SEX_AGE_RT_A&ref_area=FRA+DEU+NLD+SWE&sex=SEX_T&classif1=AGE_5YRBANDS_Y55-59+AGE_5YRBANDS_Y60-64&type=label&format=.csv', "ILOSTAT, taux d'emploi 55-59 et 60-64 ans, France, Allemagne, Pays-Bas, Suede"),
    'eurostat_lfsa_ergan.json': (E + 'lfsa_ergan?sex=T&citizen=TOTAL&age=Y55-59&age=Y60-64&age=Y55-64&geo=FR&geo=DE&geo=NL&geo=SE&unit=PC', "Eurostat lfsa_ergan, taux d'emploi par age 1995-2025"),
    'eurostat_gov_10a_exp_GF1005.json': (E + 'gov_10a_exp?geo=FR&geo=DE&sector=S13&cofog99=GF1005&na_item=TE&unit=PC_GDP', 'Eurostat COFOG 10.5 chomage, S13, % du PIB'),
    'eurostat_une_ltu_a.json': (E + 'une_ltu_a?geo=FR&geo=DE&sex=T&age=Y15-74&unit=PC_UNE&indic_em=LTU', 'Eurostat, part du chomage de longue duree'),
    'ameco_1.0.0.0.ZNAWRU.html': ('https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZNAWRU&countries=FRA,DEU', 'AMECO, NAWRU France et Allemagne 1965-2027'),
    'ameco_1.0.0.0.ZUTN.html': ('https://ec.europa.eu/economy_finance/ameco/wq/series?fullVariable=1.0.0.0.ZUTN&countries=FRA,DEU', 'AMECO, taux de chomage 1965-2027'),
    'drees_cps_1959_2024.xlsx': ('https://data.drees.solidarites-sante.gouv.fr/api/v2/catalog/datasets/305_les-comptes-de-la-protection-sociale/attachments/la_protection_sociale_en_france_de_1959_a_2024xlsx', 'Drees, comptes de la protection sociale 1959-2024 (parution 23/10/2026)'),
    'fs_cice_rapport_2020.pdf': ('https://www.strategie-plan.gouv.fr/files/files/Publications/2020/CICE/fs-2020-rapport-cice2020-16septembre-final18h.pdf', 'France Strategie, Evaluation du CICE, sept. 2020'),
    'fs_cice_cp_synthese_2020.pdf': ('https://www.strategie.gouv.fr/files/files/Presse/CP%202020/2020-09-01_Evaluation%20du%20CICE%20%3B%20France%20Strat%C3%A9gie%20publie%20une%20synth%C3%A8se%20des%20travaux%20d%27approfondissement.pdf', 'France Strategie, communique de synthese CICE, 2020'),
    'bozio_wasmer_rapport_2024.pdf': ('https://www.vie-publique.fr/files/rapport/pdf/295596.pdf', "Bozio et Wasmer, Les politiques d'exonerations de cotisations sociales : une inflexion necessaire, oct. 2024 (obtenu par WebFetch)"),
    'insee_es348a1_crepon_desplatz_2001.pdf': ('https://www.insee.fr/fr/statistiques/fichier/1376044/es348a1.pdf', 'Crepon et Desplatz, Economie et statistique n° 348, 2001'),
    'an_r2436_rtt_2014.pdf': ('https://www.assemblee-nationale.fr/14/pdf/rap-enq/r2436.pdf', "Assemblee nationale, rapport n° 2436 de la commission d'enquete sur la reduction du temps de travail, dec. 2014"),
    'econpapers_chemin_wasmer_2009.html': ('https://econpapers.repec.org/RePEc:ucp:jlabec:v:27:y:2009:i:4:p:487-524', 'Chemin et Wasmer, JOLE 2009, notice et resume'),
    'insee_es477C_contrats_aides.pdf': ('https://insee.fr/fr/statistiques/fichier/1378063/ES477C.pdf', 'Benoteau et Remy, Le Panel 2008 de la Dares, Economie et statistique n° 477, 2015'),
    'insee_es477E_contrats_aides.pdf': ('https://www.insee.fr/fr/statistiques/fichier/1378067/ES477E.pdf', 'Benoteau, Quels effets du recrutement en contrat aide, Economie et statistique n° 477, 2015'),
    'tresor_apprentissage.pdf': ('https://www.tresor.economie.gouv.fr/Articles/8e3bcd40-cec3-4bd2-88b6-e5e7a8087d39/files/fd39940b-b32e-4245-9daf-21211b1df4e1', "Tresor-Eco n° 376, L'apprentissage en France : quel bilan, nov. 2025"),
    'ofce_pbrief135_apprentissage_2024.pdf': ('https://ofce.sciences-po.fr/pdf/pbrief/2024/OFCEpbrief135.pdf', 'Coquet, OFCE Policy brief n° 135, sept. 2024'),
    'ofce_pbrief157_apprentissage_2026.pdf': ('https://ofce.sciences-po.fr/pdf/pbrief/2026/OFCEpbrief157.pdf', 'Coquet, OFCE Policy brief n° 157, mai 2026'),
    'igas_igf_apprentissage_2024.pdf': ('https://igas.gouv.fr/sites/igas/files/2024-09/Rapport%20Igas%20-IGF%20Apprentissage-Formation%20%28revue%20de%20d%C3%A9penses%29.pdf', 'IGAS-IGF, revue des depenses apprentissage et formation, mars 2024 (non exploite en detail)'),
    'unedic_synthese_evaluation_2025.pdf': ('https://unedic.org/storage/uploads/2025/04/03/Synthese-Principaux-enseignements-de-l-evaluation_uid_67ee965e4dfb9.pdf', "Unedic, Reforme 2019-2021 : principaux enseignements de l'evaluation, mars 2025"),
    'dares_comite_eval_ac_rapport_final_2025.pdf': ('https://www.vie-publique.fr/files/rapport/pdf/298088.pdf', "Rapport du comite d'evaluation de la reforme de l'assurance chomage 2019-2021 (Dares), avr. 2025 (obtenu par WebFetch)"),
    'unedic_reforme2023_contracyclicite_2025.pdf': ('https://s3.eusc-de-east-1.amazonaws.eu/unedic-eks-prod-cms/2025/12/17/reforme-2023-premiers-effets-de-la-reforme-de-contracyclicite_uid_6942b6507b077.pdf', 'Unedic, Reforme 2023 : premiers effets de la contracyclicite, dec. 2025'),
    'cae_note90_assurance_chomage_2026.pdf': ('https://cae-eco.fr/static/pdf/CAE090_Assurance-chomage_260414.pdf', "CAE, Note n° 90, Mesurer l'efficacite de l'assurance chomage, avr. 2026"),
    'cor_doc272.pdf': ('https://www.cor-retraites.fr/sites/default/files/2019-06/doc-272.pdf', 'COR, colloque Age et travail 2001, historique des cessations anticipees'),
    'cor_doc119.pdf': ('https://www.cor-retraites.fr/sites/default/files/2019-06/doc-119.pdf', 'COR, premier rapport 2001, chapitre 2'),
    'cor_2024_doc05_preretraites_jolivet.pdf': ('https://www.cor-retraites.fr/sites/default/files/2024-03/Doc_05_Pr%C3%A9retraites%20entreprise_Annie%20Jolivet.pdf', 'COR, seance du 14 mars 2024, document n° 5 (Jolivet)'),
    'persee_delalande_es372.html': ('https://www.persee.fr/doc/estat_0336-1454_2004_num_372_1_7267', 'Behaghel, Crepon, Sedillot, Contribution Delalande, Economie et statistique n° 372, 2004 (page HTML, resume)'),
}
rows = []
for fn in sorted(os.listdir(SRC)):
    if fn.endswith('.txt'):
        base = fn[:-4]
        cand = [k for k in P if os.path.splitext(k)[0] == base]
        url, desc = (P[cand[0]][0], 'Texte extrait (pdftotext -layout -enc UTF-8) de ' + cand[0]) if cand else ('', 'texte extrait')
    else:
        url, desc = P.get(fn, ('', 'NON DOCUMENTE'))
    h = hashlib.sha256(open(os.path.join(SRC, fn), 'rb').read()).hexdigest()
    rows.append(['sources/' + fn, url, DATE, h, desc])
with open(os.path.join(OUT, 'MANIFESTE_PIECES.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['fichier', 'url', 'date_acces', 'sha256', 'description'])
    w.writerows(rows)
tot = sum(os.path.getsize(os.path.join(SRC, x)) for x in os.listdir(SRC))
print(len(rows), 'pieces ;', round(tot / 1e6, 1), 'Mo ;', [r[0] for r in rows if r[4] == 'NON DOCUMENTE'])
