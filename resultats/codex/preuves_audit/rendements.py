"""Prix Euronext MOTX des deux titres le 13 novembre 2026 et rendement actuariel brut."""
from calendar import monthrange
import csv
from datetime import date
from io import StringIO
from pathlib import Path

BASE = Path(__file__).resolve().parent
SETTLEMENT = date(2026, 11, 17)  # Mardi, deux jours de bourse après le vendredi 13.


def minus_months(day, count):
    absolute = day.year * 12 + day.month - 1 - count
    year, idx = divmod(absolute, 12)
    month = idx + 1
    return date(year, month, min(day.day, monthrange(year, month)[1]))


def effective_yield(clean, coupon, maturity, frequency):
    """Coupons fixes, ACT/ACT ICMA, remboursement au pair, rendement annuel effectif."""
    next_coupon = maturity
    payments = 1
    months = 12 // frequency
    while minus_months(next_coupon, months) > SETTLEMENT:
        next_coupon = minus_months(next_coupon, months)
        payments += 1
    previous = minus_months(next_coupon, months)
    remaining = (next_coupon - SETTLEMENT) / (next_coupon - previous)
    per_period = coupon / frequency
    dirty = clean + per_period * (1 - remaining)
    lo, hi = 0.0, 0.2
    for _ in range(70):
        mid = (lo + hi) / 2
        present = sum(per_period / (1 + mid)**((remaining + j) / frequency)
                      for j in range(payments))
        present += 100 / (1 + mid)**((remaining + payments - 1) / frequency)
        if present > dirty:
            lo = mid
        else:
            hi = mid
    return 100 * (lo + hi) / 2


for name, filename, coupon, maturity, frequency in (
    ("FR0014018YR0", "oat_MOTX.csv", 3.7, date(2036, 11, 25), 1),
    ("IT0005729931", "btp_13nov.csv", 4.0, date(2036, 10, 1), 2),
):
    lines = (BASE/filename).read_text(encoding="utf-8-sig").splitlines()
    daily = csv.DictReader(StringIO("\n".join(lines[3:])), delimiter=";")
    record = next(row for row in daily if row["Date"] == "13/11/2026")
    for field in ("Low","High","Close"):
        price = float(record[field])
        print(name, field, price, f"{effective_yield(price,coupon,maturity,frequency):.4f} %")
