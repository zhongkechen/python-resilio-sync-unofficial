A Python client of unofficial Resilio Sync API.

## Usage

```

$ from rslsync import RslClient
$ c = RslClient("http://localhost:8888/", "user", "pass")
$ c.folder.list_shared_folders()  # list all shared folders
$ c.file.list_shared_files()  # list all shared files
$ share_id = c.file.share_file(path, days)   # share a single file
$ c.file.create_link(share_id)   # create a share link
$ c.file.unshare_file(share_id)   # unshare a file

```
