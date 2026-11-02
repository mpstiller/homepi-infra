# Matter on HomePi

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

The data folder is covered by the existing /srv/appdata rsync scope, and the Compose folder by /opt/homelab/stacks. A consistent copy additionally requires pausing matter-server during staging. The repository backup patch adds that container to the existing stop/restart list; it does not alter retention, locks, schedules, notification behavior or other candidates. Installation on Pi is pending. The generic script restarts only containers running before the backup. Once added, backup staging briefly interrupts Home Assistant's Matter connection; Google Home has its own fabric.

A restore needs the retained Matter data as well as Home Assistant appdata, the Compose file and independently recoverable backup access. An empty Matter data directory is not equivalent to restoring the existing fabric. No Matter restore or restart drill has been performed. Do not remove this data or existing Google Home fabrics as a troubleshooting shortcut.

## Next validation

1. Owner reports SHA256 of /usr/local/sbin/homepi-backup; compare with repository baseline before a guarded, rollback-backed installation.
2. Confirm matter-server is excluded from Arcane Auto Update.
3. Observe real backup, restart and resulting snapshot inclusion; do not print data file contents.
4. Measure steady-state container memory and optionally record device counts/types without pairing secrets.

Sources: https://www.home-assistant.io/integrations/matter/ and https://github.com/matter-js/matterjs-server/blob/v1.5.5/docs/docker.md
