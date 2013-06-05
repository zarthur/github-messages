#!/usr/bin/env python3

"""Create 24 character message on the GitHub contributions chart"""

import os
import shutil
import sys

import yaml

import fontify


SSH_CONFIG_TEMPLATE = """Host GitHub
  HostName github.com
  User {username}
  IdentityFile {key_path}
"""


class GithubCommit:
    """Make necessary commits to a github repository to display message"""
    def __init__(self, config_path):
        """Load conifguration, set some environment variables, and create the
        necessary ssh config file
        """
        with open(config_path) as config_file:
            [setattr(self, k, v) for k, v in yaml.load(config_file).items()]

        self._ssh_config_path = os.path.join(self.ssh_path, 'config')
        self._ssh_config_existed = os.path.exists(self._ssh_config_path)

        if self._ssh_config_existed:
            self._ssh_config_backup = os.path.join(self.ssh_path, '_config.bak')
            shutil.move(self._ssh_conifg_path, self._ssh_config_backup)

        ssh_config = SSH_CONFIG_TEMPLATE.format(username=self.username,
                                                key_path=self.ssh_key_path)

        with open(self._ssh_config_path, 'w') as config_file:
            config_file.write(ssh_config)

        os.environ['GIT_COMMITTER_NAME'] = self.username
        os.environ['GIT_AUTHOR_NAME'] = self.username
        os.environ['GIT_COMMITTER_EMAIL'] = self.email
        os.environ['GIT_AUTHOR_EMAIL'] = self.email

    def cleanup(self):
        """Restore the original ssh config if it existed, delete otherwise"""
        if self._ssh_config_existed:
            shutil.move(self._ssh_conifg_backup, self._ssh_config_path)
        else:
            shutil.delete(self._ssh_config_path)
