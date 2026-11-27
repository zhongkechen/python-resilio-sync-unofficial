import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from rslsync import RslClient, cli


class CliOutputTests(unittest.TestCase):
    def run_command(self, result):
        output = io.StringIO()
        argv = ["rsl", "general", "get-settings"]
        with patch.object(sys, "argv", argv), patch.object(RslClient, "refresh_token"):
            with patch.object(RslClient, "make_request", return_value=result), redirect_stdout(output):
                self.assertIsNone(cli.main())
        return output.getvalue()

    def test_prints_structured_result(self):
        self.assertEqual(self.run_command({"enabled": True}), '{"enabled": true}\n')

    def test_prints_string_without_json_quotes(self):
        self.assertEqual(self.run_command("share-id"), "share-id\n")

    def test_empty_result_is_quiet(self):
        self.assertEqual(self.run_command(None), "")
