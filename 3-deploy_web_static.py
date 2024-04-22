#!/usr/bin/python3
"""
This fabric script distributes an archive to web servers
"""
import os
from fabric.api import *
from datetime import datetime


# webservers IP addresses: [web-01, web-02]
env.hosts = ['100.25.24.173', '54.237.54.104']
env.user = "ubuntu"


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    # obtain the current date and time
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # Construct path where archive will be saved
    archive_path = f"versions/web_static_{now}.tgz"

    # use fabric function to create directory if it doesn't exist
    local("mkdir -p versions")

    # Use tar command to create a compresses archive
    archived = local("tar -cvzf {} web_static".format(archive_path))

    # Check archive Creation Status
    if archived.return_code != 0:
        return None
    else:
        return archive_path


def do_deploy(archive_path):
    '''use os module to check for valid file path'''

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
        run(f" mkdir -p {new_release_path}")

        # extract the files
        run(f" tar -xzf {tmp_path} -C {new_release_path}")

        # remove compressed file
        run(f" rm {tmp_path}")

        # move new release files to the correct directory
        run(f" mv -f {new_release_path}web_static/* {new_release_path}")

        # remove old directory
        run(f" rm -rf {new_release_path}web_static")

        # create my_index.html
        html = '''<html>
        <head></head>
        <body><p>Holberton School</p></body>
        </html>'''
        run(f"echo '{html}' > {new_release_path}my_index.html")

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

    # return false if archive path is incorrect or value of do_deploy
    if archive_path is None:
        return False
    # return the value od do_deploy
    return do_deploy(archive_path)
