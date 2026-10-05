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


## Live HomePi profile verification

Both Sonarr and Radarr have `HomePi 1080p` as profile ID 7 with:

```text
German DL                 11000
German DL (undefined)     11000
German                    10000
Not German or English    -35000
Minimum CF score              0
Upgrade-until CF score    11000
```

The 1080p group contains WEB-DL, WEBRip and Bluray 1080p only.

Exact live naming and size definitions are in `docs/media-quality-naming.md`.

### Seerr mismatch to fix

Seerr still points both Sonarr and Radarr requests to the old `HD-1080p` profile (ID 4). Change both services to `HomePi 1080p` (ID 7) before the next request.

### Cleanup configuration

qBittorrent currently seeds for 30 minutes and then uses the **Stop torrent** share-limit action. Sonarr and Radarr both have `Remove Completed` enabled. The Radarr end-to-end test will validate that this results in automatic torrent/download cleanup after the hardlink import.
