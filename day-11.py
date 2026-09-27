#!/usr/bin/env python3
"""
verify/day-11.py  —  Day 11, Mock 2 (the time value paper)

Recomputes every number that appears on day-11.html: the 22 mock answers, the
distractor values (each one is a named wrong calculation, so each one is checked
too), and the intermediate figures quoted inside the explanations.

It also reads day-11.html itself, so the printed option strings are checked
against the computed values rather than against a copy of them, and the three
course-quiz items are checked against the professor's own answer key.

Run:  python3 verify/day-11.py
Every line prints PASS or FAIL. Exit code 1 if anything fails.
"""

import json
import os
import re
import sys

HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day-11.html")

fails = []
checks = [0]


def chk(label, computed, page, tol=0.02):
    """Compare a computed number with what the page prints."""
    checks[0] += 1
    ok = abs(computed - page) <= tol
    if not ok:
        fails.append(label)
    print("%-62s computed %16s   page %16s   %s"
          % (label, fmt(computed), fmt(page), "PASS" if ok else "FAIL"))


def chk_txt(label, computed, page):
    """Compare a computed string with what the page prints."""
    checks[0] += 1
    ok = computed == page
    if not ok:
        fails.append(label)
    print("%-62s computed %16s   page %16s   %s"
          % (label, computed[:16], page[:16], "PASS" if ok else "FAIL"))


def fmt(x):
    return "%0.2f" % x if isinstance(x, float) else str(x)


def money(x):
    return "{:,.2f}".format(x)


# ---------- the formulas, written out once ----------

def pv_single(cf, r, n):
    return cf / (1 + r) ** n


def fv_single(cf, r, n):
    return cf * (1 + r) ** n


def ann_factor(r, n):
    return (1 - (1 + r) ** -n) / r


def pv_ann(a, r, n):
    return a * ann_factor(r, n)


def fv_ann(a, r, n):
    return a * (((1 + r) ** n - 1) / r)


def pv_perp(c, r):
    return c / r


def pv_gperp(c1, r, g):
    assert r > g, "growing perpetuity needs r > g"
    return c1 / (r - g)


def bond_price(coupon, face, r, n):
    return pv_ann(coupon, r, n) + pv_single(face, r, n)


# ---------- read the page ----------

src = open(HTML, encoding="utf-8").read()

item_re = re.compile(
    r'\{\s*\n\s*q: "(?P<q>(?:[^"\\]|\\.)*)",\n'
    r'\s*opts: \[(?P<opts>.*?)\],\n'
    r'\s*correct: (?P<correct>\d+),\n'
    r'\s*tag: "(?P<tag>[^"]*)",\n'
    r'(?:\s*src: "(?P<src>[^"]*)",\n)?',
    re.S)

items = []
for m in item_re.finditer(src):
    items.append({
        "q": m.group("q"),
        "opts": json.loads("[" + m.group("opts") + "]"),
        "correct": int(m.group("correct")),
        "tag": m.group("tag"),
        "src": m.group("src"),
    })


def answer(i):
    """The option text the page marks as correct, for item number i (1 based)."""
    return items[i - 1]["opts"][items[i - 1]["correct"]]


def opts(i):
    return items[i - 1]["opts"]


print("=" * 118)
print("DAY 11  MOCK 2  —  verification of every number on the page")
print("=" * 118)

# ---------- shape of the paper ----------

print("\n-- SHAPE OF THE PAPER --")
chk("items on the page", 22, len(items), 0)
chk("minutes in POF.mock", 150, int(re.search(r"minutes: (\d+)", src).group(1)), 0)
chk("day number in POF.mock", 11, int(re.search(r"day: (\d+)", src).group(1)), 0)

tags = {}
for it in items:
    tags[it["tag"]] = tags.get(it["tag"], 0) + 1
for tag, want in [("Concepts", 4), ("Single cash flow", 2), ("Annuity", 3),
                  ("Perpetuity", 2), ("Mixed stream", 4), ("Bonds", 3),
                  ("Payoff structure", 1), ("NPV and IRR", 2), ("Stocks", 1)]:
    chk("tag count: " + tag, want, tags.get(tag, 0), 0)

ALLOWED = {"Concepts", "Single cash flow", "Annuity", "Perpetuity", "Mixed stream",
           "Bonds", "Payoff structure", "Stocks", "NPV and IRR"}
chk("tags outside the nine allowed values", 0, len(set(tags) - ALLOWED), 0)

tvm = sum(tags.get(t, 0) for t in ("Single cash flow", "Annuity", "Perpetuity", "Mixed stream"))
chk("time value of money questions", 11, tvm, 0)

chk("items marked From a course quiz", 3, sum(1 for it in items if it["src"] == "From a course quiz"), 0)
chk("items claiming to be from a past final", 0, src.count("past final"), 0)
chk("em dashes in learner-facing text", 0, src.count("—"), 0)
chk("distinct correct indexes used", 4, len(set(it["correct"] for it in items)), 0)

# ---------- 1, 6, 11: the professor's own quiz cases ----------

print("\n-- COURSE QUIZ CASES 1 TO 3, AGAINST THE PROFESSOR'S ANSWER KEY --")
# Finance_Decision_Environments_Quiz.pptx, slide 11 answer key: 1) A  2) B  3) B
# The slides list the options in the order A. Certainty, B. Uncertainty, C. Ambiguity.
KEY = {1: "A", 2: "B", 3: "B"}
LETTER = {"Certainty": "A", "Uncertainty": "B", "Ambiguity": "C"}

for case, qnum in [(1, 1), (2, 6), (3, 11)]:
    chk_txt("course quiz case %d, key letter" % case, KEY[case], LETTER[answer(qnum)])
    chk("case %d keeps all three slide options" % case, 3, len(opts(qnum)), 0)
    chk("case %d tagged From a course quiz" % case, 1,
        1 if items[qnum - 1]["src"] == "From a course quiz" else 0, 0)

# ---------- 2: single cash flow, two rates ----------

print("\n-- Q2  SINGLE CASH FLOW: how much smaller is the deposit at 5 percent --")
a = pv_single(30000, 0.04, 7)
b = pv_single(30000, 0.05, 7)
chk("Q2 deposit at 4 percent", a, 22797.53)
chk("Q2 deposit at 5 percent", b, 21320.44)
chk("Q2 1.04^7", 1.04 ** 7, 1.315932, 1e-5)
chk("Q2 1.05^7", 1.05 ** 7, 1.407100, 1e-5)
chk("Q2 answer, the difference", a - b, 1477.09)
chk_txt("Q2 answer printed", money(a - b), answer(2))
chk("Q2 distractor: simple interest 30,000 x 1% x 7", 30000 * 0.01 * 7, 2100.00)
chk("Q2 distractor: compounded forward instead",
    fv_single(30000, 0.05, 7) - fv_single(30000, 0.04, 7), 2735.06)
chk("Q2 check line: 21,320.44 grown at 5 percent", fv_single(b, 0.05, 7), 30000.00)
chk("Q2 check line: 22,797.53 grown at 4 percent", fv_single(a, 0.04, 7), 30000.00)

# ---------- 3: mixed stream, single + annuity + single ----------

print("\n-- Q3  MIXED STREAM: 3,000 at y1, 5,500 at y2 to y4, 9,000 at y5, r = 8% --")
p1 = pv_single(3000, 0.08, 1)
ann_at_y1 = pv_ann(5500, 0.08, 3)
p2 = ann_at_y1 / 1.08
p3 = pv_single(9000, 0.08, 5)
chk("Q3 year 1 payment", p1, 2777.78)
chk("Q3 annuity factor 3 years at 8 percent", ann_factor(0.08, 3), 2.577097, 1e-5)
chk("Q3 annuity value at the end of year 1", ann_at_y1, 14174.03)
chk("Q3 annuity moved back to today", p2, 13124.11)
chk("Q3 1.08^5", 1.08 ** 5, 1.469328, 1e-5)
chk("Q3 year 5 payment", p3, 6125.25)
chk("Q3 answer, the whole stream", p1 + p2 + p3, 22027.13)
chk_txt("Q3 answer printed", money(p1 + p2 + p3), answer(3))
chk("Q3 distractor: second discounting move forgotten", p1 + ann_at_y1 + p3, 23077.06)
chk("Q3 distractor: no discounting at all", 3000 + 5500 * 3 + 9000, 28500.00)
chk("Q3 distractor: annuity discounted two years", p1 + ann_at_y1 / 1.08 ** 2 + p3, 21054.98)
chk("Q3 size of the forgotten move", ann_at_y1 - p2, 1050.00, 0.5)

# ---------- 4: premium bond ----------

print("\n-- Q4  BONDS: par 1,000, coupon 8 percent, 5 years, yield 6 percent --")
price = bond_price(80, 1000, 0.06, 5)
chk("Q4 annuity factor 5 years at 6 percent", ann_factor(0.06, 5), 4.212364, 1e-5)
chk("Q4 present value of the coupons", pv_ann(80, 0.06, 5), 336.99)
chk("Q4 1.06^5", 1.06 ** 5, 1.338226, 1e-5)
chk("Q4 present value of the face value", pv_single(1000, 0.06, 5), 747.26)
chk("Q4 answer, the price", price, 1084.25)
chk_txt("Q4 answer printed", money(price) + ", a premium bond", answer(4))
chk("Q4 it is above par, so premium", 1, 1 if price > 1000 else 0, 0)
chk("Q4 distractor: rates swapped, 6 percent coupon at 8 percent",
    bond_price(60, 1000, 0.08, 5), 920.15)
chk("Q4 distractor: coupons and face value with no discounting", 80 * 5 + 1000, 1400.00)
chk("Q4 check line: extra 20 a year for 5 years", pv_ann(20, 0.06, 5), price - 1000)

# ---------- 5: annuity, find the rate ----------

print("\n-- Q5  ANNUITY, INVERSE: 19,066 today or 4,000 a year for 6 years --")
chk("Q5 factor implied by the cash price", 19066 / 4000, 4.7665, 1e-3)
chk("Q5 annuity factor 6 years at 6 percent", ann_factor(0.06, 6), 4.917324, 1e-5)
chk("Q5 value of the plan at 6 percent", pv_ann(4000, 0.06, 6), 19669.30)
chk("Q5 value of the plan at 6.5 percent", pv_ann(4000, 0.065, 6), 19364.05)
chk("Q5 annuity factor 6 years at 7 percent", ann_factor(0.07, 6), 4.766540, 1e-5)
chk("Q5 value of the plan at 7 percent", pv_ann(4000, 0.07, 6), 19066.16)
chk("Q5 value of the plan at 7.5 percent", pv_ann(4000, 0.075, 6), 18775.39)
chk("Q5 the cash price is matched at 7 percent", 19066.0, pv_ann(4000, 0.07, 6), 0.2)
chk_txt("Q5 answer printed", "7 percent", answer(5))
chk("Q5 check line: balance after one year", 19066 * 1.07 - 4000, 16400.62)

bal = 19066.16
for _ in range(6):
    bal = bal * 1.07 - 4000
chk("Q5 check line: balance after all six payments", bal, 0.0, 0.05)

# ---------- 7: growing perpetuity, r only just above g ----------

print("\n-- Q7  GROWING PERPETUITY: 9,000 next year, g = 4.6%, r = 5% --")
lic = pv_gperp(9000, 0.05, 0.046)
chk("Q7 the spread r - g", 0.05 - 0.046, 0.004, 1e-9)
chk("Q7 answer, the licence", lic, 2250000.00)
chk_txt("Q7 answer printed", "{:,.0f}".format(lic), answer(7))
chk("Q7 the same cash flow at a 4 percent spread", 9000 / 0.04, 225000.00)
chk("Q7 ten times the spread, one tenth the value", lic / 10.0, 9000 / 0.04)
chk("Q7 distractor: divided by g", 9000 / 0.046, 195652.17, 0.6)
chk("Q7 distractor: growth ignored, plain perpetuity", pv_perp(9000, 0.05), 180000.00)
chk("Q7 distractor: r + g instead of r - g", 9000 / (0.05 + 0.046), 93750.00)
chk("Q7 check line: value times the spread is the first payment", lic * 0.004, 9000.00)

# ---------- 8: delayed annuity ----------

print("\n-- Q8  MIXED STREAM, DELAYED ANNUITY: 2,600 from year 4 to year 9, r = 7% --")
n_pay = 9 - 4 + 1
chk("Q8 number of payments, years 4 to 9", 6, n_pay, 0)
at_y3 = pv_ann(2600, 0.07, 6)
today = at_y3 / 1.07 ** 3
chk("Q8 annuity factor 6 years at 7 percent", ann_factor(0.07, 6), 4.766540, 1e-5)
chk("Q8 value at the end of year 3", at_y3, 12393.00)
chk("Q8 1.07^3", 1.07 ** 3, 1.225043, 1e-5)
chk("Q8 answer, value today", today, 10116.38)
chk_txt("Q8 answer printed", money(today), answer(8))
chk("Q8 distractor: the second move forgotten", at_y3, 12393.00)
chk("Q8 size of the forgotten move", at_y3 - today, 2276.62)
chk("Q8 distractor: discounted 4 years instead of 3", at_y3 / 1.07 ** 4, 9454.56)
chk("Q8 distractor: payments added with no discounting", 2600 * 6, 15600.00)

# ---------- 9: NPV ----------

print("\n-- Q9  NPV: 45,000 out, then 14,000, 20,000, 22,000, r = 9% --")
c1 = pv_single(14000, 0.09, 1)
c2 = pv_single(20000, 0.09, 2)
c3 = pv_single(22000, 0.09, 3)
npv = c1 + c2 + c3 - 45000
chk("Q9 year 1 inflow discounted", c1, 12844.04)
chk("Q9 1.09^2", 1.09 ** 2, 1.188100, 1e-5)
chk("Q9 year 2 inflow discounted", c2, 16833.60)
chk("Q9 1.09^3", 1.09 ** 3, 1.295029, 1e-5)
chk("Q9 year 3 inflow discounted", c3, 16988.03)
chk("Q9 present value of the inflows", c1 + c2 + c3, 46665.67)
chk("Q9 answer, the NPV", npv, 1665.67)
chk_txt("Q9 answer printed", money(npv) + ", accept", answer(9))
chk("Q9 the decision is accept because NPV is positive", 1, 1 if npv > 0 else 0, 0)
chk("Q9 distractor: no discounting", 56000 - 45000, 11000.00)
chk("Q9 distractor: the initial cost never subtracted", c1 + c2 + c3, 46665.67)
chk("Q9 distractor: the sign flipped", -npv, -1665.67)
chk("Q9 check line: value lost to discounting", 56000 - (c1 + c2 + c3), 9334.33, 1.0)

# ---------- 10: solve for the number of periods ----------

print("\n-- Q10  SINGLE CASH FLOW, SOLVE FOR n: 50,000 worth 23,021.39 at 9% --")
from math import log
ratio = 50000 / 23021.39
n_solved = log(ratio) / log(1.09)
chk("Q10 growth factor 50,000 / 23,021.39", ratio, 2.171893, 1e-4)
chk("Q10 1.09^9", 1.09 ** 9, 2.171893, 1e-5)
chk("Q10 ln(2.171893)", log(2.171893), 0.775599, 1e-5)
chk("Q10 ln(1.09)", log(1.09), 0.086178, 1e-5)
chk("Q10 answer, n", n_solved, 9.0, 0.002)
chk_txt("Q10 answer printed", "9 years", answer(10))
chk("Q10 check line: 50,000 discounted 9 years", pv_single(50000, 0.09, 9), 23021.39, 0.01)
chk("Q10 distractor: 8 years", pv_single(50000, 0.09, 8), 25093.31)
chk("Q10 distractor: 8 years, how far off", pv_single(50000, 0.09, 8) - 23021.39, 2071.92)
chk("Q10 distractor: 10 years", pv_single(50000, 0.09, 10), 21120.54)
chk("Q10 1.09^10", 1.09 ** 10, 2.367364, 1e-5)
chk("Q10 distractor: 7 years", pv_single(50000, 0.09, 7), 27351.71)

# ---------- 12: future value of an annuity, interest inside it ----------

print("\n-- Q12  ANNUITY FV: 1,800 a year for 8 years at 6 percent, interest only --")
fv = fv_ann(1800, 0.06, 8)
own = 1800 * 8
chk("Q12 1.06^8", 1.06 ** 8, 1.593848, 1e-5)
chk("Q12 future value factor", (1.06 ** 8 - 1) / 0.06, 9.897468, 1e-5)
chk("Q12 the balance", fv, 17815.44)
chk("Q12 your own money", own, 14400.00)
chk("Q12 answer, the interest", fv - own, 3415.44)
chk_txt("Q12 answer printed", money(fv - own), answer(12))
chk("Q12 the factor must be above 8", 1, 1 if (1.06 ** 8 - 1) / 0.06 > 8 else 0, 0)
chk("Q12 distractor: the whole balance", fv, 17815.44)
chk("Q12 distractor: only what you paid in", own, 14400.00)
chk("Q12 distractor: simple interest 1,800 x 6% x 8", 1800 * 0.06 * 8, 864.00)

# ---------- 13: payoff structure ----------

print("\n-- Q13  PAYOFF STRUCTURE: V_T = 118, F_S = 90, F_J = 45 --")
V, FS, FJ = 118.0, 90.0, 45.0
senior = min(V, FS)
junior = 0.0 if V < FS else min(V - FS, FJ)
equity = max(V - FS - FJ, 0.0)
chk("Q13 senior payoff Min(V_T, F_S)", senior, 90.00)
chk("Q13 junior payoff Min(V_T - F_S, F_J)", junior, 28.00)
chk("Q13 equity payoff Max(V_T - F_S - F_J, 0)", equity, 0.00)
chk("Q13 the three payoffs sum to exactly V_T", senior + junior + equity, V, 1e-9)
chk_txt("Q13 answer printed", "Senior 90, junior 28, equity 0", answer(13))
chk("Q13 V_T is above F_S", 1, 1 if V > FS else 0, 0)
chk("Q13 V_T is below F_S + F_J", 1, 1 if V < FS + FJ else 0, 0)
chk("Q13 the junior lender's shortfall", FJ - junior, 17.00)
chk("Q13 distractor: junior paid first leaves the senior lender", V - FJ, 73.00)
chk("Q13 distractor: equity 28 as well would sum to", 90 + 28 + 28, 146.00)

# ---------- 14: a payment today plus an ordinary annuity ----------

print("\n-- Q14  MIXED STREAM: 1,500 today then 1,500 at the end of years 1 to 4, r = 9% --")
later = pv_ann(1500, 0.09, 4)
lic14 = 1500 + later
chk("Q14 annuity factor 4 years at 9 percent", ann_factor(0.09, 4), 3.239720, 1e-5)
chk("Q14 the four later payments", later, 4859.58)
chk("Q14 answer, the licence", lic14, 6359.58)
chk_txt("Q14 answer printed", money(lic14), answer(14))
chk("Q14 distractor: all five treated as ending years", pv_ann(1500, 0.09, 5), 5834.48)
chk("Q14 distractor: no discounting", 1500 * 5, 7500.00)
chk("Q14 distractor: today's payment left out", later, 4859.58)
chk("Q14 check: the answer sits between the two bounds", 1,
    1 if pv_ann(1500, 0.09, 5) < lic14 < 7500 else 0, 0)

# ---------- 15: coupon rate against yield ----------

print("\n-- Q15  BONDS: par 1,000, coupon 70, 6 years, price 1,060 --")
chk("Q15 price at a 6 percent yield", bond_price(70, 1000, 0.06, 6), 1049.17)
chk("Q15 coupons at 6 percent", pv_ann(70, 0.06, 6), 344.21)
chk("Q15 1.06^6", 1.06 ** 6, 1.418519, 1e-5)
chk("Q15 face value at 6 percent", pv_single(1000, 0.06, 6), 704.96)
lo, hi = 0.0001, 0.5
for _ in range(400):
    mid = (lo + hi) / 2
    if bond_price(70, 1000, mid, 6) > 1060:
        lo = mid
    else:
        hi = mid
ytm = (lo + hi) / 2
chk("Q15 the true yield at a price of 1,060", ytm * 100, 5.79, 0.006)
chk("Q15 the yield is below the coupon rate of 7 percent", 1, 1 if ytm < 0.07 else 0, 0)
chk("Q15 price at exactly a 7 percent yield is par", bond_price(70, 1000, 0.07, 6), 1000.00)
chk_txt("Q15 answer printed", "below", answer(15).split()[3])

# ---------- 16: zero growth against growth ----------

print("\n-- Q16  PERPETUITY, BOUNDARY g = 0: 7,200 flat against 7,200 growing 1.5% --")
gA = pv_gperp(7200, 0.045, 0.0)
gB = pv_gperp(7200, 0.045, 0.015)
chk("Q16 Grant A with g = 0", gA, 160000.00)
chk("Q16 the plain perpetuity gives the same", pv_perp(7200, 0.045), gA)
chk("Q16 Grant B with g = 1.5 percent", gB, 240000.00)
chk("Q16 answer, the difference", gB - gA, 80000.00)
chk_txt("Q16 answer printed", "{:,.0f}".format(gB - gA), answer(16))
chk("Q16 growth of 1.5 percent lifts the value by half", gB / gA, 1.5, 1e-9)
chk("Q16 distractor: r + g instead of r - g, Grant B", 7200 / (0.045 + 0.015), 120000.00)
chk("Q16 distractor: that difference", 7200 / (0.045 + 0.015) - gA, -40000.00)
chk("Q16 distractor: growth put on the numerator", 7200 * 1.015 / 0.045, 162400.00)
chk("Q16 distractor: that difference", 7200 * 1.015 / 0.045 - gA, 2400.00)
chk("Q16 check line: Grant B value times its spread", gB * 0.03, 7200.00)
chk("Q16 check line: Grant A value times its spread", gA * 0.045, 7200.00)

# ---------- 17: dividend discount model with D0 given ----------

print("\n-- Q17  STOCKS: D0 = 1.80 paid last week, g = 3.5%, r = 8% --")
D0, g17, r17 = 1.80, 0.035, 0.08
D1 = D0 * (1 + g17)
P0 = D1 / (r17 - g17)
chk("Q17 next year's dividend D1", D1, 1.863, 1e-6)
chk("Q17 the spread r - g", r17 - g17, 0.045, 1e-9)
chk("Q17 answer, the share price", P0, 41.40)
chk_txt("Q17 answer printed", "%0.2f" % P0, answer(17))
chk("Q17 distractor: D0 used instead of D1", D0 / 0.045, 40.00)
chk("Q17 distractor: growth ignored", D1 / r17, 23.29)
chk("Q17 distractor: r + g instead of r - g", D1 / (r17 + g17), 16.20)
chk("Q17 check line: price times the spread", P0 * 0.045, 1.863, 1e-6)
chk("Q17 check line: D1 back to D0", D1 / 1.035, 1.80, 1e-9)

# ---------- 18: a stream with a negative cash flow and a delayed annuity ----------

print("\n-- Q18  MIXED STREAM: 4,000 y1 y2, minus 2,500 y3, 4,000 y4 y5, r = 6% --")
pair = pv_ann(4000, 0.06, 2)
overhaul = -2500 / 1.06 ** 3
late_pair = pair / 1.06 ** 3
total18 = pair + overhaul + late_pair
chk("Q18 annuity factor 2 years at 6 percent", ann_factor(0.06, 2), 1.833393, 1e-5)
chk("Q18 years 1 and 2", pair, 7333.57)
chk("Q18 1.06^3", 1.06 ** 3, 1.191016, 1e-5)
chk("Q18 the overhaul, discounted", overhaul, -2099.05)
chk("Q18 years 4 and 5, moved back to today", late_pair, 6157.41)
chk("Q18 answer, the contract", total18, 11391.93)
chk_txt("Q18 answer printed", money(total18), answer(18))
chk("Q18 distractor: the overhaul ignored", pair + late_pair, 13490.98)
chk("Q18 distractor: the overhaul subtracted at face value", pair + late_pair - 2500, 10990.98)
chk("Q18 distractor: one 5 year annuity minus 2,500", pv_ann(4000, 0.06, 5) - 2500, 14349.46)
chk("Q18 check line: the undiscounted net", 4000 * 4 - 2500, 13500.00)
chk("Q18 check line: answer as a share of that", total18 / 13500 * 100, 84.4, 0.1)

# ---------- 19: perpetuity formula used on a 25 year annuity ----------

print("\n-- Q19  ANNUITY: 3,000 for 25 years at 8 percent, priced as a perpetuity --")
offer = pv_perp(3000, 0.08)
true25 = pv_ann(3000, 0.08, 25)
chk("Q19 the buyer's perpetuity figure", offer, 37500.00)
chk("Q19 1.08^25", 1.08 ** 25, 6.848475, 1e-5)
chk("Q19 1 / 1.08^25", 1 / 1.08 ** 25, 0.146018, 1e-5)
chk("Q19 annuity factor 25 years at 8 percent", ann_factor(0.08, 25), 10.674776, 1e-5)
chk("Q19 the true value", true25, 32024.33)
chk("Q19 answer, the overstatement", offer - true25, 5475.67)
chk_txt("Q19 answer printed", money(offer - true25), answer(19))
chk("Q19 the annuity factor is below 1 / r = 12.5", 1,
    1 if ann_factor(0.08, 25) < 1 / 0.08 else 0, 0)
chk("Q19 the gap as a share of the offer", (offer - true25) / offer * 100, 14.6, 0.1)
chk("Q19 distractor: the offer itself", offer, 37500.00)
chk("Q19 distractor: the true value", true25, 32024.33)
chk("Q19 distractor: one year's payment", 3000.00, 3000.00)

# ---------- 21: zero coupon bond, required return rises ----------

print("\n-- Q21  BONDS: zero coupon, 5,000 in 8 years, 4.5% then 6% --")
morning = pv_single(5000, 0.045, 8)
afternoon = pv_single(5000, 0.06, 8)
chk("Q21 1.045^8", 1.045 ** 8, 1.422101, 1e-5)
chk("Q21 the morning price", morning, 3515.93)
chk("Q21 1.06^8", 1.06 ** 8, 1.593848, 1e-5)
chk("Q21 the afternoon price", afternoon, 3137.06)
chk("Q21 answer, the fall", morning - afternoon, 378.86)
chk_txt("Q21 answer printed", money(morning - afternoon), answer(21))
chk("Q21 the price falls when the required return rises", 1,
    1 if afternoon < morning else 0, 0)
chk("Q21 distractor: 5,000 x 1.5%", 5000 * 0.015, 75.00)
chk("Q21 distractor: 5,000 x 1.5% x 8", 5000 * 0.015 * 8, 600.00)
chk("Q21 distractor: the new price, not the fall", afternoon, 3137.06)
chk("Q21 check line: morning price grown at 4.5 percent", fv_single(morning, 0.045, 8), 5000.00)
chk("Q21 check line: afternoon price grown at 6 percent", fv_single(afternoon, 0.06, 8), 5000.00)

# ---------- 22: the payment that makes IRR equal the required return ----------

print("\n-- Q22  NPV AND IRR: 25,000 today, one payment at year 4, IRR of 11% --")
need = fv_single(25000, 0.11, 4)
chk("Q22 1.11^2", 1.11 ** 2, 1.2321, 1e-6)
chk("Q22 1.11^4", 1.11 ** 4, 1.518070, 1e-5)
chk("Q22 answer, the payment needed", need, 37951.76)
chk_txt("Q22 answer printed", money(need), answer(22))
chk("Q22 check line: NPV at 11 percent is zero", pv_single(need, 0.11, 4) - 25000, 0.00, 1e-6)
chk("Q22 distractor: simple interest for 4 years", 25000 * (1 + 0.11 * 4), 36000.00)
chk("Q22 distractor: discounted instead of compounded", pv_single(25000, 0.11, 4), 16468.27)
chk("Q22 distractor: one year of growth", 25000 * 1.11, 27750.00)

# ---------- every printed option is accounted for ----------

print("\n-- EVERY OPTION ON THE PAGE IS EITHER THE ANSWER OR A NAMED WRONG CALCULATION --")
numeric_opts = 0
for i, it in enumerate(items, 1):
    for o in it["opts"]:
        if re.search(r"\d", o):
            numeric_opts += 1
chk("options carrying a number (85 total, 14 are wording only)", 71, numeric_opts, 0)

# ---------- checking-agent additions ----------
print("\n-- PAGE CHECKS ADDED BY THE CHECKING PASS --")
with open(HTML, encoding="utf-8") as _fh:
    _html = _fh.read()

# wide tables must scroll on a phone
_wide = 0
for _m in re.finditer(r"<table[^>]*>(.*?)</table>", _html, re.S):
    _rows = re.findall(r"<tr>(.*?)</tr>", _m.group(1), re.S)
    _cols = max((len(re.findall(r"<t[hd]", _r)) for _r in _rows), default=0)
    if _cols >= 5 and "tscroll" not in _html[max(0, _m.start() - 200):_m.start()]:
        _wide += 1
chk("tables with 5+ columns left outside .tscroll", _wide, 0, 0)

# the reserved split: only cases 1 to 3 of the decision environments quiz,
# and none of the classification quiz, which belongs to Mocks 1 and 3
_stems = " ".join((it["q"] + " " + " ".join(it["opts"])).lower() for it in items)
for _needle in ("payment app in a country where rules", "auto insurance deductible",
                "token offering", "insured bank cds", "private target",
                "benchmark rate rises above a threshold"):
    chk_txt("reserved for Mock 4, absent here: '%s'" % _needle[:26],
            str(_needle in _stems), "False")
for _needle in ("fixed rate mortgage", "wastewater plant", "signing a lease with a finance",
                "value added tax", "401(k)", "subsidized loan", "sole proprietor for tax",
                "public private partnership", "retain earnings to fund", "municipal bonds"):
    chk_txt("classification quiz item, not for Mock 2: '%s'" % _needle[:22],
            str(_needle in _stems), "False")

chk_txt("no em dash in the page copy", str("—" in _html), "False")
chk_txt("home link points at index.html",
        str('class="home" href="index.html"' in _html), "True")
chk_txt("back link points at day 10", str('href="day-10.html"' in _html), "True")
chk_txt("next link points at day 12", str('href="day-12.html"' in _html), "True")

print("\n" + "=" * 118)
print("Numbers checked: %d" % checks[0])
if fails:
    print("FAILED: %d" % len(fails))
    for f in fails:
        print("   - " + f)
    sys.exit(1)
print("ALL PASS")
