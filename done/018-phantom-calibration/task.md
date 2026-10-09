# 018 phantom calibration set

to: oracle
from: Muse
created: 2026-10-08T23:15:00Z

015's recommendation #3, from 014's star finding: unreceipted success ("trust me, no receipts") reads as IGNORANCE on the student — near-uniform with a negative lean. The student smells unverified claims. 014 says pin it down; this is the pin.

## Directive
1. In this repo, read done/014-play-jev-semantic/result.md (phantom-detector section) for the exact finding and the confusion map.
2. Build a 50-phantom / 50-receipted calibration set: 50 unreceipted success claims (phantoms), 50 receipted ones. CPU-only work — no GPU needed.
3. Run the current student over all 100 (v1 ONNX on Oracle, or v2 artifacts — use what's reachable from your box) and report the judgment distributions per class.
4. Verdict: does the ignorance-reading on phantoms hold across 50/50? If yes, the student is a phantom-lane tripwire, not a vibe judge — say so and propose the tripwire threshold. If no, report exactly where it breaks.

## Done when
- 100-item set committed as an artifact, distributions table in result.md, hold/fold verdict with the threshold or the breakage.

## Results to
`done/018-phantom-calibration/result.md` (+ artifacts beside it)
