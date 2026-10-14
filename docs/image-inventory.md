# Container image inventory

**Captured:** 2026-10-14 15:42:40 CEST (owner-supplied read-only collector output).

The running deployment is now documented after the October update window. The raw selected-field snapshot is in `audits/image-inventory-2026-10-14.json`; the former exact baseline is archived in `audits/image-inventory-2026-10-05.md`. No pull, update, restart or configuration change was performed by the inventory.

## Results

- 13 containers running; no collection errors.
- All configured local image references match their running container image IDs. This does not check whether remote registry tags have moved or whether newer releases exist.
- All four declared healthchecks report healthy (Arcane, Gluetun, Homepage, Jellyfin). Other containers have no health result in this snapshot; running alone is not a full application-health test.
- RestartCount is 0 for all containers at capture; this is not a lifetime/manual-restart history.
- All images are Linux/arm64. Docker 29.8.0; Compose 5.5.1; kernel 6.18.39+rpt-rpi-2712; host aarch64.
- 11 recorded digests changed versus the 2026-10-05 baseline. Gluetun and FlareSolverr remain on the same captured digest. Changed digests need not imply a new app-version change on the inventory date.

## Version evidence

Live/API or installed-version evidence is distinguished from image labels. A version label is image metadata, not an independent running-app API query.

| Container | Version / label | Evidence | Status |
|---|---|---|---|
| arcane | `v2.15.1` | image version label only | running / healthy |
| flaresolverr | `v3.5.2` | image version label only | running / no health result |
| gluetun | `latest (semantic version unknown)` | image version label only | running / healthy |
| homeassistant | `2026.10.0` | installed Python version constant | running / no health result |
| homepage | `v2.4.0` | image version label only | running / healthy |
| homepage-socket-proxy | `3.4.6-r0-ls101` | image version label only | running / no health result |
| jellyfin | `12.2.0` | local public server-info API | running / healthy |
| music-assistant | `2.10.5` | image version label only | running / no health result |
| prowlarr | `2.6.5.5623` | local status API | running / no health result |
| qbittorrent | `v5.2.4` | local qBittorrent version API via Gluetun | running / no health result |
| radarr | `6.4.4.10685` | local status API | running / no health result |
| seerr | `v3.5.0` | image version label only | running / no health result |
| sonarr | `4.0.20.3014` | local status API | running / no health result |

## Exact recorded image references

RepoDigests are recorded repository references, suitable for identifying the captured image. Running image IDs are separately retained in the JSON; do not assume the two kinds of identifier are interchangeable. Rolling `latest`/`stable` tags remain unchanged in Compose and are not pinned by this documentation update.

| Container | Configured reference | Captured RepoDigest |
|---|---|---|
| arcane | `ghcr.io/getarcaneapp/manager:latest` | `ghcr.io/getarcaneapp/manager@sha256:540c01198ca3e58dfd398d25c57c8dc241fa7e7f3d1d8d646c8268f19525b1a8` |
| flaresolverr | `ghcr.io/flaresolverr/flaresolverr:latest` | `ghcr.io/flaresolverr/flaresolverr@sha256:c80ae007ce2ccdcd217a12426e4f039ef763ff90738c808d38810c3e59323767` |
| gluetun | `qmcgaw/gluetun:latest` | `qmcgaw/gluetun@sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793` |
| homeassistant | `ghcr.io/home-assistant/home-assistant:stable` | `ghcr.io/home-assistant/home-assistant@sha256:1b64d38f38d922bf9d59336451fd6453e1d614f934456af4ee3d2a51061be3a4` |
| homepage | `ghcr.io/gethomepage/homepage:latest` | `ghcr.io/gethomepage/homepage@sha256:643bd0be730d40f69d58028a55d1a896739333e8815786df42bc97f109ecbe61` |
| homepage-socket-proxy | `lscr.io/linuxserver/socket-proxy:latest` | `lscr.io/linuxserver/socket-proxy@sha256:362cadf55b3c7920189347d0f4d60b389e2f80e929581bf10793f2371aab41e5` |
| jellyfin | `jellyfin/jellyfin:latest` | `jellyfin/jellyfin@sha256:357724bf0ae27a672c7cbaa899db2d9abeb13dbd8657ccce750258a4c059d037` |
| music-assistant | `ghcr.io/music-assistant/server:latest` | `ghcr.io/music-assistant/server@sha256:28023f8c0d96ca2496391f3218a6d70d7ef3ba84db846b3a3f3cd9ce7ef8aedc` |
| prowlarr | `lscr.io/linuxserver/prowlarr:latest` | `lscr.io/linuxserver/prowlarr@sha256:f9151e5bc1025c6d0a630d503210cdcb6bb55a7cc098562609d96a408d838902` |
| qbittorrent | `lscr.io/linuxserver/qbittorrent:latest` | `lscr.io/linuxserver/qbittorrent@sha256:b522f9f4b769f8f36d49d22d5eb6a92e9aa18904c6a1830b1439df511ec21983` |
| radarr | `lscr.io/linuxserver/radarr:latest` | `lscr.io/linuxserver/radarr@sha256:7dfd049e79c00b16fbc29c3f5d96a9e7b9e73a23930b4c5b3c4541d60b366814` |
| seerr | `ghcr.io/seerr-team/seerr:latest` | `ghcr.io/seerr-team/seerr@sha256:27602401178d54f1964442287b9f23f67a3fa2252645ee8065839ea1c3f69e45` |
| sonarr | `lscr.io/linuxserver/sonarr:latest` | `lscr.io/linuxserver/sonarr@sha256:f247545d23ba8b233d6604575347e48a623fe6ad75dda02348bf81917f3b5c06` |

## Resource support and follow-ups

Docker explicitly reports memoryLimit=false and swapLimit=false. Host available RAM was about 1.56 GiB and swap usage about 275 MiB at capture. Earlier 0B/0B Docker stats and unsupported-limit warnings are consistent with this finding; the cause has not been diagnosed.

- Investigate cgroup/kernel/boot configuration in a separate read-only step before relying on Docker memory/swap limits or adding heavy workloads. No boot/runtime change is made here.
- Gluetun intentionally remains on the previously validated working digest. Evaluate pinning that known image separately; do not blindly refresh latest. Preserve qBittorrent isolation, interface binding, forwarded port and kill switch.
- Refresh inventory after future intentional updates, keeping date/source and API-vs-label evidence clear. This capture does not establish that software is the newest available or vulnerability-free.

## Collector

Run `scripts/capture-image-inventory.py` on the Pi as root. It reads selected container/image templates and local versions without exporting container environments, arbitrary labels, ports/mount contents or logs. API keys used for local *arr authentication are never printed; only the version field is retained. Error output excludes request headers/config bodies. Other services retain image labels without claiming live API verification.

[Docker inspect reference](https://docs.docker.com/reference/cli/docker/inspect/), [image inspect reference](https://docs.docker.com/reference/cli/docker/image/inspect/).
