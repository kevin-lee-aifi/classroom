# Working in this repo

`classroom` is a guided-learning system. Each topic under `topics/` is a curriculum plus a record of what its owner has actually learned. Sessions are stateless, so everything a tutor knows about the learner lives in these files.

## The three-file contract

Per topic, under `topics/<slug>/`:

| File | Role |
|---------|-------|
| `notes/learning-plan.md` | The syllabus — module table, prerequisite order, interleaving map |
| `progress.md` | **The authoritative learner record.** Concept states, evidence, carry-forward queue |
| `sessions/YYYY-MM-DD-module-NN.md` | What happened in one session — quoted, not paraphrased |

Modules and support files live in `notes/`; source material in `resources/`.

**Never write to a `progress.md` outside a `/teach` or `/review` session.** It is the learner's history, and a passing session should not rewrite it. Modules must not carry their own `| Concept | Understood? | Notes |` tables — the exemplar has them for historical reasons, but they are a second store of the same state and `progress.md` wins.

## Commands

- `/learn <concept> [resources]` — build a new topic. Multi-agent, with an adversarial audit. Slow and deliberate; user-invoked only.
- `/teach [topic] [module]` — a guided session. No arguments resumes where the record says.
- `/review [topic]` — a short retrieval drill, no new material.
- `/progress` — status. Read-only.

## Reading a PDF

There is **no `pdftotext`, no poppler, no `pypdf`** here, and the `Read` tool cannot render a PDF. Use the bundled extractor:

```
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf flat   > flat.txt   # prose
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf placed > placed.txt # figures
```

Anything inside a figure comes from `placed` or `region`, never from `flat` — flat reading order transposes tables. Inequality directions come from prose, never from figure extraction. Full rules in `.claude/skills/learn/references/extraction-discipline.md`.

## Teaching conventions

Every module follows one template, and the tutor finds sections **by heading**, so the names are fixed: `## Predict first`, then teaching sections, then `## What I now trust, and why`, `## Self-check`, and optionally `## Sources`.

Three commitments the material honours:

- **Predict first** — the learner commits to an answer before being told. Being wrong first is the mechanism.
- **Close with what you trust** — every module ends on positive claims, never only on demolished beliefs. A confrontation-only curriculum produces a cynic.
- **Analogies come with their breaking points** — an unmarked broken analogy is worse than no analogy.

`solid` in a progress record means demonstrated *use*, not one correct answer. Grading generously produces a record full of `solid` and a learner who cannot defend the material.

## Formatting

Followed exactly across the repo; match it.

- No YAML front matter in `topics/` or `README.md`. Exactly one `#` H1 on line 1, blank line 2.
- `##` and `###` only, never `####`. A blank line before *and* after every heading.
- Two-column tables use `|---------|-------|`. Progress tables use `| Concept | Understood? | Notes |` with `|---------|-------------|-------|`.
- GFM `- [ ]` for actionable items, plain `-` otherwise. Never pre-check a box.
- Unfilled content is an HTML comment, never `TODO`.
- Spaced em dash `—` for asides, en dash `–` for numeric ranges, `→` for sequences, `~` for estimates, `·` as an in-cell separator.
- Backtick technical identifiers. Relative markdown links between files.
- LF endings, no tabs, no trailing whitespace, exactly one trailing newline.
- Mark any claim not sourced to the material with an inline `unverified`. Never write a DOI you did not read.

## Status vocabulary

A topic's `README.md` carries `to-read` → `reading` → `read`. Advancing it is the learner's call, not a session's.
