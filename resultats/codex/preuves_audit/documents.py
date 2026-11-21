"""Télécharge les pièces primaires utilisées par A18 et enregistre URL et empreinte."""
import csv
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path

import requests

DEST = Path(__file__).resolve().parent
DOCS = {
    "persson":"https://www.kansascityfed.org/documents/6818/Persson_JH95.PDF",
    "suede_ocde":"https://one.oecd.org/document/PUMA/SBO(98)5/REV1/en/pdf",
    "suede_fmi":"https://www.imf.org/external/pubs/ft/scr/1998/cr98124.pdf",
    "gouvernement_suedois":"https://www.regeringen.se/contentassets/093a2523a04c43ca83d6b2e21d9e5088/the-budget-statement-and-summary/",
    "trajectoire":"https://economy-finance.ec.europa.eu/document/download/2fe78ca8-859d-41c3-8977-6979756ae73f_fr?filename=2027_dbp_fr_fr.pdf",
    "cour_retraites":"https://www.ccomptes.fr/sites/default/files/2025-02/20250220-Situation-financiere-et-perspectives-du-systeme-de%20retraites_0.pdf",
    "cor":"https://www.cor-retraites.fr/sites/default/files/2026-06/RA_2026_def.pdf",
    "commission":"https://economy-finance.ec.europa.eu/document/download/e6bb4d2e-5c46-44e6-a716-6624a57494f3_en?filename=ip348_en.pdf",
    "senat_note":"https://www.senat.fr/rap/r23-685/r23-685-syn.pdf",
    "missions":"https://www.budget.gouv.fr/documentation/file-download/33484",
    "senat_finances":"https://www.senat.fr/fileadmin/Commissions/Finances/2026-2027/PLF_2027/Divers_PLF_2027/Rapport_provisoire_Tome_I.pdf",
    "cour_recettes":"https://www.vie-publique.fr/files/rapport/pdf/294882.pdf",
    "resf":"https://www.tresor.economie.gouv.fr/Articles/03454e04-445d-4ce6-832b-cff601a11485/files/56839f98-37fc-48d8-b502-81cac5a48cad",
    "glp":"https://www.imf.org/external/pubs/ft/wp/2011/wp11158.pdf",
    "bund":"https://api.statistiken.bundesbank.de/rest/download/BBSSY/D.REN.EUR.A630.000000WT1010.A?format=csv&lang=en&startPeriod=2024-06-07&endPeriod=2026-11-13",
    "btp_13nov":"https://live.euronext.com/en/ajax/AwlHistoricalPrice/getFullDownloadAjax/IT0005729931-MOTX?format=csv&base100=no&decimal_separator=.&dateFormat=Y-m-d&from=2026-11-12&to=2026-11-17&typeDownload=2&nbSession=20&inputNbSession=20",
    "oat_MOTX":"https://live.euronext.com/en/ajax/AwlHistoricalPrice/getFullDownloadAjax/FR0014018YR0-MOTX?format=csv&decimal_separator=.&nbSession=30",
}


def fetch(item):
    name, url = item
    suffix=".csv" if name in ("bund","btp_13nov","oat_MOTX") else ".pdf"
    file=DEST/f"{name}{suffix}"
    if file.exists():
        data=file.read_bytes()
        return [name,url,len(data),sha256(data).hexdigest(),"OK, copie conservée"]
    try:
        source=requests.get(url, timeout=35)
        source.raise_for_status()
        data=source.content
        if suffix == ".pdf" and not data.startswith(b"%PDF"):
            raise ValueError("La réponse n'est pas un PDF")
        if suffix == ".csv" and len(data) < 200:
            raise ValueError("Réponse CSV insuffisante")
        file.write_bytes(data)
        return [name,source.url,len(data),sha256(data).hexdigest(),"OK"]
    except (ValueError, requests.RequestException) as error:
        return [name,url,0,"",str(error)]


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as pool:
        records=list(pool.map(fetch,DOCS.items()))
    with (DEST/"archives.csv").open("w",encoding="utf-8-sig",newline="") as f:
        out=csv.writer(f,delimiter=";")
        out.writerow(["document","url","octets","sha256","reponse"])
        out.writerows(records)
    print([(row[0],row[2],row[4]) for row in records])
