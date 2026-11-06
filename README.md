# HomePi Infrastructure

## Current deployment at a glance — 2026-11-06

- Paperless-ngx is **live** on the private Tailscale HTTPS endpoint `https://homepi.tail110996.ts.net` on authorized clients, at home and away; the host Docker port remains loopback-only `127.0.0.1:8010`, no Funnel or public router forwarding.
- Paperless is in actual private use with an owner-verified small housing/household archive and 12-tag/6-type metadata workflow. Google Drive remains the editable workspace and source files are retained for now.
- Verified synthetic Paperless backup/isolated restore on 2026-11-04; **fresh verification after real-document migration still outstanding**. Main canonical status is `CURRENT_STATE.md`, operational runbook `docs/paperless-pilot.md`, historical progression `CHANGELOG.md`.
- Infrastructure Git PR #21 is a **draft feature branch** unless GitHub explicitly reports otherwise; do not infer that `main` contains all Paperless work. No secrets or real personal document contents in repository.

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

P0 reproducibility, Homepage V1 and Backup V1 are complete within their agreed scope. Installed restart/locking hardening, real backup/maintenance, full temporary restore and 41 copied-state checks passed; Sonarr is the tested representative restored application. Other app-start/full-host recovery tests are optional/deferred, and independent secret-recovery verification remains a separate follow-up. Read `ROADMAP.md` for the ordered next steps and `CURRENT_STATE.md` for confirmed evidence. Historical audit dates do not imply a new live verification.
