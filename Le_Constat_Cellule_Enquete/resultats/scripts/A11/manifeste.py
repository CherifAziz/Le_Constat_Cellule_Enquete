# -*- coding: utf-8 -*-
"""A11 - Manifeste des pieces de donnees/A11/sources : fichier ; url_origine ; canal ; date ; octets ; sha256.
Les .txt sont des extractions locales (pdf2txt.py) du PDF de meme nom. Usage : python -I manifeste.py <dossier_sources> <sortie.csv>"""
import os, sys, hashlib, csv, datetime
URL = {
 'hatvp_agora_repertoire_opendata_20261120.json': ('https://www.hatvp.fr/agora/opendata/agora_repertoire_opendata.json', 'curl'),
 'senat_r23-685_syn.pdf': ('https://www.senat.fr/rap/r23-685/r23-685-syn.pdf', 'curl'),
 'senat_r23-685_1.pdf': ('https://www.senat.fr/rap/r23-685/r23-6851.pdf', 'curl'),
 'senat_r19-709_t1.pdf': ('https://www.senat.fr/rap/r19-709-1/r19-709-11.pdf', 'curl'),
 'senat_r19-709_syn.pdf': ('https://www.senat.fr/rap/r19-709-1/r19-709-1-syn.pdf', 'curl'),
 'adlc_avis_14a13.pdf': ('https://www.autoritedelaconcurrence.fr/sites/default/files/commitments//14a13.pdf', 'curl'),
 'igf_cgedd_2021_autoroutes_013462.pdf': ('https://www.igedd.developpement-durable.gouv.fr/IMG/pdf/013462-p_rapport-publie_cle0fe95d.pdf', 'curl'),
 'an_qe16_7045.pdf': ('https://www.assemblee-nationale.fr/dyn/16/questions/QANR5L16QE7045.pdf', 'curl'),
 'senat_r24-065_syn.pdf': ('https://www.senat.fr/rap/r24-065/r24-065-syn.pdf', 'curl'),
 'senat_r21-578_syn.pdf': ('https://www.senat.fr/rap/r21-578-1/r21-578-1-syn.pdf', 'curl'),
 'senat_r21-578_t1.pdf': ('https://www.senat.fr/rap/r21-578-1/r21-578-11.pdf', 'curl'),
 'senat_r24-808_syn.pdf': ('https://www.senat.fr/rap/r24-808-1/r24-808-1-syn.pdf', 'curl'),
 'hcsp_2026_rapport_aides_entreprises.pdf': ('https://www.strategie-plan.gouv.fr/files/files/Publications/2026/2026-07-16%20-%20Rapport%20Aides%20aux%20entreprises/HCSP-2026-RAPPORT-AIDES-ENTREPRISES.pdf', 'curl'),
 'hcsp_2026_medef_reactions.pdf': ('https://www.strategie-plan.gouv.fr/files/files/Publications/2026/2026-07-16%20-%20Rapport%20Aides%20aux%20entreprises/Medef%20-%20r%C3%A9actions%20aux%20conclusions%20du%20HCSP.pdf', 'curl'),
 'igf_revue_depenses_aides_entreprises_2024_vp295437.pdf': ('https://www.vie-publique.fr/files/rapport/pdf/295437.pdf', 'curl'),
 'an_qe17_5756.pdf': ('https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE5756.pdf', 'curl'),
 'an_cion_fin2425126_cr.pdf': ('https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/cion_fin/l17cion_fin2425126_compte-rendu.pdf', 'curl'),
 'an_ppl_1341_dutreil.pdf': ('https://www.assemblee-nationale.fr/dyn/17/textes/l17b1341_proposition-loi.pdf', 'curl'),
 'senat_seance_20151123_CIR.html': ('https://www.senat.fr/seances/s201511/s20151123/s20151123010.html', 'curl'),
 'cc_2023-862DC.html': ('https://www.conseil-constitutionnel.fr/decision/2023/2023862DC.htm', 'curl'),
 'cour_dutreil_synthese_20251118_via_archive.pdf': ('https://web.archive.org/web/2025id_/https://www.ccomptes.fr/sites/default/files/2025-11/20251118-Synthese-Pacte%20Dutreil.pdf', 'curl via web.archive.org'),
 'senat_dossier_ppl21-870.html': ('https://www.senat.fr/dossier-legislatif/ppl21-870.html', 'curl (page sans rapport avec le sujet : URL devinee, consignee [X])'),
}
src, out = sys.argv[1], sys.argv[2]
rows = []
for f in sorted(os.listdir(src)):
    p = os.path.join(src, f)
    if not os.path.isfile(p): continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    d = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M')
    if f in URL: u, c = URL[f]
    elif f.endswith('.txt'):
        base = f.rsplit('.', 1)[0]
        cands = [k for k in URL if k.rsplit('.', 1)[0] == base]
        u, c = (URL[cands[0]][0] if cands else ''), 'extraction locale pdf2txt.py du PDF de meme nom'
    else: u, c = '', 'origine non consignee'
    rows.append([f, u, c, d, os.path.getsize(p), h])
with open(out, 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter=';'); w.writerow(['fichier', 'url_origine', 'canal', 'date', 'octets', 'sha256']); w.writerows(rows)
print(len(rows), 'lignes ;', sum(1 for r in rows if not r[1]), 'sans URL')
