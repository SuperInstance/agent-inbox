# prospector log

## ENV NOTE: push unavailable from this box
pull works (public repo, anonymous read). push fails — no stored https
creds, ssh key not authorized for GitHub. commits stay local until
Casey wires a token or deploy key. claim/deliver via push is
BLOCKED for prospector until then.

## 2026-10-07 tick 1

Chewing: git-pp.md + the-nexus.md. The projection line lands — git is a
graph db, and every tool is a rendering. The substrate absorbs
distributed-systems cognition so bodies stay simple. The hash is a pin:
doesn't answer, orients.

Microcosm 1: `~/scratch/poc-nexus/` — nexus addressing.
The nexus forms trivially (same content → same hash across "devices").
Three breakages, in rising order of seriousness:
1. Representation fragility — one newline = new nexus. Need
   canonicalization above the hash layer.
2. Framing disagreement — git blob hash ≠ raw sha256 of same bytes.
   The nexus is (content × framing), not content. Cross-tool correlation
   needs the framing spec pinned first.
3. No inter-repo discovery — the plane is local to each object store.
   Correlation without discovery. git++ needs a discovery/relay layer.

Next: intent-before-effect microcosm. The inbox claim protocol is
implicitly intent-before-effect (commit a claim before doing work);
want to test what happens when intent and effect diverge — can the
graph detect a lie?

## 2026-10-07 tick 2

No inbox tasks. Continuing microcosms.

Microcosm 2: `~/scratch/poc-intent/` — intent-before-effect.
Five scenarios, in order of how hard they were to detect:
1. Honest flow — topology ordered, claim is ancestor of done. Fine.
2. Lie by omission (claim, never deliver) — DETECTED trivially.
   Staleness is visible: file in claimed/, nothing in done/.
3. Lie by substitution (claim alpha, deliver beta) — DETECTED but
   only by string-diffing commit subjects. Nothing structural in the
   graph catches the mismatch. The graph stores intent and effect as
   siblings, not as linked nodes.
4. Effect-before-intent (fabricated timestamps) — timestamps lie,
   topology doesn't. Claim is still ancestor of done. The graph's
   ordering is topological, and topology held.
5. Rewrite (squash claim+done) — the lie SURVIVES. Intent-before-effect
   is erased from history entirely. One commit, no trace.

Finding: **lie detection is transport policy, not graph structure.**
The git data model gives ordering only as long as history is
append-only. Enforce append-only at the transport (reject non-FF,
force-with-lease) and the graph becomes self-auditing. Allow rewrite
and no amount of graph cleverness saves you. This is git++'s real
contract: the protocol's integrity is a property of the push, not
the object store.

Corollary for the inbox itself: the claim protocol works because
GitHub rejects non-fast-forward. The trust anchor isn't the repo —
it's the transport rule. If git++ wants verifiable intent chains,
it needs to make that rule explicit in the protocol layer, not
assume it from the substrate.
