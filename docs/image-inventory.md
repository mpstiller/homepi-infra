# Container image inventory

**Captured:** 2026-10-05

The Compose files intentionally use rolling tags such as `:latest` and `:stable`. These are the exact image digests that were running at the capture point and provide a reproducible forensic baseline.

| Image | Running digest |
|---|---|
| `ghcr.io/home-assistant/home-assistant:stable` | `sha256:a1bc133af84ee6505fe2c266d9805b7c75b780dfdc188edfee3b11e8f3cd8efe` |
| `lscr.io/linuxserver/socket-proxy:latest` | `sha256:ba211325155c463a1a6e6a038c928f21447a8e60ce02ecf41302047974097e84` |
| `ghcr.io/seerr-team/seerr:latest` | `sha256:f4768de5f616248d723e05891f3345a1402123775d03bf0890dbfedc0831bda1` |
| `jellyfin/jellyfin:latest` | `sha256:baba630419915985442f315f08b0cf46d9f4c8a0cc4bd38e94a6d35751dd5ef5` |
| `ghcr.io/flaresolverr/flaresolverr:latest` | `sha256:c80ae007ce2ccdcd217a12426e4f039ef763ff90738c808d38810c3e59323767` |
| `ghcr.io/gethomepage/homepage:latest` | `sha256:f820276654539cdc2cf0169f28188d135919a7984fad76d83d8d5ff1383f3705` |
| `ghcr.io/getarcaneapp/manager:latest` | `sha256:a7005e4be1740ae7f3c0aa694ef825552271cb320b3906a98a5e8a642faa163a` |
| `qmcgaw/gluetun:latest` | `sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793` |
| `lscr.io/linuxserver/qbittorrent:latest` | `sha256:2be038f3421f60f62e8e4bf201f66f385b68e4fbc9ed3ab79051069ea22e2650` |
| `ghcr.io/music-assistant/server:latest` | `sha256:885872224fa541c0faefc936625c939ba705a00e89c180f89e877f58448ea5d5` |
| `lscr.io/linuxserver/prowlarr:latest` | `sha256:c7502a75b021d964481c129c84590b9cbc40f83aadd4e553f173871bc0deaa3c` |
| `lscr.io/linuxserver/radarr:latest` | `sha256:fe051413dfd91b383ba04910552e83fb0306895fefee275c48dafe7bb90807dc` |
| `lscr.io/linuxserver/sonarr:latest` | `sha256:82172b363f9eddc02aca544f880a044f2ceb9aaf190bc87e4454e2f705eb91d0` |

Known application versions from live APIs:

- qBittorrent: `5.2.3`
- Sonarr: `4.0.19.2979`
- Radarr: `6.3.0.10514`
- Prowlarr: `2.5.2.5491`


Additional live application versions:

- Home Assistant: `2026.9.2`
- Jellyfin: `12.0.0`


## Post-update status — 2026-10-08

The exact digest table above remains the forensic baseline captured on 2026-10-05. Several images were updated during the 2026-10-07/08 maintenance window, so those exact digests are now historical rather than the current live digest set.

Known post-update application versions:

- Prowlarr: `2.6.5.5623`
- Sonarr: `4.0.20.3014`
- Radarr: `6.4.4.10685`
- Seerr: `3.5.0`
- Arcane: `2.15.1`
- Music Assistant: `2.10.5`
- qBittorrent: `5.2.4`
- Jellyfin: `12.2.0`
- Home Assistant: `2026.10.0`

Intentionally not updated in this maintenance window:

- Gluetun
- Home Assistant
- Jellyfin

A fresh exact image-digest capture is still required to replace the 2026-10-05 digest baseline with a new live snapshot.


Maintenance decision:
- Gluetun intentionally remains on the previously validated working image after the 2026-10-08 update window. Its `:latest` tag is not being refreshed blindly; stable pinning will be evaluated separately.
