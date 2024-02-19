#!/usr/bin/python3
"""
bash script based on file 1-pack_web_static.py that distribut archive to
webserver
"""
import os.path
from fabric.api import *
from fabric.operations import run, put
from datetime import datetime


env.hosts = ['3.227.217.150', '3.95.27.202']
env.user = "ubuntu"


def do_pack():
    """ generates a .tgz archive from the contents of the web_static
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # creates foldere versions if it doesn’t exist
    local("mkdir -p versions")

    # extract the contents of a tar archive
    result = local("tar -czvf versions/web_static_{}.tgz web_static"
                   .format(now))
    if result.failed:
        return None
    else:
        return result


def do_deploy(archive_path):
    """distributes an archive to your web server
    """
    if not os.path.exists(archive_path):
        return False
    # Uncompress the archives to the folder,
    # /data/web_statics/releases/<archive filename without extension>
    # on the web servers
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False

    try:
        # uploade the archives to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Creates new directory for release
        run("mkdir -p {}".format(folder_path))

        # Untare archives
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))

        # Deletes the archives from the web server
        run("rm -rf /tmp/{}".format(file_name))

        # Moves extractions to propers directory
        run("mv {}web_static/* {}".format(folder_path, folder_path))

        # Deletes first copy xtraction aftere move
        run("rm -rf {}web_static".format(folder_path))

        # Deletse the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Creates new the symbolic links /data/web_static/current on web server,
        # linked to the new versions of your code,
        # (/data/web_static/releases/<archive filename without extension>
        run("ln -s {} /data/web_static/current".format(folder_path))

        print('New version deployed!')
        success = True

    except Exception:
        success = False
        print("Could not deploy")
    return success
