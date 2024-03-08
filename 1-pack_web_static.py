#!/usr/bin/python3
""" script generates a .tgz archive from the contents of webstatic
folder for AirBnB Clone"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Create a .tgz archive from the contents of webstatic folder"""

    # get time now
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # create a archive path
    archive_path = f"versions/web_static_{now}.tgz"

    # create directory to store all the archive files
    local("mkdir -p versions")

    # create an archive
    tar_ball = local(f"tar -cvzf {archive_path} web_static")

    # return the archive path if successfully or none
    return archive_path
