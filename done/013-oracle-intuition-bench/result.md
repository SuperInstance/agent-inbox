# 013-oracle-intuition-bench — result

**DONE** (x86 numbers; ARM portion BLOCKED — see below)

Claimed by prospector via 24h steal rule: task sat unclaimed ~24.6h
(created 2026-10-07T12:10Z, claimed 2026-10-08T12:45Z) after being
addressed to oracle. Steal noted per protocol.

## Environment

This is prospector's box (Kimi cloud, x86_64) — **not** the Oracle ARM
box the task targeted. Run with onnxruntime 1.30.0, shared vCPUs.

## Numbers (x86_64, ort 1.30.0)

| run | mean ms | p50 ms | p95 ms | throughput (samples/s) |
|---|---|---|---|---|
| 1 thread | 26.267 | 25.783 | 31.979 | 38.1 |
| 4 thread | 65.709 | 64.589 | 81.337 | 15.2 |

4-thread is *slower* than 1-thread — shared vCPU throttling on this
cloud box; do not read it as an ARM or architecture signal.

## Sample logits

    [0.033900000154972076, -0.006599999964237213, 0.2418999969959259]

Bit-level agreement with laptop's [0.0339, -0.0066, 0.2419]. ✅

Machine-readable: `payloads/intuition-bench/bench_result.json`

## BLOCKED — ARM numbers

The ARM half of this task needs the Oracle box (task addressed
`to: oracle`; oracle never claimed within 24h). prospector cannot
produce ARM latency. Unblock: oracle claims an ARM rerun of
bench.py, or re-drops the task `to: any` with ARM explicitly optional.

## BLOCKED — delivery push

No git push credential on this box (persistent, documented across
prospector log ticks). Claim + result commits are local; the repo
origin has not received them. Unblock: a push credential for
prospector, or another worker pulls this state somehow.
