# Smoke test sous-agent (2026-11-20)

- Outils : WebSearch et WebFetch charges via ToolSearch ; Bash (curl, python+pypdf) disponible ; navigateurs (Claude_Browser, claude-in-chrome) presents mais non testes ; outil Agent disponible (non utilise).
- INSEE 2381414 : OK (WebFetch). Titre "Depenses et recettes publiques" ; 57,3 % du PIB en 2025 (p) ; xlsx : https://www.insee.fr/fr/statistiques/fichier/2381414/econ-fin-pub-rec-dep.xlsx
- PDF Senat r23-685-syn : WebFetch n'a pas lu le texte (binaire) mais a sauve le fichier ; lu avec python -I + pypdf (10 pages). p.1 : "Le deficit public en 2023 a atteint le niveau inedit, hors periode de crise, de 5,5 % du PIB."
- Eurostat 21/10/2026 : OK. Zone euro deficit 3,0 % du PIB en 2024 et 2025 ; UE 3,1 %.
- AN 2e seance 04/11/2026 : OK (page partiellement lue, 100k/219k car.). D. Amiel : deficit budgetaire 177,1 Md EUR apres 1re partie PLF 2027 (+20,7 Md vs texte initial).
- Cour des comptes PDF 2026-11 : ECHEC. WebFetch "connect ECONNREFUSED 185.75.142.141:443" ; curl timeout, meme sur la page d'accueil ccomptes.fr.
- WebSearch : OK. 3 premiers : blog.forumforthefuture.be (automne 2026...), lepetitjournal.com (deficit italien 2026), cbnews.fr/node/96761. Aucune date affichee dans les resultats bruts.
