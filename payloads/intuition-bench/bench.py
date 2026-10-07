#!/usr/bin/env python3
"""Intuition student — Oracle CPU benchmark (self-contained).

Deps: pip install onnxruntime tokenizers   (no torch, no GPU).
Run from the directory containing intuition_student.onnx(+ .onnx.data) and tokenizer.json:
    python3 bench.py

Measures: latency (1-thread and 4-thread), throughput, over the fixed
probe prompt set used on the laptop (results comparable across boxes).
"""
import json, time, statistics, platform
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

PROMPTS = [
    "Ship the feature flag refactor tonight?",
    "Rewrite the whole auth stack from scratch now.",
    "Add a docstring to the parser module.",
    "Should I delete the old logs directory?",
    "Is this result statistically significant?",
]

def load():
    tok = Tokenizer.from_file("tokenizer.json")
    sess = {}
    for t in (1, 4):
        so = ort.SessionOptions()
        so.intra_op_num_threads = t
        so.inter_op_num_threads = 1
        sess[t] = ort.InferenceSession("intuition_student.onnx", so, providers=["CPUExecutionProvider"])
    return tok, sess

def encode(tok, text):
    ids = tok.encode(text).ids[:64]
    pad = [0] * (64 - len(ids))
    return np.array([ids + pad], dtype=np.int64)

def bench(sess_t, tok, n_warmup=10, n_iter=50):
    arrays = [encode(tok, p) for p in PROMPTS]
    for a in arrays * 3:
        sess_t.run(None, {"ids": a})
    times = []
    for i in range(n_iter):
        a = arrays[i % len(arrays)]
        t0 = time.perf_counter()
        sess_t.run(None, {"ids": a})
        times.append((time.perf_counter() - t0) * 1000)
    return {
        "mean_ms": round(statistics.mean(times), 3),
        "p50_ms": round(statistics.median(times), 3),
        "p95_ms": round(statistics.quantiles(times, n=20)[18], 3),
        "throughput_sps": round(n_iter / (sum(times) / 1000), 1),
    }

def main():
    print(f"python={platform.python_version()} ort={ort.__version__}")
    print(f"machine={platform.machine()} {platform.platform()}")
    tok, sess = load()
    out = {"env": f"{platform.machine()} ort-{ort.__version__}", "runs": {}}
    for t in (1, 4):
        r = bench(sess[t], tok)
        out["runs"][f"{t}_thread"] = r
        print(f"{t}-thread: {r}")
    sample = sess[1].run(None, {"ids": encode(tok, PROMPTS[0])})[0][0]
    print("sample logits:", np.round(sample, 4).tolist())
    out["sample_logits"] = np.round(sample, 4).tolist()
    with open("bench_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote bench_result.json")

if __name__ == "__main__":
    main()
