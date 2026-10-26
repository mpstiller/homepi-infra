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
- Jellyfin (owner-verified 2026-10-14)

The qBittorrent widget reaches the WebUI through the host port published by Gluetun; do not point Homepage at a normal `qbittorrent:8080` container address because qBittorrent shares Gluetun's network namespace.

Still open / intentionally deferred:

- **Music Assistant:** keep as a normal service card unless a genuinely useful supported widget is identified. A widget is not required for Homepage V1.
- **Gluetun:** intentionally shown as a Docker-status card without a service link/widget; this exposes container health without adding another administration surface.
- **Tailscale:** intentionally not present as a Homepage service card. Tailscale is a host-level private-access layer, not a Docker workload managed through this dashboard.

## Secret handling

Homepage service API keys/tokens are kept only in:

```text
/opt/homelab/stacks/homepage/.env
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
```

The non-secret YAML files were captured on 2026-10-07 and are mirrored under `stacks/homepage/config/`. The Jellyfin widget was added and owner-verified on 2026-10-14. The actual secret env_file is `/opt/homelab/stacks/homepage/.env`, outside the appdata YAML directory.

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
3. [x] Keep `/opt/homelab/stacks/homepage/.env` out of Git and document only safe variable names in `.env.example`.
4. [x] Final dashboard smoke test passed: current widgets render and service links work over the active access path, with the Jellyfin exception documented separately.
5. [x] Add and verify the Jellyfin widget (2026-10-14, subsequent to V1 closure).

Optional polish, not required for V1:

- refine descriptions/icons/order if desired;
- add only global/system widgets that provide clear signal rather than visual clutter;
- revisit Music Assistant/Tailscale only if supported widgets provide useful information.

## V1 status

**Homepage V1 is complete as of 2026-10-07.**

Validated:
- layout and service grouping;
- Docker stats via restricted socket proxy;
- native widgets for Sonarr, Radarr, Prowlarr, qBittorrent, Seerr, Home Assistant, and Arcane;
- service links over the active access path;
- reproducible Compose/config capture in Git;
- final smoke test.

The Jellyfin widget was added and owner-verified on 2026-10-14 after its remote-login blocker was resolved. Homepage V1 remained complete throughout this follow-up.

## Related known issue

Jellyfin remote server connection was resolved on 2026-10-14 by enabling its app-level remote flag. Both MagicDNS/IP public server-info calls return 200 and browser login works. No Homepage link change was needed; see `remote-access.md`. Remote playback remains untested; the Jellyfin widget is now configured and renders successfully.

## Jellyfin widget — confirmed 2026-10-14

Owner created a Jellyfin key named Homepage locally and added it to the verified Compose env_file `/opt/homelab/stacks/homepage/.env` as `HOMEPAGE_VAR_JELLYFIN_KEY`. The value was never shared in chat or Git; `.env.example` contains only the blank variable name. The former appdata env-file path in prose was corrected after owner readlink verification.

The existing Jellyfin card now uses:

```yaml
widget:
  type: jellyfin
  url: http://host.docker.internal:8096
  key: "{{HOMEPAGE_VAR_JELLYFIN_KEY}}"
  version: 2
  enableBlocks: true
  enableNowPlaying: true
  enableUser: false
  enableMediaControl: false
  fields:
    - movies
    - series
    - episodes
```

This follows the [official Jellyfin widget documentation](https://gethomepage.dev/widgets/services/jellyfin/) for installed Jellyfin 12.2.0. Homepage was recreated alone with `docker compose up -d --no-deps --pull never --force-recreate homepage` so it loaded the new env_file value. The owner confirmed configuration/rendering worked. No new API key is present in the checked-in configuration, and no other service was recreated by that command.

Widgets use container-to-host connectivity; browser navigation stays on `http://homepi:8096`. The socket proxy remains restricted. Keep the key in the actual env_file for future updates; a simple container restart does not reload changed environment values.


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
restore validation from the working cards. See `../operations/README.md`.

