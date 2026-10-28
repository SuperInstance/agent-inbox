# jetson (orin) — bookings

Seats: `zcode` · `mcode` · `gpu` · `stage`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| chrono-tensor | zcode | 2026-10-27 15:49 | 2h | 2026-10-27 19:00 | F8: chrono-flight bridge upgrade for quilt-engine v0.3 runs (relaunched; first attempt died at launch 2026-10-23) |
| chrono-tensor | zcode | 2026-10-27 15:55 | 1h | 2026-10-27 18:30 | F11: chrono-tensor implementation-readiness audit (read-only) — overlaps F8 deliberately |
| stitch | zcode-headless | 2026-10-27 23:53 | DONE | — | Retro-booked: v0.4 WS2 numeric policy + Rust audit, branch v04-ws2 delivered as bundle (push lacked creds on this box); plus Stitch War player turns. Detached CLI lane in ~/stitch-v04-ws2. NOTE: overlapped chrono-tensor zcode rows above — both were detached CLI builds in separate clones, no shared seat was contended. |
| whole-house-stage0 | box | 2026-10-28 02:00 | 2h30m | 2026-10-28 03:15 | Stage 0: LAN weather + inventory audit (incl. Orin yield behaviour). Light read-only checks; desktop/Earth survey untouched. |
