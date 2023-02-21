from __future__ import annotations

import json
import logging
from urllib.parse import urljoin
import urllib3
import time
import re


class RslClient:
    def __init__(self, url, username, password, timeout=30):
        self.url = urljoin(url, "gui/")
        self.auth_headers = urllib3.make_headers(basic_auth=f"{username}:{password}")
        self.timeout = timeout
        self.auth_cookie = None
        self.token = None
        self.authenticate()

    @staticmethod
    def _current_ts():
        return int(time.time() * 1000)

    @staticmethod
    def _convert_parameter(value):
        return str(value).lower() if isinstance(value, bool) else value

    def authenticate(self):
        url = urljoin(self.url, "token.html")
        fields = {"t": self._current_ts()}
        response = urllib3.PoolManager().request("GET", url, headers=self.auth_headers, fields=fields, timeout=self.timeout)
        self.auth_cookie = response.headers["Set-Cookie"].split(";")[0]
        pattern = r"<div id='token' .*>(?P<token>[\w-]+)</div>"
        m = re.search(pattern, response.data.decode("utf-8"))
        if m:
            self.token = m.group('token')
        else:
            raise "Invalid credentials"

    def make_request(self, action, verify=True, **params):
        logging.debug("get: ", action, params)
        headers = {"Cookie": self.auth_cookie, **self.auth_headers}
        params = {key: self._convert_parameter(value) for key, value in params.items()}
        fields = {"token": self.token, 'action': action, **params, "t": self._current_ts()}
        response = urllib3.PoolManager().request("GET", self.url, headers=headers, fields=fields, timeout=self.timeout)
        j = json.loads(response.data.decode('utf-8'))
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


