# Live system snapshot

**Captured:** 2026-10-05 15:45 CEST

This snapshot was generated from the running Pi and is the current verified baseline.

## OS / host

- Hostname: `homepi`
- Architecture: `aarch64`
- OS: Debian GNU/Linux 13.7 (trixie)
- Kernel: `6.18.39+rpt-rpi-2712`
- Root filesystem: `/dev/nvme0n1p2`, ext4
- NVMe: Samsung SSD 990 EVO Plus 2TB
- Root capacity: 1.8 TiB
- Used at capture: 78 GiB / 5%
- Temperature at capture: 43.9 °C
- Boot order: `0xf461`
- Bootloader: 2026-05-26, up to date at capture

## Docker runtime

- Docker Engine: `29.8.0`
- Docker Compose: `v5.5.1`

Running containers at capture:

| Container | Image tag | State |
|---|---|---|
| arcane | `ghcr.io/getarcaneapp/manager:latest` | healthy |
| homepage | `ghcr.io/gethomepage/homepage:latest` | healthy |
| homepage-socket-proxy | `lscr.io/linuxserver/socket-proxy:latest` | up |
| homeassistant | `ghcr.io/home-assistant/home-assistant:stable` | up |
| music-assistant | `ghcr.io/music-assistant/server:latest` | up |
| jellyfin | `jellyfin/jellyfin:latest` | healthy |
| gluetun | `qmcgaw/gluetun:latest` | healthy |
| qbittorrent | `lscr.io/linuxserver/qbittorrent:latest` | up |
| sonarr | `lscr.io/linuxserver/sonarr:latest` | up |
| radarr | `lscr.io/linuxserver/radarr:latest` | up |
| prowlarr | `lscr.io/linuxserver/prowlarr:latest` | up |
| seerr | `ghcr.io/seerr-team/seerr:latest` | up |
| flaresolverr | `ghcr.io/flaresolverr/flaresolverr:latest` | up |

Exact image digests and application versions are captured in the second live-config audit before P0 is considered complete.

## Storage usage

At capture:

```text
/opt/homelab/stacks   64K
/srv/appdata          264M
/srv/data             62G
/srv/backups          4K
```

The media tree contains TV libraries for Family Guy, Rick and Morty, and Severance.

## Docker networks

Verified networks:

- `arcane_default`
- `homepage_homepage-internal`
- `jellyfin_default`
- `media_default`
- Docker `bridge`, `host`, and `none`

## qBittorrent live state

Version: `v5.2.3`

Verified preferences:

```text
save_path                    /data/torrents
temp_path_enabled            true
temp_path                    /data/torrents/incomplete
current_network_interface    tun0
current_interface_address    0.0.0.0
torrent_content_layout       Original
max_ratio_enabled            false
max_seeding_time             30
max_seeding_time_enabled     true
autorun_enabled              false
```

The listen port is dynamically assigned by Proton/Gluetun and was `48367` at capture; it must not be treated as static.

Categories:

```text
radarr -> /data/torrents/movies
sonarr -> /data/torrents/tv
test   -> /data/torrents/test
```

The category share limits inherit the global/default qBittorrent policy.

## Gluetun live state

- WireGuard connected successfully.
- Firewall enabled.
- Port forwarding active and qBittorrent was successfully configured with the current forwarded port.
- DNS: DNS-over-TLS upstream, malicious-host blocking on, ad blocking off.
- Gluetun reported its running build as eight commits behind the latest build at capture. This is maintenance information, not a failure condition.

## Compose-source verification

Live Compose files were found and synchronized for:

- Arcane
- Homepage
- Home Assistant
- Jellyfin
- Media stack

The Music Assistant container is running, but no corresponding Compose file was captured under the expected `/opt/homelab/stacks` path. Its Docker labels/mounts must be inspected in the second audit before the deployment source is documented.
