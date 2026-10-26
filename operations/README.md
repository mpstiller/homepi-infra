# Homepage operations status (prepared, not installed)

Three German `customapi` list cards show backup, monthly maintenance and audio state.
The host collector reads systemd properties and allowlisted journald events every
30 seconds. Homepage polls an internal JSON server every 15 seconds. No cloud/API
credentials are needed, and existing backup/audio programs, timers and Healthchecks
notifications are unchanged. This adds a small Python stdlib container, not a
general monitoring stack. It has a 64 MiB cap, no host port, no Docker socket,
no privileges and read-only mounts of the collector script and generated data only.

## What is shown

- Running/ready/deferred/failed/missing/overdue/inactive timer, current phase or
  media basename, latest run, last successful backup or conversion, duration,
  next timer date, historical last error, latest three runs and collection time.
- Backup snapshot ID is shown separately: a snapshot alone does **not** imply that
  subsequent retention or the overall service succeeded.
- Audio successful idle polls do not erase the last conversion. Playback, shared
  lock and file-age deferrals are separate from errors. A failure after REPLACED
  (for example library refresh) marks that invocation failed.
- Time is rendered in Europe/Berlin. Realtime next-trigger dates can be absent
  during monotonic audio timers: `Nach Laufende / unbekannt` is intentional.
- The HTTP server recalculates freshness for every request. After 120 seconds
  without a complete collection it overrides status with `Unbekannt: Statusdaten
  veraltet`. Missing/invalid data is HTTP 503. Unknown log history stays unknown.
- Overdue thresholds are 30 hours for backup, 35 days for maintenance and 20
  minutes for the audio polling service; these are visibility heuristics, not
  replacements for the external scheduled Healthchecks alarms.

## History and limits

At each collection, at most the last 4000 journal records per service from 45 days
are read. systemd invocation IDs group events; stable unit lifecycle message IDs
and latest service Result/exit status capture failures without exposing raw error
bodies. Only known script markers/phases, a validated media basename and a hex
snapshot ID are published. API keys, Healthchecks URLs and raw stderr are never
copied into status. Error details remain in the root-readable service journals.
The Homepage customapi widget does not support conditional block highlighting;
states are explicit text rather than a promised red/green traffic light.

`/srv/appdata/homepi-status/status.json` atomically retains 50 invocation records
per service plus the last success/error beyond that window. Initial import is
limited by journal retention. Runs older than retained journals cannot be
reconstructed. Independently executed shell/manual runs outside these systemd
units are not included. This is operational visibility, not an exhaustive audit
log or a proof of backup restorability. No backlog scan/probe/conversion is started
by collecting status. Overlapping journal/service reads may briefly show the
previous state until the next refresh.

## Install after review / pinned download

Use a new temporary directory on the Pi for an exact, reviewed repository commit.
Do not use a moving `main` download or overwrite an existing working checkout.
Check the downloaded archive's published SHA256 before extraction/execution.
The guided chat steps will provide the pinned URL/hash after PR review.

From the extracted repository root:

```bash
sudo bash operations/install.sh
```

The installer refuses unexpected changes to the owner-supplied live Compose and
services hashes, or to the captured settings baseline. It also refuses an existing
status installation, validates the payload manifest and Compose syntax, and pulls
only the new `python:3.13-alpine` image. An update of that image is a separate
maintenance action; this initial upstream tag follows the current repository's
tag-based convention. It takes the shared nonblocking backup/audio lock before
installation; if busy, wait for that job to finish and retry. No worker is stopped.

The three existing config files are saved under a printed root-only
`/root/homepi-status-rollback.*` path. Existing `.env`, API placeholders, socket
proxy, other widgets and other containers are retained. The collector is installed
and a complete first read must succeed before publishing the widgets. Only the
Homepage and new status container are recreated; existing images are not pulled.

## Verify on Pi (pending)

```bash
sudo systemctl status homepi-status.service homepi-status.timer --no-pager
sudo journalctl -u homepi-status.service -n 10 --no-pager
sudo docker exec homepage-operations-status python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8080/audio.json').read().decode())"
```

For a completed oneshot collector, `inactive (dead)` with successful exit is
normal; its timer should be active. Open Homepage and inspect all three cards.
Verify current phase/filename during an existing run, historical errors/last
success against service journals and elapsed/next-run fields. Do not deliberately
fail a production backup/conversion to test the cards. Native Docker Compose,
systemd timestamp formatting, journald fields and actual Homepage rendering need
owner execution: local mocked tests cannot prove these interfaces on the Pi.

## Rollback

Use the exact printed rollback path as `ROLLBACK_DIR` below. This restores only
the three reviewed Homepage config files. Do not remove unrelated restore tests,
backups or audio archives.

```bash
sudo systemctl disable --now homepi-status.timer
sudo systemctl stop homepi-status.service
sudo cp -a "$ROLLBACK_DIR/compose.yaml" /opt/homelab/stacks/homepage/compose.yaml
sudo cp -a "$ROLLBACK_DIR/services.yaml" /srv/appdata/homepage/services.yaml
sudo cp -a "$ROLLBACK_DIR/settings.yaml" /srv/appdata/homepage/settings.yaml
sudo docker rm -f homepage-operations-status
sudo docker compose --project-directory /opt/homelab/stacks/homepage -f /opt/homelab/stacks/homepage/compose.yaml up -d --no-deps --pull never homepage
```

Disabled collector files/status can remain for inspection. Removal or updates
should be reviewed separately; re-running the initial installer intentionally
refuses this partially installed state.

## Local checks

`python3 -m unittest discover -s tests -p test_operations.py -v` covers running,
success, failure after replacement, deferral, snapshot-before-failure, historical
manager failures, idle runs, overdue/inactive timers, replay/deduplication,
retention across 60 idle polls, missing invocation IDs, stale/absent HTTP data,
route restrictions and atomic publication. No production API requests are sent.
YAML structure and systemd units are checked locally with only the collector
ExecStart path replaced by `/usr/bin/true` for verification.
