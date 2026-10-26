# Roadmap

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


**Reconciled:** 2026-10-15, using repository state and owner-executed targeted Gluetun checks. No new full live audit was performed. P0, Homepage V1, the main update window, operational Backup V1 and Gluetun pinning are complete. Unticked items below remain unverified or planned.

## Current handoff — 2026-10-15

PRs #1–#7 are merged, including the completed memory-controller fix. The owner executed all Pi commands and published Gluetun pinning/documentation in [PR #8](https://github.com/mpstiller/homepi-infra/pull/8) from a separate worktree based on origin/main. Check the PR merge status before assuming main contains this change. The original checkout retains existing changes against an older HEAD; preserve that checkout.

Pinning and targeted IPv4 isolation, tunnel-down blocking and final recovery checks are complete. Manual tunnel-up left qBittorrent on `lo` / port `0`; a Gluetun-only Docker restart did not restore its API path. Joint recreation restored the API, `tun0` / `0.0.0.0`, matching forwarded/listen port and outbound connectivity. Do not infer automatic recovery from Gluetun health alone. See `docs/gluetun-maintenance.md` for evidence, limitations and the validated maintenance procedure.

Next: verify independent recovery secrets privately and choose lightweight backup failure/staleness visibility. Backup V1, Jellyfin remote login, Homepage widget and memory-controller activation are complete; do not repeat them as prerequisites. Per-service memory caps remain unset. No further Pi changes are scheduled without the owner's next instruction.

## Recommended execution order

1. **Backup follow-ups.** Verify independent recovery secrets and add lightweight failure/staleness visibility after choosing a channel. Backup V1 is closed; additional app-start/full-host recovery tests are optional/deferred by owner decision.
2. **Maintenance follow-ups.** Image/digest/resource inventory, Docker memory/swap support and Gluetun pinning are complete. Use the documented joint-recreation procedure for planned VPN-container maintenance. Automatic VPN-failure recovery is not established by the manual recovery test; investigate separately if needed, preserving the fail-closed behavior.
3. **Normal-use media checks.** Capture Radarr hardlink evidence before cleanup, decide retained authorized indexers and verify Kodi client synchronization. Remote Jellyfin playback can be validated during normal use; login and Homepage widget are complete.
4. **Next household capability.** Matter/smart-home integration or a browser-first e-ink prototype; photo/file cloud requires measured resources. Preserve the decisions to defer Immich, HDD purchase and production-app migration.


## P0 — Make the current system reproducible ✅

- [x] Sync all verified Compose definitions into this repo.
  - [x] Arcane
  - [x] Homepage
  - [x] Home Assistant
  - [x] Music Assistant
  - [x] Jellyfin
  - [x] Media stack
- [x] Add safe `.env.example` files where external environment files are used.
- [x] Capture host, Docker, application versions and exact running image digests.
- [x] Reconcile reconstructed documentation against the live Pi.
- [x] Capture live *arr/Prowlarr/Seerr/Home Assistant settings.
- [x] Capture live naming and quality definitions.
- [x] Add restore/runbook documentation.

## P1 — Sony audio compatibility pilot

- [x] Probe AOT S01E01 and test AC3 variants on Sony; removing TrueHD while retaining AC3/subtitles passed owner playback/seeking tests.
- [x] Prepare guarded worker/disabled-by-default units and local tests; see audio/README.md.
- [x] Install worker only and run a read-only single-file plan on Pi (owner output 2026-10-26, two TrueHD tracks detected).
- [x] Install/verify corrected Jellyfin 12 Authorization header (owner API and real apply succeeded 2026-10-26).
- [x] Validate actual single-file worker replacement with temporary pilot archive and successful normal-library Sony playback (2026-10-26). Jellyfin refresh request returned; independent arr metadata/rename and actual rollback drill remain follow-ups, not completed claims.
- [x] Review 36-episode dry-run backlog, verify API idle path and explicitly activate timer; first two automated replacements completed without archives (2026-10-26). Busy-session deferral remains locally tested only.

## P1 — Finish media stack V1

- [x] Run Radarr end-to-end movie test.
- [ ] Verify Radarr hardlinks in the same way Sonarr was verified.
- [x] Validate automatic 30-minute seed -> stop -> Radarr cleanup behavior.
- [x] Confirm Jellyfin scans and Direct Play for imported material.
- [ ] Decide which authorized production indexers are retained.
- [ ] Deferred by owner 2026-10-24: Kodi native-library synchronization. Current priority is the Sony audio-compatibility pilot; Kodi did not provide the desired playback solution.
- [x] Close Homepage V1 and make it reproducible.
  - [x] Final service-group layout implemented.
  - [x] Sonarr widget working.
  - [x] Radarr widget working.
  - [x] Prowlarr widget working.
  - [x] qBittorrent widget working.
  - [x] Seerr widget working.
  - [x] Home Assistant widget working.
  - [x] Arcane native widget configured and retained.
  - [x] Music Assistant remains link-only; Gluetun is a Docker-status card; Tailscale is intentionally not a dashboard service.
  - [x] Jellyfin widget version 2 added and rendering owner-verified on 2026-10-14.
  - [x] Capture the exact live Homepage Compose file and sync the live `env_file` + `host.docker.internal:host-gateway` structure into Git.
  - [x] Commit sanitized `services.yaml`, `settings.yaml`, `widgets.yaml`, and `docker.yaml`; never commit the local Homepage `.env`.
  - [x] Run one final Homepage smoke test, including current service links over the active LAN/Tailscale access path; keep the known Jellyfin exception separate.
  - [ ] Optional: visual/global-widget polish only where it adds useful signal.

## P1 — Maintenance hygiene

- [x] Complete the 2026-10-08 low/medium-risk container update window.
- [x] Revalidate qBittorrent VPN binding and Proton forwarded port after update.
- [x] Pin Gluetun to the already validated running digest, without an image update; owner verified targeted IPv4 blocking and successful joint recovery on 2026-10-15. See `docs/gluetun-maintenance.md` for test limits and the observed recovery interruption.
- [x] Refresh exact image digest/version evidence after the update window (owner capture 2026-10-14, 13 containers, no errors).
- [x] Diagnose and enable Docker memory/swap-limit support: guarded boot override applied; controller and Docker flags verified after reboot, with all 13 containers running. Individual service budgets/caps remain a separate measured decision.
- [x] Update Home Assistant to `2026.10.0` and validate normal operation; monitor the separate `fritz.powerline` SSDP discovery error.
- [x] Update Jellyfin to `12.2.0` and validate startup, libraries, Seerr integration, playback, and Kodi/JellyCon.

## P1 — Backups V1 ✅

- [x] Choose restic.
- [x] Initialize encrypted restic repository in Google Drive and complete first backup of `/srv/appdata` and `/opt/homelab/stacks`.
- [x] Automate recurring backups and retention.
  - [x] Add and validate separate monthly restic prune/check maintenance job.
  - [x] Validate production-style staging backup with cache/log excludes (333.155 MiB snapshot).
  - [x] Install and enable systemd service/timer; manual systemd execution validated successfully.
- [x] Capture installed backup/maintenance scripts and all four systemd units in Git; review retention/excludes, restart failure handling and overlap behavior.
- [x] Prepare restart failure detection/cleanup and a shared backup/maintenance lock; eight local simulated tests passed.
- [x] Install revised scripts on the Pi (owner-reported successful installer output, 2026-10-14).
- [x] Validate native flock contention/release and restored timer scheduling on the Pi (owner output, 2026-10-14).
- [x] Validate real systemd backup execution with the revised script: snapshot `b37715a7`, successful retention and post-run container check (2026-10-14).
- [x] Validate real systemd maintenance execution with the revised script: prune/check completed, no errors, exit 0 (2026-10-14).
- [x] Document observed restore paths and validate restored SQLite/XML/Home Assistant JSON (41 checks, 0 failures, 2026-10-14).
- [x] Validate isolated Sonarr startup/API and retained series IDs (four series, 2026-10-14).
- [x] Test restore and run `restic check`; both completed successfully.

Backup V1 closes with full temporary restore, copied-state checks and one representative restored application start, as explicitly agreed with the owner. This does not claim every service/full-host recovery has been tested.

## Backup follow-ups (separate from V1 closure)

- [ ] Verify independent recovery access to the restic password, rclone OAuth configuration and application secrets.
- [x] Add lightweight backup failure/staleness notifications via external Healthchecks email monitoring; real failure/recovery paths and timer scheduling confirmed on 2026-10-20. Deliberately missed-run test not performed. Optional Homepage last-success display remains deferred.
- [ ] Optional/deferred: additional application-start tests, Kodi Sync Queue LiteDB integrity, YAML/PEM semantics and full-host disaster recovery.
- [ ] Choose when to remove the retained root-only restore test directory/rollback copies; no cleanup has been performed.

## P1 — Jellyfin private remote access

- [x] Resolve the documented server-connection failure over Tailscale; both API routes HTTP 200 and browser login verified (2026-10-14).
- [ ] Validate remote playback during normal use; no remote playback result is claimed.
- [x] Add Homepage Jellyfin widget with local-only API key and verify rendering (2026-10-14).

## P2 — Network / remote access

- [x] Implement and harden Tailscale as the private overlay network for admin access.
- [ ] Buy/configure own domain.
- [ ] Decide public-app tunnel/reverse-proxy architecture.
- [ ] Keep admin UIs private.

## P2 — Smart home

- [ ] Add Matter server/integration without breaking existing Google Home fabric.
- [ ] Integrate Nest Doorbell via Google SDM.
- [ ] Add Yamaha R-N1000A when physically ready.
- [ ] Optional FRITZ!Box monitoring.

## P2 — Storage / cloud

- [ ] Measure real NVMe consumption over time.
- [ ] Add HDD only when usage justifies it.
- [ ] Evaluate photo cloud when RAM/resource budget is clearer.
- [ ] Evaluate file cloud.

## P3 — Household e-ink dashboard

- [ ] Prototype portrait UI in browser first.
- [ ] Define Home Assistant data/actions contract.
- [ ] Re-evaluate available 10–13.3-inch touch e-paper hardware at purchase time.
- [ ] Implement shopping list, calendar, messages, scenes, weather.
