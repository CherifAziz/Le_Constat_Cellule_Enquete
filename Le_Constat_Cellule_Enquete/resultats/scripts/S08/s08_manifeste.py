# -*- coding: utf-8 -*-
"""S08 - écrit MANIFESTE_PIECES.csv (fichier ; url_origine ; canal ; date ; octets ; sha256).
Usage : python -I s08_manifeste.py"""
import hashlib, os, csv
RAC = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\S08"
SRC = os.path.join(RAC, "sources")
URL = {
 "r19-0401.pdf": "https://www.senat.fr/rap/r19-040/r19-0401.pdf",
 "a25-747-syn.pdf": "https://www.senat.fr/rap/a25-747/a25-747-syn.pdf",
 "a24-748-syn.pdf": "https://www.senat.fr/rap/a24-748/a24-748-syn.pdf",
 "vp_303409.pdf": "https://www.vie-publique.fr/files/rapport/pdf/303409.pdf",
 "vp_164000311.pdf": "https://www.vie-publique.fr/files/rapport/pdf/164000311.pdf",
 "an13_i0067.pdf": "https://www.assemblee-nationale.fr/13/pdf/rap-info/i0067.pdf",
 "vp_298233.pdf": "https://www.vie-publique.fr/files/rapport/pdf/298233.pdf",
 "vp_295578.pdf": "https://www.vie-publique.fr/files/rapport/pdf/295578.pdf",
 "vp_274194.pdf": "https://www.vie-publique.fr/files/rapport/pdf/274194.pdf",
 "vp_194000439.pdf": "https://www.vie-publique.fr/files/rapport/pdf/194000439.pdf",
 "vp_302978.pdf": "https://www.vie-publique.fr/files/rapport/pdf/302978.pdf",
 "senat_Presentation_PLRG_2025.pdf": "https://www.senat.fr/fileadmin/cru-1781387320/Commissions/Finances/2025-2026/Textes_legislatifs/Presentation_PLRG_2025.pdf",
 "hcfp_avis_PLRG2025.pdf": "https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1109784/file/Avis%20HCFP%20PLRG%202025-Final.pdf",
 "senat_Essentiel_RAA_2026.pdf": "https://www.senat.fr/fileadmin/cru-1777295242/Commissions/Finances/2025-2026/Essentiel_RAA_post_commission.pdf",
 "senat_l13-716-11.pdf": "https://www.senat.fr/rap/l13-716-1/l13-716-11.pdf",
 "fipeco_mesures_fiscales.pdf": "https://www.fipeco.fr/pdf/Mesures%20fiscales.pdf",
 "ofce_pbrief104.pdf": "https://www.ofce.sciences-po.fr/pdf/pbrief/2022/OFCEpbrief104.pdf",
 "ipp_note81_EN.pdf": "https://www.ipp.eu/wp-content/uploads/2022/03/Note_IPP_n81_EN.pdf",
 "insee_ES530_Paquier_Sicsic.pdf": "https://www.insee.fr/fr/statistiques/fichier/5426454/02_ES530-31_Paquier-Sicsic_FR.pdf",
}
rows = []
for fn in sorted(os.listdir(SRC)):
    p = os.path.join(SRC, fn)
    if not os.path.isfile(p): continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    rows.append((fn, URL.get(fn, "voir S08.md §17"), "curl -L -A Mozilla/5.0", "2026-11-21", os.path.getsize(p), h))
with open(os.path.join(RAC, "MANIFESTE_PIECES.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["fichier","url_origine","canal","date","octets","sha256"]); w.writerows(rows)
print(len(rows), "pièces")
for r in rows: print(r[0], r[4], r[1] == "voir S08.md §17")
