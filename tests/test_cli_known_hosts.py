import sys
import unittest
from unittest.mock import patch

from rslsync import RslClient, cli


class CliKnownHostsTests(unittest.TestCase):
    def test_repeated_options_keep_complete_addresses(self):
        hosts = ["first.example:1234", "second.example:4567"]
        for command, id_option in [("file", "--job-id"), ("folder", "--folder-id")]:
            with self.subTest(command=command):
                argv = [
                    "rsl", command, "set-known-hosts", id_option, "example",
                    "--known-hosts", hosts[0], "--known-hosts", hosts[1],
                ]
                with patch.object(sys, "argv", argv), patch.object(RslClient, "refresh_token"):
                    with patch.object(RslClient, "make_request", return_value=None) as request:
                        cli.main()
                request.assert_called_once_with(
                    "setknownhosts", id="example", isfolder=command == "folder", hosts=",".join(hosts)
                )
