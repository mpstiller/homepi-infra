# Roadmap

**Reconciled:** 2026-10-14, using repository state and checked-in runtime configuration as primary evidence. Chat findings supplement that evidence; no new live audit was performed. P0, Homepage V1, the main update window and operational Backup V1 are complete. Unticked items below remain unverified or planned.

## Recommended execution order

1. **Backup reproducibility and application recovery.** Installed scripts/units are captured. Correct masked restart failures and add a shared backup/maintenance lock, then validate the staged restore mapping. Complete when Home Assistant/media-state recovery is documented and safely validated, with secrets available independently. The prior targeted restore/check stays complete.
2. **Jellyfin over Tailscale.** Compare LAN and remote server/API access, inspect current server/user access settings and relevant logs. Complete when manual connection, login and playback work from a remote client. Add the Homepage widget afterwards if useful; keep admin UIs private.
3. **Maintenance evidence.** Refresh the post-update image/digest and resource inventory. Evaluate Gluetun pinning separately; preserve the validated VPN path and validate binding, port forwarding and kill switch after any actual change.
4. **Lightweight backup visibility.** Choose a notification channel and detect failed or stale backups; optionally show last success in Homepage. Complete with a controlled notification test.
5. **Close remaining media checks during normal use.** Capture Radarr hardlink evidence before cleanup, decide retained authorized indexers, and verify the Kodi native-library/client synchronization workflow. These need not block unrelated work.
6. **Choose the next household capability.** Matter/smart-home integration or a browser-first e-ink UI prototype can follow stabilization. Photo/file cloud requires measured RAM/storage headroom; preserve the existing decisions to defer Immich, HDD purchase and production-app migration.


## P0 — Make the current system reproducible ✅

- [x] Sync all verified Compose definitions into this repo.
  - [x] Arcane
  - [x] Homepage
  - [x] Home Assistant
  - [x] Music Assistant
  - [x] Jellyfin
  - [x] Media stack
- [x] Add safe `.env.example` files where external environment files are used.
- [x] Capture host, Docker, application versions and exact running image digests.
- [x] Reconcile reconstructed documentation against the live Pi.
- [x] Capture live *arr/Prowlarr/Seerr/Home Assistant settings.
- [x] Capture live naming and quality definitions.
- [x] Add restore/runbook documentation.

## P1 — Finish media stack V1

- [x] Run Radarr end-to-end movie test.
- [ ] Verify Radarr hardlinks in the same way Sonarr was verified.
- [x] Validate automatic 30-minute seed -> stop -> Radarr cleanup behavior.
- [x] Confirm Jellyfin scans and Direct Play for imported material.
- [ ] Decide which authorized production indexers are retained.
- [ ] Verify Jellyfin for Kodi native Movies/TV library, initial sync, offline Sync Queue catch-up and watched-state sync on Sony TV (VERIFY ON PI/TV; server plugin loading is already confirmed).
- [x] Close Homepage V1 and make it reproducible.
  - [x] Final service-group layout implemented.
  - [x] Sonarr widget working.
  - [x] Radarr widget working.
  - [x] Prowlarr widget working.
  - [x] qBittorrent widget working.
  - [x] Seerr widget working.
  - [x] Home Assistant widget working.
  - [x] Arcane native widget configured and retained.
  - [x] Music Assistant remains link-only; Gluetun is a Docker-status card; Tailscale is intentionally not a dashboard service.
  - [ ] Jellyfin widget deferred until local/admin access is available or the Tailscale issue is resolved.
  - [x] Capture the exact live Homepage Compose file and sync the live `env_file` + `host.docker.internal:host-gateway` structure into Git.
  - [x] Commit sanitized `services.yaml`, `settings.yaml`, `widgets.yaml`, and `docker.yaml`; never commit the local Homepage `.env`.
  - [x] Run one final Homepage smoke test, including current service links over the active LAN/Tailscale access path; keep the known Jellyfin exception separate.
  - [ ] Optional: visual/global-widget polish only where it adds useful signal.

## P1 — Maintenance hygiene

- [x] Complete the 2026-10-08 low/medium-risk container update window.
- [x] Revalidate qBittorrent VPN binding and Proton forwarded port after update.
- [ ] Evaluate Gluetun separately and move away from an unpinned `:latest` update path if appropriate.
- [ ] Refresh exact image digest inventory after 2026-10-08 update window.
- [x] Update Home Assistant to `2026.10.0` and validate normal operation; monitor the separate `fritz.powerline` SSDP discovery error.
- [x] Update Jellyfin to `12.2.0` and validate startup, libraries, Seerr integration, playback, and Kodi/JellyCon.

## P1 — Backups

- [x] Choose restic.
- [x] Initialize encrypted restic repository in Google Drive and complete first backup of `/srv/appdata` and `/opt/homelab/stacks`.
- [x] Automate recurring backups and retention.
  - [x] Add and validate separate monthly restic prune/check maintenance job.
  - [x] Validate production-style staging backup with cache/log excludes (333.155 MiB snapshot).
  - [x] Install and enable systemd service/timer; manual systemd execution validated successfully.
- [x] Capture installed backup/maintenance scripts and all four systemd units in Git; review retention/excludes, restart failure handling and overlap behavior.
- [ ] Correct masked container restart failures and add/validate a shared backup/maintenance lock; the captured live baseline is not yet hardened.
- [ ] Verify independent recovery access to the restic password, rclone OAuth configuration and application secrets.
- [ ] Document staging-to-original-path recovery of Home Assistant and media-stack databases and safely validate application startup/configuration.
- [ ] Add lightweight backup failure/staleness notifications after selecting a channel; optionally expose last successful backup in Homepage.
- [x] Test restore and run `restic check`; both completed successfully.

## P1 — Jellyfin private remote access

- [ ] Resolve the documented server-connection failure over Tailscale; validate remote login and playback.
- [ ] Add the deferred Homepage Jellyfin widget once admin/API-key setup is available; this does not reopen Homepage V1.

## P2 — Network / remote access

- [x] Implement and harden Tailscale as the private overlay network for admin access.
- [ ] Buy/configure own domain.
- [ ] Decide public-app tunnel/reverse-proxy architecture.
- [ ] Keep admin UIs private.

## P2 — Smart home

- [ ] Add Matter server/integration without breaking existing Google Home fabric.
- [ ] Integrate Nest Doorbell via Google SDM.
- [ ] Add Yamaha R-N1000A when physically ready.
- [ ] Optional FRITZ!Box monitoring.

## P2 — Storage / cloud

- [ ] Measure real NVMe consumption over time.
- [ ] Add HDD only when usage justifies it.
- [ ] Evaluate photo cloud when RAM/resource budget is clearer.
- [ ] Evaluate file cloud.

## P3 — Household e-ink dashboard

- [ ] Prototype portrait UI in browser first.
- [ ] Define Home Assistant data/actions contract.
- [ ] Re-evaluate available 10–13.3-inch touch e-paper hardware at purchase time.
- [ ] Implement shopping list, calendar, messages, scenes, weather.
