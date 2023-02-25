from rslsync import RslClient


class FsCommands:
    """Commands to manipulate the file system on the server side"""

    def __init__(self, client: RslClient):
        self.client = client

    def get_attr(self, path):
        """Get attributes of the path"""
        return self.client.make_request("getattr", path=path, verify=False)

    def get_dir(self, path):
        """Get contents of the directory"""
        return self.client.make_request("getdir", path=path, verify=False)

    def add_dir(self, path):
        """create a directory"""
        return self.client.make_request("adddir", path=path, verify=False)

