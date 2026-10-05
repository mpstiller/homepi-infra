# Media quality and naming configuration

**Live verified:** 2026-10-05

These values were read directly from the running Sonarr and Radarr APIs.

## Sonarr naming

```text
Rename Episodes: true
Multi-Episode Style: 5 (Prefixed Range)

Series Folder:
{Series CleanTitleWithoutYear} {(Series Year)} [tvdbid-{TvdbId}]

Season Folder:
Season {season:00}

Standard Episode:
{Series CleanTitleWithoutYear} {(Series Year)} - S{season:00}E{episode:00} - {Episode CleanTitle:90} {[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```

## Sonarr 1080p quality definitions

Values are MB/min.

| Quality | Min | Preferred | Max |
|---|---:|---:|---:|
| WEBRip-1080p | 15 | 80 | 120 |
| WEBDL-1080p | 15 | 80 | 120 |
| Bluray-1080p | 50 | 100 | 150 |

These match the intended HomePi configuration.

## Radarr naming

```text
Rename Movies: true

Movie Folder:
{Movie CleanTitle} ({Release Year})

Standard Movie:
{Movie CleanTitle} {(Release Year)} - {{Edition Tags}} {[MediaInfo 3D]}{[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```

## Radarr 1080p quality definitions

Values are MB/min.

| Quality | Min | Preferred | Max |
|---|---:|---:|---:|
| WEBDL-1080p | 12.5 | 99 | 140 |
| WEBRip-1080p | 12.5 | 99 | 140 |
| Bluray-1080p | 50 | 120 | 180 |

Note: earlier reconstructed documentation said preferred `100` for Radarr WEB 1080p. The live system is authoritative and uses **99**.
