# Principles of Finance: 15 day study pack

A static study site for the Bar-Ilan IMBA **Principles of Finance** final, Sunday 11 October 2026
(Prof. Alon Raviv). Nine learn days, four timed mocks, one sweep day, one warm-up.

Open `index.html`. No build step, no dependencies, no server needed beyond a plain static host.

## What is in here

```
index.html          the hub: all 15 days, the exam facts, and the error log
day-01 … day-15     one page per study day
assets/theme.css    the whole look
assets/study.js     the quiz engine, the timed mock engine, and the error log
verify/day-NN.py    the script that recomputes every number on that day's page
BUILD-SPEC.md       the standard the pack was built to
```

## The error log

Every question a learner gets wrong is saved in **their own browser**, under
`localStorage['pof.errorlog.v1']`. Nothing is sent anywhere. Nobody else can see it, including
whoever publishes the site.

At the bottom of each mock, on day 12, and on the hub, a button turns that log into a written
prompt the learner copies into Claude, so it can drill them on exactly what they keep missing.

Two limits, stated on the hub as well: the log lives in one browser on one device, and clearing
browsing data erases it. The prompt button doubles as the backup.

## Publishing on GitHub Pages

1. Push this folder to a repository.
2. Settings, then Pages, then set the source to the `main` branch and the root folder.
3. The site appears at `https://<user>.github.io/<repo>/`.

Nothing here reads from the internet, so it works offline and on a phone once loaded.

## Adding GoatCounter

Not yet added. When the site code exists, put the snippet in **one** place rather than in sixteen
page heads: every page already loads `assets/study.js`, so append this to the end of that file.

```js
(function () {
  var s = document.createElement('script');
  s.async = true;
  s.setAttribute('data-goatcounter', 'https://YOURCODE.goatcounter.com/count');
  s.src = '//gc.zgo.at/count.js';
  document.head.appendChild(s);
})();
```

Replace `YOURCODE`. One edit covers the whole site.

## Checking the numbers

```
for f in verify/day-*.py; do python3 "$f"; done
```

Every script recomputes that page's worked examples, try-its and quiz answers from scratch and
prints a pass or fail per number. All 16 pages were also checked a second time by a reader who did
not write them, working from the question stems alone rather than from the author's script.

## Honesty notes, carried from the build

- **There are no past exam papers in this pack.** Every question was written for it, except 19
  taken from the professor's own two class quizzes. Those are marked "From a course quiz" where
  they appear. Nothing claims to be a real past final.
- **`NPV_and_IRR_Focused_Presentation.pptx` contradicts itself.** It gives three different answers
  for its own Practice 1 and two different answers for Practice 2. Its question shapes were used;
  none of its answers were.
- **The notes PDF states Apple's expected return as 14%**, which is disputed. No Apple return
  figure appears anywhere in this pack.
- **The formula sheet and the class slides write equity differently**, as `Max(V_T − F_S, 0)` and
  as `Max(V_T − F_S − F_J, 0)`. The pack treats these as the same rule in two cases: equity gets
  what is left after all debt. Every payoff question is built so the three payoffs sum to exactly
  V_T, which is the check that settles it, and day 7 states both forms out loud.
- Where a course file was unclear, the page says so rather than picking a side quietly.

## Editing a page

Teaching content is plain HTML. Quiz questions are a data array at the bottom of each page:

```js
POF.quiz({ mount: "quiz", day: 3, topic: "Annuity", items: [ ... ] });
```

An item is `{ q, opts, correct, tag, exp }`, where `correct` is the index into `opts` as written.
The engine shuffles the options at render time and tracks the right one by identity, so the key
cannot drift out of step with the display.

`tag` must be one of: Concepts, Single cash flow, Annuity, Perpetuity, Mixed stream, Bonds,
Payoff structure, Stocks, NPV and IRR. It is what groups the learner's error log.

If you change a number, update `verify/day-NN.py` and re-run it.
