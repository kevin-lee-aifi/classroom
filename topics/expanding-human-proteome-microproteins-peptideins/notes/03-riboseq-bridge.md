# Module 3 — Ribo-seq, from a sequencing person's chair

~2 hrs. Reading, figure work and written reflection only.

This is the module where your existing expertise transfers furthest — and therefore the module where a sloppy analogy would cost you the most. Ribosome profiling produces short reads that you align to a reference and then count. It looks like something you already do. It is not, and the places where the resemblance fails are exactly the places this paper's argument lives.

## Before you read: write down three predictions

Do not skip this. Write the answers somewhere you will not be tempted to edit them.

- [ ] **P1.** Of the 7,264 ncORFs in this paper, how many end up in the tier whose *only* evidence is Ribo-seq? Give a count and a percentage.
- [ ] **P2.** GENCODE, PeptideAtlas, HGNC, UniProtKB and RefSeq all signed off on this paper. Write one sentence describing the criterion you expect them to have used for "this ncORF has sufficient Ribo-seq evidence of translation." Name the statistic.
- [ ] **P3.** Take a uORF — the largest biotype here. In one of your 10x 3′ Gene Expression libraries, what fraction of that uORF's nucleotides do you expect to be covered by reads? Give a number.

Your P2 answer is the one that matters. Most people with a count-matrix background write down an FDR, a posterior probability, or a minimum read count. Hold on to whatever you wrote.

## What this paper does and does not do with Ribo-seq

One orientation point before the mechanics, because it changes how you should read the Methods.

This paper is overwhelmingly a *consumer* of ribosome profiling, not a producer of it. The 7,264 ncORFs are inherited wholesale from the GENCODE Phase I catalogue ([Mudge et al., *Nat. Biotechnol.* 2022](https://www.nature.com/articles/s41587-022-01369-0); cited as ref. 4 throughout, e.g. in the Methods subsection "PeptideAtlas database construction and searching", which describes the search database as including "the 7,264 Ribo-seq ORFs from ref. 4"). The paper's own Ribo-seq work is of two kinds: manual inspection of public aggregate tracks (Methods, "Analysis of Ribo-seq data"), and newly generated ribosome profiling for eight cell lines used only as an expression filter — "only genes with expression levels ≥5 TPM in Ribo-seq and ≥10 TPM in RNA-seq were retained" (Methods, "Analysis of CRISPR screening data: sgRNA mapping and hit calling"; data under `PRJNA1294394`).

Consequently there is **no wet-lab ribosome profiling protocol in these Methods**. Do not go looking for one. The bench mechanics in the next section are sourced from the primers listed at the end, not from this paper. That absence is itself informative: for this consortium, "Ribo-seq evidence" is a property the catalogue arrives with, not a measurement they made.

## Part 1 — The bench mechanics (~20 min)

### What a footprint physically is

The chemistry, in the order it happens:

- **Arrest.** Elongating ribosomes are frozen in place, classically with cycloheximide added to cells before lysis. Cycloheximide has a long-standing reputation for distorting ribosome distributions; a 2021 study argued that humans and other common model organisms are largely resistant to those biases ([*Nat. Commun.* 2021](https://www.nature.com/articles/s41467-021-25411-y)). This is a live methodological question, not settled background.
- **Nuclease footprinting.** The cytoplasmic lysate is digested with a single-strand nuclease, typically RNase I. Everywhere the mRNA is naked it gets shredded; the ~30 nucleotides physically occluded by the ribosome survive. Polysomes collapse to monosomes as the connecting mRNA is digested.
- **Size selection.** The protected fragments are recovered from monosomes and gel-purified. In mammalian systems the dominant footprint length is ~28–30 nt ([Ingolia et al., *Nat. Protoc.* 2012](https://www.nature.com/articles/nprot.2012.086)), with real libraries spreading roughly 25–34 nt.
- **Library construction.** Linker ligation, reverse transcription, rRNA depletion (the nucleases chew rRNA too, so without depletion the library is mostly rRNA), circularisation or second ligation, PCR, sequence. The modern reference protocol puts sample barcodes and random nucleotides serving as UMIs into the 3′ linker ([McGlincy & Ingolia, *Methods* 2017](https://www.sciencedirect.com/science/article/pii/S1046202316303292)).

So: **a Ribo-seq read is a physical cast of a ribosome's position on an mRNA at the moment of lysis.** Its length is set by the ribosome's footprint, not by your fragmentation. Its endpoints are not arbitrary. That single fact is the source of everything in Part 2.

### Two flavours of arrest, and why the paper uses both

Ribosome profiling splits into two experimental strategies, and the paper treats them as two independent lines of evidence:

- **Elongating-ribosome profiling** — the native state. Footprints distributed across the whole ORF body.
- **Initiating-ribosome profiling** — drugs that trap ribosomes at initiation codons, giving a sharp peak at the start codon instead of a body-wide profile. Harringtonine, for example, acts at elongation by binding the A site of the large ribosomal subunit and interfering with the peptidyl transferase reaction, causing rapid polysome disassembly ([GWIPS-viz](https://academic.oup.com/nar/article/46/D1/D823/4103596), which hosts the resulting tracks).

The Methods use both, and — this is the important clause — accept either: "A given ncORF was considered to be verified at the level of Ribo-seq data if either the elongating ribosome or initiating ribosome track data were sufficient or excellent" (Methods, "Analysis of Ribo-seq data"). One track showing a clean initiation peak is enough, even if the body profile is unconvincing. For a 17-codon uORF there is barely any body to profile, so this is not a technicality — it is how short ORFs get supported at all.

## Part 2 — The inferential layer with no counterpart in your work (~30 min)

Everything so far has an analogue in library prep you already know. This part does not.

### From a read to a codon: P site and A site

A ribosome has three tRNA sites. The **P site** holds the peptidyl-tRNA — the codon currently being added to the chain. The **A site** holds the incoming aminoacyl-tRNA — the next codon. A ~29 nt footprint spans both, plus flanking mRNA on either side.

You do not get to observe which codon the ribosome is on. You observe a read's genomic coordinates and then *assign* a codon by adding an **offset** to one end of the read — conventionally the 5′ end. GWIPS-viz, the browser this paper leans on, states the operation plainly: the A-site coordinate (elongating tracks) or P-site coordinate (initiating tracks) "are inferred for each sequence read by adding a specific offset to the coordinate of the most 5′ nucleotide of the read" ([GWIPS-viz: 2018 update](https://academic.oup.com/nar/article/46/D1/D823/4103596)).

Sit with that. The signal you are about to interpret does not exist in the raw data. It is produced by an assignment step, and the assignment can be wrong. Nothing in your pipelines has this property. A 10x read's UMI and cell barcode are literally sequenced; the P site of a footprint is computed.

### Offsets depend on read length — and this is where browsers diverge

The canonical offset is 12 nt from the 5′ end for a 28-mer, which is why 28-mers show the cleanest frame preference. But the offset is not a constant of nature. The riboWaltz authors put it bluntly: "the traditional approach of defining P-site offset as a constant number of nucleotides from either the 3′ or 5′ end of ribosome protected fragments, independently from their length, may lead to an inaccurate detection of the P-site's position owing to potential offset variations associated with the length of the reads" ([riboWaltz, *PLOS Comput. Biol.* 2018](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1006169)).

A library spanning 25–34 nt therefore needs a *per-length* offset table, estimated from the distribution of read ends around annotated start and stop codons. Apply one fixed offset to all lengths and you smear the periodic signal: reads whose true offset differs by one or two nucleotides land in the wrong frame and dilute the real one. This is not a cosmetic issue. It is the difference between seeing three-nucleotide periodicity and seeing noise.

### Three-nucleotide periodicity, and frame as a dimension of the signal

Because footprint ends are set by the ribosome and ribosomes advance one codon at a time, correctly P-site-assigned reads pile up on every third nucleotide. Assign each read's P site to its position modulo 3 relative to the ORF's start codon and you get three separate coverage tracks — frames `0`, `+1` and `+2` — over the same nucleotides.

This is the conceptual move to internalise, and I want to be exact about it:

**Reading frame is not a coordinate. It is a dimension of the measurement.**

In your data, a read has a position and that is the whole of its geometry. In Ribo-seq, a read has a position *and* a phase, and the phase is a measured physical quantity — sub-codon resolution, from a 29 nt read. Two footprints at the same genomic coordinate in different frames are evidence about two different, mutually exclusive translation events. Coverage summed across frames destroys exactly the information you need.

A concrete demonstration that frame is a property of an ORF–transcript pair rather than of a genomic locus: 448 of the 7,264 ncORFs "satisfy no 'pure' biotype criterion" — one cause being an ORF that overlaps a CDS drawn from two different transcripts *in different frames* — and are set aside as `mixed`. There is no single frame to assign, so the evolutionary constraint score is undefined for them ([Module 6](06-evolution-orbl.md) picks this up; see also Extended Data Fig. 7f, which notes the 448 exclusion).

### Calling an ORF from periodicity, and why nobody agrees

Given frame-resolved P-site coverage, an ORF caller asks: is coverage in the frame defined by this candidate start codon significantly enriched over the other two, along a contiguous stretch ending at an in-frame stop? Tools implement that question very differently — ORFquant and RiboTaper work directly off triplet periodicity, RibORF trains a support-vector classifier, PRICE runs an EM algorithm, Ribo-TISH applies a nonparametric rank-sum test on positional counts.

They do not agree. A systematic comparison of five packages on the same high-resolution dataset found only ~2% of small ORFs called translated by all five, and ~15% by three or more — against ~74% five-way agreement for larger annotated genes ([*Brief. Bioinform.* 2024, PMID 38842510](https://pubmed.ncbi.nlm.nih.gov/38842510/)). **`retrieved abstract only`** — the full text was not reachable from where I wrote this, so these three percentages are second-hand. They carry real argumentative weight in the rest of this module, so check them against the paper before you repeat them.

Hold that number against the catalogue's provenance. The 7,264 set is a union: Ribo-seq ORFs from **seven publications**, mapped onto GENCODE v35, filtered to remove ORFs under 16 amino acids and non-ATG initiations, with redundant sense-overlapping ORFs merged ([Mudge et al. 2022](https://www.nature.com/articles/s41587-022-01369-0)). Seven pipelines, seven sets of judgement calls, one merged reference. Nothing about "these 7,264 ncORFs are Ribo-seq supported" means they were called the same way.

The paper measures the consequence directly, which is the single most useful thing in Fig. 2h. Read on.

## Part 3 — What this paper actually accepted as Ribo-seq evidence (~25 min)

Now retrieve your P2 prediction.

### The literal criteria, verbatim from Methods

From the Methods subsection **"Analysis of Ribo-seq data"**, the three grades:

- `excellent` — "four sequential clearly identified Ribo-seq peaks in-frame within the first 100 nucleotides of the ncORF"
- `sufficient` — "three sequential clearly identified Ribo-seq peaks in-frame within the first 100 nucleotides of the ncORF"
- `insufficient` — "there were not clearly sequential in-frame reads"

Verified at the Ribo-seq level = `sufficient` or `excellent`, in *either* the elongating or the initiating track.

That is the whole criterion. Three or four peaks. In frame. In the first 100 nt. Judged by eye. No P value, no FDR, no minimum count, no model. If your P2 answer named a statistic, this is the confrontation — and note that it is not sloppiness. It is a deliberate choice by people who annotate the reference genome, and Part 4 explains why they could afford it.

Two further details in the same subsection worth noticing:

- Some ncORFs originally called by van Heesch et al. (ref. 1) and Gaertner et al. (ref. 76) looked `insufficient` in GWIPS-viz simply because GWIPS-viz does not host those two studies' data. The authors went back to the primary datasets for those. The grade was partly a function of which libraries the browser happened to contain.
- They *did* compute quantitative metrics — "the percentage of in-frame ribosome footprints (PIF) and uniformity of ribosome coverage" — for the ncORFs with peptide support, as observed in the human body map data. `PIF` appears exactly once in the paper, in that sentence. It is reported, not thresholded. The tier assignment ran on the peak-counting rule.

### How many ncORFs fell on each side

Two separate accountings, with two separate denominators. Do not merge them.

**Fig. 2h — the HLA-nominated set.** The authors "manually inspected 859 HLA-I MS spectra and 691 matching Ribo-seq profiles, focusing the latter on ncORFs with at least two uniquely mapping peptides in the HLA build," and validated the Ribo-seq signal in 88.7% (613 of 691). Fig. 2h itself splits that by how many prior studies had reported the ncORF — its x-axis is "Number of studies in which ncORF was detected," binned `1` versus `>1`, with the bars coloured `Insufficient` / `Sufficient`:

| Reported in | Verified | Rate |
|---------|-------|-------|
| **>1 study** | 419 of 436 | 96.1% |
| **1 study only** | 194 of 255 | 76.1% |
| **All inspected** | 613 of 691 | 88.7% |

Both splits reconcile: 436 + 255 = 691, and 419 + 194 = 613. Coordinate-check the panel in your own PDF — the bar values are not printed inside it, so these come from the results text, and the axis labels above are what the panel actually carries.

That 20-point gap between single-study and multi-study ncORFs is the ORF-caller discordance problem showing up as a validation rate — and it is larger than the gap in the pass rates makes it look. Do the arithmetic on the failures, not the passes: **17 of 436** multi-study ncORFs failed inspection (3.9%), against **61 of 255** single-study ncORFs (23.9%). So an ncORF reported by a single pipeline is about **six times** more likely to fail visual Ribo-seq inspection than one reported by several, not the ~1.3× that dividing 96.1% by 76.1% would suggest. (17 + 61 = 78, the `insufficient` total — the arithmetic closes.) Comparing rare-event rates by their complements is a good way to shrink an effect sixfold, and it is worth naming because the same trap sits in every QC pass-rate table you read.

**The tier table — the whole catalogue.** Provisional Tier 3 is `0` and final Tier 3 is `90` (Fig. 5b). Work out why from the Methods definitions: Tier 3 is "any HLA immunopeptidomics and/or tryptic proteome LC–MS/MS evidence *without* Ribo-seq evidence." It is the only tier requiring Ribo-seq `-`. Every ncORF entered with Ribo-seq `+` by construction — that is what being in the catalogue meant — so provisional Tier 3 *had* to be zero, and the 90 final Tier 3 ncORFs are ncORFs that kept their proteomic evidence and lost their Ribo-seq support on manual inspection. (That reading is my inference from the tier definitions plus Fig. 5b, not a sentence in the paper; check it against Fig. 5a's row for Tier 3, which reads `– ± ±`.)

The 78 `insufficient` calls in Fig. 2h and the 90 final Tier 3 ncORFs are **not the same 78–90 ncORFs**, and the numbers are not meant to match. Different denominators, different inclusion rules. Resist the urge to reconcile them.

And the demotion reached the very top of the funnel. Of the 20 candidates the authors advanced for Tier 1A after inspecting MS spectra, "further scrutiny reduced this list to 15 ncORFs due to pseudogenic sequences, a GRCh38 assembly error and insufficient Ribo-seq evidence" ("Annotation of protein-coding ncORFs"). Ribo-seq quality was a rejection criterion for candidate protein-coding genes.

### What the calls rest on — and what they do not

Three properties of this evidence base, all stated in the Methods, all of which you should carry forward:

- **Pooled aggregate tracks, not libraries.** The GWIPS-viz settings were "the elongating ribosomes (A-site) with the global aggregate track on 'full'" and "the initiating ribosomes (P-site) with the global aggregate track on 'full'." A global aggregate track sums Ribo-seq from many studies into one profile. Cell type, drug treatment, library quality and depth are all summed away. There is no per-library signal to inspect and no way to ask whether a peak comes from one deep outlier library or from fifty.
- **Visual inspection, not a model.** "We manually inspected Ribo-seq data for 183 ncORFs … and 699 ncORFs …" — and the Discussion concedes the cost: "our efforts emphasize large-scale manual inspection of both peptide data and ribosome profiling data for annotation purposes. However, manual inspection of thousands of candidates is not feasible for most researchers."
- **Coverage, not completeness.** 183 + 699 ncORFs had their Ribo-seq inspected — call it ~880 of 7,264. The Methods note the 699 as "ncORFs with at least one peptide nominated in the HLA build" while the results describe 691 profiles for ncORFs "with at least two uniquely mapping peptides in the HLA build"; I could not resolve the 699/691 discrepancy from the PDF, so treat the inspected count as approximate. Either way: for roughly 6,400 ncORFs — nearly all of Tier 4 — the Ribo-seq `+` is **inherited from the source catalogue and never re-audited here.** That is not a flaw the authors hide; it is the direct consequence of manual inspection not scaling. But it means Tier 4's Ribo-seq evidence is, on average, weaker than the Ribo-seq evidence behind Tiers 1 and 2.

### Why GWIPS-viz, Trips-Viz and RiboCrypt disagree

Three browsers appear in the Methods, and the reason they were all used is the reason they give different-looking answers.

| Browser | What it is | Why it can disagree |
|---------|-------|-------|
| **GWIPS-viz** (ref. 75) | Genome browser; global aggregate tracks summing many studies; A-site (elongating) and P-site (initiating) tracks | **Fixed offsets applied to all read lengths.** Reads whose true offset differs get mis-phased, so periodicity looks weaker than it is. Also: only hosts the studies it hosts — two of the source publications are absent, which by itself produced `insufficient` grades. |
| **Trips-Viz** (ref. 77) | Transcriptome browser — coordinates are transcript, not genome | **Dynamically calculated read-length-dependent offsets**, so periodicity is clearer. Working in transcript space also means splice junctions and isoform choice are handled explicitly, which changes what "in frame" even means for a given candidate. |
| **RiboCrypt** (ref. 78, `RiboCrypt.org`, part of RiboSeq.Org) | Genome-aligned; "over 3,600 ribo-seq libraries" | Same dynamic read-length-dependent offsets; vastly more libraries, so a weak ORF can accumulate visible signal that is invisible in a smaller aggregate. Depth here is not independent replication. |

The Methods say it directly: "Both additional browsers apply dynamically calculated read-length-dependent offsets leading to periodic signals in the profiles that is clearer than that in GWIPS-viz where fixed offsets are applied for all lengths."

So the disagreement is not a bug, and it is not about interfaces. It is that **the same footprints, phased under different offset models against different transcript coordinate systems and different library pools, yield different frame signals.** The second-phase review of Tier 1A candidates used all three precisely because the tier assignment turns on a judgement no single browser renders reliably — and it explicitly went looking for the failure modes: "validate the support for the translation initiation and termination sites for each candidate while accounting for transcript isoform complexity and regions of poor genomic mappability."

Note the last item. In a low-mappability region, deeper aggregate data can make a spurious ORF look *better*. Your depth intuitions run the wrong way here.

## Part 4 — Why Ribo-seq alone lands you in Tier 4 (~15 min)

Now retrieve P1.

Fig. 5a's row, exactly as printed: **Tier 4 · Ribo-seq `+` · MS `-` · HLA `-` · category `Ribo-seq ORF`.** Methods: "Tier 4: Ribo-seq evidence without proteomic evidence."

Fig. 5b's counts: **5,353 provisional → 5,457 final.** That is 73.7% → 75.1% of 7,264. Three quarters of this catalogue has translation evidence and nothing else. Tier 4 is also the *only* tier that grows under manual inspection — it gains 104 while every other tier shrinks — because it is the sink. An ncORF whose only peptide fails manual spectral inspection has nowhere to fall but here.

The lesson is not that Ribo-seq is unreliable. It is a structural claim about what annotation requires:

**Translation is necessary but nowhere near sufficient for a protein-coding gene record.** A ribosome traversing an ORF in frame is a real event. It does not establish that a stable polypeptide accumulates, that it exists outside the cell line the library came from, or that it does anything. The paper's whole architecture — MS in one column, HLA in another, then function and evolution layered on top — exists because Ribo-seq answers one question and annotation asks four. [Module 8](08-tier-framework-synthesis.md) closes this loop; the conceptual distinction between protein *identification* and gene *annotation* is the spine of the whole curriculum.

### Figure work: what good Ribo-seq evidence looks like

Open your own PDF. Do not read the captions first.

- [ ] **Fig. 6b, top panel.** Frame-coloured P-site coverage over `c2riboseqorf47`, a uORF in `GMCL1`. The panel labels a `Reading frame` legend with three entries — `0`, `+1`, `+2` — an RNA-seq track for comparison, a y-axis labelled `RPF` (the caption defines it: "RPF, ribosome protected fragments"), the ORF with its stop codon, and two overlapping HLA peptides mapped onto its C-terminal region. Spend five minutes on the frame colours alone. That decomposition *is* the evidence: not "there are reads here" but "the reads are in this frame and not the other two." Ask yourself what this panel would look like collapsed to a single coverage track, which is the only form your own pipelines could produce.
- [ ] Note how it was drawn: RiboCrypt, "the sliding-window function calculating moving average of length 9 of P-site coverage," with zoomed regions using "the 'columns' setting and no sliding window to maintain single-nucleotide resolution" (Methods). A 9-nt moving average is three codons — smoothing chosen to preserve periodicity rather than erase it. Compare with how you would smooth a coverage track.
- [ ] **Extended Data Fig. 8a** — the contrast. `c11riboseqorf4`, the 171-aa uoORF in `PIDD1`, with Ribo-seq, mass spectrometry and evolutionary information side by side: "11 distinct peptides across 94 different experiments, 8 of which we classified as excellent evidence." Read only panel `a`. Leave panel `b` alone — you will want it fresh later.

The contrast is the point. `c2riboseqorf47` became protein-coding gene `ENSG00000310604` with **no tryptic MS peptides at all**, carried by Ribo-seq plus HLA plus a loss-of-fitness phenotype plus a high ORBLq score plus cross-species translation evidence. `c11riboseqorf4` is carried by an avalanche of tryptic peptides. Same tier, two completely different evidence shapes, and Ribo-seq is the one column both share. It is the floor, never the ceiling.

## Part 5 — The analogy bridge (~25 min)

This is the centrepiece. Every row has a real breakage. Read the third column first if you are tempted to skim.

| You already know | The Ribo-seq concept it maps onto | Where the analogy breaks |
|---------|-------|-------|
| Reads aligned to a reference; coverage over a transcript | Ribosome-protected footprints aligned to a genome or transcriptome | **Sub-codon phase.** A footprint's position modulo 3 relative to the ORF start is a measured physical quantity, because the ribosome — not your fragmentation — set the read's endpoints. In 3′ GEX there is no per-base geometry at all: every read from a gene collapses into one gene-level UMI count. Even in full-length RNA-seq, phase is meaningless, because fragment ends are random. Frame is real signal in Ribo-seq and pure artefact in every assay you run. |
| UMIs and cell barcodes → per-cell molecule counts | Footprint counts over an ORF | **Neither the numerator nor the denominator survives.** Bulk Ribo-seq has no cell barcode, so "in which cell?" is not a hard question — it is unaskable. And this paper is worse than bulk: it reads *global aggregate tracks* summed across studies, cell types and drug treatments. UMIs do sometimes exist ([McGlincy & Ingolia 2017](https://www.sciencedirect.com/science/article/pii/S1046202316303292) puts them in the 3′ linker), but a Ribo-seq UMI deduplicates PCR copies of a footprint — it does not count mRNA molecules. A footprint count is ribosome occupancy: number of ribosomes × dwell time, integrated over the lysate. Double the count can mean twice the translation, or the same translation with ribosomes stalled twice as long. Nothing is conserved; there is no molecule to count. |
| Coverage-depth and detection intuitions — "expressed in ≥N cells", "≥10 TPM", more depth is always better | "Is this ORF translated?" | **Three separate failures.** (1) *Scale*: a 17-codon uORF offers ~51 nt. The paper's rule inspects only the first 100 nt and asks for three or four sequential in-frame peaks — a pattern over a handful of codons, which no count threshold can express. (2) *Direction*: deeper pooled data can make a spurious ORF look better, via footprints from the host mRNA in a different frame, a neighbouring CDS, or multimapping — hence the Methods' care over "regions of poor genomic mappability." (3) *Replication*: 3,600+ libraries summed into one track is depth, not replicates. There is no dispersion, no design matrix, no FDR. Your instinct that a bigger n tightens a confidence interval does not apply to an aggregate track. |
| 5′ vs 3′ library chemistry and where reads land on a transcript | Where on a transcript the assay samples | **Ribo-seq has no privileged transcript end.** Your assay's sampling geometry is set by library chemistry — poly-A-proximal for 3′ GEX, TSS-proximal for 5′ GEX. A footprint's position is set by where a ribosome sat. This inverts the usual reasoning: you normally ask "does my chemistry reach this region?"; in Ribo-seq you ask "did a ribosome go there?", and coverage gaps are biology, not chemistry. Section below — this row is the practical payoff. |
| A reference GTF / Cell Ranger reference as ground truth | The GENCODE Phase I ncORF catalogue | **A GTF row cannot hold a frame, and a merged catalogue is not a curated one.** Add a uORF to a GTF and gene-level counting still assigns its reads to the host gene or discards them as ambiguous — the ORF is a sub-region of a transcript, not a feature your counter can separate. And this "reference" is a union of calls from seven publications on GENCODE v35, not one build. The paper measures the cost: single-study ncORFs validated at 76.1% versus 96.1% for multi-study ones (Fig. 2h). |
| Pseudobulk aggregation before DE | The GWIPS-viz global aggregate track | **Pseudobulk keeps sample identity; the aggregate track destroys it.** Your own workflow — and this paper's Fig. 6i — aggregates *per sample*, keeps the labels, and fits `~0 + condition + scsplit_assignment` with an error model. The global aggregate track discards library identity entirely. Same word, opposite epistemics: one enables inference, the other forecloses it and leaves visual inspection as the only available move. |

### The row that matters most: 5′ versus 3′ geometry

`uORF` is the single largest biotype in this catalogue: **3,083 of 7,264** (Fig. 1b, coordinate-verified). The ORBL section's figure of 2,915 uORFs is not a contradiction and not an exclusion: the biotypes were re-derived on GENCODE v42 while the catalogue itself was built on v35, and across that version change `intORF`, `doORF` and `lncRNA ORF` all *gain* members — which no exclusion criterion can do. The two counts are measuring the same ORFs against different annotation builds and are simply not comparable; use whichever build's figure matches the analysis you are reading. [Module 2](02-ncorf-atlas-biotypes.md) owns the version-drift treatment. uORFs sit in 5′UTRs, upstream of the annotated start codon.

A 10x 3′ Gene Expression library reverse-transcribes from the poly-A tail and is sequenced from the 3′ end. Reads pile up within a few hundred nucleotides of the polyadenylation site. **A 5′UTR contributes no reads by construction.** This is not a sensitivity problem that more depth or more cells would fix. It is the library geometry. Your P3 answer should have been zero, or close to it — and if you wrote something higher, that is the most useful wrong prediction in this module.

5′ GEX is genuinely better positioned: template switching puts the barcode at the 5′ end and reads land TSS-proximally, overlapping the sequence a uORF occupies. But two things still stand in the way. First, Cell Ranger's output is a gene × cell UMI matrix — position and phase are discarded before you ever see the data, and a per-gene count cannot express "in frame `0` and not `+1`." Second, and decisively: 5′ GEX measures **transcript abundance**, not ribosome occupancy. A 5′UTR present in a transcript tells you the uORF's sequence is there. It tells you nothing about whether a ribosome initiated on it.

And note the biotype asymmetry, because it bites differently across the catalogue. `lncRNA ORF` (1,917) and `dORF` (504) sit on transcripts you can at least quantify as distinct features. `uORF` (3,083), `uoORF` (688), `intORF` (720) and `doORF` (61) are sub-regions of transcripts whose gene-level count is dominated by the canonical CDS — so even a perfectly annotated reference gives you one number per gene, in which the ncORF contributes nothing separable. Probe-based assays are worse still: a Visium or Xenium panel targets a gene, and a uORF is not a separate gene. There is no probe you could design that distinguishes "this transcript's uORF is being translated" from "this transcript is present."

### The hard limit, stated plainly

**None of 3′ GEX, 5′ GEX, scATAC, Visium or Xenium measures translation.** Three measure transcript abundance in one geometry or another; one measures chromatin accessibility. Your entire platform stack is blind to this paper's core measurement, and no combination of them substitutes for a footprint.

That is not a criticism of your work, and it is not a gap you should feel any need to close. It is the reason this paper needed ribosome profiling, digest mass spectrometry ([Module 4](04-mass-spec-proteomics.md)) and HLA immunopeptidomics ([Module 5](05-immunopeptidomics.md)) as three separate evidence columns. Each answers a question the others cannot.

And there is a genuinely satisfying coda. Your toolchain *is* in this paper — Fig. 6i–j runs 10x GEM-X 3′ GEX v4, Cell Ranger v9.0.1 `multi` against `refdata-gex-GRCh38-2024-A`, SoupX, `AggregateExpression` pseudobulk, edgeR TMM and limma-voom across n = 12 cell lines. It enters as the **downstream transcriptional readout of an ncORF knockout**, not as the discovery instrument. That is exactly the right role for it, and it is where [Module 7](07-function-crispr-olmalinc.md) picks up.

## Write this down

Ten minutes, in prose, before you close the module.

- [ ] Compare your P2 prediction with "three sequential clearly identified in-frame peaks within the first 100 nucleotides." Would you have signed off on that criterion for a reference annotation used by every human geneticist on earth? Argue one side.
- [ ] Explain three-nucleotide periodicity in four sentences, to a colleague who does bulk RNA-seq, without using the word "frame" more than once.
- [ ] Name one Ribo-seq quality-control judgement you would want to see for a Tier 4 ncORF that the aggregate-track approach structurally cannot give you. Then say whether a statistical ORF caller would actually have given it to you, given the ~2% five-way agreement figure (`retrieved abstract only`, per Part 2).
- [ ] One sentence: why does the 20-point validation-rate gap between single-study and multi-study ncORFs (Fig. 2h) follow from how the 7,264 catalogue was built?

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| Footprint chemistry: arrest → nuclease → size selection → library | | |
| Elongating vs initiating profiling, and why either suffices here | | |
| P-site / A-site assignment as an inference, not an observation | | |
| Read-length-dependent offsets | | |
| Three-nucleotide periodicity; frame as a dimension, not a coordinate | | |
| ORF calling from periodicity, and inter-tool discordance | | |
| The paper's `excellent` / `sufficient` / `insufficient` rule | | |
| Fig. 2h: 613 of 691, and the single- vs multi-study split | | |
| Aggregate tracks and visual inspection — what they foreclose | | |
| GWIPS-viz vs Trips-Viz vs RiboCrypt: why offsets make them disagree | | |
| Tier 4 = Ribo-seq only, 5,457 of 7,264 | | |
| Why translation is necessary but not sufficient for annotation | | |
| The four analogy breakages, in your own words | | |
| Why 3′ GEX is structurally blind to 3,083 uORFs | | |

## What I now trust, and why

Write your own version. Mine, as a model:

- **I trust that these ncORFs are translated.** Three quarters of this catalogue rests on Ribo-seq alone, and that is a real, physical, reproducible measurement: a nuclease-protected cast of a ribosome, phased to a codon, recurring every third nucleotide in one frame and not the other two. Frame preference is not something noise produces. When the paper says Tier 4, it is making a defensible claim.
- **I trust the direction of the paper's errors.** Manual inspection was net-demoting — Tier 4 grew by 104 and every other tier shrank — insufficient Ribo-seq evidence knocked candidates out of the Tier 1A funnel, and 90 ncORFs lost their Ribo-seq `+` outright. A curation process whose errors run toward caution is one I can build on.
- **I trust Fig. 2h as an honest self-audit.** The authors could have reported 88.7% and stopped. Instead they split it by prior-study count and published the 76.1% figure for single-study ncORFs, which is an admission that their inherited catalogue is uneven. That is the behaviour of people reporting a weakness they expect to be checked on.
- **I trust that reading frame is now a real object to me.** That is the transferable win. Position plus phase, where phase is measured — not position alone. It is the one dimension of sequencing data my platforms cannot produce, and I can now say precisely why: my reads' endpoints are set by chemistry, and a footprint's are set by a ribosome.
- **I trust my own instruments more, not less, for knowing their edges.** 3′ GEX cannot see a uORF, and now I know that is geometry rather than sensitivity — which means I will never again waste a week trying to fix it with depth. Meanwhile Fig. 6i–j shows exactly what my stack is *for* in this field: the high-resolution phenotypic readout after someone else has established that the ORF is translated.

## Sources

Paper anchors above are to the Methods subsections "Analysis of Ribo-seq data", "Analysis of CRISPR screening data: sgRNA mapping and hit calling", "Use of the tier classification system" and "PeptideAtlas database construction and searching"; to the results sections "Microproteins as HLA-I-presented peptides" and "Annotation of protein-coding ncORFs"; to the Discussion; and to Figs 1b, 2h, 5a, 5b, 6b and Extended Data Figs 7f and 8a. Quotations are short and attributed; the article is CC BY-NC-ND 4.0, so read the figures in your own copy — nothing is reproduced here.

Background primers, retrieved 2 September 2026. These cover the bench mechanics and the offset/periodicity theory, none of which is in this paper. The full texts were not reachable from this environment, so the specific figures above are as reported in retrieved abstracts and summaries rather than read in situ — worth spot-checking if you lean on any of them:

- [Ingolia et al., "The ribosome profiling strategy…", *Nat. Protoc.* (2012)](https://www.nature.com/articles/nprot.2012.086) — the reference footprinting protocol; ~28–30 nt eukaryotic footprints, RNase treatment, rRNA depletion.
- [McGlincy & Ingolia, "Transcriptome-wide measurement of translation by ribosome profiling", *Methods* (2017)](https://www.sciencedirect.com/science/article/pii/S1046202316303292) — modern protocol; sample barcodes and UMIs in the 3′ linker.
- ["Humans and other commonly used model organisms are resistant to cycloheximide-mediated biases in ribosome profiling experiments", *Nat. Commun.* (2021)](https://www.nature.com/articles/s41467-021-25411-y).
- [riboWaltz, *PLOS Comput. Biol.* (2018)](https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1006169) — read-length-dependent P-site offsets and why fixed offsets mis-phase reads.
- [Michel et al., "GWIPS-viz: 2018 update", *Nucleic Acids Res.* 46](https://academic.oup.com/nar/article/46/D1/D823/4103596) — global aggregate tracks; A-site/P-site inferred by adding an offset to the read's most 5′ nucleotide. This is the paper's ref. 75, where the reference list prints it as *Nucleic Acids Res.* 46, gkx790 (2017).
- ["Comparison of software packages for detecting unannotated translated small open reading frames by Ribo-seq", *Brief. Bioinform.* 25(4), bbae268 (2024)](https://pubmed.ncbi.nlm.nih.gov/38842510/) — five smORF callers on one dataset: ~2% agreement across all five, ~15% at three or more, versus ~74% for larger annotated genes.
- [Mudge et al., "Standardized annotation of translated open reading frames", *Nat. Biotechnol.* 40, 994–999 (2022)](https://www.nature.com/articles/s41587-022-01369-0) — the paper's ref. 4; the 7,264-ORF Phase I catalogue collated from seven publications onto GENCODE v35, filtered at 16 aa and ATG starts, redundant sense-overlapping ORFs merged.
- Browser references as printed in this paper's own reference list, for orientation: Kiniry et al., Trips-Viz, *Nucleic Acids Res.* 49, W662–W670 (2021) — ref. 77; Tierney et al., RiboSeq.Org, *Nucleic Acids Res.* 53, D268–D274 (2025) — ref. 78. I have not independently retrieved either, so take the bibliographic details from the PDF rather than from here.
