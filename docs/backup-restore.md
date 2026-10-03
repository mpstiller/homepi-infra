# Backup and restore

## Current state

A real backup system has **not** been finalized yet.

The old microSD contains a clone from the NVMe migration point, but it is only a stale recovery artifact and should not be treated as a current backup.

## What must be protected

At minimum:

```text
/opt/homelab/stacks
/srv/appdata
```

Plus any irreplaceable household data added later.

## Proposed direction

Evaluate restic or Borg for encrypted, versioned backups to an independent target. The backup target must not be the same NVMe that is being protected.

## Restore principle

A backup is not considered complete until a restore procedure has been tested, especially for Home Assistant and SQLite/database-backed media services.
