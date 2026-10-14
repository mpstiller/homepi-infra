"""Verify boot-line preservation and explicit override ordering."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('change',ROOT/'scripts/enable-memory-cgroup.py')
change=importlib.util.module_from_spec(spec);spec.loader.exec_module(change)

class MemoryBootTests(unittest.TestCase):
    def test_preserves_all_original_bytes_except_append(self):
        original=b'console=tty1  root=PARTUUID=fixture-02 rootfstype=ext4 rootwait\n'
        self.assertEqual(change.proposed(original),original[:-1]+b' cgroup_enable=memory\n')
    def test_idempotent_enabled_override(self):
        original=b'root=fixture cgroup_enable=memory\n'
        self.assertEqual(change.proposed(original),original)
    def test_disable_after_enable_gets_final_override(self):
        original=b'root=fixture cgroup_enable=memory cgroup_disable=memory,cpu\n'
        self.assertTrue(change.proposed(original).endswith(b' cgroup_enable=memory\n'))
    def test_multiline_empty_and_nul_refused(self):
        for data in (b'',b'\n',b'root=fixture\nconsole=tty1\n',b'root=fi\0xture\n'):
            with self.assertRaises(ValueError):change.proposed(data)
    def test_crlf_and_no_newline_preserved(self):
        for ending in (b'\r\n',b''):
            original=b'root=fixture'+ending
            self.assertEqual(change.proposed(original),b'root=fixture cgroup_enable=memory'+ending)

if __name__=='__main__':unittest.main(verbosity=2)
