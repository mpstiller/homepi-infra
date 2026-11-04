# Current State

## Paperless-ngx pilot — 2026-11-04 (live; backup passed; restore pending)

2026-11-04 11:22:40 CET: first post-Paperless-integration systemd backup completed successfully, new restic snapshot `ef45cae4`, Paperless db/broker healthy after restart, webserver health still starting at first immediate check. Snapshot restored successfully to separate `/srv/backups/restore-paperless.OBa8o5B2` (5,442 files/dirs, 486.679 MiB); live broker/db/webserver all healthy. Restored DB start/records and media relation not yet validated; no real documents ingested.


2026-11-04: Verified installed `/usr/local/sbin/homepi-backup` SHA-256 matches `main:backup/bin/homepi-backup` exactly (0ce674a1…7d85). Current CANDIDATES does not include Paperless; proposed PR adds webserver/db/broker. Backup stop-list installed under lock with exact-diff verification and retained rollback `/root/homepi-backup-before-paperless.iutMZWUb`; no successful post-change backup or isolated restore has occurred.


After actual user discovery: archive is a personal completed-document paper trail, Google Drive remains for editable files; equal priority for gradual backlog and incoming capture, minimal administration. iPhone/Mac and controlled mail rules later. No employer/client docs; local-first processing, no external AI by default; possible future shared use/permissions unresolved. Owner reported 1.7 GiB available RAM, 745 MiB swap used, 1.4 TB free NVMe. A PR proposes Paperless 3.4.1 + PostgreSQL 18 + Valkey 9, localhost-only 8010, one OCR worker/thread, private env and all data below /srv/appdata/paperless, proposed backup CANDIDATES. **Pilot deployed 2026-11-03:** owner pulled three images; db and broker healthy, webserver initially `health: starting`; bound localhost 8010. **No installed backup integration, restore, live mobile/mail access or real personal document imports yet.** Owner read-only preflight confirmed UID/GID 1000, Compose v5.5.1, free port 8010, no Paperless directories/containers. Compose validated. All three services now **healthy**; effective Arcane opt-out labels false verified. Live docker stats: 637.5 MiB web, 45.92 MiB db, 7.922 MiB broker; RAM available 1.1 GiB, swap used 992 MiB. Owner confirmed synthetic digital PDF `Wasserkocher` and raster-only scan `Sonnenuhr` both searchable; OCR/indexing verified. Installed backup, isolated restore, real documents and large-load headroom remain unverified; checkout cleanliness still pending. See stacks/paperless/README.md and docs/paperless-pilot.md on the proposed branch. Do not mark this as installed or production-safe.


## Next session: tailored Paperless-ngx discovery — 2026-11-03

Owner selected Paperless-ngx as the next experiment, explicitly in a NEW session. Current work is documentation only: do not research the detailed setup, deploy Paperless or import documents in this session. Begin the next session with needs discovery, then thorough current upstream research, then a tailored proposal and short owner-executed Pi steps. See [Paperless discovery brief](docs/paperless-discovery.md) and [ideas backlog](docs/ideas-backlog.md). Document categories/volume, capture sources, users/sharing, taxonomy, privacy, iPhone workflow, resources and recovery are unresolved; do not assume defaults are the owner's preferences.

All discussed ideas are retained as candidates; existing household e-ink and file/photo-cloud plans are linked rather than duplicated. Immich/heavy stacks, HDD purchase and migration of existing cloud apps remain deferred under existing decisions. No new service/hardware was selected besides the Paperless trial workstream.

Additional owner evidence/decisions since the Matter PR:
- matter-server is explicitly confirmed excluded from Arcane Auto Update.
- 3 November audio journal: start 07:00:04, Deactivated successfully and Finished in the same second; no conversion messages. This verifies a scheduled successful invocation, not a multi-file conversion or lock-wait test.
- Existing logins remain unchanged: the proposed Seerr/Tailscale login bridge was explicitly deferred. No pilot commands, proxy, login service or authentication changes were applied.
- Arcane first post-fix actual update verification remains pending for 7 November 10:00 CET; do not call it completed.

## Matter backup installation and real run — owner evidence 2026-11-02

This supersedes the preparation-only backup status below.

- Installed baseline SHA256 415d749e771a87148ebdc866d9b1137e20b708c68b318bbb4e7addfc65ac2db9 matched the repository. Guarded installer added only matter-server to CANDIDATES, checked candidate SHA256 0ce674a100f0f9428516e6bb4d72c4372ec02708bd93e0398a54d780b70f7d85 and bash syntax, and retained /root/homepi-matter-backup-rollback.6fxgbvcj. Owner confirmed successful installation.
- Owner started homepi-backup.service. Journal: started 19:45:51 CET, stateful stop 19:45:52, staging 19:45:59, restart of matter-server 19:46:00, upload 19:46:05. Upload reached retention with new snapshot e43eddfa (19:46:06, 417.233 MiB); completed 19:47:13 and systemd Finished/Deactivated successfully at 19:47:14.
- Retention kept 10 snapshots and removed the earlier same-day dc59a3ce entry; this is expected daily retention, not loss of the new snapshot.
- Real backup/staging/restart/upload/retention are evidenced. Owner subsequently confirmed the requested Home Assistant switching/Google Home state test still works after the restart. Exact Matter file presence inside the cloud snapshot and Matter restoration were not separately checked. No new restore claim.
- Remaining: explicit Arcane exclusion confirmation and optional resource measurement. Preserve scheduled audio/Arcane verification dates and private fabric data.

## Matter devices connected — owner evidence 2026-11-02

- Owner installed ghcr.io/matter-js/matterjs-server:1.5.5 (arm64, image user 1000:1000); native Compose validation passed and startup reported Healthy.
- Separate project matter: /opt/homelab/stacks/matter/compose.yaml; data /srv/appdata/matter-server (created owner 1000:1000, mode 0700). Host network, read-only container root, LISTEN_ADDRESS=127.0.0.1 and PRIMARY_INTERFACE=wlan0. Home Assistant 2026.10.0 uses host networking and connected at ws://127.0.0.1:5580/ws.
- Owner output confirmed IPv6 enabled and an IPv6 route via wlan0; this is not a complete network/firewall audit. Before deployment ~1.7 GiB RAM available and 676 MiB swap used; post-start resource use remains unmeasured.
- First Eve Energy was shared from Google Home using a fresh pairing code and Home Assistant iPhone flow: Add Devices -> already in use -> Other controllers. Choosing Google Home led to a help flow without direct code entry; do not repeat that route.
- First device switching and Google Home state were owner-tested successfully. Owner subsequently confirmed all their Matter devices are connected; exact device inventory and individual tests for remaining devices were not supplied. Preserve existing Google Home fabrics; no reset/removal is needed.
- Excluding matter-server from Arcane Auto Update was instructed but not explicitly confirmed: VERIFY ON PI. Keep automatic eligibility limited to the three Homepage containers.
- Existing backup rsync includes the new data/Compose directories, but the installed stop list predates matter-server. This branch adds only matter-server to CANDIDATES; installation and a real consistent snapshot are still pending. Do not claim backup integration complete or restore tested. Fabric data/keys and pairing codes stay private, never Git/chat.
- Next: compare installed backup checksum with the baseline, install the one-line stop-list addition with rollback under the shared lock, and verify a backup and restart. Then capture resource use and optional device inventory. Audio scheduled test 3 November 07:00 CET and Arcane scheduled test 7 November 10:00 CET remain pending.
- Owner also confirmed daily audio Homepage display correct after PR #18 merged; first scheduled daily batch remains pending.

## Daily audio batch installed — owner evidence 2026-11-02

Owner verified installer SHA256 `45b87a8cfbf3f435e67310f7255b620b546255a42a9f559f6dc6cd0968b6f1ff` from commit `cbbeab4a05b8df8b37790b36137e6f55b23bd672` against the previously verified payload from `a722392a2d7624bf1cdfcc9cbf4ea27e7ab05e08`. Guarded installer completed successfully, including four-file baseline/payload checks, Python parsing, native systemd verification, collector refresh and timer restart. No conversion was started by installation.

- New daily timer is active: NEXT `Tue 2026-11-03 07:00:00 CET`. The printed LAST value refers to the previous schedule; it is not evidence of a new batch.
- Preserve rollback directory `/root/homepi-audio-daily-rollback.VFwqadR8`, containing the old four files and verified payload. Rollback recovery was not exercised.
- New worker/service support sequential batches and waiting for the existing lock. Existing media guards remain; manual apply still defaults to one file. Homepage collector uses the daily 30-hour overdue heuristic. HTTP routes/freshness remain unchanged.
- Still pending: owner visual Homepage/card verification, first daily scheduled run, native busy-lock waiting and a real multi-file batch. Do not repeat installation or claim those tests from installer success alone.

## Preparation evidence — 2026-11-02 (installation now confirmed above)

- Owner supplied successful inactive/exit-0 audio state and repeated silent timer completions. Explicit `--scan` produced no output. Within the worker's cached eligible scope, no pending candidates were reported; this is not an independent re-probe of every media file.
- Owner requested daily processing after backups instead of five-minute polling; accepted 07:00 Europe/Berlin, sequential processing of all eligible files, and waiting for the shared lock.
- Prepared `--batch` (requires --scan --apply) and `--wait-lock`. Default manual apply remains one file; dry scan still does not write media/cache. Batch stops on playback/source-race deferral or an error; remaining work waits for the next daily run, without automatic retries.
- New timer: daily 07:00 Europe/Berlin, no boot/monotonic trigger, Persistent=false (missed starts are not caught up outside the scheduled window). Existing backup 04:30 and monthly day-one maintenance 05:30 remain unchanged. Service ordering and the existing exclusive lock prevent simultaneous audio/backup/maintenance; a long batch can delay a later backup. Start time alone is not proof a backup succeeded.
- Homepage collector now allows 30 hours between audio invocations and recognizes lock waiting and completed-batch counts. JSON freshness remains 120 seconds and collector interval unchanged. A partial/deferred/failed batch is not shown as full success even if earlier files were converted.
- Local evidence: 51 audio/status tests pass; calendar expression validated; service/timer verified with only local executable path substituted by /usr/bin/true. No production API/conversion/backup run was triggered.
- Installed baselines supplied by owner still match old worker `17a2c935df16cb8f5c3747d2733e1d238cabae06b4ce9d5f673b0ef1bfef7d2f`, service `a0abaa5f3981bf5ade22700117caf3236deadc704d2529157e083df723550d00`, timer `a54bb6c1649c11262859838bcb9a854ac2894d1222e3c22b5c2a1041c71fc8d1`, collector `e3c4d12944aaaf613a477c3b7deedff070a68cb6931b84e90acf4b72083b9c35`.
- Preparation completed; installation confirmation and remaining live verification are recorded above. See audio/README.md.

## Arcane runtime labels corrected; Gmail tested — 2026-11-01

This supersedes the 29 October update handoff where runtime policy recognition was not yet proved.

- The scheduled 31 October 10:00 CET job completed, but its activity reported the three existing tags "up to date" and 17 pending image-update records; no installed update was demonstrated. Those records are not a count of applied updates. This cannot be attributed solely to the 72-hour delay.
- Owner inspect output proved all three running containers lacked updater strategy/constraint/tag-pattern labels. The previous x-arcane-only Compose was started using Docker Compose outside Arcane, which ignores the extension. Project recheck could read the file metadata while container-based checks lacked the policy. Earlier activation was therefore not evidence of working tag selection.
- Replaced the three x-arcane updater blocks with explicit com.getarcaneapp.arcane.updater.* labels, keeping all image tags, ranges, regexes and other service settings unchanged. Candidate passed native config --quiet; owner recreated only these services with --pull never under the shared host lock. Compose reported all three Healthy; this does not establish a new socket-proxy healthcheck.
- Runtime inspection now confirms tag / 2.4.x for Homepage, tag / 3.4.x for proxy, and tag / 3.13.x with alpine3.24 suffix for the status image. Fresh Image Update Watcher execution was followed by a container-list screenshot: Homepage current, proxy/status updates available. Exact new targets were not shown in that screenshot; no post-fix application is claimed.
- Owner re-enabled/saved Auto Update with the existing exclusions, 72-hour delay and Saturday 09:00 UTC schedule; reported next execution in six days on 1 November (expected 7 November 10:00 CET).
- Gmail SMTP notification setup succeeded using an owner-created app password (never supplied to chat): smtp.gmail.com:587, STARTTLS. Owner confirmed the provider test email arrived. Image-update and container-update subscriptions were instructed; exact persisted subscription flags: VERIFY ON PI if required.
- Source inspection of Arcane v2.17.1 and its updater v0.11.13 confirms container-update notifications describe successful changes; update failures return before the notifier path. Email is NOT a verified failed-update alarm. No production failure was induced and no separate failure monitor was installed.
- Next: inspect first post-fix scheduled execution and actual image/tag changes, verify Homepage/cards, then sync any changed Compose tags. Retain three-service scope; preserve independent backup/audio/Healthchecks/VPN setup and prior limitations. Do not repeat initialization or claim a comprehensive failure-stop/backup-gated controller.
- Recovery directory /root/homepi-update-policy-rollback.Lm4egmnJ now additionally holds compose.before-labels.yaml and compose.labels.yaml. The former restores the pre-fix policy bug; use it only deliberately. Older images-before.tar/config copies remain retained. See docs/update-strategy.md.

## Arcane-managed Homepage patch updates — 2026-10-29

Historical 29 October handoff; superseded by the 1 November runtime-label correction above.

- Owner upgraded Arcane from v2.15.1 to v2.17.1; running version and Docker health verified. Compose still references manager:latest; only its local tag was pointed to the explicitly pulled v2.17.1 image. Do not claim Arcane itself is version-pinned.
- Arcane Projects Directory changed from /app/data/projects to /opt/homelab/stacks. Owner then saw projects and successfully rechecked the homepage project.
- Homepage Compose now uses explicit tags plus x-arcane tag strategies: Homepage v2.4.0 constrained to 2.4.x; socket proxy 3.4.6 constrained to 3.4.x; Python 3.13.17-alpine3.24 constrained to 3.13.x and the Alpine 3.24 tag variant. The socket proxy's first manual change installed build 3.4.6-r0-ls102; owner confirmed Homepage Docker indicators still work. Homepage used the identical image; Homepage and status container passed native Compose --wait healthchecks.
- Owner configured 72-hour delay and excluded all containers except homepage, homepage-socket-proxy and homepage-operations-status. After instruction to enable/save, owner reported next execution 2026-10-31 10:00 CET. This is activation/schedule evidence, not evidence of an unattended update.
- Schedule: six-field cron 0 0 9 * * 6, UTC (no explicit TZ); Saturday 10:00 winter / 11:00 summer in Germany. Delay begins when a target is detected: the first scheduled job can skip targets younger than 72 hours.
- Screenshot recheck found Python 3.13.17-alpine3.24 -> 3.13.18-alpine3.24 and socket proxy 3.4.6 -> 3.4.7; Homepage v2.4.0 current. This confirms recognition of the prepared tag policies, not an exhaustive test of rejecting every disallowed tag.
- Owner chose built-in Arcane updates over a custom controller. Existing daily Restic backup remains the safety net. There is NO newly installed pre-update backup gate, shared host-lock integration for scheduled Arcane updates, durable failure latch, full functional validation/automatic data rollback, or Homepage update-status card. Larger versions and critical services require manual review; a patch number is not a guarantee of harmlessness.
- One-off Pi changes used the existing shared lock. Existing backup/audio workers, monitoring, status cards, Gluetun digest and qBittorrent VPN isolation were not edited. Timing alone does not prevent a long backup/audio job from overlapping a future Arcane update.
- Retain /root/homepi-arcane-rollback.HSeiC04t (Arcane data+Compose archive) and local homepi-rollback/arcane:2.15.1. The latter generated the observed registry-check error; it is a local image name, not a published repository.
- Retain /root/homepi-update-policy-rollback.Lm4egmnJ with old Compose, candidate, homepage-config copy and images-before.tar. Do not delete these. Rollback recovery itself remains untested.
- Next: inspect the first eligible scheduled run and all three service outcomes; retain explicit limits and synchronize Compose changes back to Git after future Arcane tag updates. Do not repeat initialization. See docs/update-strategy.md.

## Homepage operations status installed — owner confirmation 2026-10-26

This supersedes the earlier preparation-only status. PR #14 is merged.
Owner verified the pinned archive for commit `bee00a4500de9b7c266cb6eefc24175a6da0bdf7`
(SHA256 `79cf59d517c878d1cfcec4e578d5821faaa7b4bc594b596dbe595a0a09e36a3f`)
and supplied matching settings baseline hash. Installer output confirms the Python
image pull, successful first collection, collector timer enablement, Homepage
running and status container started. Rollback config is retained at
`/root/homepi-status-rollback.fnhzWRCx`. Owner then confirmed all Homepage cards work.

The three cards (backup, monthly maintenance, audio) are operational. Existing
workers, schedules and Healthchecks remain unchanged. No further installation,
API-key setup or production job run is needed for this feature. Twenty local
status/HTTP tests passed before deployment. Detailed field-by-field reconciliation,
live forced-failure/stale-source tests, resource measurement and reboot behavior
were not separately evidenced; do not infer full backlog completion or new backup
restore validation from the working cards. See `operations/README.md`.

## Audio cleanup complete — 2026-10-26

PR #12 is confirmed merged. Owner confirmed deletion of the single retained pilot archive `/srv/data/media-originals/20261026T120935-4bd7557179ec` and the three created MKV files in `/srv/data/media/audio-tests` (Sony-Test, AC3-only, AC3-mit-Untertiteln). The converted normal-library S01E01 remains. Do not repeat these deletions or remove other archives. The now-empty optional Audio-Test Jellyfin library/folder can remain; UI removal was not reported. Automated conversion remains enabled without permanent originals. First two automatic completions are verified; full backlog completion is not yet reported. Next session should resume from the operational state rather than repeat installation, API-key setup or the one-file pilot.


## Sony audio automation operational — owner evidence 2026-10-26

This is the latest resume point and supersedes earlier pilot-pending notes below.

- Corrected worker installed from commit `7c7e630` (SHA256 `17a2c935df16cb8f5c3747d2733e1d238cabae06b4ce9d5f673b0ef1bfef7d2f`). Existing private API key works with MediaBrowser Authorization; owner diagnostic returned API access OK and idle=True. PR #12 still open at this documentation update; merge it so main matches the running fix.
- Explicit AOT S01E01 --apply --keep-original succeeded. Source was replaced after checks; pilot original remains at `/srv/data/media-originals/20261026T120935-4bd7557179ec`. Owner confirmed the actual normal-library episode played flawlessly on Sony. This is worker output playback evidence, not just the earlier manual test.
- Full-library dry-run listed 36 additional AOT episodes: S01E02–25 and S02E01–12, two or three TrueHD tracks each, original not archived. S01E01 was correctly absent. No other title was listed in the supplied output.
- Owner installed/verified captured service+timer (systemd-analyze verify had no messages), created the enable marker and enabled/started the timer. Automatic S01E02 ran 14:07:43–14:09:45 CET, S01E03 14:14:52–14:17:27 CET. Both logged REPLACED with original archive disabled and Finished successfully. The second job handled three TrueHD tracks. A third invocation began at 14:22:48; no result for it or the full backlog is claimed.
- Automatic mode creates no permanent original archive. Temporary staging still needs space; seeding hardlinks retain original bytes until normal existing cleanup. No in-place writes to shared download inodes occur. The observed invocations confirm the timer re-arms about five minutes after completion; NEXT='-' during an active invocation is not evidence of a stopped timer.
- Remaining closure: merge PR #12, remove only reviewed pilot/test copies after confirmation (not yet claimed deleted), optionally verify Sonarr refreshed audio metadata/renaming and continue normal-use remote playback/Radarr hardlink checks or choose the next household capability. Actual pilot rollback, busy-playback deferral, future download arrival, every backlog title and cross-reboot resumption remain untested live; do not reopen completed conversion as a prerequisite.
- Use short Pi terminal steps; Mac shell is fish. Do not re-create API keys, repeat the completed one-file conversion or reinstall the old legacy-header helper.


## Audio pilot authentication fix — 2026-10-26

PR #11 is merged. Owner installed the pinned worker (original SHA256 `50515e498048a5ba21d448dc048c734e0274199f4d17395c7132524898a63cc3`) and the explicit AOT S01E01 dry-run correctly planned two TrueHD tracks -> AC3 with pilot original retention. Owner created the private Jellyfin key file. Apply stopped with generic RuntimeError; read-only API diagnostics returned HTTP 401 even after a fresh key.

The helper incorrectly used legacy `X-Emby-Token`, disabled by default in Jellyfin 12. Prepared correction uses `Authorization: MediaBrowser Token="..."` for both session queries and library refresh, keeping tokens out of URLs/logs. HTTP failures now report status/method/fixed API path, not raw response bodies, headers or secrets. Do not create more API keys or enable legacy auth to work around this client bug.

Local suite: 17 tests pass, including GET/POST header format and secret-safe HTTP 401 reporting. Corrected-header Pi HTTP success, one-file apply, Sony validation and timer activation are still pending. No successful worker replacement is claimed. Next: install the corrected pinned worker, verify the existing key with the corrected request path, then resume the explicit single-file --keep-original pilot. Automatic mode still retains no permanent original archive.


## Original retention policy — owner decision 2026-10-24

Owner rejected permanent duplicate storage for audio compatibility. Automatic processing now creates a checked temporary derivative and atomically replaces the library file without an original archive. The first explicit single-file pilot uses `--keep-original` for temporary rollback only; this flag is refused with `--scan` and is absent from the automatic service. No existing archives/test files are deleted by this preparation.

Temporary output space is still needed. Existing torrent hardlinks keep original bytes until normal qBittorrent/arr cleanup; they are not changed or deleted by the worker. Without a separately retained original, lossless TrueHD cannot be recovered from the lossy AC3 derivative. Video remains stream-copied/hash-checked.

Fifteen local tests now pass, including default no-archive replacement, release of the old unlinked file, torrent-hardlink preservation and failed-publication preservation. Conversion arguments and unit scheduling are unchanged. Nothing is installed/enabled on Pi. Next: read-only one-file pilot plan with `--keep-original`, then deliberate one-file apply with the same flag; native Pi/API/Sony validation still precedes unattended activation.


## Sony TrueHD compatibility — 2026-10-24 (automation pilot pending)

Owner explicitly deferred Kodi: it did not provide a satisfactory final solution. Earlier Kodi/JellyCon success remains historical evidence, not the current chosen workaround.

- Real AOT S01E01 probe: English TrueHD 5.1(side), Japanese TrueHD stereo; original video is HEVC Main 10. Owner host output: 1.4 TiB free, 1.7 GiB available RAM, about 399 MiB swap used.
- A resource-limited separate Docker test reused the local Jellyfin image, added AC3 English 5.1 (640k) and Japanese stereo (192k), retained TrueHD/video/subtitles and wrote a separate test MKV in `/srv/data/media/audio-tests`. It completed in 2:15.57. All four audio tracks were probed successfully. Native Jellyfin Android TV playback was Direct Play but still stuttered/aborted; turning off subtitles did not fix it.
- A minimal video+Japanese-AC3 copy played smoothly but once aborted on seeking. Do not label that abort a proven network problem.
- A further remux keeping both AC3 tracks, subtitles/chapters and other streams while removing both TrueHD tracks was owner-tested successfully with subtitles, audio switching and seeking. This supports a derived file without TrueHD; one title does not prove a universal codec diagnosis.
- Prepared `audio/bin/homepi-audio`, service/timer and tests. Worker replaces TrueHD with AC3 in the TV derivative, retains an original only for an explicit --keep-original single-file pilot; normal automatic operation creates no original archive, maps other streams, verifies video payload hashes and uses read-only source mounts/one CPU/512 MiB. Shared backup lock, source fingerprints, playback-idle checks and a disabled-by-default enable marker limit unintended overlap. See `audio/README.md` for storage/race/rollback limits.
- Local evidence: 15 unit/transaction tests pass; native synthetic FFmpeg fixture with TrueHD 5.1/stereo, subtitle, chapter and font converted successfully with identical encoded video hash; systemd units verified locally with the executable path adjusted to the local checkout. These do not establish Pi worker/Docker/API behavior.
- NOT installed or enabled on Pi. Next: merge/review this preparation, install worker only from a clean pinned checkout, create a private dedicated Jellyfin API key, run read-only `--file --keep-original` pilot plan for AOT S01E01, then one-file apply with the same retention flag and metadata/Sony validation. Review whole-library dry-run before enabling the timer; no bulk conversion is claimed. Keep backup closure intact.


## Monitoring closure — 2026-10-20

- Owner supplied exact installed notification helpers and both systemd drop-ins; captured under `backup/bin/*-notify` and `backup/systemd/*.service.d/monitoring.conf`. URL contents are never included.
- Owner confirmed both Healthchecks checks returned to green after successful real backup/maintenance, failure emails arrived in controlled tests, and final timer scheduling is correct. Final timer confirmation is owner-reported; the raw list-timers output was not supplied.
- Local checks on the captured helper sources: both parse; 12 mocked cases cover start/success/failure routing, skip of failure after success, rejected URLs and network-timeout handling without disclosing secrets or failing the backup. No live requests were sent by these checks. The maintenance helper differs only by the URL-file path and whitespace.
- A missed-run alarm is configured by the daily/monthly cron schedules and grace times; a deliberately missed schedule/offline-Pi test was not performed. Helpers are best effort and errors do not fail backups. Maintenance standard restic check passed; no full data-read scrub/full-host recovery is claimed.
- Backup visibility is complete within the tested scope. Next roadmap work: normal-use media checks (Radarr hardlinks before cleanup, Kodi native-library synchronization, remote Jellyfin playback, retained authorized indexers), then choose Matter/smart-home or browser-first household dashboard. Independent-host recovery and full application-secret coverage remain optional/separate follow-ups.
- Cleanup of temporary transfer copies was instructed, but deletion was not explicitly confirmed. Do not delete retained restore/rollback directories without a separate choice.


## Backup monitoring and OAuth recovery — 2026-10-20

This section supersedes older resume instructions below. PRs #8 and #9 are merged; #9 merge commit is `b96a376`.

- Owner confirmed the restic password is in a password manager. After OAuth reconnection, the owner replaced the saved `/etc/rclone/homepi.conf` recovery attachment with the renewed configuration. Independent-host recovery is untested and application-secret recovery is not fully verified. Deletion of temporary transfer copies remains unconfirmed.
- Healthchecks.io monitoring is installed using root-only URL files under `/etc/homepi-monitoring/`, Python notification helpers in `/usr/local/sbin/` and systemd `monitoring.conf` drop-ins. Ping URLs are secrets. Installed helper/drop-in source was subsequently captured and locally checked; see Monitoring closure above.
- Daily check: cron `30 4 * * *`, Europe/Berlin, one-hour grace. Simulated failure/email and real backup/return to green were confirmed. At 08:19:20 CEST the backup completed with Result=success, ExecMainStatus=0; snapshot `c0280e8b` (345.933 MiB) and retention succeeded. Scheduled snapshots from Oct 15–20 are evidenced by owner output.
- Monthly check: cron `30 5 1 * *`, Europe/Berlin, six-hour grace. Simulated failure/email worked. The real 16:27 CEST run failed before opening the repository with rclone `invalid_grant`.
- Owner confirmed OAuth Testing status, completed GitHub Pages/Branding setup following PR #9 and confirmed In production. Seven-day Testing-token expiry is consistent with the incident timing. The headless reconnect used the explicit `/etc/rclone/homepi.conf`, browser authorization on the Mac and no Shared Drive. No tokens/client secrets were posted or committed.
- A read-only restic snapshot listing reopened existing repository `475950f8` and showed the expected snapshots. The subsequent real maintenance completed at 17:05:40 CEST with Result=success and ExecMainStatus=0: prune finished and standard restic check examined eight snapshots with no errors. This is not a claim of a full data-read scrub or new full-host restore.
- The renewed rclone recovery copy is now owner-confirmed saved in the password manager. Owner subsequently confirmed the monthly Healthchecks check returned to green. Successful helper exit alone would not prove delivery because monitoring errors intentionally do not fail backups.
- Monthly green state, timer schedule and monitoring source capture are now confirmed; see Monitoring closure above. Do not repeat OAuth reconnect or reopen Backup V1. Independent-host secret recovery and application-secret completeness remain separate follow-ups. Preserve incremental short terminal steps; the Mac shell is fish.


**Live baseline verified:** 2026-10-05  
**State updated:** 2026-10-15 (owner-executed Gluetun pinning and targeted VPN checks; no full live audit)

## Stable / confirmed from the running Pi

- Raspberry Pi 5 boots from Samsung 990 EVO Plus 2 TB NVMe.
- Debian GNU/Linux 13.7 (trixie), kernel `6.18.39+rpt-rpi-2712`.
- Root filesystem is `/dev/nvme0n1p2` (ext4), about 1.8 TiB.
- At the audit: 78 GiB used (5%), temperature 43.9 °C.
- Bootloader is current as of 2026-05-26; `BOOT_ORDER=0xf461`.
- Docker Engine `29.8.0`, Docker Compose `v5.5.1`.
- Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the complete media stack are running.
- Arcane updated to `2.15.1` on 2026-10-08; database migrations completed successfully and the post-start image scan completed with 0 errors.
- Verified Compose definitions are now checked into this repository for Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the media stack.
- Music Assistant was historically deployed from `/srv/appdata/compose.yaml` (Compose project `appdata`); its verified definition is normalized into `stacks/music-assistant/compose.yaml`.
- Music Assistant updated to `2.10.5` on 2026-10-08; startup completed cleanly, web/stream servers came up, and SONOS/Chromecast/DLNA providers loaded.
- Sony TV Jellyfin Direct Play was previously tested successfully.
- Jellyfin updated to `12.2.0` on 2026-10-08; startup/migrations completed successfully, Kodi Sync Queue loaded, library watchers started, and local UI/libraries/Seerr integration/playback/Kodi-JellyCon were practically revalidated.
- Home Assistant has Google Cast, Sony TV, Sonos, and Music Assistant integrations.
- Home Assistant updated to `2026.10.0` on 2026-10-08; Core startup succeeded. A FRITZ! SSDP discovery flow logged a `fritz.powerline` hostname parsing error.
- SoundCloud works in Music Assistant.
- qBittorrent is isolated behind Proton VPN via Gluetun.
- Proton WireGuard, kill switch, public-IP separation and dynamic port forwarding were tested successfully.
- qBittorrent updated to `5.2.4` on 2026-10-08; post-update validation confirmed `tun0`, `0.0.0.0` (All IPv4), and a valid Proton forwarded listen port.
- Prowlarr -> Sonarr/Radarr Full Sync works.
- Prowlarr updated to `2.6.5.5623` on 2026-10-07; startup and DB checks completed cleanly.
- Seerr Automatic Search is enabled.
- Seerr updated to `3.5.0` on 2026-10-07; startup completed cleanly and the post-start Jellyfin Recently Added scan completed successfully for Movies and Series.
- Sonarr end-to-end workflow and hardlink import have succeeded in real use.
- Sonarr updated to `4.0.20.3014` on 2026-10-07; startup and DB checks completed cleanly.

## Container maintenance window 2026-10-08

Completed and validated:
- Homepage updated and healthy; Homepage V1 smoke test passed.
- Homepage socket proxy updated successfully.
- Prowlarr updated to `2.6.5.5623`.
- Sonarr updated to `4.0.20.3014`.
- Radarr updated to `6.4.4.10685`.
- Seerr updated to `3.5.0`.
- Arcane updated to `2.15.1`.
- Music Assistant updated to `2.10.5`.
- qBittorrent updated to `5.2.4`; `tun0`, All IPv4 (`0.0.0.0`), and the Proton forwarded listen port were revalidated.

Remaining follow-up:
- **Gluetun:** the existing working build was pinned by digest on 2026-10-15, without an image update. Targeted VPN checks and recovery passed; see `docs/gluetun-maintenance.md`. A future version update remains a separate decision.
- **Home Assistant:** updated to `2026.10.0` on 2026-10-08. Core startup succeeded; a separate FRITZ! SSDP discovery error for hostname `fritz.powerline` was observed and does not appear to block Home Assistant operation.
- **Jellyfin:** updated to `12.2.0`; the Jellyfin-over-Tailscale server-connection issue was subsequently resolved on 2026-10-14; remote login works, playback is not yet tested.

The Pi was shut down cleanly and restarted after the maintenance work.

## Backup state — V1 complete within agreed scope (2026-10-14)

- Encrypted restic `0.18.0` via rclone `1.75.2` to `rclone:gdrive:HomePi-Backup` protects `/srv/appdata` and `/opt/homelab/stacks`; `/srv/data` is excluded.
- Consistent staging with brief stops of previously running candidate containers; caches/logs excluded; restart occurs before cloud upload.
- Daily systemd backup at 04:30, Persistent=true; retention is 7 daily / 4 weekly / 6 monthly automatic snapshots (default grouping).
- Monthly maintenance on day 1 at 05:30 runs prune/check. Both timers were restored and scheduling verified.
- Installed scripts/units are under `backup/`. Revised scripts are installed and use a shared flock; failed restarts abort upload and are retried in EXIT cleanup. Catchable termination preserves failure status.
- Native flock contention/release and successful real backup/maintenance execution were owner-verified. Backup ran 13:25:47–13:26:38 CEST; maintenance ran 13:34:36–13:35:21 with no errors.
- Snapshot `b37715a7` (334.493 MiB) saved; full temporary restore recovered 3236 files/directories to `/srv/backups/restore-validation.Nz6ggIgG`.
- Verified restore roots are directly `<target>/srv/appdata` and `<target>/opt/homelab/stacks`, without a staging prefix.
- Corrected checker passed 41 checks: 13 SQLite integrity checks, three XML configs, 23 Home Assistant JSON files, YAML presence and Kodi Sync Queue LiteDB presence. LiteDB is not SQLite; no full LiteDB integrity scan was performed.
- Isolated Sonarr restored startup passed on version 4.0.20.3014; all four series IDs matched. Test container/copy removed; live/source data unchanged.
- Owner chose this representative application-start test as sufficient for Backup V1 and deferred further app-start tests. Home Assistant/Jellyfin startup, LiteDB integrity, UI login and full-host disaster recovery are not demonstrated; these do not reopen agreed V1 scope.
- Rollback originals remain at `/root/homepi-backup-rollback.xDZCejUc`; the root-only restore test directory is still retained.
- Local staging/restore contains plaintext secrets. Password/rclone OAuth files live outside protected source trees; independent recovery access remains VERIFY ON PI and is a separate follow-up. Never commit secret contents.

## Current media configuration

### Paths

```text
/data/torrents/tv
/data/torrents/movies
/data/torrents/incomplete
/data/media/tv
/data/media/movies
```

Host equivalents are under `/srv/data`.

### qBittorrent categories

```text
sonarr -> /data/torrents/tv
radarr -> /data/torrents/movies
test   -> /data/torrents/test
```

### qBittorrent live share-limit state

The audit shows:

```text
max_ratio_enabled        false
max_seeding_time         30
max_seeding_time_enabled true
```

The global share-limit action is **Stop torrent**. Sonarr and Radarr both have `Remove Completed` enabled. The Radarr end-to-end test has validated the full automatic cleanup chain.

### Quality profile

`HomePi 1080p`, 1080p Bluray+WEB group, German/Dual-Language CF scoring, no 4K/720p/remux in V1.

## P0 documentation status

**P0 is complete.**

The repository now contains:

- all verified Compose definitions;
- safe environment templates where required;
- exact host, Docker and image inventory;
- live Sonarr/Radarr/Prowlarr/Seerr/Home Assistant configuration snapshots;
- live naming and quality-definition values;
- a restore runbook;
- explicit architecture decisions and LLM handoff context.

## Immediate resume point

PRs #1–#7 are merged (GitHub checked on 2026-10-15). Gluetun pinning is applied on the Pi and published in [PR #8](https://github.com/mpstiller/homepi-infra/pull/8); check its merge status before assuming main contains it. The owner created commit `c20e80f` in a separate worktree based on current origin/main and pushed the branch. The original checkout still has an older HEAD and existing local changes; preserve it and do not reset or blindly stage its files.

P0, Homepage V1, the main maintenance window, Backup V1 and Gluetun pinning are complete within their recorded scope. Jellyfin remote login/widget and Docker RAM/swap-limit support are complete. Next: verify independent recovery secrets privately and choose lightweight backup failure/staleness visibility. Optional broader recovery tests remain separate follow-ups in `ROADMAP.md`.

Homepage closure evidence:

- The service-group layout is implemented.
- Sonarr, Radarr, Prowlarr, qBittorrent, Seerr, and Home Assistant native widgets are confirmed working.
- Homepage API keys/tokens are stored only in the local `/opt/homelab/stacks/homepage/.env`.
- Jellyfin widget is configured and owner-verified as of 2026-10-14; the Tailscale/admin-access blocker is resolved.
- Arcane is configured with its native widget; Music Assistant remains link-only; Gluetun is shown as a Docker-status card; Tailscale is intentionally not a dashboard service.
- Homepage reproducibility is now closed: the exact live Compose structure is synchronized, including `env_file` and `host.docker.internal:host-gateway`.
- Sanitized live copies of `services.yaml`, `settings.yaml`, `widgets.yaml`, and `docker.yaml` are checked in under `stacks/homepage/config/`.
- Homepage V1 is complete: layout, widgets, Docker stats, service links, live Compose/config capture, and the final smoke test are all validated. The Jellyfin widget was subsequently added and owner-verified on 2026-10-14.

See `docs/homepage.md`.

## Seerr profile alignment

Seerr has now been updated so **both Sonarr and Radarr use `HomePi 1080p` (profile ID 7)** for new requests. The previous `HD-1080p` mismatch is resolved.

## Automatic cleanup live state

qBittorrent global share limits seed for 30 minutes and then **Stop** the torrent. Both Sonarr and Radarr have per-client `Remove Completed` enabled. A real Radarr request validated that the torrent and torrent-side data are removed after the seed goal while the imported media file remains.


## Anime profile

Anime is handled in the existing Sonarr instance with a dedicated profile:

- Profile: `HomePi Anime 1080p`
- Normal series in Seerr: `HomePi 1080p`
- Anime in Seerr: `HomePi Anime 1080p`
- Normal and Anime root folder: `/data/media/tv`

Priority logic:

1. best Anime release-tier / image quality;
2. original audio required;
3. no raws, dub-only, LQ groups, or AV1;
4. dual audio is only a small tie-breaker;
5. German-specific CFs remain neutral in the Anime profile.

Anime episode naming uses both season/episode and absolute numbering.


## Remote access

Tailscale hardening is complete:

- Device Approval is enabled.
- Default allow-all access has been removed.
- Only the tailnet owner can access HomePi.
- Access is limited to required application/admin ports.
- Tailscale SSH remains disabled; normal OpenSSH is used.
- Key expiry is disabled for the headless HomePi node.
- Tailscale auto-update is enabled.
- Login is through a Google account protected with a passkey.


Tailscale is installed and active on the HomePi host.

```text
Tailscale hostname: homepi
Tailscale IPv4:    100.72.110.114
```

Remote access from an iPhone over cellular has been verified to Homepage on port 3000 using both the Tailscale IPv4 address and MagicDNS short hostname in Safari.

Arc on iOS may interpret the single-label hostname `homepi` as a search term; use the Tailscale IPv4 or full MagicDNS FQDN in clients where this occurs.

Homepage host validation was updated to allow `homepi.local:3000`, `homepi:3000`, and `100.72.110.114:3000`.


## Radarr end-to-end result

Radarr updated to `6.4.4.10685` on 2026-10-07; startup and DB checks completed cleanly.

A real movie request completed successfully through:

```text
Seerr -> Radarr -> Prowlarr -> qBittorrent/Gluetun -> Radarr import
```

Verified:

- qBittorrent category: `radarr`
- download path: `/data/torrents/movies`
- Radarr History reports a successful download/import
- after the configured seed period the torrent disappeared from qBittorrent
- `/srv/data/torrents/movies` no longer contains the downloaded file
- the imported movie remains under `/srv/data/media/movies`
- the remaining media file has link count `1`

This confirms the automatic cleanup chain (seed -> stop -> Radarr Remove Completed -> torrent-side data removal). The import method itself still needs one final log check because the torrent-side hardlink had already been removed before inode/link-count comparison.


## Jellyfin movie playback validation

The imported Radarr movie was detected automatically by Jellyfin and played successfully on the Sony TV using **Direct Play** with no transcoding.

Verified movie path:

```text
Seerr -> Radarr -> Prowlarr -> qBittorrent/Gluetun -> Radarr import
     -> automatic seed/cleanup -> Jellyfin -> Sony TV Direct Play
```

This confirms the movie playback path is working end to end without Pi-side video transcoding.


## Sony playback compatibility finding

A 1080p HEVC Main 10 release with TrueHD audio showed severe stutter in the native Jellyfin Android TV client on the Sony KD-65AF9.

Observed behavior:

- Jellyfin Android TV + English TrueHD 5.1: some stutter
- Jellyfin Android TV + Japanese TrueHD 2.0: unusable
- forcing audio downmix caused Direct Stream and made playback worse
- the same file played cleanly on macOS
- the same file played cleanly on the Sony TV through Kodi + JellyCon

Conclusion: this is a client/playback-path compatibility issue in the Jellyfin Android TV app on the Sony, not a bad file, insufficient network throughput, or Pi-side server limitation.

Current policy: do not downgrade Sonarr/Radarr release quality just to optimize for the native Sony Jellyfin app. Keep quality-first selection; use Kodi/JellyCon as the compatibility fallback for problematic releases.


## Jellyfin over Tailscale — resolved 2026-10-14

Owner confirmed local `/System/Info/Public` HTTP 200 and Tailscale hostname/IP HTTP 503. `EnableRemoteAccess=false` was found in network.xml; the guarded script changed only that flag to true and restarted Jellyfin. The backup lock and private rollback copy protected the change.

Afterwards both Mac requests returned HTTP 200 and browser login succeeded. Tailscale/router policy and other XML settings were unchanged. The server-connection failure is resolved; remote playback remains untested; the Homepage widget is configured and owner-verified.

Rollback file: `/root/homepi-jellyfin-network-rollback.4_6mobfk/network.xml` (retained). Next workstream: inventory/maintenance and backup visibility per `ROADMAP.md`.

Jellyfin Homepage widget is configured and renders successfully (owner confirmation). It uses version 2, movie/series/episode count blocks and Now Playing; user names/media controls are disabled. `HOMEPAGE_VAR_JELLYFIN_KEY` is local only in the owner-verified `/opt/homelab/stacks/homepage/.env`. Homepage alone was recreated without pulling an image.

## Refreshed deployment inventory — 2026-10-14 15:42 CEST

Owner provided selected-field inventory: 13 containers running, all local references match their running image IDs, four configured healthchecks healthy, restartCount 0 and no capture errors. All images Linux/arm64. Docker 29.8.0, Compose 5.5.1, kernel unchanged. Six application versions were queried directly; other versions are image-label evidence.

11 image digests differ from the 2026-10-05 baseline; Gluetun and FlareSolverr digests are unchanged. Current exact references and raw snapshot are in `docs/image-inventory.md` and `docs/audits/image-inventory-2026-10-14.json`. No registry-version/update check or runtime modification was performed.

At inventory capture, Docker reported memory/swap-limit support false; available RAM was about 1.56 GiB and swap used about 275 MiB. The immutable capture retains these historical values.

## Docker memory-controller support — resolved 2026-10-14

Owner diagnosed cgroup v2/systemd with no memory controller and active `cgroup_disable=memory`. The guarded helper appended `cgroup_enable=memory` to `/boot/firmware/cmdline.txt`, preserving the original arguments and retaining a rollback copy. After a normal reboot the owner verified `cpuset cpu io memory pids`, Docker RAM-Limits=true and Swap-Limits=true.

All 13 containers were running again; the four configured healthchecks (Homepage, Jellyfin, Arcane and Gluetun) were healthy. Per-service memory caps were not assigned and enforcement under memory pressure was not tested. See `docs/resource-limits.md` for the applied change, validation and rollback.
