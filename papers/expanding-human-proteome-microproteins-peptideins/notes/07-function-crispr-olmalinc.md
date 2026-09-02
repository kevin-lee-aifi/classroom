# Module 7 — Function: CRISPR screens and OLMALINC

~2 hrs. Prerequisites: [Module 1](01-annotation-problem.md) for the puzzle this module closes, [Module 6](06-evolution-orbl.md) for ORBLq and for the matched-null habit you are about to use a fifth time.

Covers Fig. 6a–j, Extended Data Fig. 9a–p, the results sections "Functional genomics augments annotation" and "OLMALINC produces an essential peptidein", and the Methods subsections "CRISPR screening", "Analysis of CRISPR screening data", "Meta-analysis of CRISPR data", "Analysis of CRISPRa data", "CRISPR tiling analysis and functional enrichment score for ncORF", "Pooled c10riboseqorf92 knockout", "Analysis of pooled c10riboseqorf92 knockout data" and "Multiplexed single-cell transcriptional response".

[Module 1](01-annotation-problem.md) opened with `c10riboseqorf92` and left it open on purpose. You have been carrying it for six modules. This module resolves the experimental half of the question — is the phenotype caused by the peptide? — and hands the annotation half to [Module 8](08-tier-framework-synthesis.md).

It also asks you to do something uncomfortable in the second half, and that part is the real objective.

## Predict first

Write these down before reading on.

1. A single guide RNA cutting a uORF in a 5′-UTR cuts the same DNA, and disrupts the same mRNA, as the host CDS. List every control you would demand before accepting that a fitness phenotype belongs to the uORF rather than to the host gene. Aim for four. Number them.
2. Over 2,000 ncORFs were screened across 8 cell lines. How many show a pan-essential knockout signature? Write a number.
3. Of those, how many have HLA peptide evidence for their microprotein? Write a number.
4. `c2riboseqorf47` was promoted to a protein-coding gene on the strength of this work. How many tryptic mass-spectrometry peptides does it have? Write a number.
5. Would you accept a CRISPR fitness screen as "evidence of function" sufficient for a protein-coding gene annotation? Write `yes`, `no` or `qualified`, plus one sentence.

Question 1 is the whole module. Keep your list visible — you will score it against the paper's, and the gaps in both directions are informative.

## The screen

From the Methods subsections "CRISPR screening" and "Lentiviral transduction for CRISPR screens". Read the design before the results, because the most important specificity control is in the library, not in the analysis.

**What was targeted.** 2,196 ncORFs selected from the GENCODE Phase I catalogue plus 1,245 ncORFs carried over from a previously published ncORF guide library (ref. 7 — Hofman *et al.*, *Mol. Cell* **84**, 261–276, 2024). The selection rules:

- Maximum three ncORFs per gene.
- **Exclude all `intORF`s, and any `doORF` or `uoORF` with ≥25% overlap with the main CDS.**
- Minimum ncORF size of 12 amino acids, so that enough guide sites exist.
- Exclude ncORFs with fewer than four predicted targeting guides.

Stop on the second rule. This is a specificity decision taken at design time: an `intORF` sits inside a coding exon, in a different frame, and there is no cut site that hits the ncORF and not the CDS. Rather than screen them and then try to argue the phenotype apart, the authors **did not screen them**. If your prediction-1 list did not include "some biotypes are not separable in principle and should be excluded before you start", add it now. It is the cheapest control in the paper and the one most often skipped.

The tier composition of the 2,196 GENCODE Phase I selections is printed in the Methods and sums correctly: Tier 1A 4 · 1B 224 · 2A 13 · 2B 373 · 3 13 · 4 34 · no tier 1,535. Note how few top-tier ncORFs are in there — the screen was not built to confirm the well-evidenced ones.

**The library.** 27,464 barcoded sgRNAs designed with CRISPick against GRCh38 (Ensembl v108), `CRISPRko`, SpyoCas9 (NGG), with these modifications: for multi-exon ncORFs the guides may not all come from one exon; a target of 6 guides per ncORF and 3 per parental CDS; guide-separation spacing relaxed to 1% of target length for ORFs and held at 5% for parental CDSs; a 2:1 on-target to off-target ratio; guides with ≥5 predicted genomic mapping sites removed. Controls carried over from ref. 7: 471 pan-essential guides, 503 non-targeting guides without genome cutting, and 497 non-targeting guides **with** genome cutting.

That last control class is worth naming. A cutting-but-non-targeting guide separates "Cas9 made a double-strand break" from "Cas9 made a double-strand break *here*". Without it, every hit is confounded with break toxicity, which in some lines is substantial.

**Execution.** Biological triplicate; MOI 0.3–0.5 tuned per line to 30–50% infection efficiency; representation of 500 cells per guide after puromycin selection; initial timepoint collected after 7 days of selection; final collection about 14 days after infection. Eight cell lines: `A375`, `A549`, `A673`, `CADO-ES1`, `HepG2`, `Jurkat`, `RD-ES`, `THP-1` (Fig. 6a).

**Analysis.** Guides mapped with Bowtie2 under stringent settings, intersected with GENCODE v45 plus GENCODE Phase 1 ORF definitions; guides mapping to more than five genomic coordinates dropped; ORFs with fewer than three surviving guides dropped; guides with counts more than 3 s.d. below total dropped. Fitness scores from Chronos v2.0.8 with DepMap copy-number data (CNV set to 1 where unavailable); loss-of-function hits at Chronos < −0.5. Screen quality assessed by mean median absolute deviation between positive and negative controls.

The copy-number step matters more here than in a standard screen. Amplified regions deplete more slowly and deleted regions faster for reasons that have nothing to do with the gene, and ncORFs are disproportionately in lncRNA loci where a whole-gene dependency baseline does not exist to calibrate against.

## The specificity problem

Here is the intellectual core of the module, stated as flatly as possible.

**A guide cutting a uORF in a 5′-UTR is cutting the same molecule as its host CDS.** The cut produces an indel in the 5′-UTR of an mRNA that also encodes a canonical protein. That indel may destroy the uORF's start codon or shift its frame. It may also disrupt 5′-UTR secondary structure, a Kozak context, a TOP motif, an internal ribosome entry site, an exon–intron boundary, a splice enhancer, or a transcription factor footprint in a promoter-proximal exon. Any of those can change the amount of canonical protein the cell makes. All of them produce the same observable: guides at that locus deplete.

**A locus-level phenotype does not localise to the ORF.** Nothing in a dropout measurement tells you which molecule mattered. And the null hypothesis is not "nothing happens" — it is "something at this locus matters, and it is not the microprotein". That is a substantive, plausible alternative, and it is the default for a 5′-UTR, because 5′-UTRs are dense with regulatory elements whether or not they contain a translated ORF.

This is why "we found ncORF hits in a CRISPR screen" is not, on its own, a claim about microproteins at all. Everything below is the work required to convert a locus-level observation into an ORF-level one.

### The ladder of controls, and what each one rules out

The paper's stated workflow is five steps (Fig. 6a; results, "Functional genomics augments annotation"), plus the design-time exclusion above and one orthogonal-modality check. Score your prediction-1 list against these.

**(0) Design-time exclusion.** All `intORF`s and heavily CDS-overlapping `uoORF`/`doORF`s are absent from the library.
*Rules out:* the cases where ORF-level attribution is impossible in principle. *Cost:* the catalogue's 720 `intORF`s and a fraction of its `uoORF`s and `doORF`s are simply unaddressable by this assay, which is a permanent gap and not a temporary one.

**(1) Expression and translation filtering in the actual cells.** Hits were cross-validated against RNA-seq and Ribo-seq from the same 8 lines: only targets with **≥10 TPM in RNA-seq and ≥5 TPM in Ribo-seq** were retained (Methods, "Analysis of CRISPR screening data"; Extended Data Fig. 9c shows the cumulative distributions and the thresholds, and 9c-right and 9d show the hit counts by biotype before and after).
*Rules out:* hits at loci that are neither transcribed nor translated in the screened cells — which is to say, hits that must be off-target effects, copy-number artefacts or noise, since there is no target present to knock out. *Does not rule out:* anything about specificity. This is a presence filter. An expressed, translated locus can still produce a phenotype through its CDS.

Note the Ribo-seq requirement specifically. Requiring translation *in the cells being screened*, not merely somewhere in the aggregate catalogue, is stronger than most published ncORF screens manage, and it is the step that makes the rest of the ladder worth climbing.

**(2) Separating the ncORF effect from the adjacent CDS.** Normalised phenotypic effects were computed by **subtracting the Chronos score of the associated canonical CDS from that of the ncORF**, applied only to ncORFs shown to be co-transcribed with a canonical ORF so that shared transcript context is preserved (Methods, "Analysis of CRISPR screening data"). Extended Data Fig. 9e plots this with error bars across the 8 lines, marking ncORFs whose effect is stronger than the CDS (purple, < −0.5) or weaker (green, > 0.5). The main text puts it as: "We additionally ensured that the phenotypic effect of uORF knockout was distinct from that of the adjacent coding region on that mRNA."
*Rules out:* the trivial case where cutting anywhere in the transcript kills the cell because the canonical protein is essential. If ncORF guides and CDS guides deplete equally, the subtraction returns zero and the ncORF is not a hit. *Does not rule out:* the ncORF guides disrupting a *different* 5′-UTR element — one that changes CDS output without the CDS itself being an essential gene. The subtraction handles a shared-essentiality confound, not a shared-regulation confound.

**(3) CRISPRa, against the de-repression hypothesis.** This is the most specific control in the paper and the one least likely to be on your list, so work through the logic.

The canonical function of a uORF is to **repress** translation of the downstream CDS by capturing scanning ribosomes. Destroy the uORF and you *increase* CDS output. If that CDS happens to be anti-proliferative, then knocking out the uORF causes a fitness defect — and the defect has nothing to do with losing the microprotein. It is a consequence of over-producing a canonical protein. This is a complete, mechanistically sound alternative explanation for every essential uORF in the screen, and no amount of CDS subtraction touches it, because the CDS is not essential in this scenario; it is toxic when overexpressed.

The test is to overexpress the CDS directly and see whether that is anti-proliferative. Which is what CRISPR activation does. The authors reanalysed the human CRISPRa Calabrese (P65-HSF) pooled library data (ref. 31 — Sanson *et al.*, *Nat. Commun.* **9**, 5416, 2018), reprocessing the Meljuso and A375 screens through Chronos after removing low-representation targets (Methods, "Analysis of CRISPRa data"). Result: "little evidence for anti-proliferative CDSs adjacent to essential uORFs" (Extended Data Fig. 9e,f; 9f is the scatter of standardised knockout effects in A375 against CRISPRa fitness scores).
*Rules out:* the de-repression explanation, as a class, for the essential-uORF set. *Limits:* CRISPRa drives transcription from the endogenous promoter, which is not the same perturbation as relieving a uORF's translational brake; the magnitudes and the isoform mix differ. And "little evidence" is a population statement — it does not clear any individual uORF.

**(4) Tiling screens with a gene-specific local-background permutation test.** Two published CRISPR tiling screens (refs 7 and 28) were reprocessed (Methods, "CRISPR tiling analysis and functional enrichment score for ncORF"; workflow in Fig. 6c). The pipeline: log2 fold change late versus input or earliest timepoint; low-representation guides excluded; depth corrected to CPM; normalised so that the geometric mean of positive-control (pan-essential) guides anchors dropout at −1, making magnitudes comparable across experiments; ORF-level effects denoised with empirical Bayes shrinkage in `ashr` v2.2.63 against a fitted global prior; for ORFs with more than six guides, MAD-based filtering of outlier guides.

Then the test that matters. **For an ncORF with *n* guides, the null distribution is built by resampling *n* guides from all guides targeting the same parental gene**, over typically 1,000–4,000 iterations, with `P = (1 + number of null statistics ≥ observed) / (1 + B)` one-sided, converted to two-sided as `2 × min(P, 1 − P)`. Fig. 6d shows the output for HepG2; Extended Data Fig. 9i is the equivalent heatmap for A375, HepG2 and MCF7 from ref. 28.
*Rules out:* the possibility that guides inside the ORF are no more depleting than guides elsewhere in the same locus. That is precisely the shared-regulation confound step (2) could not reach.

And notice what this is. The comparison set is matched on the one variable that would otherwise explain everything — being in this gene — and the score is a quantile against it. **This is ORBLq again**, in a domain with no phylogeny in it: raw log2 fold change is the magnitude, the permutation *P* is the magnitude relative to a matched null, and the matching variable is "same parental gene" instead of "same biotype and length". [Module 6](06-evolution-orbl.md) argued that a score is evidence only against a matched null. Here is the fifth instance, and it is the single step that makes the localisation claim possible.

**(5) Meta-analysis across 25 datasets from three studies.** The paper's main text calls this "a meta-analysis of 25 CRISPR screens", but the Methods are more precise and you should quote the Methods: three independent CRISPR studies — refs 7, 28 and the screen generated for this study — were integrated by remapping all guides to GRCh38 against GENCODE v45 plus Phase 1 ncORF annotations, dropping guides with more than five genomic loci or poor alignment, then recomputing gene-level essentiality with Chronos using DepMap release 25Q2 copy-number data. Chronos < −0.5 counts as a hit, following the tool authors' recommended threshold, and **an ORF essential in ≥60% of samples is called pan-essential** (Methods, "Meta-analysis of CRISPR data"; Fig. 6e ranks ncORFs by the number of the 25 datasets in which they score < −0.5, with the ≥60% set marked in green).
*Rules out:* single-screen noise and cell-line idiosyncrasy. *Note:* pan-essentiality is a deliberately narrow target — the authors chose it because pan-essential proteins are central to core cell functions and common drug targets (refs 29, 30). Any ncORF whose function is conditional, tissue-specific or stress-induced is invisible to this design by construction. The screen is not a survey of ncORF function; it is a search for one particular signature.

**(6) An orthogonal perturbation modality.** Cas9 knockout was compared against Cas13 RNA-targeting data (ref. 85 — Wessels *et al.*, *Nat. Biotechnol.* **38**, 722–727, 2020); `THP-1` was the only cell line shared between the platforms, so the comparison was restricted to it, using normalised gene-level depletion scores on shared high-confidence targets (Methods, "Comparison of CRISPR–Cas9 with Cas13 data"; Extended Data Fig. 9j).
*Rules out:* DNA-level artefacts specific to cutting — break toxicity, indel-dependent splicing changes, CNV interactions. *But note the trade:* Cas13 degrades the transcript. It therefore cannot distinguish an RNA-mediated function from a peptide-mediated one **at all** — it destroys both. Concordance between Cas9 and Cas13 strengthens the locus claim and weakens nothing about the peptide-versus-RNA question. Getting this backwards is easy.

### What the full ladder actually establishes

Put all seven together and the honest statement is:

> Cutting inside this ORF, at a locus that is transcribed above 10 TPM and translated above 5 TPM in these cells, depletes cells more than cutting elsewhere in the same locus, in most cell lines tested, across three independent screening studies, and is not explained by the adjacent CDS being essential or by that CDS being anti-proliferative when overexpressed.

That is a strong, well-controlled, locus-level claim, and it is more than most published ncORF screens support. It is still not "the microprotein does something". The gap between those two sentences is where the last two sections of this module live.

**Result.** 51 ncORFs exhibit a pan-essential knockout signature (Supplementary Table 13). Of those, **six** qualified as candidate peptideins or protein-coding genes on the basis of HLA peptide evidence for their encoded microproteins, and the six segregate cleanly on evolutionary constraint: four with ORBLq > 0.9, two with ORBLq < 0.7 (Fig. 6a; Extended Data Fig. 9g, which plots average loss-of-function effect against `−log10[1 − ORBLq]` with dot size for the number of essential cell lines). Two of the six are `c2riboseqorf47` and `c10riboseqorf92`, the two cases below; `c6norep15` is the other low-ORBLq member. One of the remaining three is held for your capstone, so I am not discussing it here. Its identifier does appear among the ncORF labels in this paper's figures, so if you want to meet that case cold, resist reading ORF labels closely until you have written the capstone dossier.

Compare against predictions 2 and 3. Over 2,000 ncORFs screened → 51 pan-essential → 6 with peptide-level support. If your numbers were larger, the thing to notice is that this is the same shape as the funnel in [Module 8](08-tier-framework-synthesis.md): a very large input, an aggressive series of independent filters, and a single-digit output.

## The success case: c2riboseqorf47

A Tier 1B uORF in the `GMCL1` gene. Fig. 6b prints its evidence in one panel: frame-coloured Ribo-seq P-site coverage on top, the amino acid sequence with the observed HLA peptides beneath it, and at bottom right the loss of fitness from perturbing the annotated CDS (orange) versus the ncORF (green) across the 8 lines.

The sequence as printed in Fig. 6b is 19 residues followed by a stop, with the HLA peptides tiling its C-terminal two-thirds. Take that length from the figure rather than from me — the authoritative record is now GENCODE and Supplementary Table 6 — but hold the order of magnitude, because it is the point.

The evidence assembled for it (results, "Functional genomics augments annotation"):

- A loss-of-function CRISPR phenotype, distinct from the adjacent CDS.
- A high ORBLq score (> 0.9) — ORF-level constraint across placental mammals.
- A **positive** `PhyloCSF` score. Unusual in this catalogue: only 143 of 7,264 ncORFs reach `PhyloCSF` per codon > 10 ([Module 6](06-evolution-orbl.md)), so this ORF has amino-acid-level constraint as well as frame-level constraint.
- Ribo-seq P-site density showing conserved translation across five species (Extended Data Fig. 9h). Not conservation of sequence — conservation of the *act* of translating it. That is a different and rather stronger observation than an alignment score.
- Both HLA-I **and** HLA-II peptides (Supplementary Table 6), which the authors read as suggesting "production of a stable microprotein that can be presented from both intracellular and extracellular sources". Two independent antigen-processing pathways handled this product, which is hard to reconcile with a transient, immediately-degraded translation artefact.
- **Zero tryptic MS peptides.** That is the answer to prediction 4.

GENCODE have now annotated it as protein-coding gene `ENSG00000310604`.

### Why this could not have happened under the old standard

Work out the arithmetic. HUPO-HPP protein verification requires two peptides of ≥9 amino acids spanning ≥18 amino acids of the ORF (agenda question 1). A 19-codon ORF has essentially no room to satisfy that even in principle — and it has no tryptic peptides at all, for the technological and biological reasons the Discussion lists: small size, amino acid composition, and possibly low stability with BAG6-mediated proteasomal degradation (refs 19, 21). Under the conventional standard this ORF is not merely unproven; it is **unprovable, permanently**, at any instrument sensitivity.

What got it over the line was three axes of evidence that the conventional standard does not use:

- ORF-level evolutionary constraint, from a method that did not exist before this paper;
- functional inference from CRISPR screening, with the specificity ladder above;
- immunopeptide support, which the annotation projects explicitly do not count as *function* but which they do accept as evidence of *existence*.

The Discussion says this in as many words: the development of ORBL, the assessment of CRISPR-based functional inference and the prioritisation of HLA immunopeptide support "were central to the establishment of c2riboseqorf47 as a protein-coding gene (GMCL1 uORF), despite there being no tryptic MS peptides and there being ambiguous amino acid evolutionary constraint when using conventional approaches."

This is the single best demonstration in the paper that the new evidence framework does work that the old one could not. Keep it, because the next case is the opposite result from a superficially stronger dossier, and the contrast is the lesson.

## The contrasting case: c10riboseqorf92

[Module 1](01-annotation-problem.md) laid out the dossier. Here is what each piece of it actually establishes, and where it stops.

**The locus.** A 123-amino-acid ORF on the `OLMALINC` transcript — `ENSG00000235823`, also known as `LINC00263` — an lncRNA carrying **six** ncORFs recognised by GENCODE. Fig. 6f names all six along the transcript diagram: `c10riboseqorf90`, `c10riboseqorf91`, `c10riboseqorf92`, `c10norep140`, `c10norep141`, `c10norep142`. Only `c10riboseqorf92` scores as a pan-essential dependency (Fig. 6e).

That within-transcript result is a control in its own right, and a good one. Six ORFs, one RNA, one phenotype. Whatever is essential here is not "the OLMALINC locus is required" in some diffuse sense, or all six would move together.

**Pan-essentiality across the cell-line panel.** A pooled knockout in the PRISM barcoded panel (Methods, "Pooled c10riboseqorf92 knockout"): 486 barcoded human cancer cell lines pooled and grown together; two independent guides against `c10riboseqorf92` plus a non-cutting LacZ control and a cutting Chr2-2 control; MOI 10; pellets at days 6, 10 and 15; cell-line abundance read out by barcode RNA expression.

Now check the counts yourself, because they do not fully reconcile and you should know it.

- Methods, "Analysis of pooled c10riboseqorf92 knockout data": "At day 15/20, **471 out of 486** cell lines were detectable and were used for data analysis."
- Main text: "we performed c10riboseqorf92 knockout in **over 485 cell lines**, observing a loss-of-viability phenotype in **415 cell models (85.6%)**."
- Fig. 6g: "485 pooled CRISPR screen cell lines (DepMap)". Extended Data Fig. 9m: "across 485 cell lines targeted with two independent sgRNAs".

`415 / 485 = 85.6%`, so the reported percentage is internally consistent with the 485 denominator. But 485 is larger than the 471 the Methods say survived detection, and outlier exclusion (cell lines with absolute residuals beyond two standard deviations in a regression of guide-2 viability on guide-1 viability, plus lines with missing values) can only shrink that number further. So the figure and main-text denominator of 485 and the Methods' 471 do not reconcile, and the paper does not say which set the 415 was counted in. The pan-essentiality conclusion is unaffected — 415/471 is 88.1%, which is if anything stronger — but this is exactly the sort of thing to have in hand at journal club, and the honest version of the claim is "loss of viability in roughly 85–88% of several hundred cancer cell lines" rather than a specific fraction.

Guide-to-guide agreement across lines is r = 0.77 (Extended Data Fig. 9m), and the distributions of fitness effect at days 15 and 20 are in 9n.

**The tiling screen.** Fig. 6d shows the tiling enrichment scores in HepG2, with significance from the gene-specific local-background permutation test described above; Extended Data Fig. 9i is the A375/HepG2/MCF7 heatmap from ref. 28. `c10riboseqorf92` shows selective loss of fitness against its own locus background. Fig. 6d labels a second ncORF alongside it; that one is a capstone case and I am leaving it unnamed.

**Cas13 concordance.** Extended Data Fig. 9j places `c10riboseqorf92`/`OLMALINC` on a scatter of Cas9 knockout against Cas13 RNA-targeting fitness effects for lncRNAs. As noted above, this corroborates the locus and is silent on peptide-versus-RNA.

**DepMap co-essentiality.** The knockout viability profile was correlated against DepMap release 25Q2 gene-level dependency scores — Spearman correlation of `c10riboseqorf92` against **17,110 genes across 485 cell lines**, with the top 0.5 percentile highlighted at ρ > 0.3 (Fig. 6g; Methods, "Analysis of pooled c10riboseqorf92 knockout data"). The main text reads this as "an enrichment for genes that are involved in mitosis and DNA damage regulation".

Do one thing here rather than accepting it: read the gene labels printed in Fig. 6g and ask whether they are the mitosis-and-DNA-damage set the sentence describes, or whether that characterisation comes from the full ranked list in Supplementary Table 13 rather than from the labelled points. Co-essentiality profiling is a genuinely powerful method — it is how the function of many uncharacterised genes was first guessed — but it is also a correlation across a cell-line panel with strong global structure, in which any pan-essential perturbation correlates with every other pan-essential perturbation to some degree. A top-0.5-percentile threshold at ρ > 0.3 is a permissive cut.

### The load-bearing experiment

Everything above is locus-level. This is the one experiment that reaches the ORF.

Re-expressing the `c10riboseqorf92` **coding sequence** from a separate construct rescues the loss-of-viability phenotype caused by siRNA silencing of the `OLMALINC` transcript (Fig. 6f; validation in Extended Data Fig. 9k,l). The design: isogenic A375 cells expressing either GFP or the `c10riboseqorf92` coding sequence, each treated with control siRNA or one of two independent siRNAs against `OLMALINC` (siRNA #10 and #11, from a panel of four tested in A375 and A549 for knockdown efficiency); knockdown confirmed by qPCR against GAPDH (Extended Data Fig. 9k, n = 4); proliferation followed as confluence normalised to initial measurement (Extended Data Fig. 9l). Fig. 6f reports relative proliferation rate, n = 4 biological replicates per condition, two-sided Welch *t*-test: **two significant *P* values in the GFP background (5.3 × 10⁻⁴ and 3.9 × 10⁻³) and two non-significant ones in the `c10riboseqorf92` background (0.23 and 0.64)**. The main text's reading: this indicates "an ORF-specific function".

Understand precisely why this design separates peptide from RNA, because it is the most elegant thing in the figure.

siRNA destroys the transcript. If `OLMALINC`'s essential activity were **RNA-mediated** — the lncRNA acting as a scaffold, a decoy, a *cis*-regulator of its neighbours, a chromatin tether — then supplying the ORF's coding sequence from a separate locus restores none of that. The RNA is still gone; its structure, its neighbourhood, its interaction surfaces are all still gone. The phenotype should persist. That the phenotype is **abolished** by supplying only the coding sequence means the thing that transcript was needed for, in this assay, is reconstituted by expressing that ORF somewhere else. Position-dependent RNA functions are excluded by construction.

**Where it stops, and say this out loud.** The rescue construct is a coding sequence, and a coding sequence is also RNA. A rescue by the CDS shows that this stretch of sequence, expressed ectopically, is sufficient to restore viability. It does not by itself establish that the **peptide** rather than some sequence element inside the CDS — a microRNA site, a structured motif, an RNA-binding-protein footprint — is the active moiety. The clean version of the experiment is a rescue with a construct that is sequence-identical but cannot be translated: a start-codon mutant, or a frameshift or premature stop that preserves most of the RNA sequence while abolishing the polypeptide. If the ATG-mutant construct fails to rescue while the wild-type construct rescues, the peptide is the active moiety and the argument is closed. **The paper does not report that experiment.** It is the single most valuable missing control in the OLMALINC section, and it is worth knowing what it would cost: one plasmid.

### The transcriptional work

Two experiments, in increasing order of ambition and decreasing order of power.

**Bulk RNA-seq recovery assay (Fig. 6h).** Isogenic A375 expressing GFP or `c10riboseqorf92`, each under `OLMALINC` knockdown, n = 3 per condition. Poly(A) libraries, STAR two-pass, RSEM against GENCODE v45, DESeq2 v1.46.0 with the multifactorial design `~ treatment + background + treatment:background` and apeglm shrinkage; Hallmark gene sets via clusterProfiler.

Result: **513 genes up and 456 genes down** in `c10riboseqorf92`-expressing versus GFP-expressing cells under `OLMALINC` knockdown, with **14 genes showing a statistically significant interaction *P* < 0.05**. Fig. 6h plots each gene's log2 fold change in GFP against its log2 fold change in ORF-expressing cells, with a linear fit at R² = 0.722, the top 5% of residuals in red, and the significant interaction hits circled. Extended Data Fig. 9o is the PCA. GO/Hallmark associations: hypoxia, glycolysis, DNA damage response through ultraviolet exposure, and TNF signalling via NF-κB.

Read the two numbers against each other. 969 genes move; 14 have a significant interaction term. The interaction term is the one that asks the actual question — does the ORF change how the cell responds to losing `OLMALINC`? — and the answer is 14 genes at an unadjusted *P* < 0.05. With around 15,000–20,000 genes tested, 14 hits at unadjusted *P* < 0.05 is at or below what you expect by chance. The 969-gene marginal comparison is the well-powered part of that panel and the least interpretable, and the interaction test is the interpretable part and the least powered. The R² = 0.722 concordance line is arguably the most informative thing in the panel: the two backgrounds respond to knockdown *similarly*, which is a modest result honestly displayed.

**Multiplexed single-cell knockout (Fig. 6i–j).** [Module 1](01-annotation-problem.md) walked the design; the result is that mitosis- and chromosome-related processes go **up** on knockout across cell lines while translation- and metabolism-related processes go **down** (results, "OLMALINC produces an essential peptidein"; the GO terms are legible in Fig. 6i and the module labels in Fig. 6j). Fig. 6i is a pseudobulk differential expression across n = 12 cell lines, knockout versus control, limma-voom with Benjamini–Hochberg adjustment. Fig. 6j is the hdWGCNA `ModuleTraitCorrelation` output across the co-expression modules.

## Refereeing Fig. 6i–j

This is your home turf and it is the thinnest evidence in the paper. Referee it properly, then read the section after this one immediately — the two halves only work together.

### The critique

You have the design from [Module 1](01-annotation-problem.md). Here is what is wrong with it, in descending order of how much it should bother you.

**The surviving panel is selected on the phenotype.** Twenty-one SpCas9-expressing cell lines went into the pool; lines with fewer than 100 cells after demultiplexing were dropped; **12** survive into the pseudobulk DE (Methods; Fig. 6i, `n = 12`). Nine lines — 43% of the panel — are gone. And the dropout is not random with respect to the thing being measured: a line represented by few cells at day 7 is a line that grew slowly, transduced poorly, or **died from the perturbation**. If `c10riboseqorf92` knockout is lethal in a line, that line is under-represented and gets filtered out, so the 12 lines that supply the transcriptional signature are enriched for lines that *tolerated* the knockout. The panel that reports the phenotype is conditioned on surviving it. This is the sharpest objection available and it applies to the design, not to the execution.

**~200 cells per condition, one timepoint.** Target recovery was 5,000 cells per sample, "approximately 200 cells per condition" by the Methods' own reckoning, at day 7, with 30,000 reads per cell. A pseudobulk profile aggregated from a couple of hundred cells is dominated by high-expressors and carries real sampling noise on anything below moderate expression. You would not build a primary claim on it.

**Two guides, pooled.** Both `c10riboseqorf92` guides go into one "KO" condition. Guide-specific off-target effects are not separable in the panel as presented — you cannot check whether the signature reproduces guide-by-guide, which is the standard internal replication for a CRISPR transcriptional phenotype.

**Fixed-effect design at n = 12.** `~0 + condition + scsplit_assignment` treats cell line as a fixed effect, which is reasonable at n = 12 but absorbs all line-specific response into the covariate. Any heterogeneity in how lines respond is estimated away rather than characterised, and 12 is too few to model it as random.

**Identity assignment noise.** Cell-line identity comes from demultiplexing — `demuxalot` and `dropulation` against DepMap and CellLineProject SNP profiles, plus genotype-free `scSplit`. Three tools were used, which is the right instinct, but at ~200 cells per group a small misassignment rate moves an aggregate materially, and the concordance between the three is not reported in the panel.

**"Mitosis up" is close to unfalsifiable in this design.** Any perturbation that slows or arrests a proliferating cancer line produces cell-cycle and chromosome-segregation signatures in a GO enrichment. Note also that the positive control is `KIF11` — a mitotic kinesin — so the positive control and the reported signature occupy the same pathway space. A mitotic signature in a proliferation-affecting knockout, benchmarked against a mitotic positive control, does not discriminate between hypotheses. It is consistent with the phenotype; it is not evidence for a specific mechanism.

**hdWGCNA at this scale is exploratory.** Metacells at k = 15 with a minimum of 30 cells, on 12 lines, with modules called "conserved" when significant and directionally consistent in three or more lines. That is a sensible rule and it is a low bar; Fig. 6j's module–trait correlations should be read as hypothesis generation.

**What is right about it, and say this too.** The control is a **cutting** control (Chr2-2), not a non-targeting one, so break toxicity is subtracted rather than confounded. There is a real positive control (`KIF11`). Extended Data Fig. 9p benchmarks perturbation magnitude by Euclidean and E-distance against the unperturbed population rather than resting on a bare *P* value. HVG selection is batch-aware across sample IDs. Ambient RNA is corrected with SoupX. Two pools balanced by doubling time. These are the choices you would have made.

**Write down the verdict.** A competent, conventional, modestly powered experiment, appropriate as one supporting panel among several, and not on its own evidence that a peptide has a biological function. If that is roughly what you wrote in Module 1, good — you have not learned to distrust your instincts, and you should not.

### And now the part that matters more

Here is the trap, and it is set for you specifically.

Fig. 6i–j is the paper's **weakest** evidence and it is also its **last figure**. It is the only figure in a 47-page consortium paper that you can referee on instinct. And the paper's strongest evidence sits precisely in the domains you cannot yet evaluate:

- 3.5 billion MS/MS spectra across 1,172 experiments and ~85,000 MS runs, yielding 573 million PSMs, with target–decoy FDR control and thousands of hand-inspected spectra ([Module 4](04-mass-spec-proteomics.md)).
- 240 million immunopeptidome spectra searched with **no protease constraint** — a search-space problem of a different order from a tryptic search ([Module 5](05-immunopeptidomics.md)).
- A matched null of **1,717,927** untranslated ORFs, assembled by eight documented rules, to convert a conservation score into a constraint score ([Module 6](06-evolution-orbl.md)).
- A manual curation pass over thousands of spectra and Ribo-seq tracks whose net effect was **demoting**: Tier 4 grew by 104 and every other tier shrank ([Module 8](08-tier-framework-synthesis.md)).

If you grade this paper by the figure you can read most easily, you will grade it wrongly, and the direction of the error is predictable: **down**. You will discount the 3.5 billion spectra because you cannot audit them, and weight the ~200-cells-per-condition scRNA-seq because you can.

State the general rule and keep it:

> The confidence a claim deserves is not proportional to how well *you* can check it. Legibility is a fact about your training, not about the evidence.

A reviewer who systematically down-weights what they cannot audit and up-weights what they can will misgrade every interdisciplinary paper they touch — and consortium papers are all interdisciplinary. That failure mode is not skepticism. It is a bias with a predictable sign, and it is the specific failure mode this module exists to prevent.

The practical move, and it takes ten minutes. For each major claim in the paper, write down **who the right referee is**, and then mark which claims the headline actually rests on:

| Claim | Right referee | Load-bearing for the headline? |
|---------|-------|-------|
| ~25% of 7,264 ncORFs yield detectable peptides | A bottom-up proteomicist; an immunopeptidomics specialist | Yes — this *is* the headline |
| The HLA build's no-enzyme search is FDR-controlled | An immunopeptidomics specialist | Yes |
| 30.4% of ncORFs show ORF-level constraint | A comparative genomicist | No — a separate claim |
| The tier assignments and the 37 → 3 funnel | A GENCODE/UniProt curator | Yes, for the annotation claim |
| `c10riboseqorf92` knockout has a reproducible transcriptional signature | You | No — the last claim in the paper, about one ORF |

The bottom row is the one you can referee. It is also the only row that does not carry any of the paper's weight. Notice too that the paper's own hierarchy agrees with your critique: Fig. 6i–j is never offered as annotation-grade evidence, and `c10riboseqorf92` stays a peptidein.

One more calibration, in the other direction. Being unable to audit something is not the same as having no purchase on it. You can still assess whether a method was validated against a matched null, whether the authors report the unflattering version of their own number, whether the errors of a curation process run toward caution, whether *n* values reconcile with totals. Every one of those is a domain-general check, you have applied all four in the last two modules, and none of them required you to know how a mass spectrometer works.

## Why it is still a peptidein

Now close the loop from [Module 1](01-annotation-problem.md).

`c10riboseqorf92` has more evidence than any other single ncORF in this paper: HLA immunopeptide detection, pan-essentiality across hundreds of cancer cell lines with two independent guides, selective depletion above its own locus background by permutation test, Cas13 concordance, DepMap co-essentiality structure, a coding-sequence rescue of the transcript-knockdown phenotype, and transcriptional signatures in bulk and single-cell. And the paper's verdict, stated plainly at the end of that section: it **remains annotated as a peptidein**, "because it does not possess clear evidence of function in normal physiology, as its evidence remains restricted to transformed cell lines or cancer."

**What the annotation projects would still require** (Fig. 5d; [Module 8](08-tier-framework-synthesis.md)). For "candidate protein": detection meeting HUPO-HPP criteria — two non-HLA peptides of ≥9 aa spanning ≥18 aa — **in healthy cells**, plus evidence of function. `c10riboseqorf92` fails on provenance, not on quality. And the provenance problem is general, not specific to this ORF: 2.36 of 3.53 billion non-HLA MS2 spectra searched in this study (66.9%) come from cancer tissue or cancer cell lines (agenda question 3), so the entire tryptic evidence base leans toward the malignant. Meanwhile, agenda question 5 notes that immune recognition of a peptide "is not currently considered a biological function by annotation projects", so the HLA evidence — however clean — does not satisfy the function limb either.

**What one experiment would change the call.** Detection of this microprotein by conventional, non-HLA mass spectrometry at HUPO-HPP standard in a **non-malignant human tissue**. Unlike a 19-codon uORF, that is achievable in principle here: at 123 amino acids it is long enough to yield several tryptic peptides spanning well past 18 residues, and size is a favourable detection determinant (Fig. 3; [Module 5](05-immunopeptidomics.md)). The catalogue's own best-detected member makes the point — `c11riboseqorf4` in `PIDD1` is a 171-amino-acid uoORF whose peptides appear in non-malignant tissue, cancer samples *and* cell lines, and it is one of the three ncORFs GENCODE annotated as protein-coding. Pair a non-malignant tryptic detection with the translation-dead rescue construct described above and this case becomes very hard to refuse.

**And the general point, stated once:**

> A fitness screen establishes that a locus matters. It does not establish that a 20–120 amino acid peptide is a functional protein.

The unit of a CRISPR screen is a cut site. The unit of an annotation is a molecule. The ladder of controls in this module is entirely an effort to close the distance between those two units, it closes most of it, and the residue is exactly the gap that the word "peptidein" was invented to name.

## Read the figure

Twenty minutes in your own PDF.

- [ ] Fig. 6a: trace the five workflow steps left to right and, for each, say in one clause what it rules out. Then find the ORBLq > 0.9 and ORBLq < 0.7 branches and the ncORF names on each.
- [ ] Fig. 6b: identify the frame colouring in the P-site track and confirm the ncORF is being read in a different frame from the host CDS. Then read the orange-versus-green fitness comparison at bottom right and say what it would look like if `GMCL1` itself were pan-essential.
- [ ] Fig. 6c and 6d together: 6c is the workflow for the local-background permutation test and 6d is its output. State the null hypothesis of that test in one sentence, in your own words.
- [ ] Fig. 6e: find the *x* and *y* axes and the green threshold. How many of the 25 datasets does an ncORF need for the ≥60% call?
- [ ] Fig. 6f: locate the six ncORFs on the `OLMALINC` transcript diagram and the siRNA target sites. Then read the four *P* values and confirm the pattern is two significant in one background and two non-significant in the other. Write down what the panel would look like if the phenotype were RNA-mediated.
- [ ] Fig. 6g: read the labelled genes and compare them to the main text's "mitosis and DNA damage regulation" characterisation. Then find the ρ > 0.3 threshold and decide whether a top-0.5-percentile cut on 17,110 genes is stringent.
- [ ] Fig. 6h: find the R² and the 14 circled interaction hits. Then say which of the two numbers in "513 up, 456 down, 14 significant interactions" answers the question the experiment was designed to ask.
- [ ] Extended Data Fig. 9c: read the two TPM thresholds off the dashed lines and compare the total and filtered hit counts by biotype in the right-hand panel. How much of the hit list does the expression filter remove?
- [ ] Extended Data Fig. 9e,f: work out from the axes how 9f excludes the de-repression hypothesis.
- [ ] Extended Data Fig. 9h: five species of Ribo-seq P-site density on one ORF. Say why this is a different kind of evidence from a conservation score.

## Write this down

- [ ] Score your prediction-1 control list against the seven in "The ladder of controls". Note which of the paper's you missed, and — equally — any of yours the paper did not run.
- [ ] In three sentences, explain to a colleague why a CRISPR hit on a 5′-UTR uORF does not localise to the uORF, and name the one control that comes closest to fixing it.
- [ ] State the de-repression hypothesis and explain how CRISPRa data excludes it. Then name one thing CRISPRa cannot exclude.
- [ ] Write out the local-background permutation test's null in one sentence, then write out ORBLq's null in one sentence, and say what the two have in common.
- [ ] Explain why re-expressing the coding sequence rescuing an siRNA phenotype argues for a peptide-mediated effect — and then describe the one construct that would settle it, and what result you would need from it.
- [ ] Referee Fig. 6i–j in a paragraph. Then write a second paragraph on why that paragraph should not change your overall assessment of the paper, and name the bias by its direction.
- [ ] For each of the paper's six main figures, name the discipline whose referee should assess it, and mark which are load-bearing for the abstract's headline number.
- [ ] Revisit prediction 5. Would you now accept a fitness screen as "evidence of function" for annotation? If your answer changed, write the sentence that changed it.

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| Screen scope: >2,000 ncORFs, 8 cell lines, matched RNA-seq and Ribo-seq | | |
| Library design as a specificity control — `intORF`s excluded before screening | | |
| Cutting versus non-cutting non-targeting controls | | |
| The specificity problem: one molecule, two candidate functional units | | |
| Expression/translation filtering (≥10 TPM RNA-seq, ≥5 TPM Ribo-seq) and what it does not fix | | |
| CDS-score subtraction: the shared-essentiality confound versus shared-regulation | | |
| The de-repression hypothesis, and why CRISPRa is the right test for it | | |
| The gene-specific local-background permutation test as a matched null | | |
| Meta-analysis across 25 datasets; pan-essential at ≥60% of samples | | |
| Cas13 concordance — what it adds and what it structurally cannot address | | |
| 51 pan-essential ncORFs → 6 with HLA support → ORBLq split at 0.9 / 0.7 | | |
| `c2riboseqorf47`: promoted with zero tryptic peptides, and the three axes that did it | | |
| Why a 19-codon ORF cannot satisfy HUPO-HPP at any sensitivity | | |
| `c10riboseqorf92`: 123 aa, one of six ORFs on `OLMALINC`, the only pan-essential one | | |
| The 485 / 486 / 471 discrepancy, and how to state the claim honestly | | |
| DepMap co-essentiality: 17,110 genes, top 0.5 percentile at ρ > 0.3 | | |
| The coding-sequence rescue, why it separates peptide from RNA, and where it stops | | |
| The translation-dead rescue construct that is missing | | |
| Fig. 6h: 969 marginal changes versus 14 significant interactions | | |
| Fig. 6i–j: 21 lines in, 12 out, and why the survivors are selected on the phenotype | | |
| Why "mitosis up" against a `KIF11` positive control does not discriminate hypotheses | | |
| The legibility bias, its direction, and the referee-assignment exercise | | |
| Why `c10riboseqorf92` stays a peptidein, and the one experiment that would change it | | |
| A fitness screen localises to a cut site; annotation is about a molecule | | |

## What I now trust, and why

Write your own. Mine, as a model:

- **I trust that `c10riboseqorf92` marks a locus that matters.** Two independent guides, r = 0.77 across hundreds of cancer lines, ~85% showing loss of viability, selective depletion above its own gene background by permutation test, concordance with an orthogonal Cas13 modality, and — the discriminating result — five sibling ncORFs on the same transcript that do nothing. That is a well-controlled locus-level claim and I would defend it.
- **I trust that the phenotype is ORF-associated rather than RNA-position-dependent.** The coding-sequence rescue of an siRNA knockdown excludes every function that requires the transcript to be present in its own neighbourhood. That is a real, hard-won narrowing, and it is the reason this ORF is the paper's showcase rather than a footnote.
- **I trust the controls ladder as a template I will reuse.** Exclude the inseparable cases at design time; require expression *and* translation in the actual cells; subtract the neighbouring feature's effect; test the specific alternative mechanism with a purpose-built assay; test against a local background rather than a global one; replicate across studies; confirm with an orthogonal perturbation modality. Seven steps, each ruling out a named alternative. I have run screens with fewer.
- **I trust `c2riboseqorf47` as proof that the framework earns its keep.** A 19-codon ORF with zero tryptic peptides became `ENSG00000310604` on ORF-level constraint, functional inference and immunopeptide support. Under the previous standard it was not merely unproven — it was unprovable in principle. A framework that promotes something the old one structurally could not see, while refusing something with a fatter dossier, is doing discriminating work in both directions.
- **I trust my own critique of Fig. 6i–j, and I trust that it does not settle anything.** The panel is modestly powered and its surviving cell-line set is conditioned on tolerating the perturbation. Both true. Also true: it is the last figure, about one ORF, supporting a claim the paper does not rest on — and the parts I cannot audit are the parts the headline actually needs. Holding those two judgements at once, without letting the second one soften the first, is the skill I came here for.
- **I trust the domain-general checks more than I did.** Do the *n* values reconcile with the totals? Was the score compared against a matched null? Does the paper report the unflattering version of its own number? Do the curation errors run toward caution? Four questions, none of which require me to know how a no-enzyme spectral search works, and they got me most of the way through a paper in four disciplines I do not practise.
- **Where I remain uncertain, and so does the paper:** whether a cancer-cell-line phenotype should ever count toward annotation of the human organism. That is agenda question 3, it is the only thing standing between this ORF and a gene record, and the consortium wrote it as a question rather than a policy.

## Sources

Paper anchors above are to the results sections "Functional genomics augments annotation" and "OLMALINC produces an essential peptidein"; the Discussion; agenda questions 1, 3 and 5; the Methods subsections "Lentiviral transduction for CRISPR screens", "CRISPR screening", "Analysis of CRISPR screening data: sgRNA mapping and hit calling", "Meta-analysis of CRISPR data", "Comparison of CRISPR–Cas9 with Cas13 data", "Analysis of CRISPRa data", "CRISPR tiling analysis and functional enrichment score for ncORF", "Pooled c10riboseqorf92 knockout", "Analysis of pooled c10riboseqorf92 knockout data", "siRNA and overexpression experiments" and "Multiplexed single-cell transcriptional response"; and to Fig. 3, Fig. 5d, Fig. 6a–j and Extended Data Fig. 9a–p. Quotations are short and attributed; the article is CC BY-NC-ND 4.0, so no panel is reproduced here.

Two numbers in this module do not reconcile in the paper itself, and I have flagged both rather than choosing: the PRISM cell-line denominator (486 pooled, 471 detectable per Methods, versus 485 in the main text, Fig. 6g and Extended Data Fig. 9m, with 415/485 = 85.6%), and the length of `c2riboseqorf47`, which Fig. 6b prints as 19 residues plus a stop but which is authoritatively recorded in GENCODE `ENSG00000310604` and Supplementary Table 6. The |log2 fold change| thresholds in the Fig. 6i legend and in the Methods are set as inline math that does not extract from the PDF; read those off the page.

External references cited above, all of them the paper's own: ref. 7 (Hofman *et al.*, *Mol. Cell* **84**, 261–276, 2024), ref. 28 (Prensner *et al.*, *Nat. Biotechnol.* **39**, 697–704, 2021), ref. 29 (Funk *et al.*, *Cell* **185**, 4634–4653, 2022), ref. 30 (Chang *et al.*, *Cancer Cell* **39**, 466–479, 2021), ref. 31 (Sanson *et al.*, *Nat. Commun.* **9**, 5416, 2018), ref. 32 (McFarland *et al.*, *Nat. Commun.* **11**, 4296, 2020, the multiplexed single-cell perturbation method), ref. 84 (Dempster *et al.*, Chronos, *Genome Biol.* **22**, 343, 2021) and ref. 85 (Wessels *et al.*, *Nat. Biotechnol.* **38**, 722–727, 2020). The tiling-screen permutation code is at `https://github.com/CFVALLS/tiling_screens_with_permutation` (the paper's ref. 94); the study's own analysis code is at `https://github.com/VanHeeschLab/deutsch_kok_et_al_2024` (ref. 91). One disambiguation, because the numbering is easy to get wrong and it changes a factual claim about whose screens went in: the ncORF guide library, the pan-essential and non-targeting control sets, the two tiling screens and the meta-analysis all trace to **ref. 7 = Hofman *et al.*, *Mol. Cell* **84**, 261–276 (2024)**, together with ref. 28. Chen *et al.*, *Science* **367**, 1140–1146 (2020) is **ref. 27**, cited by the paper as prior evidence that ncORF translation is functional — it is not one of the screens reanalysed here. Further reading is under "Module 7 — function" in [key references](../resources/key-references.md).
