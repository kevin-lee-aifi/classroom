# Glossary

The single canonical glossary for this curriculum. Every term is defined **as this paper uses it**, not as the wider literature might.

Anchors in parentheses name the section, figure or Methods subsection the definition comes from. Entries marked `unverified` are terms the paper uses without defining, where the definition given here comes from general usage rather than from this text — check them before relying on them in writing.

## Open reading frames and biotypes

- **ORF (open reading frame)** — for ORBL's purposes, a stretch beginning at an ATG, ending at an in-frame stop, with no in-frame stop between; selenoproteins and non-ATG-initiated CDSs are explicitly excluded from ORF comparisons (Methods, ORBL).
- **CDS (coding sequence)** — the span of a transcript annotated as encoding a protein, start codon to stop codon. In this paper, "the CDS" of a transcript is the *annotated* protein-coding region, and ncORF biotypes are defined relative to it (Fig. 1b).
- **ncORF (non-canonical open reading frame)** — an ORF with evidence of translation that is not an annotated CDS. All 7,264 entries in this study are ncORFs supported by GENCODE (main text, "A microprotein annotation workflow").
- **Biotype** — an ncORF's classification by position relative to its host transcript and that transcript's CDS. Five of the seven are positional; two are defined by the host having no CDS (Fig. 1b; [Module 2](02-ncorf-atlas-biotypes.md)).
- **uORF (upstream ORF)** — an ncORF within the 5′ UTR, terminating before the CDS begins. 3,083 ncORFs, 42.4%, the largest class (Fig. 1b). Positional detail beyond the name: `unverified`, from ref. 4's nomenclature.
- **uoORF (upstream overlapping ORF)** — initiates in the 5′ UTR and overlaps the CDS out of frame. 688, 9.5% (Fig. 1b); overlap with CDS confirmed in the ORBL section.
- **intORF (internal ORF)** — contained within the CDS, in a different reading frame from it. 720, 9.9% (Fig. 1b; ORBL section).
- **doORF (downstream overlapping ORF)** — initiates within the CDS and terminates past the CDS stop. 61, 0.8% — the rarest biotype (Fig. 1b; ORBL section).
- **dORF (downstream ORF)** — an ncORF within the 3′ UTR, beginning after the CDS ends. 504, 6.9% (Fig. 1b caption, which expands the abbreviation).
- **lncRNA ORF** — an ORF on a transcript of a gene annotated as a long non-coding RNA, so there is no CDS to be positioned against. 1,917, 26.4% (Fig. 1b).
- **Processed-transcript ORF** — an ORF on a transcript whose GENCODE transcript biotype is `processed_transcript`, carrying no annotated CDS of its own. 291, 4.0% (Fig. 1b; Fig. 2e caption abbreviates it "Proc. tr. ORFs"). The `processed_transcript` biotype definition itself: `unverified`.
- **`mixed` biotype** — the 448 of 7,264 ncORFs satisfying no 'pure' biotype criterion after re-derivation on GENCODE v42, for example ORFs overlapping CDS from two different transcripts in different reading frames. ORBLq is **undefined** for them and they are excluded, which is why later analyses run on 6,816 (Methods, ORBL).
- **Frame +1 / +2** — the shift of an overlapping ncORF relative to the host CDS. Overlapping biotypes are never in frame 0 (that would make them the same protein), and the two shifts are treated as separate classes because the host's amino-acid constraint imposes different ORFness constraint on each (Methods, ORBL).
- **Phase 1 Ribo-seq ORFs** — GENCODE's distribution of the ncORF set as a resource separate from the main annotation, which the authors had to explicitly add to GENCODE v45 for the CRISPR meta-analysis (Methods, meta-analysis of CRISPR data).
- **smORF / sORF (small open reading frame)** — a short ORF, used in the wider literature as the genomic counterpart of "microprotein". This paper uses the strings only inside contributed-dataset names (`CONTRIB_smORFs_Cui`, `CONTRIB_sORFs`; Methods, categorizing HLA peptides) and never defines the term. `unverified`.

## Proteins, products and nomenclature

- **Microprotein** — the translation product of an ncORF. The Introduction notes these are "variably referred to as microproteins, small ORF-encoded peptides (SEPs) or micropeptides" and standardises on **microprotein** as shorthand; it does not argue the three terms denote different things.
- **SEP (small ORF-encoded peptide)** — a synonym for microprotein in the wider literature, named and set aside by the Introduction. No independent definition is given here.
- **Micropeptide** — likewise a synonym named and set aside by the Introduction. No independent definition is given here.
- **Peptidein** — the paper's new annotation category. In the Results: an ORF with experimentally confirmed RNA translation and protein synthesis, but for which the data are currently insufficient to claim conventional protein-coding gene status ("Peptideins: candidates of unclear status"). In the Discussion: a translation product confidently detected endogenously, but for which a role in normal physiology cannot be verified at the present time, explicitly including potentially transient products of cellular stress or defective ribosome translation. Note the Results definition attaches to an **ORF** and the Discussion definition to a **product** — the slippage is the paper's.
- **Candidate protein** — annotation criteria, all three required: detection meeting HUPO-HPP criteria, presence in healthy cells, and evidence of function (Fig. 5d).
- **Candidate peptidein** — annotation criteria: detection need not meet HUPO-HPP criteria, may come from normal *or* cancer cells, and function may be unknown or absent (Fig. 5d).
- **Canonical protein** — in PeptideAtlas, a protein with ≥2 uniquely mapping non-nested peptides of ≥9 aa together covering ≥18 aa; critically, only entries belonging to the core set of ~20,389 neXtProt and UniProtKB/Swiss-Prot protein-coding genes **can** achieve `canonical` status at all (Methods, protein identifications and categories).
- **Non-core canonical** — an entry meeting the two-peptide criteria with peptides that cannot be mapped to the core proteome (Methods, protein identifications and categories).
- **Canonical versus non-canonical peptide** — in the HLA build's categorisation: canonical = ≥8 aa mapping to Swiss-Prot entries with ≤30 distinct mappings; non-canonical = ≥8 aa mapping to ncORFs and not to canonical proteins, with ≤10 distinct mappings; everything else is "other peptides" (Methods, categorizing HLA peptides).
- **DRiP (defective ribosomal product)** — a translation product of erroneous or aborted translation, invoked by the Discussion as a category peptideins may include; cited to ref. 40 (Yewdell & Hollý, *Curr. Opin. Immunol.* **64**, 130–136, 2020). The expansion of the acronym is `unverified` against this text.

## Ribosome profiling

- **Ribo-seq (ribosome profiling)** — sequencing of ribosome-protected mRNA fragments; the evidence type that admitted all 7,264 ncORFs to the catalogue and the `+`/`−` in the first column of the tier table (main text; Fig. 5a).
- **RPF (ribosome protected fragments)** — the sequenced fragments themselves (Fig. 6b caption).
- **P-site** — the ribosomal peptidyl site; in this paper's Ribo-seq inspection, the **initiating**-ribosome track, used to locate start codons, as against the A-site track which reflects elongating ribosomes and native Ribo-seq signal (Methods, manual inspection of Ribo-seq via GWIPS-viz).
- **GWIPS-viz** — the public genome browser used for manual Ribo-seq inspection, chosen so that readers can independently reproduce the authors' assessment; global aggregate tracks on "full" for both A-site and P-site (Methods; ref. 75).
- **RiboCrypt / Trips-Viz / RiboSeq.Org** — the further Ribo-seq visualisation tools used for area plots and single-nucleotide-resolution views (Methods; refs. 77, 78).

## Mass spectrometry

- **PSM (peptide spectrum match)** — one assignment of one MS/MS spectrum to one peptide sequence. The non-HLA build contains 573 million; the HLA build 28 million (Fig. 1b).
- **MS run** — one instrument acquisition. ~85,000 in the non-HLA build and 9,776 in the HLA build; the abstract's "95,520 proteomics experiments" corresponds to run totals, not to PeptideAtlas "experiments" (1,172 + 592) (Fig. 1b; Methods).
- **Protease-specific versus no-protease search** — the non-HLA build was searched with semi-enzymatic (typically semi-tryptic) settings; the HLA build in **no-enzyme mode**, because proteasomal products do not end at K or R (Methods, PeptideAtlas database construction and searching).
- **Target–decoy (entrapment) approach** — FDR estimation by adding scrambled versions of every target sequence at 1:1, so mistaken assignments to targets can be estimated as 1:1 with mistaken assignments to decoys; "entrapment" means the pipeline is not told which are decoys (Methods, FDR estimation).
- **FDR (false discovery rate)** — here, decoy-estimated. Set at <0.1% at the protein level, achieving peptide-level FDR of 0.0009% (non-HLA build) and 0.0041% (HLA build) — deliberately more conservative than typical studies because annotation-grade evidence demands it (main text, "A microprotein annotation workflow").
- **HUPO-HPP criteria** — two distinct, uniquely mapping, non-nested peptides of ≥9 amino acids, together covering ≥18 amino acids of the protein (main text, citing ref. 15, *HPP MS data interpretation guidelines 3.0*). The threshold that agenda question 1 asks whether to rewrite for short ORFs.
- **Manual PSM categories** — the five outcomes of human spectrum review: `excellent`, `good`, `false positive`, `close but false positive`, `low information` (Methods, manual inspection of ORF MS spectra).
- **USI (Universal Spectrum Identifier)** — a resolvable identifier for one spectrum, recorded for each validated PSM and viewable at `https://proteomecentral.proteomexchange.org/usi/`; where no USI is possible, a direct PeptideAtlas spectrum-viewer URL is given instead (Methods, procedure for manually validating PSMs).
- **PRM (parallel reaction monitoring)** — targeted MS used here to confirm endogenous expression, with isotopically labelled synthetic peptides spiked into cultured-cell tryptic digests (main text; Extended Data Fig. 3; Methods, multiplexed PRM MS of ncORF targets).
- **DDA / DIA (data-dependent / data-independent acquisition)** — this work is DDA only; the Discussion names DIA, especially coupled with targeted PRM validation, as a stated limitation and a route to greater sensitivity.
- **PTM (post-translational modification)** — chemical modification of a residue after translation; several were found on ncORF-encoded microproteins, and generic artefactual modifications were searched as variables throughout (main text; Methods).
- **MSFragger / Trans-Proteomic Pipeline (TPP) / PeptideProphet / iProphet / PTMProphet / ProteoMapper** — the search engine (MSFragger v3.7) and statistical-validation and peptide-mapping toolchain used for both builds (Methods).

## Immunopeptidomics

- **HLA (human leukocyte antigen)** — the human MHC. HLA-typed samples define the second PeptideAtlas build (main text, "A microprotein annotation workflow").
- **HLA-I / HLA-II** — class I presents peptides from the intracellular protein pool; class II largely from extracellular sources. 2,937 of 3,116 ncORF-derived HLA peptides (94.3%) were found on HLA-I alone, which the paper reads as evidence that microproteins are sourced intracellularly (main text, "Microproteins as HLA-I-presented peptides").
- **Immunopeptidome** — the population of peptides recovered from HLA molecules of a sample. The HLA build comprises 118 HLA immunopeptide-enriched ProteomeXchange datasets (Fig. 1b; Methods).
- **HLA typing** — the sample's HLA alleles, retrieved at full four-digit resolution by manually searching the publication behind each MS run. **The number of typed runs is reported three ways and they disagree**: 4,879 (Methods, annotating immunopeptidomics MS runs), 4,870 (main text, "4,870 of the 6,479 MS runs", and again as the denominator of 4,308/4,870 = 88.5%) and 4,869 (Fig. 2i caption and panel). Quote whichever your context needs and say where you got it; none of the three is *the* number.
- **NetMHCpan** — the HLA-I binding predictor used (v4.1); a peptide is called a predicted binder at percentage **rank score** ≤2, and where a run has multiple alleles the peptide is assigned to the allele with the lowest rank (Methods, HLA binding predictions).
- **Percentage rank score** — a peptide's predicted binding strength expressed as its rank against random peptides for that allele; lower is stronger, ≤2% is the binder threshold used here (Methods).

## Evolutionary analysis

- **ORBL (ORF relative branch length)** — the paper's method: from multispecies whole-genome alignments, quantify conservation of **ORFness** — the initiation codon, the termination codon, and the openness of the reading frame — **without regard to amino-acid conservation** (main text, "Evolutionary insights to interpret ncORFs"; Fig. 4a).
- **Branch length** — phylogenetic branch length in the whole-genome alignment, used as the currency of conservation. Denominators are all 116 placental or all 26 primate species in the alignment, not merely those present in the local alignment (Methods, ORBL; alignment from ref. 83).
- **ORBLv** — the ORBL **conservation** score: branch length of species in which the ORF is conserved, divided by total branch length of the clade (Fig. 4a caption; Methods).
- **ORBLq** — the ORBL **constraint** score: the quantile of an ncORF's ORBLv among the ORBLv values of ≥1,000 matched untranslated ORFs of the **same biotype and similar length**. Undefined for `mixed`-biotype ORFs (Fig. 4a caption; Methods). The hardest idea in the paper — see [Module 6](06-evolution-orbl.md).
- **Conservation versus constraint** — the paper's own distinction, and the reason ORBL has two scores: conservation (ORBLv) is what you observe, and can arise by chance in short sequences or for free from an overlapping CDS; constraint (ORBLq) is conservation in excess of a length- and biotype-matched null, and is what implies selection (Fig. 4a caption).
- **Untranslated ORF (matched set)** — the null population for ORBLq: 1,717,927 ATG-initiated ORFs in protein-coding or lncRNA transcripts of GENCODE v42 that do not overlap a CDS in the same frame, after several exclusions, split into nine biotype-and-frame classes (Methods, ORBL).
- **PhyloCSF** — a comparative-genomics codon-substitution method that scores protein-coding *amino-acid* conservation (ref. 24, Lin, Jungreis & Kellis, 2011). Used here as the contrast to ORBL: only 143 of 7,264 ncORFs (2.0%) reach PhyloCSF > 10, against 2,211 (30.4%) with placental-mammal ORBLq > 0.9 (main text; Fig. 4f).
- **MANE Select** — the single matched RefSeq/Ensembl transcript per gene, used here as the reference CDS set in ORBLv distribution comparisons (Methods, ORBL; Extended Data Fig. 7b,c). Expansion of the acronym: `unverified`.

## Structure prediction

- **pLDDT** — the per-residue confidence score output by protein-structure predictors, averaged per ncORF and compared across tiers here for AlphaFold3, ESMFold and OmegaFold (Extended Data Fig. 10b–d). The expansion "predicted local distance difference test" is `unverified` against this text.
- **Shuffled-sequence control** — the paper's check on pLDDT: 581 sequences with pLDDT > 90 were each shuffled five times, giving 2,905 shuffled sequences, to test whether high confidence survives randomising the residue order (Extended Data Fig. 10e,g,h). Worth knowing because pLDDT rises as ncORF length falls (Extended Data Fig. 10f).

## Functional genomics

- **CRISPRa (CRISPR activation)** — transcriptional activation rather than cutting. Used here as a control: CRISPRa data from a matching cell line was checked to rule out that a uORF knockout is toxic because it de-represses an anti-proliferative adjacent CDS (main text; Extended Data Fig. 9e,f; library from ref. 31).
- **Tiling screen** — a CRISPR screen with guides tiled densely across a locus, so effects can be localised within a transcript rather than attributed to a whole gene. Enrichment scores here are computed against the **local background**, which may contain other adjacent ncORFs or CDSs (main text; Fig. 6c,d).
- **Saturation mutagenesis screen** — the published dense-tiling datasets reanalysed for hit prioritisation (main text, functional genomics section; refs. 7, 28).
- **Gene-specific permutation test** — the null model for tiling significance: for an ncORF with *n* guides, resample *n* guides from all guides targeting the **same parental gene**, so the ncORF is tested against its own host locus rather than the genome (Methods, CRISPR tiling analysis).
- **Chronos** — the model used to convert raw screen counts into fitness scores, incorporating copy-number data from DepMap; hits are calls beyond ±0.5 (Methods; ref. 84).
- **Pan-essential** — operationally, an ORF essential in ≥60% of evaluated samples (Methods, meta-analysis of CRISPR data). Pan-essential proteins are singled out because they are central to core cell functions and common drug targets (main text).
- **DepMap (Dependency Map)** — the Broad's cancer dependency resource; used here for copy-number correction, for SNP profiles in single-cell demultiplexing (release 25Q2), and for the co-essentiality correlation of `c10riboseqorf92` against 17,110 genes across 485 cell lines (Fig. 6g; Methods).
- **PRISM** — the pooled barcoded cell-line platform used for the `c10riboseqorf92` knockout across 486 barcoded lines (Methods, pooled `c10riboseqorf92` knockout).
- **CRISPR–Cas13** — RNA-targeting rather than DNA-cutting screening, used as orthogonal support for the `OLMALINC` dependency (Extended Data Fig. 9j; ref. 85).
- **e-distance (energy distance)** — the per-cell-line measure of transcriptional shift from the non-targeting control in PCA space (15 components), defined as twice the mean between-group distance minus the mean within-group distance (Methods; ref. 87).

## Tiers and annotation status

Tier definitions are quoted in substance from Methods, "Use of the tier classification system"; the evidence signature grid is Fig. 5a.

- **Tier 1A** — two non-nested peptides in MS proteome data, with or without HLA data, with Ribo-seq. Category: *candidate protein*. Provisional 37 → final 16 (Fig. 5b).
- **Tier 1B** — two non-nested peptides in HLA immunopeptidomics data with Ribo-seq, and no MS peptides. Category: *presented*. Provisional 665 → final 601.
- **Tier 2A** — one peptide in MS proteome data, with or without HLA data, with Ribo-seq. Category: *detected*. Provisional 146 → final 39.
- **Tier 2B** — one peptide in HLA immunopeptidomics data with Ribo-seq. Category: *detected*. Provisional 1,063 → final 1,059.
- **Tier 3** — any HLA and/or tryptic MS evidence **without** Ribo-seq evidence. Category: *putative*. The only tier requiring Ribo-seq absent, so its provisional count is 0 and it fills only by demotion: final 90.
- **Tier 4** — Ribo-seq evidence without proteomic evidence. Category: *Ribo-seq ORF*. Provisional 5,353 → final 5,457.
- **Tier 5** — in-silico prediction of an ORF on an expressed transcript, without any Ribo-seq or proteomic evidence. Defined in Methods but **not** a row in Fig. 5a and not populated in this study, since Ribo-seq support is the catalogue's entry criterion.
- **Provisional versus final tier** — provisional tiers are assigned computationally by integrating the three data types; final tiers are assigned after manual inspection of every spectrum and Ribo-seq track. Manual inspection is net-demoting: Tier 4 grows by 104 and every other tier shrinks (Fig. 5a,b).
- **Evidence notation** — in Fig. 5a, `+` denotes detection, `++` abundant detection, `±` either presence or absence of detection, `−` absence of detection (Fig. 5 caption).

## Institutions and resources

- **TransCODE Consortium** — launched in 2022 to define standards for the reference annotation of ncORFs and their encoded microproteins; the coordinating body for this work, and the entity that convened GENCODE, PeptideAtlas, HUPO-HPP and HUPO-HIPP (main text, Introduction; ref. 4). Fig. 1a distinguishes *annotation coordinating centres* from *participating centres*.
- **GENCODE** (Ensembl-GENCODE) — the reference annotation of gene, transcript and CDS **coordinates** for human and mouse; the content of a GTF. Annotated the three new protein-coding genes here, plus `ENSG00000310604` separately. The gene-annotation work in this study was done as part of the ongoing GENCODE project using existing workflows (Methods, gene annotation; ref. 11).
- **UniProtKB/Swiss-Prot** — the manually **curated** protein sequence and function knowledgebase. Named jointly with GENCODE in the Introduction as the projects responsible for curation and maintenance of protein-coding genes (ref. 69).
- **HGNC** — the HUGO Gene Nomenclature Committee, which assigns gene **symbols** (author affiliation 19). A signatory to the peptidein decision (agenda question 6).
- **RefSeq** — NCBI's reference sequence annotation, independent of Ensembl-GENCODE; a source of primary gene annotations here and a signatory to the peptidein decision (Data availability; agenda question 6).
- **HUPO-HPP** — the Human Proteome Organization's Human Proteome Project, which sets the **verification standard** for claiming a human protein has been observed and publishes annual proteome metrics (refs. 13, 15, 66–68).
- **HUPO-HIPP** — the HUPO Human Immuno-Peptidome Project, the standards body for immunopeptidomics data and a full partner in this consortium alongside HPP (ref. 14, Caron *et al.*, *Immunity* **47**, 203–208, 2017).
- **PeptideAtlas** — the build and certification platform, described here as "the basis for certification of human protein-coding genes through HUPO and the HPP". The two builds central to this work are the 2023-06 non-HLA and 2023-11 HLA builds; the ncORF results are public at `https://peptideatlas.org/builds/human/#ncORFs`.
- **ProteomeXchange** — the MS data repository the raw data comes from; each dataset is a `PXD` accession (ref. 50). The layer that makes individual spectra independently auditable.
- **THISP** — the tiered search database from which the sequence databases were drawn: the 2023-02 THISP level 4 database for the non-HLA build and 2023-07 for the HLA build, each including the 7,264 Ribo-seq ORFs plus other contributed sequences that might be translated, at `https://peptideatlas.org/thisp/` (Methods; ref. 52, Deutsch *et al.*, "Tiered human integrated sequence search databases for shotgun proteomics", *J. Proteome Res.* **15**, 4091–4100, 2016).
- **neXtProt** — the human protein knowledgebase whose ~20,389-entry core proteome defines what can reach `canonical` status in PeptideAtlas, for consistency with HPP annual metrics (Methods, protein identifications and categories; ref. 64).
- **GTEx** — the tissue expression resource used for the ncORF RNA-expression comparisons (Fig. 3d; Data availability).
- **HLA Ligand Atlas** — the benign reference of HLA-presented peptides used for the per-tissue comparison of ncORF-derived versus canonical HLA-I peptides (Fig. 3e; ref. 22).
