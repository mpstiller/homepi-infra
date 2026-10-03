# Media stack

See `LLM_CONTEXT.md` sections 11–21 for the detailed current settings.

## Services

- Seerr — request UI
- Sonarr — TV automation
- Radarr — movie automation
- Prowlarr — indexer management
- qBittorrent — download client
- Gluetun — VPN gateway / kill switch for qBittorrent only
- Proton VPN — WireGuard provider with port forwarding
- FlareSolverr — authorized headless-browser proxy for selected/tagged sources
- Jellyfin — playback/library

## Current operational status

The Sonarr path has been tested end to end with actual downloads and hardlink imports. The next equivalent test should be Radarr.

## qBittorrent path rules

Never use the obsolete `/downloads` paths from the initial container defaults. The correct container paths are under `/data`.

```text
Default save: /data/torrents
Incomplete:   /data/torrents/incomplete
sonarr:       /data/torrents/tv
radarr:       /data/torrents/movies
```

Default Torrent Management Mode must remain `Automatic` so category paths take effect.

## Cleanup

Current cleanup is manual after successful import/hardlink verification. Automatic seeding limits/cleanup are the next design task.
