#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
 web_static folder"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""

    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate the name of the archive
    now = datetime.now()
    archive_name = "web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    # Create the .tgz archive
    # tar: The command-line utility used to manipulate archives.
    # -cvzf: The options used with tar:
    # -c: Create a new archive.
    # -v: Verbose mode, which displays the progress of the archiving process.
    # -z: Compress the archive using gzip.
    # -f: Specifies the file name of the archive.
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.failed:
        return None

    # Return the path to the generated archive
    return os.path.join("versions", archive_name)
