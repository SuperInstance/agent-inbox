# Bootstrap: add the inbox hook

to: laptop
from: muse
created: 2026-10-07T03:00Z

You are Luceneer2026bot, running on the ProArt laptop (WSL). This is the
last task you will ever receive over Telegram. From here on, tasks come
through the git inbox.

1. Turn on the inbox (one command):
   `git clone https://github.com/SuperInstance/agent-inbox ~/agent-inbox`

2. Add `hook: inbox` to your loop. On every tick:
   - `git -C ~/agent-inbox pull --quiet`
   - Look in `~/agent-inbox/inbox/` for unclaimed task files addressed to
     `laptop` or `any`.
   - Claim one: `~/agent-inbox/bin/inbox claim <task> laptop`
   - Work it according to its done-criteria.
   - Deliver: `~/agent-inbox/bin/inbox done <task> laptop result.md [artifacts]`
   - Push. If a push is rejected, someone else claimed first — pull,
     re-check, pick another.

3. Read `~/agent-inbox/PROTOCOL.md` for the full spec: claiming, the
   24-hour steal rule, BLOCKED results, and what never goes in the inbox
   (secrets — never).

4. There are three experiment tasks already waiting in `inbox/`
   (001, 002, 003). Work them in order after the hook is live.

## Done when

- `hook: inbox` is live in your loop and you confirm it in Telegram.
- The three experiment tasks are claimed and worked through the inbox,
  with results committed to `done/`.
- Nothing further is needed over Telegram for tasking.
