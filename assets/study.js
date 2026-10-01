/* Principles of Finance — 15 day study pack
   Shared engine: quizzes, timed mocks, and the browser-stored error log.
   No external libraries. Everything runs offline once the files are served.

   Two entry points:
     POF.quiz({mount, day, topic, items})                  learn-day quiz, answer shown on pick
     POF.mock({mount, day, topic, items, minutes, total})   timed mock, nothing revealed until submit

   An item looks like:
     { q:"stem", opts:["a","b","c","d"], correct:0, exp:"worked explanation", tag:"Annuity", src:"optional" }
   `correct` is the index into `opts` as written. Options are shuffled at render time and the
   right answer is tracked by identity, so the key can never drift out of step with the display.
*/
(function (global) {
  'use strict';

  var LOG_KEY = 'pof.errorlog.v1';

  /* ------------------------------------------------------------------
     VISITOR COUNTING (GoatCounter)

     PUT YOUR CODE ON THE NEXT LINE. It is the part before .goatcounter.com
     in your own address. If yours is  ifat-finance.goatcounter.com  then the
     line reads  var GOATCOUNTER_CODE = 'ifat-finance';
     Leave it as it is and nothing is loaded and nothing is counted.

     This one line covers the whole site, because every page loads this file.
     GoatCounter sets no cookies and stores no personal data, so there is
     nothing to warn your classmates about.
  ------------------------------------------------------------------ */

  var GOATCOUNTER_CODE = 'ifat-finance';

  var pendingCounts = [];

  function startCounting() {
    if (!GOATCOUNTER_CODE) return;
    try {
      var s = document.createElement('script');
      s.async = true;
      s.setAttribute('data-goatcounter',
        'https://' + GOATCOUNTER_CODE + '.goatcounter.com/count');
      s.src = 'https://gc.zgo.at/count.js';
      s.addEventListener('load', drainCounts);
      document.head.appendChild(s);
    } catch (e) { /* counting must never break a study page */ }
  }

  function drainCounts() {
    while (pendingCounts.length) {
      var q = pendingCounts.shift();
      try { global.goatcounter.count(q); } catch (e) { /* ignore */ }
    }
  }

  /* Record one thing a learner did. Safe before the script has loaded, and
     safe if it never loads at all. */
  function countEvent(path, title) {
    if (!GOATCOUNTER_CODE) return;
    var q = { path: path, title: title || path, event: true };
    if (global.goatcounter && global.goatcounter.count) {
      try { global.goatcounter.count(q); } catch (e) { /* ignore */ }
    } else {
      pendingCounts.push(q);
    }
  }

  /* Count the first play of each audio strip, once per page view. Pressing
     pause and play again, or dragging the slider, does not count twice. */
  function wireAudioCounting() {
    var players = document.querySelectorAll('audio');
    for (var i = 0; i < players.length; i++) {
      (function (el, n) {
        var counted = false;
        el.addEventListener('play', function () {
          if (counted) return;
          counted = true;
          var src = el.getAttribute('src') || '';
          var name = src.split('/').pop().replace(/\.mp3$/i, '') || ('strip-' + n);
          countEvent('audio-play/' + name, 'Played: ' + name);
        });
      })(players[i], i + 1);
    }
  }

  /* ---------- storage: never let a blocked or full localStorage break the page ---------- */

  function readLog() {
    try {
      var raw = global.localStorage.getItem(LOG_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) { return []; }
  }

  function writeLog(rows) {
    try { global.localStorage.setItem(LOG_KEY, JSON.stringify(rows)); return true; }
    catch (e) { return false; }
  }

  /* keep a stem readable in the prompt: cut at a word, not mid-word */
  function trimStem(s, max) {
    s = s || '';
    if (s.length <= max) return s;
    var cut = s.slice(0, max);
    var space = cut.lastIndexOf(' ');
    if (space > max * 0.6) cut = cut.slice(0, space);
    return cut + '...';
  }

  function addMiss(entry) {
    var rows = readLog();
    rows.push({
      d: entry.day, t: entry.topic, tag: entry.tag || entry.topic,
      q: trimStem(entry.q, 160),
      chose: entry.chose, right: entry.right,
      ts: new Date().toISOString().slice(0, 10)
    });
    if (rows.length > 400) rows = rows.slice(rows.length - 400);
    writeLog(rows);
  }

  function clearLog() { try { global.localStorage.removeItem(LOG_KEY); } catch (e) {} }

  /* ---------- the prompt: what the learner pastes into Claude ---------- */

  function buildPrompt() {
    var rows = readLog();
    if (!rows.length) {
      return 'No misses saved yet on this browser. Do a quiz or a mock first, then come back.';
    }
    var byTag = {};
    rows.forEach(function (r) {
      var k = r.tag || r.t || 'Unsorted';
      if (!byTag[k]) byTag[k] = [];
      byTag[k].push(r);
    });
    var tags = Object.keys(byTag).sort(function (a, b) { return byTag[b].length - byTag[a].length; });

    var out = [];
    out.push('I am studying for an MBA Principles of Finance final exam.');
    out.push('The exam is 22 multiple-choice questions in 2.5 hours. A formula sheet is given. Only a scientific calculator is allowed.');
    out.push('');
    out.push('These are the questions I got wrong while revising, grouped by topic, most misses first:');
    out.push('');
    tags.forEach(function (tag) {
      out.push(tag + ' — ' + byTag[tag].length + ' missed');
      byTag[tag].slice(-6).forEach(function (r) {
        out.push('  - (day ' + r.d + ') ' + r.q);
        out.push('    I answered: ' + r.chose + '  |  correct: ' + r.right);
      });
      out.push('');
    });
    out.push('Please do three things:');
    out.push('1. Tell me which single idea most of these misses share.');
    out.push('2. Explain that idea in plain words, with one everyday comparison.');
    out.push('3. Then drill me: give me one question at a time, wait for my answer, and tell me if I am right before the next one. Do not solve anything I have not attempted.');
    return out.join('\n');
  }

  /* ---------- small DOM helpers ---------- */

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function shuffled(item) {
    var pairs = item.opts.map(function (text, i) { return { text: text, right: i === item.correct }; });
    for (var i = pairs.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = pairs[i]; pairs[i] = pairs[j]; pairs[j] = t;
    }
    return pairs;
  }

  function letters(i) { return 'ABCDEFGH'.charAt(i); }

  /* ---------- learn-day quiz: reveal as soon as the learner picks ---------- */

  function quiz(cfg) {
    var mount = document.getElementById(cfg.mount);
    if (!mount) return;
    var items = cfg.items || [];
    var answered = 0, right = 0;

    var chip = el('span', 'scorechip', '0 / ' + items.length);
    var head = document.querySelector('[data-scorechip="' + cfg.mount + '"]');
    if (head) head.appendChild(chip);

    items.forEach(function (item, qi) {
      var block = el('div', 'qblock');
      var num = el('div', 'qnum', 'Question ' + (qi + 1));
      if (item.src) {
        var tg = el('span', 'examtag', item.src);
        num.appendChild(tg);
      }
      block.appendChild(num);
      block.appendChild(el('div', 'qtext', item.q));

      var exp = el('div', 'exp');
      exp.innerHTML = '<b>Why</b><br>' + item.exp;

      var pairs = shuffled(item);
      var done = false;
      var btns = [];

      pairs.forEach(function (p, oi) {
        var b = el('button', 'opt');
        b.type = 'button';
        b.textContent = letters(oi) + '.  ' + p.text;
        b.addEventListener('click', function () {
          if (done) return;
          done = true;
          answered++;
          btns.forEach(function (other, k) {
            other.disabled = true;
            if (pairs[k].right) {
              other.classList.add('correct');
              var m = el('span', 'mark', '✓');
              other.appendChild(m);
            }
          });
          if (p.right) {
            right++;
          } else {
            b.classList.add('wrong');
            var x = el('span', 'mark', '✗');
            b.appendChild(x);
            addMiss({
              day: cfg.day, topic: cfg.topic, tag: item.tag || cfg.topic,
              q: item.q, chose: p.text,
              right: pairs.filter(function (z) { return z.right; })[0].text
            });
          }
          exp.classList.add('show');
          chip.textContent = right + ' / ' + items.length;
        });
        btns.push(b);
        block.appendChild(b);
      });

      block.appendChild(exp);
      mount.appendChild(block);
    });
  }

  /* ---------- timed mock: nothing revealed until submit or time-up ---------- */

  function mock(cfg) {
    var mount = document.getElementById(cfg.mount);
    if (!mount) return;
    var items = cfg.items || [];
    var minutes = cfg.minutes || 150;
    var picks = new Array(items.length).fill(null);
    var rendered = [];
    var finished = false;

    /* timer */
    var bar = el('div', 'timer');
    var clock = el('span', null, fmt(minutes * 60));
    var startBtn = el('button', null, 'Start');
    bar.appendChild(el('span', null, 'Time left'));
    bar.appendChild(clock);
    bar.appendChild(startBtn);
    mount.appendChild(bar);

    var left = minutes * 60, tick = null;
    function fmt(s) {
      var m = Math.floor(s / 60), r = s % 60;
      return (m < 10 ? '0' : '') + m + ':' + (r < 10 ? '0' : '') + r;
    }
    startBtn.addEventListener('click', function () {
      if (tick) return;
      startBtn.disabled = true;
      startBtn.textContent = 'Running';
      tick = setInterval(function () {
        left--;
        clock.textContent = fmt(left);
        if (left <= 0) { clearInterval(tick); finish(true); }
      }, 1000);
    });

    /* questions - clicking marks the choice only, no feedback */
    items.forEach(function (item, qi) {
      var block = el('div', 'qblock');
      var num = el('div', 'qnum', 'Question ' + (qi + 1));
      if (item.src) num.appendChild(el('span', 'examtag', item.src));
      block.appendChild(num);
      block.appendChild(el('div', 'qtext', item.q));

      var pairs = shuffled(item);
      var btns = [];
      pairs.forEach(function (p, oi) {
        var b = el('button', 'opt');
        b.type = 'button';
        b.textContent = letters(oi) + '.  ' + p.text;
        b.addEventListener('click', function () {
          if (finished) return;
          btns.forEach(function (o) { o.style.borderColor = ''; o.style.background = ''; });
          b.style.borderColor = 'var(--brand)';
          b.style.background = 'var(--brand-soft)';
          picks[qi] = { text: p.text, right: p.right };
        });
        btns.push(b);
        block.appendChild(b);
      });

      var exp = el('div', 'exp');
      exp.innerHTML = '<b>Why</b><br>' + item.exp;
      block.appendChild(exp);
      mount.appendChild(block);
      rendered.push({ btns: btns, pairs: pairs, exp: exp, item: item });
    });

    var submit = el('button', 'reveal-btn');
    submit.textContent = 'Submit paper';
    submit.style.marginTop = '18px';
    submit.addEventListener('click', function () { finish(false); });
    mount.appendChild(submit);

    var results = el('div', 'panel');
    results.style.display = 'none';
    mount.appendChild(results);

    function finish(auto) {
      if (finished) return;
      finished = true;
      if (tick) clearInterval(tick);
      startBtn.disabled = true;
      submit.disabled = true;
      submit.textContent = 'Submitted';

      var score = 0, missed = [];
      rendered.forEach(function (r, qi) {
        r.btns.forEach(function (b, k) {
          b.disabled = true;
          if (r.pairs[k].right) { b.classList.add('correct'); b.appendChild(el('span', 'mark', '✓')); }
        });
        var p = picks[qi];
        if (p && p.right) {
          score++;
        } else {
          missed.push(qi + 1);
          if (p) {
            r.btns.forEach(function (b, k) {
              if (r.pairs[k].text === p.text) { b.classList.add('wrong'); b.appendChild(el('span', 'mark', '✗')); }
            });
          }
          addMiss({
            day: cfg.day, topic: cfg.topic, tag: r.item.tag || cfg.topic,
            q: r.item.q, chose: p ? p.text : 'left blank',
            right: r.pairs.filter(function (z) { return z.right; })[0].text
          });
        }
        r.exp.classList.add('show');
      });

      var pct = Math.round((score / items.length) * 100);
      results.innerHTML = '';
      results.style.display = 'block';
      results.appendChild(el('h3', null, auto ? 'Time up' : 'Paper submitted'));
      var line = el('p', 'p');
      line.innerHTML = '<b>' + score + ' out of ' + items.length + '</b> &nbsp;(' + pct + '%)';
      results.appendChild(line);
      results.appendChild(el('p', 'note',
        missed.length ? 'Missed: question ' + missed.join(', ') : 'Nothing missed.'));
      results.appendChild(el('p', 'note',
        'No pass mark is published for this course, so none is shown here. Use the misses, not the percent.'));
      results.appendChild(errorLogBox());
      results.scrollIntoView({ behavior: 'smooth' });
    }
  }

  /* ---------- the error log box: shown on mocks, the sweep day, and the hub ---------- */

  function errorLogBox() {
    var box = el('div', 'takeaway');
    var rows = readLog();

    var title = el('div', null, '');
    title.innerHTML = '<b>Your error log</b> — saved in this browser only.';
    box.appendChild(title);

    var counts = {};
    rows.forEach(function (r) { var k = r.tag || r.t; counts[k] = (counts[k] || 0) + 1; });
    var keys = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; });

    if (!keys.length) {
      box.appendChild(el('p', 'note', 'Nothing in it yet. Every question you get wrong lands here automatically.'));
    } else {
      var ul = el('ul');
      keys.forEach(function (k) { ul.appendChild(el('li', null, k + ' — ' + counts[k] + ' missed')); });
      box.appendChild(ul);
    }

    var btn = el('button', 'reveal-btn');
    btn.type = 'button';
    btn.textContent = 'Make a prompt for Claude';
    btn.style.marginTop = '10px';

    var area = document.createElement('textarea');
    area.readOnly = true;
    area.rows = 12;
    area.style.cssText = 'display:none;width:100%;margin-top:10px;font-size:13px;padding:10px;border-radius:9px;border:1px solid var(--line);font-family:inherit;';

    var copy = el('button', 'navbtn');
    copy.type = 'button';
    copy.textContent = 'Copy';
    copy.style.cssText = 'display:none;margin-top:8px;cursor:pointer;';

    var wipe = el('button', 'navbtn');
    wipe.type = 'button';
    wipe.textContent = 'Clear the log';
    wipe.style.cssText = 'margin-top:8px;margin-left:8px;cursor:pointer;';

    btn.addEventListener('click', function () {
      area.value = buildPrompt();
      area.style.display = 'block';
      copy.style.display = 'inline-block';
      area.focus();
      area.select();
    });
    copy.addEventListener('click', function () {
      area.select();
      try { document.execCommand('copy'); copy.textContent = 'Copied'; }
      catch (e) { copy.textContent = 'Select the text and copy it'; }
      setTimeout(function () { copy.textContent = 'Copy'; }, 2500);
    });
    wipe.addEventListener('click', function () {
      if (global.confirm('Clear every saved miss? This cannot be undone.')) {
        clearLog();
        box.replaceWith(errorLogBox());
      }
    });

    box.appendChild(btn);
    box.appendChild(wipe);
    box.appendChild(area);
    box.appendChild(copy);
    return box;
  }

  function mountErrorLog(id) {
    var host = document.getElementById(id);
    if (host) host.appendChild(errorLogBox());
  }

  /* ---------- try-it reveal buttons ---------- */

  function wireReveals() {
    document.querySelectorAll('[data-reveal]').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = document.getElementById(b.getAttribute('data-reveal'));
        if (!t) return;
        t.classList.toggle('show');
        b.textContent = t.classList.contains('show') ? 'Hide the answer' : 'Show the answer';
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    wireReveals();
    wireAudioCounting();
  });

  startCounting();

  global.POF = {
    quiz: quiz,
    mock: mock,
    mountErrorLog: mountErrorLog,
    buildPrompt: buildPrompt,
    readLog: readLog,
    clearLog: clearLog,
    countEvent: countEvent
  };
})(window);
