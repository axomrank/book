# Book 1 research library

Research pass dated 11 October 2026. **15 consulted source records, 7 downloaded PDFs, 78 local visual assets, 12 chapter dossiers and 60 mapped research divisions.**

This is an initial evidence and acquisition pass, not exhaustive research or manuscript clearance. Every chapter has an evidence request; several central questions remain unanswered. No manuscript prose has been written.

## Browse

- [Offline research webpage](web/index.html): open in a browser; no installation or internet needed for local assets. External source links need internet.
- [Chapter dossiers](chapter_dossiers.md), [sources](source_register.json), [claims](claim_register.json), [media and rights](media_register.json), [research leads](research_leads.json).
- [PDF acquisition log](downloads.json) and [photograph acquisition log](media-downloads.json) preserve successes and failures. Original downloads have SHA-256 hashes.

## Evidence rules

Keep archaeological sample dates, inferred occupations and regional parallels distinct. Trace dates to original methods. Treat historic Assam boundaries separately from the present state. Do not infer domesticated rice from tools alone, a trade route from similar celts, or an Assam jar age from Laos. Modern ceremonial practices and modern photographs require explicit context labels.

## Assets and rights

Original report-page facsimiles preserve captions and context. Commons licenses and credits are preserved with each photograph. Many journal and official illustrations require publication permission; public access does not establish reuse clearance. This private research library is not an approved book illustration package. No asset has been marked publication-ready.

## Acquisition and review limits

Restricted articles, the IITG login response, certificate failure, publisher protection and timeouts are recorded rather than replaced with guessed full-text findings. Downloads and reading are separate statuses. Review the specific locator on each source; scanned pages and selected sections do not amount to a complete reading of every document.

## Before drafting

Acquire original Daojali field/artefact records and the new reconnaissance report; resolve Sarutaru season discrepancies; inspect the 2024 AMS sample table; locate direct plant/animal evidence and Assam jar dating; check laboratory and material provenance; clear selected illustrations. Update claims and division-level evidence before starting chapter prose.

The page is local-only. Do not publish the collected permission-unverified assets as a public website.

## Additional registers

- [Site gazetteer](site_register.json): eleven named sites or research areas, with present geography and context limits.
- [Dating register](dating_register.json): methods, samples, locators and deliberately unconverted dates.
- [Programmatic validation](VALIDATION.json): hashes, file formats, image decoding and local dependencies checked without errors.

To rebuild the catalogue after changing the evidence or acquisition records, run `python3 research/scripts/build_catalogue.py` from the Book 1 folder. The webpage also opens directly as `research/web/index.html`; no server is required.

## Standalone photo expansion

Added 34 standalone photographic and figure assets, plus a higher-resolution replacement for the existing jar survey map. Includes eleven JNA stone-jar photographs; Marakdola menhirs, deposits, test pit, charcoal sampling, celts and potsherds from the newly acquired thesis; Daojali photographs; and the 2022 jar survey figures. Sarutari’s modern sign is orientation context, not proof of relocation of the original Sarutaru excavation.
