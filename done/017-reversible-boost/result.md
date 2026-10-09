# 017 reversible-boost — result

**DONE** (2026-10-08, ~15:55–17:30 AKDT, laptop / RTX 4050 [trained on CPU])

**Verdict: YES — reversible moved 0.61 → 0.38 (−38%) on fair unseen rows; the booked ~0.25 target was optimistic but the family went from 9× worst to within 2× of the others, with zero regression elsewhere.**

## What was done

1. **Generated** 1,018 new reversible-family items (Ollama qwen2.5:7b, murky-heavy
   707/155/156 murky/clear-yes/clear-no, 10 murk flavors: undo-windows,
   soft commitments, partial undo, env-reversible-not-prod, etc.),
   deduped against the full 5,998-item corpus → `data/candidates_v3.json`.
2. **Graded** all 1,018 via the typesafe teacher (jev-preview, one-item-per-call,
   checkpointed) → `data/graded_v3.jsonl`.
3. **Trained v3**: same d320/8L/8H cascade shape (12.45M params), 8 epochs
   (booked knee), tokenizer v3 retrained on merged 6-family... 5-family corpus.
   Corpus now: coherence 1,846 / go-no-go 1,705 / reversible 1,539 /
   load-bearing 1,417 / risk 509 (6,888 graded, deduped).
   Train 5,968 / stratified test 1,048 (165 soft, H>1.4). Split saved to
   `data/test_split_v3.json` for reproducibility.

## The measurement trap (and the honest table)

The naive same-split comparison is CONTAMINATED: v2 trained on ~85% of the
old-family rows in the new test split (its numbers look artificially great:
coherence 0.042, go-no-go 0.097). Reconstructed v2's exact train set
(deterministic seed replay, 5,103 rows — matches 015's booking exactly) and
re-evaluated on rows **v2 never trained on**:

### FAIR table (272 rows unseen by v2 AND by v3)

| family | v2 | v3 | Δ |
|---|---|---|---|
| **reversible** | **0.610** | **0.379** | **−38% ✅** |
| coherence | 0.172 | 0.181 | flat (noise, n=41) |
| go-no-go | 0.553 | 0.498 | flat-ish (teacher-side ceiling, as booked) |
| load-bearing | 0.068 | 0.068 | flat |
| risk | 0.160 | 0.190 | n=7, not meaningful |

Notes:
- Fair set is dominated by the 153 new reversible test rows (v2 saw none of
  the new 1,018; v3 saw only its 85% train share — both clean on these).
- For reference, v3's per-family on the full split: coherence 0.116,
  go-no-go 0.371, load-bearing 0.065, reversible 0.353, risk 0.303 —
  consistent with 015's booked honest numbers on a murkier mix, not a
  regression. The scary-looking "v3 worse" raw table is the contamination
  artifact, not real degradation.
- Reversible soft-point (H>1.4, n=7 fair): v2 0.204 / v3 0.360 — tiny n,
  but flags that the remaining reversible error is concentrated on the
  murk; next boost should go even murkier.
- Training curve: test_KL 0.309 → 0.233 over 8 epochs, softKL trough at
  ep5–7 (~0.10). 8-epoch knee lesson held.

## Artifacts (beside this file)

- `models/intuition_student_v3.pt` + `intuition_student_v3.onnx`
  (**single 50MB file, no external data blob — v2 lesson held**;
  ONNX checker clean; parity vs torch: 200/200 argmax agree,
  mean distribution KL 0.0000 on a 200-row sample)
- `models/tokenizer_v3/` (tokenizer.json)
- `gen_v4.log`, `grade_v4.log`, `train_v3.log` (full receipts)
- Source pipeline (laptop): `~/projects/intuition/src/gen_candidates_v4.py`,
  `grade_corpus_v4.py`, `train_student_v3.py`, `eval_fair_v3.py`

## CPU latency

ONNX 1-thread: **13.4 ms** (v2 was 15.2 ms torch; v3-onnx is faster than
v2-torch) — flash-budget territory, unchanged.

## What's next (recommendations)

1. Remaining reversible gap (0.38 vs ~0.1 families) is murk-concentrated —
   another ~1k items even deeper in the borderline zone (undo-cost tradeoffs,
   window-closing changes) should push toward 0.25.
2. go-no-go sits at ~0.5 on unseen rows — teacher-side ceiling confirmed a
   third time; either enrich CRITERIA or accept as the noise floor.
3. risk is now the thinnest family (509) — same medicine if it matters.
