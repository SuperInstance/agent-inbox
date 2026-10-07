# 011 Build the spreader harness — result

**DONE**

## Where it lives

`~/projects/spread/spread.py` (git repo, commits `592a15d` + show-fix). Reuses the verified zai-router key path (from task 008) — no key duplication, no key in repo/logs.

## Save-state format (JSON, content-addressed)

```json
{"name": "...", "model": "glm-5.3", "system_prompt": "...",
 "history": [ {"role": "user", "content": "..."} ],
 "params": {"temperature": 0.9, "top_p": 0.95, "max_tokens": 1600},
 "timestamp": "..."}
```

Hash = sha256 of everything **except seed and timestamp** — the hash names the reproducible container; `spread run` stamps per-seed variants. `spread save` writes to `saves/<hash16>.json`.

## Commands

- `spread run --from <state.json> --n 5 --vary seed [--models m1,m2] [--seed0 1]`
- `spread list <run-id>` / `spread show <run-id>/<i>` / `spread diff <run-id>/<i> <run-id>/<j>`
- `--vary model` is wired (round-robins across the models list); nugget-mining (surprise vs median, convergence detection) is v2 as specced.
- Every run dir carries `state.json` (the questions — committed, not just outputs), `MANIFEST.json`, `outputs/000.json...` (content, seed, model served, latency, usage).

## Demo run (the deliverable evidence)

Run `20261006-233100-bafd4b`: one save state, 5 seeds, glm-5.3, 6–18s per shot. Question: *"the most under-appreciated failure mode of a discriminator/builder loop where the builder sees its past scores?"*

- seed 1: **co-adaptation** — builder optimizes the judge's quirks
- seed 2: **judge capture** — held-out judge decides advancement
- seed 3: **score visibility makes the judge a searchable oracle** — rotate judges per round
- seed 4: **co-evolution; score history is a side channel** — frozen reference items
- seed 5: **private language; scores measure mutual drift** — anchor the scale with known-quality items

**The nugget, surfaced the way the harness intends:** all five seeds independently converge on *judge-gaming/co-adaptation* as the failure (that's the load-bearing answer — five independent draws agreeing), while each contributes a distinct frame and a distinct fix (held-out judge, judge rotation, frozen anchors). The convergence names the truth; the spread is what Casey pans for gold.

## Gotchas learned (now baked in)

- glm-5.3 burns hidden reasoning tokens against the `max_tokens` budget — 300 tokens yielded empty content (298 reasoning). Demo uses 1600; fallback reads `reasoning_content` if `content` is empty.
- The task-008 key lesson repeated: never hand-copy auth headers from redacted file views (`***` → `Bearer `).

## v2 queue

- `--vary model` parallax runs (glm-5.3 vs 5.2 vs minimax on identical states)
- nugget mining: median-embedding distance for surprise, seed-agreement detection for convergence, Jev field-scoring per task 003's calibrated path
