# Installed Backup V1 capture — 2026-10-14

These six files were supplied by the owner from the Pi on 2026-10-14. They represent the installed configuration, not a newly deployed hardened version. The user's combined script output starts with `homepi-backup` and then `homepi-restic-maintenance`; filenames are identified by the corresponding service ExecStart and script behavior.

- `bin/` maps to `/usr/local/sbin/` (installed scripts should be root-owned, mode 0700).
- `systemd/` maps to `/etc/systemd/system/` (root-owned units, mode 0644).
- All four units have no drop-ins according to the owner's `systemctl show` output.
- Password/rclone files are referenced by path only and are not included.
- Preserve this capture while reviewing hardening; do not deploy it as an improvement merely because it is now in Git.

## Confirmed behavior

Only previously running candidate containers are stopped. `rsync -aHAX` stages appdata and stacks with cache/log exclusions; services restart before cloud upload. Automatic snapshots use 7 daily / 4 weekly / 6 monthly retention. Retention uses restic's default grouping because no `--group-by` is specified.

## Review findings and next correction

1. `docker start ... || true` masks restart errors. The explicit restart clears `RUNNING` and removes the EXIT trap even when restart failed. A snapshot can be uploaded and the service reported successful while an application remains stopped. Correct by tracking failed restarts individually, retaining them for EXIT cleanup and returning a failing status; verify that previously running containers are running before upload. The EXIT handler should preserve the original failure and report cleanup failure. Handle catchable termination explicitly; no shell trap can recover from SIGKILL or power loss.
2. There is no shared backup/maintenance lock. `After=homepi-backup.service` supplies systemd ordering, not mutual exclusion for every scheduled/manual invocation. Correct by acquiring the same exclusive `flock` in both scripts before any work, e.g. FD 9 on `/run/lock/homepi-restic.lock`; retain it through staging/upload/retention or prune/check. Waiting is preferable to silently skipping a scheduled backup. Validate availability of `flock` on the Pi and exercise the contention path before deployment.
3. Scripts, units, the restic password and rclone config live outside the protected source trees. The first two are now captured here; password and OAuth recovery still require independent secret storage. Do not add secret values to Git.
4. `gluetun` is not a stopped candidate, although all of `/srv/appdata` is copied. VERIFY ON PI: whether its persisted files change during staging and whether they matter for recovery. Do not change the VPN boundary to resolve this without evidence.
5. Staging uses the same NVMe and retains local plaintext appdata/.env copies. Google Drive is the independent encrypted repository. VERIFY ON PI: staging permissions and free-space headroom.

Review source for ordering: [systemd.unit](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml). Lock interface: [util-linux flock manual](https://man7.org/linux/man-pages/man1/flock.1.html).

Next: apply and validate the small locking/restart correction separately, then carry out the temporary restore procedure in `docs/restore-runbook.md`. Capturing these files does not mark hardening or application recovery complete.
