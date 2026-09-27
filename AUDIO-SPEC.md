# AUDIO-SPEC — the audio strips for the 15-day Principles of Finance pack

Every agent writing a script reads this file first, in full. You load no skills. Everything you
need is here. Where this file and your instinct disagree, this file wins.

Written 22 September 2026. Read `BUILD-SPEC.md` as well: it holds the exam profile, the day table
and the honesty rules, all of which still apply.

---

## 1. What you are writing, and what you are not

You are writing **scripts**, as plain text files. No audio is generated in this pass. Ifat has not
heard a single voice yet, and nobody should generate forty files before she has approved one.

You are also **not** touching any HTML. The players go on the pages only once real mp3 files
exist. A player pointing at a missing file is worse than no player.

One file per strip, in `audio/`, named `day-NN-<slug>.txt`. The slug is short and describes the
section: `day-07-intro.txt`, `day-07-waterfall.txt`, `day-07-method.txt`.

---

## 2. THE ONE DECISION EVERYTHING ELSE FOLLOWS FROM

**Split the material into principle and procedure.**

- **Principle** goes in audio. The why. The intuition. What kind of thing a number is.
- **Procedure** stays on the page. Calculations, formulas, tables, multi-step method.

The reason is not style, it is how hearing works. A spoken sentence is gone the instant it is
said, and working memory has to hold each piece with nothing to look back at. A written line can
be re-read for free. By the third spoken number, the first has evaporated.

**The test:** would the listener need to hold a number, or see a step, to follow this? If yes, it
is procedure and it stays on the page.

**The one exception.** A strip that sits directly beside its own worked example on screen may walk
**one** calculation aloud, slowly, naming each number as the eye finds it. The listener has the
table to look back at. What stays banned everywhere: rattling off several figures with nothing on
screen to anchor them.

**And a practical reason to keep numbers out even then.** A strip that narrates an example's
numbers is welded to that example. The day someone edits the page, the audio silently goes stale
and the learner hears one thing while reading another. Reference the *story* (the buckets, the
gold mine), never the arithmetic.

---

## 3. Who is listening

Ifat, and her Bar-Ilan IMBA classmates. Adults with careers. English is a second language for
most of them. They are new to finance, not new to thinking.

**Ifat has said plainly that she does not yet understand what equity is, or what a bond is.** She
is the target listener. If a strip would leave her still asking "but why is that equity", it has
failed, however correct it is.

---

## 4. The rules for a script

**4.1 Never mention the format.** No "in this strip", "the numbers are on the page", "scroll
down", "as you can see in the diagram below". Format talk breaks the spell and spends attention
on production trivia. The episode must sound purely about its topic.

The one place this bends: **guiding the eye across a visual that is on screen is teaching, not
format talk.** "The top bucket fills first, then the one under it" is fine and wanted.

**4.2 Ask before you tell.** Open with a concrete question from the listener's world, then invite
a real pause: "Take a moment and picture it." A learner who has guessed, even wrongly, remembers
the answer better. Point the question at the exact idea you want remembered.

**4.3 Two or three stories per principle, not one.** One story is a claim. Three make it a pattern
the listener can generalise. Keep the same underlying mechanism and change the setting, so it is
clear the *idea* repeats and not the example.

**4.4 Name the terms first.** The intro strip names the few words the listener will meet that day,
and nothing more. Knowing the names frees working memory for the reasoning.

**4.5 One idea per strip.** If your strip has two ideas, it is two strips, or one of them belongs
to a different section.

**4.6 Close with recall.** "Take a breath and recall one thing" and then the single core idea.

---

## 5. The two voices, and how they must behave

Two hosts. **NOA** teaches. **TOM** is the curious learner.

The failure to avoid is two people delivering alternating monologues that do not answer each
other. A conversation teaches when one person says something and the other immediately does one
of these three things:

- says it back in their own words **with a fresh example**
- states **the implication**
- gives **a metaphor**

TOM should sound like understanding actually landing, not like a scripted setup. Vary who carries
the point. Sometimes TOM completes the idea and NOA confirms.

Label every line `NOA:` or `TOM:`. Plain text. No markdown, no stage directions, no emoji. Spell
out any unavoidable single number as a word.

---

## 6. Metaphors — read this twice, it is where these scripts will fail

**A metaphor is a claim about what the reader has already lived.** Before using one, ask whose
life it comes from. If it comes from a world you find apt rather than one she has actually been
in, it will be rejected, and it should be.

**The test: if a metaphor needs a glossary, it is not doing its job.**

**Metaphors already rejected. Do not reuse them or anything like them.**

| Rejected | Why |
|---|---|
| Buying a flat with a mortgage, "your equity is what is left" | Tried on 22 September and rejected. It asks her to accept the everyday word "equity" as if it explained the finance one. It does not. |
| Hiring a photographer | Too rare a situation to reason from |
| A hairdresser who does not ask how much time you spend on your hair | She wanted the work world |
| A saucier, a kitchen brigade | Real terms, not widely known |
| The squeaky wheel that stops squeaking before it falls off | The premise was not true to her |
| Someone found the felt-tips and a white wall | Not her English |

**Metaphors that worked, and that you should reuse.** These are hers or her lecturer's, and they
are the house style:

**The stacked buckets and the pool** — for the payoff waterfall, day 7. The lecturer's own image
in the class recording is two buckets and "some endless pool, which is called the bucket of the
stockholders". **Ifat corrected it, and her correction is the version you use:** the buckets are
not side by side, they are **stacked**. One tap. The senior bucket is on top. The junior bucket is
under it. The pool is under that. Water only reaches the junior bucket by overflowing the rim of
the senior one, and only reaches the pool by overflowing the junior one. **A bucket that is not
full passes nothing down.** That gate is the whole Absolute Priority Rule, and it is the thing the
side-by-side version failed to show. The pool can be empty but never negative, because a pool
holds no less than nothing.

**The bank balance and the withdrawal** — for equity against dividend. The balance is the value.
A withdrawal is the dividend. Withdrawing does not make you richer. Equity is a **size**, a
dividend is a **move**.

**Hiring a cook, with a nut allergy as the thing you must state** — hers, for briefing and
constraints. **The colleague who asks why are we doing this at all** — hers, for challenging a
premise. **The quiet child, because the noise is never what worries you** — hers, for a risk that
does not announce itself.

**When choosing, pick for the reader.** Ifat's own note on this: a large share of the audience are
women, and she wants metaphors a woman can actually relate to. Reach for ordinary life that most
adults have lived: a queue, a shared bill, a kettle, a shopping list, a landlord, a salary, a
group project. Not yachts, not poker, not American football.

---

## 7. Language

- Short sentences. Everyday words. If a word has a shorter everyday twin, use the twin.
- **Keep the subject's own vocabulary** — perpetuity, coupon, face value, senior debt, equity —
  and explain each one the first time it is spoken. Simplifying these away would leave a learner
  unable to read their own exam.
- Spoken English, not written English. Contractions are fine. This is the one place in the pack
  where the writing is allowed to be conversational, because that is why podcasts work.
- Do not simplify the thinking. Simple words, not simple ideas.

---

## 8. What each day gets

**One intro strip**, 45 to 70 seconds. The day's map and the key terms named. Nothing taught.

**One strip per substantial teaching panel**, 60 to 120 seconds each. Skip any panel that is a
heading plus one sentence; a player on a trivial block is noise.

Read your day's page and decide from the panels that are actually there. Most learn days will come
out at three or four strips including the intro.

---

## 9. What to return

```
DAY: NN
STRIPS: <file name, seconds, the one idea> for each
METAPHORS: <the everyday pictures you used, one line each, and whose world each comes from>
NUMBERS SPOKEN: <none, or which calculation and which on-screen table anchors it>
FLAGS: <anything you could not verify, anything the page left unclear, or "none">
```

Keep it under 250 words. Do not paste the scripts.
