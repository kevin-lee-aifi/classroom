# Module 4 — Mass spectrometry as an evidence standard

| Field   | Value |
|---------|-------|
| **Time** | ~3 hrs — the largest single block in this curriculum |
| **Why it is the largest** | Every downstream module inherits this module's evidence standard. Modules 5 and 8 are unreadable if "MS `+`" and "MS `++`" are black boxes. |
| **Paper sections** | Abstract · "A microprotein annotation workflow" · "Microproteins in digest MS/MS datasets" · Discussion · agenda questions 1–3 |
| **Methods subsections** | *PeptideAtlas database construction and searching* · *Protein identifications and categories* · *Manual inspection of ORF MS spectra* · *Procedure for manually validating PSMs* · *ncORF expression in enriched ubiquitination datasets* · *Multiplexed PRM MS of ncORF targets* · *Use of the tier classification system* |
| **Figures to open in your own copy** | Fig. 1b · Fig. 2a–d · Extended Data Fig. 1a–d · Extended Data Fig. 2a–g · Extended Data Fig. 3 · Extended Data Fig. 8a |
| **Depends on** | [Module 3](03-riboseq-bridge.md) — what a Ribo-seq ORF call is and is not |
| **Feeds** | [Module 5](05-immunopeptidomics.md) · [Module 8](08-tier-framework-synthesis.md) |

## Before you read — three commitments

Write these down now, with numbers. The point is to be wrong first.

- [ ] The non-HLA build reports a peptide-level false discovery rate of `0.0009%`. Of the 183 ncORFs that passed those automated thresholds, what fraction do you expect survived expert manual inspection of the spectra? Commit to a percentage.
- [ ] Take the set of small human proteins that nobody doubts — curated, annotated, real. Of those under 50 amino acids, what fraction do you expect meets the HUPO-HPP two-peptide verification standard? Commit to a percentage.
- [ ] Conventional tryptic proteomics found peptides for 2.5% of the 7,264 ncORFs, against 76.7% of canonical proteins. Is that gap mostly a **depth** problem (not enough spectra yet) or mostly a **chemistry** problem (the assay cannot see these molecules at any depth)? Commit to one, in one sentence, before reading on.

Keep the sheet. You will grade it at the end.

## Part 1 — One molecule, end to end (~40 min)

Follow a single polypeptide from a frozen cell pellet to a line in a supplementary table. The paper's own PRM sample prep (Methods, *Multiplexed PRM MS of ncORF targets*) gives us real reagents and real numbers for every step, so this is not a cartoon.

One note on provenance before you start. Every **parameter, reagent and number** in this Part is anchored to a Methods subsection. The **mechanistic explanations between them** — why a chaotrope denatures, why amide bonds break preferentially under collision, how charge state is read off isotope spacing — are standard bottom-up proteomics and are not stated in this paper. Treat the mechanism as textbook background, `unverified` against this source, and the anchored parameters as the paper's own.

### Lysis

A frozen pellet of HeLa S3, HEK 293 or K562 is lysed in 8 M guanidine hydrochloride with Tris-HCl at pH 8.5, held at 75 °C for 10 min, and homogenised with ceramic beads (Methods, *PRM sample preparation*, protocol 1). Guanidine at 8 M is a chaotrope: it denatures everything at once, which both solubilises the proteome and instantly kills the proteases that would otherwise chew it up. Protein is quantified by BCA and 100 µg is taken forward.

Note what has already been destroyed: all structure, all complexes, all subcellular localisation. Bottom-up proteomics begins by throwing away every level of organisation above primary sequence. That is the trade — you get sequence-level identification of thousands of proteins at once, and you get it from a homogenate.

The paper's protocol 2 is worth a moment, because it is a different attack on this module's whole problem. A second pellet is precipitated to 76% acetonitrile / 0.1% TFA / 50 mM NaCl, spun, and the **supernatant** is kept (Methods, *PRM sample preparation*, protocol 2). Large proteins crash out; small ones stay soluble. This is a biochemical enrichment for small proteins — a wet-lab answer to the microprotein detection problem, not a computational one. Hold that thought for Part 3.

### Reduction and alkylation

Reduce with 5 mM TCEP, 20 min at 37 °C. Alkylate with 15 mM iodoacetamide, 25 min at room temperature in the dark (Methods, *PRM sample preparation*).

TCEP breaks disulfide bonds to free thiols. Iodoacetamide then caps every cysteine with a carbamidomethyl group so the disulfides cannot re-form and cysteines do not scramble. This has a consequence you will meet again in five minutes: it adds a fixed mass increment to every Cys (`+57.02 Da`, `unverified` — the value is standard but is not stated in this paper). The search engine must be told, or it will get the mass of every cysteine-containing peptide wrong. The builds set it as a fixed modification, "typically carbamidomethylated cysteine" (Methods, *PeptideAtlas database construction and searching*). Iodoacetamide is light-sensitive, which is why the step is done in the dark.

There is a subtle self-consistency requirement here that the paper handles explicitly: when they synthesised authentic peptide standards, cysteines were "incorporated as carboxyamidomethylated cysteine building blocks" (Methods, *Synthetic heavy-isotope-labelled peptide standards*) — so the standard carries the same chemical scar the endogenous peptide acquired in the tube.

### Digestion

Dilute the guanidine to ≤0.5 M (trypsin does not work in 8 M chaotrope), add Trypsin-Gold, and incubate 16 h at 37 °C with shaking. Quench with 5% formic acid. Desalt by C18 solid-phase extraction and dry (Methods, *PRM sample preparation*).

**Trypsin cleaves the peptide backbone C-terminal to lysine and arginine.** That single sentence is the most consequential fact in this module, and Part 3 is built on it. `96.3%` of the experiments in the non-HLA build were digested with trypsin (main text, "Microproteins in digest MS/MS datasets", citing Supplementary Table 1). The convention that trypsin is inhibited by a following proline is standard lore but is not stated in this paper — treat it as `unverified` here.

Three search-side terms follow from digestion chemistry, and you need them precise:

- **Fully tryptic** — both termini of the identified peptide sit at a K/R cleavage site (or a protein terminus).
- **Semi-tryptic** (the paper's setting: "semi-enzymatic settings (typically semi-tryptic)", Methods) — only one terminus must satisfy the rule. This admits peptides whose other end was made by something else: a protein's own N or C terminus, in-cell proteolysis, or non-specific cleavage during prep.
- **No-enzyme** — no terminal constraint at all. "All datasets were searched in no-enzyme mode" is what the HLA build did (Methods, *PeptideAtlas database construction and searching*), because HLA ligands are not the products of a protease digest at all. The processing biology behind that is [Module 5](05-immunopeptidomics.md)'s territory; here, just note that the enzyme rule is a *search parameter*, and that dropping it is the single biggest change between the two builds.

Semi-tryptic search is a deliberate concession toward hard-to-see proteins. It also enlarges the candidate space, which costs something. Part 3, idea 2.

### LC separation

Peptides are loaded onto a 15 cm × 75 µm inner-diameter, 1.7 µm C18 column and eluted at 250 nl min⁻¹ on an acetonitrile gradient — 2% → 35% organic over 90 min, then steps to 45% and 80% (Methods, *PRM MS data collection and analysis*, ZenoTOF conditions).

Reverse-phase C18 separates by hydrophobicity. The output is a **retention time** per peptide: a reproducible coordinate that is orthogonal to mass. It matters for two reasons. First, it spreads a mixture of hundreds of thousands of peptides out in time so the mass spectrometer only sees a few hundred at once. Second, retention time is independent evidence — a peptide that is what you claim it is must elute where that sequence elutes. The paper spikes indexed retention-time (iRT) standard peptides into every sample to put retention time on a transferable scale (Methods, *PRM sample preparation*).

Eluting peptides are ionised by electrospray at the column tip (2,300 V nanospray on the ZenoTOF). Peptides arrive as multiply protonated ions, most commonly 2+ or 3+.

### MS1 survey

The instrument records a full survey scan — the ZenoTOF ran TOF-MS over *m/z* 200–2,000 with a 200 ms accumulation time (Methods, *PRM MS data collection and analysis*, ZenoTOF conditions). This is a snapshot of every ion currently entering the instrument, plotted as mass-to-charge ratio against intensity.

An MS1 peak gives you three things and only three things: an *m/z*, an intensity, and — from the spacing of its isotope peaks — a charge state. From *m/z* and charge you compute a **precursor mass**. You do not get a sequence. Many different peptides share a precursor mass to within instrument tolerance. This is why bottom-up proteomics needs a second stage.

### Precursor isolation

The quadrupole selects one narrow *m/z* window and discards everything else. The paper's Orbitrap Astral PRM runs used a 2 Th isolation width; the ZenoTOF used Q1 at unit resolution, 0.7 ± 0.1 Da (Methods, *PRM MS data collection and analysis*).

Two things are worth internalising. First, the window is a window, not a point: co-eluting peptides within ~1–2 Th are co-isolated, producing **chimeric** spectra containing fragments from more than one peptide. Second, this is the step where the **acquisition strategy** lives. In data-dependent acquisition (DDA) — which is what the vast majority of the paper's 3.5 billion spectra are, and which the Discussion names as a limitation — the instrument looks at the MS1 scan and *decides on the fly* which precursors to fragment, typically the most intense ones not recently sampled. In PRM, you supply a list in advance. The Discussion notes that data-independent acquisition, especially with targeted PRM validation, "may provide increased sensitivity to detect ncORF-derived proteins in specific contexts" (Discussion).

DDA's on-the-fly choice is a soft bias against low-abundance species that compounds every other bias in this module. A microprotein present at low copy number in a lysate dominated by ribosomal proteins and tubulin may simply never be selected.

### HCD fragmentation

The isolated precursors are accelerated into a collision cell containing an inert gas. Higher-energy collisional dissociation (HCD) deposits vibrational energy that breaks the weakest bonds — which, for a protonated peptide, are the backbone amide bonds. The paper's Orbitrap PRM runs used 28% collision energy (Methods, *PRM MS data collection and analysis*).

Amide-bond cleavage produces two complementary fragments. Which one you observe depends on which one retains the charge:

- **b ion** — charge retained on the N-terminal fragment.
- **y ion** — charge retained on the C-terminal fragment.

For a peptide of *n* residues there are *n* − 1 backbone amide bonds, so up to *n* − 1 b ions and *n* − 1 y ions. Both are numbered from their own terminus: `b2` is the first two residues from the N terminus, `y3` the last three from the C terminus.

The whole method turns on one arithmetic fact: **consecutive ions in a series differ by exactly one residue mass.** `y4 − y3` is the mass of one specific amino acid. A complete y-ion series therefore spells the sequence backwards, one residue at a time, as a ladder of mass differences. That, and not any single peak, is what a "good spectrum" means.

Three consequences you will see the paper act on directly:

- Tryptic peptides end in K or R. Both are basic and hold the proton at the C-terminal end, so tryptic spectra are **y-ion dominated**. The paper's validation criteria expect "a nearly complete y ion series and a b ion series that begins at b2 and at least meets the y ion series" (Methods, *Procedure for manually validating PSMs*, criterion i).
- If a basic residue sits at the N terminus instead, you swap the roles: the paper says exactly that — "swap y ion for b ion when there is a basic residue instead on the N terminus" (criterion i). And HLA ligands, which often have neither terminus basic, "may therefore have strong b ions and internal fragmentation ions, rather than strong y ions" (Methods, *PeptideAtlas database construction and searching*). Module 5 depends on this.
- `b1` ions are essentially never visible — "unless there is an N-terminal mass modification" (criterion vi). Park that clause. It comes back in Part 4 and it is the hinge of the `c11riboseqorf4` story.

### What a spectrum actually is

Be very concrete, because this is where newcomers build the wrong mental model.

An MS2 spectrum is a **sparse list of (*m/z*, intensity) pairs** — typically tens to a few hundred peaks — plus metadata: precursor *m/z*, precursor charge, retention time, and the run it came from. That is all. It is not a picture, it is not a sequence, and it contains no per-residue identity of any kind until a candidate sequence is proposed against it.

This is the analogy you will reach for, so let us state it and then break it:

> **Analogy.** An MS2 spectrum is like a sequencing read: one measurement of one molecule, recorded in one narrow time window, out of billions.

> **Where it breaks.** A read carries base identity and a per-position quality score; you know *what* it says before you know *where* it goes. A spectrum carries no residue identity at all — the "sequence" is an inference from consistency with a hypothesis, and the same peak list can be consistent with more than one hypothesis. There is no spectral equivalent of alignment-free counting. *De novo* spectral sequencing exists but is far weaker than database search and is not what this paper used.

One number reframes the whole scale of the build. The non-HLA build acquired **3.5 billion MS/MS spectra** and accepted **573 million PSMs** (Fig. 1b) — so roughly 84% of acquired spectra never received an accepted identification at all (my arithmetic on the paper's figures). The HLA build is similar: 28 million PSMs from 240 million spectra, ~88% unassigned. Unassigned spectra are chimeric, or too poor to score, or carry a modification the search did not model, or are non-peptide contaminants — or their peptide **was not in the search database**. That last bucket is where the ncORF peptides sat before anyone put the 7,264 sequences into the database. Remember that when you get to idea 2.

### Database search: what a search engine actually does

For each spectrum, in order:

1. Take the precursor mass (from *m/z* and charge).
2. Enumerate every peptide in the search database whose theoretical mass falls inside the precursor mass tolerance **and** whose termini satisfy the enzyme rule (fully tryptic / semi-tryptic / no-enzyme), expanded by the allowed variable modifications and missed cleavages. This is the **candidate set**.
3. For each candidate, compute its theoretical b/y ion masses.
4. Score the observed peak list against each theoretical list — how many predicted fragments are present, at what intensity, with what mass error.
5. Report the best-scoring candidate, its score, and how far ahead it is of the runner-up.

Four properties of that procedure carry the whole module:

- The output is the **best member of the candidate set**, always. There is no "none of the above" option. A spectrum from a peptide absent from the database still gets an answer; that answer is just wrong.
- Scoring is **competitive**. What counts as a good score depends on what else was in the mass window. Enlarge the database and you change the score distribution for every spectrum, not only for the added sequences.
- The raw score is not a probability. Turning it into one is a separate statistical step — the next section.
- The failure mode is frequently a **near miss**: the true peptidoform differs from the reported one by a residue or a modification. The paper has a manual category for precisely this, `close but false positive`, defined as a PSM with many matching ions that is "likely to be almost the correct peptidoform" (Methods, *Manual inspection of ORF MS spectra*). If you understand why that category has to exist, you understand database search.

### The PSM

A **peptide-spectrum match** is the unit of evidence: one spectrum, one proposed peptidoform (sequence plus modifications plus charge), one score. Everything above it is aggregation. Peptide-level evidence aggregates PSMs for the same sequence. Protein-level evidence aggregates peptides mapped onto a protein. Each aggregation step needs its own error model, and each one is a place where a claim can be inflated.

## Part 2 — The paper's stack, stage by stage (~15 min)

All from Methods, *PeptideAtlas database construction and searching*, plus *ncORF expression in enriched ubiquitination datasets*.

| Stage | Tool, version | What it contributes |
|---------|-------|-------|
| Search database | THISP level 4, `2023-02` (non-HLA) and `2023-07` (HLA), [peptideatlas.org/thisp](https://peptideatlas.org/thisp/) | The candidate space. Includes the 7,264 Ribo-seq ORFs plus other contributed sequences that might be translated; the HLA database also carries 299 common contaminants. |
| Search engine | `MSFragger` v3.7 | Both builds. Enumerates candidates and scores spectra. Non-HLA searched semi-enzymatic (typically semi-tryptic); HLA searched no-enzyme. |
| Second search engine | `Comet` v2024 | Not used for the builds. Used (a) as the comparator in Extended Data Fig. 2a,b and (b) for the independent re-analysis of 11 ubiquitination-enriched datasets. |
| PSM probability | `PeptideProphet` (TPP v7.0) | Converts search scores into posterior probabilities. The mechanism — an empirical mixture model of the correct and incorrect score distributions — is from the tool's own paper (ref. 55, Keller et al., *Anal. Chem.* 74, 5383–5392, 2002), not from this one. |
| Cross-run / cross-engine integration | `iProphet` (TPP v7.0) | Refines peptide-level probabilities and error estimates. Cross-engine combination is visible in Extended Data Fig. 2a,b; the wider multi-level integration (across runs, charge states, modifications) is from ref. 56, Shteynberg et al., *Mol. Cell. Proteom.* 10, M111.007690, 2011. |
| Modification localisation | `PTMProphet` (TPP v7.0) | Decides *which residue* carries a mass modification, not merely that one is present. |
| Peptide → protein mapping | `ProteoMapper` (TPP v7.0) | Maps accepted peptides onto the 20,389-entry neXtProt core proteome and isoforms, accounting for known single-amino-acid variants. This is where "uniquely mapping" is decided. |
| Peptide → genome mapping | Ensembl toolkit | Places peptides on genome coordinates. |
| Reported error metrics | Supplementary Tables 15 (non-HLA) and 16 (HLA) | FDR at PSM, peptide and protein level — **and separately for subsets**, including the neXtProt core proteome, the 7,264 Ribo-seq ncORFs, and all `CONTRIB` sequences. |

Two things to notice about that table.

The probability you eventually threshold on is a **posterior error probability** from PeptideProphet/iProphet, not a raw MSFragger score. That is why Extended Data Fig. 2c,d are drawn against "posterior error probability thresholds lower than the PeptideAtlas build release threshold" — the axis is a calibrated probability.

And adding a second search engine bought almost nothing. Extended Data Fig. 2a,b compare `Comet`+TPP, `MSFragger`+TPP and the iProphet-combined result on evaluation dataset `PXD010154`, for total peptides and for ncORF peptides; the legend's own verdict is that combining search engines "provides only a marginal improvement", and the main text adds that it came "at a considerable increase in computational expense". If you were hoping the 2.5% figure is a software artefact that a better engine would fix — that experiment was run, and the answer is no.

MSFragger's speed comes from indexing fragment ions rather than generating a theoretical spectrum per candidate; that mechanism is not described in this paper (it cites Kong et al., *Nat. Methods* 14, 513–520, 2017), so treat it as `unverified` here.

## Part 3 — The four ideas that matter (~80 min)

### Idea 1 — Trypsin is hostile to microproteins, and this is chemistry, not depth

Trypsin cuts after K and R. Whether a given ORF yields *any* usable peptide is therefore a property of where lysines and arginines happen to fall in its sequence — a fact fixed before the experiment starts.

For a long protein this hardly matters. A 500-residue protein contains dozens of K/R positions; the law of averages guarantees a spread of fragment lengths, several of them in the 8–25 residue window where peptides ionise well, fragment informatively and map uniquely. For a 30-residue ORF there may be one K/R, or none, or three in a row. The possible outcomes include:

- zero peptides in a usable length range;
- one usable peptide (which caps the ORF at the paper's tier 2A — see idea 4);
- peptides that exist but map to more than one sequence, so they are not *uniquely* mapping and carry no protein-level information;
- peptides too hydrophilic or too hydrophobic to survive the C18 gradient at all.

These are **hard zeros produced by chemistry**. No amount of additional sequencing depth converts a hard zero into a detection, which is why "search more data" is the wrong instinct here. The paper makes this quantitative from three directions.

**The saturation curve (Extended Data Fig. 1a–d).** Read all four panels in your own copy. The non-HLA build has accumulated over 2.8 million distinct peptides across 573 million PSMs and 1,172 experiments; the cumulative canonical-protein count in that build is 16,888 (Extended Data Fig. 1c). But the legend's own summary is the sentence that matters: over the last 100 million PSMs, the build gains roughly **~2,000 new peptides per million PSMs and ~1 newly identified protein per million PSMs**. The main text calls this "near saturation in the power to identify canonical human proteins". Peptide discovery is still moving; protein discovery has flatlined.

That is the answer to your third commitment. The depth experiment has already been run at the scale of the entire public record, and its marginal yield in *new proteins* is approximately one per million spectral matches. If microproteins were merely rare, this curve would still be climbing for them. Note that 16,888 sits on a different denominator from Fig. 3a's 15,581 of 20,326 detected canonical proteins; the two counts are not directly comparable and I did not reconcile them, so use Extended Data Fig. 1 for the *shape* of the curve, not as a headcount.

**The length distribution (agenda question 1).** `28.3%` — 2,059 of 7,264 — of the ncORFs in this study are **under 25 amino acids**, and the paper states outright that many are smaller than 18 amino acids. Put that against the verification standard in idea 4 and the arithmetic closes: a 24-residue ORF asked to yield two non-overlapping ≥9-aa peptides covering ≥18 residues must have K/R positioned at almost exactly the two boundaries required. The probability of that is not small because the assay is insensitive. It is small because the sequence is short.

**The calibration on proteins we already believe (main text, "Microproteins in digest MS/MS datasets").** This is the sharpest number in the module. Take a manually curated set of small GENCODE proteins — real, annotated, uncontroversial (Whited et al., *Biophys. Rep.* 4, 100167, 2024, the paper's ref. 17). Of the known proteins under 50 amino acids, **only 2 of 36 (5.6%) satisfy benchmarks for HUPO-HPP verification.**

Sit with that. The standard rejects roughly 94% of small proteins whose existence is not in question. Whatever "fails HUPO-HPP verification" means, it cannot mean "probably not a protein" in this size regime. Compare your second commitment.

**And the control that proves the protease is the constraint.** In a single dataset — Wang et al., *Mol. Syst. Biol.* 15, MSB188503 (2019), i.e. `PXD010154`, the paper's ref. 18 — adding alternative proteases increased both the number of microprotein identifications and their sequence coverage (main text; Extended Data Fig. 2g). The legend goes further: in that dataset the non-trypsin digests "contribute a majority of ncORF PSMs". Same study, same tissues, same search pipeline; change only the enzyme, and the ncORF yield moves. The main text is careful to add that "the overall numbers were small", so this is a demonstration of mechanism rather than a solution at scale — but as a demonstration it is decisive.

Read Extended Data Fig. 2g and Extended Data Fig. 1a–d back to back. Together they say: more spectra, no; different chemistry, yes.

### Idea 2 — Search-database dependence, and why it is not the GTF problem

A peptide whose sequence is absent from the search database cannot be identified. Not "is identified with low confidence" — cannot be identified at all, because step 2 of the search never enumerates it as a candidate. The spectrum is still acquired, still scored, and still assigned to the best *available* candidate, or discarded as unassigned.

So the 7,264 ncORFs had to be **inserted into the database before anyone could detect them**. The paper states this plainly: the search database was THISP level 4, "which included the 7,264 Ribo-seq ORFs from ref. 4 as well as other contributed sequences that might be translated" (Methods, *PeptideAtlas database construction and searching*). THISP is a tiered set of human search databases whose higher tiers add progressively more speculative sequence (Deutsch et al., *J. Proteome Res.* 15, 4091–4100, 2016; [peptideatlas.org/thisp](https://peptideatlas.org/thisp/)) — the exact composition of level 4 is not given in this paper, so do not assert it.

This is the one idea in the module that maps directly onto something you do weekly.

> **Analogy.** A sequence missing from the search database gets zero PSMs, exactly as a gene missing from the GTF gets zero counts. In both cases the molecule was in the tube and the instrument recorded it; the reference simply had no slot to put it in. Cell Ranger will happily report a beautiful count matrix in which a real, expressed gene has a hard zero in every cell, and the fault is entirely upstream of the data.

> **Where it breaks — and this is the load-bearing part of this module.** Two asymmetries.
>
> **Cost.** Re-mapping FASTQs against an edited GTF is a routine job: you own the reads, and one machine and some hours gets you a new matrix. Re-searching **3.5 billion MS/MS spectra** across 295 ProteomeXchange datasets and 1,172 experiments, each needing search parameters "appropriate for each dataset, depending on alkylation, labelling, fragmentation type, instrument, enrichment strategy and more" (Methods), is a multi-year, multi-institution consortium effort. This paper was received in September 2024 and published in May 2026, on builds snapshotted at `2023-06` and `2023-11`. You cannot casually re-run it, and neither can anyone else. That is why the community needs a governed reference build at all.
>
> **Statistical cost.** Adding a gene to a GTF does not make any other gene's counts less trustworthy. Reads either align to the new feature or they don't; the only interference is local multimapping. **Enlarging an MS search database is not free in this way.** More candidate sequences in every precursor mass window means more chances for a high-scoring random match, and because scoring is competitive and target–decoy calibration is a property of the whole database, the score distribution shifts for *every* spectrum. You pay for a larger hypothesis space in statistical power, everywhere, including on the canonical proteome you were not even asking about.

The paper demonstrates the direction of that cost empirically. Extended Data Fig. 2c,d plot ncORF PSMs and decoy PSMs against posterior error probability thresholds below the build release threshold, in absolute count and in percent increase. The legends' verdict: "the number of decoy PSM increases faster than ncORF PSMs with decreased threshold." The main text renders it as: "using more permissive FDR thresholds preferentially increased false positives."

Read that carefully, because it says something stronger than "loosening a threshold adds false positives" — everyone knows that. It says that in the region of score space just below the release threshold, the *marginal* spectrum assigned to an ncORF is more likely to be a decoy hit than a real ncORF peptide. The ncORF subset lives in the part of the distribution where the signal-to-noise has already inverted. That is the bridge to idea 3.

Two corollaries worth writing down:

- The same logic applies to **enzyme specificity**. Semi-tryptic search (non-HLA) has a much larger candidate space than fully tryptic; no-enzyme search (HLA) is larger again. The two builds' reported peptide-level FDRs differ by ~4.5× — `0.0009%` for non-HLA versus `0.0041%` for HLA (main text) — despite the HLA build having 15-fold fewer spectra. The search space is a plausible driver of that difference, but the paper does not make that causal claim; treat the attribution as my inference.
- The same logic applies to **modifications**. `protein N-terminal acetylation` was in the builds' variable-modification list (Methods). Had it not been, the acetylated `c11riboseqorf4` peptide in Part 4 would have been invisible for the same reason a missing sequence is invisible. A modification absent from the search space is as undetectable as a sequence absent from the database.

### Idea 3 — Target–decoy FDR and the base-rate trap

This is the confrontation the module is built around. Get the mechanics first, then the numbers, then the reconciliation.

**Target–decoy estimation.** Add decoy sequences — sequences you know are not real — to the database. Search normally. Every spectrum that gets assigned to a decoy above threshold is a demonstrated error. If decoys and targets are equally likely to attract a wrong assignment, then the count of accepted decoy hits estimates the count of accepted *wrong target* hits, at a 1:1 ratio. Divide by the number of accepted target hits and you have an FDR. The canonical reference is Elias & Gygi, *Nat. Methods* 4, 207–214 (2007) — the paper's ref. 61.

**The paper's entrapment variant** (Methods, *PeptideAtlas database construction and searching*): decoys are generated by **scrambling each target protein's sequence**, added at a 1:1 ratio, and — the entrapment part — the pipeline "is not given knowledge of the decoys" (Methods; the method reference is Feng et al., *BMC Genom.* 18, 143, 2017, ref. 62). Scrambling preserves amino-acid composition and therefore preserves the precursor-mass distribution and the fragment-mass landscape, which is what you want from a null. Withholding decoy identity from the pipeline means the post-processing statistics cannot inadvertently learn to treat decoys differently — a real risk when a probability model is fitted per run.

**Both directions in which it is imperfect**, in the paper's own words (same Methods subsection):

- Decoys under-count target errors: "the similarity of some real protein sequences to one another may cause a small bias toward making errors to target sequences." Real proteomes contain paralogues, repeats and low-complexity stretches. A scrambled sequence has no siblings; a real one does. So a wrong assignment is easier to make onto a target than onto a decoy, and the decoy count is an underestimate.
- Decoys over-count errors: "scrambled sequences may yield an observable sequence (not already in the target database) occasionally by pure chance." A scramble can accidentally spell a peptide that genuinely exists in the sample. Counted as a decoy hit, it is really a true detection of something the database did not list.

The Methods conclude that despite these imperfections the technique is "widely regarded as sufficiently accurate and is the standard in the community". Note what that judgement is about: the **population**. Hold onto that word — the next few paragraphs are entirely about it.

**Now the numbers.** From the main text ("A microprotein annotation workflow" and "Microproteins in digest MS/MS datasets"):

| Quantity | Value | Anchor |
|---------|-------|-------|
| Decoy-estimated protein-level FDR | `<0.1%` | main text |
| Peptide-level FDR, non-HLA build | `0.0009%` | main text |
| Peptide-level FDR, HLA build | `0.0041%` | main text |
| ncORF peptides passing thresholds (non-HLA) | 484 | Fig. 2a |
| ncORFs with ≥1 such peptide | 183 of 7,264 (~2.5%) | Fig. 2b |
| ncORFs with 2 unique peptides — validated / total | 30 of 42 | main text; Fig. 2c |
| ncORFs with 1 peptide — validated / total | 36 of 141 | main text; Fig. 2c |
| ncORFs passing inspection, total | 66 | Fig. 2d |

Everything reconciles, which is worth verifying yourself rather than taking on trust. 42 + 141 = 183. 30 + 12 rejected = 42. 36 + 105 rejected = 141. And Fig. 2d, which bins the survivors by number of distinct peptides, gives 36 + 10 + 8 + 7 + 5 = 66 = 30 + 36. Read Fig. 2c and Fig. 2d together in your own copy and check the sum; the figure is coordinate-verified but you should not need to trust me.

So: **a build reporting a `0.0009%` peptide-level FDR, on manual inspection, rejected 117 of 183 ncORFs (63.9%) — including 105 of 141 (74.5%) of those supported by a single peptide.** Survivors: 66 of 7,264, which is `0.91%`. Compare your first commitment.

One precision before the reconciliation, because the learner who does not make this distinction will overclaim. **"Rejected on inspection" is not the same as "false".** The five manual categories are `excellent`, `good`, `false positive`, `close but false positive` and `low information` (Methods, *Manual inspection of ORF MS spectra*) — and only two of those five assert that the identification is wrong. `good` and `low information` assert that the evidence is *insufficient for annotation purposes*, which is a different claim. So 63.9% is a **failure-to-meet-the-annotation-bar rate**, and it is an upper bound on the ncORF-subset false discovery rate, not an estimate of it. The paper's own subset FDR figures (Supplementary Tables 15 and 16) are the actual estimate, and they are what you should look up.

With that said, the two numbers still sit uncomfortably far apart, and they are not in contradiction. Understanding why is the point of this module.

**The reconciliation.** An FDR is a property of a **population**, and it says almost nothing about a low-prior subset inside that population.

Do the arithmetic. The non-HLA build contains over 2.8 million distinct peptides (Extended Data Fig. 1a), the overwhelming majority of them mapping to canonical proteins. A `0.0009%` peptide-level FDR corresponds to roughly 25 false peptides in the whole build. The ncORF peptides number 484 — about `0.017%` of the build's distinct peptides. If false identifications were distributed uniformly across the peptide space, you would expect *well under one* of those ~25 errors to land among the ncORFs. (My arithmetic on the paper's figures, not a paper claim.)

But false identifications are emphatically **not** uniformly distributed. They concentrate exactly where the prior is low and the score is marginal — and the paper says so, in the sentence that opens its manual-inspection Methods: false positives "are most easily found mapping to proteins that are unlikely to be detected" (Methods, *Manual inspection of ORF MS spectra*).

That is the base-rate trap stated compactly. The global FDR is dominated by the enormous, high-prior canonical population, whose peptides are corroborated many times over across 1,172 experiments. The ncORF subset is a tiny, low-prior island inside that population. Errors that are negligible as a fraction of 2.8 million peptides can be a large fraction of a 484-peptide subset. A global peptide-level FDR of `0.0009%` and a subset error rate orders of magnitude higher are perfectly compatible — nothing in the arithmetic forbids it, and the manual-inspection outcome is consistent with it.

Which is exactly why the authors do two things that would otherwise look like paranoia:

1. **They report FDR separately for the ncORF subset.** Supplementary Tables 15 and 16 give FDR metrics at PSM, peptide and protein level "as well as for certain subsets of proteins, including the neXtProt core proteome, the 7,264 Ribo-seq ncORFs, as well as all CONTRIB sequences" (Methods). This is class-specific FDR, and it is the statistically correct move. **I could not read Supplementary Tables 15 and 16, so I do not have the ncORF-subset FDR values — look them up when you have the supplement, and record them in the progress table below.** They are the single most informative numbers in this module.
2. **They hand-inspect every spectrum anyway.** All 183 ncORFs in the non-HLA build were manually inspected (main text). In the HLA build, 859 HLA-I spectra and 691 matching Ribo-seq profiles (main text). Part 4 covers what that inspection consists of.

For context, the paper positions its own thresholds as "more conservative than many studies" and cites the field's benchmarking exercise — Wacholder et al., *Nat. Commun.* 17, 1241 (2026), ref. 16 — as the comparison. The general problem of class-specific versus global FDR is not new: see Sennels, Bukowski-Wills & Rappsilber, [*BMC Bioinformatics* 10, 179 (2009)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-10-179) on local and peptide-class-specific error rates, and the paper's own ref. 25 (Prensner et al., *Mol. Cell. Proteom.* 22, 100631, 2023) which reviews it specifically for the noncanonical proteome.

**Now the analogy you will actually feel.**

> **Analogy.** A gene with eleven total UMIs across your whole experiment, carrying a BH-adjusted *p* of 0.03 in a pseudobulk contrast. You do not believe it. You have never believed it. Your disbelief is not about the arithmetic — the arithmetic is right — it is about the prior: at that count depth, the estimate is dominated by whatever produced those eleven molecules, and that is as likely to be ambient RNA, index hopping or one weird cell as a real effect. The FDR is a property of the 14,000 genes you tested, not of this gene.

> **Where it breaks. Three places, and they all matter.**
>
> **1. Benjamini–Hochberg conditions on the tested set, and you choose that set.** Your adjusted *p* is a statement about the family of hypotheses you actually tested. And you *curate that family before testing*: edgeR's `filterByExpr` removes low-count genes from the family entirely, and you set the threshold. The eleven-UMI gene usually never enters the test. **The MS analogue has no such filter.** You cannot decline to search the short ORFs — finding out whether they are there is the entire experiment. The candidate set is fixed by the database, and the low-information stratum is the stratum you care about. There is no `filterByExpr` for a 24-residue ORF.
>
> **2. There is no reliable pre-test summary statistic.** `filterByExpr` works because total count is a good proxy for testability. The nearest MS analogue is peptide count per ORF, and it does carry real information — 74.5% of single-peptide ncORFs were rejected versus 28.6% of two-peptide ncORFs — but it is nowhere near sufficient: 12 of 42 two-peptide ncORFs still failed inspection. Peptide count is a weak filter, not a clean one.
>
> **3. The error mode is different in kind.** Your eleven UMIs are still real observations *of that gene*; the problem is that the effect size is not estimable. A false PSM is not a weak observation of the ncORF — it is a confident observation of **a different molecule entirely**, misattributed. In scRNA-seq the low-count failure mode is **variance**. In low-prior MS it is **bias**. More data fixes variance; more data does not fix a misassignment, it reproduces it.

Because there is no `filterByExpr` and no clean statistic, the remedy the consortium actually used was **manual curation at scale**: expert spectral inspection of every candidate, with written criteria and a categorisation scheme. The Discussion is candid that this does not generalise — "manual inspection of thousands of candidates is not feasible for most researchers" — and points toward retention-time and ion-mobility prediction as the scalable substitute.

### Idea 4 — The HUPO-HPP standard as a statistical object

**The rule, stated precisely.** The paper gives it twice, in slightly different registers.

As the study's own filter (main text, "A microprotein annotation workflow"): a decoy-estimated FDR of `<0.1%` at the protein level, plus adherence to HUPO-HPP guidelines — "two distinct, uniquely mapping peptides of length 9 or more residues and a minimum protein coverage of 18 residues" (citing Deutsch et al., *J. Proteome Res.* 18, 4108–4116, 2019, the paper's ref. 15).

As PeptideAtlas's operational definition (Methods, *Protein identifications and categories*): proteins with 2 or more uniquely mapping **non-nested** peptides — non-nested meaning neither is contained completely within the other — of length 9 or more amino acids, together covering at least 18 amino acids, are categorised as `canonical`.

Four independent requirements, and you should be able to say what each one is for:

- **Two peptides.** A single PSM is a single measurement. In a search of 3.5 billion spectra, one chance high-scoring match is not a remote possibility — it is an expectation. Requiring two peptides makes the claim require two independent chance matches landing on the same sequence, which is roughly the square of a small number.
- **Non-nested.** Blocks the trivial cheat of counting a peptide and its own missed-cleavage extension as two independent observations. They come from the same cleavage neighbourhood and are not independent evidence.
- **≥9 amino acids.** Uniqueness. Short peptides map to many proteins and carry little protein-level information. The paper's own HLA peptide categorisation shows the same instinct from the other side: peptides of 7 amino acids are dumped into "other peptides", and canonical assignment requires mapping to at most 30 distinct entries (Methods, *Categorizing HLA peptides*).
- **≥18 amino acids covered.** Enforces the spirit of non-nestedness numerically, and demands that a non-trivial stretch of the actual sequence has been observed rather than one small window twice.

**And here is the thing to internalise: this is a governance convention, not a derived optimum.** The HPP guidelines themselves record that the "2 × 9" policy was retained deliberately after discussion, on the reasoning that a more intricate limit without a mathematical or statistical foundation was inadvisable, and that the existing policy was simple and clear ([HPP MS Data Interpretation Guidelines 3.0](https://www.biorxiv.org/content/10.1101/733576v2.full); *J. Proteome Res.* 18, 4108–4116, 2019 — retrieved via search snippet, so verify against the full text before quoting it yourself). The rule is chosen for clarity and conservatism in service of a low-false-positive reference proteome.

It is also contested on its own statistical terms, independent of microproteins. Gupta & Pevzner, ["False discovery rates of protein identifications: a strike against the two-peptide rule"](https://pubmed.ncbi.nlm.nih.gov/19627159/) (*J. Proteome Res.* 8, 4173–4181, 2009), argue that discarding single-peptide proteins removes more target than decoy proteins and therefore *raises* protein-level FDR relative to a properly error-controlled one-peptide rule. You do not have to agree. You do have to stop treating "meets HUPO-HPP criteria" as a synonym for "is a protein".

**The length-dependent power curve.** Now combine the rule with idea 1. The following is a construction from the paper's numbers, and I am labelling it as mine, not the paper's:

- An ORF must be **≥18 codons** even to be eligible. Below that, the achievable probability is exactly zero regardless of instrument, sample, depth or protease. The paper notes plainly that many ncORFs are smaller than 18 amino acids (agenda question 1).
- Between 18 and ~25 codons, the rule demands that two non-overlapping ≥9-aa peptides cover ≥18 of at most 24 residues — i.e. ≥75% of the ORF, in two pieces. That requires K/R at very nearly the two exact positions needed. `28.3%` (2,059 of 7,264) of these ncORFs are in that regime or below (agenda question 1).
- As length grows, the number of K/R positions grows and the chance of two usable, uniquely mapping fragments rises smoothly toward the near-certainty that canonical proteins enjoy: 15,581 of 20,326 canonical proteins detected, `76.7%` (Fig. 3a), against 183 of 7,264 ncORFs, `2.5%`.
- The curve is calibrated by the only clean control available: **2 of 36 (5.6%)** curated small GENCODE proteins under 50 amino acids meet HUPO-HPP benchmarks. Real proteins. 94% failure.

So the standard carries a power curve in ORF length, and the microprotein population sits almost entirely in its low-power tail. The standard is not wrong; it is **calibrated for a different molecule size** than the one it is now being asked to adjudicate.

Three consequences that Modules 5 and 8 will use directly:

- The HUPO-HPP rule *is* the boundary of the paper's tier 1A: "two non-nested peptides in MS proteome data, with or without HLA immunopeptidomics data, with Ribo-seq data" (Methods, *Use of the tier classification system*). One MS peptide instead of two puts you in tier 2A. So the standard is not an abstraction in Fig. 5 — it is the line between two rows of the table.
- `Candidate protein` in Fig. 5a/5d means, in part, "cleared this bar in normal cells, with evidence of function". That is what makes the label mean something, and it is why it is rare.
- Hence **agenda question 1**: "Are HUPO-HPP guidelines for protein verification suitable for ncORF-encoded microproteins?" The paper is not asking rhetorically. It is asking whether the reference-annotation community should rewrite a rule whose power curve excludes the class of molecule under discussion.

**The irony to carry forward.** The best-detected ncORF in the entire tryptic build, `c11riboseqorf4`, is a **171-amino-acid** uoORF in `PIDD1` (main text, "Annotation of protein-coding ncORFs"; Extended Data Fig. 8a) — far above any working microprotein size cutoff. It has 11 distinct peptides across 94 different experiments, 8 of them rated `excellent` (Extended Data Fig. 8a). It is convincing *because* it is long enough for trypsin to work on. The catalogue's most persuasive member is its least typical one, and that is a statement about the assay, not about biology.

## Part 4 — What survives, and what it took (~25 min)

### Manual PSM validation

The paper wrote its inspection criteria down, which is unusual and is the reason this module can teach them. Two Methods subsections do the work.

**The outcome categories** (Methods, *Manual inspection of ORF MS spectra*):

- `excellent` — highly compelling evidence that the identification is completely correct.
- `good` — the PSM is likely correct but lacks sufficient quality and residue coverage to be highly compelling.
- `false positive`.
- `close but false positive` — many matching ions, likely almost the correct peptidoform, but slight discrepancies indicate the truth is very close but not the listed sequence.
- `low information` — detected ions are compatible with the identification but coverage is too low to be compelling.

Two of the five categories are verdicts of *insufficiency* rather than of error — `good` and `low information` both say the identification is probably or possibly right but the evidence does not carry an annotation. And `close but false positive` is the diagnostic one: it exists because the characteristic failure of a database search is not a random peak list matched to a random sequence, but a **near neighbour** of the truth. That taxonomy only makes sense once you accept that a search engine returns the best available candidate rather than the truth.

**The criteria for `excellent`** (Methods, *Procedure for manually validating PSMs*; decision flowchart in Extended Data Fig. 2e). Ten numbered rules; the load-bearing ones, in plain terms:

- (i) The combined b and y series must give nearly complete coverage of the proposed peptidoform. For tryptic or tryptic-like peptides: a nearly complete y series, plus a b series starting at `b2` that at least meets the y series. Swap y for b if the basic residue is at the N terminus instead.
- (ii) Prominent peaks **beyond** the last matching ion disqualify the PSM — they imply the real sequence extends further with different residues.
- (iii) A gap in a series must not have a plausible unannotated candidate sitting in it with a mass defect between the flanking ions. That pattern means the truth is a near neighbour of the proposal.
- (iv)–(v) Gaps need a physical explanation, e.g. a y ion C-terminal to proline is expected to be weak; y ions N-terminal to proline should be unusually intense.
- (vi) Strong `b2` and the corresponding `a2` diketopiperazine ion are preferred in HCD spectra. `b1` is normally absent **unless there is an N-terminal mass modification**.
- (vii) Internal fragment ions must be considered when annotating, especially for peptides with no basic residue at either terminus — i.e. HLA ligands.
- (viii)–(x) Keep mass modifications to a minimum; no substantial ion-free region in long peptides; no prominent unannotated peaks suggesting contamination or misassignment.

Read this list once as a checklist, then read it again as a *description of the failure modes*. Almost every rule is aimed at one specific way a database search goes wrong: it lands on a sequence adjacent to the truth. Criterion (ii) catches truncation. Criterion (iii) catches a substituted residue. Criterion (viii) catches a modification invented to make the mass work. The care is proportionate to the base-rate problem in idea 3.

### Universal Spectrum Identifiers

The best peptide-spectrum match for each ncORF is listed in Supplementary Tables 2 and 6 as a **USI** — a Universal Spectrum Identifier — resolvable and viewable at [proteomecentral.proteomexchange.org/usi](https://proteomecentral.proteomexchange.org/usi/); where no USI is possible, a direct PeptideAtlas spectrum-viewer URL is given instead (Methods, *Manual inspection of ORF MS spectra*). The manual procedure's step 2 is literally: examine PSMs until at least one provides `excellent` evidence, and record its USI.

USIs are unavailable when a dataset has no ProteomeXchange accession — "most common in Clinical Proteomic Tumor Analysis Consortium (CPTAC) datasets, for which a PXD has not been assigned" (Methods). That gap is worth noticing: the parts of the evidence base that are hardest to point at are disproportionately the large clinical tumour cohorts.

A USI is a colon-separated multipart key: the `mzspec` prefix, a collection identifier (typically a PXD accession), the MS run name, an index type and index value, and an optional interpretation — e.g. the resolver's own worked example, `mzspec:PXD000680:0_min_M_a_QE_2:scan:20245:DEDLT[UNIMOD:21]QDYEEWKR/3` ([HUPO-PSI](https://www.psidev.info/usi); [resolver](https://proteomecentral.proteomexchange.org/usi/)). The specification was ratified by the Proteomics Standards Initiative in 2021.

> **Analogy.** A USI is to a PSM what a genomic coordinate plus CIGAR string is to a read alignment: a stable, resolvable address for one primary observation, so a reader can go and look at the actual measurement instead of taking a summary table on faith.

> **Where it breaks.** A USI addresses the **spectrum**. The peptidoform in the string is an *assertion about* that spectrum, not a property carried by it. Two people can resolve the same USI and disagree about the sequence — indeed, the paper's `close but false positive` category exists precisely for spectra where the assertion is nearly right. Nothing comparable is true of "this read aligned at chr7:5,527,151 with 90M": that is a fact about the alignment, and disagreement about it is a bug, not a judgement call.

### Synthetic peptides and PRM

Manual inspection judges a spectrum against theory. The next two layers judge it against an authentic molecule.

**Spectral matching against synthetic peptides.** The spectra of **29 of 30 PSMs** were validated by matching synthetic peptide spectra against the original spectra (main text; Supplementary Table 4). Same sequence, synthesised, fragmented on purpose — if the endogenous spectrum and the synthetic spectrum agree peak for peak, the *peptidoform assignment* is not a database artefact. Note the residual gap: this confirms which peptide the spectrum came from, not that the peptide can only have come from this ORF. Unique mapping is a separate check, done by `ProteoMapper` against the core proteome and its known variants.

**PRM against heavy isotope-labelled standards** (Extended Data Fig. 3; Supplementary Figs. 1 and 2; Methods, *Multiplexed PRM MS of ncORF targets*). This is the strongest single-peptide evidence in the paper, and the design is elegant:

- For each target ncORF peptide, an authentic analogue is chemically synthesised with **one heavy-isotope-labelled amino acid** per peptide, free amine at the N terminus and carboxylic acid at the C terminus, and cysteines pre-installed as carboxyamidomethylated building blocks so they match the iodoacetamide-treated endogenous peptide (Methods, *Synthetic heavy-isotope-labelled peptide standards*).
- The standard is spiked into the digest at a known amount — 10 fmol on the Orbitrap Astral, 6 fmol on the ZenoTOF 8600 — alongside iRT retention-time standards (Methods, *PRM sample preparation*).
- The instrument runs from a precursor list targeting **both** the endogenous and the heavy peptide. Analysis is in `Skyline` v25.1.0.142; data are deposited as `PXD066599`.

Because heavy and light differ only in isotopes, they are chemically identical: they co-elute at the same retention time and fragment into the same transitions, offset by a known mass. So a positive result is not "a score exceeded a threshold". It is "the endogenous species co-eluted with an authentic standard and produced the same fragment transitions in the same relative intensities". That is a hypothesis test against known truth, not a database inference.

**Read Extended Data Fig. 3 in your own copy.** The target is `ATPGHTGCLSPGCPDQPAR` from `c11riboseqorf4` (tier 1A), shown in HeLa S3, HEK 293 and K562. The endogenous peptide was detected in all three lysates, from **both** sample-preparation protocols P1 and P2 — the guanidine route and the acetonitrile small-protein-enrichment route. Data on a Sciex ZenoTOF 8600. The legend notes the peptide had already been seen in the PeptideAtlas non-HLA build, so this is orthogonal confirmation of an existing claim rather than a new discovery.

Two independent preparations, three cell lines, an authentic standard, and a targeted acquisition. That is what it costs to be certain about one peptide — and it is worth asking yourself how that cost scales to 7,264 ORFs.

### Multi-protease and PTM evidence

**Multi-protease** was covered in idea 1: Extended Data Fig. 2g, dataset `PXD010154`, where non-trypsin digests contribute a majority of ncORF PSMs, and where alternative proteases raised both identification count and coverage (main text). The Discussion generalises it: assessing synthetic peptide standards, PTMs or multi-protease digestions yields "unambiguous evidence for some ncORF-encoded microproteins that were not visible in routine tryptic MS studies".

**PTMs** enter in two ways. The builds themselves searched a standard set of variable modifications: methionine oxidation, protein N-terminal acetylation, peptide N-terminal pyro-glutamic acid from Glu or Gln, and Asn/Gln deamidation — plus cysteine cysteinylation in the HLA build (Methods, *PeptideAtlas database construction and searching*). Separately, 11 ubiquitination-enriched PRIDE datasets were **independently re-analysed** with `Comet` v2024: semitryptic, 4 missed cleavages, Gly–Gly ubiquitination remnant plus Met oxidation and N-terminal acetylation as variable modifications, reversed decoy for FDR, `PeptideProphet`/`iProphet`/`PTMProphet` from TPP v7.1.0, and false-localisation rates estimated by a decoy-amino-acid (alanine) approach (Methods, *ncORF expression in enriched ubiquitination datasets*). Extended Data Fig. 2f bins the resulting ncORFs by PSM count and colours them by whether they were already in the non-HLA or HLA build.

### The `c11riboseqorf4` N-terminal acetylation case — why processing beats detection

This is the most instructive single observation in the module. From Extended Data Fig. 8a:

`c11riboseqorf4` has 11 distinct peptides across 94 experiments, 8 rated `excellent`. Two are shown with nearly complete y-ion coverage and substantial b-ion coverage. And one of them, `SGLQGPSVGDGCNGGGAR`, **begins at position 2 of the ORF and carries peptide N-terminal acetylation** — which the legend reads as ORF N-terminal acetylation following removal of the initiator methionine.

Unpack why that is a different class of evidence from "we detected a peptide from this ORF":

- **It confirms the start codon.** "Position 2" is only a meaningful statement relative to a Met1. Initiator-methionine removal is interpretable *only* if the ORF's annotated start is where translation actually began. The observation therefore validates the ORF model, not just the presence of the sequence.
- **It confirms a nascent chain.** Initiator-Met excision and N-terminal acetylation are co-translational N-terminal maturation events acting on the emerging polypeptide. (The specific enzymology — methionine aminopeptidases and the NatA complex — is not in this paper; treat those names as `unverified` here.) So the molecule was not merely present. It went through the cell's protein-maturation machinery, as a nascent chain, at the ribosome.
- **It is much harder to fake.** A chance database match would have to land on this ORF *and* independently happen to carry a modification that is chemically consistent with position 2 of that same ORF. Two coincidences, not one.
- **And it closes a loop with the validation criteria.** Criterion (vi) says `b1` ions are normally invisible "unless there is an N-terminal mass modification". An N-terminally acetylated peptide is precisely the case where the spectrum can carry the extra low-mass ion that pins the N terminus directly. (That connection is my synthesis of two of the paper's own statements, not a claim the paper makes.)

The conceptual point, and it is the one to carry into Module 8: this is evidence of a **genuine, processed protein**, not merely of detection. Detection says a sequence was in the tube. Processing says the cell treated it as a protein — recognised its N terminus, trimmed it, and modified it. That is a step closer to the paper's central distinction between protein *identification* and protein-coding gene *annotation*, and it is one of the reasons `c11riboseqorf4` in `PIDD1` is one of the three ncORFs GENCODE annotated as protein-coding.

One caveat that is also idea 2 again: `protein N-terminal acetylation` was in the search's variable-modification list. Had it not been, this observation could not have existed.

## Part 5 — PeptideAtlas is a graded, governed reference, not a flat list (~10 min)

From Methods, *Protein identifications and categories*.

Peptides are mapped by `ProteoMapper` onto the **20,389 entries of the neXtProt core proteome** and their isoforms, accounting for all single-amino-acid variants encoded in neXtProt. Then each protein entry receives a category:

- `canonical` — meets the two-peptide criteria (≥2 uniquely mapping, non-nested, ≥9 aa, ≥18 aa covered).
- `non-core canonical` — meets the same two-peptide criteria, but with peptides that cannot be mapped to the core proteome.
- Nine further categories for ambiguous and redundant evidence, including `indistinguishable representative`, `indistinguishable`, `representative`, `marginally distinguished`, `subsumed`, `weak` and `insufficient evidence`.
- `identical` — sequence-identical to another entry.
- `not detected` — no peptide evidence whatsoever.

The full description is in the paper's ref. 65 (van Wijk et al., *Plant Cell* 33, 3421–3453, 2021 — the Arabidopsis PeptideAtlas paper, where the category system is laid out).

**And then the gatekeeping rule**, which is the part that changes how you read the paper: "For reasons of integration with the HPP annual metrics, only sequence entries that belong to the core set of around 20,389 neXtProt and UniProtKB/Swiss-Prot protein-coding genes can achieve `canonical` status" (Methods).

The 7,264 ncORFs are, by construction, not core-proteome entries. So **no ncORF could ever be `canonical` in PeptideAtlas, however good its spectra.** The best available category for an ncORF that clears the two-peptide bar is `non-core canonical`. The rule is administrative, adopted so that the HPP's annual proteome metrics remain comparable year to year — and it means that "not `canonical`" for a non-core entry is a statement about **membership**, not about evidence quality.

> **Analogy.** You already read a reference this way. A GTF is not a flat list of genes: `gene_type` distinguishes `protein_coding` from `lncRNA` from `processed_transcript`; the `basic` tag selects a subset of transcripts; `MANE_Select` marks one representative per gene; and Cell Ranger's reference build filters by biotype before you ever see a count. Which category a feature sits in determines what downstream tools will do with it.

> **Where it breaks.** GTF tags do not gate whether reads can be *counted* to a feature — you can always change the filter and recount, and the underlying alignment is unchanged. PeptideAtlas's core-set rule gates the **category itself**, and the category is what downstream consumers read: HPP annual metrics, neXtProt protein-existence levels, and — through this paper — the tier system in Fig. 5. The evidence and the label are decoupled in a way GTF biotypes are not.

This is the module's contribution to the curriculum's central pivot: an evidence standard is a *governed object* with a constituency, a release schedule and backward-compatibility obligations. It is not a measurement.

## The spine claim — carry this into Modules 5 and 8

State it in one breath, with the numbers:

**Conventional tryptic proteomics found peptides for 183 of 7,264 ncORFs — about 2.5%. After manual inspection, 66 survived: 0.91%. The abstract's "about 25%" is not this method's result. It is the HLA immunopeptidomics number: 3,116 peptides mapping to 1,785 of 7,264 ncORFs, 24.6%.**

Anchors: 484 peptides → 183 ncORFs (Fig. 2a,b; Supplementary Tables 2 and 3; main text, "Microproteins in digest MS/MS datasets"). 66 survivors (Fig. 2c,d, reconciled as 30 + 36 and as 36 + 10 + 8 + 7 + 5). 1,785 of 7,264 = 24.6% (Fig. 2e,f; main text, "Microproteins as HLA-I-presented peptides"). Canonical contrast 15,581 detected of 15,581 + 4,745 = 20,326 = 76.7% (Fig. 3a, coordinate-verified; the ncORF pair in the same panel is 1,867 + 5,397 = 7,264).

Three things follow, and Modules 5 and 8 will pick each of them up:

- The headline is carried almost entirely by immunopeptidomics — a window with completely different chemistry: no protease digest, a no-enzyme search, and ligands cut by the cell's own antigen-processing machinery rather than by an enzyme you added (the biology is [Module 5](05-immunopeptidomics.md)). **This is why the tier table keeps MS and HLA in separate columns.** They are not two depths of the same assay.
- The two windows barely overlap. Agenda question 2 gives the number from the annotation side: of the 1,785 ncORFs seen with HLA data, only **24** also have one peptide in tryptic MS data suitable for potential annotation.
- The MS-side funnel toward annotation is brutally narrow: after manual inspection of MS peptide data, 20 candidates for tier 1A, reduced by further scrutiny to 15, for reasons including pseudogenic sequences, a GRCh38 assembly error and insufficient Ribo-seq evidence (main text, "Annotation of protein-coding ncORFs"; Fig. 5b,c). Module 8 takes the funnel from there.

And the standard-setting consequence, which is agenda question 1 in one line: **the two-peptide standard was written for the method that reached 2.5%.**

## Figure-reading assignments

Do these in your own copy of the PDF. No images are reproduced here — the paper is CC BY-NC-ND.

- [ ] **Fig. 1b** — the two builds side by side. Note the words "Protease-specific sequence searching" versus "No-protease sequence searching". That phrase pair is the whole of Modules 4 and 5.
- [ ] **Extended Data Fig. 1a–d** — the saturation panels. Read the peptide panels (a, b) against the protein panels (c, d) and convince yourself the peptide curve is still rising while the protein curve is not.
- [ ] **Fig. 2a–d** — the non-HLA funnel. Check the arithmetic yourself: 42 + 141 = 183; 30 + 12 = 42; 36 + 105 = 141; and Fig. 2d's bars summing to 66.
- [ ] **Extended Data Fig. 2a,b** — search-engine comparison. How much did adding `Comet` buy?
- [ ] **Extended Data Fig. 2c,d** — the threshold panels. This is the base-rate trap drawn as a graph. Identify the point at which decoys are accumulating faster than ncORFs.
- [ ] **Extended Data Fig. 2e** — the manual-validation flowchart. Trace one path from "PSM" to `close but false positive`.
- [ ] **Extended Data Fig. 2g** — tryptic versus other-protease ncORF peptides in `PXD010154`.
- [ ] **Extended Data Fig. 3** — the PRM transitions. Look for co-elution of the endogenous and heavy traces, not for a big peak.
- [ ] **Extended Data Fig. 8a** — `c11riboseqorf4`. Find the two annotated spectra and the y-ion ladders, and locate the peptide that starts at ORF position 2.
- [ ] **Fig. 5a** — read only the MS column, and note where the two-peptide rule draws the line between tier 1A and tier 2A. The rest of the table is [Module 8](08-tier-framework-synthesis.md).

## Written reflection

- [ ] Grade your three opening commitments. For each, write one sentence on *why* your prior was off, not just by how much.
- [ ] In under 150 words, explain to a colleague why "just sequence deeper" cannot raise the 2.5%. Use Extended Data Fig. 1 and Extended Data Fig. 2g, and do not use the word "sensitivity".
- [ ] Write the strongest defence you can of the HUPO-HPP two-peptide rule as applied to microproteins — the best case *for* keeping it unchanged. Then write the strongest case for rewriting it. You will need both for the journal club.
- [ ] One paragraph: if you were designing a study to find microproteins that this build cannot see, what would you change first — protease, acquisition mode, sample prep, or search database? Justify with a number from this module.
- [ ] Look up the ncORF-subset FDR figures in Supplementary Tables 15 and 16 and record them below. They are the numbers this module most needs and I could not read them.

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| What an MS2 spectrum physically is (peak list, precursor, retention time) | | |
| b/y ion series and reading a ladder of residue masses | | |
| Why tryptic spectra are y-dominated and HLA spectra are not | | |
| What a database search engine actually computes | | |
| Why `close but false positive` has to be a category | | |
| PSM → peptide → protein aggregation, and where claims inflate | | |
| The paper's stack and what each stage contributes | | |
| Trypsin's K/R rule as a hard constraint on short ORFs | | |
| The saturation curve as evidence against a depth explanation | | |
| Search-database dependence and the two asymmetries vs a GTF | | |
| Target–decoy estimation and both directions of its imperfection | | |
| Why `0.0009%` FDR and 63.9% manual rejection are compatible | | |
| Class-specific FDR — and the actual ncORF-subset values | | <!-- fill in from Supplementary Tables 15 and 16 --> |
| Where the BH analogy breaks (three places) | | |
| The HUPO-HPP rule stated exactly, and each clause's purpose | | |
| The length-dependent power curve, and 2 of 36 as its calibration | | |
| USIs, and what a USI does and does not assert | | |
| Why PRM against a heavy standard is a different kind of evidence | | |
| N-terminal acetylation at ORF position 2 as evidence of processing | | |
| PeptideAtlas categories and the core-set gatekeeping rule | | |
| The spine claim: 2.5% tryptic vs 24.6% HLA | | |

## What I now trust, and why

Write your own version. Mine, as a starting point:

**I trust the 66.** Not because the FDR is low — the *global* FDR turned out to be nearly uninformative for this subset — but because each survivor cleared a stack of independent filters that fail for different reasons. A false PSM would have to survive a calibrated posterior error probability threshold, then a written ten-point spectral inspection designed specifically to catch near-miss peptidoforms, then in many cases a comparison against a synthetic peptide's own spectrum. For `c11riboseqorf4`, it would additionally have to survive PRM co-elution with a heavy-labelled authentic standard in three cell lines and two independent sample preparations, and it would have to explain why the observed peptide starts at ORF position 2 carrying an N-terminal acetyl group. Errors are correlated within a method and largely uncorrelated across methods. Stacking methods is what converts a low-prior claim into a trustworthy one, and this consortium stacked them.

**I trust the 2.5% as a fact about the assay.** Extended Data Fig. 1 shows the protein-discovery curve is flat at the scale of the entire public spectral record; Extended Data Fig. 2a,b show a second search engine adds almost nothing; Extended Data Fig. 2g shows the number moves when you change the protease. Three independent lines, all pointing at chemistry rather than depth. That is a well-supported negative result, and a well-supported negative result about a method is genuinely useful knowledge: it tells you where to spend your next experiment.

**I trust manual curation more than I expected to.** I came in assuming hand-inspection was a pre-statistical relic. It is the opposite: it is the correct response to a situation where the population-level error model provably does not transfer to the subset of interest, and where no clean pre-test filter exists. The authors wrote their criteria down, published a decision flowchart, and made every judged spectrum addressable by USI so a reader can disagree with them one spectrum at a time. That is more falsifiable than most automated pipelines I use.

**And I trust the standard more, now that I can see what it is.** HUPO-HPP's two-peptide rule is not a claim about biology and not a statistical optimum — it is a deliberately simple, deliberately conservative convention that keeps a shared reference proteome low in false positives across many years and many contributing labs. Read that way, "fails HUPO-HPP verification" stops being a verdict on a molecule and becomes a statement about which molecules the convention was calibrated for. Which is precisely what makes agenda question 1 a real question rather than a complaint.

## Sources outside the paper

Everything else in this module is anchored to the paper by section, Methods subsection, or figure number. These are the external anchors, retrieved 2 September 2026:

- HPP MS Data Interpretation Guidelines 3.0 (the paper's ref. 15) — Deutsch et al., *J. Proteome Res.* 18, 4108–4116 (2019). Full text: [biorxiv.org/content/10.1101/733576v2.full](https://www.biorxiv.org/content/10.1101/733576v2.full). The rationale for retaining the "2 × 9" policy was retrieved via search snippet rather than the full text; verify before quoting.
- Gupta & Pevzner, "False discovery rates of protein identifications: a strike against the two-peptide rule", *J. Proteome Res.* 8, 4173–4181 (2009) — [pubmed.ncbi.nlm.nih.gov/19627159](https://pubmed.ncbi.nlm.nih.gov/19627159/).
- Sennels, Bukowski-Wills & Rappsilber, "Improved results in proteomics by use of local and peptide-class specific false discovery rates", *BMC Bioinformatics* 10, 179 (2009) — [bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-10-179](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-10-179).
- Universal Spectrum Identifier specification, HUPO Proteomics Standards Initiative — [psidev.info/usi](https://www.psidev.info/usi); resolver at [proteomecentral.proteomexchange.org/usi](https://proteomecentral.proteomexchange.org/usi/).
- THISP tiered search databases — [peptideatlas.org/thisp](https://peptideatlas.org/thisp/) (the paper's ref. 52, Deutsch et al., *J. Proteome Res.* 15, 4091–4100, 2016).
- The builds themselves: [non-HLA 2023-06](https://peptideatlas.org/builds/human/non-hla/) and [HLA 2023-11](https://peptideatlas.org/builds/human/hla/); ncORF entry point at [peptideatlas.org/builds/human/#ncORFs](https://peptideatlas.org/builds/human/#ncORFs).

Claims marked `unverified` inline: trypsin's inhibition by a following proline; the numeric mass of the carbamidomethyl adduct; MSFragger's fragment-ion indexing as the source of its speed; the enzymology of initiator-methionine excision and N-terminal acetylation. None of these is stated in this paper, and no claim in this module depends on them.
