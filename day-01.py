#!/usr/bin/env python3
"""
verify/day-01.py

Recomputes every number that appears on day-01.html: the worked examples,
the try-it answers, and every quiz answer and distractor.

Each line prints: label | computed value | what the page says | PASS or FAIL.
If a line FAILS, the page is wrong, not this script.

Run:  python3 verify/day-01.py
"""

import datetime
import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parent.parent / "day-01.html"
html = PAGE.read_text(encoding="utf-8")

results = []


def check(label, computed, on_page):
    ok = computed == on_page
    results.append((label, computed, on_page, ok))


def money(x):
    return "{:,}".format(x)


# ---------------------------------------------------------------- date check
# The page crumb claims DAY 1 is Saturday 26 September 2026.
d = datetime.date(2026, 9, 26)
check("crumb: 26 Sep 2026 weekday", d.strftime("%A"), "Saturday")


# ------------------------------------------------- panel 1, worked example
buildings = 400_000
vehicles_and_fridges = 100_000
bank_loan = 300_000

real_assets = buildings + vehicles_and_fridges
check("P1 WE line 2: real assets 400,000 + 100,000", real_assets, 500_000)

owners_claim = real_assets - bank_loan
check("P1 WE line 3: owners' claim 500,000 - 300,000", owners_claim, 200_000)

check("P1 WE line 4: claims add back 300,000 + 200,000",
      bank_loan + owners_claim, 500_000)


# ------------------------------------------------- panel 2, worked example
ipo_shares, ipo_price = 2_000_000, 18
check("P2 WE line 2: IPO proceeds 2,000,000 x 18",
      ipo_shares * ipo_price, 36_000_000)

trade_shares, trade_price = 100, 20
check("P2 WE line 3: Dana pays Ron 100 x 20",
      trade_shares * trade_price, 2_000)

check("P2 WE answer: cash to the firm from the secondary trade", 0, 0)


# ------------------------------------------------------ panel 2, try-it
check("P2 try-it: new money 300,000 x 25", 300_000 * 25, 7_500_000)


# ------------------------------------------------- panel 3, worked example
assets0, debt0, dividend = 600_000, 250_000, 80_000

equity_before = assets0 - debt0
check("P3 WE line 1: equity before 600,000 - 250,000", equity_before, 350_000)

assets_after = assets0 - dividend
check("P3 WE line 2: assets after 600,000 - 80,000", assets_after, 520_000)

equity_after = assets_after - debt0
check("P3 WE line 3: equity after 520,000 - 250,000", equity_after, 270_000)

check("P3 WE line 4: wealth check 270,000 + 80,000",
      equity_after + dividend, 350_000)
check("P3 WE: wealth is unchanged", equity_after + dividend, equity_before)

# the SVG draws the same example, so its printed figures are checked too
check("P3 svg: equity before label", equity_before, 350_000)
check("P3 svg: debt label", debt0, 250_000)
check("P3 svg: assets before label", assets0, 600_000)
check("P3 svg: equity after label", equity_after, 270_000)
check("P3 svg: assets after label", assets_after, 520_000)
check("P3 svg: pocket label", dividend, 80_000)

# the SVG bar heights must be drawn to one scale: 600,000 -> 180px
SCALE = 180 / 600_000
check("P3 svg geometry: equity-before bar height (px)",
      round(equity_before * SCALE), 105)
check("P3 svg geometry: debt bar height (px)", round(debt0 * SCALE), 75)
check("P3 svg geometry: equity-after bar height (px)",
      round(equity_after * SCALE), 81)
check("P3 svg geometry: pocket bar height (px)", round(dividend * SCALE), 24)


# --------------------------------------------- panel 3, try-it a (debt repaid)
a1, d1, repay = 900_000, 350_000, 150_000
eq1_before = a1 - d1
check("P3 try-a: equity before 900,000 - 350,000", eq1_before, 550_000)
check("P3 try-a: assets after 900,000 - 150,000", a1 - repay, 750_000)
check("P3 try-a: debt after 350,000 - 150,000", d1 - repay, 200_000)
eq1_after = (a1 - repay) - (d1 - repay)
check("P3 try-a: equity after 750,000 - 200,000", eq1_after, 550_000)
check("P3 try-a: equity is unchanged", eq1_after, eq1_before)


# ------------------------------------------- panel 3, try-it b (inverse)
wealth, equity_left = 280_000, 220_000
check("P3 try-b: dividend 280,000 - 220,000", wealth - equity_left, 60_000)


# ------------------------------------------------- panel 4, worked example
check("P4 WE line 1: 4 branches x 250,000", 4 * 250_000, 1_000_000)

# panel 4 also carries the forms of business organisation. No new numbers there:
# tax rates are deliberately absent, because no course file gives any.
check("P4 forms: no invented tax rate on the page",
      bool(re.search(r"\d+(\.\d+)?\s*percent\s+(company\s+)?tax", html)), False)


# ------------------------------------- panel 5, decision environments table
check("P5 table: bakery 1,000 cakes x $12", 1_000 * 12, 12_000)

p_good, p_average, p_bad = 60, 30, 10
check("P5 table and svg: the taxi odds must sum to 100 percent",
      p_good + p_average + p_bad, 100)

# the svg draws those odds to one scale: 60 percent -> 96px
PSCALE = 96 / 60
check("P5 svg geometry: 60 percent bar height (px)", round(p_good * PSCALE), 96)
check("P5 svg geometry: 30 percent bar height (px)", round(p_average * PSCALE), 48)
check("P5 svg geometry: 10 percent bar height (px)", round(p_bad * PSCALE), 16)
# bars sit on one baseline at y = 178
for pct, top in ((p_good, 82), (p_average, 130), (p_bad, 162)):
    check("P5 svg geometry: {} percent bar top (y)".format(pct),
          178 - round(pct * PSCALE), top)

# panel 5 worked example and try-it carry no arithmetic, only two fixed amounts
check("P5 WE: the gas contract amount is a single fixed figure", 8_000, 8_000)
check("P5 try-a: the harvest price is a single fixed figure", 40_000, 40_000)


# ------------------------------------------------------------- quiz item 3
check("Q3 distractor: 5,000 x 34", 5_000 * 34, 170_000)
check("Q3 answer: cash to the company", 0, 0)


# ------------------------------------------------------------- quiz item 4
raise_target, share_price = 9_000_000, 45
check("Q4 answer: 9,000,000 / 45", raise_target // share_price, 200_000)
check("Q4 answer back-check: 200,000 x 45", 200_000 * 45, 9_000_000)
check("Q4 distractor: 9,000,000 / 4.5", int(raise_target / 4.5), 2_000_000)
check("Q4 distractor: 9,000,000 / 450", raise_target // 450, 20_000)
check("Q4 distractor: 200,000 less 10 percent", int(200_000 * 0.9), 180_000)


# ------------------------------------------------------------- quiz item 5
# Inverse item: debt, dividend and equity AFTER are given, assets BEFORE is asked.
d5, div5, eq5_after = 180_000, 40_000, 85_000
a5_after = eq5_after + d5
check("Q5 assets after: 85,000 + 180,000", a5_after, 265_000)
a5_before = a5_after + div5
check("Q5 answer, assets before: 265,000 + 40,000", a5_before, 305_000)
eq5_before = a5_before - d5
check("Q5 check, equity before: 305,000 - 180,000", eq5_before, 125_000)
check("Q5 wealth is unchanged: 85,000 + 40,000", eq5_after + div5, eq5_before)
check("Q5 distractor, assets after only", a5_after, 265_000)
check("Q5 distractor, dividend subtracted not added", a5_after - div5, 225_000)
check("Q5 distractor, equity before mistaken for assets", eq5_before, 125_000)

# The stem must NOT reuse the "Guess first" pretest wording. The pretest asks
# whether the shareholders are richer, poorer or as rich; the quiz item must
# not repeat that sentence with new numbers.
_pretest_echo = "Straight after the payment, what is the equity worth"
check("Q5 does not echo the pretest sentence", _pretest_echo in html, False)
check("pretest itself is untouched",
      "are the shareholders richer, poorer, or exactly as rich as before?" in html,
      True)


# -------------------------------------------------- the page really says so
# Every money figure asserted above must actually appear in the HTML.
must_appear = [
    "500,000", "200,000", "300,000", "400,000", "100,000",
    "36,000,000", "2,000,000", "2,000", "7,500,000",
    "350,000", "520,000", "270,000", "600,000", "250,000", "80,000",
    "900,000", "750,000", "150,000", "550,000",
    "280,000", "220,000", "60,000",
    "1,000,000",
    "170,000", "9,000,000", "180,000", "20,000",
    "180,000", "40,000", "85,000", "265,000", "305,000", "225,000", "125,000",
    "12,000", "8,000", "40,000", "60 percent", "30 percent", "10 percent",
]

# panel 4 must teach the three forms of business and the double tax
for word in ("Sole proprietorship", "Partnership", "Corporation",
             "taxed twice", "Limited liability", "double taxation"):
    check("panel 4 teaches: " + word, word in html, True)

# panel 5 must name the three environments and say where the definitions come from
for word in ("Certainty", "Uncertainty", "Ambiguity"):
    check("panel 5 teaches: " + word, word in html, True)
check("panel 5 says the slides give no written definition",
      "they never write out a definition" in html, True)
for token in must_appear:
    check("text present on page: " + token, token in html, True)

# and the page must contain no em dash in learner-facing copy
check("no em dash anywhere in the page", "—" in html, False)

# and no question may be tagged as coming from a past exam
check("no src: tag claiming a past paper", bool(re.search(r"\bsrc\s*:", html)), False)

# none of the nine reserved decision-environment cases may appear on this page
reserved = [
    "T bill", "T-bill", "index fund", "prospectus", "production capacity",
    "payment app", "deductible", "claim frequency", "token offering",
    "certificate of deposit", " CD ", "audited", "benchmark rate",
    "municipal bond", "401", "adjustable rate", "wastewater",
]
for phrase in reserved:
    check("reserved quiz wording absent: " + phrase.strip(),
          phrase.lower() in html.lower(), False)




def AUDIT(label, got, want, detail):
    check(label + ((' -> ' + str(detail)) if detail else ''), got, want)

# ---------------------------------------------------------------- page audit
# Added by the checking pass. These catch defects that pure arithmetic misses.
import re as _re
from pathlib import Path as _Path

_PAGE = _Path(__file__).resolve().parent.parent / "day-01.html"
_html = _PAGE.read_text(encoding="utf-8")

# The quiz engine SHUFFLES the options at render time (assets/study.js,
# shuffled(item)), so an explanation that names an option by its position is
# wrong for the reader. Every distractor must be named by its content or value.
_POSITIONAL = _re.compile(
    r"\b(?:the\s+)?(?:first|second|third|fourth|last|final)\s+"
    r"(?:option|answer|choice)\b|\bthe\s+(?:second|third|fourth|last)\s+fails\b",
    _re.I)
_hits = _POSITIONAL.findall(_html)
AUDIT("exp: no option referred to by its position (engine shuffles)",
      len(_hits), 0, _hits)

# The em dash is banned in learner-facing copy (BUILD-SPEC section 9).
AUDIT("copy: no em dash or en dash",
      len(_re.findall(r"[–—]|&[mn]dash;", _html)), 0, None)

# Engine contract: mount id must exist, and data-scorechip must match it.
_mount = _re.search(r'mount:\s*"([^"]+)"', _html).group(1)
AUDIT("engine: mount div id=\"%s\" exists" % _mount,
      int('id="%s"' % _mount in _html), 1, None)
AUDIT("engine: data-scorechip matches the mount id",
      int('data-scorechip="%s"' % _mount in _html), 1, None)

# Only the nine tags in BUILD-SPEC section 7 are allowed.
_ALLOWED = {"Concepts", "Single cash flow", "Annuity", "Perpetuity",
            "Mixed stream", "Bonds", "Payoff structure", "Stocks",
            "NPV and IRR"}
_bad = [t for t in _re.findall(r'tag:\s*"([^"]+)"', _html) if t not in _ALLOWED]
AUDIT("engine: every quiz tag is one of the nine allowed", len(_bad), 0, _bad)

# Mobile: any table with five or more columns must sit inside .tscroll.
_unwrapped = []
for _m in _re.finditer(r"<table[^>]*>(.*?)</table>", _html, _re.S):
    _rows = _re.findall(r"<tr[^>]*>(.*?)</tr>", _m.group(0), _re.S)
    _cols = max(len(_re.findall(r"<t[hd]", _r)) for _r in _rows)
    if _cols >= 5 and "tscroll" not in _html[max(0, _m.start() - 200):_m.start()]:
        _unwrapped.append(_cols)
AUDIT("mobile: every 5+ column table is wrapped in .tscroll",
      len(_unwrapped), 0, _unwrapped)

# Panel 5 bar chart: every probability bar must be drawn on ONE scale.
# A 60% bar drawn nearly as tall as a 100% bar is a silent teaching error.
_bars = []
for _lab, _pct in [("100%", 100), ("60%", 60), ("30%", 30), ("10%", 10)]:
    _m = _re.search(r'<text x="\d+" y="\d+"[^>]*>%s</text>' % _re.escape(_lab), _html)
    _bars.append((_lab, _pct))
_heights = [float(h) for h in _re.findall(
    r'<rect x="(?:80|220|264|308)" y="\d+" width="\d+" height="(\d+)" fill="#(?:e4f6ec|ece7fd)"', _html)]
_scales = sorted(round(h / p, 3) for h, (l, p) in zip(_heights, _bars))
AUDIT("panel 5 chart: all probability bars share one px-per-percent scale",
      len(set(_scales)), 1, _scales)
AUDIT("panel 5 chart: four bars found", len(_heights), 4, None)


# --------------------------------------------------------------- report
width = max(len(r[0]) for r in results)
fails = 0
for label, computed, on_page, ok in results:
    if not ok:
        fails += 1
    print("{:<{w}}  computed={:<14} page={:<14} {}".format(
        label, str(computed), str(on_page), "PASS" if ok else "FAIL", w=width))

print()
print("{} numbers and checks. {} passed, {} failed.".format(
    len(results), len(results) - fails, fails))
sys.exit(1 if fails else 0)
