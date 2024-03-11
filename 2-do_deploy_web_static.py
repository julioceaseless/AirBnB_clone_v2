#!/usr/bin/python3
"""
This fabfile distributes an archive to my web servers
"""
import os
from fabric.api import *
from datetime import datetime


# Set the host IP addresses for web-01 and web-02
env.hosts = ['100.25.24.173', '54.237.54.104']
env.user = "ubuntu"


def do_pack():
    """ Create a .tgz archive from the contents of webstatic folder"""

    # get time now
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # create a archive path
    archive_path = f"versions/web_static_{now}.tgz"

    # create directory to store all the archive files
    local("mkdir -p versions")

    # create an archive
    archive = local(f"tar -cvzf {archive_path} web_static")

    # return the archive path if successfully or none
    return archive_path


def do_deploy(archive_path):
    """ upload the archives to the webservers"""

    # execute this block if archive exists
    if os.path.exists(archive_path):
        # extract archive.tgz name
        archive = archive_path.split('/')[1]

        # create a temporary folder
        tmp_apath = f"/tmp/{archive}"
        folder = archive.split('.')[0]
        f_path = f"/data/web_static/releases/{folder}/"

        # upload archive to /tmp/archive in the server(s)
        put(archive_path, tmp_apath)

        # make directory for keeping extracted files
        run(f"mkdir -p {f_path}")

        # uncompress the tar ball
        run(f"tar -xzf {tmp_apath} -C {f_path}")

        # remove archived file
        run(f"rm {tmp_apath}")

        # move extracted files
        run(f"mv -f {f_path}web_static/* {f_path}")
        run(f"rm -rf {f_path}web_static")

        current_link = "/data/web_static/current"

        # delete old symbolic link from server
        run(f"rm -f {current_link}")

        # create new symbolic link
        run(f"ln -s {f_path} {current_link}")

        return True
    return False
