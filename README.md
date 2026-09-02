# Classroom

A guided-learning system. Name a concept, get a curriculum built for what you already know, then be taught it across sessions — tested as you go, with each module reinforcing what earlier ones exposed as weak.

It runs on Claude Code opened in this repo. Sessions have no memory of each other, so everything the tutor knows about you lives in files here.

## Using it

```
/learn <concept> [resources]   build a new topic — asks what you already know first
/teach                         a guided session; resumes where you left off
/review                        a short drill on what you are shaky on
/progress                       where you are up to
```

`/learn` takes a paper, a URL, or nothing at all. It asks about your background and time budget, shows you a module skeleton for approval, and only then writes the material — so a wrong sequence costs a minute rather than a day.

`/teach` opens by drilling what you got wrong last time, checks whether the module's prerequisites actually landed, teaches conversationally, tests you, and writes down what happened. That last part is what makes the next session useful.

## Structure

```
topics/
  <slug>/
    README.md          — topic record: sources, key concepts, status
    progress.md        — the learner record: what stuck, what didn't
    notes/
      learning-plan.md — syllabus: modules, prerequisites, interleaving map
      NN-<name>.md     — the modules
      glossary.md · misconceptions.md · journal-club.md
    sessions/          — one file per session, written at the time
    resources/         — source documents and references
.claude/
  skills/              — learn · teach · review · progress
  agents/              — curriculum-architect · module-author · red-team
  hooks/               — session greeting
```

## Conventions

- One folder per topic, named as a lowercase hyphenated slug.
- `progress.md` is the authoritative record of what you know. Correct it by hand whenever it gets you wrong.
- Learning status: `to-read` → `reading` → `read`.
- `CLAUDE.md` carries the formatting and teaching conventions any session here should follow.

## How curricula get built

`/learn` runs a curriculum architect, several module authors in parallel, and then an adversarial reviewer whose standing instruction is to treat its own brief as suspect and audit the orchestrator's files as harshly as anyone's.

That last agent is the reason to trust the output. On the build this system was derived from it found sixteen issues — six of them the orchestrator's own, two of which would have taught false numbers, and one that would have deleted correct content. Each topic keeps that audit as `notes/redteam-findings.md`, so you can see what was verified rather than taking it on trust.

## Topics

- [Expanding the human proteome with microproteins and peptideins](topics/expanding-human-proteome-microproteins-peptideins/README.md) — eight modules, ~18 hrs. The worked exemplar.
