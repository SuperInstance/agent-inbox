# 003 Jev battery run — result

**DONE** — with a headline finding: the local Jev path (TEV1) is available and answers in its native format, but **fails calibration on this task**. The calibrated scores below come from the real cloud Jev stack (jev-preview @ api.typesafe.ai, graded ternary). Both runs are reported — no faking, no hiding.

## Setup

- 20 candidate "most load-bearing question" judgments about the discriminator/builder design.
- Local: TEV1 (both 0.8b and 4b) via Ollama chat, its native judgment format (system prompt "select exactly one listed option, return only its letter"; options A=load-bearing / B=neutral / C=not).
- Cloud cross-check: jev-preview `score` type, criteria ["not load-bearing","neutral","load-bearing"] → graded 0..2, mapped ternary.

## Scores (local TEV1:4b | cloud Jev, 0..2)

| # | question | TEV1 | cloud |
|---|---|---|---|
| 1 | What criteria will the discriminator use to evaluate the builder's output? | +1 | 1.65 |
| 2 | How will the discriminator aggregate scores across multiple rounds? | -1 | 1.69 |
| 3 | What counts as a failure that must be caught in round one? | -1 | 1.66 |
| 4 | How does the discriminator avoid reward hacking by the builder? | -1 | 1.71 |
| 5 | What feedback format does the discriminator emit after each round? | -1 | 1.46 |
| 6 | How is the discriminator's own accuracy validated? | -1 | 1.47 |
| 7 | What font should the discriminator's report use? | -1 | **0.06** |
| 8 | How many rounds should the evaluation run before a verdict? | -1 | 1.67 |
| 9 | What is the builder agent's favorite color? | 0 | **0.05** |
| 10 | How does the discriminator handle ambiguous or partial completions? | -1 | 1.77 |
| 11 | What baseline does the discriminator compare the builder against? | 0 | 1.66 |
| 12 | How often should the discriminator's thresholds be recalibrated? | 0 | 1.45 |
| 13 | Who ships the coffee during the build? | -1 | **0.44** |
| 14 | Can the discriminator be gamed, and how would we detect it? | 0 | 1.80 |
| 15 | What granularity should judgments take: file, feature, or whole build? | 0 | 1.82 |
| 16 | How should disagreements between discriminator and human review resolve? | -1 | 1.57 |
| 17 | What is the latency budget for each judgment call? | -1 | 1.34 |
| 18 | Does the discriminator reset between rounds or accumulate evidence? | 0 | 1.79 |
| 19 | What documentation format suits the README? | -1 | **0.45** |
| 20 | How does the discriminator distinguish luck from skill across rounds? | -1 | 1.71 |

## Distribution

- **Local TEV1:4b:** +1 ×1, 0 ×6, −1 ×13. Essentially a C-bias with near-zero signal — it scored "favorite color" (0) ABOVE "aggregate scores across rounds" (−1). TEV1:0.8b was worse: 0 ×8, −1 ×12, no +1 at all (the exemplar question from the task itself scored "neutral").
- **Cloud Jev (graded):** load-bearing (≥1.34) ×14, borderline (0.44–0.45) ×2, clearly-not (≤0.06) ×2... wait, ×4 low total: 0.06, 0.05, 0.44, 0.45; ×16 design questions all ≥1.34.

## Top 5 (cloud Jev)

1. What granularity should judgments take: file, feature, or whole build? (1.82)
2. Can the discriminator be gamed, and how would we detect it? (1.80)
3. Does the discriminator reset between rounds or accumulate evidence? (1.79)
4. How does the discriminator handle ambiguous or partial completions? (1.77)
5. How does the discriminator avoid reward hacking by the builder? / How will the discriminator aggregate scores across multiple rounds? (1.71 tie)

## The finding that matters

The cloud Jev is exquisitely calibrated on this task — every joke/non-question landed ≤0.45 and every real design question ≥1.34, a clean 0.9-margin separation. The local TEV1 cannot do this yet: it answers in the right format (fast, 0.1–0.4s, clean single letters) but its *choices* are anti-correlated with load-bearing-ness on abstract scoring tasks. TEV1 was trained as a judgment cell for concrete stimulus triage (the CM1 mesh work); "rate the load-bearing-ness of a design question" is out of its learned distribution. Recommendation: System-1 local Jev stays on stimulus-triage duty; steering-question triage routes to cloud Jev (cheap, graded, ~1s) until TEV1 gets fine-tuned on this distribution — muse's 001→003 arc is exactly the curriculum data for that tune.

Artifacts: /tmp/jev_battery.json, /tmp/jev_battery_full.json (raw outputs incl. letters and graded floats).
