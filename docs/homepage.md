# Homepage dashboard

## Purpose

Homepage on port `3000` is the central HomePi service dashboard. It should provide both navigation and useful at-a-glance status without weakening the private-network security model.

## Access model

User-facing links (`href`) should work from both LAN and Tailscale clients. The preferred remote form is:

```text
http://homepi:<port>
```

where the client resolves `homepi` through Tailscale MagicDNS. The Tailscale IPv4 `100.72.110.114` is the fallback for clients that mishandle single-label hostnames.

Homepage itself currently allows:

```text
homepi.local:3000
homepi:3000
100.72.110.114:3000
```

Widget backend connectivity is a separate concern from browser navigation. Do not assume an `href` that works from a Tailscale client is automatically the correct `widget.url` from inside the Homepage container.

## Current layout

The dashboard layout is already implemented as:

```text
MEDIA
Jellyfin          Seerr

SMART HOME & AUDIO
Home Assistant    Music Assistant

MEDIA MANAGEMENT
Sonarr            Radarr
Prowlarr          qBittorrent

SYSTEM
Arcane            Tailscale
```

## Confirmed widget state

- Sonarr native widget: working.
- Sonarr API key: stored in the local Homepage `.env` as a `HOMEPAGE_VAR_...` variable.
- Homepage resolves widget backends through `host.docker.internal`.
- The live Homepage container has an `extra_hosts` mapping for `host.docker.internal:host-gateway`.
- Secrets must never be committed.

Sanitized Sonarr reference block:

```yaml
- Sonarr:
    icon: sonarr.png
    href: http://homepi:8989
    description: Serienverwaltung
    server: homepi
    container: sonarr
    showStats: true
    widget:
      type: sonarr
      url: http://host.docker.internal:8989
      key: "{{HOMEPAGE_VAR_SONARR_KEY}}"
      enableQueue: true
      fields:
        - wanted
        - queued
        - series
```

The remaining widgets should be added and validated incrementally, using this as the known-good reference pattern where applicable.

## Runtime files

The live dashboard configuration is under:

```text
/srv/appdata/homepage/
```

Key files:

```text
services.yaml
settings.yaml
widgets.yaml
docker.yaml
```

These files are not yet synchronized into Git as of 2026-10-07. Until they are captured, the live Pi is authoritative for dashboard YAML.

## Docker visibility

Homepage uses a restricted Docker socket proxy:

```text
CONTAINERS=1
INFO=1
POST=0
```

This should remain read-only in spirit. Do not give Homepage write access to Docker merely to support dashboard widgets.

## Next work

1. Continue from the working Sonarr widget.
2. Add the remaining desired widgets one at a time.
3. Validate displayed data and browser links separately.
4. Keep all API keys/tokens in the local `.env`.
5. Once stable, commit only sanitized configuration/structure so a future session can reconstruct the dashboard accurately.

## Related known issue

Jellyfin over Tailscale has a separate unresolved connection problem: the web client opens at `http://homepi:8096`, but does not connect to the server even when the server URL is entered manually. Do not diagnose that as a Homepage-link failure.
