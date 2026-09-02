# Journal Club and Capstone

~1.5 hrs. Prerequisites: all eight modules, and [misconceptions](misconceptions.md).

This is the exit exam. The standard is not "I read the paper" — it is that you could present it to a room that includes a proteomicist, a comparative genomicist and a gene-annotation curator, and hold your ground with each of them.

## How to use this

Answer from memory first, in writing. Then check. The model answers below are deliberately fuller than what you would say out loud — they include the follow-up a sharp questioner would ask. If your answer covers the first sentence of a model answer but not the caveat, you have the recall and not the understanding.

Where a model answer cites a number, that number is in the paper. Where it says "your inference", the paper does not state it and you should present it as your own reading.

## Part 1 — Can you state the paper?

Five minutes, no notes. If you cannot do this, go back to [Module 8](08-tier-framework-synthesis.md).

- [ ] What question does this paper answer, in one sentence?
- [ ] What is a peptidein, and why did the field need the word?
- [ ] What is the headline number, and what does it actually rest on?
- [ ] What did the paper deliver — not what did it measure, but what did it *produce*?
- [ ] Name the one number you would put on a single slide.

## Part 2 — The question bank

### The argument

**Q1. State the paper's headline number, then state the number you would actually defend.**

Headline: about 25% of 7,264 ncORFs give rise to detectable peptides across 95,520 proteomics experiments. What I would defend depends on which claim is being made. For *any* peptide evidence: 1,867 of 7,264 (25.7%), the union across both builds. For HLA evidence: 1,785 (24.6%). For conventional tryptic evidence surviving manual inspection: **66 (0.9%)**. For "this is a protein-coding gene": **3**.

The follow-up to be ready for: those endpoints differ by roughly 600-fold, and that spread is the paper, not a flaw in it. Also worth knowing that "95,520 proteomics experiments" is loose — the paper's own Methods define experiments as 1,172 plus 592, i.e. 1,764; 95,520 is the number of MS *runs*.

**Q2. Someone says "so 1,785 ncORFs encode proteins." Correct them in three sentences.**

1,785 ncORFs have at least one peptide in the HLA immunopeptidome build. HLA presentation shows a ribosome made something at that locus, but the presented fragment may come from a rapidly degraded product — a DRiP — rather than a stable protein, which is exactly why the paper coined "peptidein" and why the consortium's second open question asks whether immunopeptidomics should count as protein-coding evidence at all. Three ncORFs in this study became protein-coding genes.

**Q3. Why did the field need a new word? Why not just call them proteins, or not call them anything?**

Because two things that had always travelled together came apart. Protein *identification* is an experimental claim: a polypeptide was detected. Protein-coding gene *annotation* is a curatorial claim rooted in the idea that the product does something biological. For canonical proteins these coincide, so no vocabulary was needed. ncORFs break the coincidence at scale — thousands are demonstrably translated and detected, and almost none have demonstrable function. The old binary forced curators to either admit thousands of genes on existence evidence alone, with ripple effects through every downstream reference and drug program, or leave confidently detected molecules entirely unrepresented. "Peptidein" is the third option: a database record that says *this exists and I cannot yet tell you what it does*.

**Q4. What is the paper's actual product?**

Four things, none of which is a dataset: a decision procedure (the tier framework, applied at catalogue scale), a vocabulary (peptidein, now recognized by GENCODE, UniProtKB, HGNC, RefSeq and HUPO-HPP), a method (ORBL), and a governance agenda (seven questions). Read it as a standards document with a worked example attached. The 3-of-7,264 outcome is the thesis — it demonstrates that the procedure is stringent enough to be worth adopting.

Be precise about the tier framework if pressed, because this is a trap: the Methods say the tier system was "initially proposed previously" in reference 25, by one of this paper's own corresponding authors. What is new here is applying it to all 7,264, splitting provisional from final tier assignment, and wiring it to the protein-versus-peptidein decision. The genuinely novel *methods* contribution is ORBL; the genuinely novel *conceptual* contribution is the peptidein class.

### The methods

**Q5. Reproduce the tier table, then say what its shape tells you.**

| Tier | Ribo-seq | MS | HLA | Category |
|---------|-------|-------|-------|-------|
| 1A | + | ++ | ± | Candidate protein |
| 1B | + | − | ++ | Presented |
| 2A | + | + | ± | Detected |
| 2B | + | − | + | Detected |
| 3 | − | ± | ± | Putative |
| 4 | + | − | − | Ribo-seq ORF |

Three readings. Tier 3 is the only row requiring Ribo-seq negative, so nothing can start there — every ncORF entered the catalogue *because* it had Ribo-seq support — which is why its provisional count is 0 and its final count of 90 is entirely demotions. Tier 1B has no MS evidence at all, so "Presented" is a real category built purely on immunopeptidomics. And 2A versus 2B share the label "Detected" while resting on different assays, which is the second open question rendered as a table row. Note also that Methods define a seventh tier — an in-silico ORF on an expressed transcript with neither Ribo-seq nor proteomic evidence — that Fig. 5a does not show, so say "six tiers as figured, seven as defined".

**Q6. What does manual inspection do to the tier assignments, and what does that tell you about automated integration?**

It demotes. Provisional to final: 1A 37 → 16, 1B 665 → 601, 2A 146 → 39, 2B 1,063 → 1,059, 3 0 → 90, 4 5,353 → 5,457, plus 2 in "Other". Both margins close on 7,264. Tier 2A loses nearly three-quarters of its members and Tier 4 gains 104.

What it tells you: automated integration of three noisy evidence types is systematically optimistic, and the correction is large rather than marginal. Two further observations worth raising, and these are your inference rather than the paper's: final Tier 1A is a subset of provisional Tier 1A, so curation never promotes anything *into* "candidate protein" — the ceiling is set by automated tryptic MS, which is the very method the paper argues is failing. And provisional Tier 4 is perfectly stable at 5,353, meaning roughly three-quarters of the catalogue was never really adjudicated at all.

**Q7. Reconcile a very low reported FDR with the rejection of most single-peptide ncORFs.**

They are answers to different questions. The reported FDR is a global property of a build containing millions of peptides, dominated by canonical proteins with high prior probability. ncORFs are a small, low-prior stratum inside it: short, low-abundance, and concentrated in the score region where errors live. A global error rate carries no guarantee about a rare subset, so the local FDR among ncORF identifications is far worse than the headline figure.

The paper demonstrates this empirically rather than just asserting it. Of ncORFs detected by a single tryptic peptide, 36 of 141 survived inspection — a 26% survival rate — against 30 of 42 for multi-peptide ncORFs. And Extended Data Fig. 2c–d shows decoy PSMs accumulating *faster* than ncORF PSMs as the threshold relaxes, which is direct evidence that the marginal identification in this stratum is more likely false than true. That is also the empirical case for the HUPO-HPP two-peptide rule.

The analogy to resist: this is not a Benjamini–Hochberg q-value over a fixed gene list. There is no exchangeability argument, the null is a model over sequence space, and you cannot pre-filter low-information candidates the way you drop low-count genes before differential expression.

**Q8. State the HUPO-HPP rule exactly and explain why it is structurally hostile to microproteins.**

Two uniquely mapping, non-nested peptides of at least 9 amino acids, together covering at least 18 amino acids. Non-nested matters — two peptides where one contains the other are one piece of evidence.

Why each clause exists: two peptides because a single PSM is the modal failure mode of large-scale search; 9 amino acids because shorter peptides are not combinatorially unique in a 20,000-protein proteome; 18 amino acids of coverage to guard against one mis-assigned region carrying the whole claim. Every clause is defensible.

Why it cannot be met: 2,059 of 7,264 ncORFs (28.3%) are shorter than 25 amino acids. Two non-overlapping 9-mers covering 18 residues of a 22-amino-acid protein requires near-complete coverage *and* trypsin cutting in exactly the right places. The control case is that only 2 of 36 curated GENCODE proteins under 50 amino acids satisfy the rule. This is not a threshold that disadvantages microproteins — for a large fraction it is unsatisfiable at any sequencing depth. Hence open question 1.

**Q9. Why is a no-protease search harder than a tryptic one?**

Two reasons, one statistical and one physical. Statistically, a tryptic search enumerates peptides bounded by lysine and arginine; a no-enzyme search admits every substring within the mass window, so the candidate count per spectrum grows by orders of magnitude and, at a fixed score threshold, so does the chance of a high-scoring wrong answer. Physically, tryptic peptides carry a C-terminal basic residue, which localizes the mobile proton and produces the clean y-ion ladders that validation criteria assume. HLA peptides often lack a basic terminus, so their spectra are richer in b ions and internal fragments — which is why the paper's validation procedure has HLA-specific clauses about annotating internal fragmentation.

The right analogy from your own work is *de novo* transcript assembly versus quantifying against a known GTF: the hypothesis space is generated rather than enumerated. The wrong analogy is unstranded versus stranded libraries, which is a two-fold ambiguity, not a combinatorial expansion.

One thing to flag: Fig. 1b labels the non-HLA build "protease-specific", but Methods say all datasets were searched with semi-enzymatic, typically semi-tryptic settings. Semi-tryptic already enlarges the space relative to fully tryptic, so the figure overstates the constraint.

**Q10. Explain ORBLv and ORBLq to someone who knows PhyloCSF.**

PhyloCSF asks whether cross-species substitutions look filtered by the genetic code — a per-codon likelihood comparison between coding and non-coding substitution models. It measures constraint on **amino-acid identity**, and it is badly underpowered on short ORFs because there are too few codons for the likelihood to accumulate.

ORBLv asks a different question: across a clade, what fraction of total branch length preserves the ORF's start codon, stop codon and open reading frame — with no regard to what the frame encodes. It measures constraint on **ORFness**.

ORBLq is ORBLv converted into a quantile against ≥1,000 untranslated ORFs matched for biotype and similar length, drawn from a background of about 1.7 million. That matching is the actual innovation: it removes chance retention of a short nucleotide string, and it partially removes conservation inherited from an overlapping CDS. Because it is an empirical quantile, "ORBLq > 0.9" means "top 10% of matched untranslated ORFs" — and 10% is therefore precisely the null expectation, which is where the paper's expected-value line comes from.

The punchline: 2,211 of 7,264 (30.4%) exceed ORBLq 0.9 against 10% expected, while only 143 (2.0%) reach PhyloCSF above 10. Constraint on having a reading frame is roughly fifteen times more common than constraint on what it encodes. The existence proof that they are orthogonal is `c8riboseqorf102` — ORBLq 0.98, PhyloCSF per codon −30, and detected by immunopeptidomics.

**Q11. What can a CRISPR fitness screen establish about a 20–120 aa peptide, and what can it not?**

It can establish that cutting DNA inside the ORF reproducibly reduces proliferation across cell lines, and — with a tiling design and an in-gene permutation null — that the effect is spatially localized to the ORF rather than smeared across the host transcript.

It cannot establish that the peptide is the effector. Cas9 cutting inside a 5′UTR or a lncRNA exon destroys DNA, and with it RNA secondary structure, splice signals, RNA-binding-protein sites and regulatory elements; indels can also be dominantly toxic rather than null. It cannot establish anything about normal physiology, since the screens run in immortalized, mostly cancer lines under proliferative selection. And it cannot see non-proliferative function — differentiation, stress response, secretion.

Design limits specific to this screen: all intORFs were excluded, as were doORFs and uoORFs with ≥25% CDS overlap and ORFs under 12 amino acids. So the screen structurally cannot test the 720 intORFs, and the classes it does test are those least entangled with a host CDS.

### The adversarial questions

**Q12. Give the strongest alternative explanation for the ORBL result.**

That much of the constraint is on the RNA, not the peptide. uORFs are the largest and most constrained class — 1,335 of 2,915 above ORBLq 0.9. They sit in 5′UTRs under selection for translational control, Kozak context and RNA structure, all of which preserve a start codon, a stop codon and an open frame without requiring that the encoded peptide matter at all. The paper concedes this reading explicitly when it suggests the excess for uORFs and uoORFs indicates conserved *regulatory* upstream ORFs — but the abstract's "evolutionary constraint is common" invites the protein interpretation.

Two supporting points. First, the overlapping biotypes inherit constraint from the CDS they sit inside, which the authors state; ORBLq's biotype- and frame-matching mitigates this but does not obviously eliminate it. Second, ORBLv's rules are permissive by design — a *different* stop codon counts as a conserved stop, and compensating insertions and deletions count as a conserved frame. Both are correct for "ORFness" and both weaken any inference about a conserved product. The classes where ORFness constraint is hardest to explain away are dORFs and lncRNA ORFs, which have the lowest fractions.

**Q13. Is the NetMHCpan concordance independent validation?**

No — it is an internal consistency check, and a useful one, but NetMHCpan is trained in substantial part on eluted-ligand immunopeptidomics data, the same modality being checked. High concordance rules out gross artefact; it does not independently establish that these peptides are presented ligands. Marking this as `unverified`: I believe the specific training-data overlap is well established for NetMHCpan 4.x, but I have not confirmed it against the NetMHCpan publication itself, so present it as a concern to check rather than a settled fact.

**Q14. Which single panel in Fig. 6 would you delete last?**

The rescue. Pan-essentiality, the DepMap co-essentiality correlation, the Cas13 concordance and the tiling screen are all consistent with OLMALINC mattering as an RNA. Only re-expressing the `c10riboseqorf92` coding sequence and recovering proliferation after transcript knockdown speaks to the ORF product specifically.

And then the honest caveat: even that is one cell line, four replicates, a proliferation readout, and re-expression of a coding sequence — which restores the peptide *and* an exogenous RNA containing it, so an RNA-level rescue is not formally excluded. The transcriptional follow-up is weaker still: 513 genes up and 456 down, but only 14 with a significant interaction term, and R² = 0.722 between the GFP and ORF-expressing responses, meaning restoring the ORF explains little of the knockdown response.

**Q15. Where does your own expertise let you audit this paper better than a proteomicist could — and where should you not trust yourself?**

Better: the multiplexed scRNA-seq in Fig. 6i–j and Extended Data Fig. 9. It is 10x Chromium GEM-X on-chip multiplexing with 3′ GEX v4, Cell Ranger 9.0.1 `multi` against `refdata-gex-GRCh38-2024-A`, MAD-based filtering with a hard 20% mitochondrial cutoff, SoupX ambient correction, Seurat `AggregateExpression` pseudobulk, edgeR `filterByExpr` and TMM, limma-voom with cell-line identity as a covariate, and hdWGCNA modules — with cell lines deconvolved by SNP-based demultiplexing. You can judge whether roughly 200 cells per condition supports pseudobulk differential expression, and you can spot that dropping lines with too few cells risks selecting against exactly the lines where the perturbation worked, since a dying line loses cells.

Second audit surface, also yours: annotation versioning. The paper moves across GENCODE v35, v42 and v45 in different analyses, which is why Fig. 1b counts 3,083 uORFs and the ORBL analysis counts 2,915. You know from reference-building work how much biotype churn that implies.

Where not to trust yourself: everything that makes the paper strong. Billions of spectra, a 1.7-million-ORF matched null, thousands of hand-curated spectra, and a phylogenetic method you met a week ago. Fig. 6i–j is the paper's thinnest evidence and its most legible figure to you; the temptation is to grade the whole paper by the one panel you can read. Resist it. Calibration is the skill being tested here, not skepticism.

**Q16. Name three internal inconsistencies in the paper.**

The number of HLA-typed MS runs appears as 4,870 in the main text, 4,879 in Methods and 4,869 in a figure caption. The count of Ribo-seq profiles manually inspected in the HLA build is 691 in the main text and Fig. 2h but 699 in Methods. And the abstract's "95,520 proteomics experiments" contradicts the Methods' own definition of an experiment, which totals 1,764.

Others available: Fig. 3d reports 5,140 undetected ncORFs where Extended Data Fig. 6f reports 5,142; the PRISM cell-line counts run 486, 471, "over 485" and 415 without reconciling cleanly; Data Availability cites Ensembl Release 87, from 2016, against Ensembl 98 and 108 in Methods.

None of these changes a conclusion. Raising them is not point-scoring — it is the correct register for a paper this size, and it demonstrates you read the Methods rather than the abstract.

## Part 3 — Capstone

Three deliverables. Reading and writing only.

### A. The unseen case

Pick one of these three. Each appears in the paper, and none has been used as a teaching example in any module — so you are seeing the evidence cold.

1. **`c17norep146`**, a uoORF in PSMC5. Extended Data Fig. 8b.
2. **`c3riboseqorf106`**. Appears in the tiling screen panels of Fig. 6 and again in Fig. 6h.
3. **The trio of ncORFs in STK11, ZNF219 and CIRBP.** Discussed in the Discussion's limitations.

Before looking anything up, write a dossier:

- [ ] What evidence exists on each axis — Ribo-seq, tryptic MS, HLA, evolutionary, functional?
- [ ] What provisional tier does that evidence imply? Justify against the table in Q5.
- [ ] Predict the final tier, and say what manual inspection would most likely challenge.
- [ ] Recommend one of: candidate protein, candidate peptidein, or neither — against the three criteria in [Module 8](08-tier-framework-synthesis.md).
- [ ] Name the **single** experiment that would change your recommendation, and state what it would still leave unresolved.

Then find the case in the paper and check yourself. Grade the reasoning, not the label — if you reached the right tier by the wrong route, that counts as wrong.

### B. The referee report

Write the report you would submit if this manuscript had been sent to you.

- [ ] Two sentences summarizing the advance.
- [ ] Three major points, each citing a specific figure panel and proposing a specific additional analysis or control. At least one must be **in favour** of a claim the authors under-sell.
- [ ] Five minor points, at least three of them numerical or internal inconsistencies you found yourself.
- [ ] A recommendation, with the condition that would change it.

The "in favour" constraint is the hard part and the point of the exercise. A referee report that is only critical is not a good report, and the discipline of finding the under-sold claim is what separates reading critically from reading cynically. One candidate: the sample-provenance argument is the paper's strongest and least-promoted finding — if 66.9% of the world's proteomics spectra are cancer-derived, then the rate-limiting resource for annotating the non-canonical proteome is healthy-tissue proteomics, and no amount of method development substitutes for it.

### C. Teach it

- [ ] A 15-minute lab-meeting talk whose thesis is the **decision procedure**, not the numbers.
- [ ] Report 3 of 7,264 as the central finding, not as a disappointment. If your audience leaves thinking the paper failed, you have mis-taught it.
- [ ] One slide, at most six numbers, that survives the question "isn't this all just noise?" Justify each of the six in writing.
- [ ] Answer, without notes: "what would change your mind about peptideins being a useful category?"

## Closing the loop

- [ ] Update the [paper README](../README.md) status from `to-read` → `read`
- [ ] Fill in the concept table in the [learning plan](learning-plan.md)
- [ ] Add any follow-up papers you want to chase to [key references](../resources/key-references.md)
