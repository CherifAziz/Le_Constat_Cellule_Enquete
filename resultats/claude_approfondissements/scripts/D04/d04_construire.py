"""D04 : construit les tables finales a partir des saisies manuelles.
- ajoute pct_PIB (PIB base 2020, Insee, copie de la table A04) ;
- convertit les francs en euros (1 EUR = 6,55957 F) ;
- pour les bascules, exprime aussi chaque montant en points de salaires bruts (D11, copie de la table D08)
  et place a cote les variations du taux apparent calculees par D08 (aucune soustraction).
Entrees : ../../donnees/D04/*_saisie.csv, ../../donnees/D04/sources/a04_po_recettes_1959_2025.csv,
          ../../donnees/D04/sources/D08_cotisations_par_salaire_copie.csv
Sorties : ../../donnees/D04/D04_cotisations_1975_1991.csv, D04_grandes_decisions.csv,
          D04_allegements_1993_2025.csv, D04_bascules.csv"""
import os, csv
ICI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(ICI, '..', '..', 'donnees', 'D04')
F_PAR_EUR = 6.55957

def lire(nom, dossier=D):
    with open(os.path.join(dossier, nom), encoding='utf-8-sig', newline='') as h:
        return list(csv.DictReader(h, delimiter=';'))

def ecrire(nom, lignes, champs):
    with open(os.path.join(D, nom), 'w', encoding='utf-8', newline='') as h:
        w = csv.DictWriter(h, fieldnames=champs, delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(lignes)

PIB = {int(r['annee']): float(r['PIB_implicite_Md_EUR']) for r in lire('a04_po_recettes_1959_2025.csv', os.path.join(D, 'sources')) if r['PIB_implicite_Md_EUR']}
_d08 = lire('D08_cotisations_par_salaire_copie.csv', os.path.join(D, 'sources'))
D11 = {int(r['annee']): float(r['salaires_bruts_D11_MdEUR']) for r in _d08}
TAUX = {int(r['annee']): float(r['taux_apparent_cotisations_sur_salaires_pct']) for r in _d08}
DEBUT = {'1993-2000': 1993, '2017-2019': 2017}

def en_md_eur(x, unite):
    u = unite.replace(' ', '').upper()
    if u in ('MDF',):
        return x / F_PAR_EUR
    if u in ('MF',):
        return x / 1000 / F_PAR_EUR
    if u in ('MDEUR', 'MD€'):
        return x
    if u in ('MEUR', 'M€'):
        return x / 1000
    raise ValueError(unite)

def pct(x, annee, base):
    return '' if annee not in base else f"{100 * x / base[annee]:.3f}".replace('.', ',')

# 1. Cotisations 1975-1991
cot = lire('D04_cotisations_1975_1991_saisie.csv')
for r in cot:
    try:
        x = float(r['montant_num']); a = int(r['annee_du_montant'][:4])
        r['montant_MdEUR'] = f"{en_md_eur(x, 'MdF'):.3f}".replace('.', ',')
        r['pct_PIB'] = pct(en_md_eur(x, 'MdF'), a, PIB)
    except (ValueError, KeyError):
        r['montant_MdEUR'] = r['pct_PIB'] = ''
champs = list(cot[0].keys())
ecrire('D04_cotisations_1975_1991.csv', cot, champs)

# 2. Grandes decisions (ordre des colonnes de D05 d'abord)
ORDRE_D05 = ['annee', 'texte', 'date', 'mesure', 'type', 'impot', 'montant', 'unite', 'annee_du_montant',
             'ex_ante_ou_ex_post', 'brut_ou_net', 'perimetre', 'temporaire_ou_permanent', 'pct_PIB',
             'encore_en_vigueur_2025', 'beneficiaires_ou_payeurs', 'source_incidence', 'source', 'page', 'marque']
gd = lire('D04_grandes_decisions_saisie.csv')
for r in gd:
    try:
        x = float(r['montant_num']); a = int(r['annee_du_montant'][:4])
        r['pct_PIB'] = pct(en_md_eur(x, r['unite_num']), a, PIB)
    except (ValueError, KeyError):
        r['pct_PIB'] = ''
suite = ['citation', 'niveau', 'id_D04', 'id_S01', 'lien_D04_cotisations', 'lien_D05', 'montant_num', 'unite_num']
ecrire('D04_grandes_decisions.csv', gd, ORDRE_D05 + suite)

# 3. Allegements
al = lire('D04_allegements_1993_2025_saisie.csv')
for r in al:
    try:
        x = float(r['montant_num']); a = int(r['annee'])
        m = en_md_eur(x, r['unite'])
        r['montant_MdEUR'] = f"{m:.3f}".replace('.', ',')
        r['pct_PIB'] = pct(m, a, PIB)
        r['pct_salaires_bruts_D11'] = pct(m, a, D11)
    except (ValueError, KeyError):
        r['montant_MdEUR'] = r['pct_PIB'] = r['pct_salaires_bruts_D11'] = ''
champs = ['annee', 'dispositifs', 'montant', 'unite', 'montant_MdEUR', 'pct_PIB', 'pct_salaires_bruts_D11', 'champ',
          'statut', 'compensation', 'mode_compensation', 'source', 'page_pdf', 'page_imprimee', 'citation', 'marque',
          'rupture_de_serie']
ecrire('D04_allegements_1993_2025.csv', al, champs)

# 4. Bascules, a cote des variations calculees par D08 (convention : comptes nationaux, ex post)
D08_REPERES = {'1993-2000': 'taux apparent 50,32 -> 42,69 % des salaires bruts (-7,63 points) ; -2,81 points de PIB (D08)',
               '2017-2019': 'taux apparent 44,68 -> 39,59 % des salaires bruts (-5,09 points) ; -1,96 point de PIB (D08)',
               'avant 1993': 'hors des deux periodes de D08'}
ba = lire('D04_bascules_saisie.csv')
for r in ba:
    x = float(r['montant_num']); a = int(r['annee'])
    m = en_md_eur(x, r['unite'])
    r['montant_MdEUR'] = f"{m:.3f}".replace('.', ',')
    r['pct_PIB'] = pct(m, a, PIB)
    r['pct_salaires_bruts_D11'] = pct(m, a, D11)
    r['repere_D08_meme_periode'] = D08_REPERES.get(r['periode_D08'], '')
    # pas annuel et cumul depuis le debut de periode du taux apparent de D08 (points de salaires bruts), a cote
    r['D08_pas_annuel_points'] = r['D08_cumul_depuis_debut_points'] = ''
    if a in TAUX and a - 1 in TAUX:
        r['D08_pas_annuel_points'] = f"{TAUX[a] - TAUX[a - 1]:.2f}".replace('.', ',')
    if r['periode_D08'] in DEBUT and a in TAUX:
        r['D08_cumul_depuis_debut_points'] = f"{TAUX[a] - TAUX[DEBUT[r['periode_D08']]]:.2f}".replace('.', ',')
champs = ['id', 'periode_D08', 'annee', 'operation', 'classe', 'montant_num', 'unite', 'montant_MdEUR', 'pct_PIB',
          'pct_salaires_bruts_D11', 'sens_pour_les_cotisations', 'ex_ante_ou_ex_post', 'champ', 'repere_D08_meme_periode',
          'D08_pas_annuel_points', 'D08_cumul_depuis_debut_points',
          'source', 'page_pdf', 'page_imprimee', 'citation', 'marque']
ecrire('D04_bascules.csv', ba, champs)

for nom in ('D04_cotisations_1975_1991.csv', 'D04_grandes_decisions.csv', 'D04_allegements_1993_2025.csv', 'D04_bascules.csv'):
    with open(os.path.join(D, nom), encoding='utf-8') as h:
        print(nom, sum(1 for _ in h) - 1, 'lignes')
