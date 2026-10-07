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

Widget backend connectivity is separate from browser navigation. Working widgets use the HomePi host from inside the Homepage container via:

```text
http://host.docker.internal:<service-port>
```

The live Homepage Compose file includes an `extra_hosts` mapping for `host.docker.internal:host-gateway`.

## Current layout

The implemented dashboard layout is:

```text
MEDIA
Jellyfin          Seerr

SMART HOME & AUDIO
Home Assistant    Music Assistant

MEDIA MANAGEMENT
Sonarr            Radarr
Prowlarr          qBittorrent

SYSTEM
Arcane            Gluetun
```

## Confirmed native widget state

Confirmed working/configured:

- Sonarr
- Radarr
- Prowlarr
- qBittorrent
- Seerr
- Home Assistant
- Arcane

The qBittorrent widget reaches the WebUI through the host port published by Gluetun; do not point Homepage at a normal `qbittorrent:8080` container address because qBittorrent shares Gluetun's network namespace.

Still open / intentionally deferred:

- **Jellyfin:** deferred while the known Jellyfin-over-Tailscale issue prevents convenient remote admin/API-key setup. The widget backend and the browser-link problem are separate concerns.
- **Music Assistant:** keep as a normal service card unless a genuinely useful supported widget is identified. A widget is not required for Homepage V1.
- **Gluetun:** intentionally shown as a Docker-status card without a service link/widget; this exposes container health without adding another administration surface.
- **Tailscale:** intentionally not present as a Homepage service card. Tailscale is a host-level private-access layer, not a Docker workload managed through this dashboard.

## Secret handling

Homepage service API keys/tokens are kept only in:

```text
/srv/appdata/homepage/.env
```

using `HOMEPAGE_VAR_...` variables. Secrets must never be committed.

Known-good widget pattern:

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

## Runtime files and source-of-truth gap

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
.env
```

The non-secret YAML files were captured on 2026-10-07 and are mirrored under `stacks/homepage/config/`.

The exact live Compose structure was also synchronized, including:

- `env_file: .env` for local `HOMEPAGE_VAR_...` values;
- `extra_hosts: host.docker.internal:host-gateway` for widget-to-host connectivity.

The repository is now the reproducible reference for Homepage structure. The live Pi remains authoritative for secrets and for any changes made after the latest sync.

## Docker visibility

Homepage uses a restricted Docker socket proxy:

```text
CONTAINERS=1
INFO=1
POST=0
```

Keep the proxy read-only in spirit. Do not grant Homepage Docker write access merely to enrich the dashboard.

## Homepage V1 closure checklist

Required before marking Homepage V1 complete:

1. [x] Capture the exact live `/opt/homelab/stacks/homepage/compose.yaml` and synchronize its non-secret structure into Git.
2. [x] Capture and commit sanitized copies of `services.yaml`, `settings.yaml`, `widgets.yaml`, and `docker.yaml`.
3. [x] Keep `/srv/appdata/homepage/.env` out of Git and document only safe variable names in `.env.example`.
4. [ ] Run one final dashboard smoke test: current widgets render and current browser links work over the active access path, with the Jellyfin exception documented separately.
5. [ ] Add the Jellyfin widget after Jellyfin admin access is convenient again / the Tailscale issue is resolved.

Optional polish, not required for V1:

- refine descriptions/icons/order if desired;
- add only global/system widgets that provide clear signal rather than visual clutter;
- revisit Music Assistant/Tailscale only if supported widgets provide useful information.

## Related known issue

Jellyfin over Tailscale has a separate unresolved connection problem: the web client opens at `http://homepi:8096`, but does not connect to the server even when the server URL is entered manually. Do not diagnose that as a Homepage-link failure.
