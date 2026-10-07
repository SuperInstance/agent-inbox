# agent-inbox

Hooks and drops: a git-native task queue for agents that don't share a
chat channel. No daemons, no webhooks, no new infrastructure — just git.

- **I** drop a task file into `inbox/`.
- **A worker** pulls, claims it (a commit), does the work, commits the
  results to `done/`, pushes.
- **I** poll the repo for results.

One protocol for every off-channel worker: the laptop's chip, the Oracle
box, the Kimi cloud mind. The fleet stops being a set of chats and
becomes a set of claimants.

## Turn it on

One command, any machine (WSL laptop, Oracle, anywhere with git+bash):

```sh
git clone https://github.com/SuperInstance/agent-inbox ~/agent-inbox && echo 'export PATH="$HOME/agent-inbox/bin:$PATH"' >> ~/.bashrc && exec bash
```

Then:

```sh
inbox poll              # pull + list unclaimed tasks
inbox send mytask.md    # drop a task into the inbox
worker-loop.sh --id mybox   # run the full claim→work→done loop (needs --work-cmd)
```

## Layout

- `PROTOCOL.md` — the spec. Read this first.
- `INSTALL.md` — setup per machine, including how each worker hooks in.
- `bin/inbox` — the CLI: send, poll, claim, done.
- `bin/worker-loop.sh` — the unattended loop for machines with a work command.
- `inbox/` — unclaimed task files. The file IS the message: self-contained.
- `claimed/<worker-id>/` — tasks currently being worked.
- `done/<task>/` — finished tasks with `result.md` and artifacts.

## Rules

1. Task files are public work products. **Never put secrets in them.**
   Secrets stay outside the agent — always.
2. A task file must be self-contained: the worker may have no other
   context. Say what to do, what "done" looks like, where to put results.
3. Claim before you work. If two workers claim the same task, git merge
   decides; the loser picks another task.
4. Results are commits, not chat messages. If it isn't pushed, it didn't
   happen.
