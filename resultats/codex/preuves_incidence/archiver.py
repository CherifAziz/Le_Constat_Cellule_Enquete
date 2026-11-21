"""Archive les pièces publiques en PDF ; ne remplace jamais une copie existante."""

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen


DOSSIER = Path(__file__).resolve().parent
PIECES = {
    "insee_emploi_2019": "https://www.insee.fr/fr/statistiques/fichier/4253035/510_511_512_Marchand_Minni_FR.pdf",
    "insee_comptes_2019": "https://www.insee.fr/fr/statistiques/fichier/4498247/ip1801.pdf",
    "pinel_2024": "https://www.ccomptes.fr/sites/default/files/2024-08/20240905-synthese-Aide-fiscale-investissement-locatif-Pinel.pdf",
    "rls_2025": "https://www.ccomptes.fr/sites/default/files/2025-06/20250613-S2025-0769-Suivi-recommandations-dispositif-de-reduction-de-loyer-solidarite-RLS.pdf",
    "hopital_2026": "https://www.ccomptes.fr/sites/default/files/2026-05/20260527-RALFSS-2026-8-Hospitalisations-inadequates.pdf",
    "dentaire_2026": "https://www.ccomptes.fr/sites/default/files/2026-05/20260527-RALFSS-2026-6-Soins-dentaires.pdf",
    "ipp_apprentissage": "https://www.ipp.eu/wp-content/uploads/2025/06/51_jeune_1_solution_apprentissage-1.pdf",
    "drees_invalidite": "https://drees.solidarites-sante.gouv.fr/sites/default/files/2022-10/dd06.pdf",
    "cir_ipp": "https://www.strategie-plan.gouv.fr/files/files/Publications/2021/0601%20CNEPI/2021_ipp-pse_rapportfinal_pour_cnepi_impact_du_cir_0.pdf",
    "cice_evaluation": "https://www.strategie-plan.gouv.fr/files/files/Publications/2020/CICE/fs-2020-rapport-cice2020-16septembre-final18h.pdf",
    "cnav_2024": "https://www.statistiques-recherche.lassuranceretraite.fr/app/uploads/2025/09/1.7-La-situation-financiere-du-regime-general.pdf",
    "cnam_2026": "https://www.assurance-maladie.ameli.fr/sites/default/files/2025-07_rapport-propositions-pour-2026_assurance-maladie.pdf",
}


def conserver(item):
    identifiant, url = item
    fichier = DOSSIER / (identifiant + ".pdf")
    try:
        if fichier.is_file():
            contenu = fichier.read_bytes()
        else:
            requete = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(requete, timeout=25) as reponse:
                contenu = reponse.read()
        if not contenu.startswith(b"%PDF-") or b"%%EOF" not in contenu[-2048:]:
            raise ValueError("reponse autre qu'un PDF complet")
        if not fichier.exists():
            with fichier.open("xb") as sortie:
                sortie.write(contenu)
        return f"{sha256(contenu).hexdigest()}  {fichier.name}"
    except (OSError, ValueError) as erreur:
        return f"INDISPONIBLE {identifiant}  {erreur}"


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        for ligne in pool.map(conserver, PIECES.items()):
            print(ligne)
