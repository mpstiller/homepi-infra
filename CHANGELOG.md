# Changelog

## 2026-10-05

- Audited the running Pi with a sanitized export bundle.
- Verified Debian 13.7, kernel 6.18.39+rpt-rpi-2712, NVMe root, Docker 29.8.0 and Compose v5.5.1.
- Synchronized live Compose files for Arcane, Homepage, Home Assistant, Jellyfin and the media stack.
- Added safe stack-specific `.env.example` files.
- Verified qBittorrent v5.2.3 live paths, `tun0` + All IPv4 binding, and current global 30-minute seeding-time limit.
- Added live-system documentation and a restore runbook.
- Identified that Music Assistant is running but its expected Compose file was not present in the first stack export; scheduled runtime-label inspection.
- Added a second sanitized live-configuration audit script for application settings, exact image metadata and deployment-source reconciliation.


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
