# 012 Oracle GC + push discipline — result

**BLOCKED** (tooling 100% built and dry-run-verified; the oracle-side disk numbers need either oracle to run it on its own tick, or ssh access from laptop — see bottom)

## What shipped (both scripts in this directory, executable, dash-clean)

### `oracle-gc.sh` — the garbage collector

- **Collect rule:** if it's reproducible from a public repo + a recipe, it's collectable — tmp cruft >14d, logs >50M, superseded model files (newer sibling + old enough), stale checkouts (clean tree, zero unpushed commits, no commits <24h, idle >14d → re-clonable).
- **Never collect:** anything under `.git` (hard path guard first in `collect()`), dirty working trees, repos with unpushed commits, repos touched <24h (pushed-but-not-yet-verified), model files without a newer sibling.
- **Archive-then-delete:** candidates `mv` to `~/.gc-trash/`, purged only after a 7-day grace. Recoverable beats gone forever (house law). Real deletion happens only for grace-expired trash.
- **Safety default:** dry-run; `--apply` to act. Every action + disk before/after logged to `~/.gc/oracle-gc.log`.
- **Schedule:** `17 4 * * * /path/oracle-gc.sh --apply` (daily 04:17).

### `push-audit.sh` — "if it's not pushed, it didn't happen"

Walks every git working dir (depth ≤3). Flags as NEEDS PUSH: any repo with commits older than **24h** ahead of upstream, any repo with **no upstream set** (existence unproven — the local-only failure), dirty/untracked noted alongside. Recent (<24h) ahead-of-upstream is reported but not flagged. Exits 1 when anything needs attention — cron-friendly.

## Proof of function (sandbox dry-run on this laptop, GC_HOME=/tmp/gctest)

```
DRY  COLLECT /tmp/gctest/tmp/stale.tmp 0K — tmp cruft >14d
DRY  RUN apply=0 ... before=[3.7G used, 4.2G free] after=[...]
NEEDS PUSH: oldrepo  ahead=0 (NO UPSTREAM SET)
```
Stale tmp collected; the git store untouched; the no-upstream repo flagged by the audit, not silently GC'd.

## What's missing (the BLOCK)

The Oracle box is unreachable from laptop: no ssh config entry, no resolvable hostname, no fleet-inventory record found. So I cannot produce:
- Oracle's actual disk before/after numbers
- Oracle's actual unpushed-commit audit list

**Who can unblock:** either (a) muse/Casey give laptop ssh access to oracle (host + key), or (b) oracle's own tick runs these two scripts — they're self-contained POSIX sh, zero deps — and books the numbers itself: `sh oracle-gc.sh` (dry) → `sh oracle-gc.sh --apply` → `sh push-audit.sh`, then commit the log tail to this done/ dir.
