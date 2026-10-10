#!/usr/bin/env python3
"""
verify/formulas.py

Checks formulas.html, the reference page for the 15-day Principles of Finance pack.

Since 9 Oct 2026 the page is anchored to the OFFICIAL EXAM SHEET
("formulas for the final 2025_Summer.pdf"), not to the day pages. So the checks are:

  PART 0  Sheet fidelity: every formula the official sheet prints appears on the page,
          in the sheet's shape (fraction discounting, sheet letters). The sheet
          transcription is embedded below as the ground truth.
  PART 1  Day-page costumes: every alternate shape the day pages use is either the
          sheet shape itself or listed on the page as "other clothes".
  PART 2  Nothing slipped onto the page without being checked.
  PART 3  Table-cell formulas are the ones intended.
  PART 4  Page contract (theme, scripts, links, no em dashes, wide tables wrapped).
  PART 5  Regression guard: NO day page carries a negative exponent in any spelling.
          (A negative-exponent form cost a real wrong answer on 9 Oct 2026 because the
          official sheet never prints one.)

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

    Superscripts become ^x, subscripts become _x, entities are decoded, all brackets
    become round ones, every dash becomes '-', multiplication becomes '*', and all
    whitespace is dropped. Two formulas that mean the same thing and are only laid
    out differently collapse to the same string. Two formulas that differ in
    substance, for example 1/(1+r)^n against (1+r)^-n, stay different.
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
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"\s+", "", s)
    return s


# ---------------------------------------------------------------- load sources

if not os.path.exists(PAGE):
    print("FAIL  formulas.html not found at %s" % PAGE)
    sys.exit(1)

page_raw = open(PAGE, encoding="utf-8").read()
page_norm = norm(page_raw)

days_raw = {}
days = {}
for name in DAY_FILES:
    p = os.path.join(PACK, name)
    if os.path.exists(p):
        days_raw[name] = open(p, encoding="utf-8").read()
        days[name] = norm(days_raw[name])

print("Day pages loaded for comparison: %d" % len(days))

# ======================================================================= PART 0
print("=" * 90)
print("PART 0  Every formula the official exam sheet prints is on the page, sheet-shaped")
print("=" * 90)

# Hand-transcribed from the sheet images (150 dpi render, 9 Oct 2026).
# Canonical form after norm(). If the sheet ever changes, retranscribe here.
SHEET = [
    # page 1, first table (annuity; its heading on the sheet is misleading)
    ("Sheet p1 II  FV of annuity (C,t)",   "fv_t=c*(((1+r)^t-1)/r)"),
    ("Sheet p1 III PV of annuity (C,t)",   "pv=c*(1-(1/(1+r)^t))/r"),
    ("Sheet p1 IV  Perpetuity (C)",        "pv=c/r"),
    # page 1, second table (simple cash flow)
    ("Sheet p1 II  FV single (C,t)",       "fv_t=c*(1+r)^t"),
    ("Sheet p1 III PV single (C,t)",       "pv=c/(1+r)^t"),
    ("Sheet p1 IV  Basic PV equation",     "pv=fv_t/(1+r)^t"),
    # page 2
    ("Sheet p2 Bond value",                "bondvalue=c*(1-1/(1+r)^t)/r+f/(1+r)^t"),
    ("Sheet p2 Senior payoff",             "min(v_t,f_s)"),
    ("Sheet p2 Equity payoff",             "max(v_t-f_s,0)"),
    ("Sheet p2 Junior payoff",             "min(v_t-f_s,f_j)"),
    ("Sheet p2 FV annuity (A,n)",          "a*(((1+r)^n-1)/r)"),
    ("Sheet p2 Growing annuity A(1+g)",    "a(1+g)*((1-(1+g)^n/(1+r)^n)/(r-g))"),
    ("Sheet p2 Perpetuity (CF)",           "cf/r"),
    ("Sheet p2 Growing perpetuity (CF)",   "cf/(r-g)"),
    # page 3
    ("Sheet p3 HPR",                       "(p_1-p_0+d_1)/p_0"),
    ("Sheet p3 Price as dividend sum",     "p_0=d_1/(1+r)^1+d_2/(1+r)^2+d_3/(1+r)^3"),
    ("Sheet p3 Constant growth model",     "p_0=d_1/(r-g)"),
    ("Sheet p3 Required return",           "r=d_1/p_0+g"),
    # page 3 bottom and page 4
    ("Sheet p3 Stream (first+last term)",  "cf_1/(1+r)^1"),
    ("Sheet p3 Stream last term",          "cf_n/(1+r)^n"),
    ("Sheet p4 NPV",                       "σcf_i/(1+r)^i-i_0"),
]

for label, core in SHEET:
    record(label + " on formulas.html", core in page_norm,
           "" if core in page_norm else "sheet shape missing from the page")

# The three sheet traps must be named on the page.
TRAPS = [
    ("Trap: misleading page-1 heading named", "thevalueofasinglecashflow"),
    ("Trap: per Period selector named",       "perperiod"),
    ("Trap: A(1+g) first payment named",      "a(1+g)"),
]
page_text_lower = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", " ", page_raw)).lower())
for label, needle in TRAPS:
    record(label, needle in page_text_lower)

# ======================================================================= PART 1
print()
print("=" * 90)
print("PART 1  Every costume a day page wears is on the page (as the shape or as other clothes)")
print("=" * 90)

# Pack costumes still used on day pages. Each must appear on at least one day page
# (so the mapping on formulas.html is not stale) AND be represented on formulas.html.
COSTUMES = [
    ("Annuity PV, A/n fraction costume",  "a*(1-1/(1+r)^n)/r"),
    ("Growing annuity, CF1 costume",      "cf_1*(1-((1+g)/(1+r))^n)/(r-g)|cf1*(1-((1+g)/(1+r))^n)/(r-g)|(c_1/(r-g))*(1-((1+g)/(1+r))^n)"),
    ("Growing annuity r = g case",        "n*a"),
    ("Rate from both ends (off-sheet)",   "(fv/pv)^1/"),
    ("Coupon payment (off-sheet)",        "couponrate*parvalue"),
    ("ROA (off-sheet)",                   "roa=netincome/totalassets"),
    ("ROE (off-sheet)",                   "roe=netincome/equity"),
    ("Nominal against real (off-sheet)",  "realrate+expectedinflation"),
]
for label, cores in COSTUMES:
    variants = cores.split("|")
    found = sorted(n for n, text in days.items() if any(v in text for v in variants))
    record(label + " on a day page", bool(found),
           "in " + ", ".join(found) if found else "NOT FOUND on any day page")
    on_page = any(v in page_norm for v in variants)
    record(label + " represented on formulas.html", on_page,
           "" if on_page else "the page no longer shows or maps this costume")

# ======================================================================= PART 2
print()
print("=" * 90)
print("PART 2  No formula slipped onto the page without being checked above")
print("=" * 90)

BARE = {"v_t": "V_T", "f_s": "F_S", "f_j": "F_J", "i_0": "I_0", "0": "zero"}
KNOWN = [c for _, c in SHEET] + [v for _, cs in COSTUMES for v in cs.split("|")] + [
    # lines on the page that are sentences or sheet-conditional forms, checked here:
    "ifv_t<f_s→0",            # junior zero case as the sheet writes it
    "ifv_t>f_s→min(v_t-f_s,f_j)",
    "r>g",                    # growing perpetuity condition, shown as its own math span
    "max(v_t-f_s-f_j,0)",     # slides-only equity line, flagged on the page
    "d_next=d_now*(1+g)",     # next year's dividend move (sheet shows it inside box III)
    "p_0=d/r",                # no-growth model, flagged as g = 0 case
    "p_t=d_t*(1+g)/(r-g)",    # supernormal piece as the sheet prints it
    "npv=σcf_i/(1+r)^i-i_0",
    "presentvalueofaperpetuity=cf/r",
    "presentvalueofagrowingperpetuity=cf/(r-g)",
    "futurevalueofanannuity=a*(((1+r)^n-1)/r)",
    "r=(fv/pv)^1/t-1",
    "coupon=couponrate*parvalue",
    "hpr=(p_1-p_0+d_1)/p_0",
    "pv=a*(1-(1+r)^-n)/r",    # shown ONCE, inside "other clothes", as what a book may write
]

math_blocks = re.findall(r'<(?:div|span) class="math">(.*?)</(?:div|span)>', page_raw, flags=re.S)
record("Page carries .math blocks", len(math_blocks) > 0, "%d blocks found" % len(math_blocks))

uncovered = []
for block in math_blocks:
    n = norm(block)
    if any(core in n for core in KNOWN):
        continue
    if n in BARE:
        continue
    uncovered.append(n)

record(
    "Every .math block maps to a checked formula",
    not uncovered,
    "all %d covered" % len(math_blocks) if not uncovered else "uncovered: " + " | ".join(uncovered),
)

# ======================================================================= PART 3
print()
print("=" * 90)
print("PART 3  Table-cell formulas are the intended ones")
print("=" * 90)

CELLS = [
    ("Decision aid, single cash flow",   "pv=c/(1+r)^t"),
    ("Decision aid, annuity",            "c*(1-(1/(1+r)^t))/r"),
    ("Decision aid, perpetuity",         "c/r"),
    ("Decision aid, growing annuity",    "a(1+g)*((1-(1+g)^n/(1+r)^n)/(r-g))"),
    ("Decision aid, growing perpetuity", "cf/(r-g),needsr>g"),
    ("Other clothes: minus exponent explained once", "(1+r)^-nis1/(1+r)^n"),
    ("Other clothes: CF1 = A(1+g) equivalence",      "cf_1=a(1+g)"),
]
for label, core in CELLS:
    record(label, core in page_norm, "" if core in page_norm else "not found in page text")

# The minus-exponent form appears ONLY in the other-clothes context, nowhere as a taught form.
minus_count = page_norm.count("(1+r)^-n")
record("Minus-exponent form appears at most 3 times (rule box + other-clothes cell)",
       minus_count <= 3, "found %d" % minus_count)

# ======================================================================= PART 4
print()
print("=" * 90)
print("PART 4  Page contract")
print("=" * 90)

record("Theme stylesheet linked in the head",
       '<link rel="stylesheet" href="assets/theme.css">' in page_raw)

script_ok = '<script src="assets/study.js"></script>' in page_raw
body_close = page_raw.rfind("</body>")
script_pos = page_raw.rfind('<script src="assets/study.js">')
record("study.js loaded before </body>", script_ok and 0 < script_pos < body_close)

record("Nothing loaded from the internet", "http://" not in page_raw and "https://" not in page_raw)
record("No inline <style> block", "<style" not in page_raw)

em = page_raw.count("—")
record("No em dashes", em == 0, "found %d" % em if em else "")

record("Home link to index.html at the top",
       '<a class="home" href="index.html">' in page_raw)
navrow = re.search(r'<div class="navrow">(.*?)</div>', page_raw, flags=re.S)
nav_links = re.findall(r'href="([^"]+)"', navrow.group(1)) if navrow else []
record("Nav row at the bottom with one button back to index.html",
       nav_links == ["index.html"], "nav links: %s" % (nav_links or "none"))

record("No quiz, error log or timer on this page",
       not any(k in page_raw for k in ("POF.quiz", "POF.mock", "mountErrorLog", 'class="timer"')))

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
record("Tables of 5 or more columns sit inside .tscroll", not wide_unwrapped,
       "%d wide tables, all wrapped" % wide_total if wide_total else "no table on the page has 5 or more columns")

# ======================================================================= PART 5
print()
print("=" * 90)
print("PART 5  Regression guard: no day page carries a negative exponent, in any spelling")
print("=" * 90)

offenders = []
patterns = [r"<sup>\s*[−-]", r"\^−", r"⁻"]
for name, raw in days_raw.items():
    low = raw
    for pat in patterns:
        if re.search(pat, low):
            offenders.append("%s (%s)" % (name, pat))
            break
record("Day pages free of negative exponents", not offenders,
       "offenders: " + ", ".join(offenders) if offenders else "all %d day pages clean" % len(days_raw))

# ---------------------------------------------------------------- summary
print()
print("=" * 90)
failed = [r for r in results if not r[1]]
print("CHECKS RUN: %d    PASSED: %d    FAILED: %d" % (len(results), len(results) - len(failed), len(failed)))
if failed:
    for label, _, detail in failed:
        print("  FAILED: %s  %s" % (label, detail))
    sys.exit(1)
print("formulas.html matches the official exam sheet, maps every pack costume, and no day page")
print("carries a negative exponent.")
sys.exit(0)
