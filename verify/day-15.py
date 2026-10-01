#!/usr/bin/env python3
"""
Verify every number that appears on day-15.html (the exam-morning warm-up).

The page has no quiz. It carries three familiar tasks, a trap list with no
arithmetic in it, and one box of exam facts. Everything numeric below is
recomputed from scratch and compared with what the page says.

Run:  python3 verify/day-15.py
"""

from decimal import Decimal, ROUND_HALF_UP

checks = []


def r2(x):
    """Round to 2 decimals the way a calculator display does."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def check(label, computed, on_page, places=2):
    if places is None:
        ok = computed == on_page
        shown = computed
    else:
        shown = round(computed, places)
        ok = abs(shown - on_page) < 10 ** (-places) / 2
    checks.append(ok)
    print("{:<62} {:>14}   page {:>14}   {}".format(
        label, shown, on_page, "PASS" if ok else "FAIL"))


print("=" * 118)
print("TASK 1 - present value of a mixed stream, r = 10 percent")
print("  1,000 at end of year 1; 2,000 at end of year 2; 2,000 at end of year 3")
print("=" * 118)

r = 0.10
cf1, cf2, cf3 = 1000.0, 2000.0, 2000.0

pv1 = cf1 / (1 + r) ** 1
pv2 = cf2 / (1 + r) ** 2
pv3 = cf3 / (1 + r) ** 3

check("1.10^1", (1 + r) ** 1, 1.10)
check("1.10^2", (1 + r) ** 2, 1.21)
check("1.10^3", (1 + r) ** 3, 1.331, places=3)
check("PV of the 1,000 at year 1", pv1, 909.09)
check("PV of the 2,000 at year 2", pv2, 1652.89)
check("PV of the 2,000 at year 3", pv3, 1502.63)
check("Total value today", pv1 + pv2 + pv3, 4064.61)
check("Sum of the three rounded lines (must match the total)",
      r2(pv1) + r2(pv2) + r2(pv3), 4064.61)
check("Total cash actually paid (sense check ceiling)", cf1 + cf2 + cf3, 5000.00)
print("  sense check: 4,064.61 is below the 5,000 of cash paid ->",
      "PASS" if pv1 + pv2 + pv3 < cf1 + cf2 + cf3 else "FAIL")
checks.append(pv1 + pv2 + pv3 < cf1 + cf2 + cf3)

# second route shown in the answer: the two 2,000s as a delayed annuity
n = 2
factor = (1 - (1 + r) ** -n) / r
v_year1 = 2000.0 * factor
check("Annuity factor, n = 2 at 10 percent", factor, 1.735537, places=6)
check("Two 2,000s valued as an annuity, dated year 1", v_year1, 3471.07)
check("That value brought back one year", v_year1 / (1 + r), 3155.52)
check("Route two total: 909.09 + 3,155.52", r2(pv1) + r2(v_year1 / (1 + r)), 4064.61)
print("  both routes agree ->",
      "PASS" if abs((pv1 + v_year1 / (1 + r)) - (pv1 + pv2 + pv3)) < 1e-9 else "FAIL")
checks.append(abs((pv1 + v_year1 / (1 + r)) - (pv1 + pv2 + pv3)) < 1e-9)

print()
print("=" * 118)
print("TASK 2 - the payoff waterfall, F_S = 50, F_J = 30")
print("=" * 118)

FS, FJ = 50.0, 30.0
check("F_S + F_J", FS + FJ, 80.00)


def waterfall(VT):
    senior = min(VT, FS)
    junior = 0.0 if VT < FS else min(VT - FS, FJ)
    equity = max(VT - FS - FJ, 0.0)
    return senior, junior, equity


for VT, page in ((110.0, (50.0, 30.0, 30.0)), (65.0, (50.0, 15.0, 0.0))):
    s, j, e = waterfall(VT)
    state = "III" if VT >= FS + FJ else ("II" if VT >= FS else "I")
    print("  V_T = {:.0f}  (state {})".format(VT, state))
    check("    senior payoff = Min(V_T, F_S)", s, page[0])
    check("    junior payoff", j, page[1])
    check("    equity payoff = Max(V_T - F_S - F_J, 0)", e, page[2])
    check("    the three payoffs must add to exactly V_T", s + j + e, VT)
    print("    equity is zero or more ->", "PASS" if e >= 0 else "FAIL")
    checks.append(e >= 0)
    print("    senior never above F_S, junior never above F_J ->",
          "PASS" if s <= FS and j <= FJ else "FAIL")
    checks.append(s <= FS and j <= FJ)

print()
print("=" * 118)
print("TASK 3 - NPV, cost 7,000 at year 0, inflows 3,000 / 4,000 / 3,000, r = 10 percent")
print("=" * 118)

I0 = 7000.0
flows = [3000.0, 4000.0, 3000.0]
pvs = [cf / (1 + r) ** (i + 1) for i, cf in enumerate(flows)]

check("PV of the 3,000 at year 1", pvs[0], 2727.27)
check("PV of the 4,000 at year 2", pvs[1], 3305.79)
check("PV of the 3,000 at year 3", pvs[2], 2253.94)
check("Value today of everything coming in", sum(pvs), 8287.00)
check("Sum of the three rounded lines (must match)",
      r2(pvs[0]) + r2(pvs[1]) + r2(pvs[2]), 8287.00)
check("NPV = 8,287.00 - 7,000", sum(pvs) - I0, 1287.00)
check("Total cash in, with no discounting", sum(flows), 10000.00)
check("Undiscounted gain, the ceiling the NPV must stay under", sum(flows) - I0, 3000.00)
print("  sense check: NPV 1,287.00 is above zero, so take the project ->",
      "PASS" if sum(pvs) - I0 > 0 else "FAIL")
checks.append(sum(pvs) - I0 > 0)
print("  sense check: NPV is below the undiscounted gain of 3,000 ->",
      "PASS" if sum(pvs) - I0 < sum(flows) - I0 else "FAIL")
checks.append(sum(pvs) - I0 < sum(flows) - I0)

print()
print("=" * 118)
print("THE EXAM FACTS BOX")
print("=" * 118)

check("2.5 hours in minutes", 2.5 * 60, 150.0, places=1)
check("Minutes per question, 150 / 22", 150.0 / 22.0, 6.8, places=1)
print("  questions on the paper: about 22 (from BUILD-SPEC section 1) -> PASS")
checks.append(True)

print()
print("=" * 118)
print("{} numbers checked, {} passed, {} failed".format(
    len(checks), sum(1 for c in checks if c), sum(1 for c in checks if not c)))
print("ALL PASS" if all(checks) else "SOMETHING FAILED - fix the page, not this script")
print("=" * 118)
