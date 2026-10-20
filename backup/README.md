# Backup V1 — installed and validated

`bin/` maps to `/usr/local/sbin/` (root:root; backup/maintenance scripts 0700, notification helpers 0755); `systemd/` maps to `/etc/systemd/system/` (0644). Both services now have captured monitoring drop-ins; the earlier no-drop-in capture is historical. No passwords, OAuth values or API keys are included. Original installed capture is in commit `086255a08b66de824d27ccb6223daff536d13f4a`; revised scripts are installed and validated as of 2026-10-14.

## Runtime behavior

Both scripts wait for exclusive FD-9 flock on `/run/lock/homepi-restic.lock` for the entire operation. Backup stops only previously running candidates, stages appdata/stacks, then starts/checks candidates individually before upload. A failed start blocks upload; only failed containers are retained for EXIT retry. Cleanup preserves the original failure code. INT/TERM invoke cleanup; SIGKILL/power loss and long-term application health are outside that guarantee.

Scripts set root/cache environment and umask 077. Existing staging permissions are not changed automatically. Retention/exclusions, scheduling and VPN configuration are unchanged from the installed capture. `After=` remains ordering, while the shared lock supplies mutual exclusion ([systemd source](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml), [flock manual](https://man7.org/linux/man-pages/man1/flock.1.html)).

## Validation

- Eight local simulated backup/recovery/serialization tests pass (`tests/test_backup.py`). Python flock shim uses the host kernel lock; Docker/rsync/restic are simulated.
- Native flock contention/release, restored timers and real backup/maintenance execution passed on the Pi.
- Backup snapshot `b37715a7` restored in full; corrected copied-state checker passed 41 checks.
- `validate-restored-state.py`: 13 SQLite databases, XML and Home Assistant JSON; YAML/LiteDB presence only. Uses a disposable copy, handles WAL and does not print secrets. Seven local tests pass.
- `test-sonarr-restore.py`: exact owner-confirmed local image, copied config, network none, no published ports/media/socket mounts; compares series IDs via API. Four simulated lifecycle tests pass and native test passed on Sonarr 4.0.20.3014 with four matching IDs.
- Owner chose one representative application-start test for V1. No further application starts are required for agreed closure. LiteDB integrity, other startup/UI/integration and full-host recovery remain untested.

## Installation/rollback evidence

Owner confirmed successful installer execution with rollback copies at `/root/homepi-backup-rollback.xDZCejUc`. The checksum guard initially rejected a baseline copy containing one extra blank line; the owner diff confirmed this sole difference and the exact-live checksum was corrected before installation. Previously active timers were restored; the installer itself did not run backup/maintenance.

For future script replacement, verify prerequisites, pause only active timers, wait for services to finish, save private originals, syntax-check and install both scripts as root:root 0700, then restore timer state and validate. Restore both saved scripts if needed; do not intentionally break production Docker/appdata to exercise failure paths. Units are unchanged for this script-only change.

## Separate follow-ups

Independent password/OAuth recovery remains to be verified. These files and installed scripts/units live outside protected source trees (scripts/units are now in Git). Gluetun persisted-state consistency, existing staging permissions and headroom need review when relevant. Test restore data remains at `/srv/backups/restore-validation.Nz6ggIgG`; no cleanup has been performed. See `docs/backup-restore.md` and `docs/restore-runbook.md`.

## Healthchecks monitoring — 2026-10-20

See [monitoring.md](monitoring.md) for captured helper/drop-in installation paths, private URL storage, schedules, tests and rollback. Owner-confirmed notification recovery and timer scheduling complete this follow-up. Independent-host recovery is not demonstrated.
