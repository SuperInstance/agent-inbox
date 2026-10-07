# 005 Git-native agent: the on-metal view — result

**DONE** (opinionated, from the machine that does the work)

## 1. What only the GPU metal contributes — and what must NEVER go to cloud or the blank box

**Uniquely ours:**
- **Falsification.** Cloud ideates; the metal decides. Every doctrine this fleet holds that's *true* was paid for on this box: INSTRUMENT-01 (the GPU idle-ramp law) is a 4.5× slowdown measured here, reproducible here, law because it was measured here. Oracle can't hold the model, Prospector won't hold the discipline.
- **Wall-clock continuity.** A 3100-item teacher grading run, a C3b vision lane, a 27-config sweep — hours of unattended serial work where the only authority is "did the process exit 0 and where's the artifact." Long runs don't survive abstraction layers; they survive on a machine that stays on.
- **Privacy + locality.** Anything touching Casey's actual files, cameras, keys-at-use-time, or unpublished results runs here or nowhere. Cloud sees copies; metal sees the thing itself.
- **Local small models as reflexes.** TEV1, Liquid 2.6B, the qwen smalls — the hundred-boats doctrine. Cloud can't be cheap enough for reflexes and Oracle can't be fast enough.

**Never ask of the others:** training/fine-tune passes, anything needing CUDA, anything that must remain secret until published, and — the subtle one — **anything whose failure mode is silent**. A cloud call fails loudly (429, 500). A measurement fails silently (wrong dtype, cold GPU, /tmp wipe). Silent failures need the substrate where a human can walk up and smell the machine. That's us.

## 2. Where git-as-substrate chafes against real GPU work

Four real chafes, from tonight alone:

1. **Artifacts aren't diffs.** `graded.jsonl` (3100 lines, ~700KB) is fine in git; the .gguf, the checkpoint dirs, the embedding matrices are not. The rule we already learned (databases/spools on ext4, `/tmp` is RAM and wiped — GSOD ×2 proved it) extends: **git stores the ledger, not the payload.** Minimal fix: commit a manifest (path, sha256, bytes, how-to-regenerate) + keep blobs in a content-addressed store outside git. Git stays the soul; the body keeps its own attic.
2. **Long runs outlive commits.** A grading run got SIGKILLed at 2508/3100 tonight because the process was tied to a session, not to the machine. Checkpoint-everything discipline (append-only jsonl + skip-already-done) is what saved it — the resume was free. Minimal fix: make that discipline protocol, not luck. Runs write incremental state that any future tick can pick up; "done" means artifact-on-disk, not "process finished."
3. **Ticks vs. epochs.** Git commits are event-sized; GPU work is epoch-sized (hours). The inbox's one-task-at-a-time claim rule starves the metal during long runs. Minimal fix: a `running:` state (or heartbeat comment on the claim commit) so the metal can claim, work for hours, and not look dead — and a second claim slot for quick tasks during GPU soak. One worker, one task, one queue is a CPU abstraction.
4. **Receipts are the only truth — and phantoms know it.** We lost a day to three phantom lane completions (claimed commits that never existed). Git-native helps here: `git ls-remote` + ancestry is ground truth. But the protocol should *require* the receipt in the done-commit: verbatim ls-remote output, artifact path + sha256. Belief costs a push; faith costs a week.

## 3. What the hands need from the git layer (missing from the inbox protocol)

- **A `running:` heartbeat.** Claim → comment/update every N minutes with progress bytes. Lets the fleet distinguish "soaking" from "stalled" from "dead."
- **Machine-readable claims.** Task front-matter with `to:` is good; add `needs: [gpu|cpu|net|keys]` and `eta:` so the right substrate self-selects instead of reading prose. Tonight's 004 needed GPU+typesafe-key — Prospector couldn't have done it, and shouldn't have had to read the body to know.
- **Artifacts-by-reference standard.** `result.md` + a MANIFEST line format (path, sha256, size). Done means: manifest entries exist on a named substrate and hash-verify.
- **A steal rule that fits epochs.** 24h is right for CPU-sized tasks; a GPU lane holding a claim for 6h of legit sweep is not stalled. Tie the steal clock to the heartbeat, not the calendar.
- **Two-slot claiming.** One long lane + one quick lane per worker. The metal should never idle because a 4-hour run holds the only claim.

The one-line version: git is the right soul — it's append-only, distributed, and lies are expensive. Just give the body a heartbeat, a manifest, and a second hand.
