# Red-team findings

Adversarial review of the eight-module curriculum, `glossary.md`, `journal-club.md`, `learning-plan.md`, `README.md` and `resources/key-references.md`, against `paper.pdf` via coordinate-aware extraction. For the orchestrator, not the learner.

Method note: every figure-internal number below was re-extracted with `pdfx.py region` or from `paper-placed.txt` with x-coordinates, and every inequality direction was taken from prose or Methods rather than from figure text. I re-derived the provisional/final tier cross-tabulation independently rather than checking anyone's copy of it. I did not take any number from `BRIEF.md` or `CORRECTIONS.md` without re-verifying it.

Headline: **the curriculum is in good shape.** Two blockers, four majors, ten minors across ~66,000 words. The large union/101 error has been cleanly excised — the only surviving mention is Module 2's deliberate demolition of it, which is correct pedagogy. One of the two blockers is in `CORRECTIONS.md` itself, not in a module.

## BLOCKER

### B1. `CORRECTIONS.md` item 16 is wrong, and acting on it would delete correct content from Module 6

**File:** `CORRECTIONS.md` (orchestrator's own file). No module edit needed — Module 6 is right.

**The wrong text**, `CORRECTIONS.md` item 16: *"Fig. 4a contains no toy ORBLv fraction. An earlier reading thought the panel showed arithmetic like `0.3/(0.3 + 0.6)` that did not compute. Coordinate-aware extraction shows those digits are y-axis ticks of the quantile plot (1.0, 0.8, 0.6, 0.4, 0.2, 0), interleaved with the labels by reading order."*

**The correct position:** Fig. 4a contains **both**. The y-axis ticks are real and they do interleave with the `ORBLv`/`ORBLq` arrow labels — that half of item 16 is right. But the toy fractions are separately present, ~90 pt lower in the panel, in their own sub-figure.

**PDF evidence.** Coordinate extraction of stream 32, y 620–625:

```
y  625.0 | [220] = [220]ORBL [220]v  [256]0.3  [276]= 0.3  [304] = [304]ORBL [304]v  [340]0.8  [359]= 0.9
y  620.0 | [248] + 0.6 [248]0.3            [332] + 0.1 [332]0.8
```

Numerators sit at x 256 and x 340 on the upper line; the denominators `0.3 + 0.6` and `0.8 + 0.1` sit directly beneath at x 248 and x 332; the results `= 0.3` and `= 0.9` are at x 276 and x 359. Flat reading order independently gives `ORBLv = Conserved branch length / Total branch length  0.3 / 0.3 + 0.6  ORBLv = = 0.3   0.8 / 0.8 + 0.1  ORBLv = = 0.9`. Both fractions compute to one decimal: 0.3/0.9 = 0.33 → `0.3`; 0.8/0.9 = 0.89 → `0.9`. The quantile worked points (`ORBLv` 0.3 → `ORBLq` 0.51; `ORBLv` 0.9 → `ORBLq` 0.95) are at y 715–690, x 485.

**Why this is a blocker rather than a minor:** `CORRECTIONS.md` overrides `BRIEF.md` by construction, so this instruction is authoritative for any later fix round. [Module 6](06-evolution-orbl.md) line 72 states both fractions correctly and even flags the rounding; its Fig. 4a reading exercise (line 262) uses both the fractions *and* the quantile points. If item 16 is applied, the single best worked example of `ORBLv`'s definition is removed and replaced with a false claim about the panel's contents.

**Fix:** amend item 16 to say that the panel contains the two toy fractions *and* the quantile-curve arrow labels, and that the earlier "does not compute" objection was a rounding artefact, not a misreading. Module 6 needs no change.

### B2. Module 4 twice compares the tryptic 2.5% against the HLA build's 76.7%

**File:** `04-mass-spec-proteomics.md`, lines 19 and 301.

**The wrong text**, line 19 (the module's opening prediction prompt): *"Conventional tryptic proteomics found peptides for 2.5% of the 7,264 ncORFs, against 76.7% of canonical proteins."*

And line 301: *"…the chance of two usable, uniquely mapping fragments rises smoothly toward the near-certainty that canonical proteins enjoy: 15,581 of 20,326 canonical proteins detected, `76.7%` (Fig. 3a), against 183 of 7,264 ncORFs, `2.5%`."*

**Why it is wrong, twice over.** 76.7% is (a) from the **HLA build**, not the tryptic build, and (b) a **single-peptide** detection rate, not the two-peptide criterion the sentence is about.

**PDF evidence.** Fig. 3 is titled *"Determinants of ncORF peptide detection in the HLA build"*. Methods, "Detectability determinants": *"Canonical proteins were categorized as detected and undetected based on whether they were detected by a single peptide."* Fig. 3a panel labels, coordinate-verified: `Detected (n = 1,867)`, `Undetected (n = 5,397)`, `Detected (n = 15,581)`, `Undetected (n = 4,745)`.

**The build attribution can now be settled, which the module says it could not.** Extended Data Fig. 1c gives the non-HLA build **16,888** cumulative canonical proteins; Extended Data Fig. 1d gives the HLA build **13,799**. `canonical` is the two-peptide PeptideAtlas category, so a single-peptide count in the same build must exceed it and a single-peptide count in the deeper build must exceed 16,888. 13,799 < 15,581 < 16,888 pins 15,581 as **the HLA build under a one-peptide rule**, exactly as Fig. 3's title implies. That resolves the reconciliation Module 4 line 176 declines to attempt, and it is worth putting in the module.

**Aggravating:** Module 4 line 176 already flags that 16,888 and 15,581 sit on different denominators and says "I did not reconcile them" — and then uses 76.7% against the tryptic number anyway. [Module 5](05-immunopeptidomics.md) line 205 states the prohibition explicitly: *"Never quote 76.7% as tryptic coverage."* Module 4 breaks its own downstream module's rule, in the prediction prompt that anchors the module.

**Fix.** Line 19: rewrite the prompt so the contrast is within one assay, e.g. "Tryptic proteomics found peptides for 2.5% of the 7,264 ncORFs. In the same build it catalogued 16,888 canonical proteins (Extended Data Fig. 1c). Is that gap mostly depth or mostly chemistry?" Line 301: keep 15,581/20,326 = 76.7% but scope it — "the near-certainty canonical proteins enjoy even in the immunopeptidome: 15,581 of 20,326 (76.7%) in the HLA build under a one-peptide rule (Fig. 3a)" — and drop the direct juxtaposition with 2.5%, or replace it with 1,867/7,264 from the same panel. Line 425's statement of the same number is already correctly scoped and needs no change.

## MAJOR

### M1. Module 3's "roughly four times more likely to fail" is roughly six times

**File:** `03-riboseq-bridge.md`, line 122.

**Wrong text:** *"An ncORF found by one pipeline is roughly four times more likely to fail visual Ribo-seq inspection than one found by several."*

**Correct text:** roughly **six** times. Failure rates are 436 − 419 = 17, so 17/436 = 3.90%, against 255 − 194 = 61, so 61/255 = 23.92%. Ratio 6.1.

**PDF evidence.** Main text, "Microproteins as HLA-I-presented peptides": *"we validated the Ribo-seq signal in 88.7% (613 out of 691) of ncORFs and observed that ncORFs found in multiple published studies exhibited a higher rate of validation (96.1% (419 out of 436) verified) compared with ncORFs reported in a single study (76.1% (194 out of 255) verified)."*

The adjacent "20-point gap" framing (lines 122, 214) is correct and needs no change; only the ratio is wrong. Note the error understates the module's own point, so the fix strengthens it.

### M2. Module 7 misattributes reference 7 throughout

**File:** `07-function-crispr-olmalinc.md`, lines 27 and 336 (full bibliographic detail), with the ref number reused at lines 38, 80, 87.

**Wrong text**, line 27: *"1,245 ncORFs carried over from a previously published ncORF guide library (ref. 7 — Chen *et al.*, *Science* **367**, 1140–1146, 2020)"*. Line 336 repeats it: *"ref. 7 (Chen *et al.*, *Science* **367**, 1140–1146, 2020)"*.

**Correct text:** reference 7 is **Hofman, D. A. *et al.* Translation of non-canonical open reading frames as a cancer cell survival mechanism in childhood medulloblastoma. *Mol. Cell* 84, 261–276 (2024).** Chen *et al.*, *Science* 367, 1140–1146 (2020) is **reference 27**.

**PDF evidence.** Reference list, verbatim: *"7. Hofman, D. A. et al. Translation of non-canonical open reading frames as a cancer cell survival mechanism in childhood medulloblastoma. Mol. Cell 84, 261–276 (2024)."* and *"27. Chen, J. et al. Pervasive functional translation of noncanonical human open reading frames. Science 367, 1140–1146 (2020)."*

The ref *numbers* in Module 7 are all correct against the Methods (the library carry-over, the control guides, the two tiling screens `7,28`, the three-study meta-analysis) — only the bibliographic expansion is wrong. So the fix is local: swap the author/journal/volume/year at lines 27 and 336. `resources/key-references.md` lists both papers with correct bibliographic data and does not assign ref numbers, so it is unaffected.

This is the single finding most likely to embarrass the learner, because the learner's stated preference is explicit about citation integrity and they will check.

### M3. Module 2's "at most 448 − 291 = 157" is an unsound derivation, presented as clean

**File:** `02-ncorf-atlas-biotypes.md`, the paragraph beginning *"One clean structural observation does fall out."*

**Wrong text:** *"The ORBL scheme has no processed-transcript class at all … so all 291 processed-transcript ORFs are outside it, and therefore inside the 448. Which means at most `448 − 291 = 157` ORFs are excluded for the two-transcripts-two-frames reason the Methods give as their example."*

**Why it fails.** The inference "outside the ORBL biotype scheme ⇒ inside the `mixed` 448" silently assumes the 291 kept their v35 biotype under the v42 re-derivation — which is precisely what the surrounding section establishes did *not* generally happen. `processed_transcript` is a transcript biotype that occurs on genes of several gene biotypes; an ncORF on a `processed_transcript` of a lncRNA gene re-types to `lncRNA ORF` under v42, and `lncRNA ORF` **gained 95** members in that re-derivation (1,917 → 2,012). So an unknown fraction of the 291 landed in one of the six v42 classes rather than in `mixed`, and neither "all 291 are in the 448" nor "at most 157" is established. The paper publishes no per-biotype breakdown of `mixed`.

**PDF evidence.** Methods, ORBL: the nine matched-null classes are `uORF`, `uoORF+1/+2`, `intORF+1/+2`, `doORF+1/+2`, `dORF`, `lncRNA-ORF` — no processed-transcript class, confirmed. Fig. 4c, coordinate-verified: `uORF` 1,335/2,915 · `uoORF` 243/622 · `intORF` 231/743 · `doORF` 12/64 · `dORF` 79/460 · `lncRNA ORF` 311/2,012 — six rows, denominators summing to 6,816, `lncRNA ORF` up 95 on Fig. 1b. The strict pure-biotype criteria themselves are in the Supplementary Results, not the PDF.

**Fix.** Cut the sentence and the "at most 157". Replace with the defensible version: the v42 scheme has no processed-transcript class, so all 291 were either re-typed into one of the six classes or moved to `mixed`, and the paper does not say which — so the `mixed` set cannot be decomposed from the published figures at all. The charter's rule applies: a number that cannot be reconciled is cut, not hedged. The paragraph's real conclusion (the drop from 3,083 to 2,915 is re-derivation *and* exclusion in unstated proportions) is correct and survives intact.

### M4. Module 3 declares resolved-elsewhere content unresolved, and points at the wrong module

**File:** `03-riboseq-bridge.md`, the 5′-versus-3′-geometry section.

**Wrong text:** *"**3,083 of 7,264** (Fig. 1b, coordinate-verified; note that the ORBL section quotes 2,915 uORFs — [Module 6](06-evolution-orbl.md) flags that discrepancy as unresolved)."*

**Correct position.** It is resolved, in the module the learner reads *before* Module 3. [Module 2](02-ncorf-atlas-biotypes.md) gives the full v35 → v42 re-derivation table; [Module 6](06-evolution-orbl.md) states the resolution outright (*"Counts cannot increase under an exclusion. The explanation is in the Methods: the biotypes were re-derived on GENCODE v42…"*); [Module 8](08-tier-framework-synthesis.md) repeats it. Nothing in Module 6 flags it as unresolved.

**PDF evidence.** Methods, ORBL, verbatim: *"we redid the biotype determination for the ncORFs using GENCODE v42 annotations (the original biotypes from ref. 4 used v35)."* Direction of change confirmed from Fig. 4c: `intORF` 720 → 743 and `doORF` 61 → 64 both increase, which rules out pure exclusion.

**Fix.** Replace the parenthesis with a forward-pointer that matches what the other modules say: "the ORBL section quotes 2,915 uORFs because the biotypes were re-derived on GENCODE v42 — see [Module 2](02-ncorf-atlas-biotypes.md)". This is a stale artefact of the correction round rather than an independent error, but the learner reading in sequence meets the resolution and is then told it is open, which will cost them confidence in the rest of the module.

## MINOR

### m1. `journal-club.md` sends the capstone reader to the wrong panel

Capstone case 2: *"`c3riboseqorf106`. Appears in the tiling screen panels of Fig. 6 and again in Fig. 6h."* It is labelled in **Fig. 6a** (under the `ORBLq` > 0.9 branch), **Fig. 6d** (the HepG2 tiling scores) and **Fig. 6e** (the pan-essential ranking) — coordinate-verified at stream y 633, y 519 and y 453. Fig. 6h is the `OLMALINC` knockdown bulk RNA-seq scatter (`R²` = 0.722) and does not carry it. Main text: *"both c10riboseqorf92 and c3riboseqorf106 exhibited a signature of selective loss of fitness (Fig. 6d and Extended Data Fig. 9i)."* Fix: "Fig. 6a, 6d and 6e, and Extended Data Fig. 9i."

### m2. `journal-club.md` Q1 duplicates a paragraph

The "95,520 proteomics experiments is loose … 95,520 is MS *runs*" point appears twice, once as its own paragraph and again inside the "follow-up to be ready for" paragraph. Correction-round artefact; delete the second instance.

### m3. Module 4's Fig. 2d bar order, and the sourcing of 66

Module 4 writes *"Fig. 2d … gives 36 + 10 + 8 + 7 + 5 = 66"*. Coordinate-verified bar values by category (1, 2, 3, 4, >4 distinct peptides) are **36, 10, 8, 5, 7** — x 450, 460, 470, 479, 488 against x-labels at 452, 461, 470, 479, 487. Sum is right, order is not. Separately, the module's evidence table gives the row *"ncORFs passing inspection, total | 66 | Fig. 2d"*: **66 is not printed anywhere in the paper.** It is the Fig. 2d bar sum and, independently, 30 + 36 from the main text. Module 4 line 425 states this correctly; the table row should match it. This matters because 66 is load-bearing in Modules 4, 5 and 8, and a curator will ask where it comes from.

### m4. `glossary.md` uses 4,879 HLA-typed runs without the discrepancy note

The glossary's HLA-typing entry gives 4,879 (Methods, verbatim: *"For 4,879 MS runs, the full four-digit HLA typing could be retrieved"*), while Module 5 uses 4,870 (main text: *"we therefore curated the HLA types of samples used in 4,870 of the 6,479 MS runs"*) and Fig. 2i prints `n = 4,869 MS runs`. All three are honestly sourced, and `journal-club.md` Q17 flags the three-way disagreement — but the glossary, which is the file the learner will consult mid-argument, does not. Add one clause.

### m5. "The changes sum to exactly −448" is presented as a reconciliation but is tautological

`02-ncorf-atlas-biotypes.md` and `08-tier-framework-synthesis.md` both offer this as a check. 6,816 − 7,264 = −448 by construction, so it carries no information. Both files then draw the correct conclusion (three classes *gain*, so it is not a clean subtraction), so this is cosmetic — but in a curriculum that teaches figure hygiene it is worth not modelling a fake check. The real check in that paragraph is the *sign* of the intORF/doORF/lncRNA changes.

### m6. Module 7 tells the learner which panels carry the held-out capstone name

*"One of the remaining three is held for your capstone, so I am not discussing it here — you will see it labelled in Fig. 6a and 6d."* Fig. 6a additionally places it under the `ORBLq` > 0.9 branch, which is one of the capstone dossier answers. This is handled about as well as it can be without lying, but adding "don't read the labels on those two panels yet" costs nothing.

### m7. `journal-club.md` Q14 marks as `unverified` something the paper's own reference list verifies

Q14: *"Marking this as `unverified`: I believe the specific training-data overlap is well established for NetMHCpan 4.x, but I have not confirmed it against the NetMHCpan publication itself."* Reference 72's title is verbatim *"NetMHCpan-4.1 and NetMHCIIpan-4.0: improved predictions of MHC antigen presentation by concurrent motif deconvolution and integration of MS MHC eluted ligand data."* [Module 5](05-immunopeptidomics.md) already cites the title for exactly this purpose. Upgrade the marker — the circularity concern is verified from this paper, not borrowed.

### m8. Module 3's smORF-caller agreement figures are hedged 175 lines away from where they are used

The *Brief. Bioinform.* 2024 figures (~2% five-way agreement for small ORFs, ~15% at three or more, ~74% for larger annotated genes) appear in the running text, in the analogy table and in the "Write this down" prompts. The hedge — *"the full texts were not reachable from this environment, so the specific figures above are as reported in retrieved abstracts and summaries rather than read in situ"* — lives only in the Sources block at the end. The citation is honestly labelled *somewhere*, which meets the letter of the rule, but the learner's stated intolerance for unmarked recall argues for an inline marker at first use, since the ~2% figure is doing real argumentative work.

### m9. Module 7's heading "Meta-analysis across 25 screens"

Not an error against the paper — the main text says *"hit prioritization through a meta-analysis of 25 CRISPR screens"* verbatim, so `CORRECTIONS.md` item 3 is a criticism of the paper's phrasing, not of the module. Module 7's body already gives the accurate version (*"Three independent CRISPR datasets — refs 7, 28 and the screen generated for this study"*). Optional: make the heading "25 datasets from three studies" so the learner does not repeat the paper's own overstatement at journal club.

### m10. Module 8's Fig. 5e eligibility sentence omits "or other prioritization"

Module 8: *"per Fig. 5e, only Tier 1A and Tier 2A ncORFs, plus Tier 1B ncORFs detected by ≥5 HLA peptides, were considered for manual validation. The 77 ncORFs entering by that HLA route…"* The panel reads **"77 ncORFs with ≥5 HLA peptides *or other prioritization*"**, and Fig. 5b/5e separately routes "3 prioritized ncORFs" into manual validation. The `≥` direction is right (confirmed from the Fig. 5 caption prose, not from figure extraction), and Module 8 does count the 3 in its 121 decomposition, so the omission is confined to the eligibility sentence. Add "or otherwise prioritised".

## An addition, offered as a reading rather than a fact

Fig. 5e's Tier 1B row carries **"4 others are protein"** alongside the 72 peptideins (coordinate-verified: x 456, y 480, against 72 at x 478). Nobody in the curriculum mentions it, and it would let Module 8 answer a question the learner is otherwise left to guess at: *which* Tier 1B ncORFs are protein-coding. The four reconcile against the three pre-existing Tier 1B annotations named in the main text (`c14riboseqorf117`/`EIF5`, `c1riboseqorf55`/`PTP4A2`, `c3riboseqorf98`/`CGGBP1`) plus `c2riboseqorf47`, which the main text also calls "a tier 1B uORF in the GMCL1 gene". That is a satisfying closure of the "three genes" ambiguity from the other direction.

But 72 + 4 = 76 against a stated 77, so one Tier 1B ncORF in that stratum is unaccounted for by the panel, and the paper does not name the four. Offer it as a reading with the residual attached, or leave it out. Do not state it as fact.

## What I checked and found correct

This section is as important as the findings above. Everything below was independently re-extracted and reconciled; where a module hedged, I checked whether the hedge was still needed.

**The tier cross-tabulation, re-derived from scratch.** Coordinate extraction of Fig. 5b (stream 61, y 400–500, x-resolved) gives the full matrix. Rows are final tier, columns provisional:

- Final 1A: 16 (all from prov. 1A). Final 1B: 2 + 588 + 11 = 601. Final 2A: 7 + 32 = 39. Final 2B: 1 + 11 + 1,047 = 1,059. Final 3: 2 + 77 + 10 + 1 = 90. Final 4: 7 + 82 + 15 + 5,353 = 5,457. Final Other: 2.
- Provisional 1A column: 16 + 2 + 7 + 1 + 2 + 7 + 2 = **37** ✓. Prov. 1B: 588 + 77 = **665** ✓. Prov. 2A: 11 + 32 + 11 + 10 + 82 = **146** ✓. Prov. 2B: 1,047 + 1 + 15 = **1,063** ✓. Prov. 3: **0** ✓. Prov. 4: **5,353** ✓.
- Both margins close on **7,264** (37 + 665 + 146 + 1,063 + 0 + 5,353; and 16 + 601 + 39 + 1,059 + 90 + 5,457 + 2). Every cell in the matrix is consistent with every published total. The tier tables in Module 8, `glossary.md` and `journal-club.md` Q5/Q6 are all correct.
- `journal-club.md` Q6's inference that provisional Tier 4 is "perfectly stable at 5,353" is confirmed by the matrix: the prov.-4 column has a single non-zero cell, at final Tier 4.

**Fig. 5a's evidence grid.** Read column-wise from the placed text: MS `++ − + − ± −`, HLA `± ++ ± + ± −`, Ribo-seq `+ + + + − +`, categories Candidate protein / Presented / Detected / Detected / Putative / Ribo-seq ORF. Matches Modules 8, 3, 4, `glossary.md` and `journal-club.md` exactly.

**Every inequality in the curriculum.** The known `pdfx.py` glyph bug is present and the curriculum is not fooled by it. Fig. 5a's HUPO-HPP inset extracts as `≤2 non-HLA peptides` / `≤18 amino acids covered`; every module writes `≥2` and `≥18`, sourced to the main text (*"two distinct, uniquely mapping peptides of length 9 or more residues and a minimum protein coverage of 18 residues"*). Fig. 4a extracts as `≤1,000 untranslated ORFs`; Module 6 writes `≥1,000` and cites Methods "at least 1,000". Fig. 5e's `≤5 HLA` is written `≥5` and confirmed from the caption prose. Fig. 2i's `(rank 2)` is written `≤ 2` from Methods (*"if the rank score was smaller than or equal to 2"*) with the main text's `<2%` noted. Module 6's Sources block explains the bug to the learner, which is the right call. **No inequality error found anywhere.**

**Every sum the charter named.** Seven biotypes → 7,264 ✓ (3,083 + 688 + 720 + 61 + 504 + 1,917 + 291; percentages 42.4 + 9.5 + 9.9 + 0.8 + 6.9 + 26.4 + 4.0 = 99.9). 12 + 72 + 34 + 3 = 121 ✓ (Fig. 5e, x-resolved). 42 + 141 = 183 ✓. 30 + 36 = 66 ✓. 30 + 12 = 42, 36 + 105 = 141 ✓ (Fig. 2c bars: 30, 12, 36, 105). 419 + 194 = 613 ✓. 436 + 255 = 691 ✓. Funnel 2 + 1 + 1 + 1 = 5 ✓ (Fig. 5c: pseudogenic 2, downgraded to tier 3 1, novel CDS isoform 1, miscalled CDS 1) and 2 + 10 = 12 ✓. Funnel stage 1: 2 + 7 + 1 + 7 = 17 ✓, 37 − 17 = 20 ✓, 15 + 1 = 16 ✓ with the asterisk. Fig. 4c numerators → 2,211 and denominators → 6,816 ✓. Fig. 4g pairs → Fig. 4c denominators, all six ✓. Fig. 2f bars → 1,785 with 1,094 (61.3%) at one peptide and 691 at two or more ✓. Nine ORBL null classes → 1,717,927 ✓. 1,785 − 1,735 = 50, 5,479 − 5,081 = 398, 50 + 398 = 448 ✓. 1,796 + 5,142 = 6,938 = 7,264 − 326, and 1,867 − 1,796 = 71, 5,397 − 5,142 = 255, 71 + 255 = 326 ✓. 10,150 + 553 = 10,703 with 94.8%/5.2% ✓. 581 × 5 = 2,905 ✓. 1,785 + 5,479 = 7,264 ✓. Library tiers 4 + 224 + 13 + 373 + 13 + 34 + 1,535 = 2,196 ✓.

**Denominator discipline.** Apart from B2, I found no place where a module states a rate over one denominator using a numerator from another. Module 5's four-row detection table and Module 8's synthesis table both label the assignment rule and the curation stage on every row. Module 6 reports the paper's own 30.4% and then flags that 2,211/6,816 = 32.4% is the figure against the evaluable set, and notes that the paper's own uORF figure (1,335/2,915) uses the post-exclusion denominator while its aggregate does not — the paper's slip, correctly attributed to the paper. Module 2's three-denominator table (7,264 / 6,912 / 6,816) is correct, including that Fig. 3b's 6,912 drops `doORF` (61) and processed-transcript ORFs (291) — confirmed verbatim from the Fig. 3b caption.

**The union/101 excision.** The only surviving occurrence of `101` or of a cross-build union claim anywhere in the curriculum is Module 2's paragraph beginning *"Resist one tempting shortcut, because I fell for it first"*, which computes it in order to demolish it and quotes the Fig. 3 Methods sentence in full. Modules 5 and 8 and `journal-club.md` Q1 all state the correct position without printing the number. Verified verbatim: *"Contrary to most other analyses, peptides were not exclusively assigned to a single ncORF, due to which the number of detected ncORFs was larger than in Extended Data Fig. 4b."* Full-text search finds no cross-build union or overlap statement in the paper. The replacement anchor (15,581 of 20,326 in Fig. 3a) is stated accurately in Modules 2, 5 and 8 and in `journal-club.md`; only Module 4 misuses it (B2). **I recommend keeping the 101 where it is** — naming a trap by its number is how you inoculate a learner who will later see it on someone's slide.

**Spoiler discipline: clean.** `grep` across all eleven notes files, `README.md` and `key-references.md` for `c17norep146`, `c3riboseqorf106`, `PSMC5`, `ZBTB11`, `STK11`, `ZNF219`, `CIRBP` returns hits **only** in `journal-club.md`, in the capstone section. A second grep for the peptide and ORF sequences that Fig. 5a's schematic and Extended Data Fig. 8b carry (`MPAVSAEERRW`, `RLTDQSRWSW`, `DSANIICPR`, and the Fig. 4h/4i sequences) returns nothing anywhere — which also keeps the CC BY-NC-ND obligations clean. Module 3's *"Read only panel `a`. Leave panel `b` alone — you will want it fresh later"* is exactly the right handling of Extended Data Fig. 8.

**Analogy breakage notes.** Every analogy in the curriculum carries an explicit breakage. Checked individually: Module 1's count-matrix/GTF analogy; Module 3's six-row bridge table (sub-codon phase, UMIs/occupancy, depth intuitions, 5′/3′ geometry, GTF-as-ground-truth, pseudobulk-versus-aggregate-track); Module 4's spectrum-as-read, search-database-as-GTF, BH-q-value (three separate breakages), USI-as-coordinate, PeptideAtlas-categories-as-GTF-tags; Module 5's poly(A)-as-capture-reagent, CITE-seq/Xenium panel, and the explicit "hard stop, no clean analogue" on degradation products as evidence of synthesis; Module 6's `AddModuleScore` and log2FC-versus-adjusted-*P*. Module 5's one *unbroken* analogy (effect size versus *P* value in Fig. 3d) is correctly declared unbroken rather than left ambiguous, and it is genuinely the same statistics. The charter's expected offenders are all pre-empted rather than committed: target–decoy is explicitly distinguished from a BH q-value in Module 4 and again in `journal-club.md` Q8; "Ribo-seq is just RNA-seq of ribosomes" is demolished in Module 3's first paragraph; peptide detection is distinguished from expression level in Module 5's standing-pool-versus-flux section; the unstranded-library analogy for a no-enzyme search is named as the *wrong* analogy in `journal-club.md` Q10; and nobody treats PeptideAtlas as a cell atlas.

**The SNP-demultiplexing and pseudobulk analogies are used as the charter requires.** Module 1 presses on both target quantities (*"Roughly 200 cells per condition per line at target recovery; nine of twenty-one lines lost to the 100-cell floor"*), and Module 7 makes the selection argument explicitly and correctly: *"a line represented by few cells at day 7 is a line that grew slowly, transduced poorly, or **died from the perturbation** … the 12 lines that supply the transcriptional signature are enriched for lines that *tolerated* the knockout. The panel that reports the phenotype is conditioned on surviving it."* `journal-club.md` Q16 repeats it. This is the best thing in the curriculum.

**Overclaiming: none found.** Every item on the charter's hunt list is handled correctly.
- HLA detection is never allowed to imply "protein": Modules 1, 5, 7 and 8 all quote agenda question 5 verbatim (*"immune recognition of a peptide is not currently considered a biological function by annotation projects"* — confirmed as question 5, not 2).
- `ORBLq` constraint never implies a functional peptide: Module 6's "what the scores license / what they forbid" treatment of `c8riboseqorf102` and `c11norep1` is exact, and it names the regulatory-uORF reading as the *predicted* signature.
- CRISPR pan-essentiality never implies a protein-coding gene or a peptide effector: Module 7 states the missing translation-dead rescue construct outright and names its cost.
- "25%" is consistently a detection rate, never an annotation outcome.
- "121 peptideins" is correctly framed as a curation-budget result over four strata in Module 8.
- pLDDT by tier is explicitly length-confounded in Modules 5 and 6, with the instruction to read Extended Data Fig. 10a and 10f before 10b–d.
- **"Rejected on inspection" is not read as "false" anywhere.** Module 4 gets it right; Module 8 repeats the same distinction with the same upper-bound framing; `journal-club.md` Q8 and Module 5's single-peptide discussion are consistent with it. All five verdict categories verified verbatim from Methods.
- Supplementary-derived claims are marked throughout — Supplementary Tables 15/16 (subset FDR), Table 12 (the 121), Table 13, the pure-biotype criteria, the ORBL limitations, and Extended Data Fig. 10's absent Methods.

**Citation integrity: sound apart from M2.** I checked `resources/key-references.md` line by line against the paper's own reference list. Every one of the ~35 entries matches on author, title, journal, volume, page range and year — including the ones that look wrong and are not: *Nucleic Acids Res.* **54**, gkag234 (2026) is ref. 34 verbatim; *J. Proteome Res.* **25**, 539–555 (2026) is ref. 13 verbatim; *Life Sci. Alliance* **8**, e202402910 (2025) is ref. 26 verbatim. Module 6's Zenodo DOI `10.5281/zenodo.18749292` for `ORBL_tools` is ref. 93 verbatim. Module 4's ref. 65 (van Wijk, *Plant Cell* 33, 3421–3453, 2021) is correct and is a *different* van Wijk paper from ref. 12 (*J. Proteome Res.* 23, 185–214, 2024) — an easy trap that Module 4 did not fall into. Refs 51, 52, 55, 56, 61, 62, 64, 66–69, 72, 74, 75–78, 83–85 all verified. No constructed-looking DOI anywhere. Every external primer in Modules 3, 4, 5 and 6 is labelled with whether the full text was reachable.

**Methods fidelity, spot-checked hard.** All ten manual PSM validation criteria; the five verdict categories; the three Ribo-seq grades verbatim (four / three sequential in-frame peaks in the first 100 nt; either track suffices); GWIPS-viz A-site/P-site global aggregate on "full"; 183 and 699 inspected; `PIF` reported not thresholded; the `ORBLq` formula including the pseudocount and the "not added if the result would be more than 1" clause; the `ORBLv` denominator over all 116 placental or 26 primate species *"not just the ones present in the local alignment"*; the 120-mammal alignment and the 100-vertebrate/470-mammal/447-mammal extras; the Drill any-stop rule and the Bushbaby compensating-indel rule; the nine null classes and the ≥1,000 length-widening rule; the in-gene permutation test formula including the two-sided conversion; the CRISPR library design rules and all three control-guide classes (471/503/497); Chronos ±0.5 and pan-essential at ≥60%; ≥5 TPM Ribo-seq / ≥10 TPM RNA-seq; the 21-line multiplexed design with the Chr2-2 cutting control, `KIF11` positive control, MOI ~1, 5 µg ml⁻¹ puromycin; the e-distance definition; the whole PRM sample prep including protocol 2's 76% acetonitrile / 0.1% TFA / 50 mM NaCl supernatant; MSFragger v3.7 for both builds with Comet only in the Extended Data Fig. 2a,b comparison and the ubiquitination reanalysis; semi-enzymatic non-HLA and no-enzyme HLA; THISP level 4 2023-02/2023-07; the 20,389 neXtProt core set and the `canonical`/`non-core canonical` gate. **Every one of these checked out.** Module 4's Part 1 and Part 5 and Module 6's mechanics section are the most heavily anchored writing in the curriculum and I could not break either.

**Internal paper inconsistencies are all flagged, none silently resolved.** 4,870/4,879/4,869; 691/699; 5,140/5,142; 486/471/485/415; 3.5/3.53 billion; Ensembl Release 87; the `KyleDoolittle`, `GCh38` and `c8riboseq102` typos. Module 7's PRISM treatment ("roughly 85–88% of several hundred cancer cell lines") is the right register. I also found two the curriculum does not mention, both harmless: Fig. 6a prints `c14riboseqorf18` where the main text has `c14riboseqorf118`, and the Methods write "ProteomeMapper" where ref. 58's tool is `ProteoMapper` (the curriculum uses the correct `ProteoMapper`).

**Structure and pedagogy.** All eight modules open with a numbered prediction prompt and close with a positive "What I now trust, and why". Prerequisite order holds: no module depends on a concept first introduced later without a forward link — Modules 1–4 forward-reference the tier system and `ORBLq` but each links to the module that owns them and gives enough in place. Formatting conventions are met across all eleven files: no YAML, single `#` H1 on line 1, no `####`, no trailing whitespace, LF endings, one trailing newline, relative links, backticked identifiers, `- [ ]` for actionable items, HTML comments for unfilled content. `README.md` links `notes/misconceptions.md` and `learning-plan.md` schedules it for two readings, both of which now resolve.

**Module 4 pacing: defensible as written.** 11,512 words is ~50–60 min of careful reading, plus ten figure-reading assignments in the PDF (~50 min) and five written reflections (~50–75 min). That is 2.5–3.2 hrs against a 3-hr slot. If it must be trimmed, cut in this order: (1) Part 1's instrument parameters — column dimensions, flow rate, gradient steps, nanospray voltage, *m/z* ranges, accumulation times, isolation width, collision energy — which are correctly anchored but support no later claim; (2) the ten-point validation list down to the four the module actually reuses, criteria (ii), (iii), (vi) and (vii); (3) the PTM/ubiquitination paragraph. That is ~1,200–1,500 words at zero cost to the argument. Do **not** cut idea 3 (the base-rate trap) or the `c11riboseqorf4` N-terminal acetylation case — Modules 5 and 8 both draw on them, and the acetylation case is the only place in the curriculum where "processing" is distinguished from "detection".

## Fix round: files and owners

| File | Findings | Owner |
|---------|-------|-------|
| `CORRECTIONS.md` | **B1** — item 16 must be amended before any further fix round consumes it | Orchestrator |
| `notes/04-mass-spec-proteomics.md` | **B2** (lines 19, 301, and the reconciliation now available for line 176), **m3** | MS / proteomics specialist |
| `notes/03-riboseq-bridge.md` | **M1**, **M4**, **m8** | Ribo-seq specialist |
| `notes/07-function-crispr-olmalinc.md` | **M2**, **m6**, **m9** (optional) | Functional-genomics specialist |
| `notes/02-ncorf-atlas-biotypes.md` | **M3**, **m5** | Catalogue / biotypes specialist |
| `notes/08-tier-framework-synthesis.md` | **m5**, **m10**, and the Fig. 5e "4 others are protein" addition if you want it | Orchestrator |
| `notes/journal-club.md` | **m1**, **m2**, **m7** | Orchestrator |
| `notes/glossary.md` | **m4** | Whoever owns the glossary |
| `notes/01-annotation-problem.md`, `notes/05-immunopeptidomics.md`, `notes/06-evolution-orbl.md`, `notes/learning-plan.md`, `README.md`, `resources/key-references.md` | **none** — checked, no fix needed | — |

Priority order if the round is time-boxed: **B1** first, because it is authoritative and would cause a regression. Then **M2** (citation integrity, the learner will check). Then **B2** (a proteomicist will catch it in the first five minutes of journal club). Then **M3** and **M4**, then **M1**, then the minors in any order.

Nothing I found changes any conclusion the curriculum draws, and nothing I found is in the curriculum's spine. The two files most exposed to a hostile reader — Module 5 and Module 6 — came through clean.
