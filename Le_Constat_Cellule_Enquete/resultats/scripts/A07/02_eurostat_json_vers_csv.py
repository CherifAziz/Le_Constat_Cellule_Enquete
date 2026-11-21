# -*- coding: utf-8 -*-
"""Convertit un fichier JSON-stat Eurostat en CSV long (une ligne par observation), sans retraitement.
Usage : python -I 02_eurostat_json_vers_csv.py fichier.json [fichier2.json ...]
"""
import sys, json, csv, itertools

def convert(path):
    d = json.load(open(path, encoding="utf-8"))
    ids, sizes = d["id"], d["size"]
    labels = []
    for dim in ids:
        idx = d["dimension"][dim]["category"]["index"]
        inv = sorted(idx.items(), key=lambda kv: kv[1])
        labels.append([k for k, _ in inv])
    vals, stat = d.get("value", {}), d.get("status", {})
    out = path[:-5] + ".csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(ids + ["value", "status"])
        n = 0
        for flat, combo in enumerate(itertools.product(*labels)):
            k = str(flat)
            if k in vals:
                w.writerow(list(combo) + [vals[k], stat.get(k, "")])
                n += 1
    print(out, n, "obs ; updated =", d.get("updated"))

for p in sys.argv[1:]:
    convert(p)
