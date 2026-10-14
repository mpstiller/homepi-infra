# HomePi Infrastructure

Documentation and configuration repository for the `homepi` Raspberry Pi 5 homelab.

This repository is intended to be the **portable source of context** for humans and LLMs working on the system. It documents architecture, decisions, current state, known settings, troubleshooting history, and the roadmap. Verified Compose definitions and sanitized Homepage configuration are checked in and take precedence over prose. Live secrets remain on the Pi; changes after the last capture require verification.

## Start here

1. `LLM_CONTEXT.md` — compact but detailed handoff for any new LLM/session.
2. `CURRENT_STATE.md` — what is working right now and where work should resume.
3. `docs/decisions.md` — decisions that should not be casually reversed.
4. `ROADMAP.md` — planned work in priority order.
5. `AGENTS.md` — rules for automated/LLM contributors.

## Core goals

- Home Assistant / smart-home backend
- Jellyfin media server with Direct Play as the preferred playback path
- Music Assistant for local music and streaming providers
- Sonarr/Radarr/Prowlarr/Seerr/qBittorrent media automation
- qBittorrent isolated behind Gluetun + Proton VPN
- Secure remote access later, without exposing admin UIs directly
- Future photo/file cloud, own apps, monitoring/backups, and e-ink household dashboard

## Secret policy

**No secrets belong in Git.** Never commit passwords, API keys, OAuth tokens, WireGuard private keys, cookies, or private credentials. Use local `.env` files and keep only `.env.example` in the repository.

## Current documentation status

P0 reproducibility and Homepage V1 are complete. Backup V1 is operational, with a targeted restore and repository integrity check tested. Installed backup scripts/systemd units are captured; restart/locking hardening and application-level recovery validation remain open. Read `ROADMAP.md` for the ordered next steps and `CURRENT_STATE.md` for confirmed evidence. Historical audit dates do not imply a new live verification.
