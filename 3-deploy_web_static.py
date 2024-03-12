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
    tar_ball = local(f"tar -cvzf {archive_path} web_static")

    # return the archive path if successfully or none
    return archive_path


def do_deploy(archive_path):
    """ upload the archives to the webservers"""

    if os.path.exists(archive_path):
        # retrieve archive name
        archive_name = archive_path.split('/')[1]

        # create pathname for temporary storage of archive
        tmp_path = f"/tmp/{archive_name}"

        # create a dir name using archive_name without extension
        directory = archive_name.split('.')[0]
        new_release_path = f"/data/web_static/releases/{directory}/"

        # push archive to remote directory
        put(archive_path, tmp_path)

        # create directory for storing the uncompressed files
        run(f"mkdir -p {new_release_path}")

        # extract the files
        run(f"tar -xzf {tmp_path} -C {new_release_path}")

        # remove zipped file
        run(f"rm {tmp_path}")

        # move new release to the correct directory
        run(f"mv {new_release_path}web_static/* {new_release_path}")

        # remove old directory
        run(f"rm -rf {new_release_path}web_static")

        # delet old symlink
        run("rm -rf /data/web_static/current")

        # create new symlink
        run(f"ln -s {new_release_path} /data/web_static/current")
        return True
    return False


def deploy():
    """
    Create and distribute archives to web servers
    """

    # get the archive path
    archive_path = do_pack()
    print(archive_path)

    # return false if archive path is incorrect or value of do_deploy
    if archive_path is None:
        return False
    # return the value od do_deploy
    return do_deploy(archive_path)
