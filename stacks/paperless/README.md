# Paperless-ngx — live localhost pilot (backup/restore verified for synthetic docs)

This stack was deployed as a localhost-only pilot on 2026-11-03 for one personal Paperless archive. It is intentionally
**localhost-only** until a separate LAN/Tailscale access decision. It does not
replace Google Drive working files. Backup consistency and isolated
PostgreSQL/media restore were verified for synthetic documents on 2026-11-04;
the native document-exporter smoke test was explicitly deferred by the owner;
it is an optional later portability/migration enhancement, not a gate for
initial real documents after the verified Restic restore.

## Baseline and decisions

- Paperless **3.4.1** (2026-10-31), official ARM64 image
- Explicit `com.getarcaneapp.arcane.updater: "false"` labels on **all three**
  services prevent unattended image installation, even before UI exclusions
  are configured. Update checks/notifications remain enabled. Verify the
  running labels in Arcane/Docker after deployment.
- PostgreSQL **18** and Valkey **9 Alpine**, following the official PostgreSQL
  new-installation recommendation. Version ranges for these DB/broker images
  are major tags, not immutable digests; updates are manual and reviewed.
- Dedicated Compose project `paperless`; no reverse proxy or public routes.
  Host `127.0.0.1:8010` only. Mac SSH forwarding is optional during the pilot:
  `ssh -N -L 8010:127.0.0.1:8010 marc@homepi`, then
  `http://127.0.0.1:8010`. Verify hostname and port before use.
- Webserver runs as a rootless host UID/GID, set after `id -u; id -g`.
  Do not set USERMAP_* in this mode. `deu` and `eng` ship with the
  standard Paperless image; no extra language package is requested.
- Low concurrency (1 task worker × 1 OCR thread), container memory ceilings:
  webserver 1024 MiB, PostgreSQL 384 MiB, broker 96 MiB.
  These caps are safety guardrails, not guaranteed OCR capacity.
- Local-only OCR and classification. No mailbox, AI API, Tika, Gotenberg,
  cloud sync, public sharing or bulk import configured.
- `PAPERLESS_OCR_MODE=auto` preserves born-digital PDF text. Archive generation
  `auto` keeps original documents and creates archival PDF for scans.
- Files from the `consume` directory are **consumed and removed**. Never mount
  Google Drive or an original documents folder there. Copy test documents in.
  Duplicate suppression is enabled for consume imports only; confirm UI import
  and duplicate behavior separately.

## Before running anything on HomePi

1. Inspect original homepi checkout and local modifications; **do not blindly
   `git pull` or reset**. Review this PR and pin its exact merge/commit SHA.
2. Run read-only preflight: `id -u; id -g; docker compose version;
   ss -ltn '( sport = :8010 )'`, and inspect `docker ps` / memory headroom.
   Port 8010 must be free; UID/GID must be confirmed on the Pi.
3. Ensure `/srv/appdata/paperless` does not exist from any prior deployment.
   Check Docker project/container-name collisions and free disk/staging space.
4. Create `.env` locally from `.env.example`. Generate **two different**
   random secret strings using Python `secrets`, keep mode 0600, never send
   secret values in chat or commit them. Stop if any `REPLACE_` values remain.
5. Before start, create the four webserver directories owned by UID/GID,
   e.g. `sudo install -d -o "$(id -u)" -g "$(id -g)" -m 0700
   /srv/appdata/paperless/{data,media,consume,export}`.
   For db/broker, create private parent paths but let their official image
   entrypoints establish ownership as required; inspect any permission errors.
6. Validate the rendered Compose locally with `docker compose config --quiet`
   and confirm `docker compose config --services` lists only expected services.
   Do **not** post `docker compose config` output because it expands secrets.
7. Exclude all three new containers from Arcane Auto Update. Verify the
   exclusions in Arcane before treating the setup as ready for regular use.

## Verified (owner evidence)

- All three services healthy; Arcane automatic-update opt-out label `false` observed live.
- Both artificial sample PDFs imported and searched successfully: born-digital
  `Wasserkocher`, raster-only OCR `Sonnenuhr`.
- After the test Pi had 1.3 GiB available RAM, and five `vmstat` samples
  showed no swap-out; this does not establish large-import capacity.
- Installed daily backup script now includes all three Paperless containers.
  A controlled encrypted Restic snapshot `ef45cae4` was independently restored.
  Offline recovered PostgreSQL started, containing both synthetic document
  records; SHA-256 checks passed for 2 originals and 1 archival PDF.
  This is not an independent-host or full restored-application startup test.
- **Next:** real-document metadata and ingestion workflows. A native
  `document_exporter` smoke test is optional/deferred by owner.

## Pilot and stop gates

- Initial launch and OCI image pulls require separate owner-executed commands
  after preflight. Do not install automatically from repo or run a bulk import.
- Test startup/health + a tiny synthetic text PDF and scanned image PDF.
- Observe `free -h`, `docker stats --no-stream`, logs, OCR output, text search,
  and duplicate behavior. If system becomes swap-bound or OCR OOMs, stop and
  retune. No auto-restart storm or uncontrolled backfill.
- **Backup is live-integrated**: the installed `homepi-backup` now stops
  all three containers during staging and restarts them before the Restic
  upload; this was tested 2026-11-04. Schedule remains 04:30 and sources
  remain under `/srv/appdata/paperless`. Rollback and restored test copies
  are intentionally retained privately.
- Real encrypted Restic backup and isolated PostgreSQL/media integrity
  restore have passed. Owner accepted this as enough to start private
  archiving; the native `document_exporter` is **optional/deferred**,
  not a prerequisite. Large OCR batches should begin cautiously.
  A portable Paperless export is supplementary to Restic, not a replacement.
- For rollback, remove containers with `docker compose down` **without -v**;
  keep /srv/appdata/paperless and any tested snapshots unless separately
  authorized to delete. Do not delete backups or originals.
- After proof, LAN/Tailscale access, iOS integration, email rules and gradual
  Google Drive migration are separate owner-approved steps.

## References checked on 2026-11-03

- Official pinned examples:
  https://github.com/paperless-ngx/paperless-ngx/blob/v3.4.1/docker/compose/docker-compose.postgres.yml
- Setup: https://github.com/paperless-ngx/paperless-ngx/blob/v3.4.1/docs/setup.md
- Configuration: https://github.com/paperless-ngx/paperless-ngx/blob/v3.4.1/docs/configuration.md
- Administration/export/backup:
  https://github.com/paperless-ngx/paperless-ngx/blob/v3.4.1/docs/administration.md
- Releases: https://github.com/paperless-ngx/paperless-ngx/releases/tag/v3.4.1
