#!/usr/bin/python3
"""
script (based on the file 2-do_deploy_web_static.py) that create and
distribute archive  web servers
"""
import os.path
from fabric.api import *
from fabric.operations import run, put
from datetime import datetime


env.hosts = ['18.204.13.241', '52.91.153.108']
env.user = "ubuntu"


def deploy():
    """creates and distributes an archive to your web servers
    """
    # Call the do_pack() functions and store the path of the create archive
    archive_path = do_pack()
    if archive_path is None:
        print("Failed to create archive from web_static")
        return False

    # Call do_deploy functions, using the new path of the new archives
    # return the returns values of do_deploy
    return do_deploy(archive_path)


def do_pack():
    """ generates a .tgz archive from the contents of the web_static    
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        # extract the content of tar archives
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False
    # Uncompress the archive the folder,
    # /data/web_static/release/<archive filenames without extension>
    # on  web server
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False

    try:
        # upload the archives to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))

        # Creates new directory for releases
        run("mkdir -p {}".format(folder_path))

        # Untar archives
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))

        # Deletes the archives from the web server
        run("rm -rf /tmp/{}".format(file_name))

        # Moves extractions to propers directory
        run("mv {}web_static/* {}".format(folder_path, folder_path))

        # Deletes first copy  extraction after move
        run("rm -rf {}web_static".format(folder_path))

        # Deletes the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Creates new the symbolic link /data/web_static/current on web server,
        # linkede to new versions of your code,
        # (/data/web_static/release/<archive filename without extensions>
        run("ln -s {} /data/web_static/current".format(folder_path))

        print('New version deployed!')
        success = True

    except Exception:
        success = False
        print("Could not deploy")
    return success
