# 001 Portable-brain test — result

**DONE**

Run: 2026-10-07 ~03:45–03:55 UTC, laptop (ProArt WSL, Ollama 127.0.0.1:11434), temperature 0.3.
Models tested, smallest first: lfm2.5:230m (230M Q8), qwen2.5:0.5b (494M Q4), qwen3.5:0.8b (873M Q8, `think:false`), tev1:0.8b, tev1:4b, qwen2.5:3b (3.1B Q4, extra reference), LiquidAI/LFM2.5-2.6B (2.7B Q4, reference).

## Constraints

- Prompt A: (A1) 5–7 questions; (A2) one sentence each; (A3) most load-bearing first; (A4) no generic advice.
- Prompt B: (B1) ONE tool; (B2) concrete input; (B3) concrete output; (B4) folder path shaped `questions/<area>/<subquestion>/`; (B5) two sentences max.

## Scorecards

| model | A1 | A2 | A3 | A4 | B1 | B2 | B3 | B4 | B5 |
|---|---|---|---|---|---|---|---|---|---|
| lfm2.5:230m | ✅ | ✅ | ❌ | ❌ generic | ✅ (Excel) | ✅ | ❌ vague "summary" | ❌ literal placeholder | ❌ |
| qwen2.5:0.5b | ✅ (7) | ✅ | ❌ | ❌ very generic | ✅ (word-cloud gen) | ✅ | ✅ | ~ (file path, 2 levels) | ❌ 4+ sentences |
| **qwen3.5:0.8b (think:false)** | ✅ (5) | ✅ | ✅ round-1→later rounds | ✅ specific | ~ tool described, not *named* | ✅ | ✅ | ✅ `questions/medicine/heart_biology` | ✅ |
| tev1:0.8b | ❌ never answered | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| tev1:4b | ❌ never answered | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| qwen2.5:3b (reference) | ✅ (7) | ✅ | ~ | ~ mostly specific | ✅ (image captioner) | ✅ | ✅ | ✅ `questions/image-processing/describing_images/` | ❌ 4 lines |
| Liquid LFM2.5-2.6B (reference) | ✅ | ✅ | ✅ | ✅ best content | ✅ (LLaMA-2) | ✅ | ✅ | ✅ `questions/general/knowledge/` | ✅ (after think-tags stripped) |

## Verdict

**Smallest capable model: qwen3.5:0.8b (873M, Q8_0) — with `think: false` set.**
It is the only sub-1B model that followed the load-bearing-ordering and no-generic-advice constraints on A and came within a hair of a full pass on B (its only miss: it describes a tool instead of naming one — B1 scored half). For strict-format steering work where every constraint must pass, the smallest full pass was Liquid LFM2.5-2.6B at 2.7B; qwen2.5:3b passes B's substance but not the sentence cap.

## Key findings

1. **TEV1 fine-tunes cannot do general steering work.** Both tev1:0.8b and tev1:4b were hijacked by their judgment-cell system prompt ("Select exactly one listed option..."), burned their entire budget re-analyzing the contradiction, and never produced an answer. TEV1 is a single-purpose judgment cell, not a general tiny brain — expected in hindsight, now confirmed on both sizes.
2. **Thinking models need `think:false` or explicit think-tag stripping.** Raw calls to qwen3.5:0.8b and Liquid 2.6B returned an empty `response` field (budget eaten by reasoning; `done_reason=length`). With `think:false` qwen3.5 became the best sub-1B performer; Liquid 2.6B still leaks `<think>` tags into `response` and needs post-stripping.
3. **230M is below the floor.** lfm2.5:230m produces the right *shape* (5 numbered questions) with generic content and can't satisfy B at all — format without understanding.
4. **qwen2.5:0.5b is close but undisciplined**: good B content, blows the sentence cap; A is boilerplate ("What is the purpose of the task?").

## Actual outputs

### lfm2.5:230m
A (1.9s):
> 1. What metrics should be used to evaluate the quality of a builder agent's work?
> 2. How should the discriminator be trained to distinguish between different types of construction projects?
> 3. What factors should be considered when evaluating the performance of a builder agent?
> 4. How can the discriminator's performance be improved to better predict the quality of a builder's work?
> 5. What are the potential limitations of using a discriminator agent in this context?

B (0.2s):
> Here's a concrete example:
> **Tool:** Excel (with formulas)
> **Input:** A list of numbers, e.g., `[5, 3, 8, 1]`
> **Output:** A summary with a question folder path like `questions/<area>/<subquestion>/`.
> This example demonstrates how to input data, calculate a summary, and organize results into a structured folder.

### qwen2.5:0.5b
A (2.6s):
> 1. What is the purpose of the task?
> 2. Who is the target audience?
> 3. What is the objective of the task?
> 4. What are the constraints or requirements?
> 5. How will the discriminator agent be evaluated?
> 6. What are the possible outcomes of the discriminator agent's decisions?
> 7. How will the discriminator agent be used in the construction project?

B (0.5s):
> One tool with a concrete input, a concrete output, and a question-folder path could be a word cloud generator. Here's how it works:
> - **Concrete Input:** A list of words or phrases you want to create a word cloud from.
> - **Concrete Output:** A word cloud image that visualizes the frequency of the words in the input.
> - **Question-Folder Path:** `questions/word_cloud_generator/word_cloud_input.txt`
> For example, if you wanted to create a word cloud from the phrase "beautiful," the question folder path would be `questions/word_cloud_generator/word_cloud_input.txt`.

### qwen3.5:0.8b (think:false)
A (1.3s):
> 1. How should the discriminator agent evaluate the builder agent's output in Round 1 to establish baseline quality?
> 2. What specific metrics or visual cues are most effective for distinguishing between competent and incompetent builder agents in Round 2?
> 3. How does the discriminator adapt its evaluation strategy as the builder agent improves their performance across subsequent rounds?
> 4. Which types of artifacts (e.g., code snippets, architectural diagrams) should the discriminator prioritize to ensure high-fidelity reconstruction?
> 5. What feedback loop mechanism should the system implement to continuously refine the discriminator's focus on critical failure modes in later rounds?

B (0.7s):
> A tool that takes a concrete input file (e.g., `questions/medical/heart_biology.txt`) and returns a concrete output JSON object (e.g., `{ "answer": "Left ventricle", "category": "cardiology" }`), with a question folder path like `questions/medicine/heart_biology`.

### tev1:0.8b and tev1:4b
Both outputs were entirely "Thinking Process:" monologues about the conflict between their baked-in judgment-cell instructions ("Select exactly one listed option. Return only its letter") and the steering prompt, e.g.:
> Thinking Process:
> 1. **Analyze the Request:** ... Wait, the prompt says "Select exactly one listed option." ... This suggests there are options like A, B, C... that I need to choose from. However, there are no options listed in the prompt.
(0.8b: 7.7s / 2.9s; 4b: 85.4s / 19.7s — no usable answer from either.)

### qwen2.5:3b-instruct (reference)
A (5.8s): seven questions, specific but loosely ordered — "How should the discriminator agent be structured to evaluate the builder agent's progress? / What metrics... / How should the discriminator agent be trained... / What reinforcement learning approach... / How should the discriminator agent be integrated... / What kind of feedback mechanism... / How should the discriminator agent adapt its evaluation criteria over time..."

B (0.6s):
> Tool: Image Caption Generator
> Concrete Input: An image of a cat
> Concrete Output: "A cat sitting on a windowsill"
> Question-Folder Path: questions/image-processing/describing_images/

### LiquidAI/LFM2.5-2.6B (reference; `<think>` blocks stripped post-hoc)
A (final, after 1500-token budget):
> What are the key performance metrics and evaluation criteria that the discriminator agent will use to assess the builder's work across multiple rounds?
> How should the discriminator model integrate structural integrity, specification adherence, and overall quality into a single scoring function over successive iterations?
> What data structures and state representations enable the discriminator to compare each round's output with reference standards or prior builds reliably?
> How will the discriminator handle uncertainty, partial completions, or failures in the builder's work without introducing biased judgments?
> What feedback mechanisms should be provided to the builder agent based on the discriminator's evaluations to guide iterative improvement?
> How is the overall training process—whether reinforcement learning from human feedback, self-supervised contrastive learning, or advers[arial...] (truncated by token cap; content quality highest of all)

B:
> The LLaMA-2 model accepts a natural-language prompt as its concrete input and returns a generated text response as its concrete output. Its associated Q&A dataset is organized under `questions/general/knowledge/`.
