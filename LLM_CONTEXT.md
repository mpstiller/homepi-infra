# HomePi — LLM Context

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


This file is the primary handoff for a new LLM/session. Read it before proposing changes.

Latest handoff: section 28 (2026-10-15). Gluetun pinning and targeted VPN checks are complete; next work is independent recovery secrets and backup visibility. The owner executes terminal commands; explain each step and wait for results. The owner published the change in PR #8; check its current merge status.

## Live verification baseline — 2026-10-05

A sanitized audit of the running Pi verified the reconstructed architecture against the live host.

- Debian GNU/Linux 13.7 (trixie), kernel `6.18.39+rpt-rpi-2712`.
- Root is the Samsung 990 EVO Plus 2 TB NVMe (`/dev/nvme0n1p2`, ext4).
- 78 GiB used / about 1.7 TiB available at the audit.
- Pi temperature was 43.9 °C.
- Docker Engine `29.8.0`; Docker Compose `v5.5.1`.
- Verified Compose definitions are checked into this repo for Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the media stack.
- Music Assistant was historically deployed from `/srv/appdata/compose.yaml` (Compose project `appdata`) and its verified live definition is normalized into `stacks/music-assistant/compose.yaml`.
- Home Assistant live version: `2026.9.2`; Jellyfin live version: `12.0.0`.
- qBittorrent live version is `v5.2.3`; paths and `tun0` + `0.0.0.0` binding are live-verified.
- qBittorrent has a global 30-minute seeding-time limit enabled and the share-limit action is **Stop torrent**.
- See `docs/live-system.md` for the normalized live snapshot.

## 1. Purpose

`homepi` is a Raspberry Pi 5 homelab intended to become a stable household server. Current priorities are smart home, music, media, and learning how the Pi is actually used before buying more storage or adding heavy services.

The owner can code but prefers infrastructure changes to be explained and applied incrementally with validation between steps.

## 2. Hardware and operating system

- Raspberry Pi 5, **4 GB RAM**.
- db-tronic PCIe M.2 NVMe kit / case with active cooling.
- System disk: **Samsung 990 EVO Plus 2 TB NVMe** (`Samsung SSD 990 EVO Plus 2TB`).
- The Pi now boots **directly from the NVMe**.
- Usable root filesystem size observed: about **1.8 TB**; about 15 GB was used immediately after migration.
- Original 64 GB microSD was cloned to the NVMe with `rpi-clone` and is now retained as a stale recovery copy, not as the normal boot disk.
- Raspberry Pi OS Lite 64-bit, Debian 13 (`trixie`), `aarch64`.
- Hostname: `homepi`.
- Primary user: `marc`.
- Time zone: `Europe/Berlin`.
- SSH enabled.
- Bootloader was updated in 2026 before NVMe migration.
- Boot order observed before migration: `BOOT_ORDER=0xf461` (SD first, then NVMe, then USB, repeat). Normal operation is with the SD card removed.
- PCIe left at default/stable settings; no Gen 3 overclocking was intentionally enabled.

## 3. Network context

- Router: FRITZ!Box 6690 Cable.
- ISP: O2 cable; connection uses **DS-Lite**, so there is no normal public IPv4 for inbound port forwarding.
- IPv6 is available.
- Final intended server placement: cellar near router via Ethernet.
- During setup the Pi was also used over Wi-Fi; `homepi.local` resolves on the LAN.
- Do not design remote access around exposing random router ports or UPnP.
- Tailscale is the implemented private remote-access layer for admin/device access. Public-app access, if added later, should use a separate controlled tunnel/reverse-proxy design; own domain remains future work.

## 4. Host directory conventions

These conventions are intentional and should remain stable:

```text
/opt/homelab/stacks   Docker Compose stacks
/srv/appdata          persistent application configuration/state
/srv/data             downloads + media on the NVMe
/srv/backups          local backup staging (cloud repository in Google Drive)
```

Media containers are designed to see a common `/data` mount backed by `/srv/data` on the host. This is critical for hardlinks.

Current media tree:

```text
/srv/data/
├── torrents/
│   ├── movies/
│   ├── tv/
│   ├── incomplete/
│   │   ├── radarr/
│   │   └── sonarr/
│   └── test/
└── media/
    ├── movies/
    └── tv/
```

## 5. Docker base

Docker Engine was installed from Docker's official Debian repository, including the Compose plugin. The user `marc` is in the `docker` group.

Most application containers use `restart: unless-stopped`.

Normal shutdown procedure:

```bash
sudo poweroff
```

Do **not** manually `docker stop` everything first; a manually stopped container may remain stopped after reboot under `unless-stopped` semantics.

## 6. Running application stack

Known services and LAN ports:

| Service | Purpose | Port / networking |
|---|---|---|
| Arcane | Docker/container management | `3552` |
| Homepage | service dashboard | `3000` |
| Home Assistant | smart-home backend | host network, `8123` |
| Music Assistant | music server/multiroom | host network, `8095` |
| Jellyfin | movies/TV streaming | `8096` |
| qBittorrent | download client | WebUI `8080`, network namespace shared with Gluetun |
| Gluetun | VPN gateway for qBittorrent only | VPN/WireGuard |
| Sonarr | series automation | `8989` |
| Radarr | movie automation | `7878` |
| Prowlarr | indexer management | `9696` |
| Seerr | request UI | `5055` |
| FlareSolverr | headless-browser proxy for authorized Cloudflare-protected sources | host loopback `127.0.0.1:8191`, Docker-internal `flaresolverr:8191` |

Exact current running image IDs/RepoDigests and available version evidence were captured read-only on 2026-10-14; see `docs/image-inventory.md`. Six app versions are direct queries; other versions are image-label evidence.

## 7. Arcane and Homepage

### Arcane

- Stack directory: `/opt/homelab/stacks/arcane`.
- Persistent data: `/srv/appdata/arcane`.
- UI: `http://homepi.local:3552`.
- Docker socket is mounted for container management.
- `/opt/homelab/stacks` is exposed to Arcane so stacks can be managed.
- Must remain LAN/private only.

### Homepage

- Stack directory: `/opt/homelab/stacks/homepage`.
- Persistent data: `/srv/appdata/homepage`.
- UI: `http://homepi.local:3000`.
- Uses a restricted Docker socket proxy with read-only-style permissions (`CONTAINERS=1`, `INFO=1`, `POST=0`).
- Dashboard layout is already organized as:
  - Media: Jellyfin, Seerr
  - Smart Home & Audio: Home Assistant, Music Assistant
  - Media Management: Sonarr, Radarr, Prowlarr, qBittorrent
  - System: Arcane, Gluetun; Tailscale is intentionally not a service card.
- Homepage V1 is complete as of 2026-10-07. Sonarr, Radarr, Prowlarr, qBittorrent, Seerr, Home Assistant and Arcane widgets are working/configured.
- Keys/tokens are stored only in the local Homepage `.env`; never commit them.
- Sanitized live YAMLs are checked in under `stacks/homepage/config/`; Compose includes `env_file` and the host-gateway mapping.
- Jellyfin widget version 2 is configured and owner-verified (2026-10-14); Music Assistant stays link-only.

## 8. Home Assistant

- Stack: `/opt/homelab/stacks/homeassistant`.
- Persistent config: `/srv/appdata/homeassistant`.
- Uses `network_mode: host`.
- UI: `http://homepi.local:8123`.
- Onboarding completed.

Confirmed integrations/use:

- Google Cast: Nest Hubs and Sony TV visible.
- Sony KD-65AF9 Android TV paired with Android TV Remote integration.
- Sonos Era 300 integrated.
- Music Assistant integrated into Home Assistant.

Deferred / not yet finalized:

- Matter server/integration (intentionally deferred until stable/final host state; do not unnecessarily re-pair existing Google Home Matter devices).
- Nest Doorbell via Google SDM.
- FRITZ!Box monitoring can be added later but is not a priority.

Existing Google Home voice behavior should remain intact for household usability; Home Assistant is an additional backend/automation layer, not a replacement for voice control.

## 9. Music Assistant

- Persistent data: `/srv/appdata/music-assistant`.
- The historical deployment source is `/srv/appdata/compose.yaml` (Compose project `appdata`); its verified definition is now checked in as `stacks/music-assistant/compose.yaml`.
- Uses host networking.
- UI/port: `8095`.
- Sonos Era 300 playback was tested successfully.
- SoundCloud integration is configured and working.
- Do not commit the SoundCloud client/token credentials.
- Tidal was planned; current configured status is **VERIFY ON PI**.

Device strategy:

- Music Assistant is the preferred orchestration layer for music.
- Native Home Assistant player integrations may coexist, but duplicate MA entities for generic Cast devices can be hidden/disabled where unnecessary.
- Yamaha R-N1000A is planned but was not yet physically integrated at the last confirmed state.

## 10. Jellyfin

- Stack: `/opt/homelab/stacks/jellyfin`.
- Persistent config/cache under `/srv/appdata/jellyfin`.
- UI: `http://homepi.local:8096`.
- Libraries:
  - Movies -> `/media/movies`
  - TV -> `/media/tv`
- Host media mount was changed from the early test directory to `/srv/data/media:/media:ro`.
- Remote access was disabled during setup, then enabled on 2026-10-14 to allow private Tailscale clients; hostname/IP API HTTP 200 and browser login are owner-verified. Router/UPnP policy was unchanged.
- Automatic UPnP/port mapping was disabled.
- Sony TV Jellyfin client was successfully connected.
- Big Buck Bunny was used as a test and Jellyfin explicitly reported **Direct Play**.
- Jellyfin was updated to `12.2.0` on 2026-10-08; Kodi Sync Queue loaded successfully.
- The Kodi chat proposed Jellyfin for Kodi for the native Movies/TV library. VERIFY ON PI/TV: client migration, initial sync and offline change catch-up; plugin loading alone does not confirm these.

Design principle: prefer Direct Play. The Pi is not intended to be a heavy video-transcoding server.

## 11. Media automation architecture

Current intended flow:

```text
Seerr
  -> Sonarr / Radarr
      -> Prowlarr -> indexers
      -> qBittorrent
           -> network namespace: Gluetun
           -> Proton VPN (WireGuard)
      -> /data/torrents/...
      -> hardlink/import/rename
      -> /data/media/...
      -> Jellyfin
```

### Seerr

The earlier profile mismatch is resolved: normal Sonarr and Radarr requests use `HomePi 1080p` (profile ID 7), while Anime requests use the dedicated Sonarr Anime profile.

- UI: `5055`.
- Connected to Jellyfin.
- Jellyfin libraries Movies + TV selected/synced.
- Connected to Radarr and Sonarr.
- `Automatic Search` is now enabled for the live end-to-end workflow.
- Current Seerr version `3.5.0` (updated 2026-10-07); startup and Jellyfin sync validated after update.

### Sonarr / Radarr -> qBittorrent

Because qBittorrent shares Gluetun's network namespace, Sonarr/Radarr use:

```text
Host: gluetun
Port: 8080
```

Categories:

```text
Sonarr -> sonarr
Radarr -> radarr
```

Completed Download Handling:

- Enabled.
- `Remove Completed`: enabled on both Sonarr and Radarr qBittorrent clients.
- `Remove Failed`: enabled on both Sonarr and Radarr qBittorrent clients.
- Hardlinks enabled.

Hardlinks have been tested successfully in the real Sonarr workflow.

## 12. qBittorrent storage and category settings

The old/default `/downloads` paths caused real errors and were corrected. Do not reintroduce `/downloads` unless mounts are intentionally redesigned.

Global settings:

```text
Default save path: /data/torrents
Incomplete torrents: /data/torrents/incomplete
Default Torrent Management Mode: Automatic
```

Category settings:

```text
sonarr -> /data/torrents/tv
radarr -> /data/torrents/movies
test   -> /data/torrents/test
```

For Sonarr/Radarr category setting `Save path for incomplete torrents`, use `Default`, which results in category-specific subdirectories under the global incomplete path.

Saving management was changed to Automatic so category paths are actually applied. Relevant relocation behavior should remain enabled when category/default/category-save paths change.

A production Sonarr test initially downloaded some items to the wrong root path because torrent management was not Automatic. This was fixed.

## 13. qBittorrent + Gluetun + Proton VPN

This is a critical security boundary.

### Policy

Only qBittorrent goes through the VPN. Sonarr, Radarr, Prowlarr, Seerr, Jellyfin, Home Assistant, etc. remain on normal networking.

### Provider

- Proton VPN paid plan.
- WireGuard.
- Proton configuration created with NAT-PMP / port forwarding enabled.
- Moderate NAT disabled.
- VPN Accelerator enabled.
- NetShield configured conservatively (malware blocking, not aggressive ad/tracker filtering).

### Gluetun

Known important settings:

```text
VPN_SERVICE_PROVIDER=protonvpn
VPN_TYPE=wireguard
SERVER_COUNTRIES=Germany
PORT_FORWARD_ONLY=on
VPN_PORT_FORWARDING=on
```

The WireGuard private key lives only in the local `.env`, e.g. `PROTON_WIREGUARD_PRIVATE_KEY`. Never commit it.

qBittorrent uses:

```yaml
network_mode: "service:gluetun"
```

The qBittorrent WebUI port `8080` is therefore published on the Gluetun service, not qBittorrent itself.

### Binding / qBittorrent 5.2.3 workaround

A real issue occurred where trackers were not contacted until qBittorrent was bound to:

```text
Network interface: tun0
Optional IP address to bind to: All IPv4 addresses
```

The API representation observed for All IPv4 addresses is `0.0.0.0`.

This setting is important. With the previous binding, DHT/PeX/LSD could show Working while tracker contact and peer discovery did not work.

### Port forwarding

Gluetun receives a dynamic forwarded port from Proton and updates qBittorrent's `listen_port` through the qBittorrent Web API. qBittorrent is also set to `current_network_interface=tun0`.

The first implementation had a startup race: Gluetun obtained the forwarded port before qBittorrent's WebUI was ready. This was fixed with an UP command that:

1. waits for the qBittorrent WebUI,
2. sets the forwarded port + interface,
3. reads the qBittorrent preferences back,
4. confirms the expected port/interface.

Because Docker Compose interpolates `$`, shell variables in that command require `$$` escaping in Compose YAML.

qBittorrent localhost WebUI auth bypass is enabled so Gluetun can make the local API call over `127.0.0.1:8080`.

### Verified VPN properties

- qBittorrent public IP was different from the Pi's normal public IP and matched Proton.
- Kill-switch test passed: after intentionally bringing `tun0` down, qBittorrent did not fall back to the normal Internet path.
- Normal state was restored and revalidated afterward.
- Proton port forwarding successfully reached qBittorrent.

Do not alter this isolation casually.

## 14. Sonarr and Radarr quality profiles

Both have a custom profile named approximately:

```text
HomePi 1080p
```

The intended quality group combines:

```text
Bluray-1080p
WEBDL-1080p
WEBRip-1080p
```

The group was renamed to something descriptive such as `1080p Bluray + WEB` / `Bluray + WEB 1080p`.

Disabled for this V1 profile:

- Remux-1080p
- all 2160p / 4K
- all 720p
- HDTV-1080p (removed after profile refinement)

Upgrades are allowed and the combined 1080p Bluray+WEB group is the cutoff/upgrade target.

Language setting: `Any` where present. Language preference is handled through Custom Formats.

Advanced Media Management:

```text
Propers and Repacks: Do Not Prefer
```

## 15. German / Dual-Language Custom Formats

TRaSH definitions were imported separately for Radarr and Sonarr.

Scores:

```text
German DL                 11000
German DL (undefined)     11000
German                    10000
Not German or English    -35000
```

Profile settings:

```text
Minimum Custom Format Score: 0
Upgrade Until Custom Format Score: 11000
```

Resulting intent:

- English/original can be accepted as fallback.
- German-only is preferred over fallback.
- German dual-language is the preferred final state.
- Non-German/non-English releases are heavily penalized.

## 16. Quality-definition size limits

These were intentionally made more storage-conscious than unrestricted TRaSH values because the system currently uses only the 2 TB NVMe.

Radarr (MB/min):

```text
WEBDL-1080p   min 12.5  preferred 99   max 140
WEBRip-1080p  min 12.5  preferred 99   max 140
Bluray-1080p  min 50    preferred 120  max 180
```

Sonarr (MB/min):

```text
WEBDL-1080p   min 15  preferred 80   max 120
WEBRip-1080p  min 15  preferred 80   max 120
Bluray-1080p  min 50  preferred 100  max 150
```

These values were read directly from the live APIs on 2026-10-05. See `docs/media-quality-naming.md`.

## 17. Naming settings

Radarr:

```text
Rename Movies: Yes
Analyze video files: Yes
Movie Folder Format: {Movie CleanTitle} ({Release Year})
```

Standard Movie Format configured from the then-current TRaSH recommendation:

```text
{Movie CleanTitle} {(Release Year)} - {{Edition Tags}} {[MediaInfo 3D]}{[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```

Sonarr:

```text
Rename Episodes: Yes
Analyze video files: Yes
Multi-Episode Style: Prefixed Range
Series Folder Format: {Series CleanTitleWithoutYear} {(Series Year)} [tvdbid-{TvdbId}]
Season Folder Format: Season {season:00}
```

Standard Episode Format:

```text
{Series CleanTitleWithoutYear} {(Series Year)} - S{season:00}E{episode:00} - {Episode CleanTitle:90} {[Custom Formats]}{[Quality Full]}{[Mediainfo AudioCodec}{ Mediainfo AudioChannels]}{[MediaInfo VideoDynamicRangeType]}{[Mediainfo VideoCodec]}{-Release Group}
```

## 18. Prowlarr

- UI: `9696`.
- Sonarr and Radarr are connected under Settings -> Apps.
- Sync level: Full Sync.
- LinuxTracker was used as a successful legal/functionality test indexer.
- Internet Archive indexer repeatedly timed out even though both host and Prowlarr container could reach `archive.org`; it was treated as an indexer-specific issue.
- Indexers only sync to Sonarr/Radarr if their categories overlap the target app's configured categories. A TV-only indexer not appearing in Radarr was correctly diagnosed as category behavior, not a Prowlarr failure.
- Live indexer inventory on 2026-10-05: `BT.etree`, `EZTV`, and `YTS`, all currently tagged for the FlareSolverr proxy. Category sync results in EZTV in Sonarr and YTS in Radarr.

## 19. FlareSolverr

FlareSolverr was added to understand/test Prowlarr's headless-browser proxy path for sources the owner is authorized to access.

- ARM64-compatible container.
- Host exposure intentionally restricted to `127.0.0.1:8191`.
- Prowlarr accesses it internally as `http://flaresolverr:8191/`.
- A proxy tag such as `cloudflare` is used so only tagged indexers traverse the proxy.
- Direct API test succeeded.
- Prowlarr -> FlareSolverr path was successfully observed in logs.

Do not expose FlareSolverr publicly.

## 20. First real Sonarr end-to-end result

A series was requested through Seerr with Automatic Search enabled.

Confirmed flow:

1. Seerr request created Sonarr entries.
2. Sonarr searched via a Prowlarr-synced TV indexer.
3. Sonarr grabbed releases and sent them to qBittorrent.
4. qBittorrent downloaded through Gluetun/Proton.
5. Incorrect `/downloads` path settings initially caused `Errored`; fixed to `/data/...`.
6. Sonarr imported successful episodes using hardlinks.
7. Hardlinks were verified by inode/link count.
8. After deleting torrent + download files from qBittorrent, media files remained under `/srv/data/media/tv` with link count reduced from 2 to 1.
9. One bad release contained only an `info[...].mkv` file. It was removed from Sonarr's queue, blocklisted, and Sonarr automatically searched/grabbed a replacement.
10. A later path inconsistency was fixed by setting qBittorrent's Default Torrent Management Mode to Automatic.

This confirms the Sonarr pipeline is functionally working.

## 21. Seeding / cleanup state

Historical manual validation (superseded by the automatic cleanup below):

- Wait until Sonarr successfully imports.
- Confirm hardlink exists (`links=2`).
- Remove torrent **and downloaded torrent-side files** from qBittorrent when seeding is no longer desired.
- The `/data/media/...` hardlink remains and becomes `links=1`.

Live qBittorrent has a 30-minute global seeding-time limit enabled, ratio limiting disabled, and share-limit action `0`, which is **Stop torrent**. Sonarr and Radarr both have per-client `Remove Completed` enabled. The Radarr end-to-end test validated the automatic cleanup chain: after the seed period qBittorrent stops the torrent, Radarr removes the completed torrent and torrent-side data, and the imported media file remains.

Private trackers may impose ratio/seeding requirements and must be handled according to their rules.

## 22. Storage decision

Do **not** recommend buying a 12 TB HDD by default right now.

Current decision: use only the 2 TB NVMe for system, appdata, downloads, and media while learning real usage patterns. Reconsider HDD capacity when actual sustained storage usage justifies it.

This was an intentional decision to avoid unnecessary cost, noise, power use, and complexity.

## 23. Remote access / domain

Tailscale is implemented and is the private remote-access layer.

Current HomePi identity:

```text
Hostname: homepi
Tailscale IPv4: 100.72.110.114
```

Hardening is complete: Device Approval is enabled, the default allow-all policy was removed, only the tailnet owner may access HomePi, access is restricted to required ports, Tailscale SSH is disabled in favor of normal OpenSSH, key expiry is disabled for the headless HomePi node, and Tailscale auto-update is enabled.

DS-Lite remains a constraint for conventional inbound IPv4. Own-domain/public-app access is still future work and should use a separate controlled tunnel/reverse-proxy design. Admin UIs must remain private.

Resolved 2026-10-14: app-level EnableRemoteAccess=false caused the separate Jellyfin server-connection failure (local API 200, remote 503). Changing only that flag to true restored hostname/IP API HTTP 200 and browser login; remote playback remains untested. Rollback retained at /root/homepi-jellyfin-network-rollback.4_6mobfk/network.xml.

## 24. Future storage/cloud services

Planned but not yet implemented:

- Shared + personal photo cloud.
- File cloud.
- Custom web-app hosting.

Immich was considered but deferred because the Pi has only 4 GB RAM and the system should first stabilize around current workloads.

Existing custom apps (`planner` / WirZwei and `quoernchenkueche`) currently remain better suited to Vercel + Supabase Cloud rather than moving production to the Pi.

## 25. e-ink household dashboard

Long-term project: portrait, picture-frame-like e-ink household dashboard with Wi-Fi, battery, and ideally full-surface touch.

Desired functions:

- weather
- shared calendar / today's events
- shopping list with check/add interaction
- remotely sent household messages
- Home Assistant scenes/buttons (e.g. all lights off/on)
- temperatures, tasks, reminders, possibly news

Current hardware preference:

- Pragmatic V1: Seeed Studio reTerminal E1003 (10.3-inch monochrome e-paper, touch).
- Desired future option: ~13.3-inch monochrome/greyscale e-paper with full capacitive touch, Wi-Fi, battery, black frame.
- E1004 is larger but no touch and therefore not the preferred control panel.

Software direction: Home Assistant as backend/data/action layer; UI should be hardware-independent and can be prototyped in a browser first. Tesserae/ESPHome/custom frontend remain options.

## 26. Backup V1 closure and next steps

Backup V1 is complete within the owner's agreed scope as of 2026-10-14. Restic/rclone protects appdata and stacks in Google Drive with consistent staging, daily 04:30 backups, 7 daily / 4 weekly / 6 monthly automatic retention, and monthly prune/check at 05:30 on day 1. `/srv/data` is excluded.

Revised scripts under `backup/bin/` are installed: shared flock, explicit restart failures and EXIT retry. Native lock, timers and real backup/maintenance runs passed. Snapshot `b37715a7` restored fully to `/srv/backups/restore-validation.Nz6ggIgG` (3236 files/directories, 334.493 MiB); restored roots are directly `srv/appdata` and `opt/homelab/stacks`.

The corrected copied-state checker passed 41 checks (13 SQLite databases, three XML configs, 23 Home Assistant JSON files, YAML and LiteDB presence). Kodi Sync Queue uses LiteDB, not SQLite; full integrity is not proven by presence. Sonarr restored startup/API succeeded, version 4.0.20.3014, with four matching series IDs. Owner explicitly chose one representative application-start test and deferred further starts. Do not re-propose testing every application as a V1 prerequisite.

Home Assistant/Jellyfin startup, LiteDB integrity, YAML/PEM semantics, UI login, media/download integrations and full-host disaster recovery remain untested. Independently recoverable password/OAuth secrets still need verification; do not mark this done or expose secret contents. Test restore and rollback files remain local. Earlier Docker memory stats reported 0B/0B while memory-limit support was unavailable. Support is now verified after the boot fix; individual caps and enforcement under pressure remain untested.

Resume in this order:

1. Jellyfin remote login/widget, Docker RAM/swap-limit support and Gluetun pinning are complete. The full image/digest inventory remains the historical 2026-10-14 capture; targeted Gluetun checks and recovery were owner-verified on 2026-10-15. See section 28 and `docs/gluetun-maintenance.md`.
2. Add lightweight backup failure/staleness visibility after choosing a channel; verify independently stored recovery secrets.
3. During normal use verify Radarr hardlinks, retained authorized indexers and Kodi client synchronization.
4. Choose Matter/smart-home or a browser-first household dashboard; measure resources before photo/file cloud and preserve existing storage/cloud decisions.

Repository verified config and owner-supplied execution outputs are primary evidence. Refer to `CURRENT_STATE.md`, `ROADMAP.md`, `docs/backup-restore.md` and `docs/restore-runbook.md`.

Homepage Jellyfin widget is now owner-verified: version 2, backend host.docker.internal:8096, count blocks/Now Playing, no user names/media controls. Key exists only in /opt/homelab/stacks/homepage/.env (readlink-verified), not chat/Git. services.yaml and blank .env.example key match the applied instructions. No widget work remains.

Inventory completed: 13 running containers, all local tags match running IDs, no errors; Gluetun/FlareSolverr unchanged versus Oct 5. Docker memoryLimit/swapLimit=false; about 1.56 GiB host RAM available. No update/pull/restart occurred and remote-registry freshness was not checked. Preserve API-vs-label evidence in docs.

Memory-controller support is resolved: the guarded `scripts/enable-memory-cgroup.py` appended only `cgroup_enable=memory` to the verified NVMe boot command line, with rollback retained. Five local boot-line tests passed. Owner rebooted and verified root controllers `cpuset cpu io memory pids`, Docker RAM/swap limits=true, all 13 containers running and all four configured healthchecks healthy. See `docs/resource-limits.md`. No per-service caps or memory-pressure enforcement test was performed. The earlier inventory JSON intentionally preserves pre-fix flags. Do not require memory in legacy `/proc/cgroups` for this cgroup-v2 kernel or repeat the completed boot change. Do not manually stop containers before normal reboot under `unless-stopped`.

## 27. End-of-session handoff — 2026-10-14

Historical handoff; superseded by section 28 below. PR #7 was subsequently confirmed merged.

Owner explicitly stopped work. PRs #1–#6 are merged; PR #7 (https://github.com/mpstiller/homepi-infra/pull/7) was open at handoff and carries the already applied/verified memory-controller fix. Re-check PR status and read latest main plus PR #7 if still open. Local checkout contains earlier published changes; inspect before resetting or overwriting it. No new Pi action is scheduled and no Gluetun pin/update or per-service memory cap has been applied.

Resume with the concrete Gluetun pinning evaluation in ROADMAP.md, using checked-in Compose/decisions and the verified digest as the starting point. Confirm live evidence before applying changes; preserve and validate VPN isolation/binding/forwarded port/kill switch. Backup visibility and private independent-secret recovery follow next. Do not reopen all-app restore tests: owner accepted one representative Sonarr start for Backup V1. Historical inventory support=false remains an accurate pre-fix capture; current controller/Docker support is true.

## 28. Gluetun pinning and current handoff — 2026-10-15

PRs #1–#7 are merged (GitHub main `f659b8d`). The owner applied the one-line media Compose pin to `qmcgaw/gluetun@sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793`; local Compose now mirrors it. This preserves the previously validated image, not a new release. No image pull/update occurred. Backup/maintenance were inactive before the initial operation; Compose validation passed. The owner executes all terminal commands and wants incremental explanations.

Joint recreation initially confirmed the pinned image, matching namespace IDs, `tun0` / `0.0.0.0`, matching Proton/qBittorrent port and different host/VPN public IPv4 addresses. A previously reachable fixed-IP HTTP target failed with `tun0` DOWN both before and after the request. This is targeted IPv4 blocking evidence only; no IPv6/DNS leak audit or exhaustive failure test is claimed.

Recovery interruption: raising `tun0` left qBittorrent on `lo` / port `0`, consistent with the configured forwarding-down hook. A Gluetun-only Docker restart was healthy but its request to the qBittorrent API returned no parseable JSON; the forwarded-port command produced no value in the supplied output. A stale namespace is a possible explanation, not a proven diagnosis. Recreating both services restored API `v5.2.4`, binding and matching dynamic port `33266`, followed by a successful outbound IP request. Do not hardcode this port or infer automatic recovery from a healthy VPN container. Follow `docs/gluetun-maintenance.md` for planned joint recreation and postchecks; ordinary automatic reconnection/full-stack reboot behavior was not established by this test. No hook, firewall, backup or restart policy was changed.

The owner created commit `c20e80f` on branch `maintenance/gluetun-pin-2026-10-15` in a separate worktree based on origin/main and published [PR #8](https://github.com/mpstiller/homepi-infra/pull/8). Check its merge status before treating pinning as part of main. The original checkout retains an older HEAD and existing local changes, including unrelated deliverables; do not blindly stage or reset it. The original local HTTPS push failed because Git used marc-perelyn; the owner added mpstiller through gh auth login and successfully pushed using that active account. The raw October 14 inventory remains unchanged with its historical flags/references.

Next: privately verify independent recovery access to restic/rclone/application secrets and choose lightweight failure/staleness notifications. Keep Backup V1 closed within the accepted representative Sonarr-start scope. Radarr hardlinks, Kodi native-library sync and remote Jellyfin playback remain normal-use checks; per-service memory caps remain unset. No further Pi changes are scheduled without the owner's next instruction.
