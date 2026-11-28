import sys
import unittest
from unittest.mock import patch

from rslsync.cli import pass_args


class CliOptionalDefaultsTests(unittest.TestCase):
    def parse_send_stat(self, *args):
        argv = ["rsl", "stat", "send-stat", "--event-name", "example", "--event-action", "test", *args]
        with patch.object(sys, "argv", argv):
            return pass_args()

    def test_extra_can_be_omitted(self):
        self.assertIsNone(self.parse_send_stat().extra)

    def test_extra_can_be_supplied(self):
        self.assertEqual(self.parse_send_stat("--extra", '{"enabled": true}').extra, '{"enabled": true}')
