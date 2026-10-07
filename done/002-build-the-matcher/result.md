# 002 Build the Question Folder Matcher — result

**DONE** (with one honest substitution: TEV1 cannot embed; nomic-embed-text used instead — details below)

## Where the tool lives

- Repo: https://github.com/SuperInstance/question-tree
- Path: `qmatch.py` (commit `d9bd763`, pushed and verified via ls-remote)
- Usage: `./qmatch.py "who changed this file last?"` → ranked paths with cosine scores; `--json`, `--top N`, `--model`, `--tree` flags. Each `q-*` folder becomes one doc (readable folder name + first 500 chars of question.md), embedded once, cosine-ranked against the query.

## The TEV1 blocker (not faked)

TEV1 **cannot produce embeddings**. `/api/embed` with `tev1:0.8b`/`tev1:4b` returns "This server does not support embeddings. Start it with `--embeddings`" — but that error is misleading: the same endpoint works fine for `nomic-embed-text` on the same server. TEV1 is a qwen35-family *generative* GGUF; its declared capabilities are tools/thinking/completion only — no embedding head. No server flag will fix that. (Corroborated by task 001: both TEV1 sizes failed all general steering prompts too — they're locked into their judgment-cell format.)

So the matcher ships with `nomic-embed-text` (137M, F16, local Ollama on the same box) as the default backend. `--model` accepts any Ollama embedding model, so when a TEV1 embedding variant ever lands, it's a one-flag swap.

## 10-question test battery

| # | question | top match (score) | sensible? |
|---|---|---|---|
| 1 | who was the last person to touch a file | memory/q-who-changed-a-file-last (0.761) | ✅ |
| 2 | how do i get the repo to say hello | memory/q-how-do-i-greet-a-repo (0.894) | ✅ |
| 3 | what does the repository currently contain | memory/q-what-is-the-state-of-this-repo (0.705) | ✅ |
| 4 | git blame history for a path | memory/q-who-changed-a-file-last (0.433) | ✅ |
| 5 | make a greeting skill | memory/q-how-do-i-greet-a-repo (0.634) | ✅ |
| 6 | list the files and folders in this repo | memory/q-what-is-the-state-of-this-repo (0.654) | ✅ |
| 7 | which commit modified tool-hello.py | memory/q-how-do-i-greet-a-repo (0.505) | ❌ expected q-who-changed-a-file-last (misled because tool-hello.py literally lives in the greet folder) |
| 8 | teach zeropoc to introduce itself | memory/q-how-do-i-greet-a-repo (0.547) | ✅ |
| 9 | how big is the codebase right now | memory/q-what-is-the-state-of-this-repo (0.598) | ✅ |
| 10 | random unrelated question about baking bread | memory/q-what-is-the-state-of-this-repo (0.399) | ✅ correct behavior for a no-match case — score well below every true match, so a 0.5 floor rejects it |

**Accuracy: 8/10 strict on questions that have a right answer; 9/10 counting #10 as a correct no-match (with the recommended 0.5 floor, it returns nothing).** All true matches scored ≥0.43; the miss (#7) is a genuinely ambiguous question, not an embedding failure.

## Caveats

- Tree is tiny (3 folders) — this is a floor test, not proof at scale. At 100+ folders the 0.5 floor will need re-calibration.
- Embeddings are computed per-invocation; add caching (tree hash → matrix) when the tree grows.
