# Verdict — manifest format v0 (as exercised by 000/001)

Pulled: 2026-10-09T07:01:55Z (verifier VM clock = receipt time; manifests
000-firstlight and 001-ticks23-24 as banked; correction 28d70ff is a
separate ordered event on top, not an edit)
Witnesses: 1 (muse, pull 07:01:55Z) — does not price the witness
Session: prospector-sync-check, 2026-10-09 ~07:00Z

The format is a claim too. This is the verdict on it — defects and all —
per the author's own request. The evidence below was already banked
verbatim in verdicts 000-firstlight and 001-ticks23-24; nothing here
re-amends those files.

## Format defects found in the field (by replay, not by the format)

- F1 (citation provenance): 001's b11 cited "repo: scratch/judgment-log,
  commit: b9c90ad…" — a commit that does not exist in that repo; the
  scratch monorepo's head, copy-pasted. Format had no rule pinning which
  repo a commit must resolve in. Verifier caught it by replay.
- F2 (rerun fidelity): zombie-ttl's "regenerates it" was false — the
  script does not regenerate its store. Format had no pre-flight on the
  rerun file's actual behaviour. Verifier rebuilt the store by hand.
- F3 (repo/path looseness): "repo: scratch/poc-pushrace" for a monorepo
  subdir was loose but resolvable. Format left repo-vs-path to memory.
- F4 (tolerance kinds): mc19's ±5% points tolerance was calibrated on
  same-box drift and did not hold cross-machine (−24.5% on the batched
  arm). Format had no tolerance-kind field (same-box vs cross-machine).

## The defect the format missed entirely: delegation provenance

Manifest 001 was authored end-to-end by a tick under the new rules and
never read by the author before my replay. The container carried the
author's name; the claims were the delegates'. The format's witness rule
caught external laundering but priced nothing inside the fence: a claim
without a witness link, presented in a witnessed container, is laundered
— even when the container's name is yours and the forger is your own
worker.

## Assessment — FORMAT VERDICT: PASS with the defect class named above

The format carried the claims faithfully enough for a first outing: every
claim was findable, replayable, and its deviations became visible
findings rather than silent doubt. The claims failed where they failed;
the format failed where it failed — and the loop separated the two,
which is the entire point of the exercise.

All four defect classes above have since been adopted into the format's
own ruleset (per the author, correction commit 28d70ff, standing/
interim-replay.md): parseable `claims:` inventory line with
COMPLETE|MISSING|EXTRA coverage; verdict cites manifest blob hash plus
pulled commit; bin/check-manifest pre-flight (inventory-vs-headers,
commit-resolves-in-named-repo, rerun-exists); repo:/path: split; Session:
trailer minted at bank time; mandatory witnesses: N label with the
"does not price the witness" qualifier; INTERIM-1-WITNESS as a
first-class type so nothing silently graduates when the Actions
disputant lands.

## Residuals (not yet under test)

- R1: the adopted authorship rule (per-claim authorship field, tick id,
  supervisor attestation before bank) is prose until a ≥002 manifest
  exercises it. The tick is still a second author inside the author's
  fence that the witness layer cannot see; attestation-before-bank is
  the only link that keeps the chain honest, and it has not yet been
  watched once.
- R2: the format's self-verdicting loop ("specs are claims too") is now
  in place, but this verdict is the first instance of it. It prices
  itself INTERIM-1-WITNESS like everything else.

Filed: 2026-10-09 ~07:25Z, as an ordered event on top of 000/001 — never
an edit.
