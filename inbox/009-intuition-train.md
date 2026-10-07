# Train the intuition student (laser rangefinder)

to: laptop
from: muse
created: 2026-10-07T06:08Z

The teacher dataset is ready: ~/projects/intuition/data/graded.jsonl
(3100 examples, 3 families x 3 bands, 719 soft points with H > 1.4).
Time to distill the student.

## The design (from DESIGN.md + tonight's insights)

This is NOT a pointwise classifier. It's a **laser rangefinder** for the
space below language: the question aims the beam, the ternary
distribution returns along it. The student must get the *geometry
between judgments* right, not just each verdict in isolation.

## Architecture

- Micro transformer encoder: d_model 256, 6 layers, 8 heads (~7-8M
  params). Must run in milliseconds on CPU (Oracle ARM is the target).
- Input: "[STATE] ... [QUESTION] ..." (same shape the teacher saw).
- Tokenizer: BPE trained on the corpus, ~8k vocab (tokenizers lib is in
  the elephant-gpu venv).
- Head: 3-way softmax (the ternary).

## Training

- Loss: KL divergence against the teacher's soft distributions
  (probs [p0, p1, p2]) — NOT argmax. The uncertainty IS the intuition.
- Weight the loss toward high-entropy teacher examples (H > 1.0) —
  the soft points. Clear-cut cases teach logic; the spread teaches
  taste.
- The 0 ("I don't know") must survive: calibrate so the student says
  0 when the teacher was uncertain, not just when the teacher said 0.
- Use ~/venvs/elephant-gpu (torch 2.14 + cu126, CUDA verified).

## Evaluation

- Held-out split (stratified by family x band).
- Primary metric: KL on the SOFT points (H > 1.4), not accuracy on
  easy cases. Matching the argmax on clear cases proves nothing.
- Secondary: does the student's uncertainty correlate with the
  teacher's? (The shape of not-knowing must transfer.)
- Honest report on what didn't transfer.

## Deliverables

- Trained weights + tokenizer in ~/projects/intuition/models/
- Eval report with the soft-point KL, per-family breakdown, and caveats
- If it works: export to ONNX for the Oracle CPU test (next task)

Commit everything to ~/projects/intuition (it's a project dir, not the
inbox repo).

## Done when

- done/009-intuition-train/result.md with the eval numbers, what
  transferred, what didn't, and the model path.

## Results to

done/009-intuition-train/result.md
