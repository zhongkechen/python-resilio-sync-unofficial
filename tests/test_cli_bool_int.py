import sys
import unittest
from unittest.mock import patch

from rslsync.cli import pass_args


class CliBooleanAndIntegerTests(unittest.TestCase):
    def parse(self, *args):
        with patch.object(sys, "argv", ["rsl", *args]):
            return pass_args()

    def test_boolean_flags_keep_their_defaults_and_can_be_disabled(self):
        self.assertIs(self.parse("folder", "list").discovery, True)
        self.assertIs(self.parse("folder", "list", "--discovery").discovery, True)
        self.assertIs(self.parse("folder", "list", "--no-discovery").discovery, False)
        args = self.parse("folder", "add-local", "--origin-folder-id", "example", "--path", "/tmp", "--no-readonly")
        self.assertIs(args.readonly, False)

    def test_zero_and_one_defaults_still_take_integer_values(self):
        args = self.parse("general", "get-history", "--start", "50", "--order", "0")
        self.assertEqual((args.start, args.order), (50, 0))
        self.assertIs(type(args.order), int)

        args = self.parse(
            "folder", "get-link", "--folder-name", "example", "--folder-id", "1",
            "--permission", "2", "--clicklimit", "5",
        )
        self.assertEqual(args.clicklimit, 5)
