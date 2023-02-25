import json

from rslsync import RslClient


class StatCommands:
    def __init__(self, client: RslClient):
        self.client = client

    def get_session_stats(self):
        return self.client.make_request("getsessionstats")

    def get_performance_warnings(self):
        return self.client.make_request("getperformancewarnings")

    def get_peers_stat(self):
        return self.client.make_request("getpeersstat")

    def get_chart_data(self, type: int, from_ts, to_ts):
        assert int(type) in [1, 2]
        params = {"type": type, "from": from_ts, "to": to_ts}
        return self.client.make_request("getchartdata", **params)

    def send_stat(self, event_name, event_action, extra=None):
        if extra:
            if isinstance(extra, str):
                extra = json.loads(extra)
            return self.client.make_request("sendstat", eventname=event_name, eventaction=event_action, extra=extra)
        else:
            return self.client.make_request("sendstat", eventname=event_name, eventaction=event_action)

    def get_statuses(self):
        return self.client.make_request("getstatuses")
