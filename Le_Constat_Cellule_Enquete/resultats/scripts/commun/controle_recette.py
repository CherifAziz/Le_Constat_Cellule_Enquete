# -*- coding: utf-8 -*-
"""
Controle de recette mecanique des dossiers d'agents (orchestrateur).
Ne juge pas le fond : verifie l'existence, la structure imposee par
missions/00_CONSIGNES_COMMUNES.md (17 titres), les etiquettes de provenance,
les identifiants, les fiches annuelles (A02, A03) et les fichiers livres.

Usage : python controle_recette.py A01 A02 ...   (sans argument : tous les Axx.md presents)
Sortie : tableau sur la sortie standard + resultats/journal/recette_<horodatage>.md
"""
import datetime as dt
import glob
import os
import re
import sys

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TITRES = [
    "1. Question, hypothèses rivales et critères d'invalidation",
    "2. Définitions et périmètres",
    "3. Tableau des faits",
    "4. Chronologie",
    "5. Données et calculs",
    "6. Chaînes causales et contre-exemples",
    "7. Objections fortes et meilleures réponses",
    "8. Échelles",
    "9. Qui gagne, qui paie, qui peut bloquer",
    "10. Mesures et solutions",
    "11. Résultats potentiellement décisifs",
    "12. Contradictions relevées",
    "13. Ce que je n'ai pas pu établir",
    "14. Ce qui pourrait renverser ma conclusion",
    "15. Angle mort découvert",
    "16. Transmissions aux autres agents",
    "17. Références exactes et journal de recherche",
]
FICHES = {"A02": range(1974, 2001), "A03": range(2001, 2027)}
CHAMPS_FICHE = ["PIB", "Inflation", "Dépenses", "intérêts", "Dette", "sous-secteur", "Exécutif", "Lois de finances", "Contexte", "convention", "Lecture causale"]


def normaliser(s):
    return re.sub(r"[\s’'`]+", " ", s.lower()).strip()


def lire(chemin):
    with open(chemin, encoding="utf-8", errors="replace") as f:
        return f.read()


def sections(texte):
    """Decoupe en sections de niveau 2 : {titre: corps}."""
    morceaux = re.split(r"(?m)^##\s+(?!#)(.+?)\s*$", texte)
    out = {}
    for i in range(1, len(morceaux), 2):
        out[morceaux[i].strip()] = morceaux[i + 1]
    return out


def controler(agent):
    lignes = []
    principal = os.path.join(R, "agents", f"{agent}.md")
    if not os.path.exists(principal):
        return [f"### {agent}\n\n**ABSENT** : {principal} n'existe pas.\n"], False
    texte = lire(principal)
    annexes = sorted(glob.glob(os.path.join(R, "agents", f"{agent}_annexe_*.md")))
    tout = texte + "".join(lire(a) for a in annexes)
    sec = sections(texte)
    sec_norm = {normaliser(k): v for k, v in sec.items()}
    ok = True
    lignes.append(f"### {agent}\n")
    lignes.append(f"- Dossier principal : {len(texte):,} caractères ; {len(annexes)} annexe(s) : " + ", ".join(f"{os.path.basename(a)} ({os.path.getsize(a):,} o)" for a in annexes))
    manquants, maigres = [], []
    for t in TITRES:
        cle = normaliser(t)
        trouve = [k for k in sec_norm if k.startswith(cle[: max(12, len(cle) - 4)]) or cle in k]
        if not trouve:
            manquants.append(t)
        else:
            corps = sec_norm[trouve[0]].strip()
            if len(corps) < 200:
                maigres.append(f"{t} ({len(corps)} car.)")
    if manquants:
        ok = False
        lignes.append("- **Titres obligatoires manquants** : " + " ; ".join(manquants))
    else:
        lignes.append("- 17 titres obligatoires présents")
    if maigres:
        lignes.append("- Sections de moins de 200 caractères (à lire : justifiées ou vides ?) : " + " ; ".join(maigres))
    if len(maigres) > 3:
        ok = False
        lignes.append(f"- **{len(maigres)} sections quasi vides** : dossier encore à l'état de squelette ou inachevé")
    prov = {e: len(re.findall(r"\[" + e + r"\]", tout)) for e in "CSMX"}
    lignes.append(f"- Étiquettes de provenance : [C] {prov['C']} ; [S] {prov['S']} ; [M] {prov['M']} ; [X] {prov['X']}")
    if prov["C"] == 0:
        ok = False
        lignes.append("- **Aucune pièce marquée consultée [C]**")
    ids = {p: len(set(re.findall(p + r"-" + agent + r"-\d+", tout))) for p in "FHCP"}
    lignes.append(f"- Identifiants distincts : F {ids['F']} ; H {ids['H']} ; C {ids['C']} ; P {ids['P']}")
    urls = set(re.findall(r"https?://[^\s)\]>|\"']+", tout))
    lignes.append(f"- URL distinctes citées : {len(urls)}")
    nb_indispo = len(re.findall(r"(?i)indisponible", tout))
    nb_nonverif = len(re.findall(r"(?i)non vérifié", tout))
    lignes.append(f"- Mentions « indisponible » : {nb_indispo} ; « non vérifié » : {nb_nonverif}")
    if agent in FICHES:
        ann = "".join(lire(a) for a in annexes)
        blocs = re.split(r"(?m)^#{2,4}\s+(?:Fiche\s+)?((?:19|20)\d\d)\b.*$", ann)
        fiches = {}
        for i in range(1, len(blocs), 2):
            fiches.setdefault(int(blocs[i]), blocs[i + 1])
        attendues = list(FICHES[agent])
        absentes = [a for a in attendues if a not in fiches]
        incompletes = []
        for a in attendues:
            if a in fiches:
                manq = [c for c in CHAMPS_FICHE if c.lower() not in fiches[a].lower()]
                if manq:
                    incompletes.append(f"{a} (sans : {', '.join(manq)})")
        lignes.append(f"- Fiches annuelles : {len(attendues) - len(absentes)} sur {len(attendues)} présentes")
        if absentes:
            ok = False
            lignes.append("- **Fiches absentes** : " + ", ".join(map(str, absentes)))
        if incompletes:
            lignes.append("- Fiches où un champ du gabarit n'apparaît pas : " + " ; ".join(incompletes))
    for sous in ("donnees", "scripts"):
        d = os.path.join(R, sous, agent)
        n, taille = 0, 0
        for racine, _, fichiers in os.walk(d):
            for f in fichiers:
                n += 1
                taille += os.path.getsize(os.path.join(racine, f))
        lignes.append(f"- `{sous}\\{agent}\\` : {n} fichier(s), {taille:,} octets")
    lignes.append(f"- **Verdict mécanique** : {'structure conforme (le fond reste à contrôler)' if ok else 'NON CONFORME'}\n")
    return lignes, ok


def main():
    agents = sys.argv[1:] or sorted({os.path.basename(p)[:3] for p in glob.glob(os.path.join(R, "agents", "A??.md"))})
    horo = dt.datetime.now().strftime("%Y-%m-%d_%Hh%M")
    sortie = [f"# Contrôle de recette mécanique — {horo}\n", "Ce contrôle ne juge pas le fond. Il précède la relecture et le sondage des citations par l'orchestrateur.\n"]
    for a in agents:
        l, _ = controler(a)
        sortie.extend(l)
    texte = "\n".join(sortie)
    os.makedirs(os.path.join(R, "journal"), exist_ok=True)
    chemin = os.path.join(R, "journal", f"recette_{horo}.md")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    sys.stdout.reconfigure(encoding="utf-8")
    print(texte)
    print(f"\n-> {chemin}")


if __name__ == "__main__":
    main()
