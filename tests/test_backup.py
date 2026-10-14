"""Exercise recovery/serialization without Docker, restic, credentials or network.

The flock shim uses the host kernel advisory lock on inherited FD 9; the actual
util-linux executable and systemd activation must also be validated on the Pi.
"""
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOCK = '''#!/usr/bin/env python3
import fcntl, json, os, sys, time
from pathlib import Path
root=Path(os.environ['MOCK_ROOT'])
name=Path(sys.argv[0]).name
args=sys.argv[1:]
if name=='flock':
    fcntl.flock(int(args[-1]), fcntl.LOCK_EX)
    sys.exit(0)
with (root/'events').open('a') as f: f.write(name+' '+ ' '.join(args)+'\\n')
mode=os.environ.get('MOCK_MODE','success')
if name=='docker':
    state=json.loads((root/'state').read_text())
    if args[0]=='info': sys.exit(1 if mode=='docker_down' else 0)
    if args[0]=='inspect':
        container=args[-1]
        if container not in state: sys.exit(1)
        if '-f' in args: print('true' if state[container] else 'false')
    elif args[0]=='stop':
        for c in args[3:]: state[c]=False
        (root/'state').write_text(json.dumps(state))
    elif args[0]=='start':
        c=args[1]
        if mode=='restart_fail' and c=='homeassistant': sys.exit(1)
        if mode=='restart_once' and c=='homeassistant' and not (root/'failed_once').exists():
            (root/'failed_once').touch(); sys.exit(1)
        state[c]=not (mode=='not_running' and c=='homeassistant')
        (root/'state').write_text(json.dumps(state))
elif name=='rsync':
    if mode=='rsync_fail': sys.exit(23)
    if mode=='terminate':
        (root/'rsync_ready').touch()
        time.sleep(0.3)
    if mode=='hold':
        (root/'rsync_ready').touch()
        while not (root/'release').exists(): time.sleep(0.02)
'''

class BackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root/'bin'; self.bin.mkdir()
        for cmd in ('docker', 'rsync', 'restic', 'flock'):
            f=self.bin/cmd; f.write_text(MOCK); f.chmod(0o755)
        (self.root/'state').write_text(json.dumps({'homeassistant': True, 'sonarr': True, 'radarr': False}))
        (self.root/'events').touch()
        self.env={**os.environ, 'MOCK_ROOT': str(self.root)}
        for name in ('homepi-backup','homepi-restic-maintenance'):
            s=(ROOT/'backup/bin'/name).read_text()
            s=s.replace('export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', f'export PATH="{self.bin}:/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"')
            s=s.replace('/run/lock/homepi-restic.lock', str(self.root/'lock'))
            s=s.replace('/srv/backups/restic-staging', str(self.root/'stage'))
            (self.root/name).write_text(s)
    def run_backup(self, mode='success'):
        return subprocess.run(['bash',str(self.root/'homepi-backup')],env={**self.env,'MOCK_MODE':mode},capture_output=True,text=True,timeout=10)
    def events(self): return (self.root/'events').read_text()
    def state(self): return json.loads((self.root/'state').read_text())
    def test_success_restarts_before_upload_leaves_stopped_alone(self):
        r=self.run_backup(); self.assertEqual(r.returncode,0,r.stderr)
        e=self.events(); self.assertLess(e.index('docker start sonarr'),e.index('restic '))
        self.assertNotIn('docker start radarr', e)
        self.assertEqual(self.state(),{'homeassistant':True,'sonarr':True,'radarr':False})
        self.assertIn('forget --tag automatic --keep-daily 7 --keep-weekly 4 --keep-monthly 6',e)
    def test_staging_failure_recovers_and_preserves_error(self):
        r=self.run_backup('rsync_fail'); self.assertEqual(r.returncode,23,r.stderr)
        self.assertTrue(self.state()['homeassistant']); self.assertTrue(self.state()['sonarr'])
        self.assertNotIn('restic ',self.events())
    def test_restart_failure_is_not_success(self):
        r=self.run_backup('restart_fail'); self.assertEqual(r.returncode,1,r.stderr)
        self.assertTrue(self.state()['sonarr']); self.assertFalse(self.state()['homeassistant'])
        self.assertNotIn('restic ',self.events()); self.assertIn('still require recovery',r.stderr)
    def test_exit_retries_only_failed_container(self):
        r=self.run_backup('restart_once'); self.assertEqual(r.returncode,1,r.stderr)
        self.assertTrue(self.state()['homeassistant']); self.assertTrue(self.state()['sonarr'])
        self.assertEqual(self.events().count('docker start sonarr'),1)
        self.assertEqual(self.events().count('docker start homeassistant'),2)
        self.assertNotIn('restic ',self.events())
    def test_start_success_but_not_running_fails(self):
        r=self.run_backup('not_running'); self.assertEqual(r.returncode,1,r.stderr)
        self.assertNotIn('restic ',self.events())
    def test_unavailable_docker_aborts_before_staging(self):
        r=self.run_backup('docker_down'); self.assertNotEqual(r.returncode,0)
        self.assertNotIn('rsync ',self.events()); self.assertNotIn('docker stop',self.events())
    def wait_file(self,name):
        until=time.monotonic()+5
        while not (self.root/name).exists():
            if time.monotonic()>until: self.fail('timed out waiting for '+name)
            time.sleep(0.02)
    def spawn(self,name,mode):
        p=subprocess.Popen(['bash',str(self.root/name)],env={**self.env,'MOCK_MODE':mode},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        self.addCleanup(lambda: p.kill() if p.poll() is None else None)
        return p
    def test_term_recovers_and_returns_signal_status(self):
        p=self.spawn('homepi-backup','terminate'); self.wait_file('rsync_ready')
        p.send_signal(signal.SIGTERM); self.assertEqual(p.wait(timeout=5),143)
        self.assertTrue(self.state()['homeassistant']); self.assertTrue(self.state()['sonarr'])
        self.assertNotIn('restic ',self.events())
    def test_maintenance_waits_for_backup_lock(self):
        b=self.spawn('homepi-backup','hold'); self.wait_file('rsync_ready')
        m=self.spawn('homepi-restic-maintenance','success'); time.sleep(0.2)
        self.assertIsNone(m.poll()); self.assertNotIn('restic ',self.events())
        (self.root/'release').touch()
        self.assertEqual(b.wait(timeout=5),0); self.assertEqual(m.wait(timeout=5),0)
        e=self.events(); self.assertLess(e.index('forget --tag'),e.index(' prune'))
        self.assertLess(e.index(' prune'),e.index(' check'))

if __name__=='__main__': unittest.main(verbosity=2)
