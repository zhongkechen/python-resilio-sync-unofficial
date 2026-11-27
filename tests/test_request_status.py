import json
import unittest
from unittest.mock import Mock, patch
from urllib.request import HTTPHandler

from rslsync import RslClient, RslRequestError


def response(payload):
    return Mock(code=200, msg="OK", read=Mock(return_value=json.dumps(payload).encode()))


class RequestStatusTests(unittest.TestCase):
    def setUp(self):
        with patch.object(RslClient, "refresh_token"):
            self.client = RslClient("http://localhost:8888", "test", "test")
        self.client.auth_cookie = "session=test"
        self.client.token = "test"

    def test_status_failures_raise_with_action_and_status(self):
        with patch.object(HTTPHandler, "http_open", return_value=response({"status": 500})):
            with self.assertRaises(RslRequestError) as error:
                self.client.make_request("setsettings")

        self.assertEqual(error.exception.action, "setsettings")
        self.assertEqual(error.exception.status, 500)

    def test_preserves_payloads_without_status_and_with_verification_disabled(self):
        cases = [
            ({"status": 200, "value": [1, 2]}, True, [1, 2]),
            ({"value": [1, 2]}, True, [1, 2]),
            ({"status": 404, "value": "missing"}, False, "missing"),
        ]
        for payload, verify, expected in cases:
            with self.subTest(payload=payload, verify=verify):
                with patch.object(HTTPHandler, "http_open", return_value=response(payload)):
                    self.assertEqual(self.client.make_request("test", verify=verify), expected)

    def test_file_add_reports_ttl_failure(self):
        responses = [
            response({"status": 200, "value": {"id": "example"}}),
            response({"status": 200}),
            response({"status": 200}),
            response({"status": 500}),
        ]
        with patch.object(HTTPHandler, "http_open", side_effect=responses):
            with self.assertRaises(RslRequestError) as error:
                self.client.file.add("/example.txt", 3)

        self.assertEqual(error.exception.action, "setjobttl")
