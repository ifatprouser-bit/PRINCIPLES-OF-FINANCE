#!/usr/bin/env python3
"""
verify/formulas.py

Checks formulas.html, the reference page for the 15-day Principles of Finance pack.

The page teaches nothing and computes nothing, so there are no arithmetic answers to
recompute. What can go wrong instead is DRIFT: the reference sheet quietly stating a
formula in a shape no lesson in the pack actually uses. So this script checks, for every
formula printed on formulas.html, that the identical formula is present on at least one
day page. If a day page is later rewritten, this script fails.

It also checks the page contract: theme stylesheet, study.js, no em dashes, wide tables
wrapped in .tscroll, and that every link on the page points at a file that exists.

Run:  python3 verify/formulas.py
"""

import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.dirname(HERE)
PAGE = os.path.join(PACK, "formulas.html")
DAY_FILES = ["day-%02d.html" % n for n in range(1, 16)]

results = []


def record(label, ok, detail=""):
    results.append((label, ok, detail))
    print("%-4s  %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


# ---------------------------------------------------------------- normalising

def norm(s):
    """Reduce a scrap of HTML to a canonical formula string.

    Superscripts become ^x, subscripts become _x, entities are decoded, square
    brackets become round ones, every dash becomes '-', multiplication becomes '*',
    and all whitespace is dropped. Two formulas that mean the same thing and are
    only laid out differently collapse to the same string. Two formulas that differ
    in substance, for example 1/(1+r)^n against (1+r)^-n, stay different.
    """
    s = re.sub(r"<sup>(.*?)</sup>", r"^\1", s, flags=re.S)
    s = re.sub(r"<sub>(.*?)</sub>", r"_\1", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.lower()
    s = s.replace("×", "*")
    for dash in "−–—‐‑":
        s = s.replace(dash, "-")
    s = s.replace("[", "(").replace("]", ")")
    s = s.replace(" ", " ")
    s = re.sub(r"\s+", "", s)
    return s


# ---------------------------------------------------------------- load sources

if not os.path.exists(PAGE):
    print("FAIL  formulas.html not found at %s" % PAGE)
    sys.exit(1)

page_raw = open(PAGE, encoding="utf-8").read()

days = {}
for name in DAY_FILES:
    p = os.path.join(PACK, name)
    if os.path.exists(p):
        days[name] = norm(open(p, encoding="utf-8").read())

print("Day pages loaded for comparison: %d" % len(days))
print("=" * 90)
print("PART 1  Every formula on the page exists, in the same shape, on a day page")
print("=" * 90)

# ---------------------------------------------------------------- the registry
#
# label, the core of the formula in canonical form, and where the pack teaches it.
# The core leaves out the "PV =" style prefix where a day page prints the same
# expression inside a table cell without one.

CORE = [
    # Payoff at maturity (day 7, and the four mock formula panels)
    ("Senior debt payoff",            "min(v_t,f_s)"),
    ("Junior debt, the zero case",    "v_t<f_s"),
    ("Junior debt payoff",            "min(v_t-f_s,f_j)"),
    ("Equity, senior debt only",      "max(v_t-f_s,0)"),
    ("Equity, senior and junior",     "max(v_t-f_s-f_j,0)"),
    # One cash flow (day 2)
    ("Present value, one cash flow",  "fv/(1+r)^n"),
    ("Future value, one cash flow",   "pv*(1+r)^n"),
    ("Rate from both ends",           "(fv/pv)^1/n-1"),
    # Many cash flows that end (days 3 and 4)
    ("Present value of an annuity",   "a*(1-1/(1+r)^n)/r"),
    ("Annuity PV, the other layout",  "a*(1-(1+r)^-n)/r"),
    ("Future value of an annuity",    "a*((1+r)^n-1)/r"),
    ("Growing annuity",               "cf1*(1-((1+g)/(1+r))^n)/(r-g)"),
    ("Growing annuity when r = g",    "n*a"),
    # Cash flows that never end (day 4)
    ("Perpetuity",                    "a/r"),
    ("Growing perpetuity",            "cf1/(r-g)"),
    ("Growing perpetuity needs r > g", "r>g"),
    # Stocks (day 8)
    ("Holding period return",         "(p_1-p_0+d_1)/p_0"),
    ("Dividend model, no growth",     "d/r"),
    ("Dividend model, growth",        "d_1/(r-g)"),
    ("Next year's dividend",          "d_0*(1+g)"),
    # Projects (days 5 and 9)
    ("Present value of a stream",     "cf_1/(1+r)^1+cf_2/(1+r)^2+…+cf_n/(1+r)^n"),
    ("Net present value",             "σcf_i/(1+r)^i-i_0"),
    # Bonds (day 6)
    ("Coupon payment",                "couponrate*parvalue"),
    # Taught in the pack, not on the exam sheet (days 8 and 2)
    ("Return on assets",              "roa=netincome/totalassets"),
    ("Return on equity",              "roe=netincome/equity"),
    ("Nominal against real",          "realrate+expectedinflation"),
]

core_strings = [c for _, c in CORE]

for label, core in CORE:
    found = sorted(n for n, text in days.items() if core in text)
    record(label, bool(found), "in " + ", ".join(found) if found else "NOT FOUND on any day page")

# ------------------------------------------------- every .math block is covered
print()
print("=" * 90)
print("PART 2  No formula slipped onto the page without being checked above")
print("=" * 90)

# Bare symbols are labels, not formulas. They still have to appear on a day page.
BARE = {"v_t": "V_T", "f_s": "F_S", "f_j": "F_J", "i_0": "I_0", "0": "the number zero"}

math_blocks = re.findall(r'<(?:div|span) class="math">(.*?)</(?:div|span)>', page_raw, flags=re.S)
record("Page carries .math blocks", len(math_blocks) > 0, "%d blocks found" % len(math_blocks))

uncovered = []
for block in math_blocks:
    n = norm(block)
    if any(core in n for core in core_strings):
        continue
    if n in BARE:
        if not any(n in text for text in days.values()):
            uncovered.append(n + " (symbol not on any day page)")
        continue
    uncovered.append(n)

record(
    "Every .math block maps to a checked formula",
    not uncovered,
    "all %d covered" % len(math_blocks) if not uncovered else "uncovered: " + " | ".join(uncovered),
)

# -------------------------------------- formulas printed inside table cells too
print()
print("=" * 90)
print("PART 3  Formulas printed in table cells match the same day pages")
print("=" * 90)

# These strings are copied out of formulas.html by hand. Each one is first checked to be
# literally present in the page, so the page and this script cannot drift apart, then
# checked to contain a formula core that a day page teaches.
CELL_FORMULAS = [
    ("Decision aid, single cash flow",  "PV = FV / (1 + r)<sup>N</sup>"),
    ("Decision aid, annuity",           "A × [ 1 &minus; 1 / (1 + r)<sup>n</sup> ] / r"),
    ("Decision aid, perpetuity",        "<td>A / r</td>"),
    ("Decision aid, growing annuity",   "CF1 × [ 1 &minus; ((1 + g) / (1 + r))<sup>n</sup> ] / (r &minus; g)"),
    ("Decision aid, growing perpetuity", "CF1 / (r &minus; g), needs r &gt; g"),
    ("Layout note, annuity as 1/(1+r)^n", "PV = A × [ 1 &minus; 1 / (1 + r)<sup>n</sup> ] / r</td>"),
    ("Layout note, annuity as (1+r)^-n", "PV = A × (1 &minus; (1 + r)<sup>&minus;n</sup>) / r"),
]

for label, literal in CELL_FORMULAS:
    # The page uses real characters, not entities, for the minus sign in most places.
    # Try the literal as written and with the entity swapped for the character.
    variants = {literal, literal.replace("&minus;", "−"), literal.replace("−", "&minus;")}
    present = any(v in page_raw for v in variants)
    if not present:
        record(label, False, "this exact text is NOT on the page any more")
        continue
    n = norm(literal)
    hit = [c for c in core_strings if c in n]
    if not hit:
        record(label, False, "cell text matches no checked formula")
        continue
    core = hit[0]
    found = sorted(name for name, text in days.items() if core in text)
    record(label, bool(found), "matches '%s', taught in %s" % (core, ", ".join(found)))

# ---------------------------------------------------------------- page contract
print()
print("=" * 90)
print("PART 4  Page contract")
print("=" * 90)

record(
    "Theme stylesheet linked in the head",
    '<link rel="stylesheet" href="assets/theme.css">' in page_raw,
)

script_ok = '<script src="assets/study.js"></script>' in page_raw
body_close = page_raw.rfind("</body>")
script_pos = page_raw.rfind('<script src="assets/study.js">')
record(
    "study.js loaded before </body>",
    script_ok and 0 < script_pos < body_close,
)

record("Nothing loaded from the internet", "http://" not in page_raw and "https://" not in page_raw)
record("No inline <style> block", "<style" not in page_raw)

em = page_raw.count("—")
record("No em dashes", em == 0, "found %d" % em if em else "")

record(
    "Home link to index.html at the top",
    '<a class="home" href="index.html">' in page_raw,
)
navrow = re.search(r'<div class="navrow">(.*?)</div>', page_raw, flags=re.S)
nav_links = re.findall(r'href="([^"]+)"', navrow.group(1)) if navrow else []
record(
    "Nav row at the bottom with one button back to index.html",
    nav_links == ["index.html"],
    "nav links: %s" % (nav_links or "none"),
)

# No quiz, no error log, no timer on this page.
record(
    "No quiz, error log or timer on this page",
    not any(k in page_raw for k in ("POF.quiz", "POF.mock", "mountErrorLog", 'class="timer"')),
)

# Links resolve.
bad = []
for href in sorted(set(re.findall(r'href="([^"]+)"', page_raw))):
    if href.startswith(("http", "mailto:", "#")):
        continue
    if not os.path.exists(os.path.join(PACK, href)):
        bad.append(href)
for src in sorted(set(re.findall(r'src="([^"]+)"', page_raw))):
    if src.startswith("http"):
        continue
    if not os.path.exists(os.path.join(PACK, src)):
        bad.append(src)
record("Every link and script path resolves", not bad, "broken: %s" % bad if bad else "")

# Wide tables wrapped.
wide_unwrapped = []
wide_total = 0
for m in re.finditer(r"<table\b.*?</table>", page_raw, flags=re.S):
    tbl = m.group(0)
    cols = max((len(re.findall(r"<t[hd]\b", row)) for row in re.findall(r"<tr\b.*?</tr>", tbl, flags=re.S)), default=0)
    if cols >= 5:
        wide_total += 1
        before = page_raw[max(0, m.start() - 120):m.start()]
        if '<div class="tscroll">' not in before:
            wide_unwrapped.append("table with %d columns" % cols)
record(
    "Tables of 5 or more columns sit inside .tscroll",
    not wide_unwrapped,
    "%d wide tables, all wrapped" % wide_total if wide_total else "no table on the page has 5 or more columns",
)

# ---------------------------------------------------------------- summary
print()
print("=" * 90)
failed = [r for r in results if not r[1]]
print("CHECKS RUN: %d    PASSED: %d    FAILED: %d" % (len(results), len(results) - len(failed), len(failed)))
if failed:
    for label, _, detail in failed:
        print("  FAILED: %s  %s" % (label, detail))
    sys.exit(1)
print("Every formula on formulas.html is printed in the same shape on a day page.")
sys.exit(0)
