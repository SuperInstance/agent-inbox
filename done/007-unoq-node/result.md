# 007 Uno Q edge-node package — result

**DONE**

## Where it lives

**https://github.com/SuperInstance/unoq-node** (new SuperInstance repo, main @ `edbe49d`, push verified via ls-remote). Local working copy: `~/unoq-node`.

## Package layout

- `onboard.sh` — the paste block for a fresh board: installs git + jq + arduino-cli (STM32 core), generates the body keypair (key never enters any repo; pubkey printed for a deploy key), clones agent-inbox + unoq-node, registers `bodies/<id>/manifest`, writes the `BODY` identity file, installs the tick as a systemd user timer (2 min). Dash-safe (learned the hard way: `<<<` is a bash-ism, first push of onboard.sh was the only syntax casualty).
- `bin/tick.sh` — the heartbeat. sh + git only, sized for A53/2GB. Pull → filter (`to: <id>` / `to: any` + `needs:` capability match against the manifest's CAPABILITIES) → claim **by push** (lost races reset+rebase cleanly) → `run-task.sh` → push. Ends with the daily append-only witness commit in the node repo.
- `bin/run-task.sh` — executes a `deploy:` line (sketch flow) or a ` ```run ` fenced block; books DONE/BLOCKED to `done/<task>/result.md`.
- `bin/deploy.sh` — arduino-cli compile + upload to the STM32U585, receipt with sketch commit hash + previous deploy commit + rollback instructions. Deployments are commits; rollback = revert + redeploy.
- `bodies/<id>/manifest` — shell-sourcable KEY=VALUE (no parser on 2GB RAM). Keyed on **LOCATION first** — the agent commands places, not boards. Fields documented in `docs/MANIFEST.md`.
- `bodies/q1/` — a ready example body (manifest + blink sketch + uplink dir).
- `examples/blink-q1-task.md` — the exact smoke-test task to drop into agent-inbox.
- `docs/DEPLOY.md` — deploy flow + sensor-uplink rules (append-only daily, archive-never-delete, high-rate data stays in a local spool — repo is the ledger, not the payload).

## Bringing up the first board

1. Boot the Uno Q, ssh in.
2. `sh <(curl -fsSL https://raw.githubusercontent.com/SuperInstance/unoq-node/main/onboard.sh) --id q1 --location "lab-bench"`
3. Add the printed pubkey as read/write deploy key on agent-inbox + unoq-node.
4. Edit `bodies/q1/manifest` census; set `ARDUINO_FQBN`/`ARDUINO_PORT` in the systemd unit once the board variant is confirmed.
5. Drop the example blink task into the inbox; watch `journalctl --user -u unoq-tick.service -f`. Receipt lands in `done/` within one tick (2 min).

## Notes / open items for the first real board

- FQBN default is a placeholder (`STMicroelectronics:stm32:GenG0`) — must be pinned to the actual Uno Q board variant on first boot; one-line env change.
- Claiming uses plain `git mv` + commit + push per PROTOCOL.md; the tick tolerates races (reset + rebase) and offline ticks (quiet exit).
- No secrets in either repo, per protocol; the deploy key is the only credential and it lives on the board.
