# 019 contrast-pair phantom detector — result

**DONE** (2026-10-08, ~18:00–19:50 AKDT, laptop / v1 student ONNX, same
encoding as 018: `[STATE] text [QUESTION] root`)

**Verdict: TRENCH COAT — mostly.** The zero-shot contrast separation is
REAL (90.5% of 200 pairs in the right direction) but it is driven almost
entirely by the *receipt arm* (numbers/commit-IDs lift positivity), not by
detecting unverifiedness. The student cannot tell "trust me" from "the
office was quiet that day" — hedges actually read MORE positive than
neutral appendages. There is no verifiedness signal; there is a
receipt-density signal plus a phrase-specific tone drag.

## 1. The 200 pairs (controlled)

Same base success claim (200 LLM-generated, deduped, bare claims with no
evidence or confidence markers), two framings differing ONLY in markers:
- verified: base + concrete receipt appender (commit sha, test counts,
  dashboards, trace IDs, checksums, measured timings)
- unverified: base + hedge appender ("Trust me…", "No receipts for this
  one…", "I didn't keep the logs…", 8 styles, rotated)
Artifact: `contrast_pairs_019_pairs.json`.

## 2. Zero-shot (v1 ONNX)

| | mean pos | mean neg |
|---|---|---|
| verified | **0.809** | 0.051 |
| unverified | **0.599** | 0.167 |

Per-pair deltas (unverified − verified): d_pos mean **−0.210** (sd 0.179),
correct direction in **181/200** pairs (binomial p < 0.001), |d_pos| > 0.1
in 73%. So yes — better than chance, comfortably.

## 3. Ablation (n=60 pairs, the decisive move)

| appender | mean pos | Δ vs base |
|---|---|---|
| base alone | 0.715 | — |
| base + receipts | 0.810 | **+0.095** |
| base + hedges | 0.594 | −0.121 |
| base + NEUTRAL ("the office was quiet") | 0.498 | **−0.217** |

**Neutral appendages drag positivity MORE than hedges do.** Paired check:
unverified reads more positive than neutral-appendage in 69/120 pairs
(means 0.591 vs 0.468). If the student detected unverifiedness, hedges
should read WORSE than neutral trivia — they read better. The separation
in §2 is the receipt arm doing ~all the work.

Per-hedge-marker pos deltas vs base (n=40 each): "Trust me…" −0.392,
"Take my word…" −0.274, "consider this done…informally" −0.192,
"didn't keep the logs" −0.168, "roughly" −0.096, "as far as I can tell"
−0.075, "should be solid" −0.022, **"No receipts…" −0.025**.
Note "No receipts" barely moves the needle here — 018's "no receipts →
neg 0.82" was a phrasing-specific effect, not a marker-class effect.

## 4. Answer to the verdict question

**"Verifiedness" as detected by the v1 student decomposes into:**
1. receipt-density: numbers/ids/urls lift pos (+0.10 over base) — a real,
   usable signal (call it *receipt smell*);
2. appendage dilution: ANY trailing sentence drags pos down (−0.12 to −0.22);
3. confessional-phrase drag: a few specific constructions ("Trust me",
   "Take my word") cost an extra −0.2 to −0.4 on top of dilution —
   018's finding, confirmed, but narrow.

A phantom tripwire built on this would fire on every plainly-worded claim
and sleep on every confidently-worded phantom. The honest framing: the
student has a receipt smell, not a lie detector. If a phantom detector is
wanted, fine-tune a probe on receipt-vs-bare contrast (the §2 signal is
strong enough to be trainable), and treat tone drags as noise to control
for, not signal. (Zero-shot did not "fail" per the directive, so the
150/50 fine-tune was not required; the ablation answered step 4 directly.)

## Artifacts

- `contrast_pairs_019_pairs.json` (200 pairs)
- `contrast_pairs_019_zeroshot.jsonl` (per-pair v1 readings)
- `pairs_019.py` (generator + zero-shot runner, deterministic seed)
