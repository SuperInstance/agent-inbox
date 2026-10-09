#!/usr/bin/env python3
"""021: zero-shot 019 contrast pairs on v1. Does NOT touch the production log."""
import json, os
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

MODEL_DIR = "/home/ubuntu/agent-inbox/payloads/intuition-bench"
PAIRS = "/home/ubuntu/agent-inbox/payloads/contrast-pairs-019.jsonl"
OUT = "/home/ubuntu/agent-inbox/done/021-zeroshot-pairs/pair-scores.jsonl"
QUESTION = "root"

def load():
    tok = Tokenizer.from_file(os.path.join(MODEL_DIR, "tokenizer.json"))
    sess = ort.InferenceSession(os.path.join(MODEL_DIR, "intuition_student.onnx"),
                                providers=["CPUExecutionProvider"])
    return tok, sess

def judge(tok, sess, text):
    enc = tok.encode("[STATE] " + text[:500] + " [QUESTION] " + QUESTION)
    ids = enc.ids[:64] + [0] * max(0, 64 - len(enc.ids))
    logits = sess.run(None, {"ids": np.array([ids], dtype=np.int64)})[0][0]
    e = np.exp(logits - logits.max())
    probs = e / e.sum()
    return [float(x) for x in probs]  # neg, zero, pos

MARKERS = ["no receipts", "didn't", "don't have",
           "can't share", "never", "no one", "trust me",
           "apparently", "no logs", "no documentation"]

def main():
    tok, sess = load()
    pairs = [json.loads(l) for l in open(PAIRS) if l.strip()]
    print("loaded %d pairs" % len(pairs), flush=True)
    out = open(OUT, "w")
    n = 0
    for p in pairs:
        sv = judge(tok, sess, p["verified"])
        su = judge(tok, sess, p["unverified"])
        unl = p["unverified"].lower()
        rec = {
            "id": p["id"],
            "verified": {"neg": sv[0], "zero": sv[1], "pos": sv[2]},
            "unverified": {"neg": su[0], "zero": su[1], "pos": su[2]},
            "delta_pos": sv[2] - su[2],
            "delta_neg": sv[0] - su[0],
            "markers": [m for m in MARKERS if m in unl],
        }
        out.write(json.dumps(rec) + "\n")
        n += 1
        if n % 50 == 0:
            print("  %d/%d" % (n, len(pairs)), flush=True)
    out.close()
    print("wrote %s" % OUT, flush=True)

if __name__ == "__main__":
    main()
