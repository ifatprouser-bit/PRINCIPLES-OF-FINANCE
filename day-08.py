#!/usr/bin/env python3
"""
verify/day-08.py

Recomputes every number that appears on day-08.html ("What the shareholder gets").
Each line prints: label, computed value, the value printed on the page, PASS or FAIL.

Run:  python3 verify/day-08.py
"""

CHECKS = []


def chk(label, computed, on_page, tol=0.005):
    """Compare a computed value with the value written on the page."""
    ok = abs(computed - on_page) <= tol
    CHECKS.append(ok)
    print("{:<62} computed {:>14.6f}   page {:>14.6f}   {}".format(
        label, computed, on_page, "PASS" if ok else "FAIL"))


def head(t):
    print("\n--- " + t + " " + "-" * max(0, 66 - len(t)))


# ----------------------------------------------------------------------
head("RECALL BOX (day 5: delayed annuity)")
# A = 1,000, payments years 4..9, r = 8 percent
n = 6
r = 0.08
af = (1 - (1 + r) ** -n) / r
chk("recall: annuity factor, n = 6, r = 8%", af, 4.622880, tol=5e-6)
v3 = 1000 * af
chk("recall: value at year 3 (hop 1)", v3, 4622.88, tol=0.005)
chk("recall: 1.08^3", 1.08 ** 3, 1.259712, tol=5e-6)
v0 = v3 / 1.08 ** 3
chk("recall: value today (hop 2)", v0, 3669.79, tol=0.005)

# ----------------------------------------------------------------------
head("PRETEST (no answer printed on the page, checked for sense only)")
pre = (37 - 40 + 5) / 40
chk("pretest: (37 - 40 + 5) / 40, positive despite the price fall", pre, 0.05)

# ----------------------------------------------------------------------
head("PANEL 1: holding period return, worked example")
P0, P1, D1 = 120.0, 129.0, 4.80
chk("p1: price change 129 - 120", P1 - P0, 9.0)
chk("p1: whole gain 9 + 4.80", (P1 - P0) + D1, 13.80)
chk("p1: svg, cash back in pocket 129 + 4.80", P1 + D1, 133.80)
hpr = (P1 - P0 + D1) / P0
chk("p1: holding period return", hpr, 0.115)
chk("p1: as a percent", hpr * 100, 11.5)
chk("p1: dividend part 4.80 / 120", D1 / P0, 0.04)
chk("p1: price part 9 / 120", (P1 - P0) / P0, 0.075)
chk("p1: split adds back (4% + 7.5%)", D1 / P0 + (P1 - P0) / P0, 0.115)

head("PANEL 1: try-it 1 (price falls, return still positive)")
P0, P1, D1 = 60.0, 57.0, 4.20
chk("p1 try1: price change 57 - 60", P1 - P0, -3.0)
chk("p1 try1: whole gain -3 + 4.20", (P1 - P0) + D1, 1.20)
chk("p1 try1: return 1.20 / 60", (P1 - P0 + D1) / P0, 0.02)
chk("p1 try1: dividend part 4.20 / 60", D1 / P0, 0.07)
chk("p1 try1: price part -3 / 60", (P1 - P0) / P0, -0.05)

head("PANEL 1: try-it 2 (inverse, find the ending price)")
P0, D1, r = 25.0, 1.00, 0.08
chk("p1 try2: P0 x 1.08", P0 * (1 + r), 27.00)
P1 = P0 * (1 + r) - D1
chk("p1 try2: P1 = P0(1+r) - D1", P1, 26.00)
chk("p1 try2: check back, (26 - 25 + 1) / 25", (P1 - P0 + D1) / P0, 0.08)

# ----------------------------------------------------------------------
head("PANEL 2: no growth dividend discount model / preferred stock")
D = 6.00
chk("p2: price at r = 8%, 6.00 / 0.08", D / 0.08, 75.00)
chk("p2: price at r = 6%, 6.00 / 0.06", D / 0.06, 100.00)
chk("p2: check back, 6.00 / 75.00", D / 75.00, 0.08)

head("PANEL 2: try-it (inverse, find the return)")
chk("p2 try: r = 3.60 / 48.00", 3.60 / 48.00, 0.075)
chk("p2 try: check back, 48.00 x 0.075", 48.00 * 0.075, 3.60)

# ----------------------------------------------------------------------
head("PANEL 3: constant growth, worked example from the class notes")
D0, g, r = 2.73, 0.06, 0.1223
D1 = D0 * (1 + g)
chk("p3: D1 = 2.73 x 1.06", D1, 2.8938, tol=5e-5)
chk("p3: r - g = 0.1223 - 0.06", r - g, 0.0623, tol=5e-6)
chk("p3: price = 2.8938 / 0.0623", D1 / (r - g), 46.45, tol=0.005)
chk("p3: sense check, no growth 2.73 / 0.1223", D0 / r, 22.32, tol=0.005)

head("PANEL 3: table, price as g moves toward r = 10%")
R = 0.10
for gg, d1_page, price_page in [(0.00, 2.00, 20.00),
                                (0.02, 2.04, 25.50),
                                (0.04, 2.08, 34.67),
                                (0.06, 2.12, 53.00),
                                (0.08, 2.16, 108.00)]:
    d1 = 2.00 * (1 + gg)
    chk("p3 table: g = {:.0%}, D1".format(gg), d1, d1_page, tol=5e-6)
    chk("p3 table: g = {:.0%}, r - g".format(gg), R - gg, round(R - gg, 2), tol=5e-6)
    chk("p3 table: g = {:.0%}, price".format(gg), d1 / (R - gg), price_page, tol=0.005)

head("PANEL 3: try-it 1 (inverse, find the required return)")
chk("p3 try1: dividend yield 1.50 / 30.00", 1.50 / 30.00, 0.05)
chk("p3 try1: r = yield + g", 1.50 / 30.00 + 0.04, 0.09)
chk("p3 try1: check back, 1.50 / 0.05", 1.50 / (0.09 - 0.04), 30.00)

head("PANEL 3: try-it 2 (r not above g, the model breaks)")
chk("p3 try2: r - g = 0.06 - 0.08", 0.06 - 0.08, -0.02, tol=5e-6)
chk("p3 try2: 5.00 / (-0.02), a nonsense negative price", 5.00 / (0.06 - 0.08), -250.00, tol=0.005)

# ----------------------------------------------------------------------
head("PANEL 4: ROA against ROE, worked example")
assets, debt, equity, ni = 500.0, 300.0, 200.0, 40.0
chk("p4: Alpha, assets = debt + equity", debt + equity, assets)
chk("p4: Alpha ROA 40 / 500", ni / assets, 0.08)
chk("p4: Alpha ROE 40 / 200", ni / equity, 0.20)
chk("p4: Beta ROA 40 / 500", ni / 500.0, 0.08)
chk("p4: Beta ROE 40 / 500 (no debt, equity = assets)", ni / 500.0, 0.08)
chk("p4: Alpha bad year ROA -20 / 500", -20.0 / assets, -0.04)
chk("p4: Alpha bad year ROE -20 / 200", -20.0 / equity, -0.10)

# ----------------------------------------------------------------------
head("QUIZ 1: holding period return, price falls, return positive")
P0, P1, D1 = 80.0, 74.0, 9.0
chk("q1: correct, (74 - 80 + 9) / 80", (P1 - P0 + D1) / P0 * 100, 3.75)
chk("q1: distractor, price only -6 / 80", (P1 - P0) / P0 * 100, -7.5)
chk("q1: distractor, dividend only 9 / 80", D1 / P0 * 100, 11.25)
chk("q1: distractor, divided by P1, 3 / 74", (P1 - P0 + D1) / P1 * 100, 4.05, tol=0.005)
chk("q1: split check, 11.25 - 7.5", D1 / P0 * 100 + (P1 - P0) / P0 * 100, 3.75)

head("QUIZ 2: preferred share, required return rises")
D = 5.60
chk("q2: correct, 5.60 / 0.10", D / 0.10, 56.00)
chk("q2: distractor, old price 5.60 / 0.08", D / 0.08, 70.00)
chk("q2: distractor, grew the dividend 5.60 x 1.10 / 0.10", D * 1.10 / 0.10, 61.60)
chk("q2: distractor, decimal slip 5.60 / 10", D / 10, 0.56)
chk("q2: check back, 5.60 / 56.00", D / 56.00, 0.10)

head("QUIZ 3: r above g, and r below g")
chk("q3: share X, 2.00 / (0.09 - 0.04)", 2.00 / (0.09 - 0.04), 40.00)
chk("q3: share X check, 40.00 x 0.05", 40.00 * (0.09 - 0.04), 2.00)
chk("q3: share Y, 2.00 / (0.09 - 0.11), nonsense", 2.00 / (0.09 - 0.11), -100.00, tol=0.005)
chk("q3: distractor, no growth 2.00 / 0.09", 2.00 / 0.09, 22.22, tol=0.005)

head("QUIZ 4: inverse, find the required return from D0, g and P0")
D0, g, P0 = 3.00, 0.05, 45.00
D1 = D0 * (1 + g)
chk("q4: D1 = 3.00 x 1.05", D1, 3.15, tol=5e-6)
chk("q4: dividend yield 3.15 / 45.00", D1 / P0, 0.07, tol=5e-6)
chk("q4: correct, r = 0.07 + 0.05", D1 / P0 + g, 0.12, tol=5e-6)
chk("q4: correct as a percent", (D1 / P0 + g) * 100, 12.0, tol=0.005)
chk("q4: check back, 3.15 / (0.12 - 0.05)", D1 / (D1 / P0 + g - g), 45.00, tol=0.005)
chk("q4: distractor, used D0 not D1", (D0 / P0 + g) * 100, 11.67, tol=0.005)
chk("q4: distractor, yield alone", (D1 / P0) * 100, 7.0, tol=0.005)
chk("q4: distractor, subtracted g", (D1 / P0 - g) * 100, 2.0, tol=0.005)

head("QUIZ 5: inverse, find equity and debt from ROA, ROE and assets")
assets, roa, roe = 800.0, 0.06, 0.15
ni = roa * assets
chk("q5: net income = 0.06 x 800", ni, 48.0)
eq = ni / roe
chk("q5: correct, equity = 48 / 0.15", eq, 320.0)
chk("q5: correct, debt = 800 - 320", assets - eq, 480.0)
chk("q5: check back, 48 / 800 is the ROA given", ni / assets, 0.06, tol=5e-6)
chk("q5: check back, 48 / 320 is the ROE given", ni / eq, 0.15, tol=5e-6)
chk("q5: leverage multiple, 800 / 320", assets / eq, 2.5, tol=5e-6)
chk("q5: distractor, 0.15 x 800 read as equity", roe * assets, 120.0)
chk("q5: distractor, its debt 800 - 120", assets - roe * assets, 680.0)
chk("q5: distractor, even split fails the check 48 / 400", ni / 400.0 * 100, 12.0)

head("QUIZ 6: goals of the financial manager")
print("q6 carries no numbers. Nothing to recompute.")

# ----------------------------------------------------------------------
head("PAGE STRUCTURE AND NO-REPEAT GUARDS")
import os
import re

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day-08.html")
with open(HTML_PATH, encoding="utf-8") as fh:
    HTML = fh.read()
QUIZ = HTML[HTML.index("POF.quiz("):]
STEMS = " ".join(re.findall(r'^      q: "(.*)",$', QUIZ, re.M))


def flag(label, ok):
    CHECKS.append(ok)
    print("{:<62} {:>37}   {}".format(label, "ok" if ok else "PROBLEM",
                                      "PASS" if ok else "FAIL"))


# The panel 4 worked example is Alpha/Beta: assets 500, debt 300, equity 200,
# net income 40, giving ROA 8 percent and ROE 20 percent. No quiz item may re-ask it,
# not with those numbers and not with the same numbers scaled.
flag("quiz does not re-ask the Alpha/Beta worked example",
     not re.search(r"net income of 80.*financed entirely by equity", STEMS))
flag("quiz item 5 asks for equity and debt, not for the ratios",
     "return on assets of 6 percent and a return on equity of 15 percent" in STEMS)
flag("worked example Alpha/Beta is untouched in panel 4",
     "Alpha: ROA 8 percent, ROE 20 percent. Beta: ROA 8 percent, ROE 8 percent." in HTML)

# Mobile: any table of five or more columns must sit inside a .tscroll wrapper.
wide_ok = True
for m in re.finditer(r"<table[^>]*>.*?</table>", HTML, re.S):
    row = re.search(r"<tr>.*?</tr>", m.group(0), re.S).group(0)
    cols = len(re.findall(r"<t[hd]", row))
    if cols >= 5 and 'class="tscroll"' not in HTML[max(0, m.start() - 160):m.start()]:
        wide_ok = False
        print("   wide table with %d columns is NOT inside a tscroll wrapper" % cols)
flag("every table of 5+ columns sits inside a tscroll", wide_ok)

flag("no em dashes in the page", HTML.count("—") == 0)
flag("quiz mount id exists and matches the scorechip",
     'id="quiz"' in HTML and 'data-scorechip="quiz"' in HTML and 'mount: "quiz"' in HTML)
flag("every tag is on the allowed list",
     set(re.findall(r'^      tag: "([^"]+)"', QUIZ, re.M))
     <= {"Concepts", "Single cash flow", "Annuity", "Perpetuity", "Mixed stream",
         "Bonds", "Payoff structure", "Stocks", "NPV and IRR"})
flag("nav links to day 7, day 9 and the hub",
     'href="day-07.html"' in HTML and 'href="day-09.html"' in HTML
     and 'href="index.html"' in HTML)

# ----------------------------------------------------------------------
print("\n" + "=" * 92)
print("{} numbers checked, {} passed, {} failed.".format(
    len(CHECKS), sum(1 for c in CHECKS if c), sum(1 for c in CHECKS if not c)))
print("=" * 92)
raise SystemExit(0 if all(CHECKS) else 1)
