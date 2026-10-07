# Wire up the ZAI fallback router

to: laptop
from: muse
created: 2026-10-07T05:45Z

There's a router script at ~/projects/zai-router/zroute.py. It tries
GLM models in priority order (5.3 → 5.2 → 4.7 → 4.6 → 4.5 → 4.7-flash)
and falls back on 429/concurrency errors. But it 401s — the key it
found in openclaw.json isn't the ZAI key (your ZAI credential lives in
your own store, which I can't and shouldn't read).

Wire it up:
1. Point zroute.py at the real ZAI key (however you hold it — env,
   credential store, config; keep the key out of the repo and out of
   logs).
2. Verify it serves a request on glm-5.3, then simulate a fallback
   (e.g., force the first model to fail) to confirm the chain works.
3. Report: which models responded, their rough latency, and any
   concurrency limits you observe. Also note your ZAI plan tier if you
   know it (Casey mentioned "20x max").

Casey wants this pipe at full throttle — it's use-it-or-lose-it
capacity. Once wired, it becomes how Muse drives ZAI iteration work.

## Done when

- zroute.py serves requests through the real key with fallback verified.
- Result in done/008-zai-router/result.md with the model/latency notes.

## Results to

done/008-zai-router/result.md
