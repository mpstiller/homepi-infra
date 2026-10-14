"""Exercise isolated test lifecycle with a fake Docker API, never real containers."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('startup',ROOT/'backup/test-sonarr-restore.py')
startup=importlib.util.module_from_spec(spec); spec.loader.exec_module(startup)

class StartupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.restore=Path(self.tmp.name).resolve()/'restore-validation.fixture'
        self.config=self.restore/'srv/appdata/sonarr'; self.config.mkdir(parents=True)
        (self.config/'config.xml').write_text('<Config><ApiKey>private-fixture-key</ApiKey><Port>8989</Port></Config>')
        c=sqlite3.connect(self.config/'sonarr.db');c.execute('CREATE TABLE Series(Id INTEGER)');c.execute('INSERT INTO Series VALUES(7)');c.commit();c.close()
        self.events=[];self.ids=[7];self.rm_fail=False
    def docker(self,*args,input=None,timeout=30):
        self.events.append((args,input))
        if args[0]=='inspect':
            if args[2]=='{{.Image}}':return startup.IMAGE
            if args[2]=='{{json .Config.Env}}':return json.dumps(['PUID=1000','PGID=1000'])
            return 'true'
        if args[0]=='exec':
            self.assertNotIn('private-fixture-key',' '.join(args))
            if args[-1].endswith('/system/status'):return json.dumps({'version':'test'})
            return json.dumps([{'id':n} for n in self.ids])
        if args[0]=='rm' and self.rm_fail:raise RuntimeError('mock removal failure')
        return ''
    def run_test(self,mem=2*1024**3):
        output=io.StringIO()
        with patch.object(sys,'argv',['test',str(self.restore)]),patch.object(startup.os,'geteuid',return_value=0),patch.object(startup.os,'chown'),patch.object(startup,'available_memory',return_value=mem),patch.object(startup,'docker',side_effect=self.docker),contextlib.redirect_stdout(output):
            result=startup.main()
        return result,output.getvalue()
    def test_success_isolated_and_source_unchanged(self):
        before=(self.config/'sonarr.db').read_bytes();result,out=self.run_test()
        self.assertEqual(result,0,out);self.assertEqual(before,(self.config/'sonarr.db').read_bytes())
        run=next(args for args,_ in self.events if args[0]=='run')
        self.assertEqual(run[run.index('--network')+1],'none');self.assertEqual(run[-1],startup.IMAGE)
        self.assertNotIn('--publish',run);self.assertNotIn('/var/run/docker.sock',' '.join(run));self.assertNotIn('dst=/data',' '.join(run))
        self.assertTrue(any(a[0]=='rm' for a,_ in self.events));self.assertFalse(list(self.restore.parent.glob('restore-startup-sonarr.*')))
        self.assertNotIn('private-fixture-key',out)
    def test_state_mismatch_fails_and_cleans_container(self):
        self.ids=[8];result,out=self.run_test();self.assertEqual(result,1,out)
        self.assertTrue(any(a[0]=='rm' for a,_ in self.events))
        self.assertTrue(list(self.restore.parent.glob('restore-startup-sonarr.*')))
    def test_cleanup_failure_not_success(self):
        self.rm_fail=True;result,out=self.run_test();self.assertEqual(result,1,out)
        self.assertIn('cleanup required',out)
    def test_low_memory_prevents_start(self):
        with self.assertRaises(SystemExit):self.run_test(mem=512*1024**2)
        self.assertFalse(any(a[0]=='run' for a,_ in self.events))

if __name__=='__main__':unittest.main(verbosity=2)
