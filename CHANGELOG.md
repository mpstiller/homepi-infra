# Changelog

## 2026-10-15

- Owner pinned Gluetun to the previously validated digest `qmcgaw/gluetun@sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793` in the actual media Compose file; mirrored the one-line change locally. No image pull/update was performed; Gluetun and qBittorrent were recreated together.
- Owner confirmed matching Gluetun/qBittorrent namespace IDs, `tun0` / `0.0.0.0`, matching forwarded/listen ports and different host/VPN public IPv4 addresses. A fixed-IP HTTP target was reachable before the tunnel-down test and failed with `tun0` DOWN before/after the request; this is a targeted IPv4 check, not exhaustive leak testing.
- Recorded the recovery interruption: manually raising the tunnel left qBittorrent on `lo` / port `0`; a Gluetun-only Docker restart left the qBittorrent API unreachable from Gluetun. Recreating both restored API `v5.2.4`, binding, matching dynamic port `33266` and outbound connectivity. Namespace mismatch is a possible explanation, not a proven diagnosis. Added maintenance/recovery guidance and scope limits.
- Confirmed PR #7 is merged and moved the current roadmap/handoff to independent recovery secrets and backup visibility. Changes remain local for owner review/commit/publication; historical inventory JSON is unchanged.

## 2026-10-14

- Recorded owner-requested session handoff: PR #7 open at handoff, completed/untested boundaries, no scheduled Pi actions, and concrete next Gluetun pinning evaluation followed by backup visibility/recovery-secret follow-ups.

- Resolved missing Docker memory/swap-limit support: diagnosed the disabled memory controller, applied a guarded `cgroup_enable=memory` boot override with rollback, then owner verified the memory controller and both Docker support flags after reboot. All 13 containers running; four configured healthchecks healthy. Five local boot-line tests passed. Per-service caps were not assigned; enforcement under memory pressure remains untested.

- Recorded owner read-only image inventory at 15:42 CEST: 13 running containers, all local references match running IDs, no capture errors. Archived Oct 5 baseline and added selected-field JSON snapshot; distinguish six directly queried app versions from image labels.
- Confirmed 11 digest changes vs Oct 5 while Gluetun/FlareSolverr remain unchanged. Recorded missing Docker memory/swap-limit support as a separate diagnostic follow-up; no pull/update/restart/configuration change performed.


- Added and owner-verified Jellyfin Homepage widget version 2 (movie/series/episode counts and Now Playing, user/media controls disabled). Key remains local in verified stack env_file; only blank template variable is checked in. Corrected prior env-file path prose and recreated Homepage alone without pulling an image.
- Resolved Jellyfin-over-Tailscale server-connection failure: owner confirmed EnableRemoteAccess=false, applied a one-field guarded change to true with private rollback and restart, then verified both hostname/IP API HTTP 200 and browser login. Router/Tailscale/IP-filter policy unchanged; remote playback remains untested. Three local XML-edit tests passed.
- Updated roadmap/handoff/Homepage docs to remove the remote-login blocker; Jellyfin widget remains optional/unconfigured.
- Captured installed backup/maintenance scripts and four units, then installed shared flock and explicit restart-failure/EXIT cleanup handling. Eight local simulated tests passed; owner verified native lock, timers and successful real backup/maintenance runs.
- Saved snapshot `b37715a7` (334.493 MiB); owner restored all 3236 files/directories to a private test directory and confirmed direct `srv/appdata` / `opt/homelab/stacks` restore roots. Corrected the earlier inferred staging-prefix mapping.
- Owner passed 41 copied-state checks (13 SQLite, three XML, 23 JSON, YAML/LiteDB presence). Corrected Kodi Sync Queue's mistaken SQLite classification; LiteDB integrity remains untested. Seven local checker tests passed.
- Owner validated isolated Sonarr restored startup on 4.0.20.3014 with four matching series IDs; test container/copy removed. Four local simulated lifecycle tests passed.
- Closed Backup V1 with the owner's agreed representative-start-test scope; additional app starts/full-host recovery remain optional/deferred. Independent recovery secrets, backup visibility and retained restore-data cleanup remain separate follow-ups.
- Updated roadmap/handoff to resume Jellyfin-over-Tailscale next. No claim is made that the prepared Jellyfin test was executed; it was omitted from the final V1 scope.
- Removed obsolete manual restic snapshot `bd21d171` after automated-backup validation, then pruned unreferenced data.

## 2026-10-13

- Added and validated monthly restic maintenance via systemd: `prune` followed by `check`, scheduled for the 1st of each month at 05:30.
- Added and validated the systemd-managed HomePi backup flow; configured a dedicated restic cache (`XDG_CACHE_HOME=/var/cache/homepi-backup`) so automated runs complete cleanly.
- Validated the production-style restic staging backup with cache/log exclusions; the automatic snapshot size dropped to `333.155 MiB` and services were restarted before cloud upload.
- Verified the first restic backup by restoring data to a temporary path and running `restic check`; both completed successfully.
- Initialized an encrypted restic repository in Google Drive via rclone and completed the first manual backup of `/srv/appdata` and `/opt/homelab/stacks`; restore testing remains pending.

## 2026-10-08

- Completed post-update Jellyfin validation on `12.2.0` (UI, libraries, Seerr integration, playback, Kodi/JellyCon) and intentionally deferred Gluetun while the current VPN/kill-switch/port-forwarding path remains healthy.
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
