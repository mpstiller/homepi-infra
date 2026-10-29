# Arcane update strategy — limited rollout, 2026-10-29

## Decision and scope

Use the installed Arcane updater instead of building a separate controller. The owner explicitly preferred low maintenance and accepted the distinction between built-in image updates and the originally proposed comprehensive backup/validation/failure-stop chain.

Only these existing containers are eligible:

| Container | Initial configured tag | Automatic version range |
| --- | --- | --- |
| homepage | ghcr.io/gethomepage/homepage:v2.4.0 | 2.4.x, stable v-prefixed tags |
| homepage-socket-proxy | lscr.io/linuxserver/socket-proxy:3.4.6 | 3.4.x, plain numeric stable tags |
| homepage-operations-status | python:3.13.17-alpine3.24 | 3.13.x with the alpine3.24 suffix |

Strategies are in stacks/homepage/compose.yaml using x-arcane.updater. Security settings, mounts, networks, resources, worker code and existing healthchecks are unchanged. This updates the status container's Python image, not the bind-mounted homepi-status program.

Explicit tags can receive new image builds through digest changes even without a version increase. Patches can still break behavior; constraints do not classify migration requirements or security severity.

## Arcane settings and evidence

- Running manager v2.17.1 verified by owner inspect output: running, healthy. Its existing Compose still uses latest; v2.17.1 was explicitly pulled and retagged locally before a targeted --pull never update.
- Projects Directory: /opt/homelab/stacks, replacing the unused default /app/data/projects. Owner saw projects after the change.
- Auto Update activation: owner reported next execution 31 October 2026, 10:00 CET following enable/save instructions.
- Exclusions: owner confirmed every container except the three above checked as excluded. Exact persisted list/count: VERIFY ON PI if needed; no API/database export was supplied.
- Update delay: 72 hours, owner-guided configuration. Counts from detection of the target, not its upstream publication date; manual update actions bypass delay.
- Schedule: six-field cron `0 0 9 * * 6`. Arcane has no explicit TZ; official image default is UTC. Saturday 09:00 UTC = 10:00 CET / 11:00 CEST.
- Current configuration is UI state in Arcane's data, not wholly reproduced by the Compose file. Preserve its database backup. Newly added containers are not automatically excluded: review exclusions BEFORE deploying additional services.
- Never use Update All to enforce this restricted automatic scope: manual actions may include excluded services. In particular, leave Gluetun/qBittorrent maintenance to the existing documented procedure.

The recheck screenshot showed allowed targets Python 3.13.18-alpine3.24 and proxy 3.4.7, with Homepage 2.4.0 current. The owner confirmed all Homepage Docker indicators after the proxy build ls101 -> ls102 change. Homepage and status passed native Compose healthchecks. Local YAML comparison found only image references and updater metadata changed; candidate passed native Compose config --quiet. No unattended run, automatic rollback, exhaustive constraint-rejection test or post-update forced-failure drill is claimed.

The first 31 October schedule may not install images detected on 29 October: the 72-hour delay has not elapsed. If first detection was 29 October 13:16 CET and the target stays unchanged, the following weekly slot is 7 November 10:00 CET. Inspect actual history before drawing conclusions.

## Backup, concurrency and failure limits

Daily Restic backup at 04:30 Europe/Berlin, monthly maintenance at 05:30 on day one, audio and status workers, and external Healthchecks remain unchanged. Backup success on 27 October 04:31 was owner-evidenced before the Arcane work; do not infer later successful snapshots without checking.

This rollout does not add:
- a fresh backup or backup-success gate immediately before each scheduled update;
- acquisition of /run/lock/homepi-restic.lock by Arcane's scheduled updater;
- a durable global failure stop or guaranteed stop-after-first-failure for a batch;
- application-specific post-update validation or automatic restoration of application data;
- a new Homepage update-status card.

Existing healthchecks cover basic service behavior only; the socket proxy has no Docker healthcheck. Future Arcane updates may overlap a long backup/audio run despite the chosen schedule. The interactive installation steps acquired the shared lock; this does not make Arcane use that lock.

Major/minor versions outside the ranges wait for explicit review and policy changes. Out-of-range releases may be omitted from constrained pending-update results, so review upstream releases periodically; do not promise automatic notification for every excluded version. Urgent security releases may justify a reviewed manual update before the normal delay.

## Recovery material

- Arcane: /root/homepi-arcane-rollback.HSeiC04t/arcane-data-and-compose.tar.gz; the tar was made while Arcane was stopped under the shared lock, then Arcane restarted and passed health. Local old image name homepi-rollback/arcane:2.15.1 retained. Arcane may report a registry-check error for that deliberately local name.
- Homepage stack: /root/homepi-update-policy-rollback.Lm4egmnJ/ contains compose.yaml, compose.candidate.yaml, homepage-config and images-before.tar. The images tar preserves the three prior running image IDs. Retain old config and image identity together; the original latest tags are moving references and cannot alone guarantee rollback.
- Existing earlier status rollback remains /root/homepi-status-rollback.fnhzWRCx.

No rollback drill was performed. Restoring an old Arcane image alone after database migrations is not a safe recovery assumption; restore the matching data copy as needed. Capture current state first and follow the shared-lock/worker coordination when doing recovery. Do not repeat the original operations/install.sh bootstrap on this already installed stack. Its initial installation evidence refers to the historical pinned bundle, not the new version-policy rollout.

## Follow-up

After the first eligible scheduled run: inspect Arcane history, running tags/health, Homepage widgets and all three operations cards. A scheduled execution with no eligible targets is not a failed rollout. Record actual outcomes and synchronize Arcane's modified image references into Git without overwriting a newer runtime version.

References: [Arcane auto updates](https://getarcane.app/docs/docker/auto-updates), [Compose metadata](https://getarcane.app/docs/reference/compose-labels), [v2.17.1 source](https://github.com/getarcaneapp/arcane/tree/v2.17.1).
