# Module 2 — The ncORF catalogue and its coordinate system

~1.5 hrs. Prerequisite: [Module 1](01-annotation-problem.md). Everything after this module is indexed by biotype, so this is the module that makes the rest legible.

Covers Fig. 1b, the biotype re-derivation in Methods ("Evolutionary insights to interpret ncORFs"), and the two PeptideAtlas builds as a framing for [Module 4](04-mass-spec-proteomics.md) and [Module 5](05-immunopeptidomics.md).

## Predict first

Write these down before reading on.

1. Of 7,264 ncORFs, what percentage sit upstream of a coding sequence — in or overlapping a 5′ UTR? Give a number, not a range.
2. Three of the seven biotypes are defined by overlapping an annotated CDS. Which three, and roughly what share of the catalogue do they hold together?
3. The paper re-derived every ORF's biotype on a newer GENCODE release than the one the catalogue was built with. How many of the 7,264 do you think changed biotype? And can a biotype *gain* members in that re-derivation?
4. `OLMALINC` is annotated `gene_biotype "lncRNA"`. Write down, in one sentence, what you currently believe that field asserts.

## What the catalogue is, and what got you in

The 7,264 are not a discovery of this paper. They are a pre-existing consensus set of non-canonical ORFs supported by GENCODE, assembled by the same consortium's earlier standardisation effort (ref. 4, Mudge *et al.*, *Nat. Biotechnol.* **40**, 994–999, 2022) and distributed by GENCODE as a **phase 1 Ribo-seq ORF** resource, separate from the main annotation (`https://www.gencodegenes.org/pages/riboseq_orfs/`). This paper takes that set as given and asks a different question: which of them make protein.

The entry criterion is ribosome profiling. Every one of the 7,264 is in the catalogue because Ribo-seq evidence placed a ribosome on it. Hold on to that, because it explains a structural oddity of the tier system you will meet in [Module 8](08-tier-framework-synthesis.md): Tier 3 is the only tier requiring Ribo-seq absent, so nothing can *start* there — an ORF reaches Tier 3 only when manual inspection decides the evidence that admitted it does not hold up.

The corollary is what the catalogue is **not**. It is not "all ORFs in the human genome" and not "all short ORFs". For scale, when the ORBL analysis needed a null distribution it enumerated every ATG-initiated ORF of any length in any protein-coding or lncRNA transcript in GENCODE v42 that did not overlap a CDS in the same frame, applied several exclusions — including removing anything overlapping the 7,264 themselves — and was left with **1,717,927** ORFs with no translation evidence (Methods, ORBL). The human transcriptome offers ATG-initiated ORFs by the million; 7,264 is what survives requiring ribosome-profiling support. Any statistic in this paper with 7,264 in the denominator is conditioned on that filter.

## The seven biotypes

A biotype here answers one question: **where does this ORF sit relative to the host transcript and its annotated CDS?** Nothing about the ORF's own sequence enters into it.

Five of the seven are positional, defined against a CDS on the same transcript. In the schematic, `-` is UTR, `=` is CDS, `#` is the ncORF.

```
                   5' UTR                  CDS               3' UTR
transcript   --------------------========================----------------

uORF              ######
uoORF                      ###############
intORF                                       ##########
doORF                                             ###############
dORF                                                         #######
```

- **uORF** — upstream ORF. Starts and stops within the 5′ UTR, entirely ahead of the CDS. **3,083** ncORFs, 42.4% of the catalogue — the single largest class by a wide margin.
- **uoORF** — upstream **overlapping** ORF. Initiates in the 5′ UTR and runs past the CDS start codon, overlapping the CDS out of frame. **688**, 9.5%.
- **intORF** — internal ORF. Contained within the CDS, in a different reading frame from it. **720**, 9.9%.
- **doORF** — downstream **overlapping** ORF. Initiates inside the CDS and terminates past the CDS stop, out into the 3′ UTR. **61**, 0.8% — the rarest biotype by an order of magnitude, and small enough that it is dropped from some analyses for low abundance.
- **dORF** — downstream ORF. Starts and stops within the 3′ UTR, entirely after the CDS. **504**, 6.9%.

The remaining two are not positional at all. They are defined by the **host transcript having no CDS to be positioned against**.

```
lncRNA transcript — no annotated CDS anywhere in the gene
transcript   ------------------------------------------------------------
lncRNA ORF                        ############

processed_transcript — this transcript carries no CDS of its own
transcript   ------------------------------------------------------------
proc. tr. ORF                     ############
```

- **lncRNA ORF** — an ORF on a transcript of a gene annotated as a long non-coding RNA. **1,917**, 26.4% — the second-largest class.
- **processed-transcript ORF** — an ORF on a transcript whose GENCODE transcript biotype is `processed_transcript`, meaning it carries no annotated CDS of its own. **291**, 4.0%.

| Biotype | Count | % of 7,264 | Defined by |
|---------|-------|-------|-------|
| `uORF` | 3,083 | 42.4 | position, 5′ UTR only |
| `uoORF` | 688 | 9.5 | position, 5′ UTR into CDS |
| `intORF` | 720 | 9.9 | position, inside CDS |
| `doORF` | 61 | 0.8 | position, CDS into 3′ UTR |
| `dORF` | 504 | 6.9 | position, 3′ UTR only |
| `lncRNA ORF` | 1,917 | 26.4 | host has no CDS |
| processed-transcript ORF | 291 | 4.0 | host transcript has no CDS |
| **Total** | **7,264** | **100.0** | |

All counts and percentages are from Fig. 1b; the seven counts sum to 7,264 and the seven percentages to 99.9 (rounding). Answer to prediction 1: **51.9%** of the catalogue is upstream — uORF plus uoORF. More than half of everything in this paper lives in a 5′ UTR, which is a fact worth carrying into every later module.

A caveat on the geometry above. This paper expands the abbreviations (Fig. 1b caption; the ORBL section names uoORFs, intORFs and doORFs as "biotypes that overlap annotated CDSs") and it establishes that the three overlapping classes overlap the CDS out of frame — but the precise positional criteria come from the nomenclature paper, ref. 4, which I could not retrieve. Treat the *names*, the *counts*, and *which three overlap a CDS* as sourced from this paper; treat the exact UTR boundaries in my schematic as the standard reading of those names — `unverified` against this text.

The two host-biotype classes deserve one more beat, because the asymmetry has a consequence. Five biotypes are statements about a *coordinate relationship*; two are statements about *what the annotation happens to contain*. `lncRNA ORF` does not mean "this ORF is non-coding" — it means "no CDS has been annotated on this gene, so there is nothing to position the ORF against". That is a fact about the reference, not about the molecule, and it is the whole subject of the last section of this module.

## Why the overlapping three need a reading frame

For a uORF or a dORF, the biotype is the whole story: the ORF occupies sequence that no protein uses. For a uoORF, intORF or doORF, the ORF shares nucleotides with a CDS, and then a second coordinate becomes mandatory — **which frame**.

An ORF overlapping a CDS *in* frame is not a separate ORF at all; it is an alternative start or a truncation of the same protein. The ORBL Methods make this definitional: the untranslated-ORF universe was built from ORFs "that did not overlap a protein-coding CDS of any transcript in the same frame". So the overlapping biotypes are always at a shift of +1 or +2 relative to the host CDS, never 0.

Why the shift matters, on eighteen nucleotides you can check by hand:

```
nucleotides   A T G G A A C T G A A G C G T T A C
frame  0      [ATG] [GAA] [CTG] [AAG] [CGT] [TAC]
frame +1        [TGG] [AAC] [TGA]
frame +2          [GGA] [ACT] [GAA] [GCG] [TTA]
```

Frame 0 is the host CDS. Frame +1 hits `TGA` at its third codon and closes. Frame +2 stays open across the whole window. The same nucleotides support an ORF in one shifted frame and not the other, and which one stays open is entirely determined by the host protein's codon choices. That is the mechanism the Methods are pointing at when they say the frames must be handled separately:

> We segregated uoORFs, intORFs and doORFs by the frame in which they overlapped the main ORF (+1 or +2) as constraint on the main frame amino acid sequence imposes different ORFness constraint on the two overlapping frames.

(The paper states that the two frames receive different ORFness constraint. That purifying selection on the host protein's residues constrains synonymous wobble positions asymmetrically across the two shifted frames is my gloss on why — `unverified`.)

The consequence in the Methods is visible in the matched-null counts, which are given per frame: `uoORF+1` 3,231 versus `uoORF+2` 2,940; `intORF+1` 320,823 versus `intORF+2` 60,135; `doORF+1` 16,910 versus `doORF+2` 5,946. Note `intORF+1` outnumbers `intORF+2` more than fivefold. Two ORFs at the same coordinates in different shifts are drawn from populations that differ by a factor of five in size, so their null distributions cannot be shared.

This overlap does two kinds of damage downstream, and both are things you should be primed to look for.

### For evolutionary inference

Sequence inside a CDS is under purifying selection to preserve the *protein*, and that selection incidentally keeps codons intact in the shifted frames too. So an intORF gets conservation for free, from constraint that has nothing to do with the intORF. The paper observes exactly this: ncORFs with biotypes that overlap annotated CDSs "have higher ORBLv scores, presumably due to constraint to preserve the CDS" (ORBL section), and the Extended Data Fig. 7b,c caption calls it "'free' conservation from the CDS". This is precisely the confound that motivates the ORBLv/ORBLq distinction — [Module 6](06-evolution-orbl.md) is where it gets resolved rather than merely flagged.

### For CRISPR specificity

A guide RNA cutting an intORF also cuts the host CDS. There is no way to perturb the ncORF without perturbing the protein, so an essentiality signal at an intORF is uninterpretable on its own. Watch how the paper handles this, because it is careful:

- Fitness effects were normalised to separate the signature of the associated canonical CDS from that of the ncORF, "only for ncORFs shown to be co-transcribed with a canonical ORF" (Methods, CRISPR tiling analysis).
- The significance test is a **gene-specific permutation** null: "For each ncORF with *n* guides, we generated null distributions by resampling *n* guides from all guides targeting the same parental gene." The comparison is against the host gene's own background, not a genome-wide background.
- Fig. 6b plots loss of fitness from perturbing the annotated CDS and the ncORF as separate series, so the reader can see the two apart.
- For uORFs specifically, the authors "ensured that the phenotypic effect of uORF knockout was distinct from that of the adjacent coding region", and used CRISPRa data from a matching cell line to rule out the alternative explanation that uORF knockout is toxic because it de-represses an anti-proliferative downstream CDS (Extended Data Fig. 9e,f).
- sgRNAs mapping to more than five genomic loci were excluded, and ORFs with fewer than three guides dropped (Methods, meta-analysis of CRISPR data).

Note that all five of those controls exist *because* of biotype geometry. Biotype is not bookkeeping; it determines which experiments can even be interpreted. [Module 7](07-function-crispr-olmalinc.md) works this through.

## The 448 'mixed' ORFs, and why later analyses run on 6,816

Because the evolutionary analysis turns on CDS overlap, the authors did not accept the catalogue's biotypes as given. From the Methods:

> As our analysis of evolutionary constraint is strongly influenced by overlap with CDS, we redid the biotype determination for the ncORFs using GENCODE v42 annotations (the original biotypes from ref. 4 used v35), and applied strict criteria to determine ORFs with a 'pure' biotype. […] There were 448 of the 7,264 ncORFs that did not satisfy any of these criteria, for example, ORFs that overlapped CDS from two different transcripts in different reading frames; we considered these to have 'mixed' biotype and did not compute an ORBLq constraint score for them.

Read the example closely, because it is the general case in miniature. A gene has several transcripts. An ORF can be an intORF with respect to one transcript's CDS and a uoORF with respect to another's, in a different frame. There is no single frame relationship, so there is no single matched null population, so **ORBLq is undefined** — not low, not zero: undefined. The 448 are excluded rather than scored, and `7,264 − 448 = 6,816` is the denominator you will meet throughout [Module 6](06-evolution-orbl.md): Extended Data Fig. 7f compares 1,735 HLA-detected against 5,081 undetected ncORFs, and `1,735 + 5,081 = 6,816`.

Three different denominators appear in this paper for three different reasons. Keep them straight:

| Denominator | What was dropped | Why | Where |
|---------|-------|-------|-------|
| 7,264 | nothing | the whole catalogue | throughout |
| 6,912 | doORFs (61), processed-transcript ORFs (291) | too few members for a per-biotype curve | Fig. 3b |
| 6,816 | 'mixed' biotype ORFs (448) | ORBLq is undefined without a single frame relationship | Fig. 4b–g, Extended Data Fig. 7f |

`7,264 − 61 − 291 = 6,912` and `7,264 − 448 = 6,816`. If you see a figure with a denominator you cannot place, the exclusion is the interesting part.

## The re-derivation moved ORFs in both directions

This is the concrete form of Module 1's claim that annotation versions are not interchangeable, and it is worth doing the arithmetic yourself because the paper never puts it in one place.

Fig. 1b gives the biotype counts as the catalogue supplies them, from GENCODE v35. Fig. 4c gives the per-biotype denominators after re-derivation on v42, printed on the bars as `n = X/Y` fractions. Same 7,264 ORFs, two coordinate systems:

| Biotype | Fig. 1b (v35) | Fig. 4c (v42, pure only) | Change |
|---------|-------|-------|-------|
| `uORF` | 3,083 | 2,915 | −168 |
| `uoORF` | 688 | 622 | −66 |
| `intORF` | 720 | 743 | **+23** |
| `doORF` | 61 | 64 | **+3** |
| `dORF` | 504 | 460 | −44 |
| `lncRNA ORF` | 1,917 | 2,012 | **+95** |
| processed-transcript ORF | 291 | — (no class) | −291 |
| **Total** | **7,264** | **6,816** | **−448** |

The v42 column sums to exactly 6,816, and the changes sum to exactly −448. Three biotypes **gained** members. That settles a question the numbers alone invite: the drop from 3,083 uORFs to 2,915 is **not** simply "the mixed ones were removed", because a pure removal cannot make `intORF`, `doORF` or `lncRNA ORF` grow. Two things happened at once and the published text does not separate them:

- the v35 → v42 release change altered host transcript models, so ORFs moved *between* biotypes; and
- the strict 'pure' criterion moved 448 net out to `mixed`.

So the honest statement is: **168 fewer uORFs, for both reasons combined, in unstated proportions.** Do not attribute it to either alone. (The `mixed` class has no published per-biotype breakdown; the detailed 'pure' criteria are in the Supplementary Results, which I did not have.)

One clean structural observation does fall out. The ORBL scheme has no processed-transcript class at all — its nine matched-null classes are `uORF`, `uoORF+1/+2`, `intORF+1/+2`, `doORF+1/+2`, `dORF` and `lncRNA-ORF` — so all 291 processed-transcript ORFs are outside it, and therefore inside the 448. Which means at most `448 − 291 = 157` ORFs are excluded for the two-transcripts-two-frames reason the Methods give as their example. The headline exclusion criterion accounts for a minority of the exclusions; the rest is a biotype that simply has no home in the newer scheme. (That decomposition is my arithmetic from the two figures, not a statement the paper makes.)

Two reconciliations that let you trust the table above, both worth running yourself as an exercise in figure hygiene. Fig. 4c's numerators — 1,335 + 243 + 231 + 12 + 79 + 311 — sum to **2,211**, exactly the paper's "2,211 of the 7,264 ncORFs (30.4%)" with placental-mammal ORBLq > 0.9. And Fig. 4g's detected-versus-undetected pairs sum, biotype by biotype, to Fig. 4c's denominators: 759 + 2,156 = 2,915; 218 + 404 = 622; 247 + 496 = 743; 21 + 43 = 64; 62 + 398 = 460; 428 + 1,584 = 2,012. Two independent panels agreeing on all six denominators is what "this number reconciles" looks like.

## Two windows onto one catalogue

Fig. 1b is laid out as a triptych for a reason: the biotype barplot sits in the middle, flanked by the two PeptideAtlas builds that interrogate it. Those are the two windows, and they are not the same instrument pointed twice.

| | Non-HLA build 2023-06 | HLA build 2023-11 |
|---------|-------|-------|
| **Sample type** | protein digests | HLA immunopeptidome enrichments |
| **ProteomeXchange datasets** | 295 | 118 |
| **MS runs** | ~85,000 | ~10,000 (9,776) |
| **MS/MS spectra** | 3.5 billion | 240 million |
| **PSMs** | 573 million | 28 million |
| **Search mode** | protease-specific (semi-enzymatic) | **no-protease** |
| **PeptideAtlas experiments** | 1,172 | 592 |
| **ncORFs detected** | 183 (2.5%) | 1,785 (24.6%) |

Dataset, run, spectrum and PSM counts are from Fig. 1b; experiment counts, the exact 9,776 runs and the search modes from Methods ("PeptideAtlas database construction and searching"); the detection counts from the main text.

Three things to notice now, so Modules 4 and 5 have somewhere to attach.

**The search mode is the whole difference.** The non-HLA build searches with protease-specific settings, because you know where trypsin cut. The HLA build searches in **no-enzyme mode**, because a proteasome does not cut at K or R — the paper notes that HLA peptides often lack the C-terminal lysine or arginine that gives tryptic spectra their strong y-ion series, so their spectra are dominated by b ions and internal fragments instead. A no-enzyme search over 240 million spectra is a vastly larger search space than an enzyme-constrained one, which is why the FDR discipline in Module 4 is not optional.

**The windows barely overlap, and you can prove it from the figures.** Fig. 3a gives non-canonical ORFs as detected `n = 1,867` and undetected `n = 5,397` — which sum to 7,264, so 1,867 is the union of the two builds. Then:

```
183 (non-HLA)  +  1,785 (HLA)  −  1,867 (union)  =  101 seen by both
```

One hundred and one ncORFs of 1,867. Every later argument in this paper about why MS and HLA get separate columns in the tier table descends from that number. [Module 5](05-immunopeptidomics.md) is where it earns its keep.

**The abstract's "95,520 proteomics experiments" is a third sense of the word.** In the Methods, "experiment" means a PeptideAtlas experiment — 1,172 plus 592, so 1,764 of them. The abstract's 95,520 matches the *MS run* totals instead: 9,776 HLA runs, leaving 85,744 for the non-HLA build, consistent with Fig. 1b's rounded 85,000. (That subtraction is mine; the non-HLA run count is not printed exactly.) The number is fine; the word is overloaded three ways in one paper. Say "MS runs" when you mean runs.

## What `gene_biotype = lncRNA` actually asserts

Back to prediction 4, and to Module 1's example.

`OLMALINC` is `ENSG00000235823`, annotated `lncRNA` (Fig. 6e). It carries **six** GENCODE-recognised ncORFs. One of them, `c10riboseqorf92`, is a 123-amino-acid ORF that is HLA-detected, pan-essential in 415 of 485 cell models, and whose coding sequence rescues the loss-of-viability phenotype caused by knocking down the transcript. As of this paper it has a **peptidein** annotation. The gene's biotype is still `lncRNA`.

So here is what that field asserts and does not assert.

`gene_biotype "lncRNA"` asserts: **no CDS has been annotated on any transcript of this gene, in this release of this annotation.** That is all.

It does not assert that the locus is untranslated. It does not assert that no polypeptide is made. It does not assert that the gene's function is RNA-mediated. And after this paper, for `OLMALINC`, all three of those readings are wrong: it is translated, a polypeptide is made, and the phenotype is rescued by the ORF rather than the RNA.

There is a second, subtler point. `lncRNA` is a **gene-level** field, and 1,917 of the 7,264 ncORFs — 26.4% — are lncRNA ORFs, with `OLMALINC` alone supplying six. So the mapping is not one ORF per lncRNA gene, and there is no gene-level field that could carry the information even if a curator wanted it to. In your GTF, `OLMALINC` is one feature with one biotype. The six ORFs are not features. Nothing about the count matrix you get back from Cell Ranger would tell you they exist.

Which is the practical residue of this module. The 7,264 ncORFs **are already in your reference** — their host transcripts are, at any rate — but not as `protein_coding`, not as separate features, and not with symbols. When you report "this lncRNA is differentially expressed", you are reporting a change at a locus that may carry up to six translated ORFs, one of which may be doing the work. That is not a criticism of the measurement. It is a limit on what the measurement can mean, and it is set by the annotation, not by the assay.

## What I now trust, and why

Write this in your own words before moving on. Some anchors:

- **Biotype is a coordinate relationship, not a property.** Five of the seven biotypes describe where an ORF sits relative to a CDS; two describe the absence of a CDS to sit relative to. Once I know an ncORF's biotype I know which analyses can be interpreted for it and which are confounded, before I see any data.
- **More than half the catalogue is upstream.** 3,083 uORFs plus 688 uoORFs is 51.9%. Whatever ncORFs are, they are predominantly a 5′-UTR phenomenon, and that shapes every downstream expectation — including the paper's own suggestion that the excess of constrained uORFs and uoORFs points to a large population of conserved regulatory upstream ORFs.
- **Overlapping a CDS is a confound with a known direction.** It inflates conservation (the host CDS is constrained regardless of the ncORF) and it destroys CRISPR specificity (a cut is a cut in both). The paper handles both with specific, checkable controls — per-frame null sets, gene-specific permutation nulls, CDS-versus-ncORF fitness plotted separately, CRISPRa checks for de-repression.
- **`mixed` means undefined, not zero.** 448 ORFs have no single frame relationship to a CDS and therefore no matched null population, so ORBLq cannot be computed. Excluding them is the correct choice, and it is why 6,816 rather than 7,264 appears in the evolutionary figures.
- **The same ORFs re-typed on a newer release do not land in the same biotypes** — 448 net out to `mixed`, and three biotypes gain members. Two effects are superimposed and the paper does not separate them, so I will not either.
- **Numbers in this paper reconcile, and I checked.** Seven biotypes sum to 7,264; six re-derived biotypes sum to 6,816; Fig. 4c numerators sum to 2,211; Fig. 4g pairs sum to Fig. 4c denominators biotype by biotype. That is a well-kept ledger, and it is the reason I am willing to trust the numbers I did not check.
- **`gene_biotype "lncRNA"` is a statement about my reference, not about the molecule.** It means no CDS has been annotated here in this release. `OLMALINC` is the counterexample I will reach for whenever someone reads that field as a mechanistic claim.

## Self-check

- [ ] Draw all seven biotypes from memory as a schematic, and state each count to the nearest hundred
- [ ] Explain why an ORF overlapping a CDS in frame 0 is not an ncORF at all
- [ ] Given an intORF at +1 and one at +2 with identical ORBLv, explain why their ORBLq values are not comparable across a shared null
- [ ] Name the five controls the paper uses to keep a CRISPR hit at an overlapping ncORF interpretable, and say which one you would trust least
- [ ] State what `mixed` biotype means, why ORBLq is undefined for it, and reproduce `7,264 − 448 = 6,816`
- [ ] Explain why the drop from 3,083 to 2,915 uORFs cannot be attributed to the mixed-biotype exclusion alone, using one number from the table
- [ ] Derive the 101-ncORF overlap between the two builds from Fig. 3a and the two build totals
- [ ] Write one sentence stating what `gene_biotype "lncRNA"` asserts, and one stating three things it does not

## Progress

| Concept | Understood? | Notes |
|---------|-------------|-------|
| The seven biotypes and their counts | | |
| Positional versus host-biotype classes | | |
| Reading frame in the overlapping biotypes | | |
| Free conservation from an overlapping CDS | | |
| CRISPR specificity at overlapping ncORFs | | |
| `mixed` biotype and the 6,816 denominator | | |
| Biotype instability across GENCODE releases | | |
| What `gene_biotype` does and does not assert | | |

Next: [Module 3 — Ribo-seq as the bridge](03-riboseq-bridge.md). Terms are collected in the [glossary](glossary.md).
