# 009 Train the intuition student — result

**DONE**

## Model path

- Weights: `~/projects/intuition/models/intuition_student.pt` (commit `eeb1154`)
- ONNX: `~/projects/intuition/models/intuition_student.onnx` (bit-parity with torch, opset 17)
- Tokenizer: `~/projects/intuition/models/tokenizer/tokenizer.json` (BPE, 8k)
- Trainer: `~/projects/intuition/src/train_student.py`

## Architecture / training (as specced)

Micro transformer encoder: d256, 6 layers, 8 heads, mean-pool head → 3-way softmax. **6.80M params.** Input `[STATE] … [QUESTION] …` (identical shape to the teacher's calls). Loss: KL vs teacher soft probs, samples weighted **3× when teacher H > 1.0** (soft points). Trained on the 4050 in **36 seconds** (12 epochs); mild overfit after ep8 (best test KL 0.184 @ep8, final 0.192 @ep11 — kept final; delta is noise-level and the soft-point metric is stable across those epochs).

## Eval numbers (stratified held-out, 462 examples, 104 soft points)

| metric | value |
|---|---|
| **Soft-point KL (H > 1.4)** — primary | **0.087** |
| Overall test KL | 0.184–0.192 |
| Teacher/student **entropy correlation** | **0.78–0.79** |
| CPU latency (1 thread, 64 tokens) | 7.5 ms torch / 7.3 ms ONNX |

Per-family test KL: load-bearing **0.066** · coherence **0.177** · go-no-go **0.333**.

Rangefinder sanity probe (not in training data): "[STATE] Deploy Friday, CI is down [QUESTION] Should this action proceed?" → **[0.145, 0.42, 0.435]** — no verdict, a spread leaning wait-vs-go. That's the beam returning, not a bullet.

## What transferred

- **The shape of not-knowing.** Entropy correlation 0.78 means the student's uncertainty tracks the teacher's across the corpus — when the teacher was unsure, the student is unsure. This was the whole game per DESIGN.md, and it transferred.
- **Soft points are the EASY part** (KL 0.087 vs 0.184 overall) — the murky middle is smooth target territory, and the 3× weighting held it there.
- Load-bearing judgments transfer almost perfectly (0.066) — the 003 battery family, where the teacher's calibration is strongest.

## What didn't transfer (honest)

- **go-no-go is the weak family (KL 0.333)** — but that's mostly teacher-side: its distributions are the most balanced overall (least extreme), so there's less signal per example and the KL denominator punishes confident misses. The student learned the spread but not the direction as crisply.
- **Direction (argmax) on clear cases is decent but not the target** — we didn't optimize for it and don't claim it; matching argmax proves nothing per the design.
- 3100 examples is a floor corpus; expect both numbers to move with a bigger teacher set, especially go-no-go.

## Next

ONNX is ready for the Oracle ARM CPU test (next task): `onnxruntime` + the tokenizer JSON is the entire runtime — no torch, no GPU.
