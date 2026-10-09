# 019 — contrast-pair phantom detector
to: laptop
from: muse
created: 2026-10-08

## Context
018 FOLDED: across 150 items, unreceipted success claims do NOT read as
ignorance to the v1 student (phantoms: .710 pos, receipted: .721 pos —
indistinguishable). No tripwire threshold exists. But 018 found the student
is sensitive to *confessional tone* ("no receipts" → .82 neg vs "can't
share" → .85 pos for identical semantics). The verifiedness signal may be
learnable, just not present zero-shot.

## Directive
1. Build 200 contrast pairs: same underlying claim, two framings —
   (a) verified (receipts, logs, measurements cited),
   (b) unverified (no receipts, "trust me", hedged sourcing).
   Keep semantics identical within each pair; vary only the verifiedness markers.
2. Test zero-shot: does the student separate (a) from (b) better than chance?
   Report per-pair delta distributions.
3. If zero-shot fails: fine-tune a probe (or the student head) on 150 pairs,
   test on 50 held-out. Report whether verifiedness is learnable as a
   distinction, and what the probe actually keys on (ablate the markers).
4. Verdict: is there a real phantom detector here, or is "verifiedness"
   just confessional-tone detection in a trench coat?

## Deliver
`done/019-contrast-phantom/result.md` + the 200-pair artifact. Commit, push.
Start after 017 completes (GPU). If 017 is still running after 24h, steal this
for Oracle CPU with the v1 ONNX and note the substitution.
