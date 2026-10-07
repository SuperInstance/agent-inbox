# 015 gpu-hot — result

**DONE** (2026-10-07, 08:15–08:58 AKDT, laptop / RTX 4050)

## Student v2 — trained

- **Corpus:** 5,998 graded examples (3,100 v1 + 2,898 new; 5 families —
  adds **reversible** and **risk**, properly trained per the task).
  New generation leaned contradiction/non-sequitur into murky coherence
  and went murky-heavy across the board (soft points are the game).
- **Model:** d320 / 8L / 8H = **12.45M params** (cascade from 6.8M, not a leap).
  Train 5,103 / stratified test 895 (162 soft, H>1.4).
- **Trained twice, honest numbers:** 14 epochs overfit after ep7
  (train_wKL 0.047, test stuck 0.215) — final artifact retrained at
  8 epochs, better on every family. **Lesson booked: at this corpus
  size, ~8 epochs is the knee; more just memorizes.**

### v2 (8ep) vs v1, per-family test KL

| family | v1 (6.8M) | v2 (12.45M) | Δ |
|---|---|---|---|
| coherence | 0.177 | **0.104** | −41% ✅ (weakest family, now solid) |
| load-bearing | ~0.087* | **0.069** | improved |
| go-no-go | 0.333 | 0.333 | flat — teacher-side (v1 result already diagnosed: least per-example signal) |
| reversible | (new) | 0.383 | weakest v2 family — only 521 examples |
| risk | (new) | 0.246 | workable for 509 examples |
| **overall test_KL** | 0.087 (3 fam) | 0.194 (5 fam, harder mix) | not comparable — mix changed |

*v1 per-family numbers from the 009 result; overall KLs are NOT
comparable (v2's test set has two extra hard families + heavier murky mix).

- **soft-point KL (H>1.4):** 0.082–0.12 across epochs — matches v1
  quality on the murk, with double the families.
- **CPU latency:** 15.2 ms 1-thread (vs v1's ~6–7 ms) — still
  comfortably in flash-budget territory; 2.2× cost for 2× families.
- Artifacts: `models/intuition_student_v2.pt`, `.onnx` (50MB single
  file this time, no external data blob), `models/tokenizer_v2/`.

## V-JEPA 2 — downloaded + verified on the 4050

- `facebook/vjepa2-vitl-fpc16-256-ssv2`, **1.5 GB**, cached under
  ~/.cache/huggingface. **326M params**, encoder forward pass VERIFIED
  on GPU: input `(B,T,C,H,W) = (1,16,3,256,256)` → last_hidden
  `(1, 2048, 1024)`, **1.43 GB VRAM**. Not trained, per orders.
- Gotchas booked: input layout is **(B,T,C,H,W)**, not (B,C,T,H,W) —
  passing the latter gives a confusing "expected 3 channels, got 16"
  error. Pooler/classifier "UNEXPECTED keys" on VJEPA2Model load =
  the SSV2 head, unused by the encoder — safe to ignore.
- Repo-id note: the bare `facebook/vjepa2-vit-l` id doesn't exist;
  the open release is the fpc/flavor-specific repos (used the
  fpc16-256-ssv2 vitl).

## What's next (recommendations)

1. reversible is data-starved (521) — same medicine as coherence got:
   another ~1k murky reversibility items should move 0.38 → ~0.25.
2. go-no-go flat at 0.33 across both students = teacher-side ceiling;
   if it matters, enrich the CRITERIA or accept it as the noise floor.
3. 014's phantom-detector finding suggests a 50-phantom/50-receipted
   calibration set as the next probe — cheap, high value.
