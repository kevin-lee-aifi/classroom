# Extraction discipline

Rules for getting facts out of a source document without teaching something false. Every one of these was learned by getting it wrong first, on a real 47-page Nature paper, and each cost a correction round.

## There is no PDF tooling in these sandboxes

No `pdftotext`, no poppler/`pdftoppm`, no `pypdf`/`PyPDF2`. The `Read` tool **cannot render a PDF** — it fails with `pdftoppm is not installed`. Do not report a PDF as unreadable and do not try to install anything.

Use the bundled extractor:

```
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf flat   > flat.txt
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf placed > placed.txt
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf grep 'PATTERN' [CONTEXT_CHARS]
python3 .claude/skills/learn/scripts/pdfx.py FILE.pdf region YMIN YMAX 'SUBSTRING_IN_STREAM'
```

Read prose from `flat.txt`. Read **anything inside a figure** from `placed.txt` or `region`.

## The five rules

**1. Coordinates for anything inside a figure.** Flat reading order returns figure labels out of visual order and will silently transpose a table. This is not a theoretical risk: a first pass on a tier-assignment figure produced a confident, plausible, *fully transposed* table, with provisional and final columns swapped. The fix is `region`, which tracks the text matrix and rebuilds rows by y then x.

**2. Make figure numbers reconcile, or drop them.** A recovered table is trustworthy when its row sums, column sums and grand total all close. If a number cannot be reconciled, leave it out — do not hedge it into the curriculum. The transposed table above was caught precisely because its margins did not sum to the stated total.

**3. Never take an inequality direction from figure extraction.** Publishers remap glyphs onto C0 control codes per font subset, so the same byte is a different character in different runs. On the source paper, `\x1e` correctly meant `≤` in one run and `≥` inside another figure — where the extractor rendered the real criteria "≥2 peptides, ≥18 residues" as "≤2, ≤18". Get every `≥`/`≤` from prose or Methods.

**4. An extraction that finds nothing is a claim about the extraction, not about the document.** A confident correction was once issued stating a figure contained no arithmetic. It contained two worked fractions. Absence of a match means your pattern or your mode was wrong until proven otherwise.

**5. A number that reconciles is not a number you have understood.** The worst error of the session survived every arithmetic check. A figure reported 1,867 detected against 5,397 undetected, summing exactly to the catalogue total of 7,264 — so it looked like a union across two datasets. It was not. The figure was scoped to one dataset, and its Methods attributed the excess to items being counted more than once. Two different quantities can print identical digits. **Only the Methods say what a number counts.**

## Ligatures and glyph repair

The extractor's `repair()` handles the common cases: `fi`/`ff`/`ffi` ligatures dropped onto control bytes, cp1252 punctuation, superscript minus, primes, soft hyphens across line breaks, and running-header noise. Two things to know:

- Python's `\s` matches the C0 separators `\x1c`–`\x1f` that carry ligature glyphs, so any whitespace normalisation must happen **after** `repair()`, never before. `grep` mode had this backwards and silently returned "scienti c" for "scientific".
- Named diacritics and relational operators are font-dependent and are the residual risk. If a quoted passage looks odd, it is odd — re-extract before quoting.

## The verified-facts pattern

Before any module is written, produce two artefacts and hand both to every downstream agent:

- **A verified-facts block.** Every number and claim the curriculum will rest on, extracted and cross-checked, with the figure or section it came from. Agents work from this, not from their own recollection of the literature.
- **A corrections file that overrides it.** The facts block will be wrong. Mine was wrong three times — a search engine misattributed, a digestion protocol overstated, and one whole retracted item. Corrections must be able to supersede the brief without rewriting it, and downstream agents must be told which file wins.

State one standing rule in every brief: **cite the source or a retrieved URL for every factual claim, and mark anything from model memory as `unverified` inline.**

## Things that will not work

- `WebFetch` is egress-blocked for most scholarly domains in these sandboxes — `ncbi.nlm.nih.gov`, `sciencedirect.com`, `biorxiv.org`, `europepmc.org` and others. `WebSearch` works. So a citation may be honestly labelled from a search snippet rather than read in full; say so at the point of use, not in a footnote.
- Supplementary Information is usually **not** in the article PDF. If a claim depends on a supplementary table, say so rather than implying it was checked.
