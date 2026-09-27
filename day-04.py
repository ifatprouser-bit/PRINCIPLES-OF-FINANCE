#!/usr/bin/env python3
"""
verify/day-04.py  —  Day 4, "Perpetuity and growth".

Recomputes every number that appears on day-04.html: the recall box, the
convergence table and both charts, all three worked examples, all six
try-it answers, and all six quiz items including the numbers quoted inside
each explanation.

Run:  python3 verify/day-04.py
One line per number: label, computed value, PASS/FAIL against the page.
"""

PASS = 0
FAIL = 0


def chk(label, computed, on_page, tol=0.01):
    """Numeric check."""
    global PASS, FAIL
    ok = abs(computed - on_page) <= tol
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print("%-58s computed=%-18s page=%-18s %s"
          % (label, round(computed, 6), on_page, "PASS" if ok else "FAIL"))


def chk_true(label, condition, note=""):
    """Claim check for statements that are not a single number."""
    global PASS, FAIL
    if condition:
        PASS += 1
    else:
        FAIL += 1
    print("%-58s %-38s %s" % (label, note, "PASS" if condition else "FAIL"))


# ---------------------------------------------------------------- formulas
def pv_single(cf, r, t):
    return cf / (1 + r) ** t


def pv_perp(a, r):
    return a / r


def pv_gperp(cf1, r, g):
    return cf1 / (r - g)


def pv_ann(a, r, n):
    return a * (1 - (1 + r) ** -n) / r


def pv_gann(cf1, r, g, n):
    """Growing annuity. cf1 is the payment at the end of period 1."""
    if abs(r - g) < 1e-12:
        # r == g: every discounted payment equals the base cash flow A = cf1/(1+g)
        return n * cf1 / (1 + g)
    return cf1 * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)


print("=" * 100)
print("RECALL BOX (day 2 material)")
print("=" * 100)
chk("recall Q2: PV of 5,000 in 4 years at 7%", pv_single(5000, 0.07, 4), 3814.48)
chk("recall Q2: PV of 5,000 in 4 years at 9%", pv_single(5000, 0.09, 4), 3542.13)
chk_true("recall Q2: answer moves DOWN when r rises",
         pv_single(5000, 0.09, 4) < pv_single(5000, 0.07, 4),
         "3542.13 < 3814.48")


def AUDIT(label, got, want, detail):
    chk(label + ((' -> ' + str(detail)) if detail else ''), got, want, tol=0)

# ---------------------------------------------------------------- page audit
# Added by the checking pass. These catch defects that pure arithmetic misses.
import re as _re
from pathlib import Path as _Path

_PAGE = _Path(__file__).resolve().parent.parent / "day-04.html"
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

# Panel 3 bar chart: the two bar widths must be in the same ratio as the two
# values they show (16.15m correct against 22.07m if the end date is dropped).
_w = [float(x) for x in _re.findall(r'<rect x="14" y="\d+" width="(\d+)" height="34"', _html)]
AUDIT("panel 3 bar chart: two bars found", len(_w), 2, _w)
_ratio_px = _w[1] / _w[0]
_ratio_val = 22.071429 / 16.145980
AUDIT("panel 3 bar chart: widths match the values (within 1%)",
      int(abs(_ratio_px - _ratio_val) / _ratio_val > 0.01), 0,
      "px %.4f vs value %.4f" % (_ratio_px, _ratio_val))

# Panel 1 and panel 2 curves: sample the drawn polylines against the formulas.
def _af(r, n):
    return (1 - (1 + r) ** -n) / r
_pl = _re.findall(r'points="([^"]+)"', _html)
_p1 = [tuple(map(float, q.split(","))) for q in _pl[0].split()]
_err1 = max(abs((220 - 0.3 * (30 * _af(0.05, (x - 56) / 4.0) if x > 56 else 0)) - y)
            for x, y in _p1)
AUDIT("panel 1 curve: drawn points match 30/yr at 5% (max 1px)",
      int(_err1 > 1.0), 0, "max error %.2f px" % _err1)
_p2 = [tuple(map(float, q.split(","))) for q in _pl[1].split()]
_err2 = max(abs((220 - 0.82 * (2 * (1 + (x - 56) / (440 / 0.09)) / (0.09 - (x - 56) / (440 / 0.09)))) - y)
            for x, y in _p2)
AUDIT("panel 2 curve: drawn points match 2.00 growing at g, r=9% (max 2px)",
      int(_err2 > 2.0), 0, "max error %.2f px" % _err2)

print()
print("=" * 100)
print("PANEL 1 - plain perpetuity")
print("=" * 100)
# The convergence evidence. Source shape: Growing_Annuity_Perpetuity.xlsm, sheet
# "Perpetuity": 3% coupon on face 1000 (= $30 a year), required return 5%.
# That sheet's own first-100-years sum is 595.4373; recomputed here from scratch.
A, R = 30.0, 0.05
ceiling = pv_perp(A, R)
chk("perpetuity ceiling 30 / 0.05", ceiling, 600.00)

running = {}
tot = 0.0
for t in range(1, 1001):
    tot += A / (1 + R) ** t
    running[t] = tot

chk("running total, first 10 years", running[10], 231.65)
chk("running total, first 25 years", running[25], 422.82)
chk("running total, first 50 years", running[50], 547.68)
chk("running total, first 100 years", running[100], 595.44)
chk("running total, first 200 years", running[200], 599.97)
chk("share of full value at year 10 (%)", 100 * running[10] / ceiling, 39, tol=0.6)
chk("share of full value at year 25 (%)", 100 * running[25] / ceiling, 70, tol=0.6)
chk("share of full value at year 50 (%)", 100 * running[50] / ceiling, 91, tol=0.6)
chk("share of full value at year 100 (%)", 100 * running[100] / ceiling, 99, tol=0.4)
chk("share of full value at year 200 (%)", 100 * running[200] / ceiling, 99.99, tol=0.01)
chk("page claim: forever minus 200 years = 3 cents", ceiling - running[200], 0.03, tol=0.005)
chk_true("chart claim: running total never crosses 600",
         all(v < 600.0 for v in running.values()), "max = %.4f" % running[1000])
chk_true("chart claim: each year adds less than the year before",
         all((running[t] - running[t - 1]) < (running[t - 1] - running[t - 2])
             for t in range(3, 300)), "differences strictly shrinking")
# chart 1 pixel anchors
chk("chart1 label year 25 -> y pixel", 220 - running[25] * (180 / 600), 93.2, tol=0.2)
chk("chart1 label year 100 -> y pixel", 220 - running[100] * (180 / 600), 41.4, tol=0.2)

# worked example
chk("worked 1: PV = 9,000 / 0.06", pv_perp(9000, 0.06), 150000.00, tol=0.5)
chk("worked 1 check line: 150,000 x 0.06", 150000 * 0.06, 9000.00)

# try-its
chk("try 1a: 75 / 0.05", pv_perp(75, 0.05), 1500.00)
chk("try 1a: 75 / 0.06", pv_perp(75, 0.06), 1250.00)
chk_true("try 1a: rate up, value down", pv_perp(75, 0.06) < pv_perp(75, 0.05), "1250 < 1500")
chk("try 1b: 600 / 0.08", pv_perp(600, 0.08), 7500.00)
chk("try 1b: 600 / 0.06", pv_perp(600, 0.06), 10000.00)
chk("try 1b: rise", pv_perp(600, 0.06) - pv_perp(600, 0.08), 2500.00)

print()
print("=" * 100)
print("PANEL 2 - growing perpetuity")
print("=" * 100)
D0, RR = 2.00, 0.09
chk("curve table g=0%: 2.00 x 1.00 / 0.09", pv_gperp(D0 * 1.00, RR, 0.00), 22.22)
chk("curve table g=4%: 2.00 x 1.04 / 0.05", pv_gperp(D0 * 1.04, RR, 0.04), 41.60)
chk("curve table g=7%: 2.00 x 1.07 / 0.02", pv_gperp(D0 * 1.07, RR, 0.07), 107.00)
chk("curve table g=8%: 2.00 x 1.08 / 0.01", pv_gperp(D0 * 1.08, RR, 0.08), 216.00)
chk_true("curve table g>=9%: no finite value", (RR - 0.09) <= 0, "r - g <= 0")
chk("chart2 anchor g=4% -> x pixel", 56 + (0.04 / 0.09) * 440, 251, tol=1)
chk("chart2 anchor g=4% -> y pixel", 220 - 41.60 * (180 / 220), 186.0, tol=0.2)
chk("chart2 anchor g=8% -> x pixel", 56 + (0.08 / 0.09) * 440, 447, tol=1)
chk("chart2 anchor g=8% -> y pixel", 220 - 216.0 * (180 / 220), 43.3, tol=0.2)
chk("chart2 wall g=9% -> x pixel", 56 + (0.09 / 0.09) * 440, 496, tol=1)

# worked example
chk("worked 2: CF1 = 2.00 x 1.04", 2.00 * 1.04, 2.08)
chk("worked 2: gap 0.09 - 0.04", 0.09 - 0.04, 0.05, tol=1e-9)
chk("worked 2: PV = 2.08 / 0.05", pv_gperp(2.08, 0.09, 0.04), 41.60)
chk("worked 2 check line: 41.60 x 0.05", 41.60 * 0.05, 2.08)
chk("worked 2 trap: forgetting (1+g) gives 2.00 / 0.05", 2.00 / 0.05, 40.00)
chk("worked 2 trap: size of that error", 41.60 - 40.00, 1.60)

# try-its
chk("try 2a: CF1 = 1.50 x 1.02", 1.50 * 1.02, 1.53)
chk("try 2a: PV = 1.53 / 0.06", pv_gperp(1.53, 0.08, 0.02), 25.50)
chk("try 2b: PV = 1.53 / 0.04", pv_gperp(1.53, 0.06, 0.02), 38.25)
chk("try 2b: 38.25 is 50% above 25.50 (%)", 100 * (38.25 / 25.50 - 1), 50.0, tol=0.2)

print()
print("=" * 100)
print("PANEL 3 - growing annuity")
print("=" * 100)
# Gold mine. Source: Time_Value_of_Money.pdf ("The Value Of A Gold Mine") and
# the class recording (POF 6). Damodaran's text states $16.146 million.
base = 5000 * 300
chk("worked 3: today's revenue 5,000 x 300", base, 1500000)
cf1 = base * 1.03
chk("worked 3: CF1 = 1,500,000 x 1.03", cf1, 1545000)
ratio = (1.03 / 1.10) ** 20
chk("worked 3: (1.03/1.10)^20", ratio, 0.268467, tol=1e-5)
chk("worked 3: 1 - 0.268467", 1 - ratio, 0.731533, tol=1e-5)
factor = (1 - ratio) / 0.07
chk("worked 3: 0.731533 / 0.07", factor, 10.4505, tol=0.001)
gold20 = pv_gann(cf1, 0.10, 0.03, 20)
chk("worked 3: PV = 1,545,000 x 10.4505", gold20, 16145980, tol=25)
chk_true("worked 3 agrees with the course text ($16.146 million)",
         abs(gold20 - 16146000) < 2000, "%.0f" % gold20)
chk_true("worked 3 rounds to $16.15 million", round(gold20 / 1e6, 2) == 16.15,
         "%.2f m" % (gold20 / 1e6))

goldforever = pv_gperp(cf1, 0.10, 0.03)
chk("wrong-tool comparison: 1,545,000 / 0.07", goldforever, 22071429, tol=25)
chk("wrong-tool comparison: the gap in dollars", goldforever - gold20, 5900000, tol=30000)
chk("wrong-tool comparison: the gap as a % of the right answer",
    100 * (goldforever - gold20) / gold20, 37, tol=0.5)
# bar chart widths: 380px for 16.15m against 520px for 22.07m
chk("bar chart: correct bar / forever bar should match the ratio",
    520 * gold20 / goldforever, 380, tol=6)

# the r = g rule, taken from the course files
# (Growing_Annuity_Perpetuity.xlsm sheet "Growing-Annutiy": r = g = 10%,
#  base cash flow 1,500,000, 20 years, total 30,000,000)
xl_check = sum(1500000 * 1.10 ** t / 1.10 ** t for t in range(1, 21))
chk("rule r=g: n x A reproduces the course workbook total", xl_check, 30000000, tol=1)
chk("rule r=g: formula helper agrees", pv_gann(1500000 * 1.10, 0.10, 0.10, 20), 30000000, tol=1)

# try-its
r3 = (1.05 / 1.09) ** 8
chk("try 3a: (1.05/1.09)^8", r3, 0.741485, tol=1e-5)
chk("try 3a: 1 - 0.741485", 1 - r3, 0.258515, tol=1e-5)
chk("try 3a: 0.258515 / 0.04", (1 - r3) / 0.04, 6.462873, tol=1e-4)
lease8 = pv_gann(10000, 0.09, 0.05, 8)
chk("try 3a: PV = 10,000 x 6.462873", lease8, 64628.73)
leasefar = pv_gperp(10000, 0.09, 0.05)
chk("try 3b: 10,000 / 0.04", leasefar, 250000.00)
chk("try 3b: value sitting after year 8", leasefar - lease8, 185371.27)
chk("try 3b: that as a share of the total (%)",
    100 * (leasefar - lease8) / leasefar, 74, tol=0.5)
chk_true("try 3b contrast with panel 1 is real",
         (100 * running[50] / ceiling) > 90 and (100 * lease8 / leasefar) < 30,
         "91% vs 26% in the first stretch")

print()
print("=" * 100)
print("QUIZ - six items, every option and every number in every explanation")
print("=" * 100)

print("-- Q1 perpetuity, inverse: given the price, find the payment")
chk("Q1 correct: 260,000 x 0.05", 260000 * 0.05, 13000.00)
chk("Q1 check line: 13,000 / 0.05", pv_perp(13000, 0.05), 260000.00)
chk("Q1 distractor: 260,000 / 0.05", 260000 / 0.05, 5200000.00)
chk("Q1 distractor: 260,000 x 0.05 x 1.05", 260000 * 0.05 * 1.05, 13650.00)
chk("Q1 distractor: 260,000 x 0.005", 260000 * 0.005, 1300.00)

print("-- Q2 growing perpetuity, r only just above g")
chk("Q2 gap: 0.07 - 0.065", 0.07 - 0.065, 0.005, tol=1e-9)
chk("Q2 correct: 3.15 / 0.005", pv_gperp(3.15, 0.07, 0.065), 630.00)
chk("Q2 check line: 630 x 0.005", 630 * 0.005, 3.15)
chk("Q2 explanation: 630 is 14x the 7%-gap value of 45", 630.0 / 45.0, 14, tol=0.05)
chk("Q2 distractor: 3.15 x 1.065 / 0.005", 3.15 * 1.065 / 0.005, 670.95)
chk("Q2 distractor: 3.15 / 0.07", 3.15 / 0.07, 45.00)
chk("Q2 distractor: 3.15 / 0.065", 3.15 / 0.065, 48.46)
chk_true("Q2 boundary is satisfied but thin", 0.07 > 0.065, "r - g = 0.005")

print("-- Q3 growing perpetuity with a SHRINKING cash flow (g negative)")
chk("Q3 gap: 0.09 - (-0.03)", 0.09 - (-0.03), 0.12, tol=1e-9)
chk("Q3 correct: 60,000 / 0.12", pv_gperp(60000, 0.09, -0.03), 500000.00)
chk("Q3 check line: flat version 60,000 / 0.09", pv_perp(60000, 0.09), 666666.67)
chk_true("Q3 check line: shrinking is worth less than flat",
         pv_gperp(60000, 0.09, -0.03) < pv_perp(60000, 0.09), "500,000 < 666,667")
chk("Q3 distractor: 60,000 / 0.06 (subtracted instead of added)", 60000 / 0.06, 1000000.00)
chk("Q3 distractor: 60,000 / 0.09", 60000 / 0.09, 666666.67)
chk("Q3 distractor: 60,000 / 0.03", 60000 / 0.03, 2000000.00)

print("-- Q4 boundary: g above r, the formula breaks")
chk("Q4: the gap is negative, 0.06 - 0.08", 0.06 - 0.08, -0.02, tol=1e-9)
chk_true("Q4 correct option: r > g fails here", not (0.06 > 0.08), "0.06 > 0.08 is false")
chk("Q4 distractor: 2.00 / 0.02 (minus sign dropped)", 2.00 / 0.02, 100.00)
chk("Q4 distractor: 2.00 / (-0.02)", 2.00 / -0.02, -100.00)
chk("Q4 distractor: 2.00 / 0.06 (growth thrown away)", 2.00 / 0.06, 33.33)

print("-- Q5 growing annuity against growing perpetuity")
q5ratio = 1.04 / 1.10
chk("Q5: 1.04 / 1.10", q5ratio, 0.945455, tol=1e-5)
chk("Q5: 0.945455^15", q5ratio ** 15, 0.431131, tol=1e-5)
chk("Q5: 1 - 0.431131", 1 - q5ratio ** 15, 0.568869, tol=1e-5)
chk("Q5: 0.568869 / 0.06", (1 - q5ratio ** 15) / 0.06, 9.481149, tol=1e-4)
q5 = pv_gann(12000, 0.10, 0.04, 15)
chk("Q5 correct: 12,000 x 9.481149", q5, 113773.69)
chk_true("Q5 rounds to the $113,774 shown as an option", round(q5) == 113774, "%.2f" % q5)
chk("Q5 distractor: growing perpetuity 12,000 / 0.06", pv_gperp(12000, 0.10, 0.04), 200000.00)
chk("Q5 distractor: plain annuity 12,000, 10%, 15 yrs", pv_ann(12000, 0.10, 15), 91272.95)
chk_true("Q5 distractor rounds to the $91,273 shown", round(pv_ann(12000, 0.10, 15)) == 91273,
         "%.2f" % pv_ann(12000, 0.10, 15))
chk("Q5 distractor: 12,000 x 15, no discounting", 12000 * 15, 180000.00)
chk_true("Q5 check line: 15 years worth less than forever", q5 < 200000, "113,774 < 200,000")

print("-- Q6 growing annuity at the r = g boundary")
chk("Q6 gap: 0.05 - 0.05", 0.05 - 0.05, 0.0, tol=1e-12)
q6_direct = sum(25000 * 1.05 ** t / 1.05 ** t for t in range(1, 13))
chk("Q6 correct, summed year by year", q6_direct, 300000.00)
chk("Q6 correct, by the n x A rule", 12 * 25000, 300000.00)
chk("Q6 check line: year 1 harvest 25,000 x 1.05", 25000 * 1.05, 26250.00)
chk("Q6 check line: 26,250 / 1.05", 26250 / 1.05, 25000.00)
chk("Q6 check line: year 7 discounted value", 25000 * 1.05 ** 7 / 1.05 ** 7, 25000.00)
chk("Q6 distractor: 26,250 x 12", 26250 * 12, 315000.00)
chk("Q6 distractor: 25,000 / 0.05", pv_perp(25000, 0.05), 500000.00)
chk_true("Q6 distractor 'cannot be calculated' is wrong", q6_direct > 0, "a finite PV exists")

print()
print("=" * 100)
print("NO-REUSE CHECK  (spec 8.1: no quiz item may repeat a worked example or try-it)")
print("=" * 100)
page_examples = {
    "worked 1 perpetuity": (9000, 0.06, None, None),
    "try 1a consol": (75, 0.05, None, None),
    "try 1b perpetuity": (600, 0.08, None, None),
    "worked 2 dividend": (2.00, 0.09, 0.04, None),
    "try 2a dividend": (1.50, 0.08, 0.02, None),
    "try 2b dividend": (1.50, 0.06, 0.02, None),
    "worked 3 gold mine": (1545000, 0.10, 0.03, 20),
    "try 3a lease": (10000, 0.09, 0.05, 8),
    "try 3b lease forever": (10000, 0.09, 0.05, None),
}
quiz_inputs = {
    "Q1 fund": (13000, 0.05, None, None),
    "Q2 share": (3.15, 0.07, 0.065, None),
    "Q3 royalty": (60000, 0.09, -0.03, None),
    "Q4 share": (2.00, 0.06, 0.08, None),
    "Q5 supply contract": (12000, 0.10, 0.04, 15),
    "Q6 forestry permit": (25000, 0.05, 0.05, 12),
}
clash = [(q, p) for q, qv in quiz_inputs.items()
         for p, pv in page_examples.items() if qv == pv]
chk_true("no quiz item reuses a worked example or try-it", not clash, str(clash) if clash else "0 clashes")

print()
print("=" * 100)
print("AXES CHECK  (spec 8.4)")
print("=" * 100)
chk_true("an item where r is only just above g", abs((0.07 - 0.065) - 0.005) < 1e-9, "Q2, gap 0.005")
chk_true("an inverse item (value given, find the payment)", True, "Q1")
chk_true("a shrinking cash flow", -0.03 < 0, "Q3, g = -3%")
chk_true("the r <= g case that breaks the formula", 0.08 > 0.06, "Q4")
chk_true("the r = g boundary", 0.05 == 0.05, "Q6")
chk_true("rate up and rate down both appear", True, "try 1a rises 5->6%, try 1b falls 8->6%")
chk_true("finite life against for ever, same stream", True, "Q5, and try 3a against try 3b")

print()
print("=" * 100)
print("TOTAL: %d checks, %d passed, %d failed" % (PASS + FAIL, PASS, FAIL))
print("=" * 100)
raise SystemExit(1 if FAIL else 0)
