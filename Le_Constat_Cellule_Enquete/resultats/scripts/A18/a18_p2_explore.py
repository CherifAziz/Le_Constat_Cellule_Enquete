# -*- coding: utf-8 -*-
"""A18 partie 2 - exploration : annees disponibles pour les interets (Eurostat, FR) et contenu des tableaux Insee t_32xx."""
import json, os, openpyxl
D = r"C:\Users\oussa\Downloads\Le_Constat_Cellule_Enquete\Le_Constat_Cellule_Enquete\resultats\donnees"
def js(p):
    j = json.load(open(p, encoding="utf-8"))
    dims = j["id"]; size = j["size"]
    idx = {d: {v: k for k, v in j["dimension"][d]["category"]["index"].items()} for d in dims}
    out = {}
    for flat, val in j["value"].items():
        flat = int(flat); key = []
        for d, s in zip(reversed(dims), reversed(size)):
            key.append(idx[d][flat % s]); flat //= s
        out[tuple(reversed(key))] = val
    return dims, out
dims, v = js(os.path.join(D, "A18", "sources", "p2", "eurostat_gov_10a_main_FR_D41_TE_TR_B9_1978_2025.json"))
print(dims)
for it in ("D41PAY", "TE", "B9"):
    ys = sorted(k[-1] for k in v if k[dims.index("na_item")] == it and k[dims.index("unit")] == "PC_GDP")
    print(it, ys[:3], "...", ys[-2:], len(ys))
dims, v = js(os.path.join(D, "A18", "sources", "p2", "eurostat_nama_10_gdp_FR_EA20_B1GQ.json"))
print(dims, sorted(set(k[dims.index("unit")] for k in v)))
for f in ("insee_cn_t_3201.xlsx", "insee_cn_t_3202.xlsx", "insee_cn_t_3203.xlsx", "insee_ip2106_compte_apu_2025.xlsx"):
    wb = openpyxl.load_workbook(os.path.join(D, "commun", f), read_only=True, data_only=True)
    for ws in wb.worksheets[:2]:
        rows = list(ws.iter_rows(min_row=1, max_row=60, values_only=True))
        print("==", f, ws.title, ws.max_row, ws.max_column)
        for r in rows[:60]:
            if r and r[0]:
                print("   ", str(r[0])[:70], "|", [x for x in r[1:4]], "...", [x for x in r[-2:]])
