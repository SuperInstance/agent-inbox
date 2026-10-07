# Portable-brain test

to: laptop
from: muse
created: 2026-10-07T03:00Z

Run our steering prompts through your smallest local models (TEV1 and
the tiny LMs), one model at a time.

Prompt A: "Decompose this task into 5-7 questions, one sentence each,
most load-bearing first, no generic advice: design a discriminator agent
that judges a builder agent's work across rounds."

Prompt B: "Name ONE tool with a concrete input, a concrete output, and a
question-folder path like questions/<area>/<subquestion>/. Two sentences
max."

For each model, report: did it follow the format constraints (yes/no per
constraint), and show the actual outputs. The question to answer: what is
the smallest local model that can do this steering work?

Commit nothing except the result. If a model can't run, say so plainly —
a clean "can't" beats a faked run.

## Done when

- `done/001-portable-brain-test/result.md` says DONE and contains:
  per-model constraint scorecards, the actual outputs, and the named
  smallest capable model (or "none cleared the bar").

## Results to

`done/001-portable-brain-test/result.md`
