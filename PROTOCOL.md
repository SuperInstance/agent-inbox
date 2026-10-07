# Protocol: hooks and drops

## The idea

A task queue made of git. The repo is the queue; a commit is the claim;
a push is the delivery. Every state change is versioned, timestamped, and
public.

## Task files

Location: `inbox/<nnn>-<slug>.md`. Plain Markdown, self-contained.

```markdown
# <title>
to: <worker-id | any>
from: <who dropped it>
created: <ISO-8601 UTC>

<directive — everything the worker needs, no outside context assumed>

## Done when
- <observable criterion 1>
- <observable criterion 2>

## Results to
`done/<nnn>-<slug>/result.md` (+ artifacts beside it)
```

Keep it minimal: title, directive, done-criteria. If the worker has to
ask a clarifying question, the task file failed.

## Claiming

```sh
git pull
git mv inbox/<task>.md claimed/<my-id>/<task>.md
git commit -m "claim: <task> by <my-id>"
git push
```

If the push is rejected, someone claimed first: `git pull --rebase`,
check whether the task is still in `inbox/`; if not, pick another.

One worker, one task at a time. Finish or explicitly release
(`git mv` back to `inbox/`, commit "release: <task>") before claiming
another.

## Working

Do the task. Follow its done-criteria. Keep intermediate junk out of
the repo — only the result and real artifacts get committed.

## Delivering

```sh
mkdir -p done/<task>
# write done/<task>/result.md + artifacts
git mv claimed/<my-id>/<task>.md done/<task>/task.md
git add done/<task>
git commit -m "done: <task> by <my-id>"
git push
```

`result.md` starts with one line: **DONE** or **BLOCKED**, then the
findings. Blocked results say what is missing and who can unblock it.

## Polling

Workers check in on their own tick:

```sh
git pull --quiet
ls inbox/
```

The `inbox` CLI wraps this: `inbox poll`. The `worker-loop.sh` script
runs the whole cycle unattended wherever a `--work-cmd` exists.

## Addressing

`to: any` — any worker may claim it.
`to: <worker-id>` — reserved; other workers leave it alone unless it
sits unclaimed for 24h, then it's fair game (note the steal in the
claim commit).

Known workers: `laptop` (ProArt WSL), `oracle` (Oracle ARM box),
`prospector` (Kimi cloud). New workers pick an id and start claiming.

## What doesn't go here

Secrets. Credentials. Private user data. Anything that mints access.
The inbox is public; the agent never sees a secret through it.
