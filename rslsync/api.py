from __future__ import annotations

import importlib
import json
import logging
import os.path
import pkgutil
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

        if "status" in j:
            del j["status"]

        if len(j.keys()) == 1:
            for i in j.values():
                return i

        return j

    @staticmethod
    def list_commands():
        import rslsync.commands
        for _, command, _ in pkgutil.iter_modules([os.path.dirname(rslsync.commands.__file__)]):
            mod = importlib.import_module("rslsync.commands." + command)
            clazz = getattr(mod, command.capitalize() + "Commands")
            yield command, clazz

    def __getattr__(self, item):
        for command, clazz in self.list_commands():
            if command == item:
                return clazz(self)
