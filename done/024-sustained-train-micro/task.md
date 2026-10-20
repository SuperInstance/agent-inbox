# Sustained GPU training run — first long burn
to: laptop
from: main-lane (Casey: keep using the GPU, 2026-10-14)
created: 2026-10-15T03:20:00Z
resident: proart-gpu
kind: train-micro
steps: 20000
seed: 20261014

Run this only if you are the ProArt resident loop installed on the laptop /
ProArt WSL. Remain inside the existing ~/ml environment; do not download
models, packages, or data.

## Directive

Run one sustained train-micro cycle of 20,000 training steps on the
resident Markov curriculum, on CUDA. This is the box's first long burn:
the point is a real loss curve over real time, checkpointed as usual, with
wall time and final gap above the exact Bayes floor reported in the result.

## Done when
- result.md in done/024-sustained-train-micro/ records: device, steps run,
  wall seconds, first loss, final loss, exact Bayes floor, gap above floor,
  and the checkpoint path.
