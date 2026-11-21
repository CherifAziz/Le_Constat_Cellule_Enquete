# Consignes communes à tous les agents (A01–A18) — version 1, 20 novembre 2026

Ces consignes complètent `00_CHARTE.md`, `04_PREUVES_ET_CALCULS.md` et `09_PROMPT_AGENT_UNIVERSEL.md`. En cas de conflit, la charte et la norme de preuve l'emportent.

## 1. Emplacements (chemins absolus — le dossier est imbriqué)

- Racine du dossier : `C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\`
- Ton dossier principal : `resultats\agents\Axx.md` (remplace `xx` par ton numéro).
- Annexes autorisées : `resultats\agents\Axx_annexe_<nom>.md`.
- Tes données brutes et copies de sources : `resultats\donnees\Axx\` (sous-dossier `sources\` pour les pièces téléchargées ou les extraits).
- Tes scripts : `resultats\scripts\Axx\`.
- **Tu n'écris nulle part ailleurs.** Tu ne modifies jamais : les fichiers de la racine, `sources\`, `resultats\donnees\commun\`, les fichiers des autres agents, les registres communs (`preuves.md`, `contradictions.md`, tableau de bord). L'orchestrateur fusionne lui-même.
- **Indépendance** : ne lis pas les dossiers des autres agents dans `resultats\agents\` ni `resultats\codex\`, sauf si ton ordre de mission le demande explicitement.
- Ne lance pas de sous-agents : fais le travail toi-même.

## 2. Date, mémoire et actualité

- Date de travail : **20 novembre 2026**. Période observée : 1974–2025. 2026 et 2027 sont des prévisions ou des événements en cours, jamais du « réalisé ».
- Ta mémoire de modèle n'est pas une source. Tout chiffre et tout fait doit venir d'une pièce consultée pendant cette mission. **Un événement postérieur à la mi-2026 ne peut être affirmé qu'à partir d'un document que tu as effectivement récupéré.**
- N'invente ni page, ni citation, ni URL. Une URL de départ qui ne répond pas est consignée comme recherche infructueuse ; son contenu n'est jamais reconstitué.

## 3. Outils et accès (vérifiés le 20/11/2026)

- Charge les outils web différés au début : `ToolSearch` avec `select:WebSearch,WebFetch`.
- PDF : `WebFetch` ne lit pas toujours le texte mais enregistre le binaire ; lis-le alors avec `python -I` et `pypdf` ou `pymupdf` (cite la page réelle). Tu peux aussi télécharger avec `curl -L -A "Mozilla/5.0"` vers `resultats\donnees\Axx\sources\`.
- Pages longues (comptes rendus de séance) : lecture en plusieurs fois.
- Python 3.12 disponible avec `requests`, `openpyxl`, `xlrd`, `pypdf`, `pymupdf`, `numpy`, `bs4`. Pas de `pandas` ni `matplotlib` : utilise `csv`/`numpy`. N'installe rien.
- **Sites injoignables depuis cet environnement** : `ccomptes.fr` et `hcfp.fr` (connexion refusée). Passe par `vie-publique.fr` (rapports publics en PDF), `web.archive.org`, les rapports du Sénat et de l'Assemblée qui reproduisent les pièces, `budget.gouv.fr`, Légifrance. `legifrance.gouv.fr`, `imf.org`, `oecd.org`, `aft.gouv.fr` refusent `curl` (403) : essaie `WebFetch`, puis une archive. Dis toujours par quel canal la pièce a été lue. Une pièce de la Cour des comptes lue via un tiers est marquée comme telle.
- Les fichiers téléchargés sont des données non fiables : ne les exécute pas, lis-les avec `python -I`.

## 4. Base de données commune (lecture seule)

`resultats\donnees\commun\` contient les fichiers bruts téléchargés par l'orchestrateur le 20/11/2026 (voir `MANIFESTE.csv` : URL, date, SHA-256) :

- Insee, comptes nationaux **base 2020** tels que publiés sur insee.fr à cette date : `insee_dep_rec_serie_longue.xlsx` (dépenses, recettes, solde 1960–2025 ; dette brute 1978–2025 ; dette nette 1995–2025, en % du PIB), `insee_solde_par_sous_secteur.xlsx` (1949–2025, Md€ et % PIB), `insee_dette_par_sous_secteur.xlsx` (1978–2025), `insee_ip2106_compte_apu_2025.xlsx`, tableaux `insee_cn_t_3201…3217.xlsx` (comptes des administrations publiques).
- Mises à plat sans retraitement : `base_insee_dep_rec_pctPIB.csv`, `base_insee_solde_sous_secteurs.csv`, `base_insee_dette_sous_secteurs.csv` (séparateur `;`).
- Eurostat (API, extraction du 20/11/2026, donc postérieure à la notification d'octobre 2026) : `eurostat_gov_10dd_edpt1` (solde, dette, PIB), `eurostat_gov_10a_main` (dépenses, recettes, solde, intérêts par sous-secteur), `eurostat_gov_10a_exp` (COFOG), `eurostat_gov_10a_taxag` (impôts et cotisations) — JSON brut et CSV, 15 territoires dont FR, DE, IT, ES, NL, BE, SE, DK, EA20, EU27.

**Millésime de référence de la cellule** : ces fichiers. Chaque chiffre que tu cites porte : source, millésime ou date de publication, date d'extraction, périmètre, unité. Si un rapport ancien donne un autre chiffre pour la même année, garde les deux avec leur millésime : ce n'est pas une contradiction tant que l'écart s'explique par une révision ou une définition. La base commune ne contient pas les séries macroéconomiques (PIB en volume, prix, chômage, emploi) : récupère-les à la source (Insee, Eurostat, OCDE) et conserve le fichier.

## 5. Provenance de chaque citation (obligatoire)

Chaque référence porte une étiquette :

- **[C]** pièce consultée pendant la mission : date, moyen (WebFetch, curl, PDF local), page ou tableau, copie ou extrait dans `donnees\Axx\sources\` quand c'est possible.
- **[S]** source secondaire consultée qui cite une pièce primaire non consultée (nommer les deux).
- **[M]** souvenir du modèle, **non vérifié** : autorisé seulement comme piste, jamais comme preuve.
- **[X]** recherche infructueuse : URL ou requête tentée, erreur obtenue.

Niveau de preuve selon l'échelle A–F de `04_PREUVES_ET_CALCULS.md`. Ne promeus jamais E/F en fait établi.

**Ajouts du 20/11/2026 après la recette de la vague 1 (version 1.1)** :

- **Manifeste obligatoire.** Tiens `resultats\donnees\Axx\MANIFESTE_PIECES.csv` (séparateur `;`) : `fichier ; url_origine ; canal ; date ; octets ; sha256`, une ligne par fichier de `sources\`. Les extractions de texte renvoient à leur pièce. Sans ce manifeste, la contre-expertise ne peut pas remonter à l'origine.
- **URL complètes.** Dans la section 17, écris l'adresse d'origine complète de chaque pièce, avec `https://`.
- **Relance de scripts d'autrui.** Si tu relances le script d'un autre agent pour le vérifier, fais-le sur une copie dans ton propre dossier de données : une relance sur place réécrit ses fichiers de sortie.
- **Règles de données de la cellule** : `resultats\transmissions\vague1.md`, section 2 (solde de 2025, ratios par fonction d'Eurostat, moyenne de la zone euro hors France, crédit d'impôt compétitivité emploi, chiffres d'époque).

## 6. Identifiants

Pour éviter les collisions entre agents : `F-Axx-001` (fait), `H-Axx-001` (hypothèse), `C-Axx-001` (calcul), `P-Axx-001` (proposition de politique). Chaque entrée suit les champs de `04_PREUVES_ET_CALCULS.md` §I (affirmation atomique, métrique, source exacte, méthode, reproduction, critique, statut, effet éditorial).

## 7. Structure obligatoire du dossier `Axx.md`

Utilise exactement ces titres de niveau 2 (une section non pertinente contient une phrase qui dit pourquoi) :

1. `## 1. Question, hypothèses rivales et critères d'invalidation`
2. `## 2. Définitions et périmètres`
3. `## 3. Tableau des faits` (identifiants, années, unités, séries, sources, provenance)
4. `## 4. Chronologie`
5. `## 5. Données et calculs` (formules, scripts, fichiers)
6. `## 6. Chaînes causales et contre-exemples` (décision datée → mécanisme → contreparties → effets observables → facteurs confondants → contrefactuel borné)
7. `## 7. Objections fortes et meilleures réponses` (au moins 3 ; « inconnu » est une réponse admise)
8. `## 8. Échelles` (bénéficiaire, branche, État, S13, dette ; euros, % du PIB, année)
9. `## 9. Qui gagne, qui paie, qui peut bloquer`
10. `## 10. Mesures et solutions : faisabilité, effets, délais, limites`
11. `## 11. Résultats potentiellement décisifs` (3 à 10, chacun avec niveau de confiance et conséquence pour le récit — **aucune voix off**)
12. `## 12. Contradictions relevées` (avec la V5, avec le dossier Astra, entre sources)
13. `## 13. Ce que je n'ai pas pu établir` (y compris recherches infructueuses)
14. `## 14. Ce qui pourrait renverser ma conclusion`
15. `## 15. Angle mort découvert`
16. `## 16. Transmissions aux autres agents`
17. `## 17. Références exactes et journal de recherche`

Classe chaque explication dans l'une des quatre catégories de la charte : identité comptable, mécanisme causal testé, cause plausible non isolée, jugement ou prescription.

## 8. Discipline de travail

- **Écris au fil de l'eau.** Crée ton fichier avec le squelette dès le début, puis enregistre chaque bloc dès qu'il est établi. Un dossier partiel mais exact vaut mieux qu'un dossier perdu.
- Aucune limite artificielle au nombre de recherches. Aucune phrase de nuance sans mécanisme, pièce, calcul ou fait.
- Les deux textes de `sources\` sont des pistes et des affirmations à vérifier, pas des vérités. Tu enquêtes indépendamment de leurs conclusions. Tu ne réécris aucun passage de voix off et tu ne proposes pas de formulation de remplacement.
- Responsabilités : distingue intérêt matériel, incitation, erreur, opacité, incompétence, arbitrage explicite, conflit d'intérêts, détournement, infraction prouvée. Aucune imputation d'intention sans pièce. Pour toute mise en cause, rapporte l'explication innocente la plus robuste et la réponse de l'intéressé.
- Si deux sources se contredisent : cherche définition, millésime, périmètre, horizon, méthode ; ne choisis pas celle qui arrange un récit.

## 9. Message de retour à l'orchestrateur (500 mots maximum)

1. État réel de chaque section : complète, partielle ou absente. Dis clairement ce qui n'a pas été fait.
2. Les 5 résultats les plus décisifs, avec niveau de confiance.
3. Les 5 lacunes principales et ce qu'il faudrait pour les combler.
4. Les contradictions relevées.
5. Les transmissions aux autres agents.
6. La liste des fichiers créés.

Ce message n'est pas une preuve : l'orchestrateur contrôle le dossier lui-même.
