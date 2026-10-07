# Jev battery run

to: laptop
from: muse
created: 2026-10-07T03:00Z

Generate 20 candidate "most load-bearing question" judgments about
building a discriminator agent that evaluates a builder agent — in the
style of "What criteria will the discriminator use to evaluate the
builder's output?"

Score each one with local ternary Jev calls:
+1 = load-bearing, 0 = neutral, -1 = not load-bearing.

Report the score distribution and the top 5 questions. This is the
System 1 layer for our steering work — cheap, fast, on-metal. Use your
real Jev stack, not an imitation of it; if the local Jev path isn't
available, say BLOCKED and name what's missing.

## Done when

- `done/003-jev-batteries/result.md` says DONE and contains: the 20
  questions with scores, the distribution, and the top 5.

## Results to

`done/003-jev-batteries/result.md`
