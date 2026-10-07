# Current State

**Live baseline verified:** 2026-10-05  
**State updated:** 2026-10-07

## Stable / confirmed from the running Pi

- Raspberry Pi 5 boots from Samsung 990 EVO Plus 2 TB NVMe.
- Debian GNU/Linux 13.7 (trixie), kernel `6.18.39+rpt-rpi-2712`.
- Root filesystem is `/dev/nvme0n1p2` (ext4), about 1.8 TiB.
- At the audit: 78 GiB used (5%), temperature 43.9 °C.
- Bootloader is current as of 2026-05-26; `BOOT_ORDER=0xf461`.
- Docker Engine `29.8.0`, Docker Compose `v5.5.1`.
- Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the complete media stack are running.
- Verified Compose definitions are now checked into this repository for Arcane, Homepage, Home Assistant, Music Assistant, Jellyfin and the media stack.
- Music Assistant was historically deployed from `/srv/appdata/compose.yaml` (Compose project `appdata`); its verified definition is normalized into `stacks/music-assistant/compose.yaml`.
- Sony TV Jellyfin Direct Play was previously tested successfully.
- Home Assistant has Google Cast, Sony TV, Sonos, and Music Assistant integrations.
- SoundCloud works in Music Assistant.
- qBittorrent is isolated behind Proton VPN via Gluetun.
- Proton WireGuard, kill switch, public-IP separation and dynamic port forwarding were tested successfully.
- Live qBittorrent v5.2.3 is bound to `tun0` and `0.0.0.0` (All IPv4 addresses).
- Prowlarr -> Sonarr/Radarr Full Sync works.
- Seerr Automatic Search is enabled.
- Sonarr end-to-end workflow and hardlink import have succeeded in real use.

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

The current active workstream is the Homepage dashboard.

- The proposed service-group layout is already implemented.
- The Sonarr native widget is confirmed working.
- The Sonarr API key is stored in the local Homepage `.env`, not in Git.
- Continue with the remaining widgets one at a time and validate each before moving on.
- The live Homepage config files under `/srv/appdata/homepage` are not yet checked into this repository; preserve/synchronize a sanitized version once the dashboard is stable.

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


## Open issue: Jellyfin over Tailscale

From a remote MacBook connected through Tailscale, the Jellyfin web UI at `http://homepi:8096` is reachable, but Jellyfin does not successfully connect to the HomePi server.

Observed:
- Homepage link to `http://homepi:8096` opens the Jellyfin client.
- Automatic server discovery finds no server, which is expected across Tailscale because Jellyfin discovery is LAN/broadcast-oriented.
- Manually adding `http://homepi:8096` also fails.
- This is currently unresolved and should be investigated separately from the Homepage configuration.

Do not treat the Homepage link itself as the cause; other HomePi services are reachable through the same Tailscale/MagicDNS path.
