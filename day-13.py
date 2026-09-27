#!/usr/bin/env python3
"""
verify/day-13.py — recompute every number that appears on day-13.html (Mock 3).

Day 13 is a mock paper, so there are no worked examples or try-its on the page.
Every number lives inside a quiz item: its options and its explanation.
This script recomputes all of them, plus the professor's answer key for the five
reproduced course-quiz items, and plus three structural checks the page relies on.

Run:  python3 verify/day-13.py
"""

import re
import os
import sys

CHECKS = []


def chk(label, computed, page, tol=0.005):
    """Compare a computed number with what the page prints."""
    ok = abs(computed - page) <= tol
    CHECKS.append((label, computed, page, ok))


def chk_exact(label, computed, page):
    ok = (computed == page)
    CHECKS.append((label, computed, page, ok))


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------

def af(r, n):
    """present value annuity factor"""
    return (1 - (1 + r) ** -n) / r


def bond_price(par, coupon_rate, n, y):
    c = par * coupon_rate
    return c * af(y, n) + par / (1 + y) ** n


def r2(x):
    return round(x + 1e-12, 2)


# ======================================================================
# Q1  BONDS — premium bond, coupon-rate trap
#     par 2,000 · coupon rate 7% · n = 6 · yield 5%
# ======================================================================
C1 = 0.07 * 2000
chk("Q1 coupon payment 0.07 x 2,000", C1, 140.0)
chk("Q1 growth factor 1.05^6", 1.05 ** 6, 1.340096, tol=5e-7)
chk("Q1 annuity factor af(5%,6)", af(0.05, 6), 5.075692, tol=5e-7)
chk("Q1 PV of coupons 140 x af", C1 * af(0.05, 6), 710.60)
chk("Q1 PV of par 2,000 / 1.05^6", 2000 / 1.05 ** 6, 1492.43)
chk("Q1 CORRECT price", bond_price(2000, 0.07, 6, 0.05), 2203.03)
chk("Q1 pieces add to the printed price",
    r2(C1 * af(0.05, 6)) + r2(2000 / 1.05 ** 6), 2203.03)
chk("Q1 distractor 2,000.00 = discounted at the 7% coupon rate",
    bond_price(2000, 0.07, 6, 0.07), 2000.00)
chk("Q1 distractor 1,492.43 = par only", 2000 / 1.05 ** 6, 1492.43)
chk("Q1 distractor 710.60 = coupons only", C1 * af(0.05, 6), 710.60)

# ======================================================================
# Q3  PAYOFF — state II.  V_T = 118, F_S = 85, F_J = 60
# ======================================================================
VT, FS, FJ = 118.0, 85.0, 60.0
sen = min(VT, FS)
jun = 0.0 if VT < FS else min(VT - FS, FJ)
eq = max(VT - FS - FJ, 0.0)
chk("Q3 second border F_S + F_J", FS + FJ, 145.0)
chk("Q3 senior Min(118, 85)", sen, 85.0)
chk("Q3 junior Min(118-85, 60)", jun, 33.0)
chk("Q3 equity Max(118-145, 0)", eq, 0.0)
chk("Q3 payoffs sum to exactly V_T", sen + jun + eq, VT)
chk("Q3 junior shortfall 60 - 33", FJ - jun, 27.0)
chk("Q3 distractor junior-first senior = 118 - 60", VT - FJ, 58.0)
chk("Q3 distractor negative equity 118 - 145", VT - FS - FJ, -27.0)
chk("Q3 distractor 85 + 60 overshoots the pot", FS + FJ, 145.0)

# ======================================================================
# Q4  SINGLE CASH FLOW — 12,000 at year 3 vs 16,000 at year 6, r = 9%
# ======================================================================
chk("Q4 1.09^3", 1.09 ** 3, 1.295029, tol=5e-7)
chk("Q4 1.09^6", 1.09 ** 6, 1.677100, tol=5e-7)
pv_a = 12000 / 1.09 ** 3
pv_b = 16000 / 1.09 ** 6
chk("Q4 PV of offer A", pv_a, 9266.20)
chk("Q4 PV of offer B", pv_b, 9540.28)
chk("Q4 CORRECT difference B - A", pv_b - pv_a, 274.08)
chk("Q4 distractor 4,000 = 16,000 - 12,000 undiscounted", 16000 - 12000, 4000.0)
chk_exact("Q4 B really is the larger one", pv_b > pv_a, True)

# ======================================================================
# Q5  BONDS — discount bond, rate rose
#     par 1,000 · coupon rate 3% · n = 7 · yield 6.5%
# ======================================================================
chk("Q5 coupon payment 0.03 x 1,000", 0.03 * 1000, 30.0)
chk("Q5 growth factor 1.065^7", 1.065 ** 7, 1.553987, tol=5e-7)
chk("Q5 annuity factor af(6.5%,7)", af(0.065, 7), 5.484520, tol=5e-7)
chk("Q5 PV of coupons (3 dp as printed)", 30 * af(0.065, 7), 164.536, tol=5e-4)
chk("Q5 PV of par (3 dp as printed)", 1000 / 1.065 ** 7, 643.506, tol=5e-4)
chk("Q5 CORRECT price", bond_price(1000, 0.03, 7, 0.065), 808.04)
chk("Q5 distractor 830.56 = n taken as 6", bond_price(1000, 0.03, 6, 0.065), 830.56)
chk("Q5 distractor 1,000.00 = discounted at the 3% coupon rate",
    bond_price(1000, 0.03, 7, 0.03), 1000.00)
chk("Q5 distractor 643.51 = par only", 1000 / 1.065 ** 7, 643.51)
chk_exact("Q5 is a discount bond (price under par)",
          bond_price(1000, 0.03, 7, 0.065) < 1000, True)

# ======================================================================
# Q6  PAYOFF — state III, promised amounts built from face + coupon
#     face 200 @ 5% and face 90 @ 10%, V_T = 340
# ======================================================================
FS6 = 200 + 0.05 * 200
FJ6 = 90 + 0.10 * 90
VT6 = 340.0
chk("Q6 F_S = 200 + 5% coupon", FS6, 210.0)
chk("Q6 F_J = 90 + 10% coupon", FJ6, 99.0)
chk("Q6 second border F_S + F_J", FS6 + FJ6, 309.0)
sen6 = min(VT6, FS6)
jun6 = 0.0 if VT6 < FS6 else min(VT6 - FS6, FJ6)
eq6 = max(VT6 - FS6 - FJ6, 0.0)
chk("Q6 senior", sen6, 210.0)
chk("Q6 junior", jun6, 99.0)
chk("Q6 CORRECT equity", eq6, 31.0)
chk("Q6 payoffs sum to exactly V_T", sen6 + jun6 + eq6, VT6)
chk("Q6 distractor residual 340 - 210 before the junior cap", VT6 - FS6, 130.0)
chk("Q6 distractor bare face values sum", 200 + 90, 290.0)
chk("Q6 distractor bare-face equity 340 - 290", VT6 - 290, 50.0)
chk("Q6 coupon money the bare-face option loses", (FS6 + FJ6) - 290, 19.0)

# ======================================================================
# Q8  BONDS — trading at par, coupon rate equals yield
#     par 5,000 · coupon 320 · n = 9 · yield 6.4%
# ======================================================================
chk("Q8 implied coupon rate 320 / 5,000", 320 / 5000, 0.064, tol=1e-9)
chk("Q8 growth factor 1.064^9", 1.064 ** 9, 1.747731, tol=5e-7)
chk("Q8 annuity factor af(6.4%,9)", af(0.064, 9), 6.684838, tol=5e-7)
chk("Q8 PV of coupons", 320 * af(0.064, 9), 2139.15)
chk("Q8 PV of par", 5000 / 1.064 ** 9, 2860.85)
chk("Q8 CORRECT price is exactly par", bond_price(5000, 0.064, 9, 0.064), 5000.00)
chk("Q8 pieces add to the printed price",
    r2(320 * af(0.064, 9)) + r2(5000 / 1.064 ** 9), 5000.00)
chk("Q8 distractor 5,320 = par plus one coupon", 5000 + 320, 5320.0)

# ======================================================================
# Q9  MIXED STREAM — 1,500 in years 1-5, then 20,000 at year 8, r = 6%
# ======================================================================
chk("Q9 1.06^5", 1.06 ** 5, 1.338226, tol=5e-7)
chk("Q9 annuity factor af(6%,5)", af(0.06, 5), 4.212364, tol=5e-7)
chk("Q9 PV of the annuity (3 dp as printed)", 1500 * af(0.06, 5), 6318.546, tol=5e-4)
chk("Q9 1.06^8", 1.06 ** 8, 1.593848, tol=5e-7)
chk("Q9 PV of the year-8 payment (3 dp as printed)",
    20000 / 1.06 ** 8, 12548.247, tol=5e-4)
pv9 = 1500 * af(0.06, 5) + 20000 / 1.06 ** 8
chk("Q9 CORRECT total", pv9, 18866.79)
chk("Q9 distractor 21,862.94 = annuity run for 8 years",
    1500 * af(0.06, 8) + 20000 / 1.06 ** 8, 21862.94)
chk("Q9 distractor 27,500 = raw cash, no discounting", 5 * 1500 + 20000, 27500.0)
chk("Q9 distractor 17,253.84 = whole 27,500 discounted from year 8",
    27500 / 1.06 ** 8, 17253.84)
chk_exact("Q9 sanity: answer sits between the single piece and the raw cash",
          12548.25 < pv9 < 27500, True)

# ======================================================================
# Q10 PAYOFF — state I.  V_T = 38, F_S = 62, F_J = 30
# ======================================================================
VT10, FS10, FJ10 = 38.0, 62.0, 30.0
sen10 = min(VT10, FS10)
jun10 = 0.0 if VT10 < FS10 else min(VT10 - FS10, FJ10)
eq10 = max(VT10 - FS10 - FJ10, 0.0)
chk("Q10 senior Min(38, 62)", sen10, 38.0)
chk("Q10 junior (V_T below F_S)", jun10, 0.0)
chk("Q10 equity Max(38-92, 0)", eq10, 0.0)
chk("Q10 payoffs sum to exactly V_T", sen10 + jun10 + eq10, VT10)
chk("Q10 senior lender's loss 62 - 38", FS10 - sen10, 24.0)
chk("Q10 distractor: shortfall the owners are wrongly asked for",
    (FS10 + FJ10) - VT10, 54.0)
chk("Q10 distractor: pro-rata senior share 38 x 62/92",
    VT10 * FS10 / (FS10 + FJ10), 25.61)
chk("Q10 distractor: pro-rata junior share 38 x 30/92",
    VT10 * FJ10 / (FS10 + FJ10), 12.39)
chk("Q10 distractor: junior-first leftover for senior 38 - 30", VT10 - FJ10, 8.0)

# ======================================================================
# Q11 BONDS — perpetual bond, inverse.  C = 84, price 1,200
# ======================================================================
chk("Q11 CORRECT yield 84 / 1,200", 84 / 1200, 0.0700, tol=5e-6)
chk("Q11 check, forward: 84 / 0.07", 84 / 0.07, 1200.00)
chk("Q11 distractor 8.40% = 84 / 1,000", 84 / 1000, 0.0840, tol=5e-6)
chk("Q11 distractor 6.54% = 84 / (1,200 + 84)", 84 / 1284, 0.0654, tol=5e-5)

# ======================================================================
# Q13 STOCKS — holding period return.  P0 150, P1 168, D1 3.00
# ======================================================================
P0, P1, D1 = 150.0, 168.0, 3.00
chk("Q13 price gain P1 - P0", P1 - P0, 18.0)
chk("Q13 top of the formula (P1 - P0 + D1)", P1 - P0 + D1, 21.0)
chk("Q13 CORRECT holding period return", (P1 - P0 + D1) / P0, 0.140, tol=5e-6)
chk("Q13 check 150 x 1.14", P0 * (1 + (P1 - P0 + D1) / P0), 171.00)
chk("Q13 check 168 + 3.00", P1 + D1, 171.00)
chk("Q13 distractor 12.0% = price move only", (P1 - P0) / P0, 0.120, tol=5e-6)
chk("Q13 distractor 12.5% = divided by the end price", (P1 - P0 + D1) / P1, 0.125, tol=5e-6)
chk("Q13 distractor 2.0% = dividend only", D1 / P0, 0.020, tol=5e-6)

# ======================================================================
# Q14 PAYOFF — boundary, V_T exactly at F_S.  F_S = 96, F_J = 40
#     senior paid in full  ->  V_T >= 96
#     junior receives 0    ->  V_T <= 96
# ======================================================================
FS14, FJ14 = 96.0, 40.0
chk("Q14 second border F_S + F_J", FS14 + FJ14, 136.0)
lo = FS14          # smallest V_T that pays the senior lender in full
hi = FS14          # largest V_T that leaves the junior lender with nothing
chk("Q14 lower bound from the senior report", lo, 96.0)
chk("Q14 upper bound from the junior report", hi, 96.0)
chk("Q14 CORRECT V_T, the single value both reports allow", lo, 96.0)
VT14 = 96.0
s14 = min(VT14, FS14)
j14 = 0.0 if VT14 < FS14 else min(VT14 - FS14, FJ14)
e14 = max(VT14 - FS14 - FJ14, 0.0)
chk("Q14 senior at V_T = 96", s14, 96.0)
chk("Q14 junior at V_T = 96", j14, 0.0)
chk("Q14 equity at V_T = 96", e14, 0.0)
chk("Q14 payoffs sum to exactly V_T", s14 + j14 + e14, VT14)
# the ranges the distractors name must each break one of the two reports
chk_exact("Q14 at V_T = 97 the junior lender would receive something",
          min(97.0 - FS14, FJ14) > 0, True)
chk_exact("Q14 at V_T = 95 the senior lender would be short",
          min(95.0, FS14) < FS14, True)

# ======================================================================
# Q15 BONDS — zero coupon, inverse to the face value
#     price 6,268.21 · n = 5 · yield 5%
# ======================================================================
price15 = 6268.21
chk("Q15 growth factor 1.05^5", 1.05 ** 5, 1.276282, tol=5e-7)
chk("Q15 CORRECT face value price x 1.05^5", price15 * 1.05 ** 5, 8000.00)
chk("Q15 check, forward: 8,000 / 1.05^5 is the printed price",
    8000 / 1.05 ** 5, 6268.21)
chk("Q15 distractor 6,581.62 = compounded one year only", price15 * 1.05, 6581.62)
chk("Q15 distractor 7,835.26 = simple interest 5% x 5 years",
    price15 * (1 + 0.05 * 5), 7835.26)
chk("Q15 distractor 4,911.31 = divided instead of multiplied",
    price15 / 1.05 ** 5, 4911.31)

# ======================================================================
# Q16 PERPETUITY — growing.  C1 = 48,000 · g = 3% · r = 8%
# ======================================================================
chk("Q16 r - g", 0.08 - 0.03, 0.05, tol=1e-9)
chk("Q16 CORRECT value 48,000 / 0.05", 48000 / 0.05, 960000.00, tol=0.5)
chk("Q16 distractor 600,000 = growth ignored", 48000 / 0.08, 600000.00, tol=0.5)
chk("Q16 distractor 436,363.64 = r + g instead of r - g", 48000 / 0.11, 436363.64)
chk("Q16 distractor 988,800 = first payment grown once more",
    48000 * 1.03 / 0.05, 988800.00, tol=0.5)
chk_exact("Q16 r > g, so the formula is allowed", 0.08 > 0.03, True)
chk_exact("Q16 sanity: growing perpetuity worth more than the plain one",
          48000 / 0.05 > 48000 / 0.08, True)

# ======================================================================
# Q19 PAYOFF — inverse to the senior face value
#     V_T = 140 · junior owed 50, receives 32 · equity 0
# ======================================================================
VT19, FJ19, junpay19 = 140.0, 50.0, 32.0
FS19 = VT19 - junpay19 - 0.0
chk("Q19 CORRECT F_S from the adding-up rule", FS19, 108.0)
chk("Q19 second border F_S + F_J", FS19 + FJ19, 158.0)
chk("Q19 junior check Min(140 - 108, 50)", min(VT19 - FS19, FJ19), 32.0)
chk("Q19 equity check Max(140 - 158, 0)", max(VT19 - FS19 - FJ19, 0.0), 0.0)
chk("Q19 payoffs sum to exactly V_T",
    min(VT19, FS19) + min(VT19 - FS19, FJ19) + max(VT19 - FS19 - FJ19, 0.0), VT19)
chk_exact("Q19 V_T really sits in state II", FS19 <= VT19 < FS19 + FJ19, True)
chk("Q19 junior shortfall 50 - 32", FJ19 - junpay19, 18.0)
chk("Q19 distractor 90 = 140 - 50", VT19 - FJ19, 90.0)
chk("Q19 distractor 58 = 140 - 50 - 32", VT19 - FJ19 - junpay19, 58.0)

# ======================================================================
# Q20 NPV AND IRR — cost 12,000 · 4,500 for 4 years · r = 9%
# ======================================================================
chk("Q20 growth factor 1.09^4", 1.09 ** 4, 1.411582, tol=5e-7)
chk("Q20 annuity factor af(9%,4)", af(0.09, 4), 3.239720, tol=5e-7)
pv20 = 4500 * af(0.09, 4)
chk("Q20 PV of the inflows", pv20, 14578.74)
chk("Q20 CORRECT NPV", pv20 - 12000, 2578.74)
chk("Q20 distractor 6,000 = undiscounted 4 x 4,500 - 12,000",
    4 * 4500 - 12000, 6000.0)
chk("Q20 distractor 14,578.74 = PV of inflows, cost never subtracted",
    pv20, 14578.74)

# the claim that the IRR is above 9 percent: solve NPV = 0 by bisection
lo_r, hi_r = 0.0001, 1.0


def npv20(r):
    return 4500 * af(r, 4) - 12000


for _ in range(200):
    mid = (lo_r + hi_r) / 2
    if npv20(mid) > 0:
        lo_r = mid
    else:
        hi_r = mid
irr20 = (lo_r + hi_r) / 2
chk("Q20 IRR of the project (solved)", irr20, 0.1848, tol=5e-4)
chk_exact("Q20 claim: IRR is above the required 9 percent", irr20 > 0.09, True)
chk("Q20 check: NPV at the IRR is zero", npv20(irr20), 0.0, tol=1e-6)

# ======================================================================
# Q21 BONDS — rate falls, premium bond
#     par 1,000 · coupon rate 5% · n = 8 · new yield 4% (was 7%)
# ======================================================================
chk("Q21 coupon payment 0.05 x 1,000", 0.05 * 1000, 50.0)
chk("Q21 growth factor 1.04^8", 1.04 ** 8, 1.368569, tol=5e-7)
chk("Q21 annuity factor af(4%,8)", af(0.04, 8), 6.732745, tol=5e-7)
chk("Q21 PV of coupons", 50 * af(0.04, 8), 336.64)
chk("Q21 PV of par", 1000 / 1.04 ** 8, 730.69)
chk("Q21 CORRECT new price", bond_price(1000, 0.05, 8, 0.04), 1067.33)
chk("Q21 pieces add to the printed price",
    r2(50 * af(0.04, 8)) + r2(1000 / 1.04 ** 8), 1067.33)
chk("Q21 distractor 880.57 = the old price at 7%",
    bond_price(1000, 0.05, 8, 0.07), 880.57)
chk("Q21 distractor 1,000.00 = discounted at the 5% coupon rate",
    bond_price(1000, 0.05, 8, 0.05), 1000.00)
chk("Q21 distractor 336.64 = coupons only", 50 * af(0.04, 8), 336.64)
chk_exact("Q21 the price rose when the required rate fell",
          bond_price(1000, 0.05, 8, 0.04) > bond_price(1000, 0.05, 8, 0.07), True)
chk_exact("Q21 it is now a premium bond",
          bond_price(1000, 0.05, 8, 0.04) > 1000, True)

# ======================================================================
# The five reproduced course-quiz items: the professor's own answer key
# Source: Finance_Classification_Quiz.pptx, slide 12 "Answer Key".
# Only questions 6 to 10 are used on this page. Questions 1 to 5 are reserved
# for Mock 1 and are not reproduced here.
# ======================================================================
PROF_KEY = {6: "E", 7: "D", 8: "F", 9: "B", 10: "E"}
LETTERS = ["A", "B", "C", "D", "E", "F"]

# what day-13.html sets, as (course question number, page item number, correct index)
PAGE_KEY = [
    (6, 2, 4),    # student: subsidized loan vs private bank loan
    (7, 7, 3),    # founder: LLC vs sole proprietor
    (8, 12, 5),   # town: public private partnership
    (9, 17, 1),   # firm: dividend vs retained earnings
    (10, 22, 4),  # household: municipal bonds
]
for qnum, item_no, idx in PAGE_KEY:
    letter = LETTERS[idx]
    ok = (letter == PROF_KEY[qnum])
    CHECKS.append((
        "Course quiz Q%d (page item %d): page says %s, professor's key says %s"
        % (qnum, item_no, letter, PROF_KEY[qnum]),
        letter, PROF_KEY[qnum], ok))

# ======================================================================
# Structural checks on the page itself
# ======================================================================
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "..", "day-13.html")
html = open(PAGE, encoding="utf-8").read()

n_items = len(re.findall(r'^\s*q:\s*"', html, re.M))
CHECKS.append(("Page holds 22 questions", n_items, 22, n_items == 22))

mins = re.search(r"minutes:\s*(\d+)", html)
mv = int(mins.group(1)) if mins else -1
CHECKS.append(("Timer set to 150 minutes", mv, 150, mv == 150))

tags = re.findall(r'tag:\s*"([^"]+)"', html)
ALLOWED = {"Concepts", "Single cash flow", "Annuity", "Perpetuity",
           "Mixed stream", "Bonds", "Payoff structure", "Stocks", "NPV and IRR"}
bad = sorted(set(tags) - ALLOWED)
CHECKS.append(("Every tag is one of the nine allowed", bad, [], bad == []))

counts = {t: tags.count(t) for t in sorted(set(tags))}
for topic, want in [("Bonds", 7), ("Payoff structure", 5), ("Concepts", 5),
                    ("Stocks", 1), ("NPV and IRR", 1)]:
    got = counts.get(topic, 0)
    CHECKS.append(("Tag count, %s" % topic, got, want, got == want))
tvm = sum(counts.get(t, 0) for t in
          ("Single cash flow", "Annuity", "Perpetuity", "Mixed stream"))
CHECKS.append(("Tag count, time value of money (four tags together)", tvm, 3, tvm == 3))

srcs = re.findall(r'src:\s*"([^"]+)"', html)
CHECKS.append(("Exactly five items carry a src tag", len(srcs), 5, len(srcs) == 5))
CHECKS.append(('Every src reads "From a course quiz"',
               sorted(set(srcs)), ["From a course quiz"],
               sorted(set(srcs)) == ["From a course quiz"]))
CHECKS.append(('No item claims to come from a past final',
               "past final" in html.lower(), False,
               "past final" not in html.lower()))

corrects = [int(c) for c in re.findall(r"correct:\s*(\d+)", html)]
spread = len(set(corrects))
CHECKS.append(("Correct answers are spread over several positions",
               spread, ">= 3", spread >= 3))

# em dash must not appear anywhere in learner-facing copy
CHECKS.append(("No em dash on the page", html.count("\u2014"), 0,
               html.count("\u2014") == 0))

# the mock engine must be the only quiz mount, and the shared files must be linked
CHECKS.append(("Uses POF.mock, not POF.quiz",
               "POF.mock(" in html and "POF.quiz(" not in html, True,
               "POF.mock(" in html and "POF.quiz(" not in html))
CHECKS.append(("Links assets/theme.css", 'href="assets/theme.css"' in html, True,
               'href="assets/theme.css"' in html))
CHECKS.append(("Links assets/study.js", 'src="assets/study.js"' in html, True,
               'src="assets/study.js"' in html))

# every payoff item must obey: payoffs sum to V_T, equity never negative
PAYOFFS = [
    ("Q3", 118.0, 85.0, 60.0),
    ("Q6", 340.0, 210.0, 99.0),
    ("Q10", 38.0, 62.0, 30.0),
    ("Q14", 96.0, 96.0, 40.0),
    ("Q19", 140.0, 108.0, 50.0),
]
for name, v, fs, fj in PAYOFFS:
    s = min(v, fs)
    j = 0.0 if v < fs else min(v - fs, fj)
    e = max(v - fs - fj, 0.0)
    chk("%s global rule: senior + junior + equity = V_T" % name, s + j + e, v)
    chk_exact("%s global rule: equity is never negative" % name, e >= 0, True)
    chk_exact("%s global rule: senior never paid more than F_S" % name, s <= fs, True)
    chk_exact("%s global rule: junior never paid more than F_J" % name, j <= fj, True)

# the three states must all appear, and the boundary case must be present
states = []
for name, v, fs, fj in PAYOFFS:
    if v < fs:
        states.append("I")
    elif v < fs + fj:
        states.append("II")
    else:
        states.append("III")
CHECKS.append(("All three payoff states appear", sorted(set(states)),
               ["I", "II", "III"], sorted(set(states)) == ["I", "II", "III"]))
CHECKS.append(("A boundary case with V_T exactly at F_S appears",
               any(v == fs for _, v, fs, _ in PAYOFFS), True,
               any(v == fs for _, v, fs, _ in PAYOFFS)))

# a premium bond and a discount bond must both appear
prem = bond_price(2000, 0.07, 6, 0.05) > 2000
disc = bond_price(1000, 0.03, 7, 0.065) < 1000
par = bond_price(5000, 0.064, 9, 0.064) == 5000
CHECKS.append(("A premium bond appears (Q1)", prem, True, prem))
CHECKS.append(("A discount bond appears (Q5)", disc, True, disc))
CHECKS.append(("A bond trading exactly at par appears (Q8)", par, True, par))

# ----------------------------------------------------------------------
# report
# ----------------------------------------------------------------------
print("=" * 78)
print("verify/day-13.py  —  Day 13, Mock 3")
print("=" * 78)
fails = 0
for label, computed, page, ok in CHECKS:
    if not ok:
        fails += 1
    if isinstance(computed, float):
        cs = "%.6f" % computed
    else:
        cs = str(computed)
    ps = "%.6f" % page if isinstance(page, float) else str(page)
    print("%-62s computed %-16s page %-16s %s"
          % (label[:62], cs, ps, "PASS" if ok else "FAIL"))

print("-" * 78)
print("%d numbers and rules checked, %d passed, %d failed"
      % (len(CHECKS), len(CHECKS) - fails, fails))
sys.exit(1 if fails else 0)
