"""Verify the one-field edit preserves security settings and unknown XML."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('change',ROOT/'scripts/enable-jellyfin-private-remote-access.py')
change=importlib.util.module_from_spec(spec);spec.loader.exec_module(change)

class RemoteConfigTests(unittest.TestCase):
    def test_only_remote_flag_changes(self):
        original='<NetworkConfiguration>\n  <EnableRemoteAccess>false</EnableRemoteAccess>\n  <EnableUPnP>false</EnableUPnP><LocalNetworkSubnets />\n  <KnownProxies /><RemoteIPFilter /><IsRemoteIPFilterBlacklist>false</IsRemoteIPFilterBlacklist>\n</NetworkConfiguration>\n'
        self.assertEqual(change.revised(original),original.replace('<EnableRemoteAccess>false</EnableRemoteAccess>','<EnableRemoteAccess>true</EnableRemoteAccess>'))
    def test_rejects_already_enabled_or_missing(self):
        for original in ['<Config><EnableRemoteAccess>true</EnableRemoteAccess></Config>','<Config/>']:
            with self.assertRaises(ValueError):change.revised(original)
    def test_duplicate_field_rejected(self):
        with self.assertRaises(ValueError):change.revised('<Config><EnableRemoteAccess>false</EnableRemoteAccess><EnableRemoteAccess>false</EnableRemoteAccess></Config>')

if __name__=='__main__':unittest.main(verbosity=2)
