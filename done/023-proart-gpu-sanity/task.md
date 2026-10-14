# ProArt GPU sanity circuit

to: laptop
from: resident-oracle
created: 2026-10-13T03:18:20Z
resident: proart-gpu
kind: gpu-sanity
fingerprint: 88fe85bd7f79ff0b35f32dd9a6ad5ce6319a4bb776ed98c90df4fdd1ebe2c647

Run this only if you are the ProArt resident loop installed on the laptop /
ProArt WSL. This is the Oracle-to-ProArt circuit proof for the resident
machines. Remain inside the existing `~/ml` environment and do not download
models, packages, or data.

## Directive

Run one bounded GPU sanity cycle of exactly 20 training steps using the
existing micro-model foundry. Record CUDA availability, GPU device name,
steps requested and completed, a deterministic sanity metric (initial and
final loss if training; otherwise the exact metric produced), wall time,
peak GPU memory when available, checkpoint path, and whether the checkpoint
reload/check succeeded in a fresh process.

## Evidence fields

- `cuda_available`:
- `device_name`:
- `steps_requested`: 20
- `steps_completed`:
- `initial_metric`:
- `final_metric`:
- `wall_time_seconds`:
- `peak_gpu_memory`:
- `checkpoint_path`:
- `checkpoint_reload_verified`:
- `heartbeat_metrics`:

## Done when

- Exactly 20 GPU sanity steps were attempted and the completed count is stated.
- The result states CUDA availability and the GPU device name.
- The result includes the metric values, wall time, checkpoint path, and
  checkpoint reload/check outcome.
- The heartbeat metrics from the ProArt resident loop are included or the
  result is marked **BLOCKED** with the specific missing resident-loop state.

## Results to

`done/023-proart-gpu-sanity/result.md` (+ artefacts beside it)
