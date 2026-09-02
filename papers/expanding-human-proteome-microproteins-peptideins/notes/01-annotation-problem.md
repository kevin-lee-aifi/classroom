# Module 1 — The annotation problem

~1.5 hrs. No prerequisites. This is the entry point; every later module ladders back to the distinction drawn here.

Covers Fig. 6i–j and Extended Data Fig. 9 (as the way in), the Introduction, Fig. 1a, and the Discussion's central claim.

The last experiment in this paper is one you have already run. Fig. 6i–j is a multiplexed 10x knockout experiment on GEM-X 3′ Gene Expression v4 chemistry, processed with Cell Ranger v9.0.1 `multi` against `refdata-gex-GRCh38-2024-A`, ambient-corrected with SoupX, pseudobulked with Seurat `AggregateExpression`, normalised with edgeR TMM, tested with limma-voom, and networked with hdWGCNA (Methods, "Multiplexed single-cell transcriptional response"). There is nothing in it you would need explained. Start there rather than at the abstract, because it is the one part of this paper you can referee on instinct — and the judgement you form on it is what the next seven modules are going to argue with.

## Predict first

Open the PDF to Fig. 6i–j and Extended Data Fig. 9p, and read the Methods subsection "Multiplexed single-cell transcriptional response". Then write these down before reading on.

1. On your own standards for a knockout scRNA-seq experiment, would you sign off on Fig. 6i–j as evidence that losing `c10riboseqorf92` does something reproducible? Write `yes`, `no`, or `qualified`, plus one sentence of reasoning.
2. Twenty-one SpCas9-expressing cell lines went into the pool. How many survive into the pseudobulk differential expression? Write a number.
3. Target recovery was 5,000 cells per sample, split across four sgRNA conditions. How many cells per condition per cell line does that leave? Write a number.
4. `c10riboseqorf92` is a 123-amino-acid ORF inside the `OLMALINC` lncRNA. It has mass-spectrometry evidence, HLA evidence, a pan-essential CRISPR phenotype, a rescue experiment, and the signature you just looked at. Is it annotated as a protein-coding gene, `yes` or `no`? And of the 7,264 candidates in this paper, how many became protein-coding genes? Write a number.

Keep all four visible. Questions 1–3 are about experimental judgement. Question 4 is about something else entirely, and the gap between them is this module.

## The experiment you could have run

Here is the design, from the Methods, so you can hold it to your own standard rather than the paper's.

Twenty-one human cell lines expressing SpCas9 were cultured individually, then grouped into two pools by doubling time so growth dynamics stayed balanced. Each pool was transduced with four sgRNAs: a non-targeting **cutting** control (Chr2-2), two independent guides against `c10riboseqorf92`, and a positive control against `KIF11`. Each virus went in at four concentrations to bracket an MOI of about 1. Puromycin selection began 24 h post-infection at 5 µg ml⁻¹, refreshed every 48 h. On day 7 the adherent and suspension fractions were combined, the two pools merged with equal representation of each line, and viability confirmed above 90%.

Library and sequencing: 10x Chromium, GEM-X On-chip Multiplexing, 3′ Gene Expression v4; target recovery 5,000 cells per sample (approximately 200 cells per condition); 30,000 reads per cell; Illumina NovaSeq, 10B 300-cycle kits.

Processing: Cell Ranger v9.0.1 `multi`, `refdata-gex-GRCh38-2024-A`. MAD-based outlier filtering — 5 MADs on log total counts, log gene counts and percentage of counts in the top 50 genes; 3 MADs on mitochondrial percentage; hard mitochondrial cutoff at 20%. Genes detected in fewer than 20 cells dropped. SoupX ambient correction. Counts normalised to 10,000 per cell and log-transformed. 2,000 highly variable genes, `cell_ranger` flavour, batch-aware across sample IDs. 50 principal components. Cell-cycle S and G2M scores from the Regev laboratory gene sets.

Demultiplexing: `demuxalot` and `dropulation` against SNP profiles curated from DepMap release 25Q2 and CellLineProject, plus a genotype-free pass with `scSplit`. Cell lines with fewer than 100 cells were dropped from downstream analysis (Methods) — and the answer to prediction 2 is that **12 of the 21 lines survive** into the pseudobulk DE (Fig. 6i caption, `n = 12` cell lines). The filter and the surviving count are both stated; that the 100-cell floor accounts for all nine losses is not.

Differential expression: `AggregateExpression` to one pseudobulk profile per cell line × condition, `filterByExpr`, TMM, then limma-voom with design `~0 + condition + scsplit_assignment`, moderated *t*-statistics with `eBayes(trend = TRUE)`, Benjamini–Hochberg adjustment. Enrichment via clusterProfiler against GO Biological Process, `minGSSize = 5`, `maxGSSize = 500`, BH-adjusted *P* < 0.01. Co-expression modules via hdWGCNA in Seurat v5 — metacells by k-nearest neighbours (`k = 15`, max shared 12, minimum 30 cells) grouped by line and condition in UMAP space; genes in at least 5% of cells retained; signed network at the first soft-threshold power reaching scale-free fit *R*² ≥ 0.8; minimum module size 30, merge cut height 0.25. Modules significant and directionally consistent in three or more lines were called "conserved". Fig. 6j is the `ModuleTraitCorrelation` output.

Note two design choices you would have made yourself. The control is a **cutting** control, not a non-targeting one, so Cas9 double-strand-break toxicity is subtracted rather than confounded. And Extended Data Fig. 9p ends with a Euclidean-distance heatmap of perturbed versus unperturbed cells, benchmarked against the `KIF11` positive control — an explicit calibration of effect magnitude against a known essential gene, rather than a bare *P* value.

The result: mitosis and chromosome-segregation processes go **up** on knockout across lines; translation and metabolism processes go **down** (main text, "OLMALINC produces an essential peptidein"; the GO terms are legible in Fig. 6i, and the module labels in Fig. 6j).

Now judge it. Roughly 200 cells per condition per line at target recovery; nine of twenty-one lines lost to the 100-cell floor; a single day-7 timepoint; two guides; `n = 12` for the pseudobulk contrast with cell line as a covariate. That is a modest but entirely conventional experiment — the sort you would accept as one supporting panel among several, not as a standalone claim. Write down whether that matches what you predicted.

## The puzzle

Now assemble everything the paper has on `c10riboseqorf92`.

It is a 123-amino-acid ORF on the `OLMALINC` transcript, also known as `LINC00263` — an RNA carrying six ncORFs recognised by GENCODE, of which only this one scores as a pan-essential dependency (main text; Fig. 6e). Specifically:

- **Peptide evidence.** It is detected in the HLA immunopeptidomics build, which is why it entered the functional-genomics prioritisation at all (main text, "Functional genomics augments annotation", step 3 of the Fig. 6a workflow).
- **A pan-essential CRISPR phenotype.** One of 51 ncORFs with a pan-essential knockout signature across the eight-cell-line screen, then confirmed in a pooled knockout across the PRISM barcoded panel: loss of viability in **415 of 485** cell models (85.6%), with two independent sgRNAs (main text; Extended Data Fig. 9m,n). It is also supported by CRISPR–Cas13 RNA-degradation screening of lncRNAs (Extended Data Fig. 9j).
- **A rescue.** Re-expressing the `c10riboseqorf92` coding sequence rescues the loss-of-viability phenotype caused by `OLMALINC` knockdown (Fig. 6f; Extended Data Fig. 9k,l). This is the load-bearing experiment: it separates an ORF-specific function from anything the RNA might do as an RNA.
- **Co-essentiality structure.** Spearman correlation of its knockout profile against 17,110 genes across 485 DepMap screens picks out genes in mitosis and DNA-damage regulation (Fig. 6g).
- **A transcriptional signature**, in bulk (Fig. 6h) and in the multiplexed scRNA-seq you just read (Fig. 6i–j).

That is a stronger dossier than many published protein-coding genes carry. And the paper's own verdict, stated plainly at the end of that section: it **remains annotated as a peptidein**, because it does not possess clear evidence of function in normal physiology — its evidence is restricted to transformed cell lines and cancer.

So: why can't all of that buy a gene record?

The answer is not that the evidence is weak. It is that "gene record" is not a summary of evidence. It is a decision, made by named institutions, against criteria that this dossier does not address. Understanding that sentence is the whole point of Module 1.

## Identification is not annotation

From the Discussion, and this is the conceptual pivot of the entire paper:

> While protein identification refers to the experimental detection of a polypeptide molecule, protein-coding gene annotation is historically rooted in the idea that the translated protein imparts a biological function.

Two different claims, two different burdens of proof.

**Identification** is an experimental result. A polypeptide was detected. It is falsifiable, has an FDR, and lives in a spectrum file with a resolvable identifier. Everything in Modules 3 through 5 is identification.

**Annotation** is a curatorial decision about what belongs in a reference. It asserts something about the human organism — not about A375 cells, not about a spectrum. Its historical root is *function*, not detection. And the paper is explicit about where that leaves immune presentation, in agenda question 5:

> Notably, immune recognition of a peptide is not currently considered a biological function by annotation projects.

Read that twice. An ORF whose product is synthesised, processed by the proteasome, loaded onto HLA class I, displayed at the cell surface, and in some cases targetable by immunotherapy still fails the function test — because the annotation projects have not decided that being seen by a T cell counts as doing something. That is a **policy** position, not a biological finding, and the paper poses it to its own community as an open question rather than resolving it.

This is where the analogy to your own work is most tempting and most dangerous, so let me draw it and then break it.

> **Analogy.** Identification is to annotation as detecting a transcript in a count matrix is to that transcript having a record in your GTF.
>
> **Where it breaks.** For transcripts the two are nearly interchangeable, because the GTF you align against already contains essentially every locus you are going to detect — the annotation is not the bottleneck, so you never notice it is a separate act. The entire subject of this paper is the case where the reference *does not* contain the thing you detected, so there is no row to increment and no symbol to report. The analogy is useful for the shape of the distinction and actively misleading about its stakes.

## Why any addition has ripple effects

The Introduction gives the reason curators are conservative, in one sentence:

> Protein-coding genes are the bedrock of biomedical investigations, including the overwhelming majority of drug development programmes. Therefore, any wholesale addition of protein-coding genes creates ripple effects across human bioscience.

Make that concrete rather than rhetorical. A new `protein_coding` gene record propagates into: every downstream reference build and every prebuilt aligner index derived from it; variant-effect prediction, where a nucleotide that was intergenic or intronic acquires a coding consequence and a new class of loss-of-function call; gene-set and pathway databases; probe and panel designs; proteomics search databases, which then find peptides they previously could not; drug-target triage, where "is it a protein" is an early gate. And the asymmetry matters: adding a record is cheap and retracting one is not, because everything downstream has already been rebuilt on it.

Set against that, the cost of *deferring* a real gene is that a handful of specialists keep studying it under a systematic identifier. Given that asymmetry, a conservative default is defensible independently of the biology — which is exactly why "3 out of 7,264" is not a measure of how little was found.

Note also the concrete institutional form of this conservatism. In PeptideAtlas, an entry can only reach `canonical` status if it already belongs to the core set of approximately 20,389 neXtProt and UniProtKB/Swiss-Prot protein-coding genes (Methods, "Protein identifications and categories"). A sequence outside the reference set cannot be certified as canonical no matter how good its spectra are. The gate is not only evidentiary; it is definitional.

## The vocabulary, and what "peptidein" adds

Four words are used loosely in this literature and one is new.

**ncORF** — non-canonical open reading frame. An ORF with evidence of translation that is not an annotated CDS. All 7,264 entries in this paper are ncORFs.

**Microprotein / small ORF-encoded peptide (SEP) / micropeptide.** The Introduction says these are "variably referred to as microproteins, small ORF-encoded peptides (SEPs) or micropeptides (hereafter, microproteins)". Read that carefully: the paper is **not** arguing the three terms carve up different objects. It observes that usage is inconsistent, picks one, and moves on. So "microprotein" here is a chosen shorthand for the translation product of an ncORF, and if you see a paper distinguishing SEPs from micropeptides on principle, that distinction is not this paper's.

**Peptidein** — the new term, and the reason it exists is the gap opened by the identification/annotation split. The paper defines it twice, and the two definitions are worth holding side by side.

In the Results ("Peptideins: candidates of unclear status"), a peptidein is an ORF with experimentally confirmed RNA translation and protein synthesis, but for which the data are currently insufficient to claim conventional protein-coding gene status. In the Discussion, it is a translation product confidently detected endogenously, but for which a role in normal physiology cannot be verified at the present time — and it explicitly includes potentially transient products of cellular stress or defective ribosome translation.

Three things "peptidein" adds that "microprotein" does not:

- It is a claim at the **annotation layer**, not the molecular layer. "Microprotein" says what kind of molecule you have. "Peptidein" says what the reference projects are currently willing to assert about it. They are answers to different questions, and an ORF can be both.
- It has **institutional standing**. Per agenda question 6, GENCODE, UniProtKB, HGNC, RefSeq and HUPO-HPP have agreed to classify such products as peptideins; precise guidelines are in preparation. The paper reports **121 initial peptidein annotations** (Supplementary Table 12). It is a category with members, not a coinage.
- It makes a previously **unrepresentable state representable**. Before it, an ORF with excellent detection and no demonstrable physiological function had no status at all — it was simply absent from the reference. "Peptidein" gives the curator something true to write down.

One wrinkle worth noticing rather than smoothing over: the Results definition attaches "peptidein" to an **ORF**, the Discussion definition to a **translation product**. That slippage is in the paper, not in your reading of it, and it will matter the moment someone asks whether a peptidein is a locus or a molecule.

## Who actually decides

"The annotation projects" is not one body. Each holds a different kind of authority, and the paper is a negotiation between them. Open Fig. 1a while you read this.

- **GENCODE** (Ensembl-GENCODE) — the reference annotation of gene, transcript and CDS **coordinates** for human and mouse. It is what a GTF is. GENCODE annotated the three new protein-coding genes in this paper, and separately `c2riboseqorf47` as `ENSG00000310604`. Methods, "Gene annotation": the annotation work here was carried out as part of the ongoing GENCODE project using existing workflows.
- **UniProtKB/Swiss-Prot** — manually **curated** protein sequence and function. Curation, not coordinates. The Introduction names GENCODE and UniProt jointly as the projects whose task is curation and maintenance of protein-coding genes.
- **HGNC** — the HUGO Gene Nomenclature Committee (author affiliation 19), which assigns gene **symbols**. Note what the paper calls its subjects: `c10riboseqorf92`, `c12norep105`, `c11riboseqorf4`. Those are systematic catalogue identifiers, not HGNC symbols. Naming is a separate act from having coordinates.
- **RefSeq** (NCBI) — the other reference annotation, independent of Ensembl-GENCODE, and a signatory to the peptidein decision in agenda question 6.
- **HUPO-HPP** — the Human Proteome Organization's Human Proteome Project, which sets the **verification standard** for claiming a protein has been observed: two distinct, uniquely mapping peptides of nine or more residues, covering at least 18 residues of the protein. That standard, and its consequences for short ORFs, is Module 4's subject.
- **HUPO-HIPP** — the HUPO Human Immuno-Peptidome Project, the equivalent standards body for immunopeptidomics data, and a full partner in this consortium alongside HPP. Note that immunopeptidomics arrives here with its own institution rather than as a subtype of proteomics — which is consistent with the tier table keeping HLA and MS in separate columns, though the tier scheme itself was proposed earlier (ref. 25).
- **PeptideAtlas** — the build and certification platform. The paper calls it "the basis for certification of human protein-coding genes through HUPO and the HPP", and the two builds at the heart of this work (2023-06 non-HLA, 2023-11 HLA) are PeptideAtlas builds.
- **ProteomeXchange** — the repository the raw data comes from. Every dataset is a `PXD` accession; every validated spectrum resolves to a Universal Spectrum Identifier at `https://proteomecentral.proteomexchange.org/usi/`. This is the layer that makes the claims auditable by you rather than only by the authors.
- **TransCODE** — launched in 2022 to define standards for reference annotation of ncORFs and their encoded microproteins, and the coordinating body for all of the above.

Now use Fig. 1a rather than reading past it. It is a world map of participating institutions across roughly fifteen countries and four continents, with a two-class legend: **annotation coordinating centre** and **participating centre**. Count the pins in each class and note which institutions are coordinating. (The highlighting is graphical; I could not read it from the text layer, so this one is genuinely yours to do.) Then cross-check against where the paper's coordination actually sits, from the author affiliations: Deutsch and Moritz at the Institute for Systems Biology (PeptideAtlas/HUPO-HPP), Mudge at EMBL-EBI (GENCODE), Kok and van Heesch at the Princess Máxima Center, Valls and Prensner at the University of Michigan, Jungreis at MIT CSAIL and the Broad (ORBL).

The governance point Fig. 1a makes concrete: annotation authority is held by a very small number of coordinating centres, embedded in a large distributed consortium that supplies evidence but does not, on its own, confer status. A hundred laboratories can identify a protein. Three or four institutions decide whether it becomes a gene.

## The GTF in your reference *is* this annotation

This is the part to land hardest, because it collapses the distance between "governance" and "your Tuesday".

When you run `cellranger count` against `refdata-gex-GRCh38-2024-A`, the GTF inside that reference is a GENCODE annotation. The `gene_biotype` values that decide which features your count matrix has rows for, the coordinates that decide which reads are counted where, the symbols that appear in your Seurat object — those are the output of the curatorial process described above. **You are not merely using this annotation; every result you produce is conditioned on it.** This paper changed it.

Make it specific with the module's own example. `OLMALINC` is `ENSG00000235823`, annotated `lncRNA` (Fig. 6e). It carries **six** GENCODE-recognised ncORFs. In your reference, that locus is **one** feature with `gene_biotype "lncRNA"`; the six ORFs on it are not features at all. So if you had run the Fig. 6i experiment yourself, you would have measured the consequences of the knockout on every other gene and never once counted the thing you knocked out. The authors were in exactly that position, which is why the phenotype had to be established by CRISPR and rescue rather than read off a count matrix.

Then there is version drift, which this paper demonstrates on itself. Count the annotation versions in play:

| Where | Version |
|---------|-------|
| **Original ncORF biotypes** (from the source catalogue) | GENCODE v35 |
| **Re-derived biotypes** for the evolutionary analysis | GENCODE v42 |
| **CRISPR meta-analysis** target annotation | GENCODE v45 + phase 1 ncORF annotations |
| **Bulk RNA-seq** quantification (RSEM) | GENCODE v45 |
| **scRNA-seq** alignment | `refdata-gex-GRCh38-2024-A` |
| **Data availability**, primary gene annotations | GENCODE, Ensembl Release 87 |

From the Methods (ORBL section), stated outright: "we redid the biotype determination for the ncORFs using GENCODE v42 annotations (the original biotypes from ref. 4 used v35)". The same 7,264 ORFs, re-typed on a newer release, do not land in the same biotypes — and in [Module 2](02-ncorf-atlas-biotypes.md) you will see exactly how many moved and in which direction. Nothing about the ORFs changed. The **host transcript models** changed, and biotype is defined relative to the host.

The operational lesson: an annotation version is a coordinate system, not a formatting detail. "It's in GENCODE" is not a fact until you say which release, and a biotype is a statement about a locus *in a particular annotation*, not a property of the DNA.

Also worth knowing where the ncORF set actually lives: GENCODE distributes it as a separate **phase 1 Ribo-seq ORF** resource (`https://www.gencodegenes.org/pages/riboseq_orfs/`), which the authors had to explicitly augment their v45 annotation with for the CRISPR meta-analysis (Methods, "Meta-analysis of CRISPR data"). It is not in the main GTF. That is not an oversight — it is the annotation projects declining to assert `protein_coding` while still making the coordinates available. The separation of the file is the governance decision, made visible.

## What this paper actually delivers

Before Module 2, get the shape of the contribution right, because the headline number invites the wrong reading. Four products:

- **A decision procedure** — the six-tier evidence framework of Fig. 5, with an explicit provisional-versus-final split, so that automated integration and human judgement are separately auditable. [Module 8](08-tier-framework-synthesis.md).
- **A vocabulary** — `peptidein`, adopted by five annotation bodies, with 121 initial members.
- **A method** — ORBL, which scores conservation and constraint of *ORFness* rather than of amino-acid sequence. [Module 6](06-evolution-orbl.md).
- **A governance agenda** — seven numbered questions the consortium poses without answering, each a live policy dispute with named stakeholders. [Module 8](08-tier-framework-synthesis.md).

And the headline outcome: **3 new protein-coding gene records out of 7,264 candidates.**

That ratio is the thesis, not a disappointment. The paper's claim is not "we found three genes". It is: here is a procedure that takes 3.5 billion mass spectra plus 240 million immunopeptidomic spectra plus ribosome profiling plus whole-genome alignments across 116 placental mammals plus CRISPR screens in hundreds of cell lines, and yields a handful of gene records that GENCODE, UniProt, HGNC, RefSeq and HUPO-HPP will all stand behind — plus an honest, populated category for the 121 cases where they cannot. A procedure that promoted a thousand ORFs would tell you nothing about its own reliability. This one demotes most of its own top-tier automated calls, and reports that it did.

Which returns you to prediction 4. `c10riboseqorf92` is not a gene, and the reason has nothing to do with the quality of Fig. 6i–j. Hold that open. [Module 8](08-tier-framework-synthesis.md) closes it.

## What I now trust, and why

Write this in your own words before moving on. Some anchors, all positive claims:

- **Two separable questions.** "Does this polypeptide exist?" and "should this locus have a protein-coding gene record?" are different questions with different evidence and different decision-makers. I can now keep them apart, and I expect to find them conflated in most secondary coverage of this field.
- **Annotation is an institution, and I can name it.** GENCODE holds coordinates, UniProt curation, HGNC names, RefSeq the parallel reference, HUPO-HPP and HUPO-HIPP the verification standards, PeptideAtlas the certification build, ProteomeXchange the auditable raw data, TransCODE the coordination. When I read "not annotated", I now know who did not annotate it, and against what criterion.
- **`peptidein` is a real, load-bearing status.** It has a definition, five institutional signatories and 121 initial members. It names the state "this molecule exists and I cannot yet tell you what it does in a healthy human" — which was previously unrepresentable, so such ORFs were absent rather than provisional.
- **Conservatism here is a defensible engineering choice.** Gene records propagate into every downstream reference, panel and target list, and are far harder to retract than to defer. I can argue that asymmetry on its own terms, separately from any claim about the biology.
- **My reference is a curated artefact with a version.** The GTF in my Cell Ranger reference is the output of this process. Biotype is defined relative to host transcript models that change between releases, so a biotype is a claim about a locus in a named annotation version — and I will state the version from now on.
- **The scRNA-seq is competent and beside the point.** Fig. 6i–j is a reasonable, conventional experiment. That it cannot deliver a gene record is a fact about what annotation requires, not a criticism of the experiment.

## Self-check

- [ ] State the identification-versus-annotation distinction in two sentences, without using the word "evidence" in the second one
- [ ] Name four concrete downstream systems that change when a `protein_coding` record is added, and say why retraction is harder than addition
- [ ] Explain what `peptidein` adds beyond `microprotein`, and name the five bodies that adopted it
- [ ] For each of GENCODE, UniProtKB, HGNC, RefSeq, HUPO-HPP, HUPO-HIPP and PeptideAtlas, state in one clause what authority it actually holds
- [ ] Explain why an entry outside the ~20,389-protein neXtProt/Swiss-Prot core set cannot reach `canonical` status in PeptideAtlas, and why that is a governance fact rather than a technical one
- [ ] Say which GENCODE release your most recent Cell Ranger reference was built from, and what would change in your results if it were two releases older
- [ ] Recite the four products of this paper, then explain to a colleague why 3 of 7,264 is the thesis

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| Identification versus annotation | | |
| Ripple effects of adding protein-coding genes | | |
| microprotein / SEP / micropeptide / peptidein | | |
| Who holds which annotation authority | | |
| Annotation versions are not interchangeable | | |
| Why 3 of 7,264 is the thesis | | |

Next: [Module 2 — The ncORF catalogue and its coordinate system](02-ncorf-atlas-biotypes.md). Terms are collected in the [glossary](glossary.md).
