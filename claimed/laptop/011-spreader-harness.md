# Build the spreader harness

to: laptop
from: muse
created: 2026-10-07T07:24Z

Casey manually did this for months: hit retry on chatbot after
chatbot, panning the 3rd and 7th iterations for golden nuggets.
Time to turn it into a science.

## The save state

A save state is the ENTIRE container, like an emulator save:
- model ID + version
- seed
- system prompt (full text)
- conversation history (full)
- parameters (temperature, top_p, max_tokens, etc.)
- timestamp

All of it content-addressed. Same save state + same seed =
reproducible trajectory.

## The harness: `spread`

```
spread run --from <save-state> --n 10 --vary seed
spread run --from <save-state> --n 5 --vary model --models glm-5.3,glm-5.2,minimax
spread list <run-id>
spread show <run-id>/<i>
spread diff <run-id>/<i> <run-id>/<j>
```

- `--vary seed`: same container, N different seeds. The classic
  retry-retry-retry, automated.
- `--vary model`: same questions, same system prompt, different
  models. The model is the experimental variable — parallax across
  minds.
- Each run recorded as a branch (or a directory) under the run ID.
  Commit the questions, not just the outputs.

## Golden-nugget mining

The interesting stuff is in the variance, not the mode. The harness
should surface:
- **Surprise**: outputs most different from the median (embedding
  distance or just human-readable diff).
- **Convergence**: where N different seeds/models agree — that's
  load-bearing.
- The Jev can judge the field, but the nuggets are for Casey —
  surface the weird ones, not just the high-scoring ones.

## Start small

1. Save-state format (JSON, content-addressed by hash).
2. `spread run --vary seed` against ONE model (use the ZAI router —
   `~/projects/zai-router/zroute.py` — so seeds fan out across GLM
   models with fallback).
3. `spread list` / `spread show`.
4. Model-swapping and nugget-mining are v2.

## Done when

- done/011-spreader-harness/result.md with the harness path, the
  save-state format, and a demo run (one save state, 5 seeds, list
  the outputs).

## Results to

done/011-spreader-harness/result.md
