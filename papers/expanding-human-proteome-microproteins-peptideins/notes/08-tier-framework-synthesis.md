# Module 8 — The tier framework and what it commits you to

~2 hrs. Prerequisites: [Module 3](03-riboseq-bridge.md), [Module 4](04-mass-spec-proteomics.md), [Module 5](05-immunopeptidomics.md), [Module 6](06-evolution-orbl.md), [Module 7](07-function-crispr-olmalinc.md). This module integrates all of them, and it will not work if you take it early — a tier system is unreadable until you can independently judge each axis of evidence it combines.

Covers Fig. 5 in full, the seven research-agenda questions, and the Discussion.

## Predict first

Write these down before reading on. You have now met every kind of evidence the paper collects.

1. Of 7,264 ncORFs, how many do you think ended up in the top tier — the one meaning "this looks like a protein"? Give a number, not a range.
2. Of those, how many do you think GENCODE actually annotated as protein-coding genes?
3. Manual inspection sits between the provisional and final tier assignment. Does it move more ncORFs up or down?

Keep your three numbers visible. The gap between them and the real ones is the lesson.

## Why a tier system at all

By this point you have three evidence types that do not share a currency. Ribo-seq says a ribosome was there. Tryptic mass spectrometry says a peptide of a certain length was sequenced, subject to a standard written for large proteins. HLA immunopeptidomics says a fragment reached the cell surface, having been through the proteasome. ORBL says a reading frame has been kept open across mammals. A CRISPR screen says a locus matters to a cancer cell line.

None of these converts into the others, and none of them is "protein-coding gene". That is the problem Fig. 5 solves. The tier system is not a summary of the data — it is a **decision procedure** that makes incommensurable evidence comparable enough to act on, while keeping each axis visible rather than collapsing them into a single score.

That design choice is the reason the table has separate MS and HLA columns instead of one "proteomics" column. As [Module 5](05-immunopeptidomics.md) works through, the two windows find very different ncORFs — the HLA build reaches 1,785 while tryptic MS reaches 183, of which 66 survive inspection. A framework that merged them into one "proteomics" score would hide its own most important structural finding.

## The six tiers

The evidence signature, with the column order as printed in Fig. 5a. In the paper's notation `+` denotes detection, `++` abundant detection, `±` either presence or absence of detection, and `−` absence of detection.

| Tier | Ribo-seq | MS | HLA | Category |
|---------|-------|-------|-------|-------|
| 1A | + | ++ | ± | Candidate protein |
| 1B | + | − | ++ | Presented |
| 2A | + | + | ± | Detected |
| 2B | + | − | + | Detected |
| 3 | − | ± | ± | Putative |
| 4 | + | − | − | Ribo-seq ORF |

The glyphs are compact but opaque, and the Methods give the operational version — which is far more useful, and which reveals that `++` and `+` are about **peptide count**, not abundance. Quoted from "Use of the tier classification system":

- **Tier 1A** — two non-nested peptides in MS proteome data, with or without HLA immunopeptidomics data, with Ribo-seq data
- **Tier 1B** — two non-nested peptides in HLA immunopeptidomics data, with Ribo-seq data
- **Tier 2A** — one peptide in MS proteome data, with or without HLA immunopeptidomics data, with Ribo-seq data
- **Tier 2B** — one peptide in HLA immunopeptidomics data, with Ribo-seq data
- **Tier 3** — any HLA immunopeptidomics and/or tryptic proteome LC–MS/MS evidence *without* Ribo-seq evidence
- **Tier 4** — Ribo-seq evidence without proteomic evidence
- **Tier 5** — in silico prediction of an ORF on an expressed transcript, without any Ribo-seq or proteomic evidence

So `++` = two non-nested peptides, `+` = one peptide, `±` = with or without, `−` = absent. Note that Fig. 5a's caption glosses `++` as "abundant detection", which is looser than the Methods' "two non-nested peptides" — prefer the Methods wording, because the two-peptide threshold is what connects the tiers to the HUPO-HPP rule.

Note also **Tier 5**, which Fig. 5a does not show. Say "six tiers as figured, seven as defined" — a small thing, but the kind of detail that signals you read past the figure.

And one piece of provenance worth having: the tier system was **not invented in this paper**. The Methods state it was "initially proposed previously" in reference 25 — Prensner *et al.*, *Mol. Cell. Proteom.* 2023, "What can ribo-seq, immunopeptidomics, and proteomics tell us about the non-canonical proteome?", by one of this paper's corresponding authors. What is new here is applying it at catalogue scale, adding the provisional-versus-final distinction, and coupling it to the protein/peptidein annotation decision. If someone asks "what's actually new?", the tier concept is not the right answer.

Read the table as a set of claims of decreasing strength, and notice three things.

**Tier 3 is the odd one out.** It is the only row requiring Ribo-seq `−` — its definition is *any* proteomic evidence **without** Ribo-seq support. Every one of the 7,264 ncORFs is in the catalogue *because* it has Ribo-seq support, so nothing can start in Tier 3. It can only be reached by demotion, when manual inspection decides the Ribo-seq evidence does not hold up. Tier 3 is where ORFs go when the ground floor gives way. That is why its provisional count is zero.

**Tiers 2A and 2B share a name but not a basis.** Both are "Detected". 2A means tryptic MS saw it; 2B means only HLA saw it. The paper deliberately declines to rank these against each other, which is agenda question 2 in table form.

**One axis is much less verified than the other two.** Every tier except 3 requires Ribo-seq `+`, which makes Ribo-seq the load-bearing column — and it is the column that received the least independent scrutiny in this work. Manual Ribo-seq inspection covered 183 ncORFs from the non-HLA build and 699 from the HLA build. The remaining roughly 6,400 carry their Ribo-seq `+` inherited from the source catalogue without re-inspection here. The paper is not hiding this — it reports exactly what it inspected — but if you are asked which axis of the table you trust least, this is the answer, and it is not the answer most readers would guess.

**Tier 1B has no MS evidence at all.** "Presented" is a real category with abundant HLA support and no tryptic peptides. Under the pre-existing standard this ORF would have had nothing. This tier exists because the consortium decided HLA data says *something* — while stopping short of saying it says "protein".

## Provisional versus final: what manual inspection does

Provisional tiers are assigned computationally by integrating the three data types. Then a human being looks at every spectrum and every Ribo-seq track and assigns a final tier. Here is what that costs.

| Tier | Provisional | Final |
|---------|-------|-------|
| 1A | 37 | 16* |
| 1B | 665 | 601 |
| 2A | 146 | 39 |
| 2B | 1,063 | 1,059 |
| 3 | 0 | 90 |
| 4 | 5,353 | 5,457 |
| Other | — | 2 |
| **Total** | **7,264** | **7,264** |

`*` The asterisk is the paper's own, and it matters: it flags the inclusion of one likely pseudogenic sequence. Even the final top tier carries a known bad entry, labelled as such.

Manual inspection is **net-demoting, and dramatically so in the tiers that matter**. Tier 4 — Ribo-seq only, no protein evidence — *grows* by 104. Tier 2A loses nearly three-quarters of its members, 146 down to 39. Tier 1A drops from 37 to 16. The only tier that grows other than Tier 4 is Tier 3, from nothing to 90, which is entirely composed of demotions.

If you predicted that human review would promote borderline cases, that is the belief to revise. Automated integration of three noisy evidence types is systematically optimistic, and the correction is large. This is the same lesson as [Module 4](04-mass-spec-proteomics.md)'s base-rate problem, arriving from a different direction: a low global error rate does not protect the small, low-prior subset you actually care about.

## From tier to annotation: protein or peptidein

Tier is not annotation. Tier describes evidence; annotation is a decision about what to put in a public database. Fig. 5d sets out the two destinations.

**Candidate protein** requires all three of:

- detection meeting HUPO-HPP criteria — ≥2 **non-nested** non-HLA peptides of ≥9 aa, together spanning ≥18 aa of the ORF
- presence in healthy cells
- evidence of function

**Candidate peptidein** requires none of those. Detection need not meet HUPO-HPP criteria, may come from normal *or* cancer cells, and function may be unknown or absent.

"Non-nested" is load-bearing and easy to skim past: the paper defines it as "neither contained completely within the other", so two peptides where one sits inside the other are **one** piece of evidence, not two.

The peptidein class exists precisely because the first list is unreachable for most of this catalogue, for reasons that are not about biology. Agenda question 1 makes the arithmetic explicit: 28.3% of these ncORFs — 2,059 of 7,264 — are shorter than 25 amino acids, so two non-nested 9-mers covering 18 residues is close to geometrically impossible. A standard written for large proteins does not merely disadvantage microproteins; for a large fraction of them it cannot be satisfied at any depth of sequencing.

The paper supplies the control experiment for that claim, and it is decisive: taking a manually curated set of small GENCODE proteins — molecules already accepted as real — **only 2 of 36 known proteins under 50 amino acids (5.6%) satisfy the benchmarks for HUPO-HPP verification.** So the standard fails 94% of small proteins we already believe in. Any inference from "does not meet HUPO-HPP criteria" to "probably is not a protein" is therefore unsound for short sequences, and that single number is the strongest thing you can say in defence of the peptidein class.

There is also a structural ceiling above all this, easy to miss. PeptideAtlas awards the status `canonical` only to entries in the core proteome. An ncORF that clears the two-peptide bar with peptides that cannot be mapped to the core proteome is instead termed **`non-core canonical`** — a distinct, lesser category. So no ncORF can become `canonical` in PeptideAtlas regardless of how good its evidence gets. That is a *definitional* barrier rather than an evidentiary one, and it is worth separating from the biology when you discuss what would have to change.

One clean illustration of why annotation versions are not interchangeable, since it comes up the moment anyone compares Fig. 1b with Fig. 4: the ORBL analysis re-derived biotypes on GENCODE v42 while the catalogue was built on v35. The v42 per-biotype counts sum to 6,816, and the differences against Fig. 1b sum to exactly −448 — which looks like a clean subtraction of the mixed-biotype ORFs, except that the intORF, doORF and lncRNA ORF counts all *increase*, and no pure exclusion can do that. So the shortfall is transcript remodelling between versions and the pure-biotype criterion superimposed, in proportions the paper never states. Never put a Fig. 1b count and a Fig. 4 fraction in the same sentence.

Note also which ORFs were even *eligible* for review: per Fig. 5e, only Tier 1A and Tier 2A ncORFs, plus Tier 1B ncORFs detected by ≥5 HLA peptides, were considered for manual validation. The 77 ncORFs entering by that HLA route are there because of an explicit consortium judgement that abundant HLA evidence deserves a look.

The outcome was **121 initial peptidein annotations** (Supplementary Table 12), composed of 12 + 72 + 34 + 3 — drawn respectively from Tier 1A candidates not annotated as protein, the ≥5-HLA-peptide group, Tier 2A, and three separately prioritized ncORFs.

## The funnel: 37 → 3

This is the paper's most quotable sequence and its most misread. Follow it.

**37** ncORFs are provisionally Tier 1A → after manual inspection of the MS evidence, **20** are confirmed → further scrutiny reduces this to **15** prioritized for potential annotation → GENCODE has so far annotated **3** as protein-coding genes.

The losses happen in three distinct stages, and conflating them is the usual mistake. Stage one takes 37 to 20: seventeen ncORFs had insufficient MS evidence on inspection and were redistributed downward — 2 to Tier 1B, 7 to Tier 2A, 1 to Tier 2B, 7 to Tier 4. Then:

**20 → 15**, four reasons totalling five ORFs:

- **likely pseudogenic insertion** (n=2)
- **downgraded to Tier 3** on insufficient Ribo-seq evidence (n=1)
- **a novel CDS isoform** (n=1) — real, but not a new gene
- **a miscalled CDS caused by a GRCh38 assembly error** (n=1) — the reference genome itself was wrong

**15 → 3**, two reasons totalling twelve ORFs:

- **unclear evolutionary constraint beyond primates** (n=2)
- **high-quality peptide evidence only from cancer or cell-line samples** (n=10)

Both stages reconcile exactly: 2 + 1 + 1 + 1 = 5, and 2 + 10 = 12. That last number dominates. Two-thirds of the losses at the final stage were not about whether the protein exists — they were about *where it was seen*. Which is agenda question 3, and which follows directly from the sampling fact you met in [Module 5](05-immunopeptidomics.md): 2.36 of 3.53 billion non-HLA MS2 spectra, 66.9%, come from cancer tissue or cancer cell lines. The world's proteomics data is mostly cancer data, so a healthy-tissue requirement gates annotation on a minority of available evidence.

The three that made it: `c12norep105` in CYP27B1, `c21norep46` in ERVH48-1, and `c11riboseqorf4` in PIDD1. A fourth, `c2riboseqorf47` (the GMCL1 uORF), was promoted via the route described in [Module 7](07-function-crispr-olmalinc.md) — on ORBL constraint, CRISPR evidence and HLA support, with no tryptic peptides at all.

Be careful saying "three genes", because there is a second set of three. Separately from this funnel, GENCODE had *already* annotated three Tier 1B ncORFs as protein-coding on the basis of their evolutionary profiles: uoORF `c14riboseqorf117` in EIF5, uORF `c1riboseqorf55` in PTP4A2, and uORF `c3riboseqorf98` in CGGBP1. Those are prior annotations this work inherited, not products of it. When you quote the number, say which three you mean.

Look hard at `c11riboseqorf4`. It is a **171-amino-acid** uoORF, and its peptides appear in non-malignant tissue, cancer samples *and* cell lines. It is the best-detected ncORF in the entire tryptic dataset, with 11 distinct peptides. It is also, at 171 aa, well above any conventional microprotein size cutoff — and that is *why* it was detectable. Size is a determinant of detection (Fig. 3). The catalogue's most convincing member is its least typical member. Any intuition you form about microproteins from this example will be wrong about the other 7,263.

## Putting the numbers together

Here is the synthesis the paper never states in one place. You should be able to reconstruct this table unaided.

| Evidence source | ncORFs | Share of 7,264 |
|---------|-------|-------|
| **HLA immunopeptidomics — the paper's own stated figure** | **1,785** | **24.6%** |
| HLA build, under Fig. 3a's permissive peptide assignment | 1,867 | 25.7% |
| Tryptic (non-HLA) MS — detected | 183 | 2.5% |
| Tryptic MS — *surviving manual inspection* | 66 | 0.9% |
| Final Tier 1A | 16 | 0.22% |
| Peptidein annotations | 121 | 1.7% |
| **New protein-coding genes** | **3** | **0.04%** |
| *Canonical proteins, same HLA panel* | *15,581 of 20,326* | *76.7%* |

Before reading on, note carefully what is **not** in that table: a union across the two builds, and the overlap between them. It is tempting to compute both, and the temptation should be resisted.

Here is why. Fig. 3a reports 1,867 detected ncORFs against 5,397 undetected, which sums neatly to 7,264 and looks like a cross-build union. It is not — or at least, the paper gives you no way to say that it is. Fig. 3 is titled "Determinants of ncORF peptide detection **in the HLA build**", and the Methods for that analysis state that "contrary to most other analyses, peptides were not exclusively assigned to a single ncORF, due to which the number of detected ncORFs was larger than in Extended Data Fig. 4b". So the excess of 1,867 over 1,785 is attributed to *ambiguous peptides being counted against more than one ncORF within the HLA build* — not to adding the tryptic build. Two quite different quantities could both print as 1,867.

**The paper never reports the cross-build union, and never reports how many ncORFs both windows saw.** Recovering either would require the per-ncORF detection lists in the supplementary tables, which are not in the article PDF. The nearest thing the paper does state, in agenda question 2, is that the 1,785 include **24 ncORFs with one peptide in tryptic MS data** suitable for potential annotation. If someone asks you at journal club how much the two windows overlap, the correct answer is that this paper does not say, and that the prior literature — reference 19, whose title is that most non-canonical proteins uniquely populate either the proteome or the immunopeptidome — suggests the answer is "not much".

That caution costs you nothing, because the structural point does not depend on it.

Two rows deserve a second look. Tryptic MS detected 183 ncORFs, but only **66** survived manual inspection — the split is 30 of 42 ncORFs with multiple peptides versus just **36 of 141** with a single peptide (Fig. 2c–d). A 26% survival rate for single-peptide evidence is the paper's own empirical case for why HUPO-HPP demands two peptides.

Be careful how you phrase what happened to the other 117, because the obvious phrasing is wrong. They were not all shown to be false. The manual verdict categories are `excellent`, `good`, `false positive`, `close but false positive` and `low information`, and only two of those five assert the identification is *incorrect* — `good` and `low information` assert that the evidence is insufficient **for annotation purposes**, which is a weaker and different claim. So the 64% rejection rate is a failure-to-meet-the-bar rate, and it is an *upper bound* on the ncORF-subset false discovery rate rather than an estimate of it. The actual subset FDR estimates live in Supplementary Tables 15 and 16, which are not in the article PDF. [Module 4](04-mass-spec-proteomics.md) works through this properly.

When you quote a tryptic number, say which one you mean — and say whether you mean "not detected", "not annotation-grade", or "shown to be wrong".

Read down that column and the paper's real shape appears. The abstract's "about 25%" is the HLA number: the paper itself writes 1,785 of 7,264 as 24.6%. Conventional tryptic proteomics — the method whose standard defines "Candidate protein" — reached 2.5% before curation and **0.9%** after it. So the headline rests on a proteasome-output assay, while the evidentiary bar is written for the assay that found under one percent.

The cleanest single comparison in the paper is hiding in that last row, and it is an apples-to-apples one. Fig. 3a puts ncORFs and canonical proteins in the *same panel of the same HLA build*, scored the same way: canonical proteins are detected at 15,581 of 20,326, or 76.7%, against roughly a quarter for ncORFs. Same assay, same peptide-assignment rule, same spectra — a threefold gap. That comparison tells you how much of the shortfall is assay physics and ORF length rather than biology, and it is far more informative than comparing across builds.

Detection then falls by more than two orders of magnitude between "a peptide was seen" and "a gene was annotated": 1,785 → 16 in the top tier → 3 gene records.

### Numbers that do not reconcile, and why that is fine

Try to make the tier counts agree with the detection counts and you will fail. Add the final tiers that require some proteomic evidence — 16 + 601 + 39 + 1,059 + 90 + 2 — and you get **1,807**. The provisional equivalents give **1,911**. Fig. 3a's detected set is **1,867**, and the HLA build's own exclusive count is **1,785**. Four numbers for what sounds like one quantity.

They differ for two reasons, and this is my reading rather than a statement in the paper. First, peptide-to-ORF assignment is *exclusive* in the tier bookkeeping but *non-exclusive* in the Fig. 3 detectability analysis, so a peptide mapping to several ncORFs is counted differently in the two places. Second, and larger: 1,867 counts detections as nominated, while final tiers are assigned after manual spectral review — so an ncORF whose only peptide failed inspection keeps no proteomic tier and lands in Tier 4. That mechanism also accounts for Tier 4 growing by 104.

The lesson is not that the paper is sloppy. It is that "detected" is not one thing in a study this size — it means something different before and after curation, and something different again depending on how ambiguous peptides are assigned. When you quote a number from this paper, name the bookkeeping. A journal club that catches you conflating 1,785, 1,807, 1,867 and 1,911 will be right to — and note that none of the four is a union across the two builds, which the paper never reports.

None of that makes the paper weak. It makes the paper's thesis legible: **3 of 7,264 is the finding**, not a disappointing result. The contribution is a defensible procedure for getting from billions of spectra to a handful of gene records you would be willing to defend, plus a new category — peptidein — for the enormous middle ground the old binary could not represent.

## The seven open questions

The paper closes with seven questions the consortium explicitly declines to answer. Treat these as live policy disputes with named stakeholders, not rhetorical flourishes. Each one is a place where the framework you just learned could change.

1. **Are HUPO-HPP guidelines suitable for ncORF-encoded microproteins?** Two peptides ≥9 aa spanning ≥18 aa — against 28.3% of ncORFs being under 25 aa.
2. **Should HLA immunopeptidomics count as evidence of a protein-coding gene?** 1,785 of 7,264 ncORFs have HLA data, including 24 with a single tryptic peptide that would otherwise be annotatable. `c2riboseqorf47` was annotated with HLA data informing the decision.
3. **Should peptides from cancer samples or immortalized cell lines support annotation?** 66.9% of searched spectra are cancer-derived; this reason alone blocked 10 of 15 prioritized candidates.
4. **What is the role of evolutionary inference?** Most of the 7,264 lack amino-acid constraint, yet thousands show ORF-level constraint by ORBL. Whether absence of amino-acid constraint argues against function remains debated.
5. **Which other experimental analyses could support annotation?** The authors note it would make sense to annotate an ncORF as protein-coding given evidence for both existence *and* at least one biological function — and then state plainly that **immune recognition of a peptide is not currently considered a biological function by annotation projects**.
6. **How should we annotate microproteins whose function can be neither demonstrated nor inferred?** GENCODE, UniProtKB, HGNC, RefSeq and HUPO-HPP have decided: classify them as peptideins. Precise guidelines are being prepared.
7. **Should deep learning inform gene or protein annotation?** Annotation is historically rooted in manual inspection, which the authors concede does not scale.

Question 5 is the one to sit with. It is the hinge on which the whole peptidein concept turns, and it is a *policy* statement, not a biological one. An ncORF whose product is synthesized, presented to the immune system, and targetable by immunotherapy still fails the function test, because the annotation projects do not count immune recognition as function. Whether that should change is an open question the paper poses to its own community.

## The limitations the authors state

Four, in their own accounting:

1. **Sample type remains problematic.** The Discussion names three genes whose ncORFs have multiple tryptic peptides and *still* remain peptideins, because every supporting peptide comes from cancer samples or immortalized cell lines. Find them in that paragraph yourself — they are one of the capstone cases in [journal club](journal-club.md), so they are deliberately not named here.
2. **The work is data-dependent acquisition only.** Data-independent acquisition, especially coupled with targeted PRM validation, may be more sensitive in specific contexts.
3. **It relies on large-scale manual inspection**, which is not feasible for most researchers. The authors point toward retention-time and ion-mobility prediction tools for scalable work.
4. **ORBL has its own limitations**, reported in the Supplementary Results.

Add one the authors do not list, which you are now equipped to see: constraint and detectability both correlate with ORF length, so the finding that ORBLq is higher in HLA-detected ncORFs carries a circularity risk that length-matching in ORBLq mitigates but does not obviously eliminate.

## Resolving the OLMALINC puzzle

[Module 1](01-annotation-problem.md) opened with a question: `c10riboseqorf92` in the OLMALINC lncRNA has peptide evidence, HLA evidence, pan-essentiality across 415 of 485 cell lines, a rescue experiment showing the phenotype is ORF-specific rather than RNA-mediated, DepMap co-essentiality with mitosis and DNA-damage genes, and a multiplexed scRNA-seq signature across 12 cell lines. Why is it not a gene?

The paper answers directly: it remains annotated as a peptidein because it does not possess clear evidence of function in normal physiology — its evidence remains restricted to transformed cell lines or cancer.

That is the entire framework in one sentence. Not "the evidence is weak" — the functional evidence is the strongest in the paper for any single ncORF.

There is one more twist worth carrying, and it cuts against the obvious reading. Of the six pan-essential ncORFs with HLA support, four have high ORF-level constraint (ORBLq > 0.9) and two have low (ORBLq < 0.7) — and `c10riboseqorf92` is one of the two low ones. So the paper's showcase functional result sits on an ORF with *little* evolutionary constraint, while `c2riboseqorf47`, the one that became a gene, is high-constraint. The two axes disagree about which ORF matters. That is not an embarrassment for the framework; it is the clearest possible demonstration that the axes are independent measurements rather than proxies for one another — which is precisely why the tier table keeps them in separate columns and why the annotation decision is not a weighted sum. The barrier is that *every* piece of it comes from cancer or immortalized cells, and annotation is a claim about the human organism, not about A375 cells. Agenda question 3 is not academic for this ORF; it is the only thing standing between it and a gene record.

Notice also the asymmetry in the cost of being wrong. Annotating a gene propagates into every downstream reference, panel and drug program — the "ripple effects" of [Module 1](01-annotation-problem.md) — and is far harder to undo than deferring. That asymmetry justifies caution independently of the biology, and it is worth being able to argue it in both directions.

## What I now trust, and why

Write this in your own words before moving on. Some anchors:

- A tier is a statement about **evidence**, and an annotation is a **decision**. Keeping them separate is the paper's most useful gift, and it generalizes far beyond this catalogue.
- **Peptidein** is a real, load-bearing category, adopted by five annotation bodies, with 121 initial members. It names the state "this molecule exists and I cannot tell you what it does" — which was previously unrepresentable, so such ORFs were simply absent.
- **Three claims are separable**: the molecule exists; it exists in normal physiology; it does something. Most of this paper's difficulty comes from evidence that establishes the first and cannot reach the third.
- The framework **worked**. It promoted `c2riboseqorf47` on evidence the old standard could not use, and it demoted a majority of the automated top-tier calls. Both directions are the system functioning.
- Where you should remain uncertain: whether HLA evidence *should* count toward annotation, whether the HUPO-HPP threshold should be rewritten for short ORFs, and whether cancer-only evidence should block a gene record. The consortium is uncertain about these too, which is why they are questions 1, 2 and 3 rather than conclusions.

## Self-check

- [ ] Reproduce the six-tier evidence table from memory, including which tier requires Ribo-seq `−` and why that makes its provisional count zero
- [ ] State the three conditions for "Candidate protein" and explain why 2,059 of 7,264 ncORFs cannot meet the first one at any sequencing depth
- [ ] Narrate 37 → 20 → 15 → 3 with the five rejection reasons, and say which reason dominates
- [ ] Explain why manual inspection is net-demoting, and connect that to the base-rate argument in [Module 4](04-mass-spec-proteomics.md)
- [ ] Reconstruct the decomposition of "about 25%" without looking, and say what it implies about which assay is carrying the paper
- [ ] Argue agenda question 3 from both sides, grounding each in a number from the paper, then commit to a position and name the evidence that would change your mind
- [ ] Explain to a colleague why `c11riboseqorf4` is simultaneously the best-evidenced ncORF and a misleading example of a microprotein

Then go to [the journal club and capstone](journal-club.md).
