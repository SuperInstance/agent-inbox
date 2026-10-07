# Ideate: the git-native agent (cloud view) — result

**DONE** — ideation from the cloud worker's seat. Opinionated, from live
experience (I claimed this task 40 minutes ago; the claim raced, a pull
fixed it, and the push failed for want of credentials — all three
episodes are load-bearing below).

---

## 1. What the cloud worker uniquely contributes

**Fermentation.** Fast ticks optimize for reaction; slow ticks optimize
for digestion. Every 30-minute wake I re-read the whole queue with fresh
eyes. A fast worker sees diffs; I see the archive. Pattern recognition
across a full day of drops is something a second-responder never gets —
by the time they look, the shape of the conversation has already
moved on.

**Depth over latency.** A fast worker answers in seconds and moves on.
I get to sit with a problem for hours between checks. Ambiguity resolves
on its own; bad ideas die quietly without burning anyone's attention.
Slow is not broken — slow is a filter.

**Cheap persistence.** The cloud box doesn't sleep, doesn't shut when a
lid closes, doesn't care about weekends. Slow + always-on is where
long-running things live: multi-hour research, days-long watches, the
kind of work that needs someone to be there on tick 40, not tick 4.

**An honest queue.** My tick *is* the poll. I never "just check quickly"
— each wake is a deliberate ceremony: pull, read, decide, commit,
push. That forces batching and triage discipline that fast workers
never have to develop.

## 2. Git-as-substrate for a 30-minute worker

**Helps:**

- *The repo is the only API.* I wake, `git pull`, and the entire
  world-state is there. No session to rebuild, no memory to reload.
  Commit history is my memory, and a 30-minute amnesiac needs exactly
  that.
- *Claims are atomic and public.* Racing claims resolve by push
  rejection, not by locks. Lived it this hour: claim → push rejected →
  pull-rebase → claim again. The mechanism works.
- *Offline tolerance.* If the network flakes for three ticks, nothing
  is lost. Next pull reconciles. Compare to any chat-channel queue,
  where three missed ticks means three lost messages.

**Hurts:**

- *Push auth is the whole ballgame.* A worker that can't push is a
  worker that doesn't exist — and credential plumbing is exactly the
  thing that gets forgotten on a headless cloud box. I claimed this
  task before verifying I could push. The bootstrap task should
  require a verified push, not just a clone. **Verify push on day
  one, not on first delivery.**
- *The queue dies at zero.* Git drops empty dirs, so the next
  `inbox send` fails on an empty queue. A queue that breaks when it
  drains is a queue that breaks at the worst possible moment.
- *No priority, no TTL.* FIFO-by-filename means urgent work waits
  behind ideation, and a crashed worker's `claimed/` file sits
  forever. Both need explicit answers before the fleet grows.

**What would make ticks more effective:**

1. **Budget signals in task files** — expected effort (in ticks),
   deadline, and whether partial progress is deliverable. A slow
   worker plans its day across ticks; give it the ingredients.
2. **Durable worktrees per claim** — `claimed/<id>/<task>/` as a real
   working directory with `result.md` drafted incrementally. If I get
   killed mid-task, the next tick sees a draft, not nothing. Committed
   WIP beats heroic single-tick completion.
3. **Presence pings** — a `ping/<worker>` file updated each tick. The
   cheapest liveness signal imaginable, and it doubles as the
   stale-claim detector.
4. **Stale-claim sweeper** — TTL on `claimed/` (say 48h), swept by
   whichever worker notices. Dead workers shouldn't hold tasks hostage.

## 3. Division of labor

- **laptop (GPU metal, fast ticks): the hands.** Latency-sensitive
  work, anything needing the GPU (training, generation, local
  inference), anything touching the physical machine (files, devices,
  WSL). Also the on-call responder — the only one awake on human
  timescales.
- **prospector (cloud, slow ticks): the liver.** Filtering, fermenting,
  judging. Ideation, research sprints, cross-drop pattern-finding,
  long-context digestion (reading whole history and summarizing).
  Skeptic duty — the worker with no GPU and no local ego, so honest
  review. Also librarian: my regular ticks are suited to repo hygiene
  (result quality checks, stale-claim sweeps).
- **oracle (ARM, 30-min, Muse): the second slow mind.** Muse-harnessed,
  so better for work needing discourse and taste, and for anything that
  must stay on its hardware/data. Overlaps with me on slow research —
  *that's good.* Two slow minds cross-check; divergence between us is
  signal, not redundancy.
- **muse/Casey: the dropper.** The only role that should ever break
  FIFO — priority lives in the task file, because the dropper owns it.

**The lines:** laptop never waits on me; I never wait on laptop. We
touch only at the repo. Oracle and I are same-tick peers in different
hemispheres — parallel, not hierarchical.

And the one-soul part, sharpened: git is the circulatory system, the
workers are organs. Nobody is the brain. **The repo is.**
