# Misconceptions to unlearn

~1 hr, read twice: once at the end of Week 1, once after [Module 8](08-tier-framework-synthesis.md). The first pass warns you. The second pass is the audit — go through the table and mark honestly which beliefs you still hold in the reflex, whatever you now know intellectually.

Every row below is a belief a competent molecular biologist can hold without ever having been careless. Most of them are true for canonical protein-coding genes, which is exactly why they transfer badly to this catalogue. The confrontation column gives the specific evidence in this paper that breaks each one, so you can check it in your own copy rather than take my word for it.

One instruction about tone before you start. This file is deliberately adversarial, and read alone it would leave you cynical about the paper. That would be the wrong outcome and it is the failure mode this curriculum is most at risk of, because the figure you can referee best ([Fig. 6i–j](07-function-crispr-olmalinc.md)) is the paper's weakest. The last section — [What the paper does establish](#what-the-paper-does-establish) — is not a politeness. It is the point of the document, and it is where you should stop reading.

## Prior belief → confrontation → resolution

| Prior belief | What breaks it in this paper | Revised belief, stated positively |
|---------|-------|-------|
| lncRNAs are non-coding | `OLMALINC` (`ENSG00000235823`, biotype `lncRNA`) carries **six** GENCODE-recognised ncORFs; one of them, `c10riboseqorf92`, is a 123-aa pan-essential dependency whose coding sequence rescues the knockdown phenotype (Fig. 6e,f) | `gene_biotype "lncRNA"` asserts that no CDS has been annotated on this gene *in this release of this annotation*. It says nothing about whether the locus is translated, whether a polypeptide accumulates, or whether the gene's function is RNA-mediated |
| if it's in the GTF it's real | Of the 15 provisional Tier 1A ncORFs prioritised for annotation, one was a **miscalled CDS caused by a GRCh38 assembly error** and one was a **novel CDS isoform** rather than a new gene (Fig. 5c) | A reference is a set of hypotheses with different amounts of evidence behind them, and some of them are artefacts of the assembly the reference is built on. "It is annotated" and "it is real" are separate claims, and this paper found the reference genome itself wrong once in fifteen tries |
| detection means existence means function | 1,785 ncORFs yield an HLA peptide; 66 survive tryptic-peptide curation; **3** became protein-coding genes (Fig. 2, Fig. 5b,c). Agenda question 5: *immune recognition of a peptide is not currently considered a biological function by annotation projects* | Three separable claims — the molecule is synthesised; it is synthesised in normal physiology; it does something — with three different burdens of proof and three different decision-makers. `peptidein` is the word for "claim 1 established, claim 2 uncertain, claim 3 unreached", and 121 ncORFs now hold it |
| the human protein-coding gene count is settled | The Introduction states plainly that the count "was felt to be largely stable" until ncORF translation evidence arrived, and that "any wholesale addition of protein-coding genes creates ripple effects across human bioscience" | The count is a curatorial position under active negotiation between named institutions, revised conservatively because addition is cheap and retraction is not. This paper is one round of that negotiation, and it moved the number by three — [Module 1](01-annotation-problem.md) names who decides what |
| 1% FDR means 99% of my hits are right | The non-HLA build reports a peptide-level FDR of `0.0009%`. Manual inspection then rejected **117 of 183** ncORFs (63.9%), including 105 of 141 supported by a single peptide. Extended Data Fig. 2c,d show decoy PSMs accumulating *faster* than ncORF PSMs as the threshold relaxes | An FDR is a property of the population you estimated it on. A rare, low-prior, low-information subset inside that population can carry an error rate orders of magnitude higher and the global figure will not move. Ask for the class-specific FDR (here: Supplementary Tables 15 and 16) — [Module 4](04-mass-spec-proteomics.md) works this through |
| HLA presentation proves it's a functional protein | `c10riboseqorf92` has HLA peptides, pan-essentiality in ~415 of 485 cell models, an ORF-specific rescue, DepMap co-essentiality structure and a multiplexed scRNA-seq signature — and remains a **peptidein** (results, "OLMALINC produces an essential peptidein") | HLA detection is strong evidence of synthesis and *no* evidence of function under the criteria that gate a gene record. That is a policy position the consortium poses as an open question, not a biological finding — which means you can argue with it, but you cannot ignore it when reading an annotation |
| conservation is one axis, and more conserved means more likely real | 2,211 of 7,264 ncORFs (30.4%) have placental-mammal `ORBLq` > 0.9 against 10% expected, while only 143 (2.0%) reach `PhyloCSF` per codon > 10. `c8riboseqorf102`: `ORBLq` 0.98, `PhyloCSF` −30, HLA-detected. `c11norep1`: `ORBLq` 0.00, HLA-detected | Three different axes. `PhyloCSF` scores selection on the *amino acid sequence*. `ORBLv` scores raw conservation of *ORFness* and rises with shortness, clade shallowness and CDS overlap. `ORBLq` is `ORBLv` against a biotype- and length-matched null and is the only one of the three that means "constrained". A high `ORBLq` with a negative `PhyloCSF` is the *predicted* signature of a regulatory uORF, not a discordance |
| a knockout phenotype at a locus means the ORF is functional | A guide cutting a uORF cuts the same DNA and disrupts the same mRNA as the host CDS. The paper needed seven layers of control to make the localisation claim, and `intORF`s were excluded from the library outright because no cut site can separate them (Methods, "CRISPR screening") | A fitness screen localises to a cut site; annotation is about a molecule. The paper's ladder closes most of that distance — design-time exclusion, expression *and* translation filtering in the screened cells, CDS-score subtraction, CRISPRa against de-repression, an in-gene permutation null, three-study replication, Cas13 concordance — and the residue is precisely what `peptidein` names. The one construct that would close it, a translation-dead rescue, is not in the paper |
| small proteins should be easy to detect — they're short | Of a manually curated set of small GENCODE proteins whose existence nobody disputes, **only 2 of 36 under 50 amino acids (5.6%)** satisfy benchmarks for HUPO-HPP verification (main text, "Microproteins in digest MS/MS datasets") | Trypsin cuts after K and R, so whether a short ORF yields *any* usable peptide is fixed by its sequence before the experiment starts. "Fails HUPO-HPP verification" carries almost no evidential weight against a short ORF, because the standard fails 94% of short proteins we already believe in |
| AlphaFold pLDDT > 90 means a real fold | Of 581 ncORFs with AlphaFold3 pLDDT > 90, each shuffled five times into 2,905 scrambles, only **36** had no shuffle reach 90 and only **6** had none exceed 80. Separately, pLDDT tracks *inversely* with ncORF length (Extended Data Fig. 10e–h, 10f) | On a short sequence, high pLDDT is mostly a statement about amino-acid composition and chain length. Read Extended Data Fig. 10a (length by tier) and 10f (pLDDT versus length) *before* 10b–d, or you will read a length confound as a folding result. Note that Extended Data Fig. 10 has no printed Methods subsection, so none of it can be audited from the article body |
| RNA abundance tells me whether the protein is there | Detected ncORFs sit at 14.3 mean GTEx FPKM against 10.7 for undetected ones — a ratio of **1.34** with *P* = 1.1 × 10⁻²³ (Fig. 3d). Extended Data Fig. 6f repeats it per tissue and *every* stratum is significant. And the tissue differences in Fig. 3e were **not** explained by transcript expression (Extended Data Fig. 6h) | Expression is a real determinant and a useless classifier. This one you already know from your own bench: a pseudobulk contrast over tens of thousands of cells returns underflowing *P* values for log₂ fold changes of 0.05, which is why you gate on effect size too. Same statistics, same fix — and uniform significance across dozens of strata is a diagnostic of sample size, not thirty independent confirmations |

## Notes on the five hardest rows

### "Detection means existence means function" is three claims, and the paper separates them for you

Do not learn this as a slogan. Learn the asymmetry in the evidence. A peptide identified in the HLA build had to survive: a ribosome making the polypeptide, entry into the cytosolic degradation pool, proteasomal cleavage to a compatible C terminus, TAP transport, ERAP trimming, binding an allele whose motif it happened to match, surface display, immunoaffinity capture, a `0.0041%` peptide-level FDR, and — for the inspected subset — a human reviewer. Layer on that 94.8% of predicted–observed binder concordance across 493 distinct HLA typings (Fig. 2k), and claim 1 is about as well established as a detection argument gets. Claim 2 is addressed only through sample provenance, and claim 3 is not addressed at all. The gap is not a weakness in the data. It is the gap the vocabulary was invented to name.

### `ORBLq` is the same operation you already run four times a week

`AddModuleScore` against expression-matched control bins. Adjusted *P* against a fitted dispersion. pLDDT against composition- and length-matched shuffles. Guide-level log₂ fold change against an in-gene permutation null. Four domains, one move: **a score is evidence only against a matched null.** `ORBLv` → `ORBLq` is the fifth instance, and the reason [Module 6](06-evolution-orbl.md) is the module most likely to change how you read scores in your own work. The transferable question is not about evolution: it is "what was this compared against, and was the comparison matched on the thing that would otherwise explain the result?"

### "Rejected on inspection" is not "shown to be false"

This is the misconception most likely to make you overclaim while sounding rigorous. The paper's five manual verdict categories are `excellent`, `good`, `false positive`, `close but false positive` and `low information` (Methods, "Manual inspection of ORF MS spectra"). Only **two** of the five assert that the identification is wrong. `good` means "probably correct but not compelling enough"; `low information` means "compatible but coverage too low". So the 63.9% rejection rate is a **failure-to-meet-the-annotation-bar rate**, and it is an *upper bound* on the ncORF-subset false discovery rate, not an estimate of it. When you quote a tryptic number, say which of three things you mean: not detected, not annotation-grade, or shown to be wrong.

### A negative `PhyloCSF` score fails in two completely different ways

Keep these apart or you will lose the argument to a comparative genomicist. **Low power**: a 17-codon uORF offers too few codons and too few substitution events for the likelihood ratio to accumulate, so the score compresses toward zero. That is an absence of evidence in either direction, and it explains why so much of Fig. 4f's density piles up near zero. **Hypothesis mismatch**: `c8riboseqorf102`'s −30 per codon is a *confident* answer — the residues are diverging faster than a coding model predicts — and it is exactly what you expect when the reading frame is constrained and the amino acids are free. If you merge the two into "`PhyloCSF` is unreliable for short ORFs" you have replaced a precise criticism with a vague one.

### "121 peptideins" is a curation-budget result, not a survey

Per Fig. 5e, only Tier 1A and Tier 2A ncORFs, plus Tier 1B ncORFs detected by ≥5 HLA peptides (and a handful otherwise prioritised), were considered for manual validation at all. The 121 decompose as 12 + 72 + 34 + 3 — from Tier 1A candidates not annotated as protein, the ≥5-HLA-peptide Tier 1B group, Tier 2A, and three separately prioritised ncORFs. So 121 is the number of ncORFs that a finite amount of expert time was spent on, over four hand-selected strata. It is not an estimate of how many peptideins exist. The population that was never adjudicated is Tier 4: **5,457 of 7,264**, whose Ribo-seq `+` is inherited from the source catalogue and was not re-inspected in this work.

## Traps specific to this paper

### The denominator zoo

[Module 2](02-ncorf-atlas-biotypes.md) sets these up and [Module 5](05-immunopeptidomics.md) uses them. There is no single number for "detected". There are at least four, and they differ by peptide-assignment rule, by curation stage and by which ORFs had a score at all. Every one of these is correct in its own place.

| Number | What it counts | Over | Anchor |
|---------|-------|-------|-------|
| 1,785 / 5,479 | HLA build, peptides assigned **exclusively** to one ncORF | 7,264 | main text; Fig. 2e,f; Extended Data Fig. 5a–d |
| 1,867 / 5,397 | HLA build, peptides **not** exclusively assigned | 7,264 | Fig. 3a; Methods, "Detectability determinants" |
| 1,796 / 5,142 | as 1,867, minus 326 ncORFs with no GTEx gene ID | 6,938 | Fig. 3d; Extended Data Fig. 6f |
| 1,735 / 5,081 | HLA-detected ncORFs for which `ORBLq` is defined | 6,816 | Fig. 4e; Extended Data Fig. 7f |
| 183 | tryptic ncORFs passing FDR thresholds, **before** curation | 7,264 | Fig. 2a,b |
| 66 | tryptic ncORFs **surviving** manual inspection (30 of 42 + 36 of 141) | 7,264 | main text; Fig. 2c,d |
| — / 6,912 | hydrophobicity-profile panel, `doORF` (61) and processed-transcript ORFs (291) dropped for low abundance | — | Fig. 3b |

Two exclusions to have at your fingertips, because they are the ones that make the arithmetic close. `7,264 − 448 = 6,816`: the 448 `mixed`-biotype ORFs have no single frame relationship to a CDS, so no matched null, so `ORBLq` is **undefined** for them — not low, undefined. And `1,785 − 1,735 = 50`, `5,479 − 5,081 = 398`, `50 + 398 = 448`: every ORF is accounted for. When you quote a rate from this paper, name the bookkeeping, or a proteomicist will name it for you.

### The subtraction that closes and means nothing

Fig. 3a prints detected `n = 1,867` against undetected `n = 5,397`, which sums to exactly 7,264. It looks like a union across the two builds, and `183 + 1,785 − 1,867 = 101` looks like it hands you the overlap. **It does not, and you should learn the number 101 only so that you recognise it as wrong when you see it on someone's slide.**

Two things rule that reading out. Fig. 3 is titled "Determinants of ncORF peptide detection **in the HLA build**". And its Methods state verbatim: *"Contrary to most other analyses, peptides were not exclusively assigned to a single ncORF, due to which the number of detected ncORFs was larger than in Extended Data Fig. 4b."* So 1,867 exceeds 1,785 because ambiguous peptides are counted against several ncORFs *inside one build*, not because a second build was added. **This paper never reports the cross-build union and never reports the overlap.** Recovering either needs the per-ncORF supplementary tables, which are not in the article PDF.

The general habit is worth more than the specific case: **arithmetic closure tells you a figure is internally consistent; only its Methods tell you what it counts.** Two different quantities can print the same digits.

What to use instead, and it is stronger than a union would have been. Fig. 3a scores ncORFs *and* canonical proteins in the same panel, on the same spectra, under the same assignment rule: roughly a quarter of ncORFs against **15,581 of 20,326 canonical proteins (76.7%)**. A threefold gap with no between-method confound to argue about. One caveat to carry: the ncORF side lets a peptide count against several ncORFs, so if anything that quarter is generous. And do not quote 76.7% as *tryptic* coverage — it is immunopeptidomic coverage of the canonical proteome, in the HLA build.

### Version drift: never put a Fig. 1b count and a Fig. 4 fraction in one sentence

The catalogue's biotypes were defined on GENCODE v35; the evolutionary analysis re-derived them on v42. Same 7,264 ORFs, two coordinate systems, and the counts move in **both** directions: `uORF` 3,083 → 2,915, `uoORF` 688 → 622, `dORF` 504 → 460, but `intORF` 720 → **743**, `doORF` 61 → **64**, `lncRNA ORF` 1,917 → **2,012**. An exclusion cannot make a class grow, so the shortfall is transcript remodelling between releases *and* the strict pure-biotype criterion, superimposed in proportions the paper never states. Nothing about the ORFs changed. The host transcript models changed, and biotype is defined relative to the host.

The operational lesson is one you can use on Tuesday: an annotation version is a coordinate system, not a formatting detail. "It's in GENCODE" is not a fact until you say which release.

### "Three genes" is genuinely ambiguous — say which three

There are three distinct sets, and conflating them is the easiest way to look careless in front of a GENCODE curator.

- **The three from this paper's Tier 1A funnel**: `c12norep105` in `CYP27B1`, `c21norep46` in `ERVH48-1`, `c11riboseqorf4` in `PIDD1`.
- **`c2riboseqorf47`** (the `GMCL1` uORF), promoted separately as `ENSG00000310604` on `ORBL` constraint, CRISPR evidence, cross-species translation and HLA support — with **zero** tryptic MS peptides.
- **Three Tier 1B ncORFs GENCODE had already annotated before this work**, per ref. 4 and "in each case on the basis of the evolutionary profile": `c14riboseqorf117` in `EIF5`, `c1riboseqorf55` in `PTP4A2`, `c3riboseqorf98` in `CGGBP1`. These are inherited, not products of this study.

And the irony to carry with the first set: `c11riboseqorf4` is a **171-amino-acid** uoORF with 11 distinct peptides across 94 experiments, whose peptides appear in non-malignant tissue, cancer samples *and* cell lines. It is the best-detected member of the catalogue *because* it is long enough for trypsin to work on, and size is a detection determinant (Fig. 3). The catalogue's most convincing member is its least typical one. Any intuition you form about microproteins from that example will be wrong about the other 7,263.

### Tier counts and detection counts will not reconcile, and should not

Add the final tiers carrying any proteomic evidence — 16 + 601 + 39 + 1,059 + 90 + 2 — and you get **1,807**. The provisional equivalents give **1,911**. Fig. 3a's detected set is **1,867**. The HLA build's exclusive count is **1,785**. Four numbers for what sounds like one quantity, and none of them is a cross-build union.

They differ for two reasons. Peptide-to-ORF assignment is exclusive in the tier bookkeeping and non-exclusive in the Fig. 3 detectability analysis. And, larger: 1,867 counts detections *as nominated*, while final tiers are assigned *after* manual spectral review — so an ncORF whose only peptide failed inspection keeps no proteomic tier and falls to Tier 4. That mechanism is also why Tier 4 grows by 104 while every other tier shrinks. Do not try to make these agree. Instead be able to say, for any number you quote, which side of curation it sits on.

## What the paper does establish

Read this section last, and read it as carefully as the table. Everything above is a boundary on the claims. Here is what is inside the boundary, and it is a lot.

- **These ncORFs are translated** ([Module 3](03-riboseq-bridge.md)). Three quarters of the catalogue rests on ribosome profiling alone, and that is a real physical measurement: a nuclease-protected cast of a ribosome, phased to a codon, recurring in one frame and not the other two. Frame preference is not something noise produces. Where the paper did re-audit it, on the 691 HLA-nominated profiles, it held up in 613 (88.7%) — and the authors published the unflattering split, 96.1% for multi-study ncORFs against 76.1% for single-study ones, which is an admission that their inherited catalogue is uneven.
- **Thousands of these ncORFs really do make polypeptides.** The strongest reason is not the FDR. It is that the 3,116 HLA peptides carry the binding motifs of the *particular alleles the particular donors happened to have*, at 94.8% concordance across 493 typings and every sample type (Fig. 2k). A search artefact has no mechanism for that. Add PRM co-elution against heavy-labelled authentic standards in three cell lines and two independent sample preparations for `c11riboseqorf4`, plus one peptide beginning at ORF position 2 with N-terminal acetylation — which means the cell recognised the N terminus, trimmed the initiator methionine and modified it. That is evidence of a *processed protein*, not merely of a detection.
- **Immunopeptidomics and digest proteomics measure different physical quantities** ([Module 5](05-immunopeptidomics.md)). Standing pool versus flux through degradation. That single distinction explains the 24.6%-versus-2.5% yields, explains why the assay is enriched for unstable products, and made running both windows the right design rather than a redundancy.
- **The 2.5% is a fact about the assay, not about depth.** Three independent lines converge: the protein-discovery curve is flat at the scale of the entire public spectral record (~1 new protein per million PSMs, Extended Data Fig. 1); a second search engine adds almost nothing (Extended Data Fig. 2a,b); and the number *moves* when you change the protease (Extended Data Fig. 2g). A well-supported negative result about a method is genuinely useful knowledge — it tells you where to spend the next experiment.
- **ORF-level evolutionary constraint on ncORFs is real and common.** 30.4% above `ORBLq` 0.9 against a 10% null, *P* < 2.3 × 10⁻⁵⁰, from a quantile whose null contamination biases it toward *understating* the effect, with per-biotype numerators and denominators that reconcile exactly to the catalogue total. "These ORFs lack constraint" was the wrong summary, and the reason is precise: the standard test measures selection on amino acids, and the hypothesis for most of these ORFs is selection on the reading frame.
- **`ORBL` is stated precisely enough to disagree with.** Any stop codon counts as a conserved stop. Compensating indels count as a conserved frame. Species absent from the local alignment count in the denominator. The null is 1,717,927 untranslated ORFs assembled by printed rules. You could reimplement it, and you could name the specific choice you would argue about — which is more than a fitted dispersion estimate offers you.
- **The tier framework does discriminating work in both directions.** It promoted `c2riboseqorf47`, a 19-codon ORF with zero tryptic peptides that the previous standard could not merely fail to prove but could never prove *in principle*. And it demoted a majority of its own automated top-tier calls: Tier 2A from 146 to 39, Tier 1A from 37 to 16, Tier 4 growing by 104. A curation process whose errors run toward caution is one you can build on.
- **`peptidein` makes a previously unrepresentable state representable.** Before it, an ORF with excellent detection and no demonstrable physiological function had no status at all — it was simply absent from the reference. Now it has a record that says something true, with five annotation bodies behind it and 121 initial members.
- **The paper reasons in the open about its own limits.** It keeps MS and HLA in separate columns rather than collapsing them into a proteomics score that would have hidden its most important structural finding. It publishes the 2-of-36 control that undercuts its own evidence standard, the shuffle control that undercuts its own pLDDT trend, and the 66.9%-cancer-spectra figure that blocked 10 of its 15 final candidates. It reports 30.4% against the larger, less flattering denominator. And it hands seven unresolved policy questions to its own community rather than answering them quietly in its favour.
- **And 3 of 7,264 is the thesis, not a disappointment.** The claim is not "we found three genes". It is: here is a procedure that takes billions of spectra, whole-genome alignments across 116 placental mammals, and CRISPR screens in hundreds of cell lines, and yields a handful of gene records that GENCODE, UniProtKB, HGNC, RefSeq and HUPO-HPP will all stand behind — plus an honest, populated category for the cases where they cannot. A procedure that promoted a thousand ORFs would tell you nothing about its own reliability.

## Self-check

- [ ] Without looking, state the three separable claims and say which one HLA data establishes, which it only touches through sample provenance, and which it cannot reach
- [ ] Explain to a colleague why `183 + 1,785 − 1,867` does not give the cross-build overlap, quoting what Fig. 3's own Methods say 1,867 counts
- [ ] Name the number you would put on a slide for "how hard are microproteins to see", and say why a same-panel comparison beats a cross-build one
- [ ] Give the three conservation axes and the ncORF that shows two of them disagreeing in each direction
- [ ] State the 2-of-36 control and explain why it makes "fails HUPO-HPP verification" almost evidentially empty for a short ORF
- [ ] Explain why "rejected on inspection" is an upper bound on the ncORF false discovery rate rather than an estimate of it
- [ ] Say which three genes you mean, when you say "three genes"
- [ ] Reconstruct 7,264 → 6,816 and 1,785 → 1,735 → 448 without notes
- [ ] Argue that 3 of 7,264 is the finding, to someone who has read only the abstract

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| `lncRNA` biotype asserts nothing about translation | | |
| A reference contains artefacts, including assembly errors | | |
| Detection / normal physiology / function as three claims | | |
| The gene count is a curatorial position, not a measurement | | |
| Global FDR versus class-specific FDR | | |
| Immune recognition is not counted as function — as policy | | |
| `PhyloCSF` vs `ORBLv` vs `ORBLq` | | |
| A fitness screen localises to a cut site, not a molecule | | |
| The 2-of-36 small-protein control | | |
| pLDDT, length, and the shuffle control | | |
| Effect size versus *P* value in Fig. 3d | | |
| The denominator zoo, and naming the bookkeeping | | |
| Version drift between Fig. 1b and Fig. 4 | | |
| "Three genes" — which three | | |
| Tier counts versus detection counts | | |
| What the paper does establish, stated positively | | |

Read alongside [Module 8](08-tier-framework-synthesis.md), then take it to [the journal club and capstone](journal-club.md). Terms are collected in the [glossary](glossary.md).
