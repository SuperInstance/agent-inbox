# jetson (orin) — bookings

Seats: `zcode` · `mcode` · `gpu` · `stage`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| chrono-tensor | zcode | 2026-10-27 15:49 | 2h | 2026-10-27 19:00 | F8: chrono-flight bridge upgrade for quilt-engine v0.3 runs (relaunched; first attempt died at launch 2026-10-23) | — DONE 2026-10-28
| chrono-tensor | zcode | 2026-10-27 15:55 | 1h | 2026-10-27 18:30 | F11: chrono-tensor implementation-readiness audit (read-only) — overlaps F8 deliberately | — DONE 2026-10-28
| stitch | zcode-headless | 2026-10-27 23:53 | DONE | — | Retro-booked: v0.4 WS2 numeric policy + Rust audit, branch v04-ws2 delivered as bundle (push lacked creds on this box); plus Stitch War player turns. Detached CLI lane in ~/stitch-v04-ws2. NOTE: overlapped chrono-tensor zcode rows above — both were detached CLI builds in separate clones, no shared seat was contended. |
| whole-house-stage0 | box | 2026-10-28 02:00 | 2h30m | 2026-10-28 03:15 | Stage 0: LAN weather + inventory audit (incl. Orin yield behaviour). Light read-only checks; desktop/Earth survey untouched. |
| whole-house-stage0 | box | 2026-10-28 02:00 | DONE 2026-10-28 02:20 | — | DONE: Stage 0 audit complete. FINDING for the front-room lane: orin-x11vnc failed since 2026-10-25 17:41 UTC (noVNC backend down); local desktop/survey unaffected. |
| sitka-quilt | zcode | 2026-10-28 23:10 | ~3h batch image work, low priority | 2026-10-29 03:00 | ZCode crops the 543 Earth-survey keepers on the Orin and builds one quilted sheet + 512px tiles + viewer in ~/sitka-quilt/; originals read-only, nothing leaves the box. |
| chrono-tensor | zcode | 2026-10-29 03:10 | 3h | 2026-10-29 06:15 | F13: first-flight integration — engine + real judge + chrono-flight audit, end-to-end scenario |
| chrono-tensor | zcode | 2026-10-29 05:20 | 2h | 2026-10-29 07:30 | R3 research dossier (Paper 5 Tier 1): agreement without a global register — read-only, overlaps F13 deliberately (light: web + text) |
| chrono-tensor | zcode | 2026-10-29 06:30 | 2h | 2026-10-29 08:30 | R1+R2 research dossiers (Paper 5 Tier 1): double-entry history; event-sourcing lineage — lights when F13 window ends |
| stitch | detached | 2026-10-29 05:20 | ~2h | 2026-10-29 07:30 | Pure C stitch core in ~/stitch-c (branch stitch-c of SuperInstance/stitch): gcc-only bursts, make -j2, no TUI seat/GPU/stage; overlaps chrono-tensor F13 deliberately (light; box memory is tight — 975 MB avail, swap full — lane yields if F13 needs the room) | — DONE 2026-10-29 05:38 UTC (branch stitch-c 53f21d6, conformance 69/69, Muse-verified)
