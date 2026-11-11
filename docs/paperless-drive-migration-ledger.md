# Paperless / Google Drive migration ledger

This is a **status-only, non-sensitive** tracker. Do not store source document bodies, personal identifiers, tax numbers, amounts, private names or Paperless credentials here. Canonical operating model and safety gates: `docs/paperless-drive-migration-handoff.md`, ADR-013/014.

| Batch | Scope | Paperless status | Evidence | Drive source disposition | Follow-ups |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 income-tax wage certificates, tax years 2016–2023 (two separate periods in 2019) | **Complete, owner-confirmed 2026-11-10**: uploaded and processed; type `Bescheinigung`, tags `Steuer` and `Beruf`, two issuer groups, individual titles and document dates reviewed, OCR checked, `Inbox` removed | Owner's explicit confirmation in chat; **no direct Paperless API inventory/reconciliation** | Unchanged; retain source | Potential superseded 2019 certificate and unreadable 2017 candidate held out; check missing 2021 January–September certificate and an additional wage certificate from a later folder inspection. Backup after batch 1 not verified. |
| 2A | 9 tax-return PDFs, tax years 2016–2024 | **Complete, owner-confirmed 2026-11-10:** uploaded, type `Steuererklärung`, tag `Steuer`, no correspondent, titles/document dates reviewed, OCR checked, `Inbox` removed | Owner's explicit chat confirmation; **no Paperless API inventory/reconciliation or proof of tax submission** | Unchanged; retain source | Successful post-import backup not independently verified. |
| 2B | Income tax assessment notices (paper originals) | **Owner plans to locate and scan on iPhone; none imported or counted yet** | Owner decision in chat 2026-11-10 | Paper originals preserved | For each notice, use existing `Bescheid` type, `Steuer` tag, actual issuing tax office, document issue date and tax year; preserve relevant amended notices separately. |
| 3 | Insurance documents in `02_Areas/Finances/Versicherungen` | **Complete, owner-confirmed 2026-11-10:** 2 documents (liability policy endorsement and historical health-insurance certificate), individual title/date/correspondent/type/tags checked, OCR reviewed, `Inbox` removed | Explicit owner report in chat; no direct Paperless API reconciliation | Unchanged; retain source | Insurance remainder in batch 3B; post-import backup not verified. |
| 3B | Remaining insurance records in Drive | **Zurich item complete; one Bosch BKK cancellation confirmation uploaded, NOT YET classified; other legacy files deferred pending relevance review** | Owner confirmed Zurich closure, content-identity of two Bosch BKK cancellation PDFs, and upload of one copy on 2026-11-11; no independent Paperless API check | Unchanged | Finish classification of already-uploaded Bosch BKK document (title, actual issue date, issuer, type, tags, OCR, Inbox). Do not import the second copy. Other historic premium bill/device annex deferred under selective policy. |

## Migration scope change — 2026-11-11 (owner direction)

- **Selective archive, not exhaustive Drive migration.** Prioritize ongoing/active obligations, legally or financially important evidence, tax decisions and records still potentially needed, relevant contracts and warranties, open disputes or claims, and hard-to-replace documents. For old documents, ask whether there is a realistic future reason to retrieve the record. Age alone is not the criterion, but no historic file is imported merely to complete a folder.
- **Forward-first intake:** prioritize reliable capture of new invoices and documents (mobile, web, email), and selectively backfill high-value legacy evidence. Leave irrelevant, duplicate, expired routine paperwork, and low-value historic administration in Drive; no deletion without the usual reconciliation/backup/owner-approval gate.
- Earlier recommendations to automatically import the Bosch BKK cancellation duplicate, 2017 premium bill, historical device annex etc. are **withdrawn pending relevance review**. The Bosch BKK files are content-identical per owner review, but need not enter Paperless at all if no practical future use. No already imported documents are to be deleted automatically.
- **Gmail intake fixed for the tested invoice (owner-confirmed 2026-11-11).** Gmail labels were corrected; Paperless initially recorded `Processed without consumption`. Inspection of the affected Gmail message's MIME structure showed a PDF with `Content-Disposition: inline`, which was excluded under the prior attachment rule. Owner enabled inline attachments and cleared the corresponding Processed Mails record; owner explicitly confirmed successful re-import. A single successful case is confirmed; ongoing operation remains subject to normal monitoring. Do not include message contents, account credentials or private filenames in Git.

## Batch rules

1. Inventory a coherent topic via Drive and triage `import / leave in Drive / already archived / review`.
2. Owner uploads approved PDFs together; existing intake workflow adds `Inbox`.
3. Bulk-set shared metadata, then individual titles/dates/issuer, verify OCR, remove `Inbox` only after checks.
4. Record owner-confirmed result here at batch completion. Source Drive remains untouched unless separately requested and approved.
5. **No source deletion** before item-level Paperless reconciliation, a successful backup following the last pertinent import, recovery confidence and express owner approval.

## Current exceptions

- The tax folder contains two `.pfx` credential files; never ingest into Paperless or commit their contents.
- One additional filename resembling a tax wage certificate was observed in the tax folder during batch-2 inventory; requires inspection before any decision to import.
- The 2021 January–September wage-certificate coverage is not established from the reviewed batch-1 set.
- Batch 2A PDFs are owner-archived personal copies, not independently verified submission receipts. Tax assessments (2B) remain outstanding for mobile scanning.
- Insurance folder review found 2017 historical premium bill and scanned/image-only PDF candidates; do not fabricate metadata without checking originals.
- Zurich document reviewed: insurer correspondence about an accident claim, **not** a policy or proof of claim acceptance. File may contain sensitive health-related information: do not copy contents to Git. 
- Owner visually compared two Bosch BKK cancellation confirmation PDFs and explicitly confirmed identical content. Binary identity/scan quality not verified; import just one preferred copy, leave both Google Drive originals untouched. Device insurance annex could not be fetched for text verification.
