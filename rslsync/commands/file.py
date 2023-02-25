from __future__ import annotations

from rslsync import RslClient


class FileCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def add(self, file_path, expire_days):
        job_id = self.client.make_request("addmasterjob")["id"]
        self.client.make_request("addpathtojob", path=file_path, id=job_id)
        self.client.make_request("commitmasterjob", id=job_id)
        self.client.make_request("setjobttl", id=job_id, ttl=expire_days * 3600 * 24)
        return job_id

    def get_link(self, share_id):
        return self.client.make_request("createjoblink", id=share_id)

    def remove(self, share_id):
        return self.client.make_request("removejob", id=share_id)

    def list(self):
        return self.client.make_request("getsyncjobs")

    def get_preferences(self, job_id):
        return self.client.make_request("jobpref", id=job_id)

    def set_preferences(self, job_id, preferences):
        return self.client.make_request("setjobpref", id=job_id, **preferences)

    def get_known_hosts(self, job_id):
        return self.client.make_request("knownhosts", id=job_id, isfolder=False)

    def set_known_hosts(self, job_id, known_hosts: list):
        return self.client.make_request("setknownhosts", id=job_id, isfolder=False, hosts=",".join(known_hosts))

    def get_settings(self):
        return self.client.make_request("filejobpath")
