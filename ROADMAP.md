# Roadmap

## P0 — Make the current system reproducible

- [ ] Sync actual Compose files from `/opt/homelab/stacks` into this repo.
  - [x] Arcane
  - [x] Homepage
  - [x] Home Assistant
  - [x] Jellyfin
  - [x] Media stack
  - [ ] Music Assistant — resolve live deployment source first
- [ ] Add `.env.example` files with names only, never secret values.
  - [x] Arcane
  - [x] Homepage
  - [x] Media stack
  - [ ] Verify whether Music Assistant has an external env/config requirement
- [ ] Capture current container/image versions.
  - [x] Docker Engine / Compose / image tags captured
  - [ ] Exact image digests + application versions
- [ ] Reconcile reconstructed docs against live Pi.
  - [x] Host/storage/Docker/qBittorrent/Compose baseline reconciled
  - [ ] *arr/Prowlarr/Seerr/HA live settings audit
  - [ ] Music Assistant deployment source
- [x] Add a restore/runbook.

## P1 — Finish media stack V1

- [ ] Run Radarr end-to-end movie test.
- [ ] Verify Radarr hardlinks in the same way Sonarr was verified.
- [ ] Define seeding policy (ratio/time) and automatic cleanup behavior.
- [ ] Confirm Jellyfin scans and Direct Play for imported material.
- [ ] Decide which authorized production indexers are retained.
- [ ] Add media-stack services to Homepage if desired.

## P1 — Backups

- [ ] Choose restic or Borg.
- [ ] Back up `/srv/appdata`, `/opt/homelab/stacks`, and critical configuration to an independent target.
- [ ] Document recovery of Home Assistant and media-stack databases.
- [ ] Test restore, not just backup creation.

## P2 — Network / remote access

- [ ] Choose private overlay network for admin access.
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
