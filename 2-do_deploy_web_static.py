#!/usr/bin/python3
"""
Script based on the file 1-pack_web_static.py that distribute archive to
webserver
"""
import os.path
from fabric.api import *
from fabric.operations import run, put
from datetime import datetime


env.hosts = ['3.227.217.150', '3.95.27.202']
env.user = "ubuntu"


def do_pack():
    """ generate a .tgz archive from content of the web_static
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # creatse folder version if it doesn’t exist
    local("mkdir -p versions")

    # extract the contents of a tar archive
    result = local("tar -czvf versions/web_static_{}.tgz web_static"
                   .format(now))
    if result.failed:
        return None
    else:
        return result


def do_deploy(archive_path):
    """distribute an archive to your web server
    """
    if not os.path.exists(archive_path):
        return False
    # Uncompress the archive to the folder,
    # /data/web_static/release/<archive filenames without extension>
    # on the web server
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False

    try:
        # uploade the archives to /tmp/ directory of  web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Creates new directory for releases
        run("mkdir -p {}".format(folder_path))

        # Untar archives
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))

        # Deletes the archives from  web server
        run("rm -rf /tmp/{}".format(file_name))

        # Moves extraction  propere directorys
        run("mv {}web_static/* {}".format(folder_path, folder_path))

        # Deletes first copy of extraction after moves
        run("rm -rf {}web_static".format(folder_path))

        # Delete the symbolice linke /data/web_static/current from web server
        run("rm -rf /data/web_static/current")

        # Creates new the symbolic linke /data/web_static/current  web server,
        # linkeds  the new version of your code,
        # (/data/web_static/releases/<archive filename without extension>
        run("ln -s {} /data/web_static/current".format(folder_path))

        print('New version deployed!')
        success = True

    except Exception:
        success = False
        print("Could not deploy")
    return success
