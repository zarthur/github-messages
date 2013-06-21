#!/usr/bin/env python3

"""Create 24 character message on the GitHub contributions chart"""

import datetime
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

TIME_FMT = "%a %b %d %H:%M:%S %Y {utc_offset}"


def next_weekday(d, weekday):
    """Get date of first specified weekday after specified date
    Source: http://stackoverflow.com/questions/6558535/
            python-find-the-date-for-the-first-monday-after-a-given-a-date
    """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class GithubCommit():
    """Make necessary commits to a github repository to display message"""
    def __init__(self, config_path):
        """Load conifguration, set some environment variables, and create the
        necessary ssh config file
        """
        with open(config_path) as config_file:
            for k, v in yaml.load(config_file).items():
                setattr(self, k, v)
        self.time_fmt = TIME_FMT.format(utc_offset=self.utc_offset)
        self.repo_dir = os.path.join(self.clone_base_path, self.repo_name)

        # move/create ssh config file
        self._ssh_config_path = os.path.join(self.ssh_path, 'config')
        self._ssh_config_existed = os.path.exists(self._ssh_config_path)

        if self._ssh_config_existed:
            self._ssh_config_backup = os.path.join(self.ssh_path, '_config.bak')
            shutil.move(self._ssh_conifg_path, self._ssh_config_backup)

        ssh_config = SSH_CONFIG_TEMPLATE.format(username=self.username,
                                                key_path=self.ssh_key_path)

        with open(self._ssh_config_path, 'w') as config_file:
            config_file.write(ssh_config)

        # set necessary environment variables
        os.environ['GIT_COMMITTER_NAME'] = self.username
        os.environ['GIT_AUTHOR_NAME'] = self.username
        os.environ['GIT_COMMITTER_EMAIL'] = self.email
        os.environ['GIT_AUTHOR_EMAIL'] = self.email

    def gen_commits(self, message):
        """Generate commits on appropriate dates based on message"""
        message_array = fontify.convert(message).transpose()
        last_year = datetime.date.today() - datetime.timedelta(weeks=52)
        commit_day = next_weekday(last_year, 6)

        os.chdir(self.repo_dir)

        for week in message_array:
            for day in week:
                if day == 1:
                    date_str = commit_day.strftime(self.time_fmt)
                    with open('data', 'w') as outfile:
                        outfile.write(date_str)

                    os.environ['GIT_AUTHOR_DATE'] = date_str
                    os.environ['GIT_COMMITTER_DATE'] = date_str

                    os.system('git add .')
                    os.system('git commit -m "{date}"'.format(date=date_str))
                commit_day += datetime.timedelta(days=1)

    def push(self):
        """Push commits to GitHub"""
        os.chdir(self.repo_dir)
        os.system('git push')

    def cleanup(self):
        """Restore the original ssh config if it existed, delete otherwise"""
        if self._ssh_config_existed:
            shutil.move(self._ssh_conifg_backup, self._ssh_config_path)
        else:
            shutil.delete(self._ssh_config_path)


if __name__ == '__main__':
    config_path = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    gc = GithubCommit(config_path)
    gc.gen_commits(message)
    gc.push()
    gc.cleanup()
