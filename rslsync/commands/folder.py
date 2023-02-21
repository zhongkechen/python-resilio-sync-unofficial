from __future__ import annotations

from rslsync import RslClient


class FolderCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def list_folders(self, discovery=1):
        return self.client.make_request("getsyncfolders", discovery=discovery)["folders"]

    def set_folder_preferences(self, name, secret, preferences):
        return self.client.make_request("setfolderpref", name=name, secret=secret, **preferences)

    def get_folder_preferences(self, folder_id):
        return self.client.make_request("folderpref", id=folder_id)["value"]

    def get_known_hosts(self, folder_id):
        return self.client.make_request("knownhosts", id=folder_id, isfolder=True)

    def set_known_hosts(self, folder_id, known_hosts: list):
        return self.client.make_request("setknownhosts", id=folder_id, isfolder=True, hosts=",".join(known_hosts))

    def list_files(self, folder_id, path=""):
        return self.client.make_request("getfileslist", folderid=folder_id, path=path)

    def remove_folder(self, folder_id, delete_dir=False, from_all_devices=False):
        return self.client.make_request("removefolder",
                                        folderid=folder_id,
                                        deletedirectory=delete_dir,
                                        fromalldevices=from_all_devices)

    def add_folder(self, path, secret, selectivesync=False):
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        secret=secret,
                                        selectivesync=selectivesync)

    def generate_secret(self):
        return self.client.make_request("secret")["value"]

    def check_secret(self, secret):
        return self.client.make_request("secret", secret=secret)["value"]

    def get_sync_link(self, folder_name, folder_id, readonly=True, expire_days=3, clicklimit=0, ask_approval=True):
        return self.client.make_request("getsynclink",
                                        name=folder_name,
                                        folderid=folder_id,
                                        permissions=2 if readonly else 1,
                                        timelimit=expire_days*24*3600,
                                        type="copy",
                                        linktype="https",
                                        clicklimit=clicklimit,
                                        askapproval=1 if ask_approval else 0)["value"]

    def rescan(self, folder_id):
        return self.client.make_request("rescanfolder", id=folder_id)
