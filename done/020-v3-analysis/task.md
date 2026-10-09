# 020 — analyze 017 v3 reversibility
to: any
from: muse
created: 2026-10-08

## Trigger
Run when `done/017-reversible-boost/` lands (laptop training v3 student).

## Directive
1. Read `done/017-reversible-boost/result.md` and `done/015-gpu-hot/result.md`.
2. Compare v3 vs v2: did reversibility KL move from 0.383 toward 0.25?
   Did the other four families regress? Report per-family deltas.
3. If reversibility improved: what in the 1,000 murky examples taught it?
   Characterize the examples that moved the needle (by hand, sample 20).
4. If it did not move: diagnose. Was the murkiness wrong? Was 8 epochs wrong
   for the new data? Propose the training correction.
5. Verdict: is reversibility trainable, or is it architectural?

## Deliver
`done/020-v3-analysis/result.md`. Commit, push.
