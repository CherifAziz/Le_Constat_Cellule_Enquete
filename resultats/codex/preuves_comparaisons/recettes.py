"""Calcul des variantes politiques A14, en milliards d'euros à assiettes 2025 constantes."""
import csv
from pathlib import Path

POINT_TVA_NORMAL = 7.5  # Trésor-Éco 371, tableau 2, net des achats des APU
DEMI_POINT_CSG = 0.5 * 17.9  # DSS, REPSS financement, indicateur 1.4.1
COMPENSATION = 2.0  # enveloppe de remboursement aux ménages
ADMINISTRATION = 0.1
EMPLOI = 0.3
# q = fraction de la valeur théorique de CSG conservée à PIB fixé (assiette légale).
# idx = coût d'indexation en année pleine, Md€. m = pertes de PIB en euros par euro d'effort direct.
VARIANTES = {
    "favorable": dict(q=1, idx=0.4, m={2027:0.3, 2030:0.1, 2035:0}),
    "centrale": dict(q=0.95, idx=1.0, m={2027:0.7, 2030:0.3, 2035:0}),
    "adverse": dict(q=0.80, idx=2.0, m={2027:1.3, 2030:0.9, 2035:0.5}),
}
RETROACTION = 0.45  # Md€ de prélèvements/prestations cycliques par Md€ de PIB perdu, hypothèse en niveau.
def calculer():
    for nom, h in VARIANTES.items():
        for an, fraction in ((2027,0.5),(2030,1),(2035,1)):
            fiscal = fraction*(POINT_TVA_NORMAL + DEMI_POINT_CSG*h["q"])
            depenses = fraction*(COMPENSATION + h["idx"]) + ADMINISTRATION + EMPLOI
            direct = fiscal - depenses
            pib_perdu = h["m"][an] * direct
            net = direct - RETROACTION*pib_perdu
            yield dict(variante=nom, an=an, fraction=fraction, q=h["q"], indexation_pleine=h["idx"],
                       multiplicateur=h["m"][an], fiscal=round(fiscal,3), depenses=round(depenses,3),
                       direct=round(direct,3), pib_perdu=round(pib_perdu,3), net=round(net,3))

if __name__ == "__main__":
    lignes = list(calculer())
    with Path(__file__).with_name("recettes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=lignes[0])
        w.writeheader()
        w.writerows(lignes)
