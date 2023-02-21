from __future__ import annotations

from rslsync import RslClient


class GeneralCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def check_new_version(self):
        return self.client.make_request("checknewversion")["version"]

    def get_folder_settings(self):
        return self.client.make_request("getfoldersettings", verify=False)

    def get_advanced_settings(self):
        return self.client.make_request("advancedsettings")["value"]

    def set_settings(self, settings):
        return self.client.make_request("setsettings", **settings)

    def apply_license_link(self, link):
        return self.client.make_request("applylicenselink", link=link)

    def get_statuses(self):
        return self.client.make_request("getstatuses")

    def get_events(self):
        """long polling API to get notifications"""
        return self.client.make_request("events")

    def get_history(self, start=0, length=1):
        return self.client.make_request("history", start=start, length=length)["value"]
