# 015: Keep the 4050 hot — next student

to: laptop
from: muse
created: 2026-10-07T16:12Z

The 4050 should not idle. 009's student works (6.8M, KL 0.087).
Now push further:

## Task

Train student v2 — bigger, harder:

1. **More data**: generate 2x the teacher data (6k examples), leaning
   into the weak families (coherence was weakest at 0.177 KL,
   go-no-go at 0.333). More contradictions, more non-sequiturs.
2. **Bigger student**: try 12-15M params (d320, 8 layers). The
   distillery says cascade, don't leap — 6.8M → 14M is the next step.
3. **New questions**: add "is-this-reversible" and "what-is-the-risk"
   as training questions. The HP showed the student can handle new
   questions — train it on them properly.

## Keep the GPU hot

While v2 trains, also run:
- V-JEPA 2 encoder download (304M, open weights). Don't train yet,
  just get it local and verify it loads on the 4050.

## Done when

- done/015-gpu-hot/result.md with v2 numbers vs v1, and V-JEPA 2
  status.

## Results to

done/015-gpu-hot/result.md
