# Expanding the human proteome with microproteins and peptideins

## Metadata

| Field   | Value |
|---------|-------|
| **Title** | Expanding the human proteome with microproteins and peptideins |
| **Authors** | Eric W. Deutsch, Leron W. Kok, Jonathan M. Mudge, Cristian F. Valls, Irwin Jungreis *et al.* (TransCODE Consortium; 61 affiliations). Corresponding: Robert L. Moritz, John R. Prensner, Sebastiaan van Heesch |
| **Year** | 2026 |
| **Journal / Venue** | Nature, pp. 813–826 (+ Methods and Extended Data Figs 1–10; 47 pp.) |
| **DOI / URL** | [10.1038/s41586-026-10459-x](https://doi.org/10.1038/s41586-026-10459-x) |
| **Dates** | Received 7 September 2024 → accepted 27 March 2026 → published online 6 May 2026 |
| **Licence** | Open access, CC BY-NC-ND 4.0 |
| **Status** | `to-read` |

## Abstract

Quoted under the article's CC BY-NC-ND 4.0 licence; © The Author(s) 2026. Wording is unaltered; the original's superscript reference markers are omitted.

> A major scientific drive is to characterize the protein-coding genome, which is a primary basis for studying human health. But the fundamental question remains of what has been missed in previous analyses. Over the past decade, the translation of non-canonical open reading frames (ncORFs) has been observed across human cell types and disease states, with major implications for biomedical science. However, a key gap in knowledge has been which ncORFs produce small microproteins or alternative protein molecules that contribute to the human proteome. Here we report the collaborative efforts of the TransCODE Consortium to produce a consensus landscape of protein-level evidence for ncORFs. We show that about 25% of a set of 7,264 ncORFs gives rise to detectable peptides in a large-scale analysis of 95,520 proteomics experiments. We develop an annotation framework for ncORF-encoded microproteins as human proteins and codify the new conceptual model of peptideins as microproteins that have indeterminate potential as functional proteins. To probe the biological implications of peptideins, we create an evolutionary analysis approach, termed ORF relative branch length (ORBL), and determine that evolutionary constraint is common and associates with observation of ncORF-derived peptides. We then characterize a pan-essential cellular phenotype for one peptidein from the OLMALINC long non-coding RNA. Overall, we generate public research tools supported by GENCODE and PeptideAtlas and advance biomedical discovery for understudied components of the human proteome.

## Key Concepts

- Non-canonical open reading frames (ncORFs) and their seven biotypes — `uORF`, `uoORF`, `intORF`, `doORF`, `dORF`, lncRNA ORF, processed-transcript ORF
- Microproteins (small ORF-encoded peptides, SEPs, micropeptides)
- **Peptidein** — a microprotein confidently detected endogenously but whose role in normal physiology cannot presently be verified
- Protein *identification* versus protein-coding gene *annotation* — the paper's central distinction
- The six-tier evidence framework, and provisional versus final tier assignment
- HUPO-HPP verification criteria (≥2 non-nested non-HLA peptides of ≥9 aa, together spanning ≥18 aa)
- Bottom-up mass spectrometry, PSMs, and target–decoy FDR at scale
- HLA class-I immunopeptidomics as a readout of proteasome output
- `ORBL` — conservation (`ORBLv`) and constraint (`ORBLq`) of *ORFness*, as distinct from amino-acid conservation
- Reference gene-annotation governance — GENCODE, UniProtKB, HGNC, RefSeq, HUPO-HPP, HUPO-HIPP

## Notes

- [Learning plan](notes/learning-plan.md) — the 2-week syllabus
- [Progress](progress.md) — the learner record: what stuck, what didn't
- [Glossary](notes/glossary.md)
- [Misconceptions to unlearn](notes/misconceptions.md)
- [Journal club and capstone](notes/journal-club.md)
- [Audit record](notes/redteam-findings.md) — what was verified against the PDF, and what was corrected
- [Key references](resources/key-references.md)

## Questions to Answer

- What distinguishes a microprotein from a peptide or canonical protein? → [Module 1](notes/01-annotation-problem.md), [Module 2](notes/02-ncorf-atlas-biotypes.md)
- What methods are used to identify microproteins experimentally? → [Module 3](notes/03-riboseq-bridge.md), [Module 4](notes/04-mass-spec-proteomics.md), [Module 5](notes/05-immunopeptidomics.md)
- What is a "peptidein" and how does it differ from a microprotein? → [Module 8](notes/08-tier-framework-synthesis.md)
- What is the biological significance of proteome expansion through these elements? → [Module 6](notes/06-evolution-orbl.md), [Module 7](notes/07-function-crispr-olmalinc.md)
- Why did only 3 of 7,264 candidates become protein-coding genes? → [Module 8](notes/08-tier-framework-synthesis.md)
