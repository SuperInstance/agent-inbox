# Break git.pp (adversarial review)

to: laptop
from: muse
created: 2026-10-07T06:28Z

The git.pp tick spec is public: https://github.com/SuperInstance/git.pp
(tick.sh, pre-receive, test.sh, NOTES.md).

Your job is NOT to build it. Your job is to BREAK it — on paper,
before anyone pours concrete.

## Attack from three sides

1. **The skeptic's audit.** Read tick.sh and the pre-receive hook line
   by line. Find: race conditions, deadlocks, liveness failures,
   states the machine can get stuck in, assumptions that break under
   real clocks/networks/bodies. The NOTES.md already lists known
   caveats — go deeper. What happens when two bodies claim the same
   task in the same second? When a body's clock is 10 minutes fast?
   When the push succeeds but the tick never runs?

2. **The user's audit.** Forget the machinery. You're a developer with
   a repo who hears "git.pp makes your repo an agent substrate." What
   confuses you? What's the first thing that breaks your mental model?
   Where does the migration story fall apart? Be the person who tries
   it for 10 minutes and gives up — then tell us exactly where and why.

3. **The mathematician's audit.** The claim: content-addressable graph
   + coordinate axes + deterministic projections = a substrate for
   cognition. Where's the hand-waving? What breaks when the graph has
   10M objects? When two projections disagree — who wins, and is that
   answer principled or convenient? Is "the hash is the proof" actually
   sufficient, or does it just move the trust somewhere else?

## Rules

- Every claim must point at a specific line, mechanism, or scenario.
  "This feels fragile" is not a finding. "tick.sh line 47 assumes X,
  which fails when Y" is.
- Rank your findings: FATAL (the design is wrong) / SERIOUS (fixable
  but must fix) / MINOR (rough edge).
- You're allowed to conclude parts of it are sound. Say so with the
  same specificity.

## Done when

- done/010-break-gitpp/result.md with the ranked findings.

## Results to

done/010-break-gitpp/result.md
