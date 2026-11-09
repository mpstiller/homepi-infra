# HomePi Infrastructure

## Paperless V1 operational — 2026-11-09

- **Paperless daily-use V1 complete per owner:** private Paperless-ngx 3.4.1 last known, PostgreSQL 18, Valkey 9; Tailscale-only HTTPS `https://homepi.tail110996.ts.net` from Mac and remotely from iPhone. Dedicated Paperless iPhone app scanning/upload confirmed working on Nov 09. Docker still localhost-only `127.0.0.1:8010`, no Funnel.
- **Gmail intake enabled:** Gmail `Paperless` label + connected IMAP account and rule. Changed to move processed messages to `Paperless-Verarbeitet` (already-read mail behavior); final post-change test pending, not a blocker for baseline. Inbox classification workflow + exact-match supplier correspondent tested; broader automatic tagging is not guaranteed.
- **Role split:** Paperless = administrative archive; Google Drive = active project/work/reference store, including vendor comparisons. See ADR-014.
- **Backup:** 2026-11-04 synthetic isolated Paperless restore passed; 2026-11-06 encrypted Restic snapshot `c15d8d59` saved after then-current real imports. Latest Nov 09 real imports were not proven included; verify subsequent backup before any original deletions. Temporary Drive source safety copies intact.
- **Next session:** collaborate on selective migration of relevant Google Drive documents. **Start with `docs/paperless-drive-migration-handoff.md`**, then `CURRENT_STATE.md`, `ROADMAP.md` and `docs/paperless-pilot.md`. Do not repeat installation. Infra PR #21 is historically a draft on feature branch; do not assume merged into main.

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
