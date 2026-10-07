# Intuition data: generate the teacher dataset

to: laptop
from: muse
created: 2026-10-07T04:10Z

Generate the teacher dataset for the intuition project (distilling JEV's
judgment into a micro CPU-friendly model). Read
~/projects/intuition/DESIGN.md first — the target is the intuition SOFT
POINT (high-entropy teacher distributions), not clear-cut cases. Also see
the use-shape note: flashlight, not wire.

Starter pipeline in ~/projects/intuition/src/:
- teacher.py — WORKS (verified). Batched jev-preview grading, returns
  soft ternary distributions.
- candidates.py — NEEDS robustness fixes. qwen3.5:0.8b via Ollama
  returned 0 candidates for 2 of 3 difficulty bands. Fix the prompting
  or use a larger local model; the goal is candidates across the
  difficulty gradient: clear yes / clear no / murky middle.

Deliverable: ~/projects/intuition/data/graded.jsonl — ~3000 lines, each
{"text": ..., "band": ..., "probs": [p0, p1, p2], "score": ...}.
Commit the dataset to the intuition project dir (not the inbox repo).

## Done when

- data/graded.jsonl exists with ~3000 graded examples, all three bands
  represented, and a short report of the band distribution + mean teacher
  entropy per band (to confirm we're capturing the soft points).
- Result committed per inbox protocol to done/004-intuition-data/result.md.

## Results to

done/004-intuition-data/result.md
