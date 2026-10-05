# Runtime stacks

This directory contains the verified Compose definitions reconstructed directly from the running HomePi on 2026-10-05.

## Verified stacks

- `arcane/`
- `homepage/`
- `homeassistant/`
- `music-assistant/`
- `jellyfin/`
- `media/`

Arcane, Homepage, Home Assistant, Jellyfin and Media were exported from `/opt/homelab/stacks`.

Music Assistant was historically deployed from `/srv/appdata/compose.yaml` (Compose project `appdata`). Its live definition has been normalized into `stacks/music-assistant/compose.yaml` so the repository has one coherent stack layout.

## Secrets

Real `.env` files stay on the Pi. Only `.env.example` files belong in Git. Music Assistant's live Compose file has no external secret/environment file requirement.

If a future live system and this repository disagree, inspect the live system deliberately and reconcile the difference through a documented commit.
