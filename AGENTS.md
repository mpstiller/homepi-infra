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


## Avoid stale handoff traps (2026-11-06)

- `CURRENT_STATE.md`, `LLM_CONTEXT.md`, `ROADMAP.md` and Paperless pilot notes contain chronological history. Always read the newest **CURRENT** block first and treat superseded older TODOs as historical; never infer the archive is still unused, that Tailscale access is pending, or that taxonomy was not created.
- Document changes confirmed by the owner separately from live Pi command evidence and independent API/restore verification. GitHub commits do not mean runtime changes are installed or tested.
- Existing private repository PR #21 is draft until GitHub reports otherwise. Keep the selected personal GitHub identity separate from work identities. Never commit actual document OCR, legal names/addresses, IBAN, passwords, keys, certificates or sample private bank PDFs.
- For the current Google Drive → Paperless migration, preserve source files; require an observed successful post-import backup and explicit approval before any cleanup.

## Paperless / Drive continuation (2026-11-09)

When the user starts a new document migration session, **read `docs/paperless-drive-migration-handoff.md` first** before proposing work. Paperless V1 is complete for everyday use (including owner-confirmed Paperless iPhone app remote capture, and Gmail IMAP account with label `Paperless` and Move-to-`Paperless-Verarbeitet` rule). Do NOT restart deployment discovery or claim the recently changed Gmail rule is separately proven with already-read mail. `CURRENT_STATE.md` and `LLM_CONTEXT.md` top entries supersede chronological stale notes further down. Use ADR-014: Paperless only for administrative/evidence archive; Drive for projects, reference price comparisons, editable working files. Create document-by-document Drive-link plus Paperless metadata review tables and track owner-verified imports. Keep current source originals until reconciliation and later successful backup; no Google Drive deletions without explicit permission. Never commit document text, personal bank/account details, app passwords or Gmail secrets.

