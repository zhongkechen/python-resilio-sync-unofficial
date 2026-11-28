import sys
import unittest
from unittest.mock import patch

from rslsync import RslClient, cli


class FileExpiryTests(unittest.TestCase):
    def test_cli_passes_numeric_seconds(self):
        argv = ["rsl", "file", "add", "--file-path", "/example.txt", "--expire-days", "3"]
        responses = [{"id": "example"}, {}, {}, {}]
        with patch.object(sys, "argv", argv), patch.object(RslClient, "refresh_token"):
            with patch.object(RslClient, "make_request", side_effect=responses) as request:
                cli.main()

        request.assert_called_with("setjobttl", id="example", ttl=259200)

    def test_invalid_expiry_does_not_create_a_share(self):
        with patch.object(RslClient, "refresh_token"):
            client = RslClient("http://localhost:8888", "test", "test")
        with patch.object(RslClient, "make_request") as request:
            with self.assertRaises(ValueError):
                client.file.add("/example.txt", "invalid")

        request.assert_not_called()
