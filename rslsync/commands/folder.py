from __future__ import annotations

from rslsync import RslClient


class FolderCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def list(self, discovery=True):
        return self.client.make_request("getsyncfolders", discovery=1 if discovery else 0)

    def get_settings(self):
        return self.client.make_request("getfoldersettings", verify=False)

    def set_preferences(self, name, secret, preferences):
        return self.client.make_request("setfolderpref", name=name, secret=secret, **preferences)

    def get_preferences(self, folder_id):
        return self.client.make_request("folderpref", id=folder_id)

    def get_known_hosts(self, folder_id):
        return self.client.make_request("knownhosts", id=folder_id, isfolder=True)

    def set_known_hosts(self, folder_id, known_hosts: list):
        return self.client.make_request("setknownhosts", id=folder_id, isfolder=True, hosts=",".join(known_hosts))

    def get_files(self, folder_id, path=""):
        return self.client.make_request("getfileslist", folderid=folder_id, path=path)

    def select_file(self, folder_id, path, selected=True, remove_from_all=False):
        return self.client.make_request("setfilemode",
                                        folderid=folder_id,
                                        path=path,
                                        selected=selected,
                                        removefromall=remove_from_all)

    def remove(self, folder_id, delete_dir=False, from_all_devices=False):
        return self.client.make_request("removefolder",
                                        folderid=folder_id,
                                        deletedirectory=delete_dir,
                                        fromalldevices=from_all_devices)

    def add(self, path, secret="", selectivesync=False, encrypted=False):
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        secret=secret,
                                        encrypted=encrypted,
                                        selectivesync=selectivesync)

    def add_advanced(self, path, selectivesync=False):
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        selectivesync=selectivesync)

    def add_local(self, origin_folder_id, path, readonly=True, selective_sync=False):
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        origin_id=origin_folder_id,
                                        permission=2 if readonly else 1,
                                        selectivesync=selective_sync
                                        )

    def generate_secret(self):
        return self.client.make_request("secret")

    def check_secret(self, secret):
        return self.client.make_request("secret", secret=secret)

    def get_link(self, folder_name, folder_id, permission: int, expire_days=3, clicklimit=0, ask_approval=True):
        assert int(permission) in [1, 2, 4]  # read-write, read-only, owner
        return self.client.make_request("getsynclink",
                                        name=folder_name,
                                        folderid=folder_id,
                                        permissions=permission,
                                        timelimit=expire_days*24*3600,
                                        type="copy",
                                        linktype="https",
                                        clicklimit=clicklimit,
                                        askapproval=1 if ask_approval else 0)

    def rescan(self, folder_id):
        return self.client.make_request("rescanfolder", id=folder_id)

    def set_selective_sync(self, folder_id, selective_sync, clear_folder_contents=False):
        if selective_sync:
            return self.client.make_request("setselectivesync",
                                            folderid=folder_id,
                                            selectivesync=selective_sync,
                                            clearfoldercontents=clear_folder_contents)
        else:
            return self.client.make_request("setselectivesync",
                                            folderid=folder_id,
                                            selectivesync=selective_sync)
