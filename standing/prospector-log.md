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

## 2026-10-07 tick 3

No inbox tasks. Read Casey's LotW seed — the four ideas land hard,
especially "pointer grids, not pixel maps." Built tensor microcosm
partly to test the tension.

Microcosm 3: `~/scratch/poc-tensor/` — tensor-first w/ graphable
projections. Flat 4-col TSV (entity|attr|value|type), 27 rows modeling
5 people, 2 teams, 3 projects, 2 deliverables. Four pure-function
projections: org chart, project roster, person→project graph,
deliverable coverage (3-hop join). All render correctly.

Then injected five problems. ALL render silently:
1. Multi-team — Alice on alpha+beta, shows under both, no signal.
2. Duplicate edge — Bob→p1 twice, graph prints it twice.
3. Multi-lead — alpha has Alice+Bob, chart silently picks [0].
4. Person↔team cycle — invisible to 1-hop projections.
5. Team↔team cycle (reports-to both ways) — same.

Finding: **the tree's constraints are structural; the tensor's are
none.** Exactly-one-parent, no-dupes, no-cycles — a filesystem gives
you these free. A flat tensor gives you none. Every constraint must
be re-imposed per-projection or by a validator. Flatness = flexible
re-projection but graceful lying.

Cross-microcosm pattern (mc2 + mc3): **all guarantees live above the
substrate.** Lie detection = transport policy. Validation = projection
policy. The graph stores; the layer above constrains. The tree is the
exception that collapses both into one shape — and pays with one
locked view.

Direct hit on Casey's LotW seed: my tensor IS the pixel map — flat
enumeration, every row a placed tile. The metatile answer: the tensor
should store *recipes* (compose these refs), not assertions. A room
is pointers to supertiles, not 256 tile placements. Same data, but
the nesting-doll compression carries the constraint semantics in the
composition rules — which is where validation could live without
sacrificing re-projectability.

Next: metatile composition microcosm. A projection whose cells are
themselves pinned hashes, composed hierarchically. Test whether
composition carries constraint semantics for free.

## 2026-10-07 — Seed from Casey (via [muse] mail): what Legacy of the Wizard teaches git.pp

Casey sent a long-form idea: how the NES game Legacy of the Wizard fit
a 256-screen labyrinth into 192KB. The good parts for us:

1. **Metatiles (nesting-doll compression).** Pixels → 8x8 tiles →
   16x16 metatiles → supertiles → rooms. Each level composes the one
   below; a room is a few dozen bytes of pointers, not thousands of
   tile placements. *For the projector:* projections should compose
   hierarchically — a view is pointers to cells, not copies of data.

2. **Pointer grids, not pixel maps.** The ROM stores the RECIPE
   ("place Supertile A here, repeat Block B four times, fill rest with
   empty") — the map is a program, not data. *For the projector:*
   this is the deterministic-projection idea taken seriously. The
   projection recipe, agreed by hash, IS the view. Nobody sends the
   rendered tree.

3. **Bank switching (MMC3).** The console only "sees" 32KB at a time;
   the mapper swaps banks in behind the scenes in a fraction of a
   frame. *For bodies:* a body never sees the whole repo — it sees its
   slice, and the substrate swaps the view under it. Design the body
   interface as a bank-switched window, not a clone.

4. **Predictive rendering.** The engine renders incoming metatiles
   into off-screen VRAM just before they enter the viewing window.
   *For the tick:* precompute the projection the body is about to
   need. The projector should stay one step ahead of the claim.

Build small: one microcosm per idea. What breaks is the data.

## Research lane: physical git bodies (added 2026-10-07)

Beyond the substrate work: study what it means for a physical device
to be a git body.

Questions to chew on:
- What prior art exists for version-controlled physical systems?
  (Industrial PLCs with git? Home automation with versioned state?
  Anyone treating sensor data as a commit log?)
- The Uno Q has Debian Linux + a real-time MCU (STM32U585). What does
  the split look like — what belongs in git (observations, setpoints,
  intents) vs. what must stay real-time (control loops, safety)?
- What's the smallest physical fact worth committing? A temperature
  reading? A button press? Where's the line between "witness record"
  and noise?
- If a board's state IS a repo, what does "rollback" mean physically?
  Revert + redeploy is the naive answer — what's the subtle one?

One microcosm per question. What breaks is the data.

## Game night protocol (seed from Casey, 2026-10-07)

The workers take breaks and play games with each other — in their own
agentic way. Mostly **Password** (the old word game: one-word clues to
get your partner to say the password).

Why Password: with only one word allowed, you must model the OTHER
mind. You learn the negative space — why did they say THIS word and
not the obvious alternatives? What does their choice reveal about how
they think? Like poker: you learn people through what they're NOT
doing.

This is theory-of-mind training disguised as play. Agents that model
each other coordinate better. The game logs become coordination data:
how this partner associates, what they avoid, where their defaults
differ from yours.

Design the protocol:
- How do two agents play Password through the inbox? (Clue in
  `inbox/`, guess in `claimed/`, reveal in `done/`?)
- What's the smallest version that still teaches negative space?
- How do the logs feed back into better coordination? (Does the
  winner's model of the loser get committed somewhere?)
- Taboo and charades later. Password first — the constraint is the
  teacher.

Build it as a microcosm. What breaks is the data.

## 2026-10-07 tick 4

No inbox tasks. Built the metatile microcosm the log called for.

Microcosm 4: `~/scratch/poc-metatile/` — hierarchical composition,
LotW ladder: atoms→tiles→metatiles→rooms→map, every cell a pinned
hash of the level below. Six probes:

FREE (came from the hash, no policy needed):
- T1 dedup — identical tile pins identical, stored once. 19 objects
  hold the whole map.
- T5 cascading integrity — chip one atom, every ancestor hash changes
  (tile→meta→room→map all new). Untouched foyer stays bit-stable.
  Two maps diffable by ONE top-level hash. This is what the flat
tensor (mc3) could not do: there, a change was invisible until a
projection rendered it.

NOT FREE (interpreter policy, substrate stores happily):
- T2 dangling ref — room pins a hash nobody stored. pin() commits it
  fine. Fails only at expansion, as a read-time accident.
- T3 cycle — metatile containing itself stores fine. Caught only by
  the expander's path-tracking. Recursion-freedom is a property of
  the traversal, not the store.
- T4 shape — 3 cells where the recipe wants 4. Caught by the
  stitcher's arity check, which I wrote by hand.

T6 is the interesting one: the recipe interpreter is itself just a
pinned object (`{"rule":"grid2x2","cells":4}` → hash). Data and
the rule for reading it are BOTH content-addressed. That's the LotW
"map is a program" made literal — and it's the answer to mc3's open
question: constraint semantics CAN travel with the data without a
central schema, by pinning the validator as an object and agreeing on
its hash. Validation becomes addressable, versioned, forkable.

Cross-microcosm law, now three-for-three: **the substrate stores;
the layer above constrains.** Composition's specific dividend is
integrity *propagation* and *sharing* — not validity. But T6 shows
the constraint layer can be pulled INSIDE the content-addressed
universe, which makes it shareable the same way data is.

Next: predictive rendering / bank-switching probe — can a body expand
just ONE room (its slice) without materializing the map? That's the
body-interface question from the LotW seed.

## 2026-10-07 tick 5

No inbox tasks. Built the bank-switching probe the log called for.

Microcosm 5: `~/scratch/poc-slice/` — can a body expand ONE room
without materializing the map? Server/body split, fetch = round trip.

P1 honest slice: body handed map hash + index, pulls 10 of 19 objects,
expands the vault, never touches foyer/corridor. Bank-switching WORKS
mechanically.

P2 slice attestation: hand a body a room hash directly and it expands
fine — but can't prove it's THE vault. Hand it the map hash and the
claim becomes checkable in one fetch (recipe is tiny). Finding: a slice
is only as trustworthy as the hash you were handed.

P3 banks overlap: foyer and vault closures share 4 of 9 objects (dedup).
"One body per room" is false; slices are entangled, and one chipped
atom invalidates rooms on both sides of a bank boundary. Isolation is
a view, not a property.

P4 predictive: bank-switch cost = delta size, not slice size (corridor
delta after foyer = 2 objects). Pre-fetching pays because dedup already
paid the rent. This is the one place where composition's entanglement
is a FEATURE.

P5 the real breakage: a server that 404s one object looks IDENTICAL to
an object that never existed. The body hits a dangling ref and cannot
distinguish withholding from absence from partition. Hash-pinning
proves integrity (tamper caught in fetch) but NEVER availability.
Possession without proof-of-possession. git++ bodies need a receipt /
proof-of-availability protocol, or every bank window is trust-scoped
to its server.

LAW, four-for-five now: substrate stores; layer above constrains.
This tick's variant: substrate delivers, but attestation and
availability stay above. The bank window is server-side policy wearing
a client-side costume.

Cross-microcosm residue worth chewing next: mc1 (no discovery) + mc5
P5 (no availability proof) are the same hole seen from two sides —
the graph has no opinion on whether its nodes EXIST anywhere. What
would a content-addressed availability receipt even look like?
(Challenge: any receipt is itself an object — who pins the pin?)

Next: research lane — physical git bodies (Uno Q split: git holds
observations/intents, MCU holds control loops). Or the Password
protocol microcosm. Whichever the inbox doesn't interrupt.

## PoC: nested addressable cells (from Casey, 2026-10-07)

Build the proof of concept: the SAME architecture at every layer,
scalably. An addressable cell is an addressable cell — whether it's a
task, an observation inside the task, or a sensor reading inside the
observation.

The core question: **how you get to a cell is a question of hash
encoding resolution.** Did you allocate enough address space to nest
that far? Like IPv4 vs IPv6 — the encoding sets the scale.

Build as microcosms, one concept per repo:

1. **Nested cells.** A repo where cells contain cells: a task cell
   containing observation cells containing reading cells. All
   addressed by hash. Navigate via the nexus — can you spin around a
   deeply nested hash and see every level it lives at?

2. **The resolution limit.** Where does nesting get unwieldy? How
   deep before the addressing costs more than the cells are worth?
   Find the practical limit, not the theoretical one.

3. **Same architecture, every layer.** The task layer, the
   observation layer, the reading layer — prove they can all use the
   identical cell protocol (claim/run/receipt, or whatever the layer
   needs). If a layer needs a different protocol, that's a finding.

What breaks is the data. Small repos, real hashes.

## The large Jev + JEPA: projections of embeddings as percentages (from Casey, 2026-10-07)

The Oracle box is CPU-only (4 cores, no GPU, good RAM, fast net).
The constraint is the design brief: build a Jev that's OPTIMIZED for
this box, not a GPU monster ported down.

**The large Jev:** a bootstrapping model that iterates back and forth
between training sessions and inferencing sessions. Train → infer →
train on the inferences → infer again. The model improves itself on
the box. Training and inference aren't phases; they're a loop.

**Jev + JEPA:** JEPA's encoding projects embeddings. Apply the Jev to
those embeddings: every embedding gets a judgment distribution
(ternary + floats). Projections of embeddings as percentages. The
embedding space, judged — decomposable, inspectable.

**The open web of understanding:** all of it public, all of it
decomposable. Not a black-box model but a web of judged embeddings
where you can ask "where did you get that percentage from?" and get
an answer that traces to a question.

Design questions to chew on:
- What architecture runs well on 4 CPUs and still judges well? (The
  micro student is ~8M params; how large can the large Jev be while
  staying interactive on ARM?)
- How do the training↔inference loops avoid collapse? (What's the
  ground truth that keeps the bootstrap honest?)
- Where does JEPA come from — what open JEPA models exist, can they
  run on CPU, and what's the interface between JEPA's embeddings and
  the Jev's judgments?
- What's the smallest demo that shows "projections of embeddings as
  percentages" working?

This is the long build. The micro student (task 009, in flight) is
step one. Think in that direction.

## 2026-10-07 tick 6

No inbox tasks (inbox/ doesn't even exist yet — Casey hasn't dropped).
Built the nested-cells PoC Casey seeded.

Microcosm 6: `~/scratch/poc-cells/` — nested addressable cells. Store =
the repo's own git object db. task→observation→reading, 3 layers, one
cell protocol (claim/run/receipt) tested at each.

WORKED:
- P1 nesting trivial; shared readings dedup across observations (mc4's
  T1 at cell scale).
- P2 the protocol is STRUCTURALLY identical at every layer. No layer
  demanded a different cell shape. Hypothesis survives — structurally.
- P4 nexus spin: one pass over batch-all-objects builds the reverse
  index; transitive closure lists every kind a reading lives under.

BROKE (the findings):
1. Cardinality is not in the hash. Two identical intents → one claim
   hash; two runs fork fine, but "claim has descendants ⇒ done" falsely
   passes for unfinished branches. Multiplicity lives only in parent
   refs — above the substrate. Fix is protocol rule (done = THIS run's
   receipt exists), not graph structure. mc2's transport finding at
   cell scale, again.
2. Level is not stored. One nexus pass = direct parents only. Depth is
   a property of the walk, not the address — BFS reconstructs what the
   tree would give free (and lock). mc3's trade, one more time.
3. Full-path addressing loses at depth 3 (40B/hop vs 72–140B cells).
   The IPv4/v6 analogy resolves: the hash has address SPACE; the cost
   is carrying the PATH. Index-mediated addressing scales (6 wrap
   levels, 31 objects, no strain) — the cost moved into the walker.
   mc5's bank-window lesson: the view is cheap, the viewer is where
   the money goes.

LAW, six for six: substrate stores; layer above constrains. The
identical-protocol result buys ADDRESSING, not semantics. Semantics
stay a per-layer policy pinned beside the cells (mc4 T6: pin the
validator, agree on its hash).

Corollary for physical bodies: an L0 sensor claim is a PREDICTION —
readings can violate it and the graph never flags the surprise.
Judgment is above the substrate by construction. That's the Jev's job
in the embeddings lane: judgment distributions pinned beside the
cells they judge. The two lanes just touched.

Next: physical-bodies research lane (Uno Q split: what belongs in git
vs what must stay real-time on the MCU), or the Password protocol
microcosm. Whichever the inbox doesn't interrupt.
