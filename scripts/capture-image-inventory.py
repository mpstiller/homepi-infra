#!/usr/bin/env python3
"""Read-only HomePi image inventory; prints selected metadata, never env/secrets."""
from datetime import datetime
import json
from pathlib import Path
import platform
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET

CONTAINER_TEMPLATE = '''{"name":{{json .Name}},"imageReference":{{json .Config.Image}},"imageId":{{json .Image}},"status":{{json .State.Status}},"health":{{if .State.Health}}{{json .State.Health.Status}}{{else}}null{{end}},"startedAt":{{json .State.StartedAt}},"restartCount":{{json .RestartCount}}}'''
IMAGE_TEMPLATE = '''{"id":{{json .Id}},"repoDigests":{{json .RepoDigests}},"architecture":{{json .Architecture}},"os":{{json .Os}},"created":{{json .Created}},"versionLabel":{{json (index .Config.Labels "org.opencontainers.image.version")}},"buildVersionLabel":{{json (index .Config.Labels "build_version")}}}'''


def command(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.DEVNULL,
                                   timeout=20).strip()


def get_version(value):
    if isinstance(value, str) and re.fullmatch(r'[vV]?\d[\w.+-]{0,60}', value):
        return value
    raise ValueError('not a version string')


def http_json(url, key=None):
    headers = {'Accept': 'application/json'}
    if key:
        headers['X-Api-Key'] = key
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(urllib.request.Request(url, headers=headers), timeout=5) as response:
        return json.load(response)


def app_version(name):
    if name in ('sonarr', 'radarr', 'prowlarr'):
        ports = {'sonarr': 8989, 'radarr': 7878, 'prowlarr': 9696}
        xml = ET.parse('/srv/appdata/' + name + '/config.xml').getroot()
        key = xml.findtext('ApiKey')
        if not key:
            raise ValueError('missing key')
        prefix = '/api/v1' if name == 'prowlarr' else '/api/v3'
        base = xml.findtext('UrlBase', '') or ''
        url = ('http://127.0.0.1:' + str(ports[name]) + '/' + base.strip('/')).rstrip('/')
        return get_version(http_json(url + prefix + '/system/status', key)['version']), 'local status API'
    if name == 'jellyfin':
        return get_version(http_json('http://127.0.0.1:8096/System/Info/Public')['Version']), 'local public server-info API'
    if name == 'homeassistant':
        v = command('docker', 'exec', name, 'python3', '-B', '-c',
                    'from homeassistant.const import __version__; print(__version__)')
        return get_version(v), 'installed Python version constant'
    if name == 'qbittorrent':
        v = command('docker', 'exec', 'gluetun', 'wget', '-qO-',
                    'http://127.0.0.1:8080/api/v2/app/version')
        return get_version(v), 'local qBittorrent version API via Gluetun'
    return None, 'not queried; image metadata only'


def capture():
    report = {'capturedAt': datetime.now().astimezone().isoformat(),
              'kernel': platform.release(), 'hostArchitecture': platform.machine(),
              'readOnly': True, 'containers': [], 'errors': []}
    for field, args in (
        ('dockerVersion', ('docker', 'version', '--format', '{{.Server.Version}}')),
        ('composeVersion', ('docker', 'compose', 'version', '--short')),
    ):
        try:
            report[field] = command(*args)
        except Exception as error:
            report['errors'].append({'scope': field, 'type': type(error).__name__})
    try:
        report['dockerResourceSupport'] = json.loads(command(
            'docker', 'info', '--format',
            '{"memoryLimit":{{json .MemoryLimit}},"swapLimit":{{json .SwapLimit}}}'))
    except Exception as error:
        report['errors'].append({'scope': 'dockerResourceSupport', 'type': type(error).__name__})
    memory = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key, value = line.split(':', 1)
        if key in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
            memory[key + 'KiB'] = int(value.strip().split()[0])
    report['hostMemory'] = memory
    images = {}
    names = command('docker', 'ps', '-a', '--format', '{{.Names}}').splitlines()
    for name in sorted(names):
        try:
            row = json.loads(command('docker', 'inspect', '--type', 'container',
                                     '--format', CONTAINER_TEMPLATE, name))
            row['name'] = row['name'].lstrip('/')
            image_id = row['imageId']
            if image_id not in images:
                images[image_id] = json.loads(command('docker', 'image', 'inspect',
                                                     '--format', IMAGE_TEMPLATE, image_id))
            image = images[image_id]
            row['repoDigests'] = image.get('repoDigests') or []
            for key in ('architecture', 'os', 'created', 'versionLabel', 'buildVersionLabel'):
                row['image' + key[0].upper() + key[1:]] = image.get(key)
            # Only local tag comparison: no registry requests or image pulls.
            try:
                tag_id = command('docker', 'image', 'inspect', '--format', '{{.Id}}', row['imageReference'])
                row['localReferenceMatchesRunningImage'] = tag_id == image_id
            except Exception:
                row['localReferenceMatchesRunningImage'] = None
            row['appVersion'] = None
            if row['status'] == 'running':
                try:
                    row['appVersion'], row['appVersionSource'] = app_version(name)
                except Exception as error:
                    row['appVersionSource'] = 'unavailable (' + type(error).__name__ + ')'
            else:
                row['appVersionSource'] = 'not queried: container is not running'
            report['containers'].append(row)
        except Exception as error:
            report['errors'].append({'scope': name, 'type': type(error).__name__})
    return report


if __name__ == '__main__':
    try:
        print(json.dumps(capture(), indent=2, ensure_ascii=False))
    except Exception as error:
        # No command stdout/stderr, URLs, headers or config text in error output.
        print(json.dumps({'fatalError': type(error).__name__}))
        raise SystemExit(1)
