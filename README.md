A Python client of unofficial Resilio Sync API.

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
rsl --help

```

As a library
```
$ from rslsync import RslClient
$ c = RslClient("http://localhost:8888/", "user", "pass")

# general commands
$ c.general.get_settings()     # get all settings

# folder commands
$ c.folder.list_shared_folders()  # list all shared folders

# file commands
$ c.file.list_shared_files()  # list all shared files
$ share_id = c.file.share_file(path, days)   # share a single file
$ c.file.create_link(share_id)   # create a share link
$ c.file.unshare_file(share_id)   # unshare a file

```
