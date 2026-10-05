# Current State

**Live verified:** 2026-10-05

## Stable / confirmed from the running Pi

- Raspberry Pi 5 boots from Samsung 990 EVO Plus 2 TB NVMe.
- Debian GNU/Linux 13.7 (trixie), kernel `6.18.39+rpt-rpi-2712`.
- Root filesystem is `/dev/nvme0n1p2` (ext4), about 1.8 TiB.
- At the audit: 78 GiB used (5%), temperature 43.9 °C.
- Bootloader is current as of 2026-05-26; `BOOT_ORDER=0xf461`.
- Docker Engine `29.8.0`, Docker Compose `v5.5.1`.
- Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the complete media stack are running.
- Live Compose files are now checked into this repository for Arcane, Homepage, Home Assistant, Jellyfin and the media stack.
- The running Music Assistant deployment source still needs to be resolved from Docker runtime metadata; no Compose file was captured from the expected stack directory.
- Sony TV Jellyfin Direct Play was previously tested successfully.
- Home Assistant has Google Cast, Sony TV, Sonos, and Music Assistant integrations.
- SoundCloud works in Music Assistant.
- qBittorrent is isolated behind Proton VPN via Gluetun.
- Proton WireGuard, kill switch, public-IP separation and dynamic port forwarding were tested successfully.
- Live qBittorrent v5.2.3 is bound to `tun0` and `0.0.0.0` (All IPv4 addresses).
- Prowlarr -> Sonarr/Radarr Full Sync works.
- Seerr Automatic Search is enabled.
- Sonarr end-to-end workflow and hardlink import have succeeded in real use.

## Current media configuration

### Paths

```text
/data/torrents/tv
/data/torrents/movies
/data/torrents/incomplete
/data/media/tv
/data/media/movies
```

Host equivalents are under `/srv/data`.

### qBittorrent categories

```text
sonarr -> /data/torrents/tv
radarr -> /data/torrents/movies
test   -> /data/torrents/test
```

### qBittorrent live share-limit state

The audit shows:

```text
max_ratio_enabled        false
max_seeding_time         30
max_seeding_time_enabled true
```

The exact global share-limit action (pause/remove/etc.) still needs to be captured before automatic cleanup is finalized.

### Quality profile

`HomePi 1080p`, 1080p Bluray+WEB group, German/Dual-Language CF scoring, no 4K/720p/remux in V1.

## P0 documentation status

Completed:

- live Compose synced for Arcane, Homepage, Home Assistant, Jellyfin and media;
- safe environment templates checked in for stacks that currently use `.env`;
- live OS/storage/Docker snapshot documented;
- restore runbook added.

Still required before P0 is closed:

1. capture exact Docker image digests and application versions;
2. resolve Music Assistant's actual deployment/Compose source;
3. query the running *arr/Prowlarr/Seerr/Home Assistant configuration through sanitized local APIs/files;
4. reconcile those results against `LLM_CONTEXT.md`.

## Immediate resume point

Run `scripts/export-live-config-audit.sh` on the Pi and import its sanitized bundle. Once P0 is closed, continue directly with:

1. Radarr movie end-to-end test;
2. Radarr hardlink verification;
3. finalize qBittorrent seeding/cleanup behavior;
4. Jellyfin library/Direct Play verification.
