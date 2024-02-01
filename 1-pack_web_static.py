#!/usr/bin/python3
"""script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """ generates a .tgz archive from the contents of the web_static
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # creates folder version if it doesn’t exist
    local("mkdir -p versions")

    # extract the content of  tar archive
    result = local("tar -czvf versions/web_static_{}.tgz web_static"
                   .format(now))
    if result.failed:
        return None
    else:
        return result

if __name__ == "__main__":
    do_pack()
