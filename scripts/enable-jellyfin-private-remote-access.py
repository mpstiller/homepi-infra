#!/usr/bin/env python3
"""Enable Jellyfin's app-level remote flag with private rollback and restart."""
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import tempfile
import time
import urllib.request
import xml.etree.ElementTree as ET

CONFIG = Path('/srv/appdata/jellyfin/config/config/network.xml')


def revised(text):
    root = ET.fromstring(text)
    field = root.find('EnableRemoteAccess')
    if field is None or field.text != 'false':
        raise ValueError('Expected EnableRemoteAccess=false; review current config')
    result, count = re.subn(r'<EnableRemoteAccess>\s*false\s*</EnableRemoteAccess>',
                           '<EnableRemoteAccess>true</EnableRemoteAccess>', text)
    if count != 1 or ET.fromstring(result).findtext('EnableRemoteAccess') != 'true':
        raise ValueError('Unexpected network XML')
    return result


def docker(*args):
    result = subprocess.run(['docker', *args], text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=90)
    if result.returncode:
        raise RuntimeError('Docker command failed')
    return result.stdout.strip()


def atomic_write(path, content, metadata):
    fd, name = tempfile.mkstemp(prefix='.homepi-network.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            os.fchmod(handle.fileno(), stat.S_IMODE(metadata.st_mode))
            os.fchown(handle.fileno(), metadata.st_uid, metadata.st_gid)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if Path(name).exists():
            Path(name).unlink()


def main():
    if os.geteuid() != 0:
        raise RuntimeError('Run with sudo python3 on HomePi')
    os.umask(0o077)
    with open('/run/lock/homepi-restic.lock', 'a') as lock:
        print('Waiting for backup/maintenance lock...', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        if CONFIG.is_symlink() or CONFIG.resolve() != CONFIG:
            raise RuntimeError('Unexpected network configuration path')
        original = CONFIG.read_bytes()
        changed_text = revised(original.decode('utf-8')).encode('utf-8')
        metadata = CONFIG.stat()
        if docker('inspect', '-f', '{{.State.Running}}', 'jellyfin') != 'true':
            raise RuntimeError('Jellyfin was not running; no change made')
        rollback = Path(tempfile.mkdtemp(prefix='homepi-jellyfin-network-rollback.', dir='/root'))
        shutil.copy2(CONFIG, rollback/'network.xml')
        print('Rollback copy:', rollback/'network.xml', flush=True)
        changed = False
        restart_needed = False
        success = False
        try:
            restart_needed = True
            docker('stop', '--time', '60', 'jellyfin')
            # Refuse edits that appeared after our snapshot of the file.
            if CONFIG.read_bytes() != original:
                raise RuntimeError('Config changed during shutdown; review before retry')
            changed = True
            atomic_write(CONFIG, changed_text, metadata)
            docker('start', 'jellyfin')
            network = ET.fromstring(changed_text)
            port = network.findtext('InternalHttpPort', '8096')
            base = network.findtext('BaseUrl', '') or ''
            if not port.isdecimal():
                raise ValueError('Unexpected HTTP port')
            url = ('http://127.0.0.1:' + port + '/' + base.strip('/')).rstrip('/')
            url += '/System/Info/Public'
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                try:
                    with opener.open(url, timeout=5) as response:
                        data = json.load(response)
                        if response.status == 200 and data.get('Version'):
                            success = True
                            break
                except (OSError, ValueError):
                    pass
                time.sleep(2)
            if not success:
                raise RuntimeError('Jellyfin local startup check timed out')
            print('OK: EnableRemoteAccess=true; other settings unchanged')
            print('OK: local server-info API HTTP 200')
            print('Next: validate the Mac Tailscale request. No router/Tailscale policy changes made.')
            return 0
        finally:
            if not success:
                print('Change did not complete; attempting recovery.', flush=True)
                # Finish recovery if a second catchable signal arrives.
                signal.signal(signal.SIGINT, signal.SIG_IGN)
                signal.signal(signal.SIGTERM, signal.SIG_IGN)
                if changed:
                    docker('stop', '--time', '60', 'jellyfin')
                    atomic_write(CONFIG, original, metadata)
                if restart_needed:
                    docker('start', 'jellyfin')
                print('Recovery attempted; rollback copy retained at:', rollback/'network.xml')


if __name__ == '__main__':
    def terminate(signum, frame):
        raise SystemExit(128 + signum)
    signal.signal(signal.SIGTERM, terminate)
    try:
        raise SystemExit(main())
    except Exception as error:
        print('ERROR:', str(error))
        raise SystemExit(1)
