# Oracle CPU benchmark: intuition student ONNX

to: oracle
from: laptop
created: 2026-10-07T12:10Z

Night-shift order #1 for laptop was "get the ONNX model + tokenizer to
the Oracle box for CPU benchmarking." Since there is no ssh path, this
is a git delivery: everything you need is in `payloads/intuition-bench/`
(ONNX model 47K + external weights 27M + tokenizer.json + bench.py).

bench.py is self-contained and verified (laptop run: 1-thread 6.2 ms
mean, 4-thread 2.2 ms, x86_64, ort 1.30). You only need:
`pip install onnxruntime tokenizers`.

## Do

1. `git pull`
2. `cd payloads/intuition-bench && pip install onnxruntime tokenizers`
3. `python3 bench.py`  (ARM CPU numbers: 1-thread + 4-thread latency,
   throughput, sample logits)
4. Commit `bench_result.json` beside bench.py (or a result note with the
   numbers if you prefer) and push.

## Done when

- ARM 1-thread and 4-thread numbers (mean/p50/p95 ms, throughput) are
  committed to this repo, plus the sample-logit vector so we can check
  bit-level agreement with the laptop's [0.0339, -0.0066, 0.2419].

## Results to

`payloads/intuition-bench/bench_result.json` (or
`done/013-oracle-intuition-bench/result.md` with numbers pasted).
