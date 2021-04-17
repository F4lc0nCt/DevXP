
import os
import sys
import subprocess
import datetime
import developer


class GitManager:

    GIT_LOG_CMD = 'git --git-dir={0}' + os.path.sep + '.git  --work-tree={0} log {1}'
    AUTHOR_FORMAT = '"--pretty=%an;%ae"'
    AUTHOR_DATE = '--author="{0}" --pretty="%aI"'

    def __init__(self, git_path):
        self.git_path = git_path
        self.max_number_of_authors = sys.maxsize
        self.author_dict = dict()
        self.first_commit_repo = datetime.date.max

    def build_author_dict(self):
        self.retrieve_author()
        self.retrieve_commit_date()

    def retrieve_author(self):
        git_cmd = GitManager.GIT_LOG_CMD.format(self.git_path, GitManager.AUTHOR_FORMAT)
        output = subprocess.check_output(git_cmd, shell=True).decode("utf-8")
        idx = 0
        for line in set(str(output).split('\n')):
            if idx > self.max_number_of_authors:
                break
            idx += 1
            data = line.split(';')
            if len(data) != 2:
                continue
            dev = developer.Developer(data[0], data[1])
            self.author_dict[dev.hash_id] = dev

    def retrieve_commit_date(self):
        git_cmd = GitManager.GIT_LOG_CMD.format(self.git_path, GitManager.AUTHOR_DATE)
        for dev in self.author_dict.values():
            commit_dates = subprocess.check_output(git_cmd.format(dev.name),
                                                   shell=True).decode("utf-8")
            if commit_dates == '':
                continue
            dates_list = commit_dates.split('\n')
            first_date = dates_list[0]
            last_date = dates_list[-2] if dates_list[-1] == '' else dates_list[-1]
            dev.set_first_commit_date(first_date)
            dev.set_last_commit_date(last_date)
            self.update_first_commit_date(dev.first_commit_date)

    def update_first_commit_date(self, date):
        if date < self.first_commit_repo:
            self.first_commit_repo = date
