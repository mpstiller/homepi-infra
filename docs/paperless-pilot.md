# Paperless-ngx HomePi pilot — proposed, not installed

Date: 2026-11-03. See `stacks/paperless/README.md` for implementation gates
and references. This supersedes the earlier discovery-only state while keeping
the discovery brief as historical context.

## Agreed user needs

- One person initially, shared with partner potentially later; future
  individual permissions have not been defined.
- Long-term personal paper trail (bills, insurance, tax, authorities,
  household/housing, guarantees, health and personal career records).
  **No employer/client business records.**
- Both old fragmented files/paper and ongoing incoming documents matter.
- Capture via iPhone scans/share sheet, Mac, selected email rules, gradual
  Google Drive import. Live connections are explicitly deferred.
- Local-first processing; external AI only with explicit future approval.
- Find by text, correspondent, type and filters; recurring deadline reminders
  are a later acceptance test, not a pilot prerequisite.
- Google Drive remains the editable files workspace; Paperless is the
  evidence/archive system for completed documents.
- Success criterion: weekly ordinary document administration ideally
  <= 5–10 min, measured after the initial learning/migration phase.

## Observed resources (owner shell output, 2026-11-03)

- `free -h`: 4.0 GiB RAM, 2.3 GiB used, 1.7 GiB available; 745 MiB of
  2 GiB swap in use.
- Root NVMe: 1.8 TB total; 356 GB used; 1.4 TB available.
- Multiple stateful containers still running. Host-specific current port
  and UID/GID checks are **not yet provided**.
- Proposed three-container baseline; do not interpret available memory as
  guaranteed free capacity under burst load.

## Plan and explicit boundaries

1. **Prepared in branch/PR only**: Compose, private env template, runbook and
   proposed backup stop-list; no host changes or user files.
2. Verify installation prerequisites, collisions, Arcane exclusion, and
   existing HomePi checkout state. Small owner-executed changes only.
3. Deploy localhost-only; test one text PDF and one scanned image PDF,
   index/search/metadata/duplicate, inspect RAM+swap.
4. Extend installed stop-list and validate real Restic snapshot and
   isolated database+document restore. Until then **no real documents**.
5. Enable LAN/Tailscale and iPhone only after secure access design; email
   rules and gradual old-file migration only after workflow acceptance.

## Caveats

- Official new-installation guidance recommends PostgreSQL; PostgreSQL 18
  + Valkey 9 introduce more containers than SQLite+Valkey but avoid later
  backend conversion. Reassess after measured idle/OCR consumption.
- Published `POSTGRES_PASSWORD` and `PAPERLESS_SECRET_KEY` placeholders
  are invalid; real values are generated locally and never stored in Git.
- Version tags for PostgreSQL/Valkey are major-stream and will change when
  manually pulled; Docker images remain stable in running containers until
  explicitly updated.
- All persistent bind mounts intentionally reside below `/srv/appdata`,
  not excluded `/srv/data`. Raw broker/DB copy requires coordinated stop.
- Arcane Auto Update must remain limited to existing Homepage containers.
  PR files alone do not enforce exclusion in Arcane UI.
