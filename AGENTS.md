# Instructions for LLMs and automation agents

Before making recommendations or changes:

1. Read `LLM_CONTEXT.md`.
2. Read `CURRENT_STATE.md`.
3. Read `docs/decisions.md` for relevant architecture decisions.
4. Treat actual checked-in runtime configuration files as higher authority than prose once they are synchronized from the Pi.

## Operating principles

- Preserve working architecture unless there is a concrete reason to change it.
- Do not re-propose decisions already settled in `docs/decisions.md` without explaining what new evidence changes the trade-off.
- Prefer incremental changes with an explicit validation step.
- Keep admin services LAN/private-network only unless a dedicated secure-access design says otherwise.
- Never expose or commit secrets.
- Do not use `docker stop` before a normal `sudo poweroff`; containers use `restart: unless-stopped` and should be allowed to stop with Docker/systemd.
- Preserve the single `/data` filesystem view for qBittorrent/Sonarr/Radarr so hardlinks remain possible.
- qBittorrent must remain isolated behind Gluetun. Do not give it a fallback direct Internet path.
- The Raspberry Pi 5 has 4 GB RAM. Avoid adding heavy services without checking memory impact.
- Prefer Direct Play in Jellyfin; do not design around heavy server-side video transcoding on this Pi.

## Documentation discipline

After a meaningful change, update at least:

- `CURRENT_STATE.md`
- `CHANGELOG.md`
- the relevant file in `docs/`
- `LLM_CONTEXT.md` if the change materially affects future handoffs

If a setting is unknown, write `VERIFY ON PI` rather than guessing.
