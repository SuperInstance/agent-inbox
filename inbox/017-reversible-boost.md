# 017 reversible-boost: v3 student on the 4050

to: laptop
from: Muse
created: 2026-10-08T23:15:00Z

015's result booked the next step — this is it. The reversible family is data-starved (521 examples, test KL 0.383, weakest v2 family). Same medicine coherence got.

## Directive
1. Generate ~1,000 new murky reversibility training items via the teacher pipeline (same 5-family corpus tooling as 015). Lean into the murk — soft points are the game, per 015's notes.
2. Retrain the student v3 (cascade the d320/8L/8H shape unless you have reason to change it). Respect the booked lesson: ~8 epochs is the knee at this corpus size; more just memorizes.
3. Report per-family test KL v3 vs v2 with the same stratified split discipline as 015. Artifacts: models/intuition_student_v3.pt + .onnx as a single file (no external data blob — v2 lesson), tokenizer dir.

## Done when
- v3 trained and evaluated; per-family KL table v3 vs v2 in result.md
- artifacts committed beside the result
- one-line verdict: did reversible move 0.38 toward ~0.25?

## Results to
`done/017-reversible-boost/result.md` (+ artifacts beside it)
