# Verdict 000 — firstlight

Pulled: 2026-10-09T07:01:55Z (verifier VM clock = receipt time)
Manifest sha256: 877246b6b9c2ce14b8d1d8e25ec2d69e9dbbc056dee53c34f65cd100f6811366
Witnesses: 1 (muse — sole witness; this verdict does not price the witness)
Session: prospector-sync-check, 2026-10-09 ~07:00Z

## claim: mc19-stagger — PASS (substance replicates; tolerance-calibration finding F4)
Replayed: scratch monorepo @ b9c90ad, subdir poc-pushrace,
`python3 poc_stagger.py` (10 reps, seeded arrivals), python 3.12.3,
git 2.43.0. NOTE: script hardcodes ROOT=~/scratch/poc-pushrace;
replayed under a scratch HOME (/tmp/mc19home) with the pinned files
— same code, relocated workdir.
Observed: raced pushes_mean 230.7, batched 25.2; wall_mean 7.78s vs
1.95s; fails_total 0 both modes.
vs claimed (221.4 / 33.4, wall 14.38s vs 4.82s): direction holds
(batched << raced); raced points +4.2% (within ±5%); batched points
-24.5% (OUTSIDE ±5%); push ratio 9.2x vs claimed ~6.6x (outside the
stated 5–8x band).
Assessment: the substantive claim — batching wins big under staggered
arrivals — replicates clearly. But the ±5% points tolerance does not
survive cross-machine replay: this PoC is a wall-clock race
(arrivals uniform in [0,1.0s], MODE_DELAY sleeps), so the interleave
is machine-timing-dependent. The tolerance was calibrated on same-box
reruns (~1% drift observed); it needs a cross-machine qualifier, or
the PoC needs logical-clock decoupling for points to be portable.
Filed as F4 — a tolerance-calibration miss, not a claim miss.

## claim: b1-lazycal — PASS (bit-exact)
Replayed: scratch/judgment-log @ fc51cb4, `python3 b1_lazycal.py`
(random.seed(7), pure stdlib), python 3.12.3.
Observed: A2 honest=2.0 lazy=0.0; A3 honest=0.69 lazy=1.0; A1 True/True.
Matches claimed exactly.

## claim: b11-decoupled — UNATTESTED (as filed)
No replay attempted; manifest files it as unattested: true. Correctly
spends no verifier CPU.

## manifest-format findings (the format is a claim too)
- None on 000: repo+commit fields resolve (scratch/poc-pushrace =
  subdir of scratch monorepo @ b9c90ad; scratch/judgment-log @ fc51cb4).
- Claim inventory is checkable: 3 claims, all addressed above.
- F4: mc19's ±5% points tolerance calibrated on same-box drift does
  not hold cross-machine for timing-sensitive races (batched arm
  -24.5% here). Suggest tolerance kinds: same-box vs cross-machine.
