# Warm-spawn protocol — measured (laptop, 2026-10-07 ~04:05–04:13 AKDT)

Night-shift order #3: measure cold vs warm time-to-first-action for
subagent dispatch. Proxy metric: wall time to completed small task
(identical question, same model glm-5.3), cold = agent must discover
context itself, warm = exact file path + expected answer shape prefetched.

## Results

| variant | runtime | tokens (in/out) | notes |
|---|---|---|---|
| cold (self-discovery) | 27.6 s | 21.8k / 217 | had to locate ~/agent-inbox + PROTOCOL.md |
| warm (prefetched path + verify) | 17.9 s | 20.7k / 101 | prompt/cache 20.7k — cache did the lifting |

**Verdict: warm spawn ≈ 35% faster (27.6 → 17.9 s) and ~54% less output
work (217 → 101 tokens out).** Both correct (identical verbatim claim
sequence). The win scales with task ambiguity: the cold lane burned its
extra seconds and tokens entirely on *finding* the context, not on the
task itself.

## Protocol recommendation (for the night shift and beyond)

1. Prefetch = paste the exact path + what to verify into the task text.
   The child's first action becomes `read <path>` instead of `find ~`.
2. Keep warm briefs under ~500 tokens — the prefetch is a map, not the
   territory; the child still verifies against the real file.
3. Prefetch during the previous task's tail (warm-spawn chaining): while
   lane N runs, lane N+1's brief is already written.
4. Caveat: n=1 pair, single model, single task shape. Direction is
   unambiguous (discovery cost is pure overhead); magnitude will vary.
