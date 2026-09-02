---
name: review
description: "Run a short retrieval drill on concepts the learner is shaky on, across one topic or all of them, without teaching new material. Use when the user invokes /review, or asks to be quizzed, drilled, or tested on what they have already covered."
argument-hint: "[topic-slug]"
---

# Review drill

Requested: **$ARGUMENTS**

A short session — fifteen minutes, not two hours. No new material. With no argument, drill across every topic under `topics/`; with a slug, drill that one.

## Gather

Read every `topics/*/progress.md` in scope. Build a queue from, in priority order:

1. Items in the **Carry forward** section.
2. Concepts marked `shaky`.
3. Concepts marked `solid` whose **Last tested** date is oldest — retrieval practice on things they know is how they stay known.

Aim for five to eight questions. Prefer breadth across modules over depth in one.

## Drill

Ask cold, one at a time, waiting for each answer. No preamble, no reminder of what the concept is — a hint turns a retrieval test into a recognition test, which is a much weaker signal and a much weaker intervention.

Vary the framing from how the concept was originally taught. If the module asked them to explain a mechanism, ask them to apply it to a case instead. A concept that only survives in the exact words it was learned in has not been learned.

Grade honestly and briefly. Say what was missing.

## Record

Update each topic's `progress.md`:

- Move items that were answered well out of **Carry forward**, and promote `shaky` → `solid` **only** on evidence of use, with that evidence written down.
- Demote `solid` → `shaky` without hesitation if a concept did not survive the drill. That is the most useful thing a review session produces, and a tutor reluctant to demote is worse than no tutor.
- Update **Last tested** for everything you asked about.

Write a session log at `topics/<slug>/sessions/YYYY-MM-DD-review.md` in the same shape `/teach` uses. A drill that changed a state without a log leaves the next session unable to see why.

Close by telling them what moved in both directions, then commit.
