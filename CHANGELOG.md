# Changelog

## 2026-10-08

- Updated Jellyfin from `12.0.0` to `12.2.0`; database migrations completed successfully, Kodi Sync Queue loaded, library watchers started, and Core startup completed cleanly.
- Updated Home Assistant from `2026.9.2` to `2026.10.0`; Core startup succeeded. A separate FRITZ! SSDP discovery flow logged a hostname parsing error for `fritz.powerline`, to be monitored independently.
- Closed the main container maintenance window: documented completed updates, intentional Gluetun/Home Assistant/Jellyfin deferrals, successful post-maintenance reboot, and the need to refresh exact image digests.
- Updated qBittorrent to `5.2.4`; WebUI started cleanly and post-update checks confirmed `tun0`, All IPv4 (`0.0.0.0`), and the Proton forwarded listen port remained correct.
- Updated Music Assistant to `2.10.5`; startup completed cleanly, web/stream servers came up, and SONOS/Chromecast/DLNA providers loaded successfully.
- Updated Arcane to `2.15.1`; database migrations completed successfully and the post-start image scan checked 14 images with 0 errors, leaving 5 images with updates available.

## 2026-10-07

- Completed Homepage V1: final smoke test passed, current widgets and service links validated, reproducible live configuration captured in Git; Jellyfin widget remains intentionally deferred.
- Captured the exact live Homepage Compose and sanitized dashboard YAMLs into Git, added safe widget variable names to `.env.example`, reconciled the live System group (Arcane + Gluetun), and closed the Homepage reproducibility gap.
- Reconciled Homepage V1 remaining work: documented the live Compose drift (`env_file` + `host.docker.internal:host-gateway`), pending sanitized runtime-config capture, Jellyfin deferral, Arcane decision, and final smoke-test criteria; expanded the roadmap accordingly.
- Updated Seerr to `3.5.0`; startup completed without errors, Jellyfin Movies/Series sync completed successfully, and Automatic Search is enabled for both Sonarr and Radarr.
- Updated Radarr from `6.3.0.10514` to `6.4.4.10685`; startup, SQLite checks, and service binding completed without errors.
- Updated Sonarr from `4.0.19.2979` to `4.0.20.3014`; startup, SQLite checks, and service binding completed without errors.
- Updated Prowlarr from `2.5.2.5491` to `2.6.5.5623`; startup, SQLite checks, and service binding completed without errors.
- Recorded the implemented Homepage service-group layout and confirmed the Sonarr native widget is working.
- Confirmed the Radarr native Homepage widget is also working.
- Confirmed the Prowlarr native Homepage widget is working.
- Confirmed the qBittorrent native Homepage widget is working through the Gluetun-published host port.
- Confirmed the Seerr native Homepage widget is working.
- Deferred the Jellyfin Homepage widget because the documented Jellyfin-over-Tailscale issue currently blocks remote admin/API-key setup.
- Confirmed the Home Assistant native Homepage widget is working.
- Documented that Homepage API keys remain in the local `.env` and are not committed.
- Added `docs/homepage.md` as the dashboard-specific handoff and documented that the live Homepage YAML files are not yet synchronized into Git.
- Removed stale handoff instructions that still treated the Seerr profile mismatch, Radarr validation, and private overlay selection as unfinished.
- Aligned the roadmap and LLM context with the implemented/hardened Tailscale setup and the current Homepage widget workstream.
- Kept the Jellyfin-over-Tailscale connection problem documented as a separate unresolved issue.

## 2026-10-06

- Isolated a Sony Jellyfin Android TV playback issue with HEVC Main 10 + TrueHD media.
- Confirmed the same file plays cleanly on macOS and on the Sony via Kodi + JellyCon.
- Decided to keep Sonarr/Radarr quality-first and use Kodi/JellyCon as a compatibility fallback instead of hard-excluding TrueHD.

- Confirmed Jellyfin automatically detected the Radarr-imported movie.
- Confirmed Direct Play on the Sony TV with no transcoding, validating the movie playback path end to end.

- Validated a real Radarr end-to-end movie request through Seerr/Prowlarr/qBittorrent.
- Confirmed qBittorrent used the `radarr` category and movie download path.
- Confirmed the 30-minute seed -> Stop -> Radarr Remove Completed cleanup chain removes the torrent and torrent-side data while preserving the imported media file.

- Hardened the Tailnet: Device Approval enabled, default allow-all removed, owner-only HomePi access, explicit port allowlist, server key expiry disabled, and Tailscale auto-update enabled.

- Installed and joined Tailscale on HomePi.
- Verified remote access from iPhone over cellular.
- HomePi Tailscale IPv4 is `100.72.110.114`; MagicDNS hostname is `homepi`.
- Updated Homepage host validation for LAN and Tailscale access.
- Kept qBittorrent Internet traffic isolated through Gluetun + Proton VPN.


## 2026-10-05

- Added `HomePi Anime 1080p` in Sonarr with Anime-specific tier scoring, original-audio requirement, raw/dub-only/LQ exclusions, and low-weight Dual Audio preference.
- Added Anime-specific episode naming with absolute numbering.
- Configured Seerr to use `HomePi Anime 1080p` for Anime while keeping `HomePi 1080p` for normal series.

- Updated Seerr so both Sonarr and Radarr requests use `HomePi 1080p` (profile ID 7); resolved the old `HD-1080p` mismatch.

- Audited the running Pi with a sanitized export bundle.
- Verified Debian 13.7, kernel 6.18.39+rpt-rpi-2712, NVMe root, Docker 29.8.0 and Compose v5.5.1.
- Synchronized live Compose files for Arcane, Homepage, Home Assistant, Jellyfin and the media stack.
- Added safe stack-specific `.env.example` files.
- Verified qBittorrent v5.2.3 live paths, `tun0` + All IPv4 binding, and current global 30-minute seeding-time limit.
- Added live-system documentation and a restore runbook.
- Identified that Music Assistant is running but its expected Compose file was not present in the first stack export; scheduled runtime-label inspection.
- Added a second sanitized live-configuration audit script for application settings, exact image metadata and deployment-source reconciliation.
- Imported the second live audit with exact running image digests and Sonarr/Radarr/Prowlarr settings.
- Detected a live Seerr profile mismatch: both Sonarr and Radarr requests still use `HD-1080p` instead of `HomePi 1080p`.
- Confirmed qBittorrent's 30-minute seed limit uses the Stop action and both *arr clients have Remove Completed enabled.
- Identified Music Assistant's deployment source as `/srv/appdata/compose.yaml` via Docker Compose labels.
- Imported the actual Music Assistant Compose definition and normalized it under `stacks/music-assistant/`.
- Verified Home Assistant `2026.9.2` and Jellyfin `12.0.0`.
- Captured exact live Sonarr/Radarr naming templates and quality definitions.
- Corrected the documented Radarr WEB-1080p preferred size from reconstructed 100 MB/min to the live value of 99 MB/min.
- Closed P0 reproducibility baseline; repository is now the documented source of truth for the current HomePi deployment.


## 2026-10-03

- Created first portable `homepi-infra` documentation baseline from setup history.
- Established `LLM_CONTEXT.md`, `CURRENT_STATE.md`, roadmap, architecture docs, and secret-handling rules.

## 2026-09 (reconstructed)

- Migrated Raspberry Pi system from 64 GB microSD to Samsung 990 EVO Plus 2 TB NVMe using `rpi-clone`.
- Confirmed direct NVMe boot and ~1.8 TB root filesystem.
- Deployed Docker base stack: Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin.
- Added media automation stack: qBittorrent, Sonarr, Radarr, Prowlarr, Seerr.
- Added Gluetun + Proton VPN WireGuard around qBittorrent only.
- Verified VPN IP isolation, kill switch, and Proton port forwarding.
- Fixed qBittorrent startup race for dynamic port-forward update.
- Fixed qBittorrent 5.2.3 network binding by using `tun0` + All IPv4 addresses.
- Added FlareSolverr as a private/tagged Prowlarr proxy.
- Added German/Dual-Language TRaSH custom formats and HomePi 1080p profiles.
- Fixed `/downloads` path issues and moved media workflow to common `/data` layout.
- Enabled qBittorrent Automatic Torrent Management so category save paths are applied consistently.
- Completed first real Sonarr end-to-end workflow and verified hardlinks.
