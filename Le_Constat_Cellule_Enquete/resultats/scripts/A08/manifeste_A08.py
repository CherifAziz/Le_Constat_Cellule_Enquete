# -*- coding: utf-8 -*-
"""A08 - Manifeste des pieces de resultats/donnees/A08/sources/ (consignes communes v1.1, par. 5).
Colonnes : fichier ; url_origine ; canal ; date ; octets ; sha256. Separateur ';'.
Usage : python -I manifeste_A08.py
"""
import csv
import datetime
import hashlib
import pathlib

R = pathlib.Path(__file__).resolve().parents[2]
SRC = R / 'donnees' / 'A08' / 'sources'
OUT = R / 'donnees' / 'A08' / 'MANIFESTE_PIECES.csv'
WB = 'web.archive.org (capture id_)'
EC = 'https://ec.europa.eu/economy_finance/economic_governance/sgp/pdf/20_scps/'
H = 'https://www.hcfp.fr/'
U = {
    'HCFP_note_etude_2024-2.pdf': (H + "sites/default/files/2024-09/Note%20d%27%C3%A9tudes%202024-2.pdf", WB + ' 2025'),
    'ce_scp_prior2024.html': ('https://economy-finance.ec.europa.eu/economic-governance-framework/stability-and-growth-pact/preventive-arm-prior-2024/stability-and-convergence-programmes-prior-2024_en', 'curl'),
    'senat_l08-07810.html': ('https://www.senat.fr/rap/l08-078/l08-07810.html', 'curl'),
    'senat_l08-0787.html': ('https://www.senat.fr/rap/l08-078/l08-0787.html', 'curl'),
    'AN_l16b1850_rapport_LPFP2023.pdf': ('https://www.assemblee-nationale.fr/dyn/16/rapports/cion_fin/l16b1850_rapport-fond.pdf', 'curl'),
    'CE_assessment_SP2017_fr.pdf': ('https://economy-finance.ec.europa.eu/document/download/ca24aaa6-a2ec-4c06-83cd-21c52d6cb641_en?filename=10_fr_sp_assessment.pdf', 'curl'),
    'senat_r15-5501.pdf': ('https://www.senat.fr/rap/r15-550/r15-5501.pdf', 'curl'),
    'senat_r13-4831.pdf': ('https://www.senat.fr/rap/r13-483/r13-4831.pdf', 'curl'),
    'senat_r14-6011.pdf': ('https://www.senat.fr/rap/r14-601/r14-6011.pdf', 'curl'),
    'senat_r17-4381.pdf': ('https://www.senat.fr/rap/r17-438/r17-4381.pdf', 'curl'),
    'senat_r18-4681.pdf': ('https://www.senat.fr/rap/r18-468/r18-4681.pdf', 'curl'),
    'senat_r20-5551.pdf': ('https://www.senat.fr/rap/r20-555/r20-5551.pdf', 'curl'),
    'senat_r23-5591.pdf': ('https://www.senat.fr/rap/r23-559/r23-5591.pdf', 'curl'),
    'senat_r24-5671.pdf': ('https://www.senat.fr/rap/r24-567/r24-5671.pdf', 'curl'),
    'senat_r18-3381.pdf': ('https://www.senat.fr/rap/r18-338/r18-3381.pdf', 'curl'),
    'HCFP_avis_2022-3_PSTAB2022.pdf': ('http://www.hcfp.fr/sites/default/files/2022-07/Avis%20HCFP%202022-3.pdf', WB + ' 2022'),
    'HCFP_avis_2023-6_PSTAB2023.pdf': ('http://www.hcfp.fr/sites/default/files/2023-04/Avis%20HCFP-2023-6-PStab_2023.pdf', WB + ' 2023'),
    'HCFP_opinion_2022-5_PLPFP2023-2027_EN.pdf': ('http://www.hcfp.fr/sites/default/files/2022-10/Opinion%202022-5%20PFPL%202023-2027.pdf', WB + ' 2023'),
    'HCFP_opinion_2025-3_RAA2025_EN.pdf': ('http://www.hcfp.fr/sites/default/files/2025-04/Opinion%20HCFP%20-%202025%20-%203%20-%20RAA%202025%20VENG_clean.pdf', WB + ' 2025'),
    'HCFP_avis_2024-2_PSTAB2024.pdf': ('http://www.hcfp.fr/sites/default/files/2024-04/Avis%20HCFP-2024-2%20PSTAB%202024-2027%20-%20Vdef.pdf', WB + ' 2024'),
    'avis-ndeg2022-3-programme-de-stabilite-2022-2027.html': (H + 'liste-avis/avis-ndeg2022-3-programme-de-stabilite-2022-2027', WB + ' 20220926001118'),
    'avis-ndeg2023-6-programme-de-stabilite-2023-2027.html': (H + 'liste-avis/avis-ndeg2023-6-programme-de-stabilite-2023-2027', WB + ' 20230426081844'),
    'opinion-ndeg2022-5-public-finance-programming-bill.html': (H + 'en/liste-avis/opinion-ndeg2022-5-public-finance-programming-bill', WB + ' 20230209120103'),
    'opinion-ndeg2025-3-annual-progress-report-2025.html': (H + 'en/liste-avis/opinion-ndeg2025-3-annual-progress-report-2025', WB + ' 20250624050053'),
    'avis-ndeg2024-2-programme-de-stabilite-2024-2027.html': (H + 'liste-avis/avis-ndeg2024-2-programme-de-stabilite-2024-2027', WB + ' 20240418051424'),
    'AN_l17b1891_recevabilite_financiere.pdf': ('https://www.assemblee-nationale.fr/dyn/17/rapports/cion_fin/l17b1891_rapport-information.pdf', 'curl'),
    'fipeco_Pstab2023-2027.pdf': ('https://fipeco.fr/pdf/Pstab2023-2027.pdf', 'curl'),
    'VP_loi_286456_LPFP2023.html': ('https://www.vie-publique.fr/loi/286456-loi-programmation-des-finances-publiques-lpfp-2023-2027', WB + ' 2025'),
    'CC_constitution_1958.html': ('https://www.conseil-constitutionnel.fr/le-bloc-de-constitutionnalite/texte-integral-de-la-constitution-du-4-octobre-1958-en-vigueur', 'curl'),
    'CC_2023862DC.html': ('https://www.conseil-constitutionnel.fr/decision/2023/2023862DC.htm', 'curl'),
    'CC_2023857DC.html': ('https://www.conseil-constitutionnel.fr/decision/2023/2023857DC.htm', 'curl'),
    'LOLF_legifrance_archive.html': ('https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000394028', WB + ' 20241231074446 (articles non contenus dans la capture)'),
    'SE_fiscal_policy_framework_skr2025-26-76.pdf': ('https://www.government.se/contentassets/afd79a1ff8954c78b7681f6a8fa6c8e1/the-fiscal-policy-framework-skr.-20252676.pdf', 'curl'),
}
# programmes de stabilite : URL et horodatage depuis pstab/liste.txt
liste = SRC / 'pstab' / 'liste.txt'
if liste.exists():
    for line in liste.read_text(encoding='utf-8').splitlines():
        if line.strip():
            ts, url = line.split(' ', 1)
            U[url.rsplit('/', 1)[-1]] = (url, f'{WB} {ts}')

rows = []
for p in sorted(SRC.rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(SRC).as_posix()
    name = p.name
    if name in U:
        url, canal = U[name]
    elif p.suffix == '.txt' and name != 'liste.txt':
        base = [q for q in p.parent.glob(p.stem + '.*') if q.suffix in ('.pdf', '.html')]
        url = 'derive de ' + (base[0].name if base else '?')
        canal = 'extraction locale (pymupdf ou bs4, scripts/A08)'
    elif name == 'liste.txt':
        url, canal = 'index CDX web.archive.org (ec.europa.eu/economy_finance/.../20_scps/*)', 'curl web.archive.org/cdx'
    else:
        url, canal = 'non renseigne', ''
    data = p.read_bytes()
    rows.append([rel, url, canal, datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M'),
                 len(data), hashlib.sha256(data).hexdigest()])
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(['fichier', 'url_origine', 'canal', 'date', 'octets', 'sha256'])
    w.writerows(rows)
print(OUT, len(rows), 'fichiers ;', sum(1 for r in rows if r[1] == 'non renseigne'), 'sans URL')
