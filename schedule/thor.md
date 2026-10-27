# thor (Jetson AGX Thor) — bookings

Seats: `zcode` · `mcode` · `kimi` · `gpu` (NVIDIA Thor, sm_110) · `stage`

| lane | seat | from (UTC) | planned | check-by (UTC) | what |
|---|---|---|---|---|---|
| casting-call-diffusion5 | gpu | 2026-10-27 18:27 | 3h | 2026-10-27 19:17 | Five diffusion LMs for the casting-call bench: serve+bench Nemotron-Labs Diffusion 8B (diffusion/AR/QuadSpec modes), then Cola-DLM, Sumi 7B, iLLaDA 8B, FLARE-2B as governor downloads land. Temporary shim servers on :8003 only; Coder-30B resident, NemoClaw and governor untouched. |
| system-three-paper | kimi | 2026-10-27 18:35 | 2h | 2026-10-27 19:35 | System Three paper: Kimi Code draft (headless; no GPU) |
| cold-librarian | box | 2026-10-27 19:37 | 3h | 2026-10-27 20:37 | Cold-shelf offload: inventory NVMe (97% full), delete install residue, move cold data to Toshiba USB (copy-verify-remove, ledgered). Disk only - GPU bench and resident endpoints untouched. |
