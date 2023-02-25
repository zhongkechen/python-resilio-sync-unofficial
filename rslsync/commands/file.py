from __future__ import annotations

import json

from rslsync import RslClient


class FileCommands:
    """Commands to control shared files"""

    def __init__(self, client: RslClient):
        self.client = client

    def add(self, file_path, expire_days):
        """Create a share job"""
        job_id = self.client.make_request("addmasterjob")["id"]
        self.client.make_request("addpathtojob", path=file_path, id=job_id)
        self.client.make_request("commitmasterjob", id=job_id)
        self.client.make_request("setjobttl", id=job_id, ttl=expire_days * 3600 * 24)
        return job_id

    def get_link(self, job_id):
        """Get a link for a share job"""
        return self.client.make_request("createjoblink", id=job_id)

    def remove(self, job_id):
        """Remove a share job"""
        return self.client.make_request("removejob", id=job_id)

    def list(self):
        """List all share job"""
        return self.client.make_request("getsyncjobs")

    def get_preferences(self, job_id):
        """Get preferences for a share job"""
        return self.client.make_request("jobpref", id=job_id)

    def set_preferences(self, job_id, preferences):
        """Set preferences for a shre job"""
        if isinstance(preferences, str):
            preferences = json.loads(preferences)
        return self.client.make_request("setjobpref", id=job_id, **preferences)

    def get_known_hosts(self, job_id):
        """Get known hosts for a share job"""
        return self.client.make_request("knownhosts", id=job_id, isfolder=False)

    def set_known_hosts(self, job_id, known_hosts: list):
        """Set known hosts for a share job"""
        return self.client.make_request("setknownhosts", id=job_id, isfolder=False, hosts=",".join(known_hosts))

    def get_default_path(self):
        """Get default path for share jobs"""
        return self.client.make_request("filejobpath")
