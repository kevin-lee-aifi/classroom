---
name: progress
description: "Report the learner's status across all curricula in this repo: modules complete, concept mastery, what is queued for review. Read-only, no teaching. Use when the user invokes /progress or asks where they are up to, what they have covered, or what is due."
---

# Progress report

Read-only. Report, do not teach, and do not modify any file — `progress.md` is written by teaching and assessment sessions only, so that a passing session cannot rewrite the learner's history.

## Gather

For every `topics/*/`: read `progress.md` and `notes/learning-plan.md`, and list `sessions/`.

## Report

Lead with one line per topic: modules complete out of total, next module, and when it was last touched.

Then, only where it is worth saying:

- **Queued for review** — carry-forward items and anything `shaky`, with the concept named rather than just counted. A count tells them nothing they can act on.
- **Gone cold** — `solid` concepts not tested in a long time, and topics with no session in weeks. Say it neutrally; this is information, not a reprimand.
- **Nearly done** — any topic one or two modules from complete, since that is usually the cheapest useful thing they could do next.

If a topic has a curriculum but no sessions, say so plainly: it was built and never started.

If there are no topics at all, say that and point at `/learn <concept>`.

## Close

Recommend one next action, specifically — a module to teach or a drill to run — rather than listing everything they could do. The point of this command is to answer "what should I do now?" in one line.
