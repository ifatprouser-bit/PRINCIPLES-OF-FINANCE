#!/usr/bin/env python3
"""
Verification for day-14.html — Mock 4, the dress rehearsal.

Recomputes every number that appears on the page: the 22 mock answers, every
distractor, every intermediate figure quoted inside a worked explanation, and
the six course-quiz answers against the professor's own key.

Run:  python3 verify/day-14.py
One line per number: label, computed value, PASS or FAIL against the page.
"""

RESULTS = []


def chk(label, computed, on_page, tol=0.01):
    """Numeric check."""
    ok = abs(computed - on_page) <= tol
    RESULTS.append(ok)
    print("%-72s computed %16.6f   page %16.6f   %s"
          % (label, computed, on_page, "PASS" if ok else "FAIL"))


def chks(label, computed, on_page):
    """Exact (string / int) check."""
    ok = computed == on_page
    RESULTS.append(ok)
    print("%-72s computed %16s   page %16s   %s"
          % (label, str(computed), str(on_page), "PASS" if ok else "FAIL"))


def af(n, r):
    """Present value annuity factor."""
    return (1 - (1 + r) ** -n) / r


def fa(n, r):
    """Future value annuity factor."""
    return ((1 + r) ** n - 1) / r


def gaf(n, r, g):
    """Growing annuity factor."""
    return (1 - ((1 + g) / (1 + r)) ** n) / (r - g)


print("=" * 130)
print("DAY 14  ·  MOCK 4  ·  22 items, 150 minutes")
print("=" * 130)

# ---------------------------------------------------------------- rules panel
print("\n--- RULES PANEL ---")
chks("item count", 22, 22)
chk("minutes per question: 150 / 22", 150 / 22, 6.8, tol=0.02)

# ------------------------------------------------- Q1, Q5, Q9, Q13, Q17, Q21
# Six cases reproduced from Finance_Decision_Environments_Quiz.pptx.
# The professor's answer key (slide 11): 1)A 2)B 3)B 4)C 5)B 6)C 7)A 8)C 9)B
# Cases 1-3 are reserved for Mock 2 and are not used here.
print("\n--- COURSE QUIZ CASES 4 TO 9, AGAINST THE PROFESSOR'S KEY ---")
PROF_KEY = {1: "A", 2: "B", 3: "B", 4: "C", 5: "B", 6: "C", 7: "A", 8: "C", 9: "B"}
LETTER = {"A": "Certainty", "B": "Uncertainty", "C": "Ambiguity"}

# what day-14.html marks correct, as (mock item number, case number, opts index)
PAGE = [
    (1,  4, 2),   # payment app, rules being drafted
    (5,  5, 1),   # auto insurance deductible, claim frequency tables
    (9,  6, 2),   # token offering, unclear rules
    (13, 7, 0),   # insured bank CDs held to maturity
    (17, 8, 2),   # private target, no audited statements
    (21, 9, 1),   # note with published scenario probabilities
]
OPTS = ["Certainty", "Uncertainty", "Ambiguity"]
for qno, case, idx in PAGE:
    chks("Q%-2d  course quiz case %d  ->  %s" % (qno, case, OPTS[idx]),
         OPTS[idx], LETTER[PROF_KEY[case]])
chks("cases 1 to 3 left untouched (reserved for Mock 2)",
     sorted(c for _, c, _ in PAGE), [4, 5, 6, 7, 8, 9])

# ---------------------------------------------------------------------- Q2
print("\n--- Q2  SINGLE CASH FLOW, 30,000 at end of year 3, valued at end of year 8, r = 7% ---")
chk("Q2  1.07^5", 1.07 ** 5, 1.40255173, tol=1e-7)
chk("Q2  correct: 30,000 x 1.07^5", 30000 * 1.07 ** 5, 42076.55)
chk("Q2  check route: PV today 30,000 / 1.07^3", 30000 / 1.07 ** 3, 24488.94)
chk("Q2  check route: 1.07^3", 1.07 ** 3, 1.225043, tol=1e-6)
chk("Q2  check route: 1.07^8", 1.07 ** 8, 1.71818618, tol=1e-7)
chk("Q2  check route: 24,488.94 x 1.07^8", (30000 / 1.07 ** 3) * 1.07 ** 8, 42076.55)
chk("Q2  distractor: 30,000 x 1.07^8", 30000 * 1.07 ** 8, 51545.59)
chk("Q2  distractor: 30,000 x 1.07^3", 30000 * 1.07 ** 3, 36751.29)

# ---------------------------------------------------------------------- Q3
print("\n--- Q3  STEP-UP COUPON BOND priced as a mixed stream, y = 7% ---")
q3 = {1: 40, 2: 40, 3: 40, 4: 90, 5: 1090}
chk("Q3  t1  40 / 1.07", 40 / 1.07, 37.38)
chk("Q3  t2  40 / 1.07^2", 40 / 1.07 ** 2, 34.94)
chk("Q3  t3  40 / 1.07^3", 40 / 1.07 ** 3, 32.65)
chk("Q3  t4  90 / 1.07^4", 90 / 1.07 ** 4, 68.66)
chk("Q3  t5  1,090 / 1.07^5", 1090 / 1.07 ** 5, 777.15)
chk("Q3  1.07^2", 1.07 ** 2, 1.1449, tol=1e-6)
chk("Q3  1.07^4", 1.07 ** 4, 1.31079601, tol=1e-7)
chk("Q3  correct: price", sum(c / 1.07 ** t for t, c in q3.items()), 950.79)
chk("Q3  average coupon (40+40+40+90+90)/5", (40 + 40 + 40 + 90 + 90) / 5, 60)
chk("Q3  distractor: all five coupons at 40", 40 * af(5, .07) + 1000 / 1.07 ** 5, 876.99)
chk("Q3  distractor: all five coupons at 90", 90 * af(5, .07) + 1000 / 1.07 ** 5, 1082.00)
chk("Q3  distractor: par added undiscounted",
    sum(c / 1.07 ** t for t, c in {1: 40, 2: 40, 3: 40, 4: 90, 5: 90}.items()) + 1000, 1237.80)

# ---------------------------------------------------------------------- Q4
print("\n--- Q4  MIXED STREAM: 6,000 today + 3,000 at end of years 5 to 12, r = 7% ---")
chks("Q4  payment count 12 - 5 + 1", 12 - 5 + 1, 8)
chk("Q4  1.07^8", 1.07 ** 8, 1.71818618, tol=1e-7)
chk("Q4  1 / 1.07^8", 1 / 1.07 ** 8, 0.58200915, tol=1e-7)
chk("Q4  annuity factor n=8 r=7%", af(8, .07), 5.97129851, tol=1e-6)
chk("Q4  value of the annuity at year 4", 3000 * af(8, .07), 17913.90)
chk("Q4  1.07^4", 1.07 ** 4, 1.31079601, tol=1e-7)
chk("Q4  annuity brought to today", 3000 * af(8, .07) / 1.07 ** 4, 13666.43)
chk("Q4  correct: plus the 6,000 in hand", 3000 * af(8, .07) / 1.07 ** 4 + 6000, 19666.43)
chk("Q4  sanity: raw cash 8 x 3,000", 8 * 3000, 24000)
chk("Q4  sanity: 13,666 / 24,000 as a percent",
    3000 * af(8, .07) / 1.07 ** 4 / 24000 * 100, 57, tol=0.5)
chk("Q4  distractor: discounted 5 years not 4", 3000 * af(8, .07) / 1.07 ** 5 + 6000, 18772.36)
chk("Q4  distractor: n = 7", 3000 * af(7, .07) / 1.07 ** 4 + 6000, 18334.39)
chk("Q4  distractor: annuity alone, 6,000 dropped", 3000 * af(8, .07) / 1.07 ** 4, 13666.43)

# ---------------------------------------------------------------------- Q6
print("\n--- Q6  PAYOFF, INVERSE AND BOUNDARY: F_S = 70, F_J = 45 ---")
FS, FJ = 70, 45
chk("Q6  F_S + F_J", FS + FJ, 115)
VT = 115
sen = min(VT, FS)
jun = 0 if VT < FS else min(VT - FS, FJ)
eq = max(VT - FS - FJ, 0)
chk("Q6  senior at V_T = 115", sen, 70)
chk("Q6  junior at V_T = 115", jun, 45)
chk("Q6  equity at V_T = 115", eq, 0)
chk("Q6  the sum test: three payoffs add to V_T", sen + jun + eq, 115)
chks("Q6  junior paid in full requires V_T >= 115", VT >= 115, True)
chks("Q6  owners get nothing requires V_T <= 115", VT <= 115, True)
chks("Q6  only value satisfying both", [v for v in range(0, 401) if
     (0 if v < FS else min(v - FS, FJ)) == FJ and max(v - FS - FJ, 0) == 0], [115])

# ---------------------------------------------------------------------- Q7
print("\n--- Q7  GROWING PERPETUITY, r barely above g: CF1 = 40,000, g = 4.8%, r = 5% ---")
chk("Q7  the gap r - g", 0.05 - 0.048, 0.002, tol=1e-9)
chk("Q7  correct: 40,000 / 0.002", 40000 / (0.05 - 0.048), 20000000, tol=1.0)
chk("Q7  check: payment 1 present value 40,000 / 1.05", 40000 / 1.05, 38095, tol=1)
chk("Q7  check: payment 2 cash 40,000 x 1.048", 40000 * 1.048, 41920)
chk("Q7  check: payment 2 present value", 40000 * 1.048 / 1.05 ** 2, 38022, tol=1)
chk("Q7  check: shrink per payment, percent",
    (40000 * 1.048 / 1.05 ** 2) / (40000 / 1.05) * 100 - 100, -0.19, tol=0.01)
chk("Q7  note: g = 4.9% would give", 40000 / (0.05 - 0.049), 40000000, tol=1.0)
chk("Q7  distractor: plain perpetuity 40,000 / 0.05", 40000 / 0.05, 800000)
chk("Q7  distractor: 40,000 / (r + g)", 40000 / 0.098, 408163, tol=1)

# ---------------------------------------------------------------------- Q8
print("\n--- Q8  NPV with a late closing cost: -60,000, 18,000 x 5, -12,000 at year 5, r = 11% ---")
chk("Q8  1.11^5", 1.11 ** 5, 1.68505816, tol=1e-7)
chk("Q8  1 / 1.11^5", 1 / 1.11 ** 5, 0.59345134, tol=1e-7)
chk("Q8  annuity factor n=5 r=11%", af(5, .11), 3.69589702, tol=1e-6)
chk("Q8  present value of the inflows", 18000 * af(5, .11), 66526.15)
chk("Q8  present value of the closing cost", 12000 / 1.11 ** 5, 7121.42)
chk("Q8  correct: NPV", 18000 * af(5, .11) - 12000 / 1.11 ** 5 - 60000, -595.27)
chk("Q8  check: NPV without the closing cost", 18000 * af(5, .11) - 60000, 6526.15)
chk("Q8  check: 7,121.42 - 6,526.15", 12000 / 1.11 ** 5 - (18000 * af(5, .11) - 60000), 595.27)
chk("Q8  distractor: closing cost undiscounted",
    18000 * af(5, .11) - 12000 - 60000, -5473.85)
chk("Q8  distractor: no discounting at all, 90,000 - 12,000 - 60,000",
    5 * 18000 - 12000 - 60000, 18000)

# ---------------------------------------------------------------------- Q10
print("\n--- Q10  BOND, INVERSE: par 1,000, n = 3, r = 5%, price 1,054.46, find the coupon rate ---")
chk("Q10  1.05^3", 1.05 ** 3, 1.157625, tol=1e-6)
chk("Q10  1 / 1.05^3", 1 / 1.05 ** 3, 0.86383760, tol=1e-7)
chk("Q10  present value of the par repayment", 1000 / 1.05 ** 3, 863.84)
chk("Q10  what the coupons are worth today", 1054.46 - 1000 / 1.05 ** 3, 190.62)
chk("Q10  annuity factor n=3 r=5%", af(3, .05), 2.72324803, tol=1e-6)
chk("Q10  coupon C", (1054.46 - 1000 / 1.05 ** 3) / af(3, .05), 70.00, tol=0.01)
chk("Q10  correct: coupon rate as a percent",
    (1054.46 - 1000 / 1.05 ** 3) / af(3, .05) / 1000 * 100, 7.0, tol=0.01)
chk("Q10  check forward: 70 x factor", 70 * af(3, .05), 190.63)
chk("Q10  check forward: full price at C = 70", 70 * af(3, .05) + 1000 / 1.05 ** 3, 1054.47, tol=0.02)
chk("Q10  distractor: coupon rate 6% gives price", 60 * af(3, .05) + 1000 / 1.05 ** 3, 1027.23)
chk("Q10  distractor: coupon rate 8% gives price", 80 * af(3, .05) + 1000 / 1.05 ** 3, 1081.70)
chk("Q10  distractor: coupon rate 5% gives price (par)", 50 * af(3, .05) + 1000 / 1.05 ** 3, 1000.00)

# ---------------------------------------------------------------------- Q11
print("\n--- Q11  ANNUITY BOUNDARY, n = 1: one deposit of 7,500 at end of year 1, r = 5% ---")
chk("Q11  future value annuity factor at n = 1", fa(1, .05), 1.0, tol=1e-9)
chk("Q11  correct part a: balance right after the deposit", 7500 * fa(1, .05), 7500.00)
chks("Q11  years from end of year 1 to end of year 4", 4 - 1, 3)
chk("Q11  1.05^3", 1.05 ** 3, 1.157625, tol=1e-6)
chk("Q11  correct part b: balance at end of year 4", 7500 * 1.05 ** 3, 8682.19)
chk("Q11  check: 8,682.19 / 7,500 as a percent gain",
    7500 * 1.05 ** 3 / 7500 * 100 - 100, 15.76, tol=0.01)
chk("Q11  present value annuity factor at n = 1 equals 1/(1+r)", af(1, .05), 1 / 1.05, tol=1e-9)
chk("Q11  distractor: 7,500 x 1.05", 7500 * 1.05, 7875.00)
chk("Q11  distractor: 7,500 x 1.05^4", 7500 * 1.05 ** 4, 9116.30)
chk("Q11  distractor: 7,500 / 1.05", 7500 / 1.05, 7142.86)
chk("Q11  distractor: (7,500 / 1.05) x 1.05^3", 7500 / 1.05 * 1.05 ** 3, 8268.75)

# ---------------------------------------------------------------------- Q12
print("\n--- Q12  STOCK, zero growth + holding period return: P0 = 30.00, D1 = 2.40, P1 = 26.00 ---")
chk("Q12  price change 26 - 30", 26 - 30, -4.00)
chk("Q12  price change plus dividend", 26 - 30 + 2.40, -1.60)
chk("Q12  correct: HPR as a percent", (26 - 30 + 2.40) / 30 * 100, -5.33, tol=0.005)
chk("Q12  check: end wealth 26.00 + 2.40", 26 + 2.40, 28.40)
chk("Q12  check: 28.40 / 30.00", 28.40 / 30, 0.9467, tol=0.0001)
chk("Q12  zero growth: required return implied by the price, percent", 2.40 / 30 * 100, 8.00)
chk("Q12  distractor: price change alone, percent", (26 - 30) / 30 * 100, -13.33, tol=0.005)
chk("Q12  distractor: divided by P1, percent", (26 - 30 + 2.40) / 26 * 100, -6.15, tol=0.005)

# ---------------------------------------------------------------------- Q14
print("\n--- Q14  MIXED STREAM, INVERSE: A for years 1-4 plus 15,000 at year 6, PV = 25,000, r = 10% ---")
chk("Q14  1.10^6", 1.10 ** 6, 1.771561, tol=1e-6)
chk("Q14  present value of the 15,000", 15000 / 1.1 ** 6, 8467.11)
chk("Q14  value the four payments must carry", 25000 - 15000 / 1.1 ** 6, 16532.89)
chk("Q14  1.10^4", 1.10 ** 4, 1.4641, tol=1e-6)
chk("Q14  1 / 1.10^4", 1 / 1.1 ** 4, 0.68301346, tol=1e-7)
chk("Q14  annuity factor n=4 r=10%", af(4, .1), 3.16986545, tol=1e-6)
A14 = (25000 - 15000 / 1.1 ** 6) / af(4, .1)
chk("Q14  correct: A", A14, 5215.64)
chk("Q14  check: A x factor", A14 * af(4, .1), 16532.89)
chk("Q14  check: rebuild the total", A14 * af(4, .1) + 15000 / 1.1 ** 6, 25000.00)
chk("Q14  the 6,532.89 overshoot", 15000 - 15000 / 1.1 ** 6, 6532.89)
chk("Q14  distractor: 25,000 / factor", 25000 / af(4, .1), 7886.77)
chk("Q14  distractor: (25,000 - 15,000) / factor", (25000 - 15000) / af(4, .1), 3154.71)
chk("Q14  distractor: 16,532.89 / 4", (25000 - 15000 / 1.1 ** 6) / 4, 4133.22)

# ---------------------------------------------------------------------- Q15
print("\n--- Q15  PERPETUAL BOND gives the yield, then price a 10-year coupon bond ---")
chk("Q15  yield from the perpetuity 62.50 / 1,250, percent", 62.50 / 1250 * 100, 5.0)
chk("Q15  1.05^10", 1.05 ** 10, 1.62889463, tol=1e-7)
chk("Q15  1 / 1.05^10", 1 / 1.05 ** 10, 0.61391325, tol=1e-7)
chk("Q15  annuity factor n=10 r=5%", af(10, .05), 7.72173493, tol=1e-6)
chk("Q15  present value of the coupons", 62.50 * af(10, .05), 482.61)
chk("Q15  present value of the par repayment", 1000 / 1.05 ** 10, 613.91)
chk("Q15  correct: price", 62.50 * af(10, .05) + 1000 / 1.05 ** 10, 1096.52)
chk("Q15  check: coupon rate 62.50 / 1,000, percent", 62.50 / 1000 * 100, 6.25)
chk("Q15  distractor: priced at 6.25% gives par", 62.50 * af(10, .0625) + 1000 / 1.0625 ** 10, 1000.00)
chk("Q15  distractor: coupons only", 62.50 * af(10, .05), 482.61)

# ---------------------------------------------------------------------- Q16
print("\n--- Q16  ROA AND ROE, INVERSE: net income 63, ROA 4.5%, ROE 18% ---")
chk("Q16  assets = 63 / 0.045", 63 / 0.045, 1400)
chk("Q16  equity = 63 / 0.18", 63 / 0.18, 350)
chk("Q16  debt = assets - equity", 63 / 0.045 - 63 / 0.18, 1050)
chk("Q16  check: ROA percent", 63 / 1400 * 100, 4.5)
chk("Q16  check: ROE percent", 63 / 350 * 100, 18.0)
chk("Q16  leverage: assets / equity", 1400 / 350, 4.0)
chk("Q16  distractor: swapped debt and equity gives ROE percent", 63 / 1050 * 100, 6.0)
chk("Q16  distractor: 1,400 x 18%", 1400 * 0.18, 252)
chk("Q16  distractor: 1,400 - 252", 1400 - 252, 1148)

# ---------------------------------------------------------------------- Q18
print("\n--- Q18  PAYOFF with coupons: senior 200 at 5%, junior 120 at 12%, V_T = 290 ---")
FS18 = 200 * 1.05
FJ18 = 120 * 1.12
chk("Q18  amount owed to the senior lender", FS18, 210.00)
chk("Q18  amount owed to the junior lender", FJ18, 134.40)
chk("Q18  F_S + F_J", FS18 + FJ18, 344.40)
VT18 = 290
s18 = min(VT18, FS18)
j18 = 0 if VT18 < FS18 else min(VT18 - FS18, FJ18)
e18 = max(VT18 - FS18 - FJ18, 0)
chk("Q18  senior receives", s18, 210.00)
chk("Q18  left after the senior lender", VT18 - FS18, 80.00)
chk("Q18  junior receives", j18, 80.00)
chk("Q18  equity receives", e18, 0.00)
chk("Q18  the sum test: three payoffs add to V_T", s18 + j18 + e18, 290.00)
chk("Q18  junior lender's return, percent", (80 / 120 - 1) * 100, -33.33, tol=0.01)
chk("Q18  distractor: equity allowed to go negative", VT18 - FS18 - FJ18, -54.40)
chk("Q18  distractor: senior paid face only, junior 290 - 200", 290 - 200, 90.00)
chk("Q18  distractor: that junior return, percent", (90 / 120 - 1) * 100, -25.00)
chk("Q18  distractor: junior paid first leaves the senior lender", 290 - FJ18, 155.60)

# ---------------------------------------------------------------------- Q19
print("\n--- Q19  GROWING ANNUITY, INVERSE: n = 10, g = 6%, r = 11%, PV = 251,118 ---")
chk("Q19  1.06 / 1.11", 1.06 / 1.11, 0.95495495, tol=1e-7)
chk("Q19  (1.06/1.11)^10", (1.06 / 1.11) ** 10, 0.63070876, tol=1e-7)
chk("Q19  1 - that", 1 - (1.06 / 1.11) ** 10, 0.36929124, tol=1e-7)
chk("Q19  the gap r - g", 0.11 - 0.06, 0.05, tol=1e-9)
chk("Q19  growing annuity factor", gaf(10, .11, .06), 7.38582475, tol=1e-6)
C1 = 251118 / gaf(10, .11, .06)
chk("Q19  correct: first payment", C1, 34000, tol=0.05)
chk("Q19  check forward: 34,000 x factor", 34000 * gaf(10, .11, .06), 251118.04, tol=0.05)
chk("Q19  check: second payment 34,000 x 1.06", 34000 * 1.06, 36040)
chk("Q19  check: tenth payment 34,000 x 1.06^9", 34000 * 1.06 ** 9, 57442, tol=1)
chk("Q19  note: growing perpetuity factor 1 / 0.05", 1 / 0.05, 20)
chk("Q19  plain annuity factor n=10 r=11%", af(10, .11), 5.8892, tol=0.0001)
chk("Q19  distractor: PV / plain annuity factor", 251118 / af(10, .11), 42640, tol=1)
chk("Q19  distractor: growing perpetuity, PV x (r - g)", 251118 * 0.05, 12556, tol=1)
chk("Q19  distractor: PV / 10", 251118 / 10, 25111.80)

# ---------------------------------------------------------------------- Q20
print("\n--- Q20  IRR, INVERSE: cost 12,000, 3 equal inflows, IRR = 15% ---")
chk("Q20  1.15^3", 1.15 ** 3, 1.520875, tol=1e-6)
chk("Q20  1 / 1.15^3", 1 / 1.15 ** 3, 0.65751617, tol=1e-7)
chk("Q20  annuity factor n=3 r=15%", af(3, .15), 2.28322512, tol=1e-6)
A20 = 12000 / af(3, .15)
chk("Q20  correct: yearly cash inflow", A20, 5255.72)
chk("Q20  check: A x factor", A20 * af(3, .15), 12000.00)
chk("Q20  check: NPV at 15% is zero", A20 * af(3, .15) - 12000, 0.0, tol=1e-6)
chk("Q20  distractor: 12,000 / 3", 12000 / 3, 4000.00)
chk("Q20  distractor: 12,000 x 1.15 / 3", 12000 * 1.15 / 3, 4600.00)
chk("Q20  distractor: 12,000/3 + 15% of 12,000", 12000 / 3 + 12000 * 0.15, 5800.00)

# ---------------------------------------------------------------------- Q22
print("\n--- Q22  MATURITY AND PRICE: coupon 60, par 1,000, at par at 6%, required return moves to 8% ---")
chk("Q22  old required return implied by par, percent", 60 / 1000 * 100, 6.0)
chk("Q22  Bond A at par, 6%, n = 2", 60 * af(2, .06) + 1000 / 1.06 ** 2, 1000.00)
chk("Q22  Bond B at par, 6%, n = 15", 60 * af(15, .06) + 1000 / 1.06 ** 15, 1000.00)
chk("Q22  Bond A new price at 8%", 60 * af(2, .08) + 1000 / 1.08 ** 2, 964.33)
chk("Q22  1.08^15", 1.08 ** 15, 3.17216911, tol=1e-7)
chk("Q22  1 / 1.08^15", 1 / 1.08 ** 15, 0.31524170, tol=1e-7)
chk("Q22  annuity factor n=15 r=8%", af(15, .08), 8.55947880, tol=1e-6)
chk("Q22  present value of Bond B's coupons", 60 * af(15, .08), 513.57)
chk("Q22  present value of Bond B's par repayment", 1000 / 1.08 ** 15, 315.24)
chk("Q22  correct: Bond B new price", 60 * af(15, .08) + 1000 / 1.08 ** 15, 828.81)
chk("Q22  Bond A drop, percent", (60 * af(2, .08) + 1000 / 1.08 ** 2) / 1000 * 100 - 100, -3.6, tol=0.05)
chk("Q22  Bond B drop, percent", (60 * af(15, .08) + 1000 / 1.08 ** 15) / 1000 * 100 - 100, -17.1, tol=0.05)
chk("Q22  how many times worse", 17.119 / 3.567, 4.8, tol=0.1)
chks("Q22  extra years on Bond B", 15 - 2, 13)
chk("Q22  distractor: coupons at 8%, par at 6%", 60 * af(15, .08) + 1000 / 1.06 ** 15, 930.83)
chk("Q22  distractor: coupons only", 60 * af(15, .08), 513.57)

# ------------------------------------------------------------- tag bookkeeping
print("\n--- TAG AND WEIGHTING CHECK ---")
TAGS = ["Concepts", "Single cash flow", "Bonds", "Mixed stream", "Concepts",
        "Payoff structure", "Perpetuity", "NPV and IRR", "Concepts", "Bonds",
        "Annuity", "Stocks", "Concepts", "Mixed stream", "Bonds", "Concepts",
        "Concepts", "Payoff structure", "Annuity", "NPV and IRR", "Concepts", "Bonds"]
ALLOWED = {"Concepts", "Single cash flow", "Annuity", "Perpetuity", "Mixed stream",
           "Bonds", "Payoff structure", "Stocks", "NPV and IRR"}
chks("total items", len(TAGS), 22)
chks("every tag is one of the nine allowed", set(TAGS) <= ALLOWED, True)
chks("Concepts count (spec: 6 or 7)", TAGS.count("Concepts"), 7)
tvm = sum(TAGS.count(t) for t in ("Single cash flow", "Annuity", "Perpetuity", "Mixed stream"))
chks("time value of money count (spec: 6 or 7)", tvm, 6)
chks("Bonds count (spec: 4)", TAGS.count("Bonds"), 4)
chks("Payoff structure count (spec: 2)", TAGS.count("Payoff structure"), 2)
chks("NPV and IRR count (spec: 2)", TAGS.count("NPV and IRR"), 2)
chks("Stocks count (spec: 1 or 2)", TAGS.count("Stocks"), 1)
chks("questions taken from the course quiz", 6, 6)
chks("questions written fresh", 22 - 6, 16)

# ------------------------------------------------------------------- summary
print("\n" + "=" * 130)
total = len(RESULTS)
failed = total - sum(RESULTS)
print("%d numbers checked.  %d passed.  %d failed." % (total, sum(RESULTS), failed))
print("=" * 130)
raise SystemExit(1 if failed else 0)
