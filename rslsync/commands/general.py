from __future__ import annotations

import json

from rslsync import RslClient


class GeneralCommands:
    """General commands"""

    def __init__(self, client: RslClient):
        self.client = client

    def check_new_version(self):
        """Check for the new version of Resilio Sync"""
        return self.client.make_request("checknewversion")

    def get_version(self):
        """Get the current version of the server"""
        return self.client.make_request("version")

    def get_advanced_settings(self):
        """Get advanced settings"""
        return self.client.make_request("advancedsettings")

    def set_advanced_settings(self, settings):
        """Set advanced settings"""
        return self.client.make_request("setadvancedsettings", **settings)

    def get_settings(self):
        """Get settings"""
        return self.client.make_request("settings")

    def set_settings(self, settings):
        """Set settings"""
        return self.client.make_request("setsettings", **settings)

    def apply_license_link(self, link):
        return self.client.make_request("applylicenselink", link=link)

    def get_license_info(self):
        """Get the current license"""
        return self.client.make_request("getlicenseinfo")

    def get_license_agreed(self):
        """Get the features enabled by the current license"""
        return self.client.make_request("licenseagreed")

    def get_events(self):
        """long polling API to get what happened"""
        return self.client.make_request("events")

    def get_history(self, start=0, length=1000, order=1):
        return self.client.make_request("history", startid=start, length=length, order=order)

    def get_mf_devices(self):
        return self.client.make_request("getmfdevices")

    def get_system_info(self):
        """Get system info of the server"""
        return self.client.make_request("getsysteminfo")

    def get_app_info(self):
        """Get server application info"""
        return self.client.make_request("getappinfo")

    def get_user_lang(self):
        return self.client.make_request("userlang")

    def get_local_storage(self):
        return json.loads(self.client.make_request("localstorage"))

    def set_local_storage(self, local_storage: str):
        return self.client.make_request("setlocalstorage", status=200, value=local_storage)

    def get_md_local_storage(self):
        return json.loads(self.client.make_request("mdlocalstorage"))

    def get_master_folder(self):
        return self.client.make_request("getmasterfolder")

    def get_user_identity(self):
        return self.client.make_request("useridentity")

    def get_scheduler(self):
        return self.client.make_request("getscheduler")

    def get_pause(self):
        """Get the current server pause state"""
        return self.client.make_request("pause")

    def set_pause(self, pause=True):
        """Set the server pause state"""
        return self.client.make_request("pause", allowed=True, value=pause)

    def get_debug_mode(self):
        return self.client.make_request("debugmode")

    def get_proxy_settings(self):
        """Get proxy settings"""
        return self.client.make_request("proxysettings")

    def get_credentials(self):
        """Get login credentials"""
        return self.client.make_request("credentials", verify=False)

    def get_pending_requests(self):
        return self.client.make_request("getpendingrequests")

    def get_notifications(self):
        return self.client.make_request("getnotifications")

    def get_webui_context(self):
        return self.client.make_request("getwebuicontext")
