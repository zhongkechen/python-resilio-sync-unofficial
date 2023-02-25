from __future__ import annotations

from rslsync import RslClient


class FolderCommands:
    """Commands to control shared folders"""

    def __init__(self, client: RslClient):
        self.client = client

    def list(self, discovery=True):
        """List all shared folders"""
        return self.client.make_request("getsyncfolders", discovery=1 if discovery else 0)

    def get_settings(self):
        """Get folder settings"""
        return self.client.make_request("getfoldersettings", verify=False)

    def set_preferences(self, name, secret, preferences):
        """Set preferences for a shared folder"""
        return self.client.make_request("setfolderpref", name=name, secret=secret, **preferences)

    def get_preferences(self, folder_id):
        """Get preferences for a shared folder"""
        return self.client.make_request("folderpref", id=folder_id)

    def get_known_hosts(self, folder_id):
        """Get known hosts for a shared folder"""
        return self.client.make_request("knownhosts", id=folder_id, isfolder=True)

    def set_known_hosts(self, folder_id, known_hosts: list):
        """Set known hosts for a shared folder"""
        return self.client.make_request("setknownhosts", id=folder_id, isfolder=True, hosts=",".join(known_hosts))

    def get_files(self, folder_id, path=""):
        """Get a list of files for a shared folder"""
        return self.client.make_request("getfileslist", folderid=folder_id, path=path)

    def select_file(self, folder_id, path, selected=True, remove_from_all=False):
        """Select or deselect a file to sync for a shared folder"""
        return self.client.make_request("setfilemode",
                                        folderid=folder_id,
                                        path=path,
                                        selected=selected,
                                        removefromall=remove_from_all)

    def remove(self, folder_id, delete_dir=False, from_all_devices=False):
        """Delete a shared folder"""
        return self.client.make_request("removefolder",
                                        folderid=folder_id,
                                        deletedirectory=delete_dir,
                                        fromalldevices=from_all_devices)

    def add(self, path, secret="", selectivesync=False, encrypted=False):
        """Create a shared folder"""
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        secret=secret,
                                        encrypted=encrypted,
                                        selectivesync=selectivesync)

    def add_advanced(self, path, selectivesync=False):
        """Create a shared folder with advanced permission control"""
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        selectivesync=selectivesync)

    def add_local(self, origin_folder_id, path, readonly=True, selective_sync=False):
        """Create a local shared folder"""
        return self.client.make_request("addsyncfolder",
                                        path=path,
                                        origin_id=origin_folder_id,
                                        permission=2 if readonly else 1,
                                        selectivesync=selective_sync
                                        )

    def generate_secret(self):
        """Generate a folder share secret"""
        return self.client.make_request("secret")

    def check_secret(self, secret):
        """Validate a secret"""
        return self.client.make_request("secret", secret=secret)

    def get_link(self, folder_name, folder_id, permission: int, expire_days=3, clicklimit=0, ask_approval=True):
        """Get a link for a shared folder"""
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
        """Rescan local files in a shared folder"""
        return self.client.make_request("rescanfolder", id=folder_id)

    def set_selective_sync(self, folder_id, selective_sync, clear_folder_contents=False):
        """Switch on/off the selective sync flag for a shared folder"""
        if selective_sync:
            return self.client.make_request("setselectivesync",
                                            folderid=folder_id,
                                            selectivesync=selective_sync,
                                            clearfoldercontents=clear_folder_contents)
        else:
            return self.client.make_request("setselectivesync",
                                            folderid=folder_id,
                                            selectivesync=selective_sync)

    def get_default_path(self):
        """Get the default path for shared folders"""
        return self.client.make_request("getfoldersstoragepath")