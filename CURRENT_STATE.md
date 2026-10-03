# Current State

**Last reconstructed from setup conversation:** 2026-10-03

## Stable / confirmed

- Raspberry Pi 5 boots from Samsung 990 EVO Plus 2 TB NVMe.
- Docker + Compose operational.
- Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin operational.
- Sony TV Jellyfin Direct Play tested successfully.
- Home Assistant has Google Cast, Sony TV, Sonos, and Music Assistant integrated.
- SoundCloud works in Music Assistant.
- Media stack deployed: Seerr, Sonarr, Radarr, Prowlarr, qBittorrent, Gluetun, FlareSolverr.
- qBittorrent is isolated behind Proton VPN via Gluetun.
- Proton WireGuard, kill switch, public-IP separation, and dynamic port forwarding were tested successfully.
- qBittorrent binding workaround: `tun0` + `All IPv4 addresses`.
- Prowlarr -> Sonarr/Radarr Full Sync works.
- FlareSolverr works as a tagged Prowlarr proxy path.
- Seerr Automatic Search is enabled.
- Sonarr end-to-end workflow has succeeded in real use.
- qBittorrent path layout and Automatic Torrent Management are now corrected.
- Sonarr hardlink imports were verified by inode/link count.
- Removing torrent + torrent-side data after import leaves the media hardlink intact.

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

### Quality profile

`HomePi 1080p`, 1080p Bluray+WEB group, German/Dual-Language CF scoring, no 4K/720p/remux in V1.

## Immediate resume point

The first full Sonarr workflow is complete enough to trust the architecture. The next planned work was:

1. **Run the equivalent Radarr movie end-to-end test.**
2. Configure automatic seeding/cleanup so manual qBittorrent cleanup is not required every time.
3. Verify Jellyfin behavior after those imports.

## Must verify against live Pi when access returns

- Exact `docker ps` list and image versions.
- Actual contents of `/opt/homelab/stacks/*/compose.yaml`.
- Exact current `.env.example` variable names (never copy secret values).
- Exact current production indexers in Prowlarr.
- Whether Tidal is configured in Music Assistant.
- Current qBittorrent seeding-limit configuration (not finalized in conversation).
- Exact Homepage services after later changes.
- Current disk usage and temperatures.
