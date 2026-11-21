# C01 — lecture compacte de l'audit A18 (passe 1 + passe 2), lecture seule des fichiers d'A18.
# Sortie : resultats\donnees\C01\c01_vue_audit_A18.txt (UTF-8)
import csv, collections
D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
p1 = {r["identifiant"]: r for r in csv.DictReader(open(D + r"\A18\A18_audit_V5_passe1.csv", encoding="utf-8-sig"), delimiter=";")}
p2 = list(csv.DictReader(open(D + r"\A18\A18_audit_V5_passe2.csv", encoding="utf-8-sig"), delimiter=";"))
out = open(D + r"\C01\c01_vue_audit_A18.txt", "w", encoding="utf-8")
out.write(f"{len(p2)} lignes passe2 ; {len(p1)} lignes passe1\n")
out.write(str(collections.Counter(r["verdict_M2_passe2"] for r in p2)) + "\n")
for r in p2:
    a = p1.get(r["identifiant"], {})
    out.write(f'{r["identifiant"]} | L{a.get("ligne","?")} | M2p2={r["verdict_M2_passe2"]} | p2={r["verdict_passe2"]} | {r["affirmation"][:140]}\n'
              f'    trouvé: {a.get("valeur_trouvee","")[:260]}\n'
              f'    motif1: {a.get("motif","")[:300]}\n'
              f'    motif2: {r["motif"][:300]} | qui_a_raison={r["qui_a_raison"][:80]}\n')
out.close()
