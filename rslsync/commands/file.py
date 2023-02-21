from __future__ import annotations

from rslsync import RslClient


class FileCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def share_file(self, file_path, expire_days):
        job_id = self.client.make_request("addmasterjob")["value"]["id"]
        self.client.make_request("addpathtojob", path=file_path, id=job_id)
        self.client.make_request("commitmasterjob", id=job_id)
        self.client.make_request("setjobttl", id=job_id, ttl=expire_days * 3600 * 24)
        return job_id

    def create_link(self, share_id):
        return self.client.make_request("createjoblink", id=share_id)["value"]["link"]

    def unshare_file(self, share_id):
        self.client.make_request("removejob", id=share_id)

    def list_shared_files(self):
        return self.client.make_request("getsyncjobs")["value"]["jobs"]
