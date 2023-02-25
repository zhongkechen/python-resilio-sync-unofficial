from rslsync import RslClient


class FsCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def get_attr(self, path):
        return self.client.make_request("getattr", path=path, verify=False)

    def get_dir(self, path):
        return self.client.make_request("getdir", path=path, verify=False)

    def add_dir(self, path):
        return self.client.make_request("adddir", path=path, verify=False)

    def get_folder_storage_path(self):
        return self.client.make_request("getfoldersstoragepath")
