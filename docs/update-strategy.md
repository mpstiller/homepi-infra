# Arcane update strategy — runtime-label correction, 2026-11-01

## Decision and scope

Use the installed Arcane updater instead of building a separate controller. The owner explicitly preferred low maintenance and accepted the distinction between built-in image updates and the originally proposed comprehensive backup/validation/failure-stop chain.

Only these existing containers are eligible:

| Container | Initial configured tag | Automatic version range |
| --- | --- | --- |
| homepage | ghcr.io/gethomepage/homepage:v2.4.0 | 2.4.x, stable v-prefixed tags |
| homepage-socket-proxy | lscr.io/linuxserver/socket-proxy:3.4.6 | 3.4.x, plain numeric stable tags |
| homepage-operations-status | python:3.13.17-alpine3.24 | 3.13.x with the alpine3.24 suffix |

Strategies are in stacks/homepage/compose.yaml using explicit com.getarcaneapp.arcane.updater.strategy, .constraint and .tag-pattern service labels. Do not revert them to x-arcane-only metadata: external Docker Compose ignores the extension; Arcane injects equivalent labels only in its own load/deploy path. The former project recheck alone was insufficient validation. Security settings, mounts, networks, resources, worker code and existing healthchecks are unchanged. This updates the status container's Python image, not the bind-mounted homepi-status program.

Explicit tags can receive new image builds through digest changes even without a version increase. Patches can still break behavior; constraints do not classify migration requirements or security severity.

## Arcane settings and evidence

- Running manager v2.17.1 verified by owner inspect output: running, healthy. Its existing Compose still uses latest; v2.17.1 was explicitly pulled and retagged locally before a targeted --pull never update.
- Projects Directory: /opt/homelab/stacks, replacing the unused default /app/data/projects. Owner saw projects after the change.
- Auto Update was initially enabled for 31 October, then disabled during the 1 November label correction. After runtime verification, owner re-enabled/saved it and reported next run in six days (expected 7 November 10:00 CET).
- Exclusions: owner confirmed every container except the three above checked as excluded. Exact persisted list/count: VERIFY ON PI if needed; no API/database export was supplied.
- Update delay: 72 hours, owner-guided configuration. Counts from detection of the target, not its upstream publication date; manual update actions bypass delay.
- Schedule: six-field cron `0 0 9 * * 6`. Arcane has no explicit TZ; official image default is UTC. Saturday 09:00 UTC = 10:00 CET / 11:00 CEST.
- Current configuration is UI state in Arcane's data, not wholly reproduced by the Compose file. Preserve its database backup. Newly added containers are not automatically excluded: review exclusions BEFORE deploying additional services.
- Never use Update All to enforce this restricted automatic scope: manual actions may include excluded services. In particular, leave Gluetun/qBittorrent maintenance to the existing documented procedure.

### First schedule and correction

The 31 October 10:00 CET job completed successfully. Activity said "Checking 3 image references", reported each current reference up to date and found 17 pending image update records. It showed no demonstrated applied update. The success badge and "Applying updates: succeeded" alone do not prove any container changed, nor does this output establish the intended 72-hour deferral.

The earlier project screenshot had found Python 3.13.18-alpine3.24 and proxy 3.4.7, but owner inspect on 1 November showed every running updater label empty. That discrepancy exposed the x-arcane/external-Compose deployment mistake.

A candidate replacing exactly three updater extension blocks with equivalent labels passed native Compose config --quiet. Owner recreated only the three services, using existing images (--pull never) and the shared lock. Compose reported all three Healthy. Owner then inspected runtime labels: all strategies tag; ranges 2.4.x, 3.4.x and 3.13.x; regexes including the Alpine 3.24 suffix correct. No new healthcheck was added to socket-proxy; the Compose summary must not be interpreted as that claim.

After a fresh Image Update Watcher execution, the container list showed Homepage current and proxy/status updates available. Exact new targets were not visible there, and no fixed-policy unattended application, rollback or exhaustive rejection test has been demonstrated. Next inspect the post-fix scheduled run. Delay counts from each target's detection and can restart if the target changes.

### Gmail notifications

Owner configured smtp.gmail.com, port 587, STARTTLS using a dedicated Google app password, and confirmed the provider test email arrived. No address, account credential, app password or Arcane secret was collected or committed. The owner was instructed to enable image-update and container-update notifications; exact persisted event flags are VERIFY ON PI if needed. A provider test verifies mail transport, not every event subscription.

Source inspection at Arcane v2.17.1 (backend/internal/updater/service.go and backend/internal/notification/service.go), with its pinned go.getarcane.app/updater v0.11.13 (updater/container.go, restart.go, types.go), found successful changes routed to the container-update notifier and failures returning before that notifier. Failed-update outcomes are recorded in Arcane activity, but the configured "container updated" subscription is not a general failure alarm. No deliberate production failure or additional monitoring service was introduced.

Source: [Arcane notifier adapter](https://github.com/getarcaneapp/arcane/blob/v2.17.1/backend/internal/updater/service.go), [pinned updater implementation](https://github.com/getarcaneapp/kit/blob/updater/v0.11.13/updater/container.go), [notification type](https://github.com/getarcaneapp/kit/blob/updater/v0.11.13/updater/types.go).

## Backup, concurrency and failure limits

Daily Restic backup at 04:30 Europe/Berlin, monthly maintenance at 05:30 on day one, audio and status workers, and external Healthchecks remain unchanged. Backup success on 27 October 04:31 was owner-evidenced before the Arcane work; do not infer later successful snapshots without checking.

This rollout does not add:
- a fresh backup or backup-success gate immediately before each scheduled update;
- acquisition of /run/lock/homepi-restic.lock by Arcane's scheduled updater;
- a durable global failure stop or guaranteed stop-after-first-failure for a batch;
- application-specific post-update validation or automatic restoration of application data;
- a new Homepage update-status card.

Existing healthchecks cover basic service behavior only; the recorded socket-proxy Compose has no configured Docker healthcheck. Future Arcane updates may overlap a long backup/audio run despite the chosen schedule. The interactive installation steps acquired the shared lock; this does not make Arcane use that lock.

Major/minor versions outside the ranges wait for explicit review and policy changes. Out-of-range releases may be omitted from constrained pending-update results, so review upstream releases periodically; do not promise automatic notification for every excluded version. Urgent security releases may justify a reviewed manual update before the normal delay.

## Recovery material

- Arcane: /root/homepi-arcane-rollback.HSeiC04t/arcane-data-and-compose.tar.gz; the tar was made while Arcane was stopped under the shared lock, then Arcane restarted and passed health. Local old image name homepi-rollback/arcane:2.15.1 retained. Arcane may report a registry-check error for that deliberately local name.
- Homepage stack: /root/homepi-update-policy-rollback.Lm4egmnJ/ contains compose.yaml, compose.candidate.yaml, homepage-config and images-before.tar. The label correction added compose.before-labels.yaml and compose.labels.yaml; the before-labels copy deliberately retains the old missing-runtime-policy bug. The images tar preserves the three prior running image IDs. Retain old config and image identity together; the original latest tags are moving references and cannot alone guarantee rollback.
- Existing earlier status rollback remains /root/homepi-status-rollback.fnhzWRCx.

No rollback drill was performed. Restoring an old Arcane image alone after database migrations is not a safe recovery assumption; restore the matching data copy as needed. Capture current state first and follow the shared-lock/worker coordination when doing recovery. Do not repeat the original operations/install.sh bootstrap on this already installed stack. Its initial installation evidence refers to the historical pinned bundle, not the new version-policy rollout.

## Follow-up

After the first eligible scheduled run: inspect Arcane history, running tags/health, Homepage widgets and all three operations cards. A scheduled execution with no eligible targets is not a failed rollout. Record actual outcomes and synchronize Arcane's modified image references into Git without overwriting a newer runtime version.

References: [Arcane auto updates](https://getarcane.app/docs/docker/auto-updates), [Compose metadata](https://getarcane.app/docs/reference/compose-labels), [v2.17.1 source](https://github.com/getarcaneapp/arcane/tree/v2.17.1).
