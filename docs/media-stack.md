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

### Seerr profile alignment

Seerr now points both Sonarr and Radarr requests to `HomePi 1080p` (ID 7). The previous `HD-1080p` mismatch is resolved.

### Cleanup configuration

qBittorrent currently seeds for 30 minutes and then uses the **Stop torrent** share-limit action. Sonarr and Radarr both have `Remove Completed` enabled. The Radarr end-to-end test will validate that this results in automatic torrent/download cleanup after the hardlink import.


## Anime handling

Anime uses the same Sonarr instance but a separate quality profile: `HomePi Anime 1080p`.

Seerr mapping:

```text
Normal series -> HomePi 1080p
Anime         -> HomePi Anime 1080p
```

Both use `/data/media/tv`.

The Anime profile follows the TRaSH-style Anime tier model. Image/release quality is dominant. Original audio is required; raws, dub-only releases, low-quality Anime groups and AV1 are rejected. Dual Audio is scored only as a small tie-breaker, so it cannot outrank a materially better Anime tier.

The Anime naming template includes both `SxxExx` and absolute numbering. Normal-series naming remains unchanged.


### Radarr cleanup validation

A real Radarr movie request completed successfully.

Observed sequence:

```text
download to /data/torrents/movies
-> successful Radarr import
-> 30-minute qBittorrent seed limit reached
-> torrent stopped
-> Radarr Remove Completed removed torrent + torrent-side file
-> media file remained under /data/media/movies
```

The final media file had link count `1` after cleanup and no corresponding file remained in `/srv/data/torrents/movies`.

This validates the automatic cleanup behavior. A final Radarr log check is retained only to prove whether that specific import used a hardlink before cleanup.


### Jellyfin movie validation

The Radarr-imported movie appeared automatically in Jellyfin and was played on the Sony TV using **Direct Play**. No transcoding was required.

This validates the intended design principle for the Raspberry Pi 5: media should normally be served as Direct Play rather than relying on heavy server-side video transcoding.


### Sony TV playback compatibility

A real-world compatibility issue was isolated with a 1080p HEVC Main 10 release containing TrueHD audio.

The native Jellyfin Android TV client on the Sony KD-65AF9 stuttered, especially on the Japanese TrueHD 2.0 track. Forcing audio downmix triggered Direct Stream but worsened playback.

The exact same file:

- played cleanly on macOS
- played cleanly on the Sony TV using Kodi + JellyCon

Therefore the problem is attributed to the native Jellyfin Android TV playback path on the Sony rather than the media file, server, or network.

Operational guidance:

- keep Sonarr/Radarr quality-first
- do not hard-exclude TrueHD solely for Sony compatibility
- prefer Kodi + JellyCon for releases that stutter in the native Jellyfin TV client
