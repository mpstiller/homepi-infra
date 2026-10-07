# HomePi — LLM Context

This file is the primary handoff for a new LLM/session. Read it before proposing changes.

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
/srv/backups          future backups
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

VERIFY ON PI: exact image digests/tags and current container versions should be captured from the live system.

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
  - System: Arcane, Tailscale
- The Sonarr native service widget is confirmed working.
- The Sonarr API key is stored only in the local Homepage `.env`; never commit it.
- The live Homepage config files under `/srv/appdata/homepage` (`services.yaml`, `settings.yaml`, `widgets.yaml`, `docker.yaml`) are not yet synchronized into this repository.

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
- Remote access was disabled during setup.
- Automatic UPnP/port mapping was disabled.
- Sony TV Jellyfin client was successfully connected.
- Big Buck Bunny was used as a test and Jellyfin explicitly reported **Direct Play**.

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

Manual cleanup has been used so far:

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

Known exception: the Jellyfin web client opens over Tailscale at `http://homepi:8096`, but server connection currently fails even when added manually. This is a Jellyfin-specific issue, not a general Tailscale or Homepage failure.

## 24. Future storage/cloud services

Planned but not yet implemented:

- Shared + personal photo cloud.
- File cloud.
- Backups.
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

## 26. Current next steps

Resume work in this order unless requirements change:

1. Finish the Homepage widget rollout while preserving the already implemented layout. Sonarr is the confirmed working reference widget.
2. Add and validate the remaining useful native widgets one by one, keeping API keys/secrets only in the local Homepage `.env`.
3. After the Homepage configuration is stable, synchronize the sanitized non-secret config structure into this repository so future sessions can recover it.
4. Investigate the separate Jellyfin-over-Tailscale server-connection issue.
5. Verify the Radarr import method/hardlink via logs on a future suitable import if desired.
6. Decide which authorized production indexers are retained.
7. Then move to the P1 backup workstream.

See `docs/homepage.md` for the dashboard-specific handoff.
