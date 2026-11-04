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
| rolling-perception | zcode (own tmux lane-tt) | 2026-11-03 16:10 | ~2h docs build | 2026-11-03 18:30 | telltape BYO-embedder tutorial drafted from the public v0.3.2 repo in ~/lane-telltape-tutorial; detached TUI seat in own session, no stage/GPU, no contention with resident lanes |
| jacquard-build | zcode (detached, new dir) | 2026-11-03 17:15 | ~6h | 2026-11-03 19:15 | Jacquard Phase 11 slice 30: ZCode adapter deployment in ~/jacquard-p11-seat/ (new dir, detached seat process); overlaps rolling-perception deliberately per protocol (light CPU, yields on memory); lane-tt and the desktop are NOT touched |
| jacquard-build | zcode | 2026-11-03 19:45 | 2h | 2026-11-03 20:45 | Phase 11 slice 31: stranger test — cold agent onboards from the draft docs alone (jq:jacquard-build-orin-zcode-2026-11-03-19-45) | — DONE 2026-11-03 21:23 UTC (jacquard)
| jacquard-build | zcode | 2026-11-03 17:50 | 2h10m | 2026-11-03 18:40 | Phase 11 slice 30 (governed): Orin ZCode adapter deployment session in ~/jacquard-p11-seat/ — seat contention with rolling-perception is real; the tie holds and the operator releases after the incumbent window (jq:jacquard-build-orin-zcode-2026-11-03-17-50) |
| jacquard-build | zcode | 2026-11-03 21:40 | 1h | 2026-11-03 22:50 | slice 31 stranger re-run (Orin seat, fixed docs) (jq:jacquard-build-orin-zcode-2026-11-03-21-40) | — DONE 2026-11-03 21:35 UTC (jacquard)
| rolling-perception | zcode (own tmux lane-tt) | 2026-11-03 17:35 AKST | ~2h docs build | 2026-11-03 20:00 AKST | Job 2 for the proven seat: tenancy-ladder tutorial from the public rolling-perception repo in ~/lane-tenancy-tutorial; same session/workdir discipline as job 1 |
| jacquard-build | mcode | 2026-11-04 02:37 | 4h | 2026-11-04 06:37 | Phase 14 slice 39: MCode hook live-fire + adapter |
