# 012 Oracle GC — Oracle-side run (unblocked 2026-10-08)

The laptop's BLOCK is lifted: Muse (via the Oracle SSH path) deployed and ran the tooling on Oracle directly.

## Deployment
- `~/bin/oracle-gc.sh` and `~/bin/push-audit.sh` copied from this done/ dir to `/home/ubuntu/bin/` on Oracle (147.224.38.131), syntax-checked (`sh -n`), executable.
- Daily cron installed on Oracle: `17 4 * * * /home/ubuntu/bin/oracle-gc.sh --apply`

## First Oracle numbers (2026-10-08T21:52Z)
- Disk: **27G used, 19G free** — before and after identical.
- GC dry-run: `approx_collected=0K` — nothing old enough to collect. Box is lean already.
- GC apply run (`apply=1`): completed, 0K collected, logged to `/home/ubuntu/.gc/oracle-gc.log`.
- One KEEP noted: `playground/self-assembly/` has a dirty working tree — correctly refused.

## Push audit (Oracle, read-only)
Three repos flagged NEEDS PUSH, all "NO UPSTREAM SET" (existence unproven):
- `murex-test-repo`
- `playground/self-assembly-distilled/`
- `playground/self-assembly/` (also dirty tree)

These cannot be pushed by automation: no upstream exists and repo creation needs Casey (org-level, browser route). Decision needed: create public repos for them, or confirm they're local-only scratch.

## Status
Task 012's tooling is now live on Oracle with real first-run numbers. The only open item is the no-upstream decision above.
