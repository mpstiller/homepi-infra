# Matter on HomePi

## Matter backup installation and real run — owner evidence 2026-11-02

This supersedes the preparation-only backup status below.

- Installed baseline SHA256 415d749e771a87148ebdc866d9b1137e20b708c68b318bbb4e7addfc65ac2db9 matched the repository. Guarded installer added only matter-server to CANDIDATES, checked candidate SHA256 0ce674a100f0f9428516e6bb4d72c4372ec02708bd93e0398a54d780b70f7d85 and bash syntax, and retained /root/homepi-matter-backup-rollback.6fxgbvcj. Owner confirmed successful installation.
- Owner started homepi-backup.service. Journal: started 19:45:51 CET, stateful stop 19:45:52, staging 19:45:59, restart of matter-server 19:46:00, upload 19:46:05. Upload reached retention with new snapshot e43eddfa (19:46:06, 417.233 MiB); completed 19:47:13 and systemd Finished/Deactivated successfully at 19:47:14.
- Retention kept 10 snapshots and removed the earlier same-day dc59a3ce entry; this is expected daily retention, not loss of the new snapshot.
- Real backup/staging/restart/upload/retention are evidenced. Owner subsequently confirmed the requested Home Assistant switching/Google Home state test still works after the restart. Exact Matter file presence inside the cloud snapshot and Matter restoration were not separately checked. No new restore claim.
- Remaining: explicit Arcane exclusion confirmation and optional resource measurement. Preserve scheduled audio/Arcane verification dates and private fabric data.

## Matter devices connected — owner evidence 2026-11-02

- Owner installed ghcr.io/matter-js/matterjs-server:1.5.5 (arm64, image user 1000:1000); native Compose validation passed and startup reported Healthy.
- Separate project matter: /opt/homelab/stacks/matter/compose.yaml; data /srv/appdata/matter-server (created owner 1000:1000, mode 0700). Host network, read-only container root, LISTEN_ADDRESS=127.0.0.1 and PRIMARY_INTERFACE=wlan0. Home Assistant 2026.10.0 uses host networking and connected at ws://127.0.0.1:5580/ws.
- Owner output confirmed IPv6 enabled and an IPv6 route via wlan0; this is not a complete network/firewall audit. Before deployment ~1.7 GiB RAM available and 676 MiB swap used; post-start resource use remains unmeasured.
- First Eve Energy was shared from Google Home using a fresh pairing code and Home Assistant iPhone flow: Add Devices -> already in use -> Other controllers. Choosing Google Home led to a help flow without direct code entry; do not repeat that route.
- First device switching and Google Home state were owner-tested successfully. Owner subsequently confirmed all their Matter devices are connected; exact device inventory and individual tests for remaining devices were not supplied. Preserve existing Google Home fabrics; no reset/removal is needed.
- Excluding matter-server from Arcane Auto Update was instructed but not explicitly confirmed: VERIFY ON PI. Keep automatic eligibility limited to the three Homepage containers.
- Existing backup rsync includes the new data/Compose directories, but the installed stop list predates matter-server. This branch adds only matter-server to CANDIDATES; installation and a real consistent snapshot are still pending. Do not claim backup integration complete or restore tested. Fabric data/keys and pairing codes stay private, never Git/chat.
- Next: compare installed backup checksum with the baseline, install the one-line stop-list addition with rollback under the shared lock, and verify a backup and restart. Then capture resource use and optional device inventory. Audio scheduled test 3 November 07:00 CET and Arcane scheduled test 7 November 10:00 CET remain pending.
- Owner also confirmed daily audio Homepage display correct after PR #18 merged; first scheduled daily batch remains pending.


## Operation and recovery

The checked-in Compose mirrors the configuration supplied to and successfully started by the owner. No independent live file checksum capture was performed. The image user was inspected as 1000:1000. Keep the data directory private and writable by that UID/GID; do not recursively change existing data ownership without inspecting it.

Home Assistant connects to the localhost WebSocket endpoint through its host network. The management port does not need LAN exposure. PRIMARY_INTERFACE selects wlan0 for Matter/mDNS while LISTEN_ADDRESS only restricts the management listener. No new Thread border router was installed; successful commissioning is evidence of the current device path, not an inventory of border routers.

Existing Google Home devices should be shared with fresh per-device pairing codes, using Other controllers in the Home Assistant Companion app when the Google Home selection only offers linking instructions. Do not factory-reset working devices. Codes, fabric keys and the contents of /srv/appdata/matter-server must never be committed.

The data folder is covered by the existing /srv/appdata rsync scope, and the Compose folder by /opt/homelab/stacks. A consistent copy additionally requires pausing matter-server during staging. The repository backup patch adds that container to the existing stop/restart list; it does not alter retention, locks, schedules, notification behavior or other candidates. Installation and a real successful backup are now owner-confirmed; see the latest evidence above. The generic script restarts only containers running before the backup. Once added, backup staging briefly interrupts Home Assistant's Matter connection; Google Home has its own fabric.

A restore needs the retained Matter data as well as Home Assistant appdata, the Compose file and independently recoverable backup access. An empty Matter data directory is not equivalent to restoring the existing fabric. No Matter restore or restart drill has been performed. Do not remove this data or existing Google Home fabrics as a troubleshooting shortcut.

## Next validation

1. Completed: baseline checksum comparison, guarded installation and successful real backup/staging/restart/upload/retention.
2. Confirm matter-server is excluded from Arcane Auto Update.
3. Completed: owner confirmed post-backup device switching/Google Home state. Exact Matter snapshot-file inspection and restore remain separate checks. Never print data file contents.
4. Measure steady-state container memory and optionally record device counts/types without pairing secrets.

Sources: https://www.home-assistant.io/integrations/matter/ and https://github.com/matter-js/matterjs-server/blob/v1.5.5/docs/docker.md
