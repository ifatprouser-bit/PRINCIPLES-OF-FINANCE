#!/usr/bin/env python3
"""
verify/day-07.py — recompute every number printed on day-07.html (Who gets paid first).

One line per number: label, computed value, PASS/FAIL against what the page says.
If a line FAILS, the page is wrong, not this script.

Also re-derives every bar height and y position in the inline SVG waterfall from the
money values, and reads the real numbers back out of day-07.html to compare.

Run:  python3 verify/day-07.py
"""

import os
import re

CHECKS = []
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "day-07.html")
with open(HTML_PATH, encoding="utf-8") as fh:
    HTML = fh.read()


def chk(label, computed, on_page, places=2):
    ok = round(computed, places) == round(on_page, places)
    CHECKS.append((ok, label))
    print("%-64s computed %14.6f   page %14.6f   %s"
          % (label, computed, on_page, "PASS" if ok else "FAIL"))


def chk_txt(label, computed, on_page):
    ok = (computed == on_page)
    CHECKS.append((ok, label))
    print("%-64s computed %14s   page %14s   %s"
          % (label, str(computed), str(on_page), "PASS" if ok else "FAIL"))


def present(label, needle):
    ok = needle in HTML
    CHECKS.append((ok, label))
    print("%-64s %s   %s" % (label, "found in page" if ok else "NOT IN PAGE",
                             "PASS" if ok else "FAIL"))


# ---------------------------------------------------------------- the payoff model


def senior(v, fs):
    return min(v, fs)


def junior(v, fs, fj):
    return 0.0 if v < fs else min(v - fs, fj)


def equity(v, fs, fj):
    return max(v - fs - fj, 0.0)


def split(v, fs, fj):
    return senior(v, fs), junior(v, fs, fj), equity(v, fs, fj)


print("=" * 132)
print("DAY 7 — WHO GETS PAID FIRST — number check")
print("=" * 132)

# ---------------------------------------------------------------- recall box (day 4)
print("\n[RECALL BOX — day 4: perpetuity and growing perpetuity]")
chk("recall Q1 plain perpetuity 45 / 0.09", 45 / 0.09, 500.00)
chk("recall Q2 growing perpetuity 7 / (0.10 - 0.04)", 7 / (0.10 - 0.04), 116.67)
chk("recall Q2 denominator r - g", 0.10 - 0.04, 0.06, 4)
chk("recall Q2 broken case r = g = 0.04 gives r - g", 0.04 - 0.04, 0.00, 4)

# ---------------------------------------------------------------- pretest
print("\n[PRETEST — V_T 80, F_S 50, F_J 45]")
p_s, p_j, p_e = split(80, 50, 45)
chk("pretest true senior payoff", p_s, 50.00)
chk("pretest true junior payoff", p_j, 30.00)
chk("pretest true equity payoff", p_e, 0.00)
chk("pretest true payoffs sum to V_T", p_s + p_j + p_e, 80.00)
chk("pretest classmate's numbers 50 + 45 - 15 also sum to V_T", 50 + 45 - 15, 80.00)
print("     so the sum test alone does not catch it; the equity floor does:",
      "-15 < 0 is not allowed ->", (-15 < 0))

# ---------------------------------------------------------------- panel 1 set-up
print("\n[PANEL 1 — the course firm: V_0 = 100, equity 20, senior 40, junior 40]")
FS_COUPON = 40 * 0.08
FJ_COUPON = 40 * 0.20
FS = 40 + FS_COUPON
FJ = 40 + FJ_COUPON
chk("senior coupon payment 40 x 8%", FS_COUPON, 3.20)
chk("F_S = face 40 + coupon 3.2", FS, 43.20)
chk("junior coupon payment 40 x 20%", FJ_COUPON, 8.00)
chk("F_J = face 40 + coupon 8", FJ, 48.00)
chk("F_S + F_J", FS + FJ, 91.20)
chk("balance sheet: equity 20 + senior 40 + junior 40 = assets", 20 + 40 + 40, 100.00)

# ---------------------------------------------------------------- panel 1 worked example
print("\n[PANEL 1 — worked example: V_T = 70]")
s70, j70, e70 = split(70, FS, FJ)
chk("V_T 70: senior Min(70, 43.2)", s70, 43.20)
chk("V_T 70: equity Max(70 - 91.2, 0)", e70, 0.00)
chk("V_T 70: junior Min(70 - 43.2, 48)", j70, 26.80)
chk("V_T 70: 70 - 91.2 (the negative that becomes zero)", 70 - (FS + FJ), -21.20)
chk("V_T 70: sum check 43.2 + 26.8 + 0", s70 + j70 + e70, 70.00)
chk("V_T 70: senior return (43.2 - 40)/40 in percent", (s70 - 40) / 40 * 100, 8.00)
chk("V_T 70: junior return (26.8 - 40)/40 in percent", (j70 - 40) / 40 * 100, -33.00)
chk("V_T 70: owners' return (0 - 20)/20 in percent", (e70 - 20) / 20 * 100, -100.00)

# ---------------------------------------------------------------- panel 1 try-it 1
print("\n[PANEL 1 — try-it 1: V_T = 120]")
s120, j120, e120 = split(120, FS, FJ)
chk("V_T 120: senior", s120, 43.20)
chk("V_T 120: junior Min(120 - 43.2, 48) with 120 - 43.2 = 76.8", j120, 48.00)
chk("V_T 120: the 120 - 43.2 shown inside the Min", 120 - FS, 76.80)
chk("V_T 120: equity Max(120 - 91.2, 0)", e120, 28.80)
chk("V_T 120: sum check", s120 + j120 + e120, 120.00)
chk("V_T 120: owners' return (28.8 - 20)/20 in percent", (e120 - 20) / 20 * 100, 44.00)
chk("V_T 120: asset return (120 - 100)/100 in percent", (120 - 100) / 100 * 100, 20.00)

# ---------------------------------------------------------------- panel 1 try-it 2
print("\n[PANEL 1 — try-it 2: V_T = 30]")
s30, j30, e30 = split(30, FS, FJ)
chk("V_T 30: senior Min(30, 43.2)", s30, 30.00)
chk("V_T 30: junior (V_T below F_S)", j30, 0.00)
chk("V_T 30: equity Max(30 - 91.2, 0)", e30, 0.00)
chk("V_T 30: sum check", s30 + j30 + e30, 30.00)
chk("V_T 30: senior return (30 - 40)/40 in percent", (s30 - 40) / 40 * 100, -25.00)

# ---------------------------------------------------------------- cross-check vs class Excel
print("\n[CROSS-CHECK — the class Excel payoff table, rebuilt from the formulas]")
EXCEL_ROWS = {  # V_T : (senior, junior, equity) as printed in the class workbook
    0: (0, 0, 0), 30: (30, 0, 0), 40: (40, 0, 0), 45: (43.2, 1.8, 0),
    70: (43.2, 26.8, 0), 90: (43.2, 46.8, 0), 95: (43.2, 48, 3.8),
    100: (43.2, 48, 8.8), 120: (43.2, 48, 28.8), 140: (43.2, 48, 48.8),
    200: (43.2, 48, 108.8),
}
for v, (xs, xj, xe) in sorted(EXCEL_ROWS.items()):
    cs, cj, ce = split(v, FS, FJ)
    chk("Excel row V_T = %-5s senior" % v, cs, xs)
    chk("Excel row V_T = %-5s junior" % v, cj, xj)
    chk("Excel row V_T = %-5s equity" % v, ce, xe)
    chk("Excel row V_T = %-5s sums to V_T" % v, cs + cj + ce, float(v))

# ---------------------------------------------------------------- the SVG
print("\n[PANEL 1 VISUAL - the bucket stack: every rim, water level and stream re-derived from the money]")

# The picture uses its own round face values, not the worked example's 43.2 / 48.
FS_PIC, FJ_PIC = 60.0, 40.0
PX = 1.2                                   # pixels for every 1 of money, one scale in all three panels
S_FLOOR, J_FLOOR, P_FLOOR = 134.0, 202.0, 274.0
POOL_TOP, TAP_OUT = 224.0, 54.0
SENIOR_MID_X, JUNIOR_MID_X, POOL_MID_X = "50", "98", "98"


def g(x):
    return "%g" % round(x, 4)


panels = re.findall(r"<svg .*?</svg>", HTML, re.S)
chk_txt("bucket-stack panels drawn, one per state", 3, len(panels))

s_rim = S_FLOOR - FS_PIC * PX
j_rim = J_FLOOR - FJ_PIC * PX
chk("senior bucket rim y = floor 134 - 60 x 1.2", s_rim, 62.0, 4)
chk("junior bucket rim y = floor 202 - 40 x 1.2", j_rim, 154.0, 4)
chk("senior bucket is 60 of money tall", FS_PIC * PX, 72.0, 4)
chk("junior bucket is 40 of money tall", FJ_PIC * PX, 48.0, 4)


def water_rect(panel, x, width, colour):
    m = re.search(r'<rect x="%s" y="([\d.]+)" width="%s" height="([\d.]+)" fill="%s"/>'
                  % (x, width, colour), panel)
    if not m:
        return None, None
    return float(m.group(1)), float(m.group(2))


def amount_label(panel, x, y, value, colour):
    return ('<text x="%s" y="%s" text-anchor="middle" font-size="13" font-weight="700" '
            'fill="%s">%s</text>' % (x, g(y), colour, g(value))) in panel


for idx, v in enumerate([40.0, 85.0, 130.0]):
    p = panels[idx]
    s, j, e = split(v, FS_PIC, FJ_PIC)
    s_top, j_top, e_top = S_FLOOR - s * PX, J_FLOOR - j * PX, P_FLOOR - e * PX
    print("   panel %d: V_T = %g  ->  senior %g, junior %g, equity %g" % (idx + 1, v, s, j, e))

    chk("V_T %-5g three payoffs sum back to V_T" % v, s + j + e, v)
    chk_txt("V_T %-5g header names the asset value" % v, True, ">V_T = %g<" % v in p)
    chk_txt("V_T %-5g sum line under the stack" % v, True,
            ">%g + %g + %g = %g<" % (s, j, e, v) in p)

    # --- the two bucket outlines are drawn at the derived rim and floor
    chk_txt("V_T %-5g senior bucket outline runs rim 62 to floor 134" % v, True,
            'd="M14 %s L14 %s L86 %s L86 %s"' % (g(s_rim), g(S_FLOOR), g(S_FLOOR), g(s_rim)) in p)
    chk_txt("V_T %-5g junior bucket outline runs rim 154 to floor 202" % v, True,
            'd="M62 %s L62 %s L134 %s L134 %s"' % (g(j_rim), g(J_FLOOR), g(J_FLOOR), g(j_rim)) in p)
    chk_txt("V_T %-5g equity pool is drawn with no top edge" % v, True,
            ('d="M26 %s L26 %s L170 %s L170 %s"' % (g(POOL_TOP), g(P_FLOOR), g(P_FLOOR), g(POOL_TOP))
             in p) and ("no top edge" in p))

    # --- senior bucket
    y, h = water_rect(p, "15", "70", "#6b4ef0")
    chk("V_T %-5g senior water height = %g x 1.2" % (v, s), s * PX, h, 4)
    chk("V_T %-5g senior water top y = 134 - height" % v, s_top, y, 4)
    chk_txt("V_T %-5g senior water is labelled %g" % (v, s), True,
            amount_label(p, SENIOR_MID_X, s_top + s * PX / 2 + 4.5, s, "#fff"))
    chk_txt("V_T %-5g senior water is full only when V_T reaches F_S" % v,
            v >= FS_PIC, round(y, 4) == round(s_rim, 4))

    # --- the tap reaches the senior water surface
    m = re.search(r'<rect x="33" y="54" width="6" height="([\d.]+)" fill="#6b4ef0"/>', p)
    chk("V_T %-5g tap stream falls from 54 to the senior water surface" % v,
        s_top - TAP_OUT, float(m.group(1)), 4)

    # --- overflow from the senior rim into the junior bucket
    m = re.search(r'<path d="M86 63 L94 73 L94 ([\d.]+)"', p)
    chk_txt("V_T %-5g senior spills over only when the senior bucket is full" % v,
            v > FS_PIC, m is not None)
    if m:
        chk("V_T %-5g that stream ends on the junior water surface" % v,
            j_top, float(m.group(1)), 4)

    # --- junior bucket
    y, h = water_rect(p, "63", "70", "#b6791f")
    if j > 0:
        chk("V_T %-5g junior water height = %g x 1.2" % (v, j), j * PX, h, 4)
        chk("V_T %-5g junior water top y = 202 - height" % v, j_top, y, 4)
        chk_txt("V_T %-5g junior water is labelled %g" % (v, j), True,
                amount_label(p, JUNIOR_MID_X, j_top + j * PX / 2 + 4.5, j, "#fff"))
    else:
        chk_txt("V_T %-5g junior bucket is drawn with no water at all" % v, True, h is None)
        chk_txt("V_T %-5g junior bucket is labelled 0 and empty" % v, True,
                ('<text x="98" y="180" text-anchor="middle" font-size="13" font-weight="700" '
                 'fill="#6f6886">0</text>') in p)

    # --- overflow from the junior rim into the pool
    m = re.search(r'<path d="M134 155 L142 165 L142 ([\d.]+)"', p)
    chk_txt("V_T %-5g junior spills over only when the junior bucket is full" % v,
            v > FS_PIC + FJ_PIC, m is not None)
    if m:
        chk("V_T %-5g that stream ends on the pool water surface" % v,
            e_top, float(m.group(1)), 4)

    # --- equity pool
    y, h = water_rect(p, "27", "142", "#1f9d63")
    if e > 0:
        chk("V_T %-5g pool water height = %g x 1.2" % (v, e), e * PX, h, 4)
        chk("V_T %-5g pool water top y = 274 - height" % v, e_top, y, 4)
        chk_txt("V_T %-5g pool water is labelled %g" % (v, e), True,
                amount_label(p, POOL_MID_X, e_top + e * PX / 2 + 4.5, e, "#fff"))
    else:
        chk_txt("V_T %-5g pool is drawn with no water at all" % v, True, h is None)
        chk_txt("V_T %-5g pool is labelled 0 and empty" % v, True,
                ('<text x="98" y="252" text-anchor="middle" font-size="13" font-weight="700" '
                 'fill="#6f6886">0</text>') in p)

    # --- the word empty appears once for each vessel that holds nothing
    chk_txt("V_T %-5g the word empty appears once per empty vessel" % v,
            [j, e].count(0.0), p.count(">empty<"))

print("\n[PANEL 1 VISUAL - one scale, and the picture reads at phone width]")
_h = [float(re.search(r'<rect x="15" y="[\d.]+" width="70" height="([\d.]+)"', p).group(1))
      for p in panels]
chk_txt("the senior bucket is full at the same height in panels 2 and 3", _h[1], _h[2])
chk("a full senior bucket is F_S x 1.2 pixels tall", FS_PIC * PX, _h[1], 4)
chk_txt("every panel uses the same viewBox, so one scale holds across all three", 1,
        len(set(re.findall(r'<svg viewBox="([^"]+)"', HTML))))
chk_txt("each panel is capped at 184px wide so three fit a desktop row", 3,
        HTML.count("max-width:184px"))
chk_txt("the three panels sit in a flex-wrap row, so they stack on a narrow screen", True,
        "flex-wrap:wrap" in HTML)
chk_txt("every colour in the drawing comes from the theme variables", set(),
        set(re.findall(r"#[0-9a-f]{6}", HTML[HTML.index('<div class="svg-wrap">'):
                                             HTML.index('<p class="cap">')]))
        - {"#211c33", "#6f6886", "#6b4ef0", "#5238c4", "#1f9d63", "#b6791f", "#fff"})
chk_txt("the caption states the scale used", True,
        "1.2 pixels for every 1 of money" in HTML)
chk_txt("the caption states the two face values drawn", True,
        "F<sub>S</sub> 60 and F<sub>J</sub> 40" in HTML)
chk_txt("the prose says a bucket that is not full passes nothing down", True,
        "A bucket that is not full passes nothing" in HTML)
chk_txt("no em dash in the visual block", 0,
        HTML[HTML.index('The picture that makes it stick'):
             HTML.index('The three formulas from the sheet')].count("\u2014"))

# ---------------------------------------------------------------- panel 2 worked example
print("\n[PANEL 2 — worked example: F_S = 60, F_J = 45, junior received 18, find V_T]")
VT_BACK = 60 + 18 + 0
chk("V_T = senior 60 + junior 18 + equity 0", VT_BACK, 78.00)
chk("border F_S + F_J", 60 + 45, 105.00)
w_s, w_j, w_e = split(VT_BACK, 60, 45)
chk("forward check at V_T = 78: senior", w_s, 60.00)
chk("forward check at V_T = 78: junior", w_j, 18.00)
chk("forward check at V_T = 78: equity", w_e, 0.00)
chk("forward check at V_T = 78: sum", w_s + w_j + w_e, 78.00)
print("     78 sits between 60 and 105, so state II:", 60 <= 78 < 105)

# ---------------------------------------------------------------- panel 2 try-its
print("\n[PANEL 2 — try-it 1: the border, V_T = 80, F_S = 80, F_J = 40]")
b_s, b_j, b_e = split(80, 80, 40)
chk("border senior Min(80, 80)", b_s, 80.00)
chk("border junior Min(80 - 80, 40)", b_j, 0.00)
chk("border equity Max(80 - 120, 0)", b_e, 0.00)
chk("border F_S + F_J", 80 + 40, 120.00)
chk("border sum check", b_s + b_j + b_e, 80.00)

print("\n[PANEL 2 — try-it 2: V_T = 90, F_S = 60, F_J = 40]")
c_s, c_j, c_e = split(90, 60, 40)
chk("senior", c_s, 60.00)
chk("junior Min(90 - 60, 40)", c_j, 30.00)
chk("equity Max(90 - 100, 0)", c_e, 0.00)
chk("F_S + F_J", 60 + 40, 100.00)
chk("sum check", c_s + c_j + c_e, 90.00)
chk("the wrong answer 60 + 40 - 10 also sums to 90", 60 + 40 - 10, 90.00)
chk("junior shortfall 40 - 30", 40 - c_j, 10.00)

# ---------------------------------------------------------------- panel 3 worked example
print("\n[PANEL 3 — worked example: total owed 120, assets 95]")
chk("equity under strict APR Max(95 - 120, 0)", max(95 - 120, 0), 0.00)
chk("95 - 120 (the negative that becomes zero)", 95 - 120, -25.00)
chk("lenders' shortfall", 120 - 95, 25.00)

# ---------------------------------------------------------------- quiz
print("\n[QUIZ — every item recomputed]")

print("\n Q1  V_T 55, F_S 70, F_J 50  (state I)")
q1 = split(55, 70, 50)
chk("Q1 senior", q1[0], 55.00)
chk("Q1 junior", q1[1], 0.00)
chk("Q1 equity", q1[2], 0.00)
chk("Q1 sum check", sum(q1), 55.00)
chk("Q1 F_S + F_J quoted in the explanation", 70 + 50, 120.00)
chk("Q1 senior shortfall 70 - 55", 70 - 55, 15.00)
chk("Q1 distractor 55 - 120 shown as Max(-65, 0)", 55 - 120, -65.00)
chk("Q1 distractor 'equity -15' also sums to V_T", 70 + 0 - 15, 55.00)
chk("Q1 distractor 'junior first': senior 5 = 55 - 50", 55 - 50, 5.00)
chk("Q1 distractor 'equal split' 55 / 2", 55 / 2, 27.50)

print("\n Q2  V_T 64, F_S 45, F_J 35  (state II)")
q2 = split(64, 45, 35)
chk("Q2 senior", q2[0], 45.00)
chk("Q2 junior Min(64 - 45, 35)", q2[1], 19.00)
chk("Q2 equity", q2[2], 0.00)
chk("Q2 sum check", sum(q2), 64.00)
chk("Q2 F_S + F_J", 45 + 35, 80.00)
chk("Q2 junior shortfall 35 - 19", 35 - q2[1], 16.00)
chk("Q2 distractor 'junior first': senior 64 - 35", 64 - 35, 29.00)
chk("Q2 distractor 'equity -16' from 64 - 80", 64 - 80, -16.00)
chk("Q2 distractor 'both paid in full' sums to", 45 + 35 + 0, 80.00)

print("\n Q3  inverse: senior 30, junior 25, equity 41  (state III)")
chk("Q3 V_T = 30 + 25 + 41", 30 + 25 + 41, 96.00)
chk("Q3 F_S + F_J = 30 + 25", 30 + 25, 55.00)
q3 = split(96, 30, 25)
chk("Q3 forward check senior", q3[0], 30.00)
chk("Q3 forward check junior", q3[1], 25.00)
chk("Q3 forward check equity 96 - 30 - 25", q3[2], 41.00)
chk("Q3 distractor 'debts only' 30 + 25", 30 + 25, 55.00)
chk("Q3 distractor 'forgot senior' 41 + 25", 41 + 25, 66.00)

print("\n Q4  V_T 52, F_S 52, F_J 24  (exactly at F_S)")
q4 = split(52, 52, 24)
chk("Q4 senior Min(52, 52)", q4[0], 52.00)
chk("Q4 junior Min(52 - 52, 24)", q4[1], 0.00)
chk("Q4 equity Max(52 - 76, 0)", q4[2], 0.00)
chk("Q4 sum check", sum(q4), 52.00)
chk("Q4 F_S + F_J", 52 + 24, 76.00)
chk("Q4 distractor 'equity -24' from 52 - 76", 52 - 76, -24.00)
chk("Q4 distractor 'equal split' 52 / 2", 52 / 2, 26.00)
chk("Q4 distractor 'junior first': senior 52 - 24", 52 - 24, 28.00)

print("\n Q5 and Q6 are concept items with no arithmetic in the stem or the options.")

# ---------------------------------------------------------------- no reused numbers
print("\n[NO QUIZ ITEM REPEATS A WORKED EXAMPLE OR TRY-IT]")
PAGE_CASES = {
    "P1 worked (V_T, F_S, F_J)": (70, 43.2, 48),
    "P1 try-it 1": (120, 43.2, 48),
    "P1 try-it 2": (30, 43.2, 48),
    "P2 worked": (78, 60, 45),
    "P2 try-it 1": (80, 80, 40),
    "P2 try-it 2": (90, 60, 40),
    "pretest": (80, 50, 45),
}
QUIZ_CASES = {
    "Q1": (55, 70, 50),
    "Q2": (64, 45, 35),
    "Q3": (96, 30, 25),
    "Q4": (52, 52, 24),
}
clash = [(qn, pn) for qn, qc in QUIZ_CASES.items()
         for pn, pc in PAGE_CASES.items() if qc == pc]
chk_txt("quiz cases that reuse a taught case", [], clash)

# ---------------------------------------------------------------- page text spot checks
print("\n[THE PAGE ACTUALLY SAYS THESE]")
present("APR is named as the Absolute Priority Rule", "APR stands for Absolute Priority Rule")
present("the page states equity can never be negative", "equity can never be negative")
present("the page states the three payments sum to V_T",
        "the three payments must add up to exactly V")
present("recall answer 500.00 printed", "45 / 0.09 = 500.00")
present("recall answer 116.67 printed", "7 / 0.06 = 116.67")
present("worked example answer line", "Senior 43.2, junior 26.8, equity 0.")
present("panel 2 answer line", "The assets were worth 78 at maturity")
chk_txt("em dashes in the page (must be 0)", 0, HTML.count("—"))

# Mobile: any table of five or more columns must sit inside a .tscroll wrapper.
# The three-state table (State, where V_T sits, senior, junior, equity) has five.
_wide_ok = True
for _m in re.finditer(r"<table[^>]*>.*?</table>", HTML, re.S):
    _row = re.search(r"<tr>.*?</tr>", _m.group(0), re.S).group(0)
    _cols = len(re.findall(r"<t[hd]", _row))
    if _cols >= 5 and 'class="tscroll"' not in HTML[max(0, _m.start() - 160):_m.start()]:
        _wide_ok = False
        print("   wide table with %d columns is NOT inside a tscroll wrapper" % _cols)
chk_txt("every table of 5+ columns sits inside a tscroll", True, _wide_ok)
chk_txt("the three-state table is the wide one and is wrapped", True,
        'class="tscroll"' in HTML[:HTML.index("<th>State</th>")][-200:])
chk_txt("study.js is loaded before POF.quiz runs", True,
        HTML.index('src="assets/study.js"') < HTML.index("POF.quiz("))
chk_txt("theme.css is linked", True, 'href="assets/theme.css"' in HTML)
chk_txt("quiz has six items", 6, HTML.count('      tag: "'))
chk_txt("tags used", {"Payoff structure", "Concepts"},
        set(re.findall(r'^      tag: "([^"]+)"', HTML, re.M)))

# ---------------------------------------------------------------- summary
print("\n" + "=" * 132)
bad = [lab for ok, lab in CHECKS if not ok]
print("CHECKED %d numbers and facts." % len(CHECKS))
if bad:
    print("FAILED %d:" % len(bad))
    for lab in bad:
        print("   -", lab)
else:
    print("ALL PASSED.")
print("=" * 132)
