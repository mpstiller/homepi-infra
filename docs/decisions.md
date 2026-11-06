# Architecture Decision Log

## ADR-001 — Use NVMe as the primary system disk

**Decision:** Boot and run the Pi directly from the Samsung 990 EVO Plus 2 TB NVMe.

**Reason:** better durability/performance than the temporary microSD and enough capacity to learn actual usage.

## ADR-002 — Do not buy a large HDD yet

**Decision:** Use the 2 TB NVMe for OS, appdata, downloads, and media for now.

**Reason:** actual storage demand is unknown; avoid unnecessary cost, noise, power, and complexity.

**Revisit when:** sustained real usage approaches a meaningful capacity threshold or retention needs become clear.

## ADR-003 — Preserve a common `/data` mount for media automation

**Decision:** qBittorrent, Sonarr, and Radarr share the same `/data` filesystem view.

**Reason:** enables hardlinks and atomic/efficient imports.

## ADR-004 — qBittorrent only goes through VPN

**Decision:** qBittorrent shares Gluetun's network namespace; the rest of the stack does not use the VPN by default.

**Reason:** strong isolation and kill-switch behavior without unnecessarily routing Home Assistant/Jellyfin/etc. through the VPN.

## ADR-005 — Proton VPN + WireGuard + port forwarding

**Decision:** Proton paid plan, WireGuard, NAT-PMP/port-forwarding configuration, Gluetun integration.

**Reason:** supports inbound peer connectivity while keeping qBittorrent isolated. Kill-switch and IP isolation were validated.

## ADR-006 — 1080p V1 media profile

**Decision:** prioritize good 1080p Bluray/WEB encodes; no 4K, 720p, or 1080p remux in the default V1 profile.

**Reason:** balance quality, 65-inch OLED viewing, Pi Direct Play, and 2 TB storage constraints. 4K can be a separate future profile.

## ADR-007 — German dual-language is the preferred media outcome

**Decision:** prefer German DL, then German, while permitting English/original as fallback through Custom Format scoring.

## ADR-008 — Home Assistant supplements Google Home

**Decision:** keep existing Google Home voice usability and use Home Assistant as the richer backend/automation layer.

## ADR-009 — Defer heavy photo-cloud stack

**Decision:** do not add Immich yet on the 4 GB Pi.

**Reason:** stabilize current workloads and understand resource headroom first.

## ADR-010 — Keep existing web apps on Vercel/Supabase for now

**Decision:** do not move current production `planner` / `quoernchenkueche` apps to the Pi merely for the sake of self-hosting.

**Reason:** current cloud deployment is appropriate; Pi may later host staging/new small apps.

## ADR-011 — Prepare Sony-compatible audio without permanent duplicate storage (pilot pending)

**Decision:** prepare an opt-in workflow replacing TrueHD with AC3 in a derived MKV. Per owner decision, normal automatic operation atomically replaces the verified library file and retains no permanent original archive. Only an explicit single-file pilot may pass `--keep-original` for temporary rollback; the flag is refused in scan mode and absent from the automatic service. Do not change video/release quality selection or delete pre-existing archives.

**New evidence:** retained TrueHD+added-AC3 still stuttered and aborted in Direct Play. A remux removing TrueHD, retaining both AC3 tracks and subtitles, passed owner Sony playback/switching/seeking. Kodi is deferred. This supports the compatibility pilot, not a universal codec diagnosis.

**Storage/quality trade-off:** temporary output space is required until verification/atomic replacement. Existing torrent hardlinks retain original bytes until established cleanup. Without a retained original, the lossless TrueHD audio cannot be reconstructed from lossy AC3. No archive is automatically created in normal operation; the pilot archive remains outside restic scope and its later removal must target the reviewed pilot entry.

**Limits:** local tests do not prove native Pi/API behavior. Validate the actual single-file worker output, temporary pilot archive, metadata and session/race behavior before enabling unattended processing. See audio/README.md.

## ADR-012 — Use Arcane for a limited patch-update rollout

**Decision (2026-10-29):** prefer built-in Arcane updates to a bespoke controller for low operating effort. Only the three Homepage stack containers are eligible, with stable patch ranges, a 72-hour detection delay and weekly Saturday schedule. Review other services and wider version changes manually.

**Trade-off accepted in session:** existing daily Restic backup is the safety net; no fresh pre-update backup gate, scheduled shared host lock, durable batch failure latch, comprehensive functional checks/automatic data rollback or additional Homepage update card was implemented. Do not describe the initial aspirational safeguards as delivered. New containers must be reviewed because the UI configuration is exclusion-based. See update-strategy.md for native evidence, recovery copies and remaining verification.

## ADR-013 — Separate private document archive from editable cloud workspace

**Decision (2026-11-06):** use Paperless-ngx for personal final records and evidence (contracts, official letters, invoices, bank/insurance and housing proofs); keep Google Drive for editable/collaborative files, projects, photographs/media and source documents during controlled migration. Choose based on document purpose, not merely PDF extension. Actual private records stay on HomePi; no real document content or secrets belong in Git.

**Metadata convention:** document type describes form, correspondent describes issuer/author (can be different from operational contact), thematic tags represent overlapping life areas, `Inbox` is a temporary review state removed after verification, `Zu erledigen` is independent actionable status. Use automatic matching only after validating representative examples; do not create fictitious correspondents to force matches.

**Security and recovery:** Paperless only at Docker loopback `127.0.0.1:8010`, privately accessed via Tailscale Serve HTTPS `https://homepi.tail110996.ts.net` and narrow owner-only TCP 443 grant; no Funnel/public exposure. Encrypted daily Restic is the accepted primary backup, synthetic isolated recovery proved 2026-11-04, new verification after actual-data migration still due. Native document exporter optional by owner's choice.

**Source cleanup:** no Google Drive deletes or moves until documents have been validated in Paperless, a subsequent current archive backup has succeeded and the owner explicitly approves source cleanup. Final signed legal documents and historical proof may both matter; don't assume equal filenames mean duplicates.

## ADR-014 — Paperless administrative archive versus Drive reference/workspace (2026-11-06)

Decision: Paperless is the user's lean, automation-first private administrative archive for invoices, contracts, insurance, tax, banking, official correspondence and evidentiary proofs; NOT a catch-all for all PDFs. Google Drive holds project files, editable content, photos, research, vendor offers and price-comparison collections. An accepted quotation can deliberately exist in BOTH systems when Paperless preserves contract evidence and Drive keeps a comparable future price reference.

The Drive folder "00_Temporaere_Paperless_Migrationskopien" is a temporary migration safety area rather than a permanent second archive. Never delete its copies absent actual document-to-Paperless reconciliation, confidence in recoverability, and explicit owner permission. The 2026-11-06 snapshot was successful but current dataset not independently restored.

Execution: User confirmed Löwen Umzüge quote PDFs 1241/1242 imported into Paperless; both source originals moved BACK to existing Drive folder "01_Beauftragte_Firma_Loewen_Umzuege", verified by destination readback. All uncommissioned vendor offers remain in Drive. Root housing categories were renamed without new IDs: "01_Aktive_Projekte" to "01_Projekte_und_Referenzen"; moving subfolder "Umzugsunternehmen" to "Umzugsunternehmen_Angebotsvergleich"; source archive to "00_Temporaere_Paperless_Migrationskopien". No Drive originals deleted.

Paperless has existing Intake->Inbox workflow and one validated cleaning provider exact correspondent rule. Broader classification and IMAP email intake have NOT been implemented. Pilot additional automation cautiously with real samples and review before auto-filing.

