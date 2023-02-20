import logging
from urllib.parse import urljoin
import requests
import time
import re


class RslClient:
    def __init__(self, url, username, password, timeout=30):
        self.url = urljoin(url, "gui/")
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.timeout = timeout
        self.token = self.get_token()

    @staticmethod
    def current_ts():
        return int(time.time() * 1000)

    def get_token(self):
        url = urljoin(self.url, "token.html")
        response = self.session.get(url, params={"t": self.current_ts()}, timeout=self.timeout)
        pattern = r"<div id='token' .*>(?P<token>[\w-]+)</div>"
        m = re.search(pattern, response.content.decode("utf-8"))
        if m:
            return m.group('token')
        raise "Invalid credentials"

    def get_command(self, command, **params):
        logging.debug("get: ", command, params)
        response = self.session.get(
            self.url,
            params={"token": self.token, 'action': command, **params, "t": self.current_ts()},
            timeout=self.timeout,
        )
        j = response.json()
        assert j["status"] == 200
        return j

    def get_shared_folders(self):
        return self.get_command("getsyncfolders", discovery=1)["folders"]

    def share_file(self, file_path, expire_days):
        job_id = self.get_command("addmasterjob")["value"]["id"]
        self.get_command("addpathtojob", path=file_path, id=job_id)
        self.get_command("commitmasterjob", id=job_id)
        self.get_command("setjobttl", id=job_id, ttl=expire_days * 3600 * 24)
        return job_id

    def create_link_for_shared_file(self, share_id):
        return self.get_command("createjoblink", id=share_id)["value"]["link"]

    def unshare_file(self, share_id):
        self.get_command("removejob", id=share_id)

    def get_shared_files(self):
        return self.get_command("getsyncjobs")["value"]["jobs"]

