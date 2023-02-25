A Python client library and CLI of unofficial Resilio Sync (BTSync) API. No API Key is needed.

## Installation

Install from pypi

```
pip install rslsync
```

Install from repo
```
pip install .
```

## Usage

As a command line tool
```
$ rsl --help
$ rsl general get-settings
$ rsl folder list

```

As a library
```
$ from rslsync import RslClient
$ c = RslClient("http://localhost:8888/", "user", "pass")

# general commands
$ c.general.get_settings()     # get all settings

# folder commands
$ c.folder.list()  # list all shared folders

# file commands
$ c.file.list()  # list all shared files
$ share_id = c.file.share(path, days)   # share a single file
$ c.file.get_link(share_id)   # create a share link
$ c.file.unshare(share_id)   # unshare a file

# stat commands
$ c.stat.get_peers_stat()  # get the stats of peers

# fs (file system) commands
# c.fs.get_attr("/")
```

## Related Projects

 * https://github.com/kevinjqiu/btsync.py
 * https://github.com/dlawregiets/btsync_status
 * https://github.com/ywrac/btsync-api-python
 * https://github.com/jminardi/python-btsync
 * https://github.com/icy/btsync
 * https://github.com/PythonNut/resilio-sync-cli
 * https://github.com/lxiange/ResilioSync-py
 