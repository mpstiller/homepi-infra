#!/usr/bin/env python3
"""Append Raspberry Pi memory-cgroup override; preserve single-line boot args."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile

CMDLINE = Path('/boot/firmware/cmdline.txt')
CONFIG = Path('/boot/firmware/config.txt')


def proposed(data):
    text = data.decode('utf-8')
    if '\0' in text or len(text.splitlines()) != 1 or not text.strip():
        raise ValueError('Expected exactly one nonempty kernel-command-line line')
    # Only append an override; never rewrite root, console or other boot arguments.
    last_memory_action = None
    for token in text.split():
        if token.startswith(('cgroup_enable=', 'cgroup_disable=')):
            key, values = token.split('=', 1)
            if 'memory' in values.split(','):
                last_memory_action = key
    if last_memory_action == 'cgroup_enable':
        return data
    newline = b'\r\n' if data.endswith(b'\r\n') else b'\n' if data.endswith(b'\n') else b''
    body = data[:-len(newline)] if newline else data
    return body + b' cgroup_enable=memory' + newline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write after checks; never reboot')
    args = parser.parse_args()
    if platform.machine() != 'aarch64' or 'rpt' not in platform.release():
        parser.error('This helper is for the verified Raspberry Pi OS/kernel host')
    if CMDLINE.is_symlink() or CMDLINE.resolve() != CMDLINE:
        parser.error('Unexpected command-line path; review before editing')
    mount = subprocess.check_output(['findmnt', '-n', '-T', str(CMDLINE),
                                     '-o', 'TARGET,FSTYPE'], text=True).split()
    if mount != ['/boot/firmware', 'vfat']:
        parser.error('Unexpected boot mount; no edit made')
    config = CONFIG.read_text()
    if re.search(r'^\s*(?:(?:cmdline|os_prefix)\s*=|include\s+)', config, re.M):
        parser.error('Custom boot-config filename/prefix/include requires review')
    original = CMDLINE.read_bytes()
    updated = proposed(original)
    if updated == original:
        print('Already configured: last file-level memory override enables it.')
        print('Runtime activation still requires boot/controller verification.')
        return 0
    print('Planned change: append cgroup_enable=memory to the existing single line.')
    print('All existing root/NVMe/console and other arguments are preserved.')
    if not args.apply:
        print('Read-only preview complete. Run with --apply to write; no reboot is automatic.')
        return 0
    if os.geteuid() != 0:
        parser.error('Use sudo python3 with --apply')
    suffix = datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%z')
    fd, backup_name = tempfile.mkstemp(prefix='cmdline.txt.before-memory-cgroup.' + suffix + '.', dir=CMDLINE.parent)
    os.close(fd)
    backup = Path(backup_name)
    shutil.copyfile(CMDLINE, backup)
    with backup.open('rb+') as handle:
        os.fsync(handle.fileno())
    print('Rollback copy:', backup)
    fd, temporary_name = tempfile.mkstemp(prefix='.cmdline-memory.', dir=CMDLINE.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
        if CMDLINE.read_bytes() != original:
            raise RuntimeError('Boot file changed during preparation; no replacement made')
        os.replace(temporary_name, CMDLINE)
        if CMDLINE.read_bytes() != updated:
            shutil.copyfile(backup, CMDLINE)
            raise RuntimeError('Write verification failed; original restored')
    finally:
        if Path(temporary_name).exists():
            Path(temporary_name).unlink()
    print('OK: boot file updated; activation after next normal reboot.')
    print('No reboot, Docker restart, image pull or service-limit change performed.')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        print('ERROR:', type(error).__name__, str(error))
        raise SystemExit(1)
