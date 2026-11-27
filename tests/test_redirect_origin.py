import io
import unittest
from email.message import Message
from urllib.error import HTTPError
from urllib.request import Request

from rslsync.api import _SameOriginRedirectHandler


class RedirectOriginTests(unittest.TestCase):
    def redirect(self, destination):
        handler = _SameOriginRedirectHandler()
        request = Request("https://sync.example/gui/", headers={"Authorization": "Basic example"})
        return handler.redirect_request(request, io.BytesIO(), 302, "Found", Message(), destination)

    def test_allows_the_same_origin_with_the_default_port(self):
        redirected = self.redirect("https://SYNC.example:443/gui/index.html")
        self.assertEqual(redirected.full_url, "https://SYNC.example:443/gui/index.html")
        self.assertEqual(redirected.get_header("Authorization"), "Basic example")

    def test_rejects_a_change_of_scheme_host_or_port(self):
        destinations = [
            "http://sync.example/gui/",
            "https://other.example/gui/",
            "https://sync.example:8443/gui/",
        ]
        for destination in destinations:
            with self.subTest(destination=destination):
                with self.assertRaisesRegex(HTTPError, "refused a cross-origin redirect"):
                    self.redirect(destination)
