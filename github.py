#!/usr/bin/env python3

"""Create 24 character message on the GitHub contributions chart"""

import datetime
import dateutil.relativedelta
import os
import sys

import yaml

import fontify


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
        """Load conifguration and set some environment variables"""
        with open(config_path) as config_file:
            for k, v in yaml.load(config_file).items():
                setattr(self, k, v)
        self.time_fmt = TIME_FMT.format(utc_offset=self.utc_offset)
        self.repo_dir = os.path.join(self.clone_base_path, self.repo_name)

        os.environ['GIT_COMMITTER_NAME'] = self.username
        os.environ['GIT_AUTHOR_NAME'] = self.username
        os.environ['GIT_COMMITTER_EMAIL'] = self.email
        os.environ['GIT_AUTHOR_EMAIL'] = self.email

    def gen_commits(self, message):
        """Generate commits on appropriate dates based on message"""
        message_array = fontify.convert(message).transpose()
        last_year = datetime.datetime.now() - \
                    dateutil.relativedelta.relativedelta(years=1)
        commit_day = next_weekday(last_year, 6)

        if not os.path.exists(self.repo_dir):
            os.chdir(os.path.join(os.path.split(self.repo_dir)[:-1])[0])
            print(self.repository_uri)
            os.system('git clone {repo}'.format(repo=self.repository_uri))

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
        os.system('git push origin master -v')


if __name__ == '__main__':
    config_path = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    gc = GithubCommit(config_path)
    gc.gen_commits(message)
    gc.push()
