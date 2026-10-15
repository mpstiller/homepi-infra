# HomePi restore runbook

This runbook describes how to reconstruct the host architecture. Backup V1 is operational and a targeted restore has been tested. Full temporary restore, copied-state checks and an isolated Sonarr start have passed. The owner accepted this representative test as sufficient for Backup V1; other app-start/full-host drills are optional/deferred. See `backup-restore.md` for scope limits.

## 1. Prerequisites

- Raspberry Pi 5
- NVMe available as primary system disk
- Raspberry Pi OS / Debian-compatible 64-bit installation
- network access
- this repository
- separately stored secrets
- most recent backup of `/srv/appdata`

## 2. Base host

Configure:

- hostname `homepi`
- time zone `Europe/Berlin`
- SSH
- Docker Engine from the official Docker Debian repository
- Docker Compose plugin
- user `marc` in the Docker group

Create:

```bash
sudo mkdir -p /opt/homelab/stacks /srv/appdata /srv/data /srv/backups
```

Recreate the media tree:

```bash
sudo mkdir -p \
  /srv/data/torrents/{movies,tv,test,incomplete/sonarr,incomplete/radarr} \
  /srv/data/media/{movies,tv}
```

Restore correct ownership using the live PUID/PGID values before starting containers.

## 3. Restore repository configuration

Clone `mpstiller/homepi-infra` and use the verified Compose definitions under `stacks/` as the rebuild source. The historical live Music Assistant file was located at `/srv/appdata/compose.yaml`, but its verified definition is now normalized into `stacks/music-assistant/compose.yaml` in this repository.

Do not deploy placeholder documentation as runtime configuration. Only stack directories containing verified `compose.yaml` files are deployment-ready.

## 4. Restore secrets

Create local `.env` files from the corresponding `.env.example` files.

Required secrets currently include at least:

- Arcane encryption key
- Proton WireGuard private key

Application API keys and login credentials normally live in restored appdata and must not be committed to Git.

## 5. Restore persistent application state

Restore `/srv/appdata` from backup before starting the services if the intent is to recover the existing Home Assistant/Jellyfin/*arr state.

Automatic snapshot metadata records staging source paths. The owner verified a full restore of snapshot `b37715a7` on 2026-10-14: the restored tree directly contains `srv/appdata` and `opt/homelab/stacks`, without the staging prefix. For this restore, map `<target>/srv/appdata` to `/srv/appdata` and `<target>/opt/homelab/stacks` to `/opt/homelab/stacks`. Inspect the actual selected snapshot/restore layout rather than inferring it from source metadata; verify ownership and recovery commands before copying. Do not copy blindly over running databases. Preserve existing appdata and stop affected services before a live recovery. `/srv/data` is excluded from Backup V1, so media files require separate recovery or recreation.

Important state includes:

- Home Assistant `.storage`, YAML and database
- Music Assistant databases/settings
- Jellyfin config
- Sonarr/Radarr/Prowlarr databases/config
- qBittorrent config and torrent state
- Seerr config/database
- Gluetun persistent state if required

### Safe validation before application recovery

The following procedure restores only into a new local directory. It does not stop, replace or start production services. Run on the Pi; keep restored secrets private.

First select an explicit automatic snapshot and check local capacity:

```bash
sudo restic \
  -o rclone.args="serve restic --stdio --config=/etc/rclone/homepi.conf" \
  -r rclone:gdrive:HomePi-Backup \
  --password-file /etc/restic/homepi-password \
  snapshots --tag automatic

df -h /srv/backups
```

Then set the selected snapshot ID and restore. Use a new directory each time; never choose `/`, `/srv/appdata`, `/opt/homelab/stacks`, or the active staging directory as the target.

```bash
SNAPSHOT_ID=REPLACE_WITH_SELECTED_ID
RESTORE_DIR=$(sudo mktemp -d /srv/backups/restore-validation.XXXXXXXX)

sudo env HOME=/root XDG_CACHE_HOME=/var/cache/homepi-backup \
  restic \
  -o rclone.args="serve restic --stdio --config=/etc/rclone/homepi.conf" \
  -r rclone:gdrive:HomePi-Backup \
  --password-file /etc/restic/homepi-password \
  restore "$SNAPSHOT_ID" --target "$RESTORE_DIR"

printf 'Restore directory: %s\n' "$RESTORE_DIR"
sudo find "$RESTORE_DIR" -maxdepth 7 -type d \
  \( -name appdata -o -name stacks \) -print
```

Confirm the actual restored layout before setting the appdata path. Preserve SQLite `-wal`/`-shm` companions; do not discard them or use immutable mode to ignore a pending WAL. For validation, make a separate copy of the restored application state and run `PRAGMA integrity_check` against confirmed SQLite databases there. Report file-relative paths and pass/fail only; do not publish database/config contents. Record missing files separately rather than treating a test of zero databases as success.

Home Assistant: check YAML and `.storage` presence/parseability, and the recorder database if SQLite is used (VERIFY ON PI: recorder backend). Sonarr/Radarr/Prowlarr: verify `config.xml` and each restored database. Seerr/Jellyfin/Music Assistant: VERIFY ON PI: actual database locations/formats before choosing checks. qBittorrent: verify settings/torrent-state presence without starting restored downloads. Do not expose credentials in test output.

Database integrity and configuration parse checks are intermediate evidence. Sonarr startup/retained series state is verified below; other startup/login/integration tests are optional follow-ups under the agreed V1 scope. On an isolated recovery host, use recovered state plus the same tested application versions; keep Home Assistant device/automation access isolated and qBittorrent downloads disabled until VPN validation. On the production Pi, schedule a short service-specific window, preserve a rollback copy and stop the affected service before changing its state. Do not launch duplicate Compose projects with the checked-in host mounts/ports/container names.

Record snapshot ID/time, test scope, database results, service startup/state validation and rollback outcome in `CURRENT_STATE.md`/`CHANGELOG.md` only after completion. Full-host recovery stays open until tested. Restored directories contain secrets and should remain root-accessible only; choose cleanup after reviewing results.

References: [restic restore](https://restic.readthedocs.io/en/stable/050_restore.html), [SQLite integrity_check](https://www.sqlite.org/pragma.html#pragma_integrity_check), [SQLite WAL](https://www.sqlite.org/wal.html).

## 6. Start stacks

From each verified stack directory:

```bash
docker compose up -d
```

Suggested order:

1. Arcane / Homepage
2. Home Assistant
3. Music Assistant
4. Jellyfin
5. Media stack

## 7. Media-stack validation

Use the Gluetun digest from the checked-in Compose file. For planned Gluetun/qBittorrent recreation and post-start checks, follow [VPN maintenance](gluetun-maintenance.md); a Gluetun-only Docker restart did not restore the qBittorrent API path during the 2026-10-15 tunnel-down test. Validate qBittorrent as well as Gluetun health.

After media stack startup, verify:

1. Gluetun is healthy.
2. qBittorrent public IP is the VPN IP, not the normal host WAN IP.
3. qBittorrent interface is `tun0`.
4. qBittorrent bind address is `0.0.0.0` / All IPv4 addresses.
5. Proton forwarded port matches qBittorrent listen port.
6. Sonarr/Radarr qBittorrent client uses host `gluetun`, port `8080`.
7. qBittorrent category paths are correct.
8. A controlled test import creates hardlinks, not copies.
9. Jellyfin can Direct Play a test item.

## 8. Normal shutdown

Use:

```bash
sudo poweroff
```

Do not manually stop all containers first.

## Completed V1 validation — 2026-10-14

- Snapshot `b37715a7` restored to `/srv/backups/restore-validation.Nz6ggIgG`: 3236 files/directories, 334.493 MiB in 1:01. Restore roots are directly `srv/appdata` and `opt/homelab/stacks`.
- `backup/validate-restored-state.py` passed 41 checks on a disposable appdata copy: 13 SQLite integrity checks, three XML configs, 23 Home Assistant JSON state files, YAML presence and nonempty Kodi Sync Queue LiteDB presence. It preserves source databases/WAL, rejects symlinks and withholds secret contents. Seven local tests pass.
- Kodi Sync Queue [opens LiteDB](https://github.com/jellyfin/jellyfin-plugin-kodisyncqueue/blob/master/Jellyfin.Plugin.KodiSyncQueue/Data/DbRepo.cs), not SQLite. The initial header failure was corrected; presence is not LiteDB integrity proof.
- `backup/test-sonarr-restore.py` passed native startup/API on 4.0.20.3014 with four matching restored series IDs. It used the exact owner-confirmed image ID, a disposable config copy, network none, no published ports/media/socket mounts and removed its test container/copy. Four local simulated lifecycle tests pass.

To repeat these completed tests from a reviewed checkout:

```bash
sudo python3 backup/validate-restored-state.py /srv/backups/restore-validation.Nz6ggIgG
sudo python3 backup/test-sonarr-restore.py /srv/backups/restore-validation.Nz6ggIgG
```

Owner explicitly selected one representative application-start test as sufficient for V1 and deferred further app-start tests. Untested: Home Assistant/Jellyfin startup, LiteDB integrity, YAML/PEM semantics, UI login, real media/download integrations and a full-host rebuild. These are scope limits, not failed V1 checks.

Current host had 1.7 GiB available RAM, but Docker reported 0B/0B and unsupported memory limits. The Sonarr test starts only one app and checks MemAvailable (at least 1 GiB before start; stop if below 384 MiB during startup), rather than claiming an enforced memory ceiling. Optional future tests should keep household/device access isolated.

Restore test and rollback copies remain private/local; no cleanup has been performed. Jellyfin-over-Tailscale login and Gluetun pinning are now complete. Next work is independent recovery secrets and backup visibility; additional restored application starts remain optional/deferred.
