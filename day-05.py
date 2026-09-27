#!/usr/bin/env python3
"""
verify/day-05.py — recompute every number printed on day-05.html (Mixed streams).

One line per number: label, computed value, PASS/FAIL against what the page says.
If a line FAILS, the page is wrong, not this script.

Run:  python3 verify/day-05.py
"""

CHECKS = []


def chk(label, computed, on_page, places=2):
    """Compare a computed value with the value written on the page."""
    ok = round(computed, places) == round(on_page, places)
    CHECKS.append(ok)
    print("%-62s computed %16.6f   page %16.6f   %s"
          % (label, computed, on_page, "PASS" if ok else "FAIL"))


def afac(r, n):
    """Present value factor of an ordinary annuity of 1 for n periods."""
    return (1 - (1 + r) ** -n) / r


def ffac(r, n):
    """Future value factor of an ordinary annuity of 1 for n periods."""
    return ((1 + r) ** n - 1) / r


def disc(x, r, t):
    return x / (1 + r) ** t


print("=" * 130)
print("DAY 5 — MIXED STREAMS — number check")
print("=" * 130)

# ---------------------------------------------------------------- recall box (day 3)
print("\n[RECALL BOX — day 3 annuity]")
chk("recall Q2 present value 1,000 x 3 years at 10%", 1000 * afac(.10, 3), 2486.85)
chk("recall Q2 future value at end of year 3", 1000 * ffac(.10, 3), 3310.00)
chk("recall Q2 cross check 2,486.85 x 1.10^3", 1000 * afac(.10, 3) * 1.10 ** 3, 3310.00)

# ---------------------------------------------------------------- panel 1 worked example
print("\n[PANEL 1 — worked example: annuity 2,000 years 1-4, single 9,000 year 5, r = 7%]")
chk("1.07^4", 1.07 ** 4, 1.310796, 6)
chk("1 / 1.07^4", 1 / 1.07 ** 4, 0.762895, 6)
chk("annuity factor (1 - 1.07^-4)/0.07", afac(.07, 4), 3.387211, 6)
chk("piece A: 2,000 x 3.387211", 2000 * afac(.07, 4), 6774.42)
chk("1.07^5", 1.07 ** 5, 1.402552, 6)
chk("piece B: 9,000 / 1.07^5", disc(9000, .07, 5), 6416.88)
chk("total present value", 2000 * afac(.07, 4) + disc(9000, .07, 5), 13191.30)
chk("sense check: total cash paid", 2000 * 4 + 9000, 17000.00)
print("     sense check: 13,191.30 < 17,000 ?", 2000 * afac(.07, 4) + disc(9000, .07, 5) < 17000)
print("     sense check: 13,191.30 > biggest piece 6,774.42 ?",
      2000 * afac(.07, 4) + disc(9000, .07, 5) > 2000 * afac(.07, 4))

# ---------------------------------------------------------------- panel 1 try-it
print("\n[PANEL 1 — try-it: annuity 650 years 1-3, single 6,000 year 3, r = 4%]")
chk("annuity factor (1 - 1.04^-3)/0.04", afac(.04, 3), 2.775091, 6)
chk("annuity piece 650 x 2.775091", 650 * afac(.04, 3), 1803.81)
chk("1.04^3", 1.04 ** 3, 1.124864, 6)
chk("single piece 6,000 / 1.04^3", disc(6000, .04, 3), 5333.98)
chk("try-it total", 650 * afac(.04, 3) + disc(6000, .04, 3), 7137.79)

# ---------------------------------------------------------------- panel 2 worked example
print("\n[PANEL 2 — worked example: 4,000 in years 4-7, r = 9%  (delayed annuity)]")
chk("1.09^4", 1.09 ** 4, 1.411582, 6)
chk("1 / 1.09^4", 1 / 1.09 ** 4, 0.708425, 6)
chk("annuity factor (1 - 1.09^-4)/0.09", afac(.09, 4), 3.239720, 6)
v3 = 4000 * afac(.09, 4)
chk("hop 1: value dated year 3", v3, 12958.88)
chk("1.09^3", 1.09 ** 3, 1.295029, 6)
chk("hop 2: value today", disc(v3, .09, 3), 10006.63)
chk("long way: 4,000 / 1.09^4", disc(4000, .09, 4), 2833.70)
chk("long way: 4,000 / 1.09^5", disc(4000, .09, 5), 2599.73)
chk("long way: 4,000 / 1.09^6", disc(4000, .09, 6), 2385.07)
chk("long way: 4,000 / 1.09^7", disc(4000, .09, 7), 2188.14)
chk("long way total equals the two-hop answer",
    sum(disc(4000, .09, t) for t in (4, 5, 6, 7)), 10006.63)
chk("size of the trap: 12,958.88 - 10,006.63", v3 - disc(v3, .09, 3), 2952.25)
pct = (v3 / disc(v3, .09, 3) - 1) * 100
print("%-62s computed %16.6f   page  'about 30 percent'  %s"
      % ("trap as a percentage of the right answer", pct, "PASS" if 28 <= pct <= 32 else "FAIL"))
CHECKS.append(28 <= pct <= 32)

# ---------------------------------------------------------------- panel 2 try-its
print("\n[PANEL 2 — try-it: 1,800 in years 3-8, r = 12%]")
chk("annuity factor (1 - 1.12^-6)/0.12", afac(.12, 6), 4.111407, 6)
v2 = 1800 * afac(.12, 6)
chk("hop 1: value dated year 2", v2, 7400.53)
chk("1.12^2", 1.12 ** 2, 1.2544, 4)
chk("hop 2: value today", disc(v2, .12, 2), 5899.66)
chk("size of the trap if you stop at hop 1", v2 - disc(v2, .12, 2), 1500.87)

print("\n[PANEL 2 — try-it: 2,200 in years 10-15, counting only]")
print("%-62s computed %16d   page %16d   %s"
      % ("number of payments n (years 10..15 inclusive)", len(range(10, 16)), 6,
         "PASS" if len(range(10, 16)) == 6 else "FAIL"))
CHECKS.append(len(range(10, 16)) == 6)
print("%-62s computed %16d   page %16d   %s"
      % ("year the annuity value lands in (10 - 1)", 10 - 1, 9, "PASS"))
CHECKS.append(10 - 1 == 9)

# ---------------------------------------------------------------- panel 3 worked example
print("\n[PANEL 3 — worked example: 1,000 yr 1; 2,500 yrs 3-7; 12,000 yr 8; r = 6%]")
chk("piece A: 1,000 / 1.06", disc(1000, .06, 1), 943.40)
chk("1.06^5", 1.06 ** 5, 1.338226, 6)
chk("1 / 1.06^5", 1 / 1.06 ** 5, 0.747258, 6)
chk("annuity factor (1 - 1.06^-5)/0.06", afac(.06, 5), 4.212364, 6)
b2 = 2500 * afac(.06, 5)
chk("piece B hop 1: value dated year 2", b2, 10530.91)
chk("1.06^2", 1.06 ** 2, 1.1236, 4)
chk("piece B hop 2: value today", disc(b2, .06, 2), 9372.47)
chk("1.06^8", 1.06 ** 8, 1.593848, 6)
chk("piece C: 12,000 / 1.06^8", disc(12000, .06, 8), 7528.95)
tot3 = disc(1000, .06, 1) + disc(b2, .06, 2) + disc(12000, .06, 8)
chk("total present value", tot3, 17844.82)
chk("sense check: total cash paid", 1000 + 2500 * 5 + 12000, 25500.00)
print("     sense check: 17,844.82 < 25,500 ?", tot3 < 25500)
print("     sense check: 17,844.82 > biggest piece 9,372.47 ?", tot3 > disc(b2, .06, 2))

# ---------------------------------------------------------------- panel 3 try-it (rate rises)
print("\n[PANEL 3 — try-it: the same stream at r = 9%]")
chk("piece A: 1,000 / 1.09", disc(1000, .09, 1), 917.43)
chk("annuity factor (1 - 1.09^-5)/0.09", afac(.09, 5), 3.889651, 6)
b29 = 2500 * afac(.09, 5)
chk("piece B hop 1: value dated year 2", b29, 9724.13)
chk("1.09^2", 1.09 ** 2, 1.1881, 4)
chk("piece B hop 2: value today", disc(b29, .09, 2), 8184.60)
chk("1.09^8", 1.09 ** 8, 1.992563, 6)
chk("piece C: 12,000 / 1.09^8", disc(12000, .09, 8), 6022.40)
tot4 = disc(1000, .09, 1) + disc(b29, .09, 2) + disc(12000, .09, 8)
chk("total present value at 9%", tot4, 15124.43)
print("     direction check: value falls when the rate rises ?", tot4 < tot3)
CHECKS.append(tot4 < tot3)

# ---------------------------------------------------------------- quiz item 1
print("\n[QUIZ 1 — 1,200 yr1; 900 yr2; 600 yrs 3-5; r = 5%]")
q1a, q1b = disc(1200, .05, 1), disc(900, .05, 2)
chk("single year 1: 1,200 / 1.05", q1a, 1142.86)
chk("1.05^2", 1.05 ** 2, 1.1025, 4)
chk("single year 2: 900 / 1.05^2", q1b, 816.33)
chk("annuity factor (1 - 1.05^-3)/0.05", afac(.05, 3), 2.723248, 6)
q1v2 = 600 * afac(.05, 3)
chk("hop 1: value dated year 2", q1v2, 1633.95)
chk("hop 2: value today", disc(q1v2, .05, 2), 1482.04)
chk("CORRECT ANSWER", q1a + q1b + disc(q1v2, .05, 2), 3441.22)
chk("distractor: cash added with no discounting", 1200 + 900 + 1800, 3900.00)
chk("distractor: stopped after hop 1", q1a + q1b + q1v2, 3593.13)
chk("distractor: annuity discounted 3 years not 2", q1a + q1b + disc(q1v2, .05, 3), 3370.65)

# ---------------------------------------------------------------- quiz item 2
print("\n[QUIZ 2 — 5,000 yrs 6-10; rate falls from 10% to 8%]")
chk("stated in the stem: value at 10%", disc(5000 * afac(.10, 5), .10, 5), 11768.90)
chk("1.08^5", 1.08 ** 5, 1.469328, 6)
chk("1 / 1.08^5", 1 / 1.08 ** 5, 0.680583, 6)
chk("annuity factor (1 - 1.08^-5)/0.08", afac(.08, 5), 3.992710, 6)
v5 = 5000 * afac(.08, 5)
chk("hop 1: value dated year 5", v5, 19963.55)
chk("CORRECT ANSWER: hop 2, value today at 8%", disc(v5, .08, 5), 13586.86)
chk("distractor: discounted 6 years not 5", disc(v5, .08, 6), 12580.42)
print("     direction check: value rises when the rate falls ?",
      disc(v5, .08, 5) > disc(5000 * afac(.10, 5), .10, 5))
CHECKS.append(disc(v5, .08, 5) > disc(5000 * afac(.10, 5), .10, 5))

# ---------------------------------------------------------------- quiz item 3
print("\n[QUIZ 3 — 400 forever, first payment year 4, r = 8%]")
p3 = 400 / .08
chk("hop 1: perpetuity value dated year 3", p3, 5000.00)
chk("1.08^3", 1.08 ** 3, 1.259712, 6)
chk("CORRECT ANSWER: hop 2, value today", disc(p3, .08, 3), 3969.16)
chk("check: 3,969.16 x 1.08^3 back to year 3", disc(p3, .08, 3) * 1.08 ** 3, 5000.00)
chk("check: 5,000 x 0.08 is the yearly payment", 5000 * .08, 400.00)
chk("distractor: discounted 4 years not 3", disc(p3, .08, 4), 3675.15)
chk("distractor: only the first payment, 400 / 1.08^4", disc(400, .08, 4), 294.01)

# ---------------------------------------------------------------- quiz item 4 (inverse)
print("\n[QUIZ 4 — inverse: 30,000 today, 8,000 yr 1, C in yrs 2-5, r = 9%]")
s1 = disc(8000, .09, 1)
chk("present value of the 8,000", s1, 7339.45)
rem = 30000 - s1
chk("what the annuity piece must be worth today", rem, 22660.55)
chk("the same value carried to year 1", rem * 1.09, 24700.00)
chk("annuity factor (1 - 1.09^-4)/0.09", afac(.09, 4), 3.239720, 6)
C = rem * 1.09 / afac(.09, 4)
chk("CORRECT ANSWER: C", C, 7624.12)
chk("check: full present value rebuilt from C", s1 + disc(C * afac(.09, 4), .09, 1), 30000.00)
chk("distractor: skipped the extra one-year move", rem / afac(.09, 4), 6994.60)
chk("distractor: 22,660.55 split four ways, no discounting", rem / 4, 5665.14)
chk("distractor: ignored the 8,000", 30000 * 1.09 / afac(.09, 4), 10093.47)

# ---------------------------------------------------------------- quiz item 5 (concept)
print("\n[QUIZ 5 — concept: 700 in years 7-12, where does the annuity value land]")
print("%-62s computed %16d   page %16d   %s"
      % ("payments in years 7..12, so n", len(range(7, 13)), 6,
         "PASS" if len(range(7, 13)) == 6 else "FAIL"))
CHECKS.append(len(range(7, 13)) == 6)
print("%-62s computed %16d   page %16d   %s"
      % ("value lands one period before year 7", 7 - 1, 6, "PASS"))
CHECKS.append(7 - 1 == 6)

# ---------------------------------------------------------------- quiz item 6
print("\n[QUIZ 6 — 3,500 yr1; 2,800 yr2; growing perpetuity 1,400 from yr3, g = 4%, r = 11%]")
g1, g2 = disc(3500, .11, 1), disc(2800, .11, 2)
chk("single year 1: 3,500 / 1.11", g1, 3153.15)
chk("1.11^2", 1.11 ** 2, 1.2321, 4)
chk("single year 2: 2,800 / 1.11^2", g2, 2272.54)
gp2 = 1400 / (.11 - .04)
chk("hop 1: growing perpetuity value dated year 2", gp2, 20000.00)
chk("hop 2: value today", disc(gp2, .11, 2), 16232.45)
tot6 = g1 + g2 + disc(gp2, .11, 2)
chk("CORRECT ANSWER", tot6, 21658.14)
share = disc(gp2, .11, 2) / tot6
print("%-62s computed %16.4f   page 'about three quarters'  %s"
      % ("growing perpetuity share of the total", share, "PASS" if 0.70 <= share <= 0.80 else "FAIL"))
CHECKS.append(0.70 <= share <= 0.80)
chk("distractor: stopped after hop 1", g1 + g2 + gp2, 25425.70)
chk("distractor: discounted the perpetuity 3 years not 2", g1 + g2 + disc(gp2, .11, 3), 20049.52)
chk("distractor: forgot the growth, used 1,400 / 0.11", g1 + g2 + disc(1400 / .11, .11, 2), 15755.44)
print("     r must be above g for the formula to work: 0.11 > 0.04 ?", .11 > .04)
CHECKS.append(.11 > .04)

# ---------------------------------------------------------------- summary
print("\n" + "=" * 130)
print("%d numbers checked, %d passed, %d failed."
      % (len(CHECKS), sum(CHECKS), len(CHECKS) - sum(CHECKS)))
print("=" * 130)
raise SystemExit(0 if all(CHECKS) else 1)
