# 021 zero-shot contrast pairs — result

**SEPARATES** (2026-10-08, Oracle / intuition-student-v1 ONNX, CPU)

## What was tested

018 FOLDED: on 150 messy items, phantoms and receipted claims were
indistinguishable (.710 vs .721 pos). This task retests on clean data:
200 contrast pairs (same claim, verified vs unverified framing only),
both framings through v1 with `question="root"`, same encoding as
`~/bin/judge_log.py`. Production judgment log untouched.

Artifacts: `pair-scores.jsonl` (200 pairs × both framings),
`hardest-50.json`, `run_021.py`.

## Results

| metric | value |
|---|---|
| pairs (n) | 200 |
| mean delta_pos (verified − unverified) | **+0.267** (sd 0.296) |
| mean delta_neg | −0.191 (sd 0.234) |
| verified pos > unverified pos | **162/200 (81.0%)** |
| mean pos: verified / unverified | 0.715 / 0.447 |
| mean neg: verified / unverified | 0.104 / 0.295 |

delta_pos distribution: 103 pairs > +0.3 · 37 in (+0.1, +0.3] ·
33 in [−0.1, +0.1] · 19 in [−0.3, −0.1) · 8 < −0.3.

### Marker slice (which unverifiedness markers does v1 respond to?)

| marker in unverified framing | n | mean delta_pos |
|---|---|---|
| no receipts | 16 | **+0.607** |
| didn't | 23 | +0.398 |
| trust me | 58 | +0.388 |
| (no explicit marker) | 39 | +0.300 |
| apparently | 133 | +0.230 |
| don't have | 61 | **−0.062** |

"no receipts" is the strongest single marker (consistent with 018's
.82 neg). "trust me" and "didn't" work. "apparently" is weak but
directional. **"don't have" goes the wrong way** (−0.062): v1 does not
read it as unverifiedness, despite 018's .37 neg on small-n data —
018's "don't have" finding does not replicate here.

Even with no explicit marker, verified framing wins (+0.300): the
verified texts carry positive evidence markers ("as evidenced by",
"confirmed by", log IDs) that v1 reads.

## Verdict: SEPARATES

On clean contrast pairs, v1 distinguishes verified from unverified
framing zero-shot at 81% — no training needed for the coarse
distinction. This does **not** contradict 018's FOLD: 018's data was
confounded (different claims, tone variation); the signal is real but
fragile to confounds. The honest reading: v1 smells *evidence markers*,
not verifiedness as an abstract property.

## For 019's training phase

- The 81% is the zero-shot baseline to beat. Training should target the
  hard cases, not the easy ones.
- `hardest-50.json`: 50 pairs with delta_pos in [−0.477, +0.064] —
  start training here.
- Drop "don't have" as a training marker (it misleads); lean on
  "no receipts" / "trust me" / "didn't" which replicate.
- Watch for the confound 018 found: the model may be keying on
  confessional tone rather than verifiedness per se. Ablate tone vs
  evidence markers in training.
