from __future__ import annotations

import json
import logging
import re
import time
from urllib.parse import urljoin
from base64 import b64encode
import urllib.request


class RslClient:
    def __init__(self, url, username, password, timeout=30):
        self.url = urljoin(url, "gui/")
        self.timeout = timeout
        self.auth_cookie = None
        self.token = None
        self.auth_headers = self._basic_auth_headers(username, password)
        self.refresh_token()

    @staticmethod
    def _basic_auth_headers(username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return {"Authorization": "Basic " + token}

    @staticmethod
    def _current_ts():
        return int(time.time() * 1000)

    @staticmethod
    def _convert_parameter(value):
        return str(value).lower() if isinstance(value, bool) else value

    def refresh_token(self):
        url = urljoin(self.url, "token.html")
        fields = urllib.parse.urlencode({"t": self._current_ts()})
        request = urllib.request.Request(url + "?" + fields, headers=self.auth_headers)
        response = urllib.request.urlopen(request, timeout=self.timeout)
        self.auth_cookie = response.getheader("Set-Cookie").split(";")[0]
        pattern = r"<div id='token' .*>(?P<token>[\w-]+)</div>"
        m = re.search(pattern, response.read().decode("utf-8"))
        if m:
            self.token = m.group('token')
        else:
            raise "Invalid credentials"

    def make_request(self, action, verify=True, **params):
        logging.debug("get: ", action, params)
        headers = {"Cookie": self.auth_cookie, **self.auth_headers}
        params = {key: self._convert_parameter(value) for key, value in params.items()}
        fields = urllib.parse.urlencode({"token": self.token, 'action': action, **params, "t": self._current_ts()})
        request = urllib.request.Request(self.url + "?" + fields, headers=headers)
        response = urllib.request.urlopen(request, timeout=self.timeout)
        j = json.loads(response.read().decode('utf-8'))
        if verify and j.get("status") != 200:
            logging.error(j)
        return j

    @property
    def general(self):
        from rslsync.commands.general import GeneralCommands
        return GeneralCommands(self)

    @property
    def folder(self):
        from rslsync.commands.folder import FolderCommands
        return FolderCommands(self)

    @property
    def file(self):
        from rslsync.commands.file import FileCommands
        return FileCommands(self)


