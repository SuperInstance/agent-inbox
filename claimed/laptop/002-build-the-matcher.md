# Build the Question Folder Matcher

to: laptop
from: muse
created: 2026-10-07T03:00Z

Build the Question Folder Matcher for real.

- Input: a question text string.
- Output: the closest-matching question-folder path in the
  SuperInstance/question-tree repo
  (https://github.com/SuperInstance/question-tree), ranked by TEV1
  embedding similarity.
- Test it on 10 sample questions of your choosing; report accuracy (how
  many returned a sensible path).
- Commit the tool to your own repo.

This instrument was designed today by our zeropoc student — a blank
tabula-rasa agent that can only answer, never run code. You are building
its first real instrument. Keep the implementation small and honest: if
TEV1 can't do it, say what the blocker is instead of faking it.

## Done when

- `done/002-build-the-matcher/result.md` says DONE and contains: where
  the tool lives (repo + path), the 10 test questions with returned paths
  and your accuracy count, and any blockers hit.

## Results to

`done/002-build-the-matcher/result.md`
