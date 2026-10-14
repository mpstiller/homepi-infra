# Backup and restore

## Operational Backup V1 — reconciled 2026-10-14

The encrypted restic backup is operational. Evidence is recorded in `CURRENT_STATE.md` and the 2026-10-13/14 changelog. The backup chat confirms closure; this reconciliation does not constitute a new live audit.

- restic `0.18.0`, rclone `1.75.2`, dedicated Google Drive OAuth client.
- Repository: `rclone:gdrive:HomePi-Backup`, independent of the NVMe.
- Protected sources: `/srv/appdata` and `/opt/homelab/stacks`.
- Brief container stops create a staging copy; containers restart before cloud upload. Cache/log exclusions reduced the tested snapshot to about 333 MiB.
- Staged snapshot paths observed in the setup chat: `/srv/backups/restic-staging/srv/appdata` and `/srv/backups/restic-staging/opt/homelab/stacks`.
- Daily `homepi-backup.service`/timer at 04:30, `Persistent=true`.
- Monthly `homepi-restic-maintenance.service`/timer on day 1 at 05:30: `restic prune`, then `restic check`; systemd execution tested.
- Installed retention confirmed on 2026-10-14: `forget --tag automatic --keep-daily 7 --keep-weekly 4 --keep-monthly 6`; no explicit group override.
- Owner-supplied scripts/units are captured under `backup/`; four units have no drop-ins. Review and remediation plan are in `backup/README.md`.
- Targeted restore to a temporary path and `restic check` succeeded.
- Old manual bootstrap snapshot `bd21d171` was removed and prune run afterwards.

`/srv/data` media/downloads are intentionally excluded. A rebuild will not recover those files from Backup V1. The old microSD is a stale recovery copy, not a current backup. Any future irreplaceable photo/file data requires an explicit backup-scope extension.

## Recovery prerequisites and secrets

The password is local at `/etc/restic/homepi-password`; keep an independent copy in the password manager. Google Drive access uses `/etc/rclone/homepi.conf`. VERIFY ON PI: independent recovery availability of the restic password, rclone OAuth configuration, and application secrets. Never commit their contents.

The systemd setup uses `HOME=/root` and `XDG_CACHE_HOME=/var/cache/homepi-backup`. Capture these settings with the scripts rather than reconstructing them from memory.

## Next: reproducibility and application recovery

1. Installed scripts/units, exclusions and retention are captured. Correct masked `docker start` failures; validate success/failure cleanup before deployment.
2. Add a shared exclusive lock to both scripts and validate contention. Existing `After=` ordering is not a universal mutual-exclusion mechanism.
3. Extend `restore-runbook.md` with the exact staged-path mapping, source ownership and recovery of Home Assistant and media-stack databases/configuration.
4. Restore to a temporary directory first. Before replacing any live appdata, stop affected services and preserve their existing state. Prefer an isolated recovery environment where practical; avoid duplicate Home Assistant automations/device control.
5. Validate database integrity and application startup/configuration; record the chosen snapshot, test scope and outcome. VPN isolation must pass before a recovered media stack can download.

The completed targeted restore proves file retrieval, not application recovery or a full host rebuild. Those checks remain open in the roadmap.

## Lightweight operational visibility (planned)

After recovery documentation, add failure and stale-backup notification with a chosen channel. Record the last successful snapshot/maintenance run; a running container alone is not backup success. No new monitoring service or notification integration has been deployed by this documentation update.
