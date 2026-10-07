# Homepage

The verified live Homepage Compose definition is checked in as `compose.yaml`.

Persistent runtime configuration lives on the Pi under:

```text
/srv/appdata/homepage
```

The sanitized non-secret live configuration captured on 2026-10-07 is mirrored in:

```text
stacks/homepage/config/
├── services.yaml
├── settings.yaml
├── widgets.yaml
└── docker.yaml
```

The actual runtime files remain under `/srv/appdata/homepage/`. The repository copies are the reproducible reference and must be re-synchronized after intentional dashboard changes.

## Secrets

The live stack uses:

```text
/opt/homelab/stacks/homepage/.env
```

and the Compose file passes it into Homepage through `env_file`. It contains PUID/PGID plus the `HOMEPAGE_VAR_...` API keys/tokens used by native widgets.

Never commit the real `.env`. Use `.env.example` only for variable names/placeholders.

## Networking

Browser links use `http://homepi:<port>` for LAN/Tailscale navigation.

Widget backend calls use:

```text
http://host.docker.internal:<port>
```

The Compose file provides:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Docker stats are exposed to Homepage through the restricted `homepage-socket-proxy`; Homepage does not mount the Docker socket directly.

## Captured layout

- Medien: Jellyfin, Seerr
- Smart Home & Audio: Home Assistant, Music Assistant
- Medienverwaltung: Sonarr, Radarr, Prowlarr, qBittorrent
- System: Arcane, Gluetun

Native widgets are configured for Sonarr, Radarr, Prowlarr, qBittorrent, Seerr, Home Assistant and Arcane. Jellyfin remains a plain service card until the separate Jellyfin remote/admin-access issue is resolved.
