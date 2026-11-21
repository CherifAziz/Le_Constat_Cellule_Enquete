# A18 - croissance du PIB en volume : Insee BDM 010565708 (trimestriel, base 2014, série arrêtée) et Eurostat nama_10_gdp CLV_PCH_PRE (base actuelle)
# Usage : python -I a18_09_pib_volume.py <insee_bdm_010565708.xml> <eurostat_nama_gdp_volume_FR_SE.json>
import re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
t = open(sys.argv[1], encoding="utf-8").read()
obs = re.findall(r'TIME_PERIOD="(\d{4})-Q(\d)" OBS_VALUE="([0-9.]+)"', t)
an = {}
for y, q, v in obs: an.setdefault(int(y), []).append(float(v))
an = {y: sum(v) for y, v in an.items() if len(v) == 4}
g = {y: 100 * (an[y] / an[y - 1] - 1) for y in an if y - 1 in an}
print("Insee base 2014 (série arrêtée) : croissance annuelle 1974 %.2f ; 1975 %.2f" % (g[1974], g[1975]))
for a, b in [(1960, 1974), (1975, 1985)]:
    n = b - a + 1
    print(f"moyenne géométrique {a}-{b} : {100 * ((an[b] / an[a - 1]) ** (1 / n) - 1):.2f} %")
j = json.load(open(sys.argv[2], encoding="utf-8"))
ti = j["dimension"]["time"]["category"]["index"]; gi = j["dimension"]["geo"]["category"]["index"]
nt = len(ti); invt = {v: k for k, v in ti.items()}; invg = {v: k for k, v in gi.items()}
val = {(invg[int(k) // nt], int(invt[int(k) % nt])): v for k, v in j["value"].items()}
for c in ["FR", "SE"]:
    print(c, {y: val.get((c, y)) for y in [1975, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 2000, 2009, 2020, 2025] if (c, y) in val})
fr = {y: v for (c, y), v in val.items() if c == "FR"}
for a, b in [(1975, 1985), (1975, 2025)]:
    gm = 1
    for y in range(a, b + 1): gm *= 1 + fr[y] / 100
    print(f"Eurostat FR moyenne géométrique {a}-{b} : {100 * (gm ** (1 / (b - a + 1)) - 1):.2f} %")
