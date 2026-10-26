import importlib.machinery
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.machinery.SourceFileLoader('operations', str(ROOT/'operations/homepi-status'))
spec = importlib.util.spec_from_loader(loader.name, loader)
ops = importlib.util.module_from_spec(spec)
loader.exec_module(ops)

NOW = 1793023200.0
A, B = 'a'*32, 'b'*32
PATH = '/srv/data/media/tv/Test/Season 01/Episode 02.mkv'


def worker(at, message, ident=A):
    return {'__REALTIME_TIMESTAMP': str(int(at*1e6)), 'MESSAGE': message,
            '_SYSTEMD_INVOCATION_ID': ident}


def manager(at, kind, event, ident=A):
    return {'__REALTIME_TIMESTAMP': str(int(at*1e6)), 'UNIT': ops.JOBS[kind][0]+'.service',
            'INVOCATION_ID': ident, 'MESSAGE_ID': {
                'start': '7d4958e842da4a758f6c1cdc7b36dcc5',
                'success': '39f53479d3a045ac8e11786248231fbf',
                'failure': 'be02cf6855d2428ba40df7e9d022f03d'}[event]}


def service(active=False, start=0, end=0, ident=''):
    def stamp(at):
        return ops.datetime.fromtimestamp(at, ops.timezone.utc).strftime('%a %Y-%m-%d %H:%M:%S UTC') if at else ''
    return {'LoadState': 'loaded', 'ActiveState': 'activating' if active else 'inactive',
            'Result': 'success', 'ExecMainStatus': '0', 'InvocationID': ident,
            'ExecMainStartTimestamp': stamp(start), 'ExecMainExitTimestamp': stamp(end)}


def summary(kind, rows, meta=None, old=None, timer=None):
    return ops.summarize(kind, meta or service(), timer or {'ActiveState': 'active'}, rows, old or {}, NOW)


class OperationsTests(unittest.TestCase):
    def test_live_audio_title_and_elapsed(self):
        rows = [worker(NOW-120, f'PLAN: {PATH}; 2 TrueHD track(s) -> AC3; original not archived')]
        value = summary('audio', rows, service(True, NOW-120, ident=A))
        self.assertEqual(value['status'], 'Läuft')
        self.assertEqual(value['detail'], 'Episode 02.mkv')
        self.assertEqual(value['duration'], '2 min 00 s (bisher)')

    def test_successful_conversion_and_duration(self):
        rows = [manager(NOW-120, 'audio', 'start'),
                worker(NOW-119, f'PLAN: {PATH}; 2 TrueHD track(s) -> AC3; original not archived'),
                worker(NOW-1, f'REPLACED: {PATH}; original archive: disabled'),
                manager(NOW, 'audio', 'success')]
        value = summary('audio', rows)
        self.assertEqual(value['status'], 'Bereit')
        self.assertEqual(value['duration'], '2 min 00 s')
        self.assertEqual(value['last_success']['outcome'], 'converted')

    def test_refresh_failure_after_replacement_is_failure(self):
        rows = [worker(NOW-5, f'REPLACED: {PATH}; original archive: disabled'),
                worker(NOW-2, 'FAILED: Jellyfin API HTTP 401: POST /Library/Refresh'),
                manager(NOW, 'audio', 'failure')]
        value = summary('audio', rows)
        self.assertEqual(value['status'], 'Fehler')
        self.assertIsNone(value['last_success'])

    def test_deferred_is_not_failed(self):
        for message in ['DEFER: Jellyfin has a playing/paused session',
                        'DEFER: backup/maintenance/audio lock is busy',
                        f'DEFER: file younger than five minutes: {PATH}']:
            value = summary('audio', [worker(NOW, message)])
            self.assertEqual(value['status'], 'Zurückgestellt')
            self.assertEqual(value['error'], 'Keiner erfasst')

    def test_backup_snapshot_not_enough_for_success(self):
        value = summary('backup', [worker(NOW-5, 'snapshot b37715a7 saved'),
                                   manager(NOW, 'backup', 'failure')])
        self.assertEqual(value['snapshot'], 'b37715a7')
        self.assertEqual(value['status'], 'Fehler')
        self.assertIsNone(value['last_success'])

    def test_historical_failure_from_systemd_without_script_error(self):
        rows = [manager(NOW-200, 'maintenance', 'start'),
                worker(NOW-190, 'Checking repository integrity...'),
                worker(NOW-180, 'error: secret https://example.invalid/token'),
                manager(NOW-170, 'maintenance', 'failure'),
                manager(NOW-100, 'maintenance', 'start', B),
                worker(NOW-90, '=== HomePi restic maintenance completed: now ===', B),
                manager(NOW-80, 'maintenance', 'success', B)]
        value = summary('maintenance', rows)
        self.assertEqual(value['status'], 'Bereit')
        self.assertIn('fehlgeschlagen', value['error'])
        self.assertNotIn('secret', json.dumps(value))
        self.assertNotIn('https://', json.dumps(value))

    def test_idle_audio_poll_without_worker_logs(self):
        value = summary('audio', [manager(NOW-10, 'audio', 'start'),
                                  manager(NOW, 'audio', 'success')])
        self.assertEqual(value['records'][0]['outcome'], 'idle')
        self.assertIsNone(value['last_success'])

    def test_no_data_never_claims_success(self):
        value = summary('backup', [])
        self.assertIn('Unbekannt', value['status'])
        self.assertEqual(value['success'], 'Noch nicht erfasst')

    def test_overdue_thresholds(self):
        for kind in ops.JOBS:
            value = summary(kind, [manager(NOW-ops.JOBS[kind][1]-1, kind, 'success')])
            self.assertIn('Überfällig', value['status'])

    def test_disabled_timer_visible(self):
        value = summary('audio', [worker(NOW, 'DEFER: lock is busy')], timer={'ActiveState': 'inactive'})
        self.assertEqual(value['status'], 'Zeitplan inaktiv')

    def test_replaying_journal_is_idempotent(self):
        rows = [manager(NOW-50, 'audio', 'start'), worker(NOW-40, f'PLAN: {PATH}; 2 tracks'),
                worker(NOW-5, f'REPLACED: {PATH}; original archive: disabled'),
                manager(NOW, 'audio', 'success')]
        first = summary('audio', rows)
        second = summary('audio', rows, old=first)
        self.assertEqual(first, second)

    def test_last_success_survives_more_than_50_idle_polls(self):
        old = summary('audio', [worker(NOW-1000, f'REPLACED: {PATH}; original archive: disabled')])
        for i in range(60):
            ident = f'{i+10:032x}'
            old = summary('audio', [manager(NOW-60+i, 'audio', 'start', ident),
                                    manager(NOW-59+i, 'audio', 'success', ident)], old=old)
        self.assertEqual(len(old['records']), 50)
        self.assertEqual(old['last_success']['detail'], 'Episode 02.mkv')

    def test_latest_systemd_status_overrides_missing_journal(self):
        meta = service(False, NOW-100, NOW, A)
        meta['Result'], meta['ExecMainStatus'] = 'exit-code', '1'
        self.assertEqual(summary('backup', [], meta)['status'], 'Fehler')

    def test_inactive_invocation_id_missing_correlates(self):
        value = summary('audio', [worker(NOW-90, 'DEFER: Jellyfin has a playing/paused session')],
                        service(False, NOW-100, NOW))
        self.assertEqual(len(value['records']), 1)
        self.assertEqual(value['status'], 'Zurückgestellt')

    def test_freshness_computed_when_served_not_frozen_at_collection(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'status.json'
            ops.atomic_write(path, {'generated': NOW, 'updated': ops.date(NOW),
                                   'jobs': {'audio': summary('audio', [])}})
            self.assertEqual(ops.response(path, 'audio', NOW+60)['freshness'], 'Aktuell')
            self.assertIn('veraltet', ops.response(path, 'audio', NOW+121)['status'])
            self.assertIn('veraltet', ops.response(path, 'audio', NOW-10)['status'])
            self.assertNotIn('records', ops.response(path, 'audio', NOW))
            self.assertEqual(path.stat().st_mode & 0o777, 0o644)

    def test_collect_failure_keeps_last_complete_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'status.json'
            ops.atomic_write(path, {'generated': NOW})
            with patch.object(ops, 'show', side_effect=RuntimeError('unavailable')):
                with self.assertRaises(RuntimeError):
                    ops.collect(path)
            self.assertEqual(json.loads(path.read_text()), {'generated': NOW})

    def test_command_is_read_only_and_no_raw_fields(self):
        with patch.object(ops, 'command', return_value='') as mock:
            self.assertEqual(ops.journal('homepi-audio.service'), [])
            args = mock.call_args.args[0]
            self.assertIn('--lines=4000', args)
            self.assertIn('--since=45 days ago', args)

    def test_unrecognized_lines_and_outside_paths_not_published(self):
        for message in ['Authorization: MediaBrowser Token="secret"',
                        'FAILED: https://example.invalid/secret',
                        'PLAN: /etc/secret.mkv; 2 tracks']:
            event = ops.interpret(message, 'audio')
            self.assertNotIn('secret', json.dumps(event))

    def test_incomplete_historical_run_is_unknown(self):
        value = summary('backup', [worker(NOW-1, 'Uploading snapshot to Google Drive...')])
        self.assertIn('Laufabschluss fehlt', value['status'])

    def test_http_routes_freshness_and_unavailable_data(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'status.json'
            ops.atomic_write(path, {'generated': NOW, 'updated': ops.date(NOW),
                                   'jobs': {'audio': summary('audio', [])}})
            server = ops.make_server(path, 0)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = f'http://127.0.0.1:{server.server_port}'
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            try:
                with patch.object(ops.time, 'time', return_value=NOW+180):
                    with opener.open(url+'/audio.json', timeout=2) as res:
                        self.assertEqual(res.headers['Cache-Control'], 'no-store')
                        self.assertIn('veraltet', json.load(res)['status'])
                for route in ['/../status.json', '/etc/passwd', '/audio.json?x=1']:
                    with self.assertRaises(urllib.error.HTTPError) as error:
                        opener.open(url+route, timeout=2)
                    self.assertEqual(error.exception.code, 404)
                path.unlink()
                with self.assertRaises(urllib.error.HTTPError) as error:
                    opener.open(url+'/audio.json', timeout=2)
                self.assertEqual(error.exception.code, 503)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)


if __name__ == '__main__':
    unittest.main()
