# Module 6 — Evolution: ORBL, constraint versus conservation

~2 hrs. Prerequisites: [Module 2](02-ncorf-atlas-biotypes.md) for the biotypes, [Module 5](05-immunopeptidomics.md) for what "HLA-detected" means.

Covers Fig. 4, Extended Data Fig. 7, Extended Data Fig. 10, the results section "Evolutionary insights to interpret ncORFs", the Methods subsection "Evolutionary conservation and constraint (ORBL)", and agenda question 4.

This is the paper's novel method and the hardest single idea in it. It is also the module most likely to change how you read scores in your own work, because the thing ORBL gets right is not really about evolution.

## Predict first

Write these down before reading on. Numbers, not hedges.

1. Of 7,264 ncORFs, what percentage do you expect to show strong evolutionary constraint under a purpose-built ORF-level metric? Write a percentage.
2. Of the same 7,264, what percentage do you expect to show strong *amino-acid-level* coding constraint by `PhyloCSF`, the standard comparative-genomics test? Write a percentage.
3. Consider a 17-codon uORF that is a genuine, conserved, functional translational regulator — it really does control ribosome flux onto the downstream CDS in every placental mammal. What `PhyloCSF` score do you expect it to have? Write a number, with a sign.
4. Will conservation scores computed over the primate clade be *higher* or *lower* than the same scores over placental mammals? One word, plus one sentence of reasoning.
5. Which ncORF biotype should score highest for conservation of ORF structure, and is that a biological result or an artefact? Name a biotype and pick one.

Predictions 1 and 2 are the punchline. Prediction 3 is the correction. Predictions 4 and 5 are the two traps.

## The prior art, and the problem it created

The field's default reading of ncORFs, stated in the paper's own first sentence on the subject, is that their biological interpretation "has historically been framed by their lack of clear evolutionary constraint as protein-coding genes" (results, "Evolutionary insights to interpret ncORFs", citing ref. 23 — Sandmann *et al.*, *Mol. Cell* **83**, 994–1011, 2023).

That framing is an inference from a measurement, and the measurement is `PhyloCSF`.

### What PhyloCSF actually does

`PhyloCSF` (ref. 24 — Lin, Jungreis & Kellis, *Bioinformatics* **27**, i275–i282, 2011) takes a multi-species nucleotide alignment of a candidate region and asks a single question: does the pattern of substitutions across that alignment look more like a region evolving under selection on its *protein* sequence, or like a region evolving without it?

Mechanically it is a phylogenetic likelihood ratio between two fitted models:

- A **coding** empirical codon model, with independent parameters for essentially every codon-to-codon substitution rate, estimated from alignments of known coding regions.
- A **non-coding** empirical codon model, the same machinery fitted to known non-coding regions.

Both carry estimates of branch lengths, codon frequencies and codon substitution rates from genome-wide training data. `PhyloCSF` computes the likelihood of the observed alignment under each and reports the log-likelihood ratio. The units are decibans: per the tool's own documentation, "A score of 10 decibans means the coding model is 10:1 more likely than the non-coding model; 20 decibans, 100:1; 30 decibans, 1000:1." Positive means coding-like; negative means non-coding-like. This paper reports the score normalised per codon, which is what the *x* axis of Fig. 4f says, and takes `PhyloCSF` per codon > 10 as the threshold for "candidate conserved protein" (main text; Fig. 4f annotation).

What is being tested is the amino acid sequence. A synonymous substitution barely moves the score; a non-synonymous one in a constrained residue moves it a lot. That is the point of the method and it is the right question for a normal CDS.

### The limitation, stated without softening

`PhyloCSF` is badly underpowered on short ORFs, and this is the most important comparative-genomics correction in this curriculum.

Two separate things are going on, and conflating them is the mistake almost everyone makes.

**First: low power.** The score is evidence accumulated over codons and over substitution events. A 17-codon uORF offers 17 codons, and across 116 placental mammals a short, slowly-evolving string may offer very few substitutions to score at all. The tool's own documentation warns that "low branch length (or low number of substitutions) tends to compress the score towards 0." The authors of `PhyloCSF` subsequently built `PhyloCSF-Ψ`, whose entire purpose is to estimate the relative likelihood that a raw score would arise from a coding or non-coding region *of a particular length*, so that "a score threshold that is meaningful for regions of different lengths" can be set. That extension exists because the raw score is not comparable across lengths. Read the implication: **a near-zero `PhyloCSF` score on a very short ORF is not evidence against coding. It is an absence of evidence in either direction.** Treating it as a negative result is reading noise as a finding.

**Second, and independently: wrong question.** Suppose a uORF's function is to be an ORF — to capture a scanning 40S at a particular position, initiate, and terminate somewhere upstream of the main CDS, modulating flux onto it. Selection then acts on the ATG, on the absence of an intervening stop, and on the position of the terminator. It does not act on which residues the ribosome strings together in between. Such an ORF is, in `PhyloCSF`'s sense, genuinely non-coding: no protein sequence is under selection. A strongly negative score is the *correct* answer to the question `PhyloCSF` asks, and it says nothing at all about whether the ORF matters.

So there are two ways a short ncORF ends up with a non-positive `PhyloCSF` score — too little information, or a hypothesis mismatch — and neither licenses "this ORF is not constrained". This is exactly the paper's stated motivation: "it is also possible that conventional methods do not sufficiently capture their constraint as ORFs" (results, "Evolutionary insights", where ref. 24 is the "conventional method").

One detail worth holding on to, because it changes how you should read this section: **Irwin Jungreis is the middle author of the `PhyloCSF` paper and a co-first author of this one**, and the ORBL implementation is deposited under his name (ref. 93; `https://github.com/iljungr/ORBL_tools`). This is not an outsider debunking a method. It is the method's own author saying it answers a different question, and building the one that answers this question.

## ORBL, mechanically

ORBL scores conservation of **ORFness** — "conservation across species of the initiation codon, the termination codon and the 'openness' of the reading frame without regard to conservation of the amino acid sequence" (results, "Evolutionary insights"; schematic in Fig. 4a; worked example in Extended Data Fig. 7a).

Get the mechanics exactly right, because every interpretive move later depends on them. All of the following is from the Methods subsection "Evolutionary conservation and constraint (ORBL)".

**The alignments.** The local alignment of each ORF is extracted from the 120-mammal whole-genome alignment against hg38 (ref. 83 — Hecker & Hiller, *GigaScience* **9**, giz159, 2020), restricted to the 116 placental mammal subset or the 26 primate subset. Additional clades in Supplementary Table 11 use the 100-vertebrate, 470-mammal and 447-mammal alignments.

**Conserved start.** The bases aligned to the reference ORF's start — possibly more than three of them — must include three consecutive bases that are `ATG`.

**Conserved stop.** Same rule at the other end: the bases aligned to the reference stop must include three consecutive bases that are *any* stop codon. Not the same stop codon. Extended Data Fig. 7a makes this explicit: a `TAA` in Drill counts as conserved even though the human codon is different. This is the definitional heart of "ORFness" — the requirement is that translation terminates there, not that it terminates on a particular trinucleotide.

**Conserved open frame.** The aligned bases between the aligned `ATG` and the aligned stop must be a multiple of three **in total**, and must contain no in-frame stop codons and no alignment gaps. Read "in total" carefully: a frame-shifting insertion is tolerated if a compensating deletion restores the total length. Extended Data Fig. 7a's Bushbaby row is exactly this case — one frame-shifting insertion plus one frame-shifting deletion, net length a multiple of three, scored as frame-conserved. This is a deliberate and slightly unusual choice. It says the biological requirement is that a ribosome initiating at the aligned `ATG` runs to the aligned stop without terminating early; it does not require that the intervening codons correspond one-to-one with human codons.

**Conserved ORF.** All three at once: start, stop and frame.

**ORBLv.** The phylogenetic branch length of the species with a conserved ORF, divided by the branch length of **all 116 placental (or 26 primate) species in the whole-genome alignment** — explicitly "not just the ones present in the local alignment". That parenthesis is load-bearing. A species that has no alignment at your locus at all counts in the denominator and not the numerator, so missing alignment is scored as non-conservation. ORBLv is therefore a joint measure of ORF conservation and alignability, and it is bounded on [0, 1].

Fig. 4a draws two worked cases side by side. In one, the conserved branch length is 0.3 against a total of 0.3 + 0.6, printed as ORBLv = 0.3. In the other, 0.8 against 0.8 + 0.1, printed as ORBLv = 0.9. Do the arithmetic yourself as you read it — 0.3/0.9 is 0.33 and 0.8/0.9 is 0.89, so the panel's stated values are rounded to one decimal. Not an error, but it is the sort of thing you should notice about a schematic before you trust the numbers beside it.

The worked example in Extended Data Fig. 7a uses a 17-codon uORF, `c1norep308`, with the primate alignment rendered in `CodAlignView`, a per-species table of `ATG` / frame / stop, and a phylogenetic tree with the conserved branches in green. Spend real time on this panel: it is the only place in the paper where you can see the numerator and denominator of a score as tree topology.

## Why ORBLv is not the answer

ORBLv behaves exactly as it should on positive controls, and the paper reports this as expected rather than as a result (results, "Evolutionary insights"; Extended Data Fig. 7b,c):

- Annotated CDSs score higher than ncORFs.
- **Short** CDSs score higher than long ones. Of course they do — a short string has fewer chances to acquire a disrupting substitution or a net-shifting indel.
- **Primate** scores are higher than placental mammal scores. Less elapsed time, fewer substitutions, more sequence retained by inertia rather than by selection.
- Biotypes that overlap annotated CDS — `uoORF`, `intORF`, `doORF` — score higher than those that do not, in the legend's own words "presumably due to 'free' conservation from the CDS" (Extended Data Fig. 7b,c legend).

Every one of those four is a reason the raw score cannot be read as constraint. Three of them are pure nuisance: length, clade depth and CDS overlap all raise ORBLv without any selection on the ncORF itself. If you had predicted `uoORF` or `intORF` for question 5 and called it a biological result, that is the trap — the paper itself calls it a presumed artefact of the host CDS.

The general shape of the problem: **ORBLv is a magnitude with no scale.** Is 0.64 a lot? For a 17-codon uORF in a primate alignment, almost certainly not. For a 100-codon `dORF` across placental mammals, possibly extraordinary. You cannot tell from the number.

## ORBLq — the matched null

ORBLq is the constraint score: **the quantile of an ncORF's ORBLv among the ORBLv scores of untranslated ORFs matched for biotype and similar length.** Everything interesting about ORBL is in that sentence, so here is how the null set was built (Methods, "Evolutionary conservation and constraint (ORBL)").

**Constructing the background.** Start with every `ATG`-initiated ORF of any length in any protein-coding or lncRNA transcript in GENCODE v42 that does not overlap a protein-coding CDS of any transcript **in the same frame**. ORFs are not required to be maximal — if an ORF contains a downstream `ATG`, the nested ORF from that `ATG` to the same stop is also included. Then exclude:

- ORFs without a "pure" biotype under the paper's strict criteria (Supplementary Results);
- ORFs overlapping any of the 7,264 ncORFs;
- ORFs overlapping an mRNA on the opposite strand, or a pseudogene on either strand;
- `dORF`s that overlap any 5′-UTR.

Finally, `uoORF`s, `intORF`s and `doORF`s are segregated by the frame in which they overlap the main ORF, `+1` or `+2`, because — as the Methods put it — constraint on the main frame's amino acid sequence imposes different ORFness constraint on the two overlapping frames. That is a genuinely subtle piece of modelling: the wobble position of the host CDS falls in a different place relative to your ORF depending on the offset, so the two offsets have different background probabilities of retaining an open frame.

**The background set.** 1,717,927 untranslated ORFs, distributed as `uORF` 63,795 · `uoORF+1` 3,231 · `uoORF+2` 2,940 · `intORF+1` 320,823 · `intORF+2` 60,135 · `doORF+1` 16,910 · `doORF+2` 5,946 · `dORF` 653,983 · `lncRNA-ORF` 590,164. ORBLv was computed for every one of them.

**Matching.** For a given ncORF, take at least 1,000 untranslated ORFs of the same biotype (and the same overlap frame, where applicable), starting with those of exactly the same length. If fewer than 1,000 exist at that exact length — the Methods note this was common for longer ncORFs and for rarer biotypes such as `uoORF` — widen to length ±1, then ±2, and so on until the matched set reaches 1,000. Fig. 4a's panel label reads "≥1,000 untranslated ORFs matched by biotype and length"; the Methods say "at least 1,000", and they agree.

**The score.** With ORBLv\* the value for your ncORF,

`P = (number of matched ORFs having ORBLv ≥ ORBLv* + 1) / (number of matched ORFs)`

with a pseudocount of 1 in the numerator to prevent `P = 0`, not added if the result would exceed 1. Then `ORBLq = 1 − P`. For some analyses the paper uses the information-content transform `−log10[1 − ORBLq]`, which is the *y* axis of Fig. 4g and appears again in Extended Data Fig. 9g.

### Two properties of a quantile against a finite null

**There is a ceiling, and it is set by the size of the matched set.** The smallest achievable `P` is `1/N` where `N` is the number of matched ORFs, so the largest achievable ORBLq is `1 − 1/N`. With `N ≥ 1,000` the ceiling is at best 0.999, and the resolution of the score is `1/N` — you cannot extract more evidence than the null has members to provide, no matter how perfectly conserved the ORF is. The `−log10[1 − ORBLq]` transform makes this visible: it tops out at `log10(N)`, so 3 for a 1,000-ORF null. Look at the *y* axis of Fig. 4g in your copy: it runs to 4, which implies that for some ncORFs the matched set ran well past 10,000 — unsurprising for `dORF` or `lncRNA-ORF`, where hundreds of thousands of background ORFs exist and a single exact length can supply many thousands. So the ceiling is per-ORF, not global, and the same nominal ORBLq means slightly different things for a common biotype and a rare one.

This also reframes what a specific score is worth. `c8riboseqorf102`'s ORBLq of 0.98, discussed below, means that roughly 2% of at least a thousand matched untranslated ORFs of the same biotype and length were at least as ORF-conserved as it is. That is a real signal. It is also nowhere near the ceiling of 0.999, and "0.98" reads more emphatically than "about 20 in 1,000 matched controls did as well".

**The null is contaminated by construction, and the contamination is conservative.** The background is called "untranslated", but nothing was measured. It is a set of ORFs that (i) do not overlap a CDS in frame and (ii) do not overlap one of the 7,264 catalogued ncORFs. Since that catalogue is demonstrably incomplete — it is a union of prior Ribo-seq studies, and [Module 3](03-riboseq-bridge.md) covers how unevenly those agree — some fraction of the 1.7 million background ORFs are genuinely translated and genuinely constrained. They are simply undetected.

Work out the direction of the bias before you read the next sentence. Truly-constrained ORFs sitting in the background shift the background ORBLv distribution to the **right**. A real ncORF is then being compared against a null that is more conserved than a truly-neutral null would be, so its quantile comes out **lower**. **The contamination makes ORBLq conservative: the reported constraint is a floor, not a ceiling.** That is the good direction for a bias to run, and it is worth saying out loud, because a contaminated null is normally a reason to distrust a result and here it is a reason to trust the sign of it.

## Where your instincts transfer, and where they break

You already use this construction. Twice.

> **Analogy 1.** ORBLq is `AddModuleScore` with expression-matched control bins. A raw mean expression across a gene set tells you almost nothing, because highly-expressed genes drag it up; so you bin genes by expression, draw control genes from the matching bins, and report your set's score *relative to* the matched controls. ORBLv is the raw mean. ORBLq is the score after subtracting what a matched null would have given you anyway.
>
> **Where it breaks.** Two ways, and both matter.
>
> First, the matching variable. Module scores match on **expression within the same dataset** — the controls come from the same cells, the same capture, the same depth, so technical confounders cancel almost automatically and you rarely have to think about what the control bins contain. ORBLq matches on **structural properties of the ORF** — biotype, length, and for overlapping biotypes the `+1`/`+2` overlap frame — drawn from a separately constructed, genome-wide reference population. It is not cancelling a technical artefact; it is cancelling two specific, named biological nuisances: chance retention of a short nucleotide string, and bleed-through constraint from an overlapping CDS. You have to know what those are to know whether the matching worked.
>
> Second, where the null lives. `AddModuleScore`'s control bins are a within-sample randomisation — the null is generated from your own data and there is essentially nothing to argue about. ORBLq's null is an **external, explicitly constructed ORF set** with eight documented inclusion and exclusion rules. That is a modelling decision you can interrogate, and disagree with, by naming a class of ORFs that should or should not be in it. It is a strength, not a weakness — but it means "ORBLq > 0.9" is a claim about a constructed comparison set, not a bare property of the ORF.

> **Analogy 2.** ORBLv is to ORBLq as raw log2 fold change is to an adjusted *P* value. Magnitude versus magnitude-relative-to-expectation. A log2FC of 2 is meaningless until you know the dispersion; an ORBLv of 0.64 is meaningless until you know what matched ORFs do.
>
> **Where it breaks.** The DE null comes from **the data's own dispersion estimate** — edgeR or limma fits variance from your counts and shrinks it toward a trend. You cannot really disagree with it except by disagreeing with the whole model. ORBLq's null is **an explicitly constructed set of 1,717,927 ORFs** assembled by rules printed in the Methods. That makes it interrogable in a way a dispersion estimate is not: you can ask whether excluding `dORF`s that overlap 5′-UTRs was right, whether the `+1`/`+2` split is sufficient, whether "untranslated" was ever verifiable. Every one of those is an argument you can have with the authors on the record. A dispersion estimate offers you nothing to argue with.

The second breakage is the one worth carrying out of this module: an explicitly constructed null is *more* criticisable than a fitted one, and that is a virtue.

## The punchline: both numbers are true

Now compare against your predictions 1 and 2.

**ORF-level constraint is common.** 2,211 of the 7,264 ncORFs (30.4%) have a placental mammal ORBLq > 0.9, against 10% expected for untranslated ORFs, *P* < 2.3 × 10⁻⁵⁰ by binomial test (results, "Evolutionary insights"; Fig. 4b,c). Among upstream ORFs it is 1,335 of 2,915 (45.8%). The 10% figure is not an estimate — it is what a quantile *means*. If ORBLq is a well-calibrated quantile against a matched null, exactly 10% of an unconstrained population exceeds 0.9 by definition, which is why the null in Fig. 4b is drawn as a straight diagonal and the null in Fig. 4c as a vertical line at 10%.

**Amino-acid-level conservation is rare.** Only 143 of the 7,264 ncORFs (2.0%) reach `PhyloCSF` per codon > 10, including 74 of 2,915 uORFs (2.5%) (results, "Evolutionary insights"; Fig. 4f).

Thirty percent versus two percent, on the same 7,264 ORFs. If those two numbers feel contradictory, the contradiction is in the assumption that "constrained" is one property.

### Why both can be true

They are answers to different questions.

`PhyloCSF` asks: **is a protein sequence under selection here?** ORBL asks: **is an open reading frame under selection here?** For a canonical CDS the answers coincide, which is why nobody had to separate them before. For a regulatory uORF they come apart completely, and the paper draws the consequence explicitly: the excess for uORFs and uoORFs "suggests the presence of a large number of conserved functional regulatory upstream ORFs".

So: what should a conserved regulatory uORF look like on each axis? Write it down before reading the next paragraph.

**High ORBLq. `PhyloCSF` at or below zero.** Its `ATG` is conserved because initiation must happen at that position. Its stop is conserved — as a stop, not as a codon — because termination must happen before the main CDS. Its frame is open because a premature stop would shorten the arrest and change the flux. Its residues are free, because nothing downstream cares what tripeptide the 40S synthesised on the way. A high ORBLq with a negative `PhyloCSF` is not a discordance to be explained away. **It is the predicted signature of the hypothesis.**

### A denominator to check yourself on

The paper's 30.4% is `2,211 / 7,264`. But ORBLq is undefined for the 448 ncORFs with a "mixed" biotype — those that, for example, overlap CDS from two different transcripts in different reading frames — and they are excluded from the ORBL analysis entirely (Methods; Extended Data Fig. 7f legend). The 2,211 can therefore only have come from the 6,816 ORFs that *have* a score. Against the denominator that actually produced it, the figure is `2,211 / 6,816` = 32.4%.

The paper reports the smaller number. Note that its own uORF figure, 45.8%, uses `1,335 / 2,915` — the post-exclusion denominator. So the two headline percentages in the same paragraph are computed against different denominators, and the direction of the inconsistency is conservative for the aggregate. This is not a scandal; it is the sort of thing you should catch on a careful read, and it is the correct kind of error for a paper to make.

The per-biotype numerators and denominators are printed in Fig. 4c and they reconcile exactly. Copy them out and add them up yourself — `uORF` 1,335/2,915 · `uoORF` 243/622 · `intORF` 231/743 · `doORF` 12/64 · `dORF` 79/460 · `lncRNA ORF` 311/2,012. The numerators sum to 2,211 and the denominators to 6,816, which is 7,264 − 448. When a figure closes like that, you can build on it.

While you have those denominators out: compare them to the Fig. 1b biotype counts from [Module 2](02-ncorf-atlas-biotypes.md). `uORF` goes 3,083 → 2,915 and `dORF` 504 → 460, which you might read as exclusions. But `intORF` goes 720 → **743** and `doORF` 61 → **64**. Counts cannot *increase* under an exclusion. The explanation is in the Methods: the biotypes were re-derived on GENCODE v42, where the source catalogue used v35, so ORFs were reassigned between biotypes as host transcript models changed — and then the mixed-biotype ORFs were dropped on top of that. The gap between 3,083 and 2,915 is re-derivation plus exclusion, not exclusion alone. A biotype is a claim about a locus in a named annotation version, and this is what that costs you in practice.

### The clade comparison, and why it reaches the annotation decisions

Primate ORBLv exceeds placental mammal ORBLv (Extended Data Fig. 7b,c), for the reason you gave in prediction 4: less divergence time, fewer substitutions, more sequence retained without any selection acting. The primate versions of the ORBLq analyses are in Extended Data Fig. 7d,e.

ORBLq is what makes the two clades commensurable, because the quantile is taken against a null computed on the same clade — a primate ORBLq of 0.95 already has primate-wide inertia divided out. That is precisely what a raw score cannot do.

And the clade choice is not academic. Of the 15 Tier 1A candidates prioritised for annotation, **two were rejected for "unclear evolutionary constraint beyond primates"** (Fig. 5c; see [Module 8](08-tier-framework-synthesis.md)). Conservation restricted to primates was, for those two ORFs, the reason a gene record did not happen. When you read Extended Data Fig. 7b,c, you are reading the empirical basis for that curatorial rule.

### The confound the authors declare

`uoORF`, `intORF` and `doORF` score higher, and the paper attributes this to constraint on the host CDS rather than on the ncORF — "presumably due to constraint to preserve the CDS" (results, "Evolutionary insights"). Two things follow.

First, this is a statement about **ORBLv**, and ORBLq is the intended remedy: matching on biotype *and* on `+1`/`+2` overlap frame is exactly an attempt to price in the host CDS. Note that Fig. 4c still shows `uoORF` at 39.1% and `intORF` at 31.1% — both far above 10% — so either the matching leaves residual CDS bleed-through, or these biotypes really are constrained as ORFs, and ORBLq alone cannot tell you which.

Second, note the word "presumably". The authors are declaring an unresolved confound in their own headline result rather than burying it. Read that as a signal about how to read the rest: the section is written by people who expect to be checked.

## Constraint and detectability

The paper then asks whether ORF-level constraint has anything to do with whether a peptide was ever seen.

ORBLq is significantly higher for ncORFs whose microproteins were detected by HLA-I peptides than for undetected ones: `n = 1,735` versus `5,081`, *P* = 1.38 × 10⁻¹², two-sided Wilcoxon rank-sum (results, "Evolutionary insights"; Fig. 4e; Extended Data Fig. 7f). Per biotype, the effect is carried by uORFs (`n = 759` vs `2,156`, *P* = 2.66 × 10⁻⁵) and intORFs (`n = 247` vs `496`, *P* = 0.032), with Holm–Bonferroni correction for six hypotheses; the other four biotypes are not significant (Fig. 4g).

Check that those numbers close, because they do, and beautifully. `1,735 + 5,081 = 6,816` — the ORBLq-scoreable set. The full HLA-detected count is 1,785, so `1,785 − 1,735 = 50` detected ncORFs were lost to the mixed-biotype exclusion; the Methods elsewhere give 5,479 undetected, so `5,479 − 5,081 = 398` were lost from the other side; and `50 + 398 = 448`. Every ORF is accounted for. When you can trace a figure's *n* back to the total through two independent exclusions, you are reading a careful analysis.

### The circularity risk, sharpened

Here is the objection the authors do not raise, and you should.

**Both constraint and detectability correlate with ORF length.** Longer ORFs yield more tryptic peptides and more candidate HLA ligands, so length is a detection determinant in its own right (Fig. 3; [Module 5](05-immunopeptidomics.md)). And short ORFs have higher raw ORFness conservation than long ones (Extended Data Fig. 7b). If length drives both axes, an association between them can arise with no biology in it at all.

ORBLq is the defence, and it is a good one: matching on length removes the length dependence of the raw score by construction. But look at *how* the matching works. The matched set starts at the exact length and widens — ±1, ±2, ±3 — until it reaches 1,000, and the Methods state this widening "was common for longer ncORFs". So the length matching is tightest for short ORFs and loosest for long ones, which is exactly where the detection bias is strongest. The residual is small and it is not zero, and you cannot bound it from the paper alone. That is the honest form of the concern: **length-matching mitigates the circularity; it does not obviously eliminate it, and it degrades in the length regime where the confound is worst.**

### What the association licenses, and what it forbids

**Licensed:** ORF-level constraint and peptide-level detectability are positively associated across this catalogue, consistent with both being downstream of a common cause — that the ORF is genuinely, persistently translated. The paper's own conclusion is exactly this modest: "signatures of evolutionary constraint according to ORFness are associated with the detection of HLA-I peptides".

**Forbidden:** any causal direction. Constraint does not make a peptide detectable, and detection does not make an ORF constrained; both plausibly reflect a third thing. Also forbidden: **per-ORF inference.** A distributional shift with *P* = 10⁻¹² across 6,816 ORFs tells you nothing actionable about any single ORF, and the next section is two counterexamples that prove it.

## Two instructive cases

Read Fig. 4h and 4i side by side in your own copy. They are the paper's own demonstration that the two axes are independent.

### c8riboseqorf102 — high ORBLq, deeply negative PhyloCSF, HLA-detected

A `WASHC5` uORF. Fig. 4h prints it as a 20-residue sequence terminating in a stop, with **3 HLA peptides**, **ORBLq = 0.98**, **`PhyloCSF` per codon = −30**.

**What the scores license.** That the ORF structure — `ATG`, open frame, terminator — has been preserved across placental mammals far more than a biotype- and length-matched untranslated uORF: about 2% of at least a thousand matched controls did as well or better. And that its product is generated, processed, and loaded onto class I in at least one sample, three times over.

**What they forbid.** Any claim that the residues matter — the `PhyloCSF` score is the direct evidence that they do not. Any claim that the microprotein has a function; presentation is not function, and [Module 1](01-annotation-problem.md) covers why the annotation projects say so explicitly. And most importantly, the inverse inference: you may not read `−30` as evidence against this being a real, selected ORF, because `PhyloCSF` was never asking that question.

One careful note, because it is where a superficial reading goes wrong. `−30` per codon is *not* the "compressed toward zero, therefore uninformative" case. It is a confident answer — the residues are diverging faster than a coding model predicts — and it is exactly what you expect when the frame is constrained and the amino acids are free. The low-power problem explains why so much of Fig. 4f's density piles up near zero; `c8riboseqorf102` illustrates the *other* failure, the hypothesis mismatch. Keep the two apart. If you merge them into "PhyloCSF is unreliable for short ORFs" you will have lost the actual argument.

### c11norep1 — ORBLq of zero, still HLA-presented

A `BET1L` intORF. Fig. 4i prints it as a 35-residue sequence, with **2 HLA peptides**, **ORBLq = 0**, **`PhyloCSF` per codon = −1**. The main text describes it as one of the "recently emerged ncORFs" that "can also present with HLA-I peptide evidence".

Work out what ORBLq = 0 actually means from the formula. `ORBLq = 1 − P`, so `P = 1`: every matched untranslated ORF had ORBLv at least as high as this one, and the pseudocount was not applied because the result would have exceeded 1. This ORF's structure is not conserved at all relative to its own matched null. Fig. 4i's alignment panel shows why — read the legend keys for "OOF stop codon" and "Gap" and find them in the tracks.

**What the scores license.** That the ORF is young, and that youth is no barrier to entering the class-I pathway. It is translated; its product is processed; two peptides were observed.

**What they forbid.** Using low ORBLq as a filter. If you had proposed to prune the catalogue at ORBLq > 0.5 to remove noise, this ORF — with real, curated immunopeptide evidence — would have been discarded at the first step. Also forbidden: reading `PhyloCSF = −1` as anything at all. That is the near-zero, low-information case, and it means the method had nothing to say.

Note what the pair achieves together: 0.98 with detection, and 0.00 with detection. The population-level association is real and the per-ORF predictive value is close to useless. Both statements are true simultaneously, and holding them together is the skill.

## The same lesson in a second domain: structure prediction

Extended Data Fig. 10 runs the identical argument on predicted structure, and it is worth reading immediately after Fig. 4 because the shape is the same and the domain is unrelated.

**The trend.** Panels (b), (c) and (d) plot average pLDDT per ncORF by evidence tier, for AlphaFold3, ESMFold and OmegaFold respectively, with pairwise two-sided Wilcoxon tests and FDR-adjusted *P* values, only significant ones displayed.

**The confound, in the adjacent panel.** Panel (a) plots the distribution of amino acid sizes by tier. Panel (f) plots ncORF length against pLDDT and — in the legend's own words — "a clear inverse linear trend is observed, with shorter ncORFs exhibiting higher predicted pLDDT values."

Put those together before you interpret panel (b). Any difference in pLDDT between tiers is confounded by the tiers' length distributions, because length predicts pLDDT directly. The interpretive rule is: **read panel (b) against panel (a), never on its own.** Look at both in your copy and decide for yourself whether the tier ordering in (b) survives the tier ordering in (a) — that determination is the exercise, and I am deliberately not doing it for you, because the panels are raster and I could not verify the direction from the text.

**The control the authors ran, which is the good part.** Every one of the 581 original ncORF sequences with AlphaFold3 pLDDT > 90 was randomly shuffled five times, giving 2,905 shuffled sequences, and those were folded too (Extended Data Fig. 10e; 581 × 5 = 2,905, which checks). Panel (g) counts, per original sequence, how many of its shuffles exceeded pLDDT 80 or 90. Panel (h) reports the survivors: **36 ncORFs with pLDDT > 90 in which none of the five shuffled versions reached 90**, of which **six** — set in bold — had no shuffle exceed even 80.

Read the arithmetic. Of 581 sequences that AlphaFold3 was confident about, 36 remain confidently-folded-because-of-their-actual-sequence rather than because of their composition and length: **6.2%**. For 6 of them the result is emphatic. The other roughly 94% score highly for reasons a scrambled version of the same residues reproduces — which is to say, pLDDT > 90 on a short sequence is mostly a statement about amino acid composition and chain length, not about a specific fold.

That is the same correction as ORBLv → ORBLq, in a domain with no phylogeny in it. The shuffle is the matched null: same composition, same length, no real sequence.

The paper's own verdict on all of this is properly hedged — whether structure-based analysis "can be used to parse which HLA-supported ncORFs are more likely to encode a stable protein remains an open question" (Discussion).

**State the principle once, plainly, and carry it out of this module:**

> A score is evidence only against a matched null.

ORBLv → ORBLq. pLDDT → pLDDT of composition- and length-matched shuffles. log2 fold change → adjusted *P* value. Raw gene-set mean → `AddModuleScore` against expression-matched bins. Four domains, one operation. The next module runs it a fifth time, on CRISPR guides.

## Read the figure

Do these in your own PDF. Twenty minutes, and it is where the module lands.

- [ ] Fig. 4a: find both worked ORBLv fractions and check the division yourself. Then trace the arrow from ORBLv = 0.3 to ORBLq = 0.51 and from ORBLv = 0.9 to ORBLq = 0.95, and say in one sentence why the first pair barely moves and the second does.
- [ ] Fig. 4b: identify the diagonal. Say what a curve *below* the diagonal would mean, and whether any biotype does that.
- [ ] Fig. 4c: find the vertical dashed line at 10% and explain, without using the word "expected", why 10% is the correct null.
- [ ] Fig. 4e next to Fig. 4f: same 6,816 ORFs, same detected/undetected split, two different axes. Note where the bulk of the `PhyloCSF` density sits, and connect it to the low-power argument.
- [ ] Fig. 4g: read the maximum of the *y* axis and infer a lower bound on the largest matched-set size used.
- [ ] Extended Data Fig. 7a: find the Drill row and the Bushbaby row, and state in your own words the rule each one is there to illustrate.
- [ ] Extended Data Fig. 7b,c: identify the two MANE Select CDS length bins and check that short beats long, CDS beats ncORF, and primate beats placental. Then say which of those three is a nuisance and which is a positive control.
- [ ] Extended Data Fig. 10a and 10b together: decide whether the tier trend in pLDDT survives the tier trend in length.

## Write this down

- [ ] Compare predictions 1 and 2 against 30.4% and 2.0%. If you predicted them close together, write one sentence on what you were assuming about the word "constrained".
- [ ] Explain in four sentences, to a colleague who has never heard of `PhyloCSF`, why a `PhyloCSF` score of −30 on a 20-codon uORF is compatible with strong purifying selection on that uORF.
- [ ] State the difference between low power and hypothesis mismatch as reasons for a non-positive `PhyloCSF` score, and give a case from Fig. 4 that illustrates each.
- [ ] The ORBLq null contains ORFs that are translated but undetected. Derive the direction of the resulting bias from first principles, in two sentences, without looking above.
- [ ] Write the ORBLq definition from memory, including the pseudocount and the matching rule. Then state the maximum achievable ORBLq for an ncORF whose matched set has exactly 1,000 members.
- [ ] Name the one variable that could generate the ORBLq-versus-detectability association with no biology in it, and say precisely where the paper's defence against it is weakest.

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| What `PhyloCSF` computes: two empirical codon models, likelihood ratio, decibans | | |
| Why short ORFs give `PhyloCSF` little power, and what `PhyloCSF-Ψ` exists for | | |
| Low power versus hypothesis mismatch as two distinct reasons for a negative score | | |
| ORBL's three conserved features: start, stop, frame openness | | |
| Any stop counts as a conserved stop — the Drill rule | | |
| Compensating indels preserve frame — the Bushbaby rule | | |
| ORBLv = conserved branch length / total branch length over all species in the alignment | | |
| Why missing local alignment counts against ORBLv | | |
| The 1,717,927-ORF untranslated background and its eight construction rules | | |
| The `+1`/`+2` overlap-frame split, and why it is necessary | | |
| ORBLq = 1 − *P*, the pseudocount, and the ≥1,000 matching rule | | |
| The ceiling `1 − 1/N`, and why `−log10[1 − ORBLq]` tops out at `log10(N)` | | |
| Null contamination, and why it makes ORBLq conservative | | |
| 30.4% ORBLq > 0.9 versus 2.0% `PhyloCSF` > 10, and why both are true | | |
| The expected signature of a conserved regulatory uORF on each axis | | |
| Denominator care: 2,211/7,264 versus 2,211/6,816 | | |
| Why `intORF` counts rose from 720 to 743 across the v35 → v42 re-derivation | | |
| Primate versus placental clades, and the two Tier 1A rejections it caused | | |
| The declared CDS-overlap confound, and what ORBLq does and does not fix | | |
| ORBLq versus HLA detectability: 1,735 vs 5,081, and the length-circularity risk | | |
| `c8riboseqorf102` and `c11norep1` — what each licenses and forbids | | |
| pLDDT by tier, the length confound, and the 36-of-581 shuffle control | | |
| The transferable rule: a score is evidence only against a matched null | | |

## What I now trust, and why

Write your own. Mine, as a model — positive statements, not a list of things that turned out to be false:

- **I trust that ORF-level constraint on ncORFs is real and common.** Thirty percent against a 10% null, with *P* < 2.3 × 10⁻⁵⁰, from a quantile whose contamination biases it toward *understating* the effect, with per-biotype numerators and denominators that reconcile exactly to the catalogue total. The individual scores are noisy and the aggregate signal is not.
- **I trust that "these ORFs lack constraint" was the wrong summary, and I can say why in one sentence.** The standard test measures selection on amino acids; the hypothesis for most of these ORFs is selection on the reading frame. Two percent by the amino-acid test and thirty percent by the frame test are not in conflict — they are the predicted pattern.
- **I trust ORBL's mechanics because they are stated precisely enough to disagree with.** Any stop counts. Compensating indels preserve frame. Species absent from the local alignment count in the denominator. The background is 1,717,927 ORFs assembled by eight printed rules. I could reimplement this, and I could name the specific choice I would argue about.
- **I trust the authors' handling of their own confounds.** They flag CDS bleed-through as "presumably" the cause of the biotype ordering, they build the `+1`/`+2` split to address it, and they report the residual anyway. They report the aggregate percentage against the larger, less flattering denominator. That is not how people write when they are trying to get away with something.
- **I trust the shuffled-sequence control more than the pLDDT trend it qualifies.** Thirty-six of 581 is a small number honestly obtained, and the authors published it next to the trend it undercuts rather than in place of it.
- **The transferable win is not about evolution at all.** It is that a score without a matched null is a number, not evidence — and that I now have four instances of the same operation across four unrelated domains, which is enough to make it a habit rather than a fact. The first question I will ask of any score from now on is what it was compared against, and whether the comparison set was matched on the thing that would otherwise explain the result.
- **Where I remain uncertain, and the paper is too:** whether absence of amino-acid constraint argues against function at all. That is agenda question 4, it cites the de novo gene-birth literature on both sides (refs 35–37), and the consortium deliberately leaves it open. So do I.

## Sources

Paper anchors above are to the results section "Evolutionary insights to interpret ncORFs"; the Methods subsection "Evolutionary conservation and constraint (ORBL)"; the Discussion; agenda questions 4 and 5; Fig. 4a–i; Extended Data Fig. 7a–f; and Extended Data Fig. 10a–j. Figure-internal numbers were taken from coordinate-ordered extraction and cross-checked for closure — Fig. 4c's six numerators sum to 2,211 and its six denominators to 6,816, and Fig. 4g's twelve *n* values sum to 1,735 and 5,081. Quotations are short and attributed; the article is CC BY-NC-ND 4.0, so nothing is reproduced here and the figure reading has to happen in your own copy.

Two extraction caveats, in case you check my numbers against a text dump of your own. Springer subsets the figure fonts and remaps `≥` and `≤` onto the same control byte in different font runs, so inequality directions inside figure panels cannot be trusted from extracted text — Fig. 4a's matched-set label reads `≥1,000`, agreeing with the Methods' "at least 1,000", even though a naive extraction renders it as `≤`. And the Fig. 6i and Methods statements of the |log2 fold change| cutoffs are set as inline math that does not extract; read those thresholds off the page.

Background primers, retrieved 2 September 2026. `PhyloCSF`'s own documentation, since none of this is in the paper:

- [PhyloCSF wiki, `mlin/PhyloCSF`](https://github.com/mlin/PhyloCSF/wiki) — the two empirical codon models fitted to known coding and non-coding regions; scores in decibans, with "A score of 10 decibans means the coding model is 10:1 more likely than the non-coding model"; and the warning that "low branch length (or low number of substitutions) tends to compress the score towards 0". Also the rationale for `PhyloCSF-Ψ`: it estimates the relative likelihood that a raw score would arise from a coding or non-coding region of a particular length, so that a threshold "meaningful for regions of different lengths" can be set.
- [Lin, Jungreis & Kellis, *Bioinformatics* **27**, i275–i282 (2011)](https://academic.oup.com/bioinformatics/article/27/13/i275/178183) — the paper's ref. 24. The full text was not reachable from this environment; the model description above is from the wiki and from retrieved abstracts, so spot-check it if you lean on the details.
- Reference 83 for the alignment: Hecker & Hiller, *GigaScience* **9**, giz159 (2020), the 120-mammal genome alignment.
- ORBL implementation: `https://github.com/iljungr/ORBL_tools` (the paper's ref. 93, Zenodo `10.5281/zenodo.18749292`).

Further reading is listed under "Module 6 — evolution" in [key references](../resources/key-references.md), including Sandmann *et al.* (ref. 23) for the prior framing and Keeling *et al.* (ref. 37) for the dispute agenda question 4 declines to settle.
