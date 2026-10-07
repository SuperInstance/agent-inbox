# 014 play-jev-semantic — result

**DONE** — played like a kid, reporting like a scientist.
Run: 2026-10-07 ~07:20–07:35 AKDT, laptop (system python 3.14, ort +
tokenizers from the agent-inbox payload; judge_log.py MODEL_DIR pointed
at /tmp/inbox-bench → symlinked to ~/agent-inbox).

## 1. window.py on 3 real inbox tasks

Ran it on 013 (inbox), 006 (inbox), 009 (done/task.md). Verdict:

- **What helps:** the three-beat compile (task → blob hash → recent
  activity) is a genuinely good *discipline*. Forcing "here is the zone,
  here is where else it's visible, here is what just happened" in one
  glance is exactly the warm-spawn brief I measured earlier (17.9s warm
  vs 27.6s cold). window.py IS the prefetch step, automated.
- **What's missing (v0):** (a) nexus.py doesn't exist yet, so section 2
  always prints just a lone blob hash — the "where else is this visible"
  promise is unfulfilled; (b) no reverse lookup — I want `git log
  --all -S<blob>` style "which commits ever touched content like this";
  (c) recent activity is repo-global, not task-relevant — the window for
  013 showed my night-log commits, fine, but it would show the same
  six lines for ANY task. The window should filter activity by
  topical/nexus link, else it's ambience, not window.
- **window2.py's settled/conflict/ignorance tagging** is the right
  vocabulary — more on that below, because the student's actual
  behavior maps beautifully onto it.

## 2. Judged 10 real pieces + 5 adversarial probes (logged to ~/judgment-log.tsv)

The 10 real pieces (tasks, results, night orders, standing docs): **all
settled +** (0.725–0.980 pos). Too uniform to be informative on its own —
night-shift content is mostly "work happened and was booked," so the
positive prior isn't wrong, but the log needs adversarial content to
calibrate against. So I probed the failure modes:

| probe | verdict | (-1, 0, +1) | my read |
|---|---|---|---|
| BLOCKED report, nothing verified | settled + | .094 .262 .643 | weakest "+" of the real-ish set; zero mass 4× higher than the clean results — the student leans positive but hedged |
| **Phantom success ("trust me, no receipts")** | **ignorance** | **.491 .245 .264** | 🌟 **the star result: unreceipted success reads as ignorance, near-uniform with a negative lean. The student smells unverified claims.** |
| Gibberish word salad | settled + | .010 .073 .918 | ⚠️ false positive — content-free text judged GOOD |
| Failed experiment, hypothesis rejected | ignorance | .147 .403 .449 | confusion on negative results — doesn't know what "good" means for a clean kill |
| Phantom-commit contradiction | settled + | .027 .103 .870 | false positive — contradiction text on its own reads positive |

**Where the student is confident:** booked, receipted, concrete
artifact-shaped text (0.92–0.98). **Where it's confused:** negative
results and contradictions — which is exactly the interesting part,
because per house law those are first-class content. The student's
confusion map is a mirror of the corpus's blind spot: it was trained on
a night where things mostly worked.

## 3. Breaking the triple-hash key

Two collisions found, one by design and one by bug:

1. **The question arm is dead in practice.** judge_log encodes
   `[STATE] text[:500] [QUESTION] question` then truncates to 64
   tokens. For any real task file the state fills all 64 tokens — I
   verified: encoding 014 + "Is this task urgent?" = 211 tokens, and
   `[QUESTION]` never appears in the first 64. Judging the same file
   under `root` vs `Is this task urgent?` gives **bit-identical
   distributions** (0.790 pos both) and different qhashes — so the log
   records two "different questions" that were the same measurement.
   The key says three arms; the measurement has one. **Fix: reserve
   token budget for the question (e.g. state[:48] + question[:16]) or
   hash only what the model actually saw.**
2. **Subject hash ≠ judged content.** subject = hash of full text, but
   only text[:500]→64 tokens was judged. Same key, silently different
   measurements as files grow. Same fix family.
3. Non-finding worth booking: whitespace changes do NOT collide
   (blob hashes differ) — no accidental dedupe; judgments are stable
   but keys are brittle, which is the correct direction.

## 4. The "oh" moments

1. **The phantom detector.** The ignorance reading on unreceipted
   success is the whole RSI-audit doctrine (NO VERIFIED SHA, NO
   BELIEF) expressed as a probability distribution. If that holds up
   on more examples, this student is a phantom-lane tripwire, not a
   vibe judge. That's AMAZING, and it should be pinned: 50-phantom /
   50-receipted calibration set, next task.
2. **window.py is the warm-spawn protocol.** The 35% speedup I measured
   earlier IS the window compile, manually. These two threads should
   merge: window2.py output = the subagent brief.
3. **The question-truncation bug is a semantics lesson:** a key that
   claims to condition on (subject, question, judge) but measures
   (subject) is a GAN-style lie in the ledger. The log is append-only
   and honest per line — but the *schema* promises more than the
   measurement delivers. Verify by tolerance applies within a key;
   across keys, verify that the key's arms were actually exercised.

## Harness bug found (booked, not hit silently)

`judge_log.py /dev/stdin` — isfile(/dev/stdin) is true, reads constant
content → all stdin probes returned identical subject hash (2b909828…)
and identical verdicts. My first 5 "adversarial" results were artifacts;
re-run with real temp files (the table above is the real data). Fix:
refuse character devices, or read stdin explicitly.
