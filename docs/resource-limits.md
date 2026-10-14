# Docker memory-controller support

Resolved and owner-verified on 2026-10-14. Docker now reports RAM and swap limits supported. No per-service memory caps were assigned and enforcement under memory pressure was not tested.

## Diagnosis and applied change

Before the fix, Docker used cgroup v2 with the systemd driver but reported RAM/swap-limit support=false. `/sys/fs/cgroup/cgroup.controllers` contained `cpuset cpu io pids`; active boot arguments included `cgroup_disable=memory`. The boot partition was `/boot/firmware`, mounted from `/dev/nvme0n1p1` as vfat.

Raspberry Pi [maintainer guidance](https://github.com/raspberrypi/linux/issues/6980) explains that device-tree boot arguments can supply the disable flag and a later `cgroup_enable=memory` in `cmdline.txt` overrides it. The legacy `cgroup_memory=1` argument is unnecessary. See also the [kernel parameter documentation](https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html).

`scripts/enable-memory-cgroup.py` appended only `cgroup_enable=memory` to the existing single-line `/boot/firmware/cmdline.txt`. It checks the Pi architecture/kernel, boot mount and custom boot configuration, preserves existing argument bytes, creates a unique rollback copy and verifies the replacement. It defaults to a read-only preview; `--apply` writes without rebooting automatically. Five local tests cover byte/newline preservation, override ordering, idempotence and rejection of invalid lines.

Owner applied the helper at 16:14 CEST. Retained original:

`/boot/firmware/cmdline.txt.before-memory-cgroup.20261014T161422+0200.t2g80tm6`

## Post-reboot validation

After the owner's normal reboot:

- Root controllers: `cpuset cpu io memory pids`.
- Docker: `RAM-Limits: true | Swap-Limits: true`.
- All 13 containers were running, with approximately four minutes uptime.
- Homepage, Jellyfin, Arcane and Gluetun had healthy configured healthchecks; the other containers were running without a healthcheck result.

This confirms controller availability and Docker support. It does not prove an application's behavior under an assigned cap or memory pressure. The earlier image-inventory JSON intentionally retains its pre-fix flags.

The earlier disable flag may still precede the later enable override in `/proc/cmdline`. Absence of memory in legacy `/proc/cgroups` alone is not a failure criterion on this cgroup-v2 kernel; check the root controller list and Docker flags.

## Rollback and further work

If rollback is needed, restore the retained original to `/boot/firmware/cmdline.txt` and activate it through a normal reboot. Before a planned reboot check that backup/maintenance services are idle; do not manually stop containers with `unless-stopped` restart policies.

Future per-service caps require measured usage and a service-specific budget. Gluetun image pinning and backup failure/staleness visibility remain separate roadmap tasks.
