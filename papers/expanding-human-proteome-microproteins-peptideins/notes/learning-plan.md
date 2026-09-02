# Learning Plan: Expanding the human proteome with microproteins and peptideins

## Goal

Understand this paper well enough to present it at journal club and defend it — to a proteomicist, a comparative genomicist and a gene-annotation curator in the same room. Not "know what it says": be able to say which of its numbers you would stand behind, why it produced only three new genes from 7,264 candidates, and what would change your mind.

Total ~18 hrs over 2 weeks. Reading and writing only — no code, no data downloads.

## How this plan works

Eight modules, ordered by prerequisite rather than by the paper's own section order. The paper opens with the consortium and the mass spectrometry; you will open with the figure closest to your own bench and work outward toward the assays you have never touched.

Three conventions run through every module:

- **Predict first.** Each module opens with a question you answer in writing *before* reading on. Being wrong first is the mechanism, not a formality — a confrontation you read passively does not change what you believe.
- **Close with what you trust.** Each module ends with a positive statement in your own words, never just a list of things that turned out to be false. A curriculum that only demolishes produces cynicism rather than understanding.
- **Analogies come with their breaking points.** Your single-cell background transfers unusually well here, and in a few places it will actively mislead you. Every bridge is marked with where it fails.

Read alongside the PDF, not instead of it. The notes deliberately do not reproduce figures — learning to read Fig. 5 in your own copy is part of the objective.

## The paper in one paragraph

A 61-affiliation consortium — TransCODE, working with GENCODE, PeptideAtlas, HUPO-HPP, HUPO-HIPP, HGNC, UniProt and RefSeq — asked which of 7,264 non-canonical open reading frames actually produce protein, by searching 3.5 billion mass spectra plus 240 million immunopeptidome spectra. About 25% yield a detectable peptide. They then built a six-tier evidence framework to decide what that entitles an ORF to, invented a new annotation class ("peptidein") for products that are confidently detected but whose function cannot be verified, developed a new evolutionary metric (ORBL) that scores conservation of *ORFness* rather than of amino-acid sequence, and put one peptidein from the OLMALINC lncRNA through functional genomics. The end result was 121 peptidein annotations and **three** new protein-coding genes. That ratio is the finding.

## Background Prerequisites

What you already have, and what is genuinely new. Check the second list honestly — the modules are sized on the assumption that these are unfamiliar.

Already yours, and load-bearing here:

- Central dogma, ORFs, and reading frames
- Reference GTFs and how a Cell Ranger reference is built — the annotation this paper changes *is* your GTF
- Count matrices, QC thresholds, pseudobulk differential expression, limma/edgeR
- CRISPR screen logic
- Probe and panel design for targeted spatial assays

New, and taught from scratch:

- [ ] Ribosome profiling — specifically sub-codon phase, which has no counterpart in 3′ or 5′ gene expression data
- [ ] Bottom-up mass spectrometry: digestion, MS1/MS2, PSMs, search databases
- [ ] Target–decoy FDR, and why a global error rate says little about a rare subset
- [ ] HLA class-I antigen processing and immunopeptidomics
- [ ] Codon-substitution models — PhyloCSF — and branch-length conservation
- [ ] Reference gene-annotation governance, and who has authority over what

## Schedule

### Week 1 — foundations and the hardest unfamiliar domain

| Module | Title | Hrs |
|---------|-------|-------|
| [1](01-annotation-problem.md) | The annotation problem — why the gene count is contested | ~1.5 |
| [2](02-ncorf-atlas-biotypes.md) | The ncORF catalogue — seven biotypes and where they sit | ~1.5 |
| [3](03-riboseq-bridge.md) | Ribo-seq, from a sequencing person's chair | ~2 |
| [4](04-mass-spec-proteomics.md) | Mass spectrometry — the evidence standard | ~3 |

Front-loading mass spectrometry is deliberate. It is your largest gap and it is where the paper's evidence standard lives, so Modules 5 and 8 both depend on it landing properly.

### Week 2 — the second window, interpretation, and synthesis

| Module | Title | Hrs |
|---------|-------|-------|
| [5](05-immunopeptidomics.md) | Immunopeptidomics — a second, stranger window | ~2.5 |
| [6](06-evolution-orbl.md) | Evolution — ORBL, constraint versus conservation | ~2 |
| [7](07-function-crispr-olmalinc.md) | Function — CRISPR screens and OLMALINC | ~2 |
| [8](08-tier-framework-synthesis.md) | The tier framework and what it commits you to | ~2 |
| [Capstone](journal-club.md) | Journal club and capstone | ~1.5 |

Read [misconceptions](misconceptions.md) at the end of Week 1 and again after Module 8 — once to be warned, once to check yourself.

## Modules

| File | Covers |
|---------|-------|
| [01-annotation-problem.md](01-annotation-problem.md) | Identification vs annotation · the institutions · vocabulary · Fig. 1a |
| [02-ncorf-atlas-biotypes.md](02-ncorf-atlas-biotypes.md) | The seven biotypes and counts · mixed-biotype ORFs · Fig. 1b |
| [03-riboseq-bridge.md](03-riboseq-bridge.md) | Footprinting · P-sites · periodicity · why Ribo-seq alone is Tier 4 · Fig. 2h, Fig. 6b |
| [04-mass-spec-proteomics.md](04-mass-spec-proteomics.md) | Bottom-up MS · PSMs · target–decoy FDR · HUPO-HPP · PRM · Fig. 2a–d, ED 1–3 |
| [05-immunopeptidomics.md](05-immunopeptidomics.md) | HLA-I processing · no-enzyme search · detection determinants · Fig. 2e–k, Fig. 3, ED 4–6 |
| [06-evolution-orbl.md](06-evolution-orbl.md) | PhyloCSF · ORBLv vs ORBLq · matched nulls · pLDDT · Fig. 4, ED 7, ED 10 |
| [07-function-crispr-olmalinc.md](07-function-crispr-olmalinc.md) | CRISPR screens · specificity controls · OLMALINC · Fig. 6, ED 9 |
| [08-tier-framework-synthesis.md](08-tier-framework-synthesis.md) | The six tiers · the 37 → 3 funnel · the seven open questions · Fig. 5 |
| [glossary.md](glossary.md) | Every term, defined as this paper uses it |
| [misconceptions.md](misconceptions.md) | Traps, and the beliefs this paper should overturn |
| [journal-club.md](journal-club.md) | Question bank with model answers, and the capstone |

## Concepts to Master

| Concept | Understood? | Notes |
|---------|-------------|-------|
| Protein identification vs protein-coding gene annotation | | |
| smORF / ncORF and the seven biotypes | | |
| Microprotein definition and size range | | |
| Peptidein — what it asserts and what it withholds | | |
| Ribosome profiling and sub-codon periodicity | | |
| Bottom-up MS: digestion → PSM | | |
| Target–decoy FDR and the base-rate problem | | |
| HUPO-HPP criteria and why microproteins fail them | | |
| HLA-I immunopeptidomics as proteasome output | | |
| Why the headline 25% is carried by immunopeptidomics | | |
| ORBLv vs ORBLq; constraint vs conservation | | |
| PhyloCSF and its short-ORF power problem | | |
| What a CRISPR fitness screen can and cannot prove | | |
| The six-tier framework and provisional vs final tiers | | |
| The 37 → 20 → 15 → 3 funnel and its rejection reasons | | |
| The sample-provenance problem (66.9% cancer spectra) | | |
| The seven open governance questions | | |

## Progress

- [ ] Module 1 — the annotation problem
- [ ] Module 2 — the ncORF catalogue
- [ ] Module 3 — Ribo-seq
- [ ] Module 4 — mass spectrometry
- [ ] Module 5 — immunopeptidomics
- [ ] Module 6 — evolution and ORBL
- [ ] Module 7 — function, CRISPR and OLMALINC
- [ ] Module 8 — the tier framework
- [ ] Misconceptions — read twice
- [ ] Capstone A — the unseen case dossier
- [ ] Capstone B — the referee report
- [ ] Capstone C — teach it
- [ ] Update the [paper README](../README.md) status to `read`

## Follow-up Resources

- [Key references](../resources/key-references.md) — grouped by module, with three to read first
- The paper's own tools: the ncORF PeptideAtlas build, and the ORBL implementation. Both are linked in key references.

## Summary (fill in after reading)

<!-- Write a 1–2 paragraph plain-language summary of the paper here, in your own words, without looking at the modules -->
