# 004 Intuition data: generate the teacher dataset — result

**DONE**

## Deliverable

`~/projects/intuition/data/graded.jsonl` — **3100 lines**, each
`{"text","band","family","probs":[p0,p1,p2],"score"}`, committed to the intuition project at `~/projects/intuition` (commit `c645b62`, along with `gen_candidates.py` and `grade_corpus_v2.py`).

Three families per DESIGN.md's quilt patches (load-bearing / coherence / go-no-go) × three bands (clear_yes / clear_no / murky), ~344 each.

## Band distribution + mean teacher entropy per band

| family | band | n | mean entropy (bits) | mean score (0..2) |
|---|---|---|---|---|
| load-bearing | clear_yes | 348 | 1.427 | 0.734 |
| load-bearing | clear_no | 342 | 1.314 | 0.615 |
| load-bearing | murky | 346 | **1.476** | 0.952 |
| coherence | clear_yes | 342 | 0.140 | 1.974 |
| coherence | clear_no | 347 | 0.569 | 1.747 |
| coherence | murky | 345 | 0.076 | 1.984 |
| go-no-go | clear_yes | 340 | 0.918 | 1.564 |
| go-no-go | clear_no | 343 | 0.784 | 0.445 |
| go-no-go | murky | 347 | 0.795 | 1.236 |

Overall mean entropy 0.834 bits (max 1.585). **Soft points (H > 1.4): 719 examples (23%).** The murky band of load-bearing is the softest territory in the corpus (H=1.48) and murky go-no-go sits mid-spread (1.24 mean score, dead center of the scale) — exactly the flashlight waveform DESIGN.md wants the student to learn.

## What was fixed along the way (both starter bugs reproduced and repaired)

1. **candidates.py**: qwen3.5:0.8b → qwen2.5:7b-instruct with few-shot + 40 topic-anchor rotation for diversity; the v1 parser's char-stripper ate real text and destroyed lines (and 7b sometimes emits literal "N." numbering — regex now handles it). 261 calls → 3100 unique (case-folded dedupe).
2. **A bigger bug than the task knew about**: teacher.py's *batched* call shape is item-blind. Every batched variant tested — item text inside each question, items as an array/object in state — returned near-identical distributions for "reward hacking?" vs "favorite color?". jev-preview only discriminates when the single item IS the state (the verified 003 battery pattern). grade_corpus_v2.py therefore makes one call per item, 4 workers, 0.06s/item, checkpointed (survived a mid-run kill). The first batched run is archived as `data/graded.jsonl.blindbatch-archived-20261007` — flat distributions across all bands, the tell.
3. Discrimination verified before shipping: go-no-go separates hard (clear_yes 1.56 vs clear_no 0.45); known jokes from 003 score 0.07.

## Honest caveats

- Coherence's clear_no band separates weakly (1.97 vs 1.75) — the 7b generator's "obviously incoherent" statements came out too subtle. And coherence/murky graded confidently coherent (H=0.08), so that family yields few soft points as-is. Recommendation for the next round: push the coherence generator toward structural fallacies (contradiction, non-sequitur) rather than "arguably off" statements, and mine the load-bearing murky band first — it's where the intuition lives.
