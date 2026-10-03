# HomePi Infrastructure

Private documentation and configuration repository for the `homepi` Raspberry Pi 5 homelab.

This repository is intended to be the **portable source of context** for humans and LLMs working on the system. It documents architecture, decisions, current state, known settings, troubleshooting history, and the roadmap. Actual runtime configuration files from the Pi will be synchronized into this repository later and will then become the technical source of truth.

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

## Status of this initial version

This first version was reconstructed from the setup session and is intentionally explicit about what is **confirmed**, what is **planned**, and what still needs to be **verified against the live Pi**. Runtime `compose.yaml` files should be imported from the Pi before this repository is used for deployment.
