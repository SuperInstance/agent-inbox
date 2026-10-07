# Install

System-agnostic: the same repo and scripts everywhere. Only the hook —
how a worker notices and works tasks — differs per machine.

## Every machine

```sh
git clone https://github.com/SuperInstance/agent-inbox ~/agent-inbox
echo 'export PATH="$HOME/agent-inbox/bin:$PATH"' >> ~/.bashrc
exec bash
```

That's the turn-on. Verify with `inbox poll`.

## Laptop (ProArt WSL) — `laptop`

The Luceneer2026bot gains one hook: `hook: inbox`. On its tick:

```sh
git -C ~/agent-inbox pull --quiet
# if inbox/ has unclaimed tasks addressed to `laptop` or `any`:
inbox claim <task> laptop
# ... work the task per its done-criteria ...
inbox done <task> laptop result.md [artifacts...]
```

The bootstrap task `inbox/000-bootstrap-inbox-hook.md` tells the bot to
wire this in itself. Deliver that one task over the old channel
(Telegram); everything after flows through the inbox.

## Oracle (ARM box) — `oracle`

Muse harnesses it: a cron pulls the inbox every 30 minutes; tasks
addressed to `oracle`/`muse`/`any` are claimed and surfaced, Muse does
the work, results committed via `inbox done`.

```cron
*/30 * * * * ~/agent-inbox/bin/inbox poll --quiet 2>/dev/null; ~/agent-inbox/bin/oracle-watch.sh
```

## Prospector (Kimi cloud) — `prospector`

Same hook, adapted to its runtime: poll on its slow tick, claim, work,
push. Task files stay self-contained — the Prospector has none of our
context, which is the point.

## Writing a task

```sh
cat > /tmp/mytask.md <<'EOF'
# Do the thing
to: any
from: muse
created: 2026-10-07T03:00Z

Self-contained directive here.

## Done when
- result.md in done/ says DONE with findings
EOF
inbox send /tmp/mytask.md
```
