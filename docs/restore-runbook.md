# HomePi restore runbook

This runbook describes how to reconstruct the host architecture. A full disaster-recovery procedure still depends on the backup system planned in the backup roadmap.

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

Clone `mpstiller/homepi-infra` and copy/symlink the verified stack directories into `/opt/homelab/stacks`.

Do not deploy placeholder documentation as runtime configuration. Only stack directories containing verified `compose.yaml` files are deployment-ready.

## 4. Restore secrets

Create local `.env` files from the corresponding `.env.example` files.

Required secrets currently include at least:

- Arcane encryption key
- Proton WireGuard private key

Application API keys and login credentials normally live in restored appdata and must not be committed to Git.

## 5. Restore persistent application state

Restore `/srv/appdata` from backup before starting the services if the intent is to recover the existing Home Assistant/Jellyfin/*arr state.

Important state includes:

- Home Assistant `.storage`, YAML and database
- Music Assistant databases/settings
- Jellyfin config
- Sonarr/Radarr/Prowlarr databases/config
- qBittorrent config and torrent state
- Seerr config/database
- Gluetun persistent state if required

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

Music Assistant deployment source is currently marked **VERIFY ON PI** and must be resolved before this runbook is considered sufficient for a total rebuild.

## 7. Media-stack validation

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
