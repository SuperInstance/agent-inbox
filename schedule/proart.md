# proart (eileen, WSL) — bookings

Seats: `zcode` · `mcode` · `claude-code` · `gpu` (RTX 4050) · `stage`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| chrono-tensor | zcode | 2026-10-27 16:47 | 3h | 2026-10-27 20:00 | F10: quilt-engine v0.3.1 audit fixes (CC1 findings F1–F6) |
| chrono-tensor | zcode | 2026-10-27 16:47 | 3h | 2026-10-27 20:00 | F9: continuum-runtime slice 1 (Rust stream core) — overlaps F10 deliberately, light CPU |
| chrono-tensor | mcode | 2026-10-27 16:55 | 2h | 2026-10-27 20:00 | M1: DESIGN-V04 fog-prediction design note |
| system-three-paper | claude-code | 2026-10-27 18:35 | 2h | 2026-10-27 19:35 | System Three paper: Claude Code draft (headless, detached; no GPU) |
| system-three-paper | mcode | 2026-10-27 19:00 | 2h | 2026-10-27 20:00 | System Three paper: MiniMax Code draft (TUI; slot starts after chrono-tensor M1 ends) |
| system-three-paper | zcode | 2026-10-27 19:50 | 2h | 2026-10-27 20:50 | System Three paper: ZCode draft (TUI; slot starts after chrono-tensor F9/F10 end) |
| holodeck-plans | mcode | 2026-10-27 21:00 | 3h30m | 2026-10-27 22:00 | Big Project planning competition: MCode plan v1 + GAN critiques/v2 (TUI; slot starts after system-three-paper mcode ends). est: by=muse-coordinator type=design time=3h tok=~600k cost=plan range=2h30m-4h30m hor=booking-window cues=board read 19:28 UTC, formal-paper lane ahead on all three seats cont=descope to one GAN round xcl=TUI seats exclusive; no GPU |
| holodeck-plans | zcode | 2026-10-27 21:50 | 3h30m | 2026-10-27 22:50 | Big Project planning competition: ZCode plan v1 + GAN critiques/v2 (TUI; slot starts after system-three-paper zcode ends). est: by=muse-coordinator type=design time=3h tok=~600k cost=plan range=2h30m-4h30m hor=booking-window cues=board read 19:28 UTC cont=descope to one GAN round xcl=TUI seats exclusive; no GPU |
| holodeck-plans | claude-code | 2026-10-28 01:30 | 2h | 2026-10-28 02:15 | Big Project planning competition: Opus deep-think adjudication (headless, detached; no GPU). est: by=muse-coordinator type=design time=1h30m tok=~400k cost=plan range=1h-2h30m hor=after GAN rounds land cues=both v2 plans + critique trails on disk cont=adjudicate on v1s + critiques if v2s slip xcl=none |
