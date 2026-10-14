#!/usr/bin/env python3
"""Start one network-isolated Sonarr from a disposable restored-state copy."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import sqlite3
import subprocess
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET

IMAGE = 'sha256:f247545d23ba8b233d6604575347e48a623fe6ad75dda02348bf81917f3b5c06'


def docker(*args, input=None, timeout=30):
    result = subprocess.run(['docker', *args], input=input, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=timeout)
    if result.returncode:
        raise RuntimeError('Docker command failed; output withheld to protect credentials')
    return result.stdout


def available_memory():
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemAvailable:'):
            return int(line.split()[1]) * 1024
    raise RuntimeError('Cannot determine available memory')


def run_arguments(name, config, uid, gid):
    return ['run', '-d', '--pull=never', '--name', name,
            '--label', 'homepi.restore-test=sonarr', '--network', 'none',
            '--restart', 'no', '--env', 'PUID=' + uid, '--env', 'PGID=' + gid,
            '--env', 'TZ=Europe/Berlin', '--mount',
            'type=bind,src=' + str(config) + ',dst=/config', IMAGE]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('restore_directory', type=Path)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error('Run with sudo python3 on HomePi')
    root = args.restore_directory.absolute()
    if root != root.resolve(strict=True) or not root.name.startswith('restore-validation.'):
        parser.error('Use the actual restore-validation.* directory')
    source = root / 'srv/appdata/sonarr'
    for p in (root/'srv', root/'srv/appdata', source):
        if p.is_symlink() or not p.is_dir():
            parser.error('Unexpected source path')
    if available_memory() < 1024**3:
        parser.error('Less than 1 GiB available RAM; defer this test')
    if docker('inspect', '-f', '{{.Image}}', 'sonarr').strip() != IMAGE:
        parser.error('Live Sonarr image changed; review before testing')
    env = json.loads(docker('inspect', '-f', '{{json .Config.Env}}', 'sonarr'))
    selected = dict(x.split('=', 1) for x in env if x.startswith(('PUID=', 'PGID=')))
    uid, gid = selected.get('PUID'), selected.get('PGID')
    if not uid or not gid or not uid.isdecimal() or not gid.isdecimal():
        parser.error('Cannot verify live PUID/PGID')

    work = Path(tempfile.mkdtemp(prefix='restore-startup-sonarr.', dir=root.parent))
    name = 'homepi-restore-sonarr-' + uuid.uuid4().hex[:12]
    attempted = False
    success = False
    print('Temporary test directory:', work, flush=True)
    print('Test has no network, published ports, media or Docker socket mounts.', flush=True)
    try:
        config = work/'config'
        shutil.copytree(source, config, symlinks=True)
        for p in [config, *config.rglob('*')]:
            if p.is_symlink():
                raise RuntimeError('Symlink in restored config; review before testing')
            os.chown(p, int(uid), int(gid))
        xml = ET.parse(config/'config.xml').getroot()
        key = xml.findtext('ApiKey')
        port = xml.findtext('Port', '8989')
        base = xml.findtext('UrlBase', '') or ''
        if not key or '\n' in key or '\r' in key or not port.isdecimal():
            raise RuntimeError('Unexpected API configuration')
        url = 'http://127.0.0.1:' + port + '/' + base.strip('/')
        url = url.rstrip('/') + '/api/v3'
        db = sqlite3.connect((config/'sonarr.db').as_uri() + '?mode=rw', uri=True)
        try:
            expected_ids = {row[0] for row in db.execute('SELECT Id FROM Series')}
        finally:
            db.close()
        attempted = True
        docker(*run_arguments(name, config, uid, gid))

        def api(path):
            # Header is passed on stdin, not printed or put in command arguments.
            body = docker('exec', '-i', name, 'curl', '-fsS', '--max-time', '5',
                          '--header', '@-', url + path,
                          input='X-Api-Key: ' + key + '\n', timeout=10)
            return json.loads(body)

        deadline = time.monotonic() + 120
        status = None
        while time.monotonic() < deadline:
            if available_memory() < 384 * 1024**2:
                raise RuntimeError('Low available RAM; stopping test')
            if docker('inspect', '-f', '{{.State.Running}}', name).strip() != 'true':
                raise RuntimeError('Test container exited during startup')
            try:
                status = api('/system/status')
                if isinstance(status, dict) and status.get('version'):
                    break
            except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired):
                pass
            time.sleep(2)
        else:
            raise RuntimeError('Startup API timed out')
        series = api('/series')
        if not isinstance(series, list) or {s['id'] for s in series} != expected_ids:
            raise RuntimeError('Restored API series IDs differ from database')
        print('OK: Sonarr startup/API, version', status['version'])
        print('OK: restored series IDs match; count =', len(expected_ids))
        print('NOTE: login UI, media playback and download integrations are not tested.')
        success = True
    except Exception as error:
        print('FAIL:', type(error).__name__, '(details withheld; private test logs may help)')
    finally:
        if attempted:
            try:
                logs = docker('logs', name)
                log = work/'private-startup.log'
                log.write_text(logs)
                log.chmod(0o600)
            except Exception:
                pass
            # Remove only the unique test container, including on failures/signals.
            try:
                docker('rm', '-f', name)
                print('Test container removed.')
            except Exception:
                print('ERROR: cleanup required for test container:', name)
                success = False
        if success:
            shutil.rmtree(work)
            print('Disposable test copy removed. Original restore and live Sonarr unchanged.')
        else:
            print('Private test files retained at:', work)
    return 0 if success else 1


if __name__ == '__main__':
    def terminate(signum, frame):
        raise SystemExit(128 + signum)
    signal.signal(signal.SIGTERM, terminate)
    raise SystemExit(main())
