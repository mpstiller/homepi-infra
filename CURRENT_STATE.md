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
- Verified Compose definitions are now checked into this repository for Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the media stack.
- Music Assistant was historically deployed from `/srv/appdata/compose.yaml` (Compose project `appdata`); its verified definition is normalized into `stacks/music-assistant/compose.yaml`.
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

The global share-limit action is **Stop torrent**. Sonarr and Radarr both have `Remove Completed` enabled; the upcoming Radarr test will validate the full automatic cleanup chain.

### Quality profile

`HomePi 1080p`, 1080p Bluray+WEB group, German/Dual-Language CF scoring, no 4K/720p/remux in V1.

## P0 documentation status

**P0 is complete.**

The repository now contains:

- all verified Compose definitions;
- safe environment templates where required;
- exact host, Docker and image inventory;
- live Sonarr/Radarr/Prowlarr/Seerr/Home Assistant configuration snapshots;
- live naming and quality-definition values;
- a restore runbook;
- explicit architecture decisions and LLM handoff context.

## Immediate resume point

P1 Media Stack V1 starts now:

1. change Seerr's Sonarr and Radarr profile from `HD-1080p` to `HomePi 1080p`;
2. run a Radarr movie end-to-end test;
3. verify Radarr hardlinks;
4. verify automatic 30-minute seed -> stop -> *arr cleanup;
5. verify Jellyfin library import and Direct Play.

## Important live issue discovered

Seerr currently selects `HD-1080p` (profile ID 4) for **both** Sonarr and Radarr requests. The intended profile `HomePi 1080p` is live and correct as profile ID 7 in both applications.

Before the Radarr end-to-end test, change both Seerr service profiles to `HomePi 1080p`.

## Automatic cleanup live state

qBittorrent global share limits currently seed for 30 minutes and then **Stop** the torrent. Both Sonarr and Radarr have per-client `Remove Completed` enabled. According to the supported *arr/qBittorrent workflow, this should allow *arr to remove a successfully imported torrent and its torrent-side data after qBittorrent reaches the seed goal and stops it. The upcoming Radarr test will validate this end to end.
