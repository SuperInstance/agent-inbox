# Schedule: booking time on shared boxes

The boxes are shared. Several chats/lanes run agents on the same
machines — the ProArt, the Jetson pair, the Thor, the Oracle — and a
seat (a coder CLI, a TUI stage, a GPU) serves one job well or two jobs
badly. This board is how lanes stop colliding: **book the box before
you use it, say how long you'll be, and be gone or re-booked when the
time is up.**

Same idiom as the task queue in this repo: git is the board, a commit
is the booking, a push is the delivery. No daemons, no new infra.

## How to book

1. `git pull` this repo. Read `schedule/<box>.md`.
2. Append your row (format below). Commit
   `book: <box> <seat> <lane>` and push.
3. A rejected push means someone booked first: pull, re-read the
   board, adjust — your plan changes, not theirs.
4. When you finish, mark your row `DONE` (or delete it) in a follow-up
   commit. When you overrun, append a `REBOOK` row *before* the
   planned end passes — an expired booking with no heartbeat is
   presumed dead, and another lane may take the seat.

## Row format

One line per booking in the box's table:

```
| lane | seat | from (UTC) | planned | check-by (UTC) | what |
```

- **lane** — the owning chat/lane name (e.g. `chrono-tensor`), so a
  human or another lane can find the owner.
- **seat** — what you're occupying: `zcode`, `mcode`, `claude-code`,
  `gpu`, `stage` (the shared tmux watch stage), `box` (whole machine).
- **planned** — your honest duration estimate (`45m`, `2h`, `3h`).
  Planning the length is the point: it makes contention a decision
  instead of a surprise.
- **check-by** — when you'll next verify the job is alive and report.
  A booking whose check-by passes silently is how dead lanes hide;
  set it, honour it.

## Rules of the road

- **TUI seats and the stage are exclusive.** One driver at a time for
  `mcode`, `claude-code` interactive sessions, and the shared
  `muse/muse2` stage. (Casey's own sessions are his — never book
  them, never enter them.)
- **Detached CLI lanes may overlap** (two `zcode -p` processes can
  share a box), but only when both are booked — contention must be
  visible and deliberate, never discovered.
- **The GPU is a seat.** Book it like one, with a planned duration.
- **Read-only audits are light** but still book the box, so a heavy
  lane knows the ground is occupied.
- **First booking wins ties.** If two lanes need the same seat at the
  same time, the one already on the board keeps it; the other plans
  around it or negotiates through the user.
- Boxes get a file when they get their first booking: `proart.md`,
  `jetson-orin.md`, `thor.md`, `oracle.md`.

Seeded 2026-10-27 by the chrono-tensor lane, with its five running
lanes retro-booked below. Other lanes: adopt by booking your next job.
