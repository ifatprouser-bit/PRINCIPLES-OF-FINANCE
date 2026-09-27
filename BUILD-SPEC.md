# BUILD-SPEC — Principles of Finance, 15-day study pack

Every agent working on this pack reads this file first, in full, before writing a line.
You load no skills. Everything you need is here. Where this file and your own instinct
disagree, this file wins.

Written 14 September 2026. Approved by Ifat in the session that produced it.

---

## 1. What we are building

A static website of 15 pages plus a hub. It is published to GitHub Pages and shared with
Ifat's MBA classmates. Each page is one study day.

The learner is an international MBA student at Bar-Ilan. English is a second language for
most of them. They are intelligent adults who are new to finance, not children.

**Exam being prepared for**

| Fact | Value |
|---|---|
| Date | Sunday 11 October 2026 |
| Length | 2.5 hours (150 minutes) |
| Questions | about 22, all multiple choice |
| Pace | 6.8 minutes per question |
| Formula sheet | supplied by the professor, so nothing has to be memorised |
| Calculator | scientific only. No programmable or financial calculator. Nothing that computes a bond price, an annuity value or a yield directly |
| Professor | Alon Raviv |

The professor's own exam guide says **40 to 60 percent of exam questions come from the problem
sets, quizzes and practice questions given during the term**.

---

## 2. THE HONESTY RULES. Read these twice.

**2.1 There are no past exam papers in this project.** None. Do not write "from a past final",
do not set `src:"From a past final"`, and do not imply any question is a real one. Every question
in this pack is written fresh. If you are tempted to tag something as real, the answer is no.

**2.2 Never invent to fill a gap.** If the course material does not settle something, say so in
your return summary and leave it out. A confident wrong statement in exam prep is worse than a
missing one.

**2.3 Two known errors in the course files. Do not copy them forward.**

- `NPV_and_IRR_Focused_Presentation.pptx` gives three different answers for its own Practice 1
  (NPV 3,193 and 1,641; IRR 16.65%, 13.7% and 100%) and contradicts itself on Practice 2
  (slide 13 says C, slide 16 says D). **Its answer keys are not trustworthy.** You may use its
  question shapes. You may not use its answers. Recompute everything.
- `Principles of finance notes.pdf` states Apple's expected return as 14%. That figure is
  disputed in Ifat's own study note. **Do not put any Apple expected-return figure on a page.**

**2.4 Where the course file and the textbook disagree, the course file wins**, and the page says
so in one line, because the exam follows the course.

**2.5 Every number is verified in code.** See section 8. No exceptions, including numbers you are
sure about.

---

## 3. The 15 days

Day 1 is Saturday 26 September 2026. Day 15 is Saturday 10 October. The exam is the next day.

| # | File | Date | Type | Teaches / tests |
|---|---|---|---|---|
| 1 | `day-01.html` | Sat 26.9 | Learn | What kind of thing is this number: real vs financial assets, the investment process, primary vs secondary markets, size vs move (equity vs dividend) |
| 2 | `day-02.html` | Sun 27.9 | Learn | A single cash flow: why we discount at all, present value, future value, discounting vs compounding |
| 3 | `day-03.html` | Mon 28.9 | Learn | Annuity: the same payment every period. PV and FV of an annuity |
| 4 | `day-04.html` | Tue 29.9 | Learn | Perpetuity and growth: plain perpetuity, growing perpetuity, growing annuity |
| 5 | `day-05.html` | Wed 30.9 | Learn | Mixed streams: a stream made of single cash flows plus an annuity. The professor names this the most likely exam question |
| 6 | `day-06.html` | Thu 1.10 | Learn | Bonds: par value, coupon, zero coupon, premium and discount bonds, price against interest rates, T-bills vs T-notes vs T-bonds, credit risk and inflation risk |
| 7 | `day-07.html` | Fri 2.10 | Learn | Who gets paid first: the Merton 1974 structure. Senior debt, junior (subordinated) debt, equity. Absolute Priority Rule. Default, Chapter 7 vs Chapter 11 |
| 8 | `day-08.html` | Sat 3.10 | Learn | Stocks: holding period return, dividend discount model with no growth and with constant growth, preferred stock |
| 9 | `day-09.html` | Sun 4.10 | Learn | Projects: NPV, IRR, problems with IRR, independent vs mutually exclusive projects |
| 10 | `day-10.html` | Mon 5.10 | **Mock 1** | 22 questions, whole course, even spread |
| 11 | `day-11.html` | Tue 6.10 | **Mock 2** | 22 questions, weighted to time value of money |
| 12 | `day-12.html` | Wed 7.10 | Sweep | Every topic, one concrete task each, then the error log |
| 13 | `day-13.html` | Thu 8.10 | **Mock 3** | 22 questions, weighted to bonds and payoffs |
| 14 | `day-14.html` | Fri 9.10 | **Mock 4** | 22 questions, dress rehearsal, the hardest set, whole course |
| 15 | `day-15.html` | Sat 10.10 | Warm-up | Three familiar tasks and the trap list. Nothing new |

**Estimated exam weighting** (from the professor's exam guide, not from counted past papers, so
treat it as an estimate and say so nowhere on the page):

| Topic | Share | Questions out of 22 |
|---|---|---|
| Concepts: environment, markets, agency, governance, ROA vs ROE, bankruptcy | 30% | 6 or 7 |
| Time value of money: single, annuity, perpetuity, growth, mixed streams | 30% | 6 or 7 |
| Bonds and fixed income | 18% | 4 |
| Payoff structure: senior, junior, equity | 10% | 2 |
| NPV and IRR | 9% | 2 |
| Stocks: holding period return, dividend model | 7% | 1 or 2 |

Mocks follow that shape unless their row above says otherwise.

---

## 4. Course scope — the formula sheet the exam supplies

Everything below is on the sheet the professor hands out. Learners do not memorise these. What
they must know is **which one applies and why**.

- Payoff at maturity, senior debt: `Min(V_T, F_S)`
- Payoff at maturity, equity: `Max(V_T − F_S, 0)`
- Payoff at maturity, junior/subordinated debt: `0` if `V_T < F_S`, otherwise `Min(V_T − F_S, F_J)`
- Discounting and compounding of a single cash flow
- Future value of an annuity; present value of an annuity; present value of a growing annuity
- Present value of a perpetuity; present value of a growing perpetuity
- Holding period return on a stock: `r = (P1 − P0 + D1) / P0`
- Present value of a stream of cash flows
- `NPV = sum of CF_i / (1+r)^i − I0`

`F_S` is the face value of the senior debt. `F_J` is the face value of the junior debt.
`V_T` is the value of the firm's assets at time T.

**APR in this course means Absolute Priority Rule**, not annual percentage rate. This single
three-letter confusion blocked a whole question for Ifat. Day 7 must state it plainly, and it
belongs on the day 15 trap list.

---

## 5. Where the material lives

Read your own sources with the `Projects` tool, method `project_read`, path exactly as written.
Read all of your day's sources before you write anything.

Shared by everyone:

- `formulas for the final 2025_Summer.docx` — the formula sheet
- `Final_Exam_Review_Summer 2025.doc` — the professor's exam guide and topic list
- `syllabus_Summer_2025.doc` — session-by-session outline

Per day:

| Day | Sources |
|---|---|
| 1 | `Class #1 Summary.docx`, `Class 2 Summary.docx`, `Finance_Classification_Quiz.pptx`, `Finance_Decision_Environments_Quiz.pptx`, `Principles of Finance.docx` |
| 2 | `Class 3 Summary.docx`, `Class 4 Summary.docx`, `Discounting and Compounding of a single cashflow.docx`, `Time_Value_of_Money.pdf` |
| 3 | `Class 4 Summary.docx`, `Class 5 Summary.docx`, `Time_Value_of_Money.pdf`, `POF 6` |
| 4 | `POF 6`, `Time_Value_of_Money.pdf`, `Principles of finance - notes.pdf` |
| 5 | `Class 5 Summary.docx`, `POF 6`, `Principles of finance - notes.pdf` |
| 6 | `Class 3 Summary.docx`, `Principles of finance - notes.pdf`, `Final_Exam_Review_Summer 2025.doc` |
| 7 | `Merton_1974_Senior_Subordinated_OneYear_v2_with_Table.pptx`, `POF 3.docx`, `Class 2 Summary.docx` |
| 8 | `Principles of finance - notes.pdf`, `Final_Exam_Review_Summer 2025.doc` |
| 9 | `NPV_and_IRR_Focused_Presentation.pptx` (shapes only, keys are broken), `Class 5 Summary.docx` |
| Mocks | the formula sheet, the exam guide, and the finished day pages 1 to 9 |

The four Excel models (`Payoff of bonds and stocks.xlsx`, `Annuity_PV_FV_AND COUPON BOND VALUE.xlsm`,
`Payoff of bonds and stocks _Advanced.xlsx`, `Growing_Annuity_Perpetuity.xlsm`) return a local file
path rather than text. Open them with `openpyxl` if you need them.

---

## 6. Page structure

### 6.1 Every page, top and bottom

```
<link rel="stylesheet" href="assets/theme.css">
```
in the head, and
```
<script src="assets/study.js"></script>
```
just before `</body>`. Do not inline the CSS or the JS. Do not load anything from the internet.
No fonts, no libraries, no images from a URL. A diagram is inline `<svg>`.

Top of every page, in order: a `.home` link back to `index.html` reading `← All 15 days`,
a `.crumb` reading `DAY N · <weekday> <date>`, an `h1`, a one-line `.lede`.

Bottom of every page: a `.navrow` with a back button to the previous day and a `.primary`
next button to the following day. Day 1 has no back button. Day 15's next button points at
`index.html`.

### 6.2 Learn day (days 1 to 9)

In this order:

1. **Recall box** — a `.preq` box headed `FIVE MINUTES: RECALL` with two short questions on an
   OLDER day's topic, never yesterday's. Answers behind a `data-reveal` button. The rotation is
   fixed, use exactly this:

   | Day | Recalls |
   |---|---|
   | 1 | nothing, say so in one line: this is the first day |
   | 2 | day 1 |
   | 3 | day 1 |
   | 4 | day 2 |
   | 5 | day 3 |
   | 6 | day 2 |
   | 7 | day 4 |
   | 8 | day 5 |
   | 9 | day 6 |

2. **Pretest** — a second `.preq` box headed `GUESS FIRST`, one concrete question pointed at
   today's key idea, with no answer shown. It is a guess, not a test. One line saying so.

3. **Teaching panels** — two to four `.panel` blocks, one idea each. Each panel has:
   - a heading
   - short teaching prose, `.p` paragraphs
   - a `.rule` box holding the one decision the learner must be able to make
   - a **visual**, either an inline `<svg>` in a `.svg-wrap` with a `.cap` caption, or a `.dtable`
   - a worked example: the full question in a `.question` box, then `.step` rows one operation at
     a time, then a `.ans` line
   - one or two `.tryq` problems with a `data-reveal` answer

4. **Quiz panel** — 6 questions. Mount point and script as in section 7.

5. Nav row.

**Keep each learn day to about 45 minutes**: 5 minutes recall, 15 teaching, 20 quiz, 5 log.
Two to four teaching panels. No more. If your day needs five, you have split the idea wrongly.

### 6.3 Mock day (days 10, 11, 13, 14)

1. A short `.panel` explaining the rules: 22 questions, 150 minutes, formula sheet below,
   scientific calculator, nothing is revealed until you submit.
2. A **formula sheet panel** reproducing section 4 of this file, laid out as labelled groups in
   a simple grid, never one run-on line. Same on all four mocks.
3. The mock mount point. The engine draws the timer, the questions, the submit button, the
   auto-submit, the results panel and the error log box. You supply only the items.
4. Nav row.

A mock shows no score and reveals no answer while it runs. The engine enforces this; do not add
anything that works around it.

### 6.4 Day 12, the sweep

Not a mock and not a teaching day. One row per topic, days 1 to 9, each with:
- the topic name
- one concrete task the learner does on paper right now, about 5 minutes
- a `data-reveal` answer

Then `<div id="errorlog"></div>` and `POF.mountErrorLog('errorlog')` so the learner reads their
own log top to bottom. Nothing new is taught on this page.

### 6.5 Day 15, the warm-up

Read an hour before the exam. It must settle nerves, not raise them.
- Three familiar tasks, the same shapes already practised, with revealed answers.
- A **trap list**: the mistakes this course actually punishes. At minimum: APR means Absolute
  Priority Rule; equity is a size and a dividend is a move; check `V_T` against `F_S` and then
  against `F_S + F_J` before computing anything; the three payoffs must sum to exactly `V_T`;
  equity can never be negative; a growing perpetuity needs `r > g`; timing, a payment at the end
  of year 1 is not discounted zero times.
- One closing line. Calm, short, no new content.

---

## 7. The quiz engine

You never write quiz JavaScript. You write data. The engine shuffles the options, tracks the
correct one by identity, reveals the explanation, and writes every miss to the error log.

Learn day, at the end of the page:

```html
<div class="panel">
  <h3>Quiz <span data-scorechip="quiz"></span></h3>
  <p class="note">Six questions. The answer appears when you pick.</p>
  <div id="quiz"></div>
</div>
<script>
POF.quiz({
  mount: "quiz",
  day: 3,
  topic: "Annuity",
  items: [ /* six item objects */ ]
});
</script>
```

Mock day:

```html
<div id="mock"></div>
<script>
POF.mock({
  mount: "mock",
  day: 10,
  topic: "Mock 1",
  minutes: 150,
  items: [ /* 22 item objects */ ]
});
</script>
```

An item:

```js
{
  q: "the stem, with any small data inline",
  opts: ["first", "second", "third", "fourth"],
  correct: 0,                    // index into opts AS YOU WROTE THEM
  tag: "Annuity",                // the topic label that appears in the error log
  exp: "the full worked explanation"
}
```

`tag` matters. It is what groups the learner's error log and what the Claude prompt is built
from. Use one of exactly these tags, nothing else:

`Concepts` · `Single cash flow` · `Annuity` · `Perpetuity` · `Mixed stream` · `Bonds` ·
`Payoff structure` · `Stocks` · `NPV and IRR`

---

## 8. Writing the questions

**8.1 No item may repeat its own page's worked example or try-it.** Not the same names, not the
same numbers. This is the single most common defect in this kind of build. Before you finish,
list every worked example and try-it on your page and check each quiz item against the list.

**8.2 Every item is solvable from what is visible beside it.** If a question needs a table, the
table is in the question or in a `.dtable` directly above the block. Never point at a table on
another page.

**8.3 Give the scenario, never the conclusion.** A stem states the raw numbers or the raw event.
It does not say "this is a growing perpetuity" or "the firm defaults" when working that out is
the skill being tested. That belongs in `exp`.

**8.4 Vary the axes, not just the names.** Across your set, flip each of these at least once:
- direction: the rate goes up AND down; the cash flow grows AND shrinks
- threshold side: `V_T` above `F_S` AND below it; `r` above `g` AND the case where `r ≤ g` breaks
- forward AND inverse: given PV find the payment, not only given the payment find PV
- both sides of a classification: premium bond AND discount bond
- a boundary case: exactly at `F_S`, or a zero-growth perpetuity

**8.5 Distractors are real mistakes, not noise.** The trap families this course actually
punishes:
- discounting an annuity one period too many or too few
- using the annuity formula on a perpetuity, or the reverse
- forgetting that a growing perpetuity needs `r > g`
- paying the junior debtholder before the senior one
- letting equity go negative instead of stopping at zero
- reading `V_T` as a cash flow rather than an asset value
- confusing the coupon rate with the yield
- adding cash flows from different years without discounting
- nominal against real
- APR read as annual percentage rate instead of Absolute Priority Rule

**8.6 Every calculation item gets a FULL worked explanation.** Never one line. In this order:
(a) name the formula; (b) identify each input from the stem; (c) numbered substitution steps, one
operation per line; (d) a check line that plugs the answer back; (e) the exact wrong calculation
behind each tempting distractor. Concept items may be shorter but must still say why each wrong
option is wrong.

**8.7 Spread the correct answers.** The engine shuffles at render, so do not worry about the
displayed order, but do not write every item with `correct: 0` either.

---

## 9. How the copy must read

This is a hard bar, not a style note. Most readers are not native English speakers.

- **Short sentences. Everyday words.** If a word has a shorter everyday twin, use the twin.
- **Keep the subject's own vocabulary** — perpetuity, coupon, face value, senior debt — and
  explain each one the first time it appears on that page.
- **No long dashes.** The em dash is banned in learner-facing copy. Use a full stop and two
  sentences, a colon, a pair of commas, or the actual words.
- **Never state the same fact twice on one screen.** A table and a paragraph must not say the
  same thing. But a visual does NOT license cutting the explanation: the picture is for the
  scanner, the prose is for the reader who wants to know what it means. Both stay.
- **State the current position once.** Do not pair every point with the version that was
  rejected. It doubles what the reader must hold.
- **No rhetorical questions** the reader answers yes to.
- **A list of name-plus-one-line items becomes rows with a label and the line beside it**, not
  bullet points.
- **Do not use the word "step"** for anything except the numbered rows of a worked example.

Swap table, apply it mechanically:

| Do not write | Write |
|---|---|
| utilise | use |
| approximately | about |
| ceased | stopped |
| commence | start |
| in the event that | if |
| prior to | before |
| subsequent to | after |
| it is necessary to | you need to |
| a multitude of | many |
| endeavour | try |
| at the expense of | costs you |
| drifting away from | far from |

---

## 10. Verification, and it is not optional

Before you finish, write `verify/day-NN.py` in the pack folder. It recomputes **every** number
that appears on your page: every worked example, every try-it, every quiz answer.

The script prints one line per number: a label, the computed value, and PASS or FAIL against
what your page says. Run it. If anything fails, fix the page, not the script.

Your return summary states how many numbers were checked and that they all passed. If you could
not verify something, say which one and why. That is a good answer. Inventing a number is not.

---

## 11. What NOT to change

The 15-day shape is decided and approved. You are filling in your day, not redesigning the pack.

- Do not change the day order, the day count, or which day teaches what.
- Do not move a topic from your day into another day.
- Do not add audio. There is no audio in this build.
- Do not add a pass mark. The course does not publish one.
- Do not edit `assets/theme.css` or `assets/study.js`. If you believe one has a bug, say so in
  your return summary and work around it.
- Do not write to any file except your own page and your own verify script.
- Do not touch another agent's page.

---

## 12. What to return

Five lines, this exact shape, nothing longer:

```
FILE: day-NN.html
PANELS: <how many teaching panels, and their headings>
QUIZ: <how many items, and the tags used>
VERIFIED: <how many numbers checked in code, all passed / which failed>
FLAGS: <anything you could not verify, anything missing from the sources, or "none">
```
