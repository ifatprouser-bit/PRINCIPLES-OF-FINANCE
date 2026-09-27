#!/usr/bin/env python3
"""
Verification for day-12.html (the sweep).

Day 12 teaches nothing new. It carries a coverage map and nine paper tasks,
one per learn day. This script recomputes EVERY number that appears on the
page and checks it against what the page says.

One line per number: label, computed value, PASS or FAIL.
"""

import re

RESULTS = []


def chk(label, computed, page, places=2):
    """Compare a computed value with what the page prints."""
    ok = round(computed, places) == round(page, places)
    RESULTS.append(ok)
    print("{:<62} computed {:>16}   page {:>16}   {}".format(
        label,
        ("{:,.%df}" % places).format(round(computed, places)),
        ("{:,.%df}" % places).format(round(page, places)),
        "PASS" if ok else "FAIL"))


def chk_exact(label, computed, page):
    ok = computed == page
    RESULTS.append(ok)
    print("{:<62} computed {:>16}   page {:>16}   {}".format(
        label, str(computed), str(page), "PASS" if ok else "FAIL"))


def annuity_factor(r, n):
    return (1 - (1 + r) ** -n) / r


def fv_factor(r, n):
    return ((1 + r) ** n - 1) / r


# ===================================================================
print("\n--- TASK 1 : day 1, real and financial assets, equity and a dividend ---")
# Assets 840,000. Debt 510,000. Dividend 90,000. Trade 20,000 shares at 14.
eq_before = 840_000 - 510_000
chk("T1 equity before the dividend", eq_before, 330_000)

assets_after = 840_000 - 90_000
chk("T1 assets after the cash leaves", assets_after, 750_000)

eq_after = assets_after - 510_000
chk("T1 equity after the dividend", eq_after, 240_000)

chk("T1 owner wealth check, equity after + cash in pocket", eq_after + 90_000, 330_000)

chk("T1 size of the secondary trade, 20,000 x 14", 20_000 * 14, 280_000)
chk("T1 cash reaching the firm from that trade", 0, 0)


# ===================================================================
print("\n--- TASK 2 : day 2, single cash flow ---")
# 18,000 at the end of year 7, r = 6%.
f7 = 1.06 ** 7
chk("T2 growth factor 1.06^7", f7, 1.503630, 6)

pv2 = 18_000 / f7
chk("T2 present value of 18,000 in 7 years at 6%", pv2, 11_971.03)

chk("T2 compounding the answer back, PV x 1.06^7", pv2 * f7, 18_000.00)

ratio2 = 18_000 / 9_500
chk("T2 ratio of the two ends, 18,000 / 9,500", ratio2, 1.894737, 6)

root2 = ratio2 ** (1 / 7)
chk("T2 seventh root of that ratio", root2, 1.095594, 6)

r2 = root2 - 1
chk("T2 yearly return from paying 9,500 (percent)", r2 * 100, 9.56)

chk("T2 check, 9,500 x (1+r)^7", 9_500 * (1 + r2) ** 7, 18_000.00)


# ===================================================================
print("\n--- TASK 3 : day 3, annuity ---")
# 7,500 a year for 11 years at 5%.
af3 = annuity_factor(0.05, 11)
chk("T3 annuity factor, 11 payments at 5%", af3, 8.306414, 6)

chk("T3 present value of 7,500 for 11 years", 7_500 * af3, 62_298.11)

fvf3 = fv_factor(0.05, 11)
chk("T3 future value factor, 11 payments at 5%", fvf3, 14.206787, 6)

fv3 = 7_500 * fvf3
chk("T3 value on the day of the eleventh payment", fv3, 106_550.90)

chk("T3 total paid in, 11 x 7,500", 11 * 7_500, 82_500)
chk("T3 interest earned, FV minus deposits", fv3 - 82_500, 24_050.90)

pay3 = 45_000 / af3
chk("T3 yearly payment repaying 45,000 over 11 years at 5%", pay3, 5_417.50)
chk("T3 check, payment x annuity factor", pay3 * af3, 45_000.00)


# ===================================================================
print("\n--- TASK 4 : day 4, perpetuity and growth ---")
# First payment 4,200 at the end of next year, r = 7%.
chk("T4a plain perpetuity, 4,200 / 0.07", 4_200 / 0.07, 60_000.00)

chk("T4b growing perpetuity, 4,200 / (0.07 - 0.03)", 4_200 / (0.07 - 0.03), 105_000.00)

br4 = (1.03 / 1.07) ** 10
chk("T4c (1.03 / 1.07)^10", br4, 0.683179, 6)
chk("T4c 1 minus that", 1 - br4, 0.316821, 6)

gaf4 = (1 - br4) / 0.04
chk("T4c growing annuity factor", gaf4, 7.920526, 6)

pv4c = 4_200 * gaf4
chk("T4c present value of 10 growing payments", pv4c, 33_266.21)

chk("T4 value lost by stopping after 10 payments", 105_000 - pv4c, 71_733.79)


# ===================================================================
print("\n--- TASK 5 : day 5, mixed stream ---")
# 3,000 at year 1; nothing at year 2; 5,000 in years 3 to 6; 20,000 at year 7. r = 8%.
a5 = 3_000 / 1.08
chk("T5 piece A, 3,000 at year 1", a5, 2_777.78)

af5 = annuity_factor(0.08, 4)
chk("T5 annuity factor, 4 payments at 8%", af5, 3.312127, 6)

v2_5 = 5_000 * af5
chk("T5 piece B hop 1, value dated year 2", v2_5, 16_560.63)

chk("T5 1.08^2", 1.08 ** 2, 1.1664, 4)

b5 = v2_5 / 1.08 ** 2
chk("T5 piece B hop 2, value at year 0", b5, 14_198.07)

chk("T5 1.08^7", 1.08 ** 7, 1.713824, 6)

c5 = 20_000 / 1.08 ** 7
chk("T5 piece C, 20,000 at year 7", c5, 11_669.81)

total5 = a5 + b5 + c5
chk("T5 total present value of the stream", total5, 28_645.66)

chk("T5 sense check, raw cash paid out", 3_000 + 4 * 5_000 + 20_000, 43_000)
chk("T5 error from stopping after hop 1 on piece B", v2_5 - b5, 2_362.56)


# ===================================================================
print("\n--- TASK 6 : day 6, bonds ---")
# Par 1,000, coupon rate 8%, 6 years left. Yield 5%, then 10%.
coupon6 = 0.08 * 1_000
chk("T6 coupon payment, 0.08 x 1,000", coupon6, 80)

af6a = annuity_factor(0.05, 6)
chk("T6 annuity factor, 6 years at 5%", af6a, 5.075692, 6)
chk("T6 present value of the 6 coupons at 5%", coupon6 * af6a, 406.06)

chk("T6 1.05^6", 1.05 ** 6, 1.340096, 6)
par6a = 1_000 / 1.05 ** 6
chk("T6 present value of the par value at 5%", par6a, 746.22)

price6a = coupon6 * af6a + par6a
chk("T6 price at a yield of 5%", price6a, 1_152.27)
chk_exact("T6 premium bond, price above par 1,000", price6a > 1_000, True)

af6b = annuity_factor(0.10, 6)
chk("T6 annuity factor, 6 years at 10%", af6b, 4.355261, 6)
chk("T6 present value of the 6 coupons at 10%", coupon6 * af6b, 348.42)

chk("T6 1.10^6", 1.10 ** 6, 1.771561, 6)
par6b = 1_000 / 1.10 ** 6
chk("T6 present value of the par value at 10%", par6b, 564.47)

price6b = coupon6 * af6b + par6b
chk("T6 price at a yield of 10%", price6b, 912.89)
chk_exact("T6 discount bond, price below par 1,000", price6b < 1_000, True)


# ===================================================================
print("\n--- TASK 7 : day 7, the payoff waterfall ---")
FS, FJ = 90, 60
chk("T7 first border, F_S", FS, 90)
chk("T7 second border, F_S + F_J", FS + FJ, 150)


def payoffs(vt, fs, fj):
    senior = min(vt, fs)
    junior = 0 if vt < fs else min(vt - fs, fj)
    equity = max(vt - fs - fj, 0)
    return senior, junior, equity


for vt, page_set in ((75, (75, 0, 0)), (130, (90, 40, 0)), (150, (90, 60, 0))):
    s, j, e = payoffs(vt, FS, FJ)
    chk("T7 V_T = {:>3}, senior".format(vt), s, page_set[0])
    chk("T7 V_T = {:>3}, junior".format(vt), j, page_set[1])
    chk("T7 V_T = {:>3}, equity".format(vt), e, page_set[2])
    chk("T7 V_T = {:>3}, the three payments add back to V_T".format(vt), s + j + e, vt)
    RESULTS.append(e >= 0)
    print("{:<62} equity is never negative                           {}".format(
        "T7 V_T = {:>3}, limited liability check".format(vt),
        "PASS" if e >= 0 else "FAIL"))


# ===================================================================
print("\n--- TASK 8 : day 8, stocks ---")
# (a) P0 = 150, P1 = 144, D1 = 10.50
gain8 = 144 - 150 + 10.50
chk("T8a price change, 144 - 150", 144 - 150, -6)
chk("T8a whole gain, price change plus dividend", gain8, 4.50)
chk("T8a holding period return (percent)", gain8 / 150 * 100, 3.00)
chk("T8a dividend part (percent)", 10.50 / 150 * 100, 7.00)
chk("T8a price part (percent)", -6 / 150 * 100, -4.00)

# (b) preferred share, fixed 4.50, r = 9%
chk("T8b preferred share, 4.50 / 0.09", 4.50 / 0.09, 50.00)

# (c) D0 = 2.40 paid, g = 3%, r = 11%
d1_8 = 2.40 * 1.03
chk("T8c next year's dividend, 2.40 x 1.03", d1_8, 2.472, 3)
chk("T8c share value, D1 / (r - g)", d1_8 / (0.11 - 0.03), 30.90)
chk("T8c the slip: using 2.40 on top instead of 2.472", 2.40 / 0.08, 30.00)


# ===================================================================
print("\n--- TASK 9 : day 9, NPV and IRR ---")
chk("T9 1.09^2", 1.09 ** 2, 1.1881, 4)
chk("T9 1.09^3", 1.09 ** 3, 1.295029, 6)

p9a = 9_000 / 1.09
p9b = 11_000 / 1.09 ** 2
p9c = 10_000 / 1.09 ** 3
chk("T9a present value of 9,000 at year 1", p9a, 8_256.88)
chk("T9a present value of 11,000 at year 2", p9b, 9_258.48)
chk("T9a present value of 10,000 at year 3", p9c, 7_721.83)

tot9 = p9a + p9b + p9c
chk("T9a present value of all three inflows", tot9, 25_237.20)
chk("T9a NPV of project one", tot9 - 24_000, 1_237.20)
RESULTS.append(tot9 - 24_000 > 0)
print("{:<62} NPV above zero, so accept                          {}".format(
    "T9a decision check", "PASS" if tot9 - 24_000 > 0 else "FAIL"))

pv9two = 7_500 / 1.09
chk("T9b present value of 7,500 at year 1", pv9two, 6_880.73)
npv9two = pv9two - 7_000
chk("T9b NPV of project two", npv9two, -119.27)
RESULTS.append(npv9two < 0)
print("{:<62} NPV below zero, so reject                          {}".format(
    "T9b decision check", "PASS" if npv9two < 0 else "FAIL"))

irr9 = 7_500 / 7_000 - 1
chk("T9c IRR of project two (percent)", irr9 * 100, 7.14)
RESULTS.append(irr9 < 0.09 and npv9two < 0)
print("{:<62} IRR below 9% and NPV below zero, the rules agree   {}".format(
    "T9c agreement check", "PASS" if (irr9 < 0.09 and npv9two < 0) else "FAIL"))


# ===================================================================
print("\n--- COVERAGE MAP : structure, and a check against the four built mocks ---")

import os
PACK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(PACK, "day-12.html"), encoding="utf-8") as fh:
    html = fh.read()

coverage = html.split('<table class="dtable">')[1].split("</table>")[0]
row_re = re.compile(
    r'<tr><td class="lab">([^<]*)</td><td>(\d)</td><td>([^<]+)</td>'
    r'<td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td><td>([^<]+)</td></tr>')
map_rows = row_re.findall(coverage)

chk("Coverage map, number of topic rows", len(map_rows), 35, 0)
chk("Coverage map, mock cells (35 rows x 4 mocks)", len(map_rows) * 4, 140, 0)

taught = [r[1] for r in map_rows]
for day in range(1, 10):
    count = taught.count(str(day))
    RESULTS.append(count >= 1)
    print("{:<62} {} topic rows for day {}                            {}".format(
        "Coverage map, day {} appears".format(day), count, day,
        "PASS" if count >= 1 else "FAIL"))

ALLOWED = ["Concepts", "Single cash flow", "Annuity", "Perpetuity",
           "Mixed stream", "Bonds", "Payoff structure", "Stocks", "NPV and IRR"]
bad = sorted({r[2] for r in map_rows} - set(ALLOWED))
RESULTS.append(not bad)
print("{:<62} {:>16}   {}".format(
    "Coverage map, every log tag is one of the nine allowed",
    "no others" if not bad else ", ".join(bad), "PASS" if not bad else "FAIL"))

cells = {c for r in map_rows for c in r[3:]}
RESULTS.append(cells <= {"\u2713", "no"})
print("{:<62} {:>16}   {}".format(
    "Coverage map, every mock cell is a tick or the word no",
    "/".join(sorted(cells)), "PASS" if cells <= {"\u2713", "no"} else "FAIL"))


# ---------- read the four finished mock papers ----------
print("\n--- THE FOUR MOCK PAPERS : what they actually contain ---")

MOCKS = [("Mock 1", "day-10.html"), ("Mock 2", "day-11.html"),
         ("Mock 3", "day-13.html"), ("Mock 4", "day-14.html")]
item_re = re.compile(
    r'\{\s*q:\s*"((?:[^"\\]|\\.)*)",\s*opts:\s*(\[.*?\]),\s*correct:\s*(\d+),'
    r'\s*tag:\s*"([^"]+)"', re.S)

papers = []
for label, fname in MOCKS:
    with open(os.path.join(PACK, fname), encoding="utf-8") as fh:
        mh = fh.read()
    items = item_re.findall(mh)
    papers.append((label, items))
    chk("{} ({}), number of items".format(label, fname), len(items), 22, 0)

# the three counts the coordinator called out, recomputed from the papers
TVM = {"Single cash flow", "Annuity", "Perpetuity", "Mixed stream"}
m3 = dict(papers)["Mock 3"]
chk("Mock 3, Concepts items", sum(1 for i in m3 if i[3] == "Concepts"), 5, 0)
chk("Mock 3, time value of money items", sum(1 for i in m3 if i[3] in TVM), 3, 0)
chk("Mock 4, Concepts items",
    sum(1 for i in dict(papers)["Mock 4"] if i[3] == "Concepts"), 7, 0)

# decision environment items: the options are exactly the three labels
ENV = {"certainty", "uncertainty", "ambiguity"}
for label, expected in (("Mock 1", 0), ("Mock 2", 3), ("Mock 3", 0), ("Mock 4", 6)):
    n = 0
    for q, opts, c, tag in dict(papers)[label]:
        found = {o.strip().strip('"').lower() for o in re.findall(r'"([^"]+)"', opts)}
        if found == ENV:
            n += 1
    chk("{}, certainty / uncertainty / ambiguity items".format(label), n, expected, 0)

env_row = [r for r in map_rows if r[0].startswith("Certainty")]
RESULTS.append(len(env_row) == 1 and env_row[0][1] == "1")
print("{:<62} {:>16}   {}".format(
    "Coverage map has the decision environments row, taught day 1",
    "found" if env_row else "missing",
    "PASS" if (len(env_row) == 1 and env_row[0][1] == "1") else "FAIL"))


# ---------- tag present in a paper => that tag is ticked somewhere ----------
print("\n--- MAP AGAINST PAPERS : every tag a paper carries is ticked in its column ---")
for col, (label, items) in enumerate(papers):
    present = {i[3] for i in items}
    for tag in ALLOWED:
        ticked = any(r[2] == tag and r[3 + col] == "\u2713" for r in map_rows)
        if tag in present:
            ok = ticked
            note = "{} item(s) carry this tag".format(sum(1 for i in items if i[3] == tag))
        else:
            ok = True
            note = "no item carries this tag" + (", still ticked (see below)" if ticked else "")
        RESULTS.append(ok)
        print("{:<40} {:<18} {:<44} {}".format(
            label + ", tag ticked?", tag, note, "PASS" if ok else "FAIL"))

# the one justified exception, stated out loud rather than hidden
m3_annuity_rows = [r[0] for r in map_rows if r[2] == "Annuity" and r[5] == "\u2713"]
expected_exception = ["Present value of an annuity"]
RESULTS.append(m3_annuity_rows == expected_exception)
print("\n{:<62} {:>16}   {}".format(
    "Mock 3 carries no Annuity item, so only this Annuity row is ticked",
    m3_annuity_rows[0] if m3_annuity_rows else "none",
    "PASS" if m3_annuity_rows == expected_exception else "FAIL"))
print("  reason: mock 3's seven bond questions and its NPV question cannot be")
print("  answered without the present value of an annuity factor.")


# ---------- the nine never-asked rows: prove the words are absent ----------
print("\n--- NEVER ASKED : the evidence behind the rows that say no four times ---")
never = [r[0] for r in map_rows if all(r[3 + k] == "no" for k in range(4))]
chk("Rows marked no in all four mock columns", len(never), 9, 0)
for name in never:
    print("    " + name)

# search question stems and options only. explanations do not count as a test.
stems = {}
for label, items in papers:
    stems[label] = " ".join(q + " " + o for q, o, c, t in items).lower()

ABSENT = ["real asset", "financial asset", "primary market", "secondary market",
          "capital budgeting", "payout decision", "t-bill", "t-note", "t-bond",
          "tips", "deposit insurance", "credit spread",
          "preferred", "mutually exclusive", "payback", "shareholder wealth"]
for word in ABSENT:
    hits = {lab: stems[lab].count(word) for lab, _ in papers}
    ok = sum(hits.values()) == 0
    RESULTS.append(ok)
    print("{:<62} {:>16}   {}".format(
        'no mock asks about "{}"'.format(word),
        "0 in all stems" if ok else str(hits), "PASS" if ok else "FAIL"))

# --- checking-agent additions -------------------------------------------
# The original block here asserted that days 1 to 9 never teach the forms of a
# business. That was false: day 1's fourth worked example teaches sole
# proprietorship, partnership, corporation and double taxation, which is why
# Mock 1's old question 13 was a repeat of it. The item was rewritten and the
# checks below keep it from coming back.
learn = ""
for d in range(1, 10):
    with open(os.path.join(PACK, "day-0{}.html".format(d)), encoding="utf-8") as fh:
        learn += fh.read().lower()
for word in ("sole propriet", "double taxation"):
    taught = learn.count(word) > 0
    asked = word in stems["Mock 1"]
    ok = not (taught and asked)
    RESULTS.append(ok)
    print("{:<62} {:>16}   {}".format(
        'no mock repeats the day 1 lesson on "{}"'.format(word),
        "taught only" if ok else "repeated", "PASS" if ok else "FAIL"))

# Row 26 is now ticked for Mock 1. The stem must describe the situation without
# naming it (spec 8.3), so the evidence is the explanation, not the stem.
with open(os.path.join(PACK, "day-10.html"), encoding="utf-8") as fh:
    m1_html = fh.read().lower()
ok = ("agency problem" in m1_html) and ("agency" not in stems["Mock 1"])
RESULTS.append(ok)
print("{:<62} {:>16}   {}".format(
    "Mock 1 tests the agency problem without naming it in the stem",
    "found" if ok else "missing", "PASS" if ok else "FAIL"))

for lab in ("Mock 2", "Mock 3", "Mock 4"):
    ok = "agency" not in stems[lab]
    RESULTS.append(ok)
    print("{:<62} {:>16}   {}".format(
        "{} does not ask the agency problem, as the map says".format(lab),
        "absent" if ok else "found", "PASS" if ok else "FAIL"))

# every table with five or more columns sits inside a .tscroll wrapper
for d in ("09", "10", "11", "12"):
    with open(os.path.join(PACK, "day-{}.html".format(d)), encoding="utf-8") as fh:
        page = fh.read()
    wide_unwrapped = 0
    for m in re.finditer(r"<table[^>]*>(.*?)</table>", page, re.S):
        rows_ = re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)
        cols = max((len(re.findall(r"<t[hd]", r)) for r in rows_), default=0)
        if cols >= 5 and "tscroll" not in page[max(0, m.start() - 200):m.start()]:
            wide_unwrapped += 1
    ok = wide_unwrapped == 0
    RESULTS.append(ok)
    print("{:<62} {:>16}   {}".format(
        "day-{}: every 5+ column table is inside .tscroll".format(d),
        str(wide_unwrapped) + " unwrapped", "PASS" if ok else "FAIL"))

# the two counts the takeaway notes state must match the table itself
one_tick = sum(1 for r in map_rows if sum(1 for c in r[3:] if c != "no") == 1)
chk_exact("rows with a tick on exactly one paper (page says eight)", one_tick, 8)


# ===================================================================
print("\n" + "=" * 112)
total = len(RESULTS)
failed = total - sum(RESULTS)
print("{} checks run. {} passed, {} failed.".format(total, sum(RESULTS), failed))
print("=" * 112)
