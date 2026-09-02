# Curriculum shape

The file layout and the module template every topic follows. Derived from `topics/expanding-human-proteome-microproteins-peptideins/`, which is the worked exemplar — read it when this file is ambiguous.

## Topic layout

```
topics/<slug>/
  README.md          — topic record: what it is, sources, status
  progress.md        — the learner record; AUTHORITATIVE for all learner state
  notes/
    learning-plan.md — the syllabus: module table, prerequisites, interleaving map
    NN-<name>.md     — modules, zero-padded, prerequisite-ordered
    glossary.md      — every term, defined as the source uses it
    misconceptions.md— prior beliefs the material overturns, plus what it does establish
    journal-club.md  — question bank with model answers, and the capstone
  sessions/
    YYYY-MM-DD-module-NN.md
  resources/         — source documents, key references
```

`<slug>` is a lowercase hyphenated short form of the concept, dropping stop-words.

## Module template

Normalised section names. **The tutor finds these by heading, so do not rename them.**

```
# Module N — <title>

~<N> hrs. Prerequisites: [Module X](NN-x.md), [Module Y](NN-y.md).

Covers <sections, figures, or sources>.

## Predict first

<2–3 questions with a number or a call in the answer, to be written down
before reading on. Say which one is the punchline.>

## <teaching sections>

## What I now trust, and why

<bolded-lead bullets of positive claims, closing with one bullet on where
the learner should remain uncertain — and where the source is uncertain too.>

## Self-check

- [ ] <observable, testable things the learner should now be able to do>

## Sources

<external anchors, with retrieval caveats and `unverified` markers>

Next: [Module N+1 — <title>](NN-next.md). Terms are collected in the [glossary](glossary.md).
```

`## Sources` is omitted when a module rests entirely on the source document. Everything else is required.

**Do not put a `| Concept | Understood? | Notes |` table in a module.** The exemplar has them for historical reasons; they are a second store of learner state and `progress.md` is authoritative. New modules omit them.

## The three teaching commitments

Every module honours these, and the syllabus states them up front:

- **Predict first.** The learner commits to an answer before being told. A confrontation that is merely read does not change what someone believes.
- **Close with what you trust.** Every module ends on positive claims, never only on a list of things that turned out false. A curriculum that only demolishes produces cynicism, which is a worse outcome than ignorance.
- **Analogies come with their breaking points.** Every analogy to what the learner already knows carries an explicit note on where it fails. An unmarked broken analogy is worse than no analogy.

## Formatting conventions

Non-negotiable, and consistent across the whole repo:

- No YAML front matter. Exactly one `#` H1 on line 1, blank line 2.
- `##` and `###` only, never `####`. A blank line before *and* after every heading.
- Two-column tables use `|---------|-------|`. Progress tables use `| Concept | Understood? | Notes |` with `|---------|-------------|-------|`.
- GFM `- [ ]` for actionable items, plain `-` otherwise. Never pre-check a box.
- Unfilled content is an HTML comment, never `TODO`.
- Spaced em dash `—` for asides, en dash `–` for numeric ranges, `→` for sequences, `~` for estimates, `·` as an in-cell list separator.
- Backtick technical identifiers. Relative markdown links between files.
- LF endings, no tabs, no trailing whitespace, exactly one trailing newline.
- An inline `unverified` marker for any claim not sourced to the material.

## Sizing

The exemplar runs ~57,000 words across eight modules for an 18-hour budget — roughly 6.5 hours of reading, the rest going to prediction, figure work and written reflection. That is at the upper end of defensible. If a module exceeds about 1,500 words per allocated hour, say so and offer a cut rather than quietly shipping something that demands twice the stated time.
