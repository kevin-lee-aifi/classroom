---
name: learn
description: "Build a new learning curriculum in this repo from a concept and optional resources. Use when the user invokes /learn, or asks to start learning a new topic, build a curriculum, or study a paper. Runs a multi-agent build with an adversarial audit and writes a topic under topics/."
disable-model-invocation: true
argument-hint: <concept> [path-or-url to resources]
---

# Build a curriculum

The learner wants to learn: **$ARGUMENTS**

You are building a topic under `topics/<slug>/` that a later `/teach` session will deliver. You are not teaching now, and you are not writing a summary — you are building teaching material someone else (a future session, with no memory of this one) will run from.

Read `references/curriculum-shape.md` for the file layout, module template and conventions. Read `references/extraction-discipline.md` before touching any source document. Both are next to this file.

## Step 1 — Clarify, before building anything

Ask the learner, with `AskUserQuestion`, in one batch:

- **Depth and time budget.** Hours over how many weeks. This sets the module count.
- **What they already know.** The single most valuable input you will get, and the one you cannot infer. Ask what they do professionally and what adjacent methods they use daily. The exemplar curriculum works because it was built for someone who does single-cell sequencing, and every module bridges from that.
- **Hands-on or conceptual.** Whether they want exercises they run, or reading and reflection only.
- **Sources.** Whether you may retrieve outside material and cite it, or should work only from what they supplied.

If they gave you no resources, say what you intend to build the curriculum from and let them correct you. A curriculum assembled from model recollection is worth much less than one grounded in a document, and the learner deserves to know which they are getting.

## Step 2 — Extract and verify

Only if resources were supplied. Skip to step 3 otherwise.

Produce two artefacts in a scratch directory, and hand both to every downstream agent:

- **A verified-facts block** — every number and claim the curriculum will rest on, each with the figure or section it came from, extracted with `scripts/pdfx.py` and cross-checked. Downstream agents work from this rather than from their own recollection.
- **A corrections file** that overrides the facts block. It will be needed. On the build this system came from, the facts block was wrong three times and one item had to be retracted outright. Tell every agent explicitly which file wins.

Extract the source's own bibliography rather than reconstructing citations. Never write a DOI you did not read.

## Step 3 — Architect

Spawn the `curriculum-architect` agent. Give it the concept, the learner profile from step 1, the verified-facts block, and the time budget.

It returns a module sequence, an interleaving map, a prior-belief inventory, an analogy bridge with breakages, and its own top risks. Read its risks section properly — it is where the design is weakest.

## Step 4 — Show the skeleton and stop

Present the module list, objectives and hours. One screen. Then wait.

This gate exists because the build it came from wrote roughly 65,000 words before the learner saw a single module. Had the sequence been wrong, all of it was waste. This is where "based on user feedback" actually belongs — not after the prose exists, when nobody wants to throw it away.

Use `ExitPlanMode` if you are in plan mode; otherwise ask directly and wait for a real answer.

## Step 5 — Build

Write `topics/<slug>/notes/learning-plan.md` first — the syllabus, from the approved skeleton, including the interleaving map and the three teaching commitments.

Then spawn `module-author` agents **in parallel, partitioned by knowledge domain** rather than by source section, so that no module depends on one written later. Each gets: the verified-facts block, the corrections file, the approved skeleton, its own slice, the learner profile, and the standing citation rules.

Reserve two or three worked examples from the source as **held-out capstone cases** and tell every author not to use them — including not pointing at the figure panels that label them.

Then write the glossary and the question bank with model answers yourself, since both depend on all the modules.

## Step 6 — Audit

Spawn the `red-team` agent once every module exists. It writes `notes/misconceptions.md` and `notes/redteam-findings.md`.

Expect it to find real errors, including yours. On the source build it found sixteen, six of them the orchestrator's, two of which would have taught false numbers. If it comes back with nothing, something is wrong with how you briefed it.

## Step 7 — Fix round

Relay each finding to the agent that owns the file, using `SendMessage` so it corrects its own work with its context intact rather than you patching prose you did not write. Fix your own files yourself, and say so.

Verify the audit's claims before acting on them. One of its findings on the source build was itself wrong, and acting on it would have deleted correct content.

## Step 8 — Finish the topic

- `topics/<slug>/README.md` — the topic record: what it is, sources with real citations, key concepts, status `to-read`.
- `topics/<slug>/progress.md` — the learner record, seeded with every concept from the interleaving map at state `untested`. **Create this even though it is empty of results.** `/teach` reads it to know where to start, and a missing file means the first session has nowhere to write.
- `topics/<slug>/sessions/.gitkeep` — so the directory exists.

## Step 9 — Verify, then commit

Run these and report the numbers, rather than asserting the work is clean:

- Every relative link resolves.
- Conventions hold: one H1 on line 1, no `####`, no trailing whitespace, LF, single trailing newline.
- Held-out cases appear only in the capstone file.
- Every module heading matches the template names, since `/teach` finds them by heading.
- `progress.md` lists every concept in the interleaving map.

Then commit and push. Tell the learner what to run next: `/teach <slug>`.

## What good looks like

The exemplar is `topics/expanding-human-proteome-microproteins-peptideins/`. It survived a hostile audit. Read a module before writing your first one — particularly how it opens with a prediction the learner will probably get wrong, and how it closes on what they can now trust rather than on a list of demolished beliefs.
