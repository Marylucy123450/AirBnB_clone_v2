#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers and
performs deployment"""

from fabric.api import env, put, run
import os

# Define the hosts and user for Fabric
env.hosts = ['35.153.193.23', '54.146.94.67']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/alxse'


def do_deploy(archive_path):
    """Distributes an archive to your web servers and performs deployment"""

    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.split('.')[0]
        release_folder = '/data/web_static/releases/'
        full_path = release_folder + folder_name

        run('mkdir -p {}'.format(full_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, full_path))
        run('rm /tmp/{}'.format(archive_filename))
        run('mv {}/web_static/* {}'.format(full_path, full_path))
        run('rm -rf {}/web_static'.format(full_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(full_path))

        return True
    except Exception as e:
        print(e)
        return False
