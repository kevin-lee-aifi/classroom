# Key References

Background reading for the [learning plan](../notes/learning-plan.md), grouped by the module each supports. Every entry below is transcribed from the reference list of the paper itself (DOI [10.1038/s41586-026-10459-x](https://doi.org/10.1038/s41586-026-10459-x)) — that is, from a retrieved source rather than from recall. Volume and page numbers are as printed there. Where no stable link is given, none was available in the source; look the item up by title rather than trusting a constructed DOI.

## Read these first

If you only read three things before starting, read these.

- Prensner, J. R. *et al.* What can ribo-seq, immunopeptidomics, and proteomics tell us about the non-canonical proteome? *Mol. Cell. Proteom.* **22**, 100631 (2023). — The single best orientation to the three evidence types this paper integrates, by one of its corresponding authors.
- Mudge, J. M. *et al.* Standardized annotation of translated open reading frames. *Nat. Biotechnol.* **40**, 994–999 (2022). — The TransCODE standards paper that defines the ncORF catalogue and biotype vocabulary this work builds on. Reference 4 of the paper.
- Deutsch, E. W. *et al.* Human Proteome Project mass spectrometry data interpretation guidelines 3.0. *J. Proteome Res.* **18**, 4108–4116 (2019). — The HUPO-HPP criteria themselves. Reference 15, and the standard that makes "Candidate protein" mean something in the tier table.

## Module 1–2 — the annotation problem and the ncORF catalogue

- Frankish, A. *et al.* GENCODE: reference annotation for the human and mouse genomes in 2023. *Nucleic Acids Res.* **51**, D942–D949 (2022).
- Chothani, S. *et al.* An expanded reference catalog of translated open reading frames for biomedical research. *Nucleic Acids Res.* **54**, gkag234 (2026).
- Chothani, S. P. *et al.* A high-resolution map of human RNA translation. *Mol. Cell* **82**, 2885–2899 (2022).
- Martinez, T. F. *et al.* Accurate annotation of human protein-coding small open reading frames. *Nat. Chem. Biol.* **16**, 458–468 (2020).

## Module 3 — Ribo-seq

- van Heesch, S. *et al.* The translational landscape of the human heart. *Cell* **178**, 242–260 (2019). — Reference 1; the corresponding author's own foundational ncORF translation dataset.
- Chen, J. *et al.* Pervasive functional translation of non-canonical human open reading frames. *Science* **367**, 1140–1146 (2020).
- Clauwaert, J. *et al.* Deep learning to decode sites of RNA translation in normal and cancerous tissues. *Nat. Commun.* **16**, 1275 (2025).

## Module 4 — mass spectrometry

- Wacholder, A. *et al.* Community benchmarking and evaluation of human unannotated microprotein detection by mass spectrometry based proteomics. *Nat. Commun.* **17**, 1241 (2026). — Directly on the question of how reliable microprotein MS detection actually is.
- van Wijk, K. J. *et al.* Detection of the Arabidopsis proteome and its post-translational modifications and the nature of the unobserved (dark) proteome in PeptideAtlas. *J. Proteome Res.* **23**, 185–214 (2024). — How a PeptideAtlas build is constructed and what its evidence categories mean.
- Deutsch, E. W. *et al.* The 2025 Report on the Human Proteome from the HUPO Human Proteome Project. *J. Proteome Res.* **25**, 539–555 (2026).
- Adams, C. *et al.* Fragment ion intensity prediction improves the identification rate of non-tryptic peptides in timsTOF. *Nat. Commun.* **15**, 3956 (2024).
- Declercq, A. *et al.* TIMS2Rescore: a data dependent acquisition-parallel accumulation and serial fragmentation-optimized data-driven rescoring pipeline based on MS2Rescore. *J. Proteome Res.* **24**, 1067–1076 (2025).
- Bouwmeester, R. *et al.* DeepLC can predict retention times for peptides that carry as-yet unseen modifications. *Nat. Methods* **18**, 1363–1369 (2021).

## Module 5 — immunopeptidomics

- Caron, E., Aebersold, R., Banaei-Esfahani, A., Chong, C. & Bassani-Sternberg, M. A case for a Human Immuno-Peptidome Project Consortium. *Immunity* **47**, 203–208 (2017). — What HUPO-HIPP is for.
- Ouspenskaia, T. *et al.* Unannotated proteins expand the MHC-I-restricted immunopeptidome in cancer. *Nat. Biotechnol.* **40**, 209–217 (2022).
- Chong, C. *et al.* Integrated proteogenomic deep sequencing and analytics accurately identify non-canonical peptides in tumor immunopeptidomes. *Nat. Commun.* **11**, 1293 (2020).
- Marcu, A. *et al.* HLA Ligand Atlas: a benign reference of HLA-presented peptides to improve T-cell-based cancer immunotherapy. *J. Immunother. Cancer* **9**, e002071 (2021). — The healthy-tissue counterpart to cancer immunopeptidome data, and directly relevant to agenda question 3.
- Cuevas, M. V. R. *et al.* Most non-canonical proteins uniquely populate the proteome or immunopeptidome. *Cell Rep.* **34**, 108815 (2021). — The prior observation that the two windows barely overlap.
- Kesner, J. S. *et al.* Non-coding translation mitigation. *Nature* **617**, 395–402 (2023). — BAG6-mediated degradation of non-canonical translation products.
- Yewdell, J. W. & Hollý, J. DRiPs get molecular. *Curr. Opin. Immunol.* **64**, 130–136 (2020). — Defective ribosomal products.
- Laumont, C. M. *et al.* Noncoding regions are the main source of targetable tumor-specific antigens. *Sci. Transl. Med.* **10**, eaau5516 (2018).
- Abelin, J. G. *et al.* Workflow enabling deep-scale immunopeptidome, proteome, ubiquitylome, phosphoproteome, and acetylome analyses of sample-limited tissues. *Nat. Commun.* **14**, 1851 (2023).

## Module 6 — evolution

- Lin, M. F., Jungreis, I. & Kellis, M. PhyloCSF: a comparative genomics method to distinguish protein coding and non-coding regions. *Bioinformatics* **27**, i275–i282 (2011). — Reference 24; the prior art ORBL is designed to complement.
- Sandmann, C.-L. *et al.* Evolutionary origins and interactomes of human, young microproteins and small peptides translated from short open reading frames. *Mol. Cell* **83**, 994–1011 (2023).
- Broeils, L. A., Ruiz-Orera, J., Snel, B., Hubner, N. & van Heesch, S. Evolution and implications of de novo genes in humans. *Nat. Ecol. Evol.* **7**, 804–815 (2023).
- Carvunis, A.-R. *et al.* Proto-genes and de novo gene birth. *Nature* **487**, 370–374 (2012).
- Keeling, D. M., Garza, P., Nartey, C. M. & Carvunis, A.-R. The meanings of function in biology and the problematic case of de novo gene emergence. *eLife* **8**, e47014 (2019). — Read alongside agenda question 4; it is the conceptual dispute the paper is careful not to settle.
- Whited, A. M. *et al.* Biophysical characterization of high-confidence, small human proteins. *Biophys. Rep.* **4**, 100167 (2024).

## Module 7 — function

- Prensner, J. R. *et al.* Non-canonical open reading frames encode functional proteins essential for cancer cell survival. *Nat. Biotechnol.* **39**, 697–704 (2021).
- Sanson, K. R. *et al.* Optimized libraries for CRISPR-Cas9 genetic screens with multiple modalities. *Nat. Commun.* **9**, 5416 (2018). — The Calabrese CRISPRa library reanalysed here.
- McFarland, J. M. *et al.* Multiplexed single-cell transcriptional response profiling to define cancer vulnerabilities and therapeutic mechanism of action. *Nat. Commun.* **11**, 4296 (2020). — Reference 32; the multiplexed scRNA-seq approach behind Fig. 6i,j.
- Funk, L. *et al.* The phenotypic landscape of essential human genes. *Cell* **185**, 4634–4653 (2022).
- Chang, L., Ruiz, P., Ito, T. & Sellers, W. R. Targeting pan-essential genes in cancer: challenges and opportunities. *Cancer Cell* **39**, 466–479 (2021). — What "pan-essential" does and does not imply.
- Comtois, F. *et al.* Non-canonical altPIDD1 protein: unveiling the true major translational output of the PIDD1 gene. *Life Sci. Alliance* **8**, e202402910 (2025). — Reference 26; the `c11riboseqorf4` / PIDD1 uoORF, one of the three newly annotated genes.

## Module 8 — clinical and genetic stakes

- Ely, Z. A. *et al.* Pancreatic cancer-restricted cryptic antigens are targets for T-cell recognition. *Science* **388**, eadk3487 (2025).
- Huang, D. *et al.* Tumour circular RNAs elicit antitumour immunity by encoding cryptic peptides. *Nature* **625**, 593–602 (2024).
- Barczak, W. *et al.* Long non-coding RNA-derived peptides are immunogenic and drive a potent antitumour response. *Nat. Commun.* **14**, 1078 (2023).
- Whiffin, N. *et al.* Characterising the loss-of-function impact of 5′ untranslated region variants in 15,708 individuals. *Nat. Commun.* **11**, 2523 (2020). — Why uORF variants matter in human genetics.
- Hofman, D. A. *et al.* Translation of non-canonical open reading frames as a cancer cell survival mechanism in childhood medulloblastoma. *Mol. Cell* **84**, 261–276 (2024).

## Data and tools from the paper

| Resource | Location |
|---------|-------|
| **ncORF PeptideAtlas build** | https://peptideatlas.org/builds/human/#ncORFs |
| **Analysis code** | https://github.com/VanHeeschLab/deutsch_kok_et_al_2024 |
| **ORBL implementation** | https://github.com/iljungr/ORBL_tools |
| **CRISPR tiling screen analysis** | https://github.com/CFVALLS/tiling_screens_with_permutation |
| **Machine-learning scripts** | https://git.embl.de/ivfimo/machine_learning_scripts |
| **scRNA-seq raw data** | BioProject `PRJNA1294394` |
| **Annotation sources** | GENCODE, Ensembl Release 87, UniProtKB/Swiss-Prot 2023, NCBI RefSeq |

## A note on reuse

The paper is open access under CC BY-NC-ND 4.0. That licence permits non-commercial reproduction and sharing with attribution, but **not** the sharing of adapted material derived from the article. These notes are study material: they paraphrase and cite rather than reproduce, quote sparingly with attribution, and embed no figure panels. Read the figures in your own copy of the PDF — the notes are written to be used alongside it, not instead of it.
