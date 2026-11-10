# Paperless / Google Drive migration ledger

This is a **status-only, non-sensitive** tracker. Do not store source document bodies, personal identifiers, tax numbers, amounts, private names or Paperless credentials here. Canonical operating model and safety gates: `docs/paperless-drive-migration-handoff.md`, ADR-013/014.

| Batch | Scope | Paperless status | Evidence | Drive source disposition | Follow-ups |
| --- | --- | --- | --- | --- | --- |
| 1 | 9 income-tax wage certificates, tax years 2016–2023 (two separate periods in 2019) | **Complete, owner-confirmed 2026-11-10**: uploaded and processed; type `Bescheinigung`, tags `Steuer` and `Beruf`, two issuer groups, individual titles and document dates reviewed, OCR checked, `Inbox` removed | Owner's explicit confirmation in chat; **no direct Paperless API inventory/reconciliation** | Unchanged; retain source | Potential superseded 2019 certificate and unreadable 2017 candidate held out; check missing 2021 January–September certificate and an additional wage certificate from a later folder inspection. Backup after batch 1 not verified. |
| 2A | 9 tax-return PDFs, tax years 2016–2024 | **Complete, owner-confirmed 2026-11-10:** uploaded, type `Steuererklärung`, tag `Steuer`, no correspondent, titles/document dates reviewed, OCR checked, `Inbox` removed | Owner's explicit chat confirmation; **no Paperless API inventory/reconciliation or proof of tax submission** | Unchanged; retain source | Successful post-import backup not independently verified. |
| 2B | Income tax assessment notices (paper originals) | **Owner plans to locate and scan on iPhone; none imported or counted yet** | Owner decision in chat 2026-11-10 | Paper originals preserved | For each notice, use existing `Bescheid` type, `Steuer` tag, actual issuing tax office, document issue date and tax year; preserve relevant amended notices separately. |
| 3 | Insurance documents in `02_Areas/Finances/Versicherungen` | **Complete, owner-confirmed 2026-11-10:** 2 documents (liability policy endorsement and historical health-insurance certificate), individual title/date/correspondent/type/tags checked, OCR reviewed, `Inbox` removed | Explicit owner report in chat; no direct Paperless API reconciliation | Unchanged; retain source | Insurance remainder in batch 3B; post-import backup not verified. |
| 3B | Remaining insurance records in Drive | **In progress:** Zurich accident insurer letter imported, classified, OCR checked and `Inbox` removed (owner-confirmed 2026-11-10); Bosch BKK confirmation not yet imported | Owner explicitly confirmed Zurich closeout and visually compared two Bosch BKK confirmation PDFs as content-identical; no independent Paperless API check or binary equality test | Unchanged; retain both source PDFs pending approved cleanup | Import only one Bosch BKK confirmation (choose clearer legible copy), check actual issue date, classify as `Bescheinigung` from Bosch BKK with tag `Versicherungen`; retain other candidate in Drive. Review historic premium bill / device annex later. |

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
