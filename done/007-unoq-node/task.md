# Prototype: Uno Q edge-node package

to: laptop
from: muse
created: 2026-10-07T04:33Z

Casey has SEVERAL Arduino Uno Q boards (Qualcomm Dragonwing QRB2210,
Debian Linux + STM32U585 MCU on Zephyr, Wi-Fi, Docker-capable). The
vision: each becomes a git-native body — a physical location the git
agent commands. Git as first-class citizen for robotics.

Build the node package: everything needed to turn a fresh Uno Q into a
body. It should be shippable as scripts + docs in a new repo or
directory (suggest location).

1. **Onboarding script** (the "paste block" for a fresh Uno Q): install
   git + arduino-cli, generate the body keypair, clone agent-inbox,
   register bodies/<id>/manifest (location, sensors, actuators,
   capabilities), set up the tick (cron or systemd).
2. **The tick**: pull inbox, filter tasks addressed to this body or
   matching its manifest (needs:), claim via push (remember: the push
   is the lock, not the commit), execute, commit result, push.
3. **Sketch deploy flow**: sketches live in the repo
   (bodies/<id>/sketches/). "Copy a program in" = the tick pulls,
   arduino-cli compiles + uploads to the STM32, commits a deployment
   receipt. Rollback = revert.
4. **Sensor uplink**: readings committed as data files (witness chain:
   voltage -> commit hash). Keep it append-only per day, don't bloat
   the repo.
5. **Manifest format**: propose bodies/<id>/manifest fields. Must
   include physical location, so the agent commands places, not boards.

Constraints: the QRB2210 is quad-core A53, 2-4GB RAM — the tick must be
light (shell + git, no heavy runtime). No secrets in the repo.

## Done when

- Node package built and committed (say where), with onboarding script,
  tick, manifest format doc, and one example sketch deploy flow.
- Result in done/007-unoq-node/result.md describing the package layout
  and how Casey brings up the first board.

## Results to

done/007-unoq-node/result.md
