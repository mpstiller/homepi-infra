# Backup and restore

## Monitoring closure — 2026-10-20

- Owner supplied exact installed notification helpers and both systemd drop-ins; captured under `backup/bin/*-notify` and `backup/systemd/*.service.d/monitoring.conf`. URL contents are never included.
- Owner confirmed both Healthchecks checks returned to green after successful real backup/maintenance, failure emails arrived in controlled tests, and final timer scheduling is correct. Final timer confirmation is owner-reported; the raw list-timers output was not supplied.
- Local checks on the captured helper sources: both parse; 12 mocked cases cover start/success/failure routing, skip of failure after success, rejected URLs and network-timeout handling without disclosing secrets or failing the backup. No live requests were sent by these checks. The maintenance helper differs only by the URL-file path and whitespace.
- A missed-run alarm is configured by the daily/monthly cron schedules and grace times; a deliberately missed schedule/offline-Pi test was not performed. Helpers are best effort and errors do not fail backups. Maintenance standard restic check passed; no full data-read scrub/full-host recovery is claimed.
- Backup visibility is complete within the tested scope. Next roadmap work: normal-use media checks (Radarr hardlinks before cleanup, Kodi native-library synchronization, remote Jellyfin playback, retained authorized indexers), then choose Matter/smart-home or browser-first household dashboard. Independent-host recovery and full application-secret coverage remain optional/separate follow-ups.
- Cleanup of temporary transfer copies was instructed, but deletion was not explicitly confirmed. Do not delete retained restore/rollback directories without a separate choice.


## Backup monitoring and OAuth recovery — 2026-10-20

This section supersedes older resume instructions below. PRs #8 and #9 are merged; #9 merge commit is `b96a376`.

- Owner confirmed the restic password is in a password manager. After OAuth reconnection, the owner replaced the saved `/etc/rclone/homepi.conf` recovery attachment with the renewed configuration. Independent-host recovery is untested and application-secret recovery is not fully verified. Deletion of temporary transfer copies remains unconfirmed.
- Healthchecks.io monitoring is installed using root-only URL files under `/etc/homepi-monitoring/`, Python notification helpers in `/usr/local/sbin/` and systemd `monitoring.conf` drop-ins. Ping URLs are secrets. Installed helper/drop-in source was subsequently captured and locally checked; see Monitoring closure above.
- Daily check: cron `30 4 * * *`, Europe/Berlin, one-hour grace. Simulated failure/email and real backup/return to green were confirmed. At 08:19:20 CEST the backup completed with Result=success, ExecMainStatus=0; snapshot `c0280e8b` (345.933 MiB) and retention succeeded. Scheduled snapshots from Oct 15–20 are evidenced by owner output.
- Monthly check: cron `30 5 1 * *`, Europe/Berlin, six-hour grace. Simulated failure/email worked. The real 16:27 CEST run failed before opening the repository with rclone `invalid_grant`.
- Owner confirmed OAuth Testing status, completed GitHub Pages/Branding setup following PR #9 and confirmed In production. Seven-day Testing-token expiry is consistent with the incident timing. The headless reconnect used the explicit `/etc/rclone/homepi.conf`, browser authorization on the Mac and no Shared Drive. No tokens/client secrets were posted or committed.
- A read-only restic snapshot listing reopened existing repository `475950f8` and showed the expected snapshots. The subsequent real maintenance completed at 17:05:40 CEST with Result=success and ExecMainStatus=0: prune finished and standard restic check examined eight snapshots with no errors. This is not a claim of a full data-read scrub or new full-host restore.
- The renewed rclone recovery copy is now owner-confirmed saved in the password manager. Owner subsequently confirmed the monthly Healthchecks check returned to green. Successful helper exit alone would not prove delivery because monitoring errors intentionally do not fail backups.
- Monthly green state, timer schedule and monitoring source capture are now confirmed; see Monitoring closure above. Do not repeat OAuth reconnect or reopen Backup V1. Independent-host secret recovery and application-secret completeness remain separate follow-ups. Preserve incremental short terminal steps; the Mac shell is fish.


## Backup V1 complete — 2026-10-14

The owner accepted full temporary restore, copied-state integrity/configuration checks and one representative application-start test as sufficient for V1. Further app-start tests are deferred. This is the agreed operational scope, not proof of a full-host disaster recovery.

## Implementation

- restic 0.18.0, rclone 1.75.2 with dedicated Google Drive OAuth client.
- Encrypted independent repository: `rclone:gdrive:HomePi-Backup`.
- Protected sources: `/srv/appdata`, `/opt/homelab/stacks`. `/srv/data` media/downloads are excluded.
- Previously running candidate containers stop briefly for `rsync -aHAX` staging under `/srv/backups/restic-staging`; Jellyfin cache, Music Assistant .cache and */logs directories excluded. Containers restart before upload.
- Daily systemd backup at 04:30, Persistent=true; automatic retention 7 daily / 4 weekly / 6 monthly with default grouping.
- Monthly maintenance at 05:30 on day 1: prune then check.
- Scripts/units in `backup/`; local password and OAuth config remain excluded from Git. Original capture is preserved in commit `086255a08b66de824d27ccb6223daff536d13f4a`.
- Installed hardening uses a shared exclusive flock over each entire operation, per-container start/running-state checks, failed-container EXIT retry and original failure-status preservation. INT/TERM invoke cleanup; SIGKILL/power loss cannot be recovered by a shell trap.

## Verified evidence

- Native flock blocked concurrent acquisition and allowed it after release; both timers scheduled correctly.
- Revised backup succeeded 13:25:47–13:26:38 CEST. All candidates restarted before upload; snapshot `b37715a7` (334.493 MiB) saved; retention completed; exit 0 and post-run containers running.
- Revised maintenance succeeded 13:34:36–13:35:21 CEST: prune completed, three snapshots checked, no errors, exit 0.
- Full restore of `b37715a7` recovered 3236 files/directories in 1:01 at `/srv/backups/restore-validation.Nz6ggIgG`. Actual roots are directly `srv/appdata` and `opt/homelab/stacks`.
- Corrected checker passed 41 checks: 13 SQLite integrity checks, three *arr XML configs, 23 Home Assistant JSON state files, YAML presence and nonempty LiteDB presence.
- Kodi Sync Queue uses LiteDB, not SQLite; the initial SQLite header failure was a checker classification error. Full LiteDB integrity remains untested.
- Offline Sonarr restored startup/API passed on 4.0.20.3014, with all four series IDs matching the copied database. Test container/copy removed; live/source state unchanged.

## Recovery and scope limits

Follow `restore-runbook.md`: restore to a new private directory, inspect actual paths, validate on a disposable copy, preserve ownership and secrets before any controlled live recovery. Never overwrite running databases or launch duplicate Compose projects with the production mounts/ports.

Untested: other restored application starts, LiteDB integrity, YAML/PEM semantics, UI login, playback/download integrations and full-host recovery. Additional starts are optional/deferred by owner decision and do not reopen V1.

The restic password (`/etc/restic/homepi-password`) and rclone config (`/etc/rclone/homepi.conf`) are outside protected source trees. Verify independent recovery access in the password manager/offline secret storage separately. Existing microSD is a stale copy, not a current backup. Future irreplaceable household data needs an explicit scope extension.

Local staging/restore retains plaintext secrets under a private parent directory. Restore test data and rollback originals (`/root/homepi-backup-rollback.xDZCejUc`) remain retained; no cleanup is claimed.

## Follow-ups

- Independent secret-recovery verification.
- Lightweight failed/stale-backup notifications with a chosen channel; optional Homepage last-success signal.
- Optional broader recovery drills and resource/staging-permission checks. Gluetun remains outside the stopped candidate set; review whether its persisted state changes during staging without altering the VPN boundary casually.
