#!/usr/bin/env python3
"""Verify every number printed on day-03.html (Annuity: PV and FV).

Each line: label, computed value, PASS/FAIL against what the page states.
If a line FAILS, fix the page, not this script.
"""

FAILS = 0
CHECKS = 0


def pv_factor(r, n):
    """Present value annuity factor: (1 - 1/(1+r)^n) / r."""
    return (1 - (1 + r) ** -n) / r


def fv_factor(r, n):
    """Future value annuity factor: ((1+r)^n - 1) / r."""
    return ((1 + r) ** n - 1) / r


def check(label, computed, on_page, dp=2):
    global FAILS, CHECKS
    CHECKS += 1
    ok = round(computed, dp) == round(on_page, dp)
    if not ok:
        FAILS += 1
    print("{:<62} {:>16.{dp}f}   page {:>16.{dp}f}   {}".format(
        label, computed, on_page, "PASS" if ok else "FAIL", dp=dp))


print("=" * 118)
print("PANEL 1 - three tests for an annuity (worked example and try-its)")
print("=" * 118)
check("W1 payment yr1: 500 / 1.06", 500 / 1.06 ** 1, 471.70)
check("W1 payment yr2: 500 / 1.06^2", 500 / 1.06 ** 2, 445.00)
check("W1 1.06^2", 1.06 ** 2, 1.1236, 4)
check("W1 payment yr3: 500 / 1.06^3", 500 / 1.06 ** 3, 419.81)
check("W1 1.06^3", 1.06 ** 3, 1.191016, 6)
check("W1 total the long way", sum(500 / 1.06 ** k for k in (1, 2, 3)), 1336.51)
check("W1 same total via the annuity formula", 500 * pv_factor(0.06, 3), 1336.51)
check("W1 raw sum with no discounting (page says 1,500)", 500 * 3, 1500.00)
check("T1b 800 at end of yr 4, 6%: 800 / 1.06^4", 800 / 1.06 ** 4, 633.67)
check("T1b 1.06^4", 1.06 ** 4, 1.262477, 6)
check("T1b the wrong slip, only three divisions", 800 / 1.06 ** 3, 671.70)


def AUDIT(label, got, want, detail):
    check(label + ((' -> ' + str(detail)) if detail else ''), got, want, dp=0)

# ---------------------------------------------------------------- page audit
# Added by the checking pass. These catch defects that pure arithmetic misses.
import re as _re
from pathlib import Path as _Path

_PAGE = _Path(__file__).resolve().parent.parent / "day-03.html"
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

# Both timelines: the year ticks must be evenly spaced.
for _y1, _name in [("113", "panel 1 (discounting back)"), ("53", "panel 3 (compounding forward)")]:
    _ticks = sorted(int(x) for x in _re.findall(
        r'<line x1="(\d+)" y1="%s" x2="\d+" y2="\d+" stroke' % _y1, _html))
    _gaps = [_ticks[i + 1] - _ticks[i] for i in range(len(_ticks) - 1)]
    AUDIT("%s: four year ticks" % _name, len(_ticks), 4, _ticks)
    AUDIT("%s: ticks evenly spaced" % _name, max(_gaps) - min(_gaps), 0, _gaps)

print()
print("=" * 118)
print("PANEL 2 - present value of an annuity")
print("=" * 118)
# the annuity factor table
for n in (5, 10, 20):
    for r, stated in zip((0.04, 0.08, 0.12), {
            5: (4.4518, 3.9927, 3.6048),
            10: (8.1109, 6.7101, 5.6502),
            20: (13.5903, 9.8181, 7.4694)}[n]):
        check("factor table  n={:<3} r={:.0%}".format(n, r), pv_factor(r, n), stated, 4)

check("W2 1.12^5", 1.12 ** 5, 1.762342, 6)
check("W2 1 / 1.12^5", 1 / 1.12 ** 5, 0.567427, 6)
check("W2 1 - 0.567427", 1 - 1 / 1.12 ** 5, 0.432573, 6)
check("W2 annuity factor 12%, 5 years", pv_factor(0.12, 5), 3.604776, 6)
check("W2 PV of the 3,000 instalments", 3000 * pv_factor(0.12, 5), 10814.33)
for k, stated in zip(range(1, 6), (2678.57, 2391.58, 2135.34, 1906.55, 1702.28)):
    check("W2 long way, payment year {}".format(k), 3000 / 1.12 ** k, stated)
check("W2 long way, total", sum(3000 / 1.12 ** k for k in range(1, 6)), 10814.33)
check("T2a factor 7%, 6 years", pv_factor(0.07, 6), 4.766540, 6)
check("T2a PV of 4,000 for 6 years at 7%", 4000 * pv_factor(0.07, 6), 19066.16)
check("T2a factor 4%, 6 years", pv_factor(0.04, 6), 5.242137, 6)
check("T2a PV of 4,000 for 6 years at 4%", 4000 * pv_factor(0.04, 6), 20968.55)
check("T2a the rise when the rate falls to 4%",
      4000 * pv_factor(0.04, 6) - 4000 * pv_factor(0.07, 6), 1902.39)
check("T2b factor 8%, 5 years", pv_factor(0.08, 5), 3.992710, 6)
check("T2b payment on a 25,000 loan", 25000 / pv_factor(0.08, 5), 6261.41)
check("T2b check: payment x factor back to 25,000",
      (25000 / pv_factor(0.08, 5)) * pv_factor(0.08, 5), 25000.00)

print()
print("=" * 118)
print("PANEL 3 - future value of an annuity")
print("=" * 118)
check("SVG 2,000 saved end yr1, compounded 2 years at 8%", 2000 * 1.08 ** 2, 2332.80)
check("SVG 2,000 saved end yr2, compounded 1 year at 8%", 2000 * 1.08 ** 1, 2160.00)
check("SVG 2,000 saved end yr3, no interest", 2000 * 1.08 ** 0, 2000.00)
check("SVG total at the end of year 3", 2000 * fv_factor(0.08, 3), 6492.80)
check("W3 1.08^40", 1.08 ** 40, 21.724521, 6)
check("W3 1.08^40 - 1", 1.08 ** 40 - 1, 20.724521, 6)
check("W3 FV factor 8%, 40 years", fv_factor(0.08, 40), 259.056519, 6)
check("W3 FV of 2,000 a year for 40 years at 8%", 2000 * fv_factor(0.08, 40), 518113.04)
check("W3 total paid in", 40 * 2000, 80000.00)
check("W3 interest earned", 2000 * fv_factor(0.08, 40) - 80000, 438113.04)
check("T3a 1.05^10", 1.05 ** 10, 1.628895, 6)
check("T3a 1.05^10 - 1", 1.05 ** 10 - 1, 0.628895, 6)
check("T3a FV factor 5%, 10 years", fv_factor(0.05, 10), 12.577893, 6)
check("T3a FV of 1,500 a year for 10 years at 5%", 1500 * fv_factor(0.05, 10), 18866.84)
check("T3a interest part", 1500 * fv_factor(0.05, 10) - 15000, 3866.84)
check("T3b FV factor 6%, 8 years", fv_factor(0.06, 8), 9.897468, 6)
check("T3b yearly saving to reach 60,000", 60000 / fv_factor(0.06, 8), 6062.16)
check("T3b check: saving x factor back to 60,000",
      (60000 / fv_factor(0.06, 8)) * fv_factor(0.06, 8), 60000.00)

print()
print("=" * 118)
print("QUIZ - every option and every number quoted in an explanation")
print("=" * 118)

print("-- Q1 concept item: no arithmetic on the page, only the 2,400 / 2,400 / 2,600 stream")

print("-- Q2: 900 a year for 4 years, rate falls from 10% to 6%")
check("Q2 1.06^4", 1.06 ** 4, 1.262477, 6)
check("Q2 1 / 1.06^4", 1 / 1.06 ** 4, 0.792094, 6)
check("Q2 1 - 0.792094", 1 - 1 / 1.06 ** 4, 0.207906, 6)
check("Q2 factor 6%, 4 years", pv_factor(0.06, 4), 3.465106, 6)
check("Q2 CORRECT answer", 900 * pv_factor(0.06, 4), 3118.60)
for k, stated in zip(range(1, 5), (849.06, 801.00, 755.66, 712.88)):
    check("Q2 check, long way year {}".format(k), 900 / 1.06 ** k, stated)
check("Q2 check, long way total", sum(900 / 1.06 ** k for k in range(1, 5)), 3118.60)
check("Q2 distractor, stale 10% rate", 900 * pv_factor(0.10, 4), 2852.88)
check("Q2 distractor, factor at 10%", pv_factor(0.10, 4), 3.169865, 6)
check("Q2 distractor, one period too few", 900 * pv_factor(0.06, 4) * 1.06, 3305.71)
check("Q2 distractor, no discounting", 900 * 4, 3600.00)

print("-- Q3: 40,000 loan repaid over 9 years at 5%")
check("Q3 1.05^9", 1.05 ** 9, 1.551328, 6)
check("Q3 1 / 1.05^9", 1 / 1.05 ** 9, 0.644609, 6)
check("Q3 1 - 0.644609", 1 - 1 / 1.05 ** 9, 0.355391, 6)
check("Q3 factor 5%, 9 years", pv_factor(0.05, 9), 7.107822, 6)
check("Q3 CORRECT answer", 40000 / pv_factor(0.05, 9), 5627.60)
check("Q3 check, payment x factor", (40000 / pv_factor(0.05, 9)) * pv_factor(0.05, 9), 40000.00)
check("Q3 distractor, no interest", 40000 / 9, 4444.44)
check("Q3 distractor, FV factor used", fv_factor(0.05, 9), 11.026564, 6)
check("Q3 distractor, divided by the FV factor", 40000 / fv_factor(0.05, 9), 3627.60)
check("Q3 distractor, perpetuity payment", 40000 * 0.05, 2000.00)

print("-- Q4: 3,200 a year for 7 years at 4%, value at the end")
check("Q4 1.04^7", 1.04 ** 7, 1.315932, 6)
check("Q4 1.04^7 - 1", 1.04 ** 7 - 1, 0.315932, 6)
check("Q4 FV factor 4%, 7 years", fv_factor(0.04, 7), 7.898294, 6)
check("Q4 CORRECT answer", 3200 * fv_factor(0.04, 7), 25274.54)
check("Q4 check, paid in", 7 * 3200, 22400.00)
check("Q4 check, interest", 3200 * fv_factor(0.04, 7) - 22400, 2874.54)
check("Q4 distractor, last payment given a year of interest",
      3200 * fv_factor(0.04, 7) * 1.04, 26285.52)
check("Q4 distractor, no interest", 3200 * 7, 22400.00)
check("Q4 distractor, PV instead of FV", 3200 * pv_factor(0.04, 7), 19206.57)
check("Q4 distractor, PV factor 4%, 7 years", pv_factor(0.04, 7), 6.002055, 6)

print("-- Q5: 5,000 a year for 12 years, rate rises from 6% to 8%")
check("Q5 1.06^12", 1.06 ** 12, 2.012196, 6)
check("Q5 1 / 1.06^12", 1 / 1.06 ** 12, 0.496969, 6)
check("Q5 factor 6%, 12 years", pv_factor(0.06, 12), 8.383844, 6)
check("Q5 PV at 6%", 5000 * pv_factor(0.06, 12), 41919.22)
check("Q5 1.08^12", 1.08 ** 12, 2.518170, 6)
check("Q5 1 / 1.08^12", 1 / 1.08 ** 12, 0.397114, 6)
check("Q5 factor 8%, 12 years", pv_factor(0.08, 12), 7.536078, 6)
check("Q5 PV at 8%", 5000 * pv_factor(0.08, 12), 37680.39)
check("Q5 CORRECT answer, the fall",
      5000 * pv_factor(0.06, 12) - 5000 * pv_factor(0.08, 12), 4238.83)
check("Q5 distractor, flat 2% on each payment", 5000 * 0.02 * 12, 1200.00)

print("-- Q6: a single 6,000 at end of year 1, 9%, fed into the annuity formula with n = 1")
check("Q6 1 / 1.09", 1 / 1.09, 0.917431, 6)
check("Q6 1 - 0.917431", 1 - 1 / 1.09, 0.082569, 6)
check("Q6 annuity factor 9%, n = 1", pv_factor(0.09, 1), 0.917431, 6)
check("Q6 CORRECT answer", 6000 * pv_factor(0.09, 1), 5504.59)
check("Q6 check, the single cash flow way", 6000 / 1.09, 5504.59)
check("Q6 distractor, no discounting at all", 6000.0, 6000.00)
check("Q6 distractor, perpetuity 6,000 / 0.09", 6000 / 0.09, 66666.67)
check("Q6 distractor, discounted twice", 6000 / 1.09 ** 2, 5050.08)

print()
print("=" * 118)
print("Numbers checked: {}   Failures: {}".format(CHECKS, FAILS))
print("RESULT:", "ALL PASS" if FAILS == 0 else "{} FAILED".format(FAILS))
print("=" * 118)
raise SystemExit(1 if FAILS else 0)
