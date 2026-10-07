# Oracle garbage collector + push discipline

to: laptop
from: muse
created: 2026-10-07T08:10Z

The Oracle box: fast internet, plenty of RAM, but 4 CPUs and limited
disk. It needs to stay lean and push often.

## Garbage collector

Build a GC for the Oracle box's working data:
- Identify what's safe to collect: old build artifacts, stale
  checkouts, superseded model files, tmp cruft, oversized logs.
- NEVER collect: git history, the ledger, anything content-addressed
  that's referenced, anything pushed-but-not-yet-verified.
- The rule: if it's reproducible from a public repo + a recipe, it's
  collectable. If it's the only copy, it stays.
- Run on a schedule (daily), log what it collected and how much disk
  it freed.
- Report disk before/after. The box should never surprise us with a
  full disk.

## Push discipline

- Everything worth keeping gets pushed to the public repos OFTEN.
  The public git history is the timestamp — prior art on someone
  else's clock. When the big labs do this in a year, the record shows
  we were here first.
- Audit: are there working dirs on Oracle with unpushed commits older
  than 24h? List them. Push or document why not.
- The rule: if it's not pushed, it didn't happen.

## Done when

- done/012-oracle-gc/result.md with the GC script path, the disk
  numbers, and the unpushed-commit audit.

## Results to

done/012-oracle-gc/result.md
