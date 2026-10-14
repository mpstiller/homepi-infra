#!/usr/bin/env python3
"""Validate a restored HomePi tree using a disposable copy, never live appdata."""
import argparse
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import xml.etree.ElementTree as ET

DATABASES = (
    'arcane/arcane.db', 'arcane/arcane.francis.db',
    'homeassistant/home-assistant_v2.db',
    'jellyfin/config/data/jellyfin.db',
    'music-assistant/auth.db', 'music-assistant/library.db',
    'prowlarr/prowlarr.db', 'prowlarr/logs.db',
    'radarr/radarr.db', 'radarr/logs.db',
    'seerr/db/db.sqlite3', 'sonarr/sonarr.db', 'sonarr/logs.db',
)
LITEDB = 'jellyfin/config/data/kodisyncqueue.db'
STORAGE_REQUIRED = ('auth', 'core.config', 'core.config_entries',
                    'core.device_registry', 'core.entity_registry')


def regular_file(base, relative):
    """Reject symlinks at every level, including parent directories."""
    target = base
    for part in Path(relative).parts:
        target = target / part
        if target.is_symlink():
            raise ValueError('symlink')
    if not target.is_file():
        raise ValueError('missing file')
    return target


def validate(source):
    failures = 0
    checks = 0

    def check(label, function):
        nonlocal checks, failures
        checks += 1
        try:
            function()
            print('OK:', label)
        except Exception as error:
            failures += 1
            # Avoid printing database/config contents or exception messages.
            print('FAIL:', label, '(' + type(error).__name__ + ')')

    for relative in DATABASES:
        def database(relative=relative):
            path = regular_file(source, relative)
            with path.open('rb') as handle:
                if handle.read(16) != b'SQLite format 3\0':
                    raise ValueError('not SQLite')
            # Use normal WAL-aware SQLite on a copy; never immutable mode.
            connection = sqlite3.connect(path.as_uri() + '?mode=rw', uri=True,
                                         timeout=10)
            try:
                result = connection.execute('PRAGMA integrity_check').fetchall()
                if result != [('ok',)]:
                    raise ValueError('integrity failure')
            finally:
                connection.close()
        check('SQLite ' + relative, database)

    # Kodi Sync Queue uses LiteDB, not SQLite. Presence is not integrity proof.
    def litedb_presence():
        if regular_file(source, LITEDB).stat().st_size == 0:
            raise ValueError('empty LiteDB file')
    check('PRESENCE LiteDB ' + LITEDB, litedb_presence)
    print('PENDING: LiteDB integrity/startup ' + LITEDB)

    for app in ('sonarr', 'radarr', 'prowlarr'):
        relative = app + '/config.xml'
        check('XML ' + relative,
              lambda relative=relative: ET.parse(regular_file(source, relative)))

    storage = source / 'homeassistant/.storage'
    if not storage.is_dir() or storage.is_symlink() or storage.parent.is_symlink():
        checks += 1; failures += 1
        print('FAIL: Home Assistant .storage directory')
    else:
        # Include missing critical state files as failures, not zero-check success.
        names = {p.name for p in storage.iterdir() if p.name != '.'}
        for name in sorted(names | set(STORAGE_REQUIRED)):
            if name.endswith('.pem'):
                print('SKIP: PEM credential file', name, '(not parsed)')
                continue
            relative = 'homeassistant/.storage/' + name
            def storage_json(relative=relative):
                path = regular_file(source, relative)
                data = json.loads(path.read_text())
                if not isinstance(data, dict):
                    raise ValueError('unexpected JSON root')
            check('JSON ' + relative, storage_json)

    check('PRESENCE homeassistant/configuration.yaml',
          lambda: regular_file(source, 'homeassistant/configuration.yaml'))
    print('NOTE: LiteDB integrity, YAML syntax, PEM validity, application startup and device access are not tested.')
    print(f'Summary: {checks} checks, {failures} failures')
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('restore_directory', type=Path)
    args = parser.parse_args()
    supplied = args.restore_directory.absolute()
    root = supplied.resolve(strict=True)
    # Refuse production paths and indirect/symlink targets.
    if supplied != root or not root.name.startswith('restore-validation.'):
        parser.error('Use an actual restore-validation.* directory, not a symlink or live path.')
    source = root / 'srv/appdata'
    if source.is_symlink() or (root / 'srv').is_symlink() or not source.is_dir():
        parser.error('Expected non-symlink srv/appdata below the restore directory.')
    print('Validating restored state on a disposable copy; source remains unchanged.')
    with tempfile.TemporaryDirectory(prefix='restore-db-check.', dir=root.parent) as temporary:
        copy = Path(temporary) / 'appdata'
        shutil.copytree(source, copy, symlinks=True)
        return validate(copy)


if __name__ == '__main__':
    raise SystemExit(main())
