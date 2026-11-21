# -*- coding: utf-8 -*-
"""A03 - manifeste des pièces documentaires de donnees/A03/sources : fichier, URL d'origine, canal, SHA-256, taille.
Sortie : donnees/A03/MANIFESTE_PIECES_A03.csv. Lancer : python -I manifeste_pieces.py"""
import os, csv, hashlib
ICI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(ICI, "..", "..", "donnees", "A03", "sources"))
URL = {
    "AN_CR_2e_seance_2026-11-04.html": ("https://www.assemblee-nationale.fr/dyn/17/comptes-rendus/seance/session-ordinaire-de-2026-2027/deuxieme-seance-du-mercredi-04-novembre-2026", "curl 20/11/2026"),
    "CE_prev_automne_2026_ip348.pdf": ("https://economy-finance.ec.europa.eu/document/download/e6bb4d2e-5c46-44e6-a716-6624a57494f3_en?filename=ip348_en.pdf", "curl 20/11/2026"),
    "HCFP_avis_2026-5.pdf": ("https://web.archive.org/web/20261021215439/http://www.hcfp.fr/sites/default/files/2026-10/Avis%20HCFP%202026-5%20-%20PLF-PLFSS%202027.pdf", "web.archive.org, capture 21/10/2026"),
    "HCFP_avis_2026-5_page_archive.html": ("https://web.archive.org/web/20261021215439/https://www.hcfp.fr/liste-avis/avis-ndeg2026-5-lois-de-finances-2027", "web.archive.org, capture 21/10/2026"),
    "PLF2027_RESF.pdf": ("https://www.tresor.economie.gouv.fr/Articles/03454e04-445d-4ce6-832b-cff601a11485/files/56839f98-37fc-48d8-b502-81cac5a48cad", "curl 20/11/2026"),
    "senat_r23-685_syn.pdf": ("https://www.senat.fr/rap/r23-685/r23-685-syn.pdf", "curl 20/11/2026"),
    "senat_r24-153_syn.pdf": ("https://www.senat.fr/rap/r24-153/r24-153-syn.pdf", "curl 20/11/2026"),
    "AN_l17b1274_tI_rapport_enquete.pdf": ("https://www.assemblee-nationale.fr/dyn/17/rapports/cion_fin/l17b1274-ti_rapport-enquete.pdf", "curl 20/11/2026"),
    "AN_i2689_Carrez_2010.pdf": ("https://www.assemblee-nationale.fr/13/pdf/rap-info/i2689.pdf", "curl 20/11/2026"),
    "VP_293446.pdf": ("http://web.archive.org/web/20250410113353id_/https://www.vie-publique.fr/files/rapport/pdf/293446.pdf", "web.archive.org (Cour des comptes, mars 2024, lue via tiers)"),
    "VP_294882.pdf": ("http://web.archive.org/web/20261009090115id_/https://www.vie-publique.fr/files/rapport/pdf/294882.pdf", "web.archive.org (Cour des comptes, juillet 2024, lue via tiers)"),
    "VP_104000241_archive.pdf": ("http://web.archive.org/web/20221012101234id_/https://www.vie-publique.fr/sites/default/files/rapport/pdf/104000241.pdf", "web.archive.org ; NB : rapport Carrez-Thénault, pas Champsaur-Cotis"),
    "VP_104000203_archive.pdf": ("http://web.archive.org/web/20200724064058id_/https://www.vie-publique.fr/sites/default/files/rapport/pdf/104000203.pdf", "web.archive.org ; NB : rapport Jamet, pas Champsaur-Cotis"),
    "insee_fichemethodo7_B2020_revision_ratios_apu.pdf": ("https://www.insee.fr/fr/metadonnees/source/fichier/fichemethodo7_B2020_revision_ratios_apu.pdf", "WebFetch (binaire enregistré) 20/11/2026"),
    "insee_____________________________________905.html": ("https://www.insee.fr/fr/statistiques/9053525", "curl 20/11/2026 (dette T2 2026)"),
    "insee______________________________________900.html": ("https://www.insee.fr/fr/statistiques/9007857?sommaire=9007859", "curl 20/11/2026"),
    "datagouv_gouvernements_membres.csv": ("https://www.data.gouv.fr/api/1/datasets/r/0ac23b31-0dfb-47f5-8b65-e21103f4be8c", "curl 20/11/2026"),
    "datagouv_gouvernements_pm.csv": ("https://www.data.gouv.fr/api/1/datasets/r/5e8c4460-11a6-433b-b48a-694ab7a0357d", "curl 20/11/2026"),
    "datagouv_gouvernements_presidents.csv": ("https://www.data.gouv.fr/api/1/datasets/r/0492fc8f-da9f-4c43-a899-66583a626b24", "curl 20/11/2026"),
    "VP_loi_300445_LFSS2026.html": ("https://www.vie-publique.fr/loi/300445-loi-de-financement-de-la-securite-sociale-2026-retraites-lfss", "curl : 294 octets, échec [X]"),
}
rows = []
for f in sorted(os.listdir(SRC)):
    fp = os.path.join(SRC, f)
    if not os.path.isfile(fp):
        continue
    b = open(fp, "rb").read()
    u, canal = URL.get(f, ("voir MANIFESTE_A03.csv (séries) ou extraction texte d'une pièce listée", ""))
    rows.append([f, u, canal, len(b), hashlib.sha256(b).hexdigest()])
with open(os.path.join(SRC, "..", "MANIFESTE_PIECES_A03.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["fichier", "url", "canal_date", "octets", "sha256"])
    w.writerows(rows)
print(len(rows))
