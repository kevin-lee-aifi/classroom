# Module 5 — Immunopeptidomics: a second, stranger window

~2.5 hrs. Prerequisite: [Module 4](04-mass-spec-proteomics.md) — spectra, PSMs, search databases and target–decoy FDR are assumed, not re-taught. Covers Fig. 2e–k, Fig. 3, Extended Data Figs 4–6, the Methods subsections `PeptideAtlas database construction and searching` (HLA build), `Categorizing HLA peptides`, `HLA binding predictions`, `Detectability determinants`, `Expression analysis` and `MLP classifier model`, plus agenda questions 2, 3 and 5.

This is the module that carries the paper. The abstract's "about 25%" is essentially one number from one assay, and this is that assay.

## Predict first

Four answers in writing before you read on. Numbers, not ranges.

1. Tryptic proteomics found peptides for 183 of 7,264 ncORFs — 2.5%. Immunopeptidomics searched about 1/15th as many spectra. How many ncORFs did it reach?
2. Take every ncORF detected by *either* window. What fraction was detected by *both*?
3. HLA peptides are not protease products, so the search runs with no enzyme specificity. Against the semi-tryptic search used for the other build, by roughly what factor does that enlarge the candidate space for an 8–12-residue peptide?
4. Of the ncORFs immunopeptidomics did detect, what fraction rest on exactly one distinct peptide?

Question 2 is where most people are most wrong, and it is the hinge of the module.

## What the assay physically samples

Immunopeptidomics does not sample proteins. It samples short peptides the cell has already committed to destroying, intercepted while displayed on the surface.

### The class-I pathway, end to end

Standard immunology, which the paper does not re-teach. Primers cited below rather than recalled.

- **Degradation.** Cytosolic and nuclear polypeptides are degraded by the proteasome — constitutive 26S, or the immunoproteasome in interferon-exposed cells. Proteasomal cleavage typically generates the ligand's **C terminus** directly; the product is usually still N-terminally extended.
- **Transport.** The TAP1/TAP2 heterodimer moves peptides into the ER, favouring lengths of roughly 8–16 residues.
- **Trimming and loading.** In the ER the peptide meets the peptide-loading complex — TAP1/2, tapasin, ERp57, calreticulin, assembled around the class-I heavy chain and β2-microglobulin. ERAP1/ERAP2 trim the N terminus to final length. Tapasin edits, favouring peptides that give a stable complex.
- **Display.** The stable complex traffics through the Golgi to the plasma membrane.
- **Recovery.** The reanalysed datasets come from immunoaffinity purification of HLA complexes, acid elution, LC–MS/MS. The paper reanalysed 118 public ProteomeXchange datasets and does not re-describe their preparation; reference 20 (Abelin *et al.*, *Nat. Commun.* **14**, 1851, 2023) is its workflow citation.

Two consequences dominate everything downstream. Ligand length is set by the machinery, not by a protease you chose — class-I ligands cluster at 8–11 residues. And which peptides appear depends on the sample's own HLA alleles, because binding is motif-specific and each cell carries up to six classical class-I alleles.

### The reframing: a readout of proteasome output

**Tryptic proteomics measures the standing pool. Immunopeptidomics measures flux through the degradation machinery.**

Write both crudely. Identifying a protein in a digest scales with steady-state abundance — synthesis rate divided by degradation rate. Ligand supply from that protein scales with the rate its molecules are *destroyed* — synthesis rate times degradation rate, near enough. The two expressions move in opposite directions in the degradation rate. A polypeptide made constantly and destroyed immediately has a near-zero standing pool and a large ligand flux.

So these are not one window at two sensitivities. They are windows onto different physical quantities, and a whole class of molecules is bright in one and invisible in the other. That is why running both was worth doing, why the assay is *enriched* for unstable products, and — as you are about to see — why the overlap between them is tiny.

### DRiPs, and the BAG6 explanation the Discussion offers

Immunology has a name for the short-lived source material: **DRiPs**, defective ribosomal products — prematurely terminated chains, misfolded nascent chains, products of frameshifting or mis-acylated tRNA, degraded rapidly rather than joining the mature pool. A substantial fraction of the class-I immunopeptidome is thought to derive from them. The paper cites this as reference 40 (Yewdell & Hollý, *Curr. Opin. Immunol.* **64**, 130–136, 2020).

The Discussion makes the link explicit: many ncORFs generate immunopeptides but not tryptic peptides, and one potential explanation is lower stability for many ncORF-derived polypeptides, perhaps through **BAG6-mediated degradation in the proteasome** — citing reference 19 (Cuevas *et al.*, *Cell Rep.* **34**, 108815, 2021, titled "Most non-canonical proteins uniquely populate the proteome or immunopeptidome") and reference 21 (Kesner *et al.*, "Noncoding translation mitigation", *Nature* **617**, 395–402, 2023). The definition of `peptidein` carries it forward: peptideins explicitly include potentially transient products of cellular stress or defective ribosome translation.

Be precise about status. This is offered as *one potential explanation*, cited to prior work. The paper makes no stability measurement of its own — no half-life, no chase, no proteasome-inhibition immunopeptidomics. Whether structure prediction could substitute is left explicitly open, and Extended Data Fig. 10 shows why that is hard: predicted pLDDT rises as ncORF length falls, and shuffled versions of high-confidence sequences also reach high pLDDT. There is no validated stability readout here to lean on.

Retrieved primers for the background above:

- [Alternative antigen processing for MHC class I: multiple roads lead to Rome](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2015.00298/full) — *Front. Immunol.* 2015; proteasome → TAP → ERAP → PLC.
- [Chaperone function in antigen presentation by MHC class I molecules](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2023.1179846/full) — *Front. Immunol.* 2023; peptide-loading complex and tapasin editing.
- [The nature and extent of contributions by defective ribosome products to the HLA peptidome](https://www.pnas.org/content/111/16/E1591) — *PNAS* 2014; direct MS estimate of the DRiP contribution.

## The analytical consequence: no-enzyme search

### Why no enzyme, and what it costs

A tryptic digest tells the search engine where peptides can begin and end. HLA ligands were cut by the proteasome and trimmed by aminopeptidases, so no cleavage rule applies. The Methods state it plainly: for the HLA 2023-11 build, **all datasets were searched in no-enzyme mode**. The non-HLA 2023-06 build was searched with **semi-enzymatic settings (typically semi-tryptic)** — one terminus had to conform. Both used MSFragger v3.7 against a THISP level 4 database (2023-07 for HLA, 2023-02 for non-HLA) containing the 7,264 Ribo-seq ORFs plus other contributed candidate sequences.

The size of the space, as a back-of-envelope you should be able to reproduce. Protein of length *L*, search window 8–12 residues, lysine or arginine roughly once every nine or ten residues:

| Specificity | Candidates per protein | Relative |
|---------|-------|-------|
| Fully specific, no missed cleavages | ~*L*/50 (only ~19% of tryptic peptides land in 8–12 aa) | 1× |
| Semi-specific, one free terminus | ~*L* | ~50× |
| No enzyme, both termini free | ~5*L* | ~250× |

That arithmetic is mine, not the paper's, and the multipliers move with the length window and missed-cleavage setting. The robust conclusion: **against the semi-tryptic baseline this paper actually used, no-enzyme mode costs about 5× the candidate space; against a fully specific search it is closer to two orders of magnitude.**

Module 4's database-size argument then applies directly. More candidates means more chances for an incorrect sequence to score well, so the incorrect-match score distribution shifts up, so at fixed FDR the threshold rises, so sensitivity falls. Target–decoy still gives an honest global error estimate — just a worse one.

There is a second squeeze the database-size argument misses. HLA-I ligands are short. An 8-mer has seven backbone bonds, so at most fourteen singly-charged b/y ions; a 15-residue tryptic peptide has twenty-eight. You get roughly half the fragment ions with which to discriminate, exactly when you have five times as many candidates to discriminate among.

The paper's numbers show the squeeze without framing it this way:

| Quantity | non-HLA 2023-06 | HLA 2023-11 |
|---------|-------|-------|
| Datasets | 295 | 118 |
| Experiments | 1,172 | 592 |
| MS runs | ~85,000 (Fig. 1b) | 9,776 (Methods; ~10,000 in Fig. 1b) |
| MS/MS spectra | 3.5 billion | 240 million |
| PSMs | 573 million | 28 million |
| PSMs per spectrum | 16.4% | 11.7% |
| Enzyme specificity | semi-enzymatic (typically semi-tryptic) | **no enzyme** |
| Peptide-level FDR | 0.0009% | 0.0041% |
| Distinct peptides in build | — | 865,922 |
| ncORF peptides | 484 | 3,116 |
| ncORFs reached | 183 (2.5%) | 1,785 (24.6%) |

The PSMs-per-spectrum row is my division of the two rows above it, both coordinate-verified from Fig. 1b. The HLA build converts spectra into identifications at about 70% the rate of the digest build, at a peptide-level FDR about 4.6× higher — a tiny absolute number, moving in exactly the direction the search-space argument predicts.

### Why HLA spectra also *look* different

Easy to skim, worth sitting with. The Methods note that some HLA peptides do end in lysine or arginine and so fragment like tryptic peptides — but many do not, and those may give **strong b ions and internal fragment ions rather than the strong y-ion series customary in tryptic spectra**.

That is not cosmetic. Scoring functions, intensity predictors and rescoring models are overwhelmingly trained on tryptic data, so they are mis-calibrated on this population — the paper's reference 38 (Adams *et al.*, *Nat. Commun.* **15**, 3956, 2024) exists to address exactly this. And when you read a manual-inspection panel from the HLA build, remember the inspector's intuitions were also formed on tryptic spectra.

## The yield

From `Microproteins as HLA-I-presented peptides`:

- **3,116 distinct peptides mapping to 1,785 of 7,264 ncORFs — 24.6%** (Fig. 2e,f; Extended Data Fig. 4a; Supplementary Tables 6 and 7).
- **2,937 of 3,116 (94.3%) were found on HLA class-I alone**; the other 179 appear in HLA class-II datasets (Extended Data Fig. 4a–f).
- Within those 179, Extended Data Fig. 4f reports **22 detected exclusively in HLA-II samples, 14 of them ≥14 aa** — a length consistent with genuine class-II presentation. Note 3,116 − 2,937 = 179 exactly, so the set reconciles.
- The authors' reading: ncORF-derived peptides are most often sourced from the *intracellular* pool of translation products, less often from extracellular sources, in contrast to canonical proteins (references 9, 19, 20).
- Their own caveat, in Extended Data Fig. 4e: class-I and class-II detection are not mutually exclusive, since class-I peptides can be recovered incidentally from class-II pulldowns. "Seen in an HLA-II dataset" is weaker than "presented on HLA-II".

### How thin the evidence is per ORF

Not in the running text, and it changes how you read the headline. Fig. 2f plots ncORFs against the number of distinct peptides that detected them, with labelled bars. Reading them by coordinate and summing gives 1,094 + 392 + 154 + 66 + 33 + 18 + 16 + 4 + 1 + 2 + 1 + 1 + 1 + 1 + 0 + 1 = **1,785**, the full detected set, so the read is sound. The first bar is the one that matters:

**1,094 of the 1,785 HLA-detected ncORFs — 61.3% — rest on exactly one distinct peptide.** The other 691 have two or more, which is the `n = 691` annotation in Fig. 2g,h. Hold that against Module 4's finding that single-peptide tryptic evidence survived manual inspection only 36 times out of 141.

The authors do not leave it unexamined. They manually inspected **859 HLA-I MS spectra** and **691 matching Ribo-seq profiles**, restricting the latter to ncORFs with at least two uniquely mapping HLA peptides. Ribo-seq support validated in **613 of 691 (88.7%)**, tracking reproducibility: **419 of 436 (96.1%)** for ncORFs in multiple published studies versus **194 of 255 (76.1%)** for single-study ncORFs. Both splits reconcile (436 + 255 = 691; 419 + 194 = 613).

Note what that established. It checked that the *Ribo-seq* evidence for the source ORF holds up. It did not measure stability and did not address whether presentation occurred in a healthy cell. It licenses "this ORF really is translated", which is not "this ORF encodes a protein".

## The central argument: where the headline 25% comes from

The spine of the curriculum. Put the two windows side by side.

| Window | ncORFs detected | Share of 7,264 |
|---------|-------|-------|
| HLA immunopeptidomics (2023-11 build) | 1,785 | 24.6% |
| Tryptic/semi-tryptic MS (2023-06 build) | 183 | 2.5% |
| **Seen by both windows** | **101** | **1.4%** |
| **Union — the abstract's "about 25%"** | **1,867** | **25.7%** |
| Canonical proteins, same comparison (Fig. 3a) | 15,581 of 20,326 | 76.7% |

Decompose the union: HLA only 1,785 − 101 = **1,684**; both **101**; tryptic only 183 − 101 = **82**; total 1,684 + 101 + 82 = **1,867**.

Three readings, in increasing order of consequence.

**95.6% of all detected ncORFs — 1,785 of 1,867 — came from immunopeptidomics.** Delete that assay and the abstract reads "about 2.5%".

**Only 5.4% — 101 of 1,867 — were seen by both.** The windows are very nearly disjoint. Not a novel observation; it is the finding in the title of reference 19. But it is now established at consortium scale, and it is what the flux-versus-standing-pool argument predicts.

**The window carrying the claim is not the window the standard was written for.** The HUPO-HPP criteria — two distinct **non-HLA** peptides of ≥9 aa covering ≥18 aa — were written for tryptic proteomics, and are stated in terms that exclude HLA peptides by construction. Tryptic proteomics reached 2.5%. The headline is produced almost entirely by evidence the governing standard does not count.

### Why this is not a gotcha

The paper does this same accounting itself, in public, and builds its framework around it.

- **Fig. 5 keeps MS and HLA in separate columns.** A merged "proteomics" column would have concealed a 95.6%/5.4% split. Separating them is what makes the split visible.
- **Tier 1B exists at all.** "Presented" is a tier with MS `−` and HLA `++`, created because the consortium decided abundant HLA evidence says something real while declining to say it says "protein".
- **`c2riboseqorf47` was promoted with no tryptic peptides.** The GMCL1 uORF became `ENSG00000310604`; the Discussion says the identification was made *despite there being no tryptic MS peptides* and despite ambiguous amino-acid constraint by conventional methods. HLA-I and HLA-II peptides, a loss-of-function phenotype, a high ORBLq and a positive PhyloCSF score carried it.
- **Agenda question 2 asks directly**: should HLA immunopeptidomics be used as evidence that an ncORF encodes a protein-coding gene? They note 1,785 of 7,264 are observed with HLA data, including 24 ncORFs with one tryptic peptide that HLA support could push over the line, and cite `c2riboseqorf47`. Posed as a question, not a conclusion.

A project with something to hide would have merged the columns and quoted the union. This one separated them and named the question it could not answer.

### Verify the overlap before quoting it

You will be asked for the 101 in journal club, so know its provenance. Neither `101` nor the union `1,867` appears in the running text; both are recoverable only from the per-ncORF detections in Supplementary Tables 3 (non-HLA) and 6/7 (HLA), and they are arithmetically locked — given one, the other follows.

There is also a trap. Fig. 3a labels its detected ncORF set `Detected (n = 1,867)` against `Undetected (n = 5,397)`, summing to 7,264, which looks like confirmation of the union. It may not be. The `Detectability determinants` Methods state that for this analysis, contrary to most others, peptides were **not** exclusively assigned to a single ncORF, so the detected count exceeds that in Extended Data Fig. 4b — attributing the excess over 1,785 to ambiguous peptide-to-ncORF mapping rather than to adding the tryptic build. The mapping rule in that situation is itself arbitrary: for a peptide matching several ncORFs, one is chosen as the first alphanumerically. So two different quantities may both print as 1,867. Cite Supplementary Tables 3 and 6/7 rather than Fig. 3a for the overlap, and say "about 100 of roughly 1,870" if you are being careful in front of a proteomicist.

## Determinants of detection

Fig. 3 and Extended Data Figs 5–6 ask which ncORFs the assay can see. Read them with the length confound in mind throughout — it sits behind more of this figure than the paper says.

### Length, hydrophobicity and isoelectric point

Fig. 3a crosses three properties with two groups, each split detected versus undetected; two-sided Wilcoxon rank-sum with Holm–Bonferroni. P values taken by coordinate from the panel:

| Property | ncORFs (1,867 vs 5,397) | Canonical proteins (15,581 vs 4,745) |
|---------|-------|-------|
| Sequence length | P = 3.683 × 10⁻²³ | P = 4.9 × 10⁻²⁰¹ |
| Hydrophobicity (Kyte–Doolittle) | `NS` | P = 4.238 × 10⁻⁴⁹ |
| Isoelectric point | P = 2.130 × 10⁻¹⁶ | P = 3.359 × 10⁻⁷⁰ |

Directions, from the running text and Extended Data Fig. 5a–d:

- **Length: longer is detected more**, for ncORFs and canonical proteins alike; Extended Data Fig. 5c,d bins ncORFs by length and shows detection climbing. Mechanically obvious — a longer sequence offers more substrings that could bind some allele — and consequential, because the catalogue's best-detected members are its least typical microproteins.
- **Hydrophobicity: no overall difference for ncORFs.** The text flags this as running against recent reports (reference 21). C-terminal hydrophobicity does vary by biotype (Fig. 3b), which the authors put to sequence context, but it does not explain detectability: detected and undetected ncORFs show similar C-terminal hydrophobicity (Extended Data Fig. 6c,d).
- **Isoelectric point: read slowly, the direction flips.** pI is **increased** in detected ncORFs relative to undetected ones, while **detected canonical proteins show the opposite pattern** — lower pI than undetected canonical proteins. Same panel, same test, opposite signs.

That flip is the most misreadable result in Fig. 3. Skim it as "basic sequences are easier to detect" and you have the canonical half backwards.

A hypothesis, offered as one: pI proxies basic-residue content, and basic residues do opposite things in the two assays. In a tryptic digest, K and R *are* the cleavage sites, so a K/R-rich protein is chopped into fragments skewing below the identifiable length window — under-detection of high-pI proteins. In class-I presentation, several common alleles favour basic anchor residues, so basic sequences yield more bindable substrings. That allele-preference claim is `unverified` here; the panel bearing on it is Extended Data Fig. 6a,b, which compares NetMHCpan rank between detected and undetected 9-mers across the 154 alleles associated with ncORF peptides. Read those before believing the story.

One thing to check rather than assume: the Methods never say *which build* defines "detected" for canonical proteins in Fig. 3a. Fig. 3's title places the figure in the HLA build, and the Methods say canonical proteins were categorized by the same rule as ncORFs, so the consistent reading is that 15,581 of 20,326 is canonical-proteome coverage *by immunopeptidomics*. If so, the 24.6% versus 76.7% contrast is a **same-assay** contrast, which makes it stronger: the same no-enzyme search over the same spectra reaches three-quarters of the canonical proteome and a quarter of the ncORFs. Confirm the build before quoting 76.7% as tryptic coverage.

### The C-terminal enrichment

Fig. 3c plots where within its source sequence each detected peptide sits: distance from start codon to peptide start (42,787 CDS peptides; 2,344 ncORF peptides) and distance from peptide end to last residue (33,095 CDS peptides; 2,199 ncORF peptides).

The result: **the C-terminal parts of microproteins are preferentially sourced for HLA presentation, more strongly than for canonical proteins — 20.3-fold versus 7.2-fold, P = 9.8 × 10⁻⁹, Fisher's exact test.**

**The authors' explanation**: the preference probably results from fewer cleavages being required to process peptides from the termini. Mechanistically sensible. An interior ligand needs two proteolytic events; a ligand ending at the ORF's own stop-defined final residue needs one — and recall it is the *C terminus* the proteasome supplies, with the N terminus trimmed later by ERAP1/2. The terminal case is the cheap case.

**A competing explanation, and it is the strong one: length.** Enrichment is measured as distance to the terminus in absolute residues, and ncORFs are short while canonical CDSs are not. In a 30-residue ncORF *every* 9-mer sits within 22 residues of the C terminus; in a 500-residue CDS almost none do. A fixed-residue window captures a far larger fraction of a short sequence. This does not merely offer an alternative account — it specifically predicts that ncORF enrichment should *exceed* CDS enrichment, which is the very contrast 20.3× versus 7.2× rests on.

**A third: initiation heterogeneity.** If the annotated start codon is often not the codon used — plausible for ncORFs, where near-cognate and downstream initiation are common — the annotated N-terminal region may not exist in the real product, showing up as N-terminal depletion masquerading as C-terminal enrichment.

**Measurements that would separate them**, neither needing new data:

- **The decisive test for length**: recompute the contrast using **fractional** position along the sequence instead of absolute residues, and/or length-match the canonical set to the ncORF distribution. If 20.3× versus 7.2× collapses toward parity, the excess was length. This is a reanalysis of Supplementary Tables 9 and 10.
- **The test for the processing story**: split ncORF ligands into those ending *exactly* at the ORF's final residue and those ending internally. Under "fewer cleavages" the exactly-terminal class should be over-represented and — because no proteasomal cut made that C terminus — should *not* show the proteasome's cleavage-site residue preferences there, whereas the internal class should. That discriminates against both alternatives at once, and the same data answers initiation heterogeneity if you also ask whether the N-terminal panel of Fig. 3c shows outright depletion relative to the interior.

### RNA expression: statistically overwhelming, practically small

RNA expression was significantly higher for detected than undetected microproteins: **14.3 FPKM versus 10.7 FPKM, P = 1.1 × 10⁻²³, two-sided Wilcoxon rank-sum** (Fig. 3d; Extended Data Fig. 6e,f). Expression is the mean GTEx FPKM of the *gene* carrying the ncORF, across tissues excluding testis, with 326 ncORFs dropped for having no GTEx gene ID.

Now the arithmetic the paper does not do. The ratio of means is 14.3/10.7 = **1.34**; the absolute difference is 3.6 FPKM. Against that, P = 10⁻²³.

Both are true and they answer different questions. The P value answers "is the difference exactly zero?" — no, and with roughly 6,900 ncORFs in the comparison it would take a remarkably small difference to look like zero. The effect size answers "could I predict detectability from expression?" — essentially no. Look at the box plots rather than the P value: the interquartile ranges overlap almost completely. Expression is a real determinant and a useless classifier.

Extended Data Fig. 6f makes the point unintentionally: it repeats the comparison split by tissue, and the caption reports that **all** comparisons were significant. Uniform significance across dozens of strata is a statement about sample size, not biology — a diagnostic that the test is saturated, not thirty independent confirmations.

You know this failure mode from your own bench: a pseudobulk contrast with tens of thousands of cells returns underflowing P values for log2 fold changes of 0.05, which is why you gate on effect size as well as adjusted P. Same statistics, same fix. This is one analogy from your work that does not break anywhere.

Two bookkeeping notes before you quote this panel. Fig. 3d labels its groups `Detected (n = 1,796)` and `Undetected (n = 5,140)`, while the Extended Data Fig. 6f caption gives 1,796 and 5,142. The reconciling pair is 1,796 + 5,142 = 6,938 = 7,264 − 326, which also reconciles against Fig. 3a: 1,867 − 1,796 = 71, 5,397 − 5,142 = 255, and 71 + 255 = 326. So `5,140` looks like a slip in the panel. Separately, the running text gives P = 1.1 × 10⁻²³ where the Fig. 3d panel prints P = 1.076 × 10⁻²² — a one-order-of-magnitude disagreement. Nothing in the argument turns on it, but notice that you found it, and quote the text value with the discrepancy attached.

### Tissue differences, and what does not explain them

Using the HLA Ligand Atlas (reference 22), Fig. 3e compares the proportion of ncORF-derived to CDS-derived HLA-I peptides per tissue: **837 ncORF-derived peptides against 118,701 canonical**, across roughly thirty tissues, Fisher's exact with Holm–Bonferroni. Three tissues reach significance:

| Tissue | Change in ncORF peptide share | P |
|---------|-------|-------|
| Stomach | −0.6% | 1.7 × 10⁻⁴ |
| Spinal cord (myelon) | +0.8% | 1.9 × 10⁻³ |
| Uterus | +3.1% | 0.029 |

Read the internal logic before the biology. The **largest** effect (uterus, +3.1%) has the **weakest** P; the smallest (stomach, −0.6%) has the strongest. That inversion is entirely about how many peptides each tissue contributed. The authors call all three modest and say they *may* point to tissue-specific regulation of ncORF translation and presentation — an appropriate hedge.

The interesting result is negative: **these tissue differences were not explained by differences in RNA transcript expression** (Extended Data Fig. 6h, comparing GTEx expression for 224 of the 277 genes contributing ncORFs to the HLA Ligand Atlas). Whatever varies between tissues is downstream of transcript abundance — translation rate, degradation rate, proteasome composition, donor allele frequencies, or sampling. The paper does not distinguish among these, and neither should you.

Note the denominator: 837 peptides is the *entire* healthy-tissue immunopeptidome evidence base for ncORFs here. Keep it in mind below.

## Binder prediction, concordance, and one classifier to distrust

### NetMHCpan, and what the concordance actually shows

The logic here is genuinely clever and worth learning as a general technique.

Predictions used **NetMHCpan v4.1** (reference 72) for MS runs with a known four-digit HLA typing. A peptide counts as a binder if its **percentage rank score is ≤ 2** (Methods; the running text writes `<2%`). Nine runs were unpredictable because `A24:01`, `B43:01` or `C12:01` were unknown to the tool. HLA types were curated for **4,870 of 6,479 HLA-I MS runs** (Supplementary Table 8), covering the **2,711 of 3,116** ncORF peptides inside the required 8–12 aa window.

- **4,308 of 4,870 (88.5%)** analysed HLA-I MS runs had more than 70% of detected HLA-I peptides predicted as binders (Fig. 2i, plotted for 4,869 runs — one outlier with a 22.75 aa mean peptide length is not shown).
- ncORF peptides were **as likely as canonical peptides** to be predicted binders against the annotated type (Fig. 2j, n = 90 datasets).
- Grouping samples by 493 HLA typings crossed with 4 sample types (531 combinations), concordance between prediction and detection was **94.8% — 10,150 predicted binders against 553 negative predictions (5.2%)** — holding **across ORF biotypes and independent of source material**, cancerous or non-malignant, cell line or tissue (Fig. 2k). The two counts sum to 10,703, so the percentages reconcile.

Why this is a strong check: a false PSM has no reason to carry the binding motif of *the particular alleles that particular donor happened to have*. If the 3,116 peptides were largely search artefacts they would show no per-sample allele concordance. They do. This is orthogonal validation of a different kind than target–decoy, and it is the best single argument in the paper that these identifications are real.

Three limits to state alongside it:

- **It validates the peptide, not the gene.** Allele-appropriate motifs say a real HLA ligand was sequenced. They say nothing about whether the source ORF encodes a stable protein, or whether presentation occurred in a healthy cell.
- **Prediction and observation are not fully independent.** NetMHCpan-4.1's own title advertises integration of MS eluted-ligand data, so a model partly trained on immunopeptidomics is validating immunopeptidomics. Not fatal — the per-sample allele specificity still carries information — but it should temper the weight the 94.8% bears.
- **Every peptide gets an allele.** The Methods assign each peptide to the allele with the lowest predicted rank *irrespective of whether that rank is below 2*. So 94.8% is a statistic over (peptide, typing) pairs under forced assignment, not a per-peptide pass rate.

### The MLP classifier: read the Methods, then set it aside

The Methods describe two machine-learning models. Both deserve scepticism, and the reason is what the Methods omit.

The **MLP classifier**: 677 ncORF peptide sequences of 9 amino acids, each with 22 attributes; 80/20 train/test split, `random_state = 42`, `StandardScaler`, scikit-learn v1.5/1.6, `max_iter = 8000`, grid search with cross-validation over hidden layer sizes `(280)`, activation `tanh`, alpha `0.01`. Then: *"The performance of the model was assessed using standard evaluation metrics to determine its predictive capabilities."*

That sentence is the entire performance report. The Methods **do** give architecture, split, preprocessing, hyperparameters, library versions and a code location (`https://git.embl.de/ivfimo/machine_learning_scripts`). They **do not** give accuracy, AUC, precision, recall, a confusion matrix, a baseline to beat, or the class balance of the 677.

Add three observations of your own. The hyperparameter "grid" as printed holds exactly one value per parameter, so nothing was searched. A 280-unit hidden layer over 22 features is roughly 6,400 first-layer weights fitted on about 541 examples. The held-out test set is about 136 examples, on which no metric is reported.

A second model, a **TensorFlow Keras** network, is specified in more architectural detail — 7,264 ncORF sequences, 43 attributes, balanced class weights for the 1,785-versus-5,479 imbalance, ReLU and L2 with batch normalization and dropout, sigmoid output, Adam at 0.001, 60 epochs — and reported no better: again no accuracy, no AUC, no baseline.

The decisive observation is where these models appear. **Neither is mentioned in the main-text Results. Neither appears in any main figure. Neither is used in tier assignment.** They live in the Methods and the Code Availability statement — and agenda question 7 asks whether deep learning *should* inform annotation, posing it as an open community question rather than reporting a delivered tool.

The right conclusion is not "the models are bad" — you cannot know that from what is reported. It is that **nothing in this paper's conclusions rests on them**, and that you should not cite them as evidence that HLA detectability is predictable from sequence. Absent a number, treat them as exploratory; the Supplementary Results and the repository are where to look.

## The sample-type confound

The hard number, from agenda question 3: **2.36 billion of 3.53 billion MS2 spectra searched in the non-HLA PeptideAtlas — 66.9% — are from cancer tissue or cancer cell line samples.** The consortium's gloss: proteins supported by such data are potentially cancer-specific products, which has implications for their annotation as peptideins.

Be careful with scope. That statistic is stated for the **non-HLA build**. The paper gives no equivalent single percentage for the HLA build; it characterises immunopeptidome sample type categorically instead — Fig. 2k crosses cancer/non-cancer with cell line/non-cell line, and Extended Data Fig. 5e,f splits peptides by whether they were found exclusively in cancer samples, exclusively in non-cancer samples, or both. Do not transfer 66.9% to the immunopeptidome. What you *can* say is that the healthy-tissue reference contributed 837 ncORF-derived peptides — a small base.

What the paper does establish is that the confound is about **provenance, not detectability**: no significant difference in microprotein detectability between cancer and non-cancer HLA datasets; no influence of peptide mass, hydrophobicity or isoelectric point on the cancer/non-cancer distribution; no significant change in ORF biotype recovery between sample types (Extended Data Fig. 5e,f). The assay is not biased *by* cancer in any way they could detect. The problem is that annotation is a claim about human physiology, and most of the world's proteomics data comes from cells that are not behaving physiologically.

The consequence is blunt. Of the 15 Tier 1A candidates prioritized for potential annotation (Fig. 5c, coordinate-verified: 15 = 3 + 2 + 10):

| Outcome | n |
|---------|-------|
| Now annotated as protein-coding by GENCODE | 3 |
| Unclear evolutionary constraint beyond primates | 2 |
| **High-quality peptide evidence only from cancer/cell line samples** | **10** |

**Ten of fifteen.** Two-thirds of the losses at the final gate were not about whether the molecule exists, but about where it was seen.

Agenda question 3, in the consortium's framing: *should peptides detected in cancer samples or immortalized cell lines support protein-coding gene annotation?* Both sides are real. Requiring healthy-tissue evidence gates annotation on a minority of available data and will systematically miss anything expressed under stress — including, by the DRiP logic above, a plausible fraction of exactly what this assay finds best. Not requiring it means reference annotation absorbs cancer-specific products as human genes, propagating into every downstream GTF, panel and target list. Do not resolve it here; take a position in [Module 8](08-tier-framework-synthesis.md), after seeing what the tier system does with it.

## The asymmetry that makes "peptidein" necessary

Three claims that sound like one:

1. **The molecule is synthesized.**
2. **It is synthesized in normal physiology.**
3. **It does something.**

HLA presentation speaks to each completely differently.

**On synthesis, HLA evidence is strong.** Consider what a peptide must survive to be identified: a ribosome made the polypeptide; it entered the cytosolic degradation pool; the proteasome cut it to a compatible C terminus; TAP transported it; ERAP trimmed it; it bound an allele whose motif it happened to match; the complex reached the surface; enough copies accumulated for immunoaffinity capture; the spectrum passed a 0.0041% peptide-level FDR and, for the inspected subset, a human reviewer. Each step is a filter a spurious sequence has no way to pass. Layer per-sample allele concordance on top and the case that these molecules are made is about as good as a detection argument gets.

**On stability, read very carefully.** Presentation is *weak* evidence against stability — and not evidence *of* instability either. Every protein is degraded eventually; presentation only requires that some copies were. What tilts the inference toward instability is not presence in the immunopeptidome but the **contrast**: absent from the tryptic proteome *and* present in the immunopeptidome is the pattern expected of a low-standing-pool, high-turnover product. That is the 1,684 HLA-only ncORFs.

But the contrast is not clean, and the paper says so about its own flagship promotion: some HLA-detected ncORFs lack tryptic evidence *for either technological or biological reasons, such as the small size or amino acid composition of their encoded microproteins*. Technological, meaning the peptide was never identifiable — too few K/R sites, fragments too short, poor ionization. Biological, meaning the protein was not there to find. Both produce an identical HLA-only signature, and this paper does not separate them. Add that no direct stability measurement is offered and that Extended Data Fig. 10 shows pLDDT confounded by length and passed by shuffled sequences, and the correct statement is narrow: **HLA-only detection is consistent with instability and equally consistent with a detectability failure, and this paper cannot tell you which.**

**On function, HLA evidence counts for nothing — as policy, not biology.** Agenda question 5 states it flatly: *immune recognition of a peptide is not currently considered a biological function by annotation projects.* Sit with how strange that is. An ncORF product can be synthesized, degraded, processed, presented on the cell surface, recognized by T cells and pursued as an immunotherapy target — the paper cites references 41–43 for exactly that — and still fail the function test that gates a gene record.

Not an oversight. It follows from what annotation has historically meant: a protein-coding gene is one whose protein *does something for the organism*. Being visible to the immune system is something that happens *to* the molecule, not something the molecule does. Whether that should change is the question the consortium hands to its own field.

That gap — claim 1 established, claim 2 uncertain, claim 3 unreachable — is exactly the region `peptidein` was invented to name. Before it, an ncORF in that state had no representation: either a protein-coding gene or absent. The Discussion's definition is the gap in words: a translation product confidently detected endogenously, but for which a role in normal physiology cannot be verified at the present time, explicitly including potentially transient products of cellular stress or defective ribosome translation. 121 initial peptidein annotations follow (Supplementary Table 12).

## Analogies from your own bench, and where they break

### poly(A) selection as a capture reagent

**Where it fits.** Both assays see molecules only through a capture chemistry with target-dependent efficiency; in neither case is absence evidence of absence, and in neither does signal translate linearly into abundance. Your instinct to ask "what could this chemistry not have captured?" is the right instinct here.

**Where it breaks, and it breaks hard.** poly(A) bias is approximately **uniform across a library**. Every transcript, in every cell, in every sample meets the same oligo-dT and the same 3′ bias — which is why it largely cancels in a differential comparison and why you can reason about it once, globally, and move on.

HLA bias is **per sample**. Each donor carries up to six classical class-I alleles with distinct motifs, so the set of peptides that *can* be presented differs between samples; two runs on the same cell type from different donors interrogate partly non-overlapping peptide spaces. There is no poly(A) analogue of "this molecule was invisible in this sample because this donor lacked the allele that would have presented it."

Which is why the paper models binding **per MS run** rather than once globally: HLA types curated for 4,870 of 6,479 HLA-I runs, NetMHCpan run against each run's own four-digit typing, concordance tabulated across 493 distinct typings. That whole apparatus exists because the bias does not cancel. A poly(A) workflow needs no per-sample capture model; this one cannot work without one.

### A CITE-seq antibody panel, or a Xenium probe panel

**Where it fits.** Closer than poly(A). A panel defines what you can see; a target not on the panel returns zero however abundant it is, and you would never report "gene X is absent" from a 300-plex panel lacking a probe for it.

**Where it breaks.** You *designed* the CITE-seq panel — you have the list, you validated each clone, you know what is missing. Here the panel is the donor's HLA genotype: you did not choose it, it differs per sample, it is only partly recorded (1,609 of 6,479 HLA-I runs have no curated typing at all), and per-target "capture efficiency" is a *prediction* — a NetMHCpan percentile rank — not a validated reagent QC. A spatial panel whose probe list was drawn at random per sample, documented for three-quarters of your sections, with per-probe sensitivity from a neural network: that is the position immunopeptidomics is in, and the concordance analysis is the field's best available substitute for panel QC.

### The hard stop, with no clean analogue

**No single-cell assay uses a degradation product as evidence of synthesis.** Mark this as a place where transfer from your methods stops entirely.

3′ and 5′ gene expression, scATAC, Visium and Xenium all sample either the molecule you care about or its cognate DNA. The nearest thing in your world runs the other way — inferring a transcript existed from fragments in the ambient background — and that is a contaminant you *remove*; this paper's own scRNA-seq work corrects ambient RNA with SoupX before analysis. Degraded, misassigned material is noise to be subtracted.

Immunopeptidomics inverts the sign: the fragment on its way to being destroyed **is** the primary evidence, and it is evidence of a specific, cell-authored process rather than of leakage. There is no analogy to port and no intuition to adapt; reaching for one will mislead you.

One related trap, because it is the tempting shortcut: *"HLA-I purification is an enrichment step, so immunopeptidomics is just more sensitive proteomics."* No. An enrichment concentrates the standing pool — more of the same quantity. HLA presentation samples flux through degradation, which can be large when the standing pool is near zero. The difference between these assays is not sensitivity. It is measurand.

## What I now trust, and why

Write this in your own words before moving on. Anchors, all positive claims:

- **The 3,116 HLA peptides are real molecules.** The strongest reason is not the FDR — it is that they carry the binding motifs of the specific alleles the specific donors happened to have, at 94.8% concordance across 493 typings and every sample type. A search artefact has no mechanism for that. Add Ribo-seq validation in 613 of 691 inspected ncORFs and the identifications hold.
- **Immunopeptidomics measures a different physical quantity from digest proteomics**, not the same quantity better: standing pool versus degradative flux. That single distinction explains the 24.6% versus 2.5% yields, the overlap of only about 101 ncORFs, the enrichment for unstable products, and why running both windows was the right design.
- **The headline is carried by immunopeptidomics, and the paper says so.** 1,785 of 1,867 detected ncORFs — 95.6% — come from this assay. The response was to keep MS and HLA in separate columns, create Tier 1B for HLA-only support, promote `c2riboseqorf47` on HLA evidence explicitly, and pose the legitimacy of doing so as agenda question 2. That is a project reasoning in the open about the limits of its own evidence.
- **Detection determinants are real but weak.** Length matters most and matters mechanically. pI matters, in opposite directions for ncORFs and canonical proteins. Expression matters at a ratio of 1.34 with P = 10⁻²³ — the module's cleanest lesson in reading effect size and P value as answers to different questions.
- **Three claims are separable, and naming them separately is the durable skill.** The molecule is made; it is made in normal physiology; it does something. HLA data establishes the first powerfully, addresses the second only through sample provenance, and — as annotation policy stands — cannot touch the third. `peptidein` is the word for that configuration, useful precisely because it refuses to collapse the three.
- **Where to stay uncertain, in good company:** whether HLA-only detection indicates genuine instability or merely tryptic invisibility (the paper cannot separate these); whether the C-terminal enrichment survives length-matching; and whether cancer-and-cell-line evidence should support a gene record. The consortium is uncertain about the last one too — that is why it is question 3.

## Self-check

- [ ] Explain in two sentences why an unstable protein can be bright in the immunopeptidome and invisible in a tryptic digest, in terms of standing pool versus flux
- [ ] Trace a peptide from cytosolic polypeptide to mass spectrum, naming the proteasome, TAP, ERAP and the peptide-loading complex, and say which terminus each step sets
- [ ] Reproduce the decomposition of "about 25%" — 1,785 / 183 / 101 / 1,867 — and state what the abstract would have said without immunopeptidomics
- [ ] Say why no-enzyme mode costs about 5× rather than about 200× against the search this paper actually used for the other build, and name the second cost that database size alone does not capture
- [ ] State the isoelectric-point result for ncORFs *and* for canonical proteins, with the directions right
- [ ] Give the authors' explanation for the 20.3-fold C-terminal enrichment, the length-artefact alternative, and one reanalysis that would distinguish them
- [ ] Quote 14.3 versus 10.7 FPKM with its P value, then explain why it is a determinant and not a classifier
- [ ] Say what the Methods report and do not report about the MLP classifier, and where in the paper its results appear
- [ ] Argue agenda question 3 from both sides using 66.9% and 10-of-15, then name the data that would move you
- [ ] Explain why HLA presentation is strong evidence of synthesis and weak evidence against stability, without over-claiming in either direction
- [ ] State the poly(A) analogy and its breakage in one sentence each, then state the hard stop

## Concept tracker

| Concept | Understood? | Notes |
|---------|-------------|-------|
| Class-I pathway: proteasome → TAP → ERAP → PLC → surface | | |
| Immunopeptidome as proteasome output, not standing proteome | | |
| DRiPs, and the BAG6 explanation for HLA-without-tryptic | | |
| No-enzyme search: space, statistical power, spectrum character | | |
| 3,116 peptides → 1,785 ncORFs (24.6%); HLA-I only 94.3% | | |
| 61.3% of detected ncORFs rest on a single peptide | | |
| The decomposition: 1,785 / 183 / 101 / 1,867 | | |
| Why Fig. 5 separates the MS and HLA columns | | |
| Fig. 3a: length, hydrophobicity, pI — and the pI direction flip | | |
| C-terminal enrichment: 20.3× vs 7.2×, and the length confound | | |
| Statistical versus practical significance in Fig. 3d | | |
| NetMHCpan concordance — what it proves, and its circularity | | |
| Why the MLP classifier carries no weight | | |
| Sample-type confound: 66.9%, and 10 of 15 blocked | | |
| Synthesis / normal physiology / function as three claims | | |

Next: [Module 6](06-evolution-orbl.md). ORBL asks whether these same ncORFs look conserved, and Fig. 4e compares ORBLq between HLA-detected and undetected ncORFs — so this module is its prerequisite too.
