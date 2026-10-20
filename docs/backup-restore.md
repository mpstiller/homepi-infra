# Backup and restore

## Backup monitoring and OAuth recovery — 2026-10-20

This section supersedes older resume instructions below. PR #8 is confirmed merged into main (merge commit `9f81ada`).

- Owner confirmed the restic password is in a password manager and saved a copy of `/etc/rclone/homepi.conf` there. Independent-host recovery was not tested; application-secret recovery is not fully verified. Temporary-copy deletion was instructed but not confirmed.
- Healthchecks.io email monitoring was installed by the owner using local root-only URL files under `/etc/homepi-monitoring/`, Python notification helpers in `/usr/local/sbin/` and systemd `monitoring.conf` drop-ins. Ping URLs are secrets and must never be committed. Runtime helper/drop-in capture into Git remains pending.
- Daily check: cron `30 4 * * *`, Europe/Berlin, one-hour grace. Simulated failure/email delivery and real successful run/return to green were owner-confirmed. At 08:19:20 CEST the backup finished with Result=success, ExecMainStatus=0; snapshot `c0280e8b` (345.933 MiB) was saved and retention succeeded. Earlier daily snapshots establish Oct 15–20 scheduled runs.
- Monthly check: cron `30 5 1 * *`, Europe/Berlin, six-hour grace. Simulated failure/email worked. The real 16:27 CEST run failed before opening the repository: rclone `invalid_grant` while refreshing Google OAuth. No successful prune/check or monitoring recovery is claimed for this run.
- Owner confirmed the OAuth app is in Testing. Google documents seven-day refresh-token expiry in that state; timing is consistent with the Oct 13 setup. Publishing is blocked by empty homepage/privacy fields in Branding.
- Static homepage and privacy pages are prepared in `docs/index.html` and `docs/privacy.html`. Pages enablement/public reachability, OAuth publishing, reauthorization, recovery-copy replacement and successful maintenance rerun remain pending. Do not treat a prepared page or PR as a deployed site.
- Next: publish the prepared pages through GitHub Pages, fill Google Branding and authorized domain, publish the OAuth app, reconnect `gdrive:` using the explicit `/etc/rclone/homepi.conf`, privately update the password-manager copy, verify repository access and run maintenance. Keep Backup V1 closed; this is a current authentication failure, not a reason to repeat every restore test.


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
