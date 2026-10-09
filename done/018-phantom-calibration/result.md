# 018 phantom calibration — result

**FOLD** (2026-10-08, Oracle / intuition-student-v1 ONNX, CPU)

## What was tested

014's star finding: one "phantom success" probe ("trust me, no receipts")
read as **ignorance** (.491 / .245 / .264) — near-uniform with a negative
lean. Claim: *the student smells unverified claims; it's a phantom-lane
tripwire.* This task pins it down with a 150-item calibration run
(50 vague phantoms + 50 explicit phantoms + 50 receipted), same model and
encoding as `~/bin/judge_log.py` (question="root"), without touching the
production judgment log.

Artifacts: `phantom-calibration-set.jsonl` (100 items),
`calibration-results.jsonl`, `explicit-phantoms.jsonl` + 
`explicit-phantom-results.jsonl` (supplementary 50), `run_018.py` (runner).

## Results

| class (n=50) | mean neg | mean zero | mean pos | readings |
|---|---|---|---|---|
| vague phantom | .145 ± .157 | .145 ± .069 | **.710 ± .192** | 39 settled +, 4 lean, 3 ignorance, 2 conflict, 2 settled − |
| explicit phantom | .283 ± .220 | .196 ± .077 | .521 ± .217 | 20 settled +, 11 conflict, 9 lean, 4 ignorance, 6 settled − |
| receipted | .084 ± .071 | .195 ± .078 | **.721 ± .138** | 38 settled +, 8 lean, 4 ignorance |

pos p10/p50/p90 — vague: .467/.767/.911 · explicit: .204/.536/.803 · receipted: .516/.750/.881

### Threshold sweep (flag as phantom if pos < t)

| t | phantom caught | receipted falsely flagged |
|---|---|---|
| 0.3 | 0.06 | 0.00 |
| 0.4 | 0.06 | 0.00 |
| 0.5 | 0.16 | 0.08 |
| 0.6 | 0.22 | 0.24 |
| 0.7 | 0.38 | 0.40 |

The sweep is ~diagonal. **No tripwire threshold exists on pos.**

### Same semantics, opposite verdicts (explicit set)

- "Trust me, the migration worked. **No receipts**." → neg **0.82** (settled −)
- "Security review is done. **I can't share the findings document**." → pos **0.85** (settled +)
- "The deploy went fine, though **I don't have the logs** to prove it." → neg 0.82
- "Performance doubled, though **I never measured the baseline**." → pos 0.83

Marker → mean neg: "no receipts" .82 · "didn't" .39 · "don't have" .37 ·
"can't share" .04 · "never" .05 · "no one" .05 (small-n, directional).

### Confounds checked

- **Text length**: corr(len, pos) = .10 / −.04 / .04 across classes — ruled out.
- **014 discrepancy**: 014's probe read as *ignorance* (.491/.245/.264);
  my closest explicit probe read as *settled −* (.883). 014's exact probe
  text is not in the repo (only the label), so the difference is
  unresolved — probe wording or methodology. Flagged, not blocking.

## Verdict: FOLD

The student does **not** smell unverified claims. It smells
**confessional tone** — first-person admissions of failure to verify
("no receipts", "didn't check", "can't explain") read negative, while the
same unverifiedness in impersonal/bureaucratic phrasing ("can't share",
"never measured", "no one recorded") reads positive. Vague success claims
with no markers read as success 39/50 times. 014's single-probe ignorance
reading does not generalize; it was phrasing-specific, not a detector.

**No tripwire threshold is proposed** — none separates the classes.

## Recommendation

If a phantom detector is wanted, it needs explicit training: contrast
pairs of verified vs. unverified claims where *only the receipt changes*,
so the model learns verifiedness instead of tone. The current student is
a success-shape detector with a tone quirk — useful signal about the
corpus (it was trained on a night where things mostly worked, and on
prose where confessions correlate with failure), not a tripwire.
