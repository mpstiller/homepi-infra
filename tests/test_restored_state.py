"""Check WAL-aware validation, unchanged originals and failure reporting."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'backup/validate-restored-state.py'
spec = importlib.util.spec_from_file_location('validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.restore = Path(self.tmp.name).resolve() / 'restore-validation.fixture'
        self.data = self.restore / 'srv/appdata'
        self.connections = []
        self.addCleanup(lambda: [c.close() for c in self.connections])
        for relative in validator.DATABASES:
            db = self.data / relative
            db.parent.mkdir(parents=True, exist_ok=True)
            c = sqlite3.connect(db)
            c.execute('PRAGMA journal_mode=WAL')
            c.execute('PRAGMA wal_autocheckpoint=0')
            c.execute('CREATE TABLE fixture(value TEXT)')
            c.execute("INSERT INTO fixture VALUES ('private fixture')")
            c.commit()
            self.connections.append(c)
        (self.data/validator.LITEDB).write_bytes(b'non-SQLite presence fixture')
        for app in ('sonarr','radarr','prowlarr'):
            (self.data/app/'config.xml').write_text('<Config><ApiKey>private fixture</ApiKey></Config>')
        storage = self.data/'homeassistant/.storage'; storage.mkdir()
        for name in validator.STORAGE_REQUIRED:
            (storage/name).write_text(json.dumps({'data': {'private': 'fixture'}}))
        (storage/'androidtv_remote_key.pem').write_text('private fixture')
        (self.data/'homeassistant/configuration.yaml').write_text('default_config:\n')
    def run_check(self, root=None):
        return subprocess.run([sys.executable, str(SCRIPT), str(root or self.restore)],
                              capture_output=True,text=True,timeout=30)
    def bytes(self):
        return {str(p.relative_to(self.data)):p.read_bytes()
                for p in self.data.rglob('*') if p.is_file()}
    def test_valid_wal_state_and_source_unchanged(self):
        self.assertTrue(any(self.data.rglob('*-wal')))
        before=self.bytes(); r=self.run_check()
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertEqual(before,self.bytes())
        self.assertNotIn('private fixture',r.stdout+r.stderr)
        self.assertFalse(list(self.restore.parent.glob('restore-db-check.*')))
    def test_litedb_not_opened_as_sqlite(self):
        r=self.run_check(); self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('PENDING: LiteDB integrity/startup',r.stdout)
        self.assertNotIn('SQLite '+validator.LITEDB,r.stdout)
    def test_missing_litedb_fails(self):
        (self.data/validator.LITEDB).unlink()
        r=self.run_check(); self.assertEqual(r.returncode,1)
        self.assertIn('FAIL: PRESENCE LiteDB',r.stdout)
    def test_missing_database_fails(self):
        (self.data/'seerr/db/db.sqlite3').unlink()
        r=self.run_check(); self.assertEqual(r.returncode,1)
        self.assertIn('FAIL: SQLite seerr/db/db.sqlite3',r.stdout)
    def test_bad_json_fails_without_content_leak(self):
        (self.data/'homeassistant/.storage/auth').write_text('secret invalid content')
        r=self.run_check(); self.assertEqual(r.returncode,1)
        self.assertNotIn('secret invalid content',r.stdout+r.stderr)
    def test_database_symlink_rejected(self):
        db=self.data/'seerr/db/db.sqlite3'; db.unlink()
        db.symlink_to(self.data/'sonarr/sonarr.db')
        r=self.run_check(); self.assertEqual(r.returncode,1)
        self.assertIn('FAIL: SQLite seerr/db/db.sqlite3',r.stdout)
    def test_root_symlink_rejected(self):
        link=self.restore.parent/'restore-validation.link'; link.symlink_to(self.restore)
        r=self.run_check(link); self.assertEqual(r.returncode,2)

if __name__=='__main__': unittest.main(verbosity=2)
