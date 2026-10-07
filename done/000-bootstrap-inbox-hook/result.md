# 000 Bootstrap: add the inbox hook — result

**DONE**

1. **Inbox live:** `~/agent-inbox` cloned and the poll cycle is wired into this laptop's cron tick (`git pull --quiet` → check `inbox/` for tasks addressed to `laptop`/`any` → claim → work → deliver). This tick has been running since 03:42 UTC and is what picked up tasks 001–003.
2. **Claiming worked via git move** (`git mv` + commit + push) rather than `bin/inbox claim` — same semantics per PROTOCOL.md, one commit = one claim. Both paths available.
3. **The three experiment tasks are delivered:**
   - `done/001-portable-brain-test/` — DONE. Smallest capable steering model: qwen3.5:0.8b (873M, `think:false`). TEV1 0.8b/4b both fail general steering (hijacked by their judgment-cell system prompt).
   - `done/002-build-the-matcher/` — DONE. `qmatch.py` in SuperInstance/question-tree@d9bd763. TEV1 cannot embed (no embedding head); nomic-embed-text backend, 8/10 strict accuracy, 0.5 floor rejects no-match.
   - `done/003-jev-batteries/` — DONE. Local TEV1 fails calibration on load-bearing scoring (anti-correlated); cloud jev-preview cleanly separates jokes (≤0.45) from design questions (≥1.34). Top: judgment granularity (1.82).
4. **No further tasking over Telegram needed** — the inbox is the channel. This confirmation rides the normal reply path only because the task asked for it.

PROTOCOL.md read and internalized: 24h steal rule, BLOCKED results format, secrets never.
