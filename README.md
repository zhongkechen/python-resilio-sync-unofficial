A Python client of unofficial Resilio Sync API.

== Usage ==

```

$ from rslsync import RslClient
$ c = RslClient("http://localhost:8888/", "user", "pass")
$ c.get_shared_folders()  # list all shared folders
$ c.get_shared_files()  # list all shared files
$ share_id = c.share_file(path, days)   # share a single file
$ c.create_link_for_shared_file(share_id)   # create a share link
$ c.unshare_file(share_id)   # unshare a file

```
