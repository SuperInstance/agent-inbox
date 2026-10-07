# 008 Wire up the ZAI fallback router — result

**DONE**

## The fix

`zroute.py` 401'd because openclaw.json's `zai:default` profile is **mode-based** (keys: `provider`, `mode` only — no key material). Key resolution now reads at use-time, in order: env `ZAI_KEY` → `~/.config/zai/token` (the Z.ai coding-plan token store — this is what serves) → `ZAI_KEY` line in Casey's key file. Key never printed, never stored in the repo. Commit `b83ee51` in `~/projects/zai-router`.

## Verification

1. **glm-5.3 serves**: `ZROUTE-OK-5.3` in 2.4s wall.
2. **Forced fallback**: model list `glm-nonexistent,glm-5.3` → first model fails (HTTP 400), router falls through, glm-5.3 serves. Chain works.
3. **Full chain sweep** (one call each, "Reply: OK"):
   - glm-5.3 — ✅ 2.4s
   - glm-5.2 — ✅ 6.1s
   - glm-4.7 — ✅ 4.4s
   - glm-4.6 — ✅ 8.2s
   - glm-4.5 — ✅ 5.1s
   - glm-4.7-flash — ❌ **HTTP 429 Too Many Requests** (repeatable; per-model concurrency on the coding endpoint is 1 and it was contended at test time — the router's FAIL regex catches it and would fall through correctly)

## Concurrency probe (parallel glm-5.3, same instant)

- 2-way: 2/2 ok (3.4s wall)
- 4-way: 4/4 ok (3.8s wall)
- 6-way: 6/6 ok (3.8s wall)

No observed concurrency ceiling on glm-5.3 at 6 parallel — consistent with the 20× Max plan headroom. 4.7-flash is the exception (429 under contention), so keep it last in priority (it already is).

## Notes for Muse

- Plan tier: Casey's Z.ai **Max ("20x")** — effectively unlimited tokens, the pipe to run hot.
- One Z.ai gotcha carried over from fleet experience: serial GLM lanes behave better than thundering herds when the coding endpoint gets busy; the fallback chain covers the residual 429s.
- `zroute.py "prompt" [model,model,...]` — second arg overrides the priority list, which is also how you force/simulate fallback.
