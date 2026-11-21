# Contrôle de provenance des pièces de la vague 1

**Fait par l'orchestrateur le 20 novembre 2026, 12 h 52 – 12 h 58.** Scripts : `scripts\commun\controle_provenance.py`, `scripts\commun\controle_manifestes.py`. Résultat brut : `donnees\commun\controle_provenance\RAPPORT.csv`.

## Pourquoi

Les sondages de recette ont été faits dans les **copies locales** des pièces, enregistrées par les agents. Ils prouvent que l'agent a bien transcrit ce que dit sa copie ; ils ne prouvent pas que la copie est la pièce d'origine. Ce contrôle ferme cet écart pour les pièces qui portent les constats les plus lourds.

## 1. Retéléchargement à l'origine par l'orchestrateur

| Pièce | Origine | Copie comparée | Résultat |
|---|---|---|---|
| Avis du HCFP n° 2026-5 sur le budget 2027 | archive web d'une capture du 21 octobre 2026 de hcfp.fr | A03 | **identique** (même empreinte SHA-256) |
| Rapport économique, social et financier annexé au budget 2027 | tresor.economie.gouv.fr | A03 | **identique** |
| Cour des comptes, situation et perspectives des finances publiques, juillet 2024 | vie-publique.fr | A04 | **identique** |
| Rapport annuel 2026 du COR | cor-retraites.fr | A06 | **identique** |
| Commission européenne, prévisions d'automne 2026 | economy-finance.ec.europa.eu | A01 | **identique** |
| Sénat, synthèse du rapport r24-153 | senat.fr | A03 | **identique** |
| Sénat, rapport n° 133 (1975-1976) | senat.fr | A02 | **identique** |
| Assemblée nationale, séance du 4 novembre 2026 | assemblee-nationale.fr (page HTML) | A03 | scrutin « 0 pour, 458 contre » et « 5,9 % » présents à l'origine et dans la copie |
| Insee Première n° 2106 | insee.fr (page HTML) | A01 | « 152,5 » présent des deux côtés ; le motif cherché pour « 23,0 Md » n'est trouvé ni à l'origine ni dans la copie HTML (espace insécable probable) : la valeur a été relue dans le PDF conservé par A04, non recontrôlé à l'origine |

Limite : pour l'avis du HCFP, « l'origine » est une archive web, le site du HCFP étant injoignable d'ici. Pour la Cour des comptes, c'est la copie hébergée par vie-publique.fr.

## 2. Téléchargements indépendants concordants entre agents

Quatre pièces ont été téléchargées séparément par deux ou trois agents, sans coordination ; leurs empreintes sont identiques : prévisions d'automne 2026 de la Commission (A01, A03, A07) ; rapport de la Cour de juillet 2024 (A03 via l'archive web, A04 via vie-publique.fr) ; rapport annuel 2026 du COR (A01, A06) ; rapport d'information de l'Assemblée n° 2689 de 2010 (A03, A04).

## 3. Ce que ce contrôle ne couvre pas

- Les autres pièces relues dans une copie locale sans retéléchargement : projet de loi de finances 2027 (texte n° 3210), projet de collectif de 2000 (n° 2335), rapports du Sénat n° 371 et n° 168, audit de 1997, rapport Bozio-Wasmer, note de l'IPP n° 32, évaluation des voies et moyens du budget 2026, document n° 7 du COR d'octobre 2025, rapport de la Cour de février 2025, projet annuel de performances du programme 117, classeur Insee en base 2005 issu de l'archive web. Statut : **relues dans la copie de l'agent**.
- Taux à 10 ans d'octobre 2026 : la valeur d'A07 (série de la BCE) a été recoupée avec un fichier Eurostat téléchargé par A03. Les deux séries dérivent des mêmes données de la BCE : c'est un **second téléchargement**, pas un second fournisseur.

## 4. Traçabilité fichier par fichier

Contrôle des manifestes (chaque fichier de `sources\` a-t-il une ligne donnant son adresse d'origine ?) :

| Dossier | Manifeste | Pièces avec adresse d'origine au manifeste | Sans adresse au manifeste |
|---|---|---|---|
| A03 | oui | 34 | 5 |
| A05 | oui | 29 | 7 |
| A07 | oui | 56 | 11 |
| A10 | journal de téléchargement indexé par identifiant court, non par nom de fichier | 8 rapprochées automatiquement | 52 à rapprocher à la main |
| A01, A02, A04, A06 | **aucun manifeste** | 0 | 30, 39, 26, 36 |

Pour A01, A02, A04 et A06, les adresses d'origine figurent dans le texte des dossiers (section 17 ou tableau des faits), souvent sans `https://`, mais pas dans un manifeste fichier par fichier. **Conséquence** : la contre-expertise peut remonter à l'origine, mais à la main. Le manifeste est devenu obligatoire dans les consignes communes (version 1.1) pour les agents suivants ; la mise en conformité des dossiers de la vague 1 reste à faire.

## 5. Intégrité des fichiers d'agents

- En relançant le script `drees_test_principe_mesure.py` d'A10 pour le vérifier, l'orchestrateur a réécrit son fichier de sortie `drees_test_principe_mesure.csv`. Le contenu avant et après relance n'a pas été comparé ; le script étant déterministe sur des microdonnées inchangées, une différence est improbable mais n'est pas exclue. Les relances se font désormais sur une copie.
- Aucun agent de la vague 1 ne cite le chemin du dossier de l'équipe Codex dans ses fichiers ou ses scripts (recherche faite sur `agents\` et `scripts\`).
