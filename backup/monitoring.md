# Backup email monitoring — installed 2026-10-20

Healthchecks.io receives start, success and failure signals and emails the owner on failures/late checks. Monitoring is external so missing signals can be detected even if HomePi is offline. No logs or backup content are submitted.

## Captured runtime files

| Repository | Installed |
|---|---|
| `backup/bin/homepi-backup-notify` | `/usr/local/sbin/homepi-backup-notify` |
| `backup/bin/homepi-maintenance-notify` | `/usr/local/sbin/homepi-maintenance-notify` |
| `backup/systemd/homepi-backup.service.d/monitoring.conf` | `/etc/systemd/system/homepi-backup.service.d/monitoring.conf` |
| `backup/systemd/homepi-restic-maintenance.service.d/monitoring.conf` | `/etc/systemd/system/homepi-restic-maintenance.service.d/monitoring.conf` |

Owner pasted all four files from the Pi. These are captured versions, not a redesigned notification system. Each helper reads a separate root-only one-line standard `https://hc-ping.com/<UUID>` URL from `/etc/homepi-monitoring/backup.url` or `maintenance.url`. Directory mode 0700, files 0600, owned by root; helpers are root-owned 0755. Never publish the URL files, tokens or OAuth configuration.

## Timing and signals

| Check | Cron | Time zone | Grace |
|---|---|---|---|
| Daily backup | `30 4 * * *` | Europe/Berlin | 1 hour |
| Monthly maintenance | `30 5 1 * *` | Europe/Berlin | 6 hours |

Keep E-mail integrations enabled on both checks. `ExecStartPre` signals start, `ExecStartPost` signals success only after the oneshot script exits successfully, and `ExecStopPost` signals failure unless `SERVICE_RESULT=success`. The underlying shared lock, staging/restart handling, retention and timers are unchanged.

The helper performs an empty POST with a five-second urllib timeout, validates the standard host/UUID shape and rejects redirects. Exceptions produce only a generic diagnostic and return 0; systemd also prefixes commands with `-`. A notification outage must not prevent backup/recovery. Failed notifications rely on subsequent missing-signal alarms, so helper exit 0 is not delivery proof. urllib timeout is a network-operation timeout, not a separately enforced total-runtime deadline.

## Restore/install reference (already installed; do not rerun needlessly)

From a reviewed repository checkout, first restore private URL files separately using an editor. Do not put URL literals in Git or chat. Then copy the four captured files:

```bash
sudo install -d -m 700 /etc/homepi-monitoring
sudo install -d -m 755 /etc/systemd/system/homepi-backup.service.d
sudo install -d -m 755 /etc/systemd/system/homepi-restic-maintenance.service.d
sudo install -m 755 backup/bin/homepi-backup-notify /usr/local/sbin/homepi-backup-notify
sudo install -m 755 backup/bin/homepi-maintenance-notify /usr/local/sbin/homepi-maintenance-notify
sudo install -m 644 backup/systemd/homepi-backup.service.d/monitoring.conf /etc/systemd/system/homepi-backup.service.d/monitoring.conf
sudo install -m 644 backup/systemd/homepi-restic-maintenance.service.d/monitoring.conf /etc/systemd/system/homepi-restic-maintenance.service.d/monitoring.conf
sudo systemctl daemon-reload
```

The directory/URL permissions and actual saved URLs must be verified privately. Use the captured Python helpers; curl and SMTP credentials are not required. To roll back monitoring only, preserve then remove the two monitoring.conf drop-ins and reload systemd; leave base services/timers intact. Pause/disable checks at Healthchecks when deliberately removing signals to avoid expected late alerts. Helpers and private URL files can be retained for rollback.

## Evidence and limits

- Simulated failure for each check: owner confirmed red state and email delivery. These tests did not break the underlying jobs.
- Real daily backup: snapshot c0280e8b, Result=success and exit 0; check returned green.
- Real monthly maintenance after OAuth repair: completed 17:05:40 CEST, prune then standard restic check of eight snapshots, no errors; check returned green.
- Owner confirmed both timers' scheduling; raw final timer output was not posted.
- Captured helpers parse. Twelve local mock checks cover three signal routes per helper, skipping failure after success, invalid URL and timeout handling with secret-safe output. No requests were sent by local checks.
- Deliberately missed-run/offline-Pi alerts, full data-read scrub, independent-host credential recovery and full-host disaster recovery were not tested. Existing Backup V1 scope remains closed.
- State/URL configuration is not covered by the existing appdata/stacks backup. Helper/drop-ins are now reconstructable from Git; restore private check URLs separately or create new checks. Optional Homepage backup status remains deferred.
