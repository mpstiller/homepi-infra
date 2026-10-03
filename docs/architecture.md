# Architecture

## High-level view

```text
                    LAN / household clients
                            |
       +--------------------+--------------------+
       |                    |                    |
Home Assistant        Music Assistant         Jellyfin
       |                    |                    |
 smart-home              Sonos/Cast           Sony TV

Media request / automation path:

Seerr
  -> Sonarr / Radarr
      -> Prowlarr -> Indexers
      -> qBittorrent
           -> Gluetun -> Proton VPN -> Internet
      -> /srv/data/torrents
      -> hardlink/import
      -> /srv/data/media
      -> Jellyfin
```

## Design constraints

- Raspberry Pi 5, 4 GB RAM: resource budget matters.
- DS-Lite: do not assume inbound public IPv4.
- Direct Play is preferred for media.
- qBittorrent is the only service that should use the Proton VPN tunnel.
- All media download/import paths must share a single host filesystem to preserve hardlinks.
- Admin UIs remain private/LAN-side.
- 2 TB NVMe is intentionally the only mass storage for now.
