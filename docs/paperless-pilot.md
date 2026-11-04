# Paperless-ngx HomePi pilot — installed, first backup passed, restore pending

Date: 2026-11-03. See `stacks/paperless/README.md` for implementation gates
and references. This supersedes the earlier discovery-only state while keeping
the discovery brief as historical context.

## Verified synthetic import (owner confirmation, 2026-11-03)

- Both prepared synthetic documents were imported into Paperless.
- Search for `Wasserkocher` found the born-digital PDF.
- Search for `Sonnenuhr` found the image-only scanned PDF, confirming
  OCR and searchable indexing with the actual configuration.
- Small-pilot success **does not demonstrate large-batch OCR capacity**.
- Next gate: verify the **installed** `homepi-backup` script before applying
  the proposed three-container stop-list. Then confirm an encrypted backup
  snapshot and a strictly isolated database+document restore.
- No real identity/financial/medical documents yet.

## Installed backup script baseline verification (owner output, 2026-11-04)

- `/usr/local/sbin/homepi-backup` currently includes candidates through
  `homepage`, with no Paperless entries. Owner reported SHA-256
  `0ce674a100f0f9428516e6bb4d72c4372ec02708bd93e0398a54d780b70f7d85`.
- Verified this digest is byte-for-byte identical to the checked-in
  `main:backup/bin/homepi-backup` source (SHA-256 independently calculated).
  A controlled three-line extension can therefore be compared exactly.
- PR candidate stop order is webserver, database, broker (frontend first).
  Existing restart implementation will restart in list order, so check
  Paperless health carefully after the first live backup; if restart ordering
  proves fragile, address it before unsupervised scheduling.
- **No backup modification or successful backup run has occurred yet.**

## Backup candidate exactly verified (owner output, 2026-11-04)

- `systemctl show homepi-backup.service -p ExecStart` confirms active script
  `/usr/local/sbin/homepi-backup`. Most recent scheduled run started
  04:30:04 CET and finished 04:31:06 CET with `status=0`; this occurred
  **before Paperless was in the backup candidate list** and does not prove
  a Paperless snapshot.
- Candidate file `/tmp/homepi-backup.paperless-candidate` passed `bash -n`.
  `diff -u` shows **exactly three added lines** after `homepage`:
  `paperless-webserver`, `paperless-db`, `paperless-broker`.
- Owner has **not yet installed** this candidate. Next step is guarded
  atomic installation under the shared lock with a retained rollback copy,
  then a real backup run and isolated restore.

## Backup script installed (owner output, 2026-11-04)

- Protected installation was executed under the shared Restic maintenance
  flock. An exact byte-level replacement check against the verified old
  script succeeded, and `bash -n` succeeded.
- The live `CANDIDATES` list now includes `paperless-webserver`,
  `paperless-db`, and `paperless-broker` after `homepage`.
- Rollback copy retained at
  `/root/homepi-backup-before-paperless.iutMZWUb`.
- **The modified backup has NOT yet been run or restored.** Next: launch
  one controlled systemd service run, check both result and fresh restic
  snapshot, verify every Paperless container returned healthy, then restore
  into isolated temporary paths without overwriting live databases.

## First post-integration backup — success (owner log, 2026-11-04)

- `homepi-backup.service` ran from 11:20:40 to 11:22:40 CET,
  `Result=success` and `ExecMainStatus=0`.
- Logs confirmed stop/staging, explicit restart messages for all three
  Paperless services, cloud upload and retention.
- Restic created encrypted snapshot **`ef45cae4`** at 11:21:50 CET,
  processed 3930 files, logical size 486.679 MiB; 43.931 MiB was newly
  added to repository (8.739 MiB stored).
- Automatic retention completed. Most recent 04:30 snapshot `f608e5f3`
  was removed per policy after the new manual one was retained.
- Paperless broker and database reported **healthy** at immediate post-run
  check; webserver was **health: starting** 53 seconds after restart.
  Recheck until healthy before marking post-backup services stable.
- A successful backup does not prove that restored DB/media are usable.
  Next: confirm health, restore `ef45cae4` to a new root-only directory
  beneath `/srv/backups`, then independently check the restored
  PostgreSQL cluster and original/archive documents. No live state writes.

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
- Multiple stateful containers still running. Owner's read-only preflight: UID=1000, GID=1000, Docker Compose v5.5.1,
  port 8010 not listening, no Paperless container and no prior directories
  at /srv/appdata/paperless or /opt/homelab/stacks/paperless.
  These observations are not deployment or functional evidence.
- Proposed three-container baseline; do not interpret available memory as
  guaranteed free capacity under burst load.

## First boot observed (owner output, 2026-11-03)

- After copying the explicit Arcane opt-out labels, `docker compose config --quiet`
  succeeded and a matching-label count returned 3.
- All three images were pulled and the isolated `paperless_default` network
  was created. At the immediate `docker compose ps` check, `paperless-db`
  (PostgreSQL 18) and `paperless-broker` (Valkey 9) were **healthy**.
  `paperless-webserver` (Paperless 3.4.1) had just started and showed
  **health: starting**, not yet verified healthy.
- The only published host binding reported was `127.0.0.1:8010->8000/tcp`.
  Runtime auto-update labels and load under steady state still need checks.
- No verified Paperless login, OCR, real backup snapshot, restore, or personal
  document import yet. The host backup script is NOT yet updated.

## Steady-state verification (owner output, 2026-11-03)

- All three services reported **healthy** about two minutes after startup.
- Live labels: `com.getarcaneapp.arcane.updater=false` for broker, database
  and webserver; all status=running.
- Docker stats: broker 7.922 MiB / 96 MiB, PostgreSQL 45.92 MiB / 384 MiB,
  Paperless webserver 637.5 MiB / 1 GiB, CPU low at the sample.
- Pi memory: 4.0 GiB total, 2.8 GiB used, 1.1 GiB available.
  Swap: 992 MiB of 2.0 GiB. Before starting the stack, owner measured
  1.7 GiB available and 745 MiB swap used. This does not prove OCR headroom.
- The only host-published port remains loopback-only 127.0.0.1:8010.
- Next: use SSH tunnel to complete web-based first-user setup (do not share
  credentials), then synthetic PDF OCR/search trial while monitoring memory.
  Backup script is not yet installed; no real document ingestion.

## Initial local browser access

- Owner confirmed on 2026-11-03 that the Paperless web UI opens through
  the proposed localhost/SSH tunnel. This confirms reachability only:
  first-user setup, login, OCR, search and backups have **not** yet been
  verified.
- Two **synthetic test PDFs** were created for a no-private-data pilot:
  a born-digital sample containing `Wasserkocher` and a raster-only PDF
  containing `Sonnenuhr`. The latter contains no embedded PDF text, so
  successful full-text search demonstrates OCR. Files were given to the owner
  as conversation attachments, not added to Git or HomePi.

## Post-test resource snapshot (owner output, 2026-11-03)

- Webserver 606.5 MiB / 1 GiB, PostgreSQL 49.44 MiB / 384 MiB,
  Valkey 10.16 MiB / 96 MiB; total around 666 MiB.
- Host 1.3 GiB available RAM, 1.2 GiB of 2.0 GiB swap occupied.
  Higher swap occupancy than the prior 992 MiB is not evidence of active
  memory pressure; examine `vmstat` swap in/out under a future import.
- The two synthetic search checks were subsequently confirmed successful;
  see Verified synthetic import above.
- Backup script remains unapplied and restore untested; no personal documents.

## Swap activity check (owner output, 2026-11-03)

- `vmstat 1 6` returned five current samples after the startup-average
  line: `si` 16, 80, 0, 0, 0 KiB/s; `so` 0 in every sample.
- CPU idle 95–99%, I/O wait 0%, blocked processes 0. No evidence of
  sustained memory thrashing at idle. Occupied swap alone is not a reason
  to flush swap or adjust container limits.
- Search results for the synthetic PDFs were subsequently confirmed;
  backup and restore are still pending.

## Plan and explicit boundaries

1. **Pilot live, PR still draft**: Compose, private env and runtime services are in place; proposed backup change remains in PR and is not installed.
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
  Compose includes explicit `com.getarcaneapp.arcane.updater=false` labels on
  all three Paperless services; verify effective runtime labels after launch.
  The Arcane UI exclusion list can be checked as an additional safeguard.
