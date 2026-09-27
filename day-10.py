#!/usr/bin/env python3
"""
Verification for day-10.html  (Mock 1, 22 questions)

Recomputes every number that appears on the page: each correct answer, each
intermediate figure quoted inside an explanation, and the exact wrong
calculation named behind every distractor.

It also reads day-10.html back and checks:
  - there are 22 items
  - the tag mix matches the plan
  - the five items tagged "From a course quiz" carry the professor's own key
    (Finance_Classification_Quiz.pptx, answer key slide: 1)A 2)C 3)B 4)C 5)D)

Run:  python3 verify/day-10.py
"""

import os
import re
import sys

TOL = 0.005          # money is quoted to the cent
RTOL = 5e-5          # for rates quoted as percents

results = []


def chk(label, computed, page, tol=TOL):
    ok = abs(computed - page) <= tol
    results.append(ok)
    print("%-62s computed %14.6f   page %14.6f   %s"
          % (label, computed, page, "PASS" if ok else "FAIL"))


def chk_text(label, computed, page):
    ok = (computed == page)
    results.append(ok)
    print("%-62s computed %-16s page %-16s %s"
          % (label, str(computed), str(page), "PASS" if ok else "FAIL"))


def af(r, n):
    """present value annuity factor"""
    return (1 - (1 + r) ** -n) / r


def fvaf(r, n):
    """future value annuity factor"""
    return ((1 + r) ** n - 1) / r


def irr(cfs, lo=1e-6, hi=2.0):
    """cfs[0] is at t=0. bisection."""
    def npv(r):
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cfs))
    a, b = lo, hi
    fa = npv(a)
    for _ in range(400):
        m = (a + b) / 2.0
        fm = npv(m)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2.0


print("=" * 110)
print("DAY 10  MOCK 1  -  number check")
print("=" * 110)

# ---------------------------------------------------------------- Q2  single cash flow
print("\n-- Q2  single cash flow: PV of 72,000 at end of year 6, r = 9% --")
chk("1.09^3", 1.09 ** 3, 1.295029, 1e-6)
chk("1.09^6", 1.09 ** 6, 1.677100, 1e-6)
chk("ANSWER PV = 72000 / 1.09^6", 72000 / 1.09 ** 6, 42931.25, 0.005)
chk("check: 42931.25 x 1.09^6 back to 72,000", 42931.2475353 * 1.09 ** 6, 72000.00, 0.01)
chk("distractor n=5: 72000 / 1.09^5", 72000 / 1.09 ** 5, 46795.06, 0.01)
chk("distractor simple interest: 72000 / (1+0.09*6)", 72000 / (1 + 0.09 * 6), 46753.25, 0.01)
chk("distractor compounded forward: 72000 x 1.09^6", 72000 * 1.09 ** 6, 120751.21, 0.01)

# ---------------------------------------------------------------- Q3  payoff structure
print("\n-- Q3  payoff: V_T = 310, F_S = 250, F_J = 120 --")
VT, FS, FJ = 310.0, 250.0, 120.0
sen = min(VT, FS)
jun = 0.0 if VT < FS else min(VT - FS, FJ)
eq = max(VT - FS - FJ, 0.0)
chk("senior = Min(310, 250)", sen, 250.0)
chk("left after senior = 310 - 250", VT - FS, 60.0)
chk("junior = Min(60, 120)", jun, 60.0)
chk("equity = Max(310 - 250 - 120, 0)", eq, 0.0)
chk("check: three payoffs add to V_T", sen + jun + eq, 310.0)
chk("distractor 'senior 250 junior 120 equity -60' sums to", 250 + 120 - 60, 310.0)  # adds up but equity negative
chk_text("distractor equity -60 is below zero, so illegal", eq >= 0 and (-60) < 0, True)
chk("distractor 'senior 250 junior 60 equity 60' sums to F_S+F_J", 250 + 60 + 60, 370.0)
chk("distractor 'senior 190 junior 120' pays junior first: 310-120", VT - FJ, 190.0)

# ---------------------------------------------------------------- Q4  annuity
print("\n-- Q4  annuity: 7,500 a year for 11 years, r = 6% --")
chk("1.06^11", 1.06 ** 11, 1.898299, 1e-6)
chk("1.06^-11", 1 / 1.06 ** 11, 0.526788, 1e-6)
chk("1 - 0.526788", 1 - 1 / 1.06 ** 11, 0.473212, 1e-6)
chk("annuity factor (6%, 11)", af(0.06, 11), 7.886875, 1e-6)
chk("ANSWER PV = 7500 x 7.886875", 7500 * af(0.06, 11), 59151.56, 0.01)
chk("bound: factor below n = 11", 11.0 - af(0.06, 11), 11.0 - 7.886875, 1e-5)
chk("bound: perpetuity factor 1/0.06", 1 / 0.06, 16.667, 0.001)
chk("distractor n=10", 7500 * af(0.06, 10), 55200.65, 0.01)
chk("distractor undiscounted 7500 x 11", 7500 * 11, 82500.00)
chk("distractor perpetuity 7500 / 0.06", 7500 / 0.06, 125000.00)

# ---------------------------------------------------------------- Q6  premium bond
print("\n-- Q6  bond: par 1,000, coupon 8%, n = 6, yield 6% --")
chk("cash coupon 0.08 x 1000", 0.08 * 1000, 80.0)
chk("1.06^6", 1.06 ** 6, 1.418519, 1e-6)
chk("1 / 1.06^6", 1 / 1.06 ** 6, 0.704961, 1e-6)
chk("annuity factor (6%, 6)", af(0.06, 6), 4.917324, 1e-6)
chk("coupons 80 x 4.917324", 80 * af(0.06, 6), 393.39, 0.01)
chk("par value 1000 / 1.06^6", 1000 / 1.06 ** 6, 704.96, 0.01)
chk("ANSWER price = 393.39 + 704.96", 80 * af(0.06, 6) + 1000 / 1.06 ** 6, 1098.35, 0.01)
chk_text("premium: price above par", (80 * af(0.06, 6) + 1000 / 1.06 ** 6) > 1000, True)
chk("distractor discount at coupon rate 8%", 80 * af(0.08, 6) + 1000 / 1.08 ** 6, 1000.00, 0.01)
chk("distractor undiscounted 80 x 6 + 1000", 80 * 6 + 1000, 1480.00)
chk("distractor par only", 1000 / 1.06 ** 6, 704.96, 0.01)

# ---------------------------------------------------------------- Q7  mixed stream
print("\n-- Q7  mixed: 6,000 at y1; 4,000 at y2..y6; 20,000 at y7; r = 8% --")
chk("piece one 6000 / 1.08", 6000 / 1.08, 5555.56, 0.01)
chk("1.08^5", 1.08 ** 5, 1.469328, 1e-6)
chk("annuity factor (8%, 5)", af(0.08, 5), 3.992710, 1e-6)
chk("annuity value at end of year 1", 4000 * af(0.08, 5), 15970.84, 0.01)
chk("moved back one year: / 1.08", 4000 * af(0.08, 5) / 1.08, 14787.81, 0.01)
chk("1.08^7", 1.08 ** 7, 1.713824, 1e-6)
chk("piece three 20000 / 1.08^7", 20000 / 1.08 ** 7, 11669.81, 0.01)
total7 = 6000 / 1.08 + 4000 * af(0.08, 5) / 1.08 + 20000 / 1.08 ** 7
chk("ANSWER total", total7, 32013.18, 0.01)
one_by_one = sum(cf / 1.08 ** t for t, cf in
                 [(1, 6000), (2, 4000), (3, 4000), (4, 4000), (5, 4000), (6, 4000), (7, 20000)])
chk("check: all seven discounted one at a time", one_by_one, 32013.18, 0.01)
chk("raw cash 6000 + 5x4000 + 20000", 6000 + 5 * 4000 + 20000, 46000.0)
chk("distractor annuity left at t0", 6000 / 1.08 + 4000 * af(0.08, 5) + 20000 / 1.08 ** 7, 33196.20, 0.01)
chk("distractor annuity moved back twice",
    6000 / 1.08 + 4000 * af(0.08, 5) / 1.08 ** 2 + 20000 / 1.08 ** 7, 30917.78, 0.01)

# ---------------------------------------------------------------- Q9  NPV accept
print("\n-- Q9  NPV: I0 = 45,000; 18,000 / 22,000 / 16,000; r = 11% --")
chk("1.11^2", 1.11 ** 2, 1.2321, 1e-6)
chk("1.11^3", 1.11 ** 3, 1.367631, 1e-6)
chk("18000 / 1.11", 18000 / 1.11, 16216.22, 0.01)
chk("22000 / 1.11^2", 22000 / 1.11 ** 2, 17855.69, 0.01)
chk("16000 / 1.11^3", 16000 / 1.11 ** 3, 11699.06, 0.01)
pv9 = 18000 / 1.11 + 22000 / 1.11 ** 2 + 16000 / 1.11 ** 3
chk("PV of the inflows", pv9, 45770.97, 0.01)
chk("ANSWER NPV = 45770.97 - 45000", pv9 - 45000, 770.97, 0.01)
chk_text("decision: accept because NPV > 0", pv9 - 45000 > 0, True)
irr9 = irr([-45000, 18000, 22000, 16000])
chk("check: IRR of this project (percent)", irr9 * 100, 12.00, 0.01)
chk_text("check: required 11% is below the IRR", 0.11 < irr9, True)
chk("distractor undiscounted 18000+22000+16000-45000", 18000 + 22000 + 16000 - 45000, 11000.00)
chk("distractor PV of inflows with cost not subtracted", pv9, 45770.97, 0.01)

# ---------------------------------------------------------------- Q10  growing perpetuity, inverse
print("\n-- Q10  growing perpetuity: CF1 = 5,000, r = 10%, PV = 125,000, find g --")
chk("CF1 / PV = 5000 / 125000", 5000 / 125000, 0.04, 1e-12)
g10 = 0.10 - 5000 / 125000
chk("ANSWER g = r - CF1/PV (percent)", g10 * 100, 6.00, 1e-9)
chk("check forward: 5000 / (0.10 - 0.06)", 5000 / (0.10 - 0.06), 125000.00, 0.01)
chk_text("check: r > g holds", 0.10 > g10, True)
chk("distractor: reporting the gap as g (percent)", (5000 / 125000) * 100, 4.00, 1e-9)
chk("distractor: adding the gap to r (percent)", (0.10 + 0.04) * 100, 14.00, 1e-9)
chk("distractor: 125000 taken as the payment share (percent)", (5000 / 125000 / 1.6) * 100, 2.50, 1e-9)

# ---------------------------------------------------------------- Q11  par bond
print("\n-- Q11  bond: par 1,000, cash coupon 90, n = 4, price exactly 1,000 --")
chk("coupon rate = 90 / 1000 (percent)", 90 / 1000 * 100, 9.00, 1e-9)
chk("1.09^4", 1.09 ** 4, 1.411582, 1e-6)
chk("annuity factor (9%, 4)", af(0.09, 4), 3.239720, 1e-6)
chk("coupons 90 x 3.239720", 90 * af(0.09, 4), 291.57, 0.01)
chk("par 1000 / 1.09^4", 1000 / 1.09 ** 4, 708.43, 0.01)
chk("ANSWER check: price at 9% is exactly par", 90 * af(0.09, 4) + 1000 / 1.09 ** 4, 1000.00, 0.01)

# ---------------------------------------------------------------- Q12  find the rate
print("\n-- Q12  single cash flow inverse: 12,500 -> 20,000 over 7 years --")
chk("FV / PV = 20000 / 12500", 20000 / 12500, 1.6, 1e-12)
r12 = 1.6 ** (1 / 7) - 1
chk("1.6^(1/7)", 1.6 ** (1 / 7), 1.069449, 1e-6)
chk("ANSWER rate (percent)", r12 * 100, 6.94, 0.005)
chk("check: 12500 x (1+r)^7", 12500 * (1 + r12) ** 7, 20000.00, 0.01)
chk("distractor simple interest (percent)", ((20000 / 12500) - 1) / 7 * 100, 8.57, 0.005)
chk("distractor total growth over 7 years (percent)", (20000 / 12500 - 1) * 100, 60.00, 1e-9)
chk("distractor 7.5% fails the check: 12500 x 1.075^7", 12500 * 1.075 ** 7, 20738.0, 1.0)

# ---------------------------------------------------------------- Q14  holding period return
print("\n-- Q14  HPR: P0 = 40.00, P1 = 43.00, D1 = 2.40 --")
chk("price move 43 - 40", 43 - 40, 3.00)
chk("plus dividend", (43 - 40) + 2.40, 5.40)
hpr = (43 - 40 + 2.40) / 40
chk("ANSWER HPR (percent)", hpr * 100, 13.50, 1e-9)
chk("check: 40 x 1.135", 40 * 1.135, 45.40, 0.001)
chk("check: 43.00 of share + 2.40 of cash", 43.00 + 2.40, 45.40)
chk("distractor price move only (percent)", (43 - 40) / 40 * 100, 7.50, 1e-9)
chk("distractor dividend only (percent)", 2.40 / 40 * 100, 6.00, 1e-9)
chk("distractor divided by P1 (percent)", 5.40 / 43 * 100, 12.56, 0.005)

# ---------------------------------------------------------------- Q15  annuity payment
print("\n-- Q15  annuity inverse: borrow 84,000, 7 equal payments, r = 7% --")
chk("1.07^7", 1.07 ** 7, 1.605781, 1e-6)
chk("1 / 1.07^7", 1 / 1.07 ** 7, 0.622750, 1e-6)
chk("1 - 0.622750", 1 - 1 / 1.07 ** 7, 0.377250, 1e-6)
chk("annuity factor (7%, 7)", af(0.07, 7), 5.389289, 1e-6)
pay15 = 84000 / af(0.07, 7)
chk("ANSWER payment = 84000 / 5.389289", pay15, 15586.47, 0.01)
chk("check: 15586.47 x 5.389289 back to the loan", 15586.4704490 * af(0.07, 7), 84000.00, 0.01)
chk("sanity: 84000 / 7 with no interest", 84000 / 7, 12000.00)
chk_text("sanity: real payment must exceed 12,000", pay15 > 12000, True)
chk("distractor FV annuity formula 84000 x 0.07 / (1.07^7 - 1)", 84000 / fvaf(0.07, 7), 9706.47, 0.01)
chk("distractor n=8 factor", af(0.07, 8), 5.971299, 1e-6)
chk("distractor n=8 payment 84000 / 5.971299", 84000 / af(0.07, 8), 14067.29, 0.01)

# ---------------------------------------------------------------- Q16  discount bond
print("\n-- Q16  bond: par 1,000, coupon 4%, n = 5, yield 7% --")
chk("cash coupon 0.04 x 1000", 0.04 * 1000, 40.0)
chk("1.07^5", 1.07 ** 5, 1.402552, 1e-6)
chk("1 / 1.07^5", 1 / 1.07 ** 5, 0.712986, 1e-6)
chk("annuity factor (7%, 5)", af(0.07, 5), 4.100197, 1e-6)
chk("coupons 40 x 4.100197", 40 * af(0.07, 5), 164.01, 0.01)
chk("par 1000 / 1.07^5", 1000 / 1.07 ** 5, 712.99, 0.01)
price16 = 40 * af(0.07, 5) + 1000 / 1.07 ** 5
chk("ANSWER price", price16, 876.99, 0.01)
chk_text("discount: price below par", price16 < 1000, True)
chk("gap below par 1000 - 876.99", 1000 - price16, 123.01, 0.01)
chk("gap sanity: 30 a year short, 5 years, at 7%", 30 * af(0.07, 5), 123.01, 0.01)
chk("distractor discount at the coupon rate 4%", 40 * af(0.04, 5) + 1000 / 1.04 ** 5, 1000.00, 0.01)
chk("distractor n=4", 40 * af(0.07, 4) + 1000 / 1.07 ** 4, 898.38, 0.01)
chk("distractor coupon and yield swapped: 70 at 4%", 70 * af(0.04, 5) + 1000 / 1.04 ** 5, 1133.55, 0.01)

# ---------------------------------------------------------------- Q18  deferred annuity
print("\n-- Q18  deferred annuity: 3,000 a year, years 5 to 9, r = 7% --")
chk("number of payments (years 5..9)", len(range(5, 10)), 5)
chk("1.07^5", 1.07 ** 5, 1.402552, 1e-6)
chk("annuity factor (7%, 5)", af(0.07, 5), 4.100197, 1e-6)
chk("value at end of year 4: 3000 x 4.100197", 3000 * af(0.07, 5), 12300.59, 0.01)
chk("1.07^4", 1.07 ** 4, 1.310796, 1e-6)
pv18 = 3000 * af(0.07, 5) / 1.07 ** 4
chk("ANSWER PV today", pv18, 9384.06, 0.01)
chk("check: five payments discounted one at a time",
    sum(3000 / 1.07 ** t for t in range(5, 10)), 9384.06, 0.01)
chk("distractor left at year 4", 3000 * af(0.07, 5), 12300.59, 0.01)
chk("distractor divided by 1.07^5", 3000 * af(0.07, 5) / 1.07 ** 5, 8770.15, 0.01)
chk("distractor undiscounted 3000 x 5", 3000 * 5, 15000.00)

# ---------------------------------------------------------------- Q19  payoff structure
print("\n-- Q19  payoff: V_T = 175, F_S = 90, F_J = 60 --")
VT, FS, FJ = 175.0, 90.0, 60.0
sen = min(VT, FS)
jun = 0.0 if VT < FS else min(VT - FS, FJ)
eq = max(VT - FS - FJ, 0.0)
chk("F_S + F_J", FS + FJ, 150.0)
chk("senior = Min(175, 90)", sen, 90.0)
chk("left after senior", VT - FS, 85.0)
chk("junior = Min(85, 60)", jun, 60.0)
chk("ANSWER equity = Max(175 - 90 - 60, 0)", eq, 25.0)
chk("check: three payoffs add to V_T", sen + jun + eq, 175.0)
chk("distractor 'junior takes all 85' sum", 90 + 85 + 0, 175.0)  # adds up, but breaks the debt ceiling
chk_text("distractor junior 85 exceeds its face value of 60", 85 > FJ, True)
chk("distractor 'equity = V_T - F_S' gives", max(VT - FS, 0), 85.0)
chk("distractor 'senior 90 junior 60 equity 85' sums to", 90 + 60 + 85, 235.0)
chk("distractor 'senior 115' exceeds F_S", 115 - FS, 25.0)

# ---------------------------------------------------------------- Q20  zero coupon, rate rise
print("\n-- Q20  zero coupon: face 1,000, 8 years, 5% then 7% --")
chk("1.05^8", 1.05 ** 8, 1.477455, 1e-6)
chk("old price 1000 / 1.05^8", 1000 / 1.05 ** 8, 676.84, 0.01)
chk("1.07^8", 1.07 ** 8, 1.718186, 1e-6)
chk("new price 1000 / 1.07^8", 1000 / 1.07 ** 8, 582.01, 0.01)
fall = 1000 / 1.05 ** 8 - 1000 / 1.07 ** 8
chk("ANSWER fall in price", fall, 94.83, 0.01)
chk("check: 582.01 x 1.07^8 back to face", 582.0091046 * 1.07 ** 8, 1000.00, 0.01)
chk_text("direction: rates up, price down", (1000 / 1.07 ** 8) < (1000 / 1.05 ** 8), True)
chk("distractor '2 points of 1,000'", 0.02 * 1000, 20.00)

# ---------------------------------------------------------------- Q22  NPV reject
print("\n-- Q22  NPV: cost 24,000; 7,000 a year for 4 years; r = 8% --")
chk("1.08^4", 1.08 ** 4, 1.360489, 1e-6)
chk("1 / 1.08^4", 1 / 1.08 ** 4, 0.735030, 1e-6)
chk("annuity factor (8%, 4)", af(0.08, 4), 3.312127, 1e-6)
chk("PV of inflows 7000 x 3.312127", 7000 * af(0.08, 4), 23184.89, 0.01)
npv22 = 7000 * af(0.08, 4) - 24000
chk("ANSWER NPV", npv22, -815.11, 0.01)
chk_text("decision: reject because NPV < 0", npv22 < 0, True)
irr22 = irr([-24000, 7000, 7000, 7000, 7000])
chk("check: IRR (percent)", irr22 * 100, 6.46, 0.01)
chk_text("check: required 8% is above the IRR, so NPV must be negative", 0.08 > irr22, True)
chk("raw cash 7000 x 4", 7000 * 4, 28000.0)
chk("distractor undiscounted 28000 - 24000", 7000 * 4 - 24000, 4000.00)
chk("distractor NPV at 6% instead of 8%", 7000 * af(0.06, 4) - 24000, 255.74, 0.01)
chk("distractor PV of inflows, cost not subtracted", 7000 * af(0.08, 4), 23184.89, 0.01)

# ================================================================ page structure and the course key
print("\n" + "=" * 110)
print("PAGE CHECK  -  item count, tag mix, and the professor's answer key")
print("=" * 110)

here = os.path.dirname(os.path.abspath(__file__))
page_path = os.path.join(here, "..", "day-10.html")

try:
    html = open(page_path, encoding="utf-8").read()
except OSError as e:
    print("Could not open day-10.html: %s" % e)
    sys.exit(1)

items = []
for m in re.finditer(
        r'\{\s*\n\s*q:\s*"(?P<q>(?:[^"\\]|\\.)*)",\s*\n'
        r'\s*opts:\s*\[(?P<opts>.*?)\],\s*\n'
        r'\s*correct:\s*(?P<correct>\d+),\s*\n'
        r'\s*tag:\s*"(?P<tag>[^"]+)",\s*\n'
        r'(?:\s*src:\s*"(?P<src>[^"]+)",\s*\n)?', html):
    opts = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group("opts"))
    items.append({
        "q": m.group("q"),
        "opts": opts,
        "correct": int(m.group("correct")),
        "tag": m.group("tag"),
        "src": m.group("src"),
    })

chk("items parsed from the page", len(items), 22)

tags = {}
for it in items:
    tags[it["tag"]] = tags.get(it["tag"], 0) + 1

plan = {
    "Concepts": 6,
    "Single cash flow": 2,
    "Annuity": 2,
    "Perpetuity": 1,
    "Mixed stream": 2,
    "Bonds": 4,
    "Payoff structure": 2,
    "NPV and IRR": 2,
    "Stocks": 1,
}
for tag, want in plan.items():
    chk("tag count: %s" % tag, tags.get(tag, 0), want)

allowed = set(plan.keys())
chk_text("every tag is one of the nine allowed", set(tags.keys()) <= allowed, True)
chk("time value of money items (single+annuity+perp+mixed)",
    tags.get("Single cash flow", 0) + tags.get("Annuity", 0)
    + tags.get("Perpetuity", 0) + tags.get("Mixed stream", 0), 7)

# every item must have four or more options and a correct index inside range
ok_opts = all(len(it["opts"]) >= 4 and 0 <= it["correct"] < len(it["opts"]) for it in items)
chk_text("every item has 4+ options and a valid correct index", ok_opts, True)

# correct answers must not all sit on the same index
spread = len(set(it["correct"] for it in items))
chk_text("correct answers use more than one index", spread > 1, True)

# ---- the professor's key, Finance_Classification_Quiz.pptx, questions 1 to 5 only
KEY = [
    ("fixed rate mortgage", "Personal finance"),                 # prof Q1 -> A
    ("wastewater plant", "Public finance"),                      # prof Q2 -> C
    ("signing a lease with a finance company", "Corporate finance"),  # prof Q3 -> B
    ("value added tax", "Public finance"),                       # prof Q4 -> C
    ("401(k)", "Personal and Corporate"),                        # prof Q5 -> D
]

sourced = [it for it in items if it["src"]]
chk("items tagged as coming from a course quiz", len(sourced), 5)
chk_text("all five carry the honest source label",
         all(it["src"] == "From a course quiz" for it in sourced), True)

for needle, expected in KEY:
    hit = [it for it in items if needle in it["q"]]
    if len(hit) != 1:
        chk("course quiz item found for '%s'" % needle, len(hit), 1)
        continue
    it = hit[0]
    chk_text("professor's key: '%s...'" % needle[:28],
             it["opts"][it["correct"]], expected)
    chk_text("  six options reproduced faithfully", len(it["opts"]), 6)

# none of the reserved questions 6 to 10 may appear anywhere on the page
RESERVED = ["subsidized loan", "sole proprietor for tax", "public private partnership",
            "retain earnings to fund", "municipal bonds"]
for needle in RESERVED:
    chk_text("reserved for Mock 3, absent here: '%s'" % needle, needle in html, False)

# no em dash anywhere in the page copy
chk_text("no em dash in the page", "\u2014" in html, False)

# --- checking-agent additions -----------------------------------
# Item 13 used to re-ask day 1's fourth worked example: friends choosing a
# business form, answer corporation, cost double taxation. It was rewritten as
# an agency problem item. These checks stop the repeat coming back.
PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
learn = ""
for _d in range(1, 10):
    with open(os.path.join(PACK, "day-0%d.html" % _d), encoding="utf-8") as fh:
        learn += fh.read().lower()

stems_and_opts = " ".join(
    (it["q"] + " " + " ".join(it["opts"])).lower() for it in items)
for phrase in ("sole propriet", "double taxation", "partnership"):
    taught = phrase in learn
    chk_text("day 1 teaches '%s', so no mock 1 item may re-ask it" % phrase,
             taught and (phrase in stems_and_opts), False)

chk_text("item 13 tests the agency problem",
         "agency problem" in html.lower(), True)
chk_text("  and its stem never names the conclusion",
         "agency" in stems_and_opts, False)

# every table with five or more columns must sit inside a .tscroll wrapper
wide_unwrapped = 0
for m in re.finditer(r"<table[^>]*>(.*?)</table>", html, re.S):
    _rows = re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)
    _cols = max((len(re.findall(r"<t[hd]", r)) for r in _rows), default=0)
    if _cols >= 5 and "tscroll" not in html[max(0, m.start() - 200):m.start()]:
        wide_unwrapped += 1
chk("tables with 5+ columns left outside .tscroll", wide_unwrapped, 0)

# ================================================================
print("\n" + "=" * 110)
total = len(results)
failed = total - sum(1 for r in results if r)
print("%d checks run, %d passed, %d failed" % (total, total - failed, failed))
print("=" * 110)
sys.exit(1 if failed else 0)
