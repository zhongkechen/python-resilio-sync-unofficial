import unittest
from unittest.mock import MagicMock, patch
from urllib.request import HTTPHandler

from rslsync import RslClient


def response(cookie, page):
    result = MagicMock(code=200, msg="OK")
    result.getheader.return_value = cookie
    result.read.return_value = page
    return result


class TokenResponseTests(unittest.TestCase):
    def test_missing_cookie_raises_an_authentication_error(self):
        page = b"<div id='token' hidden>example-token</div>"
        with patch.object(HTTPHandler, "http_open", return_value=response(None, page)):
            with self.assertRaisesRegex(RuntimeError, "missing a session cookie"):
                RslClient("http://localhost:8888", "test", "test")

    def test_missing_token_preserves_the_existing_session(self):
        responses = [
            response("session=old; Path=/", b"<div id='token' hidden>old-token</div>"),
            response("session=new; Path=/", b"<html>Unexpected page</html>"),
        ]
        with patch.object(HTTPHandler, "http_open", side_effect=responses):
            client = RslClient("http://localhost:8888", "test", "test")
            with self.assertRaisesRegex(RuntimeError, "missing an authentication token"):
                client.refresh_token()

        self.assertEqual((client.auth_cookie, client.token), ("session=old", "old-token"))
