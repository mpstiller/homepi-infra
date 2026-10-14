# Roadmap

**Reconciled:** 2026-10-14, using repository state and checked-in runtime configuration as primary evidence. Chat findings supplement that evidence; no new live audit was performed. P0, Homepage V1, the main update window and operational Backup V1 are complete. Unticked items below remain unverified or planned.

## Recommended execution order

1. **Maintenance follow-ups.** Image/digest/resource inventory is refreshed. Docker memory/swap-limit support is enabled and verified after reboot. Evaluate Gluetun pinning separately while preserving binding, forwarded port and kill switch.
2. **Backup follow-ups.** Verify independent recovery secrets and add lightweight failure/staleness visibility after choosing a channel. Backup V1 is closed; additional app-start/full-host recovery tests are optional/deferred by owner decision.
3. **Normal-use media checks.** Capture Radarr hardlink evidence before cleanup, decide retained authorized indexers and verify Kodi client synchronization. Remote Jellyfin playback can be validated during normal use; login and Homepage widget are complete.
4. **Next household capability.** Matter/smart-home integration or a browser-first e-ink prototype; photo/file cloud requires measured resources. Preserve the decisions to defer Immich, HDD purchase and production-app migration.


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
  - [x] Jellyfin widget version 2 added and rendering owner-verified on 2026-10-14.
  - [x] Capture the exact live Homepage Compose file and sync the live `env_file` + `host.docker.internal:host-gateway` structure into Git.
  - [x] Commit sanitized `services.yaml`, `settings.yaml`, `widgets.yaml`, and `docker.yaml`; never commit the local Homepage `.env`.
  - [x] Run one final Homepage smoke test, including current service links over the active LAN/Tailscale access path; keep the known Jellyfin exception separate.
  - [ ] Optional: visual/global-widget polish only where it adds useful signal.

## P1 — Maintenance hygiene

- [x] Complete the 2026-10-08 low/medium-risk container update window.
- [x] Revalidate qBittorrent VPN binding and Proton forwarded port after update.
- [ ] Evaluate Gluetun separately and move away from an unpinned `:latest` update path if appropriate.
- [x] Refresh exact image digest/version evidence after the update window (owner capture 2026-10-14, 13 containers, no errors).
- [x] Diagnose and enable Docker memory/swap-limit support: guarded boot override applied; controller and Docker flags verified after reboot, with all 13 containers running. Individual service budgets/caps remain a separate measured decision.
- [x] Update Home Assistant to `2026.10.0` and validate normal operation; monitor the separate `fritz.powerline` SSDP discovery error.
- [x] Update Jellyfin to `12.2.0` and validate startup, libraries, Seerr integration, playback, and Kodi/JellyCon.

## P1 — Backups V1 ✅

- [x] Choose restic.
- [x] Initialize encrypted restic repository in Google Drive and complete first backup of `/srv/appdata` and `/opt/homelab/stacks`.
- [x] Automate recurring backups and retention.
  - [x] Add and validate separate monthly restic prune/check maintenance job.
  - [x] Validate production-style staging backup with cache/log excludes (333.155 MiB snapshot).
  - [x] Install and enable systemd service/timer; manual systemd execution validated successfully.
- [x] Capture installed backup/maintenance scripts and all four systemd units in Git; review retention/excludes, restart failure handling and overlap behavior.
- [x] Prepare restart failure detection/cleanup and a shared backup/maintenance lock; eight local simulated tests passed.
- [x] Install revised scripts on the Pi (owner-reported successful installer output, 2026-10-14).
- [x] Validate native flock contention/release and restored timer scheduling on the Pi (owner output, 2026-10-14).
- [x] Validate real systemd backup execution with the revised script: snapshot `b37715a7`, successful retention and post-run container check (2026-10-14).
- [x] Validate real systemd maintenance execution with the revised script: prune/check completed, no errors, exit 0 (2026-10-14).
- [x] Document observed restore paths and validate restored SQLite/XML/Home Assistant JSON (41 checks, 0 failures, 2026-10-14).
- [x] Validate isolated Sonarr startup/API and retained series IDs (four series, 2026-10-14).
- [x] Test restore and run `restic check`; both completed successfully.

Backup V1 closes with full temporary restore, copied-state checks and one representative restored application start, as explicitly agreed with the owner. This does not claim every service/full-host recovery has been tested.

## Backup follow-ups (separate from V1 closure)

- [ ] Verify independent recovery access to the restic password, rclone OAuth configuration and application secrets.
- [ ] Add lightweight backup failure/staleness notifications; optionally show last successful backup in Homepage.
- [ ] Optional/deferred: additional application-start tests, Kodi Sync Queue LiteDB integrity, YAML/PEM semantics and full-host disaster recovery.
- [ ] Choose when to remove the retained root-only restore test directory/rollback copies; no cleanup has been performed.

## P1 — Jellyfin private remote access

- [x] Resolve the documented server-connection failure over Tailscale; both API routes HTTP 200 and browser login verified (2026-10-14).
- [ ] Validate remote playback during normal use; no remote playback result is claimed.
- [x] Add Homepage Jellyfin widget with local-only API key and verify rendering (2026-10-14).

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
