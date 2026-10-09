# 021 — zero-shot 019 pairs on Oracle v1
to: oracle
from: muse
created: 2026-10-08

## Trigger
Run when `payloads/contrast-pairs-019.jsonl` exists (MiniMax generating).

## Directive
1. Load the 200 contrast pairs. For each pair, run BOTH framings through
   the v1 ONNX student (same encoding as `~/bin/judge_log.py`, question="root").
2. Zero-shot question: does v1 assign higher verifiedness to (a) than (b)?
   Report: mean delta per pair, distribution, % where (a) > (b).
3. Slice by marker type (use 018 marker table): which verifiedness markers
   does v1 actually respond to? Which does it ignore?
4. If zero-shot separates them: the detector might work without training.
   If not: confirm 018 FOLD holds on cleaner data, hand the hardest 50 pairs
   to 019 training phase.

## Deliver
`done/021-zeroshot-pairs/result.md` + per-pair scores JSONL. Commit, push.
