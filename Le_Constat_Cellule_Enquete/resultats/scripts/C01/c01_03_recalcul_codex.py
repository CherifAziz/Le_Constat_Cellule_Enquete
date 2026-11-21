# C01 — recalculs sur la COPIE de calculs\annuel.csv de Codex (donnees\C01\copies_codex\calculs\annuel.csv)
# But : mettre les chiffres de Codex dans les fenêtres et conventions de la cellule (dette 1979-2025 et 2001-2025,
# stabilisation à g = 1,9-2,5 %, intérêts 2025). Aucun fichier de Codex n'est exécuté ni modifié.
import csv, sys
sys.stdout.reconfigure(encoding="utf-8")
C = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees\C01\copies_codex\calculs\annuel.csv"
rows = {int(r["annee"]): r for r in csv.DictReader(open(C, encoding="utf-8-sig"), delimiter=";")}
f = lambda y, k: float(rows[y][k]) if rows[y][k] not in ("", None) else None

def decomp(a, b):
    """Somme des variations annuelles du ratio dette/PIB (convention Codex 02_comptabilite_reconciliee) de a à b."""
    P = I = G = A = 0.0
    for t in range(a + 1, b + 1):
        Y, Y0, D, D0 = f(t, "pib"), f(t - 1, "pib"), f(t, "dette"), f(t - 1, "dette")
        B, It = f(t, "b9"), f(t, "interets")
        Pt = B + It
        At = D - D0 + B  # ajustement stock-flux (B négatif = déficit)
        P += -100 * Pt / Y; I += 100 * It / Y; A += 100 * At / Y; G += 100 * D0 * (1 / Y - 1 / Y0)
    d = 100 * f(b, "dette") / f(b, "pib") - 100 * f(a, "dette") / f(a, "pib")
    return d, P, I, G, A

# decomp(a, b) somme les FLUX des années a+1 à b (bornes = fins d'année, convention Codex).
# La cellule nomme ses fenêtres par années de flux : « 1979-2025 » cellule = decomp(1978, 2025) ; « 2001-2025 » = decomp(2000, 2025).
for a, b in [(1978, 2025), (2000, 2025), (1979, 2025), (2001, 2025), (2014, 2019), (2015, 2019), (1998, 2001), (2023, 2025)]:
    d, P, I, G, A = decomp(a, b)
    print(f"{a}-{b} : variation {d:.2f} = déficit primaire {P:.2f} + intérêts {I:.2f} + PIB nominal {G:.2f} + stock-flux {A:.2f}"
          f" | intérêts+PIB (convention cellule « taux-croissance ») {I+G:.2f} | contrôle somme {P+I+G+A:.2f}")

Y25, D24, D25 = f(2025, "pib"), f(2024, "dette"), f(2025, "dette")
print(f"2025 : intérêts D41 {f(2025,'interets'):.3f} Md€ = {100*f(2025,'interets')/Y25:.3f} % du PIB ; primaire {f(2025,'b9')+f(2025,'interets'):.3f} Md€ = {100*(f(2025,'b9')+f(2025,'interets'))/Y25:.3f} %")
print(f"2025 : solde {f(2025,'b9'):.3f} Md€ = {100*f(2025,'b9')/Y25:.3f} % ; PIB {Y25:.3f} ; dette fin 2025 {D25} ; ratio {100*D25/Y25:.2f}")
# Stabilisation : convention cellule (A01) : déficit stabilisant = d*g/(1+g), d = 115,7 %, sans stock-flux, au PIB 2025
for g in (0.019, 0.022, 0.025, 0.03):
    ds = 1.157 * g / (1 + g)
    print(f"g={g:.3f} : déficit stabilisant {100*ds:.3f} % ; écart au déficit 2025 {100*(0.05068-ds):.3f} pts = {(0.05068-ds)*Y25:.1f} Md€ (PIB 2025)")
# Convention Codex A17 : D24 x g_2025 observée - SFA observé
g25 = Y25 / f(2024, "pib") - 1
sfa25 = D25 - D24 + f(2025, "b9")
comp = D24 * g25 - sfa25
print(f"Codex A17 : g 2025 observée {100*g25:.4f} % ; SFA 2025 {sfa25:.3f} ; déficit compatible {comp:.2f} ; écart {(-f(2025,'b9'))-comp:.2f} Md€")
comp0 = D24 * g25
print(f"variante Codex sans SFA : déficit compatible {comp0:.2f} ; écart {(-f(2025,'b9'))-comp0:.2f} Md€")
