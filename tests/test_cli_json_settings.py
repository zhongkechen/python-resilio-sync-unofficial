import sys
import unittest
from unittest.mock import patch

from rslsync import RslClient, cli


class CliJsonSettingsTests(unittest.TestCase):
    def test_passes_json_settings_as_request_parameters(self):
        settings = '{"example": false}'
        cases = [
            (["general", "set-settings", "--settings", settings], "setsettings", {}),
            (["general", "set-advanced-settings", "--settings", settings], "setadvancedsettings", {}),
            (
                ["folder", "set-preferences", "--name", "test", "--secret", "example", "--preferences", settings],
                "setfolderpref",
                {"name": "test", "secret": "example"},
            ),
        ]
        for args, action, params in cases:
            with self.subTest(action=action):
                with patch.object(sys, "argv", ["rsl", *args]), patch.object(RslClient, "refresh_token"):
                    with patch.object(RslClient, "make_request", return_value=None) as request:
                        cli.main()
                request.assert_called_once_with(action, **params, example=False)

    def test_library_still_accepts_mappings(self):
        with patch.object(RslClient, "refresh_token"):
            client = RslClient("http://localhost:8888", "test", "test")
        with patch.object(RslClient, "make_request") as request:
            client.general.set_settings({"example": False})
        request.assert_called_once_with("setsettings", example=False)
