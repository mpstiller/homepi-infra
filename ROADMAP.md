# Roadmap

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
