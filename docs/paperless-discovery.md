# Paperless-ngx: next-session discovery brief

## Owner request and scope

2026-11-03: Marc wants to try Paperless-ngx in a NEW session, with a well-researched setup tailored to his situation. Start by understanding what he needs; do not start from a generic Compose deployment or bulk import. This brief captures the questions and research to do later. No Paperless installation, configuration, new capacity measurement or detailed setup research was performed in this backlog session.

Read AGENTS.md, LLM_CONTEXT.md, CURRENT_STATE.md, docs/decisions.md, ROADMAP.md and this brief first. Reuse already known answers and ask a few focused questions at a time, not the whole checklist at once.

## Known environment

- Pi 5, 4 GB RAM, ARM64, NVMe, multiple existing Docker services. Debian/Docker inventory is historical; confirm relevant versions and current resources before choosing a deployment.
- Arcane manages services; existing automatic updates are deliberately limited to the three Homepage containers. Review any new containers and exclude them until a dedicated policy is chosen.
- Admin access stays LAN/Tailscale private. Device-based Seerr automatic login was deferred; do not revive it as a prerequisite.
- Encrypted restic/rclone backup uses consistent staging of /srv/appdata and /opt/homelab/stacks with shared locking, daily 04:30 and monthly day-one maintenance 05:30 Europe/Berlin. /srv/data is excluded. Merely putting document originals/archive files there would NOT protect them.
- Audio runs daily 07:00 Europe/Berlin under the shared lock. First scheduled run on 3 November started/finished successfully with no conversion messages; no real multi-file or busy-lock wait was shown by that run.
- Matter and existing media/smart-home services work. Preserve them. Last pre-Matter resource sample is not current headroom.
- Marc uses iPhone/Mac and values usable, low-maintenance workflows. Whether the archive is personal, shared with his partner, professional or mixed is UNKNOWN, not permission to assume shared access.

## Discover the need before architecture

1. **People and boundaries:** Marc alone or partner/shared household? Separate private vs shared documents and permissions? Any professional documents that should remain in employer systems?
2. **Document inventory:** Typical sources/types (letters, invoices, contracts, tax, house, warranties); German/English/other languages; rough existing pages/files and ongoing intake. Existing folder/cloud organization and naming worth retaining?
3. **Capture:** iPhone scans, existing scanner, PDF downloads, email attachments or watched folder? Is an easy phone sharing route essential? Is automatic mailbox intake actually wanted?
4. **Retrieval:** What would he type when searching? Search vs folders, correspondence, dates, expiry/reminder needs, household/equipment links, export expectations.
5. **Ownership and privacy:** Keep all OCR/classification local? Are any external AI APIs acceptable? AI is optional, never required for the first useful archive. Do not request real financial/identity documents in chat; use anonymized or synthetic samples where possible.
6. **Operational expectations:** Remote use, outage tolerance, backup/recovery, acceptable import delay, budget and time available. Do not infer a scanner purchase or additional server.

## Research in the new session

Use current official Paperless documentation and release notes, then verify important details against source/version-specific examples. Consult focused community experiences for real intake workflows and iOS clients while distinguishing anecdotes from supported behavior. Record chosen version, source URLs/date and trade-offs; an earlier overview is not current validation.

Investigate:

- Supported stable ARM64 images and recommended Docker/Compose architecture; database and queue choices, persistent paths, runtime user/permissions, resource tuning, OCR workers/threads and scheduling on this existing Pi.
- OCR language/order, existing-text PDFs vs scans, rotation/deskew, archival format, duplicate handling and document limits; choose settings after learning the actual inputs.
- A small, maintainable taxonomy: correspondents, document types, tags, custom fields and dates. Explain distinctions and propose examples based on Marc's material. Avoid a giant premade tag system.
- Storage naming vs display titles; whether folder-like layouts are actually needed; originals, archives, thumbnails/index/database and how exports are recovered.
- Users/ownership/default permissions and ingestion workflows for private vs shared material; automation must not unintentionally broaden access.
- iPhone capture/share routes and maintained clients; compare against a simple web/upload/consume-folder path before adding components.
- Optional email ingestion: dedicated account/folder, least privilege, read/mark/move/delete behavior, secret storage and privacy. Do not connect a mailbox or enable deletion without a deliberate user choice.
- Which features are native for the chosen version and which require third-party tools or external AI. Assess added resource/maintenance burden before recommending extras.
- Access over LAN/Tailscale, HTTPS/session behavior and Homepage link/widget only if useful; keep keys out of chat/Git and keep admin UIs private.
- Backup consistency across ALL selected database/document volumes, exclusion pitfalls, space for staging/restores and a meaningful isolated restore/export check. Do not reopen already-completed Backup V1 as a generic prerequisite.
- Initial update policy, rollback/export limits, monitoring proportional to the service, retained originals and documented recovery.

Starting references to refresh (not a claim that research is complete):
- https://docs.paperless-ngx.com/
- https://docs.paperless-ngx.com/setup/
- https://docs.paperless-ngx.com/configuration/
- https://docs.paperless-ngx.com/usage/
- https://docs.paperless-ngx.com/faq/
- https://github.com/paperless-ngx/paperless-ngx/releases

## Proposed working sequence for that session

1. Clarify the important unknowns and write a short requirements summary.
2. Research the relevant current recommendations and present a tailored design, including what to leave disabled and why.
3. Measure current Pi headroom and verify the backup/access implications before deploying.
4. Prepare a small reversible pilot in the repo, with configuration and secrets separated.
5. Guide Marc through short Pi steps; test a small representative set (e.g. scanned/text PDFs, German/English only if needed, multipage, rotated scan, duplicate) before importing an existing archive.
6. Tune retrieval, taxonomy, intake and any shared permissions with Marc, then verify persistence and recovery and document the actual result.

The pilot succeeds when Marc can capture, find and retrieve representative documents with the intended access controls and a verified recovery path, while the existing services remain usable. Bulk import, AI, mailbox automation, advanced plugins and hardware purchases are optional later choices, not the starting point.
