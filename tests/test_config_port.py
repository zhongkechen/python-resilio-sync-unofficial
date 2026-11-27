import unittest

from rslsync.cli import build_url


class ConfigPortTests(unittest.TestCase):
    def test_accepts_a_numeric_port_from_json(self):
        self.assertEqual(build_url("sync.example", 8080), "http://sync.example:8080")

    def test_preserves_default_and_string_ports(self):
        self.assertEqual(build_url(None, None), "http://localhost:8888")
        self.assertEqual(build_url("sync.example", "8080"), "http://sync.example:8080")
