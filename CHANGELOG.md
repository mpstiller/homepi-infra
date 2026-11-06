# Changelog

## 2026-11-06 — Post-import backup checkpoint (afternoon)

- Owner initiated a controlled extra encrypted Restic backup after real document imports; `homepi-backup.service` and notify hooks exited 0, consistent staging and Paperless web/db/broker restarts reported, encrypted upload completed. New snapshot `c15d8d59` saved 15:09:13 CET (509.830 MiB logical); backup finished 15:10:08 CET. Normal retention removed the earlier same-day `cea5a742`.
- Read-only staging size check after the run: PostgreSQL 71M, document media 21M, application data 1.9M. This confirms nonempty staged paths, **not** a verified current database/document manifest or independent restore. The earlier two-synthetic-document isolated restore is the historical restoration evidence.
- Owner indicated completion of the proposed deposit document import batch, though no item-by-item Paperless API reconciliation has taken place. Plan controlled Google Drive reconciliation first; **no Drive source deletion or move approved/performed**.



## 2026-11-06 — Paperless document-archive rollout and repository audit

- Confirmed owner-guided migration from Google Drive into Paperless: four housing proof documents, two heating invoices, electricity welcome letter, 12 cleaning invoices and final signed tenancy agreement V2. User states imports/checks completed. No independent Paperless API inventory or current production backup verification claimed.
- Verified practical taxonomy workflow: 12 tags (including ephemeral `Inbox` and action-state `Zu erledigen`), six document types, Inbox-on-consumption workflow. Owner configured exact correspondent match for real cleaner invoice; automatic recognition succeeded on another invoice. Inbox is removed after verification, thematic tags remain.
- Compared two tenancy contract PDFs and identified substantive negotiated revisions to clauses on minor repairs, decorating and landlord key retention. Owner confirmed V2 is executed and imported. Legal landlady vs acting son treated as distinct document correspondents (signed contract vs handover record).
- Investigated three PSD Bank deposit applications and earlier Hausbank München establishment/closure. Owner identified the larger scanned PSD PDF as signed final version and says account is active, while account confirmation exists as email only. **Import of those deposit artifacts remains pending**, so earlier records must not be marked migrated.
- Existing Tailscale Serve private HTTPS remains `https://homepi.tail110996.ts.net`; works at home over Tailscale and remotely on authorized clients. No direct LAN port 8010 or Funnel exposure.
- Documentation audit corrected superseded handoff, Roadmap, operational remote access, pilot, runbook, README, idea backlog and current-state references. No Pi configuration, services, data, Google Drive originals or secrets modified; all updates made on Paperless feature branch/draft PR #21.
- Follow-up required: fresh successful Restic backup **after** actual documents and controlled verification before considering any source deletion. Native exporter remains deferred. Historical dated entries below preserve what was known *at the time*; open items from those dates are not necessarily current.

## 2026-11-04

- Owner verified private Tailscale Serve HTTPS Paperless access on Mac and iPhone (cellular), replacing routine manual SSH tunnel. Docker remains localhost-bound; Funnel off. Access milestone complete; move to archive taxonomy/intake design.

- HTTPS Compose webserver recovered healthy; Mac connection to `homepi.tail110996.ts.net:443` timed out after 8 seconds (HTTP 000). Suspect missing port in restrictive Tailnet policy. No public access changes; live policy inspection and precise TCP 443 grant still pending.

- Owner installed private Paperless HTTPS Compose update after exact diff review with dated rollback under shared Restic lock; only webserver recreated, initially health:starting; DB/broker healthy and Docker port remains localhost-only 8010. HTTPS client login and owner-only TCP 443 Tailscale policy change pending.

- Owner configured private Tailscale Serve HTTPS `https://homepi.tail110996.ts.net (tailnet only)` → loopback:8010; both Serve/Funnel status show private mapping, no Funnel public exposure. PR Compose prepared external Paperless URL and forwarded HTTPS header, not yet deployed; owner-only TCP 443 Tailnet grant and HTTPS login tests pending.

- Owner accepted validated Restic→isolated PostgreSQL/media restore as sufficient for initial private document use; deliberately deferred native Paperless `document_exporter` and its smoke test to optional later portability/migration work. No exporter run claimed.

- **Paperless synthetic backup/restore acceptance PASSED:** Owner started restored PG18 on disposable offline copy, recovered 2 indexed document records; SHA-256 verified 2 originals and 1 archive PDF against the recovered database, all matched. No live data overwritten. Private restore, DB test clone and backup rollback remain retained. Native `document_exporter` smoke test still pending before first personal documents.

- Restored PostgreSQL 18 started independently with `--network none` on disposable `/srv/backups/paperless-db-test.HSXnpPsP`; queried restored `documents_document` returned 2 records and content matches `Wasserkocher=1`, `Sonnenuhr=1`. Test container stopped and removed. Original/archive media SHA-256 verification pending.

- Restore structure preflight: private 700 root directory, PG18 data in `18/docker` with PG_VERSION/pg_control, six restored media files and ~69 MB restored PostgreSQL cluster. Offline SQL startup using disposable clone still pending.

- Restic `ef45cae4` successfully restored to private `/srv/backups/restore-paperless.OBa8o5B2`, 5442 files/directories (486.679 MiB) in 1:19. Post-backup all three Paperless services healthy. Restored PG cluster startup and document integrity/relationship verification remain pending.

- First Paperless-inclusive backup **passed** (11:20:40–11:22:40 CET). Restic snapshot `ef45cae4` saved (3930 files / 486.679 MiB logical), retention succeeded, all three Paperless container restart messages observed. Post-run db/broker healthy; webserver still health:starting at immediate check. Isolated restore and webserver final health pending. Snapshot `f608e5f3` removed by retention.

- Owner installed Paperless additions to live backup candidate stop-list using shared flock and exact byte-match guard; retained rollback `/root/homepi-backup-before-paperless.iutMZWUb`. Next: controlled systemd backup, health and isolated restore verification. No successful new backup or restore confirmed yet.

- Owner verified Paperless backup candidate against live script: `bash -n` passed and `diff -u` showed only three new CANDIDATES lines. Systemd ExecStart points to live script; 04:30–04:31 CET scheduled run exited 0 before Paperless integration. Candidate not yet installed; guarded install/restore pending.

- Owner supplied installed backup candidate list and SHA-256 0ce674a1…7d85; independently verified it matches `main:backup/bin/homepi-backup` byte-for-byte. Paperless backup addition is still PR-only. Prepared a frontend-first stop list; live restart/restore remains to be tested.

## 2026-11-03

- Owner confirmed the two synthetic Paperless imports successfully searchable: `Wasserkocher` (born-digital PDF) and `Sonnenuhr` (raster-only scan), proving OCR and indexing. Backup candidate changes remain repository-only; real Restic snapshot and isolated restore are pending. No personal documents ingested.

- Owner `vmstat 1 6` shows only tiny intermittent swap-in (16/80 KiB/s), no swap-out in five current samples, 95–99% CPU idle, 0% I/O wait. No sustained thrashing observed. Synthetic OCR search remains unconfirmed.

- Owner supplied Paperless post-test resource snapshot: webserver 606.5 MiB, db 49.44 MiB, broker 10.16 MiB; host 1.3 GiB available RAM, 1.2 GiB swap occupied. Synthetic PDF OCR/search success is not yet confirmed; no active swap-rate sample, backup or restore verified.

- Owner verified all three Paperless pilot containers healthy and runtime Arcane opt-out labels false; localhost-only port unchanged. Live usage: web 637.5 MiB, PostgreSQL 45.92 MiB, Valkey 7.922 MiB; Pi 1.1 GiB available RAM, 992 MiB swap used. No real documents, OCR proof or installed backup/restore yet.

- Owner ran validated Paperless Compose on Pi: images pulled, broker/db healthy, webserver just started (`health: starting`); isolated network and localhost-only port 8010 confirmed. Runtime health/load/Arcane labels are next. No real documents or backup/restore testing yet.

- Add explicit Arcane updater=false labels to all three proposed Paperless services before launch, preventing unintended unattended updates; runtime verification is still pending.

- Prepare a reversible Paperless-ngx 3.4.1 pilot in a draft PR: localhost-only, PostgreSQL 18 + Valkey 9, rootless Paperless, one OCR worker/thread, all persistent data in /srv/appdata and proposed backup CANDIDATES. No Pi deployment, backups/restore or real-document imports have occurred. Owner supplied resource snapshot (1.7 GiB available RAM, 745 MiB swap used, 1.4 TB free NVMe); UID/GID/port and Arcane exclusion are pending.

- Record the owner's exploratory self-hosting ideas with source pointers, personal use cases and evaluation constraints; link existing dashboard/cloud plans instead of duplicating them.
- Select Paperless-ngx for a new session, with requirements discovery and thorough current research before tailored configuration or deployment. Add a dedicated session brief; no Paperless stack, import or detailed setup research performed here.
- Record explicit owner confirmation that Matter is excluded from Arcane Auto Update, the successful silent 07:00:04 scheduled audio invocation, and the decision to defer Seerr/Tailscale automatic login without changes. Arcane's 7 November run remains pending.

## 2026-11-02

- After the successful Matter-integrated backup/restart, owner confirmed the requested Home Assistant switching and Google Home state check still works. No Matter restore test is claimed; explicit Arcane exclusion confirmation remains pending.

- Matter backup follow-up installed with verified baseline/candidate checksums and rollback /root/homepi-matter-backup-rollback.6fxgbvcj. Real run completed 19:47:14 CET after staging/restarting matter-server, saving snapshot e43eddfa (417.233 MiB) and retention. Supersedes preparation-only status below; exact Matter file inspection, restore and post-backup functional test are not claimed.

- Record owner-installed Matter.js Server 1.5.5, localhost WebSocket connection and successful first-device multi-controller switching. Owner confirmed all Matter devices connected; exact inventory not supplied. Capture Compose/runbook without fabric secrets.
- Prepare one-line backup CANDIDATES addition for matter-server; bash syntax validation passed. Pi installation, consistent snapshot/restart, resource measurement and explicit Arcane exclusion confirmation remain pending.
- Owner confirmed the daily audio Homepage display is correct; first daily scheduled execution remains pending.

- Owner verified and ran guarded installer from cbbeab4; installation completed, collector refreshed and daily audio timer restarted. Next trigger confirmed: 3 November 07:00 CET. Rollback retained at /root/homepi-audio-daily-rollback.VFwqadR8. No conversion was started; first daily execution and Homepage visual check remain pending.

- Owner dry scan reported no candidates and requested daily audio processing after backups. Prepare daily 07:00 Europe/Berlin timer without missed-run catch-up, plus sequential batch and blocking shared-lock options for the service.
- Preserve single-file/manual defaults, playback/source/video/hardlink guards and error stop. No backup, VPN or media quality settings changed.
- Adapt Homepage audio overdue threshold to 30 hours and allowlisted waiting/batch messages; JSON freshness unchanged. 51 local tests pass; calendar and adjusted-path systemd validation pass. No new Pi run or installation claimed.

## 2026-11-01

- Corrected Homepage updater policies from x-arcane extensions to explicit container labels so both terminal Docker Compose deployments and Arcane container checks receive the same rules. Image tags, ranges, regexes and runtime security settings are unchanged.
- Owner validated candidate Compose, recreated the three services with existing images under the host lock, and verified all runtime labels. Fresh watcher/container UI showed status/proxy updates and Homepage current. Auto Update re-enabled; next slot expected 7 November 10:00 CET. Actual unattended application remains unverified.
- First scheduled run (31 October) completed but showed existing tags up to date; do not describe it as proof of successful tag-based updates or merely a delay deferral.
- Gmail SMTP provider test delivered successfully. Source review confirms successful-update notifications do not supply a general failed-update email alarm; no failure monitor or forced production failure test added.

## 2026-10-29

- Owner upgraded Arcane 2.15.1 -> 2.17.1, verified running/healthy, and corrected project discovery to /opt/homelab/stacks.
- Added explicit Homepage-stack image tags with Arcane patch-range policies (Homepage 2.4.x, proxy 3.4.x, Python 3.13.x on Alpine 3.24). Native Compose validation passed; proxy ls102 worked in Homepage; Homepage/status healthchecks passed.
- Owner configured 72-hour delay and all-container exclusions except the three Homepage services. Reported first scheduled execution: 31 October 10:00 CET. No unattended result is claimed.
- Documented retained recovery copies and limits: existing daily backups remain independent; no new backup gate, scheduled host-lock integration, global failure latch or Homepage update card. Preserve backup/audio/VPN architecture.

## 2026-10-26

- PR #12 confirmed merged. Owner confirmed targeted deletion of the retained S01E01 pilot archive and the three separate audio-test MKVs; the converted normal-library episode remains. No full-backlog completion or deletion of other archives is claimed.

- Owner verified corrected Jellyfin authorization, completed one-file AOT S01E01 apply with temporary original retention and confirmed flawless normal-library Sony playback. Backlog dry-run listed 36 further AOT episodes.
- Service/timer installed, verified and enabled by owner. Automatic S01E02 finished 14:09:45 CET and S01E03 finished 14:17:27 CET, both with archive disabled; a third invocation started 14:22:48. Timer re-arming is observed. Full backlog completion, actual rollback/busy-session behavior and pilot/test-copy cleanup are not claimed.

- Owner installed worker and confirmed two-track single-file dry-run. Initial apply was blocked by HTTP 401; no successful replacement was recorded.
- Fixed the helper's legacy Jellyfin authentication header to Authorization: MediaBrowser Token for Jellyfin 12. Added secret-safe HTTP status diagnostics; 17 local tests pass, including GET/POST auth and redacted errors. Native corrected-header/API/apply validation remains pending; do not rotate further keys or enable legacy authorization.

## 2026-10-24

- Owner chose no permanent original archive for audio conversion. Automatic apply now replaces only after verification, while --keep-original is available solely for an explicit one-file pilot. No old archives/test copies are deleted. Fifteen local tests pass, including no-archive replacement, preserved torrent bytes and failed-publication preservation. Pi installation remains pending.

- Recorded owner Sony tests: retaining TrueHD plus AC3 still stuttered/aborted; removing TrueHD while keeping both AC3 tracks/subtitles passed playback, switching and seeking. Kodi work is deferred.
- Prepared opt-in MKV TrueHD-to-AC3 worker with optional single-file pilot archive (automatic mode retains none), atomic replacement preserving torrent hardlinks, encoded-video hash checks, playback/API guards, shared backup lock, resource-limited local-image Docker jobs and gated timer. No worker installation or automatic Pi conversion is claimed.
- Fifteen local tests, a native synthetic FFmpeg conversion (subtitle/chapter/font retained, video hash identical) and adjusted-path systemd unit verification pass. Single-file native Pi/Sony worker pilot remains next.

## 2026-10-20

- Closed monitoring follow-up: owner confirmed both checks returned to green and timer scheduling is correct; captured exact supplied notification helpers/drop-ins, documented installation/rollback and kept URL credentials excluded. Both Python helpers parsed and 12 mocked routing/failure checks passed. No deliberately missed-run or full-host recovery test is claimed. This supersedes earlier pending monitoring notes in today's log.

- Follow-up recovery: owner published OAuth app to In production, reconnected the existing gdrive remote using the explicit production config, reopened repository 475950f8 and completed real maintenance at 17:05:40 CEST (Result=success, exit 0; prune and standard check of eight snapshots, no errors).
- Owner replaced the password-manager rclone recovery attachment with the renewed configuration. Monthly Healthchecks green state, temporary-copy deletion and installed monitoring source capture remain unconfirmed/pending. This supersedes the earlier incident-in-progress notes below.

- Recorded owner-confirmed independent restic/rclone secret storage (no independent-host restore claim), daily backup email alarm/recovery tests and successful snapshot c0280e8b.
- Recorded monthly monitoring test and actual maintenance failure due to Google OAuth invalid_grant; Testing status confirmed, reauthorization and maintenance recovery pending.
- Prepared static HomePi Backup homepage/privacy pages for GitHub Pages and documented the deployment/Branding/reconnect sequence. Nothing is claimed published or repaired yet; runtime monitoring source capture remains pending.

## 2026-10-15

- Owner pinned Gluetun to the previously validated digest `qmcgaw/gluetun@sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793` in the actual media Compose file; mirrored the one-line change locally. No image pull/update was performed; Gluetun and qBittorrent were recreated together.
- Owner confirmed matching Gluetun/qBittorrent namespace IDs, `tun0` / `0.0.0.0`, matching forwarded/listen ports and different host/VPN public IPv4 addresses. A fixed-IP HTTP target was reachable before the tunnel-down test and failed with `tun0` DOWN before/after the request; this is a targeted IPv4 check, not exhaustive leak testing.
- Recorded the recovery interruption: manually raising the tunnel left qBittorrent on `lo` / port `0`; a Gluetun-only Docker restart left the qBittorrent API unreachable from Gluetun. Recreating both restored API `v5.2.4`, binding, matching dynamic port `33266` and outbound connectivity. Namespace mismatch is a possible explanation, not a proven diagnosis. Added maintenance/recovery guidance and scope limits.
- Confirmed PR #7 is merged and moved the current roadmap/handoff to independent recovery secrets and backup visibility. The owner committed and published the change as [PR #8](https://github.com/mpstiller/homepi-infra/pull/8); merge status must be checked before treating it as part of main. Historical inventory JSON is unchanged.

## 2026-10-14

- Recorded owner-requested session handoff: PR #7 open at handoff, completed/untested boundaries, no scheduled Pi actions, and concrete next Gluetun pinning evaluation followed by backup visibility/recovery-secret follow-ups.

- Resolved missing Docker memory/swap-limit support: diagnosed the disabled memory controller, applied a guarded `cgroup_enable=memory` boot override with rollback, then owner verified the memory controller and both Docker support flags after reboot. All 13 containers running; four configured healthchecks healthy. Five local boot-line tests passed. Per-service caps were not assigned; enforcement under memory pressure remains untested.

- Recorded owner read-only image inventory at 15:42 CEST: 13 running containers, all local references match running IDs, no capture errors. Archived Oct 5 baseline and added selected-field JSON snapshot; distinguish six directly queried app versions from image labels.
- Confirmed 11 digest changes vs Oct 5 while Gluetun/FlareSolverr remain unchanged. Recorded missing Docker memory/swap-limit support as a separate diagnostic follow-up; no pull/update/restart/configuration change performed.


- Added and owner-verified Jellyfin Homepage widget version 2 (movie/series/episode counts and Now Playing, user/media controls disabled). Key remains local in verified stack env_file; only blank template variable is checked in. Corrected prior env-file path prose and recreated Homepage alone without pulling an image.
- Resolved Jellyfin-over-Tailscale server-connection failure: owner confirmed EnableRemoteAccess=false, applied a one-field guarded change to true with private rollback and restart, then verified both hostname/IP API HTTP 200 and browser login. Router/Tailscale/IP-filter policy unchanged; remote playback remains untested. Three local XML-edit tests passed.
- Updated roadmap/handoff/Homepage docs to remove the remote-login blocker; Jellyfin widget remains optional/unconfigured.
- Captured installed backup/maintenance scripts and four units, then installed shared flock and explicit restart-failure/EXIT cleanup handling. Eight local simulated tests passed; owner verified native lock, timers and successful real backup/maintenance runs.
- Saved snapshot `b37715a7` (334.493 MiB); owner restored all 3236 files/directories to a private test directory and confirmed direct `srv/appdata` / `opt/homelab/stacks` restore roots. Corrected the earlier inferred staging-prefix mapping.
- Owner passed 41 copied-state checks (13 SQLite, three XML, 23 JSON, YAML/LiteDB presence). Corrected Kodi Sync Queue's mistaken SQLite classification; LiteDB integrity remains untested. Seven local checker tests passed.
- Owner validated isolated Sonarr restored startup on 4.0.20.3014 with four matching series IDs; test container/copy removed. Four local simulated lifecycle tests passed.
- Closed Backup V1 with the owner's agreed representative-start-test scope; additional app starts/full-host recovery remain optional/deferred. Independent recovery secrets, backup visibility and retained restore-data cleanup remain separate follow-ups.
- Updated roadmap/handoff to resume Jellyfin-over-Tailscale next. No claim is made that the prepared Jellyfin test was executed; it was omitted from the final V1 scope.
- Removed obsolete manual restic snapshot `bd21d171` after automated-backup validation, then pruned unreferenced data.

## 2026-10-13

- Added and validated monthly restic maintenance via systemd: `prune` followed by `check`, scheduled for the 1st of each month at 05:30.
- Added and validated the systemd-managed HomePi backup flow; configured a dedicated restic cache (`XDG_CACHE_HOME=/var/cache/homepi-backup`) so automated runs complete cleanly.
- Validated the production-style restic staging backup with cache/log exclusions; the automatic snapshot size dropped to `333.155 MiB` and services were restarted before cloud upload.
- Verified the first restic backup by restoring data to a temporary path and running `restic check`; both completed successfully.
- Initialized an encrypted restic repository in Google Drive via rclone and completed the first manual backup of `/srv/appdata` and `/opt/homelab/stacks`; restore testing remains pending.

## 2026-10-08

- Completed post-update Jellyfin validation on `12.2.0` (UI, libraries, Seerr integration, playback, Kodi/JellyCon) and intentionally deferred Gluetun while the current VPN/kill-switch/port-forwarding path remains healthy.
- Updated Jellyfin from `12.0.0` to `12.2.0`; database migrations completed successfully, Kodi Sync Queue loaded, library watchers started, and Core startup completed cleanly.
- Updated Home Assistant from `2026.9.2` to `2026.10.0`; Core startup succeeded. A separate FRITZ! SSDP discovery flow logged a hostname parsing error for `fritz.powerline`, to be monitored independently.
- Closed the main container maintenance window: documented completed updates, intentional Gluetun/Home Assistant/Jellyfin deferrals, successful post-maintenance reboot, and the need to refresh exact image digests.
- Updated qBittorrent to `5.2.4`; WebUI started cleanly and post-update checks confirmed `tun0`, All IPv4 (`0.0.0.0`), and the Proton forwarded listen port remained correct.
- Updated Music Assistant to `2.10.5`; startup completed cleanly, web/stream servers came up, and SONOS/Chromecast/DLNA providers loaded successfully.
- Updated Arcane to `2.15.1`; database migrations completed successfully and the post-start image scan checked 14 images with 0 errors, leaving 5 images with updates available.

## 2026-10-07

- Completed Homepage V1: final smoke test passed, current widgets and service links validated, reproducible live configuration captured in Git; Jellyfin widget remains intentionally deferred.
- Captured the exact live Homepage Compose and sanitized dashboard YAMLs into Git, added safe widget variable names to `.env.example`, reconciled the live System group (Arcane + Gluetun), and closed the Homepage reproducibility gap.
- Reconciled Homepage V1 remaining work: documented the live Compose drift (`env_file` + `host.docker.internal:host-gateway`), pending sanitized runtime-config capture, Jellyfin deferral, Arcane decision, and final smoke-test criteria; expanded the roadmap accordingly.
- Updated Seerr to `3.5.0`; startup completed without errors, Jellyfin Movies/Series sync completed successfully, and Automatic Search is enabled for both Sonarr and Radarr.
- Updated Radarr from `6.3.0.10514` to `6.4.4.10685`; startup, SQLite checks, and service binding completed without errors.
- Updated Sonarr from `4.0.19.2979` to `4.0.20.3014`; startup, SQLite checks, and service binding completed without errors.
- Updated Prowlarr from `2.5.2.5491` to `2.6.5.5623`; startup, SQLite checks, and service binding completed without errors.
- Recorded the implemented Homepage service-group layout and confirmed the Sonarr native widget is working.
- Confirmed the Radarr native Homepage widget is also working.
- Confirmed the Prowlarr native Homepage widget is working.
- Confirmed the qBittorrent native Homepage widget is working through the Gluetun-published host port.
- Confirmed the Seerr native Homepage widget is working.
- Deferred the Jellyfin Homepage widget because the documented Jellyfin-over-Tailscale issue currently blocks remote admin/API-key setup.
- Confirmed the Home Assistant native Homepage widget is working.
- Documented that Homepage API keys remain in the local `.env` and are not committed.
- Added `docs/homepage.md` as the dashboard-specific handoff and documented that the live Homepage YAML files are not yet synchronized into Git.
- Removed stale handoff instructions that still treated the Seerr profile mismatch, Radarr validation, and private overlay selection as unfinished.
- Aligned the roadmap and LLM context with the implemented/hardened Tailscale setup and the current Homepage widget workstream.
- Kept the Jellyfin-over-Tailscale connection problem documented as a separate unresolved issue.

## 2026-10-06

- Isolated a Sony Jellyfin Android TV playback issue with HEVC Main 10 + TrueHD media.
- Confirmed the same file plays cleanly on macOS and on the Sony via Kodi + JellyCon.
- Decided to keep Sonarr/Radarr quality-first and use Kodi/JellyCon as a compatibility fallback instead of hard-excluding TrueHD.

- Confirmed Jellyfin automatically detected the Radarr-imported movie.
- Confirmed Direct Play on the Sony TV with no transcoding, validating the movie playback path end to end.

- Validated a real Radarr end-to-end movie request through Seerr/Prowlarr/qBittorrent.
- Confirmed qBittorrent used the `radarr` category and movie download path.
- Confirmed the 30-minute seed -> Stop -> Radarr Remove Completed cleanup chain removes the torrent and torrent-side data while preserving the imported media file.

- Hardened the Tailnet: Device Approval enabled, default allow-all removed, owner-only HomePi access, explicit port allowlist, server key expiry disabled, and Tailscale auto-update enabled.

- Installed and joined Tailscale on HomePi.
- Verified remote access from iPhone over cellular.
- HomePi Tailscale IPv4 is `100.72.110.114`; MagicDNS hostname is `homepi`.
- Updated Homepage host validation for LAN and Tailscale access.
- Kept qBittorrent Internet traffic isolated through Gluetun + Proton VPN.


## 2026-10-05

- Added `HomePi Anime 1080p` in Sonarr with Anime-specific tier scoring, original-audio requirement, raw/dub-only/LQ exclusions, and low-weight Dual Audio preference.
- Added Anime-specific episode naming with absolute numbering.
- Configured Seerr to use `HomePi Anime 1080p` for Anime while keeping `HomePi 1080p` for normal series.

- Updated Seerr so both Sonarr and Radarr requests use `HomePi 1080p` (profile ID 7); resolved the old `HD-1080p` mismatch.

- Audited the running Pi with a sanitized export bundle.
- Verified Debian 13.7, kernel 6.18.39+rpt-rpi-2712, NVMe root, Docker 29.8.0 and Compose v5.5.1.
- Synchronized live Compose files for Arcane, Homepage, Home Assistant, Jellyfin and the media stack.
- Added safe stack-specific `.env.example` files.
- Verified qBittorrent v5.2.3 live paths, `tun0` + All IPv4 binding, and current global 30-minute seeding-time limit.
- Added live-system documentation and a restore runbook.
- Identified that Music Assistant is running but its expected Compose file was not present in the first stack export; scheduled runtime-label inspection.
- Added a second sanitized live-configuration audit script for application settings, exact image metadata and deployment-source reconciliation.
- Imported the second live audit with exact running image digests and Sonarr/Radarr/Prowlarr settings.
- Detected a live Seerr profile mismatch: both Sonarr and Radarr requests still use `HD-1080p` instead of `HomePi 1080p`.
- Confirmed qBittorrent's 30-minute seed limit uses the Stop action and both *arr clients have Remove Completed enabled.
- Identified Music Assistant's deployment source as `/srv/appdata/compose.yaml` via Docker Compose labels.
- Imported the actual Music Assistant Compose definition and normalized it under `stacks/music-assistant/`.
- Verified Home Assistant `2026.9.2` and Jellyfin `12.0.0`.
- Captured exact live Sonarr/Radarr naming templates and quality definitions.
- Corrected the documented Radarr WEB-1080p preferred size from reconstructed 100 MB/min to the live value of 99 MB/min.
- Closed P0 reproducibility baseline; repository is now the documented source of truth for the current HomePi deployment.


## 2026-10-03

- Created first portable `homepi-infra` documentation baseline from setup history.
- Established `LLM_CONTEXT.md`, `CURRENT_STATE.md`, roadmap, architecture docs, and secret-handling rules.

## 2026-09 (reconstructed)

- Migrated Raspberry Pi system from 64 GB microSD to Samsung 990 EVO Plus 2 TB NVMe using `rpi-clone`.
- Confirmed direct NVMe boot and ~1.8 TB root filesystem.
- Deployed Docker base stack: Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin.
- Added media automation stack: qBittorrent, Sonarr, Radarr, Prowlarr, Seerr.
- Added Gluetun + Proton VPN WireGuard around qBittorrent only.
- Verified VPN IP isolation, kill switch, and Proton port forwarding.
- Fixed qBittorrent startup race for dynamic port-forward update.
- Fixed qBittorrent 5.2.3 network binding by using `tun0` + All IPv4 addresses.
- Added FlareSolverr as a private/tagged Prowlarr proxy.
- Added German/Dual-Language TRaSH custom formats and HomePi 1080p profiles.
- Fixed `/downloads` path issues and moved media workflow to common `/data` layout.
- Enabled qBittorrent Automatic Torrent Management so category save paths are applied consistently.
- Completed first real Sonarr end-to-end workflow and verified hardlinks.


## 2026-10-26 — Homepage operations cards (prepared)

- Add read-only systemd/journal collector, bounded persistent history, fresh/stale JSON serving and three internal customapi list widgets for backup, maintenance and audio.
- Add guarded installer with baseline hashes, payload checksums, shared lock and retained rollback configs. Existing worker scripts, schedules and Healthchecks are unchanged. No Pi installation is claimed.
- Twenty local status/HTTP tests pass; shell/YAML and adjusted-path systemd units validate. Actual Pi/Docker/Homepage validation remains pending. See operations/README.md.

## 2026-10-26 — Homepage operations status installed

- PR #14 merged; owner verified the pinned archive and matching settings baseline, ran the installer successfully and confirmed all three Homepage cards work.
- Retained rollback configuration: `/root/homepi-status-rollback.fnhzWRCx`. Existing workers, schedules and external Healthchecks unchanged. No full-backlog, reboot or live forced-failure test is claimed.
