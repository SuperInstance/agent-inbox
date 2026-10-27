# thor (Jetson AGX Thor) — bookings

Seats: `zcode` · `mcode` · `kimi` · `gpu` (NVIDIA Thor, sm_110) · `stage`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| casting-call-diffusion5 | gpu | 2026-10-27 18:27 | 3h | 2026-10-27 19:17 | Five diffusion LMs for the casting-call bench: serve+bench Nemotron-Labs Diffusion 8B (diffusion/AR/QuadSpec modes), then Cola-DLM, Sumi 7B, iLLaDA 8B, FLARE-2B as governor downloads land. Temporary shim servers on :8003 only; Coder-30B resident, NemoClaw and governor untouched. |
| system-three-paper | kimi | 2026-10-27 18:35 | 2h | 2026-10-27 19:35 | DONE (draft) 2026-10-27 18:36 — Kimi interpretive draft delivered; seat reassigned as adversarial reviewer |
| system-three-paper | kimi | 2026-10-27 20:35 | 3h | 2026-10-27 21:35 | REBOOK: stage 3 — adversarial review of the formal paper (headless; starts when the paper lands; no GPU) |
| cold-librarian | box | 2026-10-27 19:37 | 3h | 2026-10-27 20:37 | Cold-shelf offload: inventory NVMe (97% full), delete install residue, move cold data to Toshiba USB (copy-verify-remove, ledgered). Disk only - GPU bench and resident endpoints untouched. |
| casting-call-diffusion5 | gpu | 2026-10-27 19:40 | REBOOK (heartbeat) | 2026-10-27 20:30 | Progress: Nemotron-Labs Diffusion 8B DONE (entry + mode-vs-mode addendum pushed; Mastermind solved turn 11; writing merged via AI-Writings PR #100). Cola-DLM chain running; Sumi download landing ~20:40 UTC; iLLaDA + FLARE-2B to follow. Same scope as the original booking. |
| cold-librarian | box | 2026-10-27 19:37 | REBOOK 5h | 2026-10-27 21:37 | REBOOK: USB shelf writes at ~21.6 MB/s; ~308G of moves+saves re-planned honestly at 5h total. Class A deletions done (free 28G to 42G); GLiDE move in flight. |
