# 020 v3-analysis — result

**DONE** (2026-10-08, laptop — second read of 017's own output, data grounded)

## 2. Did it move? (per-family, honest fair-split from 017)

| family | v2 | v3 | Δ |
|---|---|---|---|
| reversible | 0.610 | 0.379 | **−38%** |
| coherence | 0.172 | 0.181 | flat |
| go-no-go | 0.553 | 0.498 | flat |
| load-bearing | 0.068 | 0.068 | flat |
| risk | 0.160 | 0.190 | flat (n=7) |

Reversibility moved from 0.61 (fair) toward — not to — 0.25. 017's naive
0.383→0.25 target conflated v2's contaminated-split number (0.38) with its
true unseen-data number (0.61); against the true baseline, −38% is a big
move. **No family regressed** beyond noise.

## 3. What in the 1,000 taught it (20-row hand read + band table)

Per-band KL on all reversible test rows: murky 0.344→0.301, clear_no
0.661→0.520, clear_yes 0.575→0.376. The **most-improved rows are
clear-cut cases v2 got catastrophically wrong** (KL 2–4 on physical
irreversibility: "burn the vintage log books", "hazardous waste byproduct";
and trivial fixes: "extra minute of recess", "temporarily disable the dust
cover" → KL ~0.00–0.6). Read: the new data first taught the **schema** —
what the three reversibility categories actually look like in the wild —
which v2 (521 examples) had only half-formed. The murk itself improved
modestly.

Characterization of the new corpus (graded_v3, n=1,018):
- argmax mix: 151 irreversible / 338 partly / 529 easily — the murk
  flavor arrived as a **partly-reversible mass** (33% vs old 46%), i.e.
  the "technically undoable but costly/awkward/traced" middle the flavors
  targeted ("undo window closing", "soft commitments", "partial undo").
- entropy: 28% H>1.0 vs old 43% — the new items are *borderline by
  content, not by teacher uncertainty*. That's why murky-KL improved
  less than schema-KL: the teacher's soft shape on these is confident
  (mean H 0.71), so there's less distribution-shape to match.
- hygiene note: ~2% generator leaks ("N. " prefix artifacts, one Chinese
  mixed-language item) — harmless at this rate, worth a parse fix in v4
  tooling.

## 4/5. Verdict: trainable, data-limited — not architectural

Reversibility is **trainable by the same medicine as coherence**: doubling+
the family moved it 38% with zero collateral, same architecture, same 8-epoch
knee. Remaining gap (0.38 vs ~0.1 for the strong families) has a visible
cause: the murk taught so far is *content-murky but teacher-confident*.
The next 1k should target **teacher-uncertain murk** (H>1.0 items — old
corpus had 43%, new has 28%): undo-cost tradeoffs where the teacher itself
spreads, window-closing changes, reversibility-asymmetries between parties.
Corrections for the next round: (a) generate adversarially toward high-H,
filter/keep only items the teacher grades murky in *distribution*, not just
band-intent; (b) fix the "N. " parse leak; (c) consider 6 epochs — v3's
softKL trough was ep5–7, and the corpus is +17% bigger.

If one more data round lands ~0.25, the family joins the strong tier and
the student is done pending risk (509) and the go-no-go teacher ceiling
(0.50 unseen — third confirmation that it's the CRITERIA, not the student).
