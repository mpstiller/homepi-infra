# Live application configuration

**Captured:** 2026-10-05

This file summarizes sanitized settings read from the running applications. It contains no API keys or login credentials.

## Sonarr

- Version: `4.0.19.2979`
- Root folder: `/data/media/tv`
- Hardlinks: enabled
- Completed Download Handling: enabled
- qBittorrent client:
  - enabled
  - Remove Completed: **enabled**
  - Remove Failed: **enabled**
- Current synced indexer: `EZTV (Prowlarr)`
- Automatic/RSS/Interactive search: enabled for that indexer
- Custom formats:
  - German
  - German DL
  - German DL (undefined)
  - Not German or English

### HomePi 1080p profile

Live profile ID: `7`

```text
Upgrade allowed                    true
Minimum Custom Format Score        0
Upgrade Until Custom Format Score  11000

German DL                 11000
German DL (undefined)     11000
German                    10000
Not German or English    -35000
```

Allowed quality group:

```text
Bluray + WEB 1080p
  - WEBRip-1080p
  - WEBDL-1080p
  - Bluray-1080p
```

HDTV-1080p, 720p, Remux and 2160p are disabled in this profile.

## Radarr

- Version: `6.3.0.10514`
- Root folder: `/data/media/movies`
- Hardlinks: enabled
- Completed Download Handling: enabled
- qBittorrent client:
  - enabled
  - Remove Completed: **enabled**
  - Remove Failed: **enabled**
- Current synced indexer: `YTS (Prowlarr)`
- Automatic/RSS/Interactive search: enabled for that indexer

### HomePi 1080p profile

Live profile ID: `7`

```text
Upgrade allowed                    true
Minimum Custom Format Score        0
Upgrade Until Custom Format Score  11000

German DL                 11000
German DL (undefined)     11000
German                    10000
Not German or English    -35000
```

Allowed quality group:

```text
Bluray + WEB 1080p
  - WEBDL-1080p
  - WEBRip-1080p
  - Bluray-1080p
```

HDTV-1080p, 720p, Remux and 2160p are disabled in this profile.

## Prowlarr

Version: `2.5.2.5491`

Connected applications:

- Sonarr — Full Sync
- Radarr — Full Sync

Current indexers:

- BT.etree
- EZTV
- YTS

All are currently public torrent indexers and carry the FlareSolverr proxy tag.

Indexer proxy:

- FlareSolverr, tagged

The synchronized categories currently result in:

- EZTV appearing in Sonarr
- YTS appearing in Radarr

## Seerr

Jellyfin server:

- name: HomePi
- host currently stored as `192.168.178.75:8096`
- SSL: off
- libraries enabled: Filme, Serien

Radarr service:

```text
host               radarr:7878
root               /data/media/movies
default            true
selected profile   HD-1080p (ID 4)
```

Sonarr service:

```text
host               sonarr:8989
root               /data/media/tv
default            true
selected profile   HD-1080p (ID 4)
```

### Important configuration mismatch

The intended production profile is `HomePi 1080p` (ID 7) in both Sonarr and Radarr, but Seerr is still configured to create requests with the old `HD-1080p` profile (ID 4).

**Before the next real media request, update both Seerr services to `HomePi 1080p`.**

This explains why requests created through Seerr can bypass the German/Dual-Language scoring even though the HomePi profile itself is configured correctly in Sonarr/Radarr.

## qBittorrent cleanup chain

Live qBittorrent v5.2.3:

```text
global seeding-time limit        enabled
seeding time                     30 minutes
ratio limit                      disabled
share-limit action               0 = Stop torrent
```

All three categories currently inherit the global share-limit policy:

```text
radarr   seeding_time_limit = -2   share_limit_action = Default
sonarr   seeding_time_limit = -2   share_limit_action = Default
test     seeding_time_limit = -2   share_limit_action = Default
```

Therefore the intended automated flow is already almost complete:

```text
download
 -> *arr imports via hardlink
 -> qBittorrent seeds for 30 minutes
 -> qBittorrent stops torrent
 -> Sonarr/Radarr sees seed goal reached + stopped
 -> Remove Completed removes torrent and torrent-side data
 -> media hardlink remains as the only link
```

This cleanup behavior should be validated with the upcoming Radarr end-to-end test before being considered production-proven.

## Home Assistant integrations

Live config entries include:

- Thread
- Google Cast
- Bluetooth
- Sonos
- Shopping List
- Android TV Remote: Sony TV
- Music Assistant
- standard system/onboarding integrations

Matter is not yet configured as a Home Assistant integration, consistent with the documented plan.
