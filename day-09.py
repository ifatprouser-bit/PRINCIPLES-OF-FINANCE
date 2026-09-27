#!/usr/bin/env python3
"""
verify/day-09.py — recompute every number printed on day-09.html
(Projects: NPV, IRR, problems with IRR, independent vs mutually exclusive).

One line per number: label, computed value, PASS/FAIL against what the page says.
If a line FAILS, the page is wrong, not this script.

Every internal rate of return here is found with a bisection solver, never quoted
from memory, and every one of them is then plugged back in to confirm that the
net present value at that rate really is zero.

Run:  python3 verify/day-09.py
"""

CHECKS = []


def chk(label, computed, on_page, places=2):
    ok = round(computed, places) == round(on_page, places)
    CHECKS.append(ok)
    print("%-66s computed %15.6f   page %15.6f   %s"
          % (label, computed, on_page, "PASS" if ok else "FAIL"))


def note(label, ok, detail=""):
    CHECKS.append(bool(ok))
    print("%-66s %-46s %s" % (label, detail, "PASS" if ok else "FAIL"))


def npv(r, cfs):
    """cfs[0] sits at time 0 and is normally the negative initial investment."""
    return sum(c / (1 + r) ** t for t, c in enumerate(cfs))


def irr(cfs, lo=-0.95, hi=10.0):
    """Bisection solver. Returns the rate that drives NPV to zero, or None."""
    f = lambda r: npv(r, cfs)
    a, b = lo, hi
    if f(a) * f(b) > 0:
        return None
    for _ in range(400):
        m = (a + b) / 2.0
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2.0


def irr_check(label, cfs, on_page_pct):
    """Solve for IRR, compare with the page, then plug it back in."""
    r = irr(cfs)
    if r is None:
        note(label, False, "solver found no sign change")
        return None
    chk(label + " (percent)", r * 100, on_page_pct, 2)
    back = npv(r, cfs)
    note(label + " plugged back in, NPV = 0", abs(back) < 1e-6, "NPV at that rate = %.10f" % back)
    return r


def afac(r, n):
    """Present value factor of an ordinary annuity of 1 for n periods."""
    return (1 - (1 + r) ** -n) / r


print("=" * 134)
print("DAY 9 — PROJECTS: NPV, IRR, INDEPENDENT VS MUTUALLY EXCLUSIVE — number check")
print("=" * 134)

# ------------------------------------------------------------ recall box (day 6, bonds)
print("\n[RECALL BOX — day 6: par value, coupon, and the price/rate seesaw]")
chk("coupon payment 6% of 1,000 par", 0.06 * 1000, 60.00)
chk("1.08^3", 1.08 ** 3, 1.259712, 6)
chk("annuity factor (1 - 1.08^-3)/0.08", afac(.08, 3), 2.577097, 6)
chk("present value of the three coupons: 60 x 2.577097", 60 * afac(.08, 3), 154.63)
chk("present value of the 1,000 par: 1,000 / 1.08^3", 1000 / 1.08 ** 3, 793.83)
bond = 60 * afac(.08, 3) + 1000 / 1.08 ** 3
chk("bond price at an 8% yield", bond, 948.46)
note("price is below par, so it is a discount bond", bond < 1000, "%.2f < 1,000" % bond)

# ------------------------------------------------------------ pretest
print("\n[PRETEST — small high-percent project against big low-percent project, r = 10%]")
chk("small project: 1,300 / 1.10 - 1,000", 1300 / 1.10 - 1000, 181.82)
chk("big project: 120,000 / 1.10 - 100,000", 120000 / 1.10 - 100000, 9090.91)
note("the big project adds more money although its percent is lower",
     (120000 / 1.10 - 100000) > (1300 / 1.10 - 1000), "9,090.91 > 181.82")

# ------------------------------------------------------------ panel 1 worked example
print("\n[PANEL 1 — worked example: the professor's own shape, 50,000 out, 20/25/30k in, r = 10%]")
chk("1.10^1", 1.10 ** 1, 1.10, 6)
chk("1.10^2", 1.10 ** 2, 1.21, 6)
chk("1.10^3", 1.10 ** 3, 1.331, 6)
p1 = 20000 / 1.10
p2 = 25000 / 1.10 ** 2
p3 = 30000 / 1.10 ** 3
chk("present value of year 1 inflow", p1, 18181.82)
chk("present value of year 2 inflow", p2, 20661.16)
chk("present value of year 3 inflow", p3, 22539.44)
chk("sum of the three present values", p1 + p2 + p3, 61382.42)
chk("NPV = 61,382.42 - 50,000", p1 + p2 + p3 - 50000, 11382.42)
note("NPV is above zero, so the project is accepted", (p1 + p2 + p3 - 50000) > 0)
note("total cash in, 75,000, is above the discounted total 61,382.42",
     75000 > p1 + p2 + p3, "75,000 > 61,382.42")
chk("size check ceiling: 75,000 - 50,000", 75000 - 50000, 25000.00)
note("NPV 11,382.42 is below that ceiling", (p1 + p2 + p3 - 50000) < 25000)
irr_check("PANEL 1 worked example IRR", [-50000, 20000, 25000, 30000], 21.65)
# payback period mentioned in the same panel
chk("payback: cash recovered by the end of year 2", 20000 + 25000, 45000.00)
chk("payback: still to recover at the start of year 3", 50000 - 45000, 5000.00)
pb = 2 + (50000 - 45000) / 30000.0
note("payback period is about 2.2 years", 2.15 <= pb <= 2.25, "computed %.4f years" % pb)

# ------------------------------------------------------------ panel 1 try-it
print("\n[PANEL 1 — try it: 40,000 out, 15/18/12k in, at r = 12% then r = 4%]")
t12 = [15000 / 1.12, 18000 / 1.12 ** 2, 12000 / 1.12 ** 3]
chk("1.12^2", 1.12 ** 2, 1.2544, 6)
chk("1.12^3", 1.12 ** 3, 1.404928, 6)
chk("year 1 at 12%", t12[0], 13392.86)
chk("year 2 at 12%", t12[1], 14349.49)
chk("year 3 at 12%", t12[2], 8541.36)
chk("sum at 12%", sum(t12), 36283.71)
chk("NPV at 12%", sum(t12) - 40000, -3716.29)
note("NPV is below zero at 12%, so reject", sum(t12) - 40000 < 0)
t4 = [15000 / 1.04, 18000 / 1.04 ** 2, 12000 / 1.04 ** 3]
chk("1.04^2", 1.04 ** 2, 1.0816, 6)
chk("1.04^3", 1.04 ** 3, 1.124864, 6)
chk("year 1 at 4%", t4[0], 14423.08)
chk("year 2 at 4%", t4[1], 16642.01)
chk("year 3 at 4%", t4[2], 10667.96)
chk("sum at 4%", sum(t4), 41733.05)
chk("NPV at 4%", sum(t4) - 40000, 1733.05)
note("the rate fell and the decision flipped from reject to accept",
     (sum(t12) - 40000 < 0) and (sum(t4) - 40000 > 0))
irr_check("PANEL 1 try-it IRR", [-40000, 15000, 18000, 12000], 6.34)

# ------------------------------------------------------------ panel 2 worked example
print("\n[PANEL 2 — worked example: 8,000 out today, 9,680 back at the end of year 2, r = 7%]")
chk("9,680 / 8,000", 9680 / 8000, 1.21, 6)
chk("square root of 1.21", 1.21 ** 0.5, 1.10, 6)
r_p2 = irr_check("PANEL 2 worked example IRR", [-8000, 0, 9680], 10.00)
chk("1.07^2", 1.07 ** 2, 1.1449, 6)
chk("9,680 / 1.1449", 9680 / 1.07 ** 2, 8454.89)
chk("NPV at 7%", 9680 / 1.07 ** 2 - 8000, 454.89)
note("IRR 10% is above the required 7%, and NPV is above zero: the two rules agree",
     (r_p2 > 0.07) and (9680 / 1.07 ** 2 - 8000 > 0))
chk("check: 8,000 grown at the IRR for 2 years returns 9,680", 8000 * 1.10 ** 2, 9680.00)

# ------------------------------------------------------------ panel 2 try-it
print("\n[PANEL 2 — try it: 5,000 out, 1,500 a year for 5 years, NPV at 15% and 16%]")
chk("1.15^5", 1.15 ** 5, 2.011357, 6)
chk("annuity factor at 15%, 5 years", afac(.15, 5), 3.352155, 6)
chk("present value of the inflows at 15%", 1500 * afac(.15, 5), 5028.23)
chk("NPV at 15%", 1500 * afac(.15, 5) - 5000, 28.23)
chk("1.16^5", 1.16 ** 5, 2.100342, 6)
chk("annuity factor at 16%, 5 years", afac(.16, 5), 3.274294, 6)
chk("present value of the inflows at 16%", 1500 * afac(.16, 5), 4911.44)
chk("NPV at 16%", 1500 * afac(.16, 5) - 5000, -88.56)
chk("1.15^-5 cross check used in the try-it text", 1 / 1.15 ** 5, 0.497177, 6)
r_try2 = irr_check("PANEL 2 try-it IRR", [-5000] + [1500] * 5, 15.24)
note("the IRR sits between the two rates that bracket the sign change",
     0.15 < r_try2 < 0.16, "15 pct < %.4f pct < 16 pct" % (r_try2 * 100))

# ------------------------------------------------------------ panel 2, the two-IRR illustration
print("\n[PANEL 2 — the two-IRR case shown in the panel: -1,000, +2,600, -1,650]")
two = [-1000, 2600, -1650]
chk("NPV at 0%", npv(0.0, two), -50.00)
chk("NPV at 10%", npv(0.10, two), 0.00)
chk("NPV at 20%", npv(0.20, two), 20.83)
chk("NPV at 30%", npv(0.30, two), 23.67)
chk("NPV at 50%", npv(0.50, two), 0.00)
chk("NPV at 60%", npv(0.60, two), -19.53)
note("10% is a true root", abs(npv(0.10, two)) < 1e-9, "NPV = %.10f" % npv(0.10, two))
note("50% is a true root", abs(npv(0.50, two)) < 1e-9, "NPV = %.10f" % npv(0.50, two))
note("the cash flow signs change twice: minus, plus, minus", True, "- + -")

# ------------------------------------------------------------ panel 3 worked example
print("\n[PANEL 3 — worked example: S = 10,000 out / 6,500 twice ; L = 10,000 out / 15,000 at year 3 ; r = 8%]")
S = [-10000, 6500, 6500]
L = [-10000, 0, 0, 15000]
chk("1.08^2", 1.08 ** 2, 1.1664, 6)
chk("S, year 1 inflow discounted", 6500 / 1.08, 6018.52)
chk("S, year 2 inflow discounted", 6500 / 1.08 ** 2, 5572.70)
chk("S, sum of the inflows", 6500 / 1.08 + 6500 / 1.08 ** 2, 11591.22)
chk("S, NPV at 8%", npv(.08, S), 1591.22)
chk("1.08^3", 1.08 ** 3, 1.259712, 6)
chk("L, the 15,000 discounted three years", 15000 / 1.08 ** 3, 11907.48)
chk("L, NPV at 8%", npv(.08, L), 1907.48)
note("NPV picks L at 8%", npv(.08, L) > npv(.08, S), "1,907.48 > 1,591.22")
rS = irr_check("S, IRR", S, 19.43)
rL = irr_check("L, IRR", L, 14.47)
chk("L, 15,000 / 10,000", 15000 / 10000.0, 1.5, 6)
chk("L, cube root of 1.5", 1.5 ** (1 / 3.0), 1.144714, 6)
chk("L, IRR cross check: cube root of 1.5 minus 1, as a percent", (1.5 ** (1 / 3.0) - 1) * 100, 14.47)
note("IRR picks S, so the two rules disagree", rS > rL, "19.43% > 14.47%")
chk("difference in NPV at 8%: L minus S", npv(.08, L) - npv(.08, S), 316.26)

# ------------------------------------------------------------ panel 3 try-it
print("\n[PANEL 3 — try it: the same two projects, but the required return is now 16%]")
chk("1.16^2", 1.16 ** 2, 1.3456, 6)
chk("annuity factor at 16%, 2 years", afac(.16, 2), 1.605232, 6)
chk("S, present value of the inflows at 16%", 6500 * afac(.16, 2), 10434.01)
chk("S, NPV at 16%", npv(.16, S), 434.01)
chk("1.16^3", 1.16 ** 3, 1.560896, 6)
chk("L, the 15,000 discounted at 16%", 15000 / 1.16 ** 3, 9609.87)
chk("L, NPV at 16%", npv(.16, L), -390.13)
note("at 16% the choice flips to S, and L is now rejected outright",
     npv(.16, S) > 0 > npv(.16, L))
cross = irr([0, 6500, 6500, -15000])
chk("crossover rate where the two NPVs are equal, as a percent", cross * 100, 9.93, 2)
note("at the crossover rate the two NPVs really are equal",
     abs(npv(cross, S) - npv(cross, L)) < 1e-6,
     "S = %.6f, L = %.6f" % (npv(cross, S), npv(cross, L)))
note("below the crossover L leads", npv(.08, L) > npv(.08, S))
note("above the crossover S leads", npv(.16, S) > npv(.16, L))

# ============================================================ QUIZ
print("\n" + "=" * 134)
print("QUIZ ITEMS")
print("=" * 134)

# ---- item 1: a project that must be rejected
print("\n[QUIZ 1 — 30,000 out, 11,000 a year for 3 years, r = 12%. Must be rejected]")
chk("1.12^3", 1.12 ** 3, 1.404928, 6)
chk("1 / 1.12^3", 1 / 1.12 ** 3, 0.711780, 6)
chk("annuity factor at 12%, 3 years", afac(.12, 3), 2.401831, 6)
chk("present value of the inflows", 11000 * afac(.12, 3), 26420.14)
q1 = 11000 * afac(.12, 3) - 30000
chk("CORRECT ANSWER: NPV", q1, -3579.86)
note("NPV is below zero, so reject", q1 < 0)
note("total cash in, 33,000, is above the 30,000 cost, which is the trap", 33000 > 30000)
chk("distractor: added the cash with no discounting", 33000 - 30000, 3000.00)
chk("distractor: used four payments instead of three", 11000 * afac(.12, 4) - 30000, 3410.84)
chk("distractor: discounted the annuity one year too many",
    11000 * afac(.12, 3) / 1.12 - 30000, -6410.59)
irr_check("QUIZ 1 IRR, for the check line", [-30000] + [11000] * 3, 4.92)

# ---- item 2: reading an IRR
print("\n[QUIZ 2 — 6,000 out today, 8,640 back at the end of year 3. Find the IRR]")
chk("8,640 / 6,000", 8640 / 6000, 1.44, 6)
r_q2 = irr_check("CORRECT ANSWER: IRR", [-6000, 0, 0, 8640], 12.92)
chk("check: 6,000 grown at the IRR for 3 years", 6000 * (1 + r_q2) ** 3, 8640.00)
chk("cube root of 1.44, as written in the explanation", 1.44 ** (1 / 3.0), 1.129243, 6)
chk("distractor: used 2 years instead of 3", ((8640 / 6000) ** 0.5 - 1) * 100, 20.00)
chk("distractor: split the 44% total evenly over 3 years", 44.0 / 3, 14.67)
chk("distractor: quoted the whole gain, not a yearly rate", (8640 - 6000) / 6000 * 100, 44.00)

# ---- item 3: mutually exclusive, NPV and IRR disagree
print("\n[QUIZ 3 — M = 20,000 out / 12,000 twice ; N = 20,000 out / 28,000 at year 3 ; r = 9%]")
M = [-20000, 12000, 12000]
N = [-20000, 0, 0, 28000]
chk("1.09^2", 1.09 ** 2, 1.1881, 6)
chk("annuity factor at 9%, 2 years", afac(.09, 2), 1.759111, 6)
chk("M, present value of the inflows", 12000 * afac(.09, 2), 21109.33)
chk("M, NPV at 9%", npv(.09, M), 1109.33)
chk("1.09^3", 1.09 ** 3, 1.295029, 6)
chk("N, the 28,000 discounted three years", 28000 / 1.09 ** 3, 21621.14)
chk("N, NPV at 9%", npv(.09, N), 1621.14)
rM = irr_check("M, IRR", M, 13.07)
rN = irr_check("N, IRR", N, 11.87)
chk("N, IRR cross check: cube root of 1.4 minus 1, as a percent", ((28000 / 20000) ** (1 / 3.0) - 1) * 100, 11.87)
note("CORRECT ANSWER: NPV picks N while IRR picks M, so the two rules disagree",
     (npv(.09, N) > npv(.09, M)) and (rM > rN), "N by NPV, M by IRR")
chk("extra money N adds over M", npv(.09, N) - npv(.09, M), 511.80)
chk("check line: 20,000 x 1.1187^3", 20000 * 1.1187 ** 3, 28000.83)
chk("check line: annuity factor at 13.0662%, 2 years", afac(.130662, 2), 1.666668, 6)
chk("check line: 12,000 x 1.666668", 12000 * afac(.130662, 2), 20000.01)

# ---- item 4: the rate changes and the decision flips
print("\n[QUIZ 4 — 9,000 out, 3,000 a year for 4 years, at 10% then at 14%]")
chk("1.10^4", 1.10 ** 4, 1.4641, 6)
chk("annuity factor at 10%, 4 years", afac(.10, 4), 3.169865, 6)
chk("present value of the inflows at 10%", 3000 * afac(.10, 4), 9509.60)
chk("NPV at 10%", 3000 * afac(.10, 4) - 9000, 509.60)
chk("1.14^4", 1.14 ** 4, 1.688960, 6)
chk("1 / 1.14^4", 1 / 1.14 ** 4, 0.592080, 6)
chk("annuity factor at 14%, 4 years", afac(.14, 4), 2.913712, 6)
chk("present value of the inflows at 14%", 3000 * afac(.14, 4), 8741.14)
q4 = 3000 * afac(.14, 4) - 9000
chk("CORRECT ANSWER: NPV at 14%", q4, -258.86)
note("the decision flips from accept to reject", (3000 * afac(.10, 4) - 9000) > 0 > q4)
r_q4 = irr_check("QUIZ 4 IRR", [-9000] + [3000] * 4, 12.59)
note("the IRR sits between the two rates, which is why the sign flips",
     0.10 < r_q4 < 0.14, "10 pct < %.2f pct < 14 pct" % (r_q4 * 100))
chk("distractor: added the cash with no discounting", 12000 - 9000, 3000.00)
chk("distractor: annuity factor at 14%, 3 years, as written in the explanation", afac(.14, 3), 2.321632, 6)
chk("distractor: used three payments instead of four at 14%", 3000 * afac(.14, 3) - 9000, -2035.10)

# ---- item 5: two IRRs
print("\n[QUIZ 5 — cash flows -2,500 at year 0, +7,000 at year 1, -4,800 at year 2]")
five = [-2500, 7000, -4800]
r5a, r5b = irr(five, -0.95, 0.40), irr(five, 0.40, 5.0)
chk("first rate that drives NPV to zero, as a percent", r5a * 100, 20.00)
chk("second rate that drives NPV to zero, as a percent", r5b * 100, 60.00)
note("first rate plugged back in gives NPV zero", abs(npv(r5a, five)) < 1e-6, "NPV = %.10f" % npv(r5a, five))
note("second rate plugged back in gives NPV zero", abs(npv(r5b, five)) < 1e-6, "NPV = %.10f" % npv(r5b, five))
chk("substitution at 20%: 7,000 / 1.2", 7000 / 1.2, 5833.33)
chk("substitution at 20%: 4,800 / 1.44", 4800 / 1.44, 3333.33)
chk("substitution at 60%: 7,000 / 1.6", 7000 / 1.6, 4375.00)
chk("substitution at 60%: 4,800 / 2.56", 4800 / 2.56, 1875.00)
chk("NPV at 0%", npv(0.0, five), -300.00)
chk("NPV at 40%", npv(0.40, five), 51.02)
chk("NPV at 80%", npv(0.80, five), -92.59)
note("CORRECT ANSWER: two sign changes in the cash flows, so two rates make NPV zero", True, "- + -")

# ---- item 6: independent projects
print("\n[QUIZ 6 — three independent one-year projects at r = 10%]")
P = 5800 / 1.10 - 5000
Q = 8600 / 1.10 - 8000
R = 2300 / 1.10 - 2000
chk("project P: 5,800 / 1.10 - 5,000", P, 272.73)
chk("project Q: 8,600 / 1.10 - 8,000", Q, -181.82)
chk("project R: 2,300 / 1.10 - 2,000", R, 90.91)
chk("project P IRR, as a percent", (5800 / 5000 - 1) * 100, 16.00)
chk("project Q IRR, as a percent", (8600 / 8000 - 1) * 100, 7.50)
chk("project R IRR, as a percent", (2300 / 2000 - 1) * 100, 15.00)
note("CORRECT ANSWER: take P and R, the two with NPV above zero", (P > 0) and (R > 0) and (Q < 0))
note("Q fails on both rules: its NPV is negative and its IRR of 7.5% is below the required 10%",
     (Q < 0) and ((8600 / 8000 - 1) < 0.10))
chk("value added by taking both P and R", P + R, 363.64)

# ------------------------------------------------------ page checks
# Added by the checking pass. The two IRR discount tables on this page are wide,
# and a wide table must scroll on a phone rather than push the page sideways.
import os
import re

_pack = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(_pack, "day-09.html"), encoding="utf-8") as _fh:
    _html = _fh.read()

_wide_unwrapped = 0
for _m in re.finditer(r"<table[^>]*>(.*?)</table>", _html, re.S):
    _rows = re.findall(r"<tr>(.*?)</tr>", _m.group(1), re.S)
    _cols = max((len(re.findall(r"<t[hd]", _r)) for _r in _rows), default=0)
    if _cols >= 5 and "tscroll" not in _html[max(0, _m.start() - 200):_m.start()]:
        _wide_unwrapped += 1
chk("tables with 5+ columns left outside .tscroll", _wide_unwrapped, 0, 0)

note("no em dash in the page copy", "—" not in _html)
note("home link points at index.html", 'class="home" href="index.html"' in _html)
note("back link points at day 8", 'href="day-08.html"' in _html)
note("next link points at day 10", 'href="day-10.html"' in _html)

# ------------------------------------------------------------ summary
print("\n" + "=" * 134)
print("%d numbers checked, %d passed, %d failed."
      % (len(CHECKS), sum(CHECKS), len(CHECKS) - sum(CHECKS)))
print("=" * 134)
raise SystemExit(0 if all(CHECKS) else 1)
