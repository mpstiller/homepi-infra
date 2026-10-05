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
- Music Assistant runtime metadata identifies its Compose source as `/srv/appdata/compose.yaml` (Compose project `appdata`), using host networking and `/srv/appdata/music-assistant:/data`. The actual Compose file still needs to be safely imported.
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

1. safely import the actual Music Assistant Compose file from `/srv/appdata/compose.yaml`;
2. capture final naming/quality-definition settings that were not exposed by the first API audit;
3. reconcile those last details against `LLM_CONTEXT.md`.

## Immediate resume point

Second live-config audit imported. Before P0 is closed, import the Music Assistant Compose source and the remaining naming/quality-definition details. Then continue directly with:

1. Radarr movie end-to-end test;
2. Radarr hardlink verification;
3. finalize qBittorrent seeding/cleanup behavior;
4. Jellyfin library/Direct Play verification.


## Important live issue discovered

Seerr currently selects `HD-1080p` (profile ID 4) for **both** Sonarr and Radarr requests. The intended profile `HomePi 1080p` is live and correct as profile ID 7 in both applications.

Before the Radarr end-to-end test, change both Seerr service profiles to `HomePi 1080p`.

## Automatic cleanup live state

qBittorrent global share limits currently seed for 30 minutes and then **Stop** the torrent. Both Sonarr and Radarr have per-client `Remove Completed` enabled. According to the supported *arr/qBittorrent workflow, this should allow *arr to remove a successfully imported torrent and its torrent-side data after qBittorrent reaches the seed goal and stops it. The upcoming Radarr test will validate this end to end.
