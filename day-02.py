#!/usr/bin/env python3
"""
Verify every number printed on day-02.html (A single cash flow).

Each line prints: label, computed value, and PASS/FAIL against the number the
page claims. Nothing on the page is taken on trust, including the figures that
came from the course files.
"""

import math

CHECKS = []


def chk(label, computed, page_says, tol=0.005):
    ok = abs(computed - page_says) <= tol
    CHECKS.append(ok)
    print("%-52s computed=%-16s page=%-14s %s"
          % (label, round(computed, 6), page_says, "PASS" if ok else "FAIL"))


# ---------------------------------------------------------------- panel 1
# Worked example: 1,000 today against 1,080 in one year at 5%.
pv_b = 1080 / 1.05
chk("P1 WE  PV of 1,080 one year at 5%", pv_b, 1028.57)
chk("P1 WE  how much bigger than 1,000", pv_b - 1000, 28.57)
chk("P1 WE  check, 1,028.57 x 1.05", pv_b * 1.05, 1080.00)
# Try-it: the rate that makes the two offers equal.
chk("P1 try indifference rate (%)", (1080 / 1000 - 1) * 100, 8.00)

# ---------------------------------------------------------------- panel 2
# Table: what 100 paid on a future date is worth today.
TABLE = {
    (1, 0.04): 96.15, (1, 0.06): 94.34, (1, 0.08): 92.59,
    (3, 0.04): 88.90, (3, 0.06): 83.96, (3, 0.08): 79.38,
    (5, 0.04): 82.19, (5, 0.06): 74.73, (5, 0.08): 68.06,
    (10, 0.04): 67.56, (10, 0.06): 55.84, (10, 0.08): 46.32,
}
for (n, r), shown in sorted(TABLE.items()):
    chk("P2 table  100 in %2d years at %d%%" % (n, round(r * 100)),
        100 / (1 + r) ** n, shown)

# Worked example: Infosoft lease, 500,000 in ten years at 10%.
f10 = 1.10 ** 10
chk("P2 WE  growth factor 1.10^10", f10, 2.5937, tol=0.00005)
pv_infosoft = 500000 / f10
chk("P2 WE  PV of the 500,000 lease payment", pv_infosoft, 192771.64)
chk("P2 WE  rounded figure shown in the answer", round(pv_infosoft), 192772)
chk("P2 WE  check, PV x factor back to 500,000", pv_infosoft * f10, 500000.00)

# Try-it: 3-year government zero at 2%. The course file asks this and gives no answer.
f3 = 1.02 ** 3
chk("P2 try1 growth factor 1.02^3", f3, 1.061208, tol=5e-7)
p3y = 100 / f3
chk("P2 try1 price of the 3-year zero at 2%", p3y, 94.23)
chk("P2 try1 check, price x factor", p3y * f3, 100.00)

# Try-it: 6-year zero, rate falls from 8% to 5%.
f8 = 1.08 ** 6
f5 = 1.05 ** 6
chk("P2 try2 growth factor 1.08^6", f8, 1.586874, tol=5e-7)
chk("P2 try2 growth factor 1.05^6", f5, 1.340096, tol=5e-7)
chk("P2 try2 price at 8%", 100 / f8, 63.02)
chk("P2 try2 price at 5%", 100 / f5, 74.62)
chk("P2 try2 rise in price", 100 / f5 - 100 / f8, 11.60)

# ---------------------------------------------------------------- panel 3
# Worked example: 2,000 for 45 years at 9%.
f45 = 1.09 ** 45
chk("P3 WE  growth factor 1.09^45", f45, 48.3273, tol=0.00005)
fv_ira = 2000 * f45
chk("P3 WE  FV of the 2,000 deposit", fv_ira, 96654.57)
chk("P3 WE  rounded figure shown in the answer", round(fv_ira), 96655)
chk("P3 WE  check, FV / factor back to 2,000", fv_ira / f45, 2000.00)
chk("P3 WE  simple interest for contrast", 2000 * (1 + 0.09 * 45), 10100.00)

# Try-it: 27,000 grows to 200,000 in 18 years. Course file sets it up, no answer given.
ratio = 200000 / 27000
chk("P3 try1 ratio 200,000 / 27,000", ratio, 7.4074, tol=0.00005)
one_plus_r = ratio ** (1 / 18)
chk("P3 try1 (1 + r) as a factor", one_plus_r, 1.117673, tol=5e-7)
chk("P3 try1 required annual rate (%)", (one_plus_r - 1) * 100, 11.77)
chk("P3 try1 check, 27,000 x factor^18", 27000 * one_plus_r ** 18, 200000.00)

# Try-it: two-year zero priced at 90, face 100.
r2 = (100 / 90) ** 0.5 - 1
chk("P3 try2 annual effective rate (%)", r2 * 100, 5.41)
chk("P3 try2 value after one year", 90 * (1 + r2), 94.87)
chk("P3 try2 check, value after two years", 90 * (1 + r2) ** 2, 100.00)
chk("P3 try2 trap, total return over 2 years (%)", (100 / 90 - 1) * 100, 11.11)
chk("P3 try2 trap, half of that total (%)", (100 / 90 - 1) * 100 / 2, 5.56)

# ---------------------------------------------------------------- quiz
# Q1  PV of 40,000 due in 4 years at 7%.
q1f = 1.07 ** 4
chk("Q1 growth factor 1.07^4", q1f, 1.310796, tol=5e-7)
chk("Q1 correct answer, PV", 40000 / q1f, 30515.81)
chk("Q1 correct answer as shown", round(40000 / q1f), 30516)
chk("Q1 check, PV x factor", (40000 / q1f) * q1f, 40000.00)
chk("Q1 distractor, multiplied instead", round(40000 * q1f), 52432)
chk("Q1 distractor, N = 3", round(40000 / 1.07 ** 3), 32652)
chk("Q1 distractor, simple interest", 40000 / (1 + 0.07 * 4), 31250.00)

# Q2  FV of 6,500 at 5.5% for 12 years.
q2f = 1.055 ** 12
chk("Q2 growth factor 1.055^12", q2f, 1.901207, tol=5e-7)
chk("Q2 correct answer, FV", 6500 * q2f, 12357.85)
chk("Q2 correct answer as shown", round(6500 * q2f), 12358)
chk("Q2 check, FV / factor", (6500 * q2f) / q2f, 6500.00)
chk("Q2 distractor, simple interest", 6500 * (1 + 0.055 * 12), 10790.00)
chk("Q2 distractor, N = 11", round(6500 * 1.055 ** 11), 11714)
chk("Q2 distractor, divided instead", round(6500 / q2f), 3419)

# Q3  zero-coupon bond, 850 today, 1,000 in 5 years.
q3ratio = 1000 / 850
chk("Q3 ratio 1,000 / 850", q3ratio, 1.176471, tol=5e-7)
q3root = q3ratio ** 0.2
chk("Q3 fifth root of the ratio", q3root, 1.033038, tol=5e-7)
chk("Q3 correct answer, annual rate (%)", (q3root - 1) * 100, 3.30)
chk("Q3 check, 850 x factor^5", 850 * q3root ** 5, 1000.00)
chk("Q3 distractor, total return (%)", (q3ratio - 1) * 100, 17.65)
chk("Q3 distractor, total divided by 5 (%)", (q3ratio - 1) * 100 / 5, 3.53)
chk("Q3 distractor, gain over face value (%)", (1000 - 850) / 1000 * 100, 15.00)

# Q4  9,000 due in 6 years, rate rises 4% to 7%.
q4f4 = 1.04 ** 6
q4f7 = 1.07 ** 6
chk("Q4 growth factor 1.04^6", q4f4, 1.265319, tol=5e-7)
chk("Q4 growth factor 1.07^6", q4f7, 1.500730, tol=5e-7)
chk("Q4 value at 4%", 9000 / q4f4, 7112.83)
chk("Q4 value at 7%", 9000 / q4f7, 5997.08)
chk("Q4 correct answer, size of the fall", 9000 / q4f4 - 9000 / q4f7, 1115.75)
chk("Q4 correct answer as shown", round(9000 / q4f4 - 9000 / q4f7), 1116)
chk("Q4 check, value at 7% x factor", (9000 / q4f7) * q4f7, 9000.00)
chk("Q4 distractor, rate gap once on payment", 9000 * (0.07 - 0.04), 270.00)
# direction check: a higher rate must give a smaller present value
dir_ok = (9000 / q4f7) < (9000 / q4f4)
CHECKS.append(dir_ok)
print("%-52s computed=%-16s page=%-14s %s"
      % ("Q4 direction, higher rate gives lower PV", dir_ok, "a fall",
         "PASS" if dir_ok else "FAIL"))

# Q5  3,000 today plus 3,000 at end of year 2 at 8%.
q5f = 1.08 ** 2
chk("Q5 growth factor 1.08^2", q5f, 1.1664, tol=5e-5)
chk("Q5 PV of the year 2 payment", 3000 / q5f, 2572.02)
chk("Q5 correct answer, whole promise today", 3000 + 3000 / q5f, 5572.02)
chk("Q5 check, 2,572.02 x factor", (3000 / q5f) * q5f, 3000.00)
chk("Q5 distractor, raw sum with no discounting", 3000 + 3000, 6000.00)
chk("Q5 distractor, today's cash discounted too",
    round(3000 / 1.08 + 3000 / q5f), 5350)

# Q6  4,000 at 8%, first whole year it reaches 8,000.
chk("Q6 factor 1.08^9", 1.08 ** 9, 1.999005, tol=5e-7)
chk("Q6 value after 9 years", 4000 * 1.08 ** 9, 7996.02)
chk("Q6 shortfall after 9 years", 8000 - 4000 * 1.08 ** 9, 3.98)
chk("Q6 factor 1.08^10", 1.08 ** 10, 2.158925, tol=5e-7)
chk("Q6 value after 10 years", 4000 * 1.08 ** 10, 8635.70)
first_year = next(n for n in range(1, 60) if 4000 * 1.08 ** n >= 8000)
chk("Q6 correct answer, first whole year at 8,000", first_year, 10, tol=0)
chk("Q6 distractor, rule of 72", 72 / 8, 9.00)
chk("Q6 distractor, continuous compounding", math.log(2) / 0.08, 8.7, tol=0.05)
chk("Q6 distractor, simple interest", 4000 / (4000 * 0.08), 12.5)



def AUDIT(label, got, want, detail):
    chk(label + ((' -> ' + str(detail)) if detail else ''), got, want, tol=0)

# ---------------------------------------------------------------- page audit
# Added by the checking pass. These catch defects that pure arithmetic misses.
import re as _re
from pathlib import Path as _Path

_PAGE = _Path(__file__).resolve().parent.parent / "day-02.html"
_html = _PAGE.read_text(encoding="utf-8")

# The quiz engine SHUFFLES the options at render time (assets/study.js,
# shuffled(item)), so an explanation that names an option by its position is
# wrong for the reader. Every distractor must be named by its content or value.
_POSITIONAL = _re.compile(
    r"\b(?:the\s+)?(?:first|second|third|fourth|last|final)\s+"
    r"(?:option|answer|choice)\b|\bthe\s+(?:second|third|fourth|last)\s+fails\b",
    _re.I)
_hits = _POSITIONAL.findall(_html)
AUDIT("exp: no option referred to by its position (engine shuffles)",
      len(_hits), 0, _hits)

# The em dash is banned in learner-facing copy (BUILD-SPEC section 9).
AUDIT("copy: no em dash or en dash",
      len(_re.findall(r"[–—]|&[mn]dash;", _html)), 0, None)

# Engine contract: mount id must exist, and data-scorechip must match it.
_mount = _re.search(r'mount:\s*"([^"]+)"', _html).group(1)
AUDIT("engine: mount div id=\"%s\" exists" % _mount,
      int('id="%s"' % _mount in _html), 1, None)
AUDIT("engine: data-scorechip matches the mount id",
      int('data-scorechip="%s"' % _mount in _html), 1, None)

# Only the nine tags in BUILD-SPEC section 7 are allowed.
_ALLOWED = {"Concepts", "Single cash flow", "Annuity", "Perpetuity",
            "Mixed stream", "Bonds", "Payoff structure", "Stocks",
            "NPV and IRR"}
_bad = [t for t in _re.findall(r'tag:\s*"([^"]+)"', _html) if t not in _ALLOWED]
AUDIT("engine: every quiz tag is one of the nine allowed", len(_bad), 0, _bad)

# Mobile: any table with five or more columns must sit inside .tscroll.
_unwrapped = []
for _m in _re.finditer(r"<table[^>]*>(.*?)</table>", _html, _re.S):
    _rows = _re.findall(r"<tr[^>]*>(.*?)</tr>", _m.group(0), _re.S)
    _cols = max(len(_re.findall(r"<t[hd]", _r)) for _r in _rows)
    if _cols >= 5 and "tscroll" not in _html[max(0, _m.start() - 200):_m.start()]:
        _unwrapped.append(_cols)
AUDIT("mobile: every 5+ column table is wrapped in .tscroll",
      len(_unwrapped), 0, _unwrapped)

# Panel 1 timeline: the four year ticks must be evenly spaced. Unequal gaps
# draw year 3 as if it were closer than year 2, which the picture must not say.
_ticks = sorted(int(x) for x in _re.findall(
    r'<line x1="(\d+)" y1="112" x2="\d+" y2="128"/>', _html))
_gaps = [_ticks[i + 1] - _ticks[i] for i in range(len(_ticks) - 1)]
AUDIT("panel 1 timeline: four year ticks", len(_ticks), 4, _ticks)
AUDIT("panel 1 timeline: year ticks evenly spaced",
      max(_gaps) - min(_gaps), 0, _gaps)


# ---------------------------------------------------------------- summary
print()
print("%d numbers checked, %d passed, %d failed"
      % (len(CHECKS), sum(CHECKS), len(CHECKS) - sum(CHECKS)))
raise SystemExit(0 if all(CHECKS) else 1)
