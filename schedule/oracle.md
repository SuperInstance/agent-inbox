# oracle (OCI Ampere A1) — bookings

Seats: `zcode` · `mcode` · `box`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| whole-house-stage0 | box | 2026-10-28 02:05 | DONE 2026-10-28 02:10 | — | Retroactive note: light read-only inventory checks only (versions, gh auth, df/free) for the Stage 0 fleet audit. No seats driven, nothing changed. |
| papers-ledger | zcode | 2026-10-28 19:50 | ~3h digest, pushes as it goes | 2026-10-28 23:30 | ZCode digests SuperInstance-papers into LEDGER.md + TOPICS.md + papers-index.json + forgotten-knowledge notes; additive only, no file moves. |
| stitch | detached | 2026-10-29 05:20 | ~3h | 2026-10-29 08:30 | Lean 4 formal spec of stitch in ~/stitch-lean (branch stitch-lean): elan toolchain install + lake builds, CPU bursts only; papers-ledger and quilt-mcode sessions untouched | — DONE 2026-10-29 05:37 UTC (branch stitch-lean 643aa74, lake build green, 0 sorry, Muse-verified)
| jacquard-build | box | 2026-11-02 19:25 | 3h | 2026-11-02 20:30 | DONE 2026-11-02 — Jacquard Phase 1 complete: SuperInstance/jacquard @ 665a57e, 46/46 tests, all four acceptance criteria pass |
| jacquard-build | box | 2026-11-02 20:05 | ~4h | 2026-11-02 21:05 | DONE 2026-11-02 — Jacquard Phase 2 complete: main @ 9148e8f, 119 tests, cold-clone verified |
| jacquard-build | box | 2026-11-02 20:40 | ~5h | check-by 2026-11-02 22:00 | DONE 2026-11-02 — Jacquard Phase 3 complete: main @ 3ce55ff, tag v0.2.0, 128 tests, CI green, tag artifact verified |
| jacquard-build | box | 2026-11-02 21:15 | ~4h | 2026-11-02 23:45 | DONE 2026-11-02 — Jacquard Phase 4 complete: spec 0.3, tag v0.3.0 @ 22d6092, main @ 5c4e619, 198 passed + 7 declared skips, TS checker 7 PASS / 3 SKIP, tag artifact cold-clone verified by coordinator |
| jacquard-build | box | 2026-11-02 22:15 | ~8h | 2026-11-03 01:00 | DONE 2026-11-02 — Jacquard Phase 5 complete: main @ 0f7a937, 249 passed + 7 skipped (cold-clone verified); slices 12-15 all landed; proof run in docs/proof-run-2026-11-02.md — headline deficit: approvals do not yet compile into rules for queued shapes (learner trains on policy outcomes) |
| jacquard-build | box | 2026-11-02 23:10 | ~6h | 2026-11-03 02:00 | Jacquard Phase 6: operator-trained learner (slice 16) + any-quotation hazard closure, spec 0.4 (slices 17) | — DONE 2026-11-03 — Jacquard Phase 6 complete: spec 0.4, tag v0.4.0 @ 6bd88d6, 266 passed + 7 skipped, TS checker 7 PASS / 3 SKIP, tag artifact cold-clone verified by coordinator; live proof run 2: queue 14/15 -> 1/16 queued, ~3 operator-min/100 marginal vs Phase 5 baseline ~11 |
