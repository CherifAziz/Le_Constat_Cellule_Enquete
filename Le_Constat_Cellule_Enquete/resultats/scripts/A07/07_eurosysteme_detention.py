# -*- coding: utf-8 -*-
"""A07 - Achats nets cumules de titres publics francais par l'Eurosysteme (PSPP + PEPP), BCE.
Usage : python -I 07_eurosysteme_detention.py <dossier A07>
Sources : sources/ecb_PSPP_breakdown_history.csv (achats nets mensuels, M EUR, valeur comptable/cout amorti, mars 2015-oct. 2026)
          sources/ecb_PEPP_public_sector_breakdown_history.csv (achats nets mensuels, M EUR, mars 2020-...)
Remarque : les montants PSPP couvrent les titres d'emetteurs francais (Etat, CADES, Unedic, collectivites, agences) ;
le PSPP/PEPP inclut aussi les achats de la BCE elle-meme (non residente au sens de la BdF) et les supranationaux sont a part.
Sortie : eurosysteme_FR_cumul_mensuel.csv
"""
import sys, os, csv, datetime
A07 = sys.argv[1]; SRC = os.path.join(A07, "sources")

def read_first_block(path, country="France"):
    rows = list(csv.reader(open(path, encoding="utf-8-sig")))
    hdr = rows[2]
    for r in rows[3:]:
        if r and r[0] == country:
            vals = {}
            for h, v in zip(hdr[1:], r[1:]):
                if not h or "cumulative" in h.lower():
                    continue
                try:
                    vals[h] = float(v.replace(",", "")) if v not in ("", None) else 0.0
                except ValueError:
                    pass
            return vals
    raise KeyError(country)

def to_ym(h):
    for fmt in ("%d/%m/%Y", "%b-%y"):
        try:
            d = datetime.datetime.strptime(h, fmt); return f"{d.year}-{d.month:02d}"
        except ValueError:
            pass
    return None

pspp = {to_ym(k): v for k, v in read_first_block(os.path.join(SRC, "ecb_PSPP_breakdown_history.csv")).items() if to_ym(k)}
pepp = {to_ym(k): v for k, v in read_first_block(os.path.join(SRC, "ecb_PEPP_public_sector_breakdown_history.csv")).items() if to_ym(k)}
months = sorted(set(pspp) | set(pepp))
cp = ce = 0.0
out = []
for m in months:
    cp += pspp.get(m, 0.0); ce += pepp.get(m, 0.0)
    out.append((m, round(cp / 1000, 1), round(ce / 1000, 1), round((cp + ce) / 1000, 1)))
with open(os.path.join(A07, "eurosysteme_FR_cumul_mensuel.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";"); w.writerow(["mois", "PSPP_cumul_mdeur", "PEPP_cumul_mdeur", "total_mdeur"]); w.writerows(out)
peak = max(out, key=lambda x: x[3])
print("pic", peak)
for m in ["2015-12", "2016-12", "2018-12", "2019-12", "2020-12", "2021-12", "2022-06", "2022-12", "2023-12", "2024-12", "2025-12", "2026-06", "2026-09", "2026-10"]:
    print([x for x in out if x[0] == m])
print("dernier mois PEPP :", max(pepp))
