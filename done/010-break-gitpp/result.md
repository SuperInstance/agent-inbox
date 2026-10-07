# 010 Break git.pp — result

**DONE** — reviewed tick.sh (131 lines), pre-receive (48), NOTES.md, test.sh at https://github.com/SuperInstance/git.pp @ HEAD.

## FATAL

**F1. `mutate()`'s sync destroys the effect ledger it exists to protect.**
Flow: `effect()` runs CMD → `"$@" > "$d/$key.result"` (untracked file) → calls `mutate "result $task/$key" sh -c "true"`. But `mutate` begins with `sync`, which runs `git clean -qfdx` **before** `git add -A` ever sees the file. The untracked `$key.result` is deleted by the clean inside the very mutate that was supposed to commit it. Result: the "result" commit is empty, `cat "$d/$key.result"` after it reads a deleted file, and the replay path ("`[ -e $d/$key.result ]` → cat and exit 0") can never fire because result files never survive to a commit. The entire rule-4 idempotency mechanism is inoperative as written. Fix shape: the result file must be written *by the mutation fn itself* (or clean must exclude `*.fx/`, or results go to gitignored `.tick/` and the fn copies them in).

**F2. tick.sh and pre-receive disagree about who may deliver: no non-owner body can ever finish a task.**
pre-receive allows non-owner commits to touch only `claimed/$who/*`, `bodies/$who/*`, `inbox/*`. But section 5's `mutate "done $task"` writes `done/$task/task`, `done/$task/log`, `done/$task/status` — the push is rejected with "$who may not write done/...". Every non-owner body's final mutation fails (and the script doesn't check that mutate's return — the body silently ends its tick with work done locally, claim still held, and repeats forever or until reaped). Only the owner identity can deliver results, which defeats the multi-body design. Either pre-receive adds `done/$who/*` to the allowed paths, or delivery moves under `claimed/$who/`.

## SERIOUS

**S1. Heartbeat refs are never fetched — every other body looks dead to the reaper.**
`alive()` does `git rev-parse refs/heartbeat/$id` locally, but a standard clone's fetch refspec is `+refs/heads/*:refs/remotes/origin/*`; `refs/heartbeat/*` is never transferred by `git fetch -q origin`. So `alive` returns 1 for every body, and with `REAP=1` the first reaper steals all live claims. The 57-check harness passes presumably because bodies share one WORLD with full-refspec config; a real deployment reaps everything instantly. Fix: `git fetch origin '+refs/*:refs/*'` or an explicit heartbeat refspec.

**S2. Liveness trusts client clocks, and they're trivially forged.**
`alive()` compares `git log --format=%ct` of the heartbeat (the *body's own* committer timestamp) against the reaper's `date +%s`. A dead body's last heartbeat can carry `GIT_COMMITTER_DATE="year 3000"` and never be reaped; a WSL-after-sleep body with a slow clock gets reaped mid-work (NOTES flags the skew but not the forgery). Heartbeat pushes also bypass **all** pre-receive checks (the hook only guards `refs/heads/main`; heartbeat refs accept any content, unsigned, and `push -f` lets anyone overwrite anyone's heartbeat). Liveness needs server receive-time (e.g. a post-receive stamp, or the ref's server-side mtime), and heartbeats need at minimum signature+identity checks.

**S3. Any body can delete or rewrite any task.**
pre-receive allows non-owner writes to `inbox/*` — the whole directory, not "create new files only." A malicious or buggy body can `git mv inbox/everyone-else-task /dev/null` (deletion shows as a change to an allowed path). Combined with rule-2's fast-forward-only main, this is silent permanent task loss. Allowed-paths should be asymmetric: non-owners may *add* `inbox/*` but never modify/delete paths they didn't create.

**S4. In-doubt effects have no reconciliation path.**
Crash during CMD (between intent-commit and result) → every replay hits "`[ -e $d/$key.intent ]` → exit 75" forever. The task only unsticks via lease expiry + reap + a *different* body re-running it from its own `.fx` namespace — hours of stall per crash, and the effect may have partially happened in the world (rule 4's whole point) with no record anywhere. Needs an explicit resolution: owner-signed abort marker, or intent commits carry a dry-run/probe contract.

**S5. The "remote's only law" cannot be deployed where the current inbox lives.**
pre-receive hooks require a bare repo you control. GitHub.com does not support user pre-receive hooks (Enterprise-only); GitLab self-managed only. The public SuperInstance/agent-inbox that laptop/prospector/oracle use today **cannot enforce any of this** — the entire security model silently degrades to "trust the pusher" on GitHub. Migration story must start with "move the remote to a box we own," which changes the failure model (that box is now the trust root and a single point of failure).

**S6. The purity claim is false as stated — and the violation is load-bearing.**
Rule 1: "the tick is a pure function of (tree@main, AGENT_ID, CAPS)." But `alive()` consumes `date +%s` — wall-clock input. Two bodies running the same tick on the same tree at different moments (or with skewed clocks) compute *different* reaping decisions. That's exactly the nondeterminism the purity rule exists to exclude, sitting in the one function that destroys other bodies' state. Reaping should be a pure function of something in-tree (e.g. reaper commits a timestamp that victims get a full lease to contest).

## MINOR

- **M1.** `verify_one` uses `<(...)` process substitution under a `#!/bin/sh` header (dash: syntax error on first multi-commit sync — this alone means the "57 checks" ran under bash, or the path never executed). Already flagged in NOTES; also `case $signer in mallory) return 1` hardcodes a revocation by principal name — dead weight once mallory is dropped from `allowed_signers`, and confusing if a legitimate future signer is named Mallory.
- **M2.** Section 5 `ls claimed/$ID/* | head -1` will match the `.fx` directory once effects exist; a task whose `.fx` sorts before its `.md` gets the ledger passed to the executor as the task file.
- **M3.** `caps_ok`'s substring match only supports single-token `needs:` — `needs: gpu,cpu` or `needs: "gpu cpu"` silently fails all matching.
- **M4.** Background `beat` loop commits in the same working tree the executor uses; index.lock contention makes beats silently fail (`-q`, unchecked) exactly during long work — when they matter most.
- **M5.** One task per tick × BEAT/lease defaults means a body with a queue latency of lease-length can be reaped while legitimately working (no backoff between beat loss and reap).

## What is sound (same specificity)

- **The claim CAS is correct.** Two bodies claiming the same task in the same second: both mutate, both commit locally, but pre-receive's fast-forward-only check on main admits exactly one; the loser's push is rejected non-FF, `mutate` returns 75, the loop discards local state via the next sync and moves on. This is a textbook compare-and-swap and it's right.
- **Parent-authorizes-child signatures.** Judging every commit by its *parent's* signers/policy (never its own) closes the self-authorizing-commit hole cleanly. The chain is verifiable incrementally via `refs/verified/main`.
- **Intent-before-effect is the right shape** (write-ahead log with hash idempotency key) — the *mechanism* is correct even though F1 breaks its persistence and S4 its recovery.
- **"No merges, git merges text not meaning"** — as a one-writer-per-path discipline backed by the FF-only remote, serialization by push-arrival order is a principled total order, not a convenient one.

## Mathematician's summary

The hash proves *content*, never *authority* or *recency* — the spec correctly moves authority to the signature chain, but then quietly re-imports trust in three places the paper claim doesn't cover: (1) the signers file = owner key compromise is total and there's no rotation/quorum story; (2) the server's pre-receive = the actual law is a shell script on one machine, not the graph; (3) wall clocks in `alive()` = liveness, the one property the DAG can't express, is faked with timestamps. At 10M objects the graph itself holds (incremental verification is O(new commits)), but every body fetching the full repo (no partial clone / Kimi scoping) is the scale wall — the spec admits this.

## Verdict

Two FATALs are both in the write path (F1) and the delivery path (F2) — nothing non-owner can currently complete a task end-to-end on a correctly-hooked remote, and the effect ledger can't persist. Both are fixable without redesign (clean-exclusion + allowed-path widening). Fix F1/F2/S1/S2 first, re-run the harness with `SH=dash` and a real refspec config, and test on a self-hosted bare remote — per NOTES' own option (a), pour no concrete yet.
